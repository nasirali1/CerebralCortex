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

def merge_consective_windows(data: OrderedDict) -> OrderedDict:
    """
    Merge two or more windows if the time difference between them is 0
    :param data:
    :return:
    """
    merged_windows = OrderedDict()
    element = None
    start = None
    end = None
    for key, val in data.items():
        if element is None:
            element = val
            start = key[0]
            end = key[1]
        elif element == val:
            element = val
            end = key[1]
        else:
            merged_windows[(start, end)] = element
            element = val
            start = key[0]
            end = key[1]
    if val is not None:
        merged_windows[(start, end)] = val

    return merged_windows