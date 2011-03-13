import math

def update_dfield(self):
    """
    """
    self.dxfield += 0.5 * self.curl_hx()
    self.dyfield += 0.5 * self.curl_hy()
    self.dzfield += 0.5 * self.curl_hz()
    return self

def update_efield(self):
    """
    """
    self.exfield = self.dxfield
    self.eyfield = self.dyfield
    self.ezfield = self.dzfield
    return self

def update_bfield(self):
    """
    """
    self.bxfield -= 0.5 * self.curl_ex()
    self.byfield -= 0.5 * self.curl_ey()
    self.bzfield -= 0.5 * self.curl_ez()
    return self

def update_hfield(self):
    """
    """
    self.hxfield = self.bxfield
    self.hyfield = self.byfield
    self.hzfield = self.bzfield
    return self
