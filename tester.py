#!/bin/env python
'''
testing
'''
from pygtpnl import *
from time import sleep

logger = logging.getLogger(__name__)
FORMAT = '%(levelname)-8s - [%(name)-17s %(funcName)26s()] %(message)s'
logging.basicConfig(level="DEBUG",format=FORMAT, datefmt="%Y-%m-%d %H:%M:%S")

if __name__ == "__main__":
    listen = "127.0.0.1"
    devname = "gtp0"
    dev_stop(devname)
    dev_create(listen,devname)
    if_mnlsock = lgnl.genl_socket_open
    if_mnlsock.restype = c_void_p
    #if_mnlsock_id = lgnl.genl_lookup_family
    #if_mnlsock_id.argtypes = [c_void_p, c_char_p]
    sockp = if_mnlsock()
    logger.debug("sockp: {}".format(sockp))
    #sockid = if_mnlsock_id(sockp, devname.encode('ascii'))
    #logger.debug("sockid: {}".format(sockid))
    tunnel_add(-1, listen, listen, 124, 125, devname, sockp)
    tunnel_list(devname, sockp)
    logger.info("deleting and reprinting tunnel list")
    tunnel_del(-1, 124, 125, devname,sockp)
    tunnel_list(devname, sockp)
    logger.info("done")
    sleep(10)
#    dev_stop(devname)

