### pygtpnl - Python bindings for libgtpnl

Works by calling libgtpnl C functions through ctypes

## Install

sudo is required to install to default env

``` shell
python3 setup.py install
```

## Usage

Write python, and call functions:

``` shell
def dev_create(ip, devname):
def dev_stop(name):
def tunnel_add(ns, ue_ip, enb_ip, i_tei, o_tei, devname, sock):
def tunnel_del(ns, i_tei, o_tei, devname, sock):
def tunnel_list(devname, sock):
def tunnel_mod(ue_ip, enb_ip, i_tei, o_tei):
```

## Requirements

Install libgtpnl, lib search path is LD_LIBRARY_PATH
