#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals


class ArduinoInfo(object):
    def __init__(self, param_dict):
        self.param_dict = {}
        self.update(param_dict)

    def set(self, key, value):
        self.param_dict[key] = value

    def get(self, key, default_value=None):
        if key in self.param_dict:
            value = self.param_dict[key]
        else:
            value = default_value
        return value

    def update(self, param_dict):
        self.param_dict.update(param_dict)

    def get_param_dict(self):
        return self.param_dict


class Package(ArduinoInfo):
    def __init__(self, param_dict):
        super(Package, self).__init__(param_dict)
        self.installed_arch_list = []
        self.installed_tool_list = []
        self.arch_platforms_dict = {}
        self.name_tools_dict = {}

    def append_platform(self, platform):
        arch = platform.get('architecture')
        if arch not in self.arch_platforms_dict:
            self.arch_platforms_dict[arch] = []
        self.arch_platforms_dict[arch].append(platform)

    def append_tool(self, tool):
        name = tool.get('name')
        if name not in self.name_tools_dict:
            self.name_tools_dict[name] = []
        self.name_tools_dict[name].append(tool)

    def append_installed_arch(self, arch):
        self.installed_arch_list.append(arch)

    def append_installed_tool(self, tool_name):
        self.installed_tool_list.append(tool_name)

    def get_platform_arch_list(self):
        arch_list = list(self.arch_platforms_dict.keys())
        arch_list.sort()
        return arch_list

    def get_platform_list(self, arch):
        platform_list = self.arch_platforms_dict.get(arch, [])
        return platform_list

    def get_tool_name_list(self):
        name_list = list(self.name_tools_dict.keys())
        name_list.sort()
        return name_list

    def get_tool_list(self, name):
        tool_list = self.name_tools_dict.get(name, [])
        return tool_list

    def get_platform(self, arch, version):
        platform = None
        platform_list = self.get_platform_list(arch)
        for cur_platform in platform_list:
            if cur_platform.get('version') == version:
                platform = cur_platform
                break
        return platform

    def get_arch_name(self, arch):
        name = 'Unknown'
        platform_list = self.get_platform_list(arch)
        if platform_list:
            name = platform_list[0].get('name')
        return name

    def get_installed_arch_list(self):
        return self.installed_arch_list

    def get_installed_tool_list(self):
        return self.installed_tool_list

    def has_installed_arch(self):
        return bool(self.installed_arch_list)


class Platform(ArduinoInfo):
    def __init__(self, param_dict):
        super(Platform, self).__init__(param_dict)
        self.set('board_list', [])

    def get_board(self, board_id):
        board = None
        board_list = self.get('board_list')
        for cur_board in board_list:
            if board_id == cur_board.get('id'):
                board = cur_board
                break
        return board
