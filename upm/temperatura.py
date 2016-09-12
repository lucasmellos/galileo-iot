import time
import pyupm_grove as grove

# Create the temperature sensor object using AIO pin 0
temp = grove.GroveTemp(0)
print temp.name()

# Read the temperature ten times, printing both the Celsius and
# equivalent Fahrenheit temperature, waiting one second between readings
for i in range(0, 10):
    celsius = temp.value()
    fahrenheit = celsius * 9.0/5.0 + 32.0;
    print "%d degrees Celsius, or %d degrees Fahrenheit" \
        % (celsius, fahrenheit)
    time.sleep(1)

# Delete the temperature sensor object
del temp