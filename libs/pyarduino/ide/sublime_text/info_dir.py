#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals

import os


def get_current_dir_path():
    return os.path.dirname(os.path.realpath(__file__))


def get_preset_dir_path():
    cur_dir_path = get_current_dir_path()
    preset_dir_path = os.path.join(cur_dir_path, 'preset')
    return os.path.abspath(preset_dir_path)
