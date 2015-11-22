#ifndef MONITOR_H
#define MONITOR_H


#include <iostream>       // std::cout
#include <thread>         // std::thread
#include <mutex>
#include <condition_variable>
#include <string>
#include <queue>

using namespace std;

template <class T>
class Monitor{

    private:
            queue<T> elemQueue_;
            int count;
            mutex mutex_;
            condition_variable not_empty;
    public:

        inline Monitor(){
            count = 0;
        }


        inline void addMessage(T message){
            unique_lock<std::mutex> l(mutex_);
            elemQueue_.push(message);
            count++;
            not_empty.notify_one();
        }

        inline T getMessage(){
            unique_lock<std::mutex> l(mutex_);
            not_empty.wait(l, [this](){return count != 0; });
            T temp;
            temp = elemQueue_.front();
            elemQueue_.pop();
            count--;
            return temp;
        }


};
#endif // MONITOR_H
