# -*- coding: utf-8 -*-
"""
    :py:mod:`~credentials.portal.devices` -- supported devices
    ==========================================================

    List of supported devices

    ----

    .. moduleauthor:: Amir Mofakhar <amofakhar@smithmicro.com>

    .. versionadded:: 3.0
"""

__all__ = ['_SUPPORTED_DEVICES', 'check_if_device_supported']

_SUPPORTED_DEVICES = {
    'SONY': '6',
    'Nexus 6': '6',
    'iPhone': '8',
    'SM-G850F': '5.0',
    'D5803': '6.0'
    }


def check_if_device_supported(device_model, os_version):
    """

    :param device_model:
    :param os_version:
    :return:
    """
    if device_model in _SUPPORTED_DEVICES and os_version >= _SUPPORTED_DEVICES[device_model]:
        return True
    return False
