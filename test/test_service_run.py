import pyberrynet


class test_sumarry():
    """
    Test the functions of service.run().
    """

    def __init__(self):
        self.berrynet = pyberrynet.run()
        self.ip = 'ipcamera'
        self.picamera = 'picamera'
        self.local = 'localimage'
        self.path = ''

    def test_input(self):
        assert self.berrynet(self.ip)
        assert self.berrynet(self.picamera)
        assert self.berrynet(self.local, self.path)
