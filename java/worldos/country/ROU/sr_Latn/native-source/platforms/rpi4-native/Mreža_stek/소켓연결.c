#include "../명명/기계연결이름.h"
/* Preserve the deterministic Java loopback endpoints; route external IPv4 to lwIP. */
#include "Mreža_stek.h"
extern int32_t 되돌림전문만들기(int32_t,int32_t,int32_t), 되돌림전문묶기(int32_t,int32_t,int32_t);
extern int32_t 되돌림전문보내기(int32_t,int32_t,int32_t,int32_t), 되돌림전문받기(int32_t,int32_t);
extern int32_t 되돌림전문접속번호(int32_t), 되돌림전문주소(int32_t), 되돌림전문상대(int32_t), 되돌림전문닫기(int32_t);
extern int32_t 자바전문넣기(int32_t,int32_t),자바전문얻기(int32_t);
extern int32_t 되돌림흐름만들기(void),되돌림흐름묶기(int32_t,int32_t,int32_t),되돌림흐름듣기(int32_t,int32_t);
extern int32_t 되돌림흐름연결(int32_t,int32_t,int32_t),되돌림흐름연결받기(int32_t),되돌림흐름읽기(int32_t,int32_t),되돌림흐름쓰기(int32_t,int32_t);
extern int32_t 되돌림흐름접속번호(int32_t),되돌림흐름상대(int32_t),되돌림흐름닫기(int32_t);
static int spoljni[24];
static int 임의주소[24], 양쪽수신창구[24], UDP_spoljni_ravnopravni_uređaj[8], ograničen_adresa[8];
static int 외부번호(int Datoteka_pokazivač) { return Datoteka_pokazivač>=32 && Datoteka_pokazivač<56 ? spoljni[Datoteka_pokazivač-32]-1 : -1; }
static int nalepiti_SMS(int Datoteka_pokazivač,int tip_oblast) {
    if(Datoteka_pokazivač<32||Datoteka_pokazivač>=56)return -9;int 이전=외부번호(Datoteka_pokazivač);if(이전>=0)return 이전;
    int stavka_COUNT=통신끝점만들기(tip_oblast);if(stavka_COUNT>=0)spoljni[Datoteka_pokazivač-32]=stavka_COUNT+1;return stavka_COUNT;
}
int32_t 자바전문만들기(int32_t 첫째값,int32_t SECOND_VALUE,int32_t kôd_znaka){return 되돌림전문만들기(첫째값,SECOND_VALUE,kôd_znaka);}
int32_t 자바전문묶기(int32_t Datoteka_pokazivač,int32_t Internet_adresa,int32_t broj_porta){
    if(Internet_adresa==0x7f000001)return 되돌림전문묶기(Datoteka_pokazivač,Internet_adresa,broj_porta);
    if(Internet_adresa!=0&&Internet_adresa!=망상태읽기(0,0))return -99;
    int 반환값=되돌림전문묶기(Datoteka_pokazivač,0,broj_porta);if(반환값<0)return 반환값;
    int stavka_COUNT=nalepiti_SMS(Datoteka_pokazivač,2);if(stavka_COUNT<0)return stavka_COUNT;반환값=NET_povezati(stavka_COUNT,망상태읽기(0,0),되돌림전문접속번호(Datoteka_pokazivač));if(!반환값)ograničen_adresa[Datoteka_pokazivač-32]=Internet_adresa;return 반환값;
}
int32_t 자바전문보내기(int32_t Datoteka_pokazivač,int32_t Internet_adresa,int32_t broj_porta,int32_t promeniti_veličinu){
    if(Internet_adresa==0x7f000001)return 되돌림전문보내기(Datoteka_pokazivač,Internet_adresa,broj_porta,promeniti_veličinu);
    if(promeniti_veličinu<0||promeniti_veličinu>512)return -90;if(broj_porta<1||broj_porta>65535)return -22;
    if(되돌림전문접속번호(Datoteka_pokazivač)<0)return -9;
    if(되돌림전문주소(Datoteka_pokazivač)==0x7f000001)return -101;
    int stavka_COUNT=외부번호(Datoteka_pokazivač);if(stavka_COUNT<0){int 반환값=0;if(되돌림전문접속번호(Datoteka_pokazivač)==0)반환값=되돌림전문묶기(Datoteka_pokazivač,0,0);if(반환값<0)return 반환값;stavka_COUNT=nalepiti_SMS(Datoteka_pokazivač,2);if(stavka_COUNT<0)return stavka_COUNT;반환값=NET_povezati(stavka_COUNT,망상태읽기(0,0),되돌림전문접속번호(Datoteka_pokazivač));if(반환값<0)return 반환값;}
    unsigned char podaci[512];for(int 순번=0;순번<promeniti_veličinu;순번++)podaci[순번]=자바전문얻기(순번);return poslati_datagram(stavka_COUNT,podaci,promeniti_veličinu,Internet_adresa,broj_porta);
}
int32_t 자바전문받기(int32_t Datoteka_pokazivač,int32_t promeniti_veličinu){
    int stavka_COUNT=외부번호(Datoteka_pokazivač);if(stavka_COUNT<0)return 되돌림전문받기(Datoteka_pokazivač,promeniti_veličinu);if(promeniti_veličinu<0||promeniti_veličinu>512)return -22;
    int lokalni=되돌림전문받기(Datoteka_pokazivač,promeniti_veličinu);if(lokalni!=-11){UDP_spoljni_ravnopravni_uređaj[Datoteka_pokazivač-32]=0;return lokalni;}
    unsigned char podaci[512];int 반환값=primiti_datagram(stavka_COUNT,podaci,promeniti_veličinu);if(반환값>=0)UDP_spoljni_ravnopravni_uređaj[Datoteka_pokazivač-32]=1;for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,podaci[순번]);return 반환값;
}
int32_t 자바전문접속번호(int32_t Datoteka_pokazivač){int stavka_COUNT=외부번호(Datoteka_pokazivač);return stavka_COUNT<0?되돌림전문접속번호(Datoteka_pokazivač):(int32_t)Mreža_broj_porta(stavka_COUNT);}
int32_t 자바전문주소(int32_t Datoteka_pokazivač){return 외부번호(Datoteka_pokazivač)<0?되돌림전문주소(Datoteka_pokazivač):ograničen_adresa[Datoteka_pokazivač-32];}
int32_t 자바전문상대(int32_t Datoteka_pokazivač){int stavka_COUNT=외부번호(Datoteka_pokazivač);return stavka_COUNT<0||!UDP_spoljni_ravnopravni_uređaj[Datoteka_pokazivač-32]?되돌림전문상대(Datoteka_pokazivač):(int32_t)ravnopravni_uređaj_broj_porta(stavka_COUNT);}
int32_t 자바전문원격주소(int32_t Datoteka_pokazivač){int stavka_COUNT=외부번호(Datoteka_pokazivač);return stavka_COUNT<0||!UDP_spoljni_ravnopravni_uređaj[Datoteka_pokazivač-32]?0x7f000001:(int32_t)NET_ravnopravni_uređaj_adresa(stavka_COUNT);}
int32_t 자바전문닫기(int32_t Datoteka_pokazivač){int stavka_COUNT=외부번호(Datoteka_pokazivač);if(stavka_COUNT>=0){Zatvori_Mreža(stavka_COUNT);spoljni[Datoteka_pokazivač-32]=0;}if(Datoteka_pokazivač>=32&&Datoteka_pokazivač<40)UDP_spoljni_ravnopravni_uređaj[Datoteka_pokazivač-32]=ograničen_adresa[Datoteka_pokazivač-32]=0;return 되돌림전문닫기(Datoteka_pokazivač);}
int32_t 자바흐름만들기(void){return 되돌림흐름만들기();}
int32_t 자바흐름묶기(int32_t Datoteka_pokazivač,int32_t Internet_adresa,int32_t broj_porta){
    if(Internet_adresa==0||Internet_adresa==0x7f000001){int 반환값=되돌림흐름묶기(Datoteka_pokazivač,Internet_adresa,broj_porta);if(!반환값)임의주소[Datoteka_pokazivač-32]=Internet_adresa==0;return 반환값;}
    if(Internet_adresa!=망상태읽기(0,0))return -99;int 반환값=되돌림흐름묶기(Datoteka_pokazivač,0,broj_porta);if(반환값<0)return 반환값;
    int stavka_COUNT=nalepiti_SMS(Datoteka_pokazivač,1);return stavka_COUNT<0?stavka_COUNT:NET_povezati(stavka_COUNT,Internet_adresa,되돌림흐름접속번호(Datoteka_pokazivač));
}
int32_t 자바흐름듣기(int32_t Datoteka_pokazivač,int32_t 연결대기한도){
    int stavka_COUNT=외부번호(Datoteka_pokazivač);if(stavka_COUNT<0){int 반환값=되돌림흐름듣기(Datoteka_pokazivač,연결대기한도);if(반환값<0||!임의주소[Datoteka_pokazivač-32])return 반환값;
        stavka_COUNT=nalepiti_SMS(Datoteka_pokazivač,1);if(stavka_COUNT<0)return stavka_COUNT;반환값=NET_povezati(stavka_COUNT,망상태읽기(0,0),되돌림흐름접속번호(Datoteka_pokazivač));if(반환값<0)return 반환값;양쪽수신창구[Datoteka_pokazivač-32]=1;
    }return 연결대기한도<1?-22:NET_slušati(stavka_COUNT);
}
int32_t 자바흐름연결(int32_t Datoteka_pokazivač,int32_t Internet_adresa,int32_t broj_porta){
    if(Internet_adresa==0x7f000001 && 외부번호(Datoteka_pokazivač)<0)return 되돌림흐름연결(Datoteka_pokazivač,Internet_adresa,broj_porta);
    if(되돌림흐름접속번호(Datoteka_pokazivač)<0)return -9;int stavka_COUNT=nalepiti_SMS(Datoteka_pokazivač,1);return stavka_COUNT<0?stavka_COUNT:NET_veze(stavka_COUNT,Internet_adresa,broj_porta);
}
int32_t 자바흐름연결받기(int32_t Datoteka_pokazivač){
    int stavka_COUNT=외부번호(Datoteka_pokazivač);if(stavka_COUNT<0)return 되돌림흐름연결받기(Datoteka_pokazivač);
    if(양쪽수신창구[Datoteka_pokazivač-32]){int lokalni=되돌림흐름연결받기(Datoteka_pokazivač);if(lokalni!=-11)return lokalni;}
    int ravnopravni_uređaj_VALUE=NET_prihvatiti(stavka_COUNT);if(ravnopravni_uređaj_VALUE<0)return ravnopravni_uređaj_VALUE;
    int cilj=되돌림흐름만들기();if(cilj<0){Zatvori_Mreža(ravnopravni_uređaj_VALUE);return cilj;}spoljni[cilj-32]=ravnopravni_uređaj_VALUE+1;return cilj;
}
int32_t 자바흐름읽기(int32_t Datoteka_pokazivač,int32_t promeniti_veličinu){
    int stavka_COUNT=외부번호(Datoteka_pokazivač);if(stavka_COUNT<0)return 되돌림흐름읽기(Datoteka_pokazivač,promeniti_veličinu);if(promeniti_veličinu<0||promeniti_veličinu>512)return -22;
    unsigned char podaci[512];int 반환값=통신읽기(stavka_COUNT,podaci,promeniti_veličinu);for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,podaci[순번]);return 반환값;
}
int32_t 자바흐름쓰기(int32_t Datoteka_pokazivač,int32_t promeniti_veličinu){
    int stavka_COUNT=외부번호(Datoteka_pokazivač);if(stavka_COUNT<0)return 되돌림흐름쓰기(Datoteka_pokazivač,promeniti_veličinu);if(promeniti_veličinu<0||promeniti_veličinu>512)return -22;
    unsigned char podaci[512];for(int 순번=0;순번<promeniti_veličinu;순번++)podaci[순번]=자바전문얻기(순번);return 통신쓰기(stavka_COUNT,podaci,promeniti_veličinu);
}
int32_t 자바흐름접속번호(int32_t Datoteka_pokazivač){int stavka_COUNT=외부번호(Datoteka_pokazivač);return stavka_COUNT<0?되돌림흐름접속번호(Datoteka_pokazivač):(int32_t)Mreža_broj_porta(stavka_COUNT);}
int32_t 자바흐름상대(int32_t Datoteka_pokazivač){int stavka_COUNT=외부번호(Datoteka_pokazivač);return stavka_COUNT<0?되돌림흐름상대(Datoteka_pokazivač):(int32_t)ravnopravni_uređaj_broj_porta(stavka_COUNT);}
int32_t 자바흐름주소(int32_t Datoteka_pokazivač){return 외부번호(Datoteka_pokazivač)<0?0x7f000001:양쪽수신창구[Datoteka_pokazivač-32]?0:망상태읽기(0,0);}
int32_t 자바흐름닫기(int32_t Datoteka_pokazivač){int stavka_COUNT=외부번호(Datoteka_pokazivač);if(stavka_COUNT>=0){Zatvori_Mreža(stavka_COUNT);spoljni[Datoteka_pokazivač-32]=0;}if(Datoteka_pokazivač>=40&&Datoteka_pokazivač<56)임의주소[Datoteka_pokazivač-32]=양쪽수신창구[Datoteka_pokazivač-32]=0;return 되돌림흐름닫기(Datoteka_pokazivač);}
