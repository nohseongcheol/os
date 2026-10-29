#include "../명명/기계연결이름.h"
/* Preserve the deterministic Java loopback endpoints; route external IPv4 to lwIP. */
#include "nettverk_stakk.h"
extern int32_t 되돌림전문만들기(int32_t,int32_t,int32_t), 되돌림전문묶기(int32_t,int32_t,int32_t);
extern int32_t 되돌림전문보내기(int32_t,int32_t,int32_t,int32_t), 되돌림전문받기(int32_t,int32_t);
extern int32_t 되돌림전문접속번호(int32_t), 되돌림전문주소(int32_t), 되돌림전문상대(int32_t), 되돌림전문닫기(int32_t);
extern int32_t 자바전문넣기(int32_t,int32_t),자바전문얻기(int32_t);
extern int32_t 되돌림흐름만들기(void),되돌림흐름묶기(int32_t,int32_t,int32_t),되돌림흐름듣기(int32_t,int32_t);
extern int32_t 되돌림흐름연결(int32_t,int32_t,int32_t),되돌림흐름연결받기(int32_t),되돌림흐름읽기(int32_t,int32_t),되돌림흐름쓰기(int32_t,int32_t);
extern int32_t 되돌림흐름접속번호(int32_t),되돌림흐름상대(int32_t),되돌림흐름닫기(int32_t);
static int ekstern[24];
static int 임의주소[24], 양쪽수신창구[24], UDP_ekstern_node[8], bundet_e_post[8];
static int ekstern_nummer_2cf41d33(int Fil_håndtak) { return Fil_håndtak>=32 && Fil_håndtak<56 ? ekstern[Fil_håndtak-32]-1 : -1; }
static int lime_inn_SMS(int Fil_håndtak,int Type_område) {
    if(Fil_håndtak<32||Fil_håndtak>=56)return -9;int Forrige_vare=ekstern_nummer_2cf41d33(Fil_håndtak);if(Forrige_vare>=0)return Forrige_vare;
    int vare_ANTALL=åpne_socket_deltaker(Type_område);if(vare_ANTALL>=0)ekstern[Fil_håndtak-32]=vare_ANTALL+1;return vare_ANTALL;
}
int32_t 자바전문만들기(int32_t 첫째값,int32_t SEKUND_VERDI,int32_t tegnkode){return 되돌림전문만들기(첫째값,SEKUND_VERDI,tegnkode);}
int32_t 자바전문묶기(int32_t Fil_håndtak,int32_t Internett_adresse,int32_t portnummer){
    if(Internett_adresse==0x7f000001)return 되돌림전문묶기(Fil_håndtak,Internett_adresse,portnummer);
    if(Internett_adresse!=0&&Internett_adresse!=망상태읽기(0,0))return -99;
    int 반환값=되돌림전문묶기(Fil_håndtak,0,portnummer);if(반환값<0)return 반환값;
    int vare_ANTALL=lime_inn_SMS(Fil_håndtak,2);if(vare_ANTALL<0)return vare_ANTALL;반환값=netto_BIND(vare_ANTALL,망상태읽기(0,0),되돌림전문접속번호(Fil_håndtak));if(!반환값)bundet_e_post[Fil_håndtak-32]=Internett_adresse;return 반환값;
}
int32_t 자바전문보내기(int32_t Fil_håndtak,int32_t Internett_adresse,int32_t portnummer,int32_t Størrelse){
    if(Internett_adresse==0x7f000001)return 되돌림전문보내기(Fil_håndtak,Internett_adresse,portnummer,Størrelse);
    if(Størrelse<0||Størrelse>512)return -90;if(portnummer<1||portnummer>65535)return -22;
    if(되돌림전문접속번호(Fil_håndtak)<0)return -9;
    if(되돌림전문주소(Fil_håndtak)==0x7f000001)return -101;
    int vare_ANTALL=ekstern_nummer_2cf41d33(Fil_håndtak);if(vare_ANTALL<0){int 반환값=0;if(되돌림전문접속번호(Fil_håndtak)==0)반환값=되돌림전문묶기(Fil_håndtak,0,0);if(반환값<0)return 반환값;vare_ANTALL=lime_inn_SMS(Fil_håndtak,2);if(vare_ANTALL<0)return vare_ANTALL;반환값=netto_BIND(vare_ANTALL,망상태읽기(0,0),되돌림전문접속번호(Fil_håndtak));if(반환값<0)return 반환값;}
    unsigned char data[512];for(int 순번=0;순번<Størrelse;순번++)data[순번]=자바전문얻기(순번);return sende_datagram(vare_ANTALL,data,Størrelse,Internett_adresse,portnummer);
}
int32_t 자바전문받기(int32_t Fil_håndtak,int32_t Størrelse){
    int vare_ANTALL=ekstern_nummer_2cf41d33(Fil_håndtak);if(vare_ANTALL<0)return 되돌림전문받기(Fil_håndtak,Størrelse);if(Størrelse<0||Størrelse>512)return -22;
    int lokal=되돌림전문받기(Fil_håndtak,Størrelse);if(lokal!=-11){UDP_ekstern_node[Fil_håndtak-32]=0;return lokal;}
    unsigned char data[512];int 반환값=motta_datagram(vare_ANTALL,data,Størrelse);if(반환값>=0)UDP_ekstern_node[Fil_håndtak-32]=1;for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,data[순번]);return 반환값;
}
int32_t 자바전문접속번호(int32_t Fil_håndtak){int vare_ANTALL=ekstern_nummer_2cf41d33(Fil_håndtak);return vare_ANTALL<0?되돌림전문접속번호(Fil_håndtak):(int32_t)nettverk_portnummer(vare_ANTALL);}
int32_t 자바전문주소(int32_t Fil_håndtak){return ekstern_nummer_2cf41d33(Fil_håndtak)<0?되돌림전문주소(Fil_håndtak):bundet_e_post[Fil_håndtak-32];}
int32_t 자바전문상대(int32_t Fil_håndtak){int vare_ANTALL=ekstern_nummer_2cf41d33(Fil_håndtak);return vare_ANTALL<0||!UDP_ekstern_node[Fil_håndtak-32]?되돌림전문상대(Fil_håndtak):(int32_t)node_portnummer(vare_ANTALL);}
int32_t 자바전문원격주소(int32_t Fil_håndtak){int vare_ANTALL=ekstern_nummer_2cf41d33(Fil_håndtak);return vare_ANTALL<0||!UDP_ekstern_node[Fil_håndtak-32]?0x7f000001:(int32_t)netto_node_e_post(vare_ANTALL);}
int32_t 자바전문닫기(int32_t Fil_håndtak){int vare_ANTALL=ekstern_nummer_2cf41d33(Fil_håndtak);if(vare_ANTALL>=0){Lukk_nettverk(vare_ANTALL);ekstern[Fil_håndtak-32]=0;}if(Fil_håndtak>=32&&Fil_håndtak<40)UDP_ekstern_node[Fil_håndtak-32]=bundet_e_post[Fil_håndtak-32]=0;return 되돌림전문닫기(Fil_håndtak);}
int32_t 자바흐름만들기(void){return 되돌림흐름만들기();}
int32_t 자바흐름묶기(int32_t Fil_håndtak,int32_t Internett_adresse,int32_t portnummer){
    if(Internett_adresse==0||Internett_adresse==0x7f000001){int 반환값=되돌림흐름묶기(Fil_håndtak,Internett_adresse,portnummer);if(!반환값)임의주소[Fil_håndtak-32]=Internett_adresse==0;return 반환값;}
    if(Internett_adresse!=망상태읽기(0,0))return -99;int 반환값=되돌림흐름묶기(Fil_håndtak,0,portnummer);if(반환값<0)return 반환값;
    int vare_ANTALL=lime_inn_SMS(Fil_håndtak,1);return vare_ANTALL<0?vare_ANTALL:netto_BIND(vare_ANTALL,Internett_adresse,되돌림흐름접속번호(Fil_håndtak));
}
int32_t 자바흐름듣기(int32_t Fil_håndtak,int32_t gjenværende_arbeid){
    int vare_ANTALL=ekstern_nummer_2cf41d33(Fil_håndtak);if(vare_ANTALL<0){int 반환값=되돌림흐름듣기(Fil_håndtak,gjenværende_arbeid);if(반환값<0||!임의주소[Fil_håndtak-32])return 반환값;
        vare_ANTALL=lime_inn_SMS(Fil_håndtak,1);if(vare_ANTALL<0)return vare_ANTALL;반환값=netto_BIND(vare_ANTALL,망상태읽기(0,0),되돌림흐름접속번호(Fil_håndtak));if(반환값<0)return 반환값;양쪽수신창구[Fil_håndtak-32]=1;
    }return gjenværende_arbeid<1?-22:연결기다리기(vare_ANTALL);
}
int32_t 자바흐름연결(int32_t Fil_håndtak,int32_t Internett_adresse,int32_t portnummer){
    if(Internett_adresse==0x7f000001 && ekstern_nummer_2cf41d33(Fil_håndtak)<0)return 되돌림흐름연결(Fil_håndtak,Internett_adresse,portnummer);
    if(되돌림흐름접속번호(Fil_håndtak)<0)return -9;int vare_ANTALL=lime_inn_SMS(Fil_håndtak,1);return vare_ANTALL<0?vare_ANTALL:netto_KOBLE_TIL(vare_ANTALL,Internett_adresse,portnummer);
}
int32_t 자바흐름연결받기(int32_t Fil_håndtak){
    int vare_ANTALL=ekstern_nummer_2cf41d33(Fil_håndtak);if(vare_ANTALL<0)return 되돌림흐름연결받기(Fil_håndtak);
    if(양쪽수신창구[Fil_håndtak-32]){int lokal=되돌림흐름연결받기(Fil_håndtak);if(lokal!=-11)return lokal;}
    int node_VERDI_6a3b6fa7=netto_godta(vare_ANTALL);if(node_VERDI_6a3b6fa7<0)return node_VERDI_6a3b6fa7;
    int mål=되돌림흐름만들기();if(mål<0){Lukk_nettverk(node_VERDI_6a3b6fa7);return mål;}ekstern[mål-32]=node_VERDI_6a3b6fa7+1;return mål;
}
int32_t 자바흐름읽기(int32_t Fil_håndtak,int32_t Størrelse){
    int vare_ANTALL=ekstern_nummer_2cf41d33(Fil_håndtak);if(vare_ANTALL<0)return 되돌림흐름읽기(Fil_håndtak,Størrelse);if(Størrelse<0||Størrelse>512)return -22;
    unsigned char data[512];int 반환값=통신읽기(vare_ANTALL,data,Størrelse);for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,data[순번]);return 반환값;
}
int32_t 자바흐름쓰기(int32_t Fil_håndtak,int32_t Størrelse){
    int vare_ANTALL=ekstern_nummer_2cf41d33(Fil_håndtak);if(vare_ANTALL<0)return 되돌림흐름쓰기(Fil_håndtak,Størrelse);if(Størrelse<0||Størrelse>512)return -22;
    unsigned char data[512];for(int 순번=0;순번<Størrelse;순번++)data[순번]=자바전문얻기(순번);return netto_skrive(vare_ANTALL,data,Størrelse);
}
int32_t 자바흐름접속번호(int32_t Fil_håndtak){int vare_ANTALL=ekstern_nummer_2cf41d33(Fil_håndtak);return vare_ANTALL<0?되돌림흐름접속번호(Fil_håndtak):(int32_t)nettverk_portnummer(vare_ANTALL);}
int32_t 자바흐름상대(int32_t Fil_håndtak){int vare_ANTALL=ekstern_nummer_2cf41d33(Fil_håndtak);return vare_ANTALL<0?되돌림흐름상대(Fil_håndtak):(int32_t)node_portnummer(vare_ANTALL);}
int32_t 자바흐름주소(int32_t Fil_håndtak){return ekstern_nummer_2cf41d33(Fil_håndtak)<0?0x7f000001:양쪽수신창구[Fil_håndtak-32]?0:망상태읽기(0,0);}
int32_t 자바흐름닫기(int32_t Fil_håndtak){int vare_ANTALL=ekstern_nummer_2cf41d33(Fil_håndtak);if(vare_ANTALL>=0){Lukk_nettverk(vare_ANTALL);ekstern[Fil_håndtak-32]=0;}if(Fil_håndtak>=40&&Fil_håndtak<56)임의주소[Fil_håndtak-32]=양쪽수신창구[Fil_håndtak-32]=0;return 되돌림흐름닫기(Fil_håndtak);}
