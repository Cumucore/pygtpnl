'''
Python representations of structs used in libmnl
'''

from ctypes import Structure
from ctypes import c_ushort, c_int, c_uint32

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
