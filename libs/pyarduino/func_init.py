#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals

import os

from . import base


def init_settings(file_name):
    settings_dir_path = base.info_dir.get_settings_dir_path()
    if not os.path.isdir(settings_dir_path):
        os.makedirs(settings_dir_path)
    settings_file_path = os.path.join(settings_dir_path, file_name)
    settings_file = base.cls_file.SettingsFile(settings_file_path)
    return settings_file
