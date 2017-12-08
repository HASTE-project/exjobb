# Microscope simulator for the HASTE project 

Master thesis work to simulate a microscope and stream the images coming from the microscope.

The simulator can either be run on its own or connected with Kafka. To run it with Kafka a Kafka server is needed. 

## Getting started

### Prerequisites

cv2, numpy, PIL, flask, kafka-python, skimage 


### Installing

For installation in development mode:

A step by step series of examples that tell you have to get a development env running

Say what the step will be

```
git clone https://github.com/LovisaLugnegard/exjobb.git

```

### Update

```
cd exjobb
git pull https://github.com/LovisaLugnegard/exjobb.git

```

## Example
### To use the web UI (run on 127.0.0.1:5000\fileWalk)
```
python3 simulator.py
```
### To use without UI
```
import simulator_no_flask
simulator_no_flask.get_files(file_path, period, binning, color_channel, connect_kafka) # period = period time in seconds,  color_channel given as
	#list with up to 5 channels ie. ["1", "2", "5"], connect_kafka set to "yes" for Kafka server connection
```
### To run profiling tests with multiple runs at once:
```
import profiling
profiling.timer_kafka("file_path_to_images.tif", "to_time") # to_time can be p: producer, p2: producer already connected to Kafka or g:simulator
profiling.time_kafka_consumer() # time Kafka consumer
profiling.timer_kafka_100bytes() # time Kafka producer when sending small messages 
```

