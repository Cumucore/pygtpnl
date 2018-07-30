#!/bin/env python3

import logging
from pyroute2.netlink.nlsocket import NetlinkSocket
from pyroute2.netlink import NLM_F_REQUEST
from pyroute2.netlink import NLM_F_ACK
from pyroute2.netlink import NLM_F_CREATE
from pyroute2.netlink import NLM_F_EXCL
from pyroute2.netlink import GENL_ID_CTRL
from pyroute2.iproute import RTM_NEWADDR
from pyroute2.netlink.rtnl import RTM_GETLINK
from pyroute2.netlink import nlmsg
from pyroute2.netlink.rtnl.ifinfmsg import ifinfmsg
import os

GTPA_UNSPEC = 0
GTPA_LINK = 1
GTPA_VERSION = 2
GTPA_TID = 3
GTPA_PEER_ADDRESS = 4
#define GTPA_SGSN_ADDRESS GTPA_PEER_ADDRESS /* maintain legacy attr name */
GTPA_MS_ADDRESS = 5
GTPA_FLOW = 6
GTPA_NET_NS_FD = 7
GTPA_I_TEI = 8
GTPA_O_TEI = 9
GTPA_PAD = 10
__GTPA_MAX = 11

logger = logging.getLogger(__name__)

class gtpmsg(nlmsg):
    fields = ( ... )
    nla_map = ( ()
              )

def tunnel_listp(devname):
    s=NetlinkSocket()
    s.bind()
    #s.put({'index': 1}, RTM_GETLINK)
    #s.get()
    #s.close()

    msg = ifinfmsg()
    nonce = 123

    # fill the protocol-specific fields
    msg['index'] = 85 # index of the interface
    msg['family'] = 18 # address family

    # attach NLA -- it MUST be a list / mutable
    msg['attrs'] = [['CTRL_ATTR_FAMILY_NAME', "gtp0"],
                    ['CTRL_ATTR_FAMILY_NAME', "gtp0"],
                    ['CTRL_ATTR_FAMILY_NAME', "gtp0"],
                    ['CTRL_ATTR_FAMILY_NAME', "gtp0"],
                    ['CTRL_ATTR_FAMILY_NAME', "gtp0"],
                    ['CTRL_ATTR_FAMILY_NAME', "gtp0"],
                   ]

#    msg['attrs'] = [['IFLA_INFO_KIND', "gtp0"],
#                    ['IFA_ADDRESS', '192.162.0.1']]
#
    # fill generic netlink fields
    msg['header']['sequence_number'] = nonce  # an unique seq number
    msg['header']['pid'] = os.getpid()
    msg['header']['type'] = GENL_ID_CTRL
    msg['header']['flags'] = NLM_F_REQUEST |\
                             NLM_F_ACK

    # encode the packet
    msg.encode()

    # send the buffer
    s.sendto(msg.data, (0, 0))
    s.get()
    s.close()

    l=1
    print("tthis is a list; {}".format(l))
    return list

if __name__ == '__main__':
    tunnel_listp("gtp0")

