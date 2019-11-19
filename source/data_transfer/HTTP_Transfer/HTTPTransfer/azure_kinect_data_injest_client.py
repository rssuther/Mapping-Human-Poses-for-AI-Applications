"""A simple client that sends an http GET command to start capturing N frames from
a connected Azure Kinect device on a remote machine.
"""

# importing the requests library
import sys
import cv2
import json
import numpy as np
import pickle
import urllib.request 
import http.client
import time
from k4apy.k4a_device import K4ADevice
from k4apy.k4a_types import *

from RemoteCapture.constants import *

class AzureKinectClient:

    def __init__(self):
        pass
    
    def __str__(self):
        return  str(self.__class__) + '\n'+ '\n'.join(('{} = {}'.format(item, self.__dict__[item]) for item in self.__dict__))

    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        return

    
    '''
        send_device_start_request()
        This function send an HTTP-GET Request to the specified remote server requesting that
            the specified device is started with the provided configuration
        @param serveraddress: A string representing the remote sever address
        @param serverport: An int specifying the remote server port
        @param deviceIndex: The server specific device index to start
        @param deviceConfig: k4a_configuration_t structure
        @param testMode: Indication to server to respond with test data or not
        @return err: (ERROR, server_repsonse)
        @return success: (SUCCESS, server_response.info, server_response.data)
    '''
    def send_device_start_request(self, serveraddress:str, port:int, deviceIndex:int=0, deviceConfig:k4a_device_configuration_t=None, testMode:int=0):
        # sending get request and saving the response as response object 
        req = urllib.request.Request('http://' + serveraddress + ':' + str(port))
        req.add_header('RequestID', START_REQUEST_ID)
        req.add_header('DeviceIndex', deviceIndex)
        req.add_header('DeviceConfig', deviceConfig)
        req.add_header('Testmode', testMode)
        response = urllib.request.urlopen(req)

        #POST Not SUpported by BaseHTTPRequestHandler (Server)
        #pickled_device_config = pickle.dumps(deviceConfig)
        #response = urllib.request.urlopen(req, pickled_device_config)

        print(response.info().get('ResponseID'))
        if (int(response.info().get('ResponseID')) is not START_RESPONSE_ID):
            return (ERROR, response)

        return (SUCCESS, response.info(), response.read())
    
    
    '''
        send_device_stop_request()
        This function send an HTTP-GET Request to the specified remote server requesting that
            the specified device is stopped
        @param serveraddress: A string representing the remote sever address
        @param serverport: An int specifying the remote server port
        @param deviceIndex: The server specific device index to start
        @param testMode: Indication to server to respond with test data or not
        @return err: (ERROR, server_repsonse)
        @return success: (SUCCESS, server_response.info, server_response.data)
    '''
    def send_device_stop_request(self, serveraddress:str, port:int, deviceIndex:int=0, testMode:int=0):
        # sending get request and saving the response as response object 
        req = urllib.request.Request('http://' + serveraddress + ':' + str(port))
        req.add_header('RequestID', STOP_REQUEST_ID)
        req.add_header('DeviceIndex', deviceIndex)
        req.add_header('Testmode', testMode)
        response = urllib.request.urlopen(req)

        if (int(response.info().get('ResponseID')) is not STOP_RESPONSE_ID):
            return (ERROR, response)

        return (SUCCESS, response.info(), response.read())
    
    
    '''
        set_device_config_request()
        This function send an HTTP-GET Request to the specified remote server requesting that
            the specified device's configuration is set to the provided configuration
        @param serveraddress: A string representing the remote sever address
        @param serverport: An int specifying the remote server port
        @param deviceIndex: The server specific device index to start
        @param deviceConfig: k4a_configuration_t structure
        @param WBValue: Value to set WB Parameter to
        @param exposureValue: Value to set Exposure Parameter to
        @param ISOSpeedValue: Value to set ISO Speed Parameter to
        @param testMode: Indication to server to respond with test data or not
        @return err: (ERROR, server_repsonse)
        @return success: (SUCCESS, server_response.info, server_response.data)
    '''
    def set_device_config_request(self, serveraddress:str, port:int, deviceIndex:int=0, deviceConfig:k4a_device_configuration_t=None, WBValue:int=0, exposureValue:int=0, ISOSpeedValue:int=0, testMode:int=0):
        # sending get request and saving the response as response object 
        req = urllib.request.Request('http://' + serveraddress + ':' + str(port))
        req.add_header('RequestID', SET_DCONFIG_REQUEST_ID)
        req.add_header('DeviceIndex', deviceIndex)
        req.add_header('DeviceConfig', deviceConfig)
        req.add_header('WBValue', WBValue)
        req.add_header('ExposureValue', exposureValue)
        req.add_header('ISOSpeedValue', ISOSpeedValue)
        req.add_header('Testmode', testMode)
        response = urllib.request.urlopen(req)

        #POST Not SUpported by BaseHTTPRequestHandler (Server)
        #pickled_device_config = pickle.dumps(deviceConfig)
        #response = urllib.request.urlopen(req, pickled_device_config)

        if (int(response.info().get('ResponseID')) is not SET_DCONFIG_RESPONSE_ID):
            return (ERROR, response)

        return (SUCCESS, response.info(), response.read())
    

    '''
        get_device_config_request()
        This function send an HTTP-GET Request to the specified remote server requesting that
            the specified device's configuration is returned
        @param serveraddress: A string representing the remote sever address
        @param serverport: An int specifying the remote server port
        @param deviceIndex: The server specific device index to start
        @param testMode: Indication to server to respond with test data or not
        @return err: (ERROR, server_repsonse)
        @return success: (SUCCESS, server_response.info, server_response.data)
    '''
    def get_device_config_request(self, serveraddress:str, port:int, deviceIndex:int=0, testMode:int=0):
        # sending get request and saving the response as response object 
        req = urllib.request.Request('http://' + serveraddress + ':' + str(port))
        req.add_header('RequestID', GET_DCONFIG_REQUEST_ID)
        req.add_header('DeviceIndex', deviceIndex)
        req.add_header('Testmode', testMode)
        response = urllib.request.urlopen(req)

        if (int(response.info().get('ResponseID')) is not GET_DCONFIG_RESPONSE_ID):
            return (ERROR, response)

        return (SUCCESS, response.info(), response.read())
    
    '''
        set_device_config_request()
        This function send an HTTP-GET Request to the specified remote server requesting that
            the specified device's configuration is set to the provided configuration
        @param serveraddress: A string representing the remote sever address
        @param serverport: An int specifying the remote server port
        @param deviceIndex: The server specific device index to start
        @param depthMode: k4a_configuration_t.depth_mode value
        @param colorResolution: k4a_configuration_t.color_resolution value
        @param testMode: Indication to server to respond with test data or not
        @return err: (ERROR, server_repsonse)
        @return success: (SUCCESS, server_response.info, server_response.data)  
    '''
    def get_intrincic_param_request(self, serveraddress:str, port:int, deviceIndex:int=0, depthMode:int=0, colorResolution:int=0, testMode:int=0):
        # sending get request and saving the response as response object 
        req = urllib.request.Request('http://' + serveraddress + ':' + str(port))
        req.add_header('RequestID', GET_DINTRIN_REQUEST_ID)
        req.add_header('DeviceIndex', deviceIndex)
        req.add_header('DepthMode', depthMode)
        req.add_header('ColorResolution', colorResolution)
        req.add_header('Testmode', testMode)
        response = urllib.request.urlopen(req)

        #POST Not SUpported by BaseHTTPRequestHandler (Server)
        #pickled_device_config = pickle.dumps(deviceConfig)
        #response = urllib.request.urlopen(req, pickled_device_config)

        if (int(response.info().get('ResponseID')) is not GET_DINTRIN_RESPONSE_ID):
            return (ERROR, response)

        return (SUCCESS, response.info(), response.read())
    

    '''
        get_device_info_request()
        This function send an HTTP-GET Request to the specified remote server requesting that
            the specified device's information (Serial Number, HW Version, etc.) is returned
        @param serveraddress: A string representing the remote sever address
        @param serverport: An int specifying the remote server port
        @param deviceIndex: The server specific device index to start
        @param testMode: Indication to server to respond with test data or not
        @return err: (ERROR, server_repsonse)
        @return success: (SUCCESS, server_response.info, server_response.data)
    '''
    def get_device_info_request(self, serveraddress:str, port:int, deviceIndex:int=0, testMode:int=0):
        # sending get request and saving the response as response object 

        req = urllib.request.Request('http://' + serveraddress + ':' + str(port))
        req.add_header('RequestID', GET_DINFO_REQUEST_ID)
        req.add_header('DeviceIndex', deviceIndex)
        req.add_header('Testmode', testMode)
        response = urllib.request.urlopen(req)

        if (int(response.info().get('ResponseID')) is not GET_DINFO_RESPONSE_ID):
            return (ERROR, response)

        return (SUCCESS, response.info(), response.read())
    
    '''
        capture_frame_request()
        This function send an HTTP-GET Request to the specified remote server requesting that
            a frame (color sensor, depth sensor (or PCM)) from the specified device is returned
        @param serveraddress: A string representing the remote sever address
        @param serverport: An int specifying the remote server port
        @param deviceIndex: The server specific device index to start
        @param testMode: Indication to server to respond with test data or not
        @return err: (ERROR, server_repsonse)
        @return success: (SUCCESS, server_response.info, server_response.data)
    '''
    def capture_frame_request(self, serveraddress:str, port:int, deviceIndex:int=0, testMode:int=0):
        # sending get request and saving the response as response object 
        req = urllib.request.Request('http://' + serveraddress + ':' + str(port))
        req.add_header('RequestID', CAP_FRAME_REQUEST_ID)
        req.add_header('DeviceIndex', deviceIndex)
        req.add_header('Testmode', testMode)
        response = urllib.request.urlopen(req)
        
        if (int(response.info().get('ResponseID')) is not CAP_FRAME_RESPONSE_ID):
            return (ERROR, response)
        
        info = response.info()

        first_pickled_data_type = int(info.get('FirstBuffType'))
        second_pickled_data_type = int(info.get('SecondBuffType'))

        first_pickled_data_len = int(info.get('FirstDataSize'))
        second_pickled_data_len = int(info.get('SecondDataSize'))

        print(str(first_pickled_data_type)+'  '+str(first_pickled_data_len)+' \n')
        print(str(second_pickled_data_type)+'  '+str(second_pickled_data_len)+' \n')

        data = response.read()

        first_pickle_data = data[:first_pickled_data_len]
        second_pickle_data = data[first_pickled_data_len:first_pickled_data_len+second_pickled_data_len]

        first_data = pickle.loads(first_pickle_data)
        second_data = pickle.loads(second_pickle_data)
  
        return (SUCCESS, info, (first_data, second_data))


    '''
        capture_frames_request()
        This function send multiple an HTTP-GET Requests ( calls capture_frame_request() ) to the 
            specified remote server requesting that N frames (color sensor, depth sensor (or PCM)) 
            from the specified device are returned
        @param serveraddress: A string representing the remote sever address
        @param serverport: An int specifying the remote server port
        @param deviceIndex: The server specific device index to start
        @param numFrames: The number of frames to request
        @param deviceIndex: The delay between frame requests
        @param testMode: Indication to server to respond with test data or not
        @return err: (ERROR, server_repsonse)
        @return success: (SUCCESS, server_response.info, server_response.data)
    '''
    def capture_frames_request(self, serveraddress:str, port:int, deviceIndex:int=0, numFrames:int=3, frameDelay:int=0, testMode:int=0):

        frame_packets = []
        for x in range(1, numFrames):
            print("Prepair to capture frame...")
            time.sleep(frameDelay)
            print("Capturing...")
            response = self.capture_frame_request(serveraddress, port, deviceIndex, testMode)

            if (response[SUCCESS] is ERROR):
                return (ERROR, response[1])

            frame_packets.append(response)
            print("Captured...")
        
        return (SUCCESS, frame_packets)

'''
    exit_procedure()
    This function performs a clean exit when called, used for error handeling
    @param stop_device: Controls wether a device stop request needs to be made, error dependant
'''
def exit_procedure(stop_device=0):

    if (stop_device):
        response = client.send_device_stop_request(serveraddress = args.serveraddress,
                port = args.port,
                deviceIndex = args.device_index,
                testMode = args.test_mode)

        if (response[SUCCESS] is ERROR):
            print('An Error Occured Stopping the Specified Device: '+response[ERROR].read()+'\n')
    
    print("Shutting Down Client\n\n")
    exit(1)

if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--serveraddress', type=str, default='localhost')
    parser.add_argument('--port', type=int, default=13579)
    parser.add_argument('--device_index', type=int, default=0)
    parser.add_argument('--start_device', type=bool, default=False)
    parser.add_argument('--stop_device', type=bool, default=False)
    parser.add_argument('--get_stored_param', type=bool, default=False)
    parser.add_argument('--capture_frames', type=bool, default=False)
    parser.add_argument('--num_frames', type=int, default=5)
    parser.add_argument('--frame_delay', type=int, default=3)
    parser.add_argument('--test_mode', type=int, default=0)
    args = parser.parse_args(sys.argv[1:])

    config = k4a_device_configuration_t(
        k4a_image_format_t.K4A_IMAGE_FORMAT_COLOR_BGRA32.value,
        k4a_color_resolution_t.K4A_COLOR_RESOLUTION_1080P.value,
        k4a_depth_mode_t.K4A_DEPTH_MODE_PASSIVE_IR.value,
        k4a_fps_t.K4A_FRAMES_PER_SECOND_30.value,
        True,
        0,
        0,
        0,
        False)

    try:
        # Send GET request.
        client = AzureKinectClient()
        response = client.send_device_start_request(serveraddress = args.serveraddress,
                            port = args.port,
                            deviceIndex = args.device_index,
                            deviceConfig = config,
                            testMode = args.test_mode)
        
        if (response[SUCCESS] is ERROR):
            print('An Error Occured Starting the Specified Device: '+str(response[ERROR].read())+'\n')
            exit_procedure(NO_STOP_DEVICE)

        print(bytes(response[DATA]))

        response = client.get_device_info_request(serveraddress = args.serveraddress,
                            port = args.port,
                            deviceIndex = args.device_index,
                            testMode = args.test_mode)
        if (response[SUCCESS] is ERROR):
            print('An Error Occured Requesting Device Info: '+str(response[ERROR].read())+'\n')
            exit_procedure(STOP_DEVICE)
        
        print(bytes(response[DATA]))

        response = client.get_intrincic_param_request(serveraddress = args.serveraddress,
                            port = args.port,
                            deviceIndex = args.device_index,
                            depthMode = config.get('depth_mode'),
                            colorResolution = config.get('color_resolution'),
                            testMode = args.test_mode)
        
        if (response[SUCCESS] is ERROR):
            print('An Error Occured Requesting Device Intrinsic Parameters: '+str(response[ERROR].read())+'\n')
            exit_procedure(STOP_DEVICE)
        
        param = pickle.loads(response[DATA])

        print(param)
        
        response = client.capture_frames_request(serveraddress = args.serveraddress,
                            port = args.port,
                            deviceIndex = args.device_index,
                            numFrames = args.num_frames,
                            frameDelay = args.frame_delay,
                            testMode = args.test_mode)
        
        if (response[SUCCESS] is ERROR):
            print('An Error Occured Requesting Device Frames: '+str(response[ERROR].read())+'\n')
            exit_procedure(STOP_DEVICE)

        for frame in response[FRAMES]:

            print('Color Image View')
            print(frame[DATA][COLOR_DATA][0])
            image = frame[DATA][COLOR_DATA]
            #image = frame[DATA][PCM_DATA]
            # Display Captured Image
            cv2.imshow('PCM Image', image)
            
            cv2.waitKey(5000)
                                    
            cv2.destroyAllWindows()

            print('PCM Image View')
            image_info = np.iinfo(frame[DATA][PCM_DATA].dtype)
            image_buf = np.sqrt((frame[DATA][PCM_DATA].astype(np.float16) / 16384.0))  #image_info.max
            image_buf = 255 * image_buf

            image = image_buf.astype(np.uint8)
        
            # Display Captured Image
            cv2.imshow('PCM Image', image)
            
            cv2.waitKey(5000)
                                    
            cv2.destroyAllWindows()

        

        response = client.send_device_stop_request(serveraddress = args.serveraddress,
                            port = args.port,
                            deviceIndex = args.device_index,
                            testMode = args.test_mode)

        if (response[SUCCESS] is ERROR):
            print('An Error Occured Stopping the Specified Device: '+response[ERROR].read()+'\n')
            exit_procedure(NO_STOP_DEVICE)
        
        print(bytes(response[DATA]))
    
    except KeyboardInterrupt:
        print('^C (Ctrl+C) received, shutting down client')
        exit_procedure(STOP_DEVICE)
    