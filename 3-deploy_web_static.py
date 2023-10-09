#!/usr/bin/python3
from fabric.api import run, env, put, local, runs_once
from os.path import exists
from datetime import datetime

env.hosts = ['<IP 100.26.236.53>', '<IP 107.22.144.34>']
env.user = '<devmat>'
env.key_filename = '<~/.ssh/id_rsa>'

@runs_once
def do_pack():
    """
    Archives the static files.

    Returns:
        str or None: Path to the created archive or None if archiving fails.
    """
    if not os.path.isdir("versions"):
        os.mkdir("versions")
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
        # Upload the archive to the server
        put(archive_path, "/tmp/")

        # Extract the archive to the appropriate directory
        archive_filename = archive_path.split("/")[-1]
        archive_folder = archive_filename[:-4]  # Remove ".tgz" extension
        remote_path = "/data/web_static/releases/{}".format(archive_folder)

        run("mkdir -p {}".format(remote_path))
        run("tar -xzf /tmp/{} -C {}".format(archive_filename, remote_path))

        # Move the contents to the correct location
        run("mv {}/web_static/* {}/".format(remote_path, remote_path))
        run("rm -rf {}/web_static".format(remote_path))

        # Update the symbolic link to the new version
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
    # Call the do_pack function and store the path of the created archive
    archive_path = do_pack()

    if not archive_path:
        return False

    # Call the do_deploy function using the new archive path
    return do_deploy(archive_path)
