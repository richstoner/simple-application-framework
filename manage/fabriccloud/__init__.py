__author__ = 'stonerri'

from .base import *

def last():
    ''' inline argument, uses the last host saved by the user

    This host is defined in the last.ini file, located in the same directory as the fabfile.py

    e.g. :code:`fab last somecommand`


    '''

    from ConfigParser import SafeConfigParser

    parser = SafeConfigParser()
    parser.read('last.ini')
    env.user = parser.get('last', 'user')
    env.host_string = parser.get('last', 'host_string')

    provider(parser.get('last', 'provider'))



def save():
    ''' inline argument, saves the host information to a file for later use

    The host & user information are stored in the last.ini file, located in the same directory as the fabfile.py

    e.g. :code:`fab provider:aws somecommand save`

    '''

    from ConfigParser import SafeConfigParser

    parser = SafeConfigParser()
    parser.add_section('last')
    parser.set('last', 'host_string', env.host_string)
    parser.set('last', 'user', env.user)
    parser.set('last', 'provider', env.provider)
    parser.write(open('last.ini', 'w'))

