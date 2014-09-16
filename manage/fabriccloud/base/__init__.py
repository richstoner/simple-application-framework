__author__ = 'stonerri'

from fabric.api import *
from fabric.colors import *
from fabric.contrib.files import *
from fabric.context_managers import shell_env

from ..base import *

from ConfigParser import SafeConfigParser

parser = SafeConfigParser()
parser.read('server.ini')

# we replace config variables with these
app_path = parser.get('path', 'apppath')
conda_path = parser.get('path', 'condapath')
sync_path = parser.get('path', 'syncpath')
saf_host_name = parser.get('general', 'safhost')
saf_user = parser.get('general', 'safuser')

mongo_root_password = parser.get('database', 'rootpassword')
mongo_user_password = parser.get('database', 'girderpass')


def debug():
    verbose = True
    # configure supervisord

    sudo('mkdir /applications')
    sudo('chown -R %s:%s /applications' % (saf_user, saf_user))



def installFramework():

    verbose = True

    # apt get things
    _updatePackages(verbose)

    # apt-get upgrade things
    _upgradePackages(verbose)

    # create user to run all things
    # Creates user + home directory, adds to sudo

    if saf_user != 'vagrant':
        _newuser(saf_user, saf_user)

    # installs core apt things
    _installBase(verbose)

    # installs nginx things
    _installNginx(verbose)

    # restarts nginx and supervisor
    _restartBase(verbose)


#region Install Framework Methods

def _updatePackages(verbose):
    ''' Runs system update commands
    '''
    _remote_cmd('sudo apt-get -y update', verbose)

def _upgradePackages(verbose):
    ''' Runs system upgrade commands
    '''
    _remote_sudo('apt-get -y upgrade', verbose)

def _newuser(admin_username, admin_password):

    with settings(warn_only=True):

        # Create the admin group and add it to the sudoers file
        admin_group = 'admin'
        sudo('addgroup {group}'.format(group=admin_group))
        sudo('echo "%{group} ALL=(ALL) ALL" >> /etc/sudoers'.format(
            group=admin_group))

        # Create the new admin user (default group=username); add to admin group
        sudo('adduser {username} --disabled-password --gecos ""'.format(
            username=admin_username))
        sudo('adduser {username} {group}'.format(
            username=admin_username,
            group=admin_group))

        # Set the password for the new admin user
        sudo('echo "{username}:{password}" | chpasswd'.format(
            username=admin_username,
            password=admin_password))



def _installBase(verbose=False):
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

        # configure supervisord

        put('config/supervisord.conf.web', 'supervisord.conf')
        _remote_sudo('mv supervisord.conf /etc/supervisor/supervisord.conf', verbose)
        _remote_sudo('service supervisor stop', verbose)
        _remote_sudo('service supervisor start', verbose)








def _installNginx(verbose=False):
    ''' Installs nginx + extras
    '''

    with settings(warn_only=True):

        packages = [
            'nginx-extras'
        ]

        packagelist = ' '.join(packages)

        _remote_sudo('apt-get -y install %s' % packagelist, verbose)

        path = os.path.join(os.path.abspath(os.curdir), 'config/nginx.conf.default')
        put(path)

        sed('nginx.conf.default', '##SAFHOST##', saf_host_name)

        _remote_sudo('mv /etc/nginx/nginx.conf /etc/nginx/conf.old', verbose)
        _remote_sudo('mv nginx.conf.default /etc/nginx/nginx.conf', verbose)

        _remote_sudo('service nginx stop', verbose)
        _remote_sudo('service nginx start', verbose)


def _restartBase(verbose=True):
    """ Restarts nginx and supervisor
    """

    _remote_sudo('service nginx restart', verbose)
    _remote_sudo('supervisorctl reload', verbose)







#endregion


def installPython():

    verbose = True

    env.user = saf_user

    _installConda(verbose)

    _installPythonCore(verbose)

    _testConda(verbose)


#region Install Python methods


def _installConda(verbose=False):
    ''' Installs miniconda installation (requires user interaction)
    '''

    run('wget http://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh')
    run('chmod +x Miniconda-latest-Linux-x86_64.sh')
    run('./Miniconda-latest-Linux-x86_64.sh -b')




def _installPythonCore(verbose=False):
    '''
    :param verbose:
    :return:
    '''

    _python_cmd('conda install --yes anaconda', verbose)
    _python_cmd('conda install --yes opencv', verbose)
    _python_cmd('conda install --yes cffi', verbose)
    _python_cmd('conda install --yes pip', verbose)



def _testConda(verbose=False):
    ''' Verifies the conda installation is correct
    '''

    _remote_cmd('export', verbose)
    _remote_cmd('which python', verbose)
    _python_cmd('conda info', verbose)



def _python_cmd(cmd, verbose=False):



    with shell_env(PATH="/%s/bin:$PATH" % (conda_path)):

        if verbose:
            with settings(warn_only=True):
                return run(cmd, pty = True)

        else:
            with hide('output','running','warnings', 'stdout', 'stderr'), settings(warn_only=True):
                return run(cmd, pty = True)


#endregion





def installMongo():

    _installMongoDB()


def _installMongoDB(verbose=False):

    ''' Installs MongoDB with default authentication
    '''

    with settings(warn_only=True):

        sudo('apt-key adv --keyserver keyserver.ubuntu.com --recv 7F0CEB10')
        sudo('echo "deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen" | tee -a /etc/apt/sources.list.d/10gen.list')
        sudo('apt-get -y update')
        sudo('apt-get -y install mongodb-org')

        sudo('mkdir -p /mongo/db')
        sudo('mkdir -p /mongo/log')

        sudo('chown -R mongodb:mongodb /mongo/db')
        sudo('chown -R mongodb:mongodb /mongo/log')


        # move mongo db into right place

        path = os.path.join(os.path.abspath(os.curdir), 'config/mongodb.girder.conf')
        put(path)

        _remote_sudo('mv -v /etc/mongod.conf /etc/mongod.conf.old', True)
        _remote_sudo('mv -v ./mongodb.girder.conf /etc/mongod.conf', True)

        sudo('service mongod stop')
        sudo('service mongod start')


        path = os.path.join(os.path.abspath(os.curdir), 'config/mongo_config.js')
        put(path, '.')

        path = os.path.join(os.path.abspath(os.curdir), 'config/mongo_root_config.js')
        put(path, '.')

        sed('mongo_root_config.js', '##SAFROOTPASS##', mongo_root_password)
        sed('mongo_config.js', '##SAFGIRDERPASS##', mongo_user_password)

        sudo('mongo admin mongo_root_config.js')
        sudo('mongo girder mongo_config.js')








def installGirderDepends():


    with settings(warn_only=True):


        sudo('sudo apt-get -y install python-software-properties')

        sudo('mkdir -p /assetstore')
        sudo('chown -R %s:%s /assetstore' % (saf_user, saf_user))

        sudo('add-apt-repository ppa:chris-lea/node.js')
        sudo('apt-get -y update')
        sudo('apt-get -y install nodejs')
        # sudo('npm install -g grunt grunt-cli')

        with cd('%s/girder' % (app_path)):
            run('npm install')
            run('grunt')








def installTiff():
    ''' Experimental tiff build
    :return:
    '''

    with settings(warn_only=True):

        sudo('apt-get -y install autoconf automake libtool pkg-config libgtk2.0-dev libxml2-dev libjpeg-dev liblzma-dev liblz-dev zlib1g-dev lzma libmatio-dev libexif-dev libfftw3-dev swig python-dev liborc-0.4-dev libopenjpeg-dev spawn-fcgi libsqlite3-dev')

        run('wget ftp://ftp.remotesensing.org/pub/libtiff/tiff-4.0.3.tar.gz')
        run('tar xvzf tiff-4.0.3.tar.gz')
        with cd('tiff-4.0.3'):
            run('./configure')
            run('make -j 4')
            sudo('make install')

        sudo('echo "/usr/local/lib/" >> /etc/ld.so.conf.d/local.conf')
        sudo('ldconfig')



def installOpenSlide():

    with settings(warn_only=True):

        run('git clone git://github.com/openslide/openslide.git')
        with cd('openslide'):
            run('autoreconf -i')
            run('./configure')
            run('make -j 4')
            sudo('make install')

        sudo('ldconfig')

def installVips():
    with settings(warn_only=True):

        run('wget http://www.vips.ecs.soton.ac.uk/supported/current/vips-7.40.4.tar.gz')
        run('tar xvzf vips-7.40.4.tar.gz')
        with cd('vips-7.40.4'):
            run('./configure')
            run('make -j 4')
            sudo('make install')

        sudo('ldconfig')

def installIIP():

    with settings(warn_only=True):

        run('svn checkout svn://svn.code.sf.net/p/iipimage/code/ iipimage-code')
        with cd('iipimage-code/iipsrv/trunk'):
            run('autoreconf -i')
            run('./configure --with-tiff-includes=/usr/local/include --with-tiff-libraries=/usr/local/lib')
            run('make')

        sudo('ldconfig')





def rsync(verbose=False):
    ''' Synchronizes the root folder with /vagrant on the remote host (emulates a vagrant config)
    '''
    if 'p' not in env.keys():
        env.p = _importProvider('')
        env.provider = 'vagrant'
        env.p.setDefaults()

    env.p.sync(sync_path)





def _installRabbitMQ(verbose=False):
    ''' Installs RabbitMQ
    '''
    with settings(warn_only=True):

        packages = [
            'rabbitmq-server'
        ]

        packagelist = ' '.join(packages)

        _remote_sudo('apt-get -y install %s' % packagelist, verbose)



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


def user(_user=None):
    ''' Set a specific user for the action
    '''

    if _user is None:
        _user = saf_user

    if 'p' not in env.keys():
        env.p = _importProvider('')
        env.provider = 'vagrant'
        env.p.setDefaults()

    env.user = _user

    print 'Setting user to %s' % _user








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



#region internal methods

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








# def _python_root_cmd(cmd, verbose=False):
#
#     with shell_env(PATH="/miniconda/bin:$PATH"):
#
#         if verbose:
#             with settings(warn_only=True):
#                 return run(cmd, pty = True)
#         else:
#
#             with hide('output','running','warnings', 'stdout', 'stderr'), settings(warn_only=True):
#                 return run(cmd, pty = True)
#






#endregion


#region externals



# def installPythonCoreRoot(verbose=True):
#
#     _python_root_cmd('conda install --yes anaconda', verbose)
#     _python_root_cmd('conda install --yes opencv', verbose)
#     _python_root_cmd('conda install --yes pip', verbose)
#



# def installCondaAsUser(_user='flaskuser', verbose=False):
#     ''' Installs miniconda installation (requires user interaction)
#     '''
#
#     # sudo('whoami', user=_user)
#     with cd('/home/%s' % (_user)):
#         sudo('wget http://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh', user=_user)
#         sudo('chmod +x Miniconda-latest-Linux-x86_64.sh', user=_user)
#         sudo('/home/%s/Miniconda-latest-Linux-x86_64.sh -b' % (_user), user=_user)

#
# def testConda(verbose=False):
#     ''' Verifies the conda installation is correct
#     '''
#
#     _remote_cmd('export', verbose)
#     _remote_cmd('which python', verbose)
#     _python_cmd('conda info', verbose)



#
# def updateConda(verbose=False):
#     ''' Updates the packages in the base anaconda environment
#     '''
#     _python_cmd('conda update conda', verbose)
#     _python_cmd('conda update anaconda', verbose)





# def installElasticsearch(verbose=False):
#     ''' Installs elasticsearch
#     '''
#
#     with settings(warn_only=True):
#
#         packages = [
#             'openjdk-7-jre-headless'
#         ]
#
#         packagelist = ' '.join(packages)
#
#         _remote_cmd('sudo apt-get -y install %s' % packagelist, verbose)
#         _remote_cmd('wget https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-1.0.1.deb', verbose)
#         _remote_cmd('dpkg -i elasticsearch-1.0.1.deb', verbose)
#         _remote_cmd('sudo service elasticsearch start', verbose)
#



def addApp(appname, giturl, branch='master'):
    '''

    :param appname:
    :param giturl:
    :return:
    '''

    if not exists(os.path.join(app_path)):
        run('mkdir -p %s' % (app_path))

    if exists(os.path.join(app_path, appname)):

        # run git pull
        with cd('%s/%s'%(app_path, appname)):

            pullstring = 'git pull origin %s' % branch
            run(pullstring)

    else:

        # run git clone
        clonestring = 'git clone %s %s/%s -b %s' % (giturl, app_path, appname, branch)
        _remote_cmd(clonestring)






def enable(appname):
    """
    Takes an app located in the server/apps folder and configures nginx, supervisor, and pip to run it
    """

    env.user = saf_user

    if exists(os.path.join(app_path, appname)):


        # link nginx site to sites-available & sites-enabled

        nginx_source_path = os.path.join(app_path, appname, 'nginx.saf')
        nginx_config_path = os.path.join(app_path, appname, 'nginx.conf')

        if exists(nginx_source_path):

            if exists(nginx_config_path):
                sudo('rm -vf %s' % nginx_config_path)

            sudo('cp %s %s' % (nginx_source_path, nginx_config_path))

            nginx_sites_avail = '/etc/nginx/sites-available/%s' % appname
            nginx_sites_enable = '/etc/nginx/sites-enabled/%s' % appname

            sed(nginx_config_path, '##SAFHOST##', saf_host_name)

            if exists(nginx_sites_enable) or exists(nginx_sites_avail):
                print(red('%s already enabled' %appname))
            else:
                sudo('ln -s %s %s' % (nginx_config_path, nginx_sites_avail))
                sudo('ln -s %s %s' % (nginx_config_path, nginx_sites_enable))

            sudo('service nginx configtest')
            sudo('service nginx restart')



        #pip configuration

        if exists(os.path.join(app_path, appname, 'requirements.txt')):
            _python_cmd('pip install --no-use-wheel -r %s' % os.path.join(app_path, appname, 'requirements.txt'), True)

        # supervisor config
        supervisor_template = os.path.join(app_path, appname, 'supervisor.saf')
        supervisor_config = os.path.join(app_path, appname, 'supervisor.conf')

        sudo('rm -vf %s' % supervisor_config)
        sudo('cp %s %s' % (supervisor_template, supervisor_config))

        sed(supervisor_config, '##SAFUSER##', saf_user)
        sed(supervisor_config, '##SAFAPPS##', app_path)
        sed(supervisor_config, '##SAFAPPNAME##', appname)

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
        print('invalid app name')



def disable(appname):
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
        from ..provider import vagrant as p



    return p


def mountStatus():

    if 'p' in env.keys():
        env.p.mountStatus()


#endregion

