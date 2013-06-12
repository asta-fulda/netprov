'''
Copyright 2013 Dustin Frisch<fooker@lab.sh>

This file is part of netprov.

netprov is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

netprov is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with netprov. If not, see <http://www.gnu.org/licenses/>.
'''

from abc import ABCMeta, abstractmethod

import hashlib
import os



class Mapping(object):
    __metaclass__ = ABCMeta


    def __init__(self,
                 path,
                 source,
                 config = None,
                 action = None):
        self.__path = path
        self.__source = source
        self.__config = config
        self.__action = action


    @property
    def path(self):
        return self.__path


    @property
    def config(self):
        return self.__config


    @property
    def subnets(self):
        return self.__source.subnets


    def __call__(self):
        md5_old = hashlib.md5()
        try:
            with open(self.__path, 'rb') as f:
                for chunk in iter(lambda: f.read(8192), b''):
                    md5_old.update(chunk)
        except Exception as e:
            md5_old.update(str(e))


        with open(self.__path, 'wb') as f:
            self.__generate__(f)

        md5_new = hashlib.md5()
        with open(self.__path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                md5_new.update(chunk)

        if md5_old.digest() != md5_new.digest():
            os.system(self.__action)
            return True

        else:
            return False


    @abstractmethod
    def __generate__(self, out):
        pass



class LineMapping(Mapping):
    def __generate__(self, out):
        for line in self.iterlines():
            out.write('%s\n' % line)


    @abstractmethod
    def iterlines(self):
        pass
