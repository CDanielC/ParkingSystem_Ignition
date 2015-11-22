#include "client.h"

#include "client.h"
#include <QHostAddress>

Client::Client(QObject* parent): QObject(parent)
{
    connect(&client, SIGNAL(connected()), this, SLOT(startTransfer()));
}

Client::~Client()
{
    client.close();
}

void Client::start(QString address, quint16 port)
{
    QHostAddress addr(address);
    client.connectToHost(addr, port);
}

void Client::startTransfer()
{
    QString str = "kreeee";

    QByteArray block;
    QDataStream out(&block, QIODevice::WriteOnly);

    // writeRawData important!!! send to different encoded socket platform!!
    out.writeRawData(str.toStdString().c_str(), str.length());

    client.write(block, 10);
}
