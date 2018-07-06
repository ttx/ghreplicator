#! /usr/bin/env python

# Copyright 2017 OpenStack Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import daemon
import json
import logging.config
import os

from ghreplicator import mappers, triggers, handlers


try:
    import daemon.pidlockfile as pid_file_module
except ImportError:
    # as of python-daemon 1.6 it doesn't bundle pidlockfile anymore
    # instead it depends on lockfile-0.9.1
    import daemon.pidfile as pid_file_module


def start(configpath):
    with open(configpath, 'r') as fp:
        config = json.load(fp)

    if 'log_config' in config:
        log_config = config['log_config']
        fp = os.path.expanduser(log_config)
        if not os.path.exists(fp):
            raise Exception("Unable to read logging config file at %s" % fp)
        logging.config.fileConfig(fp)
    else:
        logging.basicConfig(level=logging.DEBUG)

    # Load configured mapper
    # Mappers calculate destination name based on original name
    if 'mapper' not in config:
        print('AARRRRRGH')

    mapperclass = getattr(mappers, config['mapper'])

    if 'mapperargs' in config:
        args = config['mapperargs']
    else:
        args = {}

    mapper = mapperclass(**args)

    # Load configured handler
    # Handlers take original and destination names and do whatever
    # it is they do on them, like replicating git repositories
    if 'handler' not in config:
        print('AARRRRRGH')

    handlerclass = getattr(handlers, config['handler'])

    if 'handlerargs' in config:
        args = config['handlerargs']
    else:
        args = {}

    handler = handlerclass(**args)

    # Load configured trigger
    # Triggers generate events
    if 'trigger' not in config:
        print('AARRRRRGH')

    triggerclass = getattr(triggers, config['trigger'])

    if 'triggerargs' in config:
        args = config['triggerargs']
    else:
        args = {}

    def process(origin, revision):
        target = mapper.map(origin)
        handler.process(origin, target, revision)
        print("%s -> %s: copy %s" % (origin, target, revision))

    client = triggerclass(callback=process, **args)
    client.run()


def main():
    parser = argparse.ArgumentParser(description='GitHub replicator')
    parser.add_argument('configfile', help='specify the config file')
    parser.add_argument('-d', dest='nodaemon', action='store_true',
                        help='do not run as a daemon')
    args = parser.parse_args()

    if not args.nodaemon:
        pid = pid_file_module.TimeoutPIDLockFile(
            "/var/run/ghreplicator/ghreplicator.pid", 10)
        with daemon.DaemonContext(pidfile=pid):
            start(args.configfile)
    start(args.configfile)


if __name__ == "__main__":
    main()
