#include "예제규약.h"
int main(void) {
    if(Lukis_segi_empat_tepat(600,400,28,20,0x0000ff)<0)return 1;
    if(Lukis_segi_empat_tepat(600,425,28,20,0x00ff00)<0)return 2;
    if(Lukis_segi_empat_tepat(600,450,28,20,0xff0000)<0)return 3;
    출력("C 그래픽: RGB\nEnter\n");
    return 그림기다리기()<0?4:0;
}
