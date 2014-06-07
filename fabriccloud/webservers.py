__author__ = 'stonerri'

from base import *

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



#region internals

def _remote_cmd(cmd, verbose=False):

    if verbose:
        with settings(warn_only=True):
            return run(cmd, pty = True)

    else:

        with hide('output','running','warnings', 'stdout', 'stderr'), settings(warn_only=True):
            return run(cmd, pty = True)


def _python_cmd(cmd, verbose=False):

    with prefix('export PATH="/root/miniconda/envs/server/bin:$PATH"'):

        if verbose:
            with settings(warn_only=True):
                return run(cmd, pty = True)

        else:

            with hide('output','running','warnings', 'stdout', 'stderr'), settings(warn_only=True):
                return run(cmd, pty = True)




#endregion
