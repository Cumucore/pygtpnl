#!/bin/env python3

from pygtpnl import dev_create,dev_stop,tunnel_add,tunnel_del,GtpSocket

def test():
    iplist = ['127.0.0.1',
              -1,
              '45.45.45.45',
              '1722.236.3',
              832675283628376287,
              'hi',
              5,
              2352,
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
    for ns in iplist:
        tunnel_add(-1, '45.45.45.45', '23.23.23.23', 234, 12, "gtp0", s)
        tunnel_del(ns, name, name, name, s)
    s.close()

if __name__ == '__main__':
    test()

