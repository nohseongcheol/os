#include "../명명/기계연결이름.h"
/* Preserve the deterministic Java loopback endpoints; route external IPv4 to lwIP. */
#include "통신망.h"
extern int32_t 되돌림전문만들기(int32_t,int32_t,int32_t), 되돌림전문묶기(int32_t,int32_t,int32_t);
extern int32_t 되돌림전문보내기(int32_t,int32_t,int32_t,int32_t), 되돌림전문받기(int32_t,int32_t);
extern int32_t 되돌림전문접속번호(int32_t), 되돌림전문주소(int32_t), 되돌림전문상대(int32_t), 되돌림전문닫기(int32_t);
extern int32_t 자바전문넣기(int32_t,int32_t),자바전문얻기(int32_t);
extern int32_t 되돌림흐름만들기(void),되돌림흐름묶기(int32_t,int32_t,int32_t),되돌림흐름듣기(int32_t,int32_t);
extern int32_t 되돌림흐름연결(int32_t,int32_t,int32_t),되돌림흐름연결받기(int32_t),되돌림흐름읽기(int32_t,int32_t),되돌림흐름쓰기(int32_t,int32_t);
extern int32_t 되돌림흐름접속번호(int32_t),되돌림흐름상대(int32_t),되돌림흐름닫기(int32_t);
static int 외부연결[24];
static int 임의주소[24], 양쪽수신창구[24], 전문외부상대[8], 묶인주소[8];
static int 외부번호(int anaajaalaa_aapaaya) { return anaajaalaa_aapaaya>=32 && anaajaalaa_aapaaya<56 ? 외부연결[anaajaalaa_aapaaya-32]-1 : -1; }
static int 붙이기(int anaajaalaa_aapaaya,int 유형) {
    if(anaajaalaa_aapaaya<32||anaajaalaa_aapaaya>=56)return -9;int 이전=외부번호(anaajaalaa_aapaaya);if(이전>=0)return 이전;
    int 개수=통신끝점만들기(유형);if(개수>=0)외부연결[anaajaalaa_aapaaya-32]=개수+1;return 개수;
}
int32_t 자바전문만들기(int32_t 첫째값,int32_t 둘째값,int32_t 문자값){return 되돌림전문만들기(첫째값,둘째값,문자값);}
int32_t 자바전문묶기(int32_t anaajaalaa_aapaaya,int32_t ejepüsee_Internet,int32_t 접속번호){
    if(ejepüsee_Internet==0x7f000001)return 되돌림전문묶기(anaajaalaa_aapaaya,ejepüsee_Internet,접속번호);
    if(ejepüsee_Internet!=0&&ejepüsee_Internet!=망상태읽기(0,0))return -99;
    int 반환값=되돌림전문묶기(anaajaalaa_aapaaya,0,접속번호);if(반환값<0)return 반환값;
    int 개수=붙이기(anaajaalaa_aapaaya,2);if(개수<0)return 개수;반환값=망주소묶기(개수,망상태읽기(0,0),되돌림전문접속번호(anaajaalaa_aapaaya));if(!반환값)묶인주소[anaajaalaa_aapaaya-32]=ejepüsee_Internet;return 반환값;
}
int32_t 자바전문보내기(int32_t anaajaalaa_aapaaya,int32_t ejepüsee_Internet,int32_t 접속번호,int32_t 크기){
    if(ejepüsee_Internet==0x7f000001)return 되돌림전문보내기(anaajaalaa_aapaaya,ejepüsee_Internet,접속번호,크기);
    if(크기<0||크기>512)return -90;if(접속번호<1||접속번호>65535)return -22;
    if(되돌림전문접속번호(anaajaalaa_aapaaya)<0)return -9;
    if(되돌림전문주소(anaajaalaa_aapaaya)==0x7f000001)return -101;
    int 개수=외부번호(anaajaalaa_aapaaya);if(개수<0){int 반환값=0;if(되돌림전문접속번호(anaajaalaa_aapaaya)==0)반환값=되돌림전문묶기(anaajaalaa_aapaaya,0,0);if(반환값<0)return 반환값;개수=붙이기(anaajaalaa_aapaaya,2);if(개수<0)return 개수;반환값=망주소묶기(개수,망상태읽기(0,0),되돌림전문접속번호(anaajaalaa_aapaaya));if(반환값<0)return 반환값;}
    unsigned char atijaaya[512];for(int 순번=0;순번<크기;순번++)atijaaya[순번]=자바전문얻기(순번);return 전문보내기(개수,atijaaya,크기,ejepüsee_Internet,접속번호);
}
int32_t 자바전문받기(int32_t anaajaalaa_aapaaya,int32_t 크기){
    int 개수=외부번호(anaajaalaa_aapaaya);if(개수<0)return 되돌림전문받기(anaajaalaa_aapaaya,크기);if(크기<0||크기>512)return -22;
    int 내부값=되돌림전문받기(anaajaalaa_aapaaya,크기);if(내부값!=-11){전문외부상대[anaajaalaa_aapaaya-32]=0;return 내부값;}
    unsigned char atijaaya[512];int 반환값=전문받기(개수,atijaaya,크기);if(반환값>=0)전문외부상대[anaajaalaa_aapaaya-32]=1;for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,atijaaya[순번]);return 반환값;
}
int32_t 자바전문접속번호(int32_t anaajaalaa_aapaaya){int 개수=외부번호(anaajaalaa_aapaaya);return 개수<0?되돌림전문접속번호(anaajaalaa_aapaaya):(int32_t)통신접속번호(개수);}
int32_t 자바전문주소(int32_t anaajaalaa_aapaaya){return 외부번호(anaajaalaa_aapaaya)<0?되돌림전문주소(anaajaalaa_aapaaya):묶인주소[anaajaalaa_aapaaya-32];}
int32_t 자바전문상대(int32_t anaajaalaa_aapaaya){int 개수=외부번호(anaajaalaa_aapaaya);return 개수<0||!전문외부상대[anaajaalaa_aapaaya-32]?되돌림전문상대(anaajaalaa_aapaaya):(int32_t)상대접속번호(개수);}
int32_t 자바전문원격주소(int32_t anaajaalaa_aapaaya){int 개수=외부번호(anaajaalaa_aapaaya);return 개수<0||!전문외부상대[anaajaalaa_aapaaya-32]?0x7f000001:(int32_t)상대통신주소(개수);}
int32_t 자바전문닫기(int32_t anaajaalaa_aapaaya){int 개수=외부번호(anaajaalaa_aapaaya);if(개수>=0){asürülaa_kusu(개수);외부연결[anaajaalaa_aapaaya-32]=0;}if(anaajaalaa_aapaaya>=32&&anaajaalaa_aapaaya<40)전문외부상대[anaajaalaa_aapaaya-32]=묶인주소[anaajaalaa_aapaaya-32]=0;return 되돌림전문닫기(anaajaalaa_aapaaya);}
int32_t 자바흐름만들기(void){return 되돌림흐름만들기();}
int32_t 자바흐름묶기(int32_t anaajaalaa_aapaaya,int32_t ejepüsee_Internet,int32_t 접속번호){
    if(ejepüsee_Internet==0||ejepüsee_Internet==0x7f000001){int 반환값=되돌림흐름묶기(anaajaalaa_aapaaya,ejepüsee_Internet,접속번호);if(!반환값)임의주소[anaajaalaa_aapaaya-32]=ejepüsee_Internet==0;return 반환값;}
    if(ejepüsee_Internet!=망상태읽기(0,0))return -99;int 반환값=되돌림흐름묶기(anaajaalaa_aapaaya,0,접속번호);if(반환값<0)return 반환값;
    int 개수=붙이기(anaajaalaa_aapaaya,1);return 개수<0?개수:망주소묶기(개수,ejepüsee_Internet,되돌림흐름접속번호(anaajaalaa_aapaaya));
}
int32_t 자바흐름듣기(int32_t anaajaalaa_aapaaya,int32_t 연결대기한도){
    int 개수=외부번호(anaajaalaa_aapaaya);if(개수<0){int 반환값=되돌림흐름듣기(anaajaalaa_aapaaya,연결대기한도);if(반환값<0||!임의주소[anaajaalaa_aapaaya-32])return 반환값;
        개수=붙이기(anaajaalaa_aapaaya,1);if(개수<0)return 개수;반환값=망주소묶기(개수,망상태읽기(0,0),되돌림흐름접속번호(anaajaalaa_aapaaya));if(반환값<0)return 반환값;양쪽수신창구[anaajaalaa_aapaaya-32]=1;
    }return 연결대기한도<1?-22:연결기다리기(개수);
}
int32_t 자바흐름연결(int32_t anaajaalaa_aapaaya,int32_t ejepüsee_Internet,int32_t 접속번호){
    if(ejepüsee_Internet==0x7f000001 && 외부번호(anaajaalaa_aapaaya)<0)return 되돌림흐름연결(anaajaalaa_aapaaya,ejepüsee_Internet,접속번호);
    if(되돌림흐름접속번호(anaajaalaa_aapaaya)<0)return -9;int 개수=붙이기(anaajaalaa_aapaaya,1);return 개수<0?개수:망연결하기(개수,ejepüsee_Internet,접속번호);
}
int32_t 자바흐름연결받기(int32_t anaajaalaa_aapaaya){
    int 개수=외부번호(anaajaalaa_aapaaya);if(개수<0)return 되돌림흐름연결받기(anaajaalaa_aapaaya);
    if(양쪽수신창구[anaajaalaa_aapaaya-32]){int 내부값=되돌림흐름연결받기(anaajaalaa_aapaaya);if(내부값!=-11)return 내부값;}
    int wanaawasü_ajutuu=망연결받기(개수);if(wanaawasü_ajutuu<0)return wanaawasü_ajutuu;
    int 대상=되돌림흐름만들기();if(대상<0){asürülaa_kusu(wanaawasü_ajutuu);return 대상;}외부연결[대상-32]=wanaawasü_ajutuu+1;return 대상;
}
int32_t 자바흐름읽기(int32_t anaajaalaa_aapaaya,int32_t 크기){
    int 개수=외부번호(anaajaalaa_aapaaya);if(개수<0)return 되돌림흐름읽기(anaajaalaa_aapaaya,크기);if(크기<0||크기>512)return -22;
    unsigned char atijaaya[512];int 반환값=통신읽기(개수,atijaaya,크기);for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,atijaaya[순번]);return 반환값;
}
int32_t 자바흐름쓰기(int32_t anaajaalaa_aapaaya,int32_t 크기){
    int 개수=외부번호(anaajaalaa_aapaaya);if(개수<0)return 되돌림흐름쓰기(anaajaalaa_aapaaya,크기);if(크기<0||크기>512)return -22;
    unsigned char atijaaya[512];for(int 순번=0;순번<크기;순번++)atijaaya[순번]=자바전문얻기(순번);return 통신쓰기(개수,atijaaya,크기);
}
int32_t 자바흐름접속번호(int32_t anaajaalaa_aapaaya){int 개수=외부번호(anaajaalaa_aapaaya);return 개수<0?되돌림흐름접속번호(anaajaalaa_aapaaya):(int32_t)통신접속번호(개수);}
int32_t 자바흐름상대(int32_t anaajaalaa_aapaaya){int 개수=외부번호(anaajaalaa_aapaaya);return 개수<0?되돌림흐름상대(anaajaalaa_aapaaya):(int32_t)상대접속번호(개수);}
int32_t 자바흐름주소(int32_t anaajaalaa_aapaaya){return 외부번호(anaajaalaa_aapaaya)<0?0x7f000001:양쪽수신창구[anaajaalaa_aapaaya-32]?0:망상태읽기(0,0);}
int32_t 자바흐름닫기(int32_t anaajaalaa_aapaaya){int 개수=외부번호(anaajaalaa_aapaaya);if(개수>=0){asürülaa_kusu(개수);외부연결[anaajaalaa_aapaaya-32]=0;}if(anaajaalaa_aapaaya>=40&&anaajaalaa_aapaaya<56)임의주소[anaajaalaa_aapaaya-32]=양쪽수신창구[anaajaalaa_aapaaya-32]=0;return 되돌림흐름닫기(anaajaalaa_aapaaya);}
