#!/usr/bin/env python3

"""
jenkins_all will hold all methods that can operate jenkins jobs
1. pull job from jenkins and convert to yaml file to docker download folder
2. push yaml file to jenkins from docker upload folder
Usage:
    jenkins_all (--url=<jenkins-url>)
        (--user=<jenkins-user>)
        (--password=<jenkins-password>)
        (--push <jobs>|--pull <jobs>|--list|--sync <jobs>|--sync-all|--push-all|--test)
    jenkins_all (-h | --help)
Options:
    -h, --help                                     Print this screen and exit.
    --url=<jenkins-url>                            Jenkins url like http://localhost:8080/.
    --user=<jenkins-user>                          Jenkins user who has remote auth to connect Jenkins.
    --password=<jenkins-password>                  Jenkins user password, which may be your api token.
    --push                                         Upload file, use --push job, abc.yaml in docker ./upload will be upload to jenkins.
    --pull                                         Download file, use --pull job from jenkins to docker ./download folder, job.yaml.
    --sync                                         Used by jenkins-sync-job to sync jobs between prod jenkins and github repo.
    --sync-all                                     Used by jenkins-sync-all job to sync jenkins job to github repo
    --push-all                                     Upload all files in docker upload folder
    --list                                         List jobs prefix with `data`
"""

import json
import os
import subprocess

import yaml
import ruamel.yaml
import xmltodict

from docopt_dispatch import dispatch


class JenkinsJobs:
    """
    JenkinsJobs defines all operation that fetch or submit jobs between jenkins and caller
    """

    def __init__(self, jenkins_url, jenkins_user, jenkins_password, work_dir):
        self.jenkins_url = jenkins_url
        self.jenkins_user = jenkins_user
        self.jenkins_password = jenkins_password
        self.work_dir = work_dir
        self.jenkins_cli = f"java -jar jenkins-cli.jar -s {self.jenkins_url} " \
                           f"-remoting -auth {self.jenkins_user}:{self.jenkins_password}"

    def list_online_jobs(self):
        """
        List all jenkins job based on data jobs regex rule
        :return: set of all jenkins jobs
        """
        online_jobs = subprocess.check_output(f"{self.jenkins_cli} list-jobs| egrep '^data(eng)?_.*$'",
                                              encoding='UTF-8',
                                              shell=True)

        return {job for job in online_jobs.split('\n') if job}

    def pull_job(self, job):
        """
        Pull one job from jenkins to docker download folder
        :param job: job that need to fetch from jenkins
        """
        ryaml = ruamel.yaml.YAML()
        ryaml.explicit_start = True

        xml_file = os.path.join(self.work_dir, "download", job)
        final_file = os.path.join(self.work_dir, "download", f"{job}.yaml")
        fetch_command = f"{self.jenkins_cli} get-job {job} > {xml_file}"

        print(f"Will fetch {job} from {self.jenkins_url} to {final_file}")
        print(f"Running: {fetch_command}")
        subprocess.call(fetch_command, shell=True)

        with open(xml_file) as stream:
            xml_doc = xmltodict.parse(stream.read())

        doc_json = json.dumps(xml_doc, indent=4)

        with open(xml_file, 'w') as output:
            data = json.loads(str(doc_json), object_pairs_hook=ruamel.yaml.comments.CommentedMap)
            ruamel.yaml.scalarstring.walk_tree(data)

            ruamel.yaml.round_trip_dump(data, output)

        os.rename(xml_file, final_file)

    def push_job(self, job, update=False):
        """
        Push one job from docker upload folder to jenkins
        :param job: job that to be push
        :param update: If true just update job, else create a job
        :return: nothing
        """
        xml_file = os.path.join(self.work_dir, "upload", f"{job}.xml")
        yml_file = os.path.join(self.work_dir, "upload", f"{job}.yaml")

        if not os.path.isfile(yml_file):
            raise Exception(f"{yml_file} not found")

        print(f"Will convert {yml_file} to {xml_file} and submit to {self.jenkins_url}")

        with open(yml_file, 'r') as stream:
            doc_yml = yaml.load(stream)

        with open(xml_file, 'w') as output:
            xmltodict.unparse(doc_yml, output=output, pretty=True)

        if update:
            print(f"Running: {self.jenkins_cli} update-job {job} < {xml_file}")
            subprocess.call(f"{self.jenkins_cli} update-job {job} < {xml_file}", shell=True)
        else:
            print(f"Running: {self.jenkins_cli} create-job {job} < {xml_file}")
            subprocess.call(f"{self.jenkins_cli} create-job {job} < {xml_file}", shell=True)

        print(f"removing file {xml_file} from upload folder")
        os.remove(xml_file)

    def pull_jobs(self, jobs_todo):
        """
        Pull multiple jobs from jenkins to docker download folder
        :param jobs_todo: jobs that need to be fetch
        :return: nothing
        """
        all_jobs = self.list_online_jobs()
        exist_jobs = jobs_todo.intersection(all_jobs)

        print(f"jobs did not exists on jenkins: {jobs_todo - exist_jobs}")
        print(f"jobs found: {exist_jobs}")

        for job in exist_jobs:
            self.pull_job(job)

        print(f"finish fetch jobs: {jobs_todo}")

    def push_jobs(self, jobs_todo):
        """
        Push multiple jobs from upload to jenkins
        :param jobs_todo: jobs that need to be submit to jenkins
        :return: nothing
        """
        all_jobs = self.list_online_jobs()
        jobs_to_create = jobs_todo - all_jobs
        jobs_to_update = jobs_todo.intersection(all_jobs)

        for job in jobs_to_create:
            self.push_job(job)

        print(f"finish create jobs: {jobs_to_create}")

        for job in jobs_to_update:
            self.push_job(job, update=True)

        print(f"finish update jobs: {jobs_to_update}")

    def push_all_jobs(self):
        """
        Push all jobs in upload folder
        :return:
        """
        upload_path = os.path.join(self.work_dir, "upload")
        # remove .yaml from file name
        self.push_jobs(
            {[file[:-4] for file in os.listdir(upload_path)]}
        )

    def sync_jobs(self, jobs_todo):
        """
        Should mount github maintained jobs to /usr/src/github
        Will sync jobs between jenkins and schemas/jenkins
        :param jobs_todo: jobs need to sync from jenkins to github repo
        :return: nothing
        """

        def update_github_local(online_job_path, github_job_path):
            if not os.path.isfile(online_job_path):
                return

            should_override = False
            if os.path.isfile(github_job_path):
                with open(online_job_path, 'r') as online_file, open(github_job_path, 'r') as github_file:
                    online_job_yml = yaml.load(online_file)
                    github_job_yml = yaml.load(github_file)
                    # If diff should write to github repo
                    should_override = online_job_yml != github_job_yml
            else:
                # should always write new join running on jenkins but not on github
                should_override = True

            if should_override:
                print(f"should override file {github_job_path} with {online_job_path}")
                with open(online_job_path, 'r') as online_file, open(github_job_path, 'w') as github_file:
                    github_file.write(online_file.read())

        self.pull_jobs(jobs_todo)

        for job in jobs_todo:
            update_github_local(
                os.path.join(self.work_dir, "download", f"{job}.yaml"),
                os.path.join(self.work_dir, "github", f"{job}.yaml")
            )


# Entrance from main
# Dispatch deliver different behavior for different mode(pull|push|sync|test)
@dispatch.on('--test')
def test(**kwargs):
    print(kwargs)


@dispatch.on('--push')
def push_jobs(url, user, password, jobs, **kwargs):
    if not jobs:
        print("jobs not detected")
        exit(1)
    jobs_todo = set(
        map(lambda x: x.strip(), jobs.split(","))
    )

    jenkins = JenkinsJobs(
        jenkins_url=url,
        jenkins_user=user,
        jenkins_password=password,
        work_dir=os.getcwd()
    )

    jenkins.push_jobs(jobs_todo)


# Upload all file on docker upload folder
# Should mount resources/jenkins to docker upload folder
@dispatch.on('--push-all')
def push_all_jobs(url, user, password, **kwargs):
    jenkins = JenkinsJobs(
        jenkins_url=url,
        jenkins_user=user,
        jenkins_password=password,
        work_dir=os.getcwd()
    )

    jenkins.push_all_jobs()


@dispatch.on('--pull')
def pull_jobs(url, user, password, jobs, **kwargs):
    if not jobs:
        print("jobs not detected")
        exit(1)
    jobs_todo = set(
        map(lambda x: x.strip(), jobs.split(","))
    )

    jenkins = JenkinsJobs(
        jenkins_url=url,
        jenkins_user=user,
        jenkins_password=password,
        work_dir=os.getcwd()
    )

    jenkins.pull_jobs(jobs_todo)


# Sync from online jenkins job to github
# Should mount resources/jenkins to docker github folder
@dispatch.on('--sync')
def sync_jobs(url, user, password, jobs, **kwargs):
    if not jobs:
        print("jobs not detected")
        exit(1)
    jobs_todo = set(
        map(lambda x: x.strip(), jobs.split(","))
    )

    jenkins = JenkinsJobs(
        jenkins_url=url,
        jenkins_user=user,
        jenkins_password=password,
        work_dir=os.getcwd()
    )

    jenkins.sync_jobs(jobs_todo)


@dispatch.on('--sync-all')
def sync_all_jobs(url, user, password, **kwargs):
    jenkins = JenkinsJobs(
        jenkins_url=url,
        jenkins_user=user,
        jenkins_password=password,
        work_dir=os.getcwd()
    )

    all_jobs = jenkins.list_online_jobs()
    jenkins.sync_jobs(all_jobs)


@dispatch.on('--list')
def list_jobs(url, user, password, **kwargs):
    jenkins = JenkinsJobs(
        jenkins_url=url,
        jenkins_user=user,
        jenkins_password=password,
        work_dir=os.getcwd()
    )

    for x in sorted(jenkins.list_online_jobs()):
        print(x)

if __name__ == '__main__':
    dispatch(__doc__)