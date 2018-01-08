# Microscope simulator for the HASTE project 

Master thesis work to simulate a microscope and stream the images coming from the microscope.

The simulator can either be run on its own or connected with Kafka. To run it with Kafka a Kafka server is needed. 

## Getting started

### Prerequisites

cv2, numpy, PIL, Flask, kafka-python, scikit-image 

To stream to Harmonic IO, the stream connector is needed (with container support): 
https://github.com/benblamey/HarmonicIO (see 'Install the Streaming Connector only')

### Installing

For installation in development mode:

A step by step series of examples that tell you have to get a development env running

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

See `example_*.py`

```
import simulator_no_flask
simulator_no_flask.get_files(file_path, period, binning, color_channel, connect_kafka) # period = period time in seconds,  color_channel given as
	#list with up to 5 channels ie. ["1", "2", "5"], connect_kafka set to "yes" for Kafka server connection
```

You should see output like this:

```
simulator: list of files to stream:
['dummy_image_0.png']
simulator: stream ID is: 2018_01_08__10_35_55_dummy_set
simulator: initialized streaming target
file: ./test-images/dummy_image_0.png has size: 130450
Sending request..
http://192.168.1.24:8080/streamRequest?token=None&c_name=benblamey/haste-example:latest&c_os=ubuntu&priority=0&source=node1&digest=8571979be2b85fe2f64a26f67e8221e1
[OUT: Push data to worker (192.168.1.24:9001>benblamey/haste-example:latest) successful.]
simulator: all files streamed
```


### To run profiling tests with multiple runs at once:
```
import profiling
profiling.timer_kafka("file_path_to_images.tif", "to_time") # to_time can be p: producer, p2: producer already connected to Kafka or g:simulator
profiling.time_kafka_consumer() # time Kafka consumer
profiling.timer_kafka_100bytes() # time Kafka producer when sending small messages 
```

