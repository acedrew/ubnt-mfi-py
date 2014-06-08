ubnt-mfi-py
===========

Python API for Ubiquiti mFi gear.

To use the test suite, you will need to set the TESTMPORT, TESTMPOWER, TESTUSER, TESTPASS environment variables. 

Currently, you can retrieve the system.cfg file, via the http interface, into a UbntConfig object and make some changes to it.
DO NOT TRUST UbntConfg.get_config_dump() it needs much more testing before use, to ensure it does not brick any devices. I want to be very careful to avoid loading invalid configs on the device.
