#!/usr/bin/env python
'''Nagios plugin for monitoring Amazon SES quota usage'''

from boto import ses
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
        parser.add_option('-r', '--region', action="store",
                        dest="region", help="AWS secret key", default="us-east-1"),
        ]



(options, args) = parser.parse_args()

if not (options.critical_threshold and options.warning_threshold):
    print("Critical and warning thresholds are req")
    sys.exit(2)

if (options.aws_key and  options.aws_secret):
     conn = ses.connect_to_region(
                        options.region,
                        aws_access_key_id=options.aws_key,
                        aws_secret_access_key=options.aws_secret)
else:
     conn = ses.connect_to_region(options.region)

if not conn:
    print("CRITICAL: Could not connect to SES, please check credentials!")
    sys.exit(2)

try:
    quota = conn.get_send_quota()
except BotoServerError:
    print("CRITICAL: Could not connect to server")
    sys.exit(2)

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
