__author__ = 'stonerri'

from fabric.api import *
from fabric.colors import *

from webservers import *
from analysis import *


#region fabric methods

def update(verbose=False):
    ''' Runs update & upgrade for system packages
    '''
    _updatePackages(verbose)
    _upgradePackages(verbose)


def rsync(verbose=False):
    '''
    '''
    if 'p' not in env.keys():
        env.p = _importProvider('')
        env.provider = 'vagrant'
        env.p.setDefaults()

    env.p.sync()




def info():
    ''' Returns information about the system
    '''
    _systemInformation()


def provider(_provider):
    ''' Specify the provider : aws, do, vagrant, other?
    '''

    env.p = _importProvider(_provider)
    env.provider = _provider
    env.p.setDefaults()


def user(_user):
    ''' Set a specific user for the action
    '''

    if 'p' not in env.keys():
        env.p = _importProvider('')
        env.provider = 'vagrant'
        env.p.setDefaults()

    env.user = _user

    print 'Setting user to %s' % _user


def addUser(username):
    ''' Creates a non-root user to use for serving applications
    '''

    sudo('useradd -m %s' % username)
    sudo('passwd %s' % username)




def installBase(verbose=False):
    ''' Installs some of the core components needed: python, git, build-essential, unzip
    '''

    with settings(warn_only=True):

        packages = [
            'build-essential',
            'subversion',
            'git',
            'unzip',
            'supervisor'
        ]

        packagelist = ' '.join(packages)

        _remote_cmd('sudo apt-get -y install %s' % packagelist, verbose)


def configureSupervisor(verbose=False):
    ''' Updates the supervisor config file to provide the web interface on port 9999
    '''

    with settings(warn_only=True):

        put('config/supervisord.conf.web', 'supervisord.conf')
        _remote_cmd('sudo mv supervisord.conf /etc/supervisor/supervisord.conf', verbose)
        _remote_cmd('sudo service supervisor stop', verbose)
        _remote_cmd('sudo service supervisor start', verbose)



def restartAll():

    run('sudo service nginx restart')
    run('sudo supervisorctl reload')



def printssh():
    ''' prints a simple ssh command to terminal & the clipboard
    '''

    if env.key_filename:


        print 'ssh -i %s root@%s' % (env.key_filename, env.host_string)
        local('echo "ssh -i %s root@%s" | pbcopy ' % (env.key_filename, env.host_string))

    else:
        print 'ssh root@%s' % (env.host_string)
        local('echo "ssh root@%s" | pbcopy ' % (env.host_string))



def printhttp():
    ''' prints a simple http command to terminal & the clipboard
    '''

    print 'http://%s' % (env.host_string)
    local('echo "http://%s" | pbcopy ' % (env.host_string))


#endregion

#region internal methods

def _updatePackages(verbose):
    ''' Runs system update commands
    '''

    _remote_cmd('sudo apt-get -y update', verbose)


def _upgradePackages(verbose):
    ''' Runs system upgrade commands
    '''

    _remote_cmd('sudo apt-get -y upgrade', verbose)


def _remote_cmd(cmd, verbose=False):

    if verbose:
        with settings(warn_only=True):
            return run(cmd, pty = True)

    else:

        with hide('output','running','warnings', 'stdout', 'stderr'), settings(warn_only=True):
            return run(cmd, pty = True)


def _systemInformation():

    print(green(_remote_cmd('whoami')))
    print(red(_remote_cmd('uname -a')))
    print(blue(_remote_cmd('lsb_release -a')))

    if 'p' in env.keys():
        env.p.systemInformation()


def _importProvider(provider_name):
    if provider_name == 'do':
        print(green('Using digital ocean as provider'))
        from fabriccloud import digitalocean as p

    elif provider_name == 'vagrant':
        print(green('Using vagrant as provider'))
        from fabriccloud import vagrant as p

    elif provider_name == 'aws':
        print(green('Using AWS as provider'))
        from fabriccloud import aws as p

    else:
        print(yellow('No provider specified, using vagrant as default'))
        from fabriccloud import vagrant as p

    return p


#endregion

