#include "../명명/기계연결이름.h"
/* Preserve the deterministic Java loopback endpoints; route external IPv4 to lwIP. */
#include "Nettverk_Stabel.h"
extern int32_t 되돌림전문만들기(int32_t,int32_t,int32_t), 되돌림전문묶기(int32_t,int32_t,int32_t);
extern int32_t 되돌림전문보내기(int32_t,int32_t,int32_t,int32_t), 되돌림전문받기(int32_t,int32_t);
extern int32_t 되돌림전문접속번호(int32_t), 되돌림전문주소(int32_t), 되돌림전문상대(int32_t), 되돌림전문닫기(int32_t);
extern int32_t 자바전문넣기(int32_t,int32_t),자바전문얻기(int32_t);
extern int32_t 되돌림흐름만들기(void),되돌림흐름묶기(int32_t,int32_t,int32_t),되돌림흐름듣기(int32_t,int32_t);
extern int32_t 되돌림흐름연결(int32_t,int32_t,int32_t),되돌림흐름연결받기(int32_t),되돌림흐름읽기(int32_t,int32_t),되돌림흐름쓰기(int32_t,int32_t);
extern int32_t 되돌림흐름접속번호(int32_t),되돌림흐름상대(int32_t),되돌림흐름닫기(int32_t);
static int ekstern[24];
static int 임의주소[24], 양쪽수신창구[24], 전문외부상대[8], 묶인주소[8];
static int 외부번호(int fil_handtak) { return fil_handtak>=32 && fil_handtak<56 ? ekstern[fil_handtak-32]-1 : -1; }
static int lime_inn_SMS(int fil_handtak,int TYPE_kategori) {
    if(fil_handtak<32||fil_handtak>=56)return -9;int 이전=외부번호(fil_handtak);if(이전>=0)return 이전;
    int vare_COUNT=통신끝점만들기(TYPE_kategori);if(vare_COUNT>=0)ekstern[fil_handtak-32]=vare_COUNT+1;return vare_COUNT;
}
int32_t 자바전문만들기(int32_t 첫째값,int32_t SECOND_VALUE,int32_t teiknkode){return 되돌림전문만들기(첫째값,SECOND_VALUE,teiknkode);}
int32_t 자바전문묶기(int32_t fil_handtak,int32_t Internett_adresse,int32_t portnummer){
    if(Internett_adresse==0x7f000001)return 되돌림전문묶기(fil_handtak,Internett_adresse,portnummer);
    if(Internett_adresse!=0&&Internett_adresse!=망상태읽기(0,0))return -99;
    int 반환값=되돌림전문묶기(fil_handtak,0,portnummer);if(반환값<0)return 반환값;
    int vare_COUNT=lime_inn_SMS(fil_handtak,2);if(vare_COUNT<0)return vare_COUNT;반환값=망주소묶기(vare_COUNT,망상태읽기(0,0),되돌림전문접속번호(fil_handtak));if(!반환값)묶인주소[fil_handtak-32]=Internett_adresse;return 반환값;
}
int32_t 자바전문보내기(int32_t fil_handtak,int32_t Internett_adresse,int32_t portnummer,int32_t Storleik){
    if(Internett_adresse==0x7f000001)return 되돌림전문보내기(fil_handtak,Internett_adresse,portnummer,Storleik);
    if(Storleik<0||Storleik>512)return -90;if(portnummer<1||portnummer>65535)return -22;
    if(되돌림전문접속번호(fil_handtak)<0)return -9;
    if(되돌림전문주소(fil_handtak)==0x7f000001)return -101;
    int vare_COUNT=외부번호(fil_handtak);if(vare_COUNT<0){int 반환값=0;if(되돌림전문접속번호(fil_handtak)==0)반환값=되돌림전문묶기(fil_handtak,0,0);if(반환값<0)return 반환값;vare_COUNT=lime_inn_SMS(fil_handtak,2);if(vare_COUNT<0)return vare_COUNT;반환값=망주소묶기(vare_COUNT,망상태읽기(0,0),되돌림전문접속번호(fil_handtak));if(반환값<0)return 반환값;}
    unsigned char data[512];for(int 순번=0;순번<Storleik;순번++)data[순번]=자바전문얻기(순번);return 전문보내기(vare_COUNT,data,Storleik,Internett_adresse,portnummer);
}
int32_t 자바전문받기(int32_t fil_handtak,int32_t Storleik){
    int vare_COUNT=외부번호(fil_handtak);if(vare_COUNT<0)return 되돌림전문받기(fil_handtak,Storleik);if(Storleik<0||Storleik>512)return -22;
    int lokal=되돌림전문받기(fil_handtak,Storleik);if(lokal!=-11){전문외부상대[fil_handtak-32]=0;return lokal;}
    unsigned char data[512];int 반환값=전문받기(vare_COUNT,data,Storleik);if(반환값>=0)전문외부상대[fil_handtak-32]=1;for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,data[순번]);return 반환값;
}
int32_t 자바전문접속번호(int32_t fil_handtak){int vare_COUNT=외부번호(fil_handtak);return vare_COUNT<0?되돌림전문접속번호(fil_handtak):(int32_t)Nettverk_portnummer(vare_COUNT);}
int32_t 자바전문주소(int32_t fil_handtak){return 외부번호(fil_handtak)<0?되돌림전문주소(fil_handtak):묶인주소[fil_handtak-32];}
int32_t 자바전문상대(int32_t fil_handtak){int vare_COUNT=외부번호(fil_handtak);return vare_COUNT<0||!전문외부상대[fil_handtak-32]?되돌림전문상대(fil_handtak):(int32_t)node_portnummer(vare_COUNT);}
int32_t 자바전문원격주소(int32_t fil_handtak){int vare_COUNT=외부번호(fil_handtak);return vare_COUNT<0||!전문외부상대[fil_handtak-32]?0x7f000001:(int32_t)상대통신주소(vare_COUNT);}
int32_t 자바전문닫기(int32_t fil_handtak){int vare_COUNT=외부번호(fil_handtak);if(vare_COUNT>=0){Lukk_Nettverk(vare_COUNT);ekstern[fil_handtak-32]=0;}if(fil_handtak>=32&&fil_handtak<40)전문외부상대[fil_handtak-32]=묶인주소[fil_handtak-32]=0;return 되돌림전문닫기(fil_handtak);}
int32_t 자바흐름만들기(void){return 되돌림흐름만들기();}
int32_t 자바흐름묶기(int32_t fil_handtak,int32_t Internett_adresse,int32_t portnummer){
    if(Internett_adresse==0||Internett_adresse==0x7f000001){int 반환값=되돌림흐름묶기(fil_handtak,Internett_adresse,portnummer);if(!반환값)임의주소[fil_handtak-32]=Internett_adresse==0;return 반환값;}
    if(Internett_adresse!=망상태읽기(0,0))return -99;int 반환값=되돌림흐름묶기(fil_handtak,0,portnummer);if(반환값<0)return 반환값;
    int vare_COUNT=lime_inn_SMS(fil_handtak,1);return vare_COUNT<0?vare_COUNT:망주소묶기(vare_COUNT,Internett_adresse,되돌림흐름접속번호(fil_handtak));
}
int32_t 자바흐름듣기(int32_t fil_handtak,int32_t 연결대기한도){
    int vare_COUNT=외부번호(fil_handtak);if(vare_COUNT<0){int 반환값=되돌림흐름듣기(fil_handtak,연결대기한도);if(반환값<0||!임의주소[fil_handtak-32])return 반환값;
        vare_COUNT=lime_inn_SMS(fil_handtak,1);if(vare_COUNT<0)return vare_COUNT;반환값=망주소묶기(vare_COUNT,망상태읽기(0,0),되돌림흐름접속번호(fil_handtak));if(반환값<0)return 반환값;양쪽수신창구[fil_handtak-32]=1;
    }return 연결대기한도<1?-22:연결기다리기(vare_COUNT);
}
int32_t 자바흐름연결(int32_t fil_handtak,int32_t Internett_adresse,int32_t portnummer){
    if(Internett_adresse==0x7f000001 && 외부번호(fil_handtak)<0)return 되돌림흐름연결(fil_handtak,Internett_adresse,portnummer);
    if(되돌림흐름접속번호(fil_handtak)<0)return -9;int vare_COUNT=lime_inn_SMS(fil_handtak,1);return vare_COUNT<0?vare_COUNT:망연결하기(vare_COUNT,Internett_adresse,portnummer);
}
int32_t 자바흐름연결받기(int32_t fil_handtak){
    int vare_COUNT=외부번호(fil_handtak);if(vare_COUNT<0)return 되돌림흐름연결받기(fil_handtak);
    if(양쪽수신창구[fil_handtak-32]){int lokal=되돌림흐름연결받기(fil_handtak);if(lokal!=-11)return lokal;}
    int node_VALUE_6a3b6fa7=망연결받기(vare_COUNT);if(node_VALUE_6a3b6fa7<0)return node_VALUE_6a3b6fa7;
    int mål=되돌림흐름만들기();if(mål<0){Lukk_Nettverk(node_VALUE_6a3b6fa7);return mål;}ekstern[mål-32]=node_VALUE_6a3b6fa7+1;return mål;
}
int32_t 자바흐름읽기(int32_t fil_handtak,int32_t Storleik){
    int vare_COUNT=외부번호(fil_handtak);if(vare_COUNT<0)return 되돌림흐름읽기(fil_handtak,Storleik);if(Storleik<0||Storleik>512)return -22;
    unsigned char data[512];int 반환값=통신읽기(vare_COUNT,data,Storleik);for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,data[순번]);return 반환값;
}
int32_t 자바흐름쓰기(int32_t fil_handtak,int32_t Storleik){
    int vare_COUNT=외부번호(fil_handtak);if(vare_COUNT<0)return 되돌림흐름쓰기(fil_handtak,Storleik);if(Storleik<0||Storleik>512)return -22;
    unsigned char data[512];for(int 순번=0;순번<Storleik;순번++)data[순번]=자바전문얻기(순번);return 통신쓰기(vare_COUNT,data,Storleik);
}
int32_t 자바흐름접속번호(int32_t fil_handtak){int vare_COUNT=외부번호(fil_handtak);return vare_COUNT<0?되돌림흐름접속번호(fil_handtak):(int32_t)Nettverk_portnummer(vare_COUNT);}
int32_t 자바흐름상대(int32_t fil_handtak){int vare_COUNT=외부번호(fil_handtak);return vare_COUNT<0?되돌림흐름상대(fil_handtak):(int32_t)node_portnummer(vare_COUNT);}
int32_t 자바흐름주소(int32_t fil_handtak){return 외부번호(fil_handtak)<0?0x7f000001:양쪽수신창구[fil_handtak-32]?0:망상태읽기(0,0);}
int32_t 자바흐름닫기(int32_t fil_handtak){int vare_COUNT=외부번호(fil_handtak);if(vare_COUNT>=0){Lukk_Nettverk(vare_COUNT);ekstern[fil_handtak-32]=0;}if(fil_handtak>=40&&fil_handtak<56)임의주소[fil_handtak-32]=양쪽수신창구[fil_handtak-32]=0;return 되돌림흐름닫기(fil_handtak);}
