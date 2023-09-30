#include <stdio.h>
#include <thread>
#include "progressbar.hpp"
#include <vector>


using namespace std;

void run(char* cmd){
    system(cmd);
}

int main(int argc,char *argv[]){
    std::vector<std::thread> ThreadVector;
    printf("\n Making Thread for Upload\n");
    progressbar bar(argc);
    
    for(int i=1;i<argc;i++){
        char* cmd = argv[i];
        ThreadVector.emplace_back([&](){run(cmd);});
        bar.update();
    }
    printf("\n Execute the Threads \n");
    progressbar bar1(argc);
    for(auto& t:ThreadVector){
        t.join();
        bar1.update();
    }
    printf("\n Upload is complete \n");
    return 0;
}