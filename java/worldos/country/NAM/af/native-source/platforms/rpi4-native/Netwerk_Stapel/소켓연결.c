#include "../명명/기계연결이름.h"
/* Preserve the deterministic Java loopback endpoints; route external IPv4 to lwIP. */
#include "Netwerk_Stapel.h"
extern int32_t 되돌림전문만들기(int32_t,int32_t,int32_t), 되돌림전문묶기(int32_t,int32_t,int32_t);
extern int32_t 되돌림전문보내기(int32_t,int32_t,int32_t,int32_t), 되돌림전문받기(int32_t,int32_t);
extern int32_t 되돌림전문접속번호(int32_t), 되돌림전문주소(int32_t), 되돌림전문상대(int32_t), 되돌림전문닫기(int32_t);
extern int32_t 자바전문넣기(int32_t,int32_t),자바전문얻기(int32_t);
extern int32_t 되돌림흐름만들기(void),되돌림흐름묶기(int32_t,int32_t,int32_t),되돌림흐름듣기(int32_t,int32_t);
extern int32_t 되돌림흐름연결(int32_t,int32_t,int32_t),되돌림흐름연결받기(int32_t),되돌림흐름읽기(int32_t,int32_t),되돌림흐름쓰기(int32_t,int32_t);
extern int32_t 되돌림흐름접속번호(int32_t),되돌림흐름상대(int32_t),되돌림흐름닫기(int32_t);
static int 외부연결[24];
static int 임의주소[24], 양쪽수신창구[24], 전문외부상대[8], 묶인주소[8];
static int 외부번호(int lêer_handvatsel) { return lêer_handvatsel>=32 && lêer_handvatsel<56 ? 외부연결[lêer_handvatsel-32]-1 : -1; }
static int plak_SMS(int lêer_handvatsel,int TYPE_kategorie) {
    if(lêer_handvatsel<32||lêer_handvatsel>=56)return -9;int 이전=외부번호(lêer_handvatsel);if(이전>=0)return 이전;
    int item_COUNT=통신끝점만들기(TYPE_kategorie);if(item_COUNT>=0)외부연결[lêer_handvatsel-32]=item_COUNT+1;return item_COUNT;
}
int32_t 자바전문만들기(int32_t 첫째값,int32_t SECOND_VALUE,int32_t karakterkode){return 되돌림전문만들기(첫째값,SECOND_VALUE,karakterkode);}
int32_t 자바전문묶기(int32_t lêer_handvatsel,int32_t internetadres,int32_t 접속번호){
    if(internetadres==0x7f000001)return 되돌림전문묶기(lêer_handvatsel,internetadres,접속번호);
    if(internetadres!=0&&internetadres!=망상태읽기(0,0))return -99;
    int 반환값=되돌림전문묶기(lêer_handvatsel,0,접속번호);if(반환값<0)return 반환값;
    int item_COUNT=plak_SMS(lêer_handvatsel,2);if(item_COUNT<0)return item_COUNT;반환값=망주소묶기(item_COUNT,망상태읽기(0,0),되돌림전문접속번호(lêer_handvatsel));if(!반환값)묶인주소[lêer_handvatsel-32]=internetadres;return 반환값;
}
int32_t 자바전문보내기(int32_t lêer_handvatsel,int32_t internetadres,int32_t 접속번호,int32_t Grootte){
    if(internetadres==0x7f000001)return 되돌림전문보내기(lêer_handvatsel,internetadres,접속번호,Grootte);
    if(Grootte<0||Grootte>512)return -90;if(접속번호<1||접속번호>65535)return -22;
    if(되돌림전문접속번호(lêer_handvatsel)<0)return -9;
    if(되돌림전문주소(lêer_handvatsel)==0x7f000001)return -101;
    int item_COUNT=외부번호(lêer_handvatsel);if(item_COUNT<0){int 반환값=0;if(되돌림전문접속번호(lêer_handvatsel)==0)반환값=되돌림전문묶기(lêer_handvatsel,0,0);if(반환값<0)return 반환값;item_COUNT=plak_SMS(lêer_handvatsel,2);if(item_COUNT<0)return item_COUNT;반환값=망주소묶기(item_COUNT,망상태읽기(0,0),되돌림전문접속번호(lêer_handvatsel));if(반환값<0)return 반환값;}
    unsigned char data[512];for(int 순번=0;순번<Grootte;순번++)data[순번]=자바전문얻기(순번);return 전문보내기(item_COUNT,data,Grootte,internetadres,접속번호);
}
int32_t 자바전문받기(int32_t lêer_handvatsel,int32_t Grootte){
    int item_COUNT=외부번호(lêer_handvatsel);if(item_COUNT<0)return 되돌림전문받기(lêer_handvatsel,Grootte);if(Grootte<0||Grootte>512)return -22;
    int lokaal=되돌림전문받기(lêer_handvatsel,Grootte);if(lokaal!=-11){전문외부상대[lêer_handvatsel-32]=0;return lokaal;}
    unsigned char data[512];int 반환값=전문받기(item_COUNT,data,Grootte);if(반환값>=0)전문외부상대[lêer_handvatsel-32]=1;for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,data[순번]);return 반환값;
}
int32_t 자바전문접속번호(int32_t lêer_handvatsel){int item_COUNT=외부번호(lêer_handvatsel);return item_COUNT<0?되돌림전문접속번호(lêer_handvatsel):(int32_t)통신접속번호(item_COUNT);}
int32_t 자바전문주소(int32_t lêer_handvatsel){return 외부번호(lêer_handvatsel)<0?되돌림전문주소(lêer_handvatsel):묶인주소[lêer_handvatsel-32];}
int32_t 자바전문상대(int32_t lêer_handvatsel){int item_COUNT=외부번호(lêer_handvatsel);return item_COUNT<0||!전문외부상대[lêer_handvatsel-32]?되돌림전문상대(lêer_handvatsel):(int32_t)상대접속번호(item_COUNT);}
int32_t 자바전문원격주소(int32_t lêer_handvatsel){int item_COUNT=외부번호(lêer_handvatsel);return item_COUNT<0||!전문외부상대[lêer_handvatsel-32]?0x7f000001:(int32_t)상대통신주소(item_COUNT);}
int32_t 자바전문닫기(int32_t lêer_handvatsel){int item_COUNT=외부번호(lêer_handvatsel);if(item_COUNT>=0){sluit_Netwerk(item_COUNT);외부연결[lêer_handvatsel-32]=0;}if(lêer_handvatsel>=32&&lêer_handvatsel<40)전문외부상대[lêer_handvatsel-32]=묶인주소[lêer_handvatsel-32]=0;return 되돌림전문닫기(lêer_handvatsel);}
int32_t 자바흐름만들기(void){return 되돌림흐름만들기();}
int32_t 자바흐름묶기(int32_t lêer_handvatsel,int32_t internetadres,int32_t 접속번호){
    if(internetadres==0||internetadres==0x7f000001){int 반환값=되돌림흐름묶기(lêer_handvatsel,internetadres,접속번호);if(!반환값)임의주소[lêer_handvatsel-32]=internetadres==0;return 반환값;}
    if(internetadres!=망상태읽기(0,0))return -99;int 반환값=되돌림흐름묶기(lêer_handvatsel,0,접속번호);if(반환값<0)return 반환값;
    int item_COUNT=plak_SMS(lêer_handvatsel,1);return item_COUNT<0?item_COUNT:망주소묶기(item_COUNT,internetadres,되돌림흐름접속번호(lêer_handvatsel));
}
int32_t 자바흐름듣기(int32_t lêer_handvatsel,int32_t 연결대기한도){
    int item_COUNT=외부번호(lêer_handvatsel);if(item_COUNT<0){int 반환값=되돌림흐름듣기(lêer_handvatsel,연결대기한도);if(반환값<0||!임의주소[lêer_handvatsel-32])return 반환값;
        item_COUNT=plak_SMS(lêer_handvatsel,1);if(item_COUNT<0)return item_COUNT;반환값=망주소묶기(item_COUNT,망상태읽기(0,0),되돌림흐름접속번호(lêer_handvatsel));if(반환값<0)return 반환값;양쪽수신창구[lêer_handvatsel-32]=1;
    }return 연결대기한도<1?-22:연결기다리기(item_COUNT);
}
int32_t 자바흐름연결(int32_t lêer_handvatsel,int32_t internetadres,int32_t 접속번호){
    if(internetadres==0x7f000001 && 외부번호(lêer_handvatsel)<0)return 되돌림흐름연결(lêer_handvatsel,internetadres,접속번호);
    if(되돌림흐름접속번호(lêer_handvatsel)<0)return -9;int item_COUNT=plak_SMS(lêer_handvatsel,1);return item_COUNT<0?item_COUNT:망연결하기(item_COUNT,internetadres,접속번호);
}
int32_t 자바흐름연결받기(int32_t lêer_handvatsel){
    int item_COUNT=외부번호(lêer_handvatsel);if(item_COUNT<0)return 되돌림흐름연결받기(lêer_handvatsel);
    if(양쪽수신창구[lêer_handvatsel-32]){int lokaal=되돌림흐름연결받기(lêer_handvatsel);if(lokaal!=-11)return lokaal;}
    int portuur_VALUE=망연결받기(item_COUNT);if(portuur_VALUE<0)return portuur_VALUE;
    int teiken=되돌림흐름만들기();if(teiken<0){sluit_Netwerk(portuur_VALUE);return teiken;}외부연결[teiken-32]=portuur_VALUE+1;return teiken;
}
int32_t 자바흐름읽기(int32_t lêer_handvatsel,int32_t Grootte){
    int item_COUNT=외부번호(lêer_handvatsel);if(item_COUNT<0)return 되돌림흐름읽기(lêer_handvatsel,Grootte);if(Grootte<0||Grootte>512)return -22;
    unsigned char data[512];int 반환값=통신읽기(item_COUNT,data,Grootte);for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,data[순번]);return 반환값;
}
int32_t 자바흐름쓰기(int32_t lêer_handvatsel,int32_t Grootte){
    int item_COUNT=외부번호(lêer_handvatsel);if(item_COUNT<0)return 되돌림흐름쓰기(lêer_handvatsel,Grootte);if(Grootte<0||Grootte>512)return -22;
    unsigned char data[512];for(int 순번=0;순번<Grootte;순번++)data[순번]=자바전문얻기(순번);return 통신쓰기(item_COUNT,data,Grootte);
}
int32_t 자바흐름접속번호(int32_t lêer_handvatsel){int item_COUNT=외부번호(lêer_handvatsel);return item_COUNT<0?되돌림흐름접속번호(lêer_handvatsel):(int32_t)통신접속번호(item_COUNT);}
int32_t 자바흐름상대(int32_t lêer_handvatsel){int item_COUNT=외부번호(lêer_handvatsel);return item_COUNT<0?되돌림흐름상대(lêer_handvatsel):(int32_t)상대접속번호(item_COUNT);}
int32_t 자바흐름주소(int32_t lêer_handvatsel){return 외부번호(lêer_handvatsel)<0?0x7f000001:양쪽수신창구[lêer_handvatsel-32]?0:망상태읽기(0,0);}
int32_t 자바흐름닫기(int32_t lêer_handvatsel){int item_COUNT=외부번호(lêer_handvatsel);if(item_COUNT>=0){sluit_Netwerk(item_COUNT);외부연결[lêer_handvatsel-32]=0;}if(lêer_handvatsel>=40&&lêer_handvatsel<56)임의주소[lêer_handvatsel-32]=양쪽수신창구[lêer_handvatsel-32]=0;return 되돌림흐름닫기(lêer_handvatsel);}
