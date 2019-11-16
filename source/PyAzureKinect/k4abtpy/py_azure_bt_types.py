"""This module defines the types used in the k4a library. This is based on
the Azure Kinect Sensor SDK 1.0.6

.. WARNING :: This is intended to be an internal file. Users are advised to use
the k4a module (i.e. "import k4a").

Copyright (C) Microsoft Corporation. All rights reserved.
"""

import ctypes
from enum import Enum


class k4abt_joint_confidence_level_t(Enum):
    """Joint Confidence Level returned by Azure Kinect APIs.

    ======================= ===================================================
    Name                    Definition
    ======================= ===================================================
    K4ABT_JOINT_CONFIDENCE_NONE             The joint is out of range (too far from depth camera)
    K4ABT_JOINT_CONFIDENCE_LOW              The joint is not observed (likely due to occlusion), predicted joint pose.
    K4ABT_JOINT_CONFIDENCE_MEDIUM           Medium confidence in joint pose.
    K4ABT_JOINT_CONFIDENCE_HIGH             High confidence in joint pose.
    K4ABT_JOINT_CONFIDENCE_LEVELS_COUNT     The total number of confidence levels.
    ======================= ===================================================
    """
    K4ABT_JOINT_CONFIDENCE_NONE = 0
    K4ABT_JOINT_CONFIDENCE_LOW = 1
    K4ABT_JOINT_CONFIDENCE_MEDIUM = 2
    K4ABT_JOINT_CONFIDENCE_HIGH = 3
    K4ABT_JOINT_CONFIDENCE_LEVELS_COUNT = 4

class k4abt_joint_id_t(Enum):
    """Joint ID Numbers Azure Kinect APIs.

    ======================= ===================================================
    Name                    Definition
    ======================= ===================================================
    Joint ID Numbers
    ======================= ===================================================
    """
    K4ABT_JOINT_PELVIS = 0
    K4ABT_JOINT_SPINE_NAVAL = 1
    K4ABT_JOINT_SPINE_CHEST = 2
    K4ABT_JOINT_NECK = 3
    K4ABT_JOINT_CLAVICLE_LEFT = 4
    K4ABT_JOINT_SHOULDER_LEFT = 5
    K4ABT_JOINT_ELBOW_LEFT = 6
    K4ABT_JOINT_WRIST_LEFT = 7
    K4ABT_JOINT_HAND_LEFT = 8
    K4ABT_JOINT_HANDTIP_LEFT = 9
    K4ABT_JOINT_THUMB_LEFT = 10
    K4ABT_JOINT_CLAVICLE_RIGHT = 11
    K4ABT_JOINT_SHOULDER_RIGHT = 12
    K4ABT_JOINT_ELBOW_RIGHT = 13
    K4ABT_JOINT_WRIST_RIGHT = 14
    K4ABT_JOINT_HAND_RIGHT = 15
    K4ABT_JOINT_HANDTIP_RIGHT = 16
    K4ABT_JOINT_THUMB_RIGHT = 17
    K4ABT_JOINT_HIP_LEFT = 18
    K4ABT_JOINT_KNEE_LEFT = 19
    K4ABT_JOINT_ANKLE_LEFT = 20
    K4ABT_JOINT_FOOT_LEFT = 21
    K4ABT_JOINT_HIP_RIGHT = 22
    K4ABT_JOINT_KNEE_RIGHT = 23
    K4ABT_JOINT_ANKLE_RIGHT = 24
    K4ABT_JOINT_FOOT_RIGHT = 25
    K4ABT_JOINT_HEAD = 26
    K4ABT_JOINT_NOSE = 27
    K4ABT_JOINT_EYE_LEFT = 28
    K4ABT_JOINT_EAR_LEFT = 29
    K4ABT_JOINT_EYE_RIGHT = 30
    K4ABT_JOINT_EAR_RIGHT = 31
    K4ABT_JOINT_COUNT = 32

class k4abt_body_t(ctypes.Structure):
    """k4abt_body_t Structure

    ======================= ===================================================
    Name                    Definition
    ======================= ===================================================
    id                      An id for the body that can be 
                            used for frame-to-frame correlation.
    skeleton                The skeleton information for the body.
    ======================= ===================================================
    """
    _fields_ = [
        ('id', ctypes.c_uint32),
        ('skeleton', k4abt_skeleton_t)
    ]

    def __str__(self):
        """Returns field: value as a string."""
        return "{}: {{{}}}".format(self.__class__.__name__,
            ", ".join(["{}: {}".format(field[0], getattr(self, field[0]))
            for field in self._fields_]))
    
    def get(self, key:str):
        for field in self._fields_:
            if (field[0] is key):
                return getattr(self, field[0])
        # Key not found, return None
        return None

class k4abt_skeleton_t(ctypes.Structure):
    """k4abt_skeleton_t Structure

    ======================= ===================================================
    Name                    Definition
    ======================= ===================================================
    joints                  The joints for the body.
    ======================= ===================================================
    """
    _fields_ = [
        ('joints', k4abt_joint_t)
    ]

    def __str__(self):
        """Returns field: value as a string."""
        return "{}: {{{}}}".format(self.__class__.__name__,
            ", ".join(["{}: {}".format(field[0], getattr(self, field[0]))
            for field in self._fields_]))
    
    def get(self, key:str):
        for field in self._fields_:
            if (field[0] is key):
                return getattr(self, field[0])
        # Key not found, return None
        return None

class k4abt_joint_t(ctypes.Structure):
    """k4abt_joint_t Structure

    ======================= ===================================================
    Name                    Definition
    ======================= ===================================================
    positions               The position of the joint specified in millimeters.
    orientation             The orientation of the joint specified in normalized quaternion.
    confidence_level        The confidence level of the joint.
    ======================= ===================================================
    """
    _fields_ = [
        ('position', k4a_float3_t),
        ('orientation', k4a_quaternion_t),
        ('confidence_level', k4abt_joint_confidence_level_t)
    ]

    def __str__(self):
        """Returns field: value as a string."""
        return "{}: {{{}}}".format(self.__class__.__name__,
            ", ".join(["{}: {}".format(field[0], getattr(self, field[0]))
            for field in self._fields_]))
    
    def get(self, key:str):
        for field in self._fields_:
            if (field[0] is key):
                return getattr(self, field[0])
        # Key not found, return None
        return None

class k4a_quaternion_t::_wxyz(ctypes.Structure):
    """k4a_quaternion_t::_wxyz Structure

    ======================= ===================================================
    Name                    Definition
    ======================= ===================================================
    positions               The position of the joint specified in millimeters.
    orientation             The orientation of the joint specified in normalized quaternion.
    confidence_level        The confidence level of the joint.
    ======================= ===================================================
    """
    _fields_ = [
        ('w', ctypes.c_float),
        ('x', ctypes.c_float),
        ('y', ctypes.c_float),
        ('z', ctypes.c_float)
    ]

    def __str__(self):
        """Returns field: value as a string."""
        return "{}: {{{}}}".format(self.__class__.__name__,
            ", ".join(["{}: {}".format(field[0], getattr(self, field[0]))
            for field in self._fields_]))
    
    def get(self, key:str):
        for field in self._fields_:
            if (field[0] is key):
                return getattr(self, field[0])
        # Key not found, return None
        return None

class k4a_float3_t::_xyz(ctypes.Structure):
    """k4a_float3_t::_xyz Structure

    ======================= ===================================================
    Name                    Definition
    ======================= ===================================================
    x               X component of a vector.
    y               Y component of a vector.
    z               Z component of a vector.
    ======================= ===================================================
    """
    _fields_ = [
        ('x', ctypes.c_float),
        ('y', ctypes.c_float),
        ('z', ctypes.c_float)
    ]

    def __str__(self):
        """Returns field: value as a string."""
        return "{}: {{{}}}".format(self.__class__.__name__,
            ", ".join(["{}: {}".format(field[0], getattr(self, field[0]))
            for field in self._fields_]))
    
    def get(self, key:str):
        for field in self._fields_:
            if (field[0] is key):
                return getattr(self, field[0])
        # Key not found, return None
        return None

class k4a_float3_t(ctypes.Union):
    """k4abt_joint_t Union

    ======================= ===================================================
    Name                    Definition
    ======================= ===================================================
    positions               The position of the joint specified in millimeters.
    orientation             The orientation of the joint specified in normalized quaternion.
    confidence_level        The confidence level of the joint.
    ======================= ===================================================
    """
    _fields_ = [
        ('xyz', k4a_float3_t::_xyz),
        ('v', ctypes.c_float *3)
    ]

    def __str__(self):
        """Returns field: value as a string."""
        return "{}: {{{}}}".format(self.__class__.__name__,
            ", ".join(["{}: {}".format(field[0], getattr(self, field[0]))
            for field in self._fields_]))
    
    def get(self, key:str):
        for field in self._fields_:
            if (field[0] is key):
                return getattr(self, field[0])
        # Key not found, return None
        return None

class k4a_quaternion_t(ctypes.Union):
    """Versions returned by Azure Kinect APIs.

    ======================= ===================================================
    Name                    Definition
    ======================= ===================================================
    wxyz                   W, X, Y, Z representation of a quaternion.
    v                       Array representation of a quaternion.
    ======================= ===================================================
    """
    _fields_ = [
        ('wxyz', k4a_quaternion_t::_wxyz),
        ('v', ctypes.c_float * 4)
    ]

    def __str__(self):
        """Returns field: value as a string."""
        return "{}: {{{}}}".format(self.__class__.__name__,
            ", ".join(["{}: {}".format(field[0], getattr(self, field[0]))
            for field in self._fields_]))
    
    def get(self, key:str):
        for field in self._fields_:
            if (field[0] is key):
                return getattr(self, field[0])
        # Key not found, return None
        return None
