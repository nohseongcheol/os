#include "../명명/기계연결이름.h"
/* Preserve the deterministic Java loopback endpoints; route external IPv4 to lwIP. */
#include "Líonra_Cruach.h"
extern int32_t 되돌림전문만들기(int32_t,int32_t,int32_t), 되돌림전문묶기(int32_t,int32_t,int32_t);
extern int32_t 되돌림전문보내기(int32_t,int32_t,int32_t,int32_t), 되돌림전문받기(int32_t,int32_t);
extern int32_t 되돌림전문접속번호(int32_t), 되돌림전문주소(int32_t), 되돌림전문상대(int32_t), 되돌림전문닫기(int32_t);
extern int32_t 자바전문넣기(int32_t,int32_t),자바전문얻기(int32_t);
extern int32_t 되돌림흐름만들기(void),되돌림흐름묶기(int32_t,int32_t,int32_t),되돌림흐름듣기(int32_t,int32_t);
extern int32_t 되돌림흐름연결(int32_t,int32_t,int32_t),되돌림흐름연결받기(int32_t),되돌림흐름읽기(int32_t,int32_t),되돌림흐름쓰기(int32_t,int32_t);
extern int32_t 되돌림흐름접속번호(int32_t),되돌림흐름상대(int32_t),되돌림흐름닫기(int32_t);
static int 외부연결[24];
static int 임의주소[24], 양쪽수신창구[24], 전문외부상대[8], 묶인주소[8];
static int 외부번호(int comhad_hanla) { return comhad_hanla>=32 && comhad_hanla<56 ? 외부연결[comhad_hanla-32]-1 : -1; }
static int greamaigh_SMS(int comhad_hanla,int TYPE_catagóir) {
    if(comhad_hanla<32||comhad_hanla>=56)return -9;int 이전=외부번호(comhad_hanla);if(이전>=0)return 이전;
    int mír_COUNT=통신끝점만들기(TYPE_catagóir);if(mír_COUNT>=0)외부연결[comhad_hanla-32]=mír_COUNT+1;return mír_COUNT;
}
int32_t 자바전문만들기(int32_t 첫째값,int32_t SECOND_VALUE,int32_t pointe_cóid){return 되돌림전문만들기(첫째값,SECOND_VALUE,pointe_cóid);}
int32_t 자바전문묶기(int32_t comhad_hanla,int32_t seoladh_Idirlín,int32_t uimhir_phoirt){
    if(seoladh_Idirlín==0x7f000001)return 되돌림전문묶기(comhad_hanla,seoladh_Idirlín,uimhir_phoirt);
    if(seoladh_Idirlín!=0&&seoladh_Idirlín!=망상태읽기(0,0))return -99;
    int 반환값=되돌림전문묶기(comhad_hanla,0,uimhir_phoirt);if(반환값<0)return 반환값;
    int mír_COUNT=greamaigh_SMS(comhad_hanla,2);if(mír_COUNT<0)return mír_COUNT;반환값=망주소묶기(mír_COUNT,망상태읽기(0,0),되돌림전문접속번호(comhad_hanla));if(!반환값)묶인주소[comhad_hanla-32]=seoladh_Idirlín;return 반환값;
}
int32_t 자바전문보내기(int32_t comhad_hanla,int32_t seoladh_Idirlín,int32_t uimhir_phoirt,int32_t Méid){
    if(seoladh_Idirlín==0x7f000001)return 되돌림전문보내기(comhad_hanla,seoladh_Idirlín,uimhir_phoirt,Méid);
    if(Méid<0||Méid>512)return -90;if(uimhir_phoirt<1||uimhir_phoirt>65535)return -22;
    if(되돌림전문접속번호(comhad_hanla)<0)return -9;
    if(되돌림전문주소(comhad_hanla)==0x7f000001)return -101;
    int mír_COUNT=외부번호(comhad_hanla);if(mír_COUNT<0){int 반환값=0;if(되돌림전문접속번호(comhad_hanla)==0)반환값=되돌림전문묶기(comhad_hanla,0,0);if(반환값<0)return 반환값;mír_COUNT=greamaigh_SMS(comhad_hanla,2);if(mír_COUNT<0)return mír_COUNT;반환값=망주소묶기(mír_COUNT,망상태읽기(0,0),되돌림전문접속번호(comhad_hanla));if(반환값<0)return 반환값;}
    unsigned char sonraí[512];for(int 순번=0;순번<Méid;순번++)sonraí[순번]=자바전문얻기(순번);return 전문보내기(mír_COUNT,sonraí,Méid,seoladh_Idirlín,uimhir_phoirt);
}
int32_t 자바전문받기(int32_t comhad_hanla,int32_t Méid){
    int mír_COUNT=외부번호(comhad_hanla);if(mír_COUNT<0)return 되돌림전문받기(comhad_hanla,Méid);if(Méid<0||Méid>512)return -22;
    int logánta=되돌림전문받기(comhad_hanla,Méid);if(logánta!=-11){전문외부상대[comhad_hanla-32]=0;return logánta;}
    unsigned char sonraí[512];int 반환값=전문받기(mír_COUNT,sonraí,Méid);if(반환값>=0)전문외부상대[comhad_hanla-32]=1;for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,sonraí[순번]);return 반환값;
}
int32_t 자바전문접속번호(int32_t comhad_hanla){int mír_COUNT=외부번호(comhad_hanla);return mír_COUNT<0?되돌림전문접속번호(comhad_hanla):(int32_t)Líonra_uimhir_phoirt(mír_COUNT);}
int32_t 자바전문주소(int32_t comhad_hanla){return 외부번호(comhad_hanla)<0?되돌림전문주소(comhad_hanla):묶인주소[comhad_hanla-32];}
int32_t 자바전문상대(int32_t comhad_hanla){int mír_COUNT=외부번호(comhad_hanla);return mír_COUNT<0||!전문외부상대[comhad_hanla-32]?되돌림전문상대(comhad_hanla):(int32_t)piara_uimhir_phoirt(mír_COUNT);}
int32_t 자바전문원격주소(int32_t comhad_hanla){int mír_COUNT=외부번호(comhad_hanla);return mír_COUNT<0||!전문외부상대[comhad_hanla-32]?0x7f000001:(int32_t)상대통신주소(mír_COUNT);}
int32_t 자바전문닫기(int32_t comhad_hanla){int mír_COUNT=외부번호(comhad_hanla);if(mír_COUNT>=0){dún_Líonra(mír_COUNT);외부연결[comhad_hanla-32]=0;}if(comhad_hanla>=32&&comhad_hanla<40)전문외부상대[comhad_hanla-32]=묶인주소[comhad_hanla-32]=0;return 되돌림전문닫기(comhad_hanla);}
int32_t 자바흐름만들기(void){return 되돌림흐름만들기();}
int32_t 자바흐름묶기(int32_t comhad_hanla,int32_t seoladh_Idirlín,int32_t uimhir_phoirt){
    if(seoladh_Idirlín==0||seoladh_Idirlín==0x7f000001){int 반환값=되돌림흐름묶기(comhad_hanla,seoladh_Idirlín,uimhir_phoirt);if(!반환값)임의주소[comhad_hanla-32]=seoladh_Idirlín==0;return 반환값;}
    if(seoladh_Idirlín!=망상태읽기(0,0))return -99;int 반환값=되돌림흐름묶기(comhad_hanla,0,uimhir_phoirt);if(반환값<0)return 반환값;
    int mír_COUNT=greamaigh_SMS(comhad_hanla,1);return mír_COUNT<0?mír_COUNT:망주소묶기(mír_COUNT,seoladh_Idirlín,되돌림흐름접속번호(comhad_hanla));
}
int32_t 자바흐름듣기(int32_t comhad_hanla,int32_t 연결대기한도){
    int mír_COUNT=외부번호(comhad_hanla);if(mír_COUNT<0){int 반환값=되돌림흐름듣기(comhad_hanla,연결대기한도);if(반환값<0||!임의주소[comhad_hanla-32])return 반환값;
        mír_COUNT=greamaigh_SMS(comhad_hanla,1);if(mír_COUNT<0)return mír_COUNT;반환값=망주소묶기(mír_COUNT,망상태읽기(0,0),되돌림흐름접속번호(comhad_hanla));if(반환값<0)return 반환값;양쪽수신창구[comhad_hanla-32]=1;
    }return 연결대기한도<1?-22:연결기다리기(mír_COUNT);
}
int32_t 자바흐름연결(int32_t comhad_hanla,int32_t seoladh_Idirlín,int32_t uimhir_phoirt){
    if(seoladh_Idirlín==0x7f000001 && 외부번호(comhad_hanla)<0)return 되돌림흐름연결(comhad_hanla,seoladh_Idirlín,uimhir_phoirt);
    if(되돌림흐름접속번호(comhad_hanla)<0)return -9;int mír_COUNT=greamaigh_SMS(comhad_hanla,1);return mír_COUNT<0?mír_COUNT:망연결하기(mír_COUNT,seoladh_Idirlín,uimhir_phoirt);
}
int32_t 자바흐름연결받기(int32_t comhad_hanla){
    int mír_COUNT=외부번호(comhad_hanla);if(mír_COUNT<0)return 되돌림흐름연결받기(comhad_hanla);
    if(양쪽수신창구[comhad_hanla-32]){int logánta=되돌림흐름연결받기(comhad_hanla);if(logánta!=-11)return logánta;}
    int piara_VALUE=망연결받기(mír_COUNT);if(piara_VALUE<0)return piara_VALUE;
    int sprioc=되돌림흐름만들기();if(sprioc<0){dún_Líonra(piara_VALUE);return sprioc;}외부연결[sprioc-32]=piara_VALUE+1;return sprioc;
}
int32_t 자바흐름읽기(int32_t comhad_hanla,int32_t Méid){
    int mír_COUNT=외부번호(comhad_hanla);if(mír_COUNT<0)return 되돌림흐름읽기(comhad_hanla,Méid);if(Méid<0||Méid>512)return -22;
    unsigned char sonraí[512];int 반환값=통신읽기(mír_COUNT,sonraí,Méid);for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,sonraí[순번]);return 반환값;
}
int32_t 자바흐름쓰기(int32_t comhad_hanla,int32_t Méid){
    int mír_COUNT=외부번호(comhad_hanla);if(mír_COUNT<0)return 되돌림흐름쓰기(comhad_hanla,Méid);if(Méid<0||Méid>512)return -22;
    unsigned char sonraí[512];for(int 순번=0;순번<Méid;순번++)sonraí[순번]=자바전문얻기(순번);return 통신쓰기(mír_COUNT,sonraí,Méid);
}
int32_t 자바흐름접속번호(int32_t comhad_hanla){int mír_COUNT=외부번호(comhad_hanla);return mír_COUNT<0?되돌림흐름접속번호(comhad_hanla):(int32_t)Líonra_uimhir_phoirt(mír_COUNT);}
int32_t 자바흐름상대(int32_t comhad_hanla){int mír_COUNT=외부번호(comhad_hanla);return mír_COUNT<0?되돌림흐름상대(comhad_hanla):(int32_t)piara_uimhir_phoirt(mír_COUNT);}
int32_t 자바흐름주소(int32_t comhad_hanla){return 외부번호(comhad_hanla)<0?0x7f000001:양쪽수신창구[comhad_hanla-32]?0:망상태읽기(0,0);}
int32_t 자바흐름닫기(int32_t comhad_hanla){int mír_COUNT=외부번호(comhad_hanla);if(mír_COUNT>=0){dún_Líonra(mír_COUNT);외부연결[comhad_hanla-32]=0;}if(comhad_hanla>=40&&comhad_hanla<56)임의주소[comhad_hanla-32]=양쪽수신창구[comhad_hanla-32]=0;return 되돌림흐름닫기(comhad_hanla);}
