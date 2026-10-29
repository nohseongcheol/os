#include "예제규약.h"
int main(void) {
    const char date[]="C Fișier: ro 😀\n";
    int Fișier=crea_Fișier("c.txt",citire_scriere|없으면만들기|trunchia_TOC,0600);
    if(Fișier<0)return 1;
    if(scriere_Fișier_date(Fișier,date,sizeof(date)-1)!=sizeof(date)-1)return 2;
    if(căuta_Fișier(Fișier,0,처음기준)!=0)return 3;
    char 읽은글[128]={0};int lungime_VALUE=파일자료읽기(Fișier,읽은글,sizeof(읽은글)-1);
    închide_Fișier(Fișier);
    if(lungime_VALUE!=sizeof(date)-1)return 4;
    for(int 수=0;수<lungime_VALUE;수++)if(date[수]!=읽은글[수])return 5;
    return Rezultat(읽은글);
}
