#!/usr/bin/python3
#!/usr/bin/env python3

#  Copyright (c) 2018 Phil Birkelbach
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

import signal
import logging


import fixgw.server as server

args = server.main_setup()
log = logging.getLogger("fixgw")

if args.daemonize:
    try:
        import daemon
        import lockfile
    except ModuleNotFoundError:
        log.error("Unable to load daemon module.")
        raise
    log.debug("Sending to Background")
    context = daemon.DaemonContext(
        #working_directory = '/',
        umask=0o002,
        #pidfile=lockfile.FileLock('/var/run/fixgw.pid'),
    )
    context.signal_map = {
        signal.SIGTERM: server.sig_int_handler,
        signal.SIGINT: server.sig_int_handler,
        signal.SIGHUP: 'terminate',
    }
    with context:
        try:
            server.main(args)
        except Exception as e:
            log.error(str(e))
else:
    server.main(args)
