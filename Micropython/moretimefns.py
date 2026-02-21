# Python 3

# More time functions

import utime

def zeroformat(x, reqdlen):
    st = str(x)
    rf = reqdlen - len(str(x))
    if rf > 0:
        st = ('0'*rf) + st
    return st

def show_strtime(dt_tuple):
    strhour = zeroformat(dt_tuple[3], 2)
    strmin = zeroformat(dt_tuple[4], 2)
    strsec = zeroformat(dt_tuple[5], 2)
    return f'{strhour}:{strmin}:{strsec}'

def show_strdate(dt_tuple):
    strday = zeroformat(dt_tuple[2], 2)
    strmth = zeroformat(dt_tuple[1], 2)
    stryr = zeroformat(dt_tuple[0], 4)
    return f'{strday}-{strmth}-{stryr}'

def get_datetime(strdatetime):
    # strdatetime in the format of YYYY-MM-DDTHH:MM:SS+00:00
    # returns an 8-tuple in the same format as utime.localtime() with weekday and yearday set to zero
    dyear = int(strdatetime[0:4])
    dmonth = int(strdatetime[5:7])
    dday = int(strdatetime[8:10])
    dhour = int(strdatetime[11:13])
    dmin = int(strdatetime[14:16])
    dsec = int(strdatetime[17:19])
    return tuple((dyear, dmonth, dday, dhour, dmin, dsec, 0, 0))

def get_minsdiff(d1tuple, d2tuple):
    # works out the difference between two 8-tuple dates in complete minutes
    d1secs = utime.mktime(d1tuple)  # converts to seconds since 1/1/2000
    d2secs = utime.mktime(d2tuple)  # converts to seconds since 1/1/2000
    diffmins = int((d2secs - d1secs)/60.0)  # divide by 60 secs and round down
    return diffmins