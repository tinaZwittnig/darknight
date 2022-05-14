#include <painlessMesh.h>
#include <Wire.h>
#include <SPI.h>
#include <Adafruit_Sensor.h>
#include "Adafruit_BME680.h"
#include "LTR390.h"

// mesh network configuration macros
#define   MESH_SSID       "darkNet"
#define   MESH_PASSWORD   "simislu"
#define   MESH_PORT       5555
#define EDGE_NODE_ID      4193624932

// I2C configuration macros
#define LTR_I2C_ADDRESS 0x53
#define BME_I2C_ADDRESS 0x77
#define I2C_SDA 41
#define I2C_SCL 40

// forward declarations
void sensorReader();

// global counter definitions
long highCounter = 0;
long lowCounter = 0;


// init I2C sensors
Adafruit_BME680 bme;
LTR390 ltr390(LTR_I2C_ADDRESS);

// init scheduler and mesh
Scheduler mainScheduler;
painlessMesh mesh;

bool calc_delay = false;
SimpleList <uint32_t> nodes;

// start sensor task
Task sensorTask(5000, TASK_FOREVER, &sensorReader);


void setup() {
    Serial.begin(115200);

    pinMode(PIR_PIN, INPUT);

    // init I2C driver
    Wire.begin(I2C_SDA, I2C_SCL);

    // try to start BME sensor
    if (!bme.begin(BME_I2C_ADDRESS)) {
        Serial.println("Could not find a valid BME680 sensor, check wiring!");
        while (1);
    }

    // init LTR sensor
    if (!ltr390.init()) {
        Serial.println("LTR390 not connected!");
        while (1);
    }

    // configure LTR sensor to work in LUX mode, set recommended params
    ltr390.setMode(LTR390_MODE_ALS);
    ltr390.setGain(LTR390_GAIN_3);
    ltr390.setResolution(LTR390_RESOLUTION_18BIT);


    // Set up oversampling and filter initialization
    bme.setTemperatureOversampling(BME680_OS_8X);
    bme.setHumidityOversampling(BME680_OS_2X);
    bme.setPressureOversampling(BME680_OS_4X);
    bme.setIIRFilterSize(BME680_FILTER_SIZE_3);
    bme.setGasHeater(320, 150); // 320*C for 150 ms

    // start mesh
    mesh.setDebugMsgTypes(ERROR | DEBUG);  // set before init() so that you can see error messages
    mesh.init(MESH_SSID, MESH_PASSWORD, &mainScheduler, MESH_PORT);

    // start sensors task
    mainScheduler.addTask(sensorTask);
    sensorTask.enable();

}

void loop() {
    mesh.update();
}

void sensorReader() {
    float temperature = 0;
    float pressure = 0;
    float humidity = 0;
    float gas = 0;
    float lux = 0;

    if (bme.performReading()) {
        temperature = bme.temperature;
        pressure = bme.pressure / 100.0;
        humidity = bme.humidity;
        gas = bme.gas_resistance / 1000.0;
    }

    if (ltr390.newDataAvailable()) {
        if (ltr390.getMode() == LTR390_MODE_ALS) {
            lux = ltr390.getLux();
        } else {
            ltr390.setGain(LTR390_GAIN_3);
            ltr390.setResolution(LTR390_RESOLUTION_18BIT);
            ltr390.setMode(LTR390_MODE_ALS);
        }
    }

    // assemble JSON message
    String msg = "{\"type\": \"enviroment\", \"temperature\":";
    msg += String(temperature);
    msg += ",\"pressure\":" + String(pressure);
    msg += ",\"humidity\":" + String(humidity);
    msg += ",\"gas\":" + String(gas);
    msg += ",\"lux\":" + String(lux);
    msg += ", \"from\": ";
    msg += mesh.getNodeId();
    msg += "} ";

    // send message to EDGE node
    mesh.sendSingle(EDGE_NODE_ID, msg);

    Serial.printf("Sending message: %s\n", msg.c_str());


}