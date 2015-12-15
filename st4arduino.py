#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals

import os
import sys

import sublime
import sublime_plugin


cur_dir = os.path.dirname(os.path.realpath(__file__))
libs_dir = os.path.join(cur_dir, 'libs')
if libs_dir not in sys.path:
    sys.path.append(libs_dir)

subl_ver = int(sublime.version())
if subl_ver < 3000:
    import stino
else:
    def plugin_loaded():
        from . import stino


