from datetime import datetime
from pytz import timezone
from collections import OrderedDict
import csv

def datetime_to_epoch(date_obj):
    localtz = timezone('US/Central')

    epoch = datetime.utcfromtimestamp(0)
    epoch = localtz.localize(epoch)
    return (date_obj - epoch).total_seconds() * 1000.0

def write_to_csv(data: OrderedDict, file_name):
    ofile  = open('/home/ali/Documents/'+file_name, "w")
    writer = csv.writer(ofile, delimiter=",")

    for row, val in data.items():
        rr = str(row), str(val)
        writer.writerow(rr)

    ofile.close()