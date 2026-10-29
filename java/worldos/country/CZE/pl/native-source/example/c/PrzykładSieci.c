#include "예제규약.h"
#include <sieć_ABI.h>
int main(int argument_ILE_LICZB,char **argumenty) {
    if(argument_ILE_LICZB!=2)return pozycja_wyjścia("사용법: ./네트워크 UDP창구번호\n");
    unsigned port_WARTOŚĆ=0;for(int identyfikator=0;argumenty[1][identyfikator];identyfikator++) {
        if(argumenty[1][identyfikator]<'0'||argumenty[1][identyfikator]>'9')return 2;
        port_WARTOŚĆ=port_WARTOŚĆ*10+argumenty[1][identyfikator]-'0';if(port_WARTOŚĆ>65535)return 2;
    }
    if(!port_WARTOŚĆ)return 2;
    int uczestnik=Twórca_uczestnik(chmura_Rodzina,gniazdo_do_przesyłania_datagramów,datagram_protokół);if(uczestnik<0)return 3;
    struct chmura_gniazdo_ADRES Adres={0};Adres.ADRES_Rodzina=chmura_Rodzina;
    if(BIND_ADRES(uczestnik,(struct gniazdo_ADRES *)&Adres,sizeof(Adres))<0)return 4;
    Adres.numer_portu=망차례짧은수(port_WARTOŚĆ);Adres.adres_internetowy.ADRES_WARTOŚĆ=sieć_liczba_całkowita(0x0a000202);
    const char datagram[]="C UDP pl";
    if(wysłać_datagram_dane(uczestnik,datagram,sizeof(datagram)-1,0,(struct gniazdo_ADRES *)&Adres,sizeof(Adres))!=sizeof(datagram)-1)return 5;
    char odpowiedź[512];unsigned Uruchom_2=밀리초();int KWOTA_WYKUP_ILE_LICZB;
    do {
        KWOTA_WYKUP_ILE_LICZB=odbierać_datagram_dane(uczestnik,odpowiedź,sizeof(odpowiedź),0,0,0);
        if(KWOTA_WYKUP_ILE_LICZB<0&&numer_błędu!=다시시도오류)return 6;
    } while(KWOTA_WYKUP_ILE_LICZB<0&&(unsigned)(밀리초()-Uruchom_2)<700);
    Zamknij_Plik(uczestnik);if(KWOTA_WYKUP_ILE_LICZB!=sizeof(datagram)-1)return 7;
    for(int identyfikator=0;identyfikator<KWOTA_WYKUP_ILE_LICZB;identyfikator++)if(datagram[identyfikator]!=odpowiedź[identyfikator])return 8;
    return pozycja_wyjścia("C 네트워크 확인: UDP pl\n");
}
