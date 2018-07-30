#!/usr/bin/env python3

from pygtpnl import dev_create,dev_stop,tunnel_add,tunnel_del,GtpSocket
from time import sleep
from pyroute2 import IPRoute

def test():
    iplist = ['10.0.0.1',
              '45.45.45.45',
              '10.10.1.1',
              '10.10.1.2',
              '10.10.1.3',
              '10.10.1.4',
              '1722.236.3',
              'hi',
             ]
    devnames = ['gtp0',
                'äöäööäö',
                '232323',
                'ggggggggggggggggggggggggggggggggggggggggggggggg',
                 234
               ]
#    s=dev_create(iplist[0], devnamesname[0])
#    dev_stop(name)
    s=GtpSocket()
    s.discovery()
    ip=IPRoute()
    i=ip.link_lookup(ifname="gtp0")
    try:
        for addr in iplist:
            ip.route('add', dst=addr+'/32', oif=i, metrics={'mtu': 1454})
            tunnel_add(-1, addr, '23.23.23.23', 234, 12, "gtp0", s)
    except OSError as e:
        print("OSerror {}".format(e))
        pass
    sleep(123)
    s.close()

if __name__ == '__main__':
    test()

