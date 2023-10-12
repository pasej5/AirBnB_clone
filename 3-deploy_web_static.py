#!/usr/bin/python3
# deploy function that integrate do_deploy and do_pack.
import os.path
from fabric.api import env
from fabric.api import put
from fabric.api import run
from fabric.api import local
from datetime import datetime

env.hosts = ["54.175.146.62", "34.224.94.116"]


def do_pack():
	"""Create a tgz archive from the contents of the web_static folder."""
		try:
		now = datetime.now()
		archive_file = "web_static_{}{}{}{}{}{}.tgz".format(
				now.year, now.month, now.day, now.hour, now.minute, now.second
				)

		local("mkdir -p versions")

		local("tar -czvf versions/{} web_static".format(archive_file))

		return "versions/{}".format(archive_file)
		except Exception:
		return None


		def do_deploy(archive_path):
			"""
				Distributes an archive to a web server.
				"""
				if os.path.isfile(archive_path) is False:
					return False
					file = archive_path.split("/")[-1]
					name = file.split(".")[0]

					if put(archive_path, "/tmp/{}".format(file)).failed is True:
					return False
					if run("rm -rf /data/web_static/releases/{}/".
							format(name)).failed is True:
					return False
					if run("mkdir -p /data/web_static/releases/{}/".
							format(name)).failed is True:
					return False
					if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
							format(file, name)).failed is True:
					return False
					if run("rm /tmp/{}".format(file)).failed is True:
					return False
					if run("mv /data/web_static/releases/{}/web_static/* "
							"/data/web_static/releases/{}/".format(name, name)).failed is True:
					return False
					if run("rm -rf /data/web_static/releases/{}/web_static".
							format(name)).failed is True:
					return False
					if run("rm -rf /data/web_static/current").failed is True:
					return False
					if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
							format(name)).failed is True:
					return False
					return True


					def deploy():
						"""
							Deploy archive to a web server.
	"""
	   archive_path = do_pack()
	      if archive_path is None:
	return False
	return do_deploy(archive_path)
