"""
This bootstrap module should be used to setup parts of the ossvt plugin
that need to exist before all controllers are loaded.  It is best used to 
define/register hooks, setup namespaces, and the like.  

"""

from pkg_resources import get_distribution
from cement.core.namespace import CementNamespace, register_namespace

VERSION = get_distribution('iustools.ossvt').version

# Setup the 'ossvt' namespace object
ossvt = CementNamespace(
    label='ossvt', 
    description='Ossvt Plugin for Iustools',
    version=VERSION,
    controller='OssvtController',
    provider='iustools'
    )

# Disable Launchpad Tickets for now
ossvt.config['with_launchpad'] = False
# Show up to date software
ossvt.config['with_up2date'] = True
# Directory where Package Configuration is kept
ossvt.config['pkg_dir'] = '/usr/share/ossvt/pkgs/'
ossvt.config['name'] = False

ossvt.options.add_option('--name', action='store', dest='name',
    help='IUS Package Name')

# Officialize and register the namespace
register_namespace(ossvt)

