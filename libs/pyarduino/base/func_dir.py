#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals

import sys
import os


# 将包所在的目录加入sys.path中
def add_package_to_sys_path():
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    parent_dir = os.path.dirname(cur_dir)
    if parent_dir not in sys.path:
        sys.path.append(parent_dir)
