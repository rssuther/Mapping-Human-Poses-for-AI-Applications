/**
 * Mapping Human Poses
 * 
 * azure_kinect_bt_data_collect.h
 * @author Reid Sutherland
 * @date 09/20/19
 * 
 * */

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

// Data Output Resources
extern FILE* TXT_FILE_OUT;

/*
	*	init_device()
	*
	*	Initilizes Connected Device at DeviceIndex = 0
	*
	*	Returns 0
	*
*/
int init_device(void);

/*
	*	init_bt)
	*
	*	Initilizes Body Tracking Engine for Specific Device Parameters
	*
	*	Returns 0
	*
*/
int init_bt(void);

/*
	*	clean_up()
	*	
	*	Closes and Releases Resources
	*	
	*
*/
int clean_up(void);

/*
	*	get_device_bt_capture()
	*	
	*	Captures One Frame from the Connected Device
	*	Passes Frame into Body Tracking Engine 
	*		to Detect Body Skeletons
	*	Data is Placed in body_skel
	*
	*	@param  unsigned long* frame_number
	*				Pointer to Current Frame Number Counter
	*
	*	@param  k4abt_skeleton_t* body_skel
	*				Pointer to Body Skeleton Data
	*
	*	@onerror return -1
	*	
	*	Returns 0
	*
*/
int get_device_bt_capture(unsigned long* frame_number, k4abt_skeleton_t* body_skel);

/*
	*	print_body_skeleton()
	*	
	*	Prints Body Skeleton Data to Output Console
	*
	*	@param  unsigned long seq_number
	*				Current Sequence Number Counter
	*
	*	@param  unsigned long frame_number
	*				Current Frame Number Counter
	*
	*	@param  k4abt_skeleton_t body_skel
	*				Body Skeleton Data
	*
	*	@onerror return -1
	*	
	*	Returns 0
	*
*/
int print_body_skeleton(unsigned long seq_number, unsigned long frame_number, k4abt_skeleton_t body_skel);

/*
	*	parse_skeleton_to_txt()
	*	
	*	Outputs Body Skeleton Data to Costom Format Text File
	*
	*	@param  unsigned long seq_number
	*				Current Sequence Number Counter
	*
	*	@param  unsigned long frame_number
	*				Current Frame Number Counter
	*
	*	@param  k4abt_skeleton_t body_skel
	*				Body Skeleton Data
	*
	*	@param  FILE* output_file
	*				FILE Pointer for Output File
	*
	*	@onerror return -1
	*	
	*	Returns 0
	*
*/
int parse_skeleton_to_txt(unsigned long seq_number, unsigned long frame_number, k4abt_keleton_t body_skel, FILE* output_file);

/*
	*	parse_txt_to_skeleton()
	*	
	*	Outputs Body Skeleton Data to Costom Format Text File
	*
	*	@param  unsigned long* seq_number
	*				Pointer to Current Sequence Number Counter
	*
	*	@param  unsigned long* frame_number
	*				Pointer to Current Frame Number Counter
	*
	*	@param  k4abt_skeleton_t* body_skel
	*				Pointer to Body Skeleton Data Structure
	*
	*	@param  char* input_data
	*				One Line of the Body Skeleton Data File
	*
	*	@onerror return -1
	*	
	*	Returns 0
	*
*/
int parse_txt_to_skeleton(unsigned long* seq_number, unsigned long* frame_number, k4abt_keleton_t* body_skel, char* input_data);

