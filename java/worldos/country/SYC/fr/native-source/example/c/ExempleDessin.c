#include "ContratExemple.h"
int main(void) {
    if(dessinerRectangle(600,400,28,20,0x0000ff)<0)return 1;
    if(dessinerRectangle(600,425,28,20,0x00ff00)<0)return 2;
    if(dessinerRectangle(600,450,28,20,0xff0000)<0)return 3;
    Sortie("C 그래픽: RGB\nEnter\n");
    return attendreDessinPour()<0?4:0;
}
