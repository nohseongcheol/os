#include "../명명/기계연결이름.h"
/* Preserve the deterministic Java loopback endpoints; route external IPv4 to lwIP. */
#include "võrk_Virn.h"
extern int32_t 되돌림전문만들기(int32_t,int32_t,int32_t), 되돌림전문묶기(int32_t,int32_t,int32_t);
extern int32_t 되돌림전문보내기(int32_t,int32_t,int32_t,int32_t), 되돌림전문받기(int32_t,int32_t);
extern int32_t 되돌림전문접속번호(int32_t), 되돌림전문주소(int32_t), 되돌림전문상대(int32_t), 되돌림전문닫기(int32_t);
extern int32_t 자바전문넣기(int32_t,int32_t),자바전문얻기(int32_t);
extern int32_t 되돌림흐름만들기(void),되돌림흐름묶기(int32_t,int32_t,int32_t),되돌림흐름듣기(int32_t,int32_t);
extern int32_t 되돌림흐름연결(int32_t,int32_t,int32_t),되돌림흐름연결받기(int32_t),되돌림흐름읽기(int32_t,int32_t),되돌림흐름쓰기(int32_t,int32_t);
extern int32_t 되돌림흐름접속번호(int32_t),되돌림흐름상대(int32_t),되돌림흐름닫기(int32_t);
static int väline[24];
static int 임의주소[24], 양쪽수신창구[24], UDP_väline_partner[8], piir_ADDRESS[8];
static int väline_number(int Fail_pide) { return Fail_pide>=32 && Fail_pide<56 ? väline[Fail_pide-32]-1 : -1; }
static int kleepima_SMS(int Fail_pide,int TYPE_ala) {
    if(Fail_pide<32||Fail_pide>=56)return -9;int 이전=väline_number(Fail_pide);if(이전>=0)return 이전;
    int kaup_COUNT=통신끝점만들기(TYPE_ala);if(kaup_COUNT>=0)väline[Fail_pide-32]=kaup_COUNT+1;return kaup_COUNT;
}
int32_t 자바전문만들기(int32_t 첫째값,int32_t SECOND_VALUE,int32_t koodipunkt){return 되돌림전문만들기(첫째값,SECOND_VALUE,koodipunkt);}
int32_t 자바전문묶기(int32_t Fail_pide,int32_t Interneti_aadress,int32_t pordinumber){
    if(Interneti_aadress==0x7f000001)return 되돌림전문묶기(Fail_pide,Interneti_aadress,pordinumber);
    if(Interneti_aadress!=0&&Interneti_aadress!=망상태읽기(0,0))return -99;
    int 반환값=되돌림전문묶기(Fail_pide,0,pordinumber);if(반환값<0)return 반환값;
    int kaup_COUNT=kleepima_SMS(Fail_pide,2);if(kaup_COUNT<0)return kaup_COUNT;반환값=NET_BIND(kaup_COUNT,망상태읽기(0,0),되돌림전문접속번호(Fail_pide));if(!반환값)piir_ADDRESS[Fail_pide-32]=Interneti_aadress;return 반환값;
}
int32_t 자바전문보내기(int32_t Fail_pide,int32_t Interneti_aadress,int32_t pordinumber,int32_t Suurus){
    if(Interneti_aadress==0x7f000001)return 되돌림전문보내기(Fail_pide,Interneti_aadress,pordinumber,Suurus);
    if(Suurus<0||Suurus>512)return -90;if(pordinumber<1||pordinumber>65535)return -22;
    if(되돌림전문접속번호(Fail_pide)<0)return -9;
    if(되돌림전문주소(Fail_pide)==0x7f000001)return -101;
    int kaup_COUNT=väline_number(Fail_pide);if(kaup_COUNT<0){int 반환값=0;if(되돌림전문접속번호(Fail_pide)==0)반환값=되돌림전문묶기(Fail_pide,0,0);if(반환값<0)return 반환값;kaup_COUNT=kleepima_SMS(Fail_pide,2);if(kaup_COUNT<0)return kaup_COUNT;반환값=NET_BIND(kaup_COUNT,망상태읽기(0,0),되돌림전문접속번호(Fail_pide));if(반환값<0)return 반환값;}
    unsigned char andmed[512];for(int 순번=0;순번<Suurus;순번++)andmed[순번]=자바전문얻기(순번);return saatma_datagramm(kaup_COUNT,andmed,Suurus,Interneti_aadress,pordinumber);
}
int32_t 자바전문받기(int32_t Fail_pide,int32_t Suurus){
    int kaup_COUNT=väline_number(Fail_pide);if(kaup_COUNT<0)return 되돌림전문받기(Fail_pide,Suurus);if(Suurus<0||Suurus>512)return -22;
    int kohalik=되돌림전문받기(Fail_pide,Suurus);if(kohalik!=-11){UDP_väline_partner[Fail_pide-32]=0;return kohalik;}
    unsigned char andmed[512];int 반환값=saama_datagramm(kaup_COUNT,andmed,Suurus);if(반환값>=0)UDP_väline_partner[Fail_pide-32]=1;for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,andmed[순번]);return 반환값;
}
int32_t 자바전문접속번호(int32_t Fail_pide){int kaup_COUNT=väline_number(Fail_pide);return kaup_COUNT<0?되돌림전문접속번호(Fail_pide):(int32_t)võrk_pordinumber(kaup_COUNT);}
int32_t 자바전문주소(int32_t Fail_pide){return väline_number(Fail_pide)<0?되돌림전문주소(Fail_pide):piir_ADDRESS[Fail_pide-32];}
int32_t 자바전문상대(int32_t Fail_pide){int kaup_COUNT=väline_number(Fail_pide);return kaup_COUNT<0||!UDP_väline_partner[Fail_pide-32]?되돌림전문상대(Fail_pide):(int32_t)partner_pordinumber(kaup_COUNT);}
int32_t 자바전문원격주소(int32_t Fail_pide){int kaup_COUNT=väline_number(Fail_pide);return kaup_COUNT<0||!UDP_väline_partner[Fail_pide-32]?0x7f000001:(int32_t)NET_partner_ADDRESS(kaup_COUNT);}
int32_t 자바전문닫기(int32_t Fail_pide){int kaup_COUNT=väline_number(Fail_pide);if(kaup_COUNT>=0){Sule_võrk(kaup_COUNT);väline[Fail_pide-32]=0;}if(Fail_pide>=32&&Fail_pide<40)UDP_väline_partner[Fail_pide-32]=piir_ADDRESS[Fail_pide-32]=0;return 되돌림전문닫기(Fail_pide);}
int32_t 자바흐름만들기(void){return 되돌림흐름만들기();}
int32_t 자바흐름묶기(int32_t Fail_pide,int32_t Interneti_aadress,int32_t pordinumber){
    if(Interneti_aadress==0||Interneti_aadress==0x7f000001){int 반환값=되돌림흐름묶기(Fail_pide,Interneti_aadress,pordinumber);if(!반환값)임의주소[Fail_pide-32]=Interneti_aadress==0;return 반환값;}
    if(Interneti_aadress!=망상태읽기(0,0))return -99;int 반환값=되돌림흐름묶기(Fail_pide,0,pordinumber);if(반환값<0)return 반환값;
    int kaup_COUNT=kleepima_SMS(Fail_pide,1);return kaup_COUNT<0?kaup_COUNT:NET_BIND(kaup_COUNT,Interneti_aadress,되돌림흐름접속번호(Fail_pide));
}
int32_t 자바흐름듣기(int32_t Fail_pide,int32_t 연결대기한도){
    int kaup_COUNT=väline_number(Fail_pide);if(kaup_COUNT<0){int 반환값=되돌림흐름듣기(Fail_pide,연결대기한도);if(반환값<0||!임의주소[Fail_pide-32])return 반환값;
        kaup_COUNT=kleepima_SMS(Fail_pide,1);if(kaup_COUNT<0)return kaup_COUNT;반환값=NET_BIND(kaup_COUNT,망상태읽기(0,0),되돌림흐름접속번호(Fail_pide));if(반환값<0)return 반환값;양쪽수신창구[Fail_pide-32]=1;
    }return 연결대기한도<1?-22:NET_jälgima(kaup_COUNT);
}
int32_t 자바흐름연결(int32_t Fail_pide,int32_t Interneti_aadress,int32_t pordinumber){
    if(Interneti_aadress==0x7f000001 && väline_number(Fail_pide)<0)return 되돌림흐름연결(Fail_pide,Interneti_aadress,pordinumber);
    if(되돌림흐름접속번호(Fail_pide)<0)return -9;int kaup_COUNT=kleepima_SMS(Fail_pide,1);return kaup_COUNT<0?kaup_COUNT:NET_Ühenda(kaup_COUNT,Interneti_aadress,pordinumber);
}
int32_t 자바흐름연결받기(int32_t Fail_pide){
    int kaup_COUNT=väline_number(Fail_pide);if(kaup_COUNT<0)return 되돌림흐름연결받기(Fail_pide);
    if(양쪽수신창구[Fail_pide-32]){int kohalik=되돌림흐름연결받기(Fail_pide);if(kohalik!=-11)return kohalik;}
    int partner_VALUE=NET_aktsepteerima(kaup_COUNT);if(partner_VALUE<0)return partner_VALUE;
    int siht=되돌림흐름만들기();if(siht<0){Sule_võrk(partner_VALUE);return siht;}väline[siht-32]=partner_VALUE+1;return siht;
}
int32_t 자바흐름읽기(int32_t Fail_pide,int32_t Suurus){
    int kaup_COUNT=väline_number(Fail_pide);if(kaup_COUNT<0)return 되돌림흐름읽기(Fail_pide,Suurus);if(Suurus<0||Suurus>512)return -22;
    unsigned char andmed[512];int 반환값=통신읽기(kaup_COUNT,andmed,Suurus);for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,andmed[순번]);return 반환값;
}
int32_t 자바흐름쓰기(int32_t Fail_pide,int32_t Suurus){
    int kaup_COUNT=väline_number(Fail_pide);if(kaup_COUNT<0)return 되돌림흐름쓰기(Fail_pide,Suurus);if(Suurus<0||Suurus>512)return -22;
    unsigned char andmed[512];for(int 순번=0;순번<Suurus;순번++)andmed[순번]=자바전문얻기(순번);return NET_kirjutamine(kaup_COUNT,andmed,Suurus);
}
int32_t 자바흐름접속번호(int32_t Fail_pide){int kaup_COUNT=väline_number(Fail_pide);return kaup_COUNT<0?되돌림흐름접속번호(Fail_pide):(int32_t)võrk_pordinumber(kaup_COUNT);}
int32_t 자바흐름상대(int32_t Fail_pide){int kaup_COUNT=väline_number(Fail_pide);return kaup_COUNT<0?되돌림흐름상대(Fail_pide):(int32_t)partner_pordinumber(kaup_COUNT);}
int32_t 자바흐름주소(int32_t Fail_pide){return väline_number(Fail_pide)<0?0x7f000001:양쪽수신창구[Fail_pide-32]?0:망상태읽기(0,0);}
int32_t 자바흐름닫기(int32_t Fail_pide){int kaup_COUNT=väline_number(Fail_pide);if(kaup_COUNT>=0){Sule_võrk(kaup_COUNT);väline[Fail_pide-32]=0;}if(Fail_pide>=40&&Fail_pide<56)임의주소[Fail_pide-32]=양쪽수신창구[Fail_pide-32]=0;return 되돌림흐름닫기(Fail_pide);}
