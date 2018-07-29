from datetime import datetime
from datetime import timedelta
import time
import os
import argparse
import sys
import sendgrid
import pandas as pd
from bson.objectid import ObjectId
from pymongo import MongoClient
from pymongo import ReadPreference
from pymongo.database import Database
from sqlalchemy import create_engine

# python3 legacy.py  -a 591e464525727b8e22001afd -s "2017-08-01" -e "2017-08-02" -f filename.csv -r 'jun.zhu@vungle.com'

def connect_prod_mongo():
    conn = MongoClient(f"""mongodb://{os.environ['MONGO_USERNAME']}:{os.environ['MONGO_PASSWORD']}@ds051483-a1.mongolab.com:51483/vvv-repl?replicaSet=rs-ds051483""")
    db = Database(conn, "vvv-repl")
    return db


def connect_prod_redshift():
    postgres_url = f"""postgresql://{os.environ['RS_USERNAME']}:{os.environ['RS_PASSWORD']}@cheezit.c3livwoqjkry.us-east-1.redshift.amazonaws.com:5439/cheezit"""
    return create_engine(postgres_url)


def connect_local():
    client = MongoClient('localhost', 27017)
    db = client.vungle_development
    return db


def find_account(accounts, account_id):
    result = accounts.find_one({"_id": ObjectId("%s" % account_id)})
    if result:
        return {'id': account_id, 'name': quote(result.get('name'))}
    return None


def get_advertiser_campaigns(campaigns, account):
    results = {}
    for campaign in campaigns.find({"parentAccount": ObjectId("%s" % account['id'])}):
        results[campaign.get('_id')] = {"name": quote(campaign.get('name')), "OS": campaign.get('targetPlatform'),
                                        "account": account['id'], "account_name": account['name']}
    return results


def generate_advertiser_reports_redshift(account_id, start_date, end_date, engine, unified_cloumns):
    end_date_next = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
    end_date_next_str = end_date_next.strftime("%Y-%m-%d")
    sql = f"""
    WITH report AS
      (SELECT date(event_time) AS event_time,
              account_id AS account_id,
              campaign_id AS campaign_id,
              platform AS os,
              sum(impressions) AS impressions,
              sum(views) AS views,
              sum(completes) AS completes,
              sum(clicks) AS clicks,
              ROUND((sum(clicks) * 100)::float/nullif(sum(views),0), 2) AS ctr,
              sum(installs) AS installs,
              ROUND(sum(installs)::float/nullif(sum(clicks),0), 2) AS itr,
              ROUND(sum(installs)/nullif(sum(views), 0), 2) AS cvr,
              sum(adv_spend) AS spend
       FROM advertiser_report
       WHERE account_id = '{account_id}'
         AND event_time >= '{start_date}'
         AND event_time < '{end_date_next_str}'
       GROUP BY 1,
                2,
                3,
                4
                 )
    SELECT r.event_time AS Date,
           a.name AS Account,
           r.account_id AS Account_id,
           c.name AS Campaign,
           r.campaign_id AS Campaign_ID,
           r.os AS OS,
           r.impressions AS Impressions,
           r.views AS Views,
           r.completes AS Completes,
           r.clicks AS Clicks,
           r.ctr AS CTR,
           r.installs AS Installs,
           r.itr AS InstallRate,
           r.cvr AS CVR,
           r.spend AS Spend
    FROM report r
    JOIN
      (SELECT id,
              name
       FROM campaigns) c ON c.id = r.campaign_id
    JOIN
      (SELECT id,
              name
       FROM accounts) a ON a.id = r.account_id
      order by 5,1;
    """
    print(sql)
    df = pd.read_sql_query(sql, engine)
    df.columns = unified_cloumns
    return df


def generate_advertiser_reports_mongo(aggregates, campaigns, start_date, end_date, unified_cloumns):
    filter = {
        "campaign": {"$in": list(campaigns.keys())},
        "metric": "campaign",
        "date": {"$gte": "%s" % start_date, "$lte": "%s" % end_date}
    }
    print(filter)
    count = 0
    lines = []
    for report in aggregates.find(filter):
        count += 1
        if (count % 1000 == 0):
            print(count)
        cid = report.get('campaign')
        campaign = campaigns[cid]
        line = []
        line.append(str(report.get('date')))
        line.append(campaign['account_name'])
        line.append(campaign['account'])
        line.append(campaign['name'])
        line.append(str(cid))
        line.append(campaign['OS'])
        line.append(str(report.get('impressions')))
        line.append(str(report.get('views')))
        line.append(str(report.get('completes')))
        line.append(str(report.get('clicks')))
        line.append(calcCTR(report.get('views'), report.get('clicks')))
        line.append(str(report.get('installs')))
        line.append(calcInstallRate(report.get('clicks'), report.get('installs')))
        line.append(calcConversionRate(report.get('views'), report.get('installs')))
        line.append(toCurrency(report.get('revenue')))
        lines.append(line)

    return pd.DataFrame(lines, columns=unified_cloumns)


def calcCTR(views, clicks):
    if (float(views) < 0.5):
        return '0.00'
    return toPercent(float(clicks) / float(views))


def calcECPM(views, pubRevenue):
    if (float(views) < 0.5):
        return '0.00'
    return toCurrency(float(pubRevenue) * 1000 / float(views))


def calcInstallRate(clicks, installs):
    if (float(clicks) < 0.5):
        return '0.00'
    return toPercent(float(installs) / float(clicks))


def calcConversionRate(views, installs):
    if (float(views) < 0.5):
        return '0.00'
    return toPercent(float(installs) / float(views))


def toCurrency(x):
    return str(round(x, 2))


def toPercent(x):
    return str(round(x * 100, 2))


def quote(s):
    if not s:
        return s
    if s.find(',') < 0:
        return s
    return '"%s"' % s


def mail_report(subject, recipients, filename):
    sg = sendgrid.SendGridClient(os.environ['SMTP_USERNAME'], os.environ['SMTP_PASSWORD'], secure=True)
    message = sendgrid.Mail()
    for recipient in recipients.split(','):
        message.add_to(recipient.strip())
    message.set_from("de@vungle.com")
    message.set_subject(subject)
    message.set_html("Hello, Please find in attachment. Thank you.")
    message.add_attachment(os.path.basename(filename), filename)
    sg.send(message)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate reports for given advertiser account')
    parser.add_argument('-a', action='store', dest='advertiser_account', required=True,
                        help='Account ID of the advertiser')
    parser.add_argument('-s', action='store', dest='start_date', required=True,
                        help='Start date of the report')
    parser.add_argument('-e', action='store', dest='end_date', required=True,
                        help='End date of the report')
    parser.add_argument('-f', action='store', dest='file_name', required=True,
                        help='File name to save the report')
    parser.add_argument('-r', action='store', dest='recipients', required=True,
                        help='Recipients to receive this report')

    arg_results = parser.parse_args()
    db = connect_prod_mongo()
    engine = connect_prod_redshift()
    account = find_account(db.accounts, arg_results.advertiser_account)
    if not account:
        print('Failed to find the account %s' % arg_results.advertiser_account)
        sys.exit(1)

    campaigns = get_advertiser_campaigns(db.campaigns, account)
    df_all = None
    df_cloumns = ['Date',
        'Account',
        'Account_id',
        'Campaign',
        'Campaign ID',
        'OS',
        'Impressions',
        'Views',
        'Completes',
        'Clicks',
        'CTR (%)',
        'Installs',
        'Install Rate (%)',
        'Conversion Rate (%)',
        'Spend ($)']
    if arg_results.end_date <= '2017-07-05':
        df_all = generate_advertiser_reports_mongo(db.dailyaggregates, campaigns, arg_results.start_date,
                                                   arg_results.end_date, df_cloumns)
    elif arg_results.start_date > '2017-07-05':
        df_all = generate_advertiser_reports_redshift(arg_results.advertiser_account, arg_results.start_date,
                                                      arg_results.end_date, engine, df_cloumns)
    else:
        df_mongo = generate_advertiser_reports_mongo(db.dailyaggregates, campaigns, arg_results.start_date,
                                                     '2017-07-05', df_cloumns)
        df_redshift = generate_advertiser_reports_redshift(arg_results.advertiser_account, '2017-07-06',
                                                           arg_results.end_date, engine, df_cloumns)

        df_all = df_mongo.append(df_redshift)

    print(df_all.sort_values(['Campaign', 'Date'], ascending=[True, False]).head(20))
    df_all.to_csv(arg_results.file_name)
    subject = 'Report of Advertiser %s: %s ~ %s' % (account['name'], arg_results.start_date, arg_results.end_date)
    mail_report(subject, arg_results.recipients, arg_results.file_name)

