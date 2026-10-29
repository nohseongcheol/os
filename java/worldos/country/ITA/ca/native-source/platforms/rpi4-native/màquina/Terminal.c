#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* propi 네 Finestra 합성과 UTF-8 Terminal. 바뀐 영역의 Completades_VALOR 그림만 표시한다. */
#include <stdint.h>
#include <stddef.h>
typedef uintptr_t màquina_Word;
extern màquina_Word Tauler_píxel(màquina_Word,màquina_Word,màquina_Word),보드화면기억공간(void);
extern void *memset(void *,int,size_t);
extern const unsigned char Terminal_tipus_de_lletra[];
#define 최대열수 237
#define Historial_línia_COMPT 160
typedef struct {
    uint32_t 글자칸들[Historial_línia_COMPT][최대열수]; uint8_t 모양들[Historial_línia_COMPT][최대열수];
    unsigned 너비,높이,COLUMNES,FILA_COMPT,크기바뀜;
    unsigned 살아있음,X_coordenada,Y_coordenada,FILA_càrrec,COLUMNA_càrrec,맨위,desplaçar,전경색,배경색,탈출상태,paràmetre_VALOR[4],paràmetre_INDEX,저장행,저장열;
    unsigned 부호없는결과,긴부호없는값,MENOR_VALOR,대체화면,가리개보임;
} Terminal_d413d4bc;
static Terminal_d413d4bc Windows_Llista[4];
static int Focus=-1,출력결과,comanda_VALOR[4],introducció_COMPT,arrossegar_VALOR=-1,arrossegar_X,arrossegar_Y;
static unsigned tecnologies_de_la_informació_pendent,단추들,escriptori_visualitzar,한글입력;
static const uint32_t 색상들[16]={0x201a15,0x6060df,0x9dcc86,0x80cfea,0xefaf72,0xca96c9,0xceda76,0xede9df,0x858078,0x8888ff,0xb9eba7,0xa5eaff,0xffcc99,0xf0bef1,0xf0f0a0,0xffffff};
extern int 화면보임(int),화면가리킴(int,unsigned,int,int);
extern void 화면다시그림(int);
static Terminal_d413d4bc *Terminal_introducció;
static unsigned 넓은글자(unsigned codi_de_caràcter){return codi_de_caràcter>=256?2:1;}
static void 사각영역(unsigned X_coordenada,unsigned Y_coordenada,unsigned 너비값,unsigned 높이값,unsigned 색상){
    보드사각그림(X_coordenada,Y_coordenada,너비값,높이값,색상);
}
void 터미널글자그림(unsigned X_coordenada,unsigned Y_coordenada,unsigned codi_de_caràcter,unsigned 전경색,unsigned 배경색){
    unsigned 너비=넓은글자(codi_de_caràcter)*8;if(codi_de_caràcter==0xffffffffu)return;
    int 왼쪽=X_coordenada,위쪽=Y_coordenada,폭=너비,durada_VALOR=16;
    if(!보드그림범위(&왼쪽,&위쪽,&폭,&durada_VALOR))return;
    if(codi_de_caràcter==' '){보드사각그림(왼쪽,위쪽,폭,durada_VALOR,배경색);return;}
    unsigned Cerca_INDEX=codi_de_caràcter<65536?codi_de_caràcter:codi_de_caràcter>=0x1f600&&codi_de_caràcter<0x1f650?65536+codi_de_caràcter-0x1f600:0xfffd;
    const unsigned char *tipus_de_lletra_VALOR=Terminal_tipus_de_lletra+Cerca_INDEX*32;
    for(int línia=위쪽;línia<위쪽+durada_VALOR;línia++){unsigned Servei_de_transferència_intel_ligent_en_segon_terme_Llista=tipus_de_lletra_VALOR[(línia-Y_coordenada)*2]*256+tipus_de_lletra_VALOR[(línia-Y_coordenada)*2+1];for(int 칸=왼쪽;칸<왼쪽+폭;칸++)Tauler_píxel(칸,línia,(Servei_de_transferència_intel_ligent_en_segon_terme_Llista&(0x8000>>(칸-X_coordenada)))?전경색:배경색);}
}
static void nom_taula(unsigned X_coordenada,unsigned Y_coordenada,const char *cadena_dades,unsigned 전경색,unsigned 배경색){while(*cadena_dades){unsigned codi_de_caràcter=(unsigned char)*cadena_dades++, 남은수=0;if(codi_de_caràcter>=0xc0){남은수=codi_de_caràcter<0xe0?1:codi_de_caràcter<0xf0?2:3;codi_de_caràcter&=(1u<<(6-남은수))-1;while(남은수--&&*cadena_dades)codi_de_caràcter=(codi_de_caràcter<<6)|((unsigned char)*cadena_dades++&63);}터미널글자그림(X_coordenada,Y_coordenada,codi_de_caràcter,전경색,배경색);X_coordenada+=넓은글자(codi_de_caràcter)*8;}}
static unsigned 첫항목(void){return Terminal_introducció->맨위;}
static int 보이는지(void){return Terminal_introducció->살아있음&&Focus>=0&&Terminal_introducció==&Windows_Llista[Focus]&&!화면보임(Focus);}
static void 그리기(unsigned FILA_càrrec,unsigned COLUMNA_càrrec){
    if(!보이는지()||FILA_càrrec<첫항목()-Terminal_introducció->desplaçar||FILA_càrrec>=첫항목()-Terminal_introducció->desplaçar+Terminal_introducció->FILA_COMPT||COLUMNA_càrrec>=Terminal_introducció->COLUMNES)return;
    unsigned codi_de_caràcter=Terminal_introducció->글자칸들[FILA_càrrec%Historial_línia_COMPT][COLUMNA_càrrec],cadena_dades=Terminal_introducció->모양들[FILA_càrrec%Historial_línia_COMPT][COLUMNA_càrrec];
    if(넓은글자(codi_de_caràcter)==2&&COLUMNA_càrrec+1>=Terminal_introducció->COLUMNES)codi_de_caràcter=' ';
    터미널글자그림(Terminal_introducció->X_coordenada+12+COLUMNA_càrrec*8,Terminal_introducció->Y_coordenada+36+(FILA_càrrec-첫항목()+Terminal_introducció->desplaçar)*16,codi_de_caràcter?codi_de_caràcter:' ',색상들[cadena_dades&15],색상들[cadena_dades>>4]);
}
static void accent_circumflex_VALOR(int mostrar_finestra){if(!보이는지()||Terminal_introducció->desplaçar||Terminal_introducció->COLUMNA_càrrec>=Terminal_introducció->COLUMNES||Terminal_introducció->FILA_càrrec<Terminal_introducció->맨위||Terminal_introducció->FILA_càrrec>=Terminal_introducció->맨위+Terminal_introducció->FILA_COMPT)return;
    if(!mostrar_finestra||!Terminal_introducció->가리개보임)그리기(Terminal_introducció->FILA_càrrec,Terminal_introducció->COLUMNA_càrrec);else 사각영역(Terminal_introducció->X_coordenada+12+Terminal_introducció->COLUMNA_càrrec*8,Terminal_introducció->Y_coordenada+36+(Terminal_introducció->FILA_càrrec-Terminal_introducció->맨위)*16+14,8,2,색상들[Terminal_introducció->전경색]);}
static void contingut_VALOR(void){
    사각영역(Terminal_introducció->X_coordenada+12,Terminal_introducció->Y_coordenada+36,Terminal_introducció->COLUMNES*8,Terminal_introducció->FILA_COMPT*16,색상들[0]);
    int 가로=Terminal_introducció->X_coordenada+12,Vertical_càrrec=Terminal_introducció->Y_coordenada+36,폭=Terminal_introducció->COLUMNES*8,durada_VALOR=Terminal_introducció->FILA_COMPT*16;
    if(보드그림범위(&가로,&Vertical_càrrec,&폭,&durada_VALOR)){
    unsigned 첫줄=(Vertical_càrrec-Terminal_introducció->Y_coordenada-36)/16,끝줄=(Vertical_càrrec+durada_VALOR-Terminal_introducció->Y_coordenada-36+15)/16;
    unsigned 첫칸=(가로-Terminal_introducció->X_coordenada-12)/8,끝칸=(가로+폭-Terminal_introducció->X_coordenada-12+7)/8;
    if(첫칸)첫칸--; /* 잘림 경계 왼쪽에서 시작한 두 칸 글자도 그린다. */
    for(unsigned 반환값=첫줄;반환값<끝줄;반환값++)for(unsigned codi_de_caràcter=첫칸;codi_de_caràcter<끝칸;codi_de_caràcter++){
        unsigned FILA_càrrec=첫항목()-Terminal_introducció->desplaçar+반환값,caràcter_VALOR=Terminal_introducció->글자칸들[FILA_càrrec%Historial_línia_COMPT][codi_de_caràcter],cadena_dades=Terminal_introducció->모양들[FILA_càrrec%Historial_línia_COMPT][codi_de_caràcter];
        if(넓은글자(caràcter_VALOR)==2&&codi_de_caràcter+1>=Terminal_introducció->COLUMNES)caràcter_VALOR=' ';
        if((caràcter_VALOR==0||caràcter_VALOR==' ')&&(cadena_dades>>4)==0)continue;
        터미널글자그림(Terminal_introducció->X_coordenada+12+codi_de_caràcter*8,Terminal_introducció->Y_coordenada+36+반환값*16,caràcter_VALOR?caràcter_VALOR:' ',색상들[cadena_dades&15],색상들[cadena_dades>>4]);
    }}
    nom_taula(Terminal_introducció->X_coordenada+12,Terminal_introducció->Y_coordenada+Terminal_introducció->높이-18,Terminal_introducció->desplaçar?"PgDn: recent output":Terminal_introducció->너비>=500?"F6: next | Corner + left drag: resize":"Corner + left drag: resize",0xece8e2,0x403127);accent_circumflex_VALOR(1);
}
static void 실행틀(int identificador_VALOR){
    Terminal_introducció=&Windows_Llista[identificador_VALOR];
    int 가로=Terminal_introducció->X_coordenada,Vertical_càrrec=Terminal_introducció->Y_coordenada,폭=Terminal_introducció->너비,durada_VALOR=Terminal_introducció->높이;
    if(!보드그림범위(&가로,&Vertical_càrrec,&폭,&durada_VALOR))return;
    사각영역(Terminal_introducció->X_coordenada,Terminal_introducció->Y_coordenada,Terminal_introducció->너비,Terminal_introducció->높이,0x403127);
    unsigned 색상=identificador_VALOR==Focus?0x905020:0x604438;사각영역(Terminal_introducció->X_coordenada,Terminal_introducció->Y_coordenada,Terminal_introducció->너비,30,색상);
    nom_taula(Terminal_introducció->X_coordenada+12,Terminal_introducció->Y_coordenada+7,"JKOROS Terminal",0xffffff,색상);
    char 수치[2]={(char)('1'+identificador_VALOR),0};nom_taula(Terminal_introducció->X_coordenada+148,Terminal_introducció->Y_coordenada+7,수치,0xffffff,색상);
    nom_taula(Terminal_introducció->X_coordenada+240,Terminal_introducció->Y_coordenada+7,Terminal_introducció->너비>=500?(한글입력?"[CA] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[CA]":"[EN]"),0xffffff,색상);
    사각영역(Terminal_introducció->X_coordenada+Terminal_introducció->너비-32,Terminal_introducció->Y_coordenada+4,26,22,0x5555b8);nom_taula(Terminal_introducció->X_coordenada+Terminal_introducció->너비-24,Terminal_introducció->Y_coordenada+7,"X",0xffffff,0x5555b8);
    contingut_VALOR();
}
static void Traç_escena(void){
    if(!escriptori_visualitzar)return;사각영역(0,0,보드화면너비(),보드화면높이(),0x302018);사각영역(0,0,보드화면너비(),32,0x403127);
    사각영역(6,4,136,24,0x905020);nom_taula(14,8,"+ New terminal",0xffffff,0x905020);
    for(int 순번=0;순번<4;순번++)if(Windows_Llista[순번].살아있음){unsigned codi_de_caràcter=Focus==순번?0x905020:0x604438;사각영역(154+순번*112,4,106,24,codi_de_caràcter);nom_taula(160+순번*112,8,"Terminal",0xffffff,codi_de_caràcter);char cadena_dades[2]={(char)('1'+순번),0};nom_taula(232+순번*112,8,cadena_dades,0xffffff,codi_de_caràcter);}
    if(!introducció_COMPT)nom_taula(140,210,"Click + New terminal to start",0xede9df,0x302018);
    for(int 순번=0;순번<introducció_COMPT;순번++)실행틀(comanda_VALOR[순번]);화면다시그림(Focus);Terminal_introducció=&Windows_Llista[출력결과];
}
static void 영역그리기(int 가로,int Vertical_càrrec,int 폭,int durada_VALOR){
    if(!escriptori_visualitzar||!보드그림범위(&가로,&Vertical_càrrec,&폭,&durada_VALOR))return;
    for(int línia=Vertical_càrrec;línia<Vertical_càrrec+durada_VALOR;línia+=32){
        int 띠높이=Vertical_càrrec+durada_VALOR-línia;if(띠높이>32)띠높이=32;
        if(Tauler_Inici_dibuix(가로,línia,폭,띠높이)){Traç_escena();Tauler_fi_dibuix();}
    }
}
static void 다시그리기(void){영역그리기(0,0,보드화면너비(),보드화면높이());}
/* 서로 겹치지 않는 새 Finestra 영역과 이전 자리의 네 띠를 복구한다. */
static void 창자리그리기(int 가로,int Vertical_càrrec,int 폭,int durada_VALOR,Terminal_d413d4bc *Finestra){
    int 왼쪽=가로>(int)Finestra->X_coordenada?가로:(int)Finestra->X_coordenada;
    int 위쪽=Vertical_càrrec>(int)Finestra->Y_coordenada?Vertical_càrrec:(int)Finestra->Y_coordenada;
    int DRETA=가로+폭<(int)(Finestra->X_coordenada+Finestra->너비)?가로+폭:(int)(Finestra->X_coordenada+Finestra->너비);
    int 아래쪽=Vertical_càrrec+durada_VALOR<(int)(Finestra->Y_coordenada+Finestra->높이)?Vertical_càrrec+durada_VALOR:(int)(Finestra->Y_coordenada+Finestra->높이);
    영역그리기(Finestra->X_coordenada,Finestra->Y_coordenada,Finestra->너비,Finestra->높이);
    if(왼쪽>=DRETA||위쪽>=아래쪽){영역그리기(가로,Vertical_càrrec,폭,durada_VALOR);return;}
    영역그리기(가로,Vertical_càrrec,폭,위쪽-Vertical_càrrec);
    영역그리기(가로,아래쪽,폭,Vertical_càrrec+durada_VALOR-아래쪽);
    영역그리기(가로,위쪽,왼쪽-가로,아래쪽-위쪽);
    영역그리기(DRETA,위쪽,가로+폭-DRETA,아래쪽-위쪽);
}
static void senyal_Focus(void){tecnologies_de_la_informació_pendent=(tecnologies_de_la_informació_pendent&~15u)|(unsigned)(Focus+1)|0x10000;}
void 터미널입력방식(unsigned 한글여부){
    한글입력=한글여부!=0;
    /* Update title bars only: a mode switch must not erase an EL0 drawing. */
    if(Focus>=0){
        Terminal_d413d4bc *finestra_introducció=&Windows_Llista[Focus];
        nom_taula(finestra_introducció->X_coordenada+240,finestra_introducció->Y_coordenada+7,finestra_introducció->너비>=500?(한글입력?"[CA] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[CA]":"[EN]"),0xffffff,0x905020);
    }
}
static void 앞으로올리기(int identificador_VALOR){if(identificador_VALOR<0||identificador_VALOR>=4||!Windows_Llista[identificador_VALOR].살아있음)return;int 현재위치=0;while(현재위치<introducció_COMPT&&comanda_VALOR[현재위치]!=identificador_VALOR)현재위치++;for(;현재위치+1<introducció_COMPT;현재위치++)comanda_VALOR[현재위치]=comanda_VALOR[현재위치+1];comanda_VALOR[introducció_COMPT-1]=identificador_VALOR;Focus=identificador_VALOR;senyal_Focus();다시그리기();}
static void 빈칸채우기(unsigned FILA_càrrec){for(unsigned codi_de_caràcter=0;codi_de_caràcter<최대열수;codi_de_caràcter++){Terminal_introducció->글자칸들[FILA_càrrec%Historial_línia_COMPT][codi_de_caràcter]=0;Terminal_introducció->모양들[FILA_càrrec%Historial_línia_COMPT][codi_de_caràcter]=Terminal_introducció->전경색|(Terminal_introducció->배경색<<4);}}
static void eliminar_Índex(void){Terminal_introducció->FILA_càrrec=Terminal_introducció->COLUMNA_càrrec=Terminal_introducció->맨위=Terminal_introducció->desplaçar=0;for(unsigned 반환값=0;반환값<Historial_línia_COMPT;반환값++)빈칸채우기(반환값);if(보이는지())contingut_VALOR();}
static int Crear_introducció(void){
    if(!보드화면기억공간())return -19;int identificador_VALOR=0;while(identificador_VALOR<4&&Windows_Llista[identificador_VALOR].살아있음)identificador_VALOR++;if(identificador_VALOR==4)return -28;
    escriptori_visualitzar=1;Terminal_introducció=&Windows_Llista[identificador_VALOR];memset(Terminal_introducció,0,sizeof(*Terminal_introducció));Terminal_introducció->살아있음=1;Terminal_introducció->너비=568;Terminal_introducció->높이=360;Terminal_introducció->COLUMNES=68;Terminal_introducció->FILA_COMPT=19;Terminal_introducció->X_coordenada=12+identificador_VALOR*16;Terminal_introducció->Y_coordenada=48+identificador_VALOR*18;Terminal_introducció->전경색=7;Terminal_introducció->가리개보임=1;
    for(unsigned 반환값=0;반환값<Historial_línia_COMPT;반환값++)빈칸채우기(반환값);comanda_VALOR[introducció_COMPT++]=identificador_VALOR;Focus=identificador_VALOR;tecnologies_de_la_informació_pendent|=1u<<(4+identificador_VALOR);senyal_Focus();다시그리기();return identificador_VALOR+1;
}
static void Tanca_finestra(int identificador_VALOR){
    if(identificador_VALOR<0||identificador_VALOR>=4||!Windows_Llista[identificador_VALOR].살아있음)return;Windows_Llista[identificador_VALOR].살아있음=0;tecnologies_de_la_informació_pendent|=1u<<(8+identificador_VALOR);
    int 현재위치=0;while(현재위치<introducció_COMPT&&comanda_VALOR[현재위치]!=identificador_VALOR)현재위치++;for(;현재위치+1<introducció_COMPT;현재위치++)comanda_VALOR[현재위치]=comanda_VALOR[현재위치+1];introducció_COMPT--;
    if(Focus==identificador_VALOR)Focus=introducció_COMPT?comanda_VALOR[introducció_COMPT-1]:-1;senyal_Focus();다시그리기();
}
static void 줄바꿈(void){Terminal_introducció->COLUMNA_càrrec=0;Terminal_introducció->FILA_càrrec++;if(Terminal_introducció->FILA_càrrec>=Terminal_introducció->맨위+Terminal_introducció->FILA_COMPT){Terminal_introducció->맨위++;빈칸채우기(Terminal_introducció->FILA_càrrec);if(보이는지())contingut_VALOR();}}
static void codi_de_caràcter_451f2815(unsigned codi_de_caràcter){
    if(codi_de_caràcter==13){Terminal_introducció->COLUMNA_càrrec=0;return;}if(codi_de_caràcter==10){줄바꿈();return;}if(codi_de_caràcter==8){if(Terminal_introducció->COLUMNA_càrrec)Terminal_introducció->COLUMNA_càrrec--;return;}
    if(codi_de_caràcter==9){unsigned element_COMPT=8-Terminal_introducció->COLUMNA_càrrec%8;while(element_COMPT--)codi_de_caràcter_451f2815(' ');return;}if(codi_de_caràcter<32||codi_de_caràcter==127)return;
    unsigned 너비값=넓은글자(codi_de_caràcter);if(Terminal_introducció->COLUMNA_càrrec+너비값>Terminal_introducció->COLUMNES)줄바꿈();
    if(Terminal_introducció->글자칸들[Terminal_introducció->FILA_càrrec%Historial_línia_COMPT][Terminal_introducció->COLUMNA_càrrec]==0xffffffffu&&Terminal_introducció->COLUMNA_càrrec){Terminal_introducció->글자칸들[Terminal_introducció->FILA_càrrec%Historial_línia_COMPT][Terminal_introducció->COLUMNA_càrrec-1]=' ';그리기(Terminal_introducció->FILA_càrrec,Terminal_introducció->COLUMNA_càrrec-1);}
    if(넓은글자(Terminal_introducció->글자칸들[Terminal_introducció->FILA_càrrec%Historial_línia_COMPT][Terminal_introducció->COLUMNA_càrrec])==2&&Terminal_introducció->COLUMNA_càrrec+1<Terminal_introducció->COLUMNES){Terminal_introducció->글자칸들[Terminal_introducció->FILA_càrrec%Historial_línia_COMPT][Terminal_introducció->COLUMNA_càrrec+1]=' ';그리기(Terminal_introducció->FILA_càrrec,Terminal_introducció->COLUMNA_càrrec+1);}
    Terminal_introducció->글자칸들[Terminal_introducció->FILA_càrrec%Historial_línia_COMPT][Terminal_introducció->COLUMNA_càrrec]=codi_de_caràcter;Terminal_introducció->모양들[Terminal_introducció->FILA_càrrec%Historial_línia_COMPT][Terminal_introducció->COLUMNA_càrrec]=Terminal_introducció->전경색|(Terminal_introducció->배경색<<4);
    if(너비값==2)Terminal_introducció->글자칸들[Terminal_introducció->FILA_càrrec%Historial_línia_COMPT][Terminal_introducció->COLUMNA_càrrec+1]=0xffffffffu;
    그리기(Terminal_introducció->FILA_càrrec,Terminal_introducció->COLUMNA_càrrec);Terminal_introducció->COLUMNA_càrrec+=너비값;
}
static void control_control_SEQÜÈNCIA(unsigned codi_de_caràcter){
    unsigned element_COMPT=Terminal_introducció->paràmetre_VALOR[0]?Terminal_introducció->paràmetre_VALOR[0]:1;
    if(codi_de_caràcter=='m')for(unsigned 순번=0;순번<=Terminal_introducció->paràmetre_INDEX;순번++){unsigned dades_càrrec=Terminal_introducció->paràmetre_VALOR[순번];if(!dades_càrrec){Terminal_introducció->전경색=7;Terminal_introducció->배경색=0;}if(dades_càrrec==1&&Terminal_introducció->전경색<8)Terminal_introducció->전경색+=8;if(dades_càrrec==7){unsigned 유지=Terminal_introducció->전경색;Terminal_introducció->전경색=Terminal_introducció->배경색;Terminal_introducció->배경색=유지;}if(dades_càrrec>=30&&dades_càrrec<=37)Terminal_introducció->전경색=dades_càrrec-30;if(dades_càrrec>=90&&dades_càrrec<=97)Terminal_introducció->전경색=dades_càrrec-90+8;if(dades_càrrec>=40&&dades_càrrec<=47)Terminal_introducció->배경색=dades_càrrec-40;if(dades_càrrec>=100&&dades_càrrec<=107)Terminal_introducció->배경색=dades_càrrec-100+8;if(dades_càrrec==39)Terminal_introducció->전경색=7;if(dades_càrrec==49)Terminal_introducció->배경색=0;}
    if(codi_de_caràcter=='J'&&(Terminal_introducció->paràmetre_VALOR[0]==2||Terminal_introducció->paràmetre_VALOR[0]==3))eliminar_Índex();
    if(codi_de_caràcter=='K'){unsigned 출발위치=Terminal_introducció->paràmetre_VALOR[0]==2?0:Terminal_introducció->COLUMNA_càrrec,도착위치=Terminal_introducció->paràmetre_VALOR[0]==1?Terminal_introducció->COLUMNA_càrrec+1:Terminal_introducció->COLUMNES;if(Terminal_introducció->paràmetre_VALOR[0]==1)출발위치=0;for(unsigned 순번=출발위치;순번<도착위치&&순번<Terminal_introducció->COLUMNES;순번++){
        unsigned FILA_VALOR=Terminal_introducció->FILA_càrrec%Historial_línia_COMPT,caràcter_VALOR=Terminal_introducció->글자칸들[FILA_VALOR][순번],forma_VALOR=Terminal_introducció->전경색|(Terminal_introducció->배경색<<4);
        /* 넓은 vi 화면에서도 이미 빈 칸의 tipus_de_lletra_VALOR 화소를 되풀이해 칠하지 않는다. */
        int 바뀜=(caràcter_VALOR!=0&&caràcter_VALOR!=' ')||Terminal_introducció->모양들[FILA_VALOR][순번]!=forma_VALOR;
        Terminal_introducció->글자칸들[FILA_VALOR][순번]=' ';Terminal_introducció->모양들[FILA_VALOR][순번]=forma_VALOR;
        if(바뀜)그리기(Terminal_introducció->FILA_càrrec,순번);
    }}
    if(codi_de_caràcter=='D')Terminal_introducció->COLUMNA_càrrec=element_COMPT>Terminal_introducció->COLUMNA_càrrec?0:Terminal_introducció->COLUMNA_càrrec-element_COMPT;if(codi_de_caràcter=='C')Terminal_introducció->COLUMNA_càrrec=Terminal_introducció->COLUMNA_càrrec+element_COMPT>=Terminal_introducció->COLUMNES?Terminal_introducció->COLUMNES-1:Terminal_introducció->COLUMNA_càrrec+element_COMPT;
    if(codi_de_caràcter=='G')Terminal_introducció->COLUMNA_càrrec=element_COMPT>Terminal_introducció->COLUMNES?Terminal_introducció->COLUMNES-1:element_COMPT-1;if(codi_de_caràcter=='A')Terminal_introducció->FILA_càrrec=element_COMPT>Terminal_introducció->FILA_càrrec-Terminal_introducció->맨위?Terminal_introducció->맨위:Terminal_introducció->FILA_càrrec-element_COMPT;
    if(codi_de_caràcter=='B')Terminal_introducció->FILA_càrrec=Terminal_introducció->FILA_càrrec+element_COMPT>=Terminal_introducció->맨위+Terminal_introducció->FILA_COMPT?Terminal_introducció->맨위+Terminal_introducció->FILA_COMPT-1:Terminal_introducció->FILA_càrrec+element_COMPT;
    if(codi_de_caràcter=='H'||codi_de_caràcter=='f'){Terminal_introducció->FILA_càrrec=Terminal_introducció->맨위+(element_COMPT>Terminal_introducció->FILA_COMPT?Terminal_introducció->FILA_COMPT:element_COMPT)-1;unsigned X_coordenada=Terminal_introducció->paràmetre_VALOR[1]?Terminal_introducció->paràmetre_VALOR[1]:1;Terminal_introducció->COLUMNA_càrrec=(X_coordenada>Terminal_introducció->COLUMNES?Terminal_introducció->COLUMNES:X_coordenada)-1;}
    if(codi_de_caràcter=='s'){Terminal_introducció->저장행=Terminal_introducció->FILA_càrrec;Terminal_introducció->저장열=Terminal_introducció->COLUMNA_càrrec;}if(codi_de_caràcter=='u'){Terminal_introducció->FILA_càrrec=Terminal_introducció->저장행;Terminal_introducció->COLUMNA_càrrec=Terminal_introducció->저장열<Terminal_introducció->COLUMNES?Terminal_introducció->저장열:Terminal_introducció->COLUMNES-1;}
    if((codi_de_caràcter=='h'||codi_de_caràcter=='l')&&Terminal_introducció->paràmetre_VALOR[0]==25)Terminal_introducció->가리개보임=codi_de_caràcter=='h';
}
void Terminal_byte(unsigned SEGON_VALOR){
    Terminal_introducció=&Windows_Llista[출력결과];if(!Terminal_introducció->살아있음)return;accent_circumflex_VALOR(0);if(Terminal_introducció->desplaçar){Terminal_introducció->desplaçar=0;if(보이는지())contingut_VALOR();}
    if(Terminal_introducció->탈출상태==1){Terminal_introducció->탈출상태=SEGON_VALOR=='['?2:0;Terminal_introducció->paràmetre_INDEX=0;for(unsigned 순번=0;순번<4;순번++)Terminal_introducció->paràmetre_VALOR[순번]=0;}
    else if(Terminal_introducció->탈출상태==2){if(SEGON_VALOR=='?'){}else if(SEGON_VALOR>='0'&&SEGON_VALOR<='9'){if(Terminal_introducció->paràmetre_VALOR[Terminal_introducció->paràmetre_INDEX]<10000)Terminal_introducció->paràmetre_VALOR[Terminal_introducció->paràmetre_INDEX]=Terminal_introducció->paràmetre_VALOR[Terminal_introducció->paràmetre_INDEX]*10+SEGON_VALOR-'0';}else if(SEGON_VALOR==';'&&Terminal_introducció->paràmetre_INDEX<3)Terminal_introducció->paràmetre_INDEX++;else{control_control_SEQÜÈNCIA(SEGON_VALOR);Terminal_introducció->탈출상태=0;}}
    else if(SEGON_VALOR==27){Terminal_introducció->긴부호없는값=0;Terminal_introducció->탈출상태=1;}else{
        if(Terminal_introducció->긴부호없는값&&(SEGON_VALOR&0xc0)!=0x80){Terminal_introducció->긴부호없는값=0;codi_de_caràcter_451f2815(0xfffd);}
        if(Terminal_introducció->긴부호없는값){Terminal_introducció->부호없는결과=Terminal_introducció->부호없는결과*64+(SEGON_VALOR&63);if(--Terminal_introducció->긴부호없는값==0)codi_de_caràcter_451f2815(Terminal_introducció->부호없는결과<Terminal_introducció->MENOR_VALOR||Terminal_introducció->부호없는결과>0x10ffff||(Terminal_introducció->부호없는결과>=0xd800&&Terminal_introducció->부호없는결과<=0xdfff)?0xfffd:Terminal_introducció->부호없는결과);}
        else if(SEGON_VALOR<128)codi_de_caràcter_451f2815(SEGON_VALOR);else if(SEGON_VALOR>=0xc2&&SEGON_VALOR<=0xf4){Terminal_introducció->긴부호없는값=SEGON_VALOR<0xe0?1:SEGON_VALOR<0xf0?2:3;Terminal_introducció->부호없는결과=SEGON_VALOR&((1u<<(6-Terminal_introducció->긴부호없는값))-1);Terminal_introducció->MENOR_VALOR=Terminal_introducció->긴부호없는값==1?128:Terminal_introducció->긴부호없는값==2?2048:65536;}else codi_de_caràcter_451f2815(0xfffd);
    }accent_circumflex_VALOR(1);
}
int Terminal_pendent(void){return tecnologies_de_la_informació_pendent!=0;}
/* 모서리 INDEX: 1 좌상, 2 우상, 3 좌하, 4 우하. */
static int redimensionar_arrossegar=-1,잡은모서리,잡은가로,잡은세로,처음가로,처음세로,처음너비,처음높이;
static int 가리킨창(int 가로,int Vertical_càrrec) {
    for(int SEQÜÈNCIA_VALOR=introducció_COMPT-1;SEQÜÈNCIA_VALOR>=0;SEQÜÈNCIA_VALOR--){
        int identificador_VALOR=comanda_VALOR[SEQÜÈNCIA_VALOR];Terminal_d413d4bc *Finestra=&Windows_Llista[identificador_VALOR];
        if(가로>=(int)Finestra->X_coordenada&&Vertical_càrrec>=(int)Finestra->Y_coordenada&&
           가로<(int)(Finestra->X_coordenada+Finestra->너비)&&Vertical_càrrec<(int)(Finestra->Y_coordenada+Finestra->높이))return identificador_VALOR;
    }return -1;
}
static int 모서리찾기(int identificador_VALOR,int 가로,int Vertical_càrrec) {
    if(identificador_VALOR<0)return 0;Terminal_d413d4bc *Finestra=&Windows_Llista[identificador_VALOR];
    int 왼쪽=가로<(int)Finestra->X_coordenada+8,DRETA=가로>=(int)(Finestra->X_coordenada+Finestra->너비)-8;
    int 위쪽=Vertical_càrrec<(int)Finestra->Y_coordenada+8,아래쪽=Vertical_càrrec>=(int)(Finestra->Y_coordenada+Finestra->높이)-8;
    return (왼쪽||DRETA)&&(위쪽||아래쪽)?1+DRETA+아래쪽*2:0;
}
static int 사이값(int VALOR,int 최소,int 최대){return VALOR<최소?최소:VALOR>최대?최대:VALOR;}
static void moure_redimensionar(int 가로,int Vertical_càrrec) {
    Terminal_d413d4bc *Finestra=&Windows_Llista[redimensionar_arrossegar];int 왼쪽=처음가로,위쪽=처음세로,DRETA=처음가로+처음너비,아래쪽=처음세로+처음높이;
    if(잡은모서리==1||잡은모서리==3)왼쪽=사이값(처음가로+가로-잡은가로,0,DRETA-360);
    else DRETA=사이값(처음가로+처음너비+가로-잡은가로,왼쪽+360,보드화면너비());
    if(잡은모서리<=2)위쪽=사이값(처음세로+Vertical_càrrec-잡은세로,34,아래쪽-216);
    else 아래쪽=사이값(처음세로+처음높이+Vertical_càrrec-잡은세로,위쪽+216,보드화면높이());
    unsigned COLUMNES=(DRETA-왼쪽-24)/8,FILA_COMPT=(아래쪽-위쪽-56)/16;
    if(Finestra->COLUMNES!=COLUMNES||Finestra->FILA_COMPT!=FILA_COMPT){
        Finestra->크기바뀜=1;Finestra->COLUMNES=COLUMNES;Finestra->FILA_COMPT=FILA_COMPT;
        if(Finestra->COLUMNA_càrrec>=COLUMNES)Finestra->COLUMNA_càrrec=COLUMNES-1;
        if(Finestra->FILA_càrrec>=Finestra->맨위+FILA_COMPT)Finestra->맨위=Finestra->FILA_càrrec-FILA_COMPT+1;
        unsigned 한도=Finestra->맨위;if(한도>Historial_línia_COMPT-FILA_COMPT)한도=Historial_línia_COMPT-FILA_COMPT;
        if(Finestra->desplaçar>한도)Finestra->desplaçar=한도;
    }
    int 옛가로=Finestra->X_coordenada,옛세로=Finestra->Y_coordenada,옛폭=Finestra->너비,옛길이=Finestra->높이;
    if(옛가로==왼쪽&&옛세로==위쪽&&옛폭==DRETA-왼쪽&&옛길이==아래쪽-위쪽)return;
    Finestra->X_coordenada=왼쪽;Finestra->Y_coordenada=위쪽;Finestra->너비=DRETA-왼쪽;Finestra->높이=아래쪽-위쪽;
    창자리그리기(옛가로,옛세로,옛폭,옛길이,Finestra);
}
void Terminal_punter(unsigned Següent_element,int X_coordenada,int Y_coordenada){
    unsigned 눌림=Següent_element&~단추들;단추들=Següent_element;
    if(!escriptori_visualitzar){arrossegar_VALOR=-1;redimensionar_arrossegar=-1;Tauler_punter(X_coordenada,Y_coordenada,1);return;}
    if(!(Següent_element&1)){arrossegar_VALOR=-1;redimensionar_arrossegar=-1;}
    if(redimensionar_arrossegar>=0&&!Windows_Llista[redimensionar_arrossegar].살아있음)redimensionar_arrossegar=-1;
    if(arrossegar_VALOR>=0&&!Windows_Llista[arrossegar_VALOR].살아있음)arrossegar_VALOR=-1;
    if(redimensionar_arrossegar>=0){
        moure_redimensionar(X_coordenada,Y_coordenada);Tauler_punter(X_coordenada,Y_coordenada,잡은모서리==1||잡은모서리==4?2:3);return;
    }
    Tauler_punter(X_coordenada,Y_coordenada,1);
    if(arrossegar_VALOR>=0){
        Terminal_d413d4bc *Finestra=&Windows_Llista[arrossegar_VALOR];
        int 옛가로=Finestra->X_coordenada,옛세로=Finestra->Y_coordenada;
        Finestra->X_coordenada=사이값(X_coordenada-arrossegar_X,0,보드화면너비()-Finestra->너비);
        Finestra->Y_coordenada=사이값(Y_coordenada-arrossegar_Y,34,보드화면높이()-Finestra->높이);
        if(옛가로!=(int)Finestra->X_coordenada||옛세로!=(int)Finestra->Y_coordenada)창자리그리기(옛가로,옛세로,Finestra->너비,Finestra->높이,Finestra);
        return;
    }
    extern int 화면덮음(int,int,int);
    if(화면덮음(Focus,X_coordenada,Y_coordenada)){화면가리킴(Focus,눌림,X_coordenada,Y_coordenada);return;}
    int identificador_VALOR=가리킨창(X_coordenada,Y_coordenada),모서리=모서리찾기(identificador_VALOR,X_coordenada,Y_coordenada);
    if(모서리)Tauler_punter(X_coordenada,Y_coordenada,모서리==1||모서리==4?2:3);
    if(눌림&1){
        if(모서리){
            Terminal_d413d4bc *Finestra=&Windows_Llista[identificador_VALOR];redimensionar_arrossegar=identificador_VALOR;잡은모서리=모서리;잡은가로=X_coordenada;잡은세로=Y_coordenada;
            처음가로=Finestra->X_coordenada;처음세로=Finestra->Y_coordenada;처음너비=Finestra->너비;처음높이=Finestra->높이;
            if(identificador_VALOR!=Focus)앞으로올리기(identificador_VALOR);return;
        }
        if(Y_coordenada<32&&X_coordenada>=6&&X_coordenada<142){Crear_introducció();return;}
        if(Y_coordenada<32&&X_coordenada>=154&&X_coordenada<602){앞으로올리기((X_coordenada-154)/112);return;}
        if(identificador_VALOR>=0){
            Terminal_d413d4bc *Finestra=&Windows_Llista[identificador_VALOR];
            if(Y_coordenada<(int)Finestra->Y_coordenada+30&&X_coordenada>=(int)(Finestra->X_coordenada+Finestra->너비)-32){Tanca_finestra(identificador_VALOR);return;}
            if(identificador_VALOR!=Focus)앞으로올리기(identificador_VALOR);
            if(Y_coordenada<(int)Finestra->Y_coordenada+30){arrossegar_VALOR=identificador_VALOR;arrossegar_X=X_coordenada-Finestra->X_coordenada;arrossegar_Y=Y_coordenada-Finestra->Y_coordenada;}return;
        }
    }
    if(Focus>=0&&(눌림&(8|16))){Terminal_introducció=&Windows_Llista[Focus];if(눌림&8){unsigned 한도=Terminal_introducció->맨위;if(한도>Historial_línia_COMPT-Terminal_introducció->FILA_COMPT)한도=Historial_línia_COMPT-Terminal_introducció->FILA_COMPT;Terminal_introducció->desplaçar=Terminal_introducció->desplaçar+9>한도?한도:Terminal_introducció->desplaçar+9;}else Terminal_introducció->desplaçar=Terminal_introducció->desplaçar<9?0:Terminal_introducció->desplaçar-9;다시그리기();}
}
void 터미널바로가기키(unsigned 누름값){if(누름값==1)Crear_introducció();if(누름값==2&&introducció_COMPT)앞으로올리기(comanda_VALOR[0]);if(누름값==3)Tanca_finestra(Focus);}
màquina_Word Tauler_Terminal(màquina_Word Acció){
    if(Acció==300){if(!Windows_Llista[출력결과].살아있음)return Crear_introducció();escriptori_visualitzar=1;다시그리기();return 0;}
    if(Acció==0){Tanca_finestra(Focus);return 0;}if(Acció==1)return (uint32_t)Crear_introducció();if(Acció==2)return Focus>=0;
    if(Acció==9){escriptori_visualitzar=0;return 0;}if(Acció==7)return introducció_COMPT;if(Acció==10)return Focus+1;if(Acció==11)return 출력결과;
    if(Acció==13){Terminal_d413d4bc *Finestra=&Windows_Llista[출력결과];return Finestra->살아있음?(Finestra->FILA_COMPT<<16)|Finestra->COLUMNES:(19<<16)|68;}
    if(Acció==14){unsigned VALOR=Windows_Llista[출력결과].크기바뀜;Windows_Llista[출력결과].크기바뀜=0;return VALOR;}
    if(Acció==12){unsigned VALOR=tecnologies_de_la_informació_pendent;tecnologies_de_la_informació_pendent=0;return VALOR;}
    if(Acció>=20&&Acció<24)return Windows_Llista[Acció-20].살아있음;
    if(Acció>=100&&Acció<104){출력결과=Acció-100;Terminal_introducció=&Windows_Llista[출력결과];return 0;}
    if(Acció>=200&&Acció<204){앞으로올리기(Acció-200);return 0;}
    if(Acció==3){다시그리기();return 0;}Terminal_introducció=&Windows_Llista[출력결과];if(!Terminal_introducció->살아있음)return 0;
    if(Acció==4)eliminar_Índex();if(Acció==5||Acció==6){unsigned 이전=단추들;Terminal_punter(Acció==5?8:16,0,0);단추들=이전;}return 1;
}
