Master thesis work to simulate a microscope and stream the images coming from the microscope.

The simulator can either be run on its own or connected with Kafka. To run it with Kafka a Kafka server is needed. 

Instructions how to run the simulator:
Python dependencies: 
cv2, numpy, PIL, flask, kafka-python, skimage


1. Clone repo
2. to use web interface (will appear on localhost 127.0.0.1:5000/fileWalk): python3 simulator
3. to use the simulator without the interface:
	import simulator_no_flask
	simulator_no_flask.get_files(file_path, period, binning, color_channel, connect_kafka) # period = period time in seconds,  color_channel given as
	list with up to 5 channels ie. ["1", "2", "5"], connect_kafka set to "yes" for Kafka server connection
4. to profile with multiple runs at once: 
	import profiling
	profiling.timer_kafka("file_path_to_images.tif", "to_time") # to_time can be p: producer, p2: producer already connected to Kafka or g:simulator
	profiling.time_kafka_consumer() # time Kafka consumer
	profiling.timer_kafka_100bytes() # time Kafka producer when sending small messages 




# Project Title

One Paragraph of project description goes here

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

```
Give examples
```

### Installing

A step by step series of examples that tell you have to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone who's code was used
* Inspiration
* etc
