#include "예제규약.h"
int main(void) {
    if(rysować_prostokąt(600,400,28,20,0x0000ff)<0)return 1;
    if(rysować_prostokąt(600,425,28,20,0x00ff00)<0)return 2;
    if(rysować_prostokąt(600,450,28,20,0xff0000)<0)return 3;
    pozycja_wyjścia("C 그래픽: RGB\nEnter\n");
    return 그림기다리기()<0?4:0;
}
