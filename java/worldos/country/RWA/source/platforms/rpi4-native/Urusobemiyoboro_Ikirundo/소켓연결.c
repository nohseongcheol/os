#include "../명명/기계연결이름.h"
/* Preserve the deterministic Java loopback endpoints; route external IPv4 to lwIP. */
#include "Urusobemiyoboro_Ikirundo.h"
extern int32_t 되돌림전문만들기(int32_t,int32_t,int32_t), 되돌림전문묶기(int32_t,int32_t,int32_t);
extern int32_t 되돌림전문보내기(int32_t,int32_t,int32_t,int32_t), 되돌림전문받기(int32_t,int32_t);
extern int32_t 되돌림전문접속번호(int32_t), 되돌림전문주소(int32_t), 되돌림전문상대(int32_t), 되돌림전문닫기(int32_t);
extern int32_t 자바전문넣기(int32_t,int32_t),자바전문얻기(int32_t);
extern int32_t 되돌림흐름만들기(void),되돌림흐름묶기(int32_t,int32_t,int32_t),되돌림흐름듣기(int32_t,int32_t);
extern int32_t 되돌림흐름연결(int32_t,int32_t,int32_t),되돌림흐름연결받기(int32_t),되돌림흐름읽기(int32_t,int32_t),되돌림흐름쓰기(int32_t,int32_t);
extern int32_t 되돌림흐름접속번호(int32_t),되돌림흐름상대(int32_t),되돌림흐름닫기(int32_t);
static int 외부연결[24];
static int 임의주소[24], 양쪽수신창구[24], 전문외부상대[8], 묶인주소[8];
static int 외부번호(int dosiye_umukondo) { return dosiye_umukondo>=32 && dosiye_umukondo<56 ? 외부연결[dosiye_umukondo-32]-1 : -1; }
static int komeka_SMS(int dosiye_umukondo,int 유형) {
    if(dosiye_umukondo<32||dosiye_umukondo>=56)return -9;int 이전=외부번호(dosiye_umukondo);if(이전>=0)return 이전;
    int 개수=통신끝점만들기(유형);if(개수>=0)외부연결[dosiye_umukondo-32]=개수+1;return 개수;
}
int32_t 자바전문만들기(int32_t 첫째값,int32_t 둘째값,int32_t 문자값){return 되돌림전문만들기(첫째값,둘째값,문자값);}
int32_t 자바전문묶기(int32_t dosiye_umukondo,int32_t Aderesi_ya_Interineti,int32_t 접속번호){
    if(Aderesi_ya_Interineti==0x7f000001)return 되돌림전문묶기(dosiye_umukondo,Aderesi_ya_Interineti,접속번호);
    if(Aderesi_ya_Interineti!=0&&Aderesi_ya_Interineti!=망상태읽기(0,0))return -99;
    int 반환값=되돌림전문묶기(dosiye_umukondo,0,접속번호);if(반환값<0)return 반환값;
    int 개수=komeka_SMS(dosiye_umukondo,2);if(개수<0)return 개수;반환값=망주소묶기(개수,망상태읽기(0,0),되돌림전문접속번호(dosiye_umukondo));if(!반환값)묶인주소[dosiye_umukondo-32]=Aderesi_ya_Interineti;return 반환값;
}
int32_t 자바전문보내기(int32_t dosiye_umukondo,int32_t Aderesi_ya_Interineti,int32_t 접속번호,int32_t Ingano){
    if(Aderesi_ya_Interineti==0x7f000001)return 되돌림전문보내기(dosiye_umukondo,Aderesi_ya_Interineti,접속번호,Ingano);
    if(Ingano<0||Ingano>512)return -90;if(접속번호<1||접속번호>65535)return -22;
    if(되돌림전문접속번호(dosiye_umukondo)<0)return -9;
    if(되돌림전문주소(dosiye_umukondo)==0x7f000001)return -101;
    int 개수=외부번호(dosiye_umukondo);if(개수<0){int 반환값=0;if(되돌림전문접속번호(dosiye_umukondo)==0)반환값=되돌림전문묶기(dosiye_umukondo,0,0);if(반환값<0)return 반환값;개수=komeka_SMS(dosiye_umukondo,2);if(개수<0)return 개수;반환값=망주소묶기(개수,망상태읽기(0,0),되돌림전문접속번호(dosiye_umukondo));if(반환값<0)return 반환값;}
    unsigned char amakurushingiro[512];for(int 순번=0;순번<Ingano;순번++)amakurushingiro[순번]=자바전문얻기(순번);return 전문보내기(개수,amakurushingiro,Ingano,Aderesi_ya_Interineti,접속번호);
}
int32_t 자바전문받기(int32_t dosiye_umukondo,int32_t Ingano){
    int 개수=외부번호(dosiye_umukondo);if(개수<0)return 되돌림전문받기(dosiye_umukondo,Ingano);if(Ingano<0||Ingano>512)return -22;
    int mu_gace=되돌림전문받기(dosiye_umukondo,Ingano);if(mu_gace!=-11){전문외부상대[dosiye_umukondo-32]=0;return mu_gace;}
    unsigned char amakurushingiro[512];int 반환값=전문받기(개수,amakurushingiro,Ingano);if(반환값>=0)전문외부상대[dosiye_umukondo-32]=1;for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,amakurushingiro[순번]);return 반환값;
}
int32_t 자바전문접속번호(int32_t dosiye_umukondo){int 개수=외부번호(dosiye_umukondo);return 개수<0?되돌림전문접속번호(dosiye_umukondo):(int32_t)통신접속번호(개수);}
int32_t 자바전문주소(int32_t dosiye_umukondo){return 외부번호(dosiye_umukondo)<0?되돌림전문주소(dosiye_umukondo):묶인주소[dosiye_umukondo-32];}
int32_t 자바전문상대(int32_t dosiye_umukondo){int 개수=외부번호(dosiye_umukondo);return 개수<0||!전문외부상대[dosiye_umukondo-32]?되돌림전문상대(dosiye_umukondo):(int32_t)상대접속번호(개수);}
int32_t 자바전문원격주소(int32_t dosiye_umukondo){int 개수=외부번호(dosiye_umukondo);return 개수<0||!전문외부상대[dosiye_umukondo-32]?0x7f000001:(int32_t)상대통신주소(개수);}
int32_t 자바전문닫기(int32_t dosiye_umukondo){int 개수=외부번호(dosiye_umukondo);if(개수>=0){gufunga_Urusobemiyoboro(개수);외부연결[dosiye_umukondo-32]=0;}if(dosiye_umukondo>=32&&dosiye_umukondo<40)전문외부상대[dosiye_umukondo-32]=묶인주소[dosiye_umukondo-32]=0;return 되돌림전문닫기(dosiye_umukondo);}
int32_t 자바흐름만들기(void){return 되돌림흐름만들기();}
int32_t 자바흐름묶기(int32_t dosiye_umukondo,int32_t Aderesi_ya_Interineti,int32_t 접속번호){
    if(Aderesi_ya_Interineti==0||Aderesi_ya_Interineti==0x7f000001){int 반환값=되돌림흐름묶기(dosiye_umukondo,Aderesi_ya_Interineti,접속번호);if(!반환값)임의주소[dosiye_umukondo-32]=Aderesi_ya_Interineti==0;return 반환값;}
    if(Aderesi_ya_Interineti!=망상태읽기(0,0))return -99;int 반환값=되돌림흐름묶기(dosiye_umukondo,0,접속번호);if(반환값<0)return 반환값;
    int 개수=komeka_SMS(dosiye_umukondo,1);return 개수<0?개수:망주소묶기(개수,Aderesi_ya_Interineti,되돌림흐름접속번호(dosiye_umukondo));
}
int32_t 자바흐름듣기(int32_t dosiye_umukondo,int32_t 연결대기한도){
    int 개수=외부번호(dosiye_umukondo);if(개수<0){int 반환값=되돌림흐름듣기(dosiye_umukondo,연결대기한도);if(반환값<0||!임의주소[dosiye_umukondo-32])return 반환값;
        개수=komeka_SMS(dosiye_umukondo,1);if(개수<0)return 개수;반환값=망주소묶기(개수,망상태읽기(0,0),되돌림흐름접속번호(dosiye_umukondo));if(반환값<0)return 반환값;양쪽수신창구[dosiye_umukondo-32]=1;
    }return 연결대기한도<1?-22:연결기다리기(개수);
}
int32_t 자바흐름연결(int32_t dosiye_umukondo,int32_t Aderesi_ya_Interineti,int32_t 접속번호){
    if(Aderesi_ya_Interineti==0x7f000001 && 외부번호(dosiye_umukondo)<0)return 되돌림흐름연결(dosiye_umukondo,Aderesi_ya_Interineti,접속번호);
    if(되돌림흐름접속번호(dosiye_umukondo)<0)return -9;int 개수=komeka_SMS(dosiye_umukondo,1);return 개수<0?개수:망연결하기(개수,Aderesi_ya_Interineti,접속번호);
}
int32_t 자바흐름연결받기(int32_t dosiye_umukondo){
    int 개수=외부번호(dosiye_umukondo);if(개수<0)return 되돌림흐름연결받기(dosiye_umukondo);
    if(양쪽수신창구[dosiye_umukondo-32]){int mu_gace=되돌림흐름연결받기(dosiye_umukondo);if(mu_gace!=-11)return mu_gace;}
    int Mugenzi_agaciro=망연결받기(개수);if(Mugenzi_agaciro<0)return Mugenzi_agaciro;
    int gusimbuza_igishya=되돌림흐름만들기();if(gusimbuza_igishya<0){gufunga_Urusobemiyoboro(Mugenzi_agaciro);return gusimbuza_igishya;}외부연결[gusimbuza_igishya-32]=Mugenzi_agaciro+1;return gusimbuza_igishya;
}
int32_t 자바흐름읽기(int32_t dosiye_umukondo,int32_t Ingano){
    int 개수=외부번호(dosiye_umukondo);if(개수<0)return 되돌림흐름읽기(dosiye_umukondo,Ingano);if(Ingano<0||Ingano>512)return -22;
    unsigned char amakurushingiro[512];int 반환값=통신읽기(개수,amakurushingiro,Ingano);for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,amakurushingiro[순번]);return 반환값;
}
int32_t 자바흐름쓰기(int32_t dosiye_umukondo,int32_t Ingano){
    int 개수=외부번호(dosiye_umukondo);if(개수<0)return 되돌림흐름쓰기(dosiye_umukondo,Ingano);if(Ingano<0||Ingano>512)return -22;
    unsigned char amakurushingiro[512];for(int 순번=0;순번<Ingano;순번++)amakurushingiro[순번]=자바전문얻기(순번);return 통신쓰기(개수,amakurushingiro,Ingano);
}
int32_t 자바흐름접속번호(int32_t dosiye_umukondo){int 개수=외부번호(dosiye_umukondo);return 개수<0?되돌림흐름접속번호(dosiye_umukondo):(int32_t)통신접속번호(개수);}
int32_t 자바흐름상대(int32_t dosiye_umukondo){int 개수=외부번호(dosiye_umukondo);return 개수<0?되돌림흐름상대(dosiye_umukondo):(int32_t)상대접속번호(개수);}
int32_t 자바흐름주소(int32_t dosiye_umukondo){return 외부번호(dosiye_umukondo)<0?0x7f000001:양쪽수신창구[dosiye_umukondo-32]?0:망상태읽기(0,0);}
int32_t 자바흐름닫기(int32_t dosiye_umukondo){int 개수=외부번호(dosiye_umukondo);if(개수>=0){gufunga_Urusobemiyoboro(개수);외부연결[dosiye_umukondo-32]=0;}if(dosiye_umukondo>=40&&dosiye_umukondo<56)임의주소[dosiye_umukondo-32]=양쪽수신창구[dosiye_umukondo-32]=0;return 되돌림흐름닫기(dosiye_umukondo);}
