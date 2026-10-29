#include "../명명/기계연결이름.h"
/* Preserve the deterministic Java loopback endpoints; route external IPv4 to lwIP. */
#include "hálózat_Sor.h"
extern int32_t 되돌림전문만들기(int32_t,int32_t,int32_t), 되돌림전문묶기(int32_t,int32_t,int32_t);
extern int32_t 되돌림전문보내기(int32_t,int32_t,int32_t,int32_t), 되돌림전문받기(int32_t,int32_t);
extern int32_t 되돌림전문접속번호(int32_t), 되돌림전문주소(int32_t), 되돌림전문상대(int32_t), 되돌림전문닫기(int32_t);
extern int32_t 자바전문넣기(int32_t,int32_t),자바전문얻기(int32_t);
extern int32_t 되돌림흐름만들기(void),되돌림흐름묶기(int32_t,int32_t,int32_t),되돌림흐름듣기(int32_t,int32_t);
extern int32_t 되돌림흐름연결(int32_t,int32_t,int32_t),되돌림흐름연결받기(int32_t),되돌림흐름읽기(int32_t,int32_t),되돌림흐름쓰기(int32_t,int32_t);
extern int32_t 되돌림흐름접속번호(int32_t),되돌림흐름상대(int32_t),되돌림흐름닫기(int32_t);
static int külső[24];
static int 임의주소[24], 양쪽수신창구[24], UDP_külső_társ[8], határ_CÍM[8];
static int külső_szám(int fájlleíró) { return fájlleíró>=32 && fájlleíró<56 ? külső[fájlleíró-32]-1 : -1; }
static int beilleszt_SMS(int fájlleíró,int beír_terület) {
    if(fájlleíró<32||fájlleíró>=56)return -9;int Előző_cikk=külső_szám(fájlleíró);if(Előző_cikk>=0)return Előző_cikk;
    int cikk_DARAB=készít_szoftvercsatorna_végpont(beír_terület);if(cikk_DARAB>=0)külső[fájlleíró-32]=cikk_DARAB+1;return cikk_DARAB;
}
int32_t 자바전문만들기(int32_t 첫째값,int32_t MPERC_ÉRTÉK,int32_t kódpont){return 되돌림전문만들기(첫째값,MPERC_ÉRTÉK,kódpont);}
int32_t 자바전문묶기(int32_t fájlleíró,int32_t internetcím,int32_t portszám){
    if(internetcím==0x7f000001)return 되돌림전문묶기(fájlleíró,internetcím,portszám);
    if(internetcím!=0&&internetcím!=망상태읽기(0,0))return -99;
    int 반환값=되돌림전문묶기(fájlleíró,0,portszám);if(반환값<0)return 반환값;
    int cikk_DARAB=beilleszt_SMS(fájlleíró,2);if(cikk_DARAB<0)return cikk_DARAB;반환값=NET_BIND(cikk_DARAB,망상태읽기(0,0),되돌림전문접속번호(fájlleíró));if(!반환값)határ_CÍM[fájlleíró-32]=internetcím;return 반환값;
}
int32_t 자바전문보내기(int32_t fájlleíró,int32_t internetcím,int32_t portszám,int32_t Méret){
    if(internetcím==0x7f000001)return 되돌림전문보내기(fájlleíró,internetcím,portszám,Méret);
    if(Méret<0||Méret>512)return -90;if(portszám<1||portszám>65535)return -22;
    if(되돌림전문접속번호(fájlleíró)<0)return -9;
    if(되돌림전문주소(fájlleíró)==0x7f000001)return -101;
    int cikk_DARAB=külső_szám(fájlleíró);if(cikk_DARAB<0){int 반환값=0;if(되돌림전문접속번호(fájlleíró)==0)반환값=되돌림전문묶기(fájlleíró,0,0);if(반환값<0)return 반환값;cikk_DARAB=beilleszt_SMS(fájlleíró,2);if(cikk_DARAB<0)return cikk_DARAB;반환값=NET_BIND(cikk_DARAB,망상태읽기(0,0),되돌림전문접속번호(fájlleíró));if(반환값<0)return 반환값;}
    unsigned char adat[512];for(int 순번=0;순번<Méret;순번++)adat[순번]=자바전문얻기(순번);return küld_datagram(cikk_DARAB,adat,Méret,internetcím,portszám);
}
int32_t 자바전문받기(int32_t fájlleíró,int32_t Méret){
    int cikk_DARAB=külső_szám(fájlleíró);if(cikk_DARAB<0)return 되돌림전문받기(fájlleíró,Méret);if(Méret<0||Méret>512)return -22;
    int helyi=되돌림전문받기(fájlleíró,Méret);if(helyi!=-11){UDP_külső_társ[fájlleíró-32]=0;return helyi;}
    unsigned char adat[512];int 반환값=fogad_datagram(cikk_DARAB,adat,Méret);if(반환값>=0)UDP_külső_társ[fájlleíró-32]=1;for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,adat[순번]);return 반환값;
}
int32_t 자바전문접속번호(int32_t fájlleíró){int cikk_DARAB=külső_szám(fájlleíró);return cikk_DARAB<0?되돌림전문접속번호(fájlleíró):(int32_t)hálózat_portszám(cikk_DARAB);}
int32_t 자바전문주소(int32_t fájlleíró){return külső_szám(fájlleíró)<0?되돌림전문주소(fájlleíró):határ_CÍM[fájlleíró-32];}
int32_t 자바전문상대(int32_t fájlleíró){int cikk_DARAB=külső_szám(fájlleíró);return cikk_DARAB<0||!UDP_külső_társ[fájlleíró-32]?되돌림전문상대(fájlleíró):(int32_t)társ_portszám(cikk_DARAB);}
int32_t 자바전문원격주소(int32_t fájlleíró){int cikk_DARAB=külső_szám(fájlleíró);return cikk_DARAB<0||!UDP_külső_társ[fájlleíró-32]?0x7f000001:(int32_t)NET_társ_CÍM(cikk_DARAB);}
int32_t 자바전문닫기(int32_t fájlleíró){int cikk_DARAB=külső_szám(fájlleíró);if(cikk_DARAB>=0){bezár_hálózat(cikk_DARAB);külső[fájlleíró-32]=0;}if(fájlleíró>=32&&fájlleíró<40)UDP_külső_társ[fájlleíró-32]=határ_CÍM[fájlleíró-32]=0;return 되돌림전문닫기(fájlleíró);}
int32_t 자바흐름만들기(void){return 되돌림흐름만들기();}
int32_t 자바흐름묶기(int32_t fájlleíró,int32_t internetcím,int32_t portszám){
    if(internetcím==0||internetcím==0x7f000001){int 반환값=되돌림흐름묶기(fájlleíró,internetcím,portszám);if(!반환값)임의주소[fájlleíró-32]=internetcím==0;return 반환값;}
    if(internetcím!=망상태읽기(0,0))return -99;int 반환값=되돌림흐름묶기(fájlleíró,0,portszám);if(반환값<0)return 반환값;
    int cikk_DARAB=beilleszt_SMS(fájlleíró,1);return cikk_DARAB<0?cikk_DARAB:NET_BIND(cikk_DARAB,internetcím,되돌림흐름접속번호(fájlleíró));
}
int32_t 자바흐름듣기(int32_t fájlleíró,int32_t hátralék){
    int cikk_DARAB=külső_szám(fájlleíró);if(cikk_DARAB<0){int 반환값=되돌림흐름듣기(fájlleíró,hátralék);if(반환값<0||!임의주소[fájlleíró-32])return 반환값;
        cikk_DARAB=beilleszt_SMS(fájlleíró,1);if(cikk_DARAB<0)return cikk_DARAB;반환값=NET_BIND(cikk_DARAB,망상태읽기(0,0),되돌림흐름접속번호(fájlleíró));if(반환값<0)return 반환값;양쪽수신창구[fájlleíró-32]=1;
    }return hátralék<1?-22:NET_figyelés(cikk_DARAB);
}
int32_t 자바흐름연결(int32_t fájlleíró,int32_t internetcím,int32_t portszám){
    if(internetcím==0x7f000001 && külső_szám(fájlleíró)<0)return 되돌림흐름연결(fájlleíró,internetcím,portszám);
    if(되돌림흐름접속번호(fájlleíró)<0)return -9;int cikk_DARAB=beilleszt_SMS(fájlleíró,1);return cikk_DARAB<0?cikk_DARAB:NET_KAPCSOLAT(cikk_DARAB,internetcím,portszám);
}
int32_t 자바흐름연결받기(int32_t fájlleíró){
    int cikk_DARAB=külső_szám(fájlleíró);if(cikk_DARAB<0)return 되돌림흐름연결받기(fájlleíró);
    if(양쪽수신창구[fájlleíró-32]){int helyi=되돌림흐름연결받기(fájlleíró);if(helyi!=-11)return helyi;}
    int társ_ÉRTÉK=NET_elfogad(cikk_DARAB);if(társ_ÉRTÉK<0)return társ_ÉRTÉK;
    int cél=되돌림흐름만들기();if(cél<0){bezár_hálózat(társ_ÉRTÉK);return cél;}külső[cél-32]=társ_ÉRTÉK+1;return cél;
}
int32_t 자바흐름읽기(int32_t fájlleíró,int32_t Méret){
    int cikk_DARAB=külső_szám(fájlleíró);if(cikk_DARAB<0)return 되돌림흐름읽기(fájlleíró,Méret);if(Méret<0||Méret>512)return -22;
    unsigned char adat[512];int 반환값=통신읽기(cikk_DARAB,adat,Méret);for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,adat[순번]);return 반환값;
}
int32_t 자바흐름쓰기(int32_t fájlleíró,int32_t Méret){
    int cikk_DARAB=külső_szám(fájlleíró);if(cikk_DARAB<0)return 되돌림흐름쓰기(fájlleíró,Méret);if(Méret<0||Méret>512)return -22;
    unsigned char adat[512];for(int 순번=0;순번<Méret;순번++)adat[순번]=자바전문얻기(순번);return NET_ír(cikk_DARAB,adat,Méret);
}
int32_t 자바흐름접속번호(int32_t fájlleíró){int cikk_DARAB=külső_szám(fájlleíró);return cikk_DARAB<0?되돌림흐름접속번호(fájlleíró):(int32_t)hálózat_portszám(cikk_DARAB);}
int32_t 자바흐름상대(int32_t fájlleíró){int cikk_DARAB=külső_szám(fájlleíró);return cikk_DARAB<0?되돌림흐름상대(fájlleíró):(int32_t)társ_portszám(cikk_DARAB);}
int32_t 자바흐름주소(int32_t fájlleíró){return külső_szám(fájlleíró)<0?0x7f000001:양쪽수신창구[fájlleíró-32]?0:망상태읽기(0,0);}
int32_t 자바흐름닫기(int32_t fájlleíró){int cikk_DARAB=külső_szám(fájlleíró);if(cikk_DARAB>=0){bezár_hálózat(cikk_DARAB);külső[fájlleíró-32]=0;}if(fájlleíró>=40&&fájlleíró<56)임의주소[fájlleíró-32]=양쪽수신창구[fájlleíró-32]=0;return 되돌림흐름닫기(fájlleíró);}
