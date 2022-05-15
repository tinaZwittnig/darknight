#include <painlessMesh.h>

// mesh network configuration macros
#define   MESH_SSID       "darkNet"
#define   MESH_PASSWORD   "simislu"
#define   MESH_PORT       5555
#define EDGE_NODE_ID      4193624932

// PIR sensor macros
#define LOW_COUNTER_LIMIT 5
#define PIR_PIN           14
#define RELAY_PIN         12


// forward declarations
void receivedCallback(uint32_t from, String &msg);

void newConnectionCallback(uint32_t nodeId);

void nodeTimeAdjustedCallback(int32_t offset);

void delayReceivedCallback(uint32_t from, int32_t delay);

void sensorReader();



// global counter definitions
static long highCounter = 0;
static long lowCounter = 0;

// init scheduler and mesh
Scheduler mainScheduler;
painlessMesh mesh;

bool calc_delay = false;
SimpleList <uint32_t> nodes;

// start sensor task
Task sensorTask(100, TASK_FOREVER, &sensorReader);


void setup() {
    Serial.begin(115200);
    // start PIR pin as input, relay pin as output
    pinMode(PIR_PIN, INPUT);
    pinMode(RELAY_PIN, OUTPUT);

    // start WiFi mesh
    mesh.setDebugMsgTypes(ERROR | DEBUG);
    mesh.init(MESH_SSID, MESH_PASSWORD, &mainScheduler, MESH_PORT);

    // start sensor task
    mainScheduler.addTask(sensorTask);
    sensorTask.enable();

}

void loop() {
    mesh.update();
}

void sensorReader() {
    int pir = digitalRead(PIR_PIN);

    if (pir == 1) {
        highCounter += 1;
        lowCounter = 0;
        // turn on the light
        digitalWrite(RELAY_PIN, 1);
    } else {
        lowCounter += 1;
    }


    if (lowCounter > LOW_COUNTER_LIMIT) {
        lowCounter = 1;
        highCounter = 0;
        // turn of the light
        digitalWrite(RELAY_PIN, 0);
    }

    if (highCounter > 10 && lowCounter > 2) {
        sendSensorMessage(highCounter);
        highCounter = 0;
    }

}

void sendSensorMessage(long highTime) {
    // assemble JSON message
    String msg = "{\"type\": \"presence\", \"duration\":";
    msg += String(highTime);
    msg += ", \"from\": ";
    msg += mesh.getNodeId();
    msg += "} ";

    // send message to EDGE node
    mesh.sendSingle(EDGE_NODE_ID, msg);

    Serial.printf("Sending message: %s\n", msg.c_str());
}