#include <painlessMesh.h>

#define   MESH_SSID       "darkNet"
#define   MESH_PASSWORD   "simislu"
#define   MESH_PORT       5555
#define   RELAY_PIN       12
#define   LIGHT_DELAY     100
#define EDGE_NODE_ID        4193624932


// Prototypes
void sendMessage();
void receivedCallback(uint32_t from, String & msg);
void changedConnectionCallback();
void delayWorker();
void sendHeartbeat();

Scheduler     mainScheduler; // to control your personal task
painlessMesh  mesh;

bool calc_delay = false;
SimpleList<uint32_t> nodes;
long lightOn = 0;

Task delayWorkerTask( 100, TASK_FOREVER, &delayWorker );
Task hartbeatTask( 5000, TASK_FOREVER, &sendHeartbeat );


void setup() {
    Serial.begin(115200);

    pinMode(RELAY_PIN, OUTPUT);



    mesh.setDebugMsgTypes(ERROR | DEBUG);  // set before init() so that you can see error messages

    mesh.init(MESH_SSID, MESH_PASSWORD, &mainScheduler, MESH_PORT);
    mesh.onReceive(&receivedCallback);
    mesh.onChangedConnections(&changedConnectionCallback);

    Serial.print("ID: ");
    Serial.println(mesh.getNodeId());

    mainScheduler.addTask( delayWorkerTask );
    delayWorkerTask.enable();

}

void loop() {
    mesh.update();
}


void delayWorker() {

    if (lightOn > LIGHT_DELAY) {
        lightOn = 0;
        digitalWrite(RELAY_PIN, 0);
    }

    if ( lightOn > 0) {
        lightOn += 1;
    }

}

void sendHeartbeat() {
    String msg = "hartbeat:";
    msg += mesh.getNodeId();
    mesh.sendSingle(EDGE_NODE_ID, msg);
}


void receivedCallback(uint32_t from, String & msg) {
    Serial.printf("{\"from\": \"%u\", \"msg\":\%s\}\n", from, msg.c_str());

    if (from == 679185593) {
        digitalWrite(RELAY_PIN, 1);
        lightOn = 1;

    }
}


void changedConnectionCallback() {
    nodes = mesh.getNodeList();
}

