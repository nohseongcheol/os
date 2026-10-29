#include "예제규약.h"
int main(void) {
    const char údaje[]="C Súbor: Slovenský 😀\n";
    int Súbor=otvoriť_Súbor("c.txt",na_čítanie_a_zapisovanie|없으면만들기|skrátiť_Obsah,0600);
    if(Súbor<0)return 1;
    if(zapísať_Súbor_údaje(Súbor,údaje,sizeof(údaje)-1)!=sizeof(údaje)-1)return 2;
    if(hľadať_Súbor(Súbor,0,처음기준)!=0)return 3;
    char 읽은글[128]={0};int dĺžka_VALUE=파일자료읽기(Súbor,읽은글,sizeof(읽은글)-1);
    Zavrieť_Súbor(Súbor);
    if(dĺžka_VALUE!=sizeof(údaje)-1)return 4;
    for(int 수=0;수<dĺžka_VALUE;수++)if(údaje[수]!=읽은글[수])return 5;
    return Výstup(읽은글);
}
