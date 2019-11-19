import time
import sys
import win32pipe, win32file, pywintypes
import PyAzureKinect
import pickle

# Pipe Server - Data Transfer System
class K4APYBTPipeServer():
    raise NotImplementedError
    def pipe_server():
        print("pipe server")
        count = 0
        pipe = win32pipe.CreateNamedPipe(
            r'\\.\pipe\Foo',
            win32pipe.PIPE_ACCESS_DUPLEX,
            win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
            1, 65536, 65536,
            0,
            None)
        try:
            print("waiting for client")
            win32pipe.ConnectNamedPipe(pipe, None)
            print("got client")

            while count < 10:
                print(f"writing message {count}")
                # convert to bytes
                some_data = str.encode(f"{count}")
                win32file.WriteFile(pipe, some_data)
                time.sleep(1)
                count += 1

            print("finished now")
        finally:
            win32file.CloseHandle(pipe)

# Client Side - Data Transfer System
class K4APYBTPipeClient():

    pipe_handle = None
    pipe_response_state = None

    def setup_pipe_client(self):

        try:
            self.pipe_handle = win32file.CreateFile(
                r"\\\\.\\pipe\\MHP_DATA_CAPTURE_SERVICE",
                win32file.GENERIC_READ | win32file.GENERIC_WRITE,
                0,
                None,
                win32file.OPEN_EXISTING,
                0,
                None
            )
            pipe_response_state = win32pipe.SetNamedPipeHandleState(pipe_handle, win32pipe.PIPE_READMODE_MESSAGE, None, None)
            if pipe_response_state == 0:
                print(f"SetNamedPipeHandleState return code: {pipe_response_state}")
        
        except pywintypes.error as e:
                if e.args[0] == 2:
                    print("no pipe, trying again in a sec")
                    time.sleep(1)
                elif e.args[0] == 109:
                    print("broken pipe, bye bye")
                    quit = True

    def read_data(self):

        data_size_p = None
        data_size = 0
        data_p = None
        data = None

        try:

            #Read Data Size
            data_size_p = win32file.ReadFile(pipe_handle, 64*1024) # Determine Correct Size

            #Read Frame Count
            #data_size_p = win32file.ReadFile(handle, 64*1024) # Determine Correct Size

            data_size = pickle.loads(data_size_p)

            print(f"message: {data_size}")

            #Read Data

            data_p = win32file.ReadFile(pipe_handle, data_size) # Determine Correct Size

            data = pickle.loads(data_p)

            print(f"message: {data}")
        
        except pywintypes.error as e:
            
            if e.args[0] == 109:
                print("broken pipe, bye bye")
                return None
        
        return data


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("need s or c as argument")
    elif sys.argv[1] == "s":
        pipe_server()
    elif sys.argv[1] == "c":
        pipe_client()
    else:
        print(f"no can do: {sys.argv[1]}")
