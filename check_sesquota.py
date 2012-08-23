'''Nagios plugin for monitoring Amazon SES quota usage'''
from boto import connect_ses
from boto.exception import *
import optparse
import sys
import pdb

parser = optparse.OptionParser()

options = [
        parser.add_option('-w', '--warning', action="store",
                        dest="warning_threshold", help="Warning threshold"),
        parser.add_option('-c', '--critical', action="store",
                        dest="critical_threshold", help="Critical threshold"),
        parser.add_option('-k', '--aws-key', action="store",
                        dest="aws_key", help="AWS Key"),
        parser.add_option('-s', '--aws-secret', action="store",
                        dest="aws_secret", help="AWS secret key"),
        ]



(options, args) = parser.parse_args()

if not (options.critical_threshold and options.warning_threshold):
    print("Critical and warning thresholds are req")
    sys.exit(2)


if (options.aws_key and  options.aws_secret):
    try:
        conn = connect_ses(aws_access_key_id=options.aws_key,
                        aws_secret_access_key=options.aws_secret)
    except boto.exception.BotoServerError:
        print("Could not connect to server")
        sys.exit(2)
else:
    try:
        conn = connect_ses()
    except boto.exception.BotoServerError:
        print("Could not connect to server")

if not conn:
    print("Could not connect to SES, please check credentials!")
    sys.exit(2)


quota = conn.get_send_quota()
max24h_send = float(quota['GetSendQuotaResponse']['GetSendQuotaResult']['Max24HourSend'])
sent_last24h = float(quota['GetSendQuotaResponse']['GetSendQuotaResult']['SentLast24Hours'])
used_percentage = (sent_last24h * 100)/max24h_send

if (used_percentage > float(options.critical_threshold)):
    print("SES QUOTA CRITICAL: %0.2f%% (%0.2f sent out of %0.2f)" % (used_percentage,sent_last24h,max24h_send))
    sys.exit(2)
if (used_percentage > float(options.warning_threshold)):
    print("SES QUOTA WARNING: %0.2f%% (%0.2f sent out of %0.2f)" % (used_percentage,sent_last24h,max24h_send))
    sys.exit(1)

print("SES QUOTA OK: %0.2f%% (%0.2f sent out of %0.2f)" % (used_percentage,sent_last24h,max24h_send))
sys.exit(0)

