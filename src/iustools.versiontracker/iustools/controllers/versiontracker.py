"""versiontracker controller class to expose commands for iustools."""

from cement.core.controller import CementController, expose
from iustools.model.versiontracker import VersiontrackerModel
from cement.core.namespace import get_config
from iustools.lib.upstream import package, packages, latest 
from iustools.lib.ius import ius_stable, ius_testing
from iustools.lib.ver_compare import vcompare

class colors:
    red = '\033[91m'
    green = '\033[92m'
    blue = '\033[94m'
    end = '\033[0m'

config = get_config()

class VersiontrackerController(CementController):

    @expose()
    def ossvt(self):

        try:
            pkg = package(self.cli_args[1])
        except IndexError:
            pkg = packages()

        if pkg:
            # Print out our Packages and Info
            print config['versiontracker']['layout'] % config['versiontracker']['layout_titles']
            print '='*75

            for p in pkg:
                upstream_ver = latest(p)
                ius_ver = ius_stable(p['name'])

                # Do the actual version comparisons
                compare = vcompare(ius_ver, upstream_ver)
                if compare:
                    status = 'outdated'
                    color = colors.red

                    # Since its out of date we should check testing
                    try:
                        ius_test = ius_testing(p['name'])
                        compare_testing = vcompare(ius_test, upstream_ver)
                        if not compare_testing:
                            ius_ver = ius_test
                            status = 'testing'
                            color = colors.blue

                    # If we got a IndexError testing did not have the package
                    except IndexError:
                        pass

                else:
                    status = 'up2date'
                    color = colors.green

                print config['versiontracker']['layout'] % (p['name'], ius_ver, upstream_ver, color + status + colors.end)

        else:
            print 'Not a valid package name'    
