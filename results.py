#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: srajith
# @Date:   2020-03-20 22:34:31
# @Last Modified by:   srajith
# @Last Modified time: 2020-03-21 23:50:28

import re
import sys
import requests
import concurrent.futures

def calc_marks(roll):
    s = requests.Session()

    roll_no = roll
    data = {
        '__LASTFOCUS': '',
        '__VIEWSTATE': '/wEPDwULLTExNDk4NTI2NzcPZBYCAgMPZBYUAg0PD2QWAh4Hb25jbGljawURcmV0dXJuIHZhbGlkYXRlKClkAg8PDxYCHgdWaXNpYmxlaGRkAhMPDxYCHwFoZGQCFQ88KwAKAGQCFw88KwARAwAPZBYCHgtib3JkZXJjb2xvcgUHI0Y0RjRGNAEQFgAWABYADBQrAABkAhkPDxYCHwFoZGQCGw8PFgIfAWhkZAIdDw8WAh8BaGRkAh8PDxYCHwFoZGQCIQ8PFgIfAWhkZBgCBQlHcmlkVmlldzEPZ2QFCUZvcm1WaWV3MQ9nZLaGGV84hEKN39bx3qJj+4a+uqf4R6P0rR8C8lOVSVpq',
        '__VIEWSTATEGENERATOR': 'A980467A',
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        '__EVENTVALIDATION': '/wEdAAMM1iTKfqRaR+qYZptN5JwpESCFkFW/RuhzY1oLb/NUVM34O/GfAV4V4n0wgFZHr3fON8hWKDQq3TURb4VWk91Q+JSmQ8P4fnfGKZMawLVg9Q==',
        'TextBox1': str(roll_no),
        'Button1': 'Get Marks'
    }

    response = s.post(url, data=data)

    re_marks = re.findall(r'<b>\d{3}</b>|<b>AAA</b>', response.text)

    re_sub = re.findall(r'<b>\w{5}</b>', response.text)

    parse_marks = []
    for m in range(2, len(re_marks), 3):
        if "AAA" in re_marks[m]:
            parse_marks.append(0)
        else:
            parse_marks.append(
                int("".join(re.findall(r'\d\d\d', re_marks[m])).lstrip('0')))

    parse_code = [
        "".join(
            re.findall(
                r'\w{5}',
                re_sub[s])) for s in range(
            2,
            len(re_sub))]

    result = {parse_code[i]: parse_marks[i] for i in range(len(parse_code))}

    total = 0

    for sub_code in subjects:
        if sub_code in result:
            total += result[sub_code]
    results[roll_no] = total


if __name__ == "__main__":

    url = 'https://egovernance.unom.ac.in/resultnocap/'
    status = requests.get(url)
    if status.status_code == 200:
        print("Valid url submitted ! ")
    
        roll_number = [roll for roll in range(221810449, 221810499)]
        subjects = [
            'CLK3V',
            'CLZ3P',
            'SAE31',
            'SAE3A',
            'SBAOC',
            'TSSEG',
            'CLE3H',
            'CLA3M']
        results = {}

        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(calc_marks, roll_number)

        for key, value in sorted(results.items()):
            print("{} ===> {} ===> {}".format(key, value, value / 6))
    else:
        print("Invalid url ! ")
        sys.exit()
