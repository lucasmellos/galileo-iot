import paho.mqtt.client as mqtt #make sure you have installed mqtt client library for python
import ssl
import json
import time
import thread

#defining necessary pins
led = 4
buzzer = 3
button = 2

#Importing Intel Galileo Official UPM Library
import pyupm_grove as grove

# Create the temperature sensor object using AIO pin 0
temp = grove.GroveTemp(0)

# Create the light sensor object using AIO pin 0
light = grove.GroveLight(1)

# make sure python wiring x86 library is installed.
# Import the GPIOEdison class from the wiringx86 module.
from wiringx86 import GPIOGalileoGen2 as GPIO
gpio = GPIO()

gpio.pinMode(led, gpio.OUTPUT)
gpio.pinMode(buzzer , gpio.PWM)
gpio.pinMode(button, gpio.INPUT)

#defining topics
servoTopic  = "coisas/servo"
ledTopic    = "coisas/led"
buttonTopic = "coisas/butao"
buzzerTopic = "coisas/buzzer"
tempTopic   = "coisas/temp"
potTopic    = "coisas/pot"
lightTopic    = "coisas/light"


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(servoTopic)
    client.subscribe(ledTopic)
    client.subscribe(buzzerTopic)
    client.subscribe("topic/test")
    print("Subscribed to Necessary Topics")

def on_message(client, userdata, msg):
    print "Message Topic :" + str(msg.topic)
    print "Message :" + str(msg.payload)
    if str(msg.topic) == ledTopic:
	blinkLED(str(msg.payload))
    elif str(msg.topic) == buzzerTopic:
	soundBuzzer(str(msg.payload))


def blinkLED(msg):
    jsonData = json.loads(msg)
    print jsonData
    for x in range(0,(jsonData['loopFor'])):
        gpio.digitalWrite(led, gpio.HIGH)
        time.sleep(jsonData['Period'])
        gpio.digitalWrite(led, gpio.LOW)
        time.sleep(jsonData['Period'])
    print "Blink LED Done"

def soundBuzzer(msg):
    jsonData = json.loads(msg)
    print jsonData
    gpio.analogWrite(buzzer, jsonData['PWM'])
    time.sleep(jsonData['Period'])
    gpio.analogWrite(buzzer, 0)
    print "Sound Buzzer Done"


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.tls_set(ca_certs='./cert/rootCA.pem', certfile='./cert/NOME DO CERTIFICADO-certificate.pem.crt', keyfile='./cert/NOME DO CERTIFICADO-private.pem.key', tls_version=ssl.PROTOCOL_SSLv23)
client.tls_insecure_set(True)
client.connect("SUA REGIAO.amazonaws.com", 8883, 60) #Taken from REST API endpoint



#Publishing Analog Values to AWS
def publishTemp(Dummy):
	while (1):
		celsius = temp.value()
		fahrenheit = celsius * 9.0/5.0 + 32.0;
		tempJsonObject = json.dumps("{'Temp em Celsius':" + str(celsius)  + "}")
		client.publish(tempTopic, payload=tempJsonObject , qos=0, retain=False)
		print "%d graus Celsius, ou %d graus Fahrenheit.. Publicado no AWS" % (celsius, fahrenheit)
		#Wait for Five second
		time.sleep(5)

def publishLight(Dummy):
	while (1):
		print "Light Valor: " + str(light.raw_value() )
		lightJsonObject = json.dumps("{'Light Valor':" + str(light.raw_value() )  + "}")
		client.publish(lightTopic, payload=lightJsonObject , qos=0, retain=False)
		#Wait for Five second
		time.sleep(5)

def buttonPress(Dummy):
	while(1):
		#print "In Loop"
		if gpio.digitalRead(button) == 1:
			print "Botão pressionado"
			client.publish(buttonTopic, payload="Botão pressionado" , qos=0, retain=False)


thread.start_new_thread(publishTemp,("publishTempThread",))
thread.start_new_thread(publishLight,("publishLightThread",))
thread.start_new_thread(buttonPress,("publishbuttonThread",))


client.loop_forever() #MQTT's will never end
