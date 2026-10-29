#include "../명명/기계연결이름.h"
/* Preserve the deterministic Java loopback endpoints; route external IPv4 to lwIP. */
#include "net_stack.h"
extern int32_t 되돌림전문만들기(int32_t,int32_t,int32_t), 되돌림전문묶기(int32_t,int32_t,int32_t);
extern int32_t 되돌림전문보내기(int32_t,int32_t,int32_t,int32_t), 되돌림전문받기(int32_t,int32_t);
extern int32_t 되돌림전문접속번호(int32_t), 되돌림전문주소(int32_t), 되돌림전문상대(int32_t), 되돌림전문닫기(int32_t);
extern int32_t 자바전문넣기(int32_t,int32_t),자바전문얻기(int32_t);
extern int32_t 되돌림흐름만들기(void),되돌림흐름묶기(int32_t,int32_t,int32_t),되돌림흐름듣기(int32_t,int32_t);
extern int32_t 되돌림흐름연결(int32_t,int32_t,int32_t),되돌림흐름연결받기(int32_t),되돌림흐름읽기(int32_t,int32_t),되돌림흐름쓰기(int32_t,int32_t);
extern int32_t 되돌림흐름접속번호(int32_t),되돌림흐름상대(int32_t),되돌림흐름닫기(int32_t);
static int 외부연결[24];
static int 임의주소[24], 양쪽수신창구[24], UDP_extern_peer[8], grens_ADRES[8];
static int extern_nummer_2cf41d33(int bestandsingang) { return bestandsingang>=32 && bestandsingang<56 ? 외부연결[bestandsingang-32]-1 : -1; }
static int plakken_sms(int bestandsingang,int TYPE_gebied) {
    if(bestandsingang<32||bestandsingang>=56)return -9;int Vorige_item=extern_nummer_2cf41d33(bestandsingang);if(Vorige_item>=0)return Vorige_item;
    int item_AANTAL=maken_socket_eindpunt(TYPE_gebied);if(item_AANTAL>=0)외부연결[bestandsingang-32]=item_AANTAL+1;return item_AANTAL;
}
int32_t 자바전문만들기(int32_t 첫째값,int32_t SECONDE_WAARDE,int32_t codepoint){return 되돌림전문만들기(첫째값,SECONDE_WAARDE,codepoint);}
int32_t 자바전문묶기(int32_t bestandsingang,int32_t internetadres,int32_t poortnummer){
    if(internetadres==0x7f000001)return 되돌림전문묶기(bestandsingang,internetadres,poortnummer);
    if(internetadres!=0&&internetadres!=망상태읽기(0,0))return -99;
    int 반환값=되돌림전문묶기(bestandsingang,0,poortnummer);if(반환값<0)return 반환값;
    int item_AANTAL=plakken_sms(bestandsingang,2);if(item_AANTAL<0)return item_AANTAL;반환값=NET_BIND(item_AANTAL,망상태읽기(0,0),되돌림전문접속번호(bestandsingang));if(!반환값)grens_ADRES[bestandsingang-32]=internetadres;return 반환값;
}
int32_t 자바전문보내기(int32_t bestandsingang,int32_t internetadres,int32_t poortnummer,int32_t Grootte){
    if(internetadres==0x7f000001)return 되돌림전문보내기(bestandsingang,internetadres,poortnummer,Grootte);
    if(Grootte<0||Grootte>512)return -90;if(poortnummer<1||poortnummer>65535)return -22;
    if(되돌림전문접속번호(bestandsingang)<0)return -9;
    if(되돌림전문주소(bestandsingang)==0x7f000001)return -101;
    int item_AANTAL=extern_nummer_2cf41d33(bestandsingang);if(item_AANTAL<0){int 반환값=0;if(되돌림전문접속번호(bestandsingang)==0)반환값=되돌림전문묶기(bestandsingang,0,0);if(반환값<0)return 반환값;item_AANTAL=plakken_sms(bestandsingang,2);if(item_AANTAL<0)return item_AANTAL;반환값=NET_BIND(item_AANTAL,망상태읽기(0,0),되돌림전문접속번호(bestandsingang));if(반환값<0)return 반환값;}
    unsigned char gegevens[512];for(int 순번=0;순번<Grootte;순번++)gegevens[순번]=자바전문얻기(순번);return e_mailen_datagram(item_AANTAL,gegevens,Grootte,internetadres,poortnummer);
}
int32_t 자바전문받기(int32_t bestandsingang,int32_t Grootte){
    int item_AANTAL=extern_nummer_2cf41d33(bestandsingang);if(item_AANTAL<0)return 되돌림전문받기(bestandsingang,Grootte);if(Grootte<0||Grootte>512)return -22;
    int lokaal=되돌림전문받기(bestandsingang,Grootte);if(lokaal!=-11){UDP_extern_peer[bestandsingang-32]=0;return lokaal;}
    unsigned char gegevens[512];int 반환값=ontvangen_datagram(item_AANTAL,gegevens,Grootte);if(반환값>=0)UDP_extern_peer[bestandsingang-32]=1;for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,gegevens[순번]);return 반환값;
}
int32_t 자바전문접속번호(int32_t bestandsingang){int item_AANTAL=extern_nummer_2cf41d33(bestandsingang);return item_AANTAL<0?되돌림전문접속번호(bestandsingang):(int32_t)net_poortnummer(item_AANTAL);}
int32_t 자바전문주소(int32_t bestandsingang){return extern_nummer_2cf41d33(bestandsingang)<0?되돌림전문주소(bestandsingang):grens_ADRES[bestandsingang-32];}
int32_t 자바전문상대(int32_t bestandsingang){int item_AANTAL=extern_nummer_2cf41d33(bestandsingang);return item_AANTAL<0||!UDP_extern_peer[bestandsingang-32]?되돌림전문상대(bestandsingang):(int32_t)peer_poortnummer(item_AANTAL);}
int32_t 자바전문원격주소(int32_t bestandsingang){int item_AANTAL=extern_nummer_2cf41d33(bestandsingang);return item_AANTAL<0||!UDP_extern_peer[bestandsingang-32]?0x7f000001:(int32_t)NET_peer_ADRES(item_AANTAL);}
int32_t 자바전문닫기(int32_t bestandsingang){int item_AANTAL=extern_nummer_2cf41d33(bestandsingang);if(item_AANTAL>=0){Sluiten_net(item_AANTAL);외부연결[bestandsingang-32]=0;}if(bestandsingang>=32&&bestandsingang<40)UDP_extern_peer[bestandsingang-32]=grens_ADRES[bestandsingang-32]=0;return 되돌림전문닫기(bestandsingang);}
int32_t 자바흐름만들기(void){return 되돌림흐름만들기();}
int32_t 자바흐름묶기(int32_t bestandsingang,int32_t internetadres,int32_t poortnummer){
    if(internetadres==0||internetadres==0x7f000001){int 반환값=되돌림흐름묶기(bestandsingang,internetadres,poortnummer);if(!반환값)임의주소[bestandsingang-32]=internetadres==0;return 반환값;}
    if(internetadres!=망상태읽기(0,0))return -99;int 반환값=되돌림흐름묶기(bestandsingang,0,poortnummer);if(반환값<0)return 반환값;
    int item_AANTAL=plakken_sms(bestandsingang,1);return item_AANTAL<0?item_AANTAL:NET_BIND(item_AANTAL,internetadres,되돌림흐름접속번호(bestandsingang));
}
int32_t 자바흐름듣기(int32_t bestandsingang,int32_t achterstand){
    int item_AANTAL=extern_nummer_2cf41d33(bestandsingang);if(item_AANTAL<0){int 반환값=되돌림흐름듣기(bestandsingang,achterstand);if(반환값<0||!임의주소[bestandsingang-32])return 반환값;
        item_AANTAL=plakken_sms(bestandsingang,1);if(item_AANTAL<0)return item_AANTAL;반환값=NET_BIND(item_AANTAL,망상태읽기(0,0),되돌림흐름접속번호(bestandsingang));if(반환값<0)return 반환값;양쪽수신창구[bestandsingang-32]=1;
    }return achterstand<1?-22:연결기다리기(item_AANTAL);
}
int32_t 자바흐름연결(int32_t bestandsingang,int32_t internetadres,int32_t poortnummer){
    if(internetadres==0x7f000001 && extern_nummer_2cf41d33(bestandsingang)<0)return 되돌림흐름연결(bestandsingang,internetadres,poortnummer);
    if(되돌림흐름접속번호(bestandsingang)<0)return -9;int item_AANTAL=plakken_sms(bestandsingang,1);return item_AANTAL<0?item_AANTAL:NET_VERBINDEN(item_AANTAL,internetadres,poortnummer);
}
int32_t 자바흐름연결받기(int32_t bestandsingang){
    int item_AANTAL=extern_nummer_2cf41d33(bestandsingang);if(item_AANTAL<0)return 되돌림흐름연결받기(bestandsingang);
    if(양쪽수신창구[bestandsingang-32]){int lokaal=되돌림흐름연결받기(bestandsingang);if(lokaal!=-11)return lokaal;}
    int peer_WAARDE=NET_accepteren(item_AANTAL);if(peer_WAARDE<0)return peer_WAARDE;
    int doel=되돌림흐름만들기();if(doel<0){Sluiten_net(peer_WAARDE);return doel;}외부연결[doel-32]=peer_WAARDE+1;return doel;
}
int32_t 자바흐름읽기(int32_t bestandsingang,int32_t Grootte){
    int item_AANTAL=extern_nummer_2cf41d33(bestandsingang);if(item_AANTAL<0)return 되돌림흐름읽기(bestandsingang,Grootte);if(Grootte<0||Grootte>512)return -22;
    unsigned char gegevens[512];int 반환값=통신읽기(item_AANTAL,gegevens,Grootte);for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,gegevens[순번]);return 반환값;
}
int32_t 자바흐름쓰기(int32_t bestandsingang,int32_t Grootte){
    int item_AANTAL=extern_nummer_2cf41d33(bestandsingang);if(item_AANTAL<0)return 되돌림흐름쓰기(bestandsingang,Grootte);if(Grootte<0||Grootte>512)return -22;
    unsigned char gegevens[512];for(int 순번=0;순번<Grootte;순번++)gegevens[순번]=자바전문얻기(순번);return NET_schrijven(item_AANTAL,gegevens,Grootte);
}
int32_t 자바흐름접속번호(int32_t bestandsingang){int item_AANTAL=extern_nummer_2cf41d33(bestandsingang);return item_AANTAL<0?되돌림흐름접속번호(bestandsingang):(int32_t)net_poortnummer(item_AANTAL);}
int32_t 자바흐름상대(int32_t bestandsingang){int item_AANTAL=extern_nummer_2cf41d33(bestandsingang);return item_AANTAL<0?되돌림흐름상대(bestandsingang):(int32_t)peer_poortnummer(item_AANTAL);}
int32_t 자바흐름주소(int32_t bestandsingang){return extern_nummer_2cf41d33(bestandsingang)<0?0x7f000001:양쪽수신창구[bestandsingang-32]?0:망상태읽기(0,0);}
int32_t 자바흐름닫기(int32_t bestandsingang){int item_AANTAL=extern_nummer_2cf41d33(bestandsingang);if(item_AANTAL>=0){Sluiten_net(item_AANTAL);외부연결[bestandsingang-32]=0;}if(bestandsingang>=40&&bestandsingang<56)임의주소[bestandsingang-32]=양쪽수신창구[bestandsingang-32]=0;return 되돌림흐름닫기(bestandsingang);}
