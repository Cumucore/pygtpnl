'''
Python wrapper for libgtpnl
'''

from ctypes import CDLL,c_int,c_uint16,c_char_p,c_void_p
from ctypes import pointer,byref
from socket import socket,inet_aton,AF_INET,SOCK_DGRAM,AF_NETLINK # IPv4
from struct import unpack
from .gtpsock import GtpSocket
from .structures import *
import logging

from time import sleep

logger = logging.getLogger(__name__)

try:
    lgnl = CDLL("libgtpnl.so")
except OSError:
    logger.error("no libgtpnl.so in search path, check LD_LIBRARY_PATH variable")
    exit(1)

# 2 socks needed, although GTPv0 is not used, use ascii devnames
def dev_create(devname, fd0, fd1):
    bstring = devname.encode('ascii')

    # call libgtpnl to create, mnl dep
    creator = lgnl.gtp_dev_create
    creator.argtypes = [c_int, c_char_p, c_int, c_int]
    try:
        logger.debug("creating device: {} {} {} {}".format(-1, bstring, fd0, fd1))
        creator(-1 , bstring, fd0, fd1)
    # cant catch C errors
    except Exception as e:
        logger.error("{}".format(e))
        exit(1)

    #Open communications 
    sock = GtpSocket()
    sock.discovery()
    return sock

# destroy a gtp dev, kill all, no errors ever, TODO: maybe propagate from C, not trivial
def dev_stop(name):
    dev_destroy = lgnl.gtp_dev_destroy
    bstring = name.encode('ascii')
    dev_destroy.argtypes = [c_char_p]
    dev_destroy(bstring)

'''tunnel_add()

   the tunnel creator requires nlsock address as arg to preserve abstraction level it seems
   Sock is a pyroute2 NetlinkSocket object
'''

def tunnel_add(ns, ue_ip, enb_ip, i_tei, o_tei, devname, sock, ebi=0):
    logger.info("adding tunnel ue:{}, enb:{}, i:{}, o:{}, ebi:{}".format(ue_ip,
                                                                         enb_ip,
                                                                         i_tei,
                                                                         o_tei,
                                                                         ebi))

    ifindex = lgnl.if_nametoindex
    ifindex.argtypes = [c_char_p]
    idx = ifindex(devname.encode('ascii'))
    logger.debug("if_index: {}".format(idx))
    zero = V0(0)
    one = V1(i_tei, o_tei)
    versions = VERSIONS(zero, one)
    ue_bytes = IN_ADDR(unpack("<I", inet_aton(ue_ip))[0])
    enb_bytes = IN_ADDR(unpack("<I", inet_aton(enb_ip))[0])
    # 1 is gtp version
    tunnel = GTPTUNNEL(ns, idx, ue_bytes, enb_bytes, ebi, 1, versions)

    sockaddr = SOCKADDR_NL(sock.family, 0, sock.getsockname()[0], sock.groups)
    logger.debug("sock.pid: {}".format(sock.getsockname()[0]))
    c_sock = MNL_SOCK(sock.fileno(), sockaddr)
    logger.debug("c_sock done")
    logger.debug("c_sock: {}".format(c_sock))

    p_tun = pointer(tunnel)
    p_sock = pointer(c_sock)

    #TODO: pythonize
    if_mnlsock_id = lgnl.genl_lookup_family
    if_mnlsock_id.argtypes = [c_void_p, c_char_p]
    mnlsock_id = if_mnlsock_id(byref(c_sock), devname.encode('ascii'))

    tadd = lgnl.gtp_add_tunnel
    tadd.argtypes = [c_uint16, c_void_p, c_void_p]

    try:
        ret=tadd(mnlsock_id, byref(c_sock), byref(tunnel))
        logger.debug("creating tunnel: {} {} {}".format(mnlsock_id, p_sock.contents, p_tun.contents))
    except Exception as e:
        logger.error("{}".format(e))

def tunnel_del(ns, i_tei, o_tei, devname, sock, ebi=0):
    logger.info("deleting tunnel i:{}, o:{}, ebi:{}".format(i_tei, o_tei, ebi))
    ifindex = lgnl.if_nametoindex
    ifindex.argtypes = [c_char_p]
    idx = ifindex(devname.encode('ascii'))
    zero = V0(0)
    one = V1(i_tei, o_tei)
    versions = VERSIONS(zero, one)
    ue_bytes = IN_ADDR(0)
    enb_bytes = IN_ADDR(0)
    # 1 is gtp version
    tunnel = GTPTUNNEL(ns, idx, ue_bytes, enb_bytes, ebi, 1, versions)
    sockaddr = SOCKADDR_NL(sock.family, 0, sock.getsockname()[0], sock.groups)
    logger.debug("sock.pid: {}".format(sock.pid))

    c_sock = MNL_SOCK(sock.fileno(), sockaddr)
    logger.debug("c_sock done")
    logger.debug("c_sock: {}".format(c_sock))

    #TODO: pythonize
    if_mnlsock_id = lgnl.genl_lookup_family
    if_mnlsock_id.argtypes = [c_void_p, c_char_p]
    mnlsock_id = if_mnlsock_id(byref(c_sock), devname.encode('ascii'))
    logger.debug("mnlsock_id: {}".format(mnlsock_id))

    tdel = lgnl.gtp_del_tunnel
    tdel.argtypes = [c_int, c_void_p, c_void_p]
    try:
        tdel(mnlsock_id, byref(c_sock), byref(tunnel))
    except Exception as e:
        logger.error("{}".format(e))

#uses C to print tunnel list of device, maybe pythonification?
def tunnel_list(devname, sock):
    tlist = lgnl.gtp_list_tunnel
    tlist.argtypes = [c_int, c_void_p]
    if_mnlsock_id = lgnl.genl_lookup_family
    if_mnlsock_id.argtypes = [c_void_p, c_char_p]
    family_id = if_mnlsock_id(sock, devname.encode('ascii'))
    tlist(family_id, sock)

# what is this? TODO: research why mod == del add.
def tunnel_mod(ns, ue_ip, enb_ip, i_tei, o_tei, devname, sock):
    tunnel_del(ns, i_tei, o_tei, devname, sock)
    tunnel_add(ns, ue_ip, enb_ip, i_tei, o_tei, devname, sock)
