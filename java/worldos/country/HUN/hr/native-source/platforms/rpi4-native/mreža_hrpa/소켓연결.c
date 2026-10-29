#include "../명명/기계연결이름.h"
/* Preserve the deterministic Java loopback endpoints; route external IPv4 to lwIP. */
#include "mreža_hrpa.h"
extern int32_t 되돌림전문만들기(int32_t,int32_t,int32_t), 되돌림전문묶기(int32_t,int32_t,int32_t);
extern int32_t 되돌림전문보내기(int32_t,int32_t,int32_t,int32_t), 되돌림전문받기(int32_t,int32_t);
extern int32_t 되돌림전문접속번호(int32_t), 되돌림전문주소(int32_t), 되돌림전문상대(int32_t), 되돌림전문닫기(int32_t);
extern int32_t 자바전문넣기(int32_t,int32_t),자바전문얻기(int32_t);
extern int32_t 되돌림흐름만들기(void),되돌림흐름묶기(int32_t,int32_t,int32_t),되돌림흐름듣기(int32_t,int32_t);
extern int32_t 되돌림흐름연결(int32_t,int32_t,int32_t),되돌림흐름연결받기(int32_t),되돌림흐름읽기(int32_t,int32_t),되돌림흐름쓰기(int32_t,int32_t);
extern int32_t 되돌림흐름접속번호(int32_t),되돌림흐름상대(int32_t),되돌림흐름닫기(int32_t);
static int vanjski[24];
static int 임의주소[24], 양쪽수신창구[24], UDP_vanjski_ravnopravan_član[8], ograničen_adresa[8];
static int 외부번호(int Datoteka_ustroj) { return Datoteka_ustroj>=32 && Datoteka_ustroj<56 ? vanjski[Datoteka_ustroj-32]-1 : -1; }
static int zalijepiti_SMS(int Datoteka_ustroj,int TYPE_područje) {
    if(Datoteka_ustroj<32||Datoteka_ustroj>=56)return -9;int 이전=외부번호(Datoteka_ustroj);if(이전>=0)return 이전;
    int artikl_COUNT=통신끝점만들기(TYPE_područje);if(artikl_COUNT>=0)vanjski[Datoteka_ustroj-32]=artikl_COUNT+1;return artikl_COUNT;
}
int32_t 자바전문만들기(int32_t 첫째값,int32_t SECOND_VALUE,int32_t kodna_točka){return 되돌림전문만들기(첫째값,SECOND_VALUE,kodna_točka);}
int32_t 자바전문묶기(int32_t Datoteka_ustroj,int32_t internetska_adresa,int32_t broj_priključka){
    if(internetska_adresa==0x7f000001)return 되돌림전문묶기(Datoteka_ustroj,internetska_adresa,broj_priključka);
    if(internetska_adresa!=0&&internetska_adresa!=망상태읽기(0,0))return -99;
    int 반환값=되돌림전문묶기(Datoteka_ustroj,0,broj_priključka);if(반환값<0)return 반환값;
    int artikl_COUNT=zalijepiti_SMS(Datoteka_ustroj,2);if(artikl_COUNT<0)return artikl_COUNT;반환값=NET_BIND(artikl_COUNT,망상태읽기(0,0),되돌림전문접속번호(Datoteka_ustroj));if(!반환값)ograničen_adresa[Datoteka_ustroj-32]=internetska_adresa;return 반환값;
}
int32_t 자바전문보내기(int32_t Datoteka_ustroj,int32_t internetska_adresa,int32_t broj_priključka,int32_t Veličina){
    if(internetska_adresa==0x7f000001)return 되돌림전문보내기(Datoteka_ustroj,internetska_adresa,broj_priključka,Veličina);
    if(Veličina<0||Veličina>512)return -90;if(broj_priključka<1||broj_priključka>65535)return -22;
    if(되돌림전문접속번호(Datoteka_ustroj)<0)return -9;
    if(되돌림전문주소(Datoteka_ustroj)==0x7f000001)return -101;
    int artikl_COUNT=외부번호(Datoteka_ustroj);if(artikl_COUNT<0){int 반환값=0;if(되돌림전문접속번호(Datoteka_ustroj)==0)반환값=되돌림전문묶기(Datoteka_ustroj,0,0);if(반환값<0)return 반환값;artikl_COUNT=zalijepiti_SMS(Datoteka_ustroj,2);if(artikl_COUNT<0)return artikl_COUNT;반환값=NET_BIND(artikl_COUNT,망상태읽기(0,0),되돌림전문접속번호(Datoteka_ustroj));if(반환값<0)return 반환값;}
    unsigned char podaci[512];for(int 순번=0;순번<Veličina;순번++)podaci[순번]=자바전문얻기(순번);return slati_datogram(artikl_COUNT,podaci,Veličina,internetska_adresa,broj_priključka);
}
int32_t 자바전문받기(int32_t Datoteka_ustroj,int32_t Veličina){
    int artikl_COUNT=외부번호(Datoteka_ustroj);if(artikl_COUNT<0)return 되돌림전문받기(Datoteka_ustroj,Veličina);if(Veličina<0||Veličina>512)return -22;
    int lokalno=되돌림전문받기(Datoteka_ustroj,Veličina);if(lokalno!=-11){UDP_vanjski_ravnopravan_član[Datoteka_ustroj-32]=0;return lokalno;}
    unsigned char podaci[512];int 반환값=primiti_datogram(artikl_COUNT,podaci,Veličina);if(반환값>=0)UDP_vanjski_ravnopravan_član[Datoteka_ustroj-32]=1;for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,podaci[순번]);return 반환값;
}
int32_t 자바전문접속번호(int32_t Datoteka_ustroj){int artikl_COUNT=외부번호(Datoteka_ustroj);return artikl_COUNT<0?되돌림전문접속번호(Datoteka_ustroj):(int32_t)mreža_broj_priključka(artikl_COUNT);}
int32_t 자바전문주소(int32_t Datoteka_ustroj){return 외부번호(Datoteka_ustroj)<0?되돌림전문주소(Datoteka_ustroj):ograničen_adresa[Datoteka_ustroj-32];}
int32_t 자바전문상대(int32_t Datoteka_ustroj){int artikl_COUNT=외부번호(Datoteka_ustroj);return artikl_COUNT<0||!UDP_vanjski_ravnopravan_član[Datoteka_ustroj-32]?되돌림전문상대(Datoteka_ustroj):(int32_t)ravnopravan_član_broj_priključka(artikl_COUNT);}
int32_t 자바전문원격주소(int32_t Datoteka_ustroj){int artikl_COUNT=외부번호(Datoteka_ustroj);return artikl_COUNT<0||!UDP_vanjski_ravnopravan_član[Datoteka_ustroj-32]?0x7f000001:(int32_t)NET_ravnopravan_član_adresa(artikl_COUNT);}
int32_t 자바전문닫기(int32_t Datoteka_ustroj){int artikl_COUNT=외부번호(Datoteka_ustroj);if(artikl_COUNT>=0){Zatvori_mreža(artikl_COUNT);vanjski[Datoteka_ustroj-32]=0;}if(Datoteka_ustroj>=32&&Datoteka_ustroj<40)UDP_vanjski_ravnopravan_član[Datoteka_ustroj-32]=ograničen_adresa[Datoteka_ustroj-32]=0;return 되돌림전문닫기(Datoteka_ustroj);}
int32_t 자바흐름만들기(void){return 되돌림흐름만들기();}
int32_t 자바흐름묶기(int32_t Datoteka_ustroj,int32_t internetska_adresa,int32_t broj_priključka){
    if(internetska_adresa==0||internetska_adresa==0x7f000001){int 반환값=되돌림흐름묶기(Datoteka_ustroj,internetska_adresa,broj_priključka);if(!반환값)임의주소[Datoteka_ustroj-32]=internetska_adresa==0;return 반환값;}
    if(internetska_adresa!=망상태읽기(0,0))return -99;int 반환값=되돌림흐름묶기(Datoteka_ustroj,0,broj_priključka);if(반환값<0)return 반환값;
    int artikl_COUNT=zalijepiti_SMS(Datoteka_ustroj,1);return artikl_COUNT<0?artikl_COUNT:NET_BIND(artikl_COUNT,internetska_adresa,되돌림흐름접속번호(Datoteka_ustroj));
}
int32_t 자바흐름듣기(int32_t Datoteka_ustroj,int32_t 연결대기한도){
    int artikl_COUNT=외부번호(Datoteka_ustroj);if(artikl_COUNT<0){int 반환값=되돌림흐름듣기(Datoteka_ustroj,연결대기한도);if(반환값<0||!임의주소[Datoteka_ustroj-32])return 반환값;
        artikl_COUNT=zalijepiti_SMS(Datoteka_ustroj,1);if(artikl_COUNT<0)return artikl_COUNT;반환값=NET_BIND(artikl_COUNT,망상태읽기(0,0),되돌림흐름접속번호(Datoteka_ustroj));if(반환값<0)return 반환값;양쪽수신창구[Datoteka_ustroj-32]=1;
    }return 연결대기한도<1?-22:NET_osluškivati(artikl_COUNT);
}
int32_t 자바흐름연결(int32_t Datoteka_ustroj,int32_t internetska_adresa,int32_t broj_priključka){
    if(internetska_adresa==0x7f000001 && 외부번호(Datoteka_ustroj)<0)return 되돌림흐름연결(Datoteka_ustroj,internetska_adresa,broj_priključka);
    if(되돌림흐름접속번호(Datoteka_ustroj)<0)return -9;int artikl_COUNT=zalijepiti_SMS(Datoteka_ustroj,1);return artikl_COUNT<0?artikl_COUNT:NET_CONNECT(artikl_COUNT,internetska_adresa,broj_priključka);
}
int32_t 자바흐름연결받기(int32_t Datoteka_ustroj){
    int artikl_COUNT=외부번호(Datoteka_ustroj);if(artikl_COUNT<0)return 되돌림흐름연결받기(Datoteka_ustroj);
    if(양쪽수신창구[Datoteka_ustroj-32]){int lokalno=되돌림흐름연결받기(Datoteka_ustroj);if(lokalno!=-11)return lokalno;}
    int ravnopravan_član_VALUE=NET_prihvatiti(artikl_COUNT);if(ravnopravan_član_VALUE<0)return ravnopravan_član_VALUE;
    int cilj=되돌림흐름만들기();if(cilj<0){Zatvori_mreža(ravnopravan_član_VALUE);return cilj;}vanjski[cilj-32]=ravnopravan_član_VALUE+1;return cilj;
}
int32_t 자바흐름읽기(int32_t Datoteka_ustroj,int32_t Veličina){
    int artikl_COUNT=외부번호(Datoteka_ustroj);if(artikl_COUNT<0)return 되돌림흐름읽기(Datoteka_ustroj,Veličina);if(Veličina<0||Veličina>512)return -22;
    unsigned char podaci[512];int 반환값=통신읽기(artikl_COUNT,podaci,Veličina);for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,podaci[순번]);return 반환값;
}
int32_t 자바흐름쓰기(int32_t Datoteka_ustroj,int32_t Veličina){
    int artikl_COUNT=외부번호(Datoteka_ustroj);if(artikl_COUNT<0)return 되돌림흐름쓰기(Datoteka_ustroj,Veličina);if(Veličina<0||Veličina>512)return -22;
    unsigned char podaci[512];for(int 순번=0;순번<Veličina;순번++)podaci[순번]=자바전문얻기(순번);return NET_zapisivanje(artikl_COUNT,podaci,Veličina);
}
int32_t 자바흐름접속번호(int32_t Datoteka_ustroj){int artikl_COUNT=외부번호(Datoteka_ustroj);return artikl_COUNT<0?되돌림흐름접속번호(Datoteka_ustroj):(int32_t)mreža_broj_priključka(artikl_COUNT);}
int32_t 자바흐름상대(int32_t Datoteka_ustroj){int artikl_COUNT=외부번호(Datoteka_ustroj);return artikl_COUNT<0?되돌림흐름상대(Datoteka_ustroj):(int32_t)ravnopravan_član_broj_priključka(artikl_COUNT);}
int32_t 자바흐름주소(int32_t Datoteka_ustroj){return 외부번호(Datoteka_ustroj)<0?0x7f000001:양쪽수신창구[Datoteka_ustroj-32]?0:망상태읽기(0,0);}
int32_t 자바흐름닫기(int32_t Datoteka_ustroj){int artikl_COUNT=외부번호(Datoteka_ustroj);if(artikl_COUNT>=0){Zatvori_mreža(artikl_COUNT);vanjski[Datoteka_ustroj-32]=0;}if(Datoteka_ustroj>=40&&Datoteka_ustroj<56)임의주소[Datoteka_ustroj-32]=양쪽수신창구[Datoteka_ustroj-32]=0;return 되돌림흐름닫기(Datoteka_ustroj);}
