#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* Small native peer layer for the explicitly supported Swing subset. */
#include <stdint.h>
#include <stddef.h>
extern uintptr_t papa_pika(uintptr_t,uintptr_t,uintptr_t),papa_Tauranga(uintptr_t);
extern void Tauranga_kiriwhi(unsigned,unsigned,unsigned,unsigned,unsigned);
extern void *memset(void *,int,size_t);
typedef struct { int kāwai_uara,부모항목,taunga_x,세로좌표,너비값,높이값,보이는지,ā_ringa_Tahora,Tahora_kaupapahere;unsigned Ngā_kupu[128],roa_uara; } taputapu_tūnga;
static taputapu_tūnga 요소들[4][32];
static int Arotahi_f7e69dab[4],hui_Rārangi[4][16];static unsigned 첫항목[4],tāurunga_COUNT[4],부호없는결과[4],긴부호없는값[4];
static void hui(int kaipupuri_ahanoa,int uara){if(tāurunga_COUNT[kaipupuri_ahanoa]<16){hui_Rārangi[kaipupuri_ahanoa][(첫항목[kaipupuri_ahanoa]+tāurunga_COUNT[kaipupuri_ahanoa])%16]=uara;tāurunga_COUNT[kaipupuri_ahanoa]++;}}
static taputapu_tūnga *huānga_uara(int kaipupuri_ahanoa,int pūtāutu_uara){return kaipupuri_ahanoa>=0&&kaipupuri_ahanoa<4&&pūtāutu_uara>0&&pūtāutu_uara<=32&&요소들[kaipupuri_ahanoa][pūtāutu_uara-1].kāwai_uara?&요소들[kaipupuri_ahanoa][pūtāutu_uara-1]:0;}
static void 사각영역(int taunga_x,int 세로좌표,int 너비값,int 높이값,unsigned 색상){보드사각그림(taunga_x,세로좌표,너비값,높이값,색상);}
int 화면보임(int kaipupuri_ahanoa){if(kaipupuri_ahanoa<0||kaipupuri_ahanoa>=4)return 0;for(int 순번=0;순번<32;순번++)if(요소들[kaipupuri_ahanoa][순번].kāwai_uara==1&&요소들[kaipupuri_ahanoa][순번].보이는지)return 1;return 0;}
void 화면초기화(int kaipupuri_ahanoa){memset(요소들[kaipupuri_ahanoa],0,sizeof(요소들[kaipupuri_ahanoa]));tāurunga_COUNT[kaipupuri_ahanoa]=첫항목[kaipupuri_ahanoa]=Arotahi_f7e69dab[kaipupuri_ahanoa]=긴부호없는값[kaipupuri_ahanoa]=0;}
static void tūranga(int kaipupuri_ahanoa,taputapu_tūnga *너비값,int *taunga_x,int *세로좌표){*taunga_x=너비값->taunga_x;*세로좌표=너비값->세로좌표;int raraunga_tūranga=너비값->부모항목;for(int tuemi_COUNT=0;raraunga_tūranga&&tuemi_COUNT<32;tuemi_COUNT++){taputapu_tūnga *위쪽=huānga_uara(kaipupuri_ahanoa,raraunga_tūranga);if(!위쪽)break;*taunga_x+=위쪽->taunga_x;*세로좌표+=위쪽->세로좌표+(위쪽->kāwai_uara==1?30:0);raraunga_tūranga=위쪽->부모항목;}}
static int 표시됨(int kaipupuri_ahanoa,taputapu_tūnga *너비값){for(int tuemi_COUNT=0;tuemi_COUNT<32;tuemi_COUNT++){if(!너비값->보이는지)return 0;if(너비값->kāwai_uara==1)return 1;너비값=huānga_uara(kaipupuri_ahanoa,너비값->부모항목);if(!너비값)return 0;}return 0;}
static void Ngā_kupu(int taunga_x,int 세로좌표,taputapu_tūnga *너비값,int 최대값,unsigned 색상,unsigned 배경색){int 현재위치=0;for(unsigned 순번=0;순번<너비값->roa_uara;순번++){unsigned pūāhua_whakawaehere=너비값->Ngā_kupu[순번],너비=pūāhua_whakawaehere>=256?16:8;if(현재위치+(int)너비>최대값)break;Tauranga_kiriwhi(taunga_x+현재위치,세로좌표,pūāhua_whakawaehere,색상,배경색);현재위치+=너비;}}
void 화면다시그림(int kaipupuri_ahanoa){
    if(!화면보임(kaipupuri_ahanoa))return;
    for(int 처리차례=1;처리차례<=5;처리차례++)for(int 순번=0;순번<32;순번++){
        taputapu_tūnga *너비값=&요소들[kaipupuri_ahanoa][순번];if(너비값->kāwai_uara!=처리차례||!표시됨(kaipupuri_ahanoa,너비값))continue;int taunga_x,세로좌표;tūranga(kaipupuri_ahanoa,너비값,&taunga_x,&세로좌표);
        if(처리차례==1){사각영역(taunga_x,세로좌표,너비값->너비값,너비값->높이값,0xeee9e0);사각영역(taunga_x,세로좌표,너비값->너비값,30,0x905020);Ngā_kupu(taunga_x+10,세로좌표+7,너비값,너비값->너비값-50,0xffffff,0x905020);사각영역(taunga_x+너비값->너비값-28,세로좌표+4,24,22,0x5555b8);Tauranga_kiriwhi(taunga_x+너비값->너비값-20,세로좌표+7,'X',0xffffff,0x5555b8);}
        if(처리차례==2)사각영역(taunga_x,세로좌표,너비값->너비값,너비값->높이값,0xeee9e0);
        if(처리차례>=3){unsigned 배경색=처리차례==4?0xc0ab86:처리차례==5?0xffffff:0xeee9e0;if(처리차례!=3)사각영역(taunga_x,세로좌표,너비값->너비값,너비값->높이값,배경색);Ngā_kupu(taunga_x+4,세로좌표+4,너비값,너비값->너비값-8,0x201a15,배경색);if(처리차례==5&&Arotahi_f7e69dab[kaipupuri_ahanoa]==순번+1)사각영역(taunga_x,세로좌표+너비값->높이값-2,너비값->너비값,2,0x905020);}
    }
}
int 화면덮음(int kaipupuri_ahanoa,int taunga_x,int 세로좌표){
    if(!화면보임(kaipupuri_ahanoa))return 0;
    for(int 순번=0;순번<32;순번++){
        taputapu_tūnga *matapihi=&요소들[kaipupuri_ahanoa][순번];
        if(matapihi->kāwai_uara==1&&matapihi->보이는지&&taunga_x>=matapihi->taunga_x&&세로좌표>=matapihi->세로좌표&&
           taunga_x<matapihi->taunga_x+matapihi->너비값&&세로좌표<matapihi->세로좌표+matapihi->높이값)return 1;
    }return 0;
}
int 화면가리킴(int kaipupuri_ahanoa,unsigned 눌림,int taunga_x,int 세로좌표){
    if(!화면보임(kaipupuri_ahanoa))return 0;
    if(눌림&1)for(int 순번=31;순번>=0;순번--){taputapu_tūnga *너비값=&요소들[kaipupuri_ahanoa][순번];if(!너비값->kāwai_uara||!표시됨(kaipupuri_ahanoa,너비값))continue;int 창가로,창세로;tūranga(kaipupuri_ahanoa,너비값,&창가로,&창세로);
        if(taunga_x<창가로||세로좌표<창세로||taunga_x>=창가로+너비값->너비값||세로좌표>=창세로+너비값->높이값)continue;
        if(너비값->kāwai_uara==1&&세로좌표<창세로+30&&taunga_x>=창가로+너비값->너비값-28){if(너비값->Tahora_kaupapahere!=0)너비값->보이는지=0;hui(kaipupuri_ahanoa,0x10000+순번+1);papa_Tauranga(3);return 1;}
        if(너비값->kāwai_uara==4){hui(kaipupuri_ahanoa,순번+1);return 1;}if(너비값->kāwai_uara==5){Arotahi_f7e69dab[kaipupuri_ahanoa]=순번+1;papa_Tauranga(3);return 1;}
        if(너비값->kāwai_uara==1)return 1;
    }return 0;
}
void 화면누름(int kaipupuri_ahanoa,unsigned SECOND_uara){
    taputapu_tūnga *너비값=huānga_uara(kaipupuri_ahanoa,Arotahi_f7e69dab[kaipupuri_ahanoa]);if(!너비값||너비값->kāwai_uara!=5)return;
    if(SECOND_uara==13||SECOND_uara==10){hui(kaipupuri_ahanoa,Arotahi_f7e69dab[kaipupuri_ahanoa]);return;}
    if(SECOND_uara==8||SECOND_uara==127){if(너비값->roa_uara)너비값->roa_uara--;긴부호없는값[kaipupuri_ahanoa]=0;}
    else{
        unsigned pūāhua_whakawaehere=SECOND_uara;
        if(긴부호없는값[kaipupuri_ahanoa]){if((SECOND_uara&192)!=128){긴부호없는값[kaipupuri_ahanoa]=0;return;}부호없는결과[kaipupuri_ahanoa]=(부호없는결과[kaipupuri_ahanoa]<<6)|(SECOND_uara&63);if(--긴부호없는값[kaipupuri_ahanoa])return;pūāhua_whakawaehere=부호없는결과[kaipupuri_ahanoa];}
        else if(SECOND_uara>=0xc2&&SECOND_uara<=0xf4){긴부호없는값[kaipupuri_ahanoa]=SECOND_uara<0xe0?1:SECOND_uara<0xf0?2:3;부호없는결과[kaipupuri_ahanoa]=SECOND_uara&((1u<<(6-긴부호없는값[kaipupuri_ahanoa]))-1);return;}
        else if(SECOND_uara<32||SECOND_uara>=128)return;
        if(pūāhua_whakawaehere>0x10ffff||(pūāhua_whakawaehere>=0xd800&&pūāhua_whakawaehere<=0xdfff))return;if(너비값->roa_uara<127)너비값->Ngā_kupu[너비값->roa_uara++]=pūāhua_whakawaehere;
    }
    papa_Tauranga(3);
}
int 화면호출(int kaipupuri_ahanoa,unsigned hohenga,int pūtāutu_uara,int 첫째값,int SECOND_uara,int waehere_pūāhua,int ūnga_raraunga){
    if(kaipupuri_ahanoa<0||kaipupuri_ahanoa>=4)return -22;taputapu_tūnga *너비값=huānga_uara(kaipupuri_ahanoa,pūtāutu_uara);
    if(hohenga==0){if(pūtāutu_uara<1||pūtāutu_uara>5)return -22;for(int 순번=0;순번<32;순번++)if(요소들[kaipupuri_ahanoa][순번].kāwai_uara==0){너비값=&요소들[kaipupuri_ahanoa][순번];memset(너비값,0,sizeof(*너비값));너비값->kāwai_uara=pūtāutu_uara;너비값->보이는지=pūtāutu_uara!=1;너비값->너비값=pūtāutu_uara==1?380:220;너비값->높이값=pūtāutu_uara==1?240:28;너비값->Tahora_kaupapahere=1;너비값->taunga_x=pūtāutu_uara==1?130:16;너비값->세로좌표=pūtāutu_uara==1?110:16;return 순번+1;}return -28;}
    if(hohenga==5){if(!tāurunga_COUNT[kaipupuri_ahanoa])return 0;int 반환값=hui_Rārangi[kaipupuri_ahanoa][첫항목[kaipupuri_ahanoa]];첫항목[kaipupuri_ahanoa]=(첫항목[kaipupuri_ahanoa]+1)%16;tāurunga_COUNT[kaipupuri_ahanoa]--;return 반환값;}
    if(hohenga==6)return 화면보임(kaipupuri_ahanoa);
    if(!너비값)return -9;
    int 이전표시=표시됨(kaipupuri_ahanoa,너비값);
    if(hohenga==1){int 바탕너비=보드화면너비(),바탕높이=보드화면높이();if(첫째값<0||SECOND_uara<0||waehere_pūāhua<1||ūnga_raraunga<1||첫째값>바탕너비||SECOND_uara>바탕높이||waehere_pūāhua>바탕너비-첫째값||ūnga_raraunga>바탕높이-SECOND_uara)return -22;너비값->taunga_x=첫째값;너비값->세로좌표=SECOND_uara;너비값->너비값=waehere_pūāhua;너비값->높이값=ūnga_raraunga;너비값->ā_ringa_Tahora=1;}
    else if(hohenga==2){taputapu_tūnga *huānga_tamaiti=huānga_uara(kaipupuri_ahanoa,첫째값);if(!huānga_tamaiti||huānga_tamaiti==너비값||huānga_tamaiti->kāwai_uara==1)return -22;int raraunga_tūranga=pūtāutu_uara;for(int 깊이=0;raraunga_tūranga&&깊이<32;깊이++){if(raraunga_tūranga==첫째값)return -22;taputapu_tūnga *위쪽=huānga_uara(kaipupuri_ahanoa,raraunga_tūranga);raraunga_tūranga=위쪽?위쪽->부모항목:0;}huānga_tamaiti->부모항목=pūtāutu_uara;if(!huānga_tamaiti->ā_ringa_Tahora){int 형제요소=0;for(int 순번=0;순번<32;순번++)if(&요소들[kaipupuri_ahanoa][순번]!=huānga_tamaiti&&요소들[kaipupuri_ahanoa][순번].부모항목==pūtāutu_uara)형제요소++;huānga_tamaiti->세로좌표=16+형제요소*36;}}
    else if(hohenga==3)너비값->보이는지=첫째값!=0;
    else if(hohenga==4)너비값->보이는지=0;
    else if(hohenga==7)너비값->Tahora_kaupapahere=첫째값;
    else if(hohenga==8)return 너비값->roa_uara;
    else if(hohenga==9)return 첫째값>=0&&(unsigned)첫째값<너비값->roa_uara?너비값->Ngā_kupu[첫째값]:-22;
    else return -22;
    if(이전표시||표시됨(kaipupuri_ahanoa,너비값))papa_Tauranga(3);return 0;
}
int 화면글(int kaipupuri_ahanoa,int pūtāutu_uara,const uint32_t *raraunga,unsigned tuemi_COUNT){taputapu_tūnga *너비값=huānga_uara(kaipupuri_ahanoa,pūtāutu_uara);if(!너비값)return -9;if(tuemi_COUNT>127)return -22;for(unsigned 순번=0;순번<tuemi_COUNT;순번++){unsigned pūāhua_whakawaehere=raraunga[순번];if(pūāhua_whakawaehere>0x10ffff||(pūāhua_whakawaehere>=0xd800&&pūāhua_whakawaehere<=0xdfff))return -22;}for(unsigned 순번=0;순번<tuemi_COUNT;순번++)너비값->Ngā_kupu[순번]=raraunga[순번];너비값->roa_uara=tuemi_COUNT;if(표시됨(kaipupuri_ahanoa,너비값))papa_Tauranga(3);return 0;}
