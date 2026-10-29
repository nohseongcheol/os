#include "../명명/기계연결이름.h"
/* Preserve the deterministic Java loopback endpoints; route external IPv4 to lwIP. */
#include "Neteweke_kokoanyodinepe.h"
extern int32_t 되돌림전문만들기(int32_t,int32_t,int32_t), 되돌림전문묶기(int32_t,int32_t,int32_t);
extern int32_t 되돌림전문보내기(int32_t,int32_t,int32_t,int32_t), 되돌림전문받기(int32_t,int32_t);
extern int32_t 되돌림전문접속번호(int32_t), 되돌림전문주소(int32_t), 되돌림전문상대(int32_t), 되돌림전문닫기(int32_t);
extern int32_t 자바전문넣기(int32_t,int32_t),자바전문얻기(int32_t);
extern int32_t 되돌림흐름만들기(void),되돌림흐름묶기(int32_t,int32_t,int32_t),되돌림흐름듣기(int32_t,int32_t);
extern int32_t 되돌림흐름연결(int32_t,int32_t,int32_t),되돌림흐름연결받기(int32_t),되돌림흐름읽기(int32_t,int32_t),되돌림흐름쓰기(int32_t,int32_t);
extern int32_t 되돌림흐름접속번호(int32_t),되돌림흐름상대(int32_t),되돌림흐름닫기(int32_t);
static int 외부연결[24];
static int 임의주소[24], 양쪽수신창구[24], 전문외부상대[8], 묶인주소[8];
static int 외부번호(int faele_mokgwakamogelo) { return faele_mokgwakamogelo>=32 && faele_mokgwakamogelo<56 ? 외부연결[faele_mokgwakamogelo-32]-1 : -1; }
static int kgomaretsa_SMS(int faele_mokgwakamogelo,int tlanya_setlhopha) {
    if(faele_mokgwakamogelo<32||faele_mokgwakamogelo>=56)return -9;int 이전=외부번호(faele_mokgwakamogelo);if(이전>=0)return 이전;
    int 개수=통신끝점만들기(tlanya_setlhopha);if(개수>=0)외부연결[faele_mokgwakamogelo-32]=개수+1;return 개수;
}
int32_t 자바전문만들기(int32_t 첫째값,int32_t 둘째값,int32_t khoutuletshwao){return 되돌림전문만들기(첫째값,둘째값,khoutuletshwao);}
int32_t 자바전문묶기(int32_t faele_mokgwakamogelo,int32_t aterese_ya_Inthanete,int32_t 접속번호){
    if(aterese_ya_Inthanete==0x7f000001)return 되돌림전문묶기(faele_mokgwakamogelo,aterese_ya_Inthanete,접속번호);
    if(aterese_ya_Inthanete!=0&&aterese_ya_Inthanete!=망상태읽기(0,0))return -99;
    int 반환값=되돌림전문묶기(faele_mokgwakamogelo,0,접속번호);if(반환값<0)return 반환값;
    int 개수=kgomaretsa_SMS(faele_mokgwakamogelo,2);if(개수<0)return 개수;반환값=망주소묶기(개수,망상태읽기(0,0),되돌림전문접속번호(faele_mokgwakamogelo));if(!반환값)묶인주소[faele_mokgwakamogelo-32]=aterese_ya_Inthanete;return 반환값;
}
int32_t 자바전문보내기(int32_t faele_mokgwakamogelo,int32_t aterese_ya_Inthanete,int32_t 접속번호,int32_t lekanya){
    if(aterese_ya_Inthanete==0x7f000001)return 되돌림전문보내기(faele_mokgwakamogelo,aterese_ya_Inthanete,접속번호,lekanya);
    if(lekanya<0||lekanya>512)return -90;if(접속번호<1||접속번호>65535)return -22;
    if(되돌림전문접속번호(faele_mokgwakamogelo)<0)return -9;
    if(되돌림전문주소(faele_mokgwakamogelo)==0x7f000001)return -101;
    int 개수=외부번호(faele_mokgwakamogelo);if(개수<0){int 반환값=0;if(되돌림전문접속번호(faele_mokgwakamogelo)==0)반환값=되돌림전문묶기(faele_mokgwakamogelo,0,0);if(반환값<0)return 반환값;개수=kgomaretsa_SMS(faele_mokgwakamogelo,2);if(개수<0)return 개수;반환값=망주소묶기(개수,망상태읽기(0,0),되돌림전문접속번호(faele_mokgwakamogelo));if(반환값<0)return 반환값;}
    unsigned char tshedimosetso[512];for(int 순번=0;순번<lekanya;순번++)tshedimosetso[순번]=자바전문얻기(순번);return 전문보내기(개수,tshedimosetso,lekanya,aterese_ya_Inthanete,접속번호);
}
int32_t 자바전문받기(int32_t faele_mokgwakamogelo,int32_t lekanya){
    int 개수=외부번호(faele_mokgwakamogelo);if(개수<0)return 되돌림전문받기(faele_mokgwakamogelo,lekanya);if(lekanya<0||lekanya>512)return -22;
    int e_e_gaufi=되돌림전문받기(faele_mokgwakamogelo,lekanya);if(e_e_gaufi!=-11){전문외부상대[faele_mokgwakamogelo-32]=0;return e_e_gaufi;}
    unsigned char tshedimosetso[512];int 반환값=전문받기(개수,tshedimosetso,lekanya);if(반환값>=0)전문외부상대[faele_mokgwakamogelo-32]=1;for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,tshedimosetso[순번]);return 반환값;
}
int32_t 자바전문접속번호(int32_t faele_mokgwakamogelo){int 개수=외부번호(faele_mokgwakamogelo);return 개수<0?되돌림전문접속번호(faele_mokgwakamogelo):(int32_t)통신접속번호(개수);}
int32_t 자바전문주소(int32_t faele_mokgwakamogelo){return 외부번호(faele_mokgwakamogelo)<0?되돌림전문주소(faele_mokgwakamogelo):묶인주소[faele_mokgwakamogelo-32];}
int32_t 자바전문상대(int32_t faele_mokgwakamogelo){int 개수=외부번호(faele_mokgwakamogelo);return 개수<0||!전문외부상대[faele_mokgwakamogelo-32]?되돌림전문상대(faele_mokgwakamogelo):(int32_t)상대접속번호(개수);}
int32_t 자바전문원격주소(int32_t faele_mokgwakamogelo){int 개수=외부번호(faele_mokgwakamogelo);return 개수<0||!전문외부상대[faele_mokgwakamogelo-32]?0x7f000001:(int32_t)상대통신주소(개수);}
int32_t 자바전문닫기(int32_t faele_mokgwakamogelo){int 개수=외부번호(faele_mokgwakamogelo);if(개수>=0){tswala_Neteweke(개수);외부연결[faele_mokgwakamogelo-32]=0;}if(faele_mokgwakamogelo>=32&&faele_mokgwakamogelo<40)전문외부상대[faele_mokgwakamogelo-32]=묶인주소[faele_mokgwakamogelo-32]=0;return 되돌림전문닫기(faele_mokgwakamogelo);}
int32_t 자바흐름만들기(void){return 되돌림흐름만들기();}
int32_t 자바흐름묶기(int32_t faele_mokgwakamogelo,int32_t aterese_ya_Inthanete,int32_t 접속번호){
    if(aterese_ya_Inthanete==0||aterese_ya_Inthanete==0x7f000001){int 반환값=되돌림흐름묶기(faele_mokgwakamogelo,aterese_ya_Inthanete,접속번호);if(!반환값)임의주소[faele_mokgwakamogelo-32]=aterese_ya_Inthanete==0;return 반환값;}
    if(aterese_ya_Inthanete!=망상태읽기(0,0))return -99;int 반환값=되돌림흐름묶기(faele_mokgwakamogelo,0,접속번호);if(반환값<0)return 반환값;
    int 개수=kgomaretsa_SMS(faele_mokgwakamogelo,1);return 개수<0?개수:망주소묶기(개수,aterese_ya_Inthanete,되돌림흐름접속번호(faele_mokgwakamogelo));
}
int32_t 자바흐름듣기(int32_t faele_mokgwakamogelo,int32_t 연결대기한도){
    int 개수=외부번호(faele_mokgwakamogelo);if(개수<0){int 반환값=되돌림흐름듣기(faele_mokgwakamogelo,연결대기한도);if(반환값<0||!임의주소[faele_mokgwakamogelo-32])return 반환값;
        개수=kgomaretsa_SMS(faele_mokgwakamogelo,1);if(개수<0)return 개수;반환값=망주소묶기(개수,망상태읽기(0,0),되돌림흐름접속번호(faele_mokgwakamogelo));if(반환값<0)return 반환값;양쪽수신창구[faele_mokgwakamogelo-32]=1;
    }return 연결대기한도<1?-22:연결기다리기(개수);
}
int32_t 자바흐름연결(int32_t faele_mokgwakamogelo,int32_t aterese_ya_Inthanete,int32_t 접속번호){
    if(aterese_ya_Inthanete==0x7f000001 && 외부번호(faele_mokgwakamogelo)<0)return 되돌림흐름연결(faele_mokgwakamogelo,aterese_ya_Inthanete,접속번호);
    if(되돌림흐름접속번호(faele_mokgwakamogelo)<0)return -9;int 개수=kgomaretsa_SMS(faele_mokgwakamogelo,1);return 개수<0?개수:망연결하기(개수,aterese_ya_Inthanete,접속번호);
}
int32_t 자바흐름연결받기(int32_t faele_mokgwakamogelo){
    int 개수=외부번호(faele_mokgwakamogelo);if(개수<0)return 되돌림흐름연결받기(faele_mokgwakamogelo);
    if(양쪽수신창구[faele_mokgwakamogelo-32]){int e_e_gaufi=되돌림흐름연결받기(faele_mokgwakamogelo);if(e_e_gaufi!=-11)return e_e_gaufi;}
    int semphato_Boleng=망연결받기(개수);if(semphato_Boleng<0)return semphato_Boleng;
    int setotwa=되돌림흐름만들기();if(setotwa<0){tswala_Neteweke(semphato_Boleng);return setotwa;}외부연결[setotwa-32]=semphato_Boleng+1;return setotwa;
}
int32_t 자바흐름읽기(int32_t faele_mokgwakamogelo,int32_t lekanya){
    int 개수=외부번호(faele_mokgwakamogelo);if(개수<0)return 되돌림흐름읽기(faele_mokgwakamogelo,lekanya);if(lekanya<0||lekanya>512)return -22;
    unsigned char tshedimosetso[512];int 반환값=통신읽기(개수,tshedimosetso,lekanya);for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,tshedimosetso[순번]);return 반환값;
}
int32_t 자바흐름쓰기(int32_t faele_mokgwakamogelo,int32_t lekanya){
    int 개수=외부번호(faele_mokgwakamogelo);if(개수<0)return 되돌림흐름쓰기(faele_mokgwakamogelo,lekanya);if(lekanya<0||lekanya>512)return -22;
    unsigned char tshedimosetso[512];for(int 순번=0;순번<lekanya;순번++)tshedimosetso[순번]=자바전문얻기(순번);return 통신쓰기(개수,tshedimosetso,lekanya);
}
int32_t 자바흐름접속번호(int32_t faele_mokgwakamogelo){int 개수=외부번호(faele_mokgwakamogelo);return 개수<0?되돌림흐름접속번호(faele_mokgwakamogelo):(int32_t)통신접속번호(개수);}
int32_t 자바흐름상대(int32_t faele_mokgwakamogelo){int 개수=외부번호(faele_mokgwakamogelo);return 개수<0?되돌림흐름상대(faele_mokgwakamogelo):(int32_t)상대접속번호(개수);}
int32_t 자바흐름주소(int32_t faele_mokgwakamogelo){return 외부번호(faele_mokgwakamogelo)<0?0x7f000001:양쪽수신창구[faele_mokgwakamogelo-32]?0:망상태읽기(0,0);}
int32_t 자바흐름닫기(int32_t faele_mokgwakamogelo){int 개수=외부번호(faele_mokgwakamogelo);if(개수>=0){tswala_Neteweke(개수);외부연결[faele_mokgwakamogelo-32]=0;}if(faele_mokgwakamogelo>=40&&faele_mokgwakamogelo<56)임의주소[faele_mokgwakamogelo-32]=양쪽수신창구[faele_mokgwakamogelo-32]=0;return 되돌림흐름닫기(faele_mokgwakamogelo);}
