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

from netprov.config import parse as parse_config

import sys
import logging

import pkg_resources



def main():
    logging.getLogger('netprov').setLevel(logging.DEBUG)

    if len(sys.argv) == 1:
        config = '/etc/netprov.conf'

    elif len(sys.argv) == 2:
        config = sys.argv[1]

    else:
        print >> sys.stderr, 'Usage: %s [CONFIG]' % sys.argv[0]
        print >> sys.stderr, '    CONFIG  The config file to use'

        sys.exit(255)

    config = parse_config(config)

    # Load the source and mapping classes from setup tools
    source_plugins = {ep.name : ep.load()
                      for ep
                      in pkg_resources.iter_entry_points(group = 'netprov.source',
                                                         name = None)}

    mapping_plugins = {ep.name : ep.load()
                       for ep
                       in pkg_resources.iter_entry_points(group = 'netprov.mapping',
                                                          name = None)}

    # Build source instances from configuration
    sources = {name : source_plugins[source['class']](**source['config'])
               for name, source
               in config['sources'].iteritems()}

    # Build the mapping from the configuration using the loaded sources and formatters
    mappings = [mapping_plugins[config['class']](path = path,
                                                 source = sources[config['source']],
                                                 config = config['config'],
                                                 action = config['action'])
                for path, config
                in config['mappings'].iteritems()]

    # Execute the mappings
    for mapping in mappings:
        if mapping():
            logging.debug('%s updated', mapping.path)



if __name__ == '__main__':
    main()
