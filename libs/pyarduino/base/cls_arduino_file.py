#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals

import os

from . import info_dir
from . import cls_file
from . import cls_arduino_info


class PkgsIndexFile(cls_file.JSONFile):
    def __init__(self, path):
        super(PkgsIndexFile, self).__init__(path)
        self.package_list = []
        self.load_packages()

    def load_packages(self):
        a15_dir_path = info_dir.get_arduino_packages_dir_path()
        pkgs_dir_path = os.path.join(a15_dir_path, 'packages')

        pkg_list = self.data['packages']
        for pkg_info in pkg_list:
            if 'platforms'in pkg_info:
                pkg_platforms = pkg_info.pop('platforms')
            else:
                pkg_platforms = []

            if 'tools'in pkg_info:
                pkg_tools = pkg_info.pop('tools')
            else:
                pkg_tools = []

            package = cls_arduino_info.Package(pkg_info)
            pkg_name = package.get('name')

            for platform_info in pkg_platforms:
                platform = cls_arduino_info.Platform(platform_info)
                arch = platform.get('architecture')
                ver = platform.get('version')
                dir_path = os.path.join(pkgs_dir_path, pkg_name,
                                        'hardware', arch, ver)
                platform.set('package_name', pkg_name)
                platform.set('path', dir_path)
                package.append_platform(platform)

            for tool_info in pkg_tools:
                if 'systems'in tool_info:
                    tool_systems = tool_info.pop('systems')
                else:
                    tool_systems = []

                tool = cls_arduino_info.ArduinoInfo(tool_info)
                tool_name = tool.get('name', '')
                ver = tool.get('ver', '')
                dir_path = os.path.join(pkgs_dir_path, pkg_name,
                                        'tools', tool_name, ver)
                tool.set('package_name', pkg_name)
                tool.set('path', dir_path)

                for tool_system in tool_systems:
                    host = tool_system.get('host', '')
                    host_tool_info = cls_arduino_info.ArduinoInfo(tool_system)
                    tool.set(host, host_tool_info)

                package.append_tool(tool)

            self.package_list.append(package)

    def get_packages(self):
        return self.package_list


class ParamsFile(cls_file.File):
    def __init__(self, path):
        super(ParamsFile, self).__init__(path)
        self.param_dict = {}
        self.load_param_dict()

    def load_param_dict(self):
        text = self.read()
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                if '=' in line:
                    index = line.index('=')
                    key = line[:index]
                    value = line[index + 1:]
                    self.param_dict[key] = value

    def get_param_dict(self):
        return self.param_dict


class ItemsFile(ParamsFile):
    def __init__(self, path):
        super(ItemsFile, self).__init__(path)
        self.submenu_name_dict = {}
        self.item_list = []
        self.load_item_list()

    def load_item_list(self):
        item_name_list = []
        text = self.read()
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                if '.name' in line and '=' in line:
                    index = line.index('=')
                    name = line[index + 1:].strip()
                    item_name_list.append(name)

        name_params_dict = {}
        id_params_dict = {}
        for key in self.param_dict:
            value = self.param_dict[key]

            if '.' not in key:
                continue

            if key.startswith('menu.'):
                self.submenu_name_dict[key] = value
            else:
                index = key.index('.')
                item_id = key[:index]
                sub_key = key[index + 1:]

                if item_id not in id_params_dict:
                    id_params_dict[item_id] = {'id': item_id}
                id_params_dict[item_id][sub_key] = value

        for item_id in id_params_dict:
            params_dict = id_params_dict[item_id]
            name = params_dict.get('name', '')

            common_params_dict = {}
            custom_parmas_dict = {}
            for key in params_dict:
                value = params_dict[key]
                if key.startswith('menu.'):
                    custom_parmas_dict[key] = value
                else:
                    common_params_dict[key] = value

            # group
            submenu_params_dict = {}
            for submenu_id in self.submenu_name_dict:
                submenu_params_dict[submenu_id] = {}
                for key in custom_parmas_dict:
                    value = custom_parmas_dict[key]
                    if key.startswith(submenu_id):
                        key = key.replace('%s.' % submenu_id, '')
                        submenu_params_dict[submenu_id][key] = value

            submenu_subitem_list_dict = {}
            for submenu_id in submenu_params_dict:
                sub_params_dict = submenu_params_dict[submenu_id]

                subid_params_dict = {}
                for key in sub_params_dict:
                    value = sub_params_dict[key]
                    if '.' not in key:
                        key += '.name'
                    index = key.index('.')
                    item_id = key[:index]
                    sub_key = key[index + 1:]
                    if item_id not in subid_params_dict:
                        subid_params_dict[item_id] = {'id': item_id}
                    subid_params_dict[item_id][sub_key] = value

                subitem_list = []
                item_id_list = list(subid_params_dict.keys())
                item_id_list.sort()
                for item_id in item_id_list:
                    subitem_params = subid_params_dict[item_id]
                    subitem = cls_arduino_info.ArduinoInfo(subitem_params)
                    subitem_list.append(subitem)
                if subitem_list:
                    submenu_subitem_list_dict[submenu_id] = subitem_list

            common_params_dict['options'] = submenu_subitem_list_dict
            name_params_dict[name] = common_params_dict

        for name in item_name_list:
            param_dict = name_params_dict[name]
            item = cls_arduino_info.ArduinoInfo(param_dict)
            self.item_list.append(item)

    def get_item_list(self):
        return self.item_list

    def get_submenu_name_dict(self):
        return self.submenu_name_dict
