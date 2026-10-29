/* RFB 3.8 / VNC authentication / Raw true-colour rectangles.
 * 한 Conectar, 제한된 입력 duración_VALOR, 비동기 enviar_VALOR, 요청한 영역의 변경된 타일만 전송한다.
 * VNC의 화면 datos 자체는 암호화되지 않는다. SSH와 별도의 TCP 5900 서비스다. */
#include "remoto_VALOR.h"
#include "암호기반.h"
#include "Perfil.h"
#include "../Rede_Montón/Rede_Montón.h"
#include "../máquina/화면정보.h"
#include <string.h>
#include <bearssl_block.h>
_Static_assert(sizeof(화면암호)==8, "VNC authentication requires a padded eight-byte key");
extern uintptr_t 보드밀리초(void);
extern uintptr_t Panel_Terminal(uintptr_t);
void 원격글쇠(unsigned,int);
void 원격글쇠초기화(void);
void 원격글쇠확정(void);
static int A_escoitar_extremo=-1,punto_VALOR=-1,fase_VALOR,닫을예정;
static uintptr_t conexión_hora,다시받을때;
static unsigned char 입력[8192],Saída[4096],desafío_VALOR[16];
static unsigned 입력수,출력수,보낸수;
static unsigned 너비,높이,화소크기=4,큰끝,빨강최대=255,초록최대=255,파랑최대=255,빨강이동=16,초록이동=8,파랑이동;
static uint32_t 지난요약[60*68];
static unsigned short 바뀐타일[60*68];
static unsigned mosaico_CONTAR,mosaico_cargo,요청가로,요청세로,요청폭,요청높이;
static unsigned 읽기16(const unsigned char *datos_cargo){return(unsigned)datos_cargo[0]*256+datos_cargo[1];}
static uint32_t 읽기32(const unsigned char *datos_cargo){return(uint32_t)datos_cargo[0]<<24|(uint32_t)datos_cargo[1]<<16|(uint32_t)datos_cargo[2]<<8|datos_cargo[3];}
static void escribir_16(unsigned char *datos_cargo,unsigned VALOR){datos_cargo[0]=VALOR>>8;datos_cargo[1]=VALOR;}
static void escribir_32(unsigned char *datos_cargo,uint32_t VALOR){datos_cargo[0]=VALOR>>24;datos_cargo[1]=VALOR>>16;datos_cargo[2]=VALOR>>8;datos_cargo[3]=VALOR;}
static void Pechar(void){if(punto_VALOR>=0)peche_Rede(punto_VALOR);punto_VALOR=-1;fase_VALOR=0;입력수=출력수=보낸수=0;mosaico_CONTAR=mosaico_cargo=0;닫을예정=0;원격글쇠초기화();다시받을때=보드밀리초()+500;}
static void 내보내기(const void *datos,unsigned 수){memcpy(Saída,datos,수);출력수=수;보낸수=0;}
static void 소비(unsigned 수){입력수-=수;memmove(입력,입력+수,입력수);}
int control_remoto_mostrar(unsigned Acción){
    if(Acción==0){Pechar();if(A_escoitar_extremo>=0)peche_Rede(A_escoitar_extremo);A_escoitar_extremo=-1;return 0;}
    if(Acción!=1)return A_escoitar_extremo>=0;
    if(A_escoitar_extremo>=0)return 0;
    int porto_VALOR=통신끝점만들기(1);if(porto_VALOR<0)return porto_VALOR;통신주소재사용(porto_VALOR);
    int RESULTANTE=망주소묶기(porto_VALOR,0,5900);if(!RESULTANTE)RESULTANTE=연결기다리기(porto_VALOR);
    if(RESULTANTE<0){peche_Rede(porto_VALOR);return RESULTANTE;}A_escoitar_extremo=porto_VALOR;return 0;
}
static uint32_t mosaico_resumo(unsigned 가로,unsigned Vertical_cargo){
    uint32_t VALOR=2166136261u;
    for(unsigned Y_coordenada=Vertical_cargo;Y_coordenada<Vertical_cargo+16&&Y_coordenada<높이;Y_coordenada++)for(unsigned X_coordenada=가로;X_coordenada<가로+32&&X_coordenada<너비;X_coordenada++)VALOR=(VALOR^보드화면읽기(X_coordenada,Y_coordenada))*16777619u;
    return VALOR;
}
static void 화면요청(const unsigned char *datos_cargo){
    요청가로=읽기16(datos_cargo+2);요청세로=읽기16(datos_cargo+4);요청폭=읽기16(datos_cargo+6);요청높이=읽기16(datos_cargo+8);
    if(요청가로>=너비||요청세로>=높이)요청폭=요청높이=0;
    if(요청폭>너비-요청가로&&요청가로<너비)요청폭=너비-요청가로;
    if(요청높이>높이-요청세로&&요청세로<높이)요청높이=높이-요청세로;
    mosaico_CONTAR=mosaico_cargo=0;
    if(요청폭&&요청높이)for(unsigned Y_coordenada=요청세로/16;Y_coordenada<=(요청세로+요청높이-1)/16;Y_coordenada++)for(unsigned X_coordenada=요청가로/32;X_coordenada<=(요청가로+요청폭-1)/32;X_coordenada++){
        unsigned cargo_ÍNDICE=Y_coordenada*60+X_coordenada;uint32_t resumo_VALOR=mosaico_resumo(X_coordenada*32,Y_coordenada*16);
        if(!datos_cargo[1]||지난요약[cargo_ÍNDICE]!=resumo_VALOR)바뀐타일[mosaico_CONTAR++]=cargo_ÍNDICE;
    }
    Saída[0]=Saída[1]=0;escribir_16(Saída+2,mosaico_CONTAR);출력수=4;보낸수=0;
}
static void enviar_mosaico(void){
    unsigned cargo_ÍNDICE=바뀐타일[mosaico_cargo++],가로=(cargo_ÍNDICE%60)*32,Vertical_cargo=(cargo_ÍNDICE/60)*16;
    unsigned finalizar_X=가로+32,finalizar_Y=Vertical_cargo+16;if(finalizar_X>너비)finalizar_X=너비;if(finalizar_Y>높이)finalizar_Y=높이;
    /* 부분 타일 solicitude 뒤에도 나머지 화소를 보낸 것으로 처리하지 않는다. */
    int 전부=가로>=요청가로&&Vertical_cargo>=요청세로&&finalizar_X<=요청가로+요청폭&&finalizar_Y<=요청세로+요청높이;
    if(전부)지난요약[cargo_ÍNDICE]=mosaico_resumo(가로,Vertical_cargo);
    if(가로<요청가로)가로=요청가로;if(Vertical_cargo<요청세로)Vertical_cargo=요청세로;
    if(finalizar_X>요청가로+요청폭)finalizar_X=요청가로+요청폭;if(finalizar_Y>요청세로+요청높이)finalizar_Y=요청세로+요청높이;
    escribir_16(Saída,가로);escribir_16(Saída+2,Vertical_cargo);escribir_16(Saída+4,finalizar_X-가로);escribir_16(Saída+6,finalizar_Y-Vertical_cargo);escribir_32(Saída+8,0);
    출력수=12;보낸수=0;
    for(unsigned Y_coordenada=Vertical_cargo;Y_coordenada<finalizar_Y;Y_coordenada++)for(unsigned X_coordenada=가로;X_coordenada<finalizar_X;X_coordenada++){
        uint32_t 색=보드화면읽기(X_coordenada,Y_coordenada),VALOR=(((색>>16)&255)*빨강최대/255)<<빨강이동|
            (((색>>8)&255)*초록최대/255)<<초록이동|((색&255)*파랑최대/255)<<파랑이동;
        for(unsigned 순번=0;순번<화소크기;순번++)Saída[출력수++]=VALOR>>(8*(큰끝?화소크기-1-순번:순번));
    }
}
void 원격화면살피기(void){
    if(A_escoitar_extremo<0)return;
    if(punto_VALOR<0){if(보드밀리초()<다시받을때)return;punto_VALOR=망연결받기(A_escoitar_extremo);if(punto_VALOR<0)return;
        conexión_hora=보드밀리초();fase_VALOR=1;내보내기("RFB 003.008\n",12);memset(지난요약,0,sizeof(지난요약));
        화소크기=4;큰끝=0;빨강최대=초록최대=파랑최대=255;빨강이동=16;초록이동=8;파랑이동=0;}
    if(fase_VALOR<5&&보드밀리초()-conexión_hora>15000){Pechar();return;}
    if(출력수){int 수=통신쓰기(punto_VALOR,Saída+보낸수,출력수-보낸수);if(수>0){보낸수+=수;if(보낸수==출력수)출력수=보낸수=0;}else if(수!=-11){Pechar();return;}}
    if(!출력수&&닫을예정){Pechar();return;}
    if(!출력수&&mosaico_cargo<mosaico_CONTAR)enviar_mosaico();
    if(입력수==sizeof(입력)){Pechar();return;}
    int RECIBIDO_CONTAR=통신읽기(punto_VALOR,입력+입력수,sizeof(입력)-입력수);
    if(RECIBIDO_CONTAR==0||(RECIBIDO_CONTAR<0&&RECIBIDO_CONTAR!=-11)){Pechar();return;}if(RECIBIDO_CONTAR>0)입력수+=RECIBIDO_CONTAR;
    if(출력수||mosaico_cargo<mosaico_CONTAR)return;
    if(fase_VALOR==1&&입력수>=12){if(memcmp(입력,"RFB 003.008\n",12)){Pechar();return;}소비(12);const unsigned char método_de_autenticación[]={1,2};내보내기(método_de_autenticación,2);fase_VALOR=2;return;}
    if(fase_VALOR==2&&입력수){if(입력[0]!=2||원격난수(desafío_VALOR,16)){Pechar();return;}소비(1);내보내기(desafío_VALOR,16);fase_VALOR=3;return;}
    if(fase_VALOR==3&&입력수>=16){unsigned char 열쇠[8],정답[16];br_des_ct_cbcenc_keys contrasinal_VALOR;
        for(unsigned 순번=0;순번<8;순번++){unsigned VALOR=화면암호[순번],뒤집음=0;for(unsigned 안쪽순번=0;안쪽순번<8;안쪽순번++){뒤집음=(뒤집음<<1)|(VALOR&1);VALOR>>=1;}열쇠[순번]=뒤집음;}
        br_des_ct_cbcenc_init(&contrasinal_VALOR,열쇠,8);memcpy(정답,desafío_VALOR,16);
        for(unsigned 순번=0;순번<16;순번+=8){unsigned char vector_VALOR[8]={0};br_des_ct_cbcenc_run(&contrasinal_VALOR,vector_VALOR,정답+순번,8);memset(vector_VALOR,0,8);}
        unsigned 차이=0;for(unsigned 순번=0;순번<16;순번++)차이|=정답[순번]^입력[순번];소비(16);memset(&contrasinal_VALOR,0,sizeof(contrasinal_VALOR));memset(열쇠,0,8);memset(정답,0,16);memset(desafío_VALOR,0,16);
        escribir_32(Saída,차이?1:0);출력수=4;보낸수=0;
        if(차이){escribir_32(Saída+4,19);memcpy(Saída+8,"Authentication fail",19);출력수=27;닫을예정=1;}else fase_VALOR=4;return;}
    if(fase_VALOR==4&&입력수){소비(1);너비=보드화면너비();높이=보드화면높이();if(!너비||!높이||너비>1920||높이>1080){Pechar();return;}
        if(!Panel_Terminal(7)){const unsigned char Evento[]={30,2,1,0,0,0,0};원격입력넣기(Evento,7);}
        memset(Saída,0,40);escribir_16(Saída,너비);escribir_16(Saída+2,높이);Saída[4]=32;Saída[5]=24;Saída[7]=1;
        escribir_16(Saída+8,255);escribir_16(Saída+10,255);escribir_16(Saída+12,255);Saída[14]=16;Saída[15]=8;
        const char *Nome="jkoros native";escribir_32(Saída+20,strlen(Nome));memcpy(Saída+24,Nome,strlen(Nome));출력수=24+strlen(Nome);보낸수=0;fase_VALOR=5;return;}
    if(fase_VALOR!=5||!입력수)return;
    unsigned TIPO_Categoría=입력[0],필요=TIPO_Categoría==0?20:TIPO_Categoría==2?4:TIPO_Categoría==3?10:TIPO_Categoría==4?8:TIPO_Categoría==5?6:TIPO_Categoría==6?8:0;
    if(!필요){Pechar();return;}if(입력수<필요)return;
    if(TIPO_Categoría==2){unsigned 수=읽기16(입력+2);if(수>128){Pechar();return;}필요+=수*4;}
    if(TIPO_Categoría==6){unsigned 수=읽기32(입력+4);if(수>4096){Pechar();return;}필요+=수;}
    if(입력수<필요)return;
    if(TIPO_Categoría==0){unsigned bit_VALOR=입력[4],빨=읽기16(입력+8),초=읽기16(입력+10),파=읽기16(입력+12),빨이=입력[14],초이=입력[15],파이=입력[16];
        if((bit_VALOR!=16&&bit_VALOR!=32)||!입력[7]||입력[6]>1||!빨||!초||!파||빨>255||초>255||파>255||빨이>24||초이>24||파이>24||
           ((uint64_t)빨<<빨이)>((1ull<<bit_VALOR)-1)||((uint64_t)초<<초이)>((1ull<<bit_VALOR)-1)||((uint64_t)파<<파이)>((1ull<<bit_VALOR)-1)){Pechar();return;}
        화소크기=bit_VALOR/8;큰끝=입력[6];빨강최대=빨;초록최대=초;파랑최대=파;빨강이동=빨이;초록이동=초이;파랑이동=파이;memset(지난요약,0,sizeof(지난요약));
    }else if(TIPO_Categoría==3)화면요청(입력);
    else if(TIPO_Categoría==4)원격글쇠(읽기32(입력+4),입력[1]!=0);
    else if(TIPO_Categoría==5){unsigned X_coordenada=읽기16(입력+2),Y_coordenada=읽기16(입력+4);if(X_coordenada>=너비)X_coordenada=너비-1;if(Y_coordenada>=높이)Y_coordenada=높이-1;
        if(입력[1])원격글쇠확정();
        unsigned char Evento[]={30,1,입력[1],X_coordenada&255,X_coordenada>>8,Y_coordenada&255,Y_coordenada>>8};원격입력넣기(Evento,sizeof(Evento));}
    소비(필요);
}
