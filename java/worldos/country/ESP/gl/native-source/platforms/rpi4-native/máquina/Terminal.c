#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* 자체 네 Xanela 합성과 UTF-8 Terminal. 바뀐 영역의 Completadas_VALOR 그림만 표시한다. */
#include <stdint.h>
#include <stddef.h>
typedef uintptr_t máquina_Word;
extern máquina_Word Panel_píxel(máquina_Word,máquina_Word,máquina_Word),보드화면기억공간(void);
extern void *memset(void *,int,size_t);
extern const unsigned char Terminal_tipo_de_letra[];
#define 최대열수 237
#define Historial_liña_CONTAR 160
typedef struct {
    uint32_t 글자칸들[Historial_liña_CONTAR][최대열수]; uint8_t 모양들[Historial_liña_CONTAR][최대열수];
    unsigned 너비,높이,COLUMNAS,FILA_CONTAR,크기바뀜;
    unsigned 살아있음,X_coordenada,Y_coordenada,FILA_cargo,COLUMNA_cargo,맨위,desprazar,전경색,배경색,탈출상태,parámetro_VALOR[4],parámetro_ÍNDICE,저장행,저장열;
    unsigned 부호없는결과,긴부호없는값,MENOR_VALOR,대체화면,가리개보임;
} Terminal_d413d4bc;
static Terminal_d413d4bc Windows_Lista[4];
static int Foco=-1,출력결과,orde_VALOR[4],introdución_CONTAR,arrastrar_VALOR=-1,arrastrar_X,arrastrar_Y;
static unsigned Tecnoloxía_da_información_TI_pendente,단추들,escritorio_ver,한글입력;
static const uint32_t 색상들[16]={0x201a15,0x6060df,0x9dcc86,0x80cfea,0xefaf72,0xca96c9,0xceda76,0xede9df,0x858078,0x8888ff,0xb9eba7,0xa5eaff,0xffcc99,0xf0bef1,0xf0f0a0,0xffffff};
extern int 화면보임(int),화면가리킴(int,unsigned,int,int);
extern void 화면다시그림(int);
static Terminal_d413d4bc *Terminal_introdución;
static unsigned 넓은글자(unsigned código_de_carácter){return código_de_carácter>=256?2:1;}
static void 사각영역(unsigned X_coordenada,unsigned Y_coordenada,unsigned 너비값,unsigned 높이값,unsigned 색상){
    보드사각그림(X_coordenada,Y_coordenada,너비값,높이값,색상);
}
void Terminal_glifo(unsigned X_coordenada,unsigned Y_coordenada,unsigned código_de_carácter,unsigned 전경색,unsigned 배경색){
    unsigned 너비=넓은글자(código_de_carácter)*8;if(código_de_carácter==0xffffffffu)return;
    int 왼쪽=X_coordenada,위쪽=Y_coordenada,폭=너비,duración_VALOR=16;
    if(!보드그림범위(&왼쪽,&위쪽,&폭,&duración_VALOR))return;
    if(código_de_carácter==' '){보드사각그림(왼쪽,위쪽,폭,duración_VALOR,배경색);return;}
    unsigned Busca_ÍNDICE=código_de_carácter<65536?código_de_carácter:código_de_carácter>=0x1f600&&código_de_carácter<0x1f650?65536+código_de_carácter-0x1f600:0xfffd;
    const unsigned char *tipo_de_letra_VALOR=Terminal_tipo_de_letra+Busca_ÍNDICE*32;
    for(int Liña=위쪽;Liña<위쪽+duración_VALOR;Liña++){unsigned Servizo_de_transferencia_intelixente_en_segundo_plano_Lista=tipo_de_letra_VALOR[(Liña-Y_coordenada)*2]*256+tipo_de_letra_VALOR[(Liña-Y_coordenada)*2+1];for(int 칸=왼쪽;칸<왼쪽+폭;칸++)Panel_píxel(칸,Liña,(Servizo_de_transferencia_intelixente_en_segundo_plano_Lista&(0x8000>>(칸-X_coordenada)))?전경색:배경색);}
}
static void nome_táboa(unsigned X_coordenada,unsigned Y_coordenada,const char *cadea_datos,unsigned 전경색,unsigned 배경색){while(*cadea_datos){unsigned código_de_carácter=(unsigned char)*cadea_datos++, 남은수=0;if(código_de_carácter>=0xc0){남은수=código_de_carácter<0xe0?1:código_de_carácter<0xf0?2:3;código_de_carácter&=(1u<<(6-남은수))-1;while(남은수--&&*cadea_datos)código_de_carácter=(código_de_carácter<<6)|((unsigned char)*cadea_datos++&63);}Terminal_glifo(X_coordenada,Y_coordenada,código_de_carácter,전경색,배경색);X_coordenada+=넓은글자(código_de_carácter)*8;}}
static unsigned 첫항목(void){return Terminal_introdución->맨위;}
static int 보이는지(void){return Terminal_introdución->살아있음&&Foco>=0&&Terminal_introdución==&Windows_Lista[Foco]&&!화면보임(Foco);}
static void 그리기(unsigned FILA_cargo,unsigned COLUMNA_cargo){
    if(!보이는지()||FILA_cargo<첫항목()-Terminal_introdución->desprazar||FILA_cargo>=첫항목()-Terminal_introdución->desprazar+Terminal_introdución->FILA_CONTAR||COLUMNA_cargo>=Terminal_introdución->COLUMNAS)return;
    unsigned código_de_carácter=Terminal_introdución->글자칸들[FILA_cargo%Historial_liña_CONTAR][COLUMNA_cargo],cadea_datos=Terminal_introdución->모양들[FILA_cargo%Historial_liña_CONTAR][COLUMNA_cargo];
    if(넓은글자(código_de_carácter)==2&&COLUMNA_cargo+1>=Terminal_introdución->COLUMNAS)código_de_carácter=' ';
    Terminal_glifo(Terminal_introdución->X_coordenada+12+COLUMNA_cargo*8,Terminal_introdución->Y_coordenada+36+(FILA_cargo-첫항목()+Terminal_introdución->desprazar)*16,código_de_carácter?código_de_carácter:' ',색상들[cadea_datos&15],색상들[cadea_datos>>4]);
}
static void acento_circunflexo_VALOR(int mostrar_ventá){if(!보이는지()||Terminal_introdución->desprazar||Terminal_introdución->COLUMNA_cargo>=Terminal_introdución->COLUMNAS||Terminal_introdución->FILA_cargo<Terminal_introdución->맨위||Terminal_introdución->FILA_cargo>=Terminal_introdución->맨위+Terminal_introdución->FILA_CONTAR)return;
    if(!mostrar_ventá||!Terminal_introdución->가리개보임)그리기(Terminal_introdución->FILA_cargo,Terminal_introdución->COLUMNA_cargo);else 사각영역(Terminal_introdución->X_coordenada+12+Terminal_introdución->COLUMNA_cargo*8,Terminal_introdución->Y_coordenada+36+(Terminal_introdución->FILA_cargo-Terminal_introdución->맨위)*16+14,8,2,색상들[Terminal_introdución->전경색]);}
static void Contido_VALOR(void){
    사각영역(Terminal_introdución->X_coordenada+12,Terminal_introdución->Y_coordenada+36,Terminal_introdución->COLUMNAS*8,Terminal_introdución->FILA_CONTAR*16,색상들[0]);
    int 가로=Terminal_introdución->X_coordenada+12,Vertical_cargo=Terminal_introdución->Y_coordenada+36,폭=Terminal_introdución->COLUMNAS*8,duración_VALOR=Terminal_introdución->FILA_CONTAR*16;
    if(보드그림범위(&가로,&Vertical_cargo,&폭,&duración_VALOR)){
    unsigned 첫줄=(Vertical_cargo-Terminal_introdución->Y_coordenada-36)/16,끝줄=(Vertical_cargo+duración_VALOR-Terminal_introdución->Y_coordenada-36+15)/16;
    unsigned 첫칸=(가로-Terminal_introdución->X_coordenada-12)/8,끝칸=(가로+폭-Terminal_introdución->X_coordenada-12+7)/8;
    if(첫칸)첫칸--; /* 잘림 경계 왼쪽에서 시작한 두 칸 글자도 그린다. */
    for(unsigned 반환값=첫줄;반환값<끝줄;반환값++)for(unsigned código_de_carácter=첫칸;código_de_carácter<끝칸;código_de_carácter++){
        unsigned FILA_cargo=첫항목()-Terminal_introdución->desprazar+반환값,carácter_VALOR=Terminal_introdución->글자칸들[FILA_cargo%Historial_liña_CONTAR][código_de_carácter],cadea_datos=Terminal_introdución->모양들[FILA_cargo%Historial_liña_CONTAR][código_de_carácter];
        if(넓은글자(carácter_VALOR)==2&&código_de_carácter+1>=Terminal_introdución->COLUMNAS)carácter_VALOR=' ';
        if((carácter_VALOR==0||carácter_VALOR==' ')&&(cadea_datos>>4)==0)continue;
        Terminal_glifo(Terminal_introdución->X_coordenada+12+código_de_carácter*8,Terminal_introdución->Y_coordenada+36+반환값*16,carácter_VALOR?carácter_VALOR:' ',색상들[cadea_datos&15],색상들[cadea_datos>>4]);
    }}
    nome_táboa(Terminal_introdución->X_coordenada+12,Terminal_introdución->Y_coordenada+Terminal_introdución->높이-18,Terminal_introdución->desprazar?"PgDn: recent output":Terminal_introdución->너비>=500?"F6: next | Corner + left drag: resize":"Corner + left drag: resize",0xece8e2,0x403127);acento_circunflexo_VALOR(1);
}
static void 실행틀(int 식별자){
    Terminal_introdución=&Windows_Lista[식별자];
    int 가로=Terminal_introdución->X_coordenada,Vertical_cargo=Terminal_introdución->Y_coordenada,폭=Terminal_introdución->너비,duración_VALOR=Terminal_introdución->높이;
    if(!보드그림범위(&가로,&Vertical_cargo,&폭,&duración_VALOR))return;
    사각영역(Terminal_introdución->X_coordenada,Terminal_introdución->Y_coordenada,Terminal_introdución->너비,Terminal_introdución->높이,0x403127);
    unsigned 색상=식별자==Foco?0x905020:0x604438;사각영역(Terminal_introdución->X_coordenada,Terminal_introdución->Y_coordenada,Terminal_introdución->너비,30,색상);
    nome_táboa(Terminal_introdución->X_coordenada+12,Terminal_introdución->Y_coordenada+7,"JKOROS Terminal",0xffffff,색상);
    char 수치[2]={(char)('1'+식별자),0};nome_táboa(Terminal_introdución->X_coordenada+148,Terminal_introdución->Y_coordenada+7,수치,0xffffff,색상);
    nome_táboa(Terminal_introdución->X_coordenada+240,Terminal_introdución->Y_coordenada+7,Terminal_introdución->너비>=500?(한글입력?"[GL] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[GL]":"[EN]"),0xffffff,색상);
    사각영역(Terminal_introdución->X_coordenada+Terminal_introdución->너비-32,Terminal_introdución->Y_coordenada+4,26,22,0x5555b8);nome_táboa(Terminal_introdución->X_coordenada+Terminal_introdución->너비-24,Terminal_introdución->Y_coordenada+7,"X",0xffffff,0x5555b8);
    Contido_VALOR();
}
static void 장면그리기(void){
    if(!escritorio_ver)return;사각영역(0,0,보드화면너비(),보드화면높이(),0x302018);사각영역(0,0,보드화면너비(),32,0x403127);
    사각영역(6,4,136,24,0x905020);nome_táboa(14,8,"+ New terminal",0xffffff,0x905020);
    for(int 순번=0;순번<4;순번++)if(Windows_Lista[순번].살아있음){unsigned código_de_carácter=Foco==순번?0x905020:0x604438;사각영역(154+순번*112,4,106,24,código_de_carácter);nome_táboa(160+순번*112,8,"Terminal",0xffffff,código_de_carácter);char cadea_datos[2]={(char)('1'+순번),0};nome_táboa(232+순번*112,8,cadea_datos,0xffffff,código_de_carácter);}
    if(!introdución_CONTAR)nome_táboa(140,210,"Click + New terminal to start",0xede9df,0x302018);
    for(int 순번=0;순번<introdución_CONTAR;순번++)실행틀(orde_VALOR[순번]);화면다시그림(Foco);Terminal_introdución=&Windows_Lista[출력결과];
}
static void 영역그리기(int 가로,int Vertical_cargo,int 폭,int duración_VALOR){
    if(!escritorio_ver||!보드그림범위(&가로,&Vertical_cargo,&폭,&duración_VALOR))return;
    for(int Liña=Vertical_cargo;Liña<Vertical_cargo+duración_VALOR;Liña+=32){
        int 띠높이=Vertical_cargo+duración_VALOR-Liña;if(띠높이>32)띠높이=32;
        if(보드그림시작(가로,Liña,폭,띠높이)){장면그리기();보드그림마침();}
    }
}
static void 다시그리기(void){영역그리기(0,0,보드화면너비(),보드화면높이());}
/* 서로 겹치지 않는 새 Xanela 영역과 이전 자리의 네 띠를 복구한다. */
static void 창자리그리기(int 가로,int Vertical_cargo,int 폭,int duración_VALOR,Terminal_d413d4bc *Xanela){
    int 왼쪽=가로>(int)Xanela->X_coordenada?가로:(int)Xanela->X_coordenada;
    int 위쪽=Vertical_cargo>(int)Xanela->Y_coordenada?Vertical_cargo:(int)Xanela->Y_coordenada;
    int DEREITA=가로+폭<(int)(Xanela->X_coordenada+Xanela->너비)?가로+폭:(int)(Xanela->X_coordenada+Xanela->너비);
    int 아래쪽=Vertical_cargo+duración_VALOR<(int)(Xanela->Y_coordenada+Xanela->높이)?Vertical_cargo+duración_VALOR:(int)(Xanela->Y_coordenada+Xanela->높이);
    영역그리기(Xanela->X_coordenada,Xanela->Y_coordenada,Xanela->너비,Xanela->높이);
    if(왼쪽>=DEREITA||위쪽>=아래쪽){영역그리기(가로,Vertical_cargo,폭,duración_VALOR);return;}
    영역그리기(가로,Vertical_cargo,폭,위쪽-Vertical_cargo);
    영역그리기(가로,아래쪽,폭,Vertical_cargo+duración_VALOR-아래쪽);
    영역그리기(가로,위쪽,왼쪽-가로,아래쪽-위쪽);
    영역그리기(DEREITA,위쪽,가로+폭-DEREITA,아래쪽-위쪽);
}
static void sinal_Foco(void){Tecnoloxía_da_información_TI_pendente=(Tecnoloxía_da_información_TI_pendente&~15u)|(unsigned)(Foco+1)|0x10000;}
void 터미널입력방식(unsigned 한글여부){
    한글입력=한글여부!=0;
    /* Update title bars only: a mode switch must not erase an EL0 drawing. */
    if(Foco>=0){
        Terminal_d413d4bc *ventá_introdución=&Windows_Lista[Foco];
        nome_táboa(ventá_introdución->X_coordenada+240,ventá_introdución->Y_coordenada+7,ventá_introdución->너비>=500?(한글입력?"[GL] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[GL]":"[EN]"),0xffffff,0x905020);
    }
}
static void 앞으로올리기(int 식별자){if(식별자<0||식별자>=4||!Windows_Lista[식별자].살아있음)return;int ao_corrente_cargo=0;while(ao_corrente_cargo<introdución_CONTAR&&orde_VALOR[ao_corrente_cargo]!=식별자)ao_corrente_cargo++;for(;ao_corrente_cargo+1<introdución_CONTAR;ao_corrente_cargo++)orde_VALOR[ao_corrente_cargo]=orde_VALOR[ao_corrente_cargo+1];orde_VALOR[introdución_CONTAR-1]=식별자;Foco=식별자;sinal_Foco();다시그리기();}
static void 빈칸채우기(unsigned FILA_cargo){for(unsigned código_de_carácter=0;código_de_carácter<최대열수;código_de_carácter++){Terminal_introdución->글자칸들[FILA_cargo%Historial_liña_CONTAR][código_de_carácter]=0;Terminal_introdución->모양들[FILA_cargo%Historial_liña_CONTAR][código_de_carácter]=Terminal_introdución->전경색|(Terminal_introdución->배경색<<4);}}
static void desmarcar_Contido(void){Terminal_introdución->FILA_cargo=Terminal_introdución->COLUMNA_cargo=Terminal_introdución->맨위=Terminal_introdución->desprazar=0;for(unsigned 반환값=0;반환값<Historial_liña_CONTAR;반환값++)빈칸채우기(반환값);if(보이는지())Contido_VALOR();}
static int crear_introdución(void){
    if(!보드화면기억공간())return -19;int 식별자=0;while(식별자<4&&Windows_Lista[식별자].살아있음)식별자++;if(식별자==4)return -28;
    escritorio_ver=1;Terminal_introdución=&Windows_Lista[식별자];memset(Terminal_introdución,0,sizeof(*Terminal_introdución));Terminal_introdución->살아있음=1;Terminal_introdución->너비=568;Terminal_introdución->높이=360;Terminal_introdución->COLUMNAS=68;Terminal_introdución->FILA_CONTAR=19;Terminal_introdución->X_coordenada=12+식별자*16;Terminal_introdución->Y_coordenada=48+식별자*18;Terminal_introdución->전경색=7;Terminal_introdución->가리개보임=1;
    for(unsigned 반환값=0;반환값<Historial_liña_CONTAR;반환값++)빈칸채우기(반환값);orde_VALOR[introdución_CONTAR++]=식별자;Foco=식별자;Tecnoloxía_da_información_TI_pendente|=1u<<(4+식별자);sinal_Foco();다시그리기();return 식별자+1;
}
static void peche_ventá(int 식별자){
    if(식별자<0||식별자>=4||!Windows_Lista[식별자].살아있음)return;Windows_Lista[식별자].살아있음=0;Tecnoloxía_da_información_TI_pendente|=1u<<(8+식별자);
    int ao_corrente_cargo=0;while(ao_corrente_cargo<introdución_CONTAR&&orde_VALOR[ao_corrente_cargo]!=식별자)ao_corrente_cargo++;for(;ao_corrente_cargo+1<introdución_CONTAR;ao_corrente_cargo++)orde_VALOR[ao_corrente_cargo]=orde_VALOR[ao_corrente_cargo+1];introdución_CONTAR--;
    if(Foco==식별자)Foco=introdución_CONTAR?orde_VALOR[introdución_CONTAR-1]:-1;sinal_Foco();다시그리기();
}
static void 줄바꿈(void){Terminal_introdución->COLUMNA_cargo=0;Terminal_introdución->FILA_cargo++;if(Terminal_introdución->FILA_cargo>=Terminal_introdución->맨위+Terminal_introdución->FILA_CONTAR){Terminal_introdución->맨위++;빈칸채우기(Terminal_introdución->FILA_cargo);if(보이는지())Contido_VALOR();}}
static void código_de_carácter_451f2815(unsigned código_de_carácter){
    if(código_de_carácter==13){Terminal_introdución->COLUMNA_cargo=0;return;}if(código_de_carácter==10){줄바꿈();return;}if(código_de_carácter==8){if(Terminal_introdución->COLUMNA_cargo)Terminal_introdución->COLUMNA_cargo--;return;}
    if(código_de_carácter==9){unsigned elemento_CONTAR=8-Terminal_introdución->COLUMNA_cargo%8;while(elemento_CONTAR--)código_de_carácter_451f2815(' ');return;}if(código_de_carácter<32||código_de_carácter==127)return;
    unsigned 너비값=넓은글자(código_de_carácter);if(Terminal_introdución->COLUMNA_cargo+너비값>Terminal_introdución->COLUMNAS)줄바꿈();
    if(Terminal_introdución->글자칸들[Terminal_introdución->FILA_cargo%Historial_liña_CONTAR][Terminal_introdución->COLUMNA_cargo]==0xffffffffu&&Terminal_introdución->COLUMNA_cargo){Terminal_introdución->글자칸들[Terminal_introdución->FILA_cargo%Historial_liña_CONTAR][Terminal_introdución->COLUMNA_cargo-1]=' ';그리기(Terminal_introdución->FILA_cargo,Terminal_introdución->COLUMNA_cargo-1);}
    if(넓은글자(Terminal_introdución->글자칸들[Terminal_introdución->FILA_cargo%Historial_liña_CONTAR][Terminal_introdución->COLUMNA_cargo])==2&&Terminal_introdución->COLUMNA_cargo+1<Terminal_introdución->COLUMNAS){Terminal_introdución->글자칸들[Terminal_introdución->FILA_cargo%Historial_liña_CONTAR][Terminal_introdución->COLUMNA_cargo+1]=' ';그리기(Terminal_introdución->FILA_cargo,Terminal_introdución->COLUMNA_cargo+1);}
    Terminal_introdución->글자칸들[Terminal_introdución->FILA_cargo%Historial_liña_CONTAR][Terminal_introdución->COLUMNA_cargo]=código_de_carácter;Terminal_introdución->모양들[Terminal_introdución->FILA_cargo%Historial_liña_CONTAR][Terminal_introdución->COLUMNA_cargo]=Terminal_introdución->전경색|(Terminal_introdución->배경색<<4);
    if(너비값==2)Terminal_introdución->글자칸들[Terminal_introdución->FILA_cargo%Historial_liña_CONTAR][Terminal_introdución->COLUMNA_cargo+1]=0xffffffffu;
    그리기(Terminal_introdución->FILA_cargo,Terminal_introdución->COLUMNA_cargo);Terminal_introdución->COLUMNA_cargo+=너비값;
}
static void agarradoira_control_SECUENCIA(unsigned código_de_carácter){
    unsigned elemento_CONTAR=Terminal_introdución->parámetro_VALOR[0]?Terminal_introdución->parámetro_VALOR[0]:1;
    if(código_de_carácter=='m')for(unsigned 순번=0;순번<=Terminal_introdución->parámetro_ÍNDICE;순번++){unsigned datos_cargo=Terminal_introdución->parámetro_VALOR[순번];if(!datos_cargo){Terminal_introdución->전경색=7;Terminal_introdución->배경색=0;}if(datos_cargo==1&&Terminal_introdución->전경색<8)Terminal_introdución->전경색+=8;if(datos_cargo==7){unsigned 유지=Terminal_introdución->전경색;Terminal_introdución->전경색=Terminal_introdución->배경색;Terminal_introdución->배경색=유지;}if(datos_cargo>=30&&datos_cargo<=37)Terminal_introdución->전경색=datos_cargo-30;if(datos_cargo>=90&&datos_cargo<=97)Terminal_introdución->전경색=datos_cargo-90+8;if(datos_cargo>=40&&datos_cargo<=47)Terminal_introdución->배경색=datos_cargo-40;if(datos_cargo>=100&&datos_cargo<=107)Terminal_introdución->배경색=datos_cargo-100+8;if(datos_cargo==39)Terminal_introdución->전경색=7;if(datos_cargo==49)Terminal_introdución->배경색=0;}
    if(código_de_carácter=='J'&&(Terminal_introdución->parámetro_VALOR[0]==2||Terminal_introdución->parámetro_VALOR[0]==3))desmarcar_Contido();
    if(código_de_carácter=='K'){unsigned 출발위치=Terminal_introdución->parámetro_VALOR[0]==2?0:Terminal_introdución->COLUMNA_cargo,도착위치=Terminal_introdución->parámetro_VALOR[0]==1?Terminal_introdución->COLUMNA_cargo+1:Terminal_introdución->COLUMNAS;if(Terminal_introdución->parámetro_VALOR[0]==1)출발위치=0;for(unsigned 순번=출발위치;순번<도착위치&&순번<Terminal_introdución->COLUMNAS;순번++){
        unsigned FILA_VALOR=Terminal_introdución->FILA_cargo%Historial_liña_CONTAR,carácter_VALOR=Terminal_introdución->글자칸들[FILA_VALOR][순번],forma_VALOR=Terminal_introdución->전경색|(Terminal_introdución->배경색<<4);
        /* 넓은 vi 화면에서도 이미 빈 칸의 tipo_de_letra_VALOR 화소를 되풀이해 칠하지 않는다. */
        int 바뀜=(carácter_VALOR!=0&&carácter_VALOR!=' ')||Terminal_introdución->모양들[FILA_VALOR][순번]!=forma_VALOR;
        Terminal_introdución->글자칸들[FILA_VALOR][순번]=' ';Terminal_introdución->모양들[FILA_VALOR][순번]=forma_VALOR;
        if(바뀜)그리기(Terminal_introdución->FILA_cargo,순번);
    }}
    if(código_de_carácter=='D')Terminal_introdución->COLUMNA_cargo=elemento_CONTAR>Terminal_introdución->COLUMNA_cargo?0:Terminal_introdución->COLUMNA_cargo-elemento_CONTAR;if(código_de_carácter=='C')Terminal_introdución->COLUMNA_cargo=Terminal_introdución->COLUMNA_cargo+elemento_CONTAR>=Terminal_introdución->COLUMNAS?Terminal_introdución->COLUMNAS-1:Terminal_introdución->COLUMNA_cargo+elemento_CONTAR;
    if(código_de_carácter=='G')Terminal_introdución->COLUMNA_cargo=elemento_CONTAR>Terminal_introdución->COLUMNAS?Terminal_introdución->COLUMNAS-1:elemento_CONTAR-1;if(código_de_carácter=='A')Terminal_introdución->FILA_cargo=elemento_CONTAR>Terminal_introdución->FILA_cargo-Terminal_introdución->맨위?Terminal_introdución->맨위:Terminal_introdución->FILA_cargo-elemento_CONTAR;
    if(código_de_carácter=='B')Terminal_introdución->FILA_cargo=Terminal_introdución->FILA_cargo+elemento_CONTAR>=Terminal_introdución->맨위+Terminal_introdución->FILA_CONTAR?Terminal_introdución->맨위+Terminal_introdución->FILA_CONTAR-1:Terminal_introdución->FILA_cargo+elemento_CONTAR;
    if(código_de_carácter=='H'||código_de_carácter=='f'){Terminal_introdución->FILA_cargo=Terminal_introdución->맨위+(elemento_CONTAR>Terminal_introdución->FILA_CONTAR?Terminal_introdución->FILA_CONTAR:elemento_CONTAR)-1;unsigned X_coordenada=Terminal_introdución->parámetro_VALOR[1]?Terminal_introdución->parámetro_VALOR[1]:1;Terminal_introdución->COLUMNA_cargo=(X_coordenada>Terminal_introdución->COLUMNAS?Terminal_introdución->COLUMNAS:X_coordenada)-1;}
    if(código_de_carácter=='s'){Terminal_introdución->저장행=Terminal_introdución->FILA_cargo;Terminal_introdución->저장열=Terminal_introdución->COLUMNA_cargo;}if(código_de_carácter=='u'){Terminal_introdución->FILA_cargo=Terminal_introdución->저장행;Terminal_introdución->COLUMNA_cargo=Terminal_introdución->저장열<Terminal_introdución->COLUMNAS?Terminal_introdución->저장열:Terminal_introdución->COLUMNAS-1;}
    if((código_de_carácter=='h'||código_de_carácter=='l')&&Terminal_introdución->parámetro_VALOR[0]==25)Terminal_introdución->가리개보임=código_de_carácter=='h';
}
void Terminal_byte(unsigned SEGUNDO_VALOR){
    Terminal_introdución=&Windows_Lista[출력결과];if(!Terminal_introdución->살아있음)return;acento_circunflexo_VALOR(0);if(Terminal_introdución->desprazar){Terminal_introdución->desprazar=0;if(보이는지())Contido_VALOR();}
    if(Terminal_introdución->탈출상태==1){Terminal_introdución->탈출상태=SEGUNDO_VALOR=='['?2:0;Terminal_introdución->parámetro_ÍNDICE=0;for(unsigned 순번=0;순번<4;순번++)Terminal_introdución->parámetro_VALOR[순번]=0;}
    else if(Terminal_introdución->탈출상태==2){if(SEGUNDO_VALOR=='?'){}else if(SEGUNDO_VALOR>='0'&&SEGUNDO_VALOR<='9'){if(Terminal_introdución->parámetro_VALOR[Terminal_introdución->parámetro_ÍNDICE]<10000)Terminal_introdución->parámetro_VALOR[Terminal_introdución->parámetro_ÍNDICE]=Terminal_introdución->parámetro_VALOR[Terminal_introdución->parámetro_ÍNDICE]*10+SEGUNDO_VALOR-'0';}else if(SEGUNDO_VALOR==';'&&Terminal_introdución->parámetro_ÍNDICE<3)Terminal_introdución->parámetro_ÍNDICE++;else{agarradoira_control_SECUENCIA(SEGUNDO_VALOR);Terminal_introdución->탈출상태=0;}}
    else if(SEGUNDO_VALOR==27){Terminal_introdución->긴부호없는값=0;Terminal_introdución->탈출상태=1;}else{
        if(Terminal_introdución->긴부호없는값&&(SEGUNDO_VALOR&0xc0)!=0x80){Terminal_introdución->긴부호없는값=0;código_de_carácter_451f2815(0xfffd);}
        if(Terminal_introdución->긴부호없는값){Terminal_introdución->부호없는결과=Terminal_introdución->부호없는결과*64+(SEGUNDO_VALOR&63);if(--Terminal_introdución->긴부호없는값==0)código_de_carácter_451f2815(Terminal_introdución->부호없는결과<Terminal_introdución->MENOR_VALOR||Terminal_introdución->부호없는결과>0x10ffff||(Terminal_introdución->부호없는결과>=0xd800&&Terminal_introdución->부호없는결과<=0xdfff)?0xfffd:Terminal_introdución->부호없는결과);}
        else if(SEGUNDO_VALOR<128)código_de_carácter_451f2815(SEGUNDO_VALOR);else if(SEGUNDO_VALOR>=0xc2&&SEGUNDO_VALOR<=0xf4){Terminal_introdución->긴부호없는값=SEGUNDO_VALOR<0xe0?1:SEGUNDO_VALOR<0xf0?2:3;Terminal_introdución->부호없는결과=SEGUNDO_VALOR&((1u<<(6-Terminal_introdución->긴부호없는값))-1);Terminal_introdución->MENOR_VALOR=Terminal_introdución->긴부호없는값==1?128:Terminal_introdución->긴부호없는값==2?2048:65536;}else código_de_carácter_451f2815(0xfffd);
    }acento_circunflexo_VALOR(1);
}
int Terminal_pendente(void){return Tecnoloxía_da_información_TI_pendente!=0;}
/* 모서리 ÍNDICE: 1 좌상, 2 우상, 3 좌하, 4 우하. */
static int redimensionar_arrastrar=-1,잡은모서리,잡은가로,잡은세로,처음가로,처음세로,처음너비,처음높이;
static int 가리킨창(int 가로,int Vertical_cargo) {
    for(int SECUENCIA_VALOR=introdución_CONTAR-1;SECUENCIA_VALOR>=0;SECUENCIA_VALOR--){
        int 식별자=orde_VALOR[SECUENCIA_VALOR];Terminal_d413d4bc *Xanela=&Windows_Lista[식별자];
        if(가로>=(int)Xanela->X_coordenada&&Vertical_cargo>=(int)Xanela->Y_coordenada&&
           가로<(int)(Xanela->X_coordenada+Xanela->너비)&&Vertical_cargo<(int)(Xanela->Y_coordenada+Xanela->높이))return 식별자;
    }return -1;
}
static int 모서리찾기(int 식별자,int 가로,int Vertical_cargo) {
    if(식별자<0)return 0;Terminal_d413d4bc *Xanela=&Windows_Lista[식별자];
    int 왼쪽=가로<(int)Xanela->X_coordenada+8,DEREITA=가로>=(int)(Xanela->X_coordenada+Xanela->너비)-8;
    int 위쪽=Vertical_cargo<(int)Xanela->Y_coordenada+8,아래쪽=Vertical_cargo>=(int)(Xanela->Y_coordenada+Xanela->높이)-8;
    return (왼쪽||DEREITA)&&(위쪽||아래쪽)?1+DEREITA+아래쪽*2:0;
}
static int 사이값(int VALOR,int 최소,int 최대){return VALOR<최소?최소:VALOR>최대?최대:VALOR;}
static void mover_redimensionar(int 가로,int Vertical_cargo) {
    Terminal_d413d4bc *Xanela=&Windows_Lista[redimensionar_arrastrar];int 왼쪽=처음가로,위쪽=처음세로,DEREITA=처음가로+처음너비,아래쪽=처음세로+처음높이;
    if(잡은모서리==1||잡은모서리==3)왼쪽=사이값(처음가로+가로-잡은가로,0,DEREITA-360);
    else DEREITA=사이값(처음가로+처음너비+가로-잡은가로,왼쪽+360,보드화면너비());
    if(잡은모서리<=2)위쪽=사이값(처음세로+Vertical_cargo-잡은세로,34,아래쪽-216);
    else 아래쪽=사이값(처음세로+처음높이+Vertical_cargo-잡은세로,위쪽+216,보드화면높이());
    unsigned COLUMNAS=(DEREITA-왼쪽-24)/8,FILA_CONTAR=(아래쪽-위쪽-56)/16;
    if(Xanela->COLUMNAS!=COLUMNAS||Xanela->FILA_CONTAR!=FILA_CONTAR){
        Xanela->크기바뀜=1;Xanela->COLUMNAS=COLUMNAS;Xanela->FILA_CONTAR=FILA_CONTAR;
        if(Xanela->COLUMNA_cargo>=COLUMNAS)Xanela->COLUMNA_cargo=COLUMNAS-1;
        if(Xanela->FILA_cargo>=Xanela->맨위+FILA_CONTAR)Xanela->맨위=Xanela->FILA_cargo-FILA_CONTAR+1;
        unsigned 한도=Xanela->맨위;if(한도>Historial_liña_CONTAR-FILA_CONTAR)한도=Historial_liña_CONTAR-FILA_CONTAR;
        if(Xanela->desprazar>한도)Xanela->desprazar=한도;
    }
    int 옛가로=Xanela->X_coordenada,옛세로=Xanela->Y_coordenada,옛폭=Xanela->너비,옛길이=Xanela->높이;
    if(옛가로==왼쪽&&옛세로==위쪽&&옛폭==DEREITA-왼쪽&&옛길이==아래쪽-위쪽)return;
    Xanela->X_coordenada=왼쪽;Xanela->Y_coordenada=위쪽;Xanela->너비=DEREITA-왼쪽;Xanela->높이=아래쪽-위쪽;
    창자리그리기(옛가로,옛세로,옛폭,옛길이,Xanela);
}
void Terminal_punteiro(unsigned Seguinte_elemento,int X_coordenada,int Y_coordenada){
    unsigned 눌림=Seguinte_elemento&~단추들;단추들=Seguinte_elemento;
    if(!escritorio_ver){arrastrar_VALOR=-1;redimensionar_arrastrar=-1;Panel_punteiro(X_coordenada,Y_coordenada,1);return;}
    if(!(Seguinte_elemento&1)){arrastrar_VALOR=-1;redimensionar_arrastrar=-1;}
    if(redimensionar_arrastrar>=0&&!Windows_Lista[redimensionar_arrastrar].살아있음)redimensionar_arrastrar=-1;
    if(arrastrar_VALOR>=0&&!Windows_Lista[arrastrar_VALOR].살아있음)arrastrar_VALOR=-1;
    if(redimensionar_arrastrar>=0){
        mover_redimensionar(X_coordenada,Y_coordenada);Panel_punteiro(X_coordenada,Y_coordenada,잡은모서리==1||잡은모서리==4?2:3);return;
    }
    Panel_punteiro(X_coordenada,Y_coordenada,1);
    if(arrastrar_VALOR>=0){
        Terminal_d413d4bc *Xanela=&Windows_Lista[arrastrar_VALOR];
        int 옛가로=Xanela->X_coordenada,옛세로=Xanela->Y_coordenada;
        Xanela->X_coordenada=사이값(X_coordenada-arrastrar_X,0,보드화면너비()-Xanela->너비);
        Xanela->Y_coordenada=사이값(Y_coordenada-arrastrar_Y,34,보드화면높이()-Xanela->높이);
        if(옛가로!=(int)Xanela->X_coordenada||옛세로!=(int)Xanela->Y_coordenada)창자리그리기(옛가로,옛세로,Xanela->너비,Xanela->높이,Xanela);
        return;
    }
    extern int 화면덮음(int,int,int);
    if(화면덮음(Foco,X_coordenada,Y_coordenada)){화면가리킴(Foco,눌림,X_coordenada,Y_coordenada);return;}
    int 식별자=가리킨창(X_coordenada,Y_coordenada),모서리=모서리찾기(식별자,X_coordenada,Y_coordenada);
    if(모서리)Panel_punteiro(X_coordenada,Y_coordenada,모서리==1||모서리==4?2:3);
    if(눌림&1){
        if(모서리){
            Terminal_d413d4bc *Xanela=&Windows_Lista[식별자];redimensionar_arrastrar=식별자;잡은모서리=모서리;잡은가로=X_coordenada;잡은세로=Y_coordenada;
            처음가로=Xanela->X_coordenada;처음세로=Xanela->Y_coordenada;처음너비=Xanela->너비;처음높이=Xanela->높이;
            if(식별자!=Foco)앞으로올리기(식별자);return;
        }
        if(Y_coordenada<32&&X_coordenada>=6&&X_coordenada<142){crear_introdución();return;}
        if(Y_coordenada<32&&X_coordenada>=154&&X_coordenada<602){앞으로올리기((X_coordenada-154)/112);return;}
        if(식별자>=0){
            Terminal_d413d4bc *Xanela=&Windows_Lista[식별자];
            if(Y_coordenada<(int)Xanela->Y_coordenada+30&&X_coordenada>=(int)(Xanela->X_coordenada+Xanela->너비)-32){peche_ventá(식별자);return;}
            if(식별자!=Foco)앞으로올리기(식별자);
            if(Y_coordenada<(int)Xanela->Y_coordenada+30){arrastrar_VALOR=식별자;arrastrar_X=X_coordenada-Xanela->X_coordenada;arrastrar_Y=Y_coordenada-Xanela->Y_coordenada;}return;
        }
    }
    if(Foco>=0&&(눌림&(8|16))){Terminal_introdución=&Windows_Lista[Foco];if(눌림&8){unsigned 한도=Terminal_introdución->맨위;if(한도>Historial_liña_CONTAR-Terminal_introdución->FILA_CONTAR)한도=Historial_liña_CONTAR-Terminal_introdución->FILA_CONTAR;Terminal_introdución->desprazar=Terminal_introdución->desprazar+9>한도?한도:Terminal_introdución->desprazar+9;}else Terminal_introdución->desprazar=Terminal_introdución->desprazar<9?0:Terminal_introdución->desprazar-9;다시그리기();}
}
void 터미널바로가기키(unsigned 누름값){if(누름값==1)crear_introdución();if(누름값==2&&introdución_CONTAR)앞으로올리기(orde_VALOR[0]);if(누름값==3)peche_ventá(Foco);}
máquina_Word Panel_Terminal(máquina_Word Acción){
    if(Acción==300){if(!Windows_Lista[출력결과].살아있음)return crear_introdución();escritorio_ver=1;다시그리기();return 0;}
    if(Acción==0){peche_ventá(Foco);return 0;}if(Acción==1)return (uint32_t)crear_introdución();if(Acción==2)return Foco>=0;
    if(Acción==9){escritorio_ver=0;return 0;}if(Acción==7)return introdución_CONTAR;if(Acción==10)return Foco+1;if(Acción==11)return 출력결과;
    if(Acción==13){Terminal_d413d4bc *Xanela=&Windows_Lista[출력결과];return Xanela->살아있음?(Xanela->FILA_CONTAR<<16)|Xanela->COLUMNAS:(19<<16)|68;}
    if(Acción==14){unsigned VALOR=Windows_Lista[출력결과].크기바뀜;Windows_Lista[출력결과].크기바뀜=0;return VALOR;}
    if(Acción==12){unsigned VALOR=Tecnoloxía_da_información_TI_pendente;Tecnoloxía_da_información_TI_pendente=0;return VALOR;}
    if(Acción>=20&&Acción<24)return Windows_Lista[Acción-20].살아있음;
    if(Acción>=100&&Acción<104){출력결과=Acción-100;Terminal_introdución=&Windows_Lista[출력결과];return 0;}
    if(Acción>=200&&Acción<204){앞으로올리기(Acción-200);return 0;}
    if(Acción==3){다시그리기();return 0;}Terminal_introdución=&Windows_Lista[출력결과];if(!Terminal_introdución->살아있음)return 0;
    if(Acción==4)desmarcar_Contido();if(Acción==5||Acción==6){unsigned 이전=단추들;Terminal_punteiro(Acción==5?8:16,0,0);단추들=이전;}return 1;
}
