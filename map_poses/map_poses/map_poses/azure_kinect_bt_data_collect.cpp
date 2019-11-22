/**
 * Mapping Human Poses
 * 
 * azure_kinect_bt_data_collect.cpp
 * @author Reid Sutherland
 * @date 09/20/19
 * 
 * */

#include "azure_kinect_bt_data_collect.h"

using namespace std;


// Device Capture Resources
k4a_device_t device = NULL;
extern k4a_device_configuration_t device_config = K4A_DEVICE_CONFIG_INIT_DISABLE_ALL;
volitile extern k4a_capture_t device_capture = NULL;

// Body Tracking Resources
k4a_calibration_t sensor_calibration;
k4abt_tracker_t tracker = NULL;
extern k4abt_tracker_configuration_t tracker_config = K4ABT_TRACKER_CONFIG_DEFAULT;
volitile extern k4abt_frame_t body_frame = NULL;

// Configurations
int VERBOSE = 0;
int CONTINUOUS = 0;
int DURRATION = 10;
int DO_OUTPUT = 0;
extern FILE* TXT_FILE_OUT = NULL;

/*
	*	init_device()
	*
	*	Initilizes Connected Device at DeviceIndex = 0
	*
	*	Returns 0
	*
*/
int init_device(void) {

	printf("Opening Azure Kinect Device for Capture\n");

	VERIFY(k4a_device_open(0, &device), "Opening of K4A Device Failed...");

	printf("Starting Camera with Depth Sensor Enabled\n");

	device_config.depth_mode = K4A_DEPTH_MODE_NFOV_UNBINNED;
	device_config.color_resolution = K4A_COLOR_RESOLUTION_OFF;

	VERIFY(k4a_device_start_cameras(device, &device_config), "Start K4A Device Cameras Failed...");

	return 0;

}

/*
	*	init_bt)
	*
	*	Initilizes Body Tracking Engine for Specific Device Parameters
	*
	*	Returns 0
	*
*/
int init_bt(void) {

	VERIFY(k4a_device_get_calibration(device, device_config.depth_mode, device_config.color_resolution, &sensor_calibration), "Get Depth Camera Calibration Failed...");

	VERIFY(k4abt_tracker_create(&sensor_calibration, tracker_config, &tracker), "Body Tracker Initialization Failed...");

	return 0;

}

/*
	*	clean_up()
	*	
	*	Closes and Releases Resources
	*	
	*
*/
void clean_up(void) {

	k4abt_tracker_shutdown(tracker);
	k4abt_tracker_destroy(tracker);
	k4a_device_stop_cameras(device);
	k4a_device_close(device);

	if (TXT_FILE_OUT != NULL){
		TXT_FILE_OUT.close();
	}

}

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
int get_device_bt_capture(unsigned long* frame_number, k4abt_skeleton_t* body_skel) {

	// Capture Wait Result 
	k4a_wait_result_t capture_result = K4A_WAIT_RESULT_SUCCEEDED;
	k4a_wait_result_t q_capture_result = K4A_WAIT_RESULT_SUCCEEDED;
	k4a_wait_result_t pop_frame_result = K4A_WAIT_RESULT_SUCCEEDED;

	// Fet Sensor Capture from Device
	capture_result = k4a_device_get_capture(device, &device_capture, K4A_WAIT_INFINITE);

	if (q_capture_result == K4A_WAIT_RESULT_SUCCEEDED) {

		frame_number++;

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

			k4abt_frame_get_body_skeleton(body_frame, 0, body_skel);

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
int print_body_skeleton(unsigned long seq_number, unsigned long frame_number, k4abt_skeleton_t body_skel) {

	printf("Body Skeliton Joint:\n");

	for (int i = 0; i < 25; i++) {

		cout << "\tJoint Position XYZ [mm]: " << endl;
		cout << "\t\tX: " << body_skel.joints[i].position.xyz.x << endl;
		cout << "\t\tY: " << body_skel.joints[i].position.xyz.y << endl;
		cout << "\t\tZ: " << body_skel.joints[i].position.xyz.z << endl;

		cout << "\tJoint Orrientation WXYZ: " endl;
		cout << "\t\tW: " << body_skel.joints[i].orientation.wxyz.w << endl;
		cout << "\t\tX: " << body_skel.joints[i].orientation.wxyz.x << endl;
		cout << "\t\tY: " << body_skel.joints[i].orientation.wxyz.y endl;
		cout << "\t\tZ: " << body_skel.joints[i].orientation.wxyz.z endl;
		
		cout << "\tJoint Confidence: " << endl;

		switch(body_skel.joints[i].confidence_level){
			case K4ABT_JOINT_CONFIDENCE_NONE:
				cout << "\t\tK4ABT_JOINT_CONFIDENCE_NONE" << endl;
				break;
			case K4ABT_JOINT_CONFIDENCE_LOW:
				cout << "\t\tK4ABT_JOINT_CONFIDENCE_LOW" << endl;
				break;
			case K4ABT_JOINT_CONFIDENCE_MEDIUM:
				cout << "\t\tK4ABT_JOINT_CONFIDENCE_MEDIUM" << endl;
				break;
			case K4ABT_JOINT_CONFIDENCE_HIGH:
				cout << "\t\tK4ABT_JOINT_CONFIDENCE_HIGH" << endl;
				break;
			default:
				cout << "\t\tJoint Confidence Unknown:Error" << endl;
				break;
		}

		cout << "\n\n\n" << endl;


	}

	return 0;

}

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
int parse_skeleton_to_txt(unsigned long seq_number, unsigned long frame_number, k4abt_keleton_t body_skel, FILE* output_file){

	char output_data[2048] = {'\0'};
	k4a_float3_t joint_pos = NULL;
	k4a_quaternion_t joint_orr = NULL;
	int joint_conf = K4ABT_JOINT_CONFIDENCE_NONE;

	if (output_file == NULL){

		cout << "Invalid call of parse_skeleton_to_txt(): File Not Specified" << endl << endl;
		return -1;

	}

	sprintf(output_data, "%ul %ul : ", seq_number, frame_number);
	output_file.write(output_data);

	output_data = {'\0'};

	for (int i = 0; i < 25; i++) {

		joint_pos = body_skel.joints[i].position;
		joint_orr = body_skel.joints[i].orientation;

		switch(body_skel.joints[i].confidence_level){
			case K4ABT_JOINT_CONFIDENCE_NONE:
				joint_conf = int(K4ABT_JOINT_CONFIDENCE_NONE);
				break;
			case K4ABT_JOINT_CONFIDENCE_LOW:
				joint_conf = int(K4ABT_JOINT_CONFIDENCE_LOW);
				break;
			case K4ABT_JOINT_CONFIDENCE_MEDIUM:
				joint_conf = int(K4ABT_JOINT_CONFIDENCE_MEDIUM);
				break;
			case K4ABT_JOINT_CONFIDENCE_HIGH:
				joint_conf = int(K4ABT_JOINT_CONFIDENCE_HIGH);
				break;
			default:
				joint_conf = int(K4ABT_JOINT_CONFIDENCE_NONE);
				break;
		}

		sprintf(output_data, "%d %f %f %f %f %f %f %f %d : ", i, joint_pos.xyz.x, joint_pos.xyz.y, joint_pos.xyz.z, joint_orr.wxyz.w, joint_orr.wxyz.x, joint_orr.wxyz.y, joint_orr.wxyz.z, joint_conf);

		
		output_file.write(output_data);
		output_file.write("\n");

	}

	return 0

}

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
int parse_txt_to_skeleton(unsigned long* seq_number, unsigned long* frame_number, k4abt_keleton_t* body_skel, char* input_data){

	k4a_float3_t joint_pos = NULL;
	k4a_quaternion_t joint_orr = NULL;
	int joint_conf = K4ABT_JOINT_CONFIDENCE_NONE;
	char* parameters = NULL;

	float xyz_x = 0;
	float xyz_y = 0;
	float xyz_z = 0;
	float wxyz_w = 0;
	float wxyz_x = 0;
	float wxyz_y = 0;
	float wxyz_z = 0;
	int confidence = 0;

	if (strcmp(input_data[0], "\n")){

		cout << "End of Input Data File Reached" << endl << endl;
		return 1;

	}

	parameters = strtok(input_data, ":");
	
	while(parameters != NULL){

		sscanf(parameters, "%ul %ul", *seq_number, *frame_number);
		
		for (int i = 0; i < 25; i++) {
			parameters = strtok(NULL, ":");
			
			sscanf(parameters, "%*d %f %f %f %f %f %f %f %d", 
				&xyz_x, &xyz_y, &xyz_z,
				&wxyz_w, &wxyz_x, &wxyz_y, &wxyz_z,
				&confidence
				);

			body_skel->joints[i].position.xyz.x = xyz_x;
			body_skel->joints[i].position.xyz.y = xyz_y;
			body_skel->joints[i].position.xyz.z = xyz_z;

			body_skel->joints[i].orientation.wxyz.w = wxyz_w;
			body_skel->joints[i].orientation.wxyz.x = wxyz_x;
			body_skel->joints[i].orientation.wxyz.y = wxyz_y;
			body_skel->joints[i].orientation.wxyz.z = wxyz_z;

			body_skel->joints[i].confidence_level = (k4abt_joint_confidence_level_t)confidence;
			
	}

	return 0

}

/*
	*	do_one()
	*	
	*	Testing and Example for Capturing One 
	*		Collection of Body Skeleton Data
	*	
	*	Returns 0
	*
*/
int do_one() {

	k4abt_skeleton_t body_skel;
	unsigned long frame_number = 0;
	unsigned long seq_number = 0;

	if (-1 == get_device_bt_capture(&frame_number, &body_skel)) {
		cout << "An Error Occured Capturing a Body Skel" << endl << endl;
	}

	if (VERBOSE){
		print_body_skeleton(seq_number, frame_number, body_skel);
	}

	if (TXT_FILE_OUT != NULL){
			parse_skeleton_to_txt(seq_number, frame_number, body_skel, TXT_FILE_OUT);
		}

	return 0;
}

/*
	*	do_continuous()
	*	
	*	Testing and Example for Capturing Multiple 
	*		Collection of Body Skeleton Data
	*	
	*	@param  unsigned long seq_len
	*				Approxamate Durration of Continuous Capturing
	*
	*	Returns 0
	*
*/
int do_continuous(unsigned long seq_len) {

	k4abt_skeleton_t body_skel;
	unsigned long frame_number = 0;
	unsigned long seq_number = 0;

	unsigned long num_frames_seq = device_config.camera_fps * seq_len;

	do {
		if (-1 == get_device_bt_capture(&frame_number, &body_skel)) {
			cout << "An Error Occured Capturing a Body Skel" << endl << endl;
		}

		if (VERBOSE){
			print_body_skeleton(seq_number, frame_number, body_skel);
		}

		if (TXT_FILE_OUT != NULL){
			parse_skeleton_to_txt(seq_number, frame_number, body_skel, TXT_FILE_OUT);
		}

		Sleep(1000);

		if (frame_number == num_frames_seq) {

			frame_number = 0;
			seq_number++;

		}

	} while (seq_number < num_frames_seq);

	return 0;
}

/*
	*	parse_user_input()
	*	
	*	Parses User Input for Configuration Parameters
	*	
	*	@param  int argc
	*				User Input Argument Count
	*	@param  char* argv
	*				User Input Arguments
	*
	*	Returns 0
	*
*/
int parse_user_input(int argc, char* argv[]){

	int i = 0;

	if (argc > 7){
		cout << "Invalid Number of Inputs" << endl << endl;
		print_usage();
		exit(EXIT_FAILURE);
	}

	if (argc >= 2 || argc <= 7){

		for (i = 1; i < argc; i++){
			
			switch(argv[i]){
				
				// Verbose Mode
				case "-f":

					DO_OUTPUT = 1;
					TXT_FILE_OUT = fopen(argv[++i], "w+");
					break;

				// Verbose Mode
				case "-v":

					VERBOSE = 1;
					break;

				// Continuous Mode
				case "-c":

					CONTINUOUS = 1;
					break;

				// Durration Specifier
				case "-d":

					if (isdigit(argv[++i])){

						DURRATION = atoi(argv[i]);

					}
					else {

						cout << "Invalid Durration Provided: Using Default 10 Seconds"

					}
					break;

				// Invalid Input Handler
				default:

					cout << "Invalid Input Provided" << endl << endl;
					print_usage();
					exit(EXIT_FAILURE);
					break;

			}
		}

	}

	return 0;

}

/*
	*	print_usage()
	*	
	*	Prints Usage Message
	*	
	*
*/
void print_usage(void){

	cout << "USAGE: ./azure_kinect_bt_data_collect [-f <text file path> : Specifies the output file for skeleton data] [-c : Capture Continuously] [-v : Verbose Output] [-d <durration in seconds> : DURRATION, for continuous mode]" << endl << endl;

}

/*
	*	main()
	*	
	*	Demo Operation of Data Collection Functionality
	*
	*
*/
int main(int argc, char* argv[]) {

	parse_user_input();

	// Initialise Connected Device
	init_device();

	// Initialise Body Tracking Engine
	init_bt();

	// Run Operation Mode
	if (CONTINUOUS) {

		// Continuous Capture Mode
		do_continuous(DURRATION);
	
	}
	else {
	
		do_one();
	
	}

	printf("Finished Body Tracking Processing\n");

	// Close and Release Resources
	clean_up();

}