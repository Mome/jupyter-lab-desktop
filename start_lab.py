#! /usr/bin/python

"""
Start Jupyter lab like a standalon application.
"""

import sys
import subprocess as sp
import time
import secrets
import re

# change this to whatever browser you want to use
browser_cmd = 'chromium --app=%s'

# start jupyter server
token = secrets.token_hex(32)
cmd = 'jupyter lab --NotebookApp.token=%s --no-browser' % token
server = sp.Popen(cmd.split() + sys.argv[1:])

# check if server started and aquire url
pattern = re.compile(r'http://localhost:\d+/\?token=([\w]+)')
timeout = 10
tic = time.time()
found_server = False
while not found_server:
    toc = time.time()
    if tic + timeout < toc:
        raise TimeoutError('Server not found.')

    cmd = "jupyter notebook list"
    nb_list = sp.check_output(cmd.split()).decode()
    nb_list = nb_list.split('\n')[1:-1]

    for line in nb_list:
        url = line.split(' :: ')[0]
        other_token = re.match(pattern, url).groups()[0]

        if other_token == token:
            found_server = True
            break
    else:
        time.sleep(0.1)

# start browser
cmd = browser_cmd % url
browser = sp.Popen(cmd.split())

print('Wait for browser to be closed.')
browser.wait()
server.terminate()
print()
