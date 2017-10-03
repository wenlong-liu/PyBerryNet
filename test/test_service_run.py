import pyberrynet
import unittest

from pyberrynet.error import InvalidInput
from pyberrynet.error import FileNotFound

class test_sumarry(unittest.TestCase):
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

    def test_input(self):
        berrynet = pyberrynet.run()
        #self.assertTrue(berrynet.upload('ipcamera'))
        self.assertTrue(berrynet.upload('picamera'))
        self.assertTrue(berrynet.upload('localimage', '/home/pi/Pictures/5325.jpg'))
        berrynet.close()
       
    def test_InvalidInput(self):
        berrynet = pyberrynet.run()
        
        with self.assertRaises(InvalidInput):
            berrynet.upload('whatever')
        
        with self.assertRaises(InvalidInput):
            berrynet.upload('localimage','')
        
        berrynet.close()
        
    def test_FileNotFound(self):
        path = ''
        with self.assertRaises(FileNotFound):
            berrynet = pyberrynet.run(path=path)

if __name__ == '__main__':
    unittest.main()