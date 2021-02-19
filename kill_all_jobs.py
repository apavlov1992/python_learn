#!/usr/local/bin/python3

import sys
import requests


all_jobs = requests.get('https://ci.spb.yadro.com/api/json?tree=jobs[name]').json()


def build_to_kill():
    for job in all_jobs['jobs']:
        all_builds = requests.get("https://ci.spb.yadro.com/job/{}/api/json?tree=builds[id,building]"
                                  .format(job['name'])).json()
        try:
            for build in all_builds['builds']:
                if build['building']:
                    build_url = "https://ci.spb.yadro.com/job/{}/{}/stop".format(job['name'], build['id'])
                    yield build_url
        except Exception as e:
            print("Error: {}".format(e))
            pass


def main():
    for i in build_to_kill():
        requests.get(i)


if __name__ == '__main__':
    sys.exit(main())
