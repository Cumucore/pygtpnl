#!/bin/env python3

from pygtpnl import dev_create,dev_stop,tunnel_add,tunnel_del

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
    for ip in iplist:
        for name in devnames:
            s=dev_create(ip, name)
            dev_stop(name)
            for ns in iplist:
                tunnel_add(ns, ip, ip, name, name, name, s)
                tunnel_del(ns, name, name, name, s)
            s.close()

if __name__ == '__main__':
    test()

