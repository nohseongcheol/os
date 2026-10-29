#include "../명명/기계연결이름.h"
/* Preserve the deterministic Java loopback endpoints; route external IPv4 to lwIP. */
#include "sare_pila.h"
extern int32_t 되돌림전문만들기(int32_t,int32_t,int32_t), 되돌림전문묶기(int32_t,int32_t,int32_t);
extern int32_t 되돌림전문보내기(int32_t,int32_t,int32_t,int32_t), 되돌림전문받기(int32_t,int32_t);
extern int32_t 되돌림전문접속번호(int32_t), 되돌림전문주소(int32_t), 되돌림전문상대(int32_t), 되돌림전문닫기(int32_t);
extern int32_t 자바전문넣기(int32_t,int32_t),자바전문얻기(int32_t);
extern int32_t 되돌림흐름만들기(void),되돌림흐름묶기(int32_t,int32_t,int32_t),되돌림흐름듣기(int32_t,int32_t);
extern int32_t 되돌림흐름연결(int32_t,int32_t,int32_t),되돌림흐름연결받기(int32_t),되돌림흐름읽기(int32_t,int32_t),되돌림흐름쓰기(int32_t,int32_t);
extern int32_t 되돌림흐름접속번호(int32_t),되돌림흐름상대(int32_t),되돌림흐름닫기(int32_t);
static int 외부연결[24];
static int 임의주소[24], 양쪽수신창구[24], 전문외부상대[8], 묶인주소[8];
static int 외부번호(int fitxategi_helduleku) { return fitxategi_helduleku>=32 && fitxategi_helduleku<56 ? 외부연결[fitxategi_helduleku-32]-1 : -1; }
static int itsatsi_SMS(int fitxategi_helduleku,int MOTA_Kategoria) {
    if(fitxategi_helduleku<32||fitxategi_helduleku>=56)return -9;int 이전=외부번호(fitxategi_helduleku);if(이전>=0)return 이전;
    int elementu_ZENBATU=통신끝점만들기(MOTA_Kategoria);if(elementu_ZENBATU>=0)외부연결[fitxategi_helduleku-32]=elementu_ZENBATU+1;return elementu_ZENBATU;
}
int32_t 자바전문만들기(int32_t 첫째값,int32_t SEGUNDOA_balio,int32_t karaktere_kode){return 되돌림전문만들기(첫째값,SEGUNDOA_balio,karaktere_kode);}
int32_t 자바전문묶기(int32_t fitxategi_helduleku,int32_t Internet_helbide,int32_t ataka_zenbaki){
    if(Internet_helbide==0x7f000001)return 되돌림전문묶기(fitxategi_helduleku,Internet_helbide,ataka_zenbaki);
    if(Internet_helbide!=0&&Internet_helbide!=망상태읽기(0,0))return -99;
    int 반환값=되돌림전문묶기(fitxategi_helduleku,0,ataka_zenbaki);if(반환값<0)return 반환값;
    int elementu_ZENBATU=itsatsi_SMS(fitxategi_helduleku,2);if(elementu_ZENBATU<0)return elementu_ZENBATU;반환값=망주소묶기(elementu_ZENBATU,망상태읽기(0,0),되돌림전문접속번호(fitxategi_helduleku));if(!반환값)묶인주소[fitxategi_helduleku-32]=Internet_helbide;return 반환값;
}
int32_t 자바전문보내기(int32_t fitxategi_helduleku,int32_t Internet_helbide,int32_t ataka_zenbaki,int32_t Tamaina){
    if(Internet_helbide==0x7f000001)return 되돌림전문보내기(fitxategi_helduleku,Internet_helbide,ataka_zenbaki,Tamaina);
    if(Tamaina<0||Tamaina>512)return -90;if(ataka_zenbaki<1||ataka_zenbaki>65535)return -22;
    if(되돌림전문접속번호(fitxategi_helduleku)<0)return -9;
    if(되돌림전문주소(fitxategi_helduleku)==0x7f000001)return -101;
    int elementu_ZENBATU=외부번호(fitxategi_helduleku);if(elementu_ZENBATU<0){int 반환값=0;if(되돌림전문접속번호(fitxategi_helduleku)==0)반환값=되돌림전문묶기(fitxategi_helduleku,0,0);if(반환값<0)return 반환값;elementu_ZENBATU=itsatsi_SMS(fitxategi_helduleku,2);if(elementu_ZENBATU<0)return elementu_ZENBATU;반환값=망주소묶기(elementu_ZENBATU,망상태읽기(0,0),되돌림전문접속번호(fitxategi_helduleku));if(반환값<0)return 반환값;}
    unsigned char datuak[512];for(int 순번=0;순번<Tamaina;순번++)datuak[순번]=자바전문얻기(순번);return 전문보내기(elementu_ZENBATU,datuak,Tamaina,Internet_helbide,ataka_zenbaki);
}
int32_t 자바전문받기(int32_t fitxategi_helduleku,int32_t Tamaina){
    int elementu_ZENBATU=외부번호(fitxategi_helduleku);if(elementu_ZENBATU<0)return 되돌림전문받기(fitxategi_helduleku,Tamaina);if(Tamaina<0||Tamaina>512)return -22;
    int lokal=되돌림전문받기(fitxategi_helduleku,Tamaina);if(lokal!=-11){전문외부상대[fitxategi_helduleku-32]=0;return lokal;}
    unsigned char datuak[512];int 반환값=전문받기(elementu_ZENBATU,datuak,Tamaina);if(반환값>=0)전문외부상대[fitxategi_helduleku-32]=1;for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,datuak[순번]);return 반환값;
}
int32_t 자바전문접속번호(int32_t fitxategi_helduleku){int elementu_ZENBATU=외부번호(fitxategi_helduleku);return elementu_ZENBATU<0?되돌림전문접속번호(fitxategi_helduleku):(int32_t)sare_ataka_zenbaki(elementu_ZENBATU);}
int32_t 자바전문주소(int32_t fitxategi_helduleku){return 외부번호(fitxategi_helduleku)<0?되돌림전문주소(fitxategi_helduleku):묶인주소[fitxategi_helduleku-32];}
int32_t 자바전문상대(int32_t fitxategi_helduleku){int elementu_ZENBATU=외부번호(fitxategi_helduleku);return elementu_ZENBATU<0||!전문외부상대[fitxategi_helduleku-32]?되돌림전문상대(fitxategi_helduleku):(int32_t)pareko_ataka_zenbaki(elementu_ZENBATU);}
int32_t 자바전문원격주소(int32_t fitxategi_helduleku){int elementu_ZENBATU=외부번호(fitxategi_helduleku);return elementu_ZENBATU<0||!전문외부상대[fitxategi_helduleku-32]?0x7f000001:(int32_t)상대통신주소(elementu_ZENBATU);}
int32_t 자바전문닫기(int32_t fitxategi_helduleku){int elementu_ZENBATU=외부번호(fitxategi_helduleku);if(elementu_ZENBATU>=0){itxi_sare(elementu_ZENBATU);외부연결[fitxategi_helduleku-32]=0;}if(fitxategi_helduleku>=32&&fitxategi_helduleku<40)전문외부상대[fitxategi_helduleku-32]=묶인주소[fitxategi_helduleku-32]=0;return 되돌림전문닫기(fitxategi_helduleku);}
int32_t 자바흐름만들기(void){return 되돌림흐름만들기();}
int32_t 자바흐름묶기(int32_t fitxategi_helduleku,int32_t Internet_helbide,int32_t ataka_zenbaki){
    if(Internet_helbide==0||Internet_helbide==0x7f000001){int 반환값=되돌림흐름묶기(fitxategi_helduleku,Internet_helbide,ataka_zenbaki);if(!반환값)임의주소[fitxategi_helduleku-32]=Internet_helbide==0;return 반환값;}
    if(Internet_helbide!=망상태읽기(0,0))return -99;int 반환값=되돌림흐름묶기(fitxategi_helduleku,0,ataka_zenbaki);if(반환값<0)return 반환값;
    int elementu_ZENBATU=itsatsi_SMS(fitxategi_helduleku,1);return elementu_ZENBATU<0?elementu_ZENBATU:망주소묶기(elementu_ZENBATU,Internet_helbide,되돌림흐름접속번호(fitxategi_helduleku));
}
int32_t 자바흐름듣기(int32_t fitxategi_helduleku,int32_t 연결대기한도){
    int elementu_ZENBATU=외부번호(fitxategi_helduleku);if(elementu_ZENBATU<0){int 반환값=되돌림흐름듣기(fitxategi_helduleku,연결대기한도);if(반환값<0||!임의주소[fitxategi_helduleku-32])return 반환값;
        elementu_ZENBATU=itsatsi_SMS(fitxategi_helduleku,1);if(elementu_ZENBATU<0)return elementu_ZENBATU;반환값=망주소묶기(elementu_ZENBATU,망상태읽기(0,0),되돌림흐름접속번호(fitxategi_helduleku));if(반환값<0)return 반환값;양쪽수신창구[fitxategi_helduleku-32]=1;
    }return 연결대기한도<1?-22:연결기다리기(elementu_ZENBATU);
}
int32_t 자바흐름연결(int32_t fitxategi_helduleku,int32_t Internet_helbide,int32_t ataka_zenbaki){
    if(Internet_helbide==0x7f000001 && 외부번호(fitxategi_helduleku)<0)return 되돌림흐름연결(fitxategi_helduleku,Internet_helbide,ataka_zenbaki);
    if(되돌림흐름접속번호(fitxategi_helduleku)<0)return -9;int elementu_ZENBATU=itsatsi_SMS(fitxategi_helduleku,1);return elementu_ZENBATU<0?elementu_ZENBATU:망연결하기(elementu_ZENBATU,Internet_helbide,ataka_zenbaki);
}
int32_t 자바흐름연결받기(int32_t fitxategi_helduleku){
    int elementu_ZENBATU=외부번호(fitxategi_helduleku);if(elementu_ZENBATU<0)return 되돌림흐름연결받기(fitxategi_helduleku);
    if(양쪽수신창구[fitxategi_helduleku-32]){int lokal=되돌림흐름연결받기(fitxategi_helduleku);if(lokal!=-11)return lokal;}
    int pareko_balio=망연결받기(elementu_ZENBATU);if(pareko_balio<0)return pareko_balio;
    int helburu_balio=되돌림흐름만들기();if(helburu_balio<0){itxi_sare(pareko_balio);return helburu_balio;}외부연결[helburu_balio-32]=pareko_balio+1;return helburu_balio;
}
int32_t 자바흐름읽기(int32_t fitxategi_helduleku,int32_t Tamaina){
    int elementu_ZENBATU=외부번호(fitxategi_helduleku);if(elementu_ZENBATU<0)return 되돌림흐름읽기(fitxategi_helduleku,Tamaina);if(Tamaina<0||Tamaina>512)return -22;
    unsigned char datuak[512];int 반환값=통신읽기(elementu_ZENBATU,datuak,Tamaina);for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,datuak[순번]);return 반환값;
}
int32_t 자바흐름쓰기(int32_t fitxategi_helduleku,int32_t Tamaina){
    int elementu_ZENBATU=외부번호(fitxategi_helduleku);if(elementu_ZENBATU<0)return 되돌림흐름쓰기(fitxategi_helduleku,Tamaina);if(Tamaina<0||Tamaina>512)return -22;
    unsigned char datuak[512];for(int 순번=0;순번<Tamaina;순번++)datuak[순번]=자바전문얻기(순번);return 통신쓰기(elementu_ZENBATU,datuak,Tamaina);
}
int32_t 자바흐름접속번호(int32_t fitxategi_helduleku){int elementu_ZENBATU=외부번호(fitxategi_helduleku);return elementu_ZENBATU<0?되돌림흐름접속번호(fitxategi_helduleku):(int32_t)sare_ataka_zenbaki(elementu_ZENBATU);}
int32_t 자바흐름상대(int32_t fitxategi_helduleku){int elementu_ZENBATU=외부번호(fitxategi_helduleku);return elementu_ZENBATU<0?되돌림흐름상대(fitxategi_helduleku):(int32_t)pareko_ataka_zenbaki(elementu_ZENBATU);}
int32_t 자바흐름주소(int32_t fitxategi_helduleku){return 외부번호(fitxategi_helduleku)<0?0x7f000001:양쪽수신창구[fitxategi_helduleku-32]?0:망상태읽기(0,0);}
int32_t 자바흐름닫기(int32_t fitxategi_helduleku){int elementu_ZENBATU=외부번호(fitxategi_helduleku);if(elementu_ZENBATU>=0){itxi_sare(elementu_ZENBATU);외부연결[fitxategi_helduleku-32]=0;}if(fitxategi_helduleku>=40&&fitxategi_helduleku<56)임의주소[fitxategi_helduleku-32]=양쪽수신창구[fitxategi_helduleku-32]=0;return 되돌림흐름닫기(fitxategi_helduleku);}
