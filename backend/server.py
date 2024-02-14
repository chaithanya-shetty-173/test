from flask import Flask, jsonify,request
from flask_cors import CORS

import RPi.GPIO as GPIO
from time import sleep
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#measure1
trig_pin1 = 13
echo_pin1 = 6
#measure2
trig_pin2=26
echo_pin2=19
#measure3
trig_pin3=26
echo_pin3=19
#measure4
trig_pin4=8
echo_pin4=7

#mixing container
mix_trig_pin=23
mix_echo_pin=18

#motar_mix
motar_mix_pin=25

#solenoidpins
solenoid_pin1 = 4
solenoid_pin2 = 17
solenoid_pin3 = 27
solenoid_pin4 = 22

#define motar driver pins
IN1 = 16
IN2 = 20
EN = 21

GPIO.setup(solenoid_pin1, GPIO.OUT)
GPIO.setup(solenoid_pin2, GPIO.OUT)
GPIO.setup(solenoid_pin3, GPIO.OUT)
GPIO.setup(solenoid_pin4, GPIO.OUT)

GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(EN, GPIO.OUT)

GPIO.setup(motar_mix_pin, GPIO.OUT)

GPIO.setup(trig_pin1, GPIO.OUT)
GPIO.setup(echo_pin1, GPIO.IN)

GPIO.setup(trig_pin2, GPIO.OUT)
GPIO.setup(echo_pin2, GPIO.IN)

GPIO.setup(trig_pin3, GPIO.OUT)
GPIO.setup(echo_pin3, GPIO.IN)

GPIO.setup(trig_pin4, GPIO.OUT)
GPIO.setup(echo_pin4, GPIO.IN)


GPIO.setup(mix_trig_pin, GPIO.OUT)
GPIO.setup(mix_echo_pin, GPIO.IN)


def forward():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(EN, GPIO.HIGH)
def stop():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(EN, GPIO.LOW)


def measure_water_level_mixing_tank():
    # Trigger ultrasonic sensor
    pulse_start = time.time()
    GPIO.output(mix_trig_pin, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(mix_trig_pin, GPIO.LOW)

    # Wait for echo response
    while GPIO.input(mix_echo_pin) == 0:
        pulse_start = time.time()

    while GPIO.input(mix_echo_pin) == 1:
        pulse_end = time.time()

    # Calculate distance (in centimeters)
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)

    return distance

def measure_chemical_1():
    # Trigger ultrasonic sensor
    GPIO.output(trig_pin1, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(trig_pin1, GPIO.LOW)

    # Wait for echo response
    while GPIO.input(echo_pin1) == 0:
        pulse_start = time.time()

    while GPIO.input(echo_pin1) == 1:
        pulse_end = time.time()

    # Calculate distance (in centimeters)
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)

    return distance

def measure_chemical_2():
    # Trigger ultrasonic sensor
    GPIO.output(trig_pin2, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(trig_pin2, GPIO.LOW)

    # Wait for echo response
    while GPIO.input(echo_pin2) == 0:
        pulse_start = time.time()

    while GPIO.input(echo_pin2) == 1:
        pulse_end = time.time()

    # Calculate distance (in centimeters)
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)

    return distance

def measure_chemical_3():
    # Trigger ultrasonic sensor
    GPIO.output(trig_pin3, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(trig_pin3, GPIO.LOW)

    # Wait for echo response
    while GPIO.input(echo_pin3) == 0:
        pulse_start = time.time()

    while GPIO.input(echo_pin3) == 1:
        pulse_end = time.time()

    # Calculate distance (in centimeters)
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)

    return distance

def measure_chemical_4():
    # Trigger ultrasonic sensor
    GPIO.output(trig_pin4, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(trig_pin4, GPIO.LOW)

    # Wait for echo response
    while GPIO.input(echo_pin4) == 0:
        pulse_start = time.time()

    while GPIO.input(echo_pin4) == 1:
        pulse_end = time.time()

    # Calculate distance (in centimeters)
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)

    return distance



app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3004", "methods": ["GET", "POST", "PUT", "DELETE"]}}, supports_credentials=True)

@app.route('/setValveStates', methods=['POST'])
def set_states():
    body = request.json
    valveStates = body['valveStates']
    for key, value in valveStates.items():
        if key=="valve1" and valveStates[key]==True:
            print("solenoid valve 1 on")
            GPIO.output(solenoid_pin1, GPIO.LOW)
        elif key=="valve1" and valveStates[key]==False:
            print("solenoid valve 1 off")
            GPIO.output(solenoid_pin1, GPIO.HIGH)
        elif key=="valve2" and valveStates[key]==True:
            print("solenoid valve 2 on")
            GPIO.output(solenoid_pin2, GPIO.LOW)
        elif key=="valve2" and valveStates[key]==False:
            print("solenoid valve 2 off")
            GPIO.output(solenoid_pin2, GPIO.HIGH)
        elif key=="valve3" and valveStates[key]==True:
            print("solenoid valve 3 on")
            GPIO.output(solenoid_pin3, GPIO.LOW)
        elif key=="valve3" and valveStates[key]==False:
            print("solenoid valve 3 off")
            GPIO.output(solenoid_pin3, GPIO.HIGH)
        elif key=="valve4" and valveStates[key]==True:
            print("solenoid valve 4 on")
            GPIO.output(solenoid_pin4, GPIO.LOW)
        elif key=="valve4" and valveStates[key]==False:
            print("solenoid valve 4 off")
            GPIO.output(solenoid_pin4, GPIO.HIGH)
    data = {"status": "successfully triggered"}
    return jsonify(data)

@app.route('/setPumpStates', methods=['POST'])
def set_PumpStates():
    body = request.json
    pumpStates = body['pumpStates']


    for key, value in pumpStates.items():
        if key=="pump1" and pumpStates[key]==True:
            print("pump 1 on")
            
        elif key=="pump1" and pumpStates[key]==False:
            print("pump 1 off")
            stop()
        elif key=="pump2" and pumpStates[key]==True:
            print("pump 2 on")
            forward()
        elif key=="pump2" and pumpStates[key]==False:
            print("pump 2 off")
        elif key=="actuator" and pumpStates[key]==True:
            print("mixing actuator on")
            GPIO.output(motar_mix_pin, GPIO.LOW)
        elif key=="actuator" and pumpStates[key]==False:
            print("mixing actauor off")
            GPIO.output(motar_mix_pin, GPIO.HIGH)

    data = {"status": "successfully triggered"}
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
