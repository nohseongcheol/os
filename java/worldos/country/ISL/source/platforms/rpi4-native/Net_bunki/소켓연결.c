#include "../명명/기계연결이름.h"
/* Preserve the deterministic Java loopback endpoints; route external IPv4 to lwIP. */
#include "Net_bunki.h"
extern int32_t 되돌림전문만들기(int32_t,int32_t,int32_t), 되돌림전문묶기(int32_t,int32_t,int32_t);
extern int32_t 되돌림전문보내기(int32_t,int32_t,int32_t,int32_t), 되돌림전문받기(int32_t,int32_t);
extern int32_t 되돌림전문접속번호(int32_t), 되돌림전문주소(int32_t), 되돌림전문상대(int32_t), 되돌림전문닫기(int32_t);
extern int32_t 자바전문넣기(int32_t,int32_t),자바전문얻기(int32_t);
extern int32_t 되돌림흐름만들기(void),되돌림흐름묶기(int32_t,int32_t,int32_t),되돌림흐름듣기(int32_t,int32_t);
extern int32_t 되돌림흐름연결(int32_t,int32_t,int32_t),되돌림흐름연결받기(int32_t),되돌림흐름읽기(int32_t,int32_t),되돌림흐름쓰기(int32_t,int32_t);
extern int32_t 되돌림흐름접속번호(int32_t),되돌림흐름상대(int32_t),되돌림흐름닫기(int32_t);
static int 외부연결[24];
static int 임의주소[24], 양쪽수신창구[24], 전문외부상대[8], 묶인주소[8];
static int 외부번호(int skrá_hald) { return skrá_hald>=32 && skrá_hald<56 ? 외부연결[skrá_hald-32]-1 : -1; }
static int líma_SMS(int skrá_hald,int TYPE_tegund) {
    if(skrá_hald<32||skrá_hald>=56)return -9;int 이전=외부번호(skrá_hald);if(이전>=0)return 이전;
    int vara_COUNT=통신끝점만들기(TYPE_tegund);if(vara_COUNT>=0)외부연결[skrá_hald-32]=vara_COUNT+1;return vara_COUNT;
}
int32_t 자바전문만들기(int32_t 첫째값,int32_t SECOND_VALUE,int32_t stafkóði){return 되돌림전문만들기(첫째값,SECOND_VALUE,stafkóði);}
int32_t 자바전문묶기(int32_t skrá_hald,int32_t veffang,int32_t tengisnúmer){
    if(veffang==0x7f000001)return 되돌림전문묶기(skrá_hald,veffang,tengisnúmer);
    if(veffang!=0&&veffang!=망상태읽기(0,0))return -99;
    int 반환값=되돌림전문묶기(skrá_hald,0,tengisnúmer);if(반환값<0)return 반환값;
    int vara_COUNT=líma_SMS(skrá_hald,2);if(vara_COUNT<0)return vara_COUNT;반환값=nettó_BIND(vara_COUNT,망상태읽기(0,0),되돌림전문접속번호(skrá_hald));if(!반환값)묶인주소[skrá_hald-32]=veffang;return 반환값;
}
int32_t 자바전문보내기(int32_t skrá_hald,int32_t veffang,int32_t tengisnúmer,int32_t Stærð){
    if(veffang==0x7f000001)return 되돌림전문보내기(skrá_hald,veffang,tengisnúmer,Stærð);
    if(Stærð<0||Stærð>512)return -90;if(tengisnúmer<1||tengisnúmer>65535)return -22;
    if(되돌림전문접속번호(skrá_hald)<0)return -9;
    if(되돌림전문주소(skrá_hald)==0x7f000001)return -101;
    int vara_COUNT=외부번호(skrá_hald);if(vara_COUNT<0){int 반환값=0;if(되돌림전문접속번호(skrá_hald)==0)반환값=되돌림전문묶기(skrá_hald,0,0);if(반환값<0)return 반환값;vara_COUNT=líma_SMS(skrá_hald,2);if(vara_COUNT<0)return vara_COUNT;반환값=nettó_BIND(vara_COUNT,망상태읽기(0,0),되돌림전문접속번호(skrá_hald));if(반환값<0)return 반환값;}
    unsigned char gögn[512];for(int 순번=0;순번<Stærð;순번++)gögn[순번]=자바전문얻기(순번);return 전문보내기(vara_COUNT,gögn,Stærð,veffang,tengisnúmer);
}
int32_t 자바전문받기(int32_t skrá_hald,int32_t Stærð){
    int vara_COUNT=외부번호(skrá_hald);if(vara_COUNT<0)return 되돌림전문받기(skrá_hald,Stærð);if(Stærð<0||Stærð>512)return -22;
    int staðbundið=되돌림전문받기(skrá_hald,Stærð);if(staðbundið!=-11){전문외부상대[skrá_hald-32]=0;return staðbundið;}
    unsigned char gögn[512];int 반환값=전문받기(vara_COUNT,gögn,Stærð);if(반환값>=0)전문외부상대[skrá_hald-32]=1;for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,gögn[순번]);return 반환값;
}
int32_t 자바전문접속번호(int32_t skrá_hald){int vara_COUNT=외부번호(skrá_hald);return vara_COUNT<0?되돌림전문접속번호(skrá_hald):(int32_t)Net_tengisnúmer(vara_COUNT);}
int32_t 자바전문주소(int32_t skrá_hald){return 외부번호(skrá_hald)<0?되돌림전문주소(skrá_hald):묶인주소[skrá_hald-32];}
int32_t 자바전문상대(int32_t skrá_hald){int vara_COUNT=외부번호(skrá_hald);return vara_COUNT<0||!전문외부상대[skrá_hald-32]?되돌림전문상대(skrá_hald):(int32_t)jafningi_tengisnúmer(vara_COUNT);}
int32_t 자바전문원격주소(int32_t skrá_hald){int vara_COUNT=외부번호(skrá_hald);return vara_COUNT<0||!전문외부상대[skrá_hald-32]?0x7f000001:(int32_t)nettó_jafningi_slóð(vara_COUNT);}
int32_t 자바전문닫기(int32_t skrá_hald){int vara_COUNT=외부번호(skrá_hald);if(vara_COUNT>=0){loka_Net(vara_COUNT);외부연결[skrá_hald-32]=0;}if(skrá_hald>=32&&skrá_hald<40)전문외부상대[skrá_hald-32]=묶인주소[skrá_hald-32]=0;return 되돌림전문닫기(skrá_hald);}
int32_t 자바흐름만들기(void){return 되돌림흐름만들기();}
int32_t 자바흐름묶기(int32_t skrá_hald,int32_t veffang,int32_t tengisnúmer){
    if(veffang==0||veffang==0x7f000001){int 반환값=되돌림흐름묶기(skrá_hald,veffang,tengisnúmer);if(!반환값)임의주소[skrá_hald-32]=veffang==0;return 반환값;}
    if(veffang!=망상태읽기(0,0))return -99;int 반환값=되돌림흐름묶기(skrá_hald,0,tengisnúmer);if(반환값<0)return 반환값;
    int vara_COUNT=líma_SMS(skrá_hald,1);return vara_COUNT<0?vara_COUNT:nettó_BIND(vara_COUNT,veffang,되돌림흐름접속번호(skrá_hald));
}
int32_t 자바흐름듣기(int32_t skrá_hald,int32_t 연결대기한도){
    int vara_COUNT=외부번호(skrá_hald);if(vara_COUNT<0){int 반환값=되돌림흐름듣기(skrá_hald,연결대기한도);if(반환값<0||!임의주소[skrá_hald-32])return 반환값;
        vara_COUNT=líma_SMS(skrá_hald,1);if(vara_COUNT<0)return vara_COUNT;반환값=nettó_BIND(vara_COUNT,망상태읽기(0,0),되돌림흐름접속번호(skrá_hald));if(반환값<0)return 반환값;양쪽수신창구[skrá_hald-32]=1;
    }return 연결대기한도<1?-22:nettó_hlusta(vara_COUNT);
}
int32_t 자바흐름연결(int32_t skrá_hald,int32_t veffang,int32_t tengisnúmer){
    if(veffang==0x7f000001 && 외부번호(skrá_hald)<0)return 되돌림흐름연결(skrá_hald,veffang,tengisnúmer);
    if(되돌림흐름접속번호(skrá_hald)<0)return -9;int vara_COUNT=líma_SMS(skrá_hald,1);return vara_COUNT<0?vara_COUNT:nettó_TENGJA(vara_COUNT,veffang,tengisnúmer);
}
int32_t 자바흐름연결받기(int32_t skrá_hald){
    int vara_COUNT=외부번호(skrá_hald);if(vara_COUNT<0)return 되돌림흐름연결받기(skrá_hald);
    if(양쪽수신창구[skrá_hald-32]){int staðbundið=되돌림흐름연결받기(skrá_hald);if(staðbundið!=-11)return staðbundið;}
    int jafningi_VALUE=nettó_samþykkja(vara_COUNT);if(jafningi_VALUE<0)return jafningi_VALUE;
    int markmið=되돌림흐름만들기();if(markmið<0){loka_Net(jafningi_VALUE);return markmið;}외부연결[markmið-32]=jafningi_VALUE+1;return markmið;
}
int32_t 자바흐름읽기(int32_t skrá_hald,int32_t Stærð){
    int vara_COUNT=외부번호(skrá_hald);if(vara_COUNT<0)return 되돌림흐름읽기(skrá_hald,Stærð);if(Stærð<0||Stærð>512)return -22;
    unsigned char gögn[512];int 반환값=통신읽기(vara_COUNT,gögn,Stærð);for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,gögn[순번]);return 반환값;
}
int32_t 자바흐름쓰기(int32_t skrá_hald,int32_t Stærð){
    int vara_COUNT=외부번호(skrá_hald);if(vara_COUNT<0)return 되돌림흐름쓰기(skrá_hald,Stærð);if(Stærð<0||Stærð>512)return -22;
    unsigned char gögn[512];for(int 순번=0;순번<Stærð;순번++)gögn[순번]=자바전문얻기(순번);return nettó_skrifa(vara_COUNT,gögn,Stærð);
}
int32_t 자바흐름접속번호(int32_t skrá_hald){int vara_COUNT=외부번호(skrá_hald);return vara_COUNT<0?되돌림흐름접속번호(skrá_hald):(int32_t)Net_tengisnúmer(vara_COUNT);}
int32_t 자바흐름상대(int32_t skrá_hald){int vara_COUNT=외부번호(skrá_hald);return vara_COUNT<0?되돌림흐름상대(skrá_hald):(int32_t)jafningi_tengisnúmer(vara_COUNT);}
int32_t 자바흐름주소(int32_t skrá_hald){return 외부번호(skrá_hald)<0?0x7f000001:양쪽수신창구[skrá_hald-32]?0:망상태읽기(0,0);}
int32_t 자바흐름닫기(int32_t skrá_hald){int vara_COUNT=외부번호(skrá_hald);if(vara_COUNT>=0){loka_Net(vara_COUNT);외부연결[skrá_hald-32]=0;}if(skrá_hald>=40&&skrá_hald<56)임의주소[skrá_hald-32]=양쪽수신창구[skrá_hald-32]=0;return 되돌림흐름닫기(skrá_hald);}
