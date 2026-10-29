#include "../명명/기계연결이름.h"
/* Preserve the deterministic Java loopback endpoints; route external IPv4 to lwIP. */
#include "tīkls_kopa.h"
extern int32_t 되돌림전문만들기(int32_t,int32_t,int32_t), 되돌림전문묶기(int32_t,int32_t,int32_t);
extern int32_t 되돌림전문보내기(int32_t,int32_t,int32_t,int32_t), 되돌림전문받기(int32_t,int32_t);
extern int32_t 되돌림전문접속번호(int32_t), 되돌림전문주소(int32_t), 되돌림전문상대(int32_t), 되돌림전문닫기(int32_t);
extern int32_t 자바전문넣기(int32_t,int32_t),자바전문얻기(int32_t);
extern int32_t 되돌림흐름만들기(void),되돌림흐름묶기(int32_t,int32_t,int32_t),되돌림흐름듣기(int32_t,int32_t);
extern int32_t 되돌림흐름연결(int32_t,int32_t,int32_t),되돌림흐름연결받기(int32_t),되돌림흐름읽기(int32_t,int32_t),되돌림흐름쓰기(int32_t,int32_t);
extern int32_t 되돌림흐름접속번호(int32_t),되돌림흐름상대(int32_t),되돌림흐름닫기(int32_t);
static int ārējs[24];
static int 임의주소[24], 양쪽수신창구[24], UDP_ārējs_vienranga[8], robeža_adrese[8];
static int ārējs_numurs(int Fails_turis) { return Fails_turis>=32 && Fails_turis<56 ? ārējs[Fails_turis-32]-1 : -1; }
static int ielīmēt_SMS(int Fails_turis,int TYPE_joma) {
    if(Fails_turis<32||Fails_turis>=56)return -9;int 이전=ārējs_numurs(Fails_turis);if(이전>=0)return 이전;
    int krājums_COUNT=통신끝점만들기(TYPE_joma);if(krājums_COUNT>=0)ārējs[Fails_turis-32]=krājums_COUNT+1;return krājums_COUNT;
}
int32_t 자바전문만들기(int32_t 첫째값,int32_t SECOND_VALUE,int32_t koda_punkts){return 되돌림전문만들기(첫째값,SECOND_VALUE,koda_punkts);}
int32_t 자바전문묶기(int32_t Fails_turis,int32_t interneta_adrese,int32_t porta_numurs){
    if(interneta_adrese==0x7f000001)return 되돌림전문묶기(Fails_turis,interneta_adrese,porta_numurs);
    if(interneta_adrese!=0&&interneta_adrese!=망상태읽기(0,0))return -99;
    int 반환값=되돌림전문묶기(Fails_turis,0,porta_numurs);if(반환값<0)return 반환값;
    int krājums_COUNT=ielīmēt_SMS(Fails_turis,2);if(krājums_COUNT<0)return krājums_COUNT;반환값=NET_BIND(krājums_COUNT,망상태읽기(0,0),되돌림전문접속번호(Fails_turis));if(!반환값)robeža_adrese[Fails_turis-32]=interneta_adrese;return 반환값;
}
int32_t 자바전문보내기(int32_t Fails_turis,int32_t interneta_adrese,int32_t porta_numurs,int32_t Izmērs){
    if(interneta_adrese==0x7f000001)return 되돌림전문보내기(Fails_turis,interneta_adrese,porta_numurs,Izmērs);
    if(Izmērs<0||Izmērs>512)return -90;if(porta_numurs<1||porta_numurs>65535)return -22;
    if(되돌림전문접속번호(Fails_turis)<0)return -9;
    if(되돌림전문주소(Fails_turis)==0x7f000001)return -101;
    int krājums_COUNT=ārējs_numurs(Fails_turis);if(krājums_COUNT<0){int 반환값=0;if(되돌림전문접속번호(Fails_turis)==0)반환값=되돌림전문묶기(Fails_turis,0,0);if(반환값<0)return 반환값;krājums_COUNT=ielīmēt_SMS(Fails_turis,2);if(krājums_COUNT<0)return krājums_COUNT;반환값=NET_BIND(krājums_COUNT,망상태읽기(0,0),되돌림전문접속번호(Fails_turis));if(반환값<0)return 반환값;}
    unsigned char dati[512];for(int 순번=0;순번<Izmērs;순번++)dati[순번]=자바전문얻기(순번);return sūtīt_datogramma(krājums_COUNT,dati,Izmērs,interneta_adrese,porta_numurs);
}
int32_t 자바전문받기(int32_t Fails_turis,int32_t Izmērs){
    int krājums_COUNT=ārējs_numurs(Fails_turis);if(krājums_COUNT<0)return 되돌림전문받기(Fails_turis,Izmērs);if(Izmērs<0||Izmērs>512)return -22;
    int vietējs=되돌림전문받기(Fails_turis,Izmērs);if(vietējs!=-11){UDP_ārējs_vienranga[Fails_turis-32]=0;return vietējs;}
    unsigned char dati[512];int 반환값=saņemt_datogramma(krājums_COUNT,dati,Izmērs);if(반환값>=0)UDP_ārējs_vienranga[Fails_turis-32]=1;for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,dati[순번]);return 반환값;
}
int32_t 자바전문접속번호(int32_t Fails_turis){int krājums_COUNT=ārējs_numurs(Fails_turis);return krājums_COUNT<0?되돌림전문접속번호(Fails_turis):(int32_t)tīkls_porta_numurs(krājums_COUNT);}
int32_t 자바전문주소(int32_t Fails_turis){return ārējs_numurs(Fails_turis)<0?되돌림전문주소(Fails_turis):robeža_adrese[Fails_turis-32];}
int32_t 자바전문상대(int32_t Fails_turis){int krājums_COUNT=ārējs_numurs(Fails_turis);return krājums_COUNT<0||!UDP_ārējs_vienranga[Fails_turis-32]?되돌림전문상대(Fails_turis):(int32_t)vienranga_porta_numurs(krājums_COUNT);}
int32_t 자바전문원격주소(int32_t Fails_turis){int krājums_COUNT=ārējs_numurs(Fails_turis);return krājums_COUNT<0||!UDP_ārējs_vienranga[Fails_turis-32]?0x7f000001:(int32_t)NET_vienranga_adrese(krājums_COUNT);}
int32_t 자바전문닫기(int32_t Fails_turis){int krājums_COUNT=ārējs_numurs(Fails_turis);if(krājums_COUNT>=0){Aizvērt_tīkls(krājums_COUNT);ārējs[Fails_turis-32]=0;}if(Fails_turis>=32&&Fails_turis<40)UDP_ārējs_vienranga[Fails_turis-32]=robeža_adrese[Fails_turis-32]=0;return 되돌림전문닫기(Fails_turis);}
int32_t 자바흐름만들기(void){return 되돌림흐름만들기();}
int32_t 자바흐름묶기(int32_t Fails_turis,int32_t interneta_adrese,int32_t porta_numurs){
    if(interneta_adrese==0||interneta_adrese==0x7f000001){int 반환값=되돌림흐름묶기(Fails_turis,interneta_adrese,porta_numurs);if(!반환값)임의주소[Fails_turis-32]=interneta_adrese==0;return 반환값;}
    if(interneta_adrese!=망상태읽기(0,0))return -99;int 반환값=되돌림흐름묶기(Fails_turis,0,porta_numurs);if(반환값<0)return 반환값;
    int krājums_COUNT=ielīmēt_SMS(Fails_turis,1);return krājums_COUNT<0?krājums_COUNT:NET_BIND(krājums_COUNT,interneta_adrese,되돌림흐름접속번호(Fails_turis));
}
int32_t 자바흐름듣기(int32_t Fails_turis,int32_t 연결대기한도){
    int krājums_COUNT=ārējs_numurs(Fails_turis);if(krājums_COUNT<0){int 반환값=되돌림흐름듣기(Fails_turis,연결대기한도);if(반환값<0||!임의주소[Fails_turis-32])return 반환값;
        krājums_COUNT=ielīmēt_SMS(Fails_turis,1);if(krājums_COUNT<0)return krājums_COUNT;반환값=NET_BIND(krājums_COUNT,망상태읽기(0,0),되돌림흐름접속번호(Fails_turis));if(반환값<0)return 반환값;양쪽수신창구[Fails_turis-32]=1;
    }return 연결대기한도<1?-22:NET_klausīties(krājums_COUNT);
}
int32_t 자바흐름연결(int32_t Fails_turis,int32_t interneta_adrese,int32_t porta_numurs){
    if(interneta_adrese==0x7f000001 && ārējs_numurs(Fails_turis)<0)return 되돌림흐름연결(Fails_turis,interneta_adrese,porta_numurs);
    if(되돌림흐름접속번호(Fails_turis)<0)return -9;int krājums_COUNT=ielīmēt_SMS(Fails_turis,1);return krājums_COUNT<0?krājums_COUNT:NET_saziņa(krājums_COUNT,interneta_adrese,porta_numurs);
}
int32_t 자바흐름연결받기(int32_t Fails_turis){
    int krājums_COUNT=ārējs_numurs(Fails_turis);if(krājums_COUNT<0)return 되돌림흐름연결받기(Fails_turis);
    if(양쪽수신창구[Fails_turis-32]){int vietējs=되돌림흐름연결받기(Fails_turis);if(vietējs!=-11)return vietējs;}
    int vienranga_VALUE=NET_akceptēt(krājums_COUNT);if(vienranga_VALUE<0)return vienranga_VALUE;
    int mērķis=되돌림흐름만들기();if(mērķis<0){Aizvērt_tīkls(vienranga_VALUE);return mērķis;}ārējs[mērķis-32]=vienranga_VALUE+1;return mērķis;
}
int32_t 자바흐름읽기(int32_t Fails_turis,int32_t Izmērs){
    int krājums_COUNT=ārējs_numurs(Fails_turis);if(krājums_COUNT<0)return 되돌림흐름읽기(Fails_turis,Izmērs);if(Izmērs<0||Izmērs>512)return -22;
    unsigned char dati[512];int 반환값=통신읽기(krājums_COUNT,dati,Izmērs);for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,dati[순번]);return 반환값;
}
int32_t 자바흐름쓰기(int32_t Fails_turis,int32_t Izmērs){
    int krājums_COUNT=ārējs_numurs(Fails_turis);if(krājums_COUNT<0)return 되돌림흐름쓰기(Fails_turis,Izmērs);if(Izmērs<0||Izmērs>512)return -22;
    unsigned char dati[512];for(int 순번=0;순번<Izmērs;순번++)dati[순번]=자바전문얻기(순번);return NET_rakstīšana(krājums_COUNT,dati,Izmērs);
}
int32_t 자바흐름접속번호(int32_t Fails_turis){int krājums_COUNT=ārējs_numurs(Fails_turis);return krājums_COUNT<0?되돌림흐름접속번호(Fails_turis):(int32_t)tīkls_porta_numurs(krājums_COUNT);}
int32_t 자바흐름상대(int32_t Fails_turis){int krājums_COUNT=ārējs_numurs(Fails_turis);return krājums_COUNT<0?되돌림흐름상대(Fails_turis):(int32_t)vienranga_porta_numurs(krājums_COUNT);}
int32_t 자바흐름주소(int32_t Fails_turis){return ārējs_numurs(Fails_turis)<0?0x7f000001:양쪽수신창구[Fails_turis-32]?0:망상태읽기(0,0);}
int32_t 자바흐름닫기(int32_t Fails_turis){int krājums_COUNT=ārējs_numurs(Fails_turis);if(krājums_COUNT>=0){Aizvērt_tīkls(krājums_COUNT);ārējs[Fails_turis-32]=0;}if(Fails_turis>=40&&Fails_turis<56)임의주소[Fails_turis-32]=양쪽수신창구[Fails_turis-32]=0;return 되돌림흐름닫기(Fails_turis);}
