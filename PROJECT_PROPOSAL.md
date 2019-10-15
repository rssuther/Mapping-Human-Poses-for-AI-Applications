<u> _CSC 480-F19 Artificial Intelligence_ </u>
<u> _Cal Poly SLO_ </u>
<u> _Prof. Franz J. Kurfess_ </u>

# Mapping-Human-poses-for-AI-applications
### Dream Team - Mapping Human Poses to a Formal Notation
#### Arun Ulagappan, Reid Sutherland, Luke Matusiak, Colin VanDervoort, Eleanor Lewis, Rattil Chowdhury

### Overview
The purpose of this project is to produce a body-motion tracking and recognition system that enables movements of the human body to be identified. The system will describe extensively and completely the motion of the human body in a notation that will be passed into a machine learning model to recognize various motions and poses. These poses will then be labeled and identified by the system to relay useful information about the motion. For example, with ground traffic control signals at the airport, the system could recognize the particular directives of the ground crew, and relay this information to the pilot or planes computer system.

### Method and Tools Selection
OpenPose was identified in the project description as a useful tool for determining the positioning of bodies in a video. It has the advantage of not requiring any specific hardware and it can be used on any major operating system with any video source. There are C++ and Python APIs for OpenPose. The form of the data returned by API queries needs to be investigated.

An alternative would be to use the Azure Kinect Developer Kit. This is a product developed and supported by Microsoft which has several technical advantages over OpenPose. It utilizes a special sensor which collects both color and depth information. Investigation so far seems to indicate that the documentation and API for the system is superior. The Azure Kinect Body Tracking SDK has a function that attempts to return a body skeleton. The skeleton is structured as an array of joints that are sequenced in a specific order. This data is probably in the most usable form already, so we could use it directly for training. Each joint includes position and orientation data. Reid has the sensor required to use this system, so it is a viable option. Azure Kinect features three SDK’s: Low Level Hardware SDK, Body Tracking SDK, and Speech Cognitive Services SDK. While they may not all be used, it is good to know we have lots of resources.

Here is a link to the Azure Kinect documentation.

### AI Method Categories
In this project we will be aiming to identify sequences of human motion. Right now our approach is to use supervised learning to train a model on labelled sequences of human poses. Recurrent neural networks and one-dimensional convolutional techniques are known to work well with sequential data, so the performance of the two techniques will be compared and the superior technique will be selected.

### Summary
Our goal is to visually identify and track human poses and movements. These identifications will be used to relay useful information about human signals to someone who is out of viewing range. We are looking to use Microsoft’s Azure Kinect to achieve our goal because it has great documentation, as well as compatibility with our hardware. 

### Schedule:

#### <u>Week 4</u>
Decide on AI tool (Kinect vs Open Pose)
Setup dev environment
Setup interface to connect the Azure camera with Kinect
Get material for airline gestures/poses (media like videos, pictures)
Create a GitHub repository for our neural network and supporting software

#### <u>Week 5</u>
Research related work to gain background knowledge
Determine the form of the output of our program (e.g. terminal text output)

#### <u>Week 6</u>
Design prototype neural network architecture based on characteristics of the problem
Design interface between OpenPose or Azure Kinect and our neural network
Finish training/test data preparation

#### <u>Week 7</u>
Neural network development/testing
Development/testing of non-NN code (interfaces, output, etc.)

#### <u>Week 8</u>
Neural network development/testing
Development/testing of non-NN code (interfaces, output, etc.)

#### <u>Week 9</u>
Neural network development/testing

#### <u>Week 10</u>
Neural network development/testing

#### <u>Week 11</u>
Neural network development/testing


/* I dont know if we need any of the stuff after this comment just yet*/
 
### AI Tool
[Describe the tool you’ve selected here. Include the source, and a reference or link to more detailed information.]

OpenPose:
OpenPose is a OpenCV based real-time body tracking library that estimates the pose of a body, hand, or foot for multiple-subjects. The library estimates the subjects pose in real time and records this information in a format for further use. 

Link: https://github.com/CMU-Perceptual-Computing-Lab/openpose

CNN Machine Learning Model

### Problem Specification
[This is related to the scheme for problem solving and search discussed earlier in class. For a simple example, see the sample data in the code repository for this assignment.]
### Domain
[Describe the application area of your problem.]
### Domain Knowledge
[Discuss how relevant background knowledge about the application domain is used in the method and tool. In machine learning, for example, background knowledge typically is not explicitly used, but implicitly encoded in the data set used for learning. For informed search method, this knowledge is used to formulate heuristics. In knowledge-based systems, the knowledge is made explicit through rules, frames, ontologies or other methods.]
### Methods and Tools Discussion
[Describe the concepts or methods within the identified AI area you use in your project. Examples, again from the area of Learning, are:
supervised, unsupervised or reinforcement learning
learning methods (e.g., decision tree learning, categorization and classification, neural networks)
The overall project may combine several methods. You can focus on the one(s) that you consider most important here, and briefly mention others that also play a role.  
### Modifications
[Indicate if you made any modifications to the “standard” variation of the AI methods used. This may already have been addressed to some degree in the previous section. If so, point that out. Also state it if you used a “vanilla” method, without modifications.]
### Time and Space Complexity Issues
[For many AI methods, time and space complexity analyses have already been performed and I don’t expect you to do this again. It would be helpful to provide this information, especially for the less popular ones. The emphasis here is on practical aspects, so you could discuss if you encountered problems with error rates, getting stuck in local optima, time or space constraints, and what you did to address them.]


