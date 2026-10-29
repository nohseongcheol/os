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
static int 외부번호(int fiilde_jaggoode) { return fiilde_jaggoode>=32 && fiilde_jaggoode<56 ? 외부연결[fiilde_jaggoode-32]-1 : -1; }
static int ɗakkude_binndi(int fiilde_jaggoode,int 유형) {
    if(fiilde_jaggoode<32||fiilde_jaggoode>=56)return -9;int 이전=외부번호(fiilde_jaggoode);if(이전>=0)return 이전;
    int 개수=통신끝점만들기(유형);if(개수>=0)외부연결[fiilde_jaggoode-32]=개수+1;return 개수;
}
int32_t 자바전문만들기(int32_t 첫째값,int32_t 둘째값,int32_t 문자값){return 되돌림전문만들기(첫째값,둘째값,문자값);}
int32_t 자바전문묶기(int32_t fiilde_jaggoode,int32_t ñiiɓirde_enternet,int32_t 접속번호){
    if(ñiiɓirde_enternet==0x7f000001)return 되돌림전문묶기(fiilde_jaggoode,ñiiɓirde_enternet,접속번호);
    if(ñiiɓirde_enternet!=0&&ñiiɓirde_enternet!=망상태읽기(0,0))return -99;
    int 반환값=되돌림전문묶기(fiilde_jaggoode,0,접속번호);if(반환값<0)return 반환값;
    int 개수=ɗakkude_binndi(fiilde_jaggoode,2);if(개수<0)return 개수;반환값=망주소묶기(개수,망상태읽기(0,0),되돌림전문접속번호(fiilde_jaggoode));if(!반환값)묶인주소[fiilde_jaggoode-32]=ñiiɓirde_enternet;return 반환값;
}
int32_t 자바전문보내기(int32_t fiilde_jaggoode,int32_t ñiiɓirde_enternet,int32_t 접속번호,int32_t waylude_etannde){
    if(ñiiɓirde_enternet==0x7f000001)return 되돌림전문보내기(fiilde_jaggoode,ñiiɓirde_enternet,접속번호,waylude_etannde);
    if(waylude_etannde<0||waylude_etannde>512)return -90;if(접속번호<1||접속번호>65535)return -22;
    if(되돌림전문접속번호(fiilde_jaggoode)<0)return -9;
    if(되돌림전문주소(fiilde_jaggoode)==0x7f000001)return -101;
    int 개수=외부번호(fiilde_jaggoode);if(개수<0){int 반환값=0;if(되돌림전문접속번호(fiilde_jaggoode)==0)반환값=되돌림전문묶기(fiilde_jaggoode,0,0);if(반환값<0)return 반환값;개수=ɗakkude_binndi(fiilde_jaggoode,2);if(개수<0)return 개수;반환값=망주소묶기(개수,망상태읽기(0,0),되돌림전문접속번호(fiilde_jaggoode));if(반환값<0)return 반환값;}
    unsigned char keɓe[512];for(int 순번=0;순번<waylude_etannde;순번++)keɓe[순번]=자바전문얻기(순번);return 전문보내기(개수,keɓe,waylude_etannde,ñiiɓirde_enternet,접속번호);
}
int32_t 자바전문받기(int32_t fiilde_jaggoode,int32_t waylude_etannde){
    int 개수=외부번호(fiilde_jaggoode);if(개수<0)return 되돌림전문받기(fiilde_jaggoode,waylude_etannde);if(waylude_etannde<0||waylude_etannde>512)return -22;
    int nokkuwal=되돌림전문받기(fiilde_jaggoode,waylude_etannde);if(nokkuwal!=-11){전문외부상대[fiilde_jaggoode-32]=0;return nokkuwal;}
    unsigned char keɓe[512];int 반환값=전문받기(개수,keɓe,waylude_etannde);if(반환값>=0)전문외부상대[fiilde_jaggoode-32]=1;for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,keɓe[순번]);return 반환값;
}
int32_t 자바전문접속번호(int32_t fiilde_jaggoode){int 개수=외부번호(fiilde_jaggoode);return 개수<0?되돌림전문접속번호(fiilde_jaggoode):(int32_t)통신접속번호(개수);}
int32_t 자바전문주소(int32_t fiilde_jaggoode){return 외부번호(fiilde_jaggoode)<0?되돌림전문주소(fiilde_jaggoode):묶인주소[fiilde_jaggoode-32];}
int32_t 자바전문상대(int32_t fiilde_jaggoode){int 개수=외부번호(fiilde_jaggoode);return 개수<0||!전문외부상대[fiilde_jaggoode-32]?되돌림전문상대(fiilde_jaggoode):(int32_t)상대접속번호(개수);}
int32_t 자바전문원격주소(int32_t fiilde_jaggoode){int 개수=외부번호(fiilde_jaggoode);return 개수<0||!전문외부상대[fiilde_jaggoode-32]?0x7f000001:(int32_t)상대통신주소(개수);}
int32_t 자바전문닫기(int32_t fiilde_jaggoode){int 개수=외부번호(fiilde_jaggoode);if(개수>=0){uddude_laylaytol(개수);외부연결[fiilde_jaggoode-32]=0;}if(fiilde_jaggoode>=32&&fiilde_jaggoode<40)전문외부상대[fiilde_jaggoode-32]=묶인주소[fiilde_jaggoode-32]=0;return 되돌림전문닫기(fiilde_jaggoode);}
int32_t 자바흐름만들기(void){return 되돌림흐름만들기();}
int32_t 자바흐름묶기(int32_t fiilde_jaggoode,int32_t ñiiɓirde_enternet,int32_t 접속번호){
    if(ñiiɓirde_enternet==0||ñiiɓirde_enternet==0x7f000001){int 반환값=되돌림흐름묶기(fiilde_jaggoode,ñiiɓirde_enternet,접속번호);if(!반환값)임의주소[fiilde_jaggoode-32]=ñiiɓirde_enternet==0;return 반환값;}
    if(ñiiɓirde_enternet!=망상태읽기(0,0))return -99;int 반환값=되돌림흐름묶기(fiilde_jaggoode,0,접속번호);if(반환값<0)return 반환값;
    int 개수=ɗakkude_binndi(fiilde_jaggoode,1);return 개수<0?개수:망주소묶기(개수,ñiiɓirde_enternet,되돌림흐름접속번호(fiilde_jaggoode));
}
int32_t 자바흐름듣기(int32_t fiilde_jaggoode,int32_t 연결대기한도){
    int 개수=외부번호(fiilde_jaggoode);if(개수<0){int 반환값=되돌림흐름듣기(fiilde_jaggoode,연결대기한도);if(반환값<0||!임의주소[fiilde_jaggoode-32])return 반환값;
        개수=ɗakkude_binndi(fiilde_jaggoode,1);if(개수<0)return 개수;반환값=망주소묶기(개수,망상태읽기(0,0),되돌림흐름접속번호(fiilde_jaggoode));if(반환값<0)return 반환값;양쪽수신창구[fiilde_jaggoode-32]=1;
    }return 연결대기한도<1?-22:연결기다리기(개수);
}
int32_t 자바흐름연결(int32_t fiilde_jaggoode,int32_t ñiiɓirde_enternet,int32_t 접속번호){
    if(ñiiɓirde_enternet==0x7f000001 && 외부번호(fiilde_jaggoode)<0)return 되돌림흐름연결(fiilde_jaggoode,ñiiɓirde_enternet,접속번호);
    if(되돌림흐름접속번호(fiilde_jaggoode)<0)return -9;int 개수=ɗakkude_binndi(fiilde_jaggoode,1);return 개수<0?개수:망연결하기(개수,ñiiɓirde_enternet,접속번호);
}
int32_t 자바흐름연결받기(int32_t fiilde_jaggoode){
    int 개수=외부번호(fiilde_jaggoode);if(개수<0)return 되돌림흐름연결받기(fiilde_jaggoode);
    if(양쪽수신창구[fiilde_jaggoode-32]){int nokkuwal=되돌림흐름연결받기(fiilde_jaggoode);if(nokkuwal!=-11)return nokkuwal;}
    int giƴiraaɗo_njaru=망연결받기(개수);if(giƴiraaɗo_njaru<0)return giƴiraaɗo_njaru;
    int faandaare=되돌림흐름만들기();if(faandaare<0){uddude_laylaytol(giƴiraaɗo_njaru);return faandaare;}외부연결[faandaare-32]=giƴiraaɗo_njaru+1;return faandaare;
}
int32_t 자바흐름읽기(int32_t fiilde_jaggoode,int32_t waylude_etannde){
    int 개수=외부번호(fiilde_jaggoode);if(개수<0)return 되돌림흐름읽기(fiilde_jaggoode,waylude_etannde);if(waylude_etannde<0||waylude_etannde>512)return -22;
    unsigned char keɓe[512];int 반환값=통신읽기(개수,keɓe,waylude_etannde);for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,keɓe[순번]);return 반환값;
}
int32_t 자바흐름쓰기(int32_t fiilde_jaggoode,int32_t waylude_etannde){
    int 개수=외부번호(fiilde_jaggoode);if(개수<0)return 되돌림흐름쓰기(fiilde_jaggoode,waylude_etannde);if(waylude_etannde<0||waylude_etannde>512)return -22;
    unsigned char keɓe[512];for(int 순번=0;순번<waylude_etannde;순번++)keɓe[순번]=자바전문얻기(순번);return 통신쓰기(개수,keɓe,waylude_etannde);
}
int32_t 자바흐름접속번호(int32_t fiilde_jaggoode){int 개수=외부번호(fiilde_jaggoode);return 개수<0?되돌림흐름접속번호(fiilde_jaggoode):(int32_t)통신접속번호(개수);}
int32_t 자바흐름상대(int32_t fiilde_jaggoode){int 개수=외부번호(fiilde_jaggoode);return 개수<0?되돌림흐름상대(fiilde_jaggoode):(int32_t)상대접속번호(개수);}
int32_t 자바흐름주소(int32_t fiilde_jaggoode){return 외부번호(fiilde_jaggoode)<0?0x7f000001:양쪽수신창구[fiilde_jaggoode-32]?0:망상태읽기(0,0);}
int32_t 자바흐름닫기(int32_t fiilde_jaggoode){int 개수=외부번호(fiilde_jaggoode);if(개수>=0){uddude_laylaytol(개수);외부연결[fiilde_jaggoode-32]=0;}if(fiilde_jaggoode>=40&&fiilde_jaggoode<56)임의주소[fiilde_jaggoode-32]=양쪽수신창구[fiilde_jaggoode-32]=0;return 되돌림흐름닫기(fiilde_jaggoode);}
