import pyberrynet

# Start berrynet service.
berrynet = pyberrynet.run()
# Push a local file to server.
results = berrynet.upload('Localimage', path='filepath')
print(results)
# Close the service.
berrynet.close()
