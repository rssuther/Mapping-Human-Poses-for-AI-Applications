'''
    A simple server that listens for a command to start capturing N frames from
    a connected Azure Kinect device on the machine. It will send back the captured
    depth and color images.
'''

import sys
import urllib
import time
import numpy as np
import pickle
import cv2
from functools import partial
from http.server import HTTPServer, BaseHTTPRequestHandler
import k4apy.k4a as k4a
from k4apy.k4a_types import *
from k4apy.k4a_image import *
from k4apy.k4a_capture import *
from k4apy.k4a_device import *

from RemoteCapture.constants import *

class AzureKinectRequestHandler(BaseHTTPRequestHandler):
    '''
        Class that handles HTTP GET requests.
    '''

    DEVICES = [None, None]
    DEVICES_DMODE = [None, None]

    def __str__(self):
        return  str(self.__class__) + '\n'+ '\n'.join(('{} = {}'.format(item, self.__dict__[item]) for item in self.__dict__))
    
    
    '''
        do_get()
        This function determines what type of request was sent by the client side and calls the appropriate handler function
    '''
    def do_GET(self):

        print('Received a ' + self.command + ' command from ' + self.client_address[0] + ":" + str(self.client_address[1]))

        requestHandler = {
            START_REQUEST_ID : self.start_device,
            STOP_REQUEST_ID : self.stop_device, 
            SET_DCONFIG_REQUEST_ID : self.set_device_config,
            GET_DCONFIG_REQUEST_ID : self.get_device_config, 
            GET_DINTRIN_REQUEST_ID : self.get_intrinsic_param,
            GET_DINFO_REQUEST_ID : self.get_device_info,
            CAP_FRAME_REQUEST_ID : self.capture_frame,
            }

        # Parse request type
        requestType = int(self.headers['RequestID'])
        print(requestType)
        requestHandler[requestType]()
        
    
    '''
        __send_error_response__()
        This function is an internal function that sends an error message (error) to the calling client.
        @param error: An error message or value to send back to the calling client upon error
    '''
    def __send_error_response__(self, error):

        deviceIndex = int(self.headers['DeviceIndex'])
        testMode = int(self.headers['TestMode'])

        self.send_response(200)
        self.send_header('ResponseID', ERROR_RESPONSE_ID)
        self.send_header('DeviceIndex', deviceIndex)
        self.send_header('TestMode', testMode)
        self.end_headers()
        self.wfile.write(bytes(error.encode('utf-8')))
        return

    
    '''
        __parse_device_config__()
        This function is an internal function used to reconstruct a k4a_device_configuration_t structure from headder data
    '''
    def __parse_device_config__(self):

        deviceConfigBytes = bytes((self.headers['DeviceConfig']).encode('utf-8'))
        deviceConfig = k4a_device_configuration_t(int(deviceConfigBytes[0]), int(deviceConfigBytes[4]), int(deviceConfigBytes[8]), int(deviceConfigBytes[12]), int(deviceConfigBytes[16]), int(deviceConfigBytes[20]), int(deviceConfigBytes[24]), int(deviceConfigBytes[28]))
        self.DEVICES_DMODE[int(self.headers['DeviceIndex'])] = int(deviceConfigBytes[8])
        return deviceConfig

    
    '''
        start_device()
        This function handles HTTP-GET Device Start Requests to the remote server. 
            The specified device is started with the provided configuration
    '''
    def start_device(self):

        deviceIndex = int(self.headers['DeviceIndex'])
        deviceConfig = self.__parse_device_config__()
        testMode = int(self.headers['TestMode'])

        #POST Not SUpported by BaseHTTPRequestHandler
        #deviceConfig = pickle.loads(self.rfile.read())

        if (testMode):

            print(deviceConfig)
            self.send_response(200)
            self.send_header('ResponseID', START_RESPONSE_ID)
            self.send_header('DeviceIndex', deviceIndex)
            self.send_header('TestMode', testMode)
            self.end_headers()
            self.wfile.write(bytes(r'TESTMODE: start_device'.encode('utf-8')))
            return

        if (self.DEVICES[deviceIndex] is None):

            with k4a.K4A() as k4aObj:

                # Get device.
                #with k4aObj.device_open(deviceIndex) as device:
                self.DEVICES[deviceIndex] =k4aObj.device_open(deviceIndex)

                # Start the cameras.
                self.DEVICES[deviceIndex].start_cameras(deviceConfig)
                
                # Set Local Devices Config Variable
                #self.DEVICES_DMODE[deviceIndex] = deviceConfig 
        
        else:
            self.__send_error_response__('Device Already Started')
            return

        self.send_response(200)
        self.send_header('ResponseID', START_RESPONSE_ID)
        self.send_header('DeviceIndex', deviceIndex)
        self.send_header('TestMode', testMode)
        self.end_headers()
        self.wfile.write(bytes(r'Device Started'.encode('utf-8')))
        return


    '''
        stop_device()
        This function handles HTTP-GET Device Stop Requests to the remote server. 
    '''
    def stop_device(self):
        
        deviceIndex = int(self.headers['DeviceIndex'])
        testMode = int(self.headers['TestMode'])

        if (testMode):
            self.send_response(200)
            self.send_header('ResponseID', STOP_RESPONSE_ID)
            self.send_header('DeviceIndex', deviceIndex)
            self.send_header('TestMode', testMode)
            self.end_headers()
            self.wfile.write(bytes(r'TESTMODE: stop_device'.encode('utf-8')))
            return

        #with k4a.K4A() as k4aObj:

            # Get device.
            #with k4aObj.device_open(deviceIndex) as device:

        # Stop the cameras.

        if (self.DEVICES[deviceIndex] is not None):
            # Stop Device Cameras and Clear Local State
            self.DEVICES[deviceIndex].stop_cameras()
            self.DEVICES[deviceIndex] = None
            # Clear Local Devices Config Variable
            self.DEVICES_DMODE[deviceIndex] = None 
        else:
            self.__send_error_response__('Device Not Started Prior to Stop Request')
            return
            
        self.send_response(200)
        self.send_header('ResponseID', STOP_RESPONSE_ID)
        self.send_header('DeviceIndex', deviceIndex)
        self.send_header('TestMode', testMode)
        self.end_headers()
        self.wfile.write(bytes(r'Device Stopped'.encode('utf-8')))
        return

    
    '''
        set_device_config()
        This function handles HTTP-GET Requests to set the specified device's configuration on the remote server. 
    '''
    def set_device_config(self):

        deviceIndex = int(self.headers['DeviceIndex'])
        deviceConfig = self.__parse_device_config__()
        deviceWB = int(self.headers['WBValue'])
        deviceExposure = int(self.headers['ExposureValue'])
        deviceISOSpeed = int(self.headers['ISOSpeedValue'])
        testMode = int(self.headers['TestMode'])
        
        #POST Not SUpported by BaseHTTPRequestHandler
        #deviceConfig = pickle.loads(self.rfile.read())

        if (testMode):
            self.send_response(200)
            self.send_header('ResponseID', SET_DCONFIG_RESPONSE_ID)
            self.send_header('DeviceIndex', deviceIndex)
            self.send_header('TestMode', testMode)
            self.end_headers()
            self.wfile.write(bytes(r'TESTMODE: set_device_config'.encode('utf-8')))
            return

        #with k4a.K4A() as k4aObj:

            # Get device.
            #with k4aObj.device_open(deviceIndex) as device:

        if (self.DEVICES[deviceIndex] is None):
            self.__send_error_response__('Device Has Not Been Started')
            return
        # Stop the cameras.
        self.DEVICES[deviceIndex].stop_cameras()

                # Apply Config
                
                ## K4APY Fucntionality Needed for setting WB, Exposure, ISO

        # Start the cameras.
        self.DEVICES[deviceIndex].start_cameras(deviceConfig)
        
        # Set Local Devices Config Variable
        #self.DEVICES_DMODE[deviceIndex] = deviceConfig 

            
        self.send_response(200)
        self.send_header('ResponseID', SET_DCONFIG_RESPONSE_ID)
        self.send_header('DeviceIndex', deviceIndex)
        self.send_header('TestMode', testMode)
        self.end_headers()
        self.wfile.write(bytes(r'Device Config Set'.encode('utf-8')))
        return

    
    '''
        get_device_config()
        This function handles HTTP-GET Requests to get the specified device's configuration and return it to the calling client. 
    '''
    def get_device_config(self):
        
        ## FOR TESTING PURPOSES

        deviceIndex = int(self.headers['DeviceIndex'])
        testMode = int(self.headers['TestMode'])

        device_config_param = {
            'deviceConfig': self.DEVICES_DMODE[deviceIndex], 
            'deviceWB': 10,
            'deviceExposure': 20,
            'deviceISOSpeed': 30 
            }


        if (testMode):
            self.send_response(200)
            self.send_header('ResponseID', GET_DCONFIG_RESPONSE_ID)
            self.send_header('DeviceIndex', deviceIndex)
            self.send_header('TestMode', testMode)
            self.end_headers()
            self.wfile.write(bytes(r'TESTMODE: get_device_config'.encode('utf-8')))
            return


        if (self.DEVICES[deviceIndex] is None):
            self.__send_error_response__('Device Has Not Been Started')
            return

        self.send_response(200)
        self.send_header('ResponseID', GET_DCONFIG_RESPONSE_ID)
        self.send_header('DeviceIndex', deviceIndex)
        self.send_header('DeviceConfig', device_config_param['deviceConfig'])
        self.send_header('WBValue', device_config_param['deviceWB'])
        self.send_header('ExposureValue', device_config_param['deviceExposure'])
        self.send_header('ISOSpeedValue', device_config_param['deviceISOSpeed'])
        self.send_header('TestMode', testMode)
        self.end_headers()

        pickled_config = pickle.dumps(device_config_param)

        self.wfile.write(pickled_config)
        return
    

    '''
        __parse_depth_mode__()
        This function is an internal function and is used to extrapolate the k4a_detph_mode_t value used by get_intrinsic_param().
    '''
    def __parse_depth_mode__(self):

        depth_modes = {
                k4a_depth_mode_t.K4A_DEPTH_MODE_OFF.value : k4a_depth_mode_t.K4A_DEPTH_MODE_OFF,
                k4a_depth_mode_t.K4A_DEPTH_MODE_NFOV_2X2BINNED.value : k4a_depth_mode_t.K4A_DEPTH_MODE_NFOV_2X2BINNED,
                k4a_depth_mode_t.K4A_DEPTH_MODE_NFOV_UNBINNED.value : k4a_depth_mode_t.K4A_DEPTH_MODE_NFOV_UNBINNED,
                k4a_depth_mode_t.K4A_DEPTH_MODE_WFOV_2X2BINNED.value : k4a_depth_mode_t.K4A_DEPTH_MODE_WFOV_2X2BINNED,
                k4a_depth_mode_t.K4A_DEPTH_MODE_WFOV_UNBINNED.value : k4a_depth_mode_t.K4A_DEPTH_MODE_WFOV_UNBINNED,
                k4a_depth_mode_t.K4A_DEPTH_MODE_PASSIVE_IR.value : k4a_depth_mode_t.K4A_DEPTH_MODE_PASSIVE_IR

        }

        return depth_modes[int(self.headers['DepthMode'])]

    
    '''
        __parse_color_resolution__()
        This function is an internal function and is used to extrapolate the k4a_color_resolution_t value used by get_intrinsic_param().
    '''
    def __parse_color_resolution__(self):

        color_resolutions = {
                k4a_color_resolution_t.K4A_COLOR_RESOLUTION_OFF.value : k4a_color_resolution_t.K4A_COLOR_RESOLUTION_OFF,
                k4a_color_resolution_t.K4A_COLOR_RESOLUTION_720P.value : k4a_color_resolution_t.K4A_COLOR_RESOLUTION_720P,
                k4a_color_resolution_t.K4A_COLOR_RESOLUTION_1080P.value : k4a_color_resolution_t.K4A_COLOR_RESOLUTION_1080P,
                k4a_color_resolution_t.K4A_COLOR_RESOLUTION_1440P.value : k4a_color_resolution_t.K4A_COLOR_RESOLUTION_1440P,
                k4a_color_resolution_t.K4A_COLOR_RESOLUTION_1536P.value : k4a_color_resolution_t.K4A_COLOR_RESOLUTION_1536P,
                k4a_color_resolution_t.K4A_COLOR_RESOLUTION_2160P.value : k4a_color_resolution_t.K4A_COLOR_RESOLUTION_2160P,
                k4a_color_resolution_t.K4A_COLOR_RESOLUTION_3072P.value : k4a_color_resolution_t.K4A_COLOR_RESOLUTION_3072P,
        }

        return color_resolutions[int(self.headers['ColorResolution'])]

    
    '''
        get_intrinsic_param()
        This function handles get Intrinsic Parameter HTTP-GET Requests to the remote server, returning the data to the calling client. 
    '''
    def get_intrinsic_param(self):

        deviceIndex = int(self.headers['DeviceIndex'])
        deviceDepthMode = self.__parse_depth_mode__()
        deviceColorResolution = self.__parse_color_resolution__()
        testMode = int(self.headers['TestMode'])
        
        #POST Not SUpported by BaseHTTPRequestHandler
        #deviceConfig = pickle.loads(self.rfile.read())
        
        if (testMode):
            self.send_response(200)
            self.send_header('ResponseID', GET_DINTRIN_RESPONSE_ID)
            self.send_header('DeviceIndex', deviceIndex)
            self.send_header('TestMode', testMode)
            self.end_headers()
            self.wfile.write(bytes(r'TESTMODE: get_intrinsic_param'.encode('utf-8')))
            return

        # Get Device Intrinsic Parameters
        if (self.DEVICES[deviceIndex] is None):
            self.__send_error_response__('Device Has Not Been Started')
            return

        deviceIntrinsics = self.DEVICES[deviceIndex].get_calibration(deviceDepthMode, deviceColorResolution)
        self.send_response(200)
        self.send_header('ResponseID', GET_DINTRIN_RESPONSE_ID)
        self.send_header('DeviceIndex', deviceIndex)
        self.send_header('IntrinsicParam', deviceIntrinsics)
        self.send_header('TestMode', testMode)
        self.end_headers()

        pickled_intrin_param = pickle.dumps(deviceIntrinsics)
        self.wfile.write(pickled_intrin_param)
        
        return

    
    '''
        get_device_info()
        This function handles HTTP-GET Device Info Requests to the remote server, returning the data to the calling client. 
    '''
    def get_device_info(self):

        deviceIndex = int(self.headers['DeviceIndex'])
        testMode = int(self.headers['TestMode'])

        if (testMode):
            self.send_response(200)
            self.send_header('ResponseID', GET_DINFO_RESPONSE_ID)
            self.send_header('DeviceIndex', deviceIndex)
            self.send_header('TestMode', testMode)
            self.end_headers()
            self.wfile.write(bytes(r'TESTMODE: get_device_info'.encode('utf-8')))
            return

        if (self.DEVICES[deviceIndex] is None):
            self.__send_error_response__('Device Has Not Been Started')
            return

        deviceVersion = self.DEVICES[deviceIndex].get_version()
        deviceSN = self.DEVICES[deviceIndex].get_serialnum()

        self.send_response(200)
        self.send_header('ResponseID', GET_DINFO_RESPONSE_ID)
        self.send_header('DeviceIndex', deviceIndex)
        self.send_header('DeviceVersion', deviceVersion)
        self.send_header('DeviceSN', deviceSN)
        self.send_header('TestMode', testMode)
        self.end_headers()
        self.wfile.write(bytes(r'Device Info'.encode('utf-8')))
        return


    '''
        capture_frame()
        This function handles Capture Frame HTTP-GET Requests to the remote server, returning the data to the calling client. 
    '''
    def capture_frame(self):

        deviceIndex = int(self.headers['DeviceIndex'])
        testMode = int(self.headers['Testmode'])

        # Send back a simple data for testing.
        if (testMode):
            self.send_response(200)
            self.send_header('ResponseID', CAP_FRAME_RESPONSE_ID)
            self.send_header('DeviceIndex', deviceIndex)
            self.send_header('TestMode', testMode)
            self.end_headers()
            self.wfile.write(bytes(r'TESTMODE: capture_frames'.encode('utf-8')))
            return

        if (self.DEVICES[deviceIndex] is None):
            self.__send_error_response__('Device Has Not Been Started')
            return
        
        device = self.DEVICES[deviceIndex]
        capture = device.get_capture()
        
        depthMode = self.DEVICES_DMODE[deviceIndex]
        
        self.send_response(200)
        self.send_header('ResponseID', CAP_FRAME_RESPONSE_ID)
        self.send_header('DeviceIndex', deviceIndex)


        # Get color data.
        colorImage = capture.get_color_image()
        colorBuff = colorImage.get_buffer()
        
        pickled_color_buf = pickle.dumps(colorBuff)
        pickled_color_buf_len = len(pickled_color_buf)

        self.send_header('FirstBuffType', COLOR_BUFF_TYPE)
        self.send_header('FirstDataSize', pickled_color_buf_len)
        
        first_pickled_buff = pickled_color_buf

        colorImage.release()

        if depthMode is k4a_depth_mode_t.K4A_DEPTH_MODE_PASSIVE_IR.value:
            # Get pcm data.
            pcmImage = capture.get_ir_image()
            pcmBuff = pcmImage.get_buffer()

            pickled_pcm_buf = pickle.dumps(pcmBuff)
            pickled_pcm_buf_len = len(pickled_pcm_buf)

            # Write data to stdout.
            self.send_header('SecondBuffType', PCM_BUFF_TYPE)
            self.send_header('SecondDataSize', pickled_pcm_buf_len)

            second_pickled_buff = pickled_pcm_buf

            pcmImage.release()

        elif depthMode is not k4a_depth_mode_t.K4A_DEPTH_MODE_OFF:
            # Get depth data.
            depthImage = capture.get_depth_image()
            depthBuff = depthImage.get_buffer()

            pickled_depth_buf = pickle.dumps(depthBuff)
            pickled_depth_buf_len = len(pickled_depth_buf)

            # Write data to stdout.
            self.send_header('SecondBuffType', DEPTH_BUFF_TYPE)
            self.send_header('SecondDataSize', pickled_depth_buf_len)
            
            second_pickled_buff = pickled_depth_buf

            depthImage.release()

        self.send_header('Content-type', 'application/binary')
        self.send_header('TestMode', testMode)
        self.end_headers()
        self.wfile.write(first_pickled_buff)
        self.wfile.write(second_pickled_buff)

        capture.release()

        return

if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--address', type=str, default='localhost')
    parser.add_argument('--port', type=int, default=13579)
    args = parser.parse_args(sys.argv[1:])

    handler = AzureKinectRequestHandler
    server_address = (args.address, args.port)

    try:
        print('Starting Azure Kinect Server on host ' + server_address[0] + ':' + str(server_address[1]))
        print('Press ^C (Ctrl+C) to quit and close the server.')
        httpd = HTTPServer(server_address, handler)
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('^C (Ctrl+C) received, shutting down server')
        if (handler.DEVICES[DEVICE0] is not None):
            handler.DEVICES[DEVICE0].stop_cameras()
            handler.DEVICES[DEVICE0] = None
        if (handler.DEVICES[DEVICE1] is not None):
            handler.DEVICES[DEVICE1].stop_cameras()
            handler.DEVICES[DEVICE1] = None
        httpd.socket.close()

