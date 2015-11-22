#ifndef SOCKETID_H
#define SOCKETID_H


class SocketID
{
public:
    SocketID();

    quint32 getIpAddress() const;
    void setIpAddress(const quint32 &value);

    quint16 getPort() const;
    void setPort(const quint16 &value);

private:
    quint32 ipAddress;
    quint16 port;
};

#endif // SOCKETID_H
