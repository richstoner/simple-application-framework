__author__ = 'stonerri'

from fabric.api import *

def setDefaults():
    env.user = 'root'
    env.hosts = ['192.241.156.224']


def sync():

    pass