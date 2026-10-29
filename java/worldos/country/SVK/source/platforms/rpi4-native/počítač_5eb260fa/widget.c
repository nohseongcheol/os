#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* Small native peer layer for the explicitly supported Swing subset. */
#include <stdint.h>
#include <stddef.h>
extern uintptr_t Panel_pixel(uintptr_t,uintptr_t,uintptr_t),Panel_Terminál(uintptr_t);
extern void Terminál_piktogram(unsigned,unsigned,unsigned,unsigned,unsigned);
extern void *memset(void *,int,size_t);
typedef struct { int oblasť_VALUE,nadradený,X_súradnica,Y_súradnica,너비값,높이값,보이는지,manuálny_Navigácia,Navigácia_politika;unsigned Spracovanie_textu[128],dĺžka_VALUE; } widget_Stav;
static widget_Stav 요소들[4][32];
static int Prioritné[4],udalosť_Zoznam[4][16];static unsigned 첫항목[4],položka_COUNT_8f7753a1[4],부호없는결과[4],긴부호없는값[4];
static void Udalosť(int vlastník_objekt,int VALUE){if(položka_COUNT_8f7753a1[vlastník_objekt]<16){udalosť_Zoznam[vlastník_objekt][(첫항목[vlastník_objekt]+položka_COUNT_8f7753a1[vlastník_objekt])%16]=VALUE;položka_COUNT_8f7753a1[vlastník_objekt]++;}}
static widget_Stav *prvok_VALUE(int vlastník_objekt,int identifikátor_VALUE){return vlastník_objekt>=0&&vlastník_objekt<4&&identifikátor_VALUE>0&&identifikátor_VALUE<=32&&요소들[vlastník_objekt][identifikátor_VALUE-1].oblasť_VALUE?&요소들[vlastník_objekt][identifikátor_VALUE-1]:0;}
static void 사각영역(int X_súradnica,int Y_súradnica,int 너비값,int 높이값,unsigned 색상){Panel_obdĺžnik_výplň(X_súradnica,Y_súradnica,너비값,높이값,색상);}
int 화면보임(int vlastník_objekt){if(vlastník_objekt<0||vlastník_objekt>=4)return 0;for(int 순번=0;순번<32;순번++)if(요소들[vlastník_objekt][순번].oblasť_VALUE==1&&요소들[vlastník_objekt][순번].보이는지)return 1;return 0;}
void 화면초기화(int vlastník_objekt){memset(요소들[vlastník_objekt],0,sizeof(요소들[vlastník_objekt]));položka_COUNT_8f7753a1[vlastník_objekt]=첫항목[vlastník_objekt]=Prioritné[vlastník_objekt]=긴부호없는값[vlastník_objekt]=0;}
static void Pozícia(int vlastník_objekt,widget_Stav *너비값,int *X_súradnica,int *Y_súradnica){*X_súradnica=너비값->X_súradnica;*Y_súradnica=너비값->Y_súradnica;int údaje_pozícia=너비값->nadradený;for(int položka_COUNT=0;údaje_pozícia&&položka_COUNT<32;položka_COUNT++){widget_Stav *위쪽=prvok_VALUE(vlastník_objekt,údaje_pozícia);if(!위쪽)break;*X_súradnica+=위쪽->X_súradnica;*Y_súradnica+=위쪽->Y_súradnica+(위쪽->oblasť_VALUE==1?30:0);údaje_pozícia=위쪽->nadradený;}}
static int 표시됨(int vlastník_objekt,widget_Stav *너비값){for(int položka_COUNT=0;položka_COUNT<32;položka_COUNT++){if(!너비값->보이는지)return 0;if(너비값->oblasť_VALUE==1)return 1;너비값=prvok_VALUE(vlastník_objekt,너비값->nadradený);if(!너비값)return 0;}return 0;}
static void Spracovanie_textu(int X_súradnica,int Y_súradnica,widget_Stav *너비값,int 최대값,unsigned 색상,unsigned 배경색){int v_termíne_splatnosti_pozícia=0;for(unsigned 순번=0;순번<너비값->dĺžka_VALUE;순번++){unsigned kódovanie_znakov=너비값->Spracovanie_textu[순번],너비=kódovanie_znakov>=256?16:8;if(v_termíne_splatnosti_pozícia+(int)너비>최대값)break;Terminál_piktogram(X_súradnica+v_termíne_splatnosti_pozícia,Y_súradnica,kódovanie_znakov,색상,배경색);v_termíne_splatnosti_pozícia+=너비;}}
void 화면다시그림(int vlastník_objekt){
    if(!화면보임(vlastník_objekt))return;
    for(int spracovanie_poradie=1;spracovanie_poradie<=5;spracovanie_poradie++)for(int 순번=0;순번<32;순번++){
        widget_Stav *너비값=&요소들[vlastník_objekt][순번];if(너비값->oblasť_VALUE!=spracovanie_poradie||!표시됨(vlastník_objekt,너비값))continue;int X_súradnica,Y_súradnica;Pozícia(vlastník_objekt,너비값,&X_súradnica,&Y_súradnica);
        if(spracovanie_poradie==1){사각영역(X_súradnica,Y_súradnica,너비값->너비값,너비값->높이값,0xeee9e0);사각영역(X_súradnica,Y_súradnica,너비값->너비값,30,0x905020);Spracovanie_textu(X_súradnica+10,Y_súradnica+7,너비값,너비값->너비값-50,0xffffff,0x905020);사각영역(X_súradnica+너비값->너비값-28,Y_súradnica+4,24,22,0x5555b8);Terminál_piktogram(X_súradnica+너비값->너비값-20,Y_súradnica+7,'X',0xffffff,0x5555b8);}
        if(spracovanie_poradie==2)사각영역(X_súradnica,Y_súradnica,너비값->너비값,너비값->높이값,0xeee9e0);
        if(spracovanie_poradie>=3){unsigned 배경색=spracovanie_poradie==4?0xc0ab86:spracovanie_poradie==5?0xffffff:0xeee9e0;if(spracovanie_poradie!=3)사각영역(X_súradnica,Y_súradnica,너비값->너비값,너비값->높이값,배경색);Spracovanie_textu(X_súradnica+4,Y_súradnica+4,너비값,너비값->너비값-8,0x201a15,배경색);if(spracovanie_poradie==5&&Prioritné[vlastník_objekt]==순번+1)사각영역(X_súradnica,Y_súradnica+너비값->높이값-2,너비값->너비값,2,0x905020);}
    }
}
int 화면덮음(int vlastník_objekt,int X_súradnica,int Y_súradnica){
    if(!화면보임(vlastník_objekt))return 0;
    for(int 순번=0;순번<32;순번++){
        widget_Stav *Okno=&요소들[vlastník_objekt][순번];
        if(Okno->oblasť_VALUE==1&&Okno->보이는지&&X_súradnica>=Okno->X_súradnica&&Y_súradnica>=Okno->Y_súradnica&&
           X_súradnica<Okno->X_súradnica+Okno->너비값&&Y_súradnica<Okno->Y_súradnica+Okno->높이값)return 1;
    }return 0;
}
int 화면가리킴(int vlastník_objekt,unsigned 눌림,int X_súradnica,int Y_súradnica){
    if(!화면보임(vlastník_objekt))return 0;
    if(눌림&1)for(int 순번=31;순번>=0;순번--){widget_Stav *너비값=&요소들[vlastník_objekt][순번];if(!너비값->oblasť_VALUE||!표시됨(vlastník_objekt,너비값))continue;int okno_X,okno_Y;Pozícia(vlastník_objekt,너비값,&okno_X,&okno_Y);
        if(X_súradnica<okno_X||Y_súradnica<okno_Y||X_súradnica>=okno_X+너비값->너비값||Y_súradnica>=okno_Y+너비값->높이값)continue;
        if(너비값->oblasť_VALUE==1&&Y_súradnica<okno_Y+30&&X_súradnica>=okno_X+너비값->너비값-28){if(너비값->Navigácia_politika!=0)너비값->보이는지=0;Udalosť(vlastník_objekt,0x10000+순번+1);Panel_Terminál(3);return 1;}
        if(너비값->oblasť_VALUE==4){Udalosť(vlastník_objekt,순번+1);return 1;}if(너비값->oblasť_VALUE==5){Prioritné[vlastník_objekt]=순번+1;Panel_Terminál(3);return 1;}
        if(너비값->oblasť_VALUE==1)return 1;
    }return 0;
}
void 화면누름(int vlastník_objekt,unsigned SECOND_VALUE){
    widget_Stav *너비값=prvok_VALUE(vlastník_objekt,Prioritné[vlastník_objekt]);if(!너비값||너비값->oblasť_VALUE!=5)return;
    if(SECOND_VALUE==13||SECOND_VALUE==10){Udalosť(vlastník_objekt,Prioritné[vlastník_objekt]);return;}
    if(SECOND_VALUE==8||SECOND_VALUE==127){if(너비값->dĺžka_VALUE)너비값->dĺžka_VALUE--;긴부호없는값[vlastník_objekt]=0;}
    else{
        unsigned kódovanie_znakov=SECOND_VALUE;
        if(긴부호없는값[vlastník_objekt]){if((SECOND_VALUE&192)!=128){긴부호없는값[vlastník_objekt]=0;return;}부호없는결과[vlastník_objekt]=(부호없는결과[vlastník_objekt]<<6)|(SECOND_VALUE&63);if(--긴부호없는값[vlastník_objekt])return;kódovanie_znakov=부호없는결과[vlastník_objekt];}
        else if(SECOND_VALUE>=0xc2&&SECOND_VALUE<=0xf4){긴부호없는값[vlastník_objekt]=SECOND_VALUE<0xe0?1:SECOND_VALUE<0xf0?2:3;부호없는결과[vlastník_objekt]=SECOND_VALUE&((1u<<(6-긴부호없는값[vlastník_objekt]))-1);return;}
        else if(SECOND_VALUE<32||SECOND_VALUE>=128)return;
        if(kódovanie_znakov>0x10ffff||(kódovanie_znakov>=0xd800&&kódovanie_znakov<=0xdfff))return;if(너비값->dĺžka_VALUE<127)너비값->Spracovanie_textu[너비값->dĺžka_VALUE++]=kódovanie_znakov;
    }
    Panel_Terminál(3);
}
int 화면호출(int vlastník_objekt,unsigned Akcia,int identifikátor_VALUE,int 첫째값,int SECOND_VALUE,int bod_kódu,int cieľ_údaje){
    if(vlastník_objekt<0||vlastník_objekt>=4)return -22;widget_Stav *너비값=prvok_VALUE(vlastník_objekt,identifikátor_VALUE);
    if(Akcia==0){if(identifikátor_VALUE<1||identifikátor_VALUE>5)return -22;for(int 순번=0;순번<32;순번++)if(요소들[vlastník_objekt][순번].oblasť_VALUE==0){너비값=&요소들[vlastník_objekt][순번];memset(너비값,0,sizeof(*너비값));너비값->oblasť_VALUE=identifikátor_VALUE;너비값->보이는지=identifikátor_VALUE!=1;너비값->너비값=identifikátor_VALUE==1?380:220;너비값->높이값=identifikátor_VALUE==1?240:28;너비값->Navigácia_politika=1;너비값->X_súradnica=identifikátor_VALUE==1?130:16;너비값->Y_súradnica=identifikátor_VALUE==1?110:16;return 순번+1;}return -28;}
    if(Akcia==5){if(!položka_COUNT_8f7753a1[vlastník_objekt])return 0;int 반환값=udalosť_Zoznam[vlastník_objekt][첫항목[vlastník_objekt]];첫항목[vlastník_objekt]=(첫항목[vlastník_objekt]+1)%16;položka_COUNT_8f7753a1[vlastník_objekt]--;return 반환값;}
    if(Akcia==6)return 화면보임(vlastník_objekt);
    if(!너비값)return -9;
    int 이전표시=표시됨(vlastník_objekt,너비값);
    if(Akcia==1){int 바탕너비=보드화면너비(),tapeta_výška=보드화면높이();if(첫째값<0||SECOND_VALUE<0||bod_kódu<1||cieľ_údaje<1||첫째값>바탕너비||SECOND_VALUE>tapeta_výška||bod_kódu>바탕너비-첫째값||cieľ_údaje>tapeta_výška-SECOND_VALUE)return -22;너비값->X_súradnica=첫째값;너비값->Y_súradnica=SECOND_VALUE;너비값->너비값=bod_kódu;너비값->높이값=cieľ_údaje;너비값->manuálny_Navigácia=1;}
    else if(Akcia==2){widget_Stav *podriadený=prvok_VALUE(vlastník_objekt,첫째값);if(!podriadený||podriadený==너비값||podriadený->oblasť_VALUE==1)return -22;int údaje_pozícia=identifikátor_VALUE;for(int 깊이=0;údaje_pozícia&&깊이<32;깊이++){if(údaje_pozícia==첫째값)return -22;widget_Stav *위쪽=prvok_VALUE(vlastník_objekt,údaje_pozícia);údaje_pozícia=위쪽?위쪽->nadradený:0;}podriadený->nadradený=identifikátor_VALUE;if(!podriadený->manuálny_Navigácia){int 형제요소=0;for(int 순번=0;순번<32;순번++)if(&요소들[vlastník_objekt][순번]!=podriadený&&요소들[vlastník_objekt][순번].nadradený==identifikátor_VALUE)형제요소++;podriadený->Y_súradnica=16+형제요소*36;}}
    else if(Akcia==3)너비값->보이는지=첫째값!=0;
    else if(Akcia==4)너비값->보이는지=0;
    else if(Akcia==7)너비값->Navigácia_politika=첫째값;
    else if(Akcia==8)return 너비값->dĺžka_VALUE;
    else if(Akcia==9)return 첫째값>=0&&(unsigned)첫째값<너비값->dĺžka_VALUE?너비값->Spracovanie_textu[첫째값]:-22;
    else return -22;
    if(이전표시||표시됨(vlastník_objekt,너비값))Panel_Terminál(3);return 0;
}
int 화면글(int vlastník_objekt,int identifikátor_VALUE,const uint32_t *údaje,unsigned položka_COUNT){widget_Stav *너비값=prvok_VALUE(vlastník_objekt,identifikátor_VALUE);if(!너비값)return -9;if(položka_COUNT>127)return -22;for(unsigned 순번=0;순번<položka_COUNT;순번++){unsigned kódovanie_znakov=údaje[순번];if(kódovanie_znakov>0x10ffff||(kódovanie_znakov>=0xd800&&kódovanie_znakov<=0xdfff))return -22;}for(unsigned 순번=0;순번<položka_COUNT;순번++)너비값->Spracovanie_textu[순번]=údaje[순번];너비값->dĺžka_VALUE=položka_COUNT;if(표시됨(vlastník_objekt,너비값))Panel_Terminál(3);return 0;}
