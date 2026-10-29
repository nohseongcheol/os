#include "../명명/기계연결이름.h"
/* Preserve the deterministic Java loopback endpoints; route external IPv4 to lwIP. */
#include "netværk_Stak.h"
extern int32_t 되돌림전문만들기(int32_t,int32_t,int32_t), 되돌림전문묶기(int32_t,int32_t,int32_t);
extern int32_t 되돌림전문보내기(int32_t,int32_t,int32_t,int32_t), 되돌림전문받기(int32_t,int32_t);
extern int32_t 되돌림전문접속번호(int32_t), 되돌림전문주소(int32_t), 되돌림전문상대(int32_t), 되돌림전문닫기(int32_t);
extern int32_t 자바전문넣기(int32_t,int32_t),자바전문얻기(int32_t);
extern int32_t 되돌림흐름만들기(void),되돌림흐름묶기(int32_t,int32_t,int32_t),되돌림흐름듣기(int32_t,int32_t);
extern int32_t 되돌림흐름연결(int32_t,int32_t,int32_t),되돌림흐름연결받기(int32_t),되돌림흐름읽기(int32_t,int32_t),되돌림흐름쓰기(int32_t,int32_t);
extern int32_t 되돌림흐름접속번호(int32_t),되돌림흐름상대(int32_t),되돌림흐름닫기(int32_t);
static int ekstern[24];
static int 임의주소[24], 양쪽수신창구[24], UDP_ekstern_peer[8], bundet_mail[8];
static int ekstern_tal(int fil_handle) { return fil_handle>=32 && fil_handle<56 ? ekstern[fil_handle-32]-1 : -1; }
static int sætte_ind_sms(int fil_handle,int Type_område) {
    if(fil_handle<32||fil_handle>=56)return -9;int Forrige_vare=ekstern_tal(fil_handle);if(Forrige_vare>=0)return Forrige_vare;
    int vare_TÆL=åbne_socket_slutpunkt(Type_område);if(vare_TÆL>=0)ekstern[fil_handle-32]=vare_TÆL+1;return vare_TÆL;
}
int32_t 자바전문만들기(int32_t 첫째값,int32_t SEKUND_VÆRDI,int32_t tegnkode){return 되돌림전문만들기(첫째값,SEKUND_VÆRDI,tegnkode);}
int32_t 자바전문묶기(int32_t fil_handle,int32_t internetadresse,int32_t portnummer){
    if(internetadresse==0x7f000001)return 되돌림전문묶기(fil_handle,internetadresse,portnummer);
    if(internetadresse!=0&&internetadresse!=망상태읽기(0,0))return -99;
    int 반환값=되돌림전문묶기(fil_handle,0,portnummer);if(반환값<0)return 반환값;
    int vare_TÆL=sætte_ind_sms(fil_handle,2);if(vare_TÆL<0)return vare_TÆL;반환값=NET_BIND(vare_TÆL,망상태읽기(0,0),되돌림전문접속번호(fil_handle));if(!반환값)bundet_mail[fil_handle-32]=internetadresse;return 반환값;
}
int32_t 자바전문보내기(int32_t fil_handle,int32_t internetadresse,int32_t portnummer,int32_t Størrelse){
    if(internetadresse==0x7f000001)return 되돌림전문보내기(fil_handle,internetadresse,portnummer,Størrelse);
    if(Størrelse<0||Størrelse>512)return -90;if(portnummer<1||portnummer>65535)return -22;
    if(되돌림전문접속번호(fil_handle)<0)return -9;
    if(되돌림전문주소(fil_handle)==0x7f000001)return -101;
    int vare_TÆL=ekstern_tal(fil_handle);if(vare_TÆL<0){int 반환값=0;if(되돌림전문접속번호(fil_handle)==0)반환값=되돌림전문묶기(fil_handle,0,0);if(반환값<0)return 반환값;vare_TÆL=sætte_ind_sms(fil_handle,2);if(vare_TÆL<0)return vare_TÆL;반환값=NET_BIND(vare_TÆL,망상태읽기(0,0),되돌림전문접속번호(fil_handle));if(반환값<0)return 반환값;}
    unsigned char data[512];for(int 순번=0;순번<Størrelse;순번++)data[순번]=자바전문얻기(순번);return maile_datagram(vare_TÆL,data,Størrelse,internetadresse,portnummer);
}
int32_t 자바전문받기(int32_t fil_handle,int32_t Størrelse){
    int vare_TÆL=ekstern_tal(fil_handle);if(vare_TÆL<0)return 되돌림전문받기(fil_handle,Størrelse);if(Størrelse<0||Størrelse>512)return -22;
    int lokal=되돌림전문받기(fil_handle,Størrelse);if(lokal!=-11){UDP_ekstern_peer[fil_handle-32]=0;return lokal;}
    unsigned char data[512];int 반환값=modtage_datagram(vare_TÆL,data,Størrelse);if(반환값>=0)UDP_ekstern_peer[fil_handle-32]=1;for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,data[순번]);return 반환값;
}
int32_t 자바전문접속번호(int32_t fil_handle){int vare_TÆL=ekstern_tal(fil_handle);return vare_TÆL<0?되돌림전문접속번호(fil_handle):(int32_t)netværk_portnummer(vare_TÆL);}
int32_t 자바전문주소(int32_t fil_handle){return ekstern_tal(fil_handle)<0?되돌림전문주소(fil_handle):bundet_mail[fil_handle-32];}
int32_t 자바전문상대(int32_t fil_handle){int vare_TÆL=ekstern_tal(fil_handle);return vare_TÆL<0||!UDP_ekstern_peer[fil_handle-32]?되돌림전문상대(fil_handle):(int32_t)peer_portnummer(vare_TÆL);}
int32_t 자바전문원격주소(int32_t fil_handle){int vare_TÆL=ekstern_tal(fil_handle);return vare_TÆL<0||!UDP_ekstern_peer[fil_handle-32]?0x7f000001:(int32_t)NET_peer_mail(vare_TÆL);}
int32_t 자바전문닫기(int32_t fil_handle){int vare_TÆL=ekstern_tal(fil_handle);if(vare_TÆL>=0){Luk_netværk(vare_TÆL);ekstern[fil_handle-32]=0;}if(fil_handle>=32&&fil_handle<40)UDP_ekstern_peer[fil_handle-32]=bundet_mail[fil_handle-32]=0;return 되돌림전문닫기(fil_handle);}
int32_t 자바흐름만들기(void){return 되돌림흐름만들기();}
int32_t 자바흐름묶기(int32_t fil_handle,int32_t internetadresse,int32_t portnummer){
    if(internetadresse==0||internetadresse==0x7f000001){int 반환값=되돌림흐름묶기(fil_handle,internetadresse,portnummer);if(!반환값)임의주소[fil_handle-32]=internetadresse==0;return 반환값;}
    if(internetadresse!=망상태읽기(0,0))return -99;int 반환값=되돌림흐름묶기(fil_handle,0,portnummer);if(반환값<0)return 반환값;
    int vare_TÆL=sætte_ind_sms(fil_handle,1);return vare_TÆL<0?vare_TÆL:NET_BIND(vare_TÆL,internetadresse,되돌림흐름접속번호(fil_handle));
}
int32_t 자바흐름듣기(int32_t fil_handle,int32_t ordrebeholdning){
    int vare_TÆL=ekstern_tal(fil_handle);if(vare_TÆL<0){int 반환값=되돌림흐름듣기(fil_handle,ordrebeholdning);if(반환값<0||!임의주소[fil_handle-32])return 반환값;
        vare_TÆL=sætte_ind_sms(fil_handle,1);if(vare_TÆL<0)return vare_TÆL;반환값=NET_BIND(vare_TÆL,망상태읽기(0,0),되돌림흐름접속번호(fil_handle));if(반환값<0)return 반환값;양쪽수신창구[fil_handle-32]=1;
    }return ordrebeholdning<1?-22:NET_lytte(vare_TÆL);
}
int32_t 자바흐름연결(int32_t fil_handle,int32_t internetadresse,int32_t portnummer){
    if(internetadresse==0x7f000001 && ekstern_tal(fil_handle)<0)return 되돌림흐름연결(fil_handle,internetadresse,portnummer);
    if(되돌림흐름접속번호(fil_handle)<0)return -9;int vare_TÆL=sætte_ind_sms(fil_handle,1);return vare_TÆL<0?vare_TÆL:NET_Forbind(vare_TÆL,internetadresse,portnummer);
}
int32_t 자바흐름연결받기(int32_t fil_handle){
    int vare_TÆL=ekstern_tal(fil_handle);if(vare_TÆL<0)return 되돌림흐름연결받기(fil_handle);
    if(양쪽수신창구[fil_handle-32]){int lokal=되돌림흐름연결받기(fil_handle);if(lokal!=-11)return lokal;}
    int peer_VÆRDI=NET_acceptere(vare_TÆL);if(peer_VÆRDI<0)return peer_VÆRDI;
    int mål=되돌림흐름만들기();if(mål<0){Luk_netværk(peer_VÆRDI);return mål;}ekstern[mål-32]=peer_VÆRDI+1;return mål;
}
int32_t 자바흐름읽기(int32_t fil_handle,int32_t Størrelse){
    int vare_TÆL=ekstern_tal(fil_handle);if(vare_TÆL<0)return 되돌림흐름읽기(fil_handle,Størrelse);if(Størrelse<0||Størrelse>512)return -22;
    unsigned char data[512];int 반환값=통신읽기(vare_TÆL,data,Størrelse);for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,data[순번]);return 반환값;
}
int32_t 자바흐름쓰기(int32_t fil_handle,int32_t Størrelse){
    int vare_TÆL=ekstern_tal(fil_handle);if(vare_TÆL<0)return 되돌림흐름쓰기(fil_handle,Størrelse);if(Størrelse<0||Størrelse>512)return -22;
    unsigned char data[512];for(int 순번=0;순번<Størrelse;순번++)data[순번]=자바전문얻기(순번);return NET_skrive(vare_TÆL,data,Størrelse);
}
int32_t 자바흐름접속번호(int32_t fil_handle){int vare_TÆL=ekstern_tal(fil_handle);return vare_TÆL<0?되돌림흐름접속번호(fil_handle):(int32_t)netværk_portnummer(vare_TÆL);}
int32_t 자바흐름상대(int32_t fil_handle){int vare_TÆL=ekstern_tal(fil_handle);return vare_TÆL<0?되돌림흐름상대(fil_handle):(int32_t)peer_portnummer(vare_TÆL);}
int32_t 자바흐름주소(int32_t fil_handle){return ekstern_tal(fil_handle)<0?0x7f000001:양쪽수신창구[fil_handle-32]?0:망상태읽기(0,0);}
int32_t 자바흐름닫기(int32_t fil_handle){int vare_TÆL=ekstern_tal(fil_handle);if(vare_TÆL>=0){Luk_netværk(vare_TÆL);ekstern[fil_handle-32]=0;}if(fil_handle>=40&&fil_handle<56)임의주소[fil_handle-32]=양쪽수신창구[fil_handle-32]=0;return 되돌림흐름닫기(fil_handle);}
