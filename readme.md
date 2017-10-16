# PyBerryNet
A Python API for BerryNet.
 
[![PyPI version](https://badge.fury.io/py/pyberrynet.svg)](https://badge.fury.io/py/pyberrynet)
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

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
    pip3 install paho-mqtt
### Install pyBerryNet from github
    $ git clone https://github.com/wliu2016/PyBerryNet
    $ cd PyBerryNet
    $ sudo python3 setup.py install

### Install pyBerryNet via pip
    pip3 install pyberrynet
 
## Usage
After completing all the installment, the usage will be very simple:
    
    import pyberrynet
    berrynet = pyberrynet.run()
    results = berrynet.upload('picamera')
    berrynet.close()
    
## Roadmap and priorities

| Items | Priority | Status|
|------------------------|--------------|----------------------|
|Updates for Berrynet updates|*****| Not started|
|Able to change more configuration settings| ****| Not started|
|Formulate documents in readthedoc.com|****| Not started|
|Fix conflict of backend status within one session| ****| Ongoing|
|Add examples and tutorials|***| Ongoing|
|Creating a Docker image for CI Travis testing|*****| Not started|
|~~Save result image~~| *****| Done|
|~~Able to draw boxes in the result image~~| ****| Done|
|~~Add test suitcase~~|******| Done|
|~~Prepare for pip installment~~|*****| Done|
|~~Testing with RPi3~~| *****| Done|
|~~Add license file~~|*****| Done|

## Comments or questions:

Please reply to this [issue](https://github.com/wliu2016/PyBerryNet/issues/1) for problems or comments.
