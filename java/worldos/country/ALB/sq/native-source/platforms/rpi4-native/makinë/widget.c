#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* Small native peer layer for the explicitly supported Swing subset. */
#include <stdint.h>
#include <stddef.h>
extern uintptr_t panel_pikëz(uintptr_t,uintptr_t,uintptr_t),panel_Terminali(uintptr_t);
extern void Terminali_glif(unsigned,unsigned,unsigned,unsigned,unsigned);
extern void *memset(void *,int,size_t);
typedef struct { int kategori_VALUE,부모항목,koordinata_x,Y_koordinatë,너비값,높이값,보이는지,manual_Navigimi,Navigimi_politikë;unsigned Teksti[128],gjatësi_VALUE; } widget_status;
static widget_status 요소들[4][32];
static int I_E_fokusuar[4],ngjarje_Listë[4][16];static unsigned 첫항목[4],futje_COUNT[4],부호없는결과[4],긴부호없는값[4];
static void Ngjarje(int pronari_objekt,int VALUE){if(futje_COUNT[pronari_objekt]<16){ngjarje_Listë[pronari_objekt][(첫항목[pronari_objekt]+futje_COUNT[pronari_objekt])%16]=VALUE;futje_COUNT[pronari_objekt]++;}}
static widget_status *element_VALUE(int pronari_objekt,int identifikues_VALUE){return pronari_objekt>=0&&pronari_objekt<4&&identifikues_VALUE>0&&identifikues_VALUE<=32&&요소들[pronari_objekt][identifikues_VALUE-1].kategori_VALUE?&요소들[pronari_objekt][identifikues_VALUE-1]:0;}
static void 사각영역(int koordinata_x,int Y_koordinatë,int 너비값,int 높이값,unsigned 색상){보드사각그림(koordinata_x,Y_koordinatë,너비값,높이값,색상);}
int 화면보임(int pronari_objekt){if(pronari_objekt<0||pronari_objekt>=4)return 0;for(int 순번=0;순번<32;순번++)if(요소들[pronari_objekt][순번].kategori_VALUE==1&&요소들[pronari_objekt][순번].보이는지)return 1;return 0;}
void 화면초기화(int pronari_objekt){memset(요소들[pronari_objekt],0,sizeof(요소들[pronari_objekt]));futje_COUNT[pronari_objekt]=첫항목[pronari_objekt]=I_E_fokusuar[pronari_objekt]=긴부호없는값[pronari_objekt]=0;}
static void Pozicioni(int pronari_objekt,widget_status *너비값,int *koordinata_x,int *Y_koordinatë){*koordinata_x=너비값->koordinata_x;*Y_koordinatë=너비값->Y_koordinatë;int të_dhëna_pozicioni=너비값->부모항목;for(int njësi_COUNT=0;të_dhëna_pozicioni&&njësi_COUNT<32;njësi_COUNT++){widget_status *위쪽=element_VALUE(pronari_objekt,të_dhëna_pozicioni);if(!위쪽)break;*koordinata_x+=위쪽->koordinata_x;*Y_koordinatë+=위쪽->Y_koordinatë+(위쪽->kategori_VALUE==1?30:0);të_dhëna_pozicioni=위쪽->부모항목;}}
static int 표시됨(int pronari_objekt,widget_status *너비값){for(int njësi_COUNT=0;njësi_COUNT<32;njësi_COUNT++){if(!너비값->보이는지)return 0;if(너비값->kategori_VALUE==1)return 1;너비값=element_VALUE(pronari_objekt,너비값->부모항목);if(!너비값)return 0;}return 0;}
static void Teksti(int koordinata_x,int Y_koordinatë,widget_status *너비값,int 최대값,unsigned 색상,unsigned 배경색){int 현재위치=0;for(unsigned 순번=0;순번<너비값->gjatësi_VALUE;순번++){unsigned karakter_enkodim=너비값->Teksti[순번],너비=karakter_enkodim>=256?16:8;if(현재위치+(int)너비>최대값)break;Terminali_glif(koordinata_x+현재위치,Y_koordinatë,karakter_enkodim,색상,배경색);현재위치+=너비;}}
void 화면다시그림(int pronari_objekt){
    if(!화면보임(pronari_objekt))return;
    for(int 처리차례=1;처리차례<=5;처리차례++)for(int 순번=0;순번<32;순번++){
        widget_status *너비값=&요소들[pronari_objekt][순번];if(너비값->kategori_VALUE!=처리차례||!표시됨(pronari_objekt,너비값))continue;int koordinata_x,Y_koordinatë;Pozicioni(pronari_objekt,너비값,&koordinata_x,&Y_koordinatë);
        if(처리차례==1){사각영역(koordinata_x,Y_koordinatë,너비값->너비값,너비값->높이값,0xeee9e0);사각영역(koordinata_x,Y_koordinatë,너비값->너비값,30,0x905020);Teksti(koordinata_x+10,Y_koordinatë+7,너비값,너비값->너비값-50,0xffffff,0x905020);사각영역(koordinata_x+너비값->너비값-28,Y_koordinatë+4,24,22,0x5555b8);Terminali_glif(koordinata_x+너비값->너비값-20,Y_koordinatë+7,'X',0xffffff,0x5555b8);}
        if(처리차례==2)사각영역(koordinata_x,Y_koordinatë,너비값->너비값,너비값->높이값,0xeee9e0);
        if(처리차례>=3){unsigned 배경색=처리차례==4?0xc0ab86:처리차례==5?0xffffff:0xeee9e0;if(처리차례!=3)사각영역(koordinata_x,Y_koordinatë,너비값->너비값,너비값->높이값,배경색);Teksti(koordinata_x+4,Y_koordinatë+4,너비값,너비값->너비값-8,0x201a15,배경색);if(처리차례==5&&I_E_fokusuar[pronari_objekt]==순번+1)사각영역(koordinata_x,Y_koordinatë+너비값->높이값-2,너비값->너비값,2,0x905020);}
    }
}
int 화면덮음(int pronari_objekt,int koordinata_x,int Y_koordinatë){
    if(!화면보임(pronari_objekt))return 0;
    for(int 순번=0;순번<32;순번++){
        widget_status *Dritare=&요소들[pronari_objekt][순번];
        if(Dritare->kategori_VALUE==1&&Dritare->보이는지&&koordinata_x>=Dritare->koordinata_x&&Y_koordinatë>=Dritare->Y_koordinatë&&
           koordinata_x<Dritare->koordinata_x+Dritare->너비값&&Y_koordinatë<Dritare->Y_koordinatë+Dritare->높이값)return 1;
    }return 0;
}
int 화면가리킴(int pronari_objekt,unsigned 눌림,int koordinata_x,int Y_koordinatë){
    if(!화면보임(pronari_objekt))return 0;
    if(눌림&1)for(int 순번=31;순번>=0;순번--){widget_status *너비값=&요소들[pronari_objekt][순번];if(!너비값->kategori_VALUE||!표시됨(pronari_objekt,너비값))continue;int dritare_X,dritare_Y;Pozicioni(pronari_objekt,너비값,&dritare_X,&dritare_Y);
        if(koordinata_x<dritare_X||Y_koordinatë<dritare_Y||koordinata_x>=dritare_X+너비값->너비값||Y_koordinatë>=dritare_Y+너비값->높이값)continue;
        if(너비값->kategori_VALUE==1&&Y_koordinatë<dritare_Y+30&&koordinata_x>=dritare_X+너비값->너비값-28){if(너비값->Navigimi_politikë!=0)너비값->보이는지=0;Ngjarje(pronari_objekt,0x10000+순번+1);panel_Terminali(3);return 1;}
        if(너비값->kategori_VALUE==4){Ngjarje(pronari_objekt,순번+1);return 1;}if(너비값->kategori_VALUE==5){I_E_fokusuar[pronari_objekt]=순번+1;panel_Terminali(3);return 1;}
        if(너비값->kategori_VALUE==1)return 1;
    }return 0;
}
void 화면누름(int pronari_objekt,unsigned SECOND_VALUE){
    widget_status *너비값=element_VALUE(pronari_objekt,I_E_fokusuar[pronari_objekt]);if(!너비값||너비값->kategori_VALUE!=5)return;
    if(SECOND_VALUE==13||SECOND_VALUE==10){Ngjarje(pronari_objekt,I_E_fokusuar[pronari_objekt]);return;}
    if(SECOND_VALUE==8||SECOND_VALUE==127){if(너비값->gjatësi_VALUE)너비값->gjatësi_VALUE--;긴부호없는값[pronari_objekt]=0;}
    else{
        unsigned karakter_enkodim=SECOND_VALUE;
        if(긴부호없는값[pronari_objekt]){if((SECOND_VALUE&192)!=128){긴부호없는값[pronari_objekt]=0;return;}부호없는결과[pronari_objekt]=(부호없는결과[pronari_objekt]<<6)|(SECOND_VALUE&63);if(--긴부호없는값[pronari_objekt])return;karakter_enkodim=부호없는결과[pronari_objekt];}
        else if(SECOND_VALUE>=0xc2&&SECOND_VALUE<=0xf4){긴부호없는값[pronari_objekt]=SECOND_VALUE<0xe0?1:SECOND_VALUE<0xf0?2:3;부호없는결과[pronari_objekt]=SECOND_VALUE&((1u<<(6-긴부호없는값[pronari_objekt]))-1);return;}
        else if(SECOND_VALUE<32||SECOND_VALUE>=128)return;
        if(karakter_enkodim>0x10ffff||(karakter_enkodim>=0xd800&&karakter_enkodim<=0xdfff))return;if(너비값->gjatësi_VALUE<127)너비값->Teksti[너비값->gjatësi_VALUE++]=karakter_enkodim;
    }
    panel_Terminali(3);
}
int 화면호출(int pronari_objekt,unsigned Veprim,int identifikues_VALUE,int 첫째값,int SECOND_VALUE,int kodi_i_karakterit,int vendmbërritje_të_dhëna){
    if(pronari_objekt<0||pronari_objekt>=4)return -22;widget_status *너비값=element_VALUE(pronari_objekt,identifikues_VALUE);
    if(Veprim==0){if(identifikues_VALUE<1||identifikues_VALUE>5)return -22;for(int 순번=0;순번<32;순번++)if(요소들[pronari_objekt][순번].kategori_VALUE==0){너비값=&요소들[pronari_objekt][순번];memset(너비값,0,sizeof(*너비값));너비값->kategori_VALUE=identifikues_VALUE;너비값->보이는지=identifikues_VALUE!=1;너비값->너비값=identifikues_VALUE==1?380:220;너비값->높이값=identifikues_VALUE==1?240:28;너비값->Navigimi_politikë=1;너비값->koordinata_x=identifikues_VALUE==1?130:16;너비값->Y_koordinatë=identifikues_VALUE==1?110:16;return 순번+1;}return -28;}
    if(Veprim==5){if(!futje_COUNT[pronari_objekt])return 0;int 반환값=ngjarje_Listë[pronari_objekt][첫항목[pronari_objekt]];첫항목[pronari_objekt]=(첫항목[pronari_objekt]+1)%16;futje_COUNT[pronari_objekt]--;return 반환값;}
    if(Veprim==6)return 화면보임(pronari_objekt);
    if(!너비값)return -9;
    int 이전표시=표시됨(pronari_objekt,너비값);
    if(Veprim==1){int 바탕너비=보드화면너비(),바탕높이=보드화면높이();if(첫째값<0||SECOND_VALUE<0||kodi_i_karakterit<1||vendmbërritje_të_dhëna<1||첫째값>바탕너비||SECOND_VALUE>바탕높이||kodi_i_karakterit>바탕너비-첫째값||vendmbërritje_të_dhëna>바탕높이-SECOND_VALUE)return -22;너비값->koordinata_x=첫째값;너비값->Y_koordinatë=SECOND_VALUE;너비값->너비값=kodi_i_karakterit;너비값->높이값=vendmbërritje_të_dhëna;너비값->manual_Navigimi=1;}
    else if(Veprim==2){widget_status *element_fëmijë=element_VALUE(pronari_objekt,첫째값);if(!element_fëmijë||element_fëmijë==너비값||element_fëmijë->kategori_VALUE==1)return -22;int të_dhëna_pozicioni=identifikues_VALUE;for(int 깊이=0;të_dhëna_pozicioni&&깊이<32;깊이++){if(të_dhëna_pozicioni==첫째값)return -22;widget_status *위쪽=element_VALUE(pronari_objekt,të_dhëna_pozicioni);të_dhëna_pozicioni=위쪽?위쪽->부모항목:0;}element_fëmijë->부모항목=identifikues_VALUE;if(!element_fëmijë->manual_Navigimi){int 형제요소=0;for(int 순번=0;순번<32;순번++)if(&요소들[pronari_objekt][순번]!=element_fëmijë&&요소들[pronari_objekt][순번].부모항목==identifikues_VALUE)형제요소++;element_fëmijë->Y_koordinatë=16+형제요소*36;}}
    else if(Veprim==3)너비값->보이는지=첫째값!=0;
    else if(Veprim==4)너비값->보이는지=0;
    else if(Veprim==7)너비값->Navigimi_politikë=첫째값;
    else if(Veprim==8)return 너비값->gjatësi_VALUE;
    else if(Veprim==9)return 첫째값>=0&&(unsigned)첫째값<너비값->gjatësi_VALUE?너비값->Teksti[첫째값]:-22;
    else return -22;
    if(이전표시||표시됨(pronari_objekt,너비값))panel_Terminali(3);return 0;
}
int 화면글(int pronari_objekt,int identifikues_VALUE,const uint32_t *të_dhëna,unsigned njësi_COUNT){widget_status *너비값=element_VALUE(pronari_objekt,identifikues_VALUE);if(!너비값)return -9;if(njësi_COUNT>127)return -22;for(unsigned 순번=0;순번<njësi_COUNT;순번++){unsigned karakter_enkodim=të_dhëna[순번];if(karakter_enkodim>0x10ffff||(karakter_enkodim>=0xd800&&karakter_enkodim<=0xdfff))return -22;}for(unsigned 순번=0;순번<njësi_COUNT;순번++)너비값->Teksti[순번]=të_dhëna[순번];너비값->gjatësi_VALUE=njësi_COUNT;if(표시됨(pronari_objekt,너비값))panel_Terminali(3);return 0;}
