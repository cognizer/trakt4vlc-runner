#!/usr/bin/env python
# encoding: utf-8


import os
import os.path as op
import sys
import getopt
import pkg_resources
import logging

sys.path.append(pkg_resources.resource_filename(__name__, ''))
sys.path.append(pkg_resources.resource_filename(__name__, 'trakt4vlc'))

import TraktForVLC as trakt

def main():
    should_pair = should_daemon = False

    datadir = "~/.config/traktforvlc"
    pidfile = ""
    config = ""

    def help():
        helpstr = [
            'Available options:',
            '     --config=path ' +
            '          Path to config file',
            '     -d,--daemon   ' +
            '          Run as daemon',
            '     --datadir=path' +
            '          Location of the app data (logs,...)',
            '     --debug       ' +
            '          Enter DEBUG mode',
            '     -h,--help     ' +
            '          This message',
            '     --loglevel=lvl' +
            '          Specify the log level',
            '     --pidfile=path' +
            '          Indicate pidfile (for daemon mode)',
            '     --small-timers' +
            '          Activate small timers (for DEBUG mode)',
        ]
        for hlp in helpstr:
            print(hlp)

    try:
        opts, args = getopt.getopt(sys.argv[1:], "dh", [
            'config=',
            'daemon',
            'datadir=',
            'debug',
            'help',
            'loglevel=',
            'pidfile=',
            'small-timers',
        ])
    except getopt.GetoptError as e:
        print('Error:', e.msg)
        help()
        sys.exit(1)

    for o, a in opts:
        # Determine location of config file
        if o in ('--config',):
            config = str(a)

        # Run as a daemon
        elif o in ('-d', '--daemon'):
            if sys.platform == 'win32':
                print("Daemonize not supported under Windows, " +
                      "starting normally")
            else:
                should_daemon = True

        # Determine location of datadir
        elif o in ('--datadir',):
            datadir = str(a)

        # DEBUG mode
        elif o in ('--debug',):
            LOG_LEVEL = logging.DEBUG

        # Help message
        elif o in ('-h', '--help',):
            help()
            sys.exit(0)

        # Specify log level
        elif o in ('--loglevel',):
            LOG_LEVEL = None
            if a.isdigit():
                LOG_LEVEL = int(a)
            else:
                for loglvl, logstr in AVAILABLE_LOGLVL:
                    if a == logstr:
                        LOG_LEVEL = loglvl
                if LOG_LEVEL is None:
                    raise Exception("LOG_LEVEL %s unknown", a)

        # Create pid file
        elif o in ('--pidfile',):
            pidfile = str(a)

        # Use small timers instead of those in the config file
        elif o in ('--small-timers',):
            SMALL_TIMERS = True

        # An untreated command-line option has been passed
        else:
            raise Exception('Unknown command line option: %s', o)

    if should_daemon:
        trakt.daemonize(pidfile)
    elif (pidfile):
        open(pidfile, "w").write("%s\n" % str(os.getpid()))

    if '~' in datadir:
        datadir = op.expanduser(datadir)
    else:
        datadir = op.abspath(datadir)

    if not op.isdir(datadir):
        try:
            os.makedirs(datadir)
        except:
            pass

    logdir = op.join(datadir, 'logs')
    if not op.isdir(logdir):
        try:
            os.mkdir(logdir, 0700)
        except:
            pass

    if config == "":
        config = datadir
    configfile = op.join(config, "config.ini")

    if not op.isfile(configfile):
        with open(configfile, 'wb') as cfp:
            cfp.write("""\
[VLC]
IP = localhost
Port = 4222

[Trakt]
PIN = [pin code from https://trakt.tv/pin/2498]

[TraktForVLC]
Timer = 60
StartWatching = 30
UseFilenames = No
ScrobblePercent = 90
ScrobbleMovie = Yes
ScrobbleTV = Yes
WatchingMovie = Yes
WatchingTV = Yes
""")

    trakt.LOG_LEVEL = LOG_LEVEL
    client = trakt.TraktForVLC(
        datadir,
        configfile,
        daemon=(should_daemon or pidfile))
    client.run()


if __name__ == '__main__':
    main()
