# A picamera module is needed in this example.
import pyberrynet

# Start berrynet service.
berrynet = pyberrynet.run()
# Upload a picture by campturing it via picamera
results = berrynet.upload('picamera')
# RPi will preview the picamera, take a picture and upload the image to backend server.
print(results)

berrynet.close()
