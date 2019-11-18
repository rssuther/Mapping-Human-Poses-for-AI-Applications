#!/bin/bash


echo Installing Dependancies

echo Moving Files Into Place

copy "%ProgramFiles%\Azure Kinect DK\include\depthengine_1_0.dll" ".\source\PyAzureKinect\k4abtpy\lib\"

copy "%ProgramFiles%\Azure Kinect DK\include\k4a.dll" ".\source\PyAzureKinect\k4abtpy\lib\"

copy "%ProgramFiles%\Azure Kinect DK\include\k4abt.dll" ".\source\PyAzureKinect\k4abtpy\lib\"



