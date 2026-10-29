#include "../명명/기계연결이름.h"
/* Preserve the deterministic Java loopback endpoints; route external IPv4 to lwIP. */
#include "rangkaian_tindan.h"
extern int32_t 되돌림전문만들기(int32_t,int32_t,int32_t), 되돌림전문묶기(int32_t,int32_t,int32_t);
extern int32_t 되돌림전문보내기(int32_t,int32_t,int32_t,int32_t), 되돌림전문받기(int32_t,int32_t);
extern int32_t 되돌림전문접속번호(int32_t), 되돌림전문주소(int32_t), 되돌림전문상대(int32_t), 되돌림전문닫기(int32_t);
extern int32_t 자바전문넣기(int32_t,int32_t),자바전문얻기(int32_t);
extern int32_t 되돌림흐름만들기(void),되돌림흐름묶기(int32_t,int32_t,int32_t),되돌림흐름듣기(int32_t,int32_t);
extern int32_t 되돌림흐름연결(int32_t,int32_t,int32_t),되돌림흐름연결받기(int32_t),되돌림흐름읽기(int32_t,int32_t),되돌림흐름쓰기(int32_t,int32_t);
extern int32_t 되돌림흐름접속번호(int32_t),되돌림흐름상대(int32_t),되돌림흐름닫기(int32_t);
static int 외부연결[24];
static int 임의주소[24], 양쪽수신창구[24], 전문외부상대[8], sempadan_e_mel[8];
static int 외부번호(int fail_pemegang) { return fail_pemegang>=32 && fail_pemegang<56 ? 외부연결[fail_pemegang-32]-1 : -1; }
static int tampal_SMS(int fail_pemegang,int TYPE_bidang) {
    if(fail_pemegang<32||fail_pemegang>=56)return -9;int 이전=외부번호(fail_pemegang);if(이전>=0)return 이전;
    int item_COUNT=통신끝점만들기(TYPE_bidang);if(item_COUNT>=0)외부연결[fail_pemegang-32]=item_COUNT+1;return item_COUNT;
}
int32_t 자바전문만들기(int32_t 첫째값,int32_t SECOND_VALUE,int32_t titik_kod){return 되돌림전문만들기(첫째값,SECOND_VALUE,titik_kod);}
int32_t 자바전문묶기(int32_t fail_pemegang,int32_t alamat_Internet,int32_t nombor_port){
    if(alamat_Internet==0x7f000001)return 되돌림전문묶기(fail_pemegang,alamat_Internet,nombor_port);
    if(alamat_Internet!=0&&alamat_Internet!=망상태읽기(0,0))return -99;
    int 반환값=되돌림전문묶기(fail_pemegang,0,nombor_port);if(반환값<0)return 반환값;
    int item_COUNT=tampal_SMS(fail_pemegang,2);if(item_COUNT<0)return item_COUNT;반환값=망주소묶기(item_COUNT,망상태읽기(0,0),되돌림전문접속번호(fail_pemegang));if(!반환값)sempadan_e_mel[fail_pemegang-32]=alamat_Internet;return 반환값;
}
int32_t 자바전문보내기(int32_t fail_pemegang,int32_t alamat_Internet,int32_t nombor_port,int32_t Saiz){
    if(alamat_Internet==0x7f000001)return 되돌림전문보내기(fail_pemegang,alamat_Internet,nombor_port,Saiz);
    if(Saiz<0||Saiz>512)return -90;if(nombor_port<1||nombor_port>65535)return -22;
    if(되돌림전문접속번호(fail_pemegang)<0)return -9;
    if(되돌림전문주소(fail_pemegang)==0x7f000001)return -101;
    int item_COUNT=외부번호(fail_pemegang);if(item_COUNT<0){int 반환값=0;if(되돌림전문접속번호(fail_pemegang)==0)반환값=되돌림전문묶기(fail_pemegang,0,0);if(반환값<0)return 반환값;item_COUNT=tampal_SMS(fail_pemegang,2);if(item_COUNT<0)return item_COUNT;반환값=망주소묶기(item_COUNT,망상태읽기(0,0),되돌림전문접속번호(fail_pemegang));if(반환값<0)return 반환값;}
    unsigned char data[512];for(int 순번=0;순번<Saiz;순번++)data[순번]=자바전문얻기(순번);return 전문보내기(item_COUNT,data,Saiz,alamat_Internet,nombor_port);
}
int32_t 자바전문받기(int32_t fail_pemegang,int32_t Saiz){
    int item_COUNT=외부번호(fail_pemegang);if(item_COUNT<0)return 되돌림전문받기(fail_pemegang,Saiz);if(Saiz<0||Saiz>512)return -22;
    int setempat=되돌림전문받기(fail_pemegang,Saiz);if(setempat!=-11){전문외부상대[fail_pemegang-32]=0;return setempat;}
    unsigned char data[512];int 반환값=전문받기(item_COUNT,data,Saiz);if(반환값>=0)전문외부상대[fail_pemegang-32]=1;for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,data[순번]);return 반환값;
}
int32_t 자바전문접속번호(int32_t fail_pemegang){int item_COUNT=외부번호(fail_pemegang);return item_COUNT<0?되돌림전문접속번호(fail_pemegang):(int32_t)rangkaian_nombor_port(item_COUNT);}
int32_t 자바전문주소(int32_t fail_pemegang){return 외부번호(fail_pemegang)<0?되돌림전문주소(fail_pemegang):sempadan_e_mel[fail_pemegang-32];}
int32_t 자바전문상대(int32_t fail_pemegang){int item_COUNT=외부번호(fail_pemegang);return item_COUNT<0||!전문외부상대[fail_pemegang-32]?되돌림전문상대(fail_pemegang):(int32_t)rakan_nombor_port(item_COUNT);}
int32_t 자바전문원격주소(int32_t fail_pemegang){int item_COUNT=외부번호(fail_pemegang);return item_COUNT<0||!전문외부상대[fail_pemegang-32]?0x7f000001:(int32_t)상대통신주소(item_COUNT);}
int32_t 자바전문닫기(int32_t fail_pemegang){int item_COUNT=외부번호(fail_pemegang);if(item_COUNT>=0){Tutup_rangkaian(item_COUNT);외부연결[fail_pemegang-32]=0;}if(fail_pemegang>=32&&fail_pemegang<40)전문외부상대[fail_pemegang-32]=sempadan_e_mel[fail_pemegang-32]=0;return 되돌림전문닫기(fail_pemegang);}
int32_t 자바흐름만들기(void){return 되돌림흐름만들기();}
int32_t 자바흐름묶기(int32_t fail_pemegang,int32_t alamat_Internet,int32_t nombor_port){
    if(alamat_Internet==0||alamat_Internet==0x7f000001){int 반환값=되돌림흐름묶기(fail_pemegang,alamat_Internet,nombor_port);if(!반환값)임의주소[fail_pemegang-32]=alamat_Internet==0;return 반환값;}
    if(alamat_Internet!=망상태읽기(0,0))return -99;int 반환값=되돌림흐름묶기(fail_pemegang,0,nombor_port);if(반환값<0)return 반환값;
    int item_COUNT=tampal_SMS(fail_pemegang,1);return item_COUNT<0?item_COUNT:망주소묶기(item_COUNT,alamat_Internet,되돌림흐름접속번호(fail_pemegang));
}
int32_t 자바흐름듣기(int32_t fail_pemegang,int32_t tunggakan){
    int item_COUNT=외부번호(fail_pemegang);if(item_COUNT<0){int 반환값=되돌림흐름듣기(fail_pemegang,tunggakan);if(반환값<0||!임의주소[fail_pemegang-32])return 반환값;
        item_COUNT=tampal_SMS(fail_pemegang,1);if(item_COUNT<0)return item_COUNT;반환값=망주소묶기(item_COUNT,망상태읽기(0,0),되돌림흐름접속번호(fail_pemegang));if(반환값<0)return 반환값;양쪽수신창구[fail_pemegang-32]=1;
    }return tunggakan<1?-22:연결기다리기(item_COUNT);
}
int32_t 자바흐름연결(int32_t fail_pemegang,int32_t alamat_Internet,int32_t nombor_port){
    if(alamat_Internet==0x7f000001 && 외부번호(fail_pemegang)<0)return 되돌림흐름연결(fail_pemegang,alamat_Internet,nombor_port);
    if(되돌림흐름접속번호(fail_pemegang)<0)return -9;int item_COUNT=tampal_SMS(fail_pemegang,1);return item_COUNT<0?item_COUNT:망연결하기(item_COUNT,alamat_Internet,nombor_port);
}
int32_t 자바흐름연결받기(int32_t fail_pemegang){
    int item_COUNT=외부번호(fail_pemegang);if(item_COUNT<0)return 되돌림흐름연결받기(fail_pemegang);
    if(양쪽수신창구[fail_pemegang-32]){int setempat=되돌림흐름연결받기(fail_pemegang);if(setempat!=-11)return setempat;}
    int rakan_VALUE=망연결받기(item_COUNT);if(rakan_VALUE<0)return rakan_VALUE;
    int sasaran=되돌림흐름만들기();if(sasaran<0){Tutup_rangkaian(rakan_VALUE);return sasaran;}외부연결[sasaran-32]=rakan_VALUE+1;return sasaran;
}
int32_t 자바흐름읽기(int32_t fail_pemegang,int32_t Saiz){
    int item_COUNT=외부번호(fail_pemegang);if(item_COUNT<0)return 되돌림흐름읽기(fail_pemegang,Saiz);if(Saiz<0||Saiz>512)return -22;
    unsigned char data[512];int 반환값=통신읽기(item_COUNT,data,Saiz);for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,data[순번]);return 반환값;
}
int32_t 자바흐름쓰기(int32_t fail_pemegang,int32_t Saiz){
    int item_COUNT=외부번호(fail_pemegang);if(item_COUNT<0)return 되돌림흐름쓰기(fail_pemegang,Saiz);if(Saiz<0||Saiz>512)return -22;
    unsigned char data[512];for(int 순번=0;순번<Saiz;순번++)data[순번]=자바전문얻기(순번);return 통신쓰기(item_COUNT,data,Saiz);
}
int32_t 자바흐름접속번호(int32_t fail_pemegang){int item_COUNT=외부번호(fail_pemegang);return item_COUNT<0?되돌림흐름접속번호(fail_pemegang):(int32_t)rangkaian_nombor_port(item_COUNT);}
int32_t 자바흐름상대(int32_t fail_pemegang){int item_COUNT=외부번호(fail_pemegang);return item_COUNT<0?되돌림흐름상대(fail_pemegang):(int32_t)rakan_nombor_port(item_COUNT);}
int32_t 자바흐름주소(int32_t fail_pemegang){return 외부번호(fail_pemegang)<0?0x7f000001:양쪽수신창구[fail_pemegang-32]?0:망상태읽기(0,0);}
int32_t 자바흐름닫기(int32_t fail_pemegang){int item_COUNT=외부번호(fail_pemegang);if(item_COUNT>=0){Tutup_rangkaian(item_COUNT);외부연결[fail_pemegang-32]=0;}if(fail_pemegang>=40&&fail_pemegang<56)임의주소[fail_pemegang-32]=양쪽수신창구[fail_pemegang-32]=0;return 되돌림흐름닫기(fail_pemegang);}
