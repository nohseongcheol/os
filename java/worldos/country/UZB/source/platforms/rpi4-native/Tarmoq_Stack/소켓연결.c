#include "../명명/기계연결이름.h"
/* Preserve the deterministic Java loopback endpoints; route external IPv4 to lwIP. */
#include "Tarmoq_Stack.h"
extern int32_t 되돌림전문만들기(int32_t,int32_t,int32_t), 되돌림전문묶기(int32_t,int32_t,int32_t);
extern int32_t 되돌림전문보내기(int32_t,int32_t,int32_t,int32_t), 되돌림전문받기(int32_t,int32_t);
extern int32_t 되돌림전문접속번호(int32_t), 되돌림전문주소(int32_t), 되돌림전문상대(int32_t), 되돌림전문닫기(int32_t);
extern int32_t 자바전문넣기(int32_t,int32_t),자바전문얻기(int32_t);
extern int32_t 되돌림흐름만들기(void),되돌림흐름묶기(int32_t,int32_t,int32_t),되돌림흐름듣기(int32_t,int32_t);
extern int32_t 되돌림흐름연결(int32_t,int32_t,int32_t),되돌림흐름연결받기(int32_t),되돌림흐름읽기(int32_t,int32_t),되돌림흐름쓰기(int32_t,int32_t);
extern int32_t 되돌림흐름접속번호(int32_t),되돌림흐름상대(int32_t),되돌림흐름닫기(int32_t);
static int 외부연결[24];
static int 임의주소[24], 양쪽수신창구[24], 전문외부상대[8], 묶인주소[8];
static int 외부번호(int fayl_deskriptor) { return fayl_deskriptor>=32 && fayl_deskriptor<56 ? 외부연결[fayl_deskriptor-32]-1 : -1; }
static int qo_shib_qo_ymoq_SMS(int fayl_deskriptor,int TYPE_toifa) {
    if(fayl_deskriptor<32||fayl_deskriptor>=56)return -9;int 이전=외부번호(fayl_deskriptor);if(이전>=0)return 이전;
    int element_COUNT=통신끝점만들기(TYPE_toifa);if(element_COUNT>=0)외부연결[fayl_deskriptor-32]=element_COUNT+1;return element_COUNT;
}
int32_t 자바전문만들기(int32_t 첫째값,int32_t SECOND_VALUE,int32_t belgi_kodi){return 되돌림전문만들기(첫째값,SECOND_VALUE,belgi_kodi);}
int32_t 자바전문묶기(int32_t fayl_deskriptor,int32_t Internetdagi_manzil,int32_t 접속번호){
    if(Internetdagi_manzil==0x7f000001)return 되돌림전문묶기(fayl_deskriptor,Internetdagi_manzil,접속번호);
    if(Internetdagi_manzil!=0&&Internetdagi_manzil!=망상태읽기(0,0))return -99;
    int 반환값=되돌림전문묶기(fayl_deskriptor,0,접속번호);if(반환값<0)return 반환값;
    int element_COUNT=qo_shib_qo_ymoq_SMS(fayl_deskriptor,2);if(element_COUNT<0)return element_COUNT;반환값=망주소묶기(element_COUNT,망상태읽기(0,0),되돌림전문접속번호(fayl_deskriptor));if(!반환값)묶인주소[fayl_deskriptor-32]=Internetdagi_manzil;return 반환값;
}
int32_t 자바전문보내기(int32_t fayl_deskriptor,int32_t Internetdagi_manzil,int32_t 접속번호,int32_t Hajmi){
    if(Internetdagi_manzil==0x7f000001)return 되돌림전문보내기(fayl_deskriptor,Internetdagi_manzil,접속번호,Hajmi);
    if(Hajmi<0||Hajmi>512)return -90;if(접속번호<1||접속번호>65535)return -22;
    if(되돌림전문접속번호(fayl_deskriptor)<0)return -9;
    if(되돌림전문주소(fayl_deskriptor)==0x7f000001)return -101;
    int element_COUNT=외부번호(fayl_deskriptor);if(element_COUNT<0){int 반환값=0;if(되돌림전문접속번호(fayl_deskriptor)==0)반환값=되돌림전문묶기(fayl_deskriptor,0,0);if(반환값<0)return 반환값;element_COUNT=qo_shib_qo_ymoq_SMS(fayl_deskriptor,2);if(element_COUNT<0)return element_COUNT;반환값=망주소묶기(element_COUNT,망상태읽기(0,0),되돌림전문접속번호(fayl_deskriptor));if(반환값<0)return 반환값;}
    unsigned char ma_lumotlar[512];for(int 순번=0;순번<Hajmi;순번++)ma_lumotlar[순번]=자바전문얻기(순번);return 전문보내기(element_COUNT,ma_lumotlar,Hajmi,Internetdagi_manzil,접속번호);
}
int32_t 자바전문받기(int32_t fayl_deskriptor,int32_t Hajmi){
    int element_COUNT=외부번호(fayl_deskriptor);if(element_COUNT<0)return 되돌림전문받기(fayl_deskriptor,Hajmi);if(Hajmi<0||Hajmi>512)return -22;
    int mahalliy=되돌림전문받기(fayl_deskriptor,Hajmi);if(mahalliy!=-11){전문외부상대[fayl_deskriptor-32]=0;return mahalliy;}
    unsigned char ma_lumotlar[512];int 반환값=전문받기(element_COUNT,ma_lumotlar,Hajmi);if(반환값>=0)전문외부상대[fayl_deskriptor-32]=1;for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,ma_lumotlar[순번]);return 반환값;
}
int32_t 자바전문접속번호(int32_t fayl_deskriptor){int element_COUNT=외부번호(fayl_deskriptor);return element_COUNT<0?되돌림전문접속번호(fayl_deskriptor):(int32_t)통신접속번호(element_COUNT);}
int32_t 자바전문주소(int32_t fayl_deskriptor){return 외부번호(fayl_deskriptor)<0?되돌림전문주소(fayl_deskriptor):묶인주소[fayl_deskriptor-32];}
int32_t 자바전문상대(int32_t fayl_deskriptor){int element_COUNT=외부번호(fayl_deskriptor);return element_COUNT<0||!전문외부상대[fayl_deskriptor-32]?되돌림전문상대(fayl_deskriptor):(int32_t)상대접속번호(element_COUNT);}
int32_t 자바전문원격주소(int32_t fayl_deskriptor){int element_COUNT=외부번호(fayl_deskriptor);return element_COUNT<0||!전문외부상대[fayl_deskriptor-32]?0x7f000001:(int32_t)상대통신주소(element_COUNT);}
int32_t 자바전문닫기(int32_t fayl_deskriptor){int element_COUNT=외부번호(fayl_deskriptor);if(element_COUNT>=0){yopmoq_Tarmoq(element_COUNT);외부연결[fayl_deskriptor-32]=0;}if(fayl_deskriptor>=32&&fayl_deskriptor<40)전문외부상대[fayl_deskriptor-32]=묶인주소[fayl_deskriptor-32]=0;return 되돌림전문닫기(fayl_deskriptor);}
int32_t 자바흐름만들기(void){return 되돌림흐름만들기();}
int32_t 자바흐름묶기(int32_t fayl_deskriptor,int32_t Internetdagi_manzil,int32_t 접속번호){
    if(Internetdagi_manzil==0||Internetdagi_manzil==0x7f000001){int 반환값=되돌림흐름묶기(fayl_deskriptor,Internetdagi_manzil,접속번호);if(!반환값)임의주소[fayl_deskriptor-32]=Internetdagi_manzil==0;return 반환값;}
    if(Internetdagi_manzil!=망상태읽기(0,0))return -99;int 반환값=되돌림흐름묶기(fayl_deskriptor,0,접속번호);if(반환값<0)return 반환값;
    int element_COUNT=qo_shib_qo_ymoq_SMS(fayl_deskriptor,1);return element_COUNT<0?element_COUNT:망주소묶기(element_COUNT,Internetdagi_manzil,되돌림흐름접속번호(fayl_deskriptor));
}
int32_t 자바흐름듣기(int32_t fayl_deskriptor,int32_t 연결대기한도){
    int element_COUNT=외부번호(fayl_deskriptor);if(element_COUNT<0){int 반환값=되돌림흐름듣기(fayl_deskriptor,연결대기한도);if(반환값<0||!임의주소[fayl_deskriptor-32])return 반환값;
        element_COUNT=qo_shib_qo_ymoq_SMS(fayl_deskriptor,1);if(element_COUNT<0)return element_COUNT;반환값=망주소묶기(element_COUNT,망상태읽기(0,0),되돌림흐름접속번호(fayl_deskriptor));if(반환값<0)return 반환값;양쪽수신창구[fayl_deskriptor-32]=1;
    }return 연결대기한도<1?-22:연결기다리기(element_COUNT);
}
int32_t 자바흐름연결(int32_t fayl_deskriptor,int32_t Internetdagi_manzil,int32_t 접속번호){
    if(Internetdagi_manzil==0x7f000001 && 외부번호(fayl_deskriptor)<0)return 되돌림흐름연결(fayl_deskriptor,Internetdagi_manzil,접속번호);
    if(되돌림흐름접속번호(fayl_deskriptor)<0)return -9;int element_COUNT=qo_shib_qo_ymoq_SMS(fayl_deskriptor,1);return element_COUNT<0?element_COUNT:망연결하기(element_COUNT,Internetdagi_manzil,접속번호);
}
int32_t 자바흐름연결받기(int32_t fayl_deskriptor){
    int element_COUNT=외부번호(fayl_deskriptor);if(element_COUNT<0)return 되돌림흐름연결받기(fayl_deskriptor);
    if(양쪽수신창구[fayl_deskriptor-32]){int mahalliy=되돌림흐름연결받기(fayl_deskriptor);if(mahalliy!=-11)return mahalliy;}
    int bir_rangli_VALUE=망연결받기(element_COUNT);if(bir_rangli_VALUE<0)return bir_rangli_VALUE;
    int nishon=되돌림흐름만들기();if(nishon<0){yopmoq_Tarmoq(bir_rangli_VALUE);return nishon;}외부연결[nishon-32]=bir_rangli_VALUE+1;return nishon;
}
int32_t 자바흐름읽기(int32_t fayl_deskriptor,int32_t Hajmi){
    int element_COUNT=외부번호(fayl_deskriptor);if(element_COUNT<0)return 되돌림흐름읽기(fayl_deskriptor,Hajmi);if(Hajmi<0||Hajmi>512)return -22;
    unsigned char ma_lumotlar[512];int 반환값=통신읽기(element_COUNT,ma_lumotlar,Hajmi);for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,ma_lumotlar[순번]);return 반환값;
}
int32_t 자바흐름쓰기(int32_t fayl_deskriptor,int32_t Hajmi){
    int element_COUNT=외부번호(fayl_deskriptor);if(element_COUNT<0)return 되돌림흐름쓰기(fayl_deskriptor,Hajmi);if(Hajmi<0||Hajmi>512)return -22;
    unsigned char ma_lumotlar[512];for(int 순번=0;순번<Hajmi;순번++)ma_lumotlar[순번]=자바전문얻기(순번);return 통신쓰기(element_COUNT,ma_lumotlar,Hajmi);
}
int32_t 자바흐름접속번호(int32_t fayl_deskriptor){int element_COUNT=외부번호(fayl_deskriptor);return element_COUNT<0?되돌림흐름접속번호(fayl_deskriptor):(int32_t)통신접속번호(element_COUNT);}
int32_t 자바흐름상대(int32_t fayl_deskriptor){int element_COUNT=외부번호(fayl_deskriptor);return element_COUNT<0?되돌림흐름상대(fayl_deskriptor):(int32_t)상대접속번호(element_COUNT);}
int32_t 자바흐름주소(int32_t fayl_deskriptor){return 외부번호(fayl_deskriptor)<0?0x7f000001:양쪽수신창구[fayl_deskriptor-32]?0:망상태읽기(0,0);}
int32_t 자바흐름닫기(int32_t fayl_deskriptor){int element_COUNT=외부번호(fayl_deskriptor);if(element_COUNT>=0){yopmoq_Tarmoq(element_COUNT);외부연결[fayl_deskriptor-32]=0;}if(fayl_deskriptor>=40&&fayl_deskriptor<56)임의주소[fayl_deskriptor-32]=양쪽수신창구[fayl_deskriptor-32]=0;return 되돌림흐름닫기(fayl_deskriptor);}
