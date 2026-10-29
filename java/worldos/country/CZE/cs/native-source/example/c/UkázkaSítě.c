#include "예제규약.h"
#include <síť_ABI.h>
int main(int argument_POČET,char **argumenty) {
    if(argument_POČET!=2)return výstupní_pozice("사용법: ./네트워크 UDP창구번호\n");
    unsigned port_HODNOTA=0;for(int číslo=0;argumenty[1][číslo];číslo++) {
        if(argumenty[1][číslo]<'0'||argumenty[1][číslo]>'9')return 2;
        port_HODNOTA=port_HODNOTA*10+argumenty[1][číslo]-'0';if(port_HODNOTA>65535)return 2;
    }
    if(!port_HODNOTA)return 2;
    int účastník=Create_účastník(cloud_řada,datagramový_soket,datagram_protokol);if(účastník<0)return 3;
    struct cloud_soket_ODKAZ Adresa={0};Adresa.ODKAZ_řada=cloud_řada;
    if(vázat_ODKAZ(účastník,(struct soket_ODKAZ *)&Adresa,sizeof(Adresa))<0)return 4;
    Adresa.číslo_portu=망차례짧은수(port_HODNOTA);Adresa.internetová_adresa.ODKAZ_HODNOTA=síť_integer(0x0a000202);
    const char datagram[]="C UDP cs";
    if(poslat_datagram_data(účastník,datagram,sizeof(datagram)-1,0,(struct soket_ODKAZ *)&Adresa,sizeof(Adresa))!=sizeof(datagram)-1)return 5;
    char odezva[512];unsigned Spustit_2=밀리초();int RECEIVED_POČET;
    do {
        RECEIVED_POČET=dostat_datagram_data(účastník,odezva,sizeof(odezva),0,0,0);
        if(RECEIVED_POČET<0&&číslo_chyby!=다시시도오류)return 6;
    } while(RECEIVED_POČET<0&&(unsigned)(밀리초()-Spustit_2)<700);
    Zavřít_Soubor(účastník);if(RECEIVED_POČET!=sizeof(datagram)-1)return 7;
    for(int číslo=0;číslo<RECEIVED_POČET;číslo++)if(datagram[číslo]!=odezva[číslo])return 8;
    return výstupní_pozice("C 네트워크 ověřit: UDP cs\n");
}
