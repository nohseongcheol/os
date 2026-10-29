#include "../명명/기계연결이름.h"
/* Preserve the deterministic Java loopback endpoints; route external IPv4 to lwIP. */
#include "nätverk_Stack.h"
extern int32_t 되돌림전문만들기(int32_t,int32_t,int32_t), 되돌림전문묶기(int32_t,int32_t,int32_t);
extern int32_t 되돌림전문보내기(int32_t,int32_t,int32_t,int32_t), 되돌림전문받기(int32_t,int32_t);
extern int32_t 되돌림전문접속번호(int32_t), 되돌림전문주소(int32_t), 되돌림전문상대(int32_t), 되돌림전문닫기(int32_t);
extern int32_t 자바전문넣기(int32_t,int32_t),자바전문얻기(int32_t);
extern int32_t 되돌림흐름만들기(void),되돌림흐름묶기(int32_t,int32_t,int32_t),되돌림흐름듣기(int32_t,int32_t);
extern int32_t 되돌림흐름연결(int32_t,int32_t,int32_t),되돌림흐름연결받기(int32_t),되돌림흐름읽기(int32_t,int32_t),되돌림흐름쓰기(int32_t,int32_t);
extern int32_t 되돌림흐름접속번호(int32_t),되돌림흐름상대(int32_t),되돌림흐름닫기(int32_t);
static int 외부연결[24];
static int 임의주소[24], 양쪽수신창구[24], UDP_extern_peer[8], gräns_ADRESS[8];
static int extern_nummer(int filreferens) { return filreferens>=32 && filreferens<56 ? 외부연결[filreferens-32]-1 : -1; }
static int klistra_in_SMS(int filreferens,int Typ_område) {
    if(filreferens<32||filreferens>=56)return -9;int Föregående_objekt=extern_nummer(filreferens);if(Föregående_objekt>=0)return Föregående_objekt;
    int objekt_ANTAL=Skapa_socket_deltagare(Typ_område);if(objekt_ANTAL>=0)외부연결[filreferens-32]=objekt_ANTAL+1;return objekt_ANTAL;
}
int32_t 자바전문만들기(int32_t 첫째값,int32_t SEKUND_värde,int32_t kodpunkt){return 되돌림전문만들기(첫째값,SEKUND_värde,kodpunkt);}
int32_t 자바전문묶기(int32_t filreferens,int32_t Internetadress,int32_t portnummer){
    if(Internetadress==0x7f000001)return 되돌림전문묶기(filreferens,Internetadress,portnummer);
    if(Internetadress!=0&&Internetadress!=läsa_nätverk_status(0,0))return -99;
    int 반환값=되돌림전문묶기(filreferens,0,portnummer);if(반환값<0)return 반환값;
    int objekt_ANTAL=klistra_in_SMS(filreferens,2);if(objekt_ANTAL<0)return objekt_ANTAL;반환값=NET_BIND(objekt_ANTAL,läsa_nätverk_status(0,0),되돌림전문접속번호(filreferens));if(!반환값)gräns_ADRESS[filreferens-32]=Internetadress;return 반환값;
}
int32_t 자바전문보내기(int32_t filreferens,int32_t Internetadress,int32_t portnummer,int32_t Storlek){
    if(Internetadress==0x7f000001)return 되돌림전문보내기(filreferens,Internetadress,portnummer,Storlek);
    if(Storlek<0||Storlek>512)return -90;if(portnummer<1||portnummer>65535)return -22;
    if(되돌림전문접속번호(filreferens)<0)return -9;
    if(되돌림전문주소(filreferens)==0x7f000001)return -101;
    int objekt_ANTAL=extern_nummer(filreferens);if(objekt_ANTAL<0){int 반환값=0;if(되돌림전문접속번호(filreferens)==0)반환값=되돌림전문묶기(filreferens,0,0);if(반환값<0)return 반환값;objekt_ANTAL=klistra_in_SMS(filreferens,2);if(objekt_ANTAL<0)return objekt_ANTAL;반환값=NET_BIND(objekt_ANTAL,läsa_nätverk_status(0,0),되돌림전문접속번호(filreferens));if(반환값<0)return 반환값;}
    unsigned char data[512];for(int 순번=0;순번<Storlek;순번++)data[순번]=자바전문얻기(순번);return skicka_datagram(objekt_ANTAL,data,Storlek,Internetadress,portnummer);
}
int32_t 자바전문받기(int32_t filreferens,int32_t Storlek){
    int objekt_ANTAL=extern_nummer(filreferens);if(objekt_ANTAL<0)return 되돌림전문받기(filreferens,Storlek);if(Storlek<0||Storlek>512)return -22;
    int lokal=되돌림전문받기(filreferens,Storlek);if(lokal!=-11){UDP_extern_peer[filreferens-32]=0;return lokal;}
    unsigned char data[512];int 반환값=få_datagram(objekt_ANTAL,data,Storlek);if(반환값>=0)UDP_extern_peer[filreferens-32]=1;for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,data[순번]);return 반환값;
}
int32_t 자바전문접속번호(int32_t filreferens){int objekt_ANTAL=extern_nummer(filreferens);return objekt_ANTAL<0?되돌림전문접속번호(filreferens):(int32_t)nätverk_portnummer(objekt_ANTAL);}
int32_t 자바전문주소(int32_t filreferens){return extern_nummer(filreferens)<0?되돌림전문주소(filreferens):gräns_ADRESS[filreferens-32];}
int32_t 자바전문상대(int32_t filreferens){int objekt_ANTAL=extern_nummer(filreferens);return objekt_ANTAL<0||!UDP_extern_peer[filreferens-32]?되돌림전문상대(filreferens):(int32_t)peer_portnummer(objekt_ANTAL);}
int32_t 자바전문원격주소(int32_t filreferens){int objekt_ANTAL=extern_nummer(filreferens);return objekt_ANTAL<0||!UDP_extern_peer[filreferens-32]?0x7f000001:(int32_t)NET_peer_ADRESS(objekt_ANTAL);}
int32_t 자바전문닫기(int32_t filreferens){int objekt_ANTAL=extern_nummer(filreferens);if(objekt_ANTAL>=0){Stäng_nätverk(objekt_ANTAL);외부연결[filreferens-32]=0;}if(filreferens>=32&&filreferens<40)UDP_extern_peer[filreferens-32]=gräns_ADRESS[filreferens-32]=0;return 되돌림전문닫기(filreferens);}
int32_t 자바흐름만들기(void){return 되돌림흐름만들기();}
int32_t 자바흐름묶기(int32_t filreferens,int32_t Internetadress,int32_t portnummer){
    if(Internetadress==0||Internetadress==0x7f000001){int 반환값=되돌림흐름묶기(filreferens,Internetadress,portnummer);if(!반환값)임의주소[filreferens-32]=Internetadress==0;return 반환값;}
    if(Internetadress!=läsa_nätverk_status(0,0))return -99;int 반환값=되돌림흐름묶기(filreferens,0,portnummer);if(반환값<0)return 반환값;
    int objekt_ANTAL=klistra_in_SMS(filreferens,1);return objekt_ANTAL<0?objekt_ANTAL:NET_BIND(objekt_ANTAL,Internetadress,되돌림흐름접속번호(filreferens));
}
int32_t 자바흐름듣기(int32_t filreferens,int32_t kvarvarande_uppgifter){
    int objekt_ANTAL=extern_nummer(filreferens);if(objekt_ANTAL<0){int 반환값=되돌림흐름듣기(filreferens,kvarvarande_uppgifter);if(반환값<0||!임의주소[filreferens-32])return 반환값;
        objekt_ANTAL=klistra_in_SMS(filreferens,1);if(objekt_ANTAL<0)return objekt_ANTAL;반환값=NET_BIND(objekt_ANTAL,läsa_nätverk_status(0,0),되돌림흐름접속번호(filreferens));if(반환값<0)return 반환값;양쪽수신창구[filreferens-32]=1;
    }return kvarvarande_uppgifter<1?-22:NET_lyssna(objekt_ANTAL);
}
int32_t 자바흐름연결(int32_t filreferens,int32_t Internetadress,int32_t portnummer){
    if(Internetadress==0x7f000001 && extern_nummer(filreferens)<0)return 되돌림흐름연결(filreferens,Internetadress,portnummer);
    if(되돌림흐름접속번호(filreferens)<0)return -9;int objekt_ANTAL=klistra_in_SMS(filreferens,1);return objekt_ANTAL<0?objekt_ANTAL:NET_ANSLUT(objekt_ANTAL,Internetadress,portnummer);
}
int32_t 자바흐름연결받기(int32_t filreferens){
    int objekt_ANTAL=extern_nummer(filreferens);if(objekt_ANTAL<0)return 되돌림흐름연결받기(filreferens);
    if(양쪽수신창구[filreferens-32]){int lokal=되돌림흐름연결받기(filreferens);if(lokal!=-11)return lokal;}
    int peer_värde=NET_acceptera(objekt_ANTAL);if(peer_värde<0)return peer_värde;
    int mål=되돌림흐름만들기();if(mål<0){Stäng_nätverk(peer_värde);return mål;}외부연결[mål-32]=peer_värde+1;return mål;
}
int32_t 자바흐름읽기(int32_t filreferens,int32_t Storlek){
    int objekt_ANTAL=extern_nummer(filreferens);if(objekt_ANTAL<0)return 되돌림흐름읽기(filreferens,Storlek);if(Storlek<0||Storlek>512)return -22;
    unsigned char data[512];int 반환값=NET_läsa(objekt_ANTAL,data,Storlek);for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,data[순번]);return 반환값;
}
int32_t 자바흐름쓰기(int32_t filreferens,int32_t Storlek){
    int objekt_ANTAL=extern_nummer(filreferens);if(objekt_ANTAL<0)return 되돌림흐름쓰기(filreferens,Storlek);if(Storlek<0||Storlek>512)return -22;
    unsigned char data[512];for(int 순번=0;순번<Storlek;순번++)data[순번]=자바전문얻기(순번);return NET_skriva(objekt_ANTAL,data,Storlek);
}
int32_t 자바흐름접속번호(int32_t filreferens){int objekt_ANTAL=extern_nummer(filreferens);return objekt_ANTAL<0?되돌림흐름접속번호(filreferens):(int32_t)nätverk_portnummer(objekt_ANTAL);}
int32_t 자바흐름상대(int32_t filreferens){int objekt_ANTAL=extern_nummer(filreferens);return objekt_ANTAL<0?되돌림흐름상대(filreferens):(int32_t)peer_portnummer(objekt_ANTAL);}
int32_t 자바흐름주소(int32_t filreferens){return extern_nummer(filreferens)<0?0x7f000001:양쪽수신창구[filreferens-32]?0:läsa_nätverk_status(0,0);}
int32_t 자바흐름닫기(int32_t filreferens){int objekt_ANTAL=extern_nummer(filreferens);if(objekt_ANTAL>=0){Stäng_nätverk(objekt_ANTAL);외부연결[filreferens-32]=0;}if(filreferens>=40&&filreferens<56)임의주소[filreferens-32]=양쪽수신창구[filreferens-32]=0;return 되돌림흐름닫기(filreferens);}
