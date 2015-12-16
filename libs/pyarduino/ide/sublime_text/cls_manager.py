#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals

import os

from . import info_dir
from . import cls_menu


sub_menu_caption_list = ['Sketchbook',
                         'Examples',
                         'Include Library',
                         'Board',
                         'Board Options',
                         'Programmer',
                         'Serial Port',
                         'Language',
                         'Board Manager',
                         'Library Manager']


class MenuManager(object):
    def __init__(self):
        self.visible = True
        self.main_menu = cls_menu.Menu('Arduino')
        self.empty_main_menu = cls_menu.Menu('Arduino')
        self.submenu_list = []

        self.init_main_menu()
        self.init_empty_main_menu()
        self.init_submenu_list()

    def init_main_menu(self):
        preset_dir_path = info_dir.get_preset_dir_path()
        file_name = 'menu_Arduino.json'
        file_path = os.path.join(preset_dir_path, file_name)
        self.main_menu.load_from_file(file_path)
        self.main_menu.update_file()

    def init_empty_main_menu(self):
        param_dict = self.main_menu.get_param_dict()
        param_dict.pop('children')
        self.empty_main_menu.set_param_dict(param_dict)
        self.empty_main_menu.set('children', [])

    def init_submenu_list(self):
        for sub_menu_caption in sub_menu_caption_list:
            sub_menu = cls_menu.Menu(sub_menu_caption, self.empty_main_menu)
            sub_menu.update_file()
            self.submenu_list.append(sub_menu)
