#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals

import os
import glob

from . import cls_file


class Dir(cls_file.AbstractFile):
    def __init__(self, path):
        super(Dir, self).__init__(path)

    def create(self):
        if self.is_file():
            cur_file = cls_file.File(self.path)
            new_name = 'old_file_' + cur_file.name
            cur_file.change_name(new_name)
        if not self.is_dir():
            os.makedirs(self.path)

    def list_all(self, pattern='*'):
        all_files = []
        paths = glob.glob(os.path.join(self.path, pattern))
        all_files = (cls_file.AbstractFile(path) for path in paths)
        all_files = [f for f in all_files if not f.is_temp_file()]
        all_files.sort(key=lambda f: f.get_name().lower())
        return all_files

    def list_dirs(self, pattern='*'):
        all_files = self.list_all(pattern)
        dirs = [Dir(f.path) for f in all_files if f.is_dir()]
        return dirs

    def list_files(self, pattern='*'):
        all_files = self.list_all(pattern)
        files = [cls_file.File(f.path) for f in all_files if f.is_file()]
        return files

    def list_files_of_extension(self, ext=''):
        return self.list_files('*' + ext)

    def list_files_of_extensions(self, exts=['']):
        all_files = []
        for ext in exts:
            all_files += self.list_files_of_extension(ext)
        return all_files

    def recursive_list_files(self, exts=[''], exclude_dirs=[]):
        all_files = self.list_files_of_extensions(exts)
        dirs = self.list_dirs()
        for cur_dir in dirs:
            if cur_dir.get_name() not in exclude_dirs:
                all_files += cur_dir.recursive_list_files(exts)
        return all_files

    def has_file(self, file_name):
        file_path = os.path.join(self.path, file_name)
        return os.path.isfile(file_path)
