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
    def __init__(self, warm_up=10, is_closed=False, server='localhost', port=1883,
                 engine='detector', path='/home/pi/BerryNet'):
        """
        :param warm_up: Allow the service to warm up certain seconds, default: 10. If 0, disable warm up.
        :param is_closed: the status of the beryrnet service. default: False
        :param server: the server to host berrynet, default: localhose.
        :param port: the port of mqtt, default: 1883.
        :param engine: the engine to detect image or video, options: detector or classifier. default: detector.
        :param path: the fold directory for berrynet files. default: '/home/pi/BerryNet'
        """

        self.is_closed = is_closed
        self.warm_up = warm_up
        self.server = server
        self.port = port
        # supported image inputs for now as of Sep. 18, 2017.
        self.img_list = ['picamera', 'ipcamera', 'localimage']
        self.path = path
        # double check the engine in configure.js.
        self.engine = engine
        self._check_engine()
        # initialize the service.
        self.start()

    def _check_engine(self):
        """
        Check the engine configuration in config.js.  
        
        TODO: It is an ugly way to do it.  More Pythonic way is needed. 
        """
        lines = []
        try:
            with open(str(self.path)+'/config.js') as infile:
                for line in infile:
                    if line.startswith('config.inferenceEngine'):
                        line = "config.inferenceEngine = '{}';  // (classifier, detector)\n".format(self.engine)
                    lines.append(line)

            with open(str(self.path)+'/config.js', 'w') as outfile:
                for line in lines:
                    outfile.write(line)

        except IOError as e:
            raise FileNotFound(e)
            

    def _img_source(self, img_source):
        """ Return the topic and message for mqtt based on the image source type"""

        topic_dictionary = {
            'picamera': ('berrynet/event/camera','snapshot_picam'),
            'ipcamera': ('berrynet/event/camera','snapshot_ipcam'),
            'localimage': ('berrynet/event/localImage', None)
        }

        if img_source.lower() in self.img_list:
            topic, message = topic_dictionary[img_source.lower()]
        else:
            raise InvalidInput("Invalid input: {} is not in the supported list!".format(img_source))
            

        return topic,message

    def upload(self, img_source=None, path=None, client_id="", save_img=False, save_path=None,
               draw_bound=False, **kwargs):
        """
        Publish images to broker using MQTT protocol
        :param 
        img_source: the way to capture an image, such as picamera, IPcamera, or localimage.
        path: the file path for local image, default: None.
        client_id: the ID for each payload upload.
        save_img: save the img or not. default: False.
        save_path: the path to save img. default: None.
        draw_bound: draw the bounding in the img. Default: False.
        
        :return 
        Success is a dictionary of recognize results; 
        failure will raise the exceptions and return None.
        
        :todo
        Draw boxes for the image taken.        
        """
        topic, message = self._img_source(img_source)
        # if publish a local image, message is the path of the image.
        if not message:
            if path:
                message = path
            else:
                raise InvalidInput("Invalid input: local image path required!")
                

        try:
            publish.single(topic, payload=message, hostname=self.server, port=self.port, client_id=client_id, **kwargs)
            results = self._receive_result()
            #Draw boxes for the image taken.
            return results

        except Exception as e:
            raise InvalidInput(e)
            return None

    def _receive_result(self,topic='berrynet/dashboard/inferenceResult', **kwargs):
        """
        Subscribe the broker and receive the results
        :param 
        topic: the topic to subscribe to receive the results.
        
        :return 
        A dictionary with all the inferences results from the model. 
        """
        msg = subscribe.simple(topics=topic, **kwargs)
        message = msg.payload.decode()
        results = yaml.load(message)

        return results

    def _receive_img(self,topic='berrynet/dashboard/inference', **kwargs):
        """
        Subscribe the inference topic to receive the image.
        :param topic: the topic to receive image.
        :return: the published image.
        """
        msg = subscribe.simple(topics=topic, **kwargs)
        message = msg.payload.decode()

        return message

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
