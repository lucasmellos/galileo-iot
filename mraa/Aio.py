import mraa

print (mraa.getVersion())

try:
    x = mraa.Aio(0)
    print (x.read())
    print ("%.5f" % x.readFloat())
except:
    print ("Are you sure you have an ADC?")