import time
from bitalino import BITalino

macAddress = "20:18:06:13:02:19"

running_time = 5

batteryThreshold = 30
acqChannels = [0,1,2,3,4,5]
samplingRate = 1000
nSamples = 10
digitalOutput = [1,1]

device = BITalino(macAddress)

device.battery(batteryThreshold)

print(device.version())
