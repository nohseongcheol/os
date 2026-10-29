#include "../명명/기계연결이름.h"
/* Preserve the deterministic Java loopback endpoints; route external IPv4 to lwIP. */
#include "Rhwydwaith_pentwr.h"
extern int32_t 되돌림전문만들기(int32_t,int32_t,int32_t), 되돌림전문묶기(int32_t,int32_t,int32_t);
extern int32_t 되돌림전문보내기(int32_t,int32_t,int32_t,int32_t), 되돌림전문받기(int32_t,int32_t);
extern int32_t 되돌림전문접속번호(int32_t), 되돌림전문주소(int32_t), 되돌림전문상대(int32_t), 되돌림전문닫기(int32_t);
extern int32_t 자바전문넣기(int32_t,int32_t),자바전문얻기(int32_t);
extern int32_t 되돌림흐름만들기(void),되돌림흐름묶기(int32_t,int32_t,int32_t),되돌림흐름듣기(int32_t,int32_t);
extern int32_t 되돌림흐름연결(int32_t,int32_t,int32_t),되돌림흐름연결받기(int32_t),되돌림흐름읽기(int32_t,int32_t),되돌림흐름쓰기(int32_t,int32_t);
extern int32_t 되돌림흐름접속번호(int32_t),되돌림흐름상대(int32_t),되돌림흐름닫기(int32_t);
static int 외부연결[24];
static int 임의주소[24], 양쪽수신창구[24], 전문외부상대[8], 묶인주소[8];
static int 외부번호(int ffeil_dolen) { return ffeil_dolen>=32 && ffeil_dolen<56 ? 외부연결[ffeil_dolen-32]-1 : -1; }
static int gludo_SMS(int ffeil_dolen,int TYPE_ardal) {
    if(ffeil_dolen<32||ffeil_dolen>=56)return -9;int 이전=외부번호(ffeil_dolen);if(이전>=0)return 이전;
    int eitem_COUNT=통신끝점만들기(TYPE_ardal);if(eitem_COUNT>=0)외부연결[ffeil_dolen-32]=eitem_COUNT+1;return eitem_COUNT;
}
int32_t 자바전문만들기(int32_t 첫째값,int32_t SECOND_VALUE,int32_t cod_nod){return 되돌림전문만들기(첫째값,SECOND_VALUE,cod_nod);}
int32_t 자바전문묶기(int32_t ffeil_dolen,int32_t cyfeiriad_rhyngrwyd,int32_t rhif_porth){
    if(cyfeiriad_rhyngrwyd==0x7f000001)return 되돌림전문묶기(ffeil_dolen,cyfeiriad_rhyngrwyd,rhif_porth);
    if(cyfeiriad_rhyngrwyd!=0&&cyfeiriad_rhyngrwyd!=망상태읽기(0,0))return -99;
    int 반환값=되돌림전문묶기(ffeil_dolen,0,rhif_porth);if(반환값<0)return 반환값;
    int eitem_COUNT=gludo_SMS(ffeil_dolen,2);if(eitem_COUNT<0)return eitem_COUNT;반환값=망주소묶기(eitem_COUNT,망상태읽기(0,0),되돌림전문접속번호(ffeil_dolen));if(!반환값)묶인주소[ffeil_dolen-32]=cyfeiriad_rhyngrwyd;return 반환값;
}
int32_t 자바전문보내기(int32_t ffeil_dolen,int32_t cyfeiriad_rhyngrwyd,int32_t rhif_porth,int32_t Maint){
    if(cyfeiriad_rhyngrwyd==0x7f000001)return 되돌림전문보내기(ffeil_dolen,cyfeiriad_rhyngrwyd,rhif_porth,Maint);
    if(Maint<0||Maint>512)return -90;if(rhif_porth<1||rhif_porth>65535)return -22;
    if(되돌림전문접속번호(ffeil_dolen)<0)return -9;
    if(되돌림전문주소(ffeil_dolen)==0x7f000001)return -101;
    int eitem_COUNT=외부번호(ffeil_dolen);if(eitem_COUNT<0){int 반환값=0;if(되돌림전문접속번호(ffeil_dolen)==0)반환값=되돌림전문묶기(ffeil_dolen,0,0);if(반환값<0)return 반환값;eitem_COUNT=gludo_SMS(ffeil_dolen,2);if(eitem_COUNT<0)return eitem_COUNT;반환값=망주소묶기(eitem_COUNT,망상태읽기(0,0),되돌림전문접속번호(ffeil_dolen));if(반환값<0)return 반환값;}
    unsigned char data[512];for(int 순번=0;순번<Maint;순번++)data[순번]=자바전문얻기(순번);return 전문보내기(eitem_COUNT,data,Maint,cyfeiriad_rhyngrwyd,rhif_porth);
}
int32_t 자바전문받기(int32_t ffeil_dolen,int32_t Maint){
    int eitem_COUNT=외부번호(ffeil_dolen);if(eitem_COUNT<0)return 되돌림전문받기(ffeil_dolen,Maint);if(Maint<0||Maint>512)return -22;
    int lleol=되돌림전문받기(ffeil_dolen,Maint);if(lleol!=-11){전문외부상대[ffeil_dolen-32]=0;return lleol;}
    unsigned char data[512];int 반환값=전문받기(eitem_COUNT,data,Maint);if(반환값>=0)전문외부상대[ffeil_dolen-32]=1;for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,data[순번]);return 반환값;
}
int32_t 자바전문접속번호(int32_t ffeil_dolen){int eitem_COUNT=외부번호(ffeil_dolen);return eitem_COUNT<0?되돌림전문접속번호(ffeil_dolen):(int32_t)Rhwydwaith_rhif_porth(eitem_COUNT);}
int32_t 자바전문주소(int32_t ffeil_dolen){return 외부번호(ffeil_dolen)<0?되돌림전문주소(ffeil_dolen):묶인주소[ffeil_dolen-32];}
int32_t 자바전문상대(int32_t ffeil_dolen){int eitem_COUNT=외부번호(ffeil_dolen);return eitem_COUNT<0||!전문외부상대[ffeil_dolen-32]?되돌림전문상대(ffeil_dolen):(int32_t)cymar_rhif_porth(eitem_COUNT);}
int32_t 자바전문원격주소(int32_t ffeil_dolen){int eitem_COUNT=외부번호(ffeil_dolen);return eitem_COUNT<0||!전문외부상대[ffeil_dolen-32]?0x7f000001:(int32_t)상대통신주소(eitem_COUNT);}
int32_t 자바전문닫기(int32_t ffeil_dolen){int eitem_COUNT=외부번호(ffeil_dolen);if(eitem_COUNT>=0){cau_Rhwydwaith(eitem_COUNT);외부연결[ffeil_dolen-32]=0;}if(ffeil_dolen>=32&&ffeil_dolen<40)전문외부상대[ffeil_dolen-32]=묶인주소[ffeil_dolen-32]=0;return 되돌림전문닫기(ffeil_dolen);}
int32_t 자바흐름만들기(void){return 되돌림흐름만들기();}
int32_t 자바흐름묶기(int32_t ffeil_dolen,int32_t cyfeiriad_rhyngrwyd,int32_t rhif_porth){
    if(cyfeiriad_rhyngrwyd==0||cyfeiriad_rhyngrwyd==0x7f000001){int 반환값=되돌림흐름묶기(ffeil_dolen,cyfeiriad_rhyngrwyd,rhif_porth);if(!반환값)임의주소[ffeil_dolen-32]=cyfeiriad_rhyngrwyd==0;return 반환값;}
    if(cyfeiriad_rhyngrwyd!=망상태읽기(0,0))return -99;int 반환값=되돌림흐름묶기(ffeil_dolen,0,rhif_porth);if(반환값<0)return 반환값;
    int eitem_COUNT=gludo_SMS(ffeil_dolen,1);return eitem_COUNT<0?eitem_COUNT:망주소묶기(eitem_COUNT,cyfeiriad_rhyngrwyd,되돌림흐름접속번호(ffeil_dolen));
}
int32_t 자바흐름듣기(int32_t ffeil_dolen,int32_t 연결대기한도){
    int eitem_COUNT=외부번호(ffeil_dolen);if(eitem_COUNT<0){int 반환값=되돌림흐름듣기(ffeil_dolen,연결대기한도);if(반환값<0||!임의주소[ffeil_dolen-32])return 반환값;
        eitem_COUNT=gludo_SMS(ffeil_dolen,1);if(eitem_COUNT<0)return eitem_COUNT;반환값=망주소묶기(eitem_COUNT,망상태읽기(0,0),되돌림흐름접속번호(ffeil_dolen));if(반환값<0)return 반환값;양쪽수신창구[ffeil_dolen-32]=1;
    }return 연결대기한도<1?-22:연결기다리기(eitem_COUNT);
}
int32_t 자바흐름연결(int32_t ffeil_dolen,int32_t cyfeiriad_rhyngrwyd,int32_t rhif_porth){
    if(cyfeiriad_rhyngrwyd==0x7f000001 && 외부번호(ffeil_dolen)<0)return 되돌림흐름연결(ffeil_dolen,cyfeiriad_rhyngrwyd,rhif_porth);
    if(되돌림흐름접속번호(ffeil_dolen)<0)return -9;int eitem_COUNT=gludo_SMS(ffeil_dolen,1);return eitem_COUNT<0?eitem_COUNT:망연결하기(eitem_COUNT,cyfeiriad_rhyngrwyd,rhif_porth);
}
int32_t 자바흐름연결받기(int32_t ffeil_dolen){
    int eitem_COUNT=외부번호(ffeil_dolen);if(eitem_COUNT<0)return 되돌림흐름연결받기(ffeil_dolen);
    if(양쪽수신창구[ffeil_dolen-32]){int lleol=되돌림흐름연결받기(ffeil_dolen);if(lleol!=-11)return lleol;}
    int cymar_VALUE=망연결받기(eitem_COUNT);if(cymar_VALUE<0)return cymar_VALUE;
    int targed=되돌림흐름만들기();if(targed<0){cau_Rhwydwaith(cymar_VALUE);return targed;}외부연결[targed-32]=cymar_VALUE+1;return targed;
}
int32_t 자바흐름읽기(int32_t ffeil_dolen,int32_t Maint){
    int eitem_COUNT=외부번호(ffeil_dolen);if(eitem_COUNT<0)return 되돌림흐름읽기(ffeil_dolen,Maint);if(Maint<0||Maint>512)return -22;
    unsigned char data[512];int 반환값=통신읽기(eitem_COUNT,data,Maint);for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,data[순번]);return 반환값;
}
int32_t 자바흐름쓰기(int32_t ffeil_dolen,int32_t Maint){
    int eitem_COUNT=외부번호(ffeil_dolen);if(eitem_COUNT<0)return 되돌림흐름쓰기(ffeil_dolen,Maint);if(Maint<0||Maint>512)return -22;
    unsigned char data[512];for(int 순번=0;순번<Maint;순번++)data[순번]=자바전문얻기(순번);return 통신쓰기(eitem_COUNT,data,Maint);
}
int32_t 자바흐름접속번호(int32_t ffeil_dolen){int eitem_COUNT=외부번호(ffeil_dolen);return eitem_COUNT<0?되돌림흐름접속번호(ffeil_dolen):(int32_t)Rhwydwaith_rhif_porth(eitem_COUNT);}
int32_t 자바흐름상대(int32_t ffeil_dolen){int eitem_COUNT=외부번호(ffeil_dolen);return eitem_COUNT<0?되돌림흐름상대(ffeil_dolen):(int32_t)cymar_rhif_porth(eitem_COUNT);}
int32_t 자바흐름주소(int32_t ffeil_dolen){return 외부번호(ffeil_dolen)<0?0x7f000001:양쪽수신창구[ffeil_dolen-32]?0:망상태읽기(0,0);}
int32_t 자바흐름닫기(int32_t ffeil_dolen){int eitem_COUNT=외부번호(ffeil_dolen);if(eitem_COUNT>=0){cau_Rhwydwaith(eitem_COUNT);외부연결[ffeil_dolen-32]=0;}if(ffeil_dolen>=40&&ffeil_dolen<56)임의주소[ffeil_dolen-32]=양쪽수신창구[ffeil_dolen-32]=0;return 되돌림흐름닫기(ffeil_dolen);}
