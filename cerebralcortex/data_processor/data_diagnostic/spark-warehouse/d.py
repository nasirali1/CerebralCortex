from datetime import datetime
import time
import calendar
import email.utils

#epoch = datetime.datetime.utcfromtimestamp(0)
dt = datetime('2016-12-22 15:25:42.421000')

#day = dt.strftime("%Y%m%d")

print(email.utils.parsedate_tz(dt))

def unix_time_millis(dt):
    print( (dt - epoch).total_seconds() * 1000.0)