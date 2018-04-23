'''
Python representations of structs used in libgtpnl
'''

from ctypes import Structure, Union
from ctypes import c_ushort, c_int, c_uint16, c_uint32, c_uint64
from ctypes import c_byte

# libgtpnl
class V0(Structure):
    _fields_ = [("tid", c_uint, 64),
                ("flowid", c_uint, 16)
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

# in.h
in_port_t = c_uint16
sa_family_t = c_ushort
class SOCKADDR_IN(Structure):
    _fields_ = [("sin_family", sa_family_t),
                ("sin_port", in_port_t),
                ("sin_addr", IN_ADDR),
                ("sin_zero", c_byte * 8)
               ]

sa_family_t = c_ushort
class SOCKADDR_NL(Structure):
      _fields_ = [("nl_family", sa_family_t),
                  ("nl_pad", c_ushort),
                  ("nl_pid", c_uint32),
                  ("nl_groups", c_uint32)
                 ]

class MNL_SOCK(Structure):
      _fields_ = [("fd", c_int),
                  ("addr", SOCKADDR_NL)
                 ]
# libgtpnl
class GTPTUNNEL(Structure):
      _fields_ = [("ifns", c_int),
                  ("ifidx", c_uint32),
                  ("ms_addr", IN_ADDR),
                  ("sgsn_addr", IN_ADDR),
                  ("gtp_version", c_int),
                  ("u", VERSIONS) #gtp teids
                 ]
