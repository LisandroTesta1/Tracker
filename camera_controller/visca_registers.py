VISCA_registers = {
    'VISCA_BaudRate': (0x00,),
    'Monitoring_Mode': (0x72,),
    'Output_Enabling': (0x73,),
    'Zoom_Limit_Wide': (0x50,),
    'Zoom_Limit_Tele': (0x51,),
    'E-Zoom_Max': (0x52,),
    'StableZoom': (0x53,)
    }

VISCA_BaudRate_options = {
    '9600bps': (0x00, 0x00),
    '19200bps': (0x00, 0x01),
    '38400bps': (0x00, 0x02),
    }

Monitoring_Mode_options = {
    '1080i/60': (0x00, 0x01),
    '1080i/59.94': (0x00, 0x02),
    'NTSC_Analog_Output': (0x00, 0x03),
    '1080i/50': (0x00, 0x04),
    'PAL_Analog_Output': (0x00, 0x05),
    '1080p/30': (0x00, 0x06),
    '1080p/29.97': (0x00, 0x07),
    '1080p/25': (0x00, 0x08),
    '720p/60': (0x00, 0x09),
    '720p/59.94': (0x00, 0x0A),
    '720p/50': (0x00, 0x0C),
    '720p/30': (0x00, 0x0E),
    '720p/29.97': (0x00, 0x0F),
    '720p/25': (0x01, 0x01),
    }


Output_Enabling_options = {
    'Analog_Output_Enabled': (0x00, 0x01),
    'Digital_Output_Enabled': (0x00, 0x02),
    'BothA/D_Output_Enabled': (0x00, 0x03),
    }


StableZoom_options = {
    'Off': (0x00, 0x00),
    'On': (0x00, 0x01)
    }
