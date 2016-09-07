var m = require('mraa'); //require mraa
console.log('MRAA Version: ' + m.getVersion()); //write the mraa version to the console

var analogPin0 = new m.Aio(0); //setup access analog inpuput pin 0
var analogValue = analogPin0.read(); //read the value of the analog pin
var analogValueFloat = analogPin0.readFloat(); //read the pin value as a float
console.log(analogValue); //write the value of the analog pin to the console
console.log(analogValueFloat.toFixed(5)); //write the value in the float format
