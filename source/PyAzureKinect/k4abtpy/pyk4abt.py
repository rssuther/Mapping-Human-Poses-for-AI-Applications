"""This module defines the Python top-level interface for the k4a library.

================ ===============    ===========================================
Attribute        Type               Description (sizes in bytes)
================ ===============    ===========================================
None
================ ===============    ===========================================

Summary of k4a.dll functions that are also implemented here:
============================== ================================================
DLL Function                   Equivalent fsf_file_handler.py function
============================== ================================================

============================== ================================================

Copyright (C) Microsoft Corporation. All rights reserved.
"""


import os
import ctypes
#from k4apy.k4a_types import *


class K4A:
    """Class that handles top-level transactions between python and k4a.dll.

    ================= =============== =========================================
    Attribute         Type               Description (sizes in bytes)
    ================= =============== =========================================
    
    ================= =============== =========================================

    Summary of functions that are implemented here:
    ============================== ============================================
    Function                       Purpose
    ============================== ============================================
    
    ============================== ============================================
    """

    # Static class members.
    _k4a_dll = None
    _depthengine_dll = None
    _k4abt_dll = None


    def __init__(self):
        """Loads the k4a.dll into Python.
        """
        libdir = os.path.join(os.path.dirname(__file__), 'lib')

        if libdir not in os.environ['PATH']:
            os.environ['PATH'] = libdir + os.pathsep + os.environ['PATH']

        if self._k4a_dll is None:
            self._k4a_dll = ctypes.windll.LoadLibrary(
                os.path.join(libdir, 'k4a.dll'))
        
        # It seems adding the lib directory in the PATH environment variable is
        # not sufficient for k4a.dll to find depthengine_1_0.dll. A workaround
        # is to load it ourselves.
        if self._depthengine_dll is None:
            self._depthengine_dll = ctypes.windll.LoadLibrary(
                os.path.join(libdir, 'depthengine_1_0.dll'))

        if self._k4abt_dll is None:
            self._k4abt_dll = ctypes.windll.LoadLibrary(
                os.path.join(libdir, 'k4abttypes.dll'))

    def __del__(self):
        """Do not release the DLLs in case another instance needs it.
        Just let it be released when the application ends.
        """

    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        """Do not release the DLLs in case another instance needs it.
        Just let it be released when the application ends.
        """
