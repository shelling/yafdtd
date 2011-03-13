import math


def update_dfield(plane):
    """
    """
    plane.dxfield += 0.5 * plane.curl_hx()
    plane.dyfield += 0.5 * plane.curl_hy()
    plane.dzfield += 0.5 * plane.curl_hz()
    return plane

def update_efield(plane):
    """
    """
    plane.exfield = plane.dxfield
    plane.eyfield = plane.dyfield
    plane.ezfield = plane.dzfield
    return plane

def update_bfield(plane):
    """
    """
    plane.bxfield -= 0.5 * plane.curl_ex()
    plane.byfield -= 0.5 * plane.curl_ey()
    plane.bzfield -= 0.5 * plane.curl_ez()
    return plane

def update_hfield( plane ):
    """
    """
    plane.hxfield = plane.bxfield
    plane.hyfield = plane.byfield
    plane.hzfield = plane.bzfield
    return plane

