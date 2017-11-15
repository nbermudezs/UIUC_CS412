__author__ = 'Nestor Bermudez'
__email__ = 'nab6@illinois.edu, nestor.bermudezs@gmail.com'
__copyright__ = 'Copyright (C) 2017 Nestor Bermudez'
__license__ = 'Public Domain'
__version__ = '1.0'

'''
Taken from: https://stackoverflow.com/questions/6974695/python-process-pool-non-daemonic
'''

import multiprocessing.pool
from multiprocessing import Process

class NoDaemonProcess(Process):
    # make 'daemon' attribute always return False
    def _get_daemon(self):
        return False
    def _set_daemon(self, value):
        pass
    daemon = property(_get_daemon, _set_daemon)

class NonDemonicPool(multiprocessing.pool.Pool):
    Process = NoDaemonProcess