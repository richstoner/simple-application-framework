from __future__ import with_statement

from fabric.api import *
from fabric.contrib.console import *
from fabric.contrib.files import *

import fabriccloud

def last():
    ''' Use the last target configuration saved
    '''

    from ConfigParser import SafeConfigParser

    parser = SafeConfigParser()
    parser.read('last.ini')
    env.user = parser.get('last', 'user')
    env.host_string = parser.get('last', 'host_string')

    provider(parser.get('last', 'provider'))



def save():
    ''' Save the target configuration
    '''

    from ConfigParser import SafeConfigParser

    parser = SafeConfigParser()
    parser.add_section('last')
    parser.set('last', 'host_string', env.host_string)
    parser.set('last', 'user', env.user)
    parser.set('last', 'provider', env.provider)
    parser.write(open('last.ini', 'w'))






