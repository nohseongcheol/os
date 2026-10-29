#include "../명명/기계연결이름.h"
/* Preserve the deterministic Java loopback endpoints; route external IPv4 to lwIP. */
#include "sieć_Stos.h"
extern int32_t 되돌림전문만들기(int32_t,int32_t,int32_t), 되돌림전문묶기(int32_t,int32_t,int32_t);
extern int32_t 되돌림전문보내기(int32_t,int32_t,int32_t,int32_t), 되돌림전문받기(int32_t,int32_t);
extern int32_t 되돌림전문접속번호(int32_t), 되돌림전문주소(int32_t), 되돌림전문상대(int32_t), 되돌림전문닫기(int32_t);
extern int32_t 자바전문넣기(int32_t,int32_t),자바전문얻기(int32_t);
extern int32_t 되돌림흐름만들기(void),되돌림흐름묶기(int32_t,int32_t,int32_t),되돌림흐름듣기(int32_t,int32_t);
extern int32_t 되돌림흐름연결(int32_t,int32_t,int32_t),되돌림흐름연결받기(int32_t),되돌림흐름읽기(int32_t,int32_t),되돌림흐름쓰기(int32_t,int32_t);
extern int32_t 되돌림흐름접속번호(int32_t),되돌림흐름상대(int32_t),되돌림흐름닫기(int32_t);
static int zewnętrzny[24];
static int 임의주소[24], 양쪽수신창구[24], UDP_zewnętrzny_węzeł_równorzędny[8], granica_ADRES[8];
static int zewnętrzny_identyfikator(int dojście_do_pliku) { return dojście_do_pliku>=32 && dojście_do_pliku<56 ? zewnętrzny[dojście_do_pliku-32]-1 : -1; }
static int wkleić_SMS(int dojście_do_pliku,int TYP_obszar) {
    if(dojście_do_pliku<32||dojście_do_pliku>=56)return -9;int Wstecz_towar=zewnętrzny_identyfikator(dojście_do_pliku);if(Wstecz_towar>=0)return Wstecz_towar;
    int towar_ILE_LICZB=Twórca_gniazdo_uczestnik(TYP_obszar);if(towar_ILE_LICZB>=0)zewnętrzny[dojście_do_pliku-32]=towar_ILE_LICZB+1;return towar_ILE_LICZB;
}
int32_t 자바전문만들기(int32_t 첫째값,int32_t SEKUNDA_WARTOŚĆ,int32_t kod_znaku){return 되돌림전문만들기(첫째값,SEKUNDA_WARTOŚĆ,kod_znaku);}
int32_t 자바전문묶기(int32_t dojście_do_pliku,int32_t adres_internetowy,int32_t numer_portu){
    if(adres_internetowy==0x7f000001)return 되돌림전문묶기(dojście_do_pliku,adres_internetowy,numer_portu);
    if(adres_internetowy!=0&&adres_internetowy!=망상태읽기(0,0))return -99;
    int 반환값=되돌림전문묶기(dojście_do_pliku,0,numer_portu);if(반환값<0)return 반환값;
    int towar_ILE_LICZB=wkleić_SMS(dojście_do_pliku,2);if(towar_ILE_LICZB<0)return towar_ILE_LICZB;반환값=NET_BIND(towar_ILE_LICZB,망상태읽기(0,0),되돌림전문접속번호(dojście_do_pliku));if(!반환값)granica_ADRES[dojście_do_pliku-32]=adres_internetowy;return 반환값;
}
int32_t 자바전문보내기(int32_t dojście_do_pliku,int32_t adres_internetowy,int32_t numer_portu,int32_t Rozmiar){
    if(adres_internetowy==0x7f000001)return 되돌림전문보내기(dojście_do_pliku,adres_internetowy,numer_portu,Rozmiar);
    if(Rozmiar<0||Rozmiar>512)return -90;if(numer_portu<1||numer_portu>65535)return -22;
    if(되돌림전문접속번호(dojście_do_pliku)<0)return -9;
    if(되돌림전문주소(dojście_do_pliku)==0x7f000001)return -101;
    int towar_ILE_LICZB=zewnętrzny_identyfikator(dojście_do_pliku);if(towar_ILE_LICZB<0){int 반환값=0;if(되돌림전문접속번호(dojście_do_pliku)==0)반환값=되돌림전문묶기(dojście_do_pliku,0,0);if(반환값<0)return 반환값;towar_ILE_LICZB=wkleić_SMS(dojście_do_pliku,2);if(towar_ILE_LICZB<0)return towar_ILE_LICZB;반환값=NET_BIND(towar_ILE_LICZB,망상태읽기(0,0),되돌림전문접속번호(dojście_do_pliku));if(반환값<0)return 반환값;}
    unsigned char dane[512];for(int 순번=0;순번<Rozmiar;순번++)dane[순번]=자바전문얻기(순번);return wysłać_datagram(towar_ILE_LICZB,dane,Rozmiar,adres_internetowy,numer_portu);
}
int32_t 자바전문받기(int32_t dojście_do_pliku,int32_t Rozmiar){
    int towar_ILE_LICZB=zewnętrzny_identyfikator(dojście_do_pliku);if(towar_ILE_LICZB<0)return 되돌림전문받기(dojście_do_pliku,Rozmiar);if(Rozmiar<0||Rozmiar>512)return -22;
    int lokalny=되돌림전문받기(dojście_do_pliku,Rozmiar);if(lokalny!=-11){UDP_zewnętrzny_węzeł_równorzędny[dojście_do_pliku-32]=0;return lokalny;}
    unsigned char dane[512];int 반환값=odbierać_datagram(towar_ILE_LICZB,dane,Rozmiar);if(반환값>=0)UDP_zewnętrzny_węzeł_równorzędny[dojście_do_pliku-32]=1;for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,dane[순번]);return 반환값;
}
int32_t 자바전문접속번호(int32_t dojście_do_pliku){int towar_ILE_LICZB=zewnętrzny_identyfikator(dojście_do_pliku);return towar_ILE_LICZB<0?되돌림전문접속번호(dojście_do_pliku):(int32_t)sieć_numer_portu(towar_ILE_LICZB);}
int32_t 자바전문주소(int32_t dojście_do_pliku){return zewnętrzny_identyfikator(dojście_do_pliku)<0?되돌림전문주소(dojście_do_pliku):granica_ADRES[dojście_do_pliku-32];}
int32_t 자바전문상대(int32_t dojście_do_pliku){int towar_ILE_LICZB=zewnętrzny_identyfikator(dojście_do_pliku);return towar_ILE_LICZB<0||!UDP_zewnętrzny_węzeł_równorzędny[dojście_do_pliku-32]?되돌림전문상대(dojście_do_pliku):(int32_t)węzeł_równorzędny_numer_portu(towar_ILE_LICZB);}
int32_t 자바전문원격주소(int32_t dojście_do_pliku){int towar_ILE_LICZB=zewnętrzny_identyfikator(dojście_do_pliku);return towar_ILE_LICZB<0||!UDP_zewnętrzny_węzeł_równorzędny[dojście_do_pliku-32]?0x7f000001:(int32_t)NET_węzeł_równorzędny_ADRES(towar_ILE_LICZB);}
int32_t 자바전문닫기(int32_t dojście_do_pliku){int towar_ILE_LICZB=zewnętrzny_identyfikator(dojście_do_pliku);if(towar_ILE_LICZB>=0){Zamknij_sieć(towar_ILE_LICZB);zewnętrzny[dojście_do_pliku-32]=0;}if(dojście_do_pliku>=32&&dojście_do_pliku<40)UDP_zewnętrzny_węzeł_równorzędny[dojście_do_pliku-32]=granica_ADRES[dojście_do_pliku-32]=0;return 되돌림전문닫기(dojście_do_pliku);}
int32_t 자바흐름만들기(void){return 되돌림흐름만들기();}
int32_t 자바흐름묶기(int32_t dojście_do_pliku,int32_t adres_internetowy,int32_t numer_portu){
    if(adres_internetowy==0||adres_internetowy==0x7f000001){int 반환값=되돌림흐름묶기(dojście_do_pliku,adres_internetowy,numer_portu);if(!반환값)임의주소[dojście_do_pliku-32]=adres_internetowy==0;return 반환값;}
    if(adres_internetowy!=망상태읽기(0,0))return -99;int 반환값=되돌림흐름묶기(dojście_do_pliku,0,numer_portu);if(반환값<0)return 반환값;
    int towar_ILE_LICZB=wkleić_SMS(dojście_do_pliku,1);return towar_ILE_LICZB<0?towar_ILE_LICZB:NET_BIND(towar_ILE_LICZB,adres_internetowy,되돌림흐름접속번호(dojście_do_pliku));
}
int32_t 자바흐름듣기(int32_t dojście_do_pliku,int32_t lista_prac){
    int towar_ILE_LICZB=zewnętrzny_identyfikator(dojście_do_pliku);if(towar_ILE_LICZB<0){int 반환값=되돌림흐름듣기(dojście_do_pliku,lista_prac);if(반환값<0||!임의주소[dojście_do_pliku-32])return 반환값;
        towar_ILE_LICZB=wkleić_SMS(dojście_do_pliku,1);if(towar_ILE_LICZB<0)return towar_ILE_LICZB;반환값=NET_BIND(towar_ILE_LICZB,망상태읽기(0,0),되돌림흐름접속번호(dojście_do_pliku));if(반환값<0)return 반환값;양쪽수신창구[dojście_do_pliku-32]=1;
    }return lista_prac<1?-22:NET_nasłuchiwać(towar_ILE_LICZB);
}
int32_t 자바흐름연결(int32_t dojście_do_pliku,int32_t adres_internetowy,int32_t numer_portu){
    if(adres_internetowy==0x7f000001 && zewnętrzny_identyfikator(dojście_do_pliku)<0)return 되돌림흐름연결(dojście_do_pliku,adres_internetowy,numer_portu);
    if(되돌림흐름접속번호(dojście_do_pliku)<0)return -9;int towar_ILE_LICZB=wkleić_SMS(dojście_do_pliku,1);return towar_ILE_LICZB<0?towar_ILE_LICZB:NET_POŁĄCZ(towar_ILE_LICZB,adres_internetowy,numer_portu);
}
int32_t 자바흐름연결받기(int32_t dojście_do_pliku){
    int towar_ILE_LICZB=zewnętrzny_identyfikator(dojście_do_pliku);if(towar_ILE_LICZB<0)return 되돌림흐름연결받기(dojście_do_pliku);
    if(양쪽수신창구[dojście_do_pliku-32]){int lokalny=되돌림흐름연결받기(dojście_do_pliku);if(lokalny!=-11)return lokalny;}
    int węzeł_równorzędny_WARTOŚĆ=NET_akceptować(towar_ILE_LICZB);if(węzeł_równorzędny_WARTOŚĆ<0)return węzeł_równorzędny_WARTOŚĆ;
    int wartość_docelowa=되돌림흐름만들기();if(wartość_docelowa<0){Zamknij_sieć(węzeł_równorzędny_WARTOŚĆ);return wartość_docelowa;}zewnętrzny[wartość_docelowa-32]=węzeł_równorzędny_WARTOŚĆ+1;return wartość_docelowa;
}
int32_t 자바흐름읽기(int32_t dojście_do_pliku,int32_t Rozmiar){
    int towar_ILE_LICZB=zewnętrzny_identyfikator(dojście_do_pliku);if(towar_ILE_LICZB<0)return 되돌림흐름읽기(dojście_do_pliku,Rozmiar);if(Rozmiar<0||Rozmiar>512)return -22;
    unsigned char dane[512];int 반환값=통신읽기(towar_ILE_LICZB,dane,Rozmiar);for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,dane[순번]);return 반환값;
}
int32_t 자바흐름쓰기(int32_t dojście_do_pliku,int32_t Rozmiar){
    int towar_ILE_LICZB=zewnętrzny_identyfikator(dojście_do_pliku);if(towar_ILE_LICZB<0)return 되돌림흐름쓰기(dojście_do_pliku,Rozmiar);if(Rozmiar<0||Rozmiar>512)return -22;
    unsigned char dane[512];for(int 순번=0;순번<Rozmiar;순번++)dane[순번]=자바전문얻기(순번);return NET_zapis(towar_ILE_LICZB,dane,Rozmiar);
}
int32_t 자바흐름접속번호(int32_t dojście_do_pliku){int towar_ILE_LICZB=zewnętrzny_identyfikator(dojście_do_pliku);return towar_ILE_LICZB<0?되돌림흐름접속번호(dojście_do_pliku):(int32_t)sieć_numer_portu(towar_ILE_LICZB);}
int32_t 자바흐름상대(int32_t dojście_do_pliku){int towar_ILE_LICZB=zewnętrzny_identyfikator(dojście_do_pliku);return towar_ILE_LICZB<0?되돌림흐름상대(dojście_do_pliku):(int32_t)węzeł_równorzędny_numer_portu(towar_ILE_LICZB);}
int32_t 자바흐름주소(int32_t dojście_do_pliku){return zewnętrzny_identyfikator(dojście_do_pliku)<0?0x7f000001:양쪽수신창구[dojście_do_pliku-32]?0:망상태읽기(0,0);}
int32_t 자바흐름닫기(int32_t dojście_do_pliku){int towar_ILE_LICZB=zewnętrzny_identyfikator(dojście_do_pliku);if(towar_ILE_LICZB>=0){Zamknij_sieć(towar_ILE_LICZB);zewnętrzny[dojście_do_pliku-32]=0;}if(dojście_do_pliku>=40&&dojście_do_pliku<56)임의주소[dojście_do_pliku-32]=양쪽수신창구[dojście_do_pliku-32]=0;return 되돌림흐름닫기(dojście_do_pliku);}
