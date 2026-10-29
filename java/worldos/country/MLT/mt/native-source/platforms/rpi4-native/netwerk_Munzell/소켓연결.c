#include "../명명/기계연결이름.h"
/* Preserve the deterministic Java loopback endpoints; route external IPv4 to lwIP. */
#include "netwerk_Munzell.h"
extern int32_t 되돌림전문만들기(int32_t,int32_t,int32_t), 되돌림전문묶기(int32_t,int32_t,int32_t);
extern int32_t 되돌림전문보내기(int32_t,int32_t,int32_t,int32_t), 되돌림전문받기(int32_t,int32_t);
extern int32_t 되돌림전문접속번호(int32_t), 되돌림전문주소(int32_t), 되돌림전문상대(int32_t), 되돌림전문닫기(int32_t);
extern int32_t 자바전문넣기(int32_t,int32_t),자바전문얻기(int32_t);
extern int32_t 되돌림흐름만들기(void),되돌림흐름묶기(int32_t,int32_t,int32_t),되돌림흐름듣기(int32_t,int32_t);
extern int32_t 되돌림흐름연결(int32_t,int32_t,int32_t),되돌림흐름연결받기(int32_t),되돌림흐름읽기(int32_t,int32_t),되돌림흐름쓰기(int32_t,int32_t);
extern int32_t 되돌림흐름접속번호(int32_t),되돌림흐름상대(int32_t),되돌림흐름닫기(int32_t);
static int 외부연결[24];
static int 임의주소[24], 양쪽수신창구[24], 전문외부상대[8], 묶인주소[8];
static int 외부번호(int fajl_handle) { return fajl_handle>=32 && fajl_handle<56 ? 외부연결[fajl_handle-32]-1 : -1; }
static int ppejstja_SMS(int fajl_handle,int TYPE_kategorija) {
    if(fajl_handle<32||fajl_handle>=56)return -9;int 이전=외부번호(fajl_handle);if(이전>=0)return 이전;
    int element_COUNT=통신끝점만들기(TYPE_kategorija);if(element_COUNT>=0)외부연결[fajl_handle-32]=element_COUNT+1;return element_COUNT;
}
int32_t 자바전문만들기(int32_t 첫째값,int32_t SECOND_VALUE,int32_t kodiċi_tal_karattru){return 되돌림전문만들기(첫째값,SECOND_VALUE,kodiċi_tal_karattru);}
int32_t 자바전문묶기(int32_t fajl_handle,int32_t indirizz_tal_Internet,int32_t 접속번호){
    if(indirizz_tal_Internet==0x7f000001)return 되돌림전문묶기(fajl_handle,indirizz_tal_Internet,접속번호);
    if(indirizz_tal_Internet!=0&&indirizz_tal_Internet!=망상태읽기(0,0))return -99;
    int 반환값=되돌림전문묶기(fajl_handle,0,접속번호);if(반환값<0)return 반환값;
    int element_COUNT=ppejstja_SMS(fajl_handle,2);if(element_COUNT<0)return element_COUNT;반환값=망주소묶기(element_COUNT,망상태읽기(0,0),되돌림전문접속번호(fajl_handle));if(!반환값)묶인주소[fajl_handle-32]=indirizz_tal_Internet;return 반환값;
}
int32_t 자바전문보내기(int32_t fajl_handle,int32_t indirizz_tal_Internet,int32_t 접속번호,int32_t daqqas){
    if(indirizz_tal_Internet==0x7f000001)return 되돌림전문보내기(fajl_handle,indirizz_tal_Internet,접속번호,daqqas);
    if(daqqas<0||daqqas>512)return -90;if(접속번호<1||접속번호>65535)return -22;
    if(되돌림전문접속번호(fajl_handle)<0)return -9;
    if(되돌림전문주소(fajl_handle)==0x7f000001)return -101;
    int element_COUNT=외부번호(fajl_handle);if(element_COUNT<0){int 반환값=0;if(되돌림전문접속번호(fajl_handle)==0)반환값=되돌림전문묶기(fajl_handle,0,0);if(반환값<0)return 반환값;element_COUNT=ppejstja_SMS(fajl_handle,2);if(element_COUNT<0)return element_COUNT;반환값=망주소묶기(element_COUNT,망상태읽기(0,0),되돌림전문접속번호(fajl_handle));if(반환값<0)return 반환값;}
    unsigned char data[512];for(int 순번=0;순번<daqqas;순번++)data[순번]=자바전문얻기(순번);return 전문보내기(element_COUNT,data,daqqas,indirizz_tal_Internet,접속번호);
}
int32_t 자바전문받기(int32_t fajl_handle,int32_t daqqas){
    int element_COUNT=외부번호(fajl_handle);if(element_COUNT<0)return 되돌림전문받기(fajl_handle,daqqas);if(daqqas<0||daqqas>512)return -22;
    int lokali=되돌림전문받기(fajl_handle,daqqas);if(lokali!=-11){전문외부상대[fajl_handle-32]=0;return lokali;}
    unsigned char data[512];int 반환값=전문받기(element_COUNT,data,daqqas);if(반환값>=0)전문외부상대[fajl_handle-32]=1;for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,data[순번]);return 반환값;
}
int32_t 자바전문접속번호(int32_t fajl_handle){int element_COUNT=외부번호(fajl_handle);return element_COUNT<0?되돌림전문접속번호(fajl_handle):(int32_t)통신접속번호(element_COUNT);}
int32_t 자바전문주소(int32_t fajl_handle){return 외부번호(fajl_handle)<0?되돌림전문주소(fajl_handle):묶인주소[fajl_handle-32];}
int32_t 자바전문상대(int32_t fajl_handle){int element_COUNT=외부번호(fajl_handle);return element_COUNT<0||!전문외부상대[fajl_handle-32]?되돌림전문상대(fajl_handle):(int32_t)상대접속번호(element_COUNT);}
int32_t 자바전문원격주소(int32_t fajl_handle){int element_COUNT=외부번호(fajl_handle);return element_COUNT<0||!전문외부상대[fajl_handle-32]?0x7f000001:(int32_t)상대통신주소(element_COUNT);}
int32_t 자바전문닫기(int32_t fajl_handle){int element_COUNT=외부번호(fajl_handle);if(element_COUNT>=0){agħlaq_netwerk(element_COUNT);외부연결[fajl_handle-32]=0;}if(fajl_handle>=32&&fajl_handle<40)전문외부상대[fajl_handle-32]=묶인주소[fajl_handle-32]=0;return 되돌림전문닫기(fajl_handle);}
int32_t 자바흐름만들기(void){return 되돌림흐름만들기();}
int32_t 자바흐름묶기(int32_t fajl_handle,int32_t indirizz_tal_Internet,int32_t 접속번호){
    if(indirizz_tal_Internet==0||indirizz_tal_Internet==0x7f000001){int 반환값=되돌림흐름묶기(fajl_handle,indirizz_tal_Internet,접속번호);if(!반환값)임의주소[fajl_handle-32]=indirizz_tal_Internet==0;return 반환값;}
    if(indirizz_tal_Internet!=망상태읽기(0,0))return -99;int 반환값=되돌림흐름묶기(fajl_handle,0,접속번호);if(반환값<0)return 반환값;
    int element_COUNT=ppejstja_SMS(fajl_handle,1);return element_COUNT<0?element_COUNT:망주소묶기(element_COUNT,indirizz_tal_Internet,되돌림흐름접속번호(fajl_handle));
}
int32_t 자바흐름듣기(int32_t fajl_handle,int32_t 연결대기한도){
    int element_COUNT=외부번호(fajl_handle);if(element_COUNT<0){int 반환값=되돌림흐름듣기(fajl_handle,연결대기한도);if(반환값<0||!임의주소[fajl_handle-32])return 반환값;
        element_COUNT=ppejstja_SMS(fajl_handle,1);if(element_COUNT<0)return element_COUNT;반환값=망주소묶기(element_COUNT,망상태읽기(0,0),되돌림흐름접속번호(fajl_handle));if(반환값<0)return 반환값;양쪽수신창구[fajl_handle-32]=1;
    }return 연결대기한도<1?-22:연결기다리기(element_COUNT);
}
int32_t 자바흐름연결(int32_t fajl_handle,int32_t indirizz_tal_Internet,int32_t 접속번호){
    if(indirizz_tal_Internet==0x7f000001 && 외부번호(fajl_handle)<0)return 되돌림흐름연결(fajl_handle,indirizz_tal_Internet,접속번호);
    if(되돌림흐름접속번호(fajl_handle)<0)return -9;int element_COUNT=ppejstja_SMS(fajl_handle,1);return element_COUNT<0?element_COUNT:망연결하기(element_COUNT,indirizz_tal_Internet,접속번호);
}
int32_t 자바흐름연결받기(int32_t fajl_handle){
    int element_COUNT=외부번호(fajl_handle);if(element_COUNT<0)return 되돌림흐름연결받기(fajl_handle);
    if(양쪽수신창구[fajl_handle-32]){int lokali=되돌림흐름연결받기(fajl_handle);if(lokali!=-11)return lokali;}
    int peer_VALUE=망연결받기(element_COUNT);if(peer_VALUE<0)return peer_VALUE;
    int mira=되돌림흐름만들기();if(mira<0){agħlaq_netwerk(peer_VALUE);return mira;}외부연결[mira-32]=peer_VALUE+1;return mira;
}
int32_t 자바흐름읽기(int32_t fajl_handle,int32_t daqqas){
    int element_COUNT=외부번호(fajl_handle);if(element_COUNT<0)return 되돌림흐름읽기(fajl_handle,daqqas);if(daqqas<0||daqqas>512)return -22;
    unsigned char data[512];int 반환값=통신읽기(element_COUNT,data,daqqas);for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,data[순번]);return 반환값;
}
int32_t 자바흐름쓰기(int32_t fajl_handle,int32_t daqqas){
    int element_COUNT=외부번호(fajl_handle);if(element_COUNT<0)return 되돌림흐름쓰기(fajl_handle,daqqas);if(daqqas<0||daqqas>512)return -22;
    unsigned char data[512];for(int 순번=0;순번<daqqas;순번++)data[순번]=자바전문얻기(순번);return 통신쓰기(element_COUNT,data,daqqas);
}
int32_t 자바흐름접속번호(int32_t fajl_handle){int element_COUNT=외부번호(fajl_handle);return element_COUNT<0?되돌림흐름접속번호(fajl_handle):(int32_t)통신접속번호(element_COUNT);}
int32_t 자바흐름상대(int32_t fajl_handle){int element_COUNT=외부번호(fajl_handle);return element_COUNT<0?되돌림흐름상대(fajl_handle):(int32_t)상대접속번호(element_COUNT);}
int32_t 자바흐름주소(int32_t fajl_handle){return 외부번호(fajl_handle)<0?0x7f000001:양쪽수신창구[fajl_handle-32]?0:망상태읽기(0,0);}
int32_t 자바흐름닫기(int32_t fajl_handle){int element_COUNT=외부번호(fajl_handle);if(element_COUNT>=0){agħlaq_netwerk(element_COUNT);외부연결[fajl_handle-32]=0;}if(fajl_handle>=40&&fajl_handle<56)임의주소[fajl_handle-32]=양쪽수신창구[fajl_handle-32]=0;return 되돌림흐름닫기(fajl_handle);}
