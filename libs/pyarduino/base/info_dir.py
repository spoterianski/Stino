#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals

import os

from . import constants
from . import info_sys


def list_win_volumes():
    vol_list = []
    for label in range(67, 90):
        vol = chr(label) + ':\\'
        if os.path.isdir(vol):
            vol_list.append(vol)
    return vol_list


def get_current_dir_path():
    return os.path.dirname(os.path.realpath(__file__))


def get_preset_dir_path():
    cur_dir_path = get_current_dir_path()
    preset_dir_path = os.path.join(cur_dir_path, '../preset')
    return os.path.abspath(preset_dir_path)


def get_documents_dir_path():
    os_name = info_sys.get_os_name()
    if os_name == 'windows':
        python_version = info_sys.get_python_version()
        if python_version < 3:
            import _winreg as winreg
        else:
            import winreg
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows' +
            r'\CurrentVersion\Explorer\Shell Folders',)
        document_path = winreg.QueryValueEx(key, 'Personal')[0]
    elif os_name == 'osx':
        home_path = os.getenv('HOME')
        document_path = os.path.join(home_path, 'Documents')
    else:
        document_path = os.getenv('HOME')
    return document_path


def get_tmp_dir_path():
    tmp_path = '/tmp'
    os_name = info_sys.get_os_name()
    if os_name == 'windows':
        tmp_path = os.environ['tmp']
    return tmp_path


def get_sys_settings_dir_path():
    os_name = info_sys.get_os_name()
    if os_name == 'windows':
        local_app_data = os.getenv('LOCALAPPDATA')
        user_setting_path = os.path.join(local_app_data, constants.APP_NAME)
    elif os_name == 'linux':
        home = os.getenv('HOME')
        user_setting_path = os.path.join(home, '.config', constants.APP_NAME)
    elif os_name == 'osx':
        home = os.getenv('HOME')
        user_setting_path = os.path.join(home, 'Library', constants.APP_NAME)
    return user_setting_path


def get_settings_dir_path():
    if info_sys.is_in_submlime():
        import sublime
        subl_packages_path = sublime.packages_path()
        user_path = os.path.join(subl_packages_path, 'User')
        setting_path = os.path.join(user_path, constants.APP_NAME)
    else:
        setting_path = get_sys_settings_dir_path()
    return setting_path


def get_sketchbook_path():
    documents_path = get_documents_dir_path()
    sketchbook_path = os.path.join(documents_path, 'Arduino')
    return sketchbook_path


def get_arduino_app_path():
    arduino_app_path = ''
    os_name = info_sys.get_os_name()
    if os_name == 'windows':
        program_files = os.getenv('ProgramFiles(x86)')
        arduino_app_path = os.path.join(program_files, 'Arduino')
        if not os.path.isdir(arduino_app_path):
            program_files = os.getenv('ProgramFiles')
            arduino_app_path = os.path.join(program_files, 'Arduino')
    elif os_name == 'linux':
        arduino_app_path = '/usr/share/arduino'
    elif os_name == 'osx':
        arduino_app_path = '/Applications/arduino.app'
    return arduino_app_path


def get_arduino_packages_dir_path():
    arduino_packages_path = ''
    os_name = info_sys.get_os_name()
    if os_name == 'windows':
        local_app_data = os.getenv('LOCALAPPDATA')
        arduino_packages_path = os.path.join(local_app_data, 'Arduino15')
    elif os_name == 'linux':
        home = os.getenv('HOME')
        arduino_packages_path = os.path.join(home, '.arduino15')
    elif os_name == 'osx':
        home = os.getenv('HOME')
        arduino_packages_path = os.path.join(home, 'Library/Arduino15')
    return arduino_packages_path


def get_lang_dir_path():
    cur_dir_path = get_current_dir_path()
    lang_dir_path = os.path.join(cur_dir_path, '../languages')
    return os.path.abspath(lang_dir_path)
