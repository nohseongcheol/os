#include "../명명/기계연결이름.h"
/* Preserve the deterministic Java loopback endpoints; route external IPv4 to lwIP. */
#include "Rede_Montón.h"
extern int32_t 되돌림전문만들기(int32_t,int32_t,int32_t), 되돌림전문묶기(int32_t,int32_t,int32_t);
extern int32_t 되돌림전문보내기(int32_t,int32_t,int32_t,int32_t), 되돌림전문받기(int32_t,int32_t);
extern int32_t 되돌림전문접속번호(int32_t), 되돌림전문주소(int32_t), 되돌림전문상대(int32_t), 되돌림전문닫기(int32_t);
extern int32_t 자바전문넣기(int32_t,int32_t),자바전문얻기(int32_t);
extern int32_t 되돌림흐름만들기(void),되돌림흐름묶기(int32_t,int32_t,int32_t),되돌림흐름듣기(int32_t,int32_t);
extern int32_t 되돌림흐름연결(int32_t,int32_t,int32_t),되돌림흐름연결받기(int32_t),되돌림흐름읽기(int32_t,int32_t),되돌림흐름쓰기(int32_t,int32_t);
extern int32_t 되돌림흐름접속번호(int32_t),되돌림흐름상대(int32_t),되돌림흐름닫기(int32_t);
static int externo[24];
static int 임의주소[24], 양쪽수신창구[24], UDP_externo_punto[8], 묶인주소[8];
static int 외부번호(int Ficheiro_agarradoira) { return Ficheiro_agarradoira>=32 && Ficheiro_agarradoira<56 ? externo[Ficheiro_agarradoira-32]-1 : -1; }
static int pegar_SMS(int Ficheiro_agarradoira,int TIPO_Categoría) {
    if(Ficheiro_agarradoira<32||Ficheiro_agarradoira>=56)return -9;int 이전=외부번호(Ficheiro_agarradoira);if(이전>=0)return 이전;
    int elemento_CONTAR=통신끝점만들기(TIPO_Categoría);if(elemento_CONTAR>=0)externo[Ficheiro_agarradoira-32]=elemento_CONTAR+1;return elemento_CONTAR;
}
int32_t 자바전문만들기(int32_t 첫째값,int32_t SEGUNDO_VALOR,int32_t código_de_carácter){return 되돌림전문만들기(첫째값,SEGUNDO_VALOR,código_de_carácter);}
int32_t 자바전문묶기(int32_t Ficheiro_agarradoira,int32_t enderezo_de_internet,int32_t número_do_porto){
    if(enderezo_de_internet==0x7f000001)return 되돌림전문묶기(Ficheiro_agarradoira,enderezo_de_internet,número_do_porto);
    if(enderezo_de_internet!=0&&enderezo_de_internet!=망상태읽기(0,0))return -99;
    int 반환값=되돌림전문묶기(Ficheiro_agarradoira,0,número_do_porto);if(반환값<0)return 반환값;
    int elemento_CONTAR=pegar_SMS(Ficheiro_agarradoira,2);if(elemento_CONTAR<0)return elemento_CONTAR;반환값=망주소묶기(elemento_CONTAR,망상태읽기(0,0),되돌림전문접속번호(Ficheiro_agarradoira));if(!반환값)묶인주소[Ficheiro_agarradoira-32]=enderezo_de_internet;return 반환값;
}
int32_t 자바전문보내기(int32_t Ficheiro_agarradoira,int32_t enderezo_de_internet,int32_t número_do_porto,int32_t Tamaño){
    if(enderezo_de_internet==0x7f000001)return 되돌림전문보내기(Ficheiro_agarradoira,enderezo_de_internet,número_do_porto,Tamaño);
    if(Tamaño<0||Tamaño>512)return -90;if(número_do_porto<1||número_do_porto>65535)return -22;
    if(되돌림전문접속번호(Ficheiro_agarradoira)<0)return -9;
    if(되돌림전문주소(Ficheiro_agarradoira)==0x7f000001)return -101;
    int elemento_CONTAR=외부번호(Ficheiro_agarradoira);if(elemento_CONTAR<0){int 반환값=0;if(되돌림전문접속번호(Ficheiro_agarradoira)==0)반환값=되돌림전문묶기(Ficheiro_agarradoira,0,0);if(반환값<0)return 반환값;elemento_CONTAR=pegar_SMS(Ficheiro_agarradoira,2);if(elemento_CONTAR<0)return elemento_CONTAR;반환값=망주소묶기(elemento_CONTAR,망상태읽기(0,0),되돌림전문접속번호(Ficheiro_agarradoira));if(반환값<0)return 반환값;}
    unsigned char datos[512];for(int 순번=0;순번<Tamaño;순번++)datos[순번]=자바전문얻기(순번);return 전문보내기(elemento_CONTAR,datos,Tamaño,enderezo_de_internet,número_do_porto);
}
int32_t 자바전문받기(int32_t Ficheiro_agarradoira,int32_t Tamaño){
    int elemento_CONTAR=외부번호(Ficheiro_agarradoira);if(elemento_CONTAR<0)return 되돌림전문받기(Ficheiro_agarradoira,Tamaño);if(Tamaño<0||Tamaño>512)return -22;
    int local=되돌림전문받기(Ficheiro_agarradoira,Tamaño);if(local!=-11){UDP_externo_punto[Ficheiro_agarradoira-32]=0;return local;}
    unsigned char datos[512];int 반환값=전문받기(elemento_CONTAR,datos,Tamaño);if(반환값>=0)UDP_externo_punto[Ficheiro_agarradoira-32]=1;for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,datos[순번]);return 반환값;
}
int32_t 자바전문접속번호(int32_t Ficheiro_agarradoira){int elemento_CONTAR=외부번호(Ficheiro_agarradoira);return elemento_CONTAR<0?되돌림전문접속번호(Ficheiro_agarradoira):(int32_t)Rede_número_do_porto(elemento_CONTAR);}
int32_t 자바전문주소(int32_t Ficheiro_agarradoira){return 외부번호(Ficheiro_agarradoira)<0?되돌림전문주소(Ficheiro_agarradoira):묶인주소[Ficheiro_agarradoira-32];}
int32_t 자바전문상대(int32_t Ficheiro_agarradoira){int elemento_CONTAR=외부번호(Ficheiro_agarradoira);return elemento_CONTAR<0||!UDP_externo_punto[Ficheiro_agarradoira-32]?되돌림전문상대(Ficheiro_agarradoira):(int32_t)punto_número_do_porto(elemento_CONTAR);}
int32_t 자바전문원격주소(int32_t Ficheiro_agarradoira){int elemento_CONTAR=외부번호(Ficheiro_agarradoira);return elemento_CONTAR<0||!UDP_externo_punto[Ficheiro_agarradoira-32]?0x7f000001:(int32_t)상대통신주소(elemento_CONTAR);}
int32_t 자바전문닫기(int32_t Ficheiro_agarradoira){int elemento_CONTAR=외부번호(Ficheiro_agarradoira);if(elemento_CONTAR>=0){peche_Rede(elemento_CONTAR);externo[Ficheiro_agarradoira-32]=0;}if(Ficheiro_agarradoira>=32&&Ficheiro_agarradoira<40)UDP_externo_punto[Ficheiro_agarradoira-32]=묶인주소[Ficheiro_agarradoira-32]=0;return 되돌림전문닫기(Ficheiro_agarradoira);}
int32_t 자바흐름만들기(void){return 되돌림흐름만들기();}
int32_t 자바흐름묶기(int32_t Ficheiro_agarradoira,int32_t enderezo_de_internet,int32_t número_do_porto){
    if(enderezo_de_internet==0||enderezo_de_internet==0x7f000001){int 반환값=되돌림흐름묶기(Ficheiro_agarradoira,enderezo_de_internet,número_do_porto);if(!반환값)임의주소[Ficheiro_agarradoira-32]=enderezo_de_internet==0;return 반환값;}
    if(enderezo_de_internet!=망상태읽기(0,0))return -99;int 반환값=되돌림흐름묶기(Ficheiro_agarradoira,0,número_do_porto);if(반환값<0)return 반환값;
    int elemento_CONTAR=pegar_SMS(Ficheiro_agarradoira,1);return elemento_CONTAR<0?elemento_CONTAR:망주소묶기(elemento_CONTAR,enderezo_de_internet,되돌림흐름접속번호(Ficheiro_agarradoira));
}
int32_t 자바흐름듣기(int32_t Ficheiro_agarradoira,int32_t 연결대기한도){
    int elemento_CONTAR=외부번호(Ficheiro_agarradoira);if(elemento_CONTAR<0){int 반환값=되돌림흐름듣기(Ficheiro_agarradoira,연결대기한도);if(반환값<0||!임의주소[Ficheiro_agarradoira-32])return 반환값;
        elemento_CONTAR=pegar_SMS(Ficheiro_agarradoira,1);if(elemento_CONTAR<0)return elemento_CONTAR;반환값=망주소묶기(elemento_CONTAR,망상태읽기(0,0),되돌림흐름접속번호(Ficheiro_agarradoira));if(반환값<0)return 반환값;양쪽수신창구[Ficheiro_agarradoira-32]=1;
    }return 연결대기한도<1?-22:연결기다리기(elemento_CONTAR);
}
int32_t 자바흐름연결(int32_t Ficheiro_agarradoira,int32_t enderezo_de_internet,int32_t número_do_porto){
    if(enderezo_de_internet==0x7f000001 && 외부번호(Ficheiro_agarradoira)<0)return 되돌림흐름연결(Ficheiro_agarradoira,enderezo_de_internet,número_do_porto);
    if(되돌림흐름접속번호(Ficheiro_agarradoira)<0)return -9;int elemento_CONTAR=pegar_SMS(Ficheiro_agarradoira,1);return elemento_CONTAR<0?elemento_CONTAR:망연결하기(elemento_CONTAR,enderezo_de_internet,número_do_porto);
}
int32_t 자바흐름연결받기(int32_t Ficheiro_agarradoira){
    int elemento_CONTAR=외부번호(Ficheiro_agarradoira);if(elemento_CONTAR<0)return 되돌림흐름연결받기(Ficheiro_agarradoira);
    if(양쪽수신창구[Ficheiro_agarradoira-32]){int local=되돌림흐름연결받기(Ficheiro_agarradoira);if(local!=-11)return local;}
    int punto_VALOR=망연결받기(elemento_CONTAR);if(punto_VALOR<0)return punto_VALOR;
    int obxectivo_VALOR=되돌림흐름만들기();if(obxectivo_VALOR<0){peche_Rede(punto_VALOR);return obxectivo_VALOR;}externo[obxectivo_VALOR-32]=punto_VALOR+1;return obxectivo_VALOR;
}
int32_t 자바흐름읽기(int32_t Ficheiro_agarradoira,int32_t Tamaño){
    int elemento_CONTAR=외부번호(Ficheiro_agarradoira);if(elemento_CONTAR<0)return 되돌림흐름읽기(Ficheiro_agarradoira,Tamaño);if(Tamaño<0||Tamaño>512)return -22;
    unsigned char datos[512];int 반환값=통신읽기(elemento_CONTAR,datos,Tamaño);for(int 순번=0;순번<반환값;순번++)자바전문넣기(순번,datos[순번]);return 반환값;
}
int32_t 자바흐름쓰기(int32_t Ficheiro_agarradoira,int32_t Tamaño){
    int elemento_CONTAR=외부번호(Ficheiro_agarradoira);if(elemento_CONTAR<0)return 되돌림흐름쓰기(Ficheiro_agarradoira,Tamaño);if(Tamaño<0||Tamaño>512)return -22;
    unsigned char datos[512];for(int 순번=0;순번<Tamaño;순번++)datos[순번]=자바전문얻기(순번);return 통신쓰기(elemento_CONTAR,datos,Tamaño);
}
int32_t 자바흐름접속번호(int32_t Ficheiro_agarradoira){int elemento_CONTAR=외부번호(Ficheiro_agarradoira);return elemento_CONTAR<0?되돌림흐름접속번호(Ficheiro_agarradoira):(int32_t)Rede_número_do_porto(elemento_CONTAR);}
int32_t 자바흐름상대(int32_t Ficheiro_agarradoira){int elemento_CONTAR=외부번호(Ficheiro_agarradoira);return elemento_CONTAR<0?되돌림흐름상대(Ficheiro_agarradoira):(int32_t)punto_número_do_porto(elemento_CONTAR);}
int32_t 자바흐름주소(int32_t Ficheiro_agarradoira){return 외부번호(Ficheiro_agarradoira)<0?0x7f000001:양쪽수신창구[Ficheiro_agarradoira-32]?0:망상태읽기(0,0);}
int32_t 자바흐름닫기(int32_t Ficheiro_agarradoira){int elemento_CONTAR=외부번호(Ficheiro_agarradoira);if(elemento_CONTAR>=0){peche_Rede(elemento_CONTAR);externo[Ficheiro_agarradoira-32]=0;}if(Ficheiro_agarradoira>=40&&Ficheiro_agarradoira<56)임의주소[Ficheiro_agarradoira-32]=양쪽수신창구[Ficheiro_agarradoira-32]=0;return 되돌림흐름닫기(Ficheiro_agarradoira);}
