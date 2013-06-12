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



class Formatter(object):
    __metaclass__ = ABCMeta


    @abstractmethod
    def __call__(self, source):
        pass



class LineFormatter(Formatter):
    def __call__(self, source):
        return ''.join(('%s\n' % line)
                       for line
                       in self.iterlines(source))


    @abstractmethod
    def iterlines(self, source):
        pass
