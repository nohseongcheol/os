#include "예제규약.h"
#include <통신규약.h>
int main(int argument_COUNT,char **Argumenti) {
    if(argument_COUNT!=2)return Izpis("사용법: ./네트워크 UDP창구번호\n");
    unsigned vrata_VALUE=0;for(int 수=0;Argumenti[1][수];수++) {
        if(Argumenti[1][수]<'0'||Argumenti[1][수]>'9')return 2;
        vrata_VALUE=vrata_VALUE*10+Argumenti[1][수]-'0';if(vrata_VALUE>65535)return 2;
    }
    if(!vrata_VALUE)return 2;
    int končna_točka=Ustvari_končna_točka(oblak_Družina,vtičnica_za_prenos_datagramov,datagram_protokol);if(končna_točka<0)return 3;
    struct oblak_vtičnica_naslov naslov={0};naslov.naslov_Družina=oblak_Družina;
    if(BIND_naslov(končna_točka,(struct vtičnica_naslov *)&naslov,sizeof(naslov))<0)return 4;
    naslov.številka_vrat=망차례짧은수(vrata_VALUE);naslov.internetni_račun.naslov_VALUE=mreža_celo_število(0x0a000202);
    const char datagram[]="C UDP sl";
    if(poslati_datagram_podatki(končna_točka,datagram,sizeof(datagram)-1,0,(struct vtičnica_naslov *)&naslov,sizeof(naslov))!=sizeof(datagram)-1)return 5;
    char odgovor[512];unsigned Zaženi=밀리초();int RECEIVED_COUNT;
    do {
        RECEIVED_COUNT=sprejeti_sprejemati_prejeti_prejemati_datagram_podatki(končna_točka,odgovor,sizeof(odgovor),0,0,0);
        if(RECEIVED_COUNT<0&&številka_napake!=다시시도오류)return 6;
    } while(RECEIVED_COUNT<0&&(unsigned)(밀리초()-Zaženi)<700);
    Zapri_Datoteka(končna_točka);if(RECEIVED_COUNT!=sizeof(datagram)-1)return 7;
    for(int 수=0;수<RECEIVED_COUNT;수++)if(datagram[수]!=odgovor[수])return 8;
    return Izpis("C 네트워크 확인: UDP sl\n");
}
