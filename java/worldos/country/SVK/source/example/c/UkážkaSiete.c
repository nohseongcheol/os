#include "예제규약.h"
#include <통신규약.h>
int main(int argument_COUNT,char **Argumenty) {
    if(argument_COUNT!=2)return Výstup("사용법: ./네트워크 UDP창구번호\n");
    unsigned port_VALUE=0;for(int 수=0;Argumenty[1][수];수++) {
        if(Argumenty[1][수]<'0'||Argumenty[1][수]>'9')return 2;
        port_VALUE=port_VALUE*10+Argumenty[1][수]-'0';if(port_VALUE>65535)return 2;
    }
    if(!port_VALUE)return 2;
    int účastník=Create_účastník(cloud_séria,datagramový_soket,datagram_protokol);if(účastník<0)return 3;
    struct cloud_soket_adresa adresa={0};adresa.adresa_séria=cloud_séria;
    if(BIND_adresa(účastník,(struct soket_adresa *)&adresa,sizeof(adresa))<0)return 4;
    adresa.číslo_portu=망차례짧은수(port_VALUE);adresa.internetová_adresa.adresa_VALUE=sieť_celé_číslo(0x0a000202);
    const char datagram[]="C UDP Slovenský";
    if(odoslať_datagram_údaje(účastník,datagram,sizeof(datagram)-1,0,(struct soket_adresa *)&adresa,sizeof(adresa))!=sizeof(datagram)-1)return 5;
    char odozva[512];unsigned Spustiť_2=밀리초();int RECEIVED_COUNT;
    do {
        RECEIVED_COUNT=dostať_datagram_údaje(účastník,odozva,sizeof(odozva),0,0,0);
        if(RECEIVED_COUNT<0&&chybové_číslo!=다시시도오류)return 6;
    } while(RECEIVED_COUNT<0&&(unsigned)(밀리초()-Spustiť_2)<700);
    Zavrieť_Súbor(účastník);if(RECEIVED_COUNT!=sizeof(datagram)-1)return 7;
    for(int 수=0;수<RECEIVED_COUNT;수++)if(datagram[수]!=odozva[수])return 8;
    return Výstup("C 네트워크 overiť: UDP Slovenský\n");
}
