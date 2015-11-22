#ifndef SERVER_H
#define SERVER_H


#include <QtNetwork>
#include <QObject>
#include <QTcpServer>
#include <QTcpSocket>
#include <QString>

class Server: public QObject
{
    Q_OBJECT

    public:
        Server(QObject * parent = 0);
        ~Server();
        void init(unsigned int port);
public slots:
        void acceptConnection();
        bool waitConnections();
        QString read();
        void readAndClose();

    private:
        QTcpServer server;
        QTcpSocket* client;
};


#endif // SERVER_H
