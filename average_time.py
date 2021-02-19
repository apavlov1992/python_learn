#!/usr/local/bin/python3


import sys
import json
import requests
import time


jenkins_curl = requests.get('https://ci.spb.yadro.com/api/json?tree=jobs[name]')
jobs_list = json.loads(jenkins_curl.text)
jobs = jobs_list['jobs']


def main():
 f = open('./job_list', 'w')
 for j in jobs:
  abir = requests.get('https://ci.spb.yadro.com/job/{}/lastBuild/api/json?tree=result,timestamp,estimatedDuration'
  .format(j['name']), allow_redirects=False)
 try:
  jobs_time = json.loads(abir.text)
 except Exception:
  pass
 timestam = jobs_time['timestamp']
 datetime_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(timestam/1000.0))
 list_of_j = str((j['name'], datetime_time))
 print(list_of_j)
 f.write(list_of_j+'\n')


if __name__ == '__main__':
  sys.exit(main())

