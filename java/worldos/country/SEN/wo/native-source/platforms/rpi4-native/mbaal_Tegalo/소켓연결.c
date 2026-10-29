#include "../명명/기계연결이름.h"
/* Preserve the deterministic Java loopback endpoints; route external IPv4 to lwIP. */
#include "mbaal_Tegalo.h"
extern int32_t 되돌림전문만들기(int32_t,int32_t,int32_t), 되돌림전문묶기(int32_t,int32_t,int32_t);
extern int32_t 되돌림전문보내기(int32_t,int32_t,int32_t,int32_t), 되돌림전문받기(int32_t,int32_t);
extern int32_t 되돌림전문접속번호(int32_t), 되돌림전문주소(int32_t), 되돌림전문상대(int32_t), 되돌림전문닫기(int32_t);
extern int32_t 자바전문넣기(int32_t,int32_t),자바전문얻기(int32_t);
extern int32_t 되돌림흐름만들기(void),되돌림흐름묶기(int32_t,int32_t,int32_t),되돌림흐름듣기(int32_t,int32_t);
extern int32_t 되돌림흐름연결(int32_t,int32_t,int32_t),되돌림흐름연결받기(int32_t),되돌림흐름읽기(int32_t,int32_t),되돌림흐름쓰기(int32_t,int32_t);
extern int32_t 되돌림흐름접속번호(int32_t),되돌림흐름상대(int32_t),되돌림흐름닫기(int32_t);
static int 외부연결[24];
static int 임의주소[24], 양쪽수신창구[24], 전문외부상대[8], 묶인주소[8];
static int 외부번호(int bara_denc_yombal) { return bara_denc_yombal>=32 && bara_denc_yombal<56 ? 외부연결[bara_denc_yombal-32]-1 : -1; }
static int Taf_SMS(int bara_denc_yombal,int xeet_ngiir) {
    if(bara_denc_yombal<32||bara_denc_yombal>=56)return -9;int 이전=외부번호(bara_denc_yombal);if(이전>=0)return 이전;
    int 개수=통신끝점만들기(xeet_ngiir);if(개수>=0)외부연결[bara_denc_yombal-32]=개수+1;return 개수;
}
int32_t 자바전문만들기(int32_t 첫째값,int32_t 둘째값,int32_t kotu_araf){return 되돌림전문만들기(첫째값,둘째값,kotu_araf);}
int32_t 자바전문묶기(int32_t bara_denc_yombal,int32_t dëkkuwaayu_Internet,int32_t 접속번호){
    if(dëkkuwaayu_Internet==0x7f000001)return 되돌림전문묶기(bara_denc_yombal,dëkkuwaayu_Internet,접속번호);
    if(dëkkuwaayu_Internet!=0&&dëkkuwaayu_Internet!=망상태읽기(0,0))return -99;
    int 반환값=되돌림전문묶기(bara_denc_yombal,0,접속번호);if(반환값<0)return 반환값;
    int 개수=Taf_SMS(bara_denc_yombal,2);if(개수<0)return 개수;반환값=망주소묶기(개수,망상태읽기(0,0),되돌림전문접속번호(bara_denc_yombal));if(!반환값)묶인주소[bara_denc_yombal-32]=dëkkuwaayu_Internet;return 반환값;
}
int32_t 자바전문보내기(int32_t bara_denc_yombal,int32_t dëkkuwaayu_Internet,int32_t 접속번호,int32_t tolluwaay){
    if(dëkkuwaayu_Internet==0x7f000001)return 되돌림전문보내기(bara_denc_yombal,dëkkuwaayu_Internet,접속번호,tolluwaay);
    if(tolluwaay<0||tolluwaay>512)return -90;if(접속번호<1||접속번호>65535)return -22;
    if(되돌림전문접속번호(bara_denc_yombal)<0)return -9;
    if(되돌림전문주소(bara_denc_yombal)==0x7f000001)return -101;
    int 개수=외부번호(bara_denc_yombal);if(개수<0){int 반환값=0;if(되돌림전문접속번호(bara_denc_yombal)==0)반환값=되돌림전문묶기(bara_denc_yombal,0,0);if(반환값<0)return 반환값;개수=Taf_SMS(bara_denc_yombal,2);if(개수<0)return 개수;반환값=망주소묶기(개수,망상태읽기(0,0),되돌림전문접속번호(bara_denc_yombal));if(반환값<0)return 반환값;}
    unsigned char mbir[512];for(int 순번=0;순번<tolluwaay;순번++)mbir[순번]=자바전문얻기(순번);return 전문보내기(개수,mbir,tolluwaay,dëkkuwaayu_Internet,접속번호);
}
int32_t 자바전문받기(int32_t bara_denc_yombal,int32_t tolluwaay){
    int 개수=외부번호(bara_denc_yombal);if(개수<0)return 되돌림전문받기(bara_denc_yombal,tolluwaay);if(tolluwaay<0||tolluwaay>512)return -22;
    int dënnd=되돌림전문받기(bara_denc_yombal,tolluwaay);if(dënnd!=-11){전문외부상대[bara_denc_yombal-32]=0;return dënnd;}
    unsigned char mbir[512];int 반환값=전문받기(개수,mbir,tolluwaay);if(반환값>=0)전문외부상대[bara_denc_yombal-32]=1;for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,mbir[순번]);return 반환값;
}
int32_t 자바전문접속번호(int32_t bara_denc_yombal){int 개수=외부번호(bara_denc_yombal);return 개수<0?되돌림전문접속번호(bara_denc_yombal):(int32_t)통신접속번호(개수);}
int32_t 자바전문주소(int32_t bara_denc_yombal){return 외부번호(bara_denc_yombal)<0?되돌림전문주소(bara_denc_yombal):묶인주소[bara_denc_yombal-32];}
int32_t 자바전문상대(int32_t bara_denc_yombal){int 개수=외부번호(bara_denc_yombal);return 개수<0||!전문외부상대[bara_denc_yombal-32]?되돌림전문상대(bara_denc_yombal):(int32_t)상대접속번호(개수);}
int32_t 자바전문원격주소(int32_t bara_denc_yombal){int 개수=외부번호(bara_denc_yombal);return 개수<0||!전문외부상대[bara_denc_yombal-32]?0x7f000001:(int32_t)상대통신주소(개수);}
int32_t 자바전문닫기(int32_t bara_denc_yombal){int 개수=외부번호(bara_denc_yombal);if(개수>=0){Tej_mbaal(개수);외부연결[bara_denc_yombal-32]=0;}if(bara_denc_yombal>=32&&bara_denc_yombal<40)전문외부상대[bara_denc_yombal-32]=묶인주소[bara_denc_yombal-32]=0;return 되돌림전문닫기(bara_denc_yombal);}
int32_t 자바흐름만들기(void){return 되돌림흐름만들기();}
int32_t 자바흐름묶기(int32_t bara_denc_yombal,int32_t dëkkuwaayu_Internet,int32_t 접속번호){
    if(dëkkuwaayu_Internet==0||dëkkuwaayu_Internet==0x7f000001){int 반환값=되돌림흐름묶기(bara_denc_yombal,dëkkuwaayu_Internet,접속번호);if(!반환값)임의주소[bara_denc_yombal-32]=dëkkuwaayu_Internet==0;return 반환값;}
    if(dëkkuwaayu_Internet!=망상태읽기(0,0))return -99;int 반환값=되돌림흐름묶기(bara_denc_yombal,0,접속번호);if(반환값<0)return 반환값;
    int 개수=Taf_SMS(bara_denc_yombal,1);return 개수<0?개수:망주소묶기(개수,dëkkuwaayu_Internet,되돌림흐름접속번호(bara_denc_yombal));
}
int32_t 자바흐름듣기(int32_t bara_denc_yombal,int32_t 연결대기한도){
    int 개수=외부번호(bara_denc_yombal);if(개수<0){int 반환값=되돌림흐름듣기(bara_denc_yombal,연결대기한도);if(반환값<0||!임의주소[bara_denc_yombal-32])return 반환값;
        개수=Taf_SMS(bara_denc_yombal,1);if(개수<0)return 개수;반환값=망주소묶기(개수,망상태읽기(0,0),되돌림흐름접속번호(bara_denc_yombal));if(반환값<0)return 반환값;양쪽수신창구[bara_denc_yombal-32]=1;
    }return 연결대기한도<1?-22:연결기다리기(개수);
}
int32_t 자바흐름연결(int32_t bara_denc_yombal,int32_t dëkkuwaayu_Internet,int32_t 접속번호){
    if(dëkkuwaayu_Internet==0x7f000001 && 외부번호(bara_denc_yombal)<0)return 되돌림흐름연결(bara_denc_yombal,dëkkuwaayu_Internet,접속번호);
    if(되돌림흐름접속번호(bara_denc_yombal)<0)return -9;int 개수=Taf_SMS(bara_denc_yombal,1);return 개수<0?개수:망연결하기(개수,dëkkuwaayu_Internet,접속번호);
}
int32_t 자바흐름연결받기(int32_t bara_denc_yombal){
    int 개수=외부번호(bara_denc_yombal);if(개수<0)return 되돌림흐름연결받기(bara_denc_yombal);
    if(양쪽수신창구[bara_denc_yombal-32]){int dënnd=되돌림흐름연결받기(bara_denc_yombal);if(dënnd!=-11)return dënnd;}
    int Nàttangoo_xëyma=망연결받기(개수);if(Nàttangoo_xëyma<0)return Nàttangoo_xëyma;
    int luñu_name=되돌림흐름만들기();if(luñu_name<0){Tej_mbaal(Nàttangoo_xëyma);return luñu_name;}외부연결[luñu_name-32]=Nàttangoo_xëyma+1;return luñu_name;
}
int32_t 자바흐름읽기(int32_t bara_denc_yombal,int32_t tolluwaay){
    int 개수=외부번호(bara_denc_yombal);if(개수<0)return 되돌림흐름읽기(bara_denc_yombal,tolluwaay);if(tolluwaay<0||tolluwaay>512)return -22;
    unsigned char mbir[512];int 반환값=통신읽기(개수,mbir,tolluwaay);for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,mbir[순번]);return 반환값;
}
int32_t 자바흐름쓰기(int32_t bara_denc_yombal,int32_t tolluwaay){
    int 개수=외부번호(bara_denc_yombal);if(개수<0)return 되돌림흐름쓰기(bara_denc_yombal,tolluwaay);if(tolluwaay<0||tolluwaay>512)return -22;
    unsigned char mbir[512];for(int 순번=0;순번<tolluwaay;순번++)mbir[순번]=자바전문얻기(순번);return 통신쓰기(개수,mbir,tolluwaay);
}
int32_t 자바흐름접속번호(int32_t bara_denc_yombal){int 개수=외부번호(bara_denc_yombal);return 개수<0?되돌림흐름접속번호(bara_denc_yombal):(int32_t)통신접속번호(개수);}
int32_t 자바흐름상대(int32_t bara_denc_yombal){int 개수=외부번호(bara_denc_yombal);return 개수<0?되돌림흐름상대(bara_denc_yombal):(int32_t)상대접속번호(개수);}
int32_t 자바흐름주소(int32_t bara_denc_yombal){return 외부번호(bara_denc_yombal)<0?0x7f000001:양쪽수신창구[bara_denc_yombal-32]?0:망상태읽기(0,0);}
int32_t 자바흐름닫기(int32_t bara_denc_yombal){int 개수=외부번호(bara_denc_yombal);if(개수>=0){Tej_mbaal(개수);외부연결[bara_denc_yombal-32]=0;}if(bara_denc_yombal>=40&&bara_denc_yombal<56)임의주소[bara_denc_yombal-32]=양쪽수신창구[bara_denc_yombal-32]=0;return 되돌림흐름닫기(bara_denc_yombal);}
