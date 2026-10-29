#include "예제규약.h"
#include <통신규약.h>
int main(int argument_ANTALL,char **Argumenter) {
    if(argument_ANTALL!=2)return Utgang("사용법: ./네트워크 UDP창구번호\n");
    unsigned port_VERDI=0;for(int nummer=0;Argumenter[1][nummer];nummer++) {
        if(Argumenter[1][nummer]<'0'||Argumenter[1][nummer]>'9')return 2;
        port_VERDI=port_VERDI*10+Argumenter[1][nummer]-'0';if(port_VERDI>65535)return 2;
    }
    if(!port_VERDI)return 2;
    int deltaker=åpne_deltaker(sky_serie,datagramsocket,datagram_protokoll);if(deltaker<0)return 3;
    struct sky_socket_e_post e_post={0};e_post.e_post_serie=sky_serie;
    if(BIND_e_post(deltaker,(struct socket_e_post *)&e_post,sizeof(e_post))<0)return 4;
    e_post.portnummer=망차례짧은수(port_VERDI);e_post.Internett_adresse.e_post_VERDI=nettverk_heltall(0x0a000202);
    const char datagram[]="C UDP Norwegian Bokmål";
    if(sende_datagram_data(deltaker,datagram,sizeof(datagram)-1,0,(struct socket_e_post *)&e_post,sizeof(e_post))!=sizeof(datagram)-1)return 5;
    char svar[512];unsigned Kjør_2=밀리초();int MOTTATT_AVKAST_ANTALL;
    do {
        MOTTATT_AVKAST_ANTALL=motta_datagram_data(deltaker,svar,sizeof(svar),0,0,0);
        if(MOTTATT_AVKAST_ANTALL<0&&feilnummer!=다시시도오류)return 6;
    } while(MOTTATT_AVKAST_ANTALL<0&&(unsigned)(밀리초()-Kjør_2)<700);
    Lukk_Fil(deltaker);if(MOTTATT_AVKAST_ANTALL!=sizeof(datagram)-1)return 7;
    for(int nummer=0;nummer<MOTTATT_AVKAST_ANTALL;nummer++)if(datagram[nummer]!=svar[nummer])return 8;
    return Utgang("C 네트워크 bekrefte: UDP Norwegian Bokmål\n");
}
