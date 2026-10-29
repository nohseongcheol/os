#include "../명명/기계연결이름.h"
/* Preserve the deterministic Java loopback endpoints; route external IPv4 to lwIP. */
#include "Tor_Desse.h"
extern int32_t 되돌림전문만들기(int32_t,int32_t,int32_t), 되돌림전문묶기(int32_t,int32_t,int32_t);
extern int32_t 되돌림전문보내기(int32_t,int32_t,int32_t,int32_t), 되돌림전문받기(int32_t,int32_t);
extern int32_t 되돌림전문접속번호(int32_t), 되돌림전문주소(int32_t), 되돌림전문상대(int32_t), 되돌림전문닫기(int32_t);
extern int32_t 자바전문넣기(int32_t,int32_t),자바전문얻기(int32_t);
extern int32_t 되돌림흐름만들기(void),되돌림흐름묶기(int32_t,int32_t,int32_t),되돌림흐름듣기(int32_t,int32_t);
extern int32_t 되돌림흐름연결(int32_t,int32_t,int32_t),되돌림흐름연결받기(int32_t),되돌림흐름읽기(int32_t,int32_t),되돌림흐름쓰기(int32_t,int32_t);
extern int32_t 되돌림흐름접속번호(int32_t),되돌림흐름상대(int32_t),되돌림흐름닫기(int32_t);
static int 외부연결[24];
static int 임의주소[24], 양쪽수신창구[24], 전문외부상대[8], 묶인주소[8];
static int 외부번호(int faýl_ryçag) { return faýl_ryçag>=32 && faýl_ryçag<56 ? 외부연결[faýl_ryçag-32]-1 : -1; }
static int ýelme_SMS(int faýl_ryçag,int ýaz_kategoriýa) {
    if(faýl_ryçag<32||faýl_ryçag>=56)return -9;int 이전=외부번호(faýl_ryçag);if(이전>=0)return 이전;
    int 개수=통신끝점만들기(ýaz_kategoriýa);if(개수>=0)외부연결[faýl_ryçag-32]=개수+1;return 개수;
}
int32_t 자바전문만들기(int32_t 첫째값,int32_t 둘째값,int32_t nyşanyň_kody){return 되돌림전문만들기(첫째값,둘째값,nyşanyň_kody);}
int32_t 자바전문묶기(int32_t faýl_ryçag,int32_t Internet_salgy,int32_t 접속번호){
    if(Internet_salgy==0x7f000001)return 되돌림전문묶기(faýl_ryçag,Internet_salgy,접속번호);
    if(Internet_salgy!=0&&Internet_salgy!=망상태읽기(0,0))return -99;
    int 반환값=되돌림전문묶기(faýl_ryçag,0,접속번호);if(반환값<0)return 반환값;
    int 개수=ýelme_SMS(faýl_ryçag,2);if(개수<0)return 개수;반환값=망주소묶기(개수,망상태읽기(0,0),되돌림전문접속번호(faýl_ryçag));if(!반환값)묶인주소[faýl_ryçag-32]=Internet_salgy;return 반환값;
}
int32_t 자바전문보내기(int32_t faýl_ryçag,int32_t Internet_salgy,int32_t 접속번호,int32_t Ululyk){
    if(Internet_salgy==0x7f000001)return 되돌림전문보내기(faýl_ryçag,Internet_salgy,접속번호,Ululyk);
    if(Ululyk<0||Ululyk>512)return -90;if(접속번호<1||접속번호>65535)return -22;
    if(되돌림전문접속번호(faýl_ryçag)<0)return -9;
    if(되돌림전문주소(faýl_ryçag)==0x7f000001)return -101;
    int 개수=외부번호(faýl_ryçag);if(개수<0){int 반환값=0;if(되돌림전문접속번호(faýl_ryçag)==0)반환값=되돌림전문묶기(faýl_ryçag,0,0);if(반환값<0)return 반환값;개수=ýelme_SMS(faýl_ryçag,2);if(개수<0)return 개수;반환값=망주소묶기(개수,망상태읽기(0,0),되돌림전문접속번호(faýl_ryçag));if(반환값<0)return 반환값;}
    unsigned char maglumat[512];for(int 순번=0;순번<Ululyk;순번++)maglumat[순번]=자바전문얻기(순번);return 전문보내기(개수,maglumat,Ululyk,Internet_salgy,접속번호);
}
int32_t 자바전문받기(int32_t faýl_ryçag,int32_t Ululyk){
    int 개수=외부번호(faýl_ryçag);if(개수<0)return 되돌림전문받기(faýl_ryçag,Ululyk);if(Ululyk<0||Ululyk>512)return -22;
    int ýerli=되돌림전문받기(faýl_ryçag,Ululyk);if(ýerli!=-11){전문외부상대[faýl_ryçag-32]=0;return ýerli;}
    unsigned char maglumat[512];int 반환값=전문받기(개수,maglumat,Ululyk);if(반환값>=0)전문외부상대[faýl_ryçag-32]=1;for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,maglumat[순번]);return 반환값;
}
int32_t 자바전문접속번호(int32_t faýl_ryçag){int 개수=외부번호(faýl_ryçag);return 개수<0?되돌림전문접속번호(faýl_ryçag):(int32_t)통신접속번호(개수);}
int32_t 자바전문주소(int32_t faýl_ryçag){return 외부번호(faýl_ryçag)<0?되돌림전문주소(faýl_ryçag):묶인주소[faýl_ryçag-32];}
int32_t 자바전문상대(int32_t faýl_ryçag){int 개수=외부번호(faýl_ryçag);return 개수<0||!전문외부상대[faýl_ryçag-32]?되돌림전문상대(faýl_ryçag):(int32_t)상대접속번호(개수);}
int32_t 자바전문원격주소(int32_t faýl_ryçag){int 개수=외부번호(faýl_ryçag);return 개수<0||!전문외부상대[faýl_ryçag-32]?0x7f000001:(int32_t)상대통신주소(개수);}
int32_t 자바전문닫기(int32_t faýl_ryçag){int 개수=외부번호(faýl_ryçag);if(개수>=0){ýap_Tor(개수);외부연결[faýl_ryçag-32]=0;}if(faýl_ryçag>=32&&faýl_ryçag<40)전문외부상대[faýl_ryçag-32]=묶인주소[faýl_ryçag-32]=0;return 되돌림전문닫기(faýl_ryçag);}
int32_t 자바흐름만들기(void){return 되돌림흐름만들기();}
int32_t 자바흐름묶기(int32_t faýl_ryçag,int32_t Internet_salgy,int32_t 접속번호){
    if(Internet_salgy==0||Internet_salgy==0x7f000001){int 반환값=되돌림흐름묶기(faýl_ryçag,Internet_salgy,접속번호);if(!반환값)임의주소[faýl_ryçag-32]=Internet_salgy==0;return 반환값;}
    if(Internet_salgy!=망상태읽기(0,0))return -99;int 반환값=되돌림흐름묶기(faýl_ryçag,0,접속번호);if(반환값<0)return 반환값;
    int 개수=ýelme_SMS(faýl_ryçag,1);return 개수<0?개수:망주소묶기(개수,Internet_salgy,되돌림흐름접속번호(faýl_ryçag));
}
int32_t 자바흐름듣기(int32_t faýl_ryçag,int32_t 연결대기한도){
    int 개수=외부번호(faýl_ryçag);if(개수<0){int 반환값=되돌림흐름듣기(faýl_ryçag,연결대기한도);if(반환값<0||!임의주소[faýl_ryçag-32])return 반환값;
        개수=ýelme_SMS(faýl_ryçag,1);if(개수<0)return 개수;반환값=망주소묶기(개수,망상태읽기(0,0),되돌림흐름접속번호(faýl_ryçag));if(반환값<0)return 반환값;양쪽수신창구[faýl_ryçag-32]=1;
    }return 연결대기한도<1?-22:연결기다리기(개수);
}
int32_t 자바흐름연결(int32_t faýl_ryçag,int32_t Internet_salgy,int32_t 접속번호){
    if(Internet_salgy==0x7f000001 && 외부번호(faýl_ryçag)<0)return 되돌림흐름연결(faýl_ryçag,Internet_salgy,접속번호);
    if(되돌림흐름접속번호(faýl_ryçag)<0)return -9;int 개수=ýelme_SMS(faýl_ryçag,1);return 개수<0?개수:망연결하기(개수,Internet_salgy,접속번호);
}
int32_t 자바흐름연결받기(int32_t faýl_ryçag){
    int 개수=외부번호(faýl_ryçag);if(개수<0)return 되돌림흐름연결받기(faýl_ryçag);
    if(양쪽수신창구[faýl_ryçag-32]){int ýerli=되돌림흐름연결받기(faýl_ryçag);if(ýerli!=-11)return ýerli;}
    int deň_derejeli_düwün_baha=망연결받기(개수);if(deň_derejeli_düwün_baha<0)return deň_derejeli_düwün_baha;
    int niýet=되돌림흐름만들기();if(niýet<0){ýap_Tor(deň_derejeli_düwün_baha);return niýet;}외부연결[niýet-32]=deň_derejeli_düwün_baha+1;return niýet;
}
int32_t 자바흐름읽기(int32_t faýl_ryçag,int32_t Ululyk){
    int 개수=외부번호(faýl_ryçag);if(개수<0)return 되돌림흐름읽기(faýl_ryçag,Ululyk);if(Ululyk<0||Ululyk>512)return -22;
    unsigned char maglumat[512];int 반환값=통신읽기(개수,maglumat,Ululyk);for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,maglumat[순번]);return 반환값;
}
int32_t 자바흐름쓰기(int32_t faýl_ryçag,int32_t Ululyk){
    int 개수=외부번호(faýl_ryçag);if(개수<0)return 되돌림흐름쓰기(faýl_ryçag,Ululyk);if(Ululyk<0||Ululyk>512)return -22;
    unsigned char maglumat[512];for(int 순번=0;순번<Ululyk;순번++)maglumat[순번]=자바전문얻기(순번);return 통신쓰기(개수,maglumat,Ululyk);
}
int32_t 자바흐름접속번호(int32_t faýl_ryçag){int 개수=외부번호(faýl_ryçag);return 개수<0?되돌림흐름접속번호(faýl_ryçag):(int32_t)통신접속번호(개수);}
int32_t 자바흐름상대(int32_t faýl_ryçag){int 개수=외부번호(faýl_ryçag);return 개수<0?되돌림흐름상대(faýl_ryçag):(int32_t)상대접속번호(개수);}
int32_t 자바흐름주소(int32_t faýl_ryçag){return 외부번호(faýl_ryçag)<0?0x7f000001:양쪽수신창구[faýl_ryçag-32]?0:망상태읽기(0,0);}
int32_t 자바흐름닫기(int32_t faýl_ryçag){int 개수=외부번호(faýl_ryçag);if(개수>=0){ýap_Tor(개수);외부연결[faýl_ryçag-32]=0;}if(faýl_ryçag>=40&&faýl_ryçag<56)임의주소[faýl_ryçag-32]=양쪽수신창구[faýl_ryçag-32]=0;return 되돌림흐름닫기(faýl_ryçag);}
