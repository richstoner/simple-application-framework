__author__ = 'stonerri'

from fabric.contrib.files import *
from base import *
import os

#region external commands - exposed to fabric

def installFlask(verbose=False):
    ''' installs python modules needed to run flask on either mod_wsgi or nginx (needs user interaction)
    '''

    with settings(warn_only=True):

        packages = [
            'flask',
            'flask-oauth',
            'sqlalchemy',
            'gunicorn'
        ]

        for each_package in packages:
             _python_cmd('pip install %s' % each_package, verbose)


def enableFlaskApp(appname):

    if exists(os.path.join('/vagrant/server', 'flaskapp', appname)):

        print 'found'

    else:
        print 'invalid app name'



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