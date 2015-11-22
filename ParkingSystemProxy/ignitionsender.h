#ifndef IGNITIONSENDER_H
#define IGNITIONSENDER_H
#include "monitor.h"


class IgnitionSender
{
public:
    IgnitionSender();

signals:

public slots:

private:
    /**
     * @brief requestQueue
     * Shared memory between with the thread that sends to ignition, contains JSON Requests
     */
    Monitor<QString> *requestQueue;

    Server server;
};

#endif // IGNITIONSENDER_H
