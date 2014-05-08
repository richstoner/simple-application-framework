__author__ = 'stonerri'

from fabric.api import *
from fabric.colors import *
from fabric.contrib.files import *

from base import *

#region externals

def installConda(verbose=False):
    ''' Installs miniconda installation (requires user interaction)
    '''

    run('wget http://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh')
    run('chmod +x Miniconda-latest-Linux-x86_64.sh')
    run('./Miniconda-latest-Linux-x86_64.sh')


def testConda(verbose=False):
    ''' Verifies the conda installation is correct
    '''

    _remote_cmd('export', verbose)
    _remote_cmd('which python', verbose)
    _remote_cmd('conda info', verbose)


def installCondaBase(verbose=False):
    ''' Creates a new server environment to ~/miniconda/envs/server
    '''

    _remote_cmd('conda create -n py27 server ', verbose)


def installAnaconda(verbose=False):
    ''' Installs python dependencies for anaconda tools to ~/miniconda/envs/server
    '''

    _remote_cmd('conda create -n server anaconda', verbose)


def updateConda(verbose=False):
    ''' Updates the packages in the base anaconda environment
    '''

    _remote_cmd('conda update conda', verbose)
    _remote_cmd('conda update anaconda', verbose)



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

            run('sudo service nginx configtest')
            run('sudo service nginx restart')

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
            sudo('supervisorctl stop %s' % appname)

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

    sudo('supervisorctl stop %s' % appname)
    sudo('supervisorctl remove %s' % appname)

    for link in links_to_remove:
        sudo('rm %s' % link)

    run('sudo service nginx configtest')
    run('sudo service nginx restart')





#endregion



#region internals

def _remote_cmd(cmd, verbose=False):

    with prefix('export PATH="/home/flaskuser/miniconda/bin:$PATH"'):

        if verbose:
            with settings(warn_only=True):
                return run(cmd, pty = True)

        else:

            with hide('output','running','warnings', 'stdout', 'stderr'), settings(warn_only=True):
                return run(cmd, pty = True)


def _python_cmd(cmd, verbose=False):

    with prefix('export PATH="/home/flaskuser/miniconda/envs/server/bin:$PATH"'):

        if verbose:
            with settings(warn_only=True):
                return run(cmd, pty = True)

        else:

            with hide('output','running','warnings', 'stdout', 'stderr'), settings(warn_only=True):
                return run(cmd, pty = True)



#endregion
