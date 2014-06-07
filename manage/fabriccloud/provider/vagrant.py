__author__ = 'stonerri'

def setDefaults():

    env.user = 'vagrant'
    env.hosts = ['127.0.0.1']
    env.port = 2222

    # use vagrant ssh key
    result = local('vagrant ssh-config | grep IdentityFile', capture=True)
    env.key_filename = result.split()[1]


def systemInformation():
    pass


def sync():
    print 'vagrant gets sync for free'