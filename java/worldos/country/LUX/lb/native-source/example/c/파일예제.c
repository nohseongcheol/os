#include "예제규약.h"
int main(void) {
    const char Daten[]="C Fichier: lb 😀\n";
    int Fichier=ariichten_Fichier("c.txt",lies_schreiffäeg|없으면만들기|내용비우기,0600);
    if(Fichier<0)return 1;
    if(schreiwen_Fichier_Daten(Fichier,Daten,sizeof(Daten)-1)!=sizeof(Daten)-1)return 2;
    if(sichen_Fichier(Fichier,0,처음기준)!=0)return 3;
    char 읽은글[128]={0};int Längt_VALUE=파일자료읽기(Fichier,읽은글,sizeof(읽은글)-1);
    Clôture_Fichier(Fichier);
    if(Längt_VALUE!=sizeof(Daten)-1)return 4;
    for(int 수=0;수<Längt_VALUE;수++)if(Daten[수]!=읽은글[수])return 5;
    return 출력(읽은글);
}
