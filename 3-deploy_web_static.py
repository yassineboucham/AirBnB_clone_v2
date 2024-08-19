#!/usr/bin/python3
"""
Creates and distributes an archive to your web servers
"""
from fabric.api import *
from datetime import datetime
import os.path

env.hosts = [
    "18.206.208.23",
    "54.210.152.224"
]

def do_pack():
    """generates a .tgz archive from the contents of the web_static folder
    Usage:
        fab -f 1-pack_web_static.py do_pack
    """
    local("mkdir -p versions")
    curr_time = datetime.now()
    ver_time = curr_time.strftime("%Y%m%d%H%M%S")
    tar_path = "versions/web_static_{}.tgz".format(ver_time)

    r = local("tar czf {} web_static/".format(tar_path))

    if r.succeeded:
        return tar_path
    else:
        return None

def Uploading(archive_path):
    """Helper function to avoid long lines"""
    # Upload the archive to the /tmp/ directory of the web server
    put(archive_path, "/tmp/")

    releases_path = "/data/web_static/releases/"
    # Get the name of the archive web_static_longdate.org
    archive_file = archive_path.split("/")[-1]
    # The path where archive is located in the curr remote server
    remote_archive_path = "/tmp/" + archive_file
    # The path where archive will be extracted
    new_release_path = releases_path + archive_file.split(".")[-2]

    # Extract the archive into releases_path
    tar_args = (remote_archive_path, releases_path)
    cmd = run("tar xvf {} --directory={}".format(*tar_args))

    # We done with the archive, so let's get ride of it
    run("rm {}".format(remote_archive_path))

    # The archive is consists of the directory web_static, so I had to mess
    # around with it to get its content moved to new_release_path, and finally
    # remove it, Please DO NOT ask me why I didn't compress the files directly
    # into the archive file, I was told to do it this way.
    run("mkdir -p {}".format(new_release_path))
    run("cp -r {}/* {}/".format(releases_path+"web_static", new_release_path))
    run("rm -rf {}".format(releases_path+"web_static"))

    run("rm /data/web_static/current")
    run("ln -sf {} /data/web_static/current".format(new_release_path))


def do_deploy(archive_path):
    """Distributes an archive to your web servers
        Usage:
            fab -f 2-do_deploy_web_static.py
            do_deploy:<path/to/archive>
            [-i my_ssh_private_key -u ubuntu]
    """
    if not os.path.isfile(archive_path):
        return False
    try:
        Uploading(archive_path)
        print("--- Everything goes well ---")
        return True
    except Exception as e:
        print("Some thing went worng!")
        return False

def deploy():
    """creates and distributes an archive to the web servers

    Usage: 
        fab -f 3-deploy_web_static.py deploy [-i my_ssh_private_key]
        [-u ubuntu]
    """
    packed_path = do_pack()
    if not packed_path:
        return False
    return do_deploy(packed_path)
