#!/usr/bin/python3
""" script that generates a .tgz archive from the contents """


from fabric.api import *
from datetime import datetime

def do_pack():
    """archive from the contents of the web_static folder"""
    local("sudo mkdir -p versions")
    filename = "versions/web_static_{}.tgz".format(datetime.now().strftime("%Y%m%d%H%M%S"))
    result = local("sudo tar -cvzf {} web_static".format(filename))
    if result.succeeded:
        return filename
    else:
        return None
