#!/usr/bin/python3
"""
Fabric script to clean out-of-date archives.
"""

from fabric.api import run, local, env
import os

env.hosts = ['IP 100.26.236.53', 'IP 107.22.144.34']

def do_clean(number=0):
    """
    Deletes out-of-date archives.
    """
    number = int(number)
    if number < 2:
        number = 1
    local_archives = local("ls -t versions", capture=True).split('\n')
    for archive in local_archives[number:]:
        local("rm -f versions/{}".format(archive))


    remote_archives = run("ls -t /data/web_static/releases").split()
    for archive in remote_archives[number:]:
        run("rm -rf /data/web_static/releases/{}".format(archive))
