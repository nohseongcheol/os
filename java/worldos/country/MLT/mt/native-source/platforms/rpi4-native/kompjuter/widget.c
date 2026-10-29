#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* Small native peer layer for the explicitly supported Swing subset. */
#include <stdint.h>
#include <stddef.h>
extern uintptr_t bord_pel(uintptr_t,uintptr_t,uintptr_t),bord_Terminal(uintptr_t);
extern void Terminal_glyph(unsigned,unsigned,unsigned,unsigned,unsigned);
extern void *memset(void *,int,size_t);
typedef struct { int kategorija_VALUE,부모항목,koordinat_x,세로좌표,너비값,높이값,보이는지,manwali_Tqassim,Tqassim_politika;unsigned SMS[128],tul_VALUE; } widget_stat;
static widget_stat 요소들[4][32];
static int Ffokata[4],avveniment_Lista[4][16];static unsigned 첫항목[4],entrata_COUNT[4],부호없는결과[4],긴부호없는값[4];
static void avveniment(int propjetarju_oġġett,int VALUE){if(entrata_COUNT[propjetarju_oġġett]<16){avveniment_Lista[propjetarju_oġġett][(첫항목[propjetarju_oġġett]+entrata_COUNT[propjetarju_oġġett])%16]=VALUE;entrata_COUNT[propjetarju_oġġett]++;}}
static widget_stat *element_VALUE(int propjetarju_oġġett,int identifikatur_VALUE){return propjetarju_oġġett>=0&&propjetarju_oġġett<4&&identifikatur_VALUE>0&&identifikatur_VALUE<=32&&요소들[propjetarju_oġġett][identifikatur_VALUE-1].kategorija_VALUE?&요소들[propjetarju_oġġett][identifikatur_VALUE-1]:0;}
static void 사각영역(int koordinat_x,int 세로좌표,int 너비값,int 높이값,unsigned 색상){보드사각그림(koordinat_x,세로좌표,너비값,높이값,색상);}
int 화면보임(int propjetarju_oġġett){if(propjetarju_oġġett<0||propjetarju_oġġett>=4)return 0;for(int 순번=0;순번<32;순번++)if(요소들[propjetarju_oġġett][순번].kategorija_VALUE==1&&요소들[propjetarju_oġġett][순번].보이는지)return 1;return 0;}
void 화면초기화(int propjetarju_oġġett){memset(요소들[propjetarju_oġġett],0,sizeof(요소들[propjetarju_oġġett]));entrata_COUNT[propjetarju_oġġett]=첫항목[propjetarju_oġġett]=Ffokata[propjetarju_oġġett]=긴부호없는값[propjetarju_oġġett]=0;}
static void pożizzjoni(int propjetarju_oġġett,widget_stat *너비값,int *koordinat_x,int *세로좌표){*koordinat_x=너비값->koordinat_x;*세로좌표=너비값->세로좌표;int data_pożizzjoni=너비값->부모항목;for(int element_COUNT=0;data_pożizzjoni&&element_COUNT<32;element_COUNT++){widget_stat *위쪽=element_VALUE(propjetarju_oġġett,data_pożizzjoni);if(!위쪽)break;*koordinat_x+=위쪽->koordinat_x;*세로좌표+=위쪽->세로좌표+(위쪽->kategorija_VALUE==1?30:0);data_pożizzjoni=위쪽->부모항목;}}
static int 표시됨(int propjetarju_oġġett,widget_stat *너비값){for(int element_COUNT=0;element_COUNT<32;element_COUNT++){if(!너비값->보이는지)return 0;if(너비값->kategorija_VALUE==1)return 1;너비값=element_VALUE(propjetarju_oġġett,너비값->부모항목);if(!너비값)return 0;}return 0;}
static void SMS(int koordinat_x,int 세로좌표,widget_stat *너비값,int 최대값,unsigned 색상,unsigned 배경색){int 현재위치=0;for(unsigned 순번=0;순번<너비값->tul_VALUE;순번++){unsigned karattru_kodifikar=너비값->SMS[순번],너비=karattru_kodifikar>=256?16:8;if(현재위치+(int)너비>최대값)break;Terminal_glyph(koordinat_x+현재위치,세로좌표,karattru_kodifikar,색상,배경색);현재위치+=너비;}}
void 화면다시그림(int propjetarju_oġġett){
    if(!화면보임(propjetarju_oġġett))return;
    for(int 처리차례=1;처리차례<=5;처리차례++)for(int 순번=0;순번<32;순번++){
        widget_stat *너비값=&요소들[propjetarju_oġġett][순번];if(너비값->kategorija_VALUE!=처리차례||!표시됨(propjetarju_oġġett,너비값))continue;int koordinat_x,세로좌표;pożizzjoni(propjetarju_oġġett,너비값,&koordinat_x,&세로좌표);
        if(처리차례==1){사각영역(koordinat_x,세로좌표,너비값->너비값,너비값->높이값,0xeee9e0);사각영역(koordinat_x,세로좌표,너비값->너비값,30,0x905020);SMS(koordinat_x+10,세로좌표+7,너비값,너비값->너비값-50,0xffffff,0x905020);사각영역(koordinat_x+너비값->너비값-28,세로좌표+4,24,22,0x5555b8);Terminal_glyph(koordinat_x+너비값->너비값-20,세로좌표+7,'X',0xffffff,0x5555b8);}
        if(처리차례==2)사각영역(koordinat_x,세로좌표,너비값->너비값,너비값->높이값,0xeee9e0);
        if(처리차례>=3){unsigned 배경색=처리차례==4?0xc0ab86:처리차례==5?0xffffff:0xeee9e0;if(처리차례!=3)사각영역(koordinat_x,세로좌표,너비값->너비값,너비값->높이값,배경색);SMS(koordinat_x+4,세로좌표+4,너비값,너비값->너비값-8,0x201a15,배경색);if(처리차례==5&&Ffokata[propjetarju_oġġett]==순번+1)사각영역(koordinat_x,세로좌표+너비값->높이값-2,너비값->너비값,2,0x905020);}
    }
}
int 화면덮음(int propjetarju_oġġett,int koordinat_x,int 세로좌표){
    if(!화면보임(propjetarju_oġġett))return 0;
    for(int 순번=0;순번<32;순번++){
        widget_stat *tieqa=&요소들[propjetarju_oġġett][순번];
        if(tieqa->kategorija_VALUE==1&&tieqa->보이는지&&koordinat_x>=tieqa->koordinat_x&&세로좌표>=tieqa->세로좌표&&
           koordinat_x<tieqa->koordinat_x+tieqa->너비값&&세로좌표<tieqa->세로좌표+tieqa->높이값)return 1;
    }return 0;
}
int 화면가리킴(int propjetarju_oġġett,unsigned 눌림,int koordinat_x,int 세로좌표){
    if(!화면보임(propjetarju_oġġett))return 0;
    if(눌림&1)for(int 순번=31;순번>=0;순번--){widget_stat *너비값=&요소들[propjetarju_oġġett][순번];if(!너비값->kategorija_VALUE||!표시됨(propjetarju_oġġett,너비값))continue;int 창가로,창세로;pożizzjoni(propjetarju_oġġett,너비값,&창가로,&창세로);
        if(koordinat_x<창가로||세로좌표<창세로||koordinat_x>=창가로+너비값->너비값||세로좌표>=창세로+너비값->높이값)continue;
        if(너비값->kategorija_VALUE==1&&세로좌표<창세로+30&&koordinat_x>=창가로+너비값->너비값-28){if(너비값->Tqassim_politika!=0)너비값->보이는지=0;avveniment(propjetarju_oġġett,0x10000+순번+1);bord_Terminal(3);return 1;}
        if(너비값->kategorija_VALUE==4){avveniment(propjetarju_oġġett,순번+1);return 1;}if(너비값->kategorija_VALUE==5){Ffokata[propjetarju_oġġett]=순번+1;bord_Terminal(3);return 1;}
        if(너비값->kategorija_VALUE==1)return 1;
    }return 0;
}
void 화면누름(int propjetarju_oġġett,unsigned SECOND_VALUE){
    widget_stat *너비값=element_VALUE(propjetarju_oġġett,Ffokata[propjetarju_oġġett]);if(!너비값||너비값->kategorija_VALUE!=5)return;
    if(SECOND_VALUE==13||SECOND_VALUE==10){avveniment(propjetarju_oġġett,Ffokata[propjetarju_oġġett]);return;}
    if(SECOND_VALUE==8||SECOND_VALUE==127){if(너비값->tul_VALUE)너비값->tul_VALUE--;긴부호없는값[propjetarju_oġġett]=0;}
    else{
        unsigned karattru_kodifikar=SECOND_VALUE;
        if(긴부호없는값[propjetarju_oġġett]){if((SECOND_VALUE&192)!=128){긴부호없는값[propjetarju_oġġett]=0;return;}부호없는결과[propjetarju_oġġett]=(부호없는결과[propjetarju_oġġett]<<6)|(SECOND_VALUE&63);if(--긴부호없는값[propjetarju_oġġett])return;karattru_kodifikar=부호없는결과[propjetarju_oġġett];}
        else if(SECOND_VALUE>=0xc2&&SECOND_VALUE<=0xf4){긴부호없는값[propjetarju_oġġett]=SECOND_VALUE<0xe0?1:SECOND_VALUE<0xf0?2:3;부호없는결과[propjetarju_oġġett]=SECOND_VALUE&((1u<<(6-긴부호없는값[propjetarju_oġġett]))-1);return;}
        else if(SECOND_VALUE<32||SECOND_VALUE>=128)return;
        if(karattru_kodifikar>0x10ffff||(karattru_kodifikar>=0xd800&&karattru_kodifikar<=0xdfff))return;if(너비값->tul_VALUE<127)너비값->SMS[너비값->tul_VALUE++]=karattru_kodifikar;
    }
    bord_Terminal(3);
}
int 화면호출(int propjetarju_oġġett,unsigned azzjoni,int identifikatur_VALUE,int 첫째값,int SECOND_VALUE,int kodiċi_tal_karattru,int destinazzjoni_data){
    if(propjetarju_oġġett<0||propjetarju_oġġett>=4)return -22;widget_stat *너비값=element_VALUE(propjetarju_oġġett,identifikatur_VALUE);
    if(azzjoni==0){if(identifikatur_VALUE<1||identifikatur_VALUE>5)return -22;for(int 순번=0;순번<32;순번++)if(요소들[propjetarju_oġġett][순번].kategorija_VALUE==0){너비값=&요소들[propjetarju_oġġett][순번];memset(너비값,0,sizeof(*너비값));너비값->kategorija_VALUE=identifikatur_VALUE;너비값->보이는지=identifikatur_VALUE!=1;너비값->너비값=identifikatur_VALUE==1?380:220;너비값->높이값=identifikatur_VALUE==1?240:28;너비값->Tqassim_politika=1;너비값->koordinat_x=identifikatur_VALUE==1?130:16;너비값->세로좌표=identifikatur_VALUE==1?110:16;return 순번+1;}return -28;}
    if(azzjoni==5){if(!entrata_COUNT[propjetarju_oġġett])return 0;int 반환값=avveniment_Lista[propjetarju_oġġett][첫항목[propjetarju_oġġett]];첫항목[propjetarju_oġġett]=(첫항목[propjetarju_oġġett]+1)%16;entrata_COUNT[propjetarju_oġġett]--;return 반환값;}
    if(azzjoni==6)return 화면보임(propjetarju_oġġett);
    if(!너비값)return -9;
    int 이전표시=표시됨(propjetarju_oġġett,너비값);
    if(azzjoni==1){int 바탕너비=보드화면너비(),바탕높이=보드화면높이();if(첫째값<0||SECOND_VALUE<0||kodiċi_tal_karattru<1||destinazzjoni_data<1||첫째값>바탕너비||SECOND_VALUE>바탕높이||kodiċi_tal_karattru>바탕너비-첫째값||destinazzjoni_data>바탕높이-SECOND_VALUE)return -22;너비값->koordinat_x=첫째값;너비값->세로좌표=SECOND_VALUE;너비값->너비값=kodiċi_tal_karattru;너비값->높이값=destinazzjoni_data;너비값->manwali_Tqassim=1;}
    else if(azzjoni==2){widget_stat *element_dixxendent=element_VALUE(propjetarju_oġġett,첫째값);if(!element_dixxendent||element_dixxendent==너비값||element_dixxendent->kategorija_VALUE==1)return -22;int data_pożizzjoni=identifikatur_VALUE;for(int 깊이=0;data_pożizzjoni&&깊이<32;깊이++){if(data_pożizzjoni==첫째값)return -22;widget_stat *위쪽=element_VALUE(propjetarju_oġġett,data_pożizzjoni);data_pożizzjoni=위쪽?위쪽->부모항목:0;}element_dixxendent->부모항목=identifikatur_VALUE;if(!element_dixxendent->manwali_Tqassim){int 형제요소=0;for(int 순번=0;순번<32;순번++)if(&요소들[propjetarju_oġġett][순번]!=element_dixxendent&&요소들[propjetarju_oġġett][순번].부모항목==identifikatur_VALUE)형제요소++;element_dixxendent->세로좌표=16+형제요소*36;}}
    else if(azzjoni==3)너비값->보이는지=첫째값!=0;
    else if(azzjoni==4)너비값->보이는지=0;
    else if(azzjoni==7)너비값->Tqassim_politika=첫째값;
    else if(azzjoni==8)return 너비값->tul_VALUE;
    else if(azzjoni==9)return 첫째값>=0&&(unsigned)첫째값<너비값->tul_VALUE?너비값->SMS[첫째값]:-22;
    else return -22;
    if(이전표시||표시됨(propjetarju_oġġett,너비값))bord_Terminal(3);return 0;
}
int 화면글(int propjetarju_oġġett,int identifikatur_VALUE,const uint32_t *data,unsigned element_COUNT){widget_stat *너비값=element_VALUE(propjetarju_oġġett,identifikatur_VALUE);if(!너비값)return -9;if(element_COUNT>127)return -22;for(unsigned 순번=0;순번<element_COUNT;순번++){unsigned karattru_kodifikar=data[순번];if(karattru_kodifikar>0x10ffff||(karattru_kodifikar>=0xd800&&karattru_kodifikar<=0xdfff))return -22;}for(unsigned 순번=0;순번<element_COUNT;순번++)너비값->SMS[순번]=data[순번];너비값->tul_VALUE=element_COUNT;if(표시됨(propjetarju_oġġett,너비값))bord_Terminal(3);return 0;}
