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



class DhcpMapping(LineMapping):
    def iterlines(self):
        from itertools import groupby, ifilter
        from operator import itemgetter

        # Yield global options
        def has_config(field):
                return field in self.config and self.config[field]

        if has_config('authoritative'):
            yield 'authoritative;'

        if has_config('default-lease-time'):
            yield 'default-lease-time {config[default-lease-time]};'.format(config = self.config)

        if has_config('max-lease-time'):
            yield 'max-lease-time {config[max-lease-time]};'.format(config = self.config)

        if has_config('use-host-decl-names'):
            yield 'use-host-decl-names on;'

        for subnet, entries in sorted(self.subnets.iteritems()):
            # Search for consecutive DHCP ranges to build pools
            pools = [itemgetter(0, -1)(map(lambda (_, entry): entry.ipaddr.address_str,
                                           group))
                     for _, group
                     in groupby(enumerate(ifilter(lambda entry: entry.usage == 'dynamic',
                                                  sorted(entries))),
                                lambda (i, entry): i - entry.ipaddr.address_int)]

            # Yield subnet declaration
            yield 'subnet {subnet.network.address_str} netmask {subnet.netmask} {{'.format(subnet = subnet)

            # Yield subnet options
            yield '  option subnet-mask {subnet.netmask};'.format(subnet = subnet)

            def has_field(field):
                return field in subnet.fields and subnet.fields[field]

            if has_field('dhcp_dns_server'):
                yield '  option domain-name-servers {dhcp_dns_server};'.format(**subnet.fields)

            if has_field('dhcp_dns_domain'):
                yield '  option domain-name "{dhcp_dns_domain}";'.format(**subnet.fields)

            if has_field('dhcp_dns_search'):
                yield '  option domain-search "{dhcp_dns_search}";'.format(**subnet.fields)

            if has_field('dhcp_router'):
                yield '  option routers {dhcp_router};'.format(**subnet.fields)

            if has_field('dhcp_tftp_server'):
                yield '  option tftp-server-name {dhcp_tftp_server};'.format(**subnet.fields)
                yield '  next-server {dhcp_tftp_server};'.format(**subnet.fields)

            if has_field('dhcp_tftp_file'):
                yield '  filename "{dhcp_tftp_file}";'.format(**subnet.fields)

            # Yield pool declarations
            for pool in sorted(pools):
                yield '  pool {{'.format(pool = pool)
                yield '    range {pool[0]} {pool[1]};'.format(pool = pool)
                yield '  }}'.format(pool = pool)

            for entry in sorted(entries):
                if entry.usage == 'static':
                    yield '  host {entry.name} {{ hardware ethernet {entry.hwaddr}; fixed-address {entry.ipaddr.address_str}; }}'.format(entry = entry)

            yield '}}'.format(subnet = subnet)
