#include <painlessMesh.h>

// mesh network configuration macros
#define   MESH_SSID       "darkNet"
#define   MESH_PASSWORD   "simislu"
#define   MESH_PORT       5555

// forward declarations
void receivedCallback(uint32_t from, String &msg);

void newConnectionCallback(uint32_t nodeId);

void changedConnectionCallback();

// init scheduler and mesh
Scheduler userScheduler;
painlessMesh mesh;

bool calc_delay = false;
SimpleList <uint32_t> nodes;

void setup() {
    Serial.begin(115200);
    // start WiFi mesh
    mesh.setDebugMsgTypes(ERROR | DEBUG);  // set before init() so that you can see error messages
    mesh.init(MESH_SSID, MESH_PASSWORD, &userScheduler, MESH_PORT);
    mesh.onReceive(&receivedCallback);
    mesh.onChangedConnections(&changedConnectionCallback);
}

void loop() {
    mesh.update();
}


void receivedCallback(uint32_t from, String &msg) {
    // print JSON formatted message to RPi
    Serial.printf("{\"from\": \"%u\", \"msg\":\%s\}\n", from, msg.c_str());
}


void changedConnectionCallback() {
    nodes = mesh.getNodeList();
}