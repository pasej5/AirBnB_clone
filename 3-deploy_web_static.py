#!/usr/bin/python3
from fabric.api import local, env, put, run
from os.path import exists
from datetime import datetime

env.hosts = ['<IP web-01>', '<IP web-02>']
env.user = '<your_username>'
env.key_filename = '<path_to_your_private_key>'

def do_pack():
	"""
		Archives the static files locally.

		Returns:
		str or None: Path to the created archive or None if archiving fails.
		"""
		if not exists("versions"):
	local("mkdir -p versions")
d_time = datetime.now()
	output = "versions/web_static_{}{}{}{}{}{}.tgz".format(
			d_time.year,
			d_time.month,
			d_time.day,
			d_time.hour,
			d_time.minute,
			d_time.second
			)
	try:
	print("Packing web_static to {}".format(output))
	local("tar -cvzf {} web_static".format(output))
	size = os.stat(output).st_size
	print("web_static packed: {} -> {} Bytes".format(output, size))
	except Exception:
	output = None
	return output

	def do_deploy(archive_path):
		"""
			Distributes an archive to your web servers.

			Args:
			archive_path (str): Path to the archive file to be deployed.

					    Returns:
bool: True if deployment succeeds, False otherwise.
"""
if not exists(archive_path):
	return False

	try:
	put(archive_path, "/tmp/")


	archive_filename = archive_path.split("/")[-1]
	archive_folder = archive_filename[:-4]
	remote_path = "/data/web_static/releases/{}".format(archive_folder)

	run("mkdir -p {}".format(remote_path))
	run("tar -xzf /tmp/{} -C {}".format(archive_filename, remote_path))


	run("mv {}/web_static/* {}/".format(remote_path, remote_path))
	run("rm -rf {}/web_static".format(remote_path))


	current_path = "/data/web_static/current"
	run("rm -f {}".format(current_path))
	run("ln -s {} {}".format(remote_path, current_path))

	print("New version deployed!")

	return True
	except Exception:
	return False

	def deploy():
		"""
			Deploys the web_static archive to the web servers.

			Returns:
bool: True if deployment succeeds, False otherwise.
"""

archive_path = do_pack()

	if not archive_path:
	return False

return do_deploy(archive_path)
