__author__ = 'stonerri'


from fabric.contrib.project import rsync_project

from base import *


def setDefaults():

    env.user = 'root'
    env.hosts = ['192.241.156.224']



def systemInformation():

    pass


def sync():

    exclude_list = [
        '.git',
        '.vagrant',
        '.idea',
        '.DS_Store',
        'manage/.git/',
        'manage/.vagrant/',
        'manage/.idea/',
        'manage/.DS_Store'
    ]

    rsync_project('/vagrant', local_dir='../', exclude=exclude_list)