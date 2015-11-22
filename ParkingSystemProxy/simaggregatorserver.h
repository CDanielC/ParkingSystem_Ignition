#ifndef SIMAGGREGATORSERVER_H
#define SIMAGGREGATORSERVER_H
#include <map>
#include "monitor.h"

using namespace std;

class SimAggregatorServer
{
public:
    SimAggregatorServer();

signals:

public slots:

private:
    /**
     * @brief ticketClientMap
     * Maps the parkingStationId to the client that request an to enter in a parking station.
     * The mapping is valid only for the first message exchange (of each client) because after that
     * the client obtains a TicketID */
    map<int, SocketID> stationClientMap;

    /**
     * @brief ticketClientMap
     * Maps a TicketID to a client. The entry relative to a particular TicketID has to be removed after that
     * the client exit the parking station
     */
    map<int, SocketID> ticketClientMap;

    /**
     * @brief requestQueue
     * Shared memory between with the thread that sends to ignition, contains JSON Requests
     */
    Monitor<QString> *requestQueue;

    /**
     * @brief replyQueue
     * Shared memory between with the thread that receives from ignition, contains JSON Replies
     */
    Monitor<QString> *replyQueue;

    Server server;

};

#endif // SIMAGGREGATORSERVER_H
