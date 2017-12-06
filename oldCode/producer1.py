import time
import cv2
from kafka import SimpleProducer, KafkaClient
#from kafka.common import LeaderNotAvailableError



#connect to Kafka
kafka = KafkaClient('lovisa:9092')
producer = SimpleProducer(kafka)
#Assign a topic
topic = 'test'
def video_emitter(video):
    # Open the video
    video = cv2.VideoCapture(video)
    print(' emitting.....')

    # read the file
    while (video.isOpened):
        # read the image in each frame
        success, image = video.read()
        # check if the file has read to the end
        if not success:
            break
        # convert the image png
        ret, jpeg = cv2.imencode('.png', image)
        # Convert the image to bytes and send to kafka
        producer.send_messages(topic, jpeg.tobytes())
        # To reduce CPU usage create sleep time of 0.2sec
        time.sleep(0.2)
    # clear the capture
    video.release()
    print('done emitting')

def print_response(response=None):
    if response:
        print('Error: {0}'.format(response[0].error))
        print('Offset: {0}'.format(response[0].offset))

def main():
	msg = b'Hello from the other side!'
	
#	try:
	print_response(producer.send_messages(topic, msg))
#	except LeaderNotAvailableError:
#		time.sleep(1)
#		print_response(producer.send_messages(topic, msg))
	kafka.close()

if __name__ == '__main__':
 #   video_emitter('video.mp4')
	main()

