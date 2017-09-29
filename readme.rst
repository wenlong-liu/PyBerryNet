PyBerryNet
==========

A Python API for BerryNet.

Requirements
------------

-  Raspberry Pi 3 Model B (Or newer)

-  Python libraries:

   -  `Paho-MQTT <https://pypi.python.org/pypi/paho-mqtt/1.3.0>`__
   -  `BerryNet <https://github.com/DT42/BerryNet>`__

Install
-------

To use this library, you need to properly setup Rapsberry Pi 3, install
MQTT protocol and configure berrynet services.

Setup Rapsberry Pi 3
~~~~~~~~~~~~~~~~~~~~

Please follow
`this <https://www.raspberrypi.org/documentation/setup/>`__ to set up
your Pi. ### Configure BerryNet

DT42 group have kindly provided an installment guideline:

::

    $ git clone https://github.com/DT42/BerryNet.git
    $ cd BerryNet
    $ ./configure

It will take a while to build the programs. Please refer to the `GitHub
page <https://github.com/DT42/BerryNet>`__ for further info.

Install `paho-mqtt 1.3.0 <https://pypi.python.org/pypi/paho-mqtt/1.3.0>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    pip install paho-mqtt

Install pyBerryNet from github
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    $ git clone https://github.com/wliu2016/PyBerryNet
    $ cd PyBerryNet
    $ sudo python3 setup.py install

Install pyBerryNet via pip
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    pip install pyberrynet

Usage
-----

After completing all the installment, the usage will be very simple:

::

    import pyberrynet
    berrynet = pyberrynet.run()
    results = berrynet.upload('picamera')
    berrynet.close()


Comments or questions:
----------------------

Please reply to this
`issue <https://github.com/wliu2016/PyBerryNet/issues/1>`__ for problems
or comments.
