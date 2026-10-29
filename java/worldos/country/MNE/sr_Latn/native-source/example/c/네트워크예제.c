#include "예제규약.h"
#include <통신규약.h>
int main(int argument_COUNT,char **인수) {
    if(argument_COUNT!=2)return 출력("사용법: ./네트워크 UDP창구번호\n");
    unsigned port_VALUE=0;for(int 수=0;인수[1][수];수++) {
        if(인수[1][수]<'0'||인수[1][수]>'9')return 2;
        port_VALUE=port_VALUE*10+인수[1][수]-'0';if(port_VALUE>65535)return 2;
    }
    if(!port_VALUE)return 2;
    int učesnik=Create_učesnik(oblak_Porodica,datagramski_priključak,datagram_protokol);if(učesnik<0)return 3;
    struct 인터넷통신주소 adresa={0};adresa.adresa_Porodica=oblak_Porodica;
    if(povezati_adresa(učesnik,(struct 통신주소 *)&adresa,sizeof(adresa))<0)return 4;
    adresa.broj_porta=망차례짧은수(port_VALUE);adresa.Internet_adresa.adresa_VALUE=Mreža_ceo_broj(0x0a000202);
    const char datagram[]="C UDP sr_Latn";
    if(poslati_datagram_podaci(učesnik,datagram,sizeof(datagram)-1,0,(struct 통신주소 *)&adresa,sizeof(adresa))!=sizeof(datagram)-1)return 5;
    char odgovor[512];unsigned koristiti=밀리초();int RECEIVED_COUNT;
    do {
        RECEIVED_COUNT=primiti_datagram_podaci(učesnik,odgovor,sizeof(odgovor),0,0,0);
        if(RECEIVED_COUNT<0&&broj_greške!=다시시도오류)return 6;
    } while(RECEIVED_COUNT<0&&(unsigned)(밀리초()-koristiti)<700);
    Zatvori_Datoteka(učesnik);if(RECEIVED_COUNT!=sizeof(datagram)-1)return 7;
    for(int 수=0;수<RECEIVED_COUNT;수++)if(datagram[수]!=odgovor[수])return 8;
    return 출력("C 네트워크 verifikovati: UDP sr_Latn\n");
}
