#include "예제규약.h"
int main(void) {
    if(Desen_dreptunghi(600,400,28,20,0x0000ff)<0)return 1;
    if(Desen_dreptunghi(600,425,28,20,0x00ff00)<0)return 2;
    if(Desen_dreptunghi(600,450,28,20,0xff0000)<0)return 3;
    Rezultat("C 그래픽: RGB\nEnter\n");
    return 그림기다리기()<0?4:0;
}
