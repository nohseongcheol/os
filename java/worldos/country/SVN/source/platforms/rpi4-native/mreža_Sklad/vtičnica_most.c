#include "../명명/기계연결이름.h"
/* Preserve the deterministic Java loopback endpoints; route external IPv4 to lwIP. */
#include "mreža_Sklad.h"
extern int32_t 되돌림전문만들기(int32_t,int32_t,int32_t), 되돌림전문묶기(int32_t,int32_t,int32_t);
extern int32_t 되돌림전문보내기(int32_t,int32_t,int32_t,int32_t), 되돌림전문받기(int32_t,int32_t);
extern int32_t 되돌림전문접속번호(int32_t), 되돌림전문주소(int32_t), 되돌림전문상대(int32_t), 되돌림전문닫기(int32_t);
extern int32_t 자바전문넣기(int32_t,int32_t),자바전문얻기(int32_t);
extern int32_t 되돌림흐름만들기(void),되돌림흐름묶기(int32_t,int32_t,int32_t),되돌림흐름듣기(int32_t,int32_t);
extern int32_t 되돌림흐름연결(int32_t,int32_t,int32_t),되돌림흐름연결받기(int32_t),되돌림흐름읽기(int32_t,int32_t),되돌림흐름쓰기(int32_t,int32_t);
extern int32_t 되돌림흐름접속번호(int32_t),되돌림흐름상대(int32_t),되돌림흐름닫기(int32_t);
static int zunanji[24];
static int 임의주소[24], 양쪽수신창구[24], UDP_zunanji_enakovreden[8], meja_naslov[8];
static int 외부번호(int Datoteka_ročica) { return Datoteka_ročica>=32 && Datoteka_ročica<56 ? zunanji[Datoteka_ročica-32]-1 : -1; }
static int prilepiti_SMS(int Datoteka_ročica,int Tip_območje) {
    if(Datoteka_ročica<32||Datoteka_ročica>=56)return -9;int 이전=외부번호(Datoteka_ročica);if(이전>=0)return 이전;
    int element_COUNT=Ustvari_vtičnica_končna_točka(Tip_območje);if(element_COUNT>=0)zunanji[Datoteka_ročica-32]=element_COUNT+1;return element_COUNT;
}
int32_t 자바전문만들기(int32_t 첫째값,int32_t SECOND_VALUE,int32_t koda_znaka){return 되돌림전문만들기(첫째값,SECOND_VALUE,koda_znaka);}
int32_t 자바전문묶기(int32_t Datoteka_ročica,int32_t internetni_račun,int32_t številka_vrat){
    if(internetni_račun==0x7f000001)return 되돌림전문묶기(Datoteka_ročica,internetni_račun,številka_vrat);
    if(internetni_račun!=0&&internetni_račun!=망상태읽기(0,0))return -99;
    int 반환값=되돌림전문묶기(Datoteka_ročica,0,številka_vrat);if(반환값<0)return 반환값;
    int element_COUNT=prilepiti_SMS(Datoteka_ročica,2);if(element_COUNT<0)return element_COUNT;반환값=NET_BIND(element_COUNT,망상태읽기(0,0),되돌림전문접속번호(Datoteka_ročica));if(!반환값)meja_naslov[Datoteka_ročica-32]=internetni_račun;return 반환값;
}
int32_t 자바전문보내기(int32_t Datoteka_ročica,int32_t internetni_račun,int32_t številka_vrat,int32_t Velikost){
    if(internetni_račun==0x7f000001)return 되돌림전문보내기(Datoteka_ročica,internetni_račun,številka_vrat,Velikost);
    if(Velikost<0||Velikost>512)return -90;if(številka_vrat<1||številka_vrat>65535)return -22;
    if(되돌림전문접속번호(Datoteka_ročica)<0)return -9;
    if(되돌림전문주소(Datoteka_ročica)==0x7f000001)return -101;
    int element_COUNT=외부번호(Datoteka_ročica);if(element_COUNT<0){int 반환값=0;if(되돌림전문접속번호(Datoteka_ročica)==0)반환값=되돌림전문묶기(Datoteka_ročica,0,0);if(반환값<0)return 반환값;element_COUNT=prilepiti_SMS(Datoteka_ročica,2);if(element_COUNT<0)return element_COUNT;반환값=NET_BIND(element_COUNT,망상태읽기(0,0),되돌림전문접속번호(Datoteka_ročica));if(반환값<0)return 반환값;}
    unsigned char podatki[512];for(int 순번=0;순번<Velikost;순번++)podatki[순번]=자바전문얻기(순번);return poslati_datagram(element_COUNT,podatki,Velikost,internetni_račun,številka_vrat);
}
int32_t 자바전문받기(int32_t Datoteka_ročica,int32_t Velikost){
    int element_COUNT=외부번호(Datoteka_ročica);if(element_COUNT<0)return 되돌림전문받기(Datoteka_ročica,Velikost);if(Velikost<0||Velikost>512)return -22;
    int lokalen_krajeven=되돌림전문받기(Datoteka_ročica,Velikost);if(lokalen_krajeven!=-11){UDP_zunanji_enakovreden[Datoteka_ročica-32]=0;return lokalen_krajeven;}
    unsigned char podatki[512];int 반환값=sprejeti_sprejemati_prejeti_prejemati_datagram(element_COUNT,podatki,Velikost);if(반환값>=0)UDP_zunanji_enakovreden[Datoteka_ročica-32]=1;for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,podatki[순번]);return 반환값;
}
int32_t 자바전문접속번호(int32_t Datoteka_ročica){int element_COUNT=외부번호(Datoteka_ročica);return element_COUNT<0?되돌림전문접속번호(Datoteka_ročica):(int32_t)mreža_številka_vrat(element_COUNT);}
int32_t 자바전문주소(int32_t Datoteka_ročica){return 외부번호(Datoteka_ročica)<0?되돌림전문주소(Datoteka_ročica):meja_naslov[Datoteka_ročica-32];}
int32_t 자바전문상대(int32_t Datoteka_ročica){int element_COUNT=외부번호(Datoteka_ročica);return element_COUNT<0||!UDP_zunanji_enakovreden[Datoteka_ročica-32]?되돌림전문상대(Datoteka_ročica):(int32_t)enakovreden_številka_vrat(element_COUNT);}
int32_t 자바전문원격주소(int32_t Datoteka_ročica){int element_COUNT=외부번호(Datoteka_ročica);return element_COUNT<0||!UDP_zunanji_enakovreden[Datoteka_ročica-32]?0x7f000001:(int32_t)NET_enakovreden_naslov(element_COUNT);}
int32_t 자바전문닫기(int32_t Datoteka_ročica){int element_COUNT=외부번호(Datoteka_ročica);if(element_COUNT>=0){Zapri_mreža(element_COUNT);zunanji[Datoteka_ročica-32]=0;}if(Datoteka_ročica>=32&&Datoteka_ročica<40)UDP_zunanji_enakovreden[Datoteka_ročica-32]=meja_naslov[Datoteka_ročica-32]=0;return 되돌림전문닫기(Datoteka_ročica);}
int32_t 자바흐름만들기(void){return 되돌림흐름만들기();}
int32_t 자바흐름묶기(int32_t Datoteka_ročica,int32_t internetni_račun,int32_t številka_vrat){
    if(internetni_račun==0||internetni_račun==0x7f000001){int 반환값=되돌림흐름묶기(Datoteka_ročica,internetni_račun,številka_vrat);if(!반환값)임의주소[Datoteka_ročica-32]=internetni_račun==0;return 반환값;}
    if(internetni_račun!=망상태읽기(0,0))return -99;int 반환값=되돌림흐름묶기(Datoteka_ročica,0,številka_vrat);if(반환값<0)return 반환값;
    int element_COUNT=prilepiti_SMS(Datoteka_ročica,1);return element_COUNT<0?element_COUNT:NET_BIND(element_COUNT,internetni_račun,되돌림흐름접속번호(Datoteka_ročica));
}
int32_t 자바흐름듣기(int32_t Datoteka_ročica,int32_t 연결대기한도){
    int element_COUNT=외부번호(Datoteka_ročica);if(element_COUNT<0){int 반환값=되돌림흐름듣기(Datoteka_ročica,연결대기한도);if(반환값<0||!임의주소[Datoteka_ročica-32])return 반환값;
        element_COUNT=prilepiti_SMS(Datoteka_ročica,1);if(element_COUNT<0)return element_COUNT;반환값=NET_BIND(element_COUNT,망상태읽기(0,0),되돌림흐름접속번호(Datoteka_ročica));if(반환값<0)return 반환값;양쪽수신창구[Datoteka_ročica-32]=1;
    }return 연결대기한도<1?-22:NET_poslušati(element_COUNT);
}
int32_t 자바흐름연결(int32_t Datoteka_ročica,int32_t internetni_račun,int32_t številka_vrat){
    if(internetni_račun==0x7f000001 && 외부번호(Datoteka_ročica)<0)return 되돌림흐름연결(Datoteka_ročica,internetni_račun,številka_vrat);
    if(되돌림흐름접속번호(Datoteka_ročica)<0)return -9;int element_COUNT=prilepiti_SMS(Datoteka_ročica,1);return element_COUNT<0?element_COUNT:NET_POVEŽI(element_COUNT,internetni_račun,številka_vrat);
}
int32_t 자바흐름연결받기(int32_t Datoteka_ročica){
    int element_COUNT=외부번호(Datoteka_ročica);if(element_COUNT<0)return 되돌림흐름연결받기(Datoteka_ročica);
    if(양쪽수신창구[Datoteka_ročica-32]){int lokalen_krajeven=되돌림흐름연결받기(Datoteka_ročica);if(lokalen_krajeven!=-11)return lokalen_krajeven;}
    int enakovreden_VALUE=NET_sprejeti(element_COUNT);if(enakovreden_VALUE<0)return enakovreden_VALUE;
    int tarča=되돌림흐름만들기();if(tarča<0){Zapri_mreža(enakovreden_VALUE);return tarča;}zunanji[tarča-32]=enakovreden_VALUE+1;return tarča;
}
int32_t 자바흐름읽기(int32_t Datoteka_ročica,int32_t Velikost){
    int element_COUNT=외부번호(Datoteka_ročica);if(element_COUNT<0)return 되돌림흐름읽기(Datoteka_ročica,Velikost);if(Velikost<0||Velikost>512)return -22;
    unsigned char podatki[512];int 반환값=통신읽기(element_COUNT,podatki,Velikost);for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,podatki[순번]);return 반환값;
}
int32_t 자바흐름쓰기(int32_t Datoteka_ročica,int32_t Velikost){
    int element_COUNT=외부번호(Datoteka_ročica);if(element_COUNT<0)return 되돌림흐름쓰기(Datoteka_ročica,Velikost);if(Velikost<0||Velikost>512)return -22;
    unsigned char podatki[512];for(int 순번=0;순번<Velikost;순번++)podatki[순번]=자바전문얻기(순번);return NET_pisati(element_COUNT,podatki,Velikost);
}
int32_t 자바흐름접속번호(int32_t Datoteka_ročica){int element_COUNT=외부번호(Datoteka_ročica);return element_COUNT<0?되돌림흐름접속번호(Datoteka_ročica):(int32_t)mreža_številka_vrat(element_COUNT);}
int32_t 자바흐름상대(int32_t Datoteka_ročica){int element_COUNT=외부번호(Datoteka_ročica);return element_COUNT<0?되돌림흐름상대(Datoteka_ročica):(int32_t)enakovreden_številka_vrat(element_COUNT);}
int32_t 자바흐름주소(int32_t Datoteka_ročica){return 외부번호(Datoteka_ročica)<0?0x7f000001:양쪽수신창구[Datoteka_ročica-32]?0:망상태읽기(0,0);}
int32_t 자바흐름닫기(int32_t Datoteka_ročica){int element_COUNT=외부번호(Datoteka_ročica);if(element_COUNT>=0){Zapri_mreža(element_COUNT);zunanji[Datoteka_ročica-32]=0;}if(Datoteka_ročica>=40&&Datoteka_ročica<56)임의주소[Datoteka_ročica-32]=양쪽수신창구[Datoteka_ročica-32]=0;return 되돌림흐름닫기(Datoteka_ročica);}
