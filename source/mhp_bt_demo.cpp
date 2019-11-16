#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <iostream> 
#include <windows.h>

#include <k4a/k4a.h>
#include <k4a/k4atypes.h>
#include <k4abt.h>
#include <k4abttypes.h>


using namespace std;

// Error Checking Macros
#define VERIFY(result, error)                                                                            \
    if(result != K4A_RESULT_SUCCEEDED)                                                                   \
    {                                                                                                    \
        printf("%s \n - (File: %s, Function: %s, Line: %d)\n", error, __FILE__, __FUNCTION__, __LINE__); \
        exit(1);                                                                                         \
    } 

#define TIMEOUT_IN_MS 20;

// Device Capture Resources
k4a_device_t device = NULL;
k4a_device_configuration_t device_config = K4A_DEVICE_CONFIG_INIT_DISABLE_ALL;
k4a_capture_t device_capture = NULL;

// Body Tracking Resources
k4a_calibration_t sensor_calibration;
k4abt_tracker_t tracker = NULL;
k4abt_tracker_configuration_t tracker_config = K4ABT_TRACKER_CONFIG_DEFAULT;
k4abt_frame_t body_frame = NULL;

int init_device(void){

    printf("Opening Azure Kinect Device for Capture\n");

    VERIFY(k4a_device_open(0, &device), "Opening of K4A Device Failed...");

    printf("Starting Camera with Depth Sensor Enabled\n");

    device_config.depth_mode = K4A_DEPTH_MODE_NFOV_UNBINNED;
    device_config.color_resolution = K4A_COLOR_RESOLUTION_OFF;

    VERIFY(k4a_device_start_cameras(device, &device_config), "Start K4A Device Cameras Failed...");

    return 0;

}

int init_bt(void){

    VERIFY(k4a_device_get_calibration(device, device_config.depth_mode, device_config.color_resolution, &sensor_calibration), "Get Depth Camera Calibration Failed...");

    VERIFY(k4abt_tracker_create(&sensor_calibration, tracker_config, &tracker), "Body Tracker Initialization Failed...");

    return 0;

}

int get_device_bt_capture(int* frame_count){

    // Capture Wait Result 
	k4a_wait_result_t capture_result = K4A_WAIT_RESULT_SUCCEEDED;
    k4a_wait_result_t q_capture_result = K4A_WAIT_RESULT_SUCCEEDED;
    k4a_wait_result_t pop_frame_result = K4A_WAIT_RESULT_SUCCEEDED;

    k4abt_skeleton_t body_skel;


    // Fet Sensor Capture from Device
    capture_result = k4a_device_get_capture(device, &device_capture, K4A_WAIT_INFINITE);

    if (q_capture_result == K4A_WAIT_RESULT_SUCCEEDED){

        frame_count++;

        // Enque Sensor Capture Result tor Tracking
        q_capture_result = k4abt_tracker_enqueue_capture(tracker, device_capture, K4A_WAIT_INFINITE);

        // Relsease Sensor Capture after Use
        k4a_capture_release(device_capture);

        // Check Q Capture Result
        if (q_capture_result == K4A_WAIT_RESULT_TIMEOUT)
        {
            // It should never hit timeout when K4A_WAIT_INFINITE is set.
            printf("Error! Add capture to tracker process queue timeout!\n");
            return -1;
        }
        else if (q_capture_result == K4A_WAIT_RESULT_FAILED)
        {
            printf("Error! Add capture to tracker process queue failed!\n");
            return -1;
        }

        // Pop Body Tracking Result from Processed Queue
        pop_frame_result = k4abt_tracker_pop_result(tracker, &body_frame, K4A_WAIT_INFINITE);

        // Check Pop Frame Result
        if (pop_frame_result == K4A_WAIT_RESULT_SUCCEEDED)
        {
            // Successfully popped the body tracking result.

            size_t num_bodies = k4abt_frame_get_num_bodies(body_frame);
            printf("%zu bodies are detected!\n", num_bodies);

            k4abt_frame_get_body_skeleton(body_frame, 0, &body_skel);

            int i = 0;
			for (i = 0; i < 25; i++) {

                printf("Body Skeliton Joint %d:\n", i);

                cout << "Joint Position [mm]: " << body_skel.joints[i].position.v << "\n";
                cout << "Joint Orrientation: " << body_skel.joints[i].orientation.v << "\n";
                cout << "Joint Confidence: ";

				cout << "API Broken\n";

				/*
                
                switch( body_skel.joints[i].confidence_level){

                    case K4ABT_JOINT_CONFIDENCE_NONE :
                        cout << "K4ABT_JOINT_CONFIDENCE_NONE \n";
                        break;

                    case K4ABT_JOINT_CONFIDENCE_LOW :
                        cout << "K4ABT_JOINT_CONFIDENCE_LOW \n";
                        break;

                    case K4ABT_JOINT_CONFIDENCE_MEDIUM :
                        cout << "K4ABT_JOINT_CONFIDENCE_MEDIUM \n";
                        break;

                    case K4ABT_JOINT_CONFIDENCE_HIGH :
                        cout << "K4ABT_JOINT_CONFIDENCE_HIGH \n";
                        break;

                    case K4ABT_JOINT_CONFIDENCE_LEVELS_COUNT :
                        cout << "K4ABT_JOINT_CONFIDENCE_LEVELS_COUNT \n";
                        break;

                    default:

                        cout << "CONFIDENCE LEVEL VALUE ERROR\n";
                        break;
                }

				*/

            }

            k4abt_frame_release(body_frame); // Remember to release the body frame once you finish using it
        }
        else if (pop_frame_result == K4A_WAIT_RESULT_TIMEOUT)
        {
            //  It should never hit timeout when K4A_WAIT_INFINITE is set.
            printf("Error! Pop body frame result timeout!\n");
            return -1;
        }
        else
        {
            printf("Pop body frame result failed!\n");
            return -1;
        }

    }
    else if (capture_result == K4A_WAIT_RESULT_TIMEOUT)
    {
        // It should never hit time out when K4A_WAIT_INFINITE is set.
        printf("Error! Get depth frame time out!\n");
        return -1;
    }
    else
    {
        printf("Get depth capture returned error: %d\n", capture_result);
        return -1;
    }

	return 0;

}

int clean_up(void){

    k4abt_tracker_shutdown(tracker);
    k4abt_tracker_destroy(tracker);
    k4a_device_stop_cameras(device);
    k4a_device_close(device);

	return 0;

}

int main(void){

    int frame_count = 0;

    init_device();
    init_bt();

    do {
        get_device_bt_capture(&frame_count);

        Sleep(1000);

    } while (frame_count < 100);

    printf("Finished Body Tracking Processing\n");

    clean_up();

}