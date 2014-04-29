#!/usr/bin/env python 
"""Epics Support for
Stanford Research Systems 570 current amplifier
"""
import epics

VALID_STEPS = [1, 2, 5, 10, 20, 50, 100, 200, 500]
VALID_UNITS = ['pA/V', 'nA/V','uA/V', 'mA/V']

class SRS570(epics.Device):
    """ 
    SRS (Stanford Research Systems) 570 current amplifier
    """

    attrs = ('sens_num', 'sens_unit', 'offset_num', 'offset_unit',
             'offset_sign', 'offset_on' 'off_u_put', 'bias_put',
             'gain_mode', 'filter_type', 'invert_on', 'init.PROC')
    

    _fields = ('_prefix', '_pvs', '_delim', '_nchan', '_chans')
    
    def __init__(self, prefix):
        epics.Device.__init__(self, prefix, delim='', attrs=attrs)
        self.initialize()

    def initialize(self, bias=0, gain_mode=0, filter_type=0,
                   invert=False):
        """set initial values"""
        inv_val = 0
        if invert: inv_val = 1
        self.put('gain_mode', gain_mode) # 0 = low noise
        self.put('filter_type', filter_type) # 0  no filter
        self.put('invert_on', inv_val)
        self.put('bias_put', bias)
        
        
    def set_sensitivity(self, value, units):
        "set sensitivity"
        if value not in VALID_STEPS or units not in VALID_UNITS:
            print('invalid input')
            return
        
        ival = VALID_STEPS.index(value)
        uval = VALID_UNITS.index(units)

        self.put('sens_num', ival)
        self.put('sens_unit', uval)
            
        ioff = ival - 3
        uoff = uval
        if ioff < 0:
            ioff = ival + 6
            uoff = uval - 1

        self.put('offest_num',  ioff)
        self.put('offsets_unit', uoff)

