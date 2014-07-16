__author__ = 'stonerri'

from fabric.api import *
from fabric.colors import *
from fabric.contrib.files import *
from fabric.context_managers import shell_env

from ..base import *

#region fabric methods

default_app_path = '/home/cdsaadmin/apps'

def update(verbose=False):
    ''' Runs update & upgrade for system packages
    '''
    _updatePackages(verbose)
    _upgradePackages(verbose)


def rsync(verbose=False):
    ''' Synchronizes the root folder with /vagrant on the remote host (emulates a vagrant config)
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
            'supervisor',
            'libffi-dev'
        ]

        packagelist = ' '.join(packages)

        _remote_sudo('apt-get -y install %s' % packagelist, verbose)


def configureSupervisor(verbose=False):
    ''' Updates the supervisor config file to provide the web interface on port 9999
    '''

    with settings(warn_only=True):

        put('config/supervisord.conf.web', 'supervisord.conf')
        _remote_sudo('mv supervisord.conf /etc/supervisor/supervisord.conf', verbose)
        _remote_sudo('service supervisor stop', verbose)
        _remote_sudo('service supervisor start', verbose)



def restartAll():
    """ Restarts nginx and supervisor
    """

    _remote_sudo('service nginx restart')
    _remote_sudo('supervisorctl reload')



def printssh():
    ''' prints a simple ssh command to terminal & the clipboard
    '''

    if env.key_filename:

        print 'ssh -i %s %s@%s' % (env.key_filename, env.user, env.host_string)
        local('echo "ssh -i %s %s@%s" | pbcopy ' % (env.key_filename, env.user, env.host_string))

    else:
        print 'ssh %s@%s' % (env.user, env.host_string)
        local('echo "ssh %s@%s" | pbcopy ' % (env.user, env.host_string))



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

    _remote_sudo('apt-get -y upgrade', verbose)


def _remote_cmd(cmd, verbose=False):

    if verbose:
        with settings(warn_only=True):
            return run(cmd, pty = True)

    else:

        with hide('output','running','warnings', 'stdout', 'stderr'), settings(warn_only=True):
            return run(cmd, pty = True)


def _remote_sudo(cmd, verbose=False):

    if verbose:
        with settings(warn_only=True):
            return sudo(cmd, pty = True)

    else:

        with hide('output','running','warnings', 'stdout', 'stderr'), settings(warn_only=True):
            return sudo(cmd, pty = True)


def _python_cmd(cmd, verbose=False):

    with shell_env(PATH="/home/%s/miniconda/bin:$PATH" % (env.user)):

        if verbose:
            with settings(warn_only=True):
                return run(cmd, pty = True)

        else:

            with hide('output','running','warnings', 'stdout', 'stderr'), settings(warn_only=True):
                return run(cmd, pty = True)



def installNginx(verbose=False):
    ''' Installs nginx + extras
    '''

    with settings(warn_only=True):

        packages = [
            'nginx-extras'
        ]

        packagelist = ' '.join(packages)

        _remote_sudo('apt-get -y install %s' % packagelist, verbose)


def startNginx(verbose=False):
    ''' Starts nginx
    '''

    _remote_sudo('service nginx start', verbose)


def configureNginx(verbose=False):
    ''' Configures nginx to use the configuration file in ./manage/config
    '''

    path = os.path.join(os.path.abspath(os.curdir), 'config/nginx.conf.default')
    put(path)
    _remote_sudo('mv /etc/nginx/nginx.conf /etc/nginx/conf.old', verbose)
    _remote_sudo('mv nginx.conf.default /etc/nginx/nginx.conf', verbose)


def installApache(verbose=False):
    ''' Installs apache 2 + mod_wsgi for serving python apps
    '''

    with settings(warn_only=True):

        packages = [
            'apache2',
            'libapache2-mod-wsgi'
        ]

        packagelist = ' '.join(packages)

        _remote_sudo('apt-get -y install %s' % packagelist, verbose)

        # configure apache
        _remote_sudo('a2enmod headers', verbose)
        _remote_sudo('a2enmod wsgi', verbose)





#endregion


#region externals

def installConda(verbose=False):
    ''' Installs miniconda installation (requires user interaction)
    '''

    run('wget http://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh')
    run('chmod +x Miniconda-latest-Linux-x86_64.sh')
    run('./Miniconda-latest-Linux-x86_64.sh -b')


def installCondaAsUser(_user='flaskuser', verbose=False):
    ''' Installs miniconda installation (requires user interaction)
    '''

    # sudo('whoami', user=_user)
    with cd('/home/%s' % (_user)):
        sudo('wget http://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh', user=_user)
        sudo('chmod +x Miniconda-latest-Linux-x86_64.sh', user=_user)
        sudo('/home/%s/Miniconda-latest-Linux-x86_64.sh -b' % (_user), user=_user)


def testConda(verbose=False):
    ''' Verifies the conda installation is correct
    '''

    _remote_cmd('export', verbose)
    _remote_cmd('which python', verbose)
    _python_cmd('conda info', verbose)


def installPythonCore(verbose=False):
    '''

    :param verbose:
    :return:
    '''

    _python_cmd('conda install --yes anaconda', verbose)
    _python_cmd('conda install --yes opencv', verbose)
    _python_cmd('conda install --yes pip', verbose)



#
# def updateConda(verbose=False):
#     ''' Updates the packages in the base anaconda environment
#     '''
#
#     _python_cmd('conda update conda', verbose)
#     _python_cmd('conda update anaconda', verbose)



def installRabbitMQ(verbose=False):
    ''' Installs RabbitMQ
    '''
    with settings(warn_only=True):

        packages = [
            'rabbitmq-server'
        ]

        packagelist = ' '.join(packages)

        _remote_sudo('apt-get -y install %s' % packagelist, verbose)



def installMongoDB(verbose=False):
    ''' Installs MongoDB with default authentication
    '''

    with settings(warn_only=True):

        sudo('apt-key adv --keyserver keyserver.ubuntu.com --recv 7F0CEB10')
        sudo('echo "deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen" | tee -a /etc/apt/sources.list.d/10gen.list')
        sudo('apt-get update')
        sudo('apt-get install mongodb-10gen')



def installElasticsearch(verbose=False):
    ''' Installs elasticsearch
    '''

    with settings(warn_only=True):

        packages = [
            'openjdk-7-jre-headless'
        ]

        packagelist = ' '.join(packages)

        _remote_cmd('sudo apt-get -y install %s' % packagelist, verbose)
        _remote_cmd('wget https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-1.0.1.deb', verbose)
        _remote_cmd('dpkg -i elasticsearch-1.0.1.deb', verbose)
        _remote_cmd('sudo service elasticsearch start', verbose)




def addApp(appname, giturl):
    '''

    :param appname:
    :param giturl:
    :return:
    '''

    if not exists(os.path.join(default_app_path)):
        run('mkdir -p %s' % (default_app_path))

    if exists(os.path.join(default_app_path, appname)):

        # run git pull
        with cd('%s/%s'%(default_app_path, appname)):

            pullstring = 'git pull origin master'
            run(pullstring)

    else:

        # run git clone
        clonestring = 'git clone %s %s/%s' % (giturl, default_app_path, appname)
        _remote_cmd(clonestring)


def updateApp(appname):
    '''

    :param appname:
    :param giturl:
    :return:
    '''

    if exists(os.path.join(default_app_path, appname)):

        # run git pull
        with cd('%s/%s'%(default_app_path, appname)):

            pullstring = 'git pull origin master'

            run(pullstring)








def enableApp(appname):
    """
    Takes an app located in the server/apps folder and configures nginx, supervisor, and pip to run it
    """


    if exists(os.path.join(default_app_path, appname)):

        _python_cmd('pip uninstall cherrypy', True)

        #region nginx configuration

        # link nginx site to sites-available & sites-enabled
        nginx_source_path = os.path.join(default_app_path, appname, 'nginx.conf')

        if exists(nginx_source_path):

            nginx_sites_avail = '/etc/nginx/sites-available/%s' % appname
            nginx_sites_enable = '/etc/nginx/sites-enabled/%s' % appname

            if exists(nginx_sites_enable) or exists(nginx_sites_avail):
                print(red('%s already enabled' %appname))

            else:

                sudo('ln -s %s %s' % (nginx_source_path, nginx_sites_avail))
                sudo('ln -s %s %s' % (nginx_source_path, nginx_sites_enable))

            sudo('service nginx configtest')
            sudo('service nginx restart')

        #endregion



        #region pip configuration

        

        if exists(os.path.join(default_app_path, appname, 'requirements.txt')):

            _python_cmd('pip install --upgrade --no-use-wheel -r %s' % os.path.join(default_app_path, appname, 'requirements.txt'),
                        True)


        #endregion



        #region supervisor configuration

        supervisor_config = os.path.join(default_app_path, appname, 'supervisor.conf')

        sed(supervisor_config, '##SAFUSER##', env.user)
        sed(supervisor_config, '##SAFAPPS##', default_app_path)

        if exists(supervisor_config):

            supervisor_enable = '/etc/supervisor/conf.d/%s.conf' % appname

            if exists(supervisor_enable):
                print(red('%s super config already enabled' % appname))

            else:
                sudo('ln -s %s %s' % (supervisor_config, supervisor_enable))

            sudo('supervisorctl reread')
            sudo('supervisorctl add %s' % appname)
            sudo('supervisorctl stop %s:' % appname)

        #endregion

    else:
        print 'invalid app name'



def disableApp(appname):
    """
    Disables an app, provided as by parameter
    """

    nginx_sites_avail = '/etc/nginx/sites-available/%s' % appname
    nginx_sites_enable = '/etc/nginx/sites-enabled/%s' % appname
    supervisor_enable = '/etc/supervisor/conf.d/%s.conf' % appname

    links_to_remove = [nginx_sites_avail, nginx_sites_enable, supervisor_enable]

    sudo('supervisorctl stop %s:*' % appname)
    sudo('supervisorctl remove %s' % appname)

    for link in links_to_remove:
        sudo('rm %s*' % link)

    sudo('service nginx configtest')
    sudo('service nginx restart')





#endregion





def _systemInformation():

    print(green(_remote_cmd('whoami')))
    print(red(_remote_cmd('uname -a')))
    print(blue(_remote_cmd('lsb_release -a')))
    print(yellow(_remote_cmd('df -h')))

    if 'p' in env.keys():
        env.p.systemInformation()


def _importProvider(provider_name):
    if provider_name == 'do':
        print(green('Using digital ocean as provider'))
        from ..provider import digitalocean as p

    elif provider_name == 'cdsa':
        print(green('Using cdsa as provider'))
        from ..provider import cdsa as p


    elif provider_name == 'vagrant':
        print(green('Using vagrant as provider'))
        from ..provider import vagrant as p

    elif provider_name == 'aws':
        print(green('Using AWS as provider'))
        from ..provider import aws as p

    elif provider_name == 'azure':
        print(green('Using Azure as provider'))
        from ..provider import azure as p

    elif provider_name == 'linode':
        print(green('Using Linode  as provider'))
        from ..provider import linode as p

    else:
        print(yellow('No provider specified, using vagrant as default'))
        from ..provider  import vagrant as p



    return p


def mountStatus():

    if 'p' in env.keys():
        env.p.mountStatus()


#endregion

