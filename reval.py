#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: srajith
# @Date:   2020-03-29 17:26:29
# @Last Modified by:   srajith
# @Last Modified time: 2020-03-29 18:43:36


import re
import requests
import concurrent.futures
import sys

def calc_reval(roll):
    s = requests.Session()

    roll_no = roll

    data = {
        '__LASTFOCUS': '',
        '__VIEWSTATE': '/wEPDwUJODEwOTUzODMyD2QWAgIDD2QWDgINDw9kFgIeB29uY2xpY2sFEXJldHVybiB2YWxpZGF0ZSgpZAIPDw8WAh4HVmlzaWJsZWhkZAIRDw8WAh8BaGRkAhMPDxYCHwFoZGQCFQ88KwAKAGQCFw88KwARAwAPZBYCHgtib3JkZXJjb2xvcgUHI0Y0RjRGNAEQFgAWABYADBQrAABkAhkPDxYCHwFoZGQYAgUJR3JpZFZpZXcxD2dkBQlGb3JtVmlldzEPZ2Tfdvhl7BTyehkS/2IirXre+dWXHUGudvANtU82yKxvDA==',
        '__VIEWSTATEGENERATOR': 'B2629E41',
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        '__EVENTVALIDATION': '/wEdAAM4BwhzC3yKHH4siEx+iEyuESCFkFW/RuhzY1oLb/NUVM34O/GfAV4V4n0wgFZHr3fxiLwv6L5Ozd5PGfKmBeoNzVXf1WPreDieg8Rngi/JHQ==',
        'TextBox1': roll_no,
        'Button1': 'Get Marks'
    }

    response = s.post(url, data=data)

    re_marks = re.findall(r'>\d\d\d</', response.text)
    re_sub = re.findall(r'>\w{5}</', response.text)

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
    if result:
        print("{} ===> {}".format(roll_no, result))


if __name__ == "__main__":

    url = 'https://egovernance.unom.ac.in/RVNOV2019/'
    status = requests.get(url)
    if status.status_code == 200:
        print("Valid url submitted ! ")
        with concurrent.futures.ThreadPoolExecutor() as executor:
            roll_number = [roll for roll in range(221810449, 221810499)]
            executor.map(calc_reval, roll_number)
    else:
        print("Invalid url ! ")
        sys.exit()

