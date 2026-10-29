#include "예제규약.h"
int main(void) {
    const char adat[]="C Fájl: magyar 😀\n";
    int Fájl=készít_Fájl("c.txt",읽고쓰기|없으면만들기|vág_Tartalom,0600);
    if(Fájl<0)return 1;
    if(ír_Fájl_adat(Fájl,adat,sizeof(adat)-1)!=sizeof(adat)-1)return 2;
    if(keres_Fájl(Fájl,0,처음기준)!=0)return 3;
    char 읽은글[128]={0};int hossz_ÉRTÉK=파일자료읽기(Fájl,읽은글,sizeof(읽은글)-1);
    bezár_Fájl(Fájl);
    if(hossz_ÉRTÉK!=sizeof(adat)-1)return 4;
    for(int szám=0;szám<hossz_ÉRTÉK;szám++)if(adat[szám]!=읽은글[szám])return 5;
    return Kimenet(읽은글);
}
