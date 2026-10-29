#include "예제규약.h"
#include <통신규약.h>
int main(int argument_COUNT,char **Argumente) {
    if(argument_COUNT!=2)return Rezultat("사용법: ./네트워크 UDP창구번호\n");
    unsigned muta_VALUE=0;for(int 수=0;Argumente[1][수];수++) {
        if(Argumente[1][수]<'0'||Argumente[1][수]>'9')return 2;
        muta_VALUE=muta_VALUE*10+Argumente[1][수]-'0';if(muta_VALUE>65535)return 2;
    }
    if(!muta_VALUE)return 2;
    int participant=crea_participant(cloud_Familie,racord_diagramă_informații,diagramă_informații_protocol);if(participant<0)return 3;
    struct 인터넷통신주소 adresa={0};adresa.adresa_Familie=cloud_Familie;
    if(BIND_adresa(participant,(struct 통신주소 *)&adresa,sizeof(adresa))<0)return 4;
    adresa.număr_port=망차례짧은수(muta_VALUE);adresa.adresă_internet.adresa_VALUE=rețea_întreg(0x0a000202);
    const char diagramă_informații[]="C UDP ro";
    if(trimite_diagramă_informații_date(participant,diagramă_informații,sizeof(diagramă_informații)-1,0,(struct 통신주소 *)&adresa,sizeof(adresa))!=sizeof(diagramă_informații)-1)return 5;
    char replică[512];unsigned Pornește=밀리초();int RECEIVED_COUNT;
    do {
        RECEIVED_COUNT=primi_diagramă_informații_date(participant,replică,sizeof(replică),0,0,0);
        if(RECEIVED_COUNT<0&&număr_de_eroare!=다시시도오류)return 6;
    } while(RECEIVED_COUNT<0&&(unsigned)(밀리초()-Pornește)<700);
    închide_Fișier(participant);if(RECEIVED_COUNT!=sizeof(diagramă_informații)-1)return 7;
    for(int 수=0;수<RECEIVED_COUNT;수++)if(diagramă_informații[수]!=replică[수])return 8;
    return Rezultat("C 네트워크 verifica: UDP ro\n");
}
