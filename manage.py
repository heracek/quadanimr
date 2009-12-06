#!/usr/bin/env python
import sys
from os.path import abspath, dirname, join
sys.path.insert(0, abspath(join(dirname(__file__), 'local_apps')))
sys.path.insert(0, abspath(join(dirname(__file__), 'external_apps')))
sys.path.insert(0, abspath(join(dirname(__file__), 'external_libs')))
sys.path.insert(0, abspath(dirname(__file__)))

import warnings
warnings.filterwarnings("ignore")

if __name__ == '__main__':
    from common.appenginepatch.aecmd import setup_env
    setup_env(manage_py_env=True)

    # Recompile translation files
    from mediautils.compilemessages import updatemessages
    updatemessages()

    # Generate compressed media files for manage.py update
    import sys
    from mediautils.generatemedia import updatemedia
    if len(sys.argv) >= 2 and sys.argv[1] == 'update':
        updatemedia(True)

    import settings
    from django.core.management import execute_manager
    execute_manager(settings)
