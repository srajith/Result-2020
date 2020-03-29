#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: srajith
# @Date:   2020-03-25 14:08:18
# @Last Modified by:   srajith
# @Last Modified time: 2020-03-29 18:44:23

import requests
import re
import concurrent.futures
import sys


def calc_arrears(roll):
    roll_no = roll

    data = {
        '__LASTFOCUS': '',
        '__VIEWSTATE': '/wEPDwULLTExNDk4NTI2NzcPZBYCAgMPZBYUAg0PD2QWAh4Hb25jbGljawURcmV0dXJuIHZhbGlkYXRlKClkAg8PDxYCHgdWaXNpYmxlaGRkAhMPDxYCHwFoZGQCFQ88KwAKAGQCFw88KwARAwAPZBYCHgtib3JkZXJjb2xvcgUHI0Y0RjRGNAEQFgAWABYADBQrAABkAhkPDxYCHwFoZGQCGw8PFgIfAWhkZAIdDw8WAh8BaGRkAh8PDxYCHwFoZGQCIQ8PFgIfAWhkZBgCBQlHcmlkVmlldzEPZ2QFCUZvcm1WaWV3MQ9nZLaGGV84hEKN39bx3qJj+4a+uqf4R6P0rR8C8lOVSVpq',
        '__VIEWSTATEGENERATOR': 'A980467A',
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        '__EVENTVALIDATION': '/wEdAAMM1iTKfqRaR+qYZptN5JwpESCFkFW/RuhzY1oLb/NUVM34O/GfAV4V4n0wgFZHr3fON8hWKDQq3TURb4VWk91Q+JSmQ8P4fnfGKZMawLVg9Q==',
        'TextBox1': roll_no,
        'Button1': 'Get Marks'
    }

    response = requests.post(
        url, data=data)
    re_status = re.findall(
        r'<b>RA</b>|<b>A</b>|<b>F</b>|<b>P</b>', response.text)

    re_sub = re.findall(r'<b>\w{5}</b>', response.text)
    re_sub = re_sub[2:]
    re_sub = re.findall(r'\w{5}', ''.join(re_sub))

    string = ""
    for i in range(len(re_status)):
        if "A" in re_status[i]:
            string += re_sub[i] + ","

    print("{} ===> {}".format(roll_no, string))
    

if __name__ == '__main__':
    url = 'https://egovernance.unom.ac.in/resultnocap/'
    status = requests.get(url)
    if status.status_code == 200:
        print("Valid url submitted ! ")
        with concurrent.futures.ThreadPoolExecutor() as executor:
            roll_number = [roll for roll in range(221810449, 221810499)]
            executor.map(calc_arrears, roll_number)
    else:
        print("Invalid url ! ")
        sys.exit()
