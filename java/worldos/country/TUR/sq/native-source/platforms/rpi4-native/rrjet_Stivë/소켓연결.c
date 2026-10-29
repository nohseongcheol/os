#include "../명명/기계연결이름.h"
/* Preserve the deterministic Java loopback endpoints; route external IPv4 to lwIP. */
#include "rrjet_Stivë.h"
extern int32_t 되돌림전문만들기(int32_t,int32_t,int32_t), 되돌림전문묶기(int32_t,int32_t,int32_t);
extern int32_t 되돌림전문보내기(int32_t,int32_t,int32_t,int32_t), 되돌림전문받기(int32_t,int32_t);
extern int32_t 되돌림전문접속번호(int32_t), 되돌림전문주소(int32_t), 되돌림전문상대(int32_t), 되돌림전문닫기(int32_t);
extern int32_t 자바전문넣기(int32_t,int32_t),자바전문얻기(int32_t);
extern int32_t 되돌림흐름만들기(void),되돌림흐름묶기(int32_t,int32_t,int32_t),되돌림흐름듣기(int32_t,int32_t);
extern int32_t 되돌림흐름연결(int32_t,int32_t,int32_t),되돌림흐름연결받기(int32_t),되돌림흐름읽기(int32_t,int32_t),되돌림흐름쓰기(int32_t,int32_t);
extern int32_t 되돌림흐름접속번호(int32_t),되돌림흐름상대(int32_t),되돌림흐름닫기(int32_t);
static int 외부연결[24];
static int 임의주소[24], 양쪽수신창구[24], 전문외부상대[8], 묶인주소[8];
static int 외부번호(int skedar_dorezë) { return skedar_dorezë>=32 && skedar_dorezë<56 ? 외부연결[skedar_dorezë-32]-1 : -1; }
static int ngjit_SMS(int skedar_dorezë,int TYPE_kategori) {
    if(skedar_dorezë<32||skedar_dorezë>=56)return -9;int 이전=외부번호(skedar_dorezë);if(이전>=0)return 이전;
    int njësi_COUNT=통신끝점만들기(TYPE_kategori);if(njësi_COUNT>=0)외부연결[skedar_dorezë-32]=njësi_COUNT+1;return njësi_COUNT;
}
int32_t 자바전문만들기(int32_t 첫째값,int32_t SECOND_VALUE,int32_t kodi_i_karakterit){return 되돌림전문만들기(첫째값,SECOND_VALUE,kodi_i_karakterit);}
int32_t 자바전문묶기(int32_t skedar_dorezë,int32_t adresë_në_internet,int32_t numri_i_portës){
    if(adresë_në_internet==0x7f000001)return 되돌림전문묶기(skedar_dorezë,adresë_në_internet,numri_i_portës);
    if(adresë_në_internet!=0&&adresë_në_internet!=망상태읽기(0,0))return -99;
    int 반환값=되돌림전문묶기(skedar_dorezë,0,numri_i_portës);if(반환값<0)return 반환값;
    int njësi_COUNT=ngjit_SMS(skedar_dorezë,2);if(njësi_COUNT<0)return njësi_COUNT;반환값=망주소묶기(njësi_COUNT,망상태읽기(0,0),되돌림전문접속번호(skedar_dorezë));if(!반환값)묶인주소[skedar_dorezë-32]=adresë_në_internet;return 반환값;
}
int32_t 자바전문보내기(int32_t skedar_dorezë,int32_t adresë_në_internet,int32_t numri_i_portës,int32_t Madhësi){
    if(adresë_në_internet==0x7f000001)return 되돌림전문보내기(skedar_dorezë,adresë_në_internet,numri_i_portës,Madhësi);
    if(Madhësi<0||Madhësi>512)return -90;if(numri_i_portës<1||numri_i_portës>65535)return -22;
    if(되돌림전문접속번호(skedar_dorezë)<0)return -9;
    if(되돌림전문주소(skedar_dorezë)==0x7f000001)return -101;
    int njësi_COUNT=외부번호(skedar_dorezë);if(njësi_COUNT<0){int 반환값=0;if(되돌림전문접속번호(skedar_dorezë)==0)반환값=되돌림전문묶기(skedar_dorezë,0,0);if(반환값<0)return 반환값;njësi_COUNT=ngjit_SMS(skedar_dorezë,2);if(njësi_COUNT<0)return njësi_COUNT;반환값=망주소묶기(njësi_COUNT,망상태읽기(0,0),되돌림전문접속번호(skedar_dorezë));if(반환값<0)return 반환값;}
    unsigned char të_dhëna[512];for(int 순번=0;순번<Madhësi;순번++)të_dhëna[순번]=자바전문얻기(순번);return 전문보내기(njësi_COUNT,të_dhëna,Madhësi,adresë_në_internet,numri_i_portës);
}
int32_t 자바전문받기(int32_t skedar_dorezë,int32_t Madhësi){
    int njësi_COUNT=외부번호(skedar_dorezë);if(njësi_COUNT<0)return 되돌림전문받기(skedar_dorezë,Madhësi);if(Madhësi<0||Madhësi>512)return -22;
    int lokal=되돌림전문받기(skedar_dorezë,Madhësi);if(lokal!=-11){전문외부상대[skedar_dorezë-32]=0;return lokal;}
    unsigned char të_dhëna[512];int 반환값=전문받기(njësi_COUNT,të_dhëna,Madhësi);if(반환값>=0)전문외부상대[skedar_dorezë-32]=1;for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,të_dhëna[순번]);return 반환값;
}
int32_t 자바전문접속번호(int32_t skedar_dorezë){int njësi_COUNT=외부번호(skedar_dorezë);return njësi_COUNT<0?되돌림전문접속번호(skedar_dorezë):(int32_t)rrjet_numri_i_portës(njësi_COUNT);}
int32_t 자바전문주소(int32_t skedar_dorezë){return 외부번호(skedar_dorezë)<0?되돌림전문주소(skedar_dorezë):묶인주소[skedar_dorezë-32];}
int32_t 자바전문상대(int32_t skedar_dorezë){int njësi_COUNT=외부번호(skedar_dorezë);return njësi_COUNT<0||!전문외부상대[skedar_dorezë-32]?되돌림전문상대(skedar_dorezë):(int32_t)homolog_numri_i_portës(njësi_COUNT);}
int32_t 자바전문원격주소(int32_t skedar_dorezë){int njësi_COUNT=외부번호(skedar_dorezë);return njësi_COUNT<0||!전문외부상대[skedar_dorezë-32]?0x7f000001:(int32_t)상대통신주소(njësi_COUNT);}
int32_t 자바전문닫기(int32_t skedar_dorezë){int njësi_COUNT=외부번호(skedar_dorezë);if(njësi_COUNT>=0){mbyll_rrjet(njësi_COUNT);외부연결[skedar_dorezë-32]=0;}if(skedar_dorezë>=32&&skedar_dorezë<40)전문외부상대[skedar_dorezë-32]=묶인주소[skedar_dorezë-32]=0;return 되돌림전문닫기(skedar_dorezë);}
int32_t 자바흐름만들기(void){return 되돌림흐름만들기();}
int32_t 자바흐름묶기(int32_t skedar_dorezë,int32_t adresë_në_internet,int32_t numri_i_portës){
    if(adresë_në_internet==0||adresë_në_internet==0x7f000001){int 반환값=되돌림흐름묶기(skedar_dorezë,adresë_në_internet,numri_i_portës);if(!반환값)임의주소[skedar_dorezë-32]=adresë_në_internet==0;return 반환값;}
    if(adresë_në_internet!=망상태읽기(0,0))return -99;int 반환값=되돌림흐름묶기(skedar_dorezë,0,numri_i_portës);if(반환값<0)return 반환값;
    int njësi_COUNT=ngjit_SMS(skedar_dorezë,1);return njësi_COUNT<0?njësi_COUNT:망주소묶기(njësi_COUNT,adresë_në_internet,되돌림흐름접속번호(skedar_dorezë));
}
int32_t 자바흐름듣기(int32_t skedar_dorezë,int32_t 연결대기한도){
    int njësi_COUNT=외부번호(skedar_dorezë);if(njësi_COUNT<0){int 반환값=되돌림흐름듣기(skedar_dorezë,연결대기한도);if(반환값<0||!임의주소[skedar_dorezë-32])return 반환값;
        njësi_COUNT=ngjit_SMS(skedar_dorezë,1);if(njësi_COUNT<0)return njësi_COUNT;반환값=망주소묶기(njësi_COUNT,망상태읽기(0,0),되돌림흐름접속번호(skedar_dorezë));if(반환값<0)return 반환값;양쪽수신창구[skedar_dorezë-32]=1;
    }return 연결대기한도<1?-22:연결기다리기(njësi_COUNT);
}
int32_t 자바흐름연결(int32_t skedar_dorezë,int32_t adresë_në_internet,int32_t numri_i_portës){
    if(adresë_në_internet==0x7f000001 && 외부번호(skedar_dorezë)<0)return 되돌림흐름연결(skedar_dorezë,adresë_në_internet,numri_i_portës);
    if(되돌림흐름접속번호(skedar_dorezë)<0)return -9;int njësi_COUNT=ngjit_SMS(skedar_dorezë,1);return njësi_COUNT<0?njësi_COUNT:망연결하기(njësi_COUNT,adresë_në_internet,numri_i_portës);
}
int32_t 자바흐름연결받기(int32_t skedar_dorezë){
    int njësi_COUNT=외부번호(skedar_dorezë);if(njësi_COUNT<0)return 되돌림흐름연결받기(skedar_dorezë);
    if(양쪽수신창구[skedar_dorezë-32]){int lokal=되돌림흐름연결받기(skedar_dorezë);if(lokal!=-11)return lokal;}
    int homolog_VALUE=망연결받기(njësi_COUNT);if(homolog_VALUE<0)return homolog_VALUE;
    int objektiv=되돌림흐름만들기();if(objektiv<0){mbyll_rrjet(homolog_VALUE);return objektiv;}외부연결[objektiv-32]=homolog_VALUE+1;return objektiv;
}
int32_t 자바흐름읽기(int32_t skedar_dorezë,int32_t Madhësi){
    int njësi_COUNT=외부번호(skedar_dorezë);if(njësi_COUNT<0)return 되돌림흐름읽기(skedar_dorezë,Madhësi);if(Madhësi<0||Madhësi>512)return -22;
    unsigned char të_dhëna[512];int 반환값=통신읽기(njësi_COUNT,të_dhëna,Madhësi);for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,të_dhëna[순번]);return 반환값;
}
int32_t 자바흐름쓰기(int32_t skedar_dorezë,int32_t Madhësi){
    int njësi_COUNT=외부번호(skedar_dorezë);if(njësi_COUNT<0)return 되돌림흐름쓰기(skedar_dorezë,Madhësi);if(Madhësi<0||Madhësi>512)return -22;
    unsigned char të_dhëna[512];for(int 순번=0;순번<Madhësi;순번++)të_dhëna[순번]=자바전문얻기(순번);return 통신쓰기(njësi_COUNT,të_dhëna,Madhësi);
}
int32_t 자바흐름접속번호(int32_t skedar_dorezë){int njësi_COUNT=외부번호(skedar_dorezë);return njësi_COUNT<0?되돌림흐름접속번호(skedar_dorezë):(int32_t)rrjet_numri_i_portës(njësi_COUNT);}
int32_t 자바흐름상대(int32_t skedar_dorezë){int njësi_COUNT=외부번호(skedar_dorezë);return njësi_COUNT<0?되돌림흐름상대(skedar_dorezë):(int32_t)homolog_numri_i_portës(njësi_COUNT);}
int32_t 자바흐름주소(int32_t skedar_dorezë){return 외부번호(skedar_dorezë)<0?0x7f000001:양쪽수신창구[skedar_dorezë-32]?0:망상태읽기(0,0);}
int32_t 자바흐름닫기(int32_t skedar_dorezë){int njësi_COUNT=외부번호(skedar_dorezë);if(njësi_COUNT>=0){mbyll_rrjet(njësi_COUNT);외부연결[skedar_dorezë-32]=0;}if(skedar_dorezë>=40&&skedar_dorezë<56)임의주소[skedar_dorezë-32]=양쪽수신창구[skedar_dorezë-32]=0;return 되돌림흐름닫기(skedar_dorezë);}
