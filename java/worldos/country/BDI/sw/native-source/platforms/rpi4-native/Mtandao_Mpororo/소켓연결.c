#include "../명명/기계연결이름.h"
/* Preserve the deterministic Java loopback endpoints; route external IPv4 to lwIP. */
#include "Mtandao_Mpororo.h"
extern int32_t 되돌림전문만들기(int32_t,int32_t,int32_t), 되돌림전문묶기(int32_t,int32_t,int32_t);
extern int32_t 되돌림전문보내기(int32_t,int32_t,int32_t,int32_t), 되돌림전문받기(int32_t,int32_t);
extern int32_t 되돌림전문접속번호(int32_t), 되돌림전문주소(int32_t), 되돌림전문상대(int32_t), 되돌림전문닫기(int32_t);
extern int32_t 자바전문넣기(int32_t,int32_t),자바전문얻기(int32_t);
extern int32_t 되돌림흐름만들기(void),되돌림흐름묶기(int32_t,int32_t,int32_t),되돌림흐름듣기(int32_t,int32_t);
extern int32_t 되돌림흐름연결(int32_t,int32_t,int32_t),되돌림흐름연결받기(int32_t),되돌림흐름읽기(int32_t,int32_t),되돌림흐름쓰기(int32_t,int32_t);
extern int32_t 되돌림흐름접속번호(int32_t),되돌림흐름상대(int32_t),되돌림흐름닫기(int32_t);
static int 외부연결[24];
static int 임의주소[24], 양쪽수신창구[24], 전문외부상대[8], 묶인주소[8];
static int 외부번호(int faili_kishiko) { return faili_kishiko>=32 && faili_kishiko<56 ? 외부연결[faili_kishiko-32]-1 : -1; }
static int bandika_SMS(int faili_kishiko,int aina_kategoria) {
    if(faili_kishiko<32||faili_kishiko>=56)return -9;int 이전=외부번호(faili_kishiko);if(이전>=0)return 이전;
    int 개수=통신끝점만들기(aina_kategoria);if(개수>=0)외부연결[faili_kishiko-32]=개수+1;return 개수;
}
int32_t 자바전문만들기(int32_t 첫째값,int32_t 둘째값,int32_t msimbo_wa_kibambo){return 되돌림전문만들기(첫째값,둘째값,msimbo_wa_kibambo);}
int32_t 자바전문묶기(int32_t faili_kishiko,int32_t Anwani_tovuti,int32_t namba_ya_kituo){
    if(Anwani_tovuti==0x7f000001)return 되돌림전문묶기(faili_kishiko,Anwani_tovuti,namba_ya_kituo);
    if(Anwani_tovuti!=0&&Anwani_tovuti!=망상태읽기(0,0))return -99;
    int 반환값=되돌림전문묶기(faili_kishiko,0,namba_ya_kituo);if(반환값<0)return 반환값;
    int 개수=bandika_SMS(faili_kishiko,2);if(개수<0)return 개수;반환값=망주소묶기(개수,망상태읽기(0,0),되돌림전문접속번호(faili_kishiko));if(!반환값)묶인주소[faili_kishiko-32]=Anwani_tovuti;return 반환값;
}
int32_t 자바전문보내기(int32_t faili_kishiko,int32_t Anwani_tovuti,int32_t namba_ya_kituo,int32_t panga_ukubwa){
    if(Anwani_tovuti==0x7f000001)return 되돌림전문보내기(faili_kishiko,Anwani_tovuti,namba_ya_kituo,panga_ukubwa);
    if(panga_ukubwa<0||panga_ukubwa>512)return -90;if(namba_ya_kituo<1||namba_ya_kituo>65535)return -22;
    if(되돌림전문접속번호(faili_kishiko)<0)return -9;
    if(되돌림전문주소(faili_kishiko)==0x7f000001)return -101;
    int 개수=외부번호(faili_kishiko);if(개수<0){int 반환값=0;if(되돌림전문접속번호(faili_kishiko)==0)반환값=되돌림전문묶기(faili_kishiko,0,0);if(반환값<0)return 반환값;개수=bandika_SMS(faili_kishiko,2);if(개수<0)return 개수;반환값=망주소묶기(개수,망상태읽기(0,0),되돌림전문접속번호(faili_kishiko));if(반환값<0)return 반환값;}
    unsigned char data[512];for(int 순번=0;순번<panga_ukubwa;순번++)data[순번]=자바전문얻기(순번);return 전문보내기(개수,data,panga_ukubwa,Anwani_tovuti,namba_ya_kituo);
}
int32_t 자바전문받기(int32_t faili_kishiko,int32_t panga_ukubwa){
    int 개수=외부번호(faili_kishiko);if(개수<0)return 되돌림전문받기(faili_kishiko,panga_ukubwa);if(panga_ukubwa<0||panga_ukubwa>512)return -22;
    int jirani=되돌림전문받기(faili_kishiko,panga_ukubwa);if(jirani!=-11){전문외부상대[faili_kishiko-32]=0;return jirani;}
    unsigned char data[512];int 반환값=전문받기(개수,data,panga_ukubwa);if(반환값>=0)전문외부상대[faili_kishiko-32]=1;for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,data[순번]);return 반환값;
}
int32_t 자바전문접속번호(int32_t faili_kishiko){int 개수=외부번호(faili_kishiko);return 개수<0?되돌림전문접속번호(faili_kishiko):(int32_t)Mtandao_namba_ya_kituo(개수);}
int32_t 자바전문주소(int32_t faili_kishiko){return 외부번호(faili_kishiko)<0?되돌림전문주소(faili_kishiko):묶인주소[faili_kishiko-32];}
int32_t 자바전문상대(int32_t faili_kishiko){int 개수=외부번호(faili_kishiko);return 개수<0||!전문외부상대[faili_kishiko-32]?되돌림전문상대(faili_kishiko):(int32_t)kompyuta_rika_namba_ya_kituo(개수);}
int32_t 자바전문원격주소(int32_t faili_kishiko){int 개수=외부번호(faili_kishiko);return 개수<0||!전문외부상대[faili_kishiko-32]?0x7f000001:(int32_t)상대통신주소(개수);}
int32_t 자바전문닫기(int32_t faili_kishiko){int 개수=외부번호(faili_kishiko);if(개수>=0){funga_Mtandao(개수);외부연결[faili_kishiko-32]=0;}if(faili_kishiko>=32&&faili_kishiko<40)전문외부상대[faili_kishiko-32]=묶인주소[faili_kishiko-32]=0;return 되돌림전문닫기(faili_kishiko);}
int32_t 자바흐름만들기(void){return 되돌림흐름만들기();}
int32_t 자바흐름묶기(int32_t faili_kishiko,int32_t Anwani_tovuti,int32_t namba_ya_kituo){
    if(Anwani_tovuti==0||Anwani_tovuti==0x7f000001){int 반환값=되돌림흐름묶기(faili_kishiko,Anwani_tovuti,namba_ya_kituo);if(!반환값)임의주소[faili_kishiko-32]=Anwani_tovuti==0;return 반환값;}
    if(Anwani_tovuti!=망상태읽기(0,0))return -99;int 반환값=되돌림흐름묶기(faili_kishiko,0,namba_ya_kituo);if(반환값<0)return 반환값;
    int 개수=bandika_SMS(faili_kishiko,1);return 개수<0?개수:망주소묶기(개수,Anwani_tovuti,되돌림흐름접속번호(faili_kishiko));
}
int32_t 자바흐름듣기(int32_t faili_kishiko,int32_t 연결대기한도){
    int 개수=외부번호(faili_kishiko);if(개수<0){int 반환값=되돌림흐름듣기(faili_kishiko,연결대기한도);if(반환값<0||!임의주소[faili_kishiko-32])return 반환값;
        개수=bandika_SMS(faili_kishiko,1);if(개수<0)return 개수;반환값=망주소묶기(개수,망상태읽기(0,0),되돌림흐름접속번호(faili_kishiko));if(반환값<0)return 반환값;양쪽수신창구[faili_kishiko-32]=1;
    }return 연결대기한도<1?-22:연결기다리기(개수);
}
int32_t 자바흐름연결(int32_t faili_kishiko,int32_t Anwani_tovuti,int32_t namba_ya_kituo){
    if(Anwani_tovuti==0x7f000001 && 외부번호(faili_kishiko)<0)return 되돌림흐름연결(faili_kishiko,Anwani_tovuti,namba_ya_kituo);
    if(되돌림흐름접속번호(faili_kishiko)<0)return -9;int 개수=bandika_SMS(faili_kishiko,1);return 개수<0?개수:망연결하기(개수,Anwani_tovuti,namba_ya_kituo);
}
int32_t 자바흐름연결받기(int32_t faili_kishiko){
    int 개수=외부번호(faili_kishiko);if(개수<0)return 되돌림흐름연결받기(faili_kishiko);
    if(양쪽수신창구[faili_kishiko-32]){int jirani=되돌림흐름연결받기(faili_kishiko);if(jirani!=-11)return jirani;}
    int kompyuta_rika_thamani=망연결받기(개수);if(kompyuta_rika_thamani<0)return kompyuta_rika_thamani;
    int lengo=되돌림흐름만들기();if(lengo<0){funga_Mtandao(kompyuta_rika_thamani);return lengo;}외부연결[lengo-32]=kompyuta_rika_thamani+1;return lengo;
}
int32_t 자바흐름읽기(int32_t faili_kishiko,int32_t panga_ukubwa){
    int 개수=외부번호(faili_kishiko);if(개수<0)return 되돌림흐름읽기(faili_kishiko,panga_ukubwa);if(panga_ukubwa<0||panga_ukubwa>512)return -22;
    unsigned char data[512];int 반환값=통신읽기(개수,data,panga_ukubwa);for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,data[순번]);return 반환값;
}
int32_t 자바흐름쓰기(int32_t faili_kishiko,int32_t panga_ukubwa){
    int 개수=외부번호(faili_kishiko);if(개수<0)return 되돌림흐름쓰기(faili_kishiko,panga_ukubwa);if(panga_ukubwa<0||panga_ukubwa>512)return -22;
    unsigned char data[512];for(int 순번=0;순번<panga_ukubwa;순번++)data[순번]=자바전문얻기(순번);return 통신쓰기(개수,data,panga_ukubwa);
}
int32_t 자바흐름접속번호(int32_t faili_kishiko){int 개수=외부번호(faili_kishiko);return 개수<0?되돌림흐름접속번호(faili_kishiko):(int32_t)Mtandao_namba_ya_kituo(개수);}
int32_t 자바흐름상대(int32_t faili_kishiko){int 개수=외부번호(faili_kishiko);return 개수<0?되돌림흐름상대(faili_kishiko):(int32_t)kompyuta_rika_namba_ya_kituo(개수);}
int32_t 자바흐름주소(int32_t faili_kishiko){return 외부번호(faili_kishiko)<0?0x7f000001:양쪽수신창구[faili_kishiko-32]?0:망상태읽기(0,0);}
int32_t 자바흐름닫기(int32_t faili_kishiko){int 개수=외부번호(faili_kishiko);if(개수>=0){funga_Mtandao(개수);외부연결[faili_kishiko-32]=0;}if(faili_kishiko>=40&&faili_kishiko<56)임의주소[faili_kishiko-32]=양쪽수신창구[faili_kishiko-32]=0;return 되돌림흐름닫기(faili_kishiko);}
