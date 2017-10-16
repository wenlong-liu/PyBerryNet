import pyberrynet

# Start berrynet service.
berrynet = pyberrynet.run()

# Start and stop video streaming.
berrynet.stream_start('stream_boardcam')
berrynet.stream_stop('stream_boardcam')

berrynet.close()