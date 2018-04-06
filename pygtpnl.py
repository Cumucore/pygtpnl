#!/bin/env python3

from ctypes import CDLL,c_int,c_char_p,c_void_p
from ctypes import byref
from socket import socket,inet_aton,AF_INET,SOCK_DGRAM # IPv4
from struct import unpack
import logging
from gtpclasses import *
from mnlclass import *

try:
    lgnl = CDLL("./libgtpnl.so")
except OSError:
    logger.error("no libgtpnl .so")
    exit(1)


# 2 socks needed, although GTPv0 is not used, use ascii devnames
def dev_create(ip, devname):
    bstring = devname.encode('ascii')
    sock0 = socket(AF_INET, SOCK_DGRAM)
    sock1 = socket(AF_INET, SOCK_DGRAM)

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
    creator = lgnl.gtp_dev_create_sgsn
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

# the tunnel creator requires nlsock address as arg to  preserve abstraction level it seems
def tunnel_add(ns, ue_ip, enb_ip, i_tei, o_tei, devname, sock):
    ifindex = lgnl.if_nametoindex
    ifindex.argtypes = [c_char_p]
    idx = ifindex(devname.encode('ascii'))
    zero = V0(0)
    one = V1(i_tei, o_tei)
    versions = VERSIONS(zero, one)
    ue_bytes = IN_ADDR(unpack("<I", inet_aton(ue_ip))[0])
    enb_bytes = IN_ADDR(unpack("<I", inet_aton(enb_ip))[0])
    # 1 is gtp version
    tunnel = GTPTUNNEL(ns, idx, ue_bytes, enb_bytes, 1, versions)

    if_mnlsock_id = lgnl.genl_lookup_family
    if_mnlsock_id.argtypes = [c_void_p, c_char_p]
    family_id = if_mnlsock_id(sock, devname.encode('ascii'))

    tadd = lgnl.gtp_add_tunnel
    tadd.argtypes = [c_int, c_void_p, c_void_p]
    try:
        tadd(family_id, sock, byref(tunnel))
    except Exception as e:
        logger.error("{}".format(e))

def tunnel_del(ns, i_tei, o_tei, devname, sock):
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

    if_mnlsock_id = lgnl.genl_lookup_family
    if_mnlsock_id.argtypes = [c_void_p, c_char_p]
    family_id = if_mnlsock_id(sock, devname.encode('ascii'))

    tdel = lgnl.gtp_del_tunnel
    tdel.argtypes = [c_int, c_void_p, c_void_p]
    try:
        tdel(family_id, sock, byref(tunnel))
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
def tunnel_mod(ue_ip, enb_ip, i_tei, o_tei):
    tmod = lgnl.gtp_add_tunnel
 #   tmod.argtypes = [c_int, struct mnl_socket*, gtp_tunnel*]
    try:
        tmod(genl_id, nlsock, tunnel)
    except Exception as e:
        logger.error("{}".format(e))
