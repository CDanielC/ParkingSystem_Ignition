#include "server.h"
#include <iostream>
#include <string>

using namespace std;

Server::Server(QObject* parent): QObject(parent)
{

}

void Server::init(unsigned int port){
    connect(&server, SIGNAL(newConnection()), this, SLOT(acceptConnection()));
    cout<<"port "<<port<<endl;
    server.listen(QHostAddress::Any, port);
}

Server::~Server()
{
    server.close();
}

void Server::acceptConnection()
{
    client = server.nextPendingConnection();

    connect(client, SIGNAL(readyRead()), this, SLOT(readAndClose()));
}

bool Server::waitConnections()
{
    //cout<<server.hasPendingConnections()<<endl;
    return server.hasPendingConnections();
}

QString Server::read()
{
    char buffer[1024] = {0};
    client->read(buffer, client->bytesAvailable());
    cout<<client->localAddress().toIPv4Address()<<endl;
    cout<<client->localAddress().toString().toStdString()<<endl;
    cout<<client->localPort()<<endl;
    QString str(buffer);
    cout<<str.toStdString()<<endl;
    return str;
}

void Server::readAndClose()
{
    cout<<"read and close ;"<<endl;
    char buffer[1024] = {0};
    client->read(buffer, client->bytesAvailable());
    cout<<client->localAddress().toIPv4Address()<<endl;
    cout<<client->localAddress().toString().toStdString()<<endl;
    cout<<client->localPort()<<endl;
    cout<<buffer<<endl;
    client->close();

}
