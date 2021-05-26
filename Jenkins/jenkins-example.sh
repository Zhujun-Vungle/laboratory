#!/bin/bash -e
cd $WORKSPACE

#sudo add-apt-repository ppa:cpick/hub
#sudo apt-get -f update
#sudo apt-get -f install hub

git clone git@github.com:Vungle/goblin.git
cd goblin

git checkout dev


rm -r res/jenkins/
mkdir -p res/jenkins/

docker run -v $WORKSPACE/goblin/res/jenkins:/usr/src/github \
           -v $WORKSPACE/goblin/core/jenkins/jenkins_all.py:/usr/src/jenkins_all.py \
           --rm vungle/jenkins-family-bucket \
           python3 /usr/src/jenkins_all.py --url="https://jenkins.vungle.io/" --user="junjun" --password="123456" \
           --sync-all
           


export GITHUB_USER=zhu1988jun@gmail@vungle.com
export GITHUB_PASSWORD=123456
branch=wip-autoPR-$(date +%Y%m%d%H%M%S)-USERA
git config --global user.email $GITHUB_USER
git config --global user.name $GITHUB_PASSWORD
git config --global --add hub.host https://github.com/Vungle

status=$(git status|grep "nothing to commit"| wc -l|tr -d '[:space:]')
echo status-${status}
if [ "$status" = "1" ]
then
echo "Nothing to commit"
exit 0
fi

git add .

git commit -m "auto PR"
git checkout -b $branch
git push origin HEAD

hub pull-request -b vungle:dev -h vungle:${branch} -F- <<< "This is auto PR from jenkins ^_^

Auot PR from jenkins: Update jobs from prod to github
- jobs: sync all!
- what: weekly sync job
"



