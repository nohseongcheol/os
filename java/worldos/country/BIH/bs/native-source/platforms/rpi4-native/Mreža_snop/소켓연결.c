#include "../명명/기계연결이름.h"
/* Preserve the deterministic Java loopback endpoints; route external IPv4 to lwIP. */
#include "Mreža_snop.h"
extern int32_t 되돌림전문만들기(int32_t,int32_t,int32_t), 되돌림전문묶기(int32_t,int32_t,int32_t);
extern int32_t 되돌림전문보내기(int32_t,int32_t,int32_t,int32_t), 되돌림전문받기(int32_t,int32_t);
extern int32_t 되돌림전문접속번호(int32_t), 되돌림전문주소(int32_t), 되돌림전문상대(int32_t), 되돌림전문닫기(int32_t);
extern int32_t 자바전문넣기(int32_t,int32_t),자바전문얻기(int32_t);
extern int32_t 되돌림흐름만들기(void),되돌림흐름묶기(int32_t,int32_t,int32_t),되돌림흐름듣기(int32_t,int32_t);
extern int32_t 되돌림흐름연결(int32_t,int32_t,int32_t),되돌림흐름연결받기(int32_t),되돌림흐름읽기(int32_t,int32_t),되돌림흐름쓰기(int32_t,int32_t);
extern int32_t 되돌림흐름접속번호(int32_t),되돌림흐름상대(int32_t),되돌림흐름닫기(int32_t);
static int iz_eksternog_izvora[24];
static int 임의주소[24], 양쪽수신창구[24], UDP_iz_eksternog_izvora_peer[8], 묶인주소[8];
static int 외부번호(int fajl_hvatište) { return fajl_hvatište>=32 && fajl_hvatište<56 ? iz_eksternog_izvora[fajl_hvatište-32]-1 : -1; }
static int zalijepiti_SMS(int fajl_hvatište,int TYPE_oblast) {
    if(fajl_hvatište<32||fajl_hvatište>=56)return -9;int 이전=외부번호(fajl_hvatište);if(이전>=0)return 이전;
    int stavka_COUNT=통신끝점만들기(TYPE_oblast);if(stavka_COUNT>=0)iz_eksternog_izvora[fajl_hvatište-32]=stavka_COUNT+1;return stavka_COUNT;
}
int32_t 자바전문만들기(int32_t 첫째값,int32_t SECOND_VALUE,int32_t kôd_znaka){return 되돌림전문만들기(첫째값,SECOND_VALUE,kôd_znaka);}
int32_t 자바전문묶기(int32_t fajl_hvatište,int32_t internetska_adresa,int32_t broj_priključka){
    if(internetska_adresa==0x7f000001)return 되돌림전문묶기(fajl_hvatište,internetska_adresa,broj_priključka);
    if(internetska_adresa!=0&&internetska_adresa!=망상태읽기(0,0))return -99;
    int 반환값=되돌림전문묶기(fajl_hvatište,0,broj_priključka);if(반환값<0)return 반환값;
    int stavka_COUNT=zalijepiti_SMS(fajl_hvatište,2);if(stavka_COUNT<0)return stavka_COUNT;반환값=망주소묶기(stavka_COUNT,망상태읽기(0,0),되돌림전문접속번호(fajl_hvatište));if(!반환값)묶인주소[fajl_hvatište-32]=internetska_adresa;return 반환값;
}
int32_t 자바전문보내기(int32_t fajl_hvatište,int32_t internetska_adresa,int32_t broj_priključka,int32_t Veličina){
    if(internetska_adresa==0x7f000001)return 되돌림전문보내기(fajl_hvatište,internetska_adresa,broj_priključka,Veličina);
    if(Veličina<0||Veličina>512)return -90;if(broj_priključka<1||broj_priključka>65535)return -22;
    if(되돌림전문접속번호(fajl_hvatište)<0)return -9;
    if(되돌림전문주소(fajl_hvatište)==0x7f000001)return -101;
    int stavka_COUNT=외부번호(fajl_hvatište);if(stavka_COUNT<0){int 반환값=0;if(되돌림전문접속번호(fajl_hvatište)==0)반환값=되돌림전문묶기(fajl_hvatište,0,0);if(반환값<0)return 반환값;stavka_COUNT=zalijepiti_SMS(fajl_hvatište,2);if(stavka_COUNT<0)return stavka_COUNT;반환값=망주소묶기(stavka_COUNT,망상태읽기(0,0),되돌림전문접속번호(fajl_hvatište));if(반환값<0)return 반환값;}
    unsigned char podaci[512];for(int 순번=0;순번<Veličina;순번++)podaci[순번]=자바전문얻기(순번);return 전문보내기(stavka_COUNT,podaci,Veličina,internetska_adresa,broj_priključka);
}
int32_t 자바전문받기(int32_t fajl_hvatište,int32_t Veličina){
    int stavka_COUNT=외부번호(fajl_hvatište);if(stavka_COUNT<0)return 되돌림전문받기(fajl_hvatište,Veličina);if(Veličina<0||Veličina>512)return -22;
    int lokalni=되돌림전문받기(fajl_hvatište,Veličina);if(lokalni!=-11){UDP_iz_eksternog_izvora_peer[fajl_hvatište-32]=0;return lokalni;}
    unsigned char podaci[512];int 반환값=전문받기(stavka_COUNT,podaci,Veličina);if(반환값>=0)UDP_iz_eksternog_izvora_peer[fajl_hvatište-32]=1;for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,podaci[순번]);return 반환값;
}
int32_t 자바전문접속번호(int32_t fajl_hvatište){int stavka_COUNT=외부번호(fajl_hvatište);return stavka_COUNT<0?되돌림전문접속번호(fajl_hvatište):(int32_t)Mreža_broj_priključka(stavka_COUNT);}
int32_t 자바전문주소(int32_t fajl_hvatište){return 외부번호(fajl_hvatište)<0?되돌림전문주소(fajl_hvatište):묶인주소[fajl_hvatište-32];}
int32_t 자바전문상대(int32_t fajl_hvatište){int stavka_COUNT=외부번호(fajl_hvatište);return stavka_COUNT<0||!UDP_iz_eksternog_izvora_peer[fajl_hvatište-32]?되돌림전문상대(fajl_hvatište):(int32_t)peer_broj_priključka(stavka_COUNT);}
int32_t 자바전문원격주소(int32_t fajl_hvatište){int stavka_COUNT=외부번호(fajl_hvatište);return stavka_COUNT<0||!UDP_iz_eksternog_izvora_peer[fajl_hvatište-32]?0x7f000001:(int32_t)상대통신주소(stavka_COUNT);}
int32_t 자바전문닫기(int32_t fajl_hvatište){int stavka_COUNT=외부번호(fajl_hvatište);if(stavka_COUNT>=0){zatvoriti_Mreža(stavka_COUNT);iz_eksternog_izvora[fajl_hvatište-32]=0;}if(fajl_hvatište>=32&&fajl_hvatište<40)UDP_iz_eksternog_izvora_peer[fajl_hvatište-32]=묶인주소[fajl_hvatište-32]=0;return 되돌림전문닫기(fajl_hvatište);}
int32_t 자바흐름만들기(void){return 되돌림흐름만들기();}
int32_t 자바흐름묶기(int32_t fajl_hvatište,int32_t internetska_adresa,int32_t broj_priključka){
    if(internetska_adresa==0||internetska_adresa==0x7f000001){int 반환값=되돌림흐름묶기(fajl_hvatište,internetska_adresa,broj_priključka);if(!반환값)임의주소[fajl_hvatište-32]=internetska_adresa==0;return 반환값;}
    if(internetska_adresa!=망상태읽기(0,0))return -99;int 반환값=되돌림흐름묶기(fajl_hvatište,0,broj_priključka);if(반환값<0)return 반환값;
    int stavka_COUNT=zalijepiti_SMS(fajl_hvatište,1);return stavka_COUNT<0?stavka_COUNT:망주소묶기(stavka_COUNT,internetska_adresa,되돌림흐름접속번호(fajl_hvatište));
}
int32_t 자바흐름듣기(int32_t fajl_hvatište,int32_t 연결대기한도){
    int stavka_COUNT=외부번호(fajl_hvatište);if(stavka_COUNT<0){int 반환값=되돌림흐름듣기(fajl_hvatište,연결대기한도);if(반환값<0||!임의주소[fajl_hvatište-32])return 반환값;
        stavka_COUNT=zalijepiti_SMS(fajl_hvatište,1);if(stavka_COUNT<0)return stavka_COUNT;반환값=망주소묶기(stavka_COUNT,망상태읽기(0,0),되돌림흐름접속번호(fajl_hvatište));if(반환값<0)return 반환값;양쪽수신창구[fajl_hvatište-32]=1;
    }return 연결대기한도<1?-22:연결기다리기(stavka_COUNT);
}
int32_t 자바흐름연결(int32_t fajl_hvatište,int32_t internetska_adresa,int32_t broj_priključka){
    if(internetska_adresa==0x7f000001 && 외부번호(fajl_hvatište)<0)return 되돌림흐름연결(fajl_hvatište,internetska_adresa,broj_priključka);
    if(되돌림흐름접속번호(fajl_hvatište)<0)return -9;int stavka_COUNT=zalijepiti_SMS(fajl_hvatište,1);return stavka_COUNT<0?stavka_COUNT:망연결하기(stavka_COUNT,internetska_adresa,broj_priključka);
}
int32_t 자바흐름연결받기(int32_t fajl_hvatište){
    int stavka_COUNT=외부번호(fajl_hvatište);if(stavka_COUNT<0)return 되돌림흐름연결받기(fajl_hvatište);
    if(양쪽수신창구[fajl_hvatište-32]){int lokalni=되돌림흐름연결받기(fajl_hvatište);if(lokalni!=-11)return lokalni;}
    int peer_VALUE=망연결받기(stavka_COUNT);if(peer_VALUE<0)return peer_VALUE;
    int cilj=되돌림흐름만들기();if(cilj<0){zatvoriti_Mreža(peer_VALUE);return cilj;}iz_eksternog_izvora[cilj-32]=peer_VALUE+1;return cilj;
}
int32_t 자바흐름읽기(int32_t fajl_hvatište,int32_t Veličina){
    int stavka_COUNT=외부번호(fajl_hvatište);if(stavka_COUNT<0)return 되돌림흐름읽기(fajl_hvatište,Veličina);if(Veličina<0||Veličina>512)return -22;
    unsigned char podaci[512];int 반환값=통신읽기(stavka_COUNT,podaci,Veličina);for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,podaci[순번]);return 반환값;
}
int32_t 자바흐름쓰기(int32_t fajl_hvatište,int32_t Veličina){
    int stavka_COUNT=외부번호(fajl_hvatište);if(stavka_COUNT<0)return 되돌림흐름쓰기(fajl_hvatište,Veličina);if(Veličina<0||Veličina>512)return -22;
    unsigned char podaci[512];for(int 순번=0;순번<Veličina;순번++)podaci[순번]=자바전문얻기(순번);return 통신쓰기(stavka_COUNT,podaci,Veličina);
}
int32_t 자바흐름접속번호(int32_t fajl_hvatište){int stavka_COUNT=외부번호(fajl_hvatište);return stavka_COUNT<0?되돌림흐름접속번호(fajl_hvatište):(int32_t)Mreža_broj_priključka(stavka_COUNT);}
int32_t 자바흐름상대(int32_t fajl_hvatište){int stavka_COUNT=외부번호(fajl_hvatište);return stavka_COUNT<0?되돌림흐름상대(fajl_hvatište):(int32_t)peer_broj_priključka(stavka_COUNT);}
int32_t 자바흐름주소(int32_t fajl_hvatište){return 외부번호(fajl_hvatište)<0?0x7f000001:양쪽수신창구[fajl_hvatište-32]?0:망상태읽기(0,0);}
int32_t 자바흐름닫기(int32_t fajl_hvatište){int stavka_COUNT=외부번호(fajl_hvatište);if(stavka_COUNT>=0){zatvoriti_Mreža(stavka_COUNT);iz_eksternog_izvora[fajl_hvatište-32]=0;}if(fajl_hvatište>=40&&fajl_hvatište<56)임의주소[fajl_hvatište-32]=양쪽수신창구[fajl_hvatište-32]=0;return 되돌림흐름닫기(fajl_hvatište);}
