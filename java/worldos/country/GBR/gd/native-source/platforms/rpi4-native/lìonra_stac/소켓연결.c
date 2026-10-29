#include "../명명/기계연결이름.h"
/* Preserve the deterministic Java loopback endpoints; route external IPv4 to lwIP. */
#include "lìonra_stac.h"
extern int32_t 되돌림전문만들기(int32_t,int32_t,int32_t), 되돌림전문묶기(int32_t,int32_t,int32_t);
extern int32_t 되돌림전문보내기(int32_t,int32_t,int32_t,int32_t), 되돌림전문받기(int32_t,int32_t);
extern int32_t 되돌림전문접속번호(int32_t), 되돌림전문주소(int32_t), 되돌림전문상대(int32_t), 되돌림전문닫기(int32_t);
extern int32_t 자바전문넣기(int32_t,int32_t),자바전문얻기(int32_t);
extern int32_t 되돌림흐름만들기(void),되돌림흐름묶기(int32_t,int32_t,int32_t),되돌림흐름듣기(int32_t,int32_t);
extern int32_t 되돌림흐름연결(int32_t,int32_t,int32_t),되돌림흐름연결받기(int32_t),되돌림흐름읽기(int32_t,int32_t),되돌림흐름쓰기(int32_t,int32_t);
extern int32_t 되돌림흐름접속번호(int32_t),되돌림흐름상대(int32_t),되돌림흐름닫기(int32_t);
static int 외부연결[24];
static int 임의주소[24], 양쪽수신창구[24], 전문외부상대[8], 묶인주소[8];
static int 외부번호(int faidhle_làmhrachan) { return faidhle_làmhrachan>=32 && faidhle_làmhrachan<56 ? 외부연결[faidhle_làmhrachan-32]-1 : -1; }
static int cuir_ann_SMS(int faidhle_làmhrachan,int TYPE_roinn_seòrsa) {
    if(faidhle_làmhrachan<32||faidhle_làmhrachan>=56)return -9;int 이전=외부번호(faidhle_làmhrachan);if(이전>=0)return 이전;
    int nì_COUNT=통신끝점만들기(TYPE_roinn_seòrsa);if(nì_COUNT>=0)외부연결[faidhle_làmhrachan-32]=nì_COUNT+1;return nì_COUNT;
}
int32_t 자바전문만들기(int32_t 첫째값,int32_t SECOND_VALUE,int32_t còd_a_charactair){return 되돌림전문만들기(첫째값,SECOND_VALUE,còd_a_charactair);}
int32_t 자바전문묶기(int32_t faidhle_làmhrachan,int32_t Seòladh_eadar_lìn,int32_t 접속번호){
    if(Seòladh_eadar_lìn==0x7f000001)return 되돌림전문묶기(faidhle_làmhrachan,Seòladh_eadar_lìn,접속번호);
    if(Seòladh_eadar_lìn!=0&&Seòladh_eadar_lìn!=망상태읽기(0,0))return -99;
    int 반환값=되돌림전문묶기(faidhle_làmhrachan,0,접속번호);if(반환값<0)return 반환값;
    int nì_COUNT=cuir_ann_SMS(faidhle_làmhrachan,2);if(nì_COUNT<0)return nì_COUNT;반환값=망주소묶기(nì_COUNT,망상태읽기(0,0),되돌림전문접속번호(faidhle_làmhrachan));if(!반환값)묶인주소[faidhle_làmhrachan-32]=Seòladh_eadar_lìn;return 반환값;
}
int32_t 자바전문보내기(int32_t faidhle_làmhrachan,int32_t Seòladh_eadar_lìn,int32_t 접속번호,int32_t atharraich_am_meud){
    if(Seòladh_eadar_lìn==0x7f000001)return 되돌림전문보내기(faidhle_làmhrachan,Seòladh_eadar_lìn,접속번호,atharraich_am_meud);
    if(atharraich_am_meud<0||atharraich_am_meud>512)return -90;if(접속번호<1||접속번호>65535)return -22;
    if(되돌림전문접속번호(faidhle_làmhrachan)<0)return -9;
    if(되돌림전문주소(faidhle_làmhrachan)==0x7f000001)return -101;
    int nì_COUNT=외부번호(faidhle_làmhrachan);if(nì_COUNT<0){int 반환값=0;if(되돌림전문접속번호(faidhle_làmhrachan)==0)반환값=되돌림전문묶기(faidhle_làmhrachan,0,0);if(반환값<0)return 반환값;nì_COUNT=cuir_ann_SMS(faidhle_làmhrachan,2);if(nì_COUNT<0)return nì_COUNT;반환값=망주소묶기(nì_COUNT,망상태읽기(0,0),되돌림전문접속번호(faidhle_làmhrachan));if(반환값<0)return 반환값;}
    unsigned char dàta[512];for(int 순번=0;순번<atharraich_am_meud;순번++)dàta[순번]=자바전문얻기(순번);return 전문보내기(nì_COUNT,dàta,atharraich_am_meud,Seòladh_eadar_lìn,접속번호);
}
int32_t 자바전문받기(int32_t faidhle_làmhrachan,int32_t atharraich_am_meud){
    int nì_COUNT=외부번호(faidhle_làmhrachan);if(nì_COUNT<0)return 되돌림전문받기(faidhle_làmhrachan,atharraich_am_meud);if(atharraich_am_meud<0||atharraich_am_meud>512)return -22;
    int ionadail=되돌림전문받기(faidhle_làmhrachan,atharraich_am_meud);if(ionadail!=-11){전문외부상대[faidhle_làmhrachan-32]=0;return ionadail;}
    unsigned char dàta[512];int 반환값=전문받기(nì_COUNT,dàta,atharraich_am_meud);if(반환값>=0)전문외부상대[faidhle_làmhrachan-32]=1;for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,dàta[순번]);return 반환값;
}
int32_t 자바전문접속번호(int32_t faidhle_làmhrachan){int nì_COUNT=외부번호(faidhle_làmhrachan);return nì_COUNT<0?되돌림전문접속번호(faidhle_làmhrachan):(int32_t)통신접속번호(nì_COUNT);}
int32_t 자바전문주소(int32_t faidhle_làmhrachan){return 외부번호(faidhle_làmhrachan)<0?되돌림전문주소(faidhle_làmhrachan):묶인주소[faidhle_làmhrachan-32];}
int32_t 자바전문상대(int32_t faidhle_làmhrachan){int nì_COUNT=외부번호(faidhle_làmhrachan);return nì_COUNT<0||!전문외부상대[faidhle_làmhrachan-32]?되돌림전문상대(faidhle_làmhrachan):(int32_t)상대접속번호(nì_COUNT);}
int32_t 자바전문원격주소(int32_t faidhle_làmhrachan){int nì_COUNT=외부번호(faidhle_làmhrachan);return nì_COUNT<0||!전문외부상대[faidhle_làmhrachan-32]?0x7f000001:(int32_t)상대통신주소(nì_COUNT);}
int32_t 자바전문닫기(int32_t faidhle_làmhrachan){int nì_COUNT=외부번호(faidhle_làmhrachan);if(nì_COUNT>=0){dùin_lìonra(nì_COUNT);외부연결[faidhle_làmhrachan-32]=0;}if(faidhle_làmhrachan>=32&&faidhle_làmhrachan<40)전문외부상대[faidhle_làmhrachan-32]=묶인주소[faidhle_làmhrachan-32]=0;return 되돌림전문닫기(faidhle_làmhrachan);}
int32_t 자바흐름만들기(void){return 되돌림흐름만들기();}
int32_t 자바흐름묶기(int32_t faidhle_làmhrachan,int32_t Seòladh_eadar_lìn,int32_t 접속번호){
    if(Seòladh_eadar_lìn==0||Seòladh_eadar_lìn==0x7f000001){int 반환값=되돌림흐름묶기(faidhle_làmhrachan,Seòladh_eadar_lìn,접속번호);if(!반환값)임의주소[faidhle_làmhrachan-32]=Seòladh_eadar_lìn==0;return 반환값;}
    if(Seòladh_eadar_lìn!=망상태읽기(0,0))return -99;int 반환값=되돌림흐름묶기(faidhle_làmhrachan,0,접속번호);if(반환값<0)return 반환값;
    int nì_COUNT=cuir_ann_SMS(faidhle_làmhrachan,1);return nì_COUNT<0?nì_COUNT:망주소묶기(nì_COUNT,Seòladh_eadar_lìn,되돌림흐름접속번호(faidhle_làmhrachan));
}
int32_t 자바흐름듣기(int32_t faidhle_làmhrachan,int32_t 연결대기한도){
    int nì_COUNT=외부번호(faidhle_làmhrachan);if(nì_COUNT<0){int 반환값=되돌림흐름듣기(faidhle_làmhrachan,연결대기한도);if(반환값<0||!임의주소[faidhle_làmhrachan-32])return 반환값;
        nì_COUNT=cuir_ann_SMS(faidhle_làmhrachan,1);if(nì_COUNT<0)return nì_COUNT;반환값=망주소묶기(nì_COUNT,망상태읽기(0,0),되돌림흐름접속번호(faidhle_làmhrachan));if(반환값<0)return 반환값;양쪽수신창구[faidhle_làmhrachan-32]=1;
    }return 연결대기한도<1?-22:연결기다리기(nì_COUNT);
}
int32_t 자바흐름연결(int32_t faidhle_làmhrachan,int32_t Seòladh_eadar_lìn,int32_t 접속번호){
    if(Seòladh_eadar_lìn==0x7f000001 && 외부번호(faidhle_làmhrachan)<0)return 되돌림흐름연결(faidhle_làmhrachan,Seòladh_eadar_lìn,접속번호);
    if(되돌림흐름접속번호(faidhle_làmhrachan)<0)return -9;int nì_COUNT=cuir_ann_SMS(faidhle_làmhrachan,1);return nì_COUNT<0?nì_COUNT:망연결하기(nì_COUNT,Seòladh_eadar_lìn,접속번호);
}
int32_t 자바흐름연결받기(int32_t faidhle_làmhrachan){
    int nì_COUNT=외부번호(faidhle_làmhrachan);if(nì_COUNT<0)return 되돌림흐름연결받기(faidhle_làmhrachan);
    if(양쪽수신창구[faidhle_làmhrachan-32]){int ionadail=되돌림흐름연결받기(faidhle_làmhrachan);if(ionadail!=-11)return ionadail;}
    int seise_VALUE=망연결받기(nì_COUNT);if(seise_VALUE<0)return seise_VALUE;
    int targaid=되돌림흐름만들기();if(targaid<0){dùin_lìonra(seise_VALUE);return targaid;}외부연결[targaid-32]=seise_VALUE+1;return targaid;
}
int32_t 자바흐름읽기(int32_t faidhle_làmhrachan,int32_t atharraich_am_meud){
    int nì_COUNT=외부번호(faidhle_làmhrachan);if(nì_COUNT<0)return 되돌림흐름읽기(faidhle_làmhrachan,atharraich_am_meud);if(atharraich_am_meud<0||atharraich_am_meud>512)return -22;
    unsigned char dàta[512];int 반환값=통신읽기(nì_COUNT,dàta,atharraich_am_meud);for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,dàta[순번]);return 반환값;
}
int32_t 자바흐름쓰기(int32_t faidhle_làmhrachan,int32_t atharraich_am_meud){
    int nì_COUNT=외부번호(faidhle_làmhrachan);if(nì_COUNT<0)return 되돌림흐름쓰기(faidhle_làmhrachan,atharraich_am_meud);if(atharraich_am_meud<0||atharraich_am_meud>512)return -22;
    unsigned char dàta[512];for(int 순번=0;순번<atharraich_am_meud;순번++)dàta[순번]=자바전문얻기(순번);return 통신쓰기(nì_COUNT,dàta,atharraich_am_meud);
}
int32_t 자바흐름접속번호(int32_t faidhle_làmhrachan){int nì_COUNT=외부번호(faidhle_làmhrachan);return nì_COUNT<0?되돌림흐름접속번호(faidhle_làmhrachan):(int32_t)통신접속번호(nì_COUNT);}
int32_t 자바흐름상대(int32_t faidhle_làmhrachan){int nì_COUNT=외부번호(faidhle_làmhrachan);return nì_COUNT<0?되돌림흐름상대(faidhle_làmhrachan):(int32_t)상대접속번호(nì_COUNT);}
int32_t 자바흐름주소(int32_t faidhle_làmhrachan){return 외부번호(faidhle_làmhrachan)<0?0x7f000001:양쪽수신창구[faidhle_làmhrachan-32]?0:망상태읽기(0,0);}
int32_t 자바흐름닫기(int32_t faidhle_làmhrachan){int nì_COUNT=외부번호(faidhle_làmhrachan);if(nì_COUNT>=0){dùin_lìonra(nì_COUNT);외부연결[faidhle_làmhrachan-32]=0;}if(faidhle_làmhrachan>=40&&faidhle_làmhrachan<56)임의주소[faidhle_làmhrachan-32]=양쪽수신창구[faidhle_làmhrachan-32]=0;return 되돌림흐름닫기(faidhle_làmhrachan);}
