#include "예제규약.h"
#include <통신규약.h>
int main(int argument_COUNT,char **Argumenti) {
    if(argument_COUNT!=2)return Ispis("사용법: ./네트워크 UDP창구번호\n");
    unsigned port_VALUE=0;for(int 수=0;Argumenti[1][수];수++) {
        if(Argumenti[1][수]<'0'||Argumenti[1][수]>'9')return 2;
        port_VALUE=port_VALUE*10+Argumenti[1][수]-'0';if(port_VALUE>65535)return 2;
    }
    if(!port_VALUE)return 2;
    int završna_tačka=Create_završna_tačka(oblak_Porodica,전문통신,전문전송규약);if(završna_tačka<0)return 3;
    struct 인터넷통신주소 adresa={0};adresa.adresa_Porodica=oblak_Porodica;
    if(BIND_adresa(završna_tačka,(struct 통신주소 *)&adresa,sizeof(adresa))<0)return 4;
    adresa.broj_priključka=망차례짧은수(port_VALUE);adresa.internetska_adresa.adresa_VALUE=Mreža_cijeli_broj(0x0a000202);
    const char 전문[]="C UDP bs";
    if(자료전문보내기(završna_tačka,전문,sizeof(전문)-1,0,(struct 통신주소 *)&adresa,sizeof(adresa))!=sizeof(전문)-1)return 5;
    char odgovoriti[512];unsigned Pokreni=밀리초();int RECEIVED_COUNT;
    do {
        RECEIVED_COUNT=자료전문받기(završna_tačka,odgovoriti,sizeof(odgovoriti),0,0,0);
        if(RECEIVED_COUNT<0&&broj_greške!=다시시도오류)return 6;
    } while(RECEIVED_COUNT<0&&(unsigned)(밀리초()-Pokreni)<700);
    zatvoriti_fajl(završna_tačka);if(RECEIVED_COUNT!=sizeof(전문)-1)return 7;
    for(int 수=0;수<RECEIVED_COUNT;수++)if(전문[수]!=odgovoriti[수])return 8;
    return Ispis("C 네트워크 potvrditi: UDP bs\n");
}
