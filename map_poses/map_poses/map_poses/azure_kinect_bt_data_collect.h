#pragma once
#pragma once

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <string>
#include <iostream> 
#include <windows.h>

#include <k4a/k4a.h>
#include <k4abt.h>

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
extern k4a_device_configuration_t device_config;
volitile extern k4a_capture_t device_capture;

// Body Tracking Resources
extern k4abt_tracker_configuration_t tracker_config;
volitile extern k4abt_frame_t body_frame;




int init_device(void);

int init_bt(void);

int get_device_bt_capture(unsigned long* frame_number, k4abt_skeleton_t* body_skel);

int clean_up(void);

int print_output(unsigned long seq_number, unsigned long frame_number, k4abt_skeleton_t body_skel);

int do_one();

int do_continuous(unsigned long seq_len);

//int parse_input(int argc, char* argv);

//int init_data_file();
