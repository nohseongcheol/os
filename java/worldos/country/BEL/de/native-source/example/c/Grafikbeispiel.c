#include "Beispielvertrag.h"
int main(void) {
    if(rechteckZeichnen(600,400,28,20,0x0000ff)<0)return 1;
    if(rechteckZeichnen(600,425,28,20,0x00ff00)<0)return 2;
    if(rechteckZeichnen(600,450,28,20,0xff0000)<0)return 3;
    Ausgabe("C 그래픽: RGB\nEnter\n");
    return fürZeichnungWarten()<0?4:0;
}
