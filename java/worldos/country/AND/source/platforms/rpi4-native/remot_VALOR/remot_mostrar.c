/* RFB 3.8 / VNC authentication / Raw true-colour rectangles.
 * 한 Connecta, 제한된 입력 durada_VALOR, 비동기 enviar_VALOR, 요청한 영역의 변경된 타일만 전송한다.
 * VNC의 화면 dades 자체는 암호화되지 않는다. SSH와 별도의 TCP 5900 서비스다. */
#include "remot_VALOR.h"
#include "암호기반.h"
#include "Perfil.h"
#include "../xarxa_Pila/xarxa_Pila.h"
#include "../màquina/화면정보.h"
#include <string.h>
#include <bearssl_block.h>
_Static_assert(sizeof(화면암호)==8, "VNC authentication requires a padded eight-byte key");
extern uintptr_t 보드밀리초(void);
extern uintptr_t Tauler_Terminal(uintptr_t);
void 원격글쇠(unsigned,int);
void 원격글쇠초기화(void);
void 원격글쇠확정(void);
static int S_està_escoltant_extrem=-1,homòleg_VALOR=-1,fase_VALOR,닫을예정;
static uintptr_t connexió_Hora,다시받을때;
static unsigned char 입력[8192],Sortida[4096],repte_VALOR[16];
static unsigned 입력수,출력수,보낸수;
static unsigned 너비,높이,píxel_canviar_la_mida=4,큰끝,빨강최대=255,초록최대=255,파랑최대=255,빨강이동=16,초록이동=8,파랑이동;
static uint32_t 지난요약[60*68];
static unsigned short 바뀐타일[60*68];
static unsigned peça_COMPT,peça_càrrec,요청가로,요청세로,요청폭,요청높이;
static unsigned tancar_16(const unsigned char *dades_càrrec){return(unsigned)dades_càrrec[0]*256+dades_càrrec[1];}
static uint32_t tancar_32(const unsigned char *dades_càrrec){return(uint32_t)dades_càrrec[0]<<24|(uint32_t)dades_càrrec[1]<<16|(uint32_t)dades_càrrec[2]<<8|dades_càrrec[3];}
static void escriure_16(unsigned char *dades_càrrec,unsigned VALOR){dades_càrrec[0]=VALOR>>8;dades_càrrec[1]=VALOR;}
static void escriure_32(unsigned char *dades_càrrec,uint32_t VALOR){dades_càrrec[0]=VALOR>>24;dades_càrrec[1]=VALOR>>16;dades_càrrec[2]=VALOR>>8;dades_càrrec[3]=VALOR;}
static void Tanca(void){if(homòleg_VALOR>=0)Tanca_xarxa(homòleg_VALOR);homòleg_VALOR=-1;fase_VALOR=0;입력수=출력수=보낸수=0;peça_COMPT=peça_càrrec=0;닫을예정=0;원격글쇠초기화();다시받을때=보드밀리초()+500;}
static void 내보내기(const void *dades,unsigned 수){memcpy(Sortida,dades,수);출력수=수;보낸수=0;}
static void 소비(unsigned 수){입력수-=수;memmove(입력,입력+수,입력수);}
int control_remot_mostrar(unsigned Acció){
    if(Acció==0){Tanca();if(S_està_escoltant_extrem>=0)Tanca_xarxa(S_està_escoltant_extrem);S_està_escoltant_extrem=-1;return 0;}
    if(Acció!=1)return S_està_escoltant_extrem>=0;
    if(S_està_escoltant_extrem>=0)return 0;
    int port_VALOR=통신끝점만들기(1);if(port_VALOR<0)return port_VALOR;통신주소재사용(port_VALOR);
    int RESULTAT=망주소묶기(port_VALOR,0,5900);if(!RESULTAT)RESULTAT=연결기다리기(port_VALOR);
    if(RESULTAT<0){Tanca_xarxa(port_VALOR);return RESULTAT;}S_està_escoltant_extrem=port_VALOR;return 0;
}
static uint32_t peça_resum(unsigned 가로,unsigned Vertical_càrrec){
    uint32_t VALOR=2166136261u;
    for(unsigned Y_coordenada=Vertical_càrrec;Y_coordenada<Vertical_càrrec+16&&Y_coordenada<높이;Y_coordenada++)for(unsigned X_coordenada=가로;X_coordenada<가로+32&&X_coordenada<너비;X_coordenada++)VALOR=(VALOR^보드화면읽기(X_coordenada,Y_coordenada))*16777619u;
    return VALOR;
}
static void 화면요청(const unsigned char *dades_càrrec){
    요청가로=tancar_16(dades_càrrec+2);요청세로=tancar_16(dades_càrrec+4);요청폭=tancar_16(dades_càrrec+6);요청높이=tancar_16(dades_càrrec+8);
    if(요청가로>=너비||요청세로>=높이)요청폭=요청높이=0;
    if(요청폭>너비-요청가로&&요청가로<너비)요청폭=너비-요청가로;
    if(요청높이>높이-요청세로&&요청세로<높이)요청높이=높이-요청세로;
    peça_COMPT=peça_càrrec=0;
    if(요청폭&&요청높이)for(unsigned Y_coordenada=요청세로/16;Y_coordenada<=(요청세로+요청높이-1)/16;Y_coordenada++)for(unsigned X_coordenada=요청가로/32;X_coordenada<=(요청가로+요청폭-1)/32;X_coordenada++){
        unsigned càrrec_INDEX=Y_coordenada*60+X_coordenada;uint32_t resum_VALOR=peça_resum(X_coordenada*32,Y_coordenada*16);
        if(!dades_càrrec[1]||지난요약[càrrec_INDEX]!=resum_VALOR)바뀐타일[peça_COMPT++]=càrrec_INDEX;
    }
    Sortida[0]=Sortida[1]=0;escriure_16(Sortida+2,peça_COMPT);출력수=4;보낸수=0;
}
static void enviar_peça(void){
    unsigned càrrec_INDEX=바뀐타일[peça_càrrec++],가로=(càrrec_INDEX%60)*32,Vertical_càrrec=(càrrec_INDEX/60)*16;
    unsigned finalitzar_X=가로+32,finalitzar_Y=Vertical_càrrec+16;if(finalitzar_X>너비)finalitzar_X=너비;if(finalitzar_Y>높이)finalitzar_Y=높이;
    /* 부분 타일 sol_licitud 뒤에도 나머지 화소를 보낸 것으로 처리하지 않는다. */
    int 전부=가로>=요청가로&&Vertical_càrrec>=요청세로&&finalitzar_X<=요청가로+요청폭&&finalitzar_Y<=요청세로+요청높이;
    if(전부)지난요약[càrrec_INDEX]=peça_resum(가로,Vertical_càrrec);
    if(가로<요청가로)가로=요청가로;if(Vertical_càrrec<요청세로)Vertical_càrrec=요청세로;
    if(finalitzar_X>요청가로+요청폭)finalitzar_X=요청가로+요청폭;if(finalitzar_Y>요청세로+요청높이)finalitzar_Y=요청세로+요청높이;
    escriure_16(Sortida,가로);escriure_16(Sortida+2,Vertical_càrrec);escriure_16(Sortida+4,finalitzar_X-가로);escriure_16(Sortida+6,finalitzar_Y-Vertical_càrrec);escriure_32(Sortida+8,0);
    출력수=12;보낸수=0;
    for(unsigned Y_coordenada=Vertical_càrrec;Y_coordenada<finalitzar_Y;Y_coordenada++)for(unsigned X_coordenada=가로;X_coordenada<finalitzar_X;X_coordenada++){
        uint32_t 색=보드화면읽기(X_coordenada,Y_coordenada),VALOR=(((색>>16)&255)*빨강최대/255)<<빨강이동|
            (((색>>8)&255)*초록최대/255)<<초록이동|((색&255)*파랑최대/255)<<파랑이동;
        for(unsigned 순번=0;순번<píxel_canviar_la_mida;순번++)Sortida[출력수++]=VALOR>>(8*(큰끝?píxel_canviar_la_mida-1-순번:순번));
    }
}
void 원격화면살피기(void){
    if(S_està_escoltant_extrem<0)return;
    if(homòleg_VALOR<0){if(보드밀리초()<다시받을때)return;homòleg_VALOR=망연결받기(S_està_escoltant_extrem);if(homòleg_VALOR<0)return;
        connexió_Hora=보드밀리초();fase_VALOR=1;내보내기("RFB 003.008\n",12);memset(지난요약,0,sizeof(지난요약));
        píxel_canviar_la_mida=4;큰끝=0;빨강최대=초록최대=파랑최대=255;빨강이동=16;초록이동=8;파랑이동=0;}
    if(fase_VALOR<5&&보드밀리초()-connexió_Hora>15000){Tanca();return;}
    if(출력수){int 수=통신쓰기(homòleg_VALOR,Sortida+보낸수,출력수-보낸수);if(수>0){보낸수+=수;if(보낸수==출력수)출력수=보낸수=0;}else if(수!=-11){Tanca();return;}}
    if(!출력수&&닫을예정){Tanca();return;}
    if(!출력수&&peça_càrrec<peça_COMPT)enviar_peça();
    if(입력수==sizeof(입력)){Tanca();return;}
    int CANTIDAD_RECIBIDA_COMPT=통신읽기(homòleg_VALOR,입력+입력수,sizeof(입력)-입력수);
    if(CANTIDAD_RECIBIDA_COMPT==0||(CANTIDAD_RECIBIDA_COMPT<0&&CANTIDAD_RECIBIDA_COMPT!=-11)){Tanca();return;}if(CANTIDAD_RECIBIDA_COMPT>0)입력수+=CANTIDAD_RECIBIDA_COMPT;
    if(출력수||peça_càrrec<peça_COMPT)return;
    if(fase_VALOR==1&&입력수>=12){if(memcmp(입력,"RFB 003.008\n",12)){Tanca();return;}소비(12);const unsigned char mètode_d_autenticació[]={1,2};내보내기(mètode_d_autenticació,2);fase_VALOR=2;return;}
    if(fase_VALOR==2&&입력수){if(입력[0]!=2||원격난수(repte_VALOR,16)){Tanca();return;}소비(1);내보내기(repte_VALOR,16);fase_VALOR=3;return;}
    if(fase_VALOR==3&&입력수>=16){unsigned char 열쇠[8],정답[16];br_des_ct_cbcenc_keys contrasenya_VALOR;
        for(unsigned 순번=0;순번<8;순번++){unsigned VALOR=화면암호[순번],뒤집음=0;for(unsigned 안쪽순번=0;안쪽순번<8;안쪽순번++){뒤집음=(뒤집음<<1)|(VALOR&1);VALOR>>=1;}열쇠[순번]=뒤집음;}
        br_des_ct_cbcenc_init(&contrasenya_VALOR,열쇠,8);memcpy(정답,repte_VALOR,16);
        for(unsigned 순번=0;순번<16;순번+=8){unsigned char vector_VALOR[8]={0};br_des_ct_cbcenc_run(&contrasenya_VALOR,vector_VALOR,정답+순번,8);memset(vector_VALOR,0,8);}
        unsigned 차이=0;for(unsigned 순번=0;순번<16;순번++)차이|=정답[순번]^입력[순번];소비(16);memset(&contrasenya_VALOR,0,sizeof(contrasenya_VALOR));memset(열쇠,0,8);memset(정답,0,16);memset(repte_VALOR,0,16);
        escriure_32(Sortida,차이?1:0);출력수=4;보낸수=0;
        if(차이){escriure_32(Sortida+4,19);memcpy(Sortida+8,"Authentication fail",19);출력수=27;닫을예정=1;}else fase_VALOR=4;return;}
    if(fase_VALOR==4&&입력수){소비(1);너비=보드화면너비();높이=보드화면높이();if(!너비||!높이||너비>1920||높이>1080){Tanca();return;}
        if(!Tauler_Terminal(7)){const unsigned char Esdeveniment[]={30,2,1,0,0,0,0};원격입력넣기(Esdeveniment,7);}
        memset(Sortida,0,40);escriure_16(Sortida,너비);escriure_16(Sortida+2,높이);Sortida[4]=32;Sortida[5]=24;Sortida[7]=1;
        escriure_16(Sortida+8,255);escriure_16(Sortida+10,255);escriure_16(Sortida+12,255);Sortida[14]=16;Sortida[15]=8;
        const char *Nom="jkoros native";escriure_32(Sortida+20,strlen(Nom));memcpy(Sortida+24,Nom,strlen(Nom));출력수=24+strlen(Nom);보낸수=0;fase_VALOR=5;return;}
    if(fase_VALOR!=5||!입력수)return;
    unsigned TIPUS_Categoria=입력[0],필요=TIPUS_Categoria==0?20:TIPUS_Categoria==2?4:TIPUS_Categoria==3?10:TIPUS_Categoria==4?8:TIPUS_Categoria==5?6:TIPUS_Categoria==6?8:0;
    if(!필요){Tanca();return;}if(입력수<필요)return;
    if(TIPUS_Categoria==2){unsigned 수=tancar_16(입력+2);if(수>128){Tanca();return;}필요+=수*4;}
    if(TIPUS_Categoria==6){unsigned 수=tancar_32(입력+4);if(수>4096){Tanca();return;}필요+=수;}
    if(입력수<필요)return;
    if(TIPUS_Categoria==0){unsigned bit_VALOR=입력[4],빨=tancar_16(입력+8),초=tancar_16(입력+10),파=tancar_16(입력+12),빨이=입력[14],초이=입력[15],파이=입력[16];
        if((bit_VALOR!=16&&bit_VALOR!=32)||!입력[7]||입력[6]>1||!빨||!초||!파||빨>255||초>255||파>255||빨이>24||초이>24||파이>24||
           ((uint64_t)빨<<빨이)>((1ull<<bit_VALOR)-1)||((uint64_t)초<<초이)>((1ull<<bit_VALOR)-1)||((uint64_t)파<<파이)>((1ull<<bit_VALOR)-1)){Tanca();return;}
        píxel_canviar_la_mida=bit_VALOR/8;큰끝=입력[6];빨강최대=빨;초록최대=초;파랑최대=파;빨강이동=빨이;초록이동=초이;파랑이동=파이;memset(지난요약,0,sizeof(지난요약));
    }else if(TIPUS_Categoria==3)화면요청(입력);
    else if(TIPUS_Categoria==4)원격글쇠(tancar_32(입력+4),입력[1]!=0);
    else if(TIPUS_Categoria==5){unsigned X_coordenada=tancar_16(입력+2),Y_coordenada=tancar_16(입력+4);if(X_coordenada>=너비)X_coordenada=너비-1;if(Y_coordenada>=높이)Y_coordenada=높이-1;
        if(입력[1])원격글쇠확정();
        unsigned char Esdeveniment[]={30,1,입력[1],X_coordenada&255,X_coordenada>>8,Y_coordenada&255,Y_coordenada>>8};원격입력넣기(Esdeveniment,sizeof(Esdeveniment));}
    소비(필요);
}
