#include "mainwindow.h"
#include "ui_mainwindow.h"

#include <iostream>       // std::cout
#include <thread>         // std::thread
#include <mutex>
#include <condition_variable>
#include "Monitor.h"
#include "server.h"
#include "client.h"
#include <string>
#include <QTcpSocket>
#include <qabstractsocket.h>

using namespace std;

mutex mutex_;
condition_variable cv;
bool ready = false;
Monitor<string> monitor;
QTcpSocket socket;

void foo()
{
    /*std::unique_lock<std::mutex> lck(mutex_);
    mutex_.lock();
    while (!ready) cv.wait(lck);
    cout<<"ciao"<<endl;
    mutex_.unlock();*/
    cout<<"prod"<<endl;
    monitor.addMessage("ciao\n");

}

void bar(int x)
{
    /*std::unique_lock<std::mutex> lck(mutex_);
    mutex_.lock();
    cout<<"kree"<<endl;
    ready = true;
    mutex_.unlock();
    cv.notify_all();*/
    cout<<"cons"<<endl;
    string message = monitor.getMessage();
    cout<<message<<endl;

}


MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::on_runBtn_clicked()
{
    char c;

    std::thread second(bar,0);  // spawn new thread that calls bar(0)
    std::thread first(foo);     // spawn new thread that calls foo()

    cout << "main, foo and bar now execute concurrently...\n";

    // synchronize threads:
    first.join();                // pauses until first finishes
    second.join();               // pauses until second finishes

    std::cout << "foo and bar completed.\n";


}

void MainWindow::on_socketBtn_clicked()
{
    server = new Server();
    server->init(50008);
    // while(server->waitConnections() == false) {}
    if(server->waitConnections()){
        server->acceptConnection();
        server->read();
    }

}

void MainWindow::on_clientBtn_clicked()
{
    Client client;
    client.start("127.0.0.1", 50008);
    cout<<"transfer"<<endl;
    client.startTransfer();
    cout<<"inviato"<<endl;
}
