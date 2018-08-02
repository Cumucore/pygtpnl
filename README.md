### pygtpnl - Python bindings for libgtpnl

Works by calling libgtpnl C functions through ctypes

## Install

``` shell
python3 setup.py install
pip install -r requirements.txt
```

## Usage

Write python, and call functions:

``` shell
# creates one gtp device endpoint
def dev_create(ip, devname):

# destroys a device
def dev_stop(name):

# adds a GTP-U tunnel
def tunnel_add(ns, ue_ip, enb_ip, i_tei, o_tei, devname, sock):

# deletes a tunnel
def tunnel_del(ns, i_tei, o_tei, devname, sock):

# placeholder, most likely not working
def tunnel_list(devname, sock):

# wrapper fun, to replace a tunnel
def tunnel_mod(ue_ip, enb_ip, i_tei, o_tei):
```

## Requirements

Install libgtpnl, lib search path is LD_LIBRARY_PATH
