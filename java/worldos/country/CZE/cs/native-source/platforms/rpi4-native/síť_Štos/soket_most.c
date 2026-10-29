#include "../명명/기계연결이름.h"
/* Preserve the deterministic Java loopback endpoints; route external IPv4 to lwIP. */
#include "síť_Štos.h"
extern int32_t 되돌림전문만들기(int32_t,int32_t,int32_t), 되돌림전문묶기(int32_t,int32_t,int32_t);
extern int32_t 되돌림전문보내기(int32_t,int32_t,int32_t,int32_t), 되돌림전문받기(int32_t,int32_t);
extern int32_t 되돌림전문접속번호(int32_t), 되돌림전문주소(int32_t), 되돌림전문상대(int32_t), 되돌림전문닫기(int32_t);
extern int32_t 자바전문넣기(int32_t,int32_t),자바전문얻기(int32_t);
extern int32_t 되돌림흐름만들기(void),되돌림흐름묶기(int32_t,int32_t,int32_t),되돌림흐름듣기(int32_t,int32_t);
extern int32_t 되돌림흐름연결(int32_t,int32_t,int32_t),되돌림흐름연결받기(int32_t),되돌림흐름읽기(int32_t,int32_t),되돌림흐름쓰기(int32_t,int32_t);
extern int32_t 되돌림흐름접속번호(int32_t),되돌림흐름상대(int32_t),되돌림흐름닫기(int32_t);
static int externí[24];
static int 임의주소[24], 양쪽수신창구[24], protokol_UDP_externí_partner[8], mez_ODKAZ[8];
static int externí_číslo(int popisovač_souboru) { return popisovač_souboru>=32 && popisovač_souboru<56 ? externí[popisovač_souboru-32]-1 : -1; }
static int vložit_SMS(int popisovač_souboru,int TYP_oblast) {
    if(popisovač_souboru<32||popisovač_souboru>=56)return -9;int Předchozí_zboží=externí_číslo(popisovač_souboru);if(Předchozí_zboží>=0)return Předchozí_zboží;
    int zboží_POČET=Create_soket_účastník(TYP_oblast);if(zboží_POČET>=0)externí[popisovač_souboru-32]=zboží_POČET+1;return zboží_POČET;
}
int32_t 자바전문만들기(int32_t 첫째값,int32_t SEKUNDA_HODNOTA,int32_t bod_kódu){return 되돌림전문만들기(첫째값,SEKUNDA_HODNOTA,bod_kódu);}
int32_t 자바전문묶기(int32_t popisovač_souboru,int32_t internetová_adresa,int32_t číslo_portu){
    if(internetová_adresa==0x7f000001)return 되돌림전문묶기(popisovač_souboru,internetová_adresa,číslo_portu);
    if(internetová_adresa!=0&&internetová_adresa!=망상태읽기(0,0))return -99;
    int 반환값=되돌림전문묶기(popisovač_souboru,0,číslo_portu);if(반환값<0)return 반환값;
    int zboží_POČET=vložit_SMS(popisovač_souboru,2);if(zboží_POČET<0)return zboží_POČET;반환값=čistý_vázat(zboží_POČET,망상태읽기(0,0),되돌림전문접속번호(popisovač_souboru));if(!반환값)mez_ODKAZ[popisovač_souboru-32]=internetová_adresa;return 반환값;
}
int32_t 자바전문보내기(int32_t popisovač_souboru,int32_t internetová_adresa,int32_t číslo_portu,int32_t Velikost){
    if(internetová_adresa==0x7f000001)return 되돌림전문보내기(popisovač_souboru,internetová_adresa,číslo_portu,Velikost);
    if(Velikost<0||Velikost>512)return -90;if(číslo_portu<1||číslo_portu>65535)return -22;
    if(되돌림전문접속번호(popisovač_souboru)<0)return -9;
    if(되돌림전문주소(popisovač_souboru)==0x7f000001)return -101;
    int zboží_POČET=externí_číslo(popisovač_souboru);if(zboží_POČET<0){int 반환값=0;if(되돌림전문접속번호(popisovač_souboru)==0)반환값=되돌림전문묶기(popisovač_souboru,0,0);if(반환값<0)return 반환값;zboží_POČET=vložit_SMS(popisovač_souboru,2);if(zboží_POČET<0)return zboží_POČET;반환값=čistý_vázat(zboží_POČET,망상태읽기(0,0),되돌림전문접속번호(popisovač_souboru));if(반환값<0)return 반환값;}
    unsigned char data[512];for(int 순번=0;순번<Velikost;순번++)data[순번]=자바전문얻기(순번);return poslat_datagram(zboží_POČET,data,Velikost,internetová_adresa,číslo_portu);
}
int32_t 자바전문받기(int32_t popisovač_souboru,int32_t Velikost){
    int zboží_POČET=externí_číslo(popisovač_souboru);if(zboží_POČET<0)return 되돌림전문받기(popisovač_souboru,Velikost);if(Velikost<0||Velikost>512)return -22;
    int místní=되돌림전문받기(popisovač_souboru,Velikost);if(místní!=-11){protokol_UDP_externí_partner[popisovač_souboru-32]=0;return místní;}
    unsigned char data[512];int 반환값=dostat_datagram(zboží_POČET,data,Velikost);if(반환값>=0)protokol_UDP_externí_partner[popisovač_souboru-32]=1;for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,data[순번]);return 반환값;
}
int32_t 자바전문접속번호(int32_t popisovač_souboru){int zboží_POČET=externí_číslo(popisovač_souboru);return zboží_POČET<0?되돌림전문접속번호(popisovač_souboru):(int32_t)síť_číslo_portu(zboží_POČET);}
int32_t 자바전문주소(int32_t popisovač_souboru){return externí_číslo(popisovač_souboru)<0?되돌림전문주소(popisovač_souboru):mez_ODKAZ[popisovač_souboru-32];}
int32_t 자바전문상대(int32_t popisovač_souboru){int zboží_POČET=externí_číslo(popisovač_souboru);return zboží_POČET<0||!protokol_UDP_externí_partner[popisovač_souboru-32]?되돌림전문상대(popisovač_souboru):(int32_t)partner_číslo_portu(zboží_POČET);}
int32_t 자바전문원격주소(int32_t popisovač_souboru){int zboží_POČET=externí_číslo(popisovač_souboru);return zboží_POČET<0||!protokol_UDP_externí_partner[popisovač_souboru-32]?0x7f000001:(int32_t)čistý_partner_ODKAZ(zboží_POČET);}
int32_t 자바전문닫기(int32_t popisovač_souboru){int zboží_POČET=externí_číslo(popisovač_souboru);if(zboží_POČET>=0){Zavřít_síť(zboží_POČET);externí[popisovač_souboru-32]=0;}if(popisovač_souboru>=32&&popisovač_souboru<40)protokol_UDP_externí_partner[popisovač_souboru-32]=mez_ODKAZ[popisovač_souboru-32]=0;return 되돌림전문닫기(popisovač_souboru);}
int32_t 자바흐름만들기(void){return 되돌림흐름만들기();}
int32_t 자바흐름묶기(int32_t popisovač_souboru,int32_t internetová_adresa,int32_t číslo_portu){
    if(internetová_adresa==0||internetová_adresa==0x7f000001){int 반환값=되돌림흐름묶기(popisovač_souboru,internetová_adresa,číslo_portu);if(!반환값)임의주소[popisovač_souboru-32]=internetová_adresa==0;return 반환값;}
    if(internetová_adresa!=망상태읽기(0,0))return -99;int 반환값=되돌림흐름묶기(popisovač_souboru,0,číslo_portu);if(반환값<0)return 반환값;
    int zboží_POČET=vložit_SMS(popisovač_souboru,1);return zboží_POČET<0?zboží_POČET:čistý_vázat(zboží_POČET,internetová_adresa,되돌림흐름접속번호(popisovač_souboru));
}
int32_t 자바흐름듣기(int32_t popisovač_souboru,int32_t backlog){
    int zboží_POČET=externí_číslo(popisovač_souboru);if(zboží_POČET<0){int 반환값=되돌림흐름듣기(popisovač_souboru,backlog);if(반환값<0||!임의주소[popisovač_souboru-32])return 반환값;
        zboží_POČET=vložit_SMS(popisovač_souboru,1);if(zboží_POČET<0)return zboží_POČET;반환값=čistý_vázat(zboží_POČET,망상태읽기(0,0),되돌림흐름접속번호(popisovač_souboru));if(반환값<0)return 반환값;양쪽수신창구[popisovač_souboru-32]=1;
    }return backlog<1?-22:čistý_naslouchat(zboží_POČET);
}
int32_t 자바흐름연결(int32_t popisovač_souboru,int32_t internetová_adresa,int32_t číslo_portu){
    if(internetová_adresa==0x7f000001 && externí_číslo(popisovač_souboru)<0)return 되돌림흐름연결(popisovač_souboru,internetová_adresa,číslo_portu);
    if(되돌림흐름접속번호(popisovač_souboru)<0)return -9;int zboží_POČET=vložit_SMS(popisovač_souboru,1);return zboží_POČET<0?zboží_POČET:čistý_spojit(zboží_POČET,internetová_adresa,číslo_portu);
}
int32_t 자바흐름연결받기(int32_t popisovač_souboru){
    int zboží_POČET=externí_číslo(popisovač_souboru);if(zboží_POČET<0)return 되돌림흐름연결받기(popisovač_souboru);
    if(양쪽수신창구[popisovač_souboru-32]){int místní=되돌림흐름연결받기(popisovač_souboru);if(místní!=-11)return místní;}
    int partner_HODNOTA=čistý_přijmout(zboží_POČET);if(partner_HODNOTA<0)return partner_HODNOTA;
    int cílová_úroveň=되돌림흐름만들기();if(cílová_úroveň<0){Zavřít_síť(partner_HODNOTA);return cílová_úroveň;}externí[cílová_úroveň-32]=partner_HODNOTA+1;return cílová_úroveň;
}
int32_t 자바흐름읽기(int32_t popisovač_souboru,int32_t Velikost){
    int zboží_POČET=externí_číslo(popisovač_souboru);if(zboží_POČET<0)return 되돌림흐름읽기(popisovač_souboru,Velikost);if(Velikost<0||Velikost>512)return -22;
    unsigned char data[512];int 반환값=통신읽기(zboží_POČET,data,Velikost);for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,data[순번]);return 반환값;
}
int32_t 자바흐름쓰기(int32_t popisovač_souboru,int32_t Velikost){
    int zboží_POČET=externí_číslo(popisovač_souboru);if(zboží_POČET<0)return 되돌림흐름쓰기(popisovač_souboru,Velikost);if(Velikost<0||Velikost>512)return -22;
    unsigned char data[512];for(int 순번=0;순번<Velikost;순번++)data[순번]=자바전문얻기(순번);return čistý_zápis(zboží_POČET,data,Velikost);
}
int32_t 자바흐름접속번호(int32_t popisovač_souboru){int zboží_POČET=externí_číslo(popisovač_souboru);return zboží_POČET<0?되돌림흐름접속번호(popisovač_souboru):(int32_t)síť_číslo_portu(zboží_POČET);}
int32_t 자바흐름상대(int32_t popisovač_souboru){int zboží_POČET=externí_číslo(popisovač_souboru);return zboží_POČET<0?되돌림흐름상대(popisovač_souboru):(int32_t)partner_číslo_portu(zboží_POČET);}
int32_t 자바흐름주소(int32_t popisovač_souboru){return externí_číslo(popisovač_souboru)<0?0x7f000001:양쪽수신창구[popisovač_souboru-32]?0:망상태읽기(0,0);}
int32_t 자바흐름닫기(int32_t popisovač_souboru){int zboží_POČET=externí_číslo(popisovač_souboru);if(zboží_POČET>=0){Zavřít_síť(zboží_POČET);externí[popisovač_souboru-32]=0;}if(popisovač_souboru>=40&&popisovač_souboru<56)임의주소[popisovač_souboru-32]=양쪽수신창구[popisovač_souboru-32]=0;return 되돌림흐름닫기(popisovač_souboru);}
