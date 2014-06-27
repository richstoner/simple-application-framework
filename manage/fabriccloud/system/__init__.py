
__author__ = 'stonerri'

from fabric.api import *
from fabric.colors import *
from fabric.contrib.files import *

from fabric.context_managers import shell_env

from ..base import *

#region external commands - exposed to fabric

def installNginx(verbose=False):
    ''' Installs nginx + extras
    '''

    with settings(warn_only=True):

        packages = [
            'nginx-extras'
        ]

        packagelist = ' '.join(packages)

        _remote_cmd('sudo apt-get -y install %s' % packagelist, verbose)


def startNginx(verbose=False):
    ''' Starts nginx
    '''

    _remote_cmd('sudo service nginx start', verbose)


def configureNginx(verbose=False):
    ''' Configures nginx to use the configuration file in ./manage/config
    '''

    _remote_cmd('sudo mv /etc/nginx/nginx.conf /etc/nginx/conf.old', verbose)
    _remote_cmd('sudo ln -s /vagrant/manage/config/nginx.conf.default /etc/nginx/nginx.conf', verbose)


def installApache(verbose=False):
    ''' Installs apache 2 + mod_wsgi for serving python apps
    '''

    with settings(warn_only=True):

        packages = [
            'apache2',
            'libapache2-mod-wsgi'
        ]

        packagelist = ' '.join(packages)

        _remote_cmd('sudo apt-get -y install %s' % packagelist, verbose)

        # configure apache
        _remote_cmd('a2enmod headers', verbose)
        _remote_cmd('a2enmod wsgi', verbose)





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

        _remote_cmd('sudo apt-get -y install %s' % packagelist, verbose)



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

    if exists(os.path.join('/vagrant/server', 'apps', appname)):

        # run git pull
        with cd('/vagrant/server/apps/%s'%(appname)):

            pullstring = 'git pull origin master'

            run(pullstring)

    else:

        # run git clone

        clonestring = 'git clone %s /vagrant/server/apps/%s' % (giturl, appname)

        _remote_cmd(clonestring)


def updateApp(appname):
    '''

    :param appname:
    :param giturl:
    :return:
    '''

    if exists(os.path.join('/vagrant/server', 'apps', appname)):

        # run git pull
        with cd('/vagrant/server/apps/%s'%(appname)):

            pullstring = 'git pull origin master'

            run(pullstring)








def enableApp(appname):
    """
    Takes an app located in the server/apps folder and configures nginx, supervisor, and pip to run it
    """


    if exists(os.path.join('/vagrant/server', 'apps', appname)):

        #region nginx configuration

        # link nginx site to sites-available & sites-enabled
        nginx_source_path = os.path.join('/vagrant/server', 'apps', appname, 'nginx.conf')

        if exists(nginx_source_path):

            nginx_sites_avail = '/etc/nginx/sites-available/%s' % appname
            nginx_sites_enable = '/etc/nginx/sites-enabled/%s' % appname

            if exists(nginx_sites_enable) or exists(nginx_sites_avail):
                print(red('%s already enabled' %appname))

            else:

                run('sudo ln -s %s %s' % (nginx_source_path, nginx_sites_avail))
                run('sudo ln -s %s %s' % (nginx_source_path, nginx_sites_enable))

            sudo('service nginx configtest')
            sudo(' service nginx restart')

        #endregion



        #region pip configuration

        if exists(os.path.join('/vagrant/server', 'apps', appname, 'requirements.txt')):

            _python_cmd('pip install -r %s' % os.path.join('/vagrant/server', 'apps', appname, 'requirements.txt'),
                        True)


        #endregion



        #region supervisor configuration

        supervisor_config = os.path.join('/vagrant/server', 'apps', appname, 'supervisor.conf')

        if exists(supervisor_config):

            supervisor_enable = '/etc/supervisor/conf.d/%s.conf' % appname

            if exists(supervisor_enable):
                print(red('%s super config already enabled' % appname))

            else:
                run('sudo ln -s %s %s' % (supervisor_config, supervisor_enable))

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

    run('sudo service nginx configtest')
    run('sudo service nginx restart')





#endregion


#region internals

def _remote_cmd(cmd, verbose=False):

    if verbose:
        with settings(warn_only=True):
            return run(cmd, pty = True)

    else:

        with hide('output','running','warnings', 'stdout', 'stderr'), settings(warn_only=True):
            return run(cmd, pty = True)


def _python_cmd(cmd, verbose=False):

    with shell_env(PATH="/home/flaskuser/miniconda/bin:$PATH"):

        if verbose:
            with settings(warn_only=True):
                return run(cmd, pty = True)

        else:

            with hide('output','running','warnings', 'stdout', 'stderr'), settings(warn_only=True):
                return run(cmd, pty = True)






#endregion
