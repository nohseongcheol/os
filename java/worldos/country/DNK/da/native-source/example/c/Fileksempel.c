#include "예제규약.h"
int main(void) {
    const char data[]="C Fil: da 😀\n";
    int Fil=åben_fil("c.txt",læse_skrive|없으면만들기|afkorte_Indhold,0600);
    if(Fil<0)return 1;
    if(skrive_fil_data(Fil,data,sizeof(data)-1)!=sizeof(data)-1)return 2;
    if(søge_fil(Fil,0,처음기준)!=0)return 3;
    char 읽은글[128]={0};int varighed_VÆRDI=파일자료읽기(Fil,읽은글,sizeof(읽은글)-1);
    Luk_fil(Fil);
    if(varighed_VÆRDI!=sizeof(data)-1)return 4;
    for(int tal=0;tal<varighed_VÆRDI;tal++)if(data[tal]!=읽은글[tal])return 5;
    return Udgang(읽은글);
}
