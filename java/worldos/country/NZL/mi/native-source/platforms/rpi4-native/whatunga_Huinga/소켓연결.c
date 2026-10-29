#include "../명명/기계연결이름.h"
/* Preserve the deterministic Java loopback endpoints; route external IPv4 to lwIP. */
#include "whatunga_Huinga.h"
extern int32_t 되돌림전문만들기(int32_t,int32_t,int32_t), 되돌림전문묶기(int32_t,int32_t,int32_t);
extern int32_t 되돌림전문보내기(int32_t,int32_t,int32_t,int32_t), 되돌림전문받기(int32_t,int32_t);
extern int32_t 되돌림전문접속번호(int32_t), 되돌림전문주소(int32_t), 되돌림전문상대(int32_t), 되돌림전문닫기(int32_t);
extern int32_t 자바전문넣기(int32_t,int32_t),자바전문얻기(int32_t);
extern int32_t 되돌림흐름만들기(void),되돌림흐름묶기(int32_t,int32_t,int32_t),되돌림흐름듣기(int32_t,int32_t);
extern int32_t 되돌림흐름연결(int32_t,int32_t,int32_t),되돌림흐름연결받기(int32_t),되돌림흐름읽기(int32_t,int32_t),되돌림흐름쓰기(int32_t,int32_t);
extern int32_t 되돌림흐름접속번호(int32_t),되돌림흐름상대(int32_t),되돌림흐름닫기(int32_t);
static int 외부연결[24];
static int 임의주소[24], 양쪽수신창구[24], 전문외부상대[8], 묶인주소[8];
static int 외부번호(int kōnae_raweke) { return kōnae_raweke>=32 && kōnae_raweke<56 ? 외부연결[kōnae_raweke-32]-1 : -1; }
static int whakapiri_TEXT(int kōnae_raweke,int TYPE_kāwai) {
    if(kōnae_raweke<32||kōnae_raweke>=56)return -9;int 이전=외부번호(kōnae_raweke);if(이전>=0)return 이전;
    int tuemi_COUNT=통신끝점만들기(TYPE_kāwai);if(tuemi_COUNT>=0)외부연결[kōnae_raweke-32]=tuemi_COUNT+1;return tuemi_COUNT;
}
int32_t 자바전문만들기(int32_t 첫째값,int32_t SECOND_uara,int32_t waehere_pūāhua){return 되돌림전문만들기(첫째값,SECOND_uara,waehere_pūāhua);}
int32_t 자바전문묶기(int32_t kōnae_raweke,int32_t Wāhitau_ipurangi,int32_t 접속번호){
    if(Wāhitau_ipurangi==0x7f000001)return 되돌림전문묶기(kōnae_raweke,Wāhitau_ipurangi,접속번호);
    if(Wāhitau_ipurangi!=0&&Wāhitau_ipurangi!=망상태읽기(0,0))return -99;
    int 반환값=되돌림전문묶기(kōnae_raweke,0,접속번호);if(반환값<0)return 반환값;
    int tuemi_COUNT=whakapiri_TEXT(kōnae_raweke,2);if(tuemi_COUNT<0)return tuemi_COUNT;반환값=망주소묶기(tuemi_COUNT,망상태읽기(0,0),되돌림전문접속번호(kōnae_raweke));if(!반환값)묶인주소[kōnae_raweke-32]=Wāhitau_ipurangi;return 반환값;
}
int32_t 자바전문보내기(int32_t kōnae_raweke,int32_t Wāhitau_ipurangi,int32_t 접속번호,int32_t rahi){
    if(Wāhitau_ipurangi==0x7f000001)return 되돌림전문보내기(kōnae_raweke,Wāhitau_ipurangi,접속번호,rahi);
    if(rahi<0||rahi>512)return -90;if(접속번호<1||접속번호>65535)return -22;
    if(되돌림전문접속번호(kōnae_raweke)<0)return -9;
    if(되돌림전문주소(kōnae_raweke)==0x7f000001)return -101;
    int tuemi_COUNT=외부번호(kōnae_raweke);if(tuemi_COUNT<0){int 반환값=0;if(되돌림전문접속번호(kōnae_raweke)==0)반환값=되돌림전문묶기(kōnae_raweke,0,0);if(반환값<0)return 반환값;tuemi_COUNT=whakapiri_TEXT(kōnae_raweke,2);if(tuemi_COUNT<0)return tuemi_COUNT;반환값=망주소묶기(tuemi_COUNT,망상태읽기(0,0),되돌림전문접속번호(kōnae_raweke));if(반환값<0)return 반환값;}
    unsigned char raraunga[512];for(int 순번=0;순번<rahi;순번++)raraunga[순번]=자바전문얻기(순번);return 전문보내기(tuemi_COUNT,raraunga,rahi,Wāhitau_ipurangi,접속번호);
}
int32_t 자바전문받기(int32_t kōnae_raweke,int32_t rahi){
    int tuemi_COUNT=외부번호(kōnae_raweke);if(tuemi_COUNT<0)return 되돌림전문받기(kōnae_raweke,rahi);if(rahi<0||rahi>512)return -22;
    int paetata=되돌림전문받기(kōnae_raweke,rahi);if(paetata!=-11){전문외부상대[kōnae_raweke-32]=0;return paetata;}
    unsigned char raraunga[512];int 반환값=전문받기(tuemi_COUNT,raraunga,rahi);if(반환값>=0)전문외부상대[kōnae_raweke-32]=1;for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,raraunga[순번]);return 반환값;
}
int32_t 자바전문접속번호(int32_t kōnae_raweke){int tuemi_COUNT=외부번호(kōnae_raweke);return tuemi_COUNT<0?되돌림전문접속번호(kōnae_raweke):(int32_t)통신접속번호(tuemi_COUNT);}
int32_t 자바전문주소(int32_t kōnae_raweke){return 외부번호(kōnae_raweke)<0?되돌림전문주소(kōnae_raweke):묶인주소[kōnae_raweke-32];}
int32_t 자바전문상대(int32_t kōnae_raweke){int tuemi_COUNT=외부번호(kōnae_raweke);return tuemi_COUNT<0||!전문외부상대[kōnae_raweke-32]?되돌림전문상대(kōnae_raweke):(int32_t)상대접속번호(tuemi_COUNT);}
int32_t 자바전문원격주소(int32_t kōnae_raweke){int tuemi_COUNT=외부번호(kōnae_raweke);return tuemi_COUNT<0||!전문외부상대[kōnae_raweke-32]?0x7f000001:(int32_t)상대통신주소(tuemi_COUNT);}
int32_t 자바전문닫기(int32_t kōnae_raweke){int tuemi_COUNT=외부번호(kōnae_raweke);if(tuemi_COUNT>=0){kati_whatunga(tuemi_COUNT);외부연결[kōnae_raweke-32]=0;}if(kōnae_raweke>=32&&kōnae_raweke<40)전문외부상대[kōnae_raweke-32]=묶인주소[kōnae_raweke-32]=0;return 되돌림전문닫기(kōnae_raweke);}
int32_t 자바흐름만들기(void){return 되돌림흐름만들기();}
int32_t 자바흐름묶기(int32_t kōnae_raweke,int32_t Wāhitau_ipurangi,int32_t 접속번호){
    if(Wāhitau_ipurangi==0||Wāhitau_ipurangi==0x7f000001){int 반환값=되돌림흐름묶기(kōnae_raweke,Wāhitau_ipurangi,접속번호);if(!반환값)임의주소[kōnae_raweke-32]=Wāhitau_ipurangi==0;return 반환값;}
    if(Wāhitau_ipurangi!=망상태읽기(0,0))return -99;int 반환값=되돌림흐름묶기(kōnae_raweke,0,접속번호);if(반환값<0)return 반환값;
    int tuemi_COUNT=whakapiri_TEXT(kōnae_raweke,1);return tuemi_COUNT<0?tuemi_COUNT:망주소묶기(tuemi_COUNT,Wāhitau_ipurangi,되돌림흐름접속번호(kōnae_raweke));
}
int32_t 자바흐름듣기(int32_t kōnae_raweke,int32_t 연결대기한도){
    int tuemi_COUNT=외부번호(kōnae_raweke);if(tuemi_COUNT<0){int 반환값=되돌림흐름듣기(kōnae_raweke,연결대기한도);if(반환값<0||!임의주소[kōnae_raweke-32])return 반환값;
        tuemi_COUNT=whakapiri_TEXT(kōnae_raweke,1);if(tuemi_COUNT<0)return tuemi_COUNT;반환값=망주소묶기(tuemi_COUNT,망상태읽기(0,0),되돌림흐름접속번호(kōnae_raweke));if(반환값<0)return 반환값;양쪽수신창구[kōnae_raweke-32]=1;
    }return 연결대기한도<1?-22:연결기다리기(tuemi_COUNT);
}
int32_t 자바흐름연결(int32_t kōnae_raweke,int32_t Wāhitau_ipurangi,int32_t 접속번호){
    if(Wāhitau_ipurangi==0x7f000001 && 외부번호(kōnae_raweke)<0)return 되돌림흐름연결(kōnae_raweke,Wāhitau_ipurangi,접속번호);
    if(되돌림흐름접속번호(kōnae_raweke)<0)return -9;int tuemi_COUNT=whakapiri_TEXT(kōnae_raweke,1);return tuemi_COUNT<0?tuemi_COUNT:망연결하기(tuemi_COUNT,Wāhitau_ipurangi,접속번호);
}
int32_t 자바흐름연결받기(int32_t kōnae_raweke){
    int tuemi_COUNT=외부번호(kōnae_raweke);if(tuemi_COUNT<0)return 되돌림흐름연결받기(kōnae_raweke);
    if(양쪽수신창구[kōnae_raweke-32]){int paetata=되돌림흐름연결받기(kōnae_raweke);if(paetata!=-11)return paetata;}
    int hoa_uara=망연결받기(tuemi_COUNT);if(hoa_uara<0)return hoa_uara;
    int ūnga=되돌림흐름만들기();if(ūnga<0){kati_whatunga(hoa_uara);return ūnga;}외부연결[ūnga-32]=hoa_uara+1;return ūnga;
}
int32_t 자바흐름읽기(int32_t kōnae_raweke,int32_t rahi){
    int tuemi_COUNT=외부번호(kōnae_raweke);if(tuemi_COUNT<0)return 되돌림흐름읽기(kōnae_raweke,rahi);if(rahi<0||rahi>512)return -22;
    unsigned char raraunga[512];int 반환값=통신읽기(tuemi_COUNT,raraunga,rahi);for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,raraunga[순번]);return 반환값;
}
int32_t 자바흐름쓰기(int32_t kōnae_raweke,int32_t rahi){
    int tuemi_COUNT=외부번호(kōnae_raweke);if(tuemi_COUNT<0)return 되돌림흐름쓰기(kōnae_raweke,rahi);if(rahi<0||rahi>512)return -22;
    unsigned char raraunga[512];for(int 순번=0;순번<rahi;순번++)raraunga[순번]=자바전문얻기(순번);return 통신쓰기(tuemi_COUNT,raraunga,rahi);
}
int32_t 자바흐름접속번호(int32_t kōnae_raweke){int tuemi_COUNT=외부번호(kōnae_raweke);return tuemi_COUNT<0?되돌림흐름접속번호(kōnae_raweke):(int32_t)통신접속번호(tuemi_COUNT);}
int32_t 자바흐름상대(int32_t kōnae_raweke){int tuemi_COUNT=외부번호(kōnae_raweke);return tuemi_COUNT<0?되돌림흐름상대(kōnae_raweke):(int32_t)상대접속번호(tuemi_COUNT);}
int32_t 자바흐름주소(int32_t kōnae_raweke){return 외부번호(kōnae_raweke)<0?0x7f000001:양쪽수신창구[kōnae_raweke-32]?0:망상태읽기(0,0);}
int32_t 자바흐름닫기(int32_t kōnae_raweke){int tuemi_COUNT=외부번호(kōnae_raweke);if(tuemi_COUNT>=0){kati_whatunga(tuemi_COUNT);외부연결[kōnae_raweke-32]=0;}if(kōnae_raweke>=40&&kōnae_raweke<56)임의주소[kōnae_raweke-32]=양쪽수신창구[kōnae_raweke-32]=0;return 되돌림흐름닫기(kōnae_raweke);}
