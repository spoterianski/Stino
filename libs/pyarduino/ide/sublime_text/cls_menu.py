#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals

import os
import pyarduino


class Menu(object):
    def __init__(self, caption, parent=None):
        self.param_dict = {}
        self.param_dict['caption'] = caption
        self.param_dict['id'] = '_'.join(caption.lower().split())
        self.param_dict['command'] = ''
        self.param_dict['args'] = {}
        self.param_dict['checkbox'] = False
        self.param_dict['children'] = []
        self.set_parent(parent)

    def set(self, key, value):
        self.param_dict[key] = value

    def get(self, key, default_value=None):
        if key in self.param_dict:
            value = self.param_dict[key]
        else:
            value = default_value
        return value

    def set_param_dict(self, param_dict):
        self.param_dict = param_dict

    def get_param_dict(self):
        return self.param_dict

    def set_parent(self, parent):
        self.set('parent', parent)
        self.param_dict['level'] = self.get_level()
        self.param_dict['file'] = self.get_file()

    def append_child(self, child):
        self.param_dict['children'].append(child)

    def get_file(self):
        parent = self.get('parent')
        settings_dir_path = pyarduino.base.info_dir.get_settings_dir_path()
        menu_dir_path = os.path.join(settings_dir_path, 'menu')

        dir_list = [self.param_dict['caption']]
        while parent:
            dir_list.append(parent.param_dict['caption'])
            parent = parent.param_dict['parent']
        dir_list.append(menu_dir_path)

        dir_path = os.path.sep.join(dir_list[::-1])
        file_path = os.path.join(dir_path, 'Main.sublime-menu')
        menu_file = pyarduino.base.cls_file.JSONFile(file_path)
        return menu_file

    def get_level(self):
        parent = self.param_dict['parent']
        if parent:
            level = parent.get_level() + 1
        else:
            level = 0
        return level

    def get_self_data(self):
        menu_data = {}
        menu_data['caption'] = self.param_dict['caption']
        menu_data['id'] = self.param_dict['id']
        children = self.param_dict['children']
        if children:
            mnemonic = self.param_dict.get('mnemonic', '')
            if mnemonic:
                menu_data['mnemonic'] = mnemonic
            menu_data['children'] = []
            for child in children:
                child_menu_data = child.get_self_data()
                menu_data['children'].append(child_menu_data)
        else:
            menu_data['command'] = self.param_dict['command']
            if self.param_dict['args']:
                menu_data['args'] = self.param_dict['args']
            if self.param_dict['checkbox']:
                menu_data['checkbox'] = True
        return menu_data

    def get_all_data(self):
        menu_data = self.get_self_data()
        parent = self.param_dict['parent']
        while parent:
            parent_menu_data = {}
            parent_menu_data['caption'] = parent.param_dict['caption']
            parent_menu_data['id'] = parent.param_dict['id']
            parent_menu_data['children'] = [menu_data]
            menu_data = parent_menu_data
            parent = parent.param_dict['parent']
        return menu_data

    def load_from_file(self, file_path):
        menu = load_menu_from_file(file_path)
        if menu:
            self.param_dict.update(menu.param_dict)

    def update_file(self, visible=True):
        if visible:
            file_data = [self.get_all_data()]
        else:
            file_data = []
        menu_file = self.param_dict['file']
        menu_file.set_data(file_data)
        menu_file.save()


def load_menu_from_file(file_path):
    menu = None
    data_file = pyarduino.base.cls_file.JSONFile(file_path)
    data = data_file.get_data()
    if data:
        data_dict = data[0]
        menu = load_menu_from_data_dict(data_dict)
    return menu


def load_menu_from_data_dict(data_dict, parent=None):
    menu = None
    caption = data_dict.get('caption', '')
    if caption:
        menu = Menu(caption, parent)
        if 'children' in data_dict:
            children = data_dict.pop('children')
            for sub_data_dict in children:
                sub_menu = load_menu_from_data_dict(sub_data_dict, menu)
                if sub_menu:
                    menu.append_child(sub_menu)
        menu.param_dict.update(data_dict)
    return menu
