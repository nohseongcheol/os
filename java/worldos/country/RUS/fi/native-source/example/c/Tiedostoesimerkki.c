#include "예제규약.h"
int main(void) {
    const char data[]="C tiedoston_nimi: fi 😀\n";
    int tiedoston_nimi=avata_Tiedosto("c.txt",luku_ja_kirjoitus|없으면만들기|내용비우기,0600);
    if(tiedoston_nimi<0)return 1;
    if(kirjoitus_Tiedosto_data(tiedoston_nimi,data,sizeof(data)-1)!=sizeof(data)-1)return 2;
    if(hae_Tiedosto(tiedoston_nimi,0,처음기준)!=0)return 3;
    char lukea_SMS_ARVO[128]={0};int kesto_ARVO=lukea_Tiedosto_data(tiedoston_nimi,lukea_SMS_ARVO,sizeof(lukea_SMS_ARVO)-1);
    Sulje_Tiedosto(tiedoston_nimi);
    if(kesto_ARVO!=sizeof(data)-1)return 4;
    for(int numero=0;numero<kesto_ARVO;numero++)if(data[numero]!=lukea_SMS_ARVO[numero])return 5;
    return tulostuspaikka(lukea_SMS_ARVO);
}
