#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* Small native peer layer for the explicitly supported Swing subset. */
#include <stdint.h>
#include <stddef.h>
extern uintptr_t fal_képpont(uintptr_t,uintptr_t,uintptr_t),fal_Terminál(uintptr_t);
extern void Terminál_betűkép(unsigned,unsigned,unsigned,unsigned,unsigned);
extern void *memset(void *,int,size_t);
typedef struct { int terület_ÉRTÉK,szülő,x_koordináta,Y_koordináta,너비값,높이값,보이는지,kézi_Navigáció,Navigáció_Policy;unsigned Szöveg[128],hossz_ÉRTÉK; } widget_Állapot;
static widget_Állapot 요소들[4][32];
static int Szűrt[4],esemény_Lista[4][16];static unsigned 첫항목[4],bejegyzés_DARAB[4],부호없는결과[4],긴부호없는값[4];
static void Esemény(int tulajdonos_objektum,int ÉRTÉK){if(bejegyzés_DARAB[tulajdonos_objektum]<16){esemény_Lista[tulajdonos_objektum][(첫항목[tulajdonos_objektum]+bejegyzés_DARAB[tulajdonos_objektum])%16]=ÉRTÉK;bejegyzés_DARAB[tulajdonos_objektum]++;}}
static widget_Állapot *elem_ÉRTÉK(int tulajdonos_objektum,int azonosító_ÉRTÉK){return tulajdonos_objektum>=0&&tulajdonos_objektum<4&&azonosító_ÉRTÉK>0&&azonosító_ÉRTÉK<=32&&요소들[tulajdonos_objektum][azonosító_ÉRTÉK-1].terület_ÉRTÉK?&요소들[tulajdonos_objektum][azonosító_ÉRTÉK-1]:0;}
static void 사각영역(int x_koordináta,int Y_koordináta,int 너비값,int 높이값,unsigned 색상){fal_téglalap_kitöltés(x_koordináta,Y_koordináta,너비값,높이값,색상);}
int 화면보임(int tulajdonos_objektum){if(tulajdonos_objektum<0||tulajdonos_objektum>=4)return 0;for(int 순번=0;순번<32;순번++)if(요소들[tulajdonos_objektum][순번].terület_ÉRTÉK==1&&요소들[tulajdonos_objektum][순번].보이는지)return 1;return 0;}
void 화면초기화(int tulajdonos_objektum){memset(요소들[tulajdonos_objektum],0,sizeof(요소들[tulajdonos_objektum]));bejegyzés_DARAB[tulajdonos_objektum]=첫항목[tulajdonos_objektum]=Szűrt[tulajdonos_objektum]=긴부호없는값[tulajdonos_objektum]=0;}
static void Pozíció(int tulajdonos_objektum,widget_Állapot *너비값,int *x_koordináta,int *Y_koordináta){*x_koordináta=너비값->x_koordináta;*Y_koordináta=너비값->Y_koordináta;int adat_pozíció=너비값->szülő;for(int cikk_DARAB=0;adat_pozíció&&cikk_DARAB<32;cikk_DARAB++){widget_Állapot *위쪽=elem_ÉRTÉK(tulajdonos_objektum,adat_pozíció);if(!위쪽)break;*x_koordináta+=위쪽->x_koordináta;*Y_koordináta+=위쪽->Y_koordináta+(위쪽->terület_ÉRTÉK==1?30:0);adat_pozíció=위쪽->szülő;}}
static int 표시됨(int tulajdonos_objektum,widget_Állapot *너비값){for(int cikk_DARAB=0;cikk_DARAB<32;cikk_DARAB++){if(!너비값->보이는지)return 0;if(너비값->terület_ÉRTÉK==1)return 1;너비값=elem_ÉRTÉK(tulajdonos_objektum,너비값->szülő);if(!너비값)return 0;}return 0;}
static void Szöveg(int x_koordináta,int Y_koordináta,widget_Állapot *너비값,int 최대값,unsigned 색상,unsigned 배경색){int aktuális_pozíció=0;for(unsigned 순번=0;순번<너비값->hossz_ÉRTÉK;순번++){unsigned karakterkódolás=너비값->Szöveg[순번],너비=karakterkódolás>=256?16:8;if(aktuális_pozíció+(int)너비>최대값)break;Terminál_betűkép(x_koordináta+aktuális_pozíció,Y_koordináta,karakterkódolás,색상,배경색);aktuális_pozíció+=너비;}}
void 화면다시그림(int tulajdonos_objektum){
    if(!화면보임(tulajdonos_objektum))return;
    for(int feldolgozás_rendel=1;feldolgozás_rendel<=5;feldolgozás_rendel++)for(int 순번=0;순번<32;순번++){
        widget_Állapot *너비값=&요소들[tulajdonos_objektum][순번];if(너비값->terület_ÉRTÉK!=feldolgozás_rendel||!표시됨(tulajdonos_objektum,너비값))continue;int x_koordináta,Y_koordináta;Pozíció(tulajdonos_objektum,너비값,&x_koordináta,&Y_koordináta);
        if(feldolgozás_rendel==1){사각영역(x_koordináta,Y_koordináta,너비값->너비값,너비값->높이값,0xeee9e0);사각영역(x_koordináta,Y_koordináta,너비값->너비값,30,0x905020);Szöveg(x_koordináta+10,Y_koordináta+7,너비값,너비값->너비값-50,0xffffff,0x905020);사각영역(x_koordináta+너비값->너비값-28,Y_koordináta+4,24,22,0x5555b8);Terminál_betűkép(x_koordináta+너비값->너비값-20,Y_koordináta+7,'X',0xffffff,0x5555b8);}
        if(feldolgozás_rendel==2)사각영역(x_koordináta,Y_koordináta,너비값->너비값,너비값->높이값,0xeee9e0);
        if(feldolgozás_rendel>=3){unsigned 배경색=feldolgozás_rendel==4?0xc0ab86:feldolgozás_rendel==5?0xffffff:0xeee9e0;if(feldolgozás_rendel!=3)사각영역(x_koordináta,Y_koordináta,너비값->너비값,너비값->높이값,배경색);Szöveg(x_koordináta+4,Y_koordináta+4,너비값,너비값->너비값-8,0x201a15,배경색);if(feldolgozás_rendel==5&&Szűrt[tulajdonos_objektum]==순번+1)사각영역(x_koordináta,Y_koordináta+너비값->높이값-2,너비값->너비값,2,0x905020);}
    }
}
int 화면덮음(int tulajdonos_objektum,int x_koordináta,int Y_koordináta){
    if(!화면보임(tulajdonos_objektum))return 0;
    for(int 순번=0;순번<32;순번++){
        widget_Állapot *Ablak=&요소들[tulajdonos_objektum][순번];
        if(Ablak->terület_ÉRTÉK==1&&Ablak->보이는지&&x_koordináta>=Ablak->x_koordináta&&Y_koordináta>=Ablak->Y_koordináta&&
           x_koordináta<Ablak->x_koordináta+Ablak->너비값&&Y_koordináta<Ablak->Y_koordináta+Ablak->높이값)return 1;
    }return 0;
}
int 화면가리킴(int tulajdonos_objektum,unsigned 눌림,int x_koordináta,int Y_koordináta){
    if(!화면보임(tulajdonos_objektum))return 0;
    if(눌림&1)for(int 순번=31;순번>=0;순번--){widget_Állapot *너비값=&요소들[tulajdonos_objektum][순번];if(!너비값->terület_ÉRTÉK||!표시됨(tulajdonos_objektum,너비값))continue;int ablak_X,ablak_Y;Pozíció(tulajdonos_objektum,너비값,&ablak_X,&ablak_Y);
        if(x_koordináta<ablak_X||Y_koordináta<ablak_Y||x_koordináta>=ablak_X+너비값->너비값||Y_koordináta>=ablak_Y+너비값->높이값)continue;
        if(너비값->terület_ÉRTÉK==1&&Y_koordináta<ablak_Y+30&&x_koordináta>=ablak_X+너비값->너비값-28){if(너비값->Navigáció_Policy!=0)너비값->보이는지=0;Esemény(tulajdonos_objektum,0x10000+순번+1);fal_Terminál(3);return 1;}
        if(너비값->terület_ÉRTÉK==4){Esemény(tulajdonos_objektum,순번+1);return 1;}if(너비값->terület_ÉRTÉK==5){Szűrt[tulajdonos_objektum]=순번+1;fal_Terminál(3);return 1;}
        if(너비값->terület_ÉRTÉK==1)return 1;
    }return 0;
}
void 화면누름(int tulajdonos_objektum,unsigned MPERC_ÉRTÉK){
    widget_Állapot *너비값=elem_ÉRTÉK(tulajdonos_objektum,Szűrt[tulajdonos_objektum]);if(!너비값||너비값->terület_ÉRTÉK!=5)return;
    if(MPERC_ÉRTÉK==13||MPERC_ÉRTÉK==10){Esemény(tulajdonos_objektum,Szűrt[tulajdonos_objektum]);return;}
    if(MPERC_ÉRTÉK==8||MPERC_ÉRTÉK==127){if(너비값->hossz_ÉRTÉK)너비값->hossz_ÉRTÉK--;긴부호없는값[tulajdonos_objektum]=0;}
    else{
        unsigned karakterkódolás=MPERC_ÉRTÉK;
        if(긴부호없는값[tulajdonos_objektum]){if((MPERC_ÉRTÉK&192)!=128){긴부호없는값[tulajdonos_objektum]=0;return;}부호없는결과[tulajdonos_objektum]=(부호없는결과[tulajdonos_objektum]<<6)|(MPERC_ÉRTÉK&63);if(--긴부호없는값[tulajdonos_objektum])return;karakterkódolás=부호없는결과[tulajdonos_objektum];}
        else if(MPERC_ÉRTÉK>=0xc2&&MPERC_ÉRTÉK<=0xf4){긴부호없는값[tulajdonos_objektum]=MPERC_ÉRTÉK<0xe0?1:MPERC_ÉRTÉK<0xf0?2:3;부호없는결과[tulajdonos_objektum]=MPERC_ÉRTÉK&((1u<<(6-긴부호없는값[tulajdonos_objektum]))-1);return;}
        else if(MPERC_ÉRTÉK<32||MPERC_ÉRTÉK>=128)return;
        if(karakterkódolás>0x10ffff||(karakterkódolás>=0xd800&&karakterkódolás<=0xdfff))return;if(너비값->hossz_ÉRTÉK<127)너비값->Szöveg[너비값->hossz_ÉRTÉK++]=karakterkódolás;
    }
    fal_Terminál(3);
}
int 화면호출(int tulajdonos_objektum,unsigned Művelet,int azonosító_ÉRTÉK,int 첫째값,int MPERC_ÉRTÉK,int kódpont,int cél_adat){
    if(tulajdonos_objektum<0||tulajdonos_objektum>=4)return -22;widget_Állapot *너비값=elem_ÉRTÉK(tulajdonos_objektum,azonosító_ÉRTÉK);
    if(Művelet==0){if(azonosító_ÉRTÉK<1||azonosító_ÉRTÉK>5)return -22;for(int 순번=0;순번<32;순번++)if(요소들[tulajdonos_objektum][순번].terület_ÉRTÉK==0){너비값=&요소들[tulajdonos_objektum][순번];memset(너비값,0,sizeof(*너비값));너비값->terület_ÉRTÉK=azonosító_ÉRTÉK;너비값->보이는지=azonosító_ÉRTÉK!=1;너비값->너비값=azonosító_ÉRTÉK==1?380:220;너비값->높이값=azonosító_ÉRTÉK==1?240:28;너비값->Navigáció_Policy=1;너비값->x_koordináta=azonosító_ÉRTÉK==1?130:16;너비값->Y_koordináta=azonosító_ÉRTÉK==1?110:16;return 순번+1;}return -28;}
    if(Művelet==5){if(!bejegyzés_DARAB[tulajdonos_objektum])return 0;int 반환값=esemény_Lista[tulajdonos_objektum][첫항목[tulajdonos_objektum]];첫항목[tulajdonos_objektum]=(첫항목[tulajdonos_objektum]+1)%16;bejegyzés_DARAB[tulajdonos_objektum]--;return 반환값;}
    if(Művelet==6)return 화면보임(tulajdonos_objektum);
    if(!너비값)return -9;
    int 이전표시=표시됨(tulajdonos_objektum,너비값);
    if(Művelet==1){int 바탕너비=보드화면너비(),바탕높이=보드화면높이();if(첫째값<0||MPERC_ÉRTÉK<0||kódpont<1||cél_adat<1||첫째값>바탕너비||MPERC_ÉRTÉK>바탕높이||kódpont>바탕너비-첫째값||cél_adat>바탕높이-MPERC_ÉRTÉK)return -22;너비값->x_koordináta=첫째값;너비값->Y_koordináta=MPERC_ÉRTÉK;너비값->너비값=kódpont;너비값->높이값=cél_adat;너비값->kézi_Navigáció=1;}
    else if(Művelet==2){widget_Állapot *gyermek=elem_ÉRTÉK(tulajdonos_objektum,첫째값);if(!gyermek||gyermek==너비값||gyermek->terület_ÉRTÉK==1)return -22;int adat_pozíció=azonosító_ÉRTÉK;for(int 깊이=0;adat_pozíció&&깊이<32;깊이++){if(adat_pozíció==첫째값)return -22;widget_Állapot *위쪽=elem_ÉRTÉK(tulajdonos_objektum,adat_pozíció);adat_pozíció=위쪽?위쪽->szülő:0;}gyermek->szülő=azonosító_ÉRTÉK;if(!gyermek->kézi_Navigáció){int 형제요소=0;for(int 순번=0;순번<32;순번++)if(&요소들[tulajdonos_objektum][순번]!=gyermek&&요소들[tulajdonos_objektum][순번].szülő==azonosító_ÉRTÉK)형제요소++;gyermek->Y_koordináta=16+형제요소*36;}}
    else if(Művelet==3)너비값->보이는지=첫째값!=0;
    else if(Művelet==4)너비값->보이는지=0;
    else if(Művelet==7)너비값->Navigáció_Policy=첫째값;
    else if(Művelet==8)return 너비값->hossz_ÉRTÉK;
    else if(Művelet==9)return 첫째값>=0&&(unsigned)첫째값<너비값->hossz_ÉRTÉK?너비값->Szöveg[첫째값]:-22;
    else return -22;
    if(이전표시||표시됨(tulajdonos_objektum,너비값))fal_Terminál(3);return 0;
}
int 화면글(int tulajdonos_objektum,int azonosító_ÉRTÉK,const uint32_t *adat,unsigned cikk_DARAB){widget_Állapot *너비값=elem_ÉRTÉK(tulajdonos_objektum,azonosító_ÉRTÉK);if(!너비값)return -9;if(cikk_DARAB>127)return -22;for(unsigned 순번=0;순번<cikk_DARAB;순번++){unsigned karakterkódolás=adat[순번];if(karakterkódolás>0x10ffff||(karakterkódolás>=0xd800&&karakterkódolás<=0xdfff))return -22;}for(unsigned 순번=0;순번<cikk_DARAB;순번++)너비값->Szöveg[순번]=adat[순번];너비값->hossz_ÉRTÉK=cikk_DARAB;if(표시됨(tulajdonos_objektum,너비값))fal_Terminál(3);return 0;}
