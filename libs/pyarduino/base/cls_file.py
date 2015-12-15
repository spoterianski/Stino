#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals

import os
import codecs
import json


class AbstractFile(object):
    def __init__(self, path):
        path = os.path.realpath(path)
        self.set_path(path)

    def set_path(self, path):
        self.path = path
        self.dir = os.path.dirname(self.path)
        self.name = os.path.basename(self.path)
        self.caption = self.name

    def __str__(self):
        return '%s (%s)' % (self.name, self.path)

    def get_path(self):
        return self.path

    def get_dir(self):
        return self.dir

    def get_name(self):
        return self.name

    def get_ctime(self):
        ctime = 0
        if os.path.exists(self.path):
            ctime = os.path.getctime(self.path)
        return ctime

    def get_mtime(self):
        mtime = 0
        if os.path.exists(self.path):
            mtime = os.path.getmtime(self.path)
        return mtime

    def is_file(self):
        return os.path.isfile(self.path)

    def is_dir(self):
        return os.path.isdir(self.path)

    def is_temp_file(self):
        state = False
        lower_name = self.name.lower()
        if lower_name == 'cvs':
            state = True
        elif lower_name.startswith('$') or lower_name.startswith('.'):
            state = True
        elif lower_name.endswith('.tmp') or lower_name.endswith('.bak'):
            state = True
        return state

    def change_name(self, new_name):
        os.chdir(self.dir)
        os.rename(self.name, new_name)
        new_path = os.path.join(self.dir, new_name)
        self.set_path(new_path)


class File(AbstractFile):
    """
    Doc of this class
    """
    def __init__(self, path, encoding='utf-8'):
        super(File, self).__init__(path)
        self.set_encoding(encoding)

    def has_ext(self, extension):
        return self.get_ext() == extension

    def get_ext(self):
        return os.path.splitext(self.name)[1]

    def get_basename(self):
        return os.path.splitext(self.name)[0]

    def get_encoding(self):
        return self.encoding

    def set_encoding(self, encoding='utf-8'):
        self.encoding = encoding

    def read(self):
        text = ''
        try:
            with codecs.open(self.path, 'r', self.encoding) as f:
                text = f.read()
        except (IOError, UnicodeError):
            pass
        return text

    def write(self, text, append=False):
        mode = 'w'
        if append:
            mode = 'a'
        try:
            if not os.path.isdir(self.dir):
                os.makedirs(self.dir)
            with codecs.open(self.path, mode, self.encoding) as f:
                f.write(text)
        except (IOError, UnicodeError):
            pass


class JSONFile(File):
    def __init__(self, path):
        super(JSONFile, self).__init__(path)
        self.data = {}
        self.load()

    def set_data(self, data):
        self.data = data
        self.save()

    def get_data(self):
        return self.data

    def load(self):
        text = self.read()
        try:
            self.data = json.loads(text)
        except (ValueError):
            pass
            # print('Error while loading Json file %s.' % self.path)

    def save(self):
        text = json.dumps(self.data, sort_keys=True, indent=4)
        self.write(text)


class SettingsFile(JSONFile):
    def __init__(self, path):
        super(SettingsFile, self).__init__(path)

    def get(self, key, default_value=None):
        value = self.data.get(key, default_value)
        return value

    def set(self, key, value):
        self.data[key] = value
        self.save()

    def change_dir_path(self, new_dir_path):
        if os.path.isdir(new_dir_path):
            new_path = os.path.join(new_dir_path, self.name)
            self.set_path(new_path)
        if self.isfile():
            self.load()
        else:
            self.save()


class PkgsUrlListFile(File):
    def __init__(self, path):
        super(PkgsUrlListFile, self).__init__(path)
        self.packages_url_list = []
        self.load_packages_url_list()

    def load_packages_url_list(self):
        text = self.read()
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                self.packages_url_list.append(line)

    def get_packages_url_list(self):
        return self.packages_url_list
