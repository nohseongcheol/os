#include "예제규약.h"
int main(void) {
    const char podaci[]="C Datoteka: hrvatski 😀\n";
    int Datoteka=otvoreno_Datoteka("c.txt",읽고쓰기|없으면만들기|skratiti_Sadržaj,0600);
    if(Datoteka<0)return 1;
    if(zapisivanje_Datoteka_podaci(Datoteka,podaci,sizeof(podaci)-1)!=sizeof(podaci)-1)return 2;
    if(tražiti_Datoteka(Datoteka,0,처음기준)!=0)return 3;
    char 읽은글[128]={0};int 길이=파일자료읽기(Datoteka,읽은글,sizeof(읽은글)-1);
    Zatvori_Datoteka(Datoteka);
    if(길이!=sizeof(podaci)-1)return 4;
    for(int 수=0;수<길이;수++)if(podaci[수]!=읽은글[수])return 5;
    return Izlaz(읽은글);
}
