#include "예제규약.h"
#include <통신규약.h>
int main(int argument_AANTAL,char **argumenten) {
    if(argument_AANTAL!=2)return tekstuitvoer("사용법: ./네트워크 UDP창구번호\n");
    unsigned poort_WAARDE=0;for(int nummer=0;argumenten[1][nummer];nummer++) {
        if(argumenten[1][nummer]<'0'||argumenten[1][nummer]>'9')return 2;
        poort_WAARDE=poort_WAARDE*10+argumenten[1][nummer]-'0';if(poort_WAARDE>65535)return 2;
    }
    if(!poort_WAARDE)return 2;
    int eindpunt=maken_eindpunt(mesh_Gezin,datagramsocket,datagram_protocol);if(eindpunt<0)return 3;
    struct mesh_socket_ADRES ADRES={0};ADRES.ADRES_Gezin=mesh_Gezin;
    if(BIND_ADRES(eindpunt,(struct socket_ADRES *)&ADRES,sizeof(ADRES))<0)return 4;
    ADRES.poortnummer=망차례짧은수(poort_WAARDE);ADRES.internetadres.ADRES_WAARDE=net_geheel_getal(0x0a000202);
    const char datagram[]="C UDP Nederlands";
    if(e_mailen_datagram_gegevens(eindpunt,datagram,sizeof(datagram)-1,0,(struct socket_ADRES *)&ADRES,sizeof(ADRES))!=sizeof(datagram)-1)return 5;
    char reactie[512];unsigned starten=밀리초();int OPBRENGST_AANTAL;
    do {
        OPBRENGST_AANTAL=ontvangen_datagram_gegevens(eindpunt,reactie,sizeof(reactie),0,0,0);
        if(OPBRENGST_AANTAL<0&&foutnummer!=다시시도오류)return 6;
    } while(OPBRENGST_AANTAL<0&&(unsigned)(밀리초()-starten)<700);
    Sluiten_Bestand(eindpunt);if(OPBRENGST_AANTAL!=sizeof(datagram)-1)return 7;
    for(int nummer=0;nummer<OPBRENGST_AANTAL;nummer++)if(datagram[nummer]!=reactie[nummer])return 8;
    return tekstuitvoer("C 네트워크 bevestigen: UDP Nederlands\n");
}
