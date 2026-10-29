#include "../명명/기계연결이름.h"
/* Preserve the deterministic Java loopback endpoints; route external IPv4 to lwIP. */
#include "xarxa_Pila.h"
extern int32_t 되돌림전문만들기(int32_t,int32_t,int32_t), 되돌림전문묶기(int32_t,int32_t,int32_t);
extern int32_t 되돌림전문보내기(int32_t,int32_t,int32_t,int32_t), 되돌림전문받기(int32_t,int32_t);
extern int32_t 되돌림전문접속번호(int32_t), 되돌림전문주소(int32_t), 되돌림전문상대(int32_t), 되돌림전문닫기(int32_t);
extern int32_t 자바전문넣기(int32_t,int32_t),자바전문얻기(int32_t);
extern int32_t 되돌림흐름만들기(void),되돌림흐름묶기(int32_t,int32_t,int32_t),되돌림흐름듣기(int32_t,int32_t);
extern int32_t 되돌림흐름연결(int32_t,int32_t,int32_t),되돌림흐름연결받기(int32_t),되돌림흐름읽기(int32_t,int32_t),되돌림흐름쓰기(int32_t,int32_t);
extern int32_t 되돌림흐름접속번호(int32_t),되돌림흐름상대(int32_t),되돌림흐름닫기(int32_t);
static int 외부연결[24];
static int 임의주소[24], 양쪽수신창구[24], UDP_extern_homòleg[8], 묶인주소[8];
static int 외부번호(int arxiu_control_7f4cdfd5) { return arxiu_control_7f4cdfd5>=32 && arxiu_control_7f4cdfd5<56 ? 외부연결[arxiu_control_7f4cdfd5-32]-1 : -1; }
static int enganxar_SMS(int arxiu_control_7f4cdfd5,int TIPUS_Categoria) {
    if(arxiu_control_7f4cdfd5<32||arxiu_control_7f4cdfd5>=56)return -9;int 이전=외부번호(arxiu_control_7f4cdfd5);if(이전>=0)return 이전;
    int element_COMPT=통신끝점만들기(TIPUS_Categoria);if(element_COMPT>=0)외부연결[arxiu_control_7f4cdfd5-32]=element_COMPT+1;return element_COMPT;
}
int32_t 자바전문만들기(int32_t 첫째값,int32_t SEGON_VALOR,int32_t codi_de_caràcter){return 되돌림전문만들기(첫째값,SEGON_VALOR,codi_de_caràcter);}
int32_t 자바전문묶기(int32_t arxiu_control_7f4cdfd5,int32_t adreça_d_Internet,int32_t número_de_port){
    if(adreça_d_Internet==0x7f000001)return 되돌림전문묶기(arxiu_control_7f4cdfd5,adreça_d_Internet,número_de_port);
    if(adreça_d_Internet!=0&&adreça_d_Internet!=tancar_xarxa_estat(0,0))return -99;
    int 반환값=되돌림전문묶기(arxiu_control_7f4cdfd5,0,número_de_port);if(반환값<0)return 반환값;
    int element_COMPT=enganxar_SMS(arxiu_control_7f4cdfd5,2);if(element_COMPT<0)return element_COMPT;반환값=망주소묶기(element_COMPT,tancar_xarxa_estat(0,0),되돌림전문접속번호(arxiu_control_7f4cdfd5));if(!반환값)묶인주소[arxiu_control_7f4cdfd5-32]=adreça_d_Internet;return 반환값;
}
int32_t 자바전문보내기(int32_t arxiu_control_7f4cdfd5,int32_t adreça_d_Internet,int32_t número_de_port,int32_t Mida){
    if(adreça_d_Internet==0x7f000001)return 되돌림전문보내기(arxiu_control_7f4cdfd5,adreça_d_Internet,número_de_port,Mida);
    if(Mida<0||Mida>512)return -90;if(número_de_port<1||número_de_port>65535)return -22;
    if(되돌림전문접속번호(arxiu_control_7f4cdfd5)<0)return -9;
    if(되돌림전문주소(arxiu_control_7f4cdfd5)==0x7f000001)return -101;
    int element_COMPT=외부번호(arxiu_control_7f4cdfd5);if(element_COMPT<0){int 반환값=0;if(되돌림전문접속번호(arxiu_control_7f4cdfd5)==0)반환값=되돌림전문묶기(arxiu_control_7f4cdfd5,0,0);if(반환값<0)return 반환값;element_COMPT=enganxar_SMS(arxiu_control_7f4cdfd5,2);if(element_COMPT<0)return element_COMPT;반환값=망주소묶기(element_COMPT,tancar_xarxa_estat(0,0),되돌림전문접속번호(arxiu_control_7f4cdfd5));if(반환값<0)return 반환값;}
    unsigned char dades[512];for(int 순번=0;순번<Mida;순번++)dades[순번]=자바전문얻기(순번);return 전문보내기(element_COMPT,dades,Mida,adreça_d_Internet,número_de_port);
}
int32_t 자바전문받기(int32_t arxiu_control_7f4cdfd5,int32_t Mida){
    int element_COMPT=외부번호(arxiu_control_7f4cdfd5);if(element_COMPT<0)return 되돌림전문받기(arxiu_control_7f4cdfd5,Mida);if(Mida<0||Mida>512)return -22;
    int local=되돌림전문받기(arxiu_control_7f4cdfd5,Mida);if(local!=-11){UDP_extern_homòleg[arxiu_control_7f4cdfd5-32]=0;return local;}
    unsigned char dades[512];int 반환값=전문받기(element_COMPT,dades,Mida);if(반환값>=0)UDP_extern_homòleg[arxiu_control_7f4cdfd5-32]=1;for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,dades[순번]);return 반환값;
}
int32_t 자바전문접속번호(int32_t arxiu_control_7f4cdfd5){int element_COMPT=외부번호(arxiu_control_7f4cdfd5);return element_COMPT<0?되돌림전문접속번호(arxiu_control_7f4cdfd5):(int32_t)xarxa_número_de_port(element_COMPT);}
int32_t 자바전문주소(int32_t arxiu_control_7f4cdfd5){return 외부번호(arxiu_control_7f4cdfd5)<0?되돌림전문주소(arxiu_control_7f4cdfd5):묶인주소[arxiu_control_7f4cdfd5-32];}
int32_t 자바전문상대(int32_t arxiu_control_7f4cdfd5){int element_COMPT=외부번호(arxiu_control_7f4cdfd5);return element_COMPT<0||!UDP_extern_homòleg[arxiu_control_7f4cdfd5-32]?되돌림전문상대(arxiu_control_7f4cdfd5):(int32_t)homòleg_número_de_port(element_COMPT);}
int32_t 자바전문원격주소(int32_t arxiu_control_7f4cdfd5){int element_COMPT=외부번호(arxiu_control_7f4cdfd5);return element_COMPT<0||!UDP_extern_homòleg[arxiu_control_7f4cdfd5-32]?0x7f000001:(int32_t)상대통신주소(element_COMPT);}
int32_t 자바전문닫기(int32_t arxiu_control_7f4cdfd5){int element_COMPT=외부번호(arxiu_control_7f4cdfd5);if(element_COMPT>=0){Tanca_xarxa(element_COMPT);외부연결[arxiu_control_7f4cdfd5-32]=0;}if(arxiu_control_7f4cdfd5>=32&&arxiu_control_7f4cdfd5<40)UDP_extern_homòleg[arxiu_control_7f4cdfd5-32]=묶인주소[arxiu_control_7f4cdfd5-32]=0;return 되돌림전문닫기(arxiu_control_7f4cdfd5);}
int32_t 자바흐름만들기(void){return 되돌림흐름만들기();}
int32_t 자바흐름묶기(int32_t arxiu_control_7f4cdfd5,int32_t adreça_d_Internet,int32_t número_de_port){
    if(adreça_d_Internet==0||adreça_d_Internet==0x7f000001){int 반환값=되돌림흐름묶기(arxiu_control_7f4cdfd5,adreça_d_Internet,número_de_port);if(!반환값)임의주소[arxiu_control_7f4cdfd5-32]=adreça_d_Internet==0;return 반환값;}
    if(adreça_d_Internet!=tancar_xarxa_estat(0,0))return -99;int 반환값=되돌림흐름묶기(arxiu_control_7f4cdfd5,0,número_de_port);if(반환값<0)return 반환값;
    int element_COMPT=enganxar_SMS(arxiu_control_7f4cdfd5,1);return element_COMPT<0?element_COMPT:망주소묶기(element_COMPT,adreça_d_Internet,되돌림흐름접속번호(arxiu_control_7f4cdfd5));
}
int32_t 자바흐름듣기(int32_t arxiu_control_7f4cdfd5,int32_t 연결대기한도){
    int element_COMPT=외부번호(arxiu_control_7f4cdfd5);if(element_COMPT<0){int 반환값=되돌림흐름듣기(arxiu_control_7f4cdfd5,연결대기한도);if(반환값<0||!임의주소[arxiu_control_7f4cdfd5-32])return 반환값;
        element_COMPT=enganxar_SMS(arxiu_control_7f4cdfd5,1);if(element_COMPT<0)return element_COMPT;반환값=망주소묶기(element_COMPT,tancar_xarxa_estat(0,0),되돌림흐름접속번호(arxiu_control_7f4cdfd5));if(반환값<0)return 반환값;양쪽수신창구[arxiu_control_7f4cdfd5-32]=1;
    }return 연결대기한도<1?-22:연결기다리기(element_COMPT);
}
int32_t 자바흐름연결(int32_t arxiu_control_7f4cdfd5,int32_t adreça_d_Internet,int32_t número_de_port){
    if(adreça_d_Internet==0x7f000001 && 외부번호(arxiu_control_7f4cdfd5)<0)return 되돌림흐름연결(arxiu_control_7f4cdfd5,adreça_d_Internet,número_de_port);
    if(되돌림흐름접속번호(arxiu_control_7f4cdfd5)<0)return -9;int element_COMPT=enganxar_SMS(arxiu_control_7f4cdfd5,1);return element_COMPT<0?element_COMPT:망연결하기(element_COMPT,adreça_d_Internet,número_de_port);
}
int32_t 자바흐름연결받기(int32_t arxiu_control_7f4cdfd5){
    int element_COMPT=외부번호(arxiu_control_7f4cdfd5);if(element_COMPT<0)return 되돌림흐름연결받기(arxiu_control_7f4cdfd5);
    if(양쪽수신창구[arxiu_control_7f4cdfd5-32]){int local=되돌림흐름연결받기(arxiu_control_7f4cdfd5);if(local!=-11)return local;}
    int homòleg_VALOR=망연결받기(element_COMPT);if(homòleg_VALOR<0)return homòleg_VALOR;
    int objectiu=되돌림흐름만들기();if(objectiu<0){Tanca_xarxa(homòleg_VALOR);return objectiu;}외부연결[objectiu-32]=homòleg_VALOR+1;return objectiu;
}
int32_t 자바흐름읽기(int32_t arxiu_control_7f4cdfd5,int32_t Mida){
    int element_COMPT=외부번호(arxiu_control_7f4cdfd5);if(element_COMPT<0)return 되돌림흐름읽기(arxiu_control_7f4cdfd5,Mida);if(Mida<0||Mida>512)return -22;
    unsigned char dades[512];int 반환값=통신읽기(element_COMPT,dades,Mida);for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,dades[순번]);return 반환값;
}
int32_t 자바흐름쓰기(int32_t arxiu_control_7f4cdfd5,int32_t Mida){
    int element_COMPT=외부번호(arxiu_control_7f4cdfd5);if(element_COMPT<0)return 되돌림흐름쓰기(arxiu_control_7f4cdfd5,Mida);if(Mida<0||Mida>512)return -22;
    unsigned char dades[512];for(int 순번=0;순번<Mida;순번++)dades[순번]=자바전문얻기(순번);return 통신쓰기(element_COMPT,dades,Mida);
}
int32_t 자바흐름접속번호(int32_t arxiu_control_7f4cdfd5){int element_COMPT=외부번호(arxiu_control_7f4cdfd5);return element_COMPT<0?되돌림흐름접속번호(arxiu_control_7f4cdfd5):(int32_t)xarxa_número_de_port(element_COMPT);}
int32_t 자바흐름상대(int32_t arxiu_control_7f4cdfd5){int element_COMPT=외부번호(arxiu_control_7f4cdfd5);return element_COMPT<0?되돌림흐름상대(arxiu_control_7f4cdfd5):(int32_t)homòleg_número_de_port(element_COMPT);}
int32_t 자바흐름주소(int32_t arxiu_control_7f4cdfd5){return 외부번호(arxiu_control_7f4cdfd5)<0?0x7f000001:양쪽수신창구[arxiu_control_7f4cdfd5-32]?0:tancar_xarxa_estat(0,0);}
int32_t 자바흐름닫기(int32_t arxiu_control_7f4cdfd5){int element_COMPT=외부번호(arxiu_control_7f4cdfd5);if(element_COMPT>=0){Tanca_xarxa(element_COMPT);외부연결[arxiu_control_7f4cdfd5-32]=0;}if(arxiu_control_7f4cdfd5>=40&&arxiu_control_7f4cdfd5<56)임의주소[arxiu_control_7f4cdfd5-32]=양쪽수신창구[arxiu_control_7f4cdfd5-32]=0;return 되돌림흐름닫기(arxiu_control_7f4cdfd5);}
