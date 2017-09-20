# PyBerryNet
A Python API for BerryNet. 

## Requirements

* Raspberry Pi 3 Model B (Or newer)
          
* Python libraries:
    * [Paho-MQTT](https://pypi.python.org/pypi/paho-mqtt/1.3.0)
    * [BerryNet](https://github.com/DT42/BerryNet)

## Install
To use this library, you need to properly setup Rapsberry Pi 3, install MQTT protocol and configure berrynet services.

### Setup Rapsberry Pi 3
    
   Please follow [this](https://www.raspberrypi.org/documentation/setup/) to set up your Pi.
### Configure BerryNet

DT42 group have kindly provided an installment guideline:

    $ git clone https://github.com/DT42/BerryNet.git
    $ cd BerryNet
    $ ./configure
It will take a while to build the programs.  Please refer to the [GitHub page](https://github.com/DT42/BerryNet) for further info. 

### Install [paho-mqtt 1.3.0](https://pypi.python.org/pypi/paho-mqtt/1.3.0) 
    pip install paho-mqtt
### Install pyBerryNet (under developing)
    pip install pyberrynet
 
## Usage
After completing all the installment, the usage will be very simple:
    
    import pyberrynet
    berrynet = pyberrynet.run()
    results = berrynet.upload('Localimage', path='filepath')

## Comments or questions:

Please reply to this [issue](https://github.com/wliu2016/PyBerryNet/issues/1) for problems or comments.