#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* Small native peer layer for the explicitly supported Swing subset. */
#include <stdint.h>
#include <stddef.h>
extern uintptr_t Tauler_píxel(uintptr_t,uintptr_t,uintptr_t),Tauler_Terminal(uintptr_t);
extern void 터미널글자그림(unsigned,unsigned,unsigned,unsigned,unsigned);
extern void *memset(void *,int,size_t);
typedef struct { int Categoria_VALOR,부모항목,X_coordenada,Y_coordenada,너비값,높이값,보이는지,manual_disseny,disseny_norma;unsigned SMS[128],durada_VALOR; } giny_Estat;
static giny_Estat 요소들[4][32];
static int Prioritaris[4],incidència_Llista[4][16];static unsigned 첫항목[4],introducció_COMPT[4],부호없는결과[4],긴부호없는값[4];
static void Esdeveniment(int propietari_objecte,int VALOR){if(introducció_COMPT[propietari_objecte]<16){incidència_Llista[propietari_objecte][(첫항목[propietari_objecte]+introducció_COMPT[propietari_objecte])%16]=VALOR;introducció_COMPT[propietari_objecte]++;}}
static giny_Estat *element_VALOR(int propietari_objecte,int identificador_VALOR){return propietari_objecte>=0&&propietari_objecte<4&&identificador_VALOR>0&&identificador_VALOR<=32&&요소들[propietari_objecte][identificador_VALOR-1].Categoria_VALOR?&요소들[propietari_objecte][identificador_VALOR-1]:0;}
static void 사각영역(int X_coordenada,int Y_coordenada,int 너비값,int 높이값,unsigned 색상){보드사각그림(X_coordenada,Y_coordenada,너비값,높이값,색상);}
int 화면보임(int propietari_objecte){if(propietari_objecte<0||propietari_objecte>=4)return 0;for(int 순번=0;순번<32;순번++)if(요소들[propietari_objecte][순번].Categoria_VALOR==1&&요소들[propietari_objecte][순번].보이는지)return 1;return 0;}
void 화면초기화(int propietari_objecte){memset(요소들[propietari_objecte],0,sizeof(요소들[propietari_objecte]));introducció_COMPT[propietari_objecte]=첫항목[propietari_objecte]=Prioritaris[propietari_objecte]=긴부호없는값[propietari_objecte]=0;}
static void Posició(int propietari_objecte,giny_Estat *너비값,int *X_coordenada,int *Y_coordenada){*X_coordenada=너비값->X_coordenada;*Y_coordenada=너비값->Y_coordenada;int dades_càrrec=너비값->부모항목;for(int element_COMPT=0;dades_càrrec&&element_COMPT<32;element_COMPT++){giny_Estat *위쪽=element_VALOR(propietari_objecte,dades_càrrec);if(!위쪽)break;*X_coordenada+=위쪽->X_coordenada;*Y_coordenada+=위쪽->Y_coordenada+(위쪽->Categoria_VALOR==1?30:0);dades_càrrec=위쪽->부모항목;}}
static int 표시됨(int propietari_objecte,giny_Estat *너비값){for(int element_COMPT=0;element_COMPT<32;element_COMPT++){if(!너비값->보이는지)return 0;if(너비값->Categoria_VALOR==1)return 1;너비값=element_VALOR(propietari_objecte,너비값->부모항목);if(!너비값)return 0;}return 0;}
static void SMS(int X_coordenada,int Y_coordenada,giny_Estat *너비값,int 최대값,unsigned 색상,unsigned 배경색){int 현재위치=0;for(unsigned 순번=0;순번<너비값->durada_VALOR;순번++){unsigned caràcter_codificació=너비값->SMS[순번],너비=caràcter_codificació>=256?16:8;if(현재위치+(int)너비>최대값)break;터미널글자그림(X_coordenada+현재위치,Y_coordenada,caràcter_codificació,색상,배경색);현재위치+=너비;}}
void 화면다시그림(int propietari_objecte){
    if(!화면보임(propietari_objecte))return;
    for(int processament_comanda=1;processament_comanda<=5;processament_comanda++)for(int 순번=0;순번<32;순번++){
        giny_Estat *너비값=&요소들[propietari_objecte][순번];if(너비값->Categoria_VALOR!=processament_comanda||!표시됨(propietari_objecte,너비값))continue;int X_coordenada,Y_coordenada;Posició(propietari_objecte,너비값,&X_coordenada,&Y_coordenada);
        if(processament_comanda==1){사각영역(X_coordenada,Y_coordenada,너비값->너비값,너비값->높이값,0xeee9e0);사각영역(X_coordenada,Y_coordenada,너비값->너비값,30,0x905020);SMS(X_coordenada+10,Y_coordenada+7,너비값,너비값->너비값-50,0xffffff,0x905020);사각영역(X_coordenada+너비값->너비값-28,Y_coordenada+4,24,22,0x5555b8);터미널글자그림(X_coordenada+너비값->너비값-20,Y_coordenada+7,'X',0xffffff,0x5555b8);}
        if(processament_comanda==2)사각영역(X_coordenada,Y_coordenada,너비값->너비값,너비값->높이값,0xeee9e0);
        if(processament_comanda>=3){unsigned 배경색=processament_comanda==4?0xc0ab86:processament_comanda==5?0xffffff:0xeee9e0;if(processament_comanda!=3)사각영역(X_coordenada,Y_coordenada,너비값->너비값,너비값->높이값,배경색);SMS(X_coordenada+4,Y_coordenada+4,너비값,너비값->너비값-8,0x201a15,배경색);if(processament_comanda==5&&Prioritaris[propietari_objecte]==순번+1)사각영역(X_coordenada,Y_coordenada+너비값->높이값-2,너비값->너비값,2,0x905020);}
    }
}
int 화면덮음(int propietari_objecte,int X_coordenada,int Y_coordenada){
    if(!화면보임(propietari_objecte))return 0;
    for(int 순번=0;순번<32;순번++){
        giny_Estat *Finestra=&요소들[propietari_objecte][순번];
        if(Finestra->Categoria_VALOR==1&&Finestra->보이는지&&X_coordenada>=Finestra->X_coordenada&&Y_coordenada>=Finestra->Y_coordenada&&
           X_coordenada<Finestra->X_coordenada+Finestra->너비값&&Y_coordenada<Finestra->Y_coordenada+Finestra->높이값)return 1;
    }return 0;
}
int 화면가리킴(int propietari_objecte,unsigned 눌림,int X_coordenada,int Y_coordenada){
    if(!화면보임(propietari_objecte))return 0;
    if(눌림&1)for(int 순번=31;순번>=0;순번--){giny_Estat *너비값=&요소들[propietari_objecte][순번];if(!너비값->Categoria_VALOR||!표시됨(propietari_objecte,너비값))continue;int finestra_X,finestra_Y;Posició(propietari_objecte,너비값,&finestra_X,&finestra_Y);
        if(X_coordenada<finestra_X||Y_coordenada<finestra_Y||X_coordenada>=finestra_X+너비값->너비값||Y_coordenada>=finestra_Y+너비값->높이값)continue;
        if(너비값->Categoria_VALOR==1&&Y_coordenada<finestra_Y+30&&X_coordenada>=finestra_X+너비값->너비값-28){if(너비값->disseny_norma!=0)너비값->보이는지=0;Esdeveniment(propietari_objecte,0x10000+순번+1);Tauler_Terminal(3);return 1;}
        if(너비값->Categoria_VALOR==4){Esdeveniment(propietari_objecte,순번+1);return 1;}if(너비값->Categoria_VALOR==5){Prioritaris[propietari_objecte]=순번+1;Tauler_Terminal(3);return 1;}
        if(너비값->Categoria_VALOR==1)return 1;
    }return 0;
}
void 화면누름(int propietari_objecte,unsigned SEGON_VALOR){
    giny_Estat *너비값=element_VALOR(propietari_objecte,Prioritaris[propietari_objecte]);if(!너비값||너비값->Categoria_VALOR!=5)return;
    if(SEGON_VALOR==13||SEGON_VALOR==10){Esdeveniment(propietari_objecte,Prioritaris[propietari_objecte]);return;}
    if(SEGON_VALOR==8||SEGON_VALOR==127){if(너비값->durada_VALOR)너비값->durada_VALOR--;긴부호없는값[propietari_objecte]=0;}
    else{
        unsigned caràcter_codificació=SEGON_VALOR;
        if(긴부호없는값[propietari_objecte]){if((SEGON_VALOR&192)!=128){긴부호없는값[propietari_objecte]=0;return;}부호없는결과[propietari_objecte]=(부호없는결과[propietari_objecte]<<6)|(SEGON_VALOR&63);if(--긴부호없는값[propietari_objecte])return;caràcter_codificació=부호없는결과[propietari_objecte];}
        else if(SEGON_VALOR>=0xc2&&SEGON_VALOR<=0xf4){긴부호없는값[propietari_objecte]=SEGON_VALOR<0xe0?1:SEGON_VALOR<0xf0?2:3;부호없는결과[propietari_objecte]=SEGON_VALOR&((1u<<(6-긴부호없는값[propietari_objecte]))-1);return;}
        else if(SEGON_VALOR<32||SEGON_VALOR>=128)return;
        if(caràcter_codificació>0x10ffff||(caràcter_codificació>=0xd800&&caràcter_codificació<=0xdfff))return;if(너비값->durada_VALOR<127)너비값->SMS[너비값->durada_VALOR++]=caràcter_codificació;
    }
    Tauler_Terminal(3);
}
int 화면호출(int propietari_objecte,unsigned Acció,int identificador_VALOR,int 첫째값,int SEGON_VALOR,int codi_de_caràcter,int destinació_dades){
    if(propietari_objecte<0||propietari_objecte>=4)return -22;giny_Estat *너비값=element_VALOR(propietari_objecte,identificador_VALOR);
    if(Acció==0){if(identificador_VALOR<1||identificador_VALOR>5)return -22;for(int 순번=0;순번<32;순번++)if(요소들[propietari_objecte][순번].Categoria_VALOR==0){너비값=&요소들[propietari_objecte][순번];memset(너비값,0,sizeof(*너비값));너비값->Categoria_VALOR=identificador_VALOR;너비값->보이는지=identificador_VALOR!=1;너비값->너비값=identificador_VALOR==1?380:220;너비값->높이값=identificador_VALOR==1?240:28;너비값->disseny_norma=1;너비값->X_coordenada=identificador_VALOR==1?130:16;너비값->Y_coordenada=identificador_VALOR==1?110:16;return 순번+1;}return -28;}
    if(Acció==5){if(!introducció_COMPT[propietari_objecte])return 0;int 반환값=incidència_Llista[propietari_objecte][첫항목[propietari_objecte]];첫항목[propietari_objecte]=(첫항목[propietari_objecte]+1)%16;introducció_COMPT[propietari_objecte]--;return 반환값;}
    if(Acció==6)return 화면보임(propietari_objecte);
    if(!너비값)return -9;
    int 이전표시=표시됨(propietari_objecte,너비값);
    if(Acció==1){int 바탕너비=보드화면너비(),바탕높이=보드화면높이();if(첫째값<0||SEGON_VALOR<0||codi_de_caràcter<1||destinació_dades<1||첫째값>바탕너비||SEGON_VALOR>바탕높이||codi_de_caràcter>바탕너비-첫째값||destinació_dades>바탕높이-SEGON_VALOR)return -22;너비값->X_coordenada=첫째값;너비값->Y_coordenada=SEGON_VALOR;너비값->너비값=codi_de_caràcter;너비값->높이값=destinació_dades;너비값->manual_disseny=1;}
    else if(Acció==2){giny_Estat *element_secundari=element_VALOR(propietari_objecte,첫째값);if(!element_secundari||element_secundari==너비값||element_secundari->Categoria_VALOR==1)return -22;int dades_càrrec=identificador_VALOR;for(int 깊이=0;dades_càrrec&&깊이<32;깊이++){if(dades_càrrec==첫째값)return -22;giny_Estat *위쪽=element_VALOR(propietari_objecte,dades_càrrec);dades_càrrec=위쪽?위쪽->부모항목:0;}element_secundari->부모항목=identificador_VALOR;if(!element_secundari->manual_disseny){int 형제요소=0;for(int 순번=0;순번<32;순번++)if(&요소들[propietari_objecte][순번]!=element_secundari&&요소들[propietari_objecte][순번].부모항목==identificador_VALOR)형제요소++;element_secundari->Y_coordenada=16+형제요소*36;}}
    else if(Acció==3)너비값->보이는지=첫째값!=0;
    else if(Acció==4)너비값->보이는지=0;
    else if(Acció==7)너비값->disseny_norma=첫째값;
    else if(Acció==8)return 너비값->durada_VALOR;
    else if(Acció==9)return 첫째값>=0&&(unsigned)첫째값<너비값->durada_VALOR?너비값->SMS[첫째값]:-22;
    else return -22;
    if(이전표시||표시됨(propietari_objecte,너비값))Tauler_Terminal(3);return 0;
}
int 화면글(int propietari_objecte,int identificador_VALOR,const uint32_t *dades,unsigned element_COMPT){giny_Estat *너비값=element_VALOR(propietari_objecte,identificador_VALOR);if(!너비값)return -9;if(element_COMPT>127)return -22;for(unsigned 순번=0;순번<element_COMPT;순번++){unsigned caràcter_codificació=dades[순번];if(caràcter_codificació>0x10ffff||(caràcter_codificació>=0xd800&&caràcter_codificació<=0xdfff))return -22;}for(unsigned 순번=0;순번<element_COMPT;순번++)너비값->SMS[순번]=dades[순번];너비값->durada_VALOR=element_COMPT;if(표시됨(propietari_objecte,너비값))Tauler_Terminal(3);return 0;}
