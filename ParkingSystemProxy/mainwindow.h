#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include "server.h"

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();

private slots:
    void on_runBtn_clicked();

    void on_socketBtn_clicked();

    void on_clientBtn_clicked();

private:
    Ui::MainWindow *ui;
    Server *server;
};

#endif // MAINWINDOW_H
