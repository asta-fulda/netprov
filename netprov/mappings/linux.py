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

from netprov.mapping import LineMapping



class HostsMapping(LineMapping):
    def iterlines(self):

        if 'localhost' in self.config and self.config['localhost']:
            yield '127.0.0.1 localhost'

        for subnet, entries in self.subnets.iteritems():
            if 'dns_domain' in subnet.fields and subnet.fields['dns_domain']:
                domain = subnet.fields['dns_domain']

            for entry in entries:
                addr = entry.ipaddr.address_str

                if domain:
                    name = '%s.%s' % (entry.name,
                                      domain)
                else:
                    name = entry.name

                yield '%s %s' % (addr,
                                 name)
