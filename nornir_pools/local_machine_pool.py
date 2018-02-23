'''
Created on Apr 17, 2014

@author: u0490822
'''

import nornir_pools
from . import poolbase

class LocalMachinePool(poolbase.PoolBase):
    '''
    Unified interface for the process and multithreading pools allowing both threads and processes to be launched from the same pool.
    '''

    @property
    def _multithreading_pool(self):
        if self._mtpool is None:
            
            if self.is_global:
                self._mtpool = nornir_pools.GetGlobalMultithreadingPool()
            else:
                self._mtpool = nornir_pools.GetMultithreadingPool(self.Name + " multithreading pool", self._num_threads)
        
        return self._mtpool

    @property
    def _process_pool(self):
        if self._ppool is None:
            if self.is_global:
                self._ppool = nornir_pools.GetGlobalProcessPool()
            else:
                self._ppool = nornir_pools.GetProcessPool(self.Name + " process pool", self._num_threads)
            
        return self._ppool

    def get_active_nodes(self):
        return ["localhost"]

    def __init__(self, num_threads, is_global = False):
        '''
        Constructor
        '''

        self._num_threads = num_threads
        
        self.is_global = is_global
        self._mtpool = None
        self._ppool = None


    def add_task(self, name, func, *args, **kwargs):
        return self._multithreading_pool.add_task(name, func, *args, **kwargs)

    def add_process(self, name, func, *args, **kwargs):
        return self._process_pool.add_process(name, func, *args, **kwargs)

    def wait_completion(self):

        """Wait for completion of all the tasks in the queue"""
        if not self._mtpool is None:
            self._mtpool.wait_completion()
            self._mtpool = None

        if not self._ppool is None:
            self._ppool.wait_completion()
            self._ppool = None

    def shutdown(self):
        self.wait_completion()