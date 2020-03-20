#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: r4j
# @Date:   2020-03-20 13:37:27
# @Last Modified by:   r4j
# @Last Modified time: 2020-03-20 13:37:56

from requests import post
from re import findall
from tqdm import tqdm

all_results = { }
given_sub = ['CLK3V', 'CLZ3P', 'SAE31', 'SAE3A', 'SBAOC', 'TSSEG', 'CLE3H', 'CLA3M']

for roll in tqdm(range(221810449,221810499)):

	roll = str(roll)

	mapping = { }
	cookies = {
	  'ASP.NET_SessionId': 'm353wvmvregv4jg3pffxast3',
	}

	headers = {
	  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0',
	  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	  'Accept-Language': 'en-US,en;q=0.5',
	  'Referer': 'https://results.unom.ac.in/ResultApr19/',
	  'Content-Type': 'application/x-www-form-urlencoded',
	  'DNT': '1',
	  'Connection': 'keep-alive',
	  'Upgrade-Insecure-Requests': '1',
	}

	data = {
		'__VIEWSTATE': '/wEPDwULLTExNDk4NTI2NzcPZBYCAgMPZBYYAgsPDxYCHgRUZXh0BQkyMjE4MTA0OTZkZAINDw9kFgIeB29uY2xpY2sFEXJldHVybiB2YWxpZGF0ZSgpZAIPDw8WAh4HVmlzaWJsZWhkZAIRDw8WAh8CZxYCHghkaXNhYmxlZAUIZGlzYWJsZWRkAhMPDxYCHwJnZGQCFQ88KwAKAQAPFgQeC18hRGF0YUJvdW5kZx4LXyFJdGVtQ291bnQCBmQWAmYPZBYGZg8PFgIfAmhkZAIBD2QWAmYPZBYCAgEPZBYGZg9kFgICAQ9kFgJmDw8WAh8ABQ/CoMKgwqAyMjE4MTA0OTZkZAIBD2QWAgIBD2QWAmYPDxYCHwAFDsKgwqDCoFJBSklUSCBTZGQCAg9kFgICAQ9kFgJmDw8WAh8ABRDCoMKgwqAwMi8wMy8yMDAxZGQCAg8PFgIfAmhkZAIXDzwrABEDAA8WBB8EZx8FAgYWAh4LYm9yZGVyY29sb3IFByNGNEY0RjQBEBYAFgAWAAwUKwAAFgJmD2QWDgIBD2QWCmYPDxYCHwAFBUNMSzNWZGQCAQ8PFgIfAAUDMDQyZGQCAg8PFgIfAAUDMDI1ZGQCAw8PFgIfAAUDMDY3ZGQCBA8PFgIfAAUBUGRkAgIPZBYKZg8PFgIfAAUFQ0xaM1BkZAIBDw8WAh8ABQMwMzdkZAICDw8WAh8ABQMwMjNkZAIDDw8WAh8ABQMwNjBkZAIEDw8WAh8ABQFQZGQCAw9kFgpmDw8WAh8ABQVTQUUzMWRkAgEPDxYCHwAFAzA2MGRkAgIPDxYCHwAFAzA0MGRkAgMPDxYCHwAFAzEwMGRkAgQPDxYCHwAFAVBkZAIED2QWCmYPDxYCHwAFBVNBRTNBZGQCAQ8PFgIfAAUDMDQxZGQCAg8PFgIfAAUDMDI1ZGQCAw8PFgIfAAUDMDY2ZGQCBA8PFgIfAAUBUGRkAgUPZBYKZg8PFgIfAAUFU0JBT0NkZAIBDw8WAh8ABQMwNTJkZAICDw8WAh8ABQMwMjVkZAIDDw8WAh8ABQMwNzdkZAIEDw8WAh8ABQFQZGQCBg9kFgpmDw8WAh8ABQVUU1NFR2RkAgEPDxYCHwAFAzA0MWRkAgIPDxYCHwAFAzAzOWRkAgMPDxYCHwAFAzA4MGRkAgQPDxYCHwAFAVBkZAIHDw8WAh8CaGRkAhkPDxYCHwJnZGQCGw8PFgIfAmdkZAIdDw8WAh8CZ2RkAh8PDxYCHwJnZGQCIQ8PFgIfAmdkZBgCBQlHcmlkVmlldzEPPCsADAEIAgFkBQlGb3JtVmlldzEPFCsAB2RkZGRkFgACBmT2olW6nihzxRuejxfMPUZO3E/jfUplu6SOuYNBBw2lww==',
		'__VIEWSTATEGENERATOR': 'A980467A',
		'__EVENTVALIDATION': '/wEdAAV8rl9A1L4mohPzlg2zIrm7ESCFkFW/RuhzY1oLb/NUVM34O/GfAV4V4n0wgFZHr3foLFFNa6TDQkcC5AMQGEYsEJY0Gz2I8aOlPkvy97T/cjz2RB7v7LunONGQszFfx7Kh1ifiHdJhZ23cZly1ic8V',
		'TextBox1': roll,	#userid
		'Button1': 'Get Marks'
	}

	response = post('https://egovernance.unom.ac.in/resultnocap/', headers=headers, cookies=cookies, data=data)
	
	response = response.text
	# print(response)
	matches = findall(r'>\d{3}<|;">AAA',response)
	subject_found = findall(r'%;">\w{5}<',response)
	
	final_mark = []
	for match in range(2,len(matches),3):
		if(matches[match]==';">AAA'):
			final_mark.append(0)
		else:
			final_mark.append(int(matches[match][1:-1]))
	subject_found = [sub[4:-1] for sub in subject_found]
	sum =0

	for i in range(len(final_mark)):
		mapping[subject_found[i]] = final_mark[i]
	checker = []
	for i,j in mapping.items():
		checker.append(i)

	diff = list(set(given_sub)&set(checker))

	for i in range(len(diff)):
		sum += mapping[diff[i]]
	all_results.update({roll:sum})


print(all_results)

