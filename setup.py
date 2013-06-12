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

import setuptools


version = open('VERSION').read().strip()

setuptools.setup(
    license = 'GNU GPLv3',

    name = 'netprov',
    version = version,

    author = 'Dustin Frisch',
    author_email = 'fooker@lab.sh',

    url = 'http://www.opendesk.net/tftprov',

    description = 'Network Configuration Provisioner',
    long_description = open('README').read(),
    keywords = 'netprov network configuration config provisioning provision',

    packages = setuptools.find_packages(),

    install_requires = [
        'bitarray >= 0.8.0',
        'MySQL-python >= 1.2.4',
    ],

    entry_points = {
        'console_scripts' : [
            'netprov = netprov.__main__:main'
        ],

        'netprov.source' : [
            'phpipam = netprov.sources.phpipam:PhpipamSource',
        ],

        'netprov.mapping' : [
            'isc:dhcp = netprov.mappings.isc:DhcpMapping',
            'linux:hosts = netprov.mappings.linux:HostsMapping',
        ],
    },
)
