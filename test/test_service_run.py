import pyberrynet
import unittest

from pyberrynet.error import InvalidInput
from pyberrynet.error import FileNotFound


class TestSummary(unittest.TestCase):
    """
    Test the functions of service.run().
    """

    def test_init(self):
        berrynet = pyberrynet.run()
        self.assertEqual(berrynet.is_closed, False)
        berrynet.close()
        self.assertEqual(berrynet.is_closed, True)
        berrynet.start()
        self.assertEqual(berrynet.is_closed, False)
        berrynet.restart()
        self.assertEqual(berrynet.is_closed, True)

    def test_input(self):
        with pyberrynet.run() as berrynet:
            #self.assertTrue(berrynet.upload('ipcamera'))
            self.assertTrue(berrynet.upload('boardcam'))
            self.assertTrue(berrynet.upload('localimage', '/home/pi/Pictures/5325.jpg'))

            # Stream from board cameras and ip cameras.
            self.assertTrue(berrynet.stream_start('stream_boardcam'))
            self.assertTrue(berrynet.stream_stop('stream_boardcam'))
            self.assertTrue(berrynet.stream_start('stream_ipcamera'))
            self.assertTrue(berrynet.stream_stop('stream_ipcamera'))

            self.assertTrue(berrynet.stream('stream_boardcam'))
            self.assertTrue(berrynet.stream('stream_boardcam'))

            self.assertTrue(berrynet.stream('stream_boardcam', stream_time=10))

    def test_InvalidInput(self):
        with pyberrynet.run() as berrynet:
            with self.assertRaises(InvalidInput):
                berrynet.upload('whatever')
            # BerryNet V2.1.0 changed the picamera to boardcam.
            with self.assertRaises(InvalidInput):
                berrynet.upload('picamera')
            with self.assertRaises(InvalidInput):
                berrynet.upload('')

            with self.assertRaises(InvalidInput):
                berrynet.upload('localimage','')

    def test_FileNotFound(self):
        path = ''
        with self.assertRaises(FileNotFound):
            berrynet = pyberrynet.run(path=path)

if __name__ == '__main__':
    unittest.main()