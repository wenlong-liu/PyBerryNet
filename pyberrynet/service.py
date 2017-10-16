import os
import time
import yaml

import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish

from pyberrynet.error import InvalidInput
from pyberrynet.error import FileNotFound


class run():
    """
    PyBN is a wrap-up for the package in BerryNet.
    """
    # supported image inputs for now as of Oct. 16, 2017.
    _img_list = ['boardcam', 'ipcamera', 'localimage', 'stream_boardcam', 'stream_ipcamera']
    # Get current working directory.
    _current_wd = os.getcwd()

    def __init__(self, warm_up=5, is_closed=True, server='localhost', port=1883,
                 engine='detector', save_path=_current_wd, path='/home/pi/BerryNet'):
        """
        :param warm_up: Allow the service to warm up certain seconds, default: 10. If 0, disable warm up.
        :param is_closed: the status of the beryrnet service. default: True.
        :param server: the server to host berrynet, default: localhose.
        :param port: the port of mqtt, default: 1883.
        :param engine: the engine to detect image or video, options: detector or classifier. default: detector.
        :param save_path: the directory to save the results.  Default: current working directory.
        :param path: the fold directory for berrynet files. default: '/home/pi/BerryNet'
        """
        self.is_closed = is_closed
        self.warm_up = warm_up
        self.server = server
        self.port = port
        self.path = str(path)
        # double check the engine in configure.js.
        self.engine = engine
        self.save_path = save_path + '/images'
        self._check_config()
        # initialize the service.
        self.start()

    def _check_config(self):
        """
        Check the current configuration in config.js.  
        
        TODO: It is an ugly way to do it.  More Pythonic way is needed. 
        """
        lines = []
        try:
            with open(self.path + '/config.js') as infile:
                for line in infile:
                    if line.startswith('config.inferenceEngine'):
                        line = "config.inferenceEngine = '{}';  // (classifier, detector)\n".format(self.engine)
                    elif line.startswith('config.storageDirPath'):
                        line = "config.storageDirPath = '{};\n".format(self.save_path)
                    lines.append(line)

            with open(self.path + '/config.js', 'w') as outfile:
                for line in lines:
                    outfile.write(line)

        except IOError as e:
            raise FileNotFound(e)

    def _img_source(self, img_source):
        """ Return the topic and message for mqtt based on the image source type"""

        _topic_dictionary = {
            'boardcam': ('berrynet/event/camera', 'snapshot_boardcam'),
            'ipcamera': ('berrynet/event/camera', 'snapshot_ipcam'),
            'localimage': ('berrynet/event/localImage', None),
            'stream_boardcam': ('berrynet/event/camera', 'stream_boardcam'),
            'stream_ipcamera': ('berrynet/event/camera', 'stream_nest_ipcam')
        }

        try:
            topic, message = _topic_dictionary[img_source.lower()]
        except KeyError:
            raise InvalidInput("{} is not in the supported list!".format(img_source))
        except AttributeError as e:
            raise InvalidInput(e)

        return topic, message

    def upload(self, img_source=None, path=None, client_id="", **kwargs):
        """
        Publish images to broker using MQTT protocol
        :param img_source: the way to capture an image, such as picamera, IPcamera, or localimage.
        :param path: the file path for local image, default: None.
        :param client_id: the ID for each payload upload.
        
        :return Success is a dictionary of recognize results; 
        :return failure will raise the exceptions and return None.
            
        """
        topic, message = self._img_source(img_source)

        # if publish a local image, message is the path of the image.
        if not message:
            if path:
                message = path
            else:
                raise InvalidInput("Local image path required!")

        try:
            publish.single(topic, payload=message, hostname=self.server, port=self.port, client_id=client_id, **kwargs)
            results = self._receive_result()
            return results

        except Exception as e:
            raise InvalidInput(e)
            return None

    def stream(self, stream_source=None, stream_time=1):
        """
        Identify real-time stream video from ip cameras and on-board cameras.  This function will run the stream for
        specific time periods.
        :param stream_source: The source of cameras. Options:  stream_boardcam and stream_ipcamera.
        :param stream_time: The duration of video streaming. unit: seconds. Default: 1 seconds.
        :return: results of the video streaming.
        """

        self.stream_start(stream_source)
        time.sleep(stream_time)
        self.stream_stop(stream_source)

    def stream_start(self, stream_source=None, client_id="", **kwargs):
        topic, message = self._img_source(stream_source)
        message = message + '_start'
        publish.single(topic, payload=message, hostname=self.server, port=self.port, client_id=client_id, **kwargs)

        return True

    def stream_stop(self, stream_source=None, client_id="", **kwargs):
        topic, message = self._img_source(stream_source)
        message = message + '_stop'
        publish.single(topic, payload=message, hostname=self.server, port=self.port, client_id=client_id, **kwargs)

        return True

    def _receive_result(self, topic='berrynet/dashboard/inferenceResult', **kwargs):
        """
        Subscribe the broker and receive the results
        :param  topic: the topic to subscribe to receive the results.
        
        :return A dictionary with all the inferences results from the model. 
        """
        msg = subscribe.simple(topics=topic, **kwargs)
        message = msg.payload.decode()
        results = yaml.load(message)

        return results

    def receive_img(self, topic='berrynet/dashboard/inference', **kwargs):
        """
        Subscribe the inference topic to receive the image.
        :param topic: the topic to receive image.
        :return: the published image.
        """
        msg = subscribe.simple(topics=topic, **kwargs)
        message = msg.payload.decode()

        return message

    def restart(self, delay=None):
        """
        Automatically restart the backend system. 
        :param delay: optional.  Restart the system after certain seconds. Unit: seconds.
        """
        if delay:
            time.sleep(delay)
        try:
            if self.is_closed:
                print('The BerryNet is already closed, starting it now')
            else:
                self.close()
                # wait 0.1 second to restart the backend.
                time.sleep(0.1)
        finally:
            self.start()

    def close(self):
        self.is_closed = True
        # Call to close the backend service
        os.system('berrynet-manager stop')

    def start(self):
        if self.is_closed:
            self.is_closed = False
            # Call to start the backend service
            os.system('berrynet-manager start')

            # It is better to warm up the system for 10 seconds.
            if self.warm_up:
                print('Warming up......')
                time.sleep(self.warm_up)
        else:
            print('The BerryNet is already started.')

    @staticmethod
    def status():
        """
        :return: return the status of the backend berrynet.
        """
        return os.system('berrynet-manager status')

    @staticmethod
    def return_log():
        """
        :return: return the status of the backend berrynet.
        """
        return os.system('berrynet-manager log')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.is_closed:
            self.close()
        return False

    def __del__(self):
        try:
            if not self.is_closed:
                self.close()
        except AttributeError:
            pass
