__author__ = 'stonerri'

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
    ''' Installs Celery, rabbitMQ, and flower
    '''
    with settings(warn_only=True):

        packages = [
            'rabbitmq-server'
        ]

        packagelist = ' '.join(packages)

        _remote_cmd('sudo apt-get -y install %s' % packagelist, verbose)



def installCelery(verbose=False):
    ''' Installs Celery, rabbitMQ, and flower
    '''
    with settings(warn_only=True):

        packages = [
            'celery',
            'flower'
        ]

        for each_package in packages:
             _python_cmd('pip install %s' % each_package, verbose)






#endregion



#region internals

def _remote_cmd(cmd, verbose=False):

    with prefix('export PATH="~/miniconda/bin:$PATH"'):

        if verbose:
            with settings(warn_only=True):
                return run(cmd, pty = True)

        else:

            with hide('output','running','warnings', 'stdout', 'stderr'), settings(warn_only=True):
                return run(cmd, pty = True)


def _python_cmd(cmd, verbose=False):

    with prefix('export PATH="~/miniconda/envs/server/bin:$PATH"'):

        if verbose:
            with settings(warn_only=True):
                return run(cmd, pty = True)

        else:

            with hide('output','running','warnings', 'stdout', 'stderr'), settings(warn_only=True):
                return run(cmd, pty = True)



#endregion
