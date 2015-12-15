#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals

import os
import shutil

from . import constants
from . import info_dir
from . import cls_file
from . import cls_arduino_file


class BoardManager():
    def __init__(self, settings):
        self.settings = settings
        # all packages
        self.avilable_package_list = []
        self.name_package_dict = {}
        # current used platforms, to list boards
        self.cur_platform_list = []

        self.dir_path = info_dir.get_arduino_packages_dir_path()
        self.pkgs_dir_path = os.path.join(self.dir_path, 'packages')
        if not os.path.isdir(self.dir_path):
            os.makedirs(self.dir_path)

        self.gen_packages_url_list()
        self.load_packages()

        self.check_platform_installed()
        self.check_tool_installed()
        self.check_current_platform_list()

        self.load_current_platforms_params()
        self.load_current_board_list()
        self.load_current_programmer_list()

        self.check_platform_selected()
        self.check_board_selected()
        self.check_board_option_selected()

    def gen_packages_url_list(self):
        file_name = constants.PKG_URL_LIST_FILE_NAME
        pkg_url_list_file_path = os.path.join(self.dir_path, file_name)
        if not os.path.isfile(pkg_url_list_file_path):
            preset_dir_path = info_dir.get_preset_dir_path()
            preset_file_path = os.path.join(preset_dir_path, file_name)
            shutil.copy(preset_file_path, pkg_url_list_file_path)
        cur_file = cls_file.PkgsUrlListFile(pkg_url_list_file_path)
        self.packages_url_list = cur_file.get_packages_url_list()

    def load_packages(self):
        index_file_path_list = []
        for packages_url in self.packages_url_list:
            index_file_name = os.path.basename(packages_url)
            index_file_path = os.path.join(self.dir_path, index_file_name)
            if os.path.isfile(index_file_path):
                index_file_path_list.append(index_file_path)

        if not index_file_path_list:
            file_name = 'package_index.json'
            preset_dir_path = info_dir.get_preset_dir_path()
            preset_file_path = os.path.join(preset_dir_path, file_name)
            index_file_path = os.path.join(self.dir_path, file_name)
            shutil.copy(preset_file_path, index_file_path)
            index_file_path_list.append(index_file_path)

        for index_file_path in index_file_path_list:
            index_file = cls_arduino_file.PkgsIndexFile(index_file_path)
            self.avilable_package_list += index_file.get_packages()

        for package in self.avilable_package_list:
            pkg_name = package.get('name', '')
            self.name_package_dict[pkg_name] = package

    def check_platform_installed(self):
        for package in self.avilable_package_list:
            arch_list = package.get_platform_arch_list()
            for arch in arch_list:
                is_arch_installed = False
                platform_list = package.get_platform_list(arch)
                for platform in platform_list:
                    dir_path = platform.get('path', '')
                    is_installed = False
                    if os.path.isdir(dir_path):
                        is_installed = True
                        is_arch_installed = True
                    platform.set('installed', is_installed)
                if is_arch_installed:
                    package.append_installed_arch(arch)

    def check_tool_installed(self):
        for package in self.avilable_package_list:
            name_list = package.get_tool_name_list()
            for name in name_list:
                is_tool_installed = False
                tool_list = package.get_tool_list(name)
                for tool in tool_list:
                    dir_path = tool.get('path', '')
                    is_installed = False
                    if os.path.isdir(dir_path):
                        is_installed = True
                        is_tool_installed = True
                    tool.set('installed', is_installed)
                if is_tool_installed:
                    package.append_installed_tool(name)

    def check_current_platform_list(self):
        cur_arch_ver_dict = self.settings.get('current_platform_version', {})
        new_arch_ver_dict = {}

        for package in self.avilable_package_list:
            package_name = package.get('name', '')
            installed_arch_list = package.get_installed_arch_list()

            for arch in installed_arch_list:
                is_in_cur_dict = False
                platform_list = package.get_platform_list(arch)
                inst_platform_list = [p for p in platform_list
                                      if p.get('installed')]

                arch_key = '%s@%s' % (arch, package_name)
                if arch_key in cur_arch_ver_dict:
                    cur_ver = cur_arch_ver_dict[arch_key]
                    for platform in inst_platform_list:
                        ver = platform.get('version', '')
                        if ver == cur_ver:
                            self.cur_platform_list.append(platform)
                            is_in_cur_dict = True
                            break
                if not is_in_cur_dict:
                    platform = inst_platform_list[-1]
                    self.cur_platform_list.append(platform)
                    cur_ver = platform.get('version', '')
                new_arch_ver_dict[arch_key] = cur_ver
        self.settings.set('current_platform_version', new_arch_ver_dict)

    def load_current_platforms_params(self):
        for platform in self.cur_platform_list:
            preset_dir_path = info_dir.get_preset_dir_path()
            arch = platform.get('architecture')
            platform_file_name = 'platform_%s.txt' % arch
            file_path = os.path.join(preset_dir_path, platform_file_name)
            platform_file = cls_arduino_file.ParamsFile(file_path)
            param_dict = platform_file.get_param_dict()
            platform.set('build_params', param_dict)

    def load_current_board_list(self):
        for platform in self.cur_platform_list:
            dir_path = platform.get('path', '')
            file_path = os.path.join(dir_path, 'boards.txt')
            boards_file = cls_arduino_file.ItemsFile(file_path)
            submenu_name_dict = boards_file.get_submenu_name_dict()
            board_list = boards_file.get_item_list()
            platform.set('menu_name_dict', submenu_name_dict)
            platform.set('board_list', board_list)

    def load_current_programmer_list(self):
        for platform in self.cur_platform_list:
            dir_path = platform.get('path', '')
            file_path = os.path.join(dir_path, 'programmers.txt')
            programmers_file = cls_arduino_file.ItemsFile(file_path)
            programmer_list = programmers_file.get_item_list()
            platform.set('programmer_list', programmer_list)

    def check_platform_selected(self):
        selected_package_name = self.settings.get('selected_package', '')
        selected_platform_arch = self.settings.get('selected_arch', '')
        selected_platform_ver = self.settings.get('selected_ver', '')

        is_platform_selected = False
        platform_list = self.get_current_platform_list()
        for platform in platform_list:
            package_name = platform.get('package_name')
            arch = platform.get('architecture')
            ver = platform.get('version')
            if package_name == selected_package_name and \
                    arch == selected_platform_arch and \
                    ver == selected_platform_ver:
                is_platform_selected = True
                break

        if not is_platform_selected and platform_list:
            platform = platform_list[0]
            package_name = platform.get('package_name')
            arch = platform.get('architecture')
            ver = platform.get('version')
            self.settings.set('selected_package', package_name)
            self.settings.set('selected_arch', arch)
            self.settings.set('selected_ver', ver)

    def check_board_selected(self):
        selected_board_id = self.settings.get('selected_board', '')

        is_board_selected = False
        platform = self.get_selected_platform()
        if platform:
            board_list = platform.get('board_list')
            for board in board_list:
                board_id = board.get('id')
                if board_id == selected_board_id:
                    is_board_selected = True
                    break

            if not is_board_selected and board_list:
                board_id = board_list[0].get('id', '')
                self.settings.set('selected_board', board_id)

    def check_board_option_selected(self):
        for platform in self.cur_platform_list:
            pkg_name = platform.get('package_name')
            arch = platform.get('architecture')
            ver = platform.get('version')
            board_list = platform.get('board_list', [])
            for board in board_list:
                menu_subitem_list_dict = board.get('options')
                if menu_subitem_list_dict:
                    board_id = board.get('id')
                    info_list = [board_id, ver, arch, pkg_name]
                    board_info = '@'.join(info_list)
                    board_option_dict = self.settings.get(board_info, {})
                    for menu_id in menu_subitem_list_dict:
                        subitem_list = menu_subitem_list_dict[menu_id]
                        subitem_id_list = [i.get('id') for i in subitem_list]
                        sel_subitem_id = board_option_dict.get(menu_id, '')
                        if sel_subitem_id not in subitem_id_list:
                            sel_subitem_id = subitem_id_list[0]
                            board_option_dict[menu_id] = sel_subitem_id
                    self.settings.set(board_info, board_option_dict)

    def on_board_selected(self, board_info):
        # board_info: board_id@ver@arch@package_name
        selected_board_info = self.get_selected_board_info()
        if board_info != selected_board_info:
            info_list = board_info.split('@')
            if len(info_list) == 4:
                board_id = info_list[0]
                ver = info_list[1]
                arch = info_list[2]
                pkg_name = info_list[3]
                package = self.get_package(pkg_name)
                if package:
                    platform = package.get_platform(arch, ver)
                    if platform:
                        board = platform.get_board(board_id)
                        if board:
                            self.settings.set('selected_package', pkg_name)
                            self.settings.set('selected_arch', arch)
                            self.settings.set('selected_ver', ver)
                            self.settings.set('selected_board', board_id)

    def on_board_option_selected(self, option_info):
        # option_info: subitem_id@menu_id
        info_list = option_info.split('@')
        if len(info_list) == 2:
            board_info = self.get_selected_board_info()
            board_option_dict = self.settings.get(board_info, {})

            subitem_id = info_list[0]
            menu_id = info_list[1]
            board_id = self.settings.get('selected_board', '')
            board = self.get_selected_platform().get_board(board_id)
            if board:
                menu_subitem_list_dict = board.get('options')
                if menu_id in menu_subitem_list_dict:
                    subitem_list = menu_subitem_list_dict[menu_id]
                    subitem_id_list = [i.get('id') for i in subitem_list]
                    if subitem_id in subitem_id_list:
                        board_option_dict[menu_id] = subitem_id
                        self.settings.set(board_info, board_option_dict)

    def get_packages_url_list(self):
        return self.packages_url_list

    def get_current_platform_list(self):
        return self.cur_platform_list

    def get_selected_platform(self):
        pkg_name = self.settings.get('selected_package')
        arch = self.settings.get('selected_arch')
        ver = self.settings.get('selected_ver')
        sel_pkg = self.get_package(pkg_name)
        selected_platform = sel_pkg.get_platform(arch, ver)
        return selected_platform

    def get_selected_board_info(self):
        pkg_name = self.settings.get('selected_package')
        arch = self.settings.get('selected_arch')
        ver = self.settings.get('selected_ver')
        board_id = self.settings.get('selected_board', '')
        info_list = [board_id, ver, arch, pkg_name]
        board_info = '@'.join(info_list)
        return board_info

    def get_package(self, pkg_name):
        return self.name_package_dict.get(pkg_name, None)

    def print_avilable_platforms(self):
        for package in self.avilable_package_list:
            print(package.get('name'))
            arch_list = package.get_platform_arch_list()
            for arch in arch_list:
                arch_name = package.get_arch_name(arch)
                print('\t%s (%s)' % (arch_name, arch))
                platform_list = package.get_platform_list(arch)
                for platform in platform_list:
                    version = platform.get('version', 'Unknown')
                    is_installed = platform.get('installed', False)
                    flag = ''
                    if is_installed:
                        flag = '[Inst]'
                    print('\t\t%s %s' % (version, flag))

    def print_current_boards(self):
        selected_package_name = self.settings.get('selected_package', '')
        selected_platform_arch = self.settings.get('selected_arch', '')
        selected_platform_ver = self.settings.get('selected_ver', '')
        selected_board_id = self.settings.get('selected_board', '')

        platform_list = self.get_current_platform_list()
        for platform in platform_list:
            name = platform.get('name')
            print(name)
            package_name = platform.get('package_name')
            arch = platform.get('architecture')
            ver = platform.get('version')

            board_list = platform.get('board_list')
            for board in board_list:
                board_name = board.get('name')
                board_id = board.get('id')
                text = '\t%s' % board_name

                if package_name == selected_package_name and \
                        arch == selected_platform_arch and \
                        ver == selected_platform_ver and \
                        board_id == selected_board_id:
                    text += ' [checked]'
                print(text)
