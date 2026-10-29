#include "예제규약.h"
int main(void) {
    const char podatki[]="C Datoteka: sl 😀\n";
    int Datoteka=odprto_Datoteka("c.txt",branje_pisanje|없으면만들기|내용비우기,0600);
    if(Datoteka<0)return 1;
    if(pisati_Datoteka_podatki(Datoteka,podatki,sizeof(podatki)-1)!=sizeof(podatki)-1)return 2;
    if(iskati_Datoteka(Datoteka,0,처음기준)!=0)return 3;
    char 읽은글[128]={0};int 길이=파일자료읽기(Datoteka,읽은글,sizeof(읽은글)-1);
    Zapri_Datoteka(Datoteka);
    if(길이!=sizeof(podatki)-1)return 4;
    for(int 수=0;수<길이;수++)if(podatki[수]!=읽은글[수])return 5;
    return Izpis(읽은글);
}
