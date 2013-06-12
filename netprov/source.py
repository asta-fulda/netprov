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

from abc import ABCMeta, abstractproperty

from bitarray import bitarray



class Entry(object):
    def __init__(self,
                 name,
                 usage,
                 ipaddr,
                 hwaddr):
        self.__name = name
        self.__usage = usage

        if isinstance(ipaddr, Address):
            self.__ipaddr = ipaddr
        else:
            self.__ipaddr = Address(ipaddr)

        self.__hwaddr = hwaddr


    @staticmethod
    def fixed(name, ipaddr):
        return Entry(name = name,
                     usage = 'fixed',
                     ipaddr = ipaddr,
                     hwaddr = None)


    @staticmethod
    def static(name, ipaddr, hwaddr):
        return Entry(name = name,
                     usage = 'static',
                     ipaddr = ipaddr,
                     hwaddr = hwaddr)


    @staticmethod
    def dynamic(name, ipaddr):
        return Entry(name = name,
                     usage = 'dynamic',
                     ipaddr = ipaddr,
                     hwaddr = None)


    @property
    def name(self):
        return self.__name


    @property
    def usage(self):
        return self.__usage


    @property
    def ipaddr(self):
        return self.__ipaddr


    @property
    def hwaddr(self):
        return self.__hwaddr



class Address(object):
    def __init__(self, address):
        if isinstance(address, int) or isinstance(address, long):
            self.__address = bytearray((address >> n * 8) & 0xFF
                                       for n
                                       in reversed(xrange(4)))
        elif isinstance(address, bytearray):
            self.__address = address
        else:
            self.__address = bytearray(int(part)
                                       for part
                                       in address.split('.'))


    @property
    def address(self):
        return self.__address


    @property
    def address_str(self):
        return '.'.join(str(b)
                        for b
                        in self.__address)


    @property
    def address_int(self):
        return sum(x << (8 * (3 - n))
                   for n, x
                   in enumerate(self.__address))



class Subnet(object):
    def __init__(self,
                 network,
                 netmask,
                 **fields):

        if isinstance(network, Address):
            self.__network = network
        else:
            self.__network = Address(network)

        if isinstance(netmask, int) or isinstance(netmask, long):
            self.__suffix = netmask
        else:
            bits = bitarray()
            bits.frombytes(str(bytearray(int(part)
                                         for part
                                         in netmask.split('.'))))

            self.__suffix = bits.count(True)

        self.__fields = fields


    @property
    def network(self):
        return self.__network


    @property
    def suffix(self):
        return self.__suffix


    @property
    def netmask(self):
        bits = bitarray(32)
        bits.setall(False)
        bits[0:self.__suffix] = True

        return '.'.join(str(ord(byte))
                        for byte
                        in bits.tobytes())


    @property
    def fields(self):
        return self.__fields


    def __str__(self):
        return '%s/%d' % (self.network,
                          self.suffix)



class Source(object):
    __metaclass__ = ABCMeta


    @abstractproperty
    def subnets(self):
        pass
