from . import visca_packet as vp
from . import visca_commands as vc
import queue

BROADCAST_ADDRESS = 0x8

class VISCACommandInterpreter:

    def __init__(self, device_address, cmd_queue):
        self.__cmd_queue = cmd_queue
        self.__device_address = device_address
        #self.__digital_zoom_


    def AddressSet(self):
        """
        Address setting for the peripheral device
        """
        message = vc.AddressSet_cmd + (self.__device_address,)
        packet = vp.VISCAPacket(BROADCAST_ADDRESS, message)
        self.__cmd_queue.put(packet)        


    def IF_Clear(self):
        """
        Clears the command buffers in the FCB camera and cancels the command 
        currently being executed.
        """
        packet = vp.VISCAPacket(BROADCAST_ADDRESS, vc.IF_Clear_cmd)
        self.__cmd_queue.put(packet)


    def CAM_Power(self, command):
        """
        Camera Power ON/OFF

        Keyword Arguments:
        command -- 'On' or 'Off'
        """
        packet = vp.VISCAPacket(self.__device_address,\
            vc.CAM_Power_cmd[command])
        self.__cmd_queue.put(packet)


    def CAM_Zoom(self, command, option=None):
        """
        Camera Zoom Setting

        Keyword Arguments:
        command -- 'Stop', 'Tele_Standard', 'Wide_Standard', 'Tele_Variable',\
                    'Wide_Variable', 'Direct'
        option -- For 'Tele_Variable': 'Zoom_TV_Speed_X' -> X=[0-7]
                  For 'Wide_Variable': 'Zoom_WV_Speed_X' -> X=[0-7]
                  For 'Direct': 'Zoom_xX' -> X = [1-30], or values = [0x0000-\
                    0x4000]
        """    
        try:
            message = vc.CAM_Zoom_cmd[command]
        except KeyError:
            raise ValueError("Invalid Command") 
        else:
            #print("Message: {}".format(message))
            
            # Check for different types of zoom
            if (command == 'Tele_Variable'):
                message += vc.CAM_Zoom_Tele_Variable_options[option]
            elif (command == 'Wide_Variable'):
                message += vc.CAM_Zoom_Wide_Variable_options[option]
            elif (command == 'Direct'):
                # Check if the option is one the reference zoom value
                if (option in vc.CAM_Zoom_Direct_options.keys()):
                    message += vc.CAM_Zoom_Direct_options[option]
                # If not, the value could be given as an exact zoom position
                elif (isinstance(option, int) and (option >= 0 and\
                    option <= vc.ZOOM_MAX_VALUE)):
                    zoom_value=[]
                    for i in range(vc.ZOOM_DIGITS):
                        zoom_value.append((option >> (i*vc.ZOOM_DIGITS)) & 0xF)
                    zoom_value.reverse()
                    message += tuple(zoom_value)
                # Otherwise, raise an error
                else:
                    raise ValueError("Invalid option")

            packet = vp.VISCAPacket(self.__device_address, message)
            self.__cmd_queue.put(packet)


    def CAM_DZoom(self, command, option=None ):
        """
        Camera Digital Zoom configuration and handling

        Keyword Arguments:
        command -- 'On','Off','Combine_Mode','Separate_Mode','Stop',\
            'Tele_Variable', 'Wide_Variable', 'x1_Max', 'Direct'
        option -- For 'Tele_Variable': 'DZoom_TV_Speed_X' -> X=[0-7]
                  For 'Wide_Variable': 'DZoom_WV_Speed_X' -> X=[0-7]
                  For 'Direct': 'DZoom_xX' -> X = [1-12]
        """
        try:
            message = vc.CAM_DZoom_cmd[command]
        except KeyError:
            raise ValueError("Invalid Command") 
        else:
            if (command == 'Tele_Variable'):
                message += vc.CAM_DZoom_Tele_Variable_options[option]
            elif (command == 'Wide_Variable'):
                message += vc.CAM_DZoom_Wide_Variable_options[option]
            elif (command == 'Direct'):
                # Check if the option is one the reference zoom value
                if (option in vc.CAM_DZoom_Direct_SM_options.keys()):
                    message += vc.CAM_DZoom_Direct_SM_options[option]
                # If not, the value could be given as an exact zoom position
                elif (isinstance(option, int) and ((option >= 0) and\
                    option <= vc.DZOOM_SM_MAX_VALUE)):
                    zoom_value=[]
                    for i in range(vc.DZOOM_DIGITS):
                        zoom_value.append((option >> (i*vc.DZOOM_DIGITS)) & 0xF)
                    zoom_value.reverse()
                    message += tuple(zoom_value)
                # Otherwise, raise an error
                else:
                    raise ValueError("Invalid option")

            packet = vp.VISCAPacket(self.__device_address, message)
            self.__cmd_queue.put(packet)


    def CAM_Focus(self, command, options=None):
        pass


    def AF_Sensitivity(self, command):
        """
        Sets Auto Focus sensitivity

        Keywords Argument:
        command -- 'Normal', 'Low'
        """
        packet = vp.VISCAPacket(self.__device_address,\
            vc.AF_Sensivity_cmd[command])
        self.__cmd_queue.put(packet)


    def CAM_AFMode(self, command, movtime=0, interval=0):
        """
        Sets Auto Focus movement mode

        Keywords Argument:
        command -- 'Normal_AF','Interval_AF', 'Zoom_Trigger_AF',\
            'Active_Interval_Time'

        Only for 'Active_Interval_Time' command:
        movtime -- Auto-Focus Active Time in seconds =[0x00 - 0xFF](default = 0)
        interval -- Auto-Focus Interval Time in seconds =[0x00 - 0xFF]\
            (default = 0)
        """
        message = vc.CAM_AFMode_cmd[command]
        if (command == 'Active_Interval_Time'):
            # Check if the arguments are in the range [0x00 - 0xFF]
            if((movtime < 0 or movtime > 0xFF) or\
                (interval < 0 or interval > 0xFF)):
                raise ValueError("Los valores ingresados estan fuera de rango")
            else:
                af_movtime = ((movtime >> 4) & 0xF, movtime & 0xF)
                af_interval = ((interval >> 4) & 0xF, interval & 0xF)
                message += af_movtime + af_interval
        packet = vp.VISCAPacket(self.__device_address, message)
        self.__cmd_queue.pùt(packet)


    def CAM_IRCorrection(self, command):
        """
        FOCUS IR compensation data switching

        Keyword Arguments:
        command -- 'Standard', 'IR_Light'
        """
        packet = vp.VISCAPacket(self.__device_address,\
            vc.CAM_IRCorrection_cmd[command])
        self.__cmd_queue.put(packet)


    def CAM_ZoomFocus(self, zoomposition=None, focusposition=None):
        pass   


    def CAM_Initialize(self, command):
        """ 
        Lens initializing or camera reset

        Argument Keywords:
        command -- 'Lens', 'Camera'
        """
        packet = vp.VISCAPacket(self.__device_address,\
            vc.CAM_Initialize_cmd[command])
        self.__cmd_queue.put(packet)


    def CAM_WB(self, command):
        pass


    def CAM_RGain(self, command, rgain=None):
        pass


    def CAM_BGain(self, command, bgain=None):
        pass


    def CAM_AE(self, command):
        pass


    def CAM_SlowShutter(self, command):
        pass


    def CAM_Shutter(self, command, shutterpos=None):
        pass


    def CAM_Iris(self, command, irispos=None):
        pass


    def CAM_Gain(self, command, gainpos=None):
        pass


    def CAM_Bright(self, command, brightpos=None):
        pass


    def CAM_Stabilizer(self, command):
        pass


    def CAM_ExpComp(self, command, excomppos=None):
        pass


    def CAM_BackLight(self, command):
        pass


    def CAM_SpotAE(self, command, xpos=None, ypos=None):
        pass


    def CAM_AE_Response(self, command, setting=None):
        pass


    def CAM_WD(self, command, screedis=None, detsens=None, blkdup_sh_corr=None,\
        blownout_hglt_corr=None, expratio=None):
        pass


    def CAM_WDAlarmReply(self, command):
        pass


    def CAM_Aperture(self, command, apgain=None):
        pass


    def CAM_HR(self, command):
        pass


    def CAM_NR(self, nrsetting):
        pass


    def CAM_Gamma(self, gammasetting):
        pass


    def CAM_HighSensitivity(self, command):
        pass


    def CAM_LR_Reverse(self, command):
        pass


    def CAM_Freeze(self, commamd):
        pass


    def CAM_PictureEffect(self, command):
        pass


    def CAM_PictureFlip(self, command):
        pass


    def CAM_ICR(self, command):
        pass


    def CAM_AutoICR(self, command, thresholdlevel=None):
        pass


    def CAM_AutoICRAlarmReply(self, command):
        pass


    def CAM_Memory(self, command, memnumber):
        pass


    def CAM_CUSTOM(self, command):
        pass


    def CAM_MemSave(self, address, data):
        pass


    def CAM_Display(self, command):
        pass


    def CAM_Mute(self, command):
        pass


    def CAM_IDWrite(self, cameraid):
        pass


    def CAM_ContinuousZoomPosReply(self, command):
        pass


    def CAM_ReplyIntervalTimeSet(self, intervaltime):
        pass


    def CAM_RegisterValue(self, regnum, regvalue):
        pass


    def CAM_ColorEnhance(self, command, fbyte_thres, sbyte_thres, tbyte_thres,\
        lowcolor, highcolor):
        pass


    def CAM_ChromaSuppress(self, level):
        pass


    def CAM_ColorGain(self, colorgain):
        pass


    def CAM_ColorHue(self, colorhue):
        pass
