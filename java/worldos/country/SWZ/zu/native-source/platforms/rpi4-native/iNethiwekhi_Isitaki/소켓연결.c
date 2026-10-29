#include "../명명/기계연결이름.h"
/* Preserve the deterministic Java loopback endpoints; route external IPv4 to lwIP. */
#include "iNethiwekhi_Isitaki.h"
extern int32_t 되돌림전문만들기(int32_t,int32_t,int32_t), 되돌림전문묶기(int32_t,int32_t,int32_t);
extern int32_t 되돌림전문보내기(int32_t,int32_t,int32_t,int32_t), 되돌림전문받기(int32_t,int32_t);
extern int32_t 되돌림전문접속번호(int32_t), 되돌림전문주소(int32_t), 되돌림전문상대(int32_t), 되돌림전문닫기(int32_t);
extern int32_t 자바전문넣기(int32_t,int32_t),자바전문얻기(int32_t);
extern int32_t 되돌림흐름만들기(void),되돌림흐름묶기(int32_t,int32_t,int32_t),되돌림흐름듣기(int32_t,int32_t);
extern int32_t 되돌림흐름연결(int32_t,int32_t,int32_t),되돌림흐름연결받기(int32_t),되돌림흐름읽기(int32_t,int32_t),되돌림흐름쓰기(int32_t,int32_t);
extern int32_t 되돌림흐름접속번호(int32_t),되돌림흐름상대(int32_t),되돌림흐름닫기(int32_t);
static int 외부연결[24];
static int 임의주소[24], 양쪽수신창구[24], 전문외부상대[8], 묶인주소[8];
static int 외부번호(int ifayela_isibambo) { return ifayela_isibambo>=32 && ifayela_isibambo<56 ? 외부연결[ifayela_isibambo-32]-1 : -1; }
static int namathisela_I_SMS(int ifayela_isibambo,int thayipha_umunxa) {
    if(ifayela_isibambo<32||ifayela_isibambo>=56)return -9;int 이전=외부번호(ifayela_isibambo);if(이전>=0)return 이전;
    int 개수=통신끝점만들기(thayipha_umunxa);if(개수>=0)외부연결[ifayela_isibambo-32]=개수+1;return 개수;
}
int32_t 자바전문만들기(int32_t 첫째값,int32_t 둘째값,int32_t ikhodi_yohlamvu){return 되돌림전문만들기(첫째값,둘째값,ikhodi_yohlamvu);}
int32_t 자바전문묶기(int32_t ifayela_isibambo,int32_t ikheli_le_inthanethi,int32_t 접속번호){
    if(ikheli_le_inthanethi==0x7f000001)return 되돌림전문묶기(ifayela_isibambo,ikheli_le_inthanethi,접속번호);
    if(ikheli_le_inthanethi!=0&&ikheli_le_inthanethi!=망상태읽기(0,0))return -99;
    int 반환값=되돌림전문묶기(ifayela_isibambo,0,접속번호);if(반환값<0)return 반환값;
    int 개수=namathisela_I_SMS(ifayela_isibambo,2);if(개수<0)return 개수;반환값=망주소묶기(개수,망상태읽기(0,0),되돌림전문접속번호(ifayela_isibambo));if(!반환값)묶인주소[ifayela_isibambo-32]=ikheli_le_inthanethi;return 반환값;
}
int32_t 자바전문보내기(int32_t ifayela_isibambo,int32_t ikheli_le_inthanethi,int32_t 접속번호,int32_t Ubungako){
    if(ikheli_le_inthanethi==0x7f000001)return 되돌림전문보내기(ifayela_isibambo,ikheli_le_inthanethi,접속번호,Ubungako);
    if(Ubungako<0||Ubungako>512)return -90;if(접속번호<1||접속번호>65535)return -22;
    if(되돌림전문접속번호(ifayela_isibambo)<0)return -9;
    if(되돌림전문주소(ifayela_isibambo)==0x7f000001)return -101;
    int 개수=외부번호(ifayela_isibambo);if(개수<0){int 반환값=0;if(되돌림전문접속번호(ifayela_isibambo)==0)반환값=되돌림전문묶기(ifayela_isibambo,0,0);if(반환값<0)return 반환값;개수=namathisela_I_SMS(ifayela_isibambo,2);if(개수<0)return 개수;반환값=망주소묶기(개수,망상태읽기(0,0),되돌림전문접속번호(ifayela_isibambo));if(반환값<0)return 반환값;}
    unsigned char imininingwane[512];for(int 순번=0;순번<Ubungako;순번++)imininingwane[순번]=자바전문얻기(순번);return 전문보내기(개수,imininingwane,Ubungako,ikheli_le_inthanethi,접속번호);
}
int32_t 자바전문받기(int32_t ifayela_isibambo,int32_t Ubungako){
    int 개수=외부번호(ifayela_isibambo);if(개수<0)return 되돌림전문받기(ifayela_isibambo,Ubungako);if(Ubungako<0||Ubungako>512)return -22;
    int endaweni=되돌림전문받기(ifayela_isibambo,Ubungako);if(endaweni!=-11){전문외부상대[ifayela_isibambo-32]=0;return endaweni;}
    unsigned char imininingwane[512];int 반환값=전문받기(개수,imininingwane,Ubungako);if(반환값>=0)전문외부상대[ifayela_isibambo-32]=1;for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,imininingwane[순번]);return 반환값;
}
int32_t 자바전문접속번호(int32_t ifayela_isibambo){int 개수=외부번호(ifayela_isibambo);return 개수<0?되돌림전문접속번호(ifayela_isibambo):(int32_t)통신접속번호(개수);}
int32_t 자바전문주소(int32_t ifayela_isibambo){return 외부번호(ifayela_isibambo)<0?되돌림전문주소(ifayela_isibambo):묶인주소[ifayela_isibambo-32];}
int32_t 자바전문상대(int32_t ifayela_isibambo){int 개수=외부번호(ifayela_isibambo);return 개수<0||!전문외부상대[ifayela_isibambo-32]?되돌림전문상대(ifayela_isibambo):(int32_t)상대접속번호(개수);}
int32_t 자바전문원격주소(int32_t ifayela_isibambo){int 개수=외부번호(ifayela_isibambo);return 개수<0||!전문외부상대[ifayela_isibambo-32]?0x7f000001:(int32_t)상대통신주소(개수);}
int32_t 자바전문닫기(int32_t ifayela_isibambo){int 개수=외부번호(ifayela_isibambo);if(개수>=0){vala_iNethiwekhi(개수);외부연결[ifayela_isibambo-32]=0;}if(ifayela_isibambo>=32&&ifayela_isibambo<40)전문외부상대[ifayela_isibambo-32]=묶인주소[ifayela_isibambo-32]=0;return 되돌림전문닫기(ifayela_isibambo);}
int32_t 자바흐름만들기(void){return 되돌림흐름만들기();}
int32_t 자바흐름묶기(int32_t ifayela_isibambo,int32_t ikheli_le_inthanethi,int32_t 접속번호){
    if(ikheli_le_inthanethi==0||ikheli_le_inthanethi==0x7f000001){int 반환값=되돌림흐름묶기(ifayela_isibambo,ikheli_le_inthanethi,접속번호);if(!반환값)임의주소[ifayela_isibambo-32]=ikheli_le_inthanethi==0;return 반환값;}
    if(ikheli_le_inthanethi!=망상태읽기(0,0))return -99;int 반환값=되돌림흐름묶기(ifayela_isibambo,0,접속번호);if(반환값<0)return 반환값;
    int 개수=namathisela_I_SMS(ifayela_isibambo,1);return 개수<0?개수:망주소묶기(개수,ikheli_le_inthanethi,되돌림흐름접속번호(ifayela_isibambo));
}
int32_t 자바흐름듣기(int32_t ifayela_isibambo,int32_t 연결대기한도){
    int 개수=외부번호(ifayela_isibambo);if(개수<0){int 반환값=되돌림흐름듣기(ifayela_isibambo,연결대기한도);if(반환값<0||!임의주소[ifayela_isibambo-32])return 반환값;
        개수=namathisela_I_SMS(ifayela_isibambo,1);if(개수<0)return 개수;반환값=망주소묶기(개수,망상태읽기(0,0),되돌림흐름접속번호(ifayela_isibambo));if(반환값<0)return 반환값;양쪽수신창구[ifayela_isibambo-32]=1;
    }return 연결대기한도<1?-22:연결기다리기(개수);
}
int32_t 자바흐름연결(int32_t ifayela_isibambo,int32_t ikheli_le_inthanethi,int32_t 접속번호){
    if(ikheli_le_inthanethi==0x7f000001 && 외부번호(ifayela_isibambo)<0)return 되돌림흐름연결(ifayela_isibambo,ikheli_le_inthanethi,접속번호);
    if(되돌림흐름접속번호(ifayela_isibambo)<0)return -9;int 개수=namathisela_I_SMS(ifayela_isibambo,1);return 개수<0?개수:망연결하기(개수,ikheli_le_inthanethi,접속번호);
}
int32_t 자바흐름연결받기(int32_t ifayela_isibambo){
    int 개수=외부번호(ifayela_isibambo);if(개수<0)return 되돌림흐름연결받기(ifayela_isibambo);
    if(양쪽수신창구[ifayela_isibambo-32]){int endaweni=되돌림흐름연결받기(ifayela_isibambo);if(endaweni!=-11)return endaweni;}
    int untanga_inani=망연결받기(개수);if(untanga_inani<0)return untanga_inani;
    int impokophelo=되돌림흐름만들기();if(impokophelo<0){vala_iNethiwekhi(untanga_inani);return impokophelo;}외부연결[impokophelo-32]=untanga_inani+1;return impokophelo;
}
int32_t 자바흐름읽기(int32_t ifayela_isibambo,int32_t Ubungako){
    int 개수=외부번호(ifayela_isibambo);if(개수<0)return 되돌림흐름읽기(ifayela_isibambo,Ubungako);if(Ubungako<0||Ubungako>512)return -22;
    unsigned char imininingwane[512];int 반환값=통신읽기(개수,imininingwane,Ubungako);for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,imininingwane[순번]);return 반환값;
}
int32_t 자바흐름쓰기(int32_t ifayela_isibambo,int32_t Ubungako){
    int 개수=외부번호(ifayela_isibambo);if(개수<0)return 되돌림흐름쓰기(ifayela_isibambo,Ubungako);if(Ubungako<0||Ubungako>512)return -22;
    unsigned char imininingwane[512];for(int 순번=0;순번<Ubungako;순번++)imininingwane[순번]=자바전문얻기(순번);return 통신쓰기(개수,imininingwane,Ubungako);
}
int32_t 자바흐름접속번호(int32_t ifayela_isibambo){int 개수=외부번호(ifayela_isibambo);return 개수<0?되돌림흐름접속번호(ifayela_isibambo):(int32_t)통신접속번호(개수);}
int32_t 자바흐름상대(int32_t ifayela_isibambo){int 개수=외부번호(ifayela_isibambo);return 개수<0?되돌림흐름상대(ifayela_isibambo):(int32_t)상대접속번호(개수);}
int32_t 자바흐름주소(int32_t ifayela_isibambo){return 외부번호(ifayela_isibambo)<0?0x7f000001:양쪽수신창구[ifayela_isibambo-32]?0:망상태읽기(0,0);}
int32_t 자바흐름닫기(int32_t ifayela_isibambo){int 개수=외부번호(ifayela_isibambo);if(개수>=0){vala_iNethiwekhi(개수);외부연결[ifayela_isibambo-32]=0;}if(ifayela_isibambo>=40&&ifayela_isibambo<56)임의주소[ifayela_isibambo-32]=양쪽수신창구[ifayela_isibambo-32]=0;return 되돌림흐름닫기(ifayela_isibambo);}
