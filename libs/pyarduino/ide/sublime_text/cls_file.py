#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals

import pyarduino


class MenuFile(pyarduino.base.cls_file.JSONFile):
    def __init__(self, path):
        super(MenuFile, self).__init__(path)

    def update(self, data, visible=True):
        if not visible:
            self.write('[\n]')
        else:
            self.data = data
            self.save()
