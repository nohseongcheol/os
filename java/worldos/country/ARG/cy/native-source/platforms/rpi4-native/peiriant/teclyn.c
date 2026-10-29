#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* Small native peer layer for the explicitly supported Swing subset. */
#include <stdint.h>
#include <stddef.h>
extern uintptr_t bwrdd_pel(uintptr_t,uintptr_t,uintptr_t),bwrdd_Terfynell(uintptr_t);
extern void Terfynell_glyff(unsigned,unsigned,unsigned,unsigned,unsigned);
extern void *memset(void *,int,size_t);
typedef struct { int ardal_VALUE,부모항목,cyfesuryn_x,Y_cyfesuryn,너비값,높이값,보이는지,llaw_Llywio,Llywio_polisi;unsigned Testun[128],hyd_VALUE; } teclyn_cyflwr;
static teclyn_cyflwr 요소들[4][32];
static int Blaenoriaeth[4],digwyddiad_Rhestr[4][16];static unsigned 첫항목[4],cofnod_COUNT[4],부호없는결과[4],긴부호없는값[4];
static void digwyddiad(int perchennog_gwrthrych,int VALUE){if(cofnod_COUNT[perchennog_gwrthrych]<16){digwyddiad_Rhestr[perchennog_gwrthrych][(첫항목[perchennog_gwrthrych]+cofnod_COUNT[perchennog_gwrthrych])%16]=VALUE;cofnod_COUNT[perchennog_gwrthrych]++;}}
static teclyn_cyflwr *elfen_VALUE(int perchennog_gwrthrych,int dynodwr_VALUE){return perchennog_gwrthrych>=0&&perchennog_gwrthrych<4&&dynodwr_VALUE>0&&dynodwr_VALUE<=32&&요소들[perchennog_gwrthrych][dynodwr_VALUE-1].ardal_VALUE?&요소들[perchennog_gwrthrych][dynodwr_VALUE-1]:0;}
static void 사각영역(int cyfesuryn_x,int Y_cyfesuryn,int 너비값,int 높이값,unsigned 색상){보드사각그림(cyfesuryn_x,Y_cyfesuryn,너비값,높이값,색상);}
int 화면보임(int perchennog_gwrthrych){if(perchennog_gwrthrych<0||perchennog_gwrthrych>=4)return 0;for(int 순번=0;순번<32;순번++)if(요소들[perchennog_gwrthrych][순번].ardal_VALUE==1&&요소들[perchennog_gwrthrych][순번].보이는지)return 1;return 0;}
void 화면초기화(int perchennog_gwrthrych){memset(요소들[perchennog_gwrthrych],0,sizeof(요소들[perchennog_gwrthrych]));cofnod_COUNT[perchennog_gwrthrych]=첫항목[perchennog_gwrthrych]=Blaenoriaeth[perchennog_gwrthrych]=긴부호없는값[perchennog_gwrthrych]=0;}
static void safle(int perchennog_gwrthrych,teclyn_cyflwr *너비값,int *cyfesuryn_x,int *Y_cyfesuryn){*cyfesuryn_x=너비값->cyfesuryn_x;*Y_cyfesuryn=너비값->Y_cyfesuryn;int data_safle=너비값->부모항목;for(int eitem_COUNT=0;data_safle&&eitem_COUNT<32;eitem_COUNT++){teclyn_cyflwr *위쪽=elfen_VALUE(perchennog_gwrthrych,data_safle);if(!위쪽)break;*cyfesuryn_x+=위쪽->cyfesuryn_x;*Y_cyfesuryn+=위쪽->Y_cyfesuryn+(위쪽->ardal_VALUE==1?30:0);data_safle=위쪽->부모항목;}}
static int 표시됨(int perchennog_gwrthrych,teclyn_cyflwr *너비값){for(int eitem_COUNT=0;eitem_COUNT<32;eitem_COUNT++){if(!너비값->보이는지)return 0;if(너비값->ardal_VALUE==1)return 1;너비값=elfen_VALUE(perchennog_gwrthrych,너비값->부모항목);if(!너비값)return 0;}return 0;}
static void Testun(int cyfesuryn_x,int Y_cyfesuryn,teclyn_cyflwr *너비값,int 최대값,unsigned 색상,unsigned 배경색){int 현재위치=0;for(unsigned 순번=0;순번<너비값->hyd_VALUE;순번++){unsigned nod_amgodio=너비값->Testun[순번],너비=nod_amgodio>=256?16:8;if(현재위치+(int)너비>최대값)break;Terfynell_glyff(cyfesuryn_x+현재위치,Y_cyfesuryn,nod_amgodio,색상,배경색);현재위치+=너비;}}
void 화면다시그림(int perchennog_gwrthrych){
    if(!화면보임(perchennog_gwrthrych))return;
    for(int 처리차례=1;처리차례<=5;처리차례++)for(int 순번=0;순번<32;순번++){
        teclyn_cyflwr *너비값=&요소들[perchennog_gwrthrych][순번];if(너비값->ardal_VALUE!=처리차례||!표시됨(perchennog_gwrthrych,너비값))continue;int cyfesuryn_x,Y_cyfesuryn;safle(perchennog_gwrthrych,너비값,&cyfesuryn_x,&Y_cyfesuryn);
        if(처리차례==1){사각영역(cyfesuryn_x,Y_cyfesuryn,너비값->너비값,너비값->높이값,0xeee9e0);사각영역(cyfesuryn_x,Y_cyfesuryn,너비값->너비값,30,0x905020);Testun(cyfesuryn_x+10,Y_cyfesuryn+7,너비값,너비값->너비값-50,0xffffff,0x905020);사각영역(cyfesuryn_x+너비값->너비값-28,Y_cyfesuryn+4,24,22,0x5555b8);Terfynell_glyff(cyfesuryn_x+너비값->너비값-20,Y_cyfesuryn+7,'X',0xffffff,0x5555b8);}
        if(처리차례==2)사각영역(cyfesuryn_x,Y_cyfesuryn,너비값->너비값,너비값->높이값,0xeee9e0);
        if(처리차례>=3){unsigned 배경색=처리차례==4?0xc0ab86:처리차례==5?0xffffff:0xeee9e0;if(처리차례!=3)사각영역(cyfesuryn_x,Y_cyfesuryn,너비값->너비값,너비값->높이값,배경색);Testun(cyfesuryn_x+4,Y_cyfesuryn+4,너비값,너비값->너비값-8,0x201a15,배경색);if(처리차례==5&&Blaenoriaeth[perchennog_gwrthrych]==순번+1)사각영역(cyfesuryn_x,Y_cyfesuryn+너비값->높이값-2,너비값->너비값,2,0x905020);}
    }
}
int 화면덮음(int perchennog_gwrthrych,int cyfesuryn_x,int Y_cyfesuryn){
    if(!화면보임(perchennog_gwrthrych))return 0;
    for(int 순번=0;순번<32;순번++){
        teclyn_cyflwr *ffenestr=&요소들[perchennog_gwrthrych][순번];
        if(ffenestr->ardal_VALUE==1&&ffenestr->보이는지&&cyfesuryn_x>=ffenestr->cyfesuryn_x&&Y_cyfesuryn>=ffenestr->Y_cyfesuryn&&
           cyfesuryn_x<ffenestr->cyfesuryn_x+ffenestr->너비값&&Y_cyfesuryn<ffenestr->Y_cyfesuryn+ffenestr->높이값)return 1;
    }return 0;
}
int 화면가리킴(int perchennog_gwrthrych,unsigned 눌림,int cyfesuryn_x,int Y_cyfesuryn){
    if(!화면보임(perchennog_gwrthrych))return 0;
    if(눌림&1)for(int 순번=31;순번>=0;순번--){teclyn_cyflwr *너비값=&요소들[perchennog_gwrthrych][순번];if(!너비값->ardal_VALUE||!표시됨(perchennog_gwrthrych,너비값))continue;int ffenestr_X,ffenestr_Y;safle(perchennog_gwrthrych,너비값,&ffenestr_X,&ffenestr_Y);
        if(cyfesuryn_x<ffenestr_X||Y_cyfesuryn<ffenestr_Y||cyfesuryn_x>=ffenestr_X+너비값->너비값||Y_cyfesuryn>=ffenestr_Y+너비값->높이값)continue;
        if(너비값->ardal_VALUE==1&&Y_cyfesuryn<ffenestr_Y+30&&cyfesuryn_x>=ffenestr_X+너비값->너비값-28){if(너비값->Llywio_polisi!=0)너비값->보이는지=0;digwyddiad(perchennog_gwrthrych,0x10000+순번+1);bwrdd_Terfynell(3);return 1;}
        if(너비값->ardal_VALUE==4){digwyddiad(perchennog_gwrthrych,순번+1);return 1;}if(너비값->ardal_VALUE==5){Blaenoriaeth[perchennog_gwrthrych]=순번+1;bwrdd_Terfynell(3);return 1;}
        if(너비값->ardal_VALUE==1)return 1;
    }return 0;
}
void 화면누름(int perchennog_gwrthrych,unsigned SECOND_VALUE){
    teclyn_cyflwr *너비값=elfen_VALUE(perchennog_gwrthrych,Blaenoriaeth[perchennog_gwrthrych]);if(!너비값||너비값->ardal_VALUE!=5)return;
    if(SECOND_VALUE==13||SECOND_VALUE==10){digwyddiad(perchennog_gwrthrych,Blaenoriaeth[perchennog_gwrthrych]);return;}
    if(SECOND_VALUE==8||SECOND_VALUE==127){if(너비값->hyd_VALUE)너비값->hyd_VALUE--;긴부호없는값[perchennog_gwrthrych]=0;}
    else{
        unsigned nod_amgodio=SECOND_VALUE;
        if(긴부호없는값[perchennog_gwrthrych]){if((SECOND_VALUE&192)!=128){긴부호없는값[perchennog_gwrthrych]=0;return;}부호없는결과[perchennog_gwrthrych]=(부호없는결과[perchennog_gwrthrych]<<6)|(SECOND_VALUE&63);if(--긴부호없는값[perchennog_gwrthrych])return;nod_amgodio=부호없는결과[perchennog_gwrthrych];}
        else if(SECOND_VALUE>=0xc2&&SECOND_VALUE<=0xf4){긴부호없는값[perchennog_gwrthrych]=SECOND_VALUE<0xe0?1:SECOND_VALUE<0xf0?2:3;부호없는결과[perchennog_gwrthrych]=SECOND_VALUE&((1u<<(6-긴부호없는값[perchennog_gwrthrych]))-1);return;}
        else if(SECOND_VALUE<32||SECOND_VALUE>=128)return;
        if(nod_amgodio>0x10ffff||(nod_amgodio>=0xd800&&nod_amgodio<=0xdfff))return;if(너비값->hyd_VALUE<127)너비값->Testun[너비값->hyd_VALUE++]=nod_amgodio;
    }
    bwrdd_Terfynell(3);
}
int 화면호출(int perchennog_gwrthrych,unsigned Gweithrediad,int dynodwr_VALUE,int 첫째값,int SECOND_VALUE,int cod_nod,int cyrchfan_data){
    if(perchennog_gwrthrych<0||perchennog_gwrthrych>=4)return -22;teclyn_cyflwr *너비값=elfen_VALUE(perchennog_gwrthrych,dynodwr_VALUE);
    if(Gweithrediad==0){if(dynodwr_VALUE<1||dynodwr_VALUE>5)return -22;for(int 순번=0;순번<32;순번++)if(요소들[perchennog_gwrthrych][순번].ardal_VALUE==0){너비값=&요소들[perchennog_gwrthrych][순번];memset(너비값,0,sizeof(*너비값));너비값->ardal_VALUE=dynodwr_VALUE;너비값->보이는지=dynodwr_VALUE!=1;너비값->너비값=dynodwr_VALUE==1?380:220;너비값->높이값=dynodwr_VALUE==1?240:28;너비값->Llywio_polisi=1;너비값->cyfesuryn_x=dynodwr_VALUE==1?130:16;너비값->Y_cyfesuryn=dynodwr_VALUE==1?110:16;return 순번+1;}return -28;}
    if(Gweithrediad==5){if(!cofnod_COUNT[perchennog_gwrthrych])return 0;int 반환값=digwyddiad_Rhestr[perchennog_gwrthrych][첫항목[perchennog_gwrthrych]];첫항목[perchennog_gwrthrych]=(첫항목[perchennog_gwrthrych]+1)%16;cofnod_COUNT[perchennog_gwrthrych]--;return 반환값;}
    if(Gweithrediad==6)return 화면보임(perchennog_gwrthrych);
    if(!너비값)return -9;
    int 이전표시=표시됨(perchennog_gwrthrych,너비값);
    if(Gweithrediad==1){int 바탕너비=보드화면너비(),바탕높이=보드화면높이();if(첫째값<0||SECOND_VALUE<0||cod_nod<1||cyrchfan_data<1||첫째값>바탕너비||SECOND_VALUE>바탕높이||cod_nod>바탕너비-첫째값||cyrchfan_data>바탕높이-SECOND_VALUE)return -22;너비값->cyfesuryn_x=첫째값;너비값->Y_cyfesuryn=SECOND_VALUE;너비값->너비값=cod_nod;너비값->높이값=cyrchfan_data;너비값->llaw_Llywio=1;}
    else if(Gweithrediad==2){teclyn_cyflwr *iselfen=elfen_VALUE(perchennog_gwrthrych,첫째값);if(!iselfen||iselfen==너비값||iselfen->ardal_VALUE==1)return -22;int data_safle=dynodwr_VALUE;for(int 깊이=0;data_safle&&깊이<32;깊이++){if(data_safle==첫째값)return -22;teclyn_cyflwr *위쪽=elfen_VALUE(perchennog_gwrthrych,data_safle);data_safle=위쪽?위쪽->부모항목:0;}iselfen->부모항목=dynodwr_VALUE;if(!iselfen->llaw_Llywio){int 형제요소=0;for(int 순번=0;순번<32;순번++)if(&요소들[perchennog_gwrthrych][순번]!=iselfen&&요소들[perchennog_gwrthrych][순번].부모항목==dynodwr_VALUE)형제요소++;iselfen->Y_cyfesuryn=16+형제요소*36;}}
    else if(Gweithrediad==3)너비값->보이는지=첫째값!=0;
    else if(Gweithrediad==4)너비값->보이는지=0;
    else if(Gweithrediad==7)너비값->Llywio_polisi=첫째값;
    else if(Gweithrediad==8)return 너비값->hyd_VALUE;
    else if(Gweithrediad==9)return 첫째값>=0&&(unsigned)첫째값<너비값->hyd_VALUE?너비값->Testun[첫째값]:-22;
    else return -22;
    if(이전표시||표시됨(perchennog_gwrthrych,너비값))bwrdd_Terfynell(3);return 0;
}
int 화면글(int perchennog_gwrthrych,int dynodwr_VALUE,const uint32_t *data,unsigned eitem_COUNT){teclyn_cyflwr *너비값=elfen_VALUE(perchennog_gwrthrych,dynodwr_VALUE);if(!너비값)return -9;if(eitem_COUNT>127)return -22;for(unsigned 순번=0;순번<eitem_COUNT;순번++){unsigned nod_amgodio=data[순번];if(nod_amgodio>0x10ffff||(nod_amgodio>=0xd800&&nod_amgodio<=0xdfff))return -22;}for(unsigned 순번=0;순번<eitem_COUNT;순번++)너비값->Testun[순번]=data[순번];너비값->hyd_VALUE=eitem_COUNT;if(표시됨(perchennog_gwrthrych,너비값))bwrdd_Terfynell(3);return 0;}
