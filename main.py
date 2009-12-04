#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from os.path import abspath, dirname, join
sys.path.insert(0, abspath(join(dirname(__file__), 'local_apps')))
sys.path.insert(0, abspath(join(dirname(__file__), 'external_apps')))
sys.path.insert(0, abspath(join(dirname(__file__), 'external_libs')))
sys.path.insert(0, abspath(dirname(__file__)))

from common.appenginepatch.main import main

if __name__ == '__main__':
    main()
