#include "socketid.h"

SocketID::SocketID()
{

}

quint32 SocketID::getIpAddress() const
{
    return ipAddress;
}

void SocketID::setIpAddress(const quint32 &value)
{
    ipAddress = value;
}

quint16 SocketID::getPort() const
{
    return port;
}

void SocketID::setPort(const quint16 &value)
{
    port = value;
}

