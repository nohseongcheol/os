#include "예제규약.h"
#include <통신규약.h>
int main(int argument_TÆL,char **Argumenter) {
    if(argument_TÆL!=2)return Udgang("사용법: ./네트워크 UDP창구번호\n");
    unsigned port_VÆRDI=0;for(int tal=0;Argumenter[1][tal];tal++) {
        if(Argumenter[1][tal]<'0'||Argumenter[1][tal]>'9')return 2;
        port_VÆRDI=port_VÆRDI*10+Argumenter[1][tal]-'0';if(port_VÆRDI>65535)return 2;
    }
    if(!port_VÆRDI)return 2;
    int slutpunkt=åbne_slutpunkt(net_serie,datagram_socket,datagram_protokol);if(slutpunkt<0)return 3;
    struct net_socket_mail mail={0};mail.mail_serie=net_serie;
    if(BIND_mail(slutpunkt,(struct socket_mail *)&mail,sizeof(mail))<0)return 4;
    mail.portnummer=망차례짧은수(port_VÆRDI);mail.internetadresse.mail_VÆRDI=netværk_heltal(0x0a000202);
    const char datagram[]="C UDP da";
    if(maile_datagram_data(slutpunkt,datagram,sizeof(datagram)-1,0,(struct socket_mail *)&mail,sizeof(mail))!=sizeof(datagram)-1)return 5;
    char svar[512];unsigned Kør_2=밀리초();int MODTAGET_VED_UDLØB_TÆL;
    do {
        MODTAGET_VED_UDLØB_TÆL=modtage_datagram_data(slutpunkt,svar,sizeof(svar),0,0,0);
        if(MODTAGET_VED_UDLØB_TÆL<0&&fejlnummer!=다시시도오류)return 6;
    } while(MODTAGET_VED_UDLØB_TÆL<0&&(unsigned)(밀리초()-Kør_2)<700);
    Luk_fil(slutpunkt);if(MODTAGET_VED_UDLØB_TÆL!=sizeof(datagram)-1)return 7;
    for(int tal=0;tal<MODTAGET_VED_UDLØB_TÆL;tal++)if(datagram[tal]!=svar[tal])return 8;
    return Udgang("C 네트워크 bekræfte: UDP da\n");
}
