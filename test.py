import mfi
import os

test_mpower = mfi.MPower(os.environ['TESTMPOWER'], os.environ['TESTUSER'],
                         os.environ['TESTPASS'])
test_mport = mfi.MPort(os.environ['TESTMPORT'], os.environ['TESTUSER'],
                       os.environ['TESTPASS'])
print(test_mpower.get_data())
print(test_mpower.get_power(1))
print(test_mpower.get_power(2))
test_mpower.switch(1)
test_mpower.switch(1)
test_mpower.switch(1, 0)
test_mpower.switch(1, 1)
test_config = test_mpower.get_cfg()
print(test_config)
print(test_mpower.set_cfg(test_config))
print(test_mport.get_data())
print(test_mport.get_temperature(1))
print(test_mport.get_temperature(1, 'f'))
print(test_mport.get_temperature(2))
