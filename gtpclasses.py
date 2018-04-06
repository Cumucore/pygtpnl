'''
Python representations of structs used in libgtpnl
'''

from ctypes import Structure, Union
from ctypes import c_ushort, c_int, c_uint16, c_uint32, c_uint64
from ctypes import c_byte

# libgtpnl
class V0(Structure):
      _fields_ = [("tid", c_uint64),
                  ("flowid", c_uint16)
                 ]

# libgtpnl
class V1(Structure):
      _fields_ = [("i_tei", c_uint32),
                  ("o_tei", c_uint32)
                 ]

# libgtpnl
class VERSIONS(Union):
      _fields_ = [("v0", V0),
                  ("v1", V1)
                 ]

# in.h
in_addr_t = c_uint32
class IN_ADDR(Structure):
      _fields_ = [("s_addr", in_addr_t)
                 ]

# libgtpnl
in_addr = c_uint32 #32bit
class GTPTUNNEL(Structure):
      _fields_ = [("ifns", c_int),
                  ("ifidx", c_uint32),
                  ("ms_addr", IN_ADDR),
                  ("sgsn_addr", IN_ADDR),
                  ("gtp_version", c_int),
                  ("u", VERSIONS), #gtp teids
                 ]
