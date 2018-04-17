from pyroute2.netlink import CTRL_CMD_GETFAMILY
from pyroute2.netlink import GENL_ID_CTRL
from pyroute2.netlink import NLM_F_REQUEST
from pyroute2.netlink import ctrlmsg
from pyroute2.netlink.generic import GenericNetlinkSocket
import logging

logger = logging.getLogger(__name__)

'''
pyroute2 low-level socket, with gtp discovery
'''
class GtpSocket(GenericNetlinkSocket):

    def discovery(self):
        '''
        Resolve gtp netlink protocol
        '''
        msg = ctrlmsg()
        msg['cmd'] = CTRL_CMD_GETFAMILY
        msg['version'] = 1
        msg['attrs'].append(['CTRL_ATTR_FAMILY_ID', GENL_ID_CTRL])
        msg['attrs'].append(['CTRL_ATTR_FAMILY_NAME', "gtp"])
        msg['header']['type'] = GENL_ID_CTRL
        msg['header']['flags'] = NLM_F_REQUEST
        msg['header']['pid'] = self.pid
        msg.encode()
        self.sendto(msg.data, (0, 0))
        msg = self.get()[0]
        err = msg['header'].get('error', None)
        if err is not None:
            if hasattr(err, 'code') and err.code == errno.ENOENT:
                logger.error('gtp netlink protocol not found')
                logger.error('Please check if the protocol module is loaded')
            raise err
        return msg
