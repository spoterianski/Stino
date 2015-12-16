#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals

from . import base
from . import func_init


base.func_dir.add_package_to_sys_path()
# 实例化settings
settings = func_init.init_settings('Preferences.settings')
board_manager = base.cls_manager.BoardManager(settings)
board_manager.on_board_selected('lilypad@1.6.9@avr@arduino')
board_manager.on_board_option_selected('atmega328@menu.cpu')
# board_manager.print_current_boards()
# pkg_url_list_downloader = base.cls_downloader(dir_path, url_list, settings)
# pkg_index_downloader = base.cls_downloader(dir_path, url_list, settings)
# lib_url_list_downloader = base.cls_downloader(dir_path, url_list, settings)
# lib_index_downloader = base.cls_downloader(dir_path, url_list, settings)

if base.info_sys.is_in_submlime():
    from .ide import sublime_text
    menu_manager = sublime_text.cls_manager.MenuManager()
