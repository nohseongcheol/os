#include "예제규약.h"
#include <통신규약.h>
int main(int argument_ANTAL,char **argument) {
    if(argument_ANTAL!=2)return utmatningsposition("사용법: ./네트워크 UDP창구번호\n");
    unsigned port_värde=0;for(int nummer=0;argument[1][nummer];nummer++) {
        if(argument[1][nummer]<'0'||argument[1][nummer]>'9')return 2;
        port_värde=port_värde*10+argument[1][nummer]-'0';if(port_värde>65535)return 2;
    }
    if(!port_värde)return 2;
    int deltagare=Skapa_deltagare(nät_serie,datagramsocket,datagram_protokoll);if(deltagare<0)return 3;
    struct nät_socket_ADRESS Adress={0};Adress.ADRESS_serie=nät_serie;
    if(BIND_ADRESS(deltagare,(struct socket_ADRESS *)&Adress,sizeof(Adress))<0)return 4;
    Adress.portnummer=망차례짧은수(port_värde);Adress.Internetadress.ADRESS_värde=nätverk_heltal(0x0a000202);
    const char datagram[]="C UDP sv";
    if(skicka_datagram_data(deltagare,datagram,sizeof(datagram)-1,0,(struct socket_ADRESS *)&Adress,sizeof(Adress))!=sizeof(datagram)-1)return 5;
    char svara[512];unsigned Kör=밀리초();int BELOPP_ANTAL;
    do {
        BELOPP_ANTAL=få_datagram_data(deltagare,svara,sizeof(svara),0,0,0);
        if(BELOPP_ANTAL<0&&felnummer!=다시시도오류)return 6;
    } while(BELOPP_ANTAL<0&&(unsigned)(밀리초()-Kör)<700);
    Stäng_fil(deltagare);if(BELOPP_ANTAL!=sizeof(datagram)-1)return 7;
    for(int nummer=0;nummer<BELOPP_ANTAL;nummer++)if(datagram[nummer]!=svara[nummer])return 8;
    return utmatningsposition("C 네트워크 verifiera: UDP sv\n");
}
