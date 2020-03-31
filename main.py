
#!/usr/bin/env python3

import re
import sys
import argparse
import requests
import concurrent.futures


subjects = [
    'CLK3V',
    'CLZ3P',
    'SAE31',
    'SAE3A',
    'SBAOC',
    'TSSEG',
    'CLE3H',
    'CLA3M']

result_url = 'https://egovernance.unom.ac.in/resultnocap/'
arrear_url = result_url
reval_url = 'https://egovernance.unom.ac.in/RVNOV2019/'

roll_number = [roll for roll in range(221810449, 221810499)]


def status(url):
    if requests.get(url).status_code == 200:
        return True


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
        arrear_url, data=data)
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


def calc_result(roll):
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

    response = s.post(result_url, data=data)

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

    response = s.post(reval_url, data=data)

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


def Main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-r", "--result", help="Get the result", action="store_true")
    parser.add_argument(
        "-a", "--arrear", help="Get the arrear result", action="store_true")
    parser.add_argument(
        "-re", "--reval", help="Get the reval result", action="store_true")
    parser.add_argument(
        "-o", "--out",    help="store the output to a file", action="store_true")

    args = parser.parse_args()

    if args.reval:
        if status(reval_url):

            print("========== Revaluation ==========")
            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.map(calc_reval, roll_number)

            print("========== End ==========")

        else:
            print("Invalid url ")

    if args.arrear:
        if status(arrear_url):

            print("========== Arrears ==========")

            with concurrent.futures.ProcessPoolExecutor() as executor:
                executor.map(calc_arrears, roll_number)

            print("========== End ==========")

        else:
            print("Invalid url ")

    if args.result:
        if status(result_url):
            print("========== Results ==========")

            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.map(calc_result, roll_number)

            for key, value in sorted(results.items()):

                print("{} ===> {} ===> {}".format(key, value, value / 6))

            print("========== End ==========")
        else:
            print("Invalid url ")


if __name__ == "__main__":
    results = {}
    Main()
# Todo output func 