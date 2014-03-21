__author__ = 'stonerri'


from fabric.contrib.project import rsync_project

from base import *


def setDefaults():

    env.user = 'root'
    env.hosts = ['192.241.196.151']



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
        'manage/.DS_Store',
        'server/apps/annotator/venv'
    ]

    rsync_project('/vagrant', local_dir='../', exclude=exclude_list)



# parser = SafeConfigParser()
# parser.read('settings.ini')
#
# client_id = parser.get('digitalocean', 'client_id')
# api_key = parser.get('digitalocean', 'api_key')
#
# def dostat():
#
#     import digitalocean
#
#     manager = digitalocean.Manager(client_id=client_id, api_key=api_key)
#     my_droplets = manager.get_all_droplets()
#     for droplet in my_droplets:
#         print '%s, %s, %s' % (droplet.name, droplet.ip_address, droplet.image_id)
#
# def dolaunch():
#
#     import digitalocean
#
#     droplet = digitalocean.Droplet(client_id=client_id, api_key=api_key, name='autodrop', region_id=3, image_id=284203,
#                                    size_id=66, backup_active=False)
#
#     # this configures a 512MB droplet in NYC running 12.04 LTS
#     # ... I had to install a ruby gem (tugboat) first to get the list of image ids...
#
#     print droplet
#     droplet.create()
#
#     while event.percentage != 100:
#         ### Refreshing the event status
#         #### Checking the status of the droplet
#         event = droplet.get_events()[0]
#         event.load()
#         #Once it shows 100, droplet is up and running
#         print event
#         print event.percentage
#
#     print droplet.ip_address
#
#
#
