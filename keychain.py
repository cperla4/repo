from netmiko import ConnectHandler
import requests
from datetime import datetime
import os, sys

def current_time(i):
    month_list = ['Void','Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    current_month = month_list[i.month]
    current_day = i.day
    current_year = i.year 
    return '%s %s %s' % (current_month, current_day, current_year)
date_now = current_time(datetime.now())
