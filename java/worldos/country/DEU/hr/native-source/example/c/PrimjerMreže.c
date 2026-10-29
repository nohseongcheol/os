#include "예제규약.h"
#include <통신규약.h>
int main(int argument_COUNT,char **Argumenti) {
    if(argument_COUNT!=2)return Izlaz("사용법: ./네트워크 UDP창구번호\n");
    unsigned prebaciti_VALUE=0;for(int 수=0;Argumenti[1][수];수++) {
        if(Argumenti[1][수]<'0'||Argumenti[1][수]>'9')return 2;
        prebaciti_VALUE=prebaciti_VALUE*10+Argumenti[1][수]-'0';if(prebaciti_VALUE>65535)return 2;
    }
    if(!prebaciti_VALUE)return 2;
    int sudionik=Create_sudionik(oblak_linija,datogramska_utičnica,datogram_protokol);if(sudionik<0)return 3;
    struct 인터넷통신주소 adresa={0};adresa.adresa_linija=oblak_linija;
    if(BIND_adresa(sudionik,(struct 통신주소 *)&adresa,sizeof(adresa))<0)return 4;
    adresa.broj_priključka=망차례짧은수(prebaciti_VALUE);adresa.internetska_adresa.adresa_VALUE=mreža_cijeli_broj(0x0a000202);
    const char datogram[]="C UDP hr";
    if(slati_datogram_podaci(sudionik,datogram,sizeof(datogram)-1,0,(struct 통신주소 *)&adresa,sizeof(adresa))!=sizeof(datogram)-1)return 5;
    char odgovor[512];unsigned Pokreni=밀리초();int RECEIVED_COUNT;
    do {
        RECEIVED_COUNT=primiti_datogram_podaci(sudionik,odgovor,sizeof(odgovor),0,0,0);
        if(RECEIVED_COUNT<0&&broj_pogreške!=다시시도오류)return 6;
    } while(RECEIVED_COUNT<0&&(unsigned)(밀리초()-Pokreni)<700);
    Zatvori_Datoteka(sudionik);if(RECEIVED_COUNT!=sizeof(datogram)-1)return 7;
    for(int 수=0;수<RECEIVED_COUNT;수++)if(datogram[수]!=odgovor[수])return 8;
    return Izlaz("C 네트워크 provjeriti: UDP hr\n");
}
