#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* Small native peer layer for the explicitly supported Swing subset. */
#include <stdint.h>
#include <stddef.h>
extern uintptr_t Tavle_piksel(uintptr_t,uintptr_t,uintptr_t),Tavle_Terminal(uintptr_t);
extern void Terminal_figur(unsigned,unsigned,unsigned,unsigned,unsigned);
extern void *memset(void *,int,size_t);
typedef struct { int kategori_VALUE,forelder,x_koordinat,Y_koordinat,너비값,높이값,보이는지,manuell_Oppsett,Oppsett_policy;unsigned Tekst[128],lengd_VALUE; } miniprogram_status;
static miniprogram_status 요소들[4][32];
static int Fokus_f7e69dab[4],hending_Liste[4][16];static unsigned 첫항목[4],oppføring_COUNT[4],부호없는결과[4],긴부호없는값[4];
static void Hending(int eigar_objekt,int VALUE){if(oppføring_COUNT[eigar_objekt]<16){hending_Liste[eigar_objekt][(첫항목[eigar_objekt]+oppføring_COUNT[eigar_objekt])%16]=VALUE;oppføring_COUNT[eigar_objekt]++;}}
static miniprogram_status *element_VALUE(int eigar_objekt,int identifikator_VALUE){return eigar_objekt>=0&&eigar_objekt<4&&identifikator_VALUE>0&&identifikator_VALUE<=32&&요소들[eigar_objekt][identifikator_VALUE-1].kategori_VALUE?&요소들[eigar_objekt][identifikator_VALUE-1]:0;}
static void 사각영역(int x_koordinat,int Y_koordinat,int 너비값,int 높이값,unsigned 색상){보드사각그림(x_koordinat,Y_koordinat,너비값,높이값,색상);}
int 화면보임(int eigar_objekt){if(eigar_objekt<0||eigar_objekt>=4)return 0;for(int 순번=0;순번<32;순번++)if(요소들[eigar_objekt][순번].kategori_VALUE==1&&요소들[eigar_objekt][순번].보이는지)return 1;return 0;}
void 화면초기화(int eigar_objekt){memset(요소들[eigar_objekt],0,sizeof(요소들[eigar_objekt]));oppføring_COUNT[eigar_objekt]=첫항목[eigar_objekt]=Fokus_f7e69dab[eigar_objekt]=긴부호없는값[eigar_objekt]=0;}
static void Posisjon(int eigar_objekt,miniprogram_status *너비값,int *x_koordinat,int *Y_koordinat){*x_koordinat=너비값->x_koordinat;*Y_koordinat=너비값->Y_koordinat;int data_plassere=너비값->forelder;for(int vare_COUNT=0;data_plassere&&vare_COUNT<32;vare_COUNT++){miniprogram_status *위쪽=element_VALUE(eigar_objekt,data_plassere);if(!위쪽)break;*x_koordinat+=위쪽->x_koordinat;*Y_koordinat+=위쪽->Y_koordinat+(위쪽->kategori_VALUE==1?30:0);data_plassere=위쪽->forelder;}}
static int 표시됨(int eigar_objekt,miniprogram_status *너비값){for(int vare_COUNT=0;vare_COUNT<32;vare_COUNT++){if(!너비값->보이는지)return 0;if(너비값->kategori_VALUE==1)return 1;너비값=element_VALUE(eigar_objekt,너비값->forelder);if(!너비값)return 0;}return 0;}
static void Tekst(int x_koordinat,int Y_koordinat,miniprogram_status *너비값,int 최대값,unsigned 색상,unsigned 배경색){int betalt_plassere=0;for(unsigned 순번=0;순번<너비값->lengd_VALUE;순번++){unsigned teikn_koding=너비값->Tekst[순번],너비=teikn_koding>=256?16:8;if(betalt_plassere+(int)너비>최대값)break;Terminal_figur(x_koordinat+betalt_plassere,Y_koordinat,teikn_koding,색상,배경색);betalt_plassere+=너비;}}
void 화면다시그림(int eigar_objekt){
    if(!화면보임(eigar_objekt))return;
    for(int 처리차례=1;처리차례<=5;처리차례++)for(int 순번=0;순번<32;순번++){
        miniprogram_status *너비값=&요소들[eigar_objekt][순번];if(너비값->kategori_VALUE!=처리차례||!표시됨(eigar_objekt,너비값))continue;int x_koordinat,Y_koordinat;Posisjon(eigar_objekt,너비값,&x_koordinat,&Y_koordinat);
        if(처리차례==1){사각영역(x_koordinat,Y_koordinat,너비값->너비값,너비값->높이값,0xeee9e0);사각영역(x_koordinat,Y_koordinat,너비값->너비값,30,0x905020);Tekst(x_koordinat+10,Y_koordinat+7,너비값,너비값->너비값-50,0xffffff,0x905020);사각영역(x_koordinat+너비값->너비값-28,Y_koordinat+4,24,22,0x5555b8);Terminal_figur(x_koordinat+너비값->너비값-20,Y_koordinat+7,'X',0xffffff,0x5555b8);}
        if(처리차례==2)사각영역(x_koordinat,Y_koordinat,너비값->너비값,너비값->높이값,0xeee9e0);
        if(처리차례>=3){unsigned 배경색=처리차례==4?0xc0ab86:처리차례==5?0xffffff:0xeee9e0;if(처리차례!=3)사각영역(x_koordinat,Y_koordinat,너비값->너비값,너비값->높이값,배경색);Tekst(x_koordinat+4,Y_koordinat+4,너비값,너비값->너비값-8,0x201a15,배경색);if(처리차례==5&&Fokus_f7e69dab[eigar_objekt]==순번+1)사각영역(x_koordinat,Y_koordinat+너비값->높이값-2,너비값->너비값,2,0x905020);}
    }
}
int 화면덮음(int eigar_objekt,int x_koordinat,int Y_koordinat){
    if(!화면보임(eigar_objekt))return 0;
    for(int 순번=0;순번<32;순번++){
        miniprogram_status *vindauge=&요소들[eigar_objekt][순번];
        if(vindauge->kategori_VALUE==1&&vindauge->보이는지&&x_koordinat>=vindauge->x_koordinat&&Y_koordinat>=vindauge->Y_koordinat&&
           x_koordinat<vindauge->x_koordinat+vindauge->너비값&&Y_koordinat<vindauge->Y_koordinat+vindauge->높이값)return 1;
    }return 0;
}
int 화면가리킴(int eigar_objekt,unsigned 눌림,int x_koordinat,int Y_koordinat){
    if(!화면보임(eigar_objekt))return 0;
    if(눌림&1)for(int 순번=31;순번>=0;순번--){miniprogram_status *너비값=&요소들[eigar_objekt][순번];if(!너비값->kategori_VALUE||!표시됨(eigar_objekt,너비값))continue;int vindauge_X,vindauge_Y;Posisjon(eigar_objekt,너비값,&vindauge_X,&vindauge_Y);
        if(x_koordinat<vindauge_X||Y_koordinat<vindauge_Y||x_koordinat>=vindauge_X+너비값->너비값||Y_koordinat>=vindauge_Y+너비값->높이값)continue;
        if(너비값->kategori_VALUE==1&&Y_koordinat<vindauge_Y+30&&x_koordinat>=vindauge_X+너비값->너비값-28){if(너비값->Oppsett_policy!=0)너비값->보이는지=0;Hending(eigar_objekt,0x10000+순번+1);Tavle_Terminal(3);return 1;}
        if(너비값->kategori_VALUE==4){Hending(eigar_objekt,순번+1);return 1;}if(너비값->kategori_VALUE==5){Fokus_f7e69dab[eigar_objekt]=순번+1;Tavle_Terminal(3);return 1;}
        if(너비값->kategori_VALUE==1)return 1;
    }return 0;
}
void 화면누름(int eigar_objekt,unsigned SECOND_VALUE){
    miniprogram_status *너비값=element_VALUE(eigar_objekt,Fokus_f7e69dab[eigar_objekt]);if(!너비값||너비값->kategori_VALUE!=5)return;
    if(SECOND_VALUE==13||SECOND_VALUE==10){Hending(eigar_objekt,Fokus_f7e69dab[eigar_objekt]);return;}
    if(SECOND_VALUE==8||SECOND_VALUE==127){if(너비값->lengd_VALUE)너비값->lengd_VALUE--;긴부호없는값[eigar_objekt]=0;}
    else{
        unsigned teikn_koding=SECOND_VALUE;
        if(긴부호없는값[eigar_objekt]){if((SECOND_VALUE&192)!=128){긴부호없는값[eigar_objekt]=0;return;}부호없는결과[eigar_objekt]=(부호없는결과[eigar_objekt]<<6)|(SECOND_VALUE&63);if(--긴부호없는값[eigar_objekt])return;teikn_koding=부호없는결과[eigar_objekt];}
        else if(SECOND_VALUE>=0xc2&&SECOND_VALUE<=0xf4){긴부호없는값[eigar_objekt]=SECOND_VALUE<0xe0?1:SECOND_VALUE<0xf0?2:3;부호없는결과[eigar_objekt]=SECOND_VALUE&((1u<<(6-긴부호없는값[eigar_objekt]))-1);return;}
        else if(SECOND_VALUE<32||SECOND_VALUE>=128)return;
        if(teikn_koding>0x10ffff||(teikn_koding>=0xd800&&teikn_koding<=0xdfff))return;if(너비값->lengd_VALUE<127)너비값->Tekst[너비값->lengd_VALUE++]=teikn_koding;
    }
    Tavle_Terminal(3);
}
int 화면호출(int eigar_objekt,unsigned Handling,int identifikator_VALUE,int 첫째값,int SECOND_VALUE,int teiknkode,int mål_data){
    if(eigar_objekt<0||eigar_objekt>=4)return -22;miniprogram_status *너비값=element_VALUE(eigar_objekt,identifikator_VALUE);
    if(Handling==0){if(identifikator_VALUE<1||identifikator_VALUE>5)return -22;for(int 순번=0;순번<32;순번++)if(요소들[eigar_objekt][순번].kategori_VALUE==0){너비값=&요소들[eigar_objekt][순번];memset(너비값,0,sizeof(*너비값));너비값->kategori_VALUE=identifikator_VALUE;너비값->보이는지=identifikator_VALUE!=1;너비값->너비값=identifikator_VALUE==1?380:220;너비값->높이값=identifikator_VALUE==1?240:28;너비값->Oppsett_policy=1;너비값->x_koordinat=identifikator_VALUE==1?130:16;너비값->Y_koordinat=identifikator_VALUE==1?110:16;return 순번+1;}return -28;}
    if(Handling==5){if(!oppføring_COUNT[eigar_objekt])return 0;int 반환값=hending_Liste[eigar_objekt][첫항목[eigar_objekt]];첫항목[eigar_objekt]=(첫항목[eigar_objekt]+1)%16;oppføring_COUNT[eigar_objekt]--;return 반환값;}
    if(Handling==6)return 화면보임(eigar_objekt);
    if(!너비값)return -9;
    int 이전표시=표시됨(eigar_objekt,너비값);
    if(Handling==1){int 바탕너비=보드화면너비(),바탕높이=보드화면높이();if(첫째값<0||SECOND_VALUE<0||teiknkode<1||mål_data<1||첫째값>바탕너비||SECOND_VALUE>바탕높이||teiknkode>바탕너비-첫째값||mål_data>바탕높이-SECOND_VALUE)return -22;너비값->x_koordinat=첫째값;너비값->Y_koordinat=SECOND_VALUE;너비값->너비값=teiknkode;너비값->높이값=mål_data;너비값->manuell_Oppsett=1;}
    else if(Handling==2){miniprogram_status *underordna_element=element_VALUE(eigar_objekt,첫째값);if(!underordna_element||underordna_element==너비값||underordna_element->kategori_VALUE==1)return -22;int data_plassere=identifikator_VALUE;for(int 깊이=0;data_plassere&&깊이<32;깊이++){if(data_plassere==첫째값)return -22;miniprogram_status *위쪽=element_VALUE(eigar_objekt,data_plassere);data_plassere=위쪽?위쪽->forelder:0;}underordna_element->forelder=identifikator_VALUE;if(!underordna_element->manuell_Oppsett){int 형제요소=0;for(int 순번=0;순번<32;순번++)if(&요소들[eigar_objekt][순번]!=underordna_element&&요소들[eigar_objekt][순번].forelder==identifikator_VALUE)형제요소++;underordna_element->Y_koordinat=16+형제요소*36;}}
    else if(Handling==3)너비값->보이는지=첫째값!=0;
    else if(Handling==4)너비값->보이는지=0;
    else if(Handling==7)너비값->Oppsett_policy=첫째값;
    else if(Handling==8)return 너비값->lengd_VALUE;
    else if(Handling==9)return 첫째값>=0&&(unsigned)첫째값<너비값->lengd_VALUE?너비값->Tekst[첫째값]:-22;
    else return -22;
    if(이전표시||표시됨(eigar_objekt,너비값))Tavle_Terminal(3);return 0;
}
int 화면글(int eigar_objekt,int identifikator_VALUE,const uint32_t *data,unsigned vare_COUNT){miniprogram_status *너비값=element_VALUE(eigar_objekt,identifikator_VALUE);if(!너비값)return -9;if(vare_COUNT>127)return -22;for(unsigned 순번=0;순번<vare_COUNT;순번++){unsigned teikn_koding=data[순번];if(teikn_koding>0x10ffff||(teikn_koding>=0xd800&&teikn_koding<=0xdfff))return -22;}for(unsigned 순번=0;순번<vare_COUNT;순번++)너비값->Tekst[순번]=data[순번];너비값->lengd_VALUE=vare_COUNT;if(표시됨(eigar_objekt,너비값))Tavle_Terminal(3);return 0;}
