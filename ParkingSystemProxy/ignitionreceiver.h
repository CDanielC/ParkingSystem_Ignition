#ifndef IGNITIONRECEIVER_H
#define IGNITIONRECEIVER_H
#include "monitor.h"


class IgnitionReceiver
{
public:
    IgnitionReceiver();

signals:

public slots:

private:
    /**
     * @brief replyQueue
     * Shared memory between with the thread that receives from ignition, contains JSON Replies
     */
    Monitor<QString> *replyQueue;

    Server server;

    /**
     * @brief client
     * Client that sends replies to the SimAggregatorServer
     */
    Client client;

};

#endif // IGNITIONRECEIVER_H
