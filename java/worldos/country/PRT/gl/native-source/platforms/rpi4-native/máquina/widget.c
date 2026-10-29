#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* Small native peer layer for the explicitly supported Swing subset. */
#include <stdint.h>
#include <stddef.h>
extern uintptr_t Panel_píxel(uintptr_t,uintptr_t,uintptr_t),Panel_Terminal(uintptr_t);
extern void Terminal_glifo(unsigned,unsigned,unsigned,unsigned,unsigned);
extern void *memset(void *,int,size_t);
typedef struct { int Categoría_VALOR,부모항목,X_coordenada,Y_coordenada,너비값,높이값,보이는지,manual_deseño,deseño_política;unsigned Texto[128],duración_VALOR; } widget_Estado;
static widget_Estado 요소들[4][32];
static int Importantes[4],evento_Lista[4][16];static unsigned 첫항목[4],introdución_CONTAR[4],부호없는결과[4],긴부호없는값[4];
static void Evento(int propietario_obxecto,int VALOR){if(introdución_CONTAR[propietario_obxecto]<16){evento_Lista[propietario_obxecto][(첫항목[propietario_obxecto]+introdución_CONTAR[propietario_obxecto])%16]=VALOR;introdución_CONTAR[propietario_obxecto]++;}}
static widget_Estado *elemento_VALOR(int propietario_obxecto,int 식별자){return propietario_obxecto>=0&&propietario_obxecto<4&&식별자>0&&식별자<=32&&요소들[propietario_obxecto][식별자-1].Categoría_VALOR?&요소들[propietario_obxecto][식별자-1]:0;}
static void 사각영역(int X_coordenada,int Y_coordenada,int 너비값,int 높이값,unsigned 색상){보드사각그림(X_coordenada,Y_coordenada,너비값,높이값,색상);}
int 화면보임(int propietario_obxecto){if(propietario_obxecto<0||propietario_obxecto>=4)return 0;for(int 순번=0;순번<32;순번++)if(요소들[propietario_obxecto][순번].Categoría_VALOR==1&&요소들[propietario_obxecto][순번].보이는지)return 1;return 0;}
void 화면초기화(int propietario_obxecto){memset(요소들[propietario_obxecto],0,sizeof(요소들[propietario_obxecto]));introdución_CONTAR[propietario_obxecto]=첫항목[propietario_obxecto]=Importantes[propietario_obxecto]=긴부호없는값[propietario_obxecto]=0;}
static void Posición(int propietario_obxecto,widget_Estado *너비값,int *X_coordenada,int *Y_coordenada){*X_coordenada=너비값->X_coordenada;*Y_coordenada=너비값->Y_coordenada;int datos_cargo=너비값->부모항목;for(int elemento_CONTAR=0;datos_cargo&&elemento_CONTAR<32;elemento_CONTAR++){widget_Estado *위쪽=elemento_VALOR(propietario_obxecto,datos_cargo);if(!위쪽)break;*X_coordenada+=위쪽->X_coordenada;*Y_coordenada+=위쪽->Y_coordenada+(위쪽->Categoría_VALOR==1?30:0);datos_cargo=위쪽->부모항목;}}
static int 표시됨(int propietario_obxecto,widget_Estado *너비값){for(int elemento_CONTAR=0;elemento_CONTAR<32;elemento_CONTAR++){if(!너비값->보이는지)return 0;if(너비값->Categoría_VALOR==1)return 1;너비값=elemento_VALOR(propietario_obxecto,너비값->부모항목);if(!너비값)return 0;}return 0;}
static void Texto(int X_coordenada,int Y_coordenada,widget_Estado *너비값,int 최대값,unsigned 색상,unsigned 배경색){int ao_corrente_cargo=0;for(unsigned 순번=0;순번<너비값->duración_VALOR;순번++){unsigned carácter_codificación=너비값->Texto[순번],너비=carácter_codificación>=256?16:8;if(ao_corrente_cargo+(int)너비>최대값)break;Terminal_glifo(X_coordenada+ao_corrente_cargo,Y_coordenada,carácter_codificación,색상,배경색);ao_corrente_cargo+=너비;}}
void 화면다시그림(int propietario_obxecto){
    if(!화면보임(propietario_obxecto))return;
    for(int procesamento_orde=1;procesamento_orde<=5;procesamento_orde++)for(int 순번=0;순번<32;순번++){
        widget_Estado *너비값=&요소들[propietario_obxecto][순번];if(너비값->Categoría_VALOR!=procesamento_orde||!표시됨(propietario_obxecto,너비값))continue;int X_coordenada,Y_coordenada;Posición(propietario_obxecto,너비값,&X_coordenada,&Y_coordenada);
        if(procesamento_orde==1){사각영역(X_coordenada,Y_coordenada,너비값->너비값,너비값->높이값,0xeee9e0);사각영역(X_coordenada,Y_coordenada,너비값->너비값,30,0x905020);Texto(X_coordenada+10,Y_coordenada+7,너비값,너비값->너비값-50,0xffffff,0x905020);사각영역(X_coordenada+너비값->너비값-28,Y_coordenada+4,24,22,0x5555b8);Terminal_glifo(X_coordenada+너비값->너비값-20,Y_coordenada+7,'X',0xffffff,0x5555b8);}
        if(procesamento_orde==2)사각영역(X_coordenada,Y_coordenada,너비값->너비값,너비값->높이값,0xeee9e0);
        if(procesamento_orde>=3){unsigned 배경색=procesamento_orde==4?0xc0ab86:procesamento_orde==5?0xffffff:0xeee9e0;if(procesamento_orde!=3)사각영역(X_coordenada,Y_coordenada,너비값->너비값,너비값->높이값,배경색);Texto(X_coordenada+4,Y_coordenada+4,너비값,너비값->너비값-8,0x201a15,배경색);if(procesamento_orde==5&&Importantes[propietario_obxecto]==순번+1)사각영역(X_coordenada,Y_coordenada+너비값->높이값-2,너비값->너비값,2,0x905020);}
    }
}
int 화면덮음(int propietario_obxecto,int X_coordenada,int Y_coordenada){
    if(!화면보임(propietario_obxecto))return 0;
    for(int 순번=0;순번<32;순번++){
        widget_Estado *Xanela=&요소들[propietario_obxecto][순번];
        if(Xanela->Categoría_VALOR==1&&Xanela->보이는지&&X_coordenada>=Xanela->X_coordenada&&Y_coordenada>=Xanela->Y_coordenada&&
           X_coordenada<Xanela->X_coordenada+Xanela->너비값&&Y_coordenada<Xanela->Y_coordenada+Xanela->높이값)return 1;
    }return 0;
}
int 화면가리킴(int propietario_obxecto,unsigned 눌림,int X_coordenada,int Y_coordenada){
    if(!화면보임(propietario_obxecto))return 0;
    if(눌림&1)for(int 순번=31;순번>=0;순번--){widget_Estado *너비값=&요소들[propietario_obxecto][순번];if(!너비값->Categoría_VALOR||!표시됨(propietario_obxecto,너비값))continue;int ventá_X,ventá_Y;Posición(propietario_obxecto,너비값,&ventá_X,&ventá_Y);
        if(X_coordenada<ventá_X||Y_coordenada<ventá_Y||X_coordenada>=ventá_X+너비값->너비값||Y_coordenada>=ventá_Y+너비값->높이값)continue;
        if(너비값->Categoría_VALOR==1&&Y_coordenada<ventá_Y+30&&X_coordenada>=ventá_X+너비값->너비값-28){if(너비값->deseño_política!=0)너비값->보이는지=0;Evento(propietario_obxecto,0x10000+순번+1);Panel_Terminal(3);return 1;}
        if(너비값->Categoría_VALOR==4){Evento(propietario_obxecto,순번+1);return 1;}if(너비값->Categoría_VALOR==5){Importantes[propietario_obxecto]=순번+1;Panel_Terminal(3);return 1;}
        if(너비값->Categoría_VALOR==1)return 1;
    }return 0;
}
void 화면누름(int propietario_obxecto,unsigned SEGUNDO_VALOR){
    widget_Estado *너비값=elemento_VALOR(propietario_obxecto,Importantes[propietario_obxecto]);if(!너비값||너비값->Categoría_VALOR!=5)return;
    if(SEGUNDO_VALOR==13||SEGUNDO_VALOR==10){Evento(propietario_obxecto,Importantes[propietario_obxecto]);return;}
    if(SEGUNDO_VALOR==8||SEGUNDO_VALOR==127){if(너비값->duración_VALOR)너비값->duración_VALOR--;긴부호없는값[propietario_obxecto]=0;}
    else{
        unsigned carácter_codificación=SEGUNDO_VALOR;
        if(긴부호없는값[propietario_obxecto]){if((SEGUNDO_VALOR&192)!=128){긴부호없는값[propietario_obxecto]=0;return;}부호없는결과[propietario_obxecto]=(부호없는결과[propietario_obxecto]<<6)|(SEGUNDO_VALOR&63);if(--긴부호없는값[propietario_obxecto])return;carácter_codificación=부호없는결과[propietario_obxecto];}
        else if(SEGUNDO_VALOR>=0xc2&&SEGUNDO_VALOR<=0xf4){긴부호없는값[propietario_obxecto]=SEGUNDO_VALOR<0xe0?1:SEGUNDO_VALOR<0xf0?2:3;부호없는결과[propietario_obxecto]=SEGUNDO_VALOR&((1u<<(6-긴부호없는값[propietario_obxecto]))-1);return;}
        else if(SEGUNDO_VALOR<32||SEGUNDO_VALOR>=128)return;
        if(carácter_codificación>0x10ffff||(carácter_codificación>=0xd800&&carácter_codificación<=0xdfff))return;if(너비값->duración_VALOR<127)너비값->Texto[너비값->duración_VALOR++]=carácter_codificación;
    }
    Panel_Terminal(3);
}
int 화면호출(int propietario_obxecto,unsigned Acción,int 식별자,int 첫째값,int SEGUNDO_VALOR,int código_de_carácter,int destino_datos){
    if(propietario_obxecto<0||propietario_obxecto>=4)return -22;widget_Estado *너비값=elemento_VALOR(propietario_obxecto,식별자);
    if(Acción==0){if(식별자<1||식별자>5)return -22;for(int 순번=0;순번<32;순번++)if(요소들[propietario_obxecto][순번].Categoría_VALOR==0){너비값=&요소들[propietario_obxecto][순번];memset(너비값,0,sizeof(*너비값));너비값->Categoría_VALOR=식별자;너비값->보이는지=식별자!=1;너비값->너비값=식별자==1?380:220;너비값->높이값=식별자==1?240:28;너비값->deseño_política=1;너비값->X_coordenada=식별자==1?130:16;너비값->Y_coordenada=식별자==1?110:16;return 순번+1;}return -28;}
    if(Acción==5){if(!introdución_CONTAR[propietario_obxecto])return 0;int 반환값=evento_Lista[propietario_obxecto][첫항목[propietario_obxecto]];첫항목[propietario_obxecto]=(첫항목[propietario_obxecto]+1)%16;introdución_CONTAR[propietario_obxecto]--;return 반환값;}
    if(Acción==6)return 화면보임(propietario_obxecto);
    if(!너비값)return -9;
    int 이전표시=표시됨(propietario_obxecto,너비값);
    if(Acción==1){int 바탕너비=보드화면너비(),바탕높이=보드화면높이();if(첫째값<0||SEGUNDO_VALOR<0||código_de_carácter<1||destino_datos<1||첫째값>바탕너비||SEGUNDO_VALOR>바탕높이||código_de_carácter>바탕너비-첫째값||destino_datos>바탕높이-SEGUNDO_VALOR)return -22;너비값->X_coordenada=첫째값;너비값->Y_coordenada=SEGUNDO_VALOR;너비값->너비값=código_de_carácter;너비값->높이값=destino_datos;너비값->manual_deseño=1;}
    else if(Acción==2){widget_Estado *elemento_secundario=elemento_VALOR(propietario_obxecto,첫째값);if(!elemento_secundario||elemento_secundario==너비값||elemento_secundario->Categoría_VALOR==1)return -22;int datos_cargo=식별자;for(int 깊이=0;datos_cargo&&깊이<32;깊이++){if(datos_cargo==첫째값)return -22;widget_Estado *위쪽=elemento_VALOR(propietario_obxecto,datos_cargo);datos_cargo=위쪽?위쪽->부모항목:0;}elemento_secundario->부모항목=식별자;if(!elemento_secundario->manual_deseño){int 형제요소=0;for(int 순번=0;순번<32;순번++)if(&요소들[propietario_obxecto][순번]!=elemento_secundario&&요소들[propietario_obxecto][순번].부모항목==식별자)형제요소++;elemento_secundario->Y_coordenada=16+형제요소*36;}}
    else if(Acción==3)너비값->보이는지=첫째값!=0;
    else if(Acción==4)너비값->보이는지=0;
    else if(Acción==7)너비값->deseño_política=첫째값;
    else if(Acción==8)return 너비값->duración_VALOR;
    else if(Acción==9)return 첫째값>=0&&(unsigned)첫째값<너비값->duración_VALOR?너비값->Texto[첫째값]:-22;
    else return -22;
    if(이전표시||표시됨(propietario_obxecto,너비값))Panel_Terminal(3);return 0;
}
int 화면글(int propietario_obxecto,int 식별자,const uint32_t *datos,unsigned elemento_CONTAR){widget_Estado *너비값=elemento_VALOR(propietario_obxecto,식별자);if(!너비값)return -9;if(elemento_CONTAR>127)return -22;for(unsigned 순번=0;순번<elemento_CONTAR;순번++){unsigned carácter_codificación=datos[순번];if(carácter_codificación>0x10ffff||(carácter_codificación>=0xd800&&carácter_codificación<=0xdfff))return -22;}for(unsigned 순번=0;순번<elemento_CONTAR;순번++)너비값->Texto[순번]=datos[순번];너비값->duración_VALOR=elemento_CONTAR;if(표시됨(propietario_obxecto,너비값))Panel_Terminal(3);return 0;}
