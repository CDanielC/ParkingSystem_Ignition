#-------------------------------------------------
#
# Project created by QtCreator 2015-11-22T18:00:01
#
#-------------------------------------------------

QT       += core gui
QT	 += network

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = ParkingSystemProxy
TEMPLATE = app


SOURCES += main.cpp\
        mainwindow.cpp \
    server.cpp \
    client.cpp \
    simaggregatorserver.cpp \
    socketid.cpp \
    ignitionsender.cpp \
    ignitionreceiver.cpp

HEADERS  += mainwindow.h \
    monitor.h \
    server.h \
    client.h \
    simaggregatorserver.h \
    socketid.h \
    ignitionsender.h \
    ignitionreceiver.h

FORMS    += mainwindow.ui
