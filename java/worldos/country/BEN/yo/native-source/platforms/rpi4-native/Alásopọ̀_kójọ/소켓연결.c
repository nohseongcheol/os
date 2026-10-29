#include "../명명/기계연결이름.h"
/* Preserve the deterministic Java loopback endpoints; route external IPv4 to lwIP. */
#include "Alásopọ̀_kójọ.h"
extern int32_t 되돌림전문만들기(int32_t,int32_t,int32_t), 되돌림전문묶기(int32_t,int32_t,int32_t);
extern int32_t 되돌림전문보내기(int32_t,int32_t,int32_t,int32_t), 되돌림전문받기(int32_t,int32_t);
extern int32_t 되돌림전문접속번호(int32_t), 되돌림전문주소(int32_t), 되돌림전문상대(int32_t), 되돌림전문닫기(int32_t);
extern int32_t 자바전문넣기(int32_t,int32_t),자바전문얻기(int32_t);
extern int32_t 되돌림흐름만들기(void),되돌림흐름묶기(int32_t,int32_t,int32_t),되돌림흐름듣기(int32_t,int32_t);
extern int32_t 되돌림흐름연결(int32_t,int32_t,int32_t),되돌림흐름연결받기(int32_t),되돌림흐름읽기(int32_t,int32_t),되돌림흐름쓰기(int32_t,int32_t);
extern int32_t 되돌림흐름접속번호(int32_t),되돌림흐름상대(int32_t),되돌림흐름닫기(int32_t);
static int 외부연결[24];
static int 임의주소[24], 양쪽수신창구[24], 전문외부상대[8], 묶인주소[8];
static int 외부번호(int fáìlì_èkù) { return fáìlì_èkù>=32 && fáìlì_èkù<56 ? 외부연결[fáìlì_èkù-32]-1 : -1; }
static int lẹ_SMS(int fáìlì_èkù,int irú_ìsọ̀rí) {
    if(fáìlì_èkù<32||fáìlì_èkù>=56)return -9;int 이전=외부번호(fáìlì_èkù);if(이전>=0)return 이전;
    int 개수=통신끝점만들기(irú_ìsọ̀rí);if(개수>=0)외부연결[fáìlì_èkù-32]=개수+1;return 개수;
}
int32_t 자바전문만들기(int32_t 첫째값,int32_t 둘째값,int32_t kóòdù_ẹyọ_ọ̀rọ̀){return 되돌림전문만들기(첫째값,둘째값,kóòdù_ẹyọ_ọ̀rọ̀);}
int32_t 자바전문묶기(int32_t fáìlì_èkù,int32_t àdíréẹ̀sì_íntánẹ́ẹ̀tì,int32_t 접속번호){
    if(àdíréẹ̀sì_íntánẹ́ẹ̀tì==0x7f000001)return 되돌림전문묶기(fáìlì_èkù,àdíréẹ̀sì_íntánẹ́ẹ̀tì,접속번호);
    if(àdíréẹ̀sì_íntánẹ́ẹ̀tì!=0&&àdíréẹ̀sì_íntánẹ́ẹ̀tì!=망상태읽기(0,0))return -99;
    int 반환값=되돌림전문묶기(fáìlì_èkù,0,접속번호);if(반환값<0)return 반환값;
    int 개수=lẹ_SMS(fáìlì_èkù,2);if(개수<0)return 개수;반환값=망주소묶기(개수,망상태읽기(0,0),되돌림전문접속번호(fáìlì_èkù));if(!반환값)묶인주소[fáìlì_èkù-32]=àdíréẹ̀sì_íntánẹ́ẹ̀tì;return 반환값;
}
int32_t 자바전문보내기(int32_t fáìlì_èkù,int32_t àdíréẹ̀sì_íntánẹ́ẹ̀tì,int32_t 접속번호,int32_t Ìwọ̀n){
    if(àdíréẹ̀sì_íntánẹ́ẹ̀tì==0x7f000001)return 되돌림전문보내기(fáìlì_èkù,àdíréẹ̀sì_íntánẹ́ẹ̀tì,접속번호,Ìwọ̀n);
    if(Ìwọ̀n<0||Ìwọ̀n>512)return -90;if(접속번호<1||접속번호>65535)return -22;
    if(되돌림전문접속번호(fáìlì_èkù)<0)return -9;
    if(되돌림전문주소(fáìlì_èkù)==0x7f000001)return -101;
    int 개수=외부번호(fáìlì_èkù);if(개수<0){int 반환값=0;if(되돌림전문접속번호(fáìlì_èkù)==0)반환값=되돌림전문묶기(fáìlì_èkù,0,0);if(반환값<0)return 반환값;개수=lẹ_SMS(fáìlì_èkù,2);if(개수<0)return 개수;반환값=망주소묶기(개수,망상태읽기(0,0),되돌림전문접속번호(fáìlì_èkù));if(반환값<0)return 반환값;}
    unsigned char détà[512];for(int 순번=0;순번<Ìwọ̀n;순번++)détà[순번]=자바전문얻기(순번);return 전문보내기(개수,détà,Ìwọ̀n,àdíréẹ̀sì_íntánẹ́ẹ̀tì,접속번호);
}
int32_t 자바전문받기(int32_t fáìlì_èkù,int32_t Ìwọ̀n){
    int 개수=외부번호(fáìlì_èkù);if(개수<0)return 되돌림전문받기(fáìlì_èkù,Ìwọ̀n);if(Ìwọ̀n<0||Ìwọ̀n>512)return -22;
    int agbègbè=되돌림전문받기(fáìlì_èkù,Ìwọ̀n);if(agbègbè!=-11){전문외부상대[fáìlì_èkù-32]=0;return agbègbè;}
    unsigned char détà[512];int 반환값=전문받기(개수,détà,Ìwọ̀n);if(반환값>=0)전문외부상대[fáìlì_èkù-32]=1;for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,détà[순번]);return 반환값;
}
int32_t 자바전문접속번호(int32_t fáìlì_èkù){int 개수=외부번호(fáìlì_èkù);return 개수<0?되돌림전문접속번호(fáìlì_èkù):(int32_t)통신접속번호(개수);}
int32_t 자바전문주소(int32_t fáìlì_èkù){return 외부번호(fáìlì_èkù)<0?되돌림전문주소(fáìlì_èkù):묶인주소[fáìlì_èkù-32];}
int32_t 자바전문상대(int32_t fáìlì_èkù){int 개수=외부번호(fáìlì_èkù);return 개수<0||!전문외부상대[fáìlì_èkù-32]?되돌림전문상대(fáìlì_èkù):(int32_t)상대접속번호(개수);}
int32_t 자바전문원격주소(int32_t fáìlì_èkù){int 개수=외부번호(fáìlì_èkù);return 개수<0||!전문외부상대[fáìlì_èkù-32]?0x7f000001:(int32_t)상대통신주소(개수);}
int32_t 자바전문닫기(int32_t fáìlì_èkù){int 개수=외부번호(fáìlì_èkù);if(개수>=0){pa_dé_Alásopọ̀(개수);외부연결[fáìlì_èkù-32]=0;}if(fáìlì_èkù>=32&&fáìlì_èkù<40)전문외부상대[fáìlì_èkù-32]=묶인주소[fáìlì_èkù-32]=0;return 되돌림전문닫기(fáìlì_èkù);}
int32_t 자바흐름만들기(void){return 되돌림흐름만들기();}
int32_t 자바흐름묶기(int32_t fáìlì_èkù,int32_t àdíréẹ̀sì_íntánẹ́ẹ̀tì,int32_t 접속번호){
    if(àdíréẹ̀sì_íntánẹ́ẹ̀tì==0||àdíréẹ̀sì_íntánẹ́ẹ̀tì==0x7f000001){int 반환값=되돌림흐름묶기(fáìlì_èkù,àdíréẹ̀sì_íntánẹ́ẹ̀tì,접속번호);if(!반환값)임의주소[fáìlì_èkù-32]=àdíréẹ̀sì_íntánẹ́ẹ̀tì==0;return 반환값;}
    if(àdíréẹ̀sì_íntánẹ́ẹ̀tì!=망상태읽기(0,0))return -99;int 반환값=되돌림흐름묶기(fáìlì_èkù,0,접속번호);if(반환값<0)return 반환값;
    int 개수=lẹ_SMS(fáìlì_èkù,1);return 개수<0?개수:망주소묶기(개수,àdíréẹ̀sì_íntánẹ́ẹ̀tì,되돌림흐름접속번호(fáìlì_èkù));
}
int32_t 자바흐름듣기(int32_t fáìlì_èkù,int32_t 연결대기한도){
    int 개수=외부번호(fáìlì_èkù);if(개수<0){int 반환값=되돌림흐름듣기(fáìlì_èkù,연결대기한도);if(반환값<0||!임의주소[fáìlì_èkù-32])return 반환값;
        개수=lẹ_SMS(fáìlì_èkù,1);if(개수<0)return 개수;반환값=망주소묶기(개수,망상태읽기(0,0),되돌림흐름접속번호(fáìlì_èkù));if(반환값<0)return 반환값;양쪽수신창구[fáìlì_èkù-32]=1;
    }return 연결대기한도<1?-22:연결기다리기(개수);
}
int32_t 자바흐름연결(int32_t fáìlì_èkù,int32_t àdíréẹ̀sì_íntánẹ́ẹ̀tì,int32_t 접속번호){
    if(àdíréẹ̀sì_íntánẹ́ẹ̀tì==0x7f000001 && 외부번호(fáìlì_èkù)<0)return 되돌림흐름연결(fáìlì_èkù,àdíréẹ̀sì_íntánẹ́ẹ̀tì,접속번호);
    if(되돌림흐름접속번호(fáìlì_èkù)<0)return -9;int 개수=lẹ_SMS(fáìlì_èkù,1);return 개수<0?개수:망연결하기(개수,àdíréẹ̀sì_íntánẹ́ẹ̀tì,접속번호);
}
int32_t 자바흐름연결받기(int32_t fáìlì_èkù){
    int 개수=외부번호(fáìlì_èkù);if(개수<0)return 되돌림흐름연결받기(fáìlì_èkù);
    if(양쪽수신창구[fáìlì_èkù-32]){int agbègbè=되돌림흐름연결받기(fáìlì_èkù);if(agbègbè!=-11)return agbègbè;}
    int ọ̀gbà_iye=망연결받기(개수);if(ọ̀gbà_iye<0)return ọ̀gbà_iye;
    int àfojúsùn=되돌림흐름만들기();if(àfojúsùn<0){pa_dé_Alásopọ̀(ọ̀gbà_iye);return àfojúsùn;}외부연결[àfojúsùn-32]=ọ̀gbà_iye+1;return àfojúsùn;
}
int32_t 자바흐름읽기(int32_t fáìlì_èkù,int32_t Ìwọ̀n){
    int 개수=외부번호(fáìlì_èkù);if(개수<0)return 되돌림흐름읽기(fáìlì_èkù,Ìwọ̀n);if(Ìwọ̀n<0||Ìwọ̀n>512)return -22;
    unsigned char détà[512];int 반환값=통신읽기(개수,détà,Ìwọ̀n);for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,détà[순번]);return 반환값;
}
int32_t 자바흐름쓰기(int32_t fáìlì_èkù,int32_t Ìwọ̀n){
    int 개수=외부번호(fáìlì_èkù);if(개수<0)return 되돌림흐름쓰기(fáìlì_èkù,Ìwọ̀n);if(Ìwọ̀n<0||Ìwọ̀n>512)return -22;
    unsigned char détà[512];for(int 순번=0;순번<Ìwọ̀n;순번++)détà[순번]=자바전문얻기(순번);return 통신쓰기(개수,détà,Ìwọ̀n);
}
int32_t 자바흐름접속번호(int32_t fáìlì_èkù){int 개수=외부번호(fáìlì_èkù);return 개수<0?되돌림흐름접속번호(fáìlì_èkù):(int32_t)통신접속번호(개수);}
int32_t 자바흐름상대(int32_t fáìlì_èkù){int 개수=외부번호(fáìlì_èkù);return 개수<0?되돌림흐름상대(fáìlì_èkù):(int32_t)상대접속번호(개수);}
int32_t 자바흐름주소(int32_t fáìlì_èkù){return 외부번호(fáìlì_èkù)<0?0x7f000001:양쪽수신창구[fáìlì_èkù-32]?0:망상태읽기(0,0);}
int32_t 자바흐름닫기(int32_t fáìlì_èkù){int 개수=외부번호(fáìlì_èkù);if(개수>=0){pa_dé_Alásopọ̀(개수);외부연결[fáìlì_èkù-32]=0;}if(fáìlì_èkù>=40&&fáìlì_èkù<56)임의주소[fáìlì_èkù-32]=양쪽수신창구[fáìlì_èkù-32]=0;return 되돌림흐름닫기(fáìlì_èkù);}
