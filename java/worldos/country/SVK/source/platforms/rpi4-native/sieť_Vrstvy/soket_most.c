#include "../명명/기계연결이름.h"
/* Preserve the deterministic Java loopback endpoints; route external IPv4 to lwIP. */
#include "sieť_Vrstvy.h"
extern int32_t 되돌림전문만들기(int32_t,int32_t,int32_t), 되돌림전문묶기(int32_t,int32_t,int32_t);
extern int32_t 되돌림전문보내기(int32_t,int32_t,int32_t,int32_t), 되돌림전문받기(int32_t,int32_t);
extern int32_t 되돌림전문접속번호(int32_t), 되돌림전문주소(int32_t), 되돌림전문상대(int32_t), 되돌림전문닫기(int32_t);
extern int32_t 자바전문넣기(int32_t,int32_t),자바전문얻기(int32_t);
extern int32_t 되돌림흐름만들기(void),되돌림흐름묶기(int32_t,int32_t,int32_t),되돌림흐름듣기(int32_t,int32_t);
extern int32_t 되돌림흐름연결(int32_t,int32_t,int32_t),되돌림흐름연결받기(int32_t),되돌림흐름읽기(int32_t,int32_t),되돌림흐름쓰기(int32_t,int32_t);
extern int32_t 되돌림흐름접속번호(int32_t),되돌림흐름상대(int32_t),되돌림흐름닫기(int32_t);
static int externý[24];
static int 임의주소[24], 양쪽수신창구[24], UDP_externý_partnerský_uzol[8], hranica_adresa[8];
static int 외부번호(int Súbor_rukoväť) { return Súbor_rukoväť>=32 && Súbor_rukoväť<56 ? externý[Súbor_rukoväť-32]-1 : -1; }
static int prilepiť_SMS(int Súbor_rukoväť,int Typ_oblasť) {
    if(Súbor_rukoväť<32||Súbor_rukoväť>=56)return -9;int 이전=외부번호(Súbor_rukoväť);if(이전>=0)return 이전;
    int položka_COUNT=Create_soket_účastník(Typ_oblasť);if(položka_COUNT>=0)externý[Súbor_rukoväť-32]=položka_COUNT+1;return položka_COUNT;
}
int32_t 자바전문만들기(int32_t 첫째값,int32_t SECOND_VALUE,int32_t bod_kódu){return 되돌림전문만들기(첫째값,SECOND_VALUE,bod_kódu);}
int32_t 자바전문묶기(int32_t Súbor_rukoväť,int32_t internetová_adresa,int32_t číslo_portu){
    if(internetová_adresa==0x7f000001)return 되돌림전문묶기(Súbor_rukoväť,internetová_adresa,číslo_portu);
    if(internetová_adresa!=0&&internetová_adresa!=망상태읽기(0,0))return -99;
    int 반환값=되돌림전문묶기(Súbor_rukoväť,0,číslo_portu);if(반환값<0)return 반환값;
    int položka_COUNT=prilepiť_SMS(Súbor_rukoväť,2);if(položka_COUNT<0)return položka_COUNT;반환값=NET_BIND(položka_COUNT,망상태읽기(0,0),되돌림전문접속번호(Súbor_rukoväť));if(!반환값)hranica_adresa[Súbor_rukoväť-32]=internetová_adresa;return 반환값;
}
int32_t 자바전문보내기(int32_t Súbor_rukoväť,int32_t internetová_adresa,int32_t číslo_portu,int32_t Veľkosť){
    if(internetová_adresa==0x7f000001)return 되돌림전문보내기(Súbor_rukoväť,internetová_adresa,číslo_portu,Veľkosť);
    if(Veľkosť<0||Veľkosť>512)return -90;if(číslo_portu<1||číslo_portu>65535)return -22;
    if(되돌림전문접속번호(Súbor_rukoväť)<0)return -9;
    if(되돌림전문주소(Súbor_rukoväť)==0x7f000001)return -101;
    int položka_COUNT=외부번호(Súbor_rukoväť);if(položka_COUNT<0){int 반환값=0;if(되돌림전문접속번호(Súbor_rukoväť)==0)반환값=되돌림전문묶기(Súbor_rukoväť,0,0);if(반환값<0)return 반환값;položka_COUNT=prilepiť_SMS(Súbor_rukoväť,2);if(položka_COUNT<0)return položka_COUNT;반환값=NET_BIND(položka_COUNT,망상태읽기(0,0),되돌림전문접속번호(Súbor_rukoväť));if(반환값<0)return 반환값;}
    unsigned char údaje[512];for(int 순번=0;순번<Veľkosť;순번++)údaje[순번]=자바전문얻기(순번);return odoslať_datagram(položka_COUNT,údaje,Veľkosť,internetová_adresa,číslo_portu);
}
int32_t 자바전문받기(int32_t Súbor_rukoväť,int32_t Veľkosť){
    int položka_COUNT=외부번호(Súbor_rukoväť);if(položka_COUNT<0)return 되돌림전문받기(Súbor_rukoväť,Veľkosť);if(Veľkosť<0||Veľkosť>512)return -22;
    int miestny=되돌림전문받기(Súbor_rukoväť,Veľkosť);if(miestny!=-11){UDP_externý_partnerský_uzol[Súbor_rukoväť-32]=0;return miestny;}
    unsigned char údaje[512];int 반환값=dostať_datagram(položka_COUNT,údaje,Veľkosť);if(반환값>=0)UDP_externý_partnerský_uzol[Súbor_rukoväť-32]=1;for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,údaje[순번]);return 반환값;
}
int32_t 자바전문접속번호(int32_t Súbor_rukoväť){int položka_COUNT=외부번호(Súbor_rukoväť);return položka_COUNT<0?되돌림전문접속번호(Súbor_rukoväť):(int32_t)sieť_číslo_portu(položka_COUNT);}
int32_t 자바전문주소(int32_t Súbor_rukoväť){return 외부번호(Súbor_rukoväť)<0?되돌림전문주소(Súbor_rukoväť):hranica_adresa[Súbor_rukoväť-32];}
int32_t 자바전문상대(int32_t Súbor_rukoväť){int položka_COUNT=외부번호(Súbor_rukoväť);return položka_COUNT<0||!UDP_externý_partnerský_uzol[Súbor_rukoväť-32]?되돌림전문상대(Súbor_rukoväť):(int32_t)partnerský_uzol_číslo_portu(položka_COUNT);}
int32_t 자바전문원격주소(int32_t Súbor_rukoväť){int položka_COUNT=외부번호(Súbor_rukoväť);return položka_COUNT<0||!UDP_externý_partnerský_uzol[Súbor_rukoväť-32]?0x7f000001:(int32_t)NET_partnerský_uzol_adresa(položka_COUNT);}
int32_t 자바전문닫기(int32_t Súbor_rukoväť){int položka_COUNT=외부번호(Súbor_rukoväť);if(položka_COUNT>=0){Zavrieť_sieť(položka_COUNT);externý[Súbor_rukoväť-32]=0;}if(Súbor_rukoväť>=32&&Súbor_rukoväť<40)UDP_externý_partnerský_uzol[Súbor_rukoväť-32]=hranica_adresa[Súbor_rukoväť-32]=0;return 되돌림전문닫기(Súbor_rukoväť);}
int32_t 자바흐름만들기(void){return 되돌림흐름만들기();}
int32_t 자바흐름묶기(int32_t Súbor_rukoväť,int32_t internetová_adresa,int32_t číslo_portu){
    if(internetová_adresa==0||internetová_adresa==0x7f000001){int 반환값=되돌림흐름묶기(Súbor_rukoväť,internetová_adresa,číslo_portu);if(!반환값)임의주소[Súbor_rukoväť-32]=internetová_adresa==0;return 반환값;}
    if(internetová_adresa!=망상태읽기(0,0))return -99;int 반환값=되돌림흐름묶기(Súbor_rukoväť,0,číslo_portu);if(반환값<0)return 반환값;
    int položka_COUNT=prilepiť_SMS(Súbor_rukoväť,1);return položka_COUNT<0?položka_COUNT:NET_BIND(položka_COUNT,internetová_adresa,되돌림흐름접속번호(Súbor_rukoväť));
}
int32_t 자바흐름듣기(int32_t Súbor_rukoväť,int32_t 연결대기한도){
    int položka_COUNT=외부번호(Súbor_rukoväť);if(položka_COUNT<0){int 반환값=되돌림흐름듣기(Súbor_rukoväť,연결대기한도);if(반환값<0||!임의주소[Súbor_rukoväť-32])return 반환값;
        položka_COUNT=prilepiť_SMS(Súbor_rukoväť,1);if(položka_COUNT<0)return položka_COUNT;반환값=NET_BIND(položka_COUNT,망상태읽기(0,0),되돌림흐름접속번호(Súbor_rukoväť));if(반환값<0)return 반환값;양쪽수신창구[Súbor_rukoväť-32]=1;
    }return 연결대기한도<1?-22:NET_načúvať(položka_COUNT);
}
int32_t 자바흐름연결(int32_t Súbor_rukoväť,int32_t internetová_adresa,int32_t číslo_portu){
    if(internetová_adresa==0x7f000001 && 외부번호(Súbor_rukoväť)<0)return 되돌림흐름연결(Súbor_rukoväť,internetová_adresa,číslo_portu);
    if(되돌림흐름접속번호(Súbor_rukoväť)<0)return -9;int položka_COUNT=prilepiť_SMS(Súbor_rukoväť,1);return položka_COUNT<0?položka_COUNT:NET_spojiť(položka_COUNT,internetová_adresa,číslo_portu);
}
int32_t 자바흐름연결받기(int32_t Súbor_rukoväť){
    int položka_COUNT=외부번호(Súbor_rukoväť);if(položka_COUNT<0)return 되돌림흐름연결받기(Súbor_rukoväť);
    if(양쪽수신창구[Súbor_rukoväť-32]){int miestny=되돌림흐름연결받기(Súbor_rukoväť);if(miestny!=-11)return miestny;}
    int partnerský_uzol_VALUE=NET_prijať(položka_COUNT);if(partnerský_uzol_VALUE<0)return partnerský_uzol_VALUE;
    int cieľová_hodnota=되돌림흐름만들기();if(cieľová_hodnota<0){Zavrieť_sieť(partnerský_uzol_VALUE);return cieľová_hodnota;}externý[cieľová_hodnota-32]=partnerský_uzol_VALUE+1;return cieľová_hodnota;
}
int32_t 자바흐름읽기(int32_t Súbor_rukoväť,int32_t Veľkosť){
    int položka_COUNT=외부번호(Súbor_rukoväť);if(položka_COUNT<0)return 되돌림흐름읽기(Súbor_rukoväť,Veľkosť);if(Veľkosť<0||Veľkosť>512)return -22;
    unsigned char údaje[512];int 반환값=통신읽기(položka_COUNT,údaje,Veľkosť);for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,údaje[순번]);return 반환값;
}
int32_t 자바흐름쓰기(int32_t Súbor_rukoväť,int32_t Veľkosť){
    int položka_COUNT=외부번호(Súbor_rukoväť);if(položka_COUNT<0)return 되돌림흐름쓰기(Súbor_rukoväť,Veľkosť);if(Veľkosť<0||Veľkosť>512)return -22;
    unsigned char údaje[512];for(int 순번=0;순번<Veľkosť;순번++)údaje[순번]=자바전문얻기(순번);return NET_zapísať(položka_COUNT,údaje,Veľkosť);
}
int32_t 자바흐름접속번호(int32_t Súbor_rukoväť){int položka_COUNT=외부번호(Súbor_rukoväť);return položka_COUNT<0?되돌림흐름접속번호(Súbor_rukoväť):(int32_t)sieť_číslo_portu(položka_COUNT);}
int32_t 자바흐름상대(int32_t Súbor_rukoväť){int položka_COUNT=외부번호(Súbor_rukoväť);return položka_COUNT<0?되돌림흐름상대(Súbor_rukoväť):(int32_t)partnerský_uzol_číslo_portu(položka_COUNT);}
int32_t 자바흐름주소(int32_t Súbor_rukoväť){return 외부번호(Súbor_rukoväť)<0?0x7f000001:양쪽수신창구[Súbor_rukoväť-32]?0:망상태읽기(0,0);}
int32_t 자바흐름닫기(int32_t Súbor_rukoväť){int položka_COUNT=외부번호(Súbor_rukoväť);if(položka_COUNT>=0){Zavrieť_sieť(položka_COUNT);externý[Súbor_rukoväť-32]=0;}if(Súbor_rukoväť>=40&&Súbor_rukoväť<56)임의주소[Súbor_rukoväť-32]=양쪽수신창구[Súbor_rukoväť-32]=0;return 되돌림흐름닫기(Súbor_rukoväť);}
