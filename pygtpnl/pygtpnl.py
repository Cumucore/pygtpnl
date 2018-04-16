#!/bin/env python3

from ctypes import CDLL,c_int,c_uint16,c_char_p,c_void_p
from ctypes import byref
from socket import socket,inet_aton,AF_INET,SOCK_DGRAM # IPv4
from struct import unpack
from os import environ
import logging
from .structures import *

logger = logging.getLogger(__name__)

try:
    lgnl = CDLL("libgtpnl.so")
except OSError:
    logger.error("no libgtpnl.so in search path, check LD_LIBRARY_PATH variable")
    exit(1)

# 2 socks needed, although GTPv0 is not used, use ascii devnames
def dev_create(ip, devname):
    bstring = devname.encode('ascii')
    sock0 = socket(AF_INET, SOCK_DGRAM)
    sock1 = socket(AF_INET, SOCK_DGRAM)
    #ip_bytes = IN_ADDR(unpack("<I", inet_aton(ip))[0])
    #c_sock0 = SOCKADDR_IN(AF_INET, 3386, ip_bytes, [0]*8)
    #c_sock1 = SOCKADDR_IN(AF_INET, 2152, ip_bytes, [0]*8)

    # sockname tuple str, int
    v0 = (ip, 3386)
    v1 = (ip, 2152)
    try:
        sock0.bind(v0)
        sock1.bind(v1)
    except Exception as e:
        logger.error("bind fail".format(e))
        exit(1)

    # call libgtpnl to do it, mnl dep
    creator = lgnl.gtp_dev_create
    try:
        creator(-1 , bstring, sock0.fileno(), sock1.fileno())
    # cant catch C errors
    except Exception as e:
        logger.error("{}".format(e))
        exit(1)

# destroy a gtp dev, kill all, no errors ever, TODO: maybe propagate from C, not trivial
def dev_stop(name):
    dev_destroy = lgnl.gtp_dev_destroy
    bstring = name.encode('ascii')
    dev_destroy.argtypes = [c_char_p]
    dev_destroy(bstring)

'''the tunnel creator requires nlsock address as arg to  preserve abstraction level it seems
   Sock is a pyroute2 NetlinkSocket object
'''
def tunnel_add(ns, ue_ip, enb_ip, i_tei, o_tei, devname, sock):
    logger.info("adding tunnel ue:{}, enb:{}, i:{}, o:{}".format(ue_ip, enb_ip, i_tei, o_tei))

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
    tunnel = GTPTUNNEL(ns, idx, ue_bytes, enb_bytes, 1, versions)
    sockaddr = SOCKADDR_NL(sock.family, 0, sock.pid, 0)
    logger.debug("sock.pid: {}".format(sock.pid))

    c_sock = MNL_SOCK(sock.fileno(), sockaddr)
    logger.debug("c_sock done")
    logger.debug("c_sock: {}".format(c_sock))

    #what is this sock_id, do it in Python maybe?
    #if_mnlsock_id = lgnl.genl_lookup_family
    #if_mnlsock_id.argtypes = [c_void_p, c_char_p]
    #mnlsock_id = if_mnlsock_id(byref(c_sock), devname.encode('ascii'))
    #mnlsock_id = if_mnlsock_id(sock, devname.encode('ascii'))
    #logger.debug("mnlsock_id: {}".format(mnlsock_id))
    mnlsock_id=28

    tadd = lgnl.gtp_add_tunnel
    tadd.argtypes = [c_uint16, c_void_p, c_void_p]
    try:
        ret=tadd(mnlsock_id, byref(c_sock), byref(tunnel))
        #ret=tadd(mnlsock_id, sock, byref(tunnel))
    except Exception as e:
        logger.error("{}".format(e))

def tunnel_del(ns, i_tei, o_tei, devname, sock):
    logger.info("deleting tunnel i:{}, o:{}".format(i_tei, o_tei))
    ifindex = lgnl.if_nametoindex
    ifindex.argtypes = [c_char_p]
    idx = ifindex(devname.encode('ascii'))
    zero = V0(0)
    one = V1(i_tei, o_tei)
    versions = VERSIONS(zero, one)
    ue_bytes = IN_ADDR(0)
    enb_bytes = IN_ADDR(0)
    # 1 is gtp version
    tunnel = GTPTUNNEL(ns, idx, ue_bytes, enb_bytes, 1, versions)
    sockaddr = SOCKADDR_NL(sock.family, 0, sock.pid, 0)
    logger.debug("sock.pid: {}".format(sock.pid))
    c_sock = MNL_SOCK(sock._sock.fileno(), sockaddr)
    logger.debug("c_sock: {}".format(c_sock))

    #what is this sock_id, do it in Python maybe?
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
