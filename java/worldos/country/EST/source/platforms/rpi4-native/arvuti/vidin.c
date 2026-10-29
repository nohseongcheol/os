#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* Small native peer layer for the explicitly supported Swing subset. */
#include <stdint.h>
#include <stddef.h>
extern uintptr_t Tahvel_piksel(uintptr_t,uintptr_t,uintptr_t),Tahvel_terminal(uintptr_t);
extern void terminal_glüüf(unsigned,unsigned,unsigned,unsigned,unsigned);
extern void *memset(void *,int,size_t);
typedef struct { int ala_VALUE,ema,가로좌표,세로좌표,너비값,높이값,보이는지,käsitsi_küljend,küljend_eeskirjad;unsigned Tekst[128],길이; } vidin_Olek;
static vidin_Olek 요소들[4][32];
static int Fookuses[4],sündmus_Loend[4][16];static unsigned 첫항목[4],kirje_COUNT[4],부호없는결과[4],긴부호없는값[4];
static void Sündmus(int omanik_objekt,int VALUE){if(kirje_COUNT[omanik_objekt]<16){sündmus_Loend[omanik_objekt][(첫항목[omanik_objekt]+kirje_COUNT[omanik_objekt])%16]=VALUE;kirje_COUNT[omanik_objekt]++;}}
static vidin_Olek *element_VALUE(int omanik_objekt,int identifikaator_VALUE){return omanik_objekt>=0&&omanik_objekt<4&&identifikaator_VALUE>0&&identifikaator_VALUE<=32&&요소들[omanik_objekt][identifikaator_VALUE-1].ala_VALUE?&요소들[omanik_objekt][identifikaator_VALUE-1]:0;}
static void 사각영역(int 가로좌표,int 세로좌표,int 너비값,int 높이값,unsigned 색상){Tahvel_ristkülik_täide(가로좌표,세로좌표,너비값,높이값,색상);}
int 화면보임(int omanik_objekt){if(omanik_objekt<0||omanik_objekt>=4)return 0;for(int 순번=0;순번<32;순번++)if(요소들[omanik_objekt][순번].ala_VALUE==1&&요소들[omanik_objekt][순번].보이는지)return 1;return 0;}
void 화면초기화(int omanik_objekt){memset(요소들[omanik_objekt],0,sizeof(요소들[omanik_objekt]));kirje_COUNT[omanik_objekt]=첫항목[omanik_objekt]=Fookuses[omanik_objekt]=긴부호없는값[omanik_objekt]=0;}
static void Asukoht(int omanik_objekt,vidin_Olek *너비값,int *가로좌표,int *세로좌표){*가로좌표=너비값->가로좌표;*세로좌표=너비값->세로좌표;int andmed_ametikoht=너비값->ema;for(int kaup_COUNT=0;andmed_ametikoht&&kaup_COUNT<32;kaup_COUNT++){vidin_Olek *위쪽=element_VALUE(omanik_objekt,andmed_ametikoht);if(!위쪽)break;*가로좌표+=위쪽->가로좌표;*세로좌표+=위쪽->세로좌표+(위쪽->ala_VALUE==1?30:0);andmed_ametikoht=위쪽->ema;}}
static int 표시됨(int omanik_objekt,vidin_Olek *너비값){for(int kaup_COUNT=0;kaup_COUNT<32;kaup_COUNT++){if(!너비값->보이는지)return 0;if(너비값->ala_VALUE==1)return 1;너비값=element_VALUE(omanik_objekt,너비값->ema);if(!너비값)return 0;}return 0;}
static void Tekst(int 가로좌표,int 세로좌표,vidin_Olek *너비값,int 최대값,unsigned 색상,unsigned 배경색){int tähtaja_piires_ametikoht=0;for(unsigned 순번=0;순번<너비값->길이;순번++){unsigned märk_kodeerimine=너비값->Tekst[순번],너비=märk_kodeerimine>=256?16:8;if(tähtaja_piires_ametikoht+(int)너비>최대값)break;terminal_glüüf(가로좌표+tähtaja_piires_ametikoht,세로좌표,märk_kodeerimine,색상,배경색);tähtaja_piires_ametikoht+=너비;}}
void 화면다시그림(int omanik_objekt){
    if(!화면보임(omanik_objekt))return;
    for(int töötlemine_tellimus=1;töötlemine_tellimus<=5;töötlemine_tellimus++)for(int 순번=0;순번<32;순번++){
        vidin_Olek *너비값=&요소들[omanik_objekt][순번];if(너비값->ala_VALUE!=töötlemine_tellimus||!표시됨(omanik_objekt,너비값))continue;int 가로좌표,세로좌표;Asukoht(omanik_objekt,너비값,&가로좌표,&세로좌표);
        if(töötlemine_tellimus==1){사각영역(가로좌표,세로좌표,너비값->너비값,너비값->높이값,0xeee9e0);사각영역(가로좌표,세로좌표,너비값->너비값,30,0x905020);Tekst(가로좌표+10,세로좌표+7,너비값,너비값->너비값-50,0xffffff,0x905020);사각영역(가로좌표+너비값->너비값-28,세로좌표+4,24,22,0x5555b8);terminal_glüüf(가로좌표+너비값->너비값-20,세로좌표+7,'X',0xffffff,0x5555b8);}
        if(töötlemine_tellimus==2)사각영역(가로좌표,세로좌표,너비값->너비값,너비값->높이값,0xeee9e0);
        if(töötlemine_tellimus>=3){unsigned 배경색=töötlemine_tellimus==4?0xc0ab86:töötlemine_tellimus==5?0xffffff:0xeee9e0;if(töötlemine_tellimus!=3)사각영역(가로좌표,세로좌표,너비값->너비값,너비값->높이값,배경색);Tekst(가로좌표+4,세로좌표+4,너비값,너비값->너비값-8,0x201a15,배경색);if(töötlemine_tellimus==5&&Fookuses[omanik_objekt]==순번+1)사각영역(가로좌표,세로좌표+너비값->높이값-2,너비값->너비값,2,0x905020);}
    }
}
int 화면덮음(int omanik_objekt,int 가로좌표,int 세로좌표){
    if(!화면보임(omanik_objekt))return 0;
    for(int 순번=0;순번<32;순번++){
        vidin_Olek *aken=&요소들[omanik_objekt][순번];
        if(aken->ala_VALUE==1&&aken->보이는지&&가로좌표>=aken->가로좌표&&세로좌표>=aken->세로좌표&&
           가로좌표<aken->가로좌표+aken->너비값&&세로좌표<aken->세로좌표+aken->높이값)return 1;
    }return 0;
}
int 화면가리킴(int omanik_objekt,unsigned 눌림,int 가로좌표,int 세로좌표){
    if(!화면보임(omanik_objekt))return 0;
    if(눌림&1)for(int 순번=31;순번>=0;순번--){vidin_Olek *너비값=&요소들[omanik_objekt][순번];if(!너비값->ala_VALUE||!표시됨(omanik_objekt,너비값))continue;int aken_X,aken_Y;Asukoht(omanik_objekt,너비값,&aken_X,&aken_Y);
        if(가로좌표<aken_X||세로좌표<aken_Y||가로좌표>=aken_X+너비값->너비값||세로좌표>=aken_Y+너비값->높이값)continue;
        if(너비값->ala_VALUE==1&&세로좌표<aken_Y+30&&가로좌표>=aken_X+너비값->너비값-28){if(너비값->küljend_eeskirjad!=0)너비값->보이는지=0;Sündmus(omanik_objekt,0x10000+순번+1);Tahvel_terminal(3);return 1;}
        if(너비값->ala_VALUE==4){Sündmus(omanik_objekt,순번+1);return 1;}if(너비값->ala_VALUE==5){Fookuses[omanik_objekt]=순번+1;Tahvel_terminal(3);return 1;}
        if(너비값->ala_VALUE==1)return 1;
    }return 0;
}
void 화면누름(int omanik_objekt,unsigned SECOND_VALUE){
    vidin_Olek *너비값=element_VALUE(omanik_objekt,Fookuses[omanik_objekt]);if(!너비값||너비값->ala_VALUE!=5)return;
    if(SECOND_VALUE==13||SECOND_VALUE==10){Sündmus(omanik_objekt,Fookuses[omanik_objekt]);return;}
    if(SECOND_VALUE==8||SECOND_VALUE==127){if(너비값->길이)너비값->길이--;긴부호없는값[omanik_objekt]=0;}
    else{
        unsigned märk_kodeerimine=SECOND_VALUE;
        if(긴부호없는값[omanik_objekt]){if((SECOND_VALUE&192)!=128){긴부호없는값[omanik_objekt]=0;return;}부호없는결과[omanik_objekt]=(부호없는결과[omanik_objekt]<<6)|(SECOND_VALUE&63);if(--긴부호없는값[omanik_objekt])return;märk_kodeerimine=부호없는결과[omanik_objekt];}
        else if(SECOND_VALUE>=0xc2&&SECOND_VALUE<=0xf4){긴부호없는값[omanik_objekt]=SECOND_VALUE<0xe0?1:SECOND_VALUE<0xf0?2:3;부호없는결과[omanik_objekt]=SECOND_VALUE&((1u<<(6-긴부호없는값[omanik_objekt]))-1);return;}
        else if(SECOND_VALUE<32||SECOND_VALUE>=128)return;
        if(märk_kodeerimine>0x10ffff||(märk_kodeerimine>=0xd800&&märk_kodeerimine<=0xdfff))return;if(너비값->길이<127)너비값->Tekst[너비값->길이++]=märk_kodeerimine;
    }
    Tahvel_terminal(3);
}
int 화면호출(int omanik_objekt,unsigned Nimi,int identifikaator_VALUE,int 첫째값,int SECOND_VALUE,int koodipunkt,int sihtkoht_andmed){
    if(omanik_objekt<0||omanik_objekt>=4)return -22;vidin_Olek *너비값=element_VALUE(omanik_objekt,identifikaator_VALUE);
    if(Nimi==0){if(identifikaator_VALUE<1||identifikaator_VALUE>5)return -22;for(int 순번=0;순번<32;순번++)if(요소들[omanik_objekt][순번].ala_VALUE==0){너비값=&요소들[omanik_objekt][순번];memset(너비값,0,sizeof(*너비값));너비값->ala_VALUE=identifikaator_VALUE;너비값->보이는지=identifikaator_VALUE!=1;너비값->너비값=identifikaator_VALUE==1?380:220;너비값->높이값=identifikaator_VALUE==1?240:28;너비값->küljend_eeskirjad=1;너비값->가로좌표=identifikaator_VALUE==1?130:16;너비값->세로좌표=identifikaator_VALUE==1?110:16;return 순번+1;}return -28;}
    if(Nimi==5){if(!kirje_COUNT[omanik_objekt])return 0;int 반환값=sündmus_Loend[omanik_objekt][첫항목[omanik_objekt]];첫항목[omanik_objekt]=(첫항목[omanik_objekt]+1)%16;kirje_COUNT[omanik_objekt]--;return 반환값;}
    if(Nimi==6)return 화면보임(omanik_objekt);
    if(!너비값)return -9;
    int 이전표시=표시됨(omanik_objekt,너비값);
    if(Nimi==1){int 바탕너비=보드화면너비(),바탕높이=보드화면높이();if(첫째값<0||SECOND_VALUE<0||koodipunkt<1||sihtkoht_andmed<1||첫째값>바탕너비||SECOND_VALUE>바탕높이||koodipunkt>바탕너비-첫째값||sihtkoht_andmed>바탕높이-SECOND_VALUE)return -22;너비값->가로좌표=첫째값;너비값->세로좌표=SECOND_VALUE;너비값->너비값=koodipunkt;너비값->높이값=sihtkoht_andmed;너비값->käsitsi_küljend=1;}
    else if(Nimi==2){vidin_Olek *tütar=element_VALUE(omanik_objekt,첫째값);if(!tütar||tütar==너비값||tütar->ala_VALUE==1)return -22;int andmed_ametikoht=identifikaator_VALUE;for(int 깊이=0;andmed_ametikoht&&깊이<32;깊이++){if(andmed_ametikoht==첫째값)return -22;vidin_Olek *위쪽=element_VALUE(omanik_objekt,andmed_ametikoht);andmed_ametikoht=위쪽?위쪽->ema:0;}tütar->ema=identifikaator_VALUE;if(!tütar->käsitsi_küljend){int 형제요소=0;for(int 순번=0;순번<32;순번++)if(&요소들[omanik_objekt][순번]!=tütar&&요소들[omanik_objekt][순번].ema==identifikaator_VALUE)형제요소++;tütar->세로좌표=16+형제요소*36;}}
    else if(Nimi==3)너비값->보이는지=첫째값!=0;
    else if(Nimi==4)너비값->보이는지=0;
    else if(Nimi==7)너비값->küljend_eeskirjad=첫째값;
    else if(Nimi==8)return 너비값->길이;
    else if(Nimi==9)return 첫째값>=0&&(unsigned)첫째값<너비값->길이?너비값->Tekst[첫째값]:-22;
    else return -22;
    if(이전표시||표시됨(omanik_objekt,너비값))Tahvel_terminal(3);return 0;
}
int 화면글(int omanik_objekt,int identifikaator_VALUE,const uint32_t *andmed,unsigned kaup_COUNT){vidin_Olek *너비값=element_VALUE(omanik_objekt,identifikaator_VALUE);if(!너비값)return -9;if(kaup_COUNT>127)return -22;for(unsigned 순번=0;순번<kaup_COUNT;순번++){unsigned märk_kodeerimine=andmed[순번];if(märk_kodeerimine>0x10ffff||(märk_kodeerimine>=0xd800&&märk_kodeerimine<=0xdfff))return -22;}for(unsigned 순번=0;순번<kaup_COUNT;순번++)너비값->Tekst[순번]=andmed[순번];너비값->길이=kaup_COUNT;if(표시됨(omanik_objekt,너비값))Tahvel_terminal(3);return 0;}
