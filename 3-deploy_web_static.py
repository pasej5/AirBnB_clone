#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to your web servers.
"""

from fabric.api import local, env, run, put
from datetime import datetime
import os

env.hosts = ['<IP 100.26.236.53>', '<IP 107.22.144.34>']

def do_pack():
    """
    Creates a compressed archive of web_static folder.
    """
    try:
        time_format = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = "versions/web_static_{}.tgz".format(time_format)
        local("mkdir -p versions")
        local("tar -cvzf {} web_static".format(archive_path))
        return archive_path
    except:
        return None

def do_deploy(archive_path):
    """
    Deploys the compressed archive to web servers.
    """
    if not os.path.exists(archive_path):
        return False

    try:
        archive_name = os.path.basename(archive_path)
        dest = "/data/web_static/releases/{}".format(archive_name[:-4])

        put(archive_path, "/tmp")
        run("mkdir -p {}".format(dest))
        run("tar -xzf /tmp/{} -C {}".format(archive_name, dest))
        run("rm /tmp/{}".format(archive_name))
        run("mv {}/web_static/* {}/".format(dest, dest))
        run("rm -rf {}/web_static".format(dest))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(dest))
        return True
    except:
        return False

def deploy():
    """
    Deploys the web static content to web servers.
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
