#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* Small native peer layer for the explicitly supported Swing subset. */
#include <stdint.h>
#include <stddef.h>
extern uintptr_t 보드화소(uintptr_t,uintptr_t,uintptr_t),보드터미널(uintptr_t);
extern void 터미널글자그림(unsigned,unsigned,unsigned,unsigned,unsigned);
extern void *memset(void *,int,size_t);
typedef struct { int setlhopha_Boleng_4b6d6445,부모항목,kgokagano_ya_x,세로좌표,너비값,높이값,보이는지,kaela_tiriso_Boalo,Boalo_pholisi;unsigned SMS[128],boleele_Boleng; } wijete_kemo;
static wijete_kemo 요소들[4][32];
static int Tlhomameng[4],tiragalo_lenaane[4][16];static unsigned 첫항목[4],항목수[4],부호없는결과[4],긴부호없는값[4];
static void tiragalo(int mong_selwana,int Boleng){if(항목수[mong_selwana]<16){tiragalo_lenaane[mong_selwana][(첫항목[mong_selwana]+항목수[mong_selwana])%16]=Boleng;항목수[mong_selwana]++;}}
static wijete_kemo *tlhakakaelo_Boleng(int mong_selwana,int setlhaodi_Boleng){return mong_selwana>=0&&mong_selwana<4&&setlhaodi_Boleng>0&&setlhaodi_Boleng<=32&&요소들[mong_selwana][setlhaodi_Boleng-1].setlhopha_Boleng_4b6d6445?&요소들[mong_selwana][setlhaodi_Boleng-1]:0;}
static void 사각영역(int kgokagano_ya_x,int 세로좌표,int 너비값,int 높이값,unsigned 색상){보드사각그림(kgokagano_ya_x,세로좌표,너비값,높이값,색상);}
int 화면보임(int mong_selwana){if(mong_selwana<0||mong_selwana>=4)return 0;for(int 순번=0;순번<32;순번++)if(요소들[mong_selwana][순번].setlhopha_Boleng_4b6d6445==1&&요소들[mong_selwana][순번].보이는지)return 1;return 0;}
void 화면초기화(int mong_selwana){memset(요소들[mong_selwana],0,sizeof(요소들[mong_selwana]));항목수[mong_selwana]=첫항목[mong_selwana]=Tlhomameng[mong_selwana]=긴부호없는값[mong_selwana]=0;}
static void 위치(int mong_selwana,wijete_kemo *너비값,int *kgokagano_ya_x,int *세로좌표){*kgokagano_ya_x=너비값->kgokagano_ya_x;*세로좌표=너비값->세로좌표;int 자료위치=너비값->부모항목;for(int 개수=0;자료위치&&개수<32;개수++){wijete_kemo *위쪽=tlhakakaelo_Boleng(mong_selwana,자료위치);if(!위쪽)break;*kgokagano_ya_x+=위쪽->kgokagano_ya_x;*세로좌표+=위쪽->세로좌표+(위쪽->setlhopha_Boleng_4b6d6445==1?30:0);자료위치=위쪽->부모항목;}}
static int 표시됨(int mong_selwana,wijete_kemo *너비값){for(int 개수=0;개수<32;개수++){if(!너비값->보이는지)return 0;if(너비값->setlhopha_Boleng_4b6d6445==1)return 1;너비값=tlhakakaelo_Boleng(mong_selwana,너비값->부모항목);if(!너비값)return 0;}return 0;}
static void SMS(int kgokagano_ya_x,int 세로좌표,wijete_kemo *너비값,int 최대값,unsigned 색상,unsigned 배경색){int 현재위치=0;for(unsigned 순번=0;순번<너비값->boleele_Boleng;순번++){unsigned Letshwao_khoutufatso=너비값->SMS[순번],너비=Letshwao_khoutufatso>=256?16:8;if(현재위치+(int)너비>최대값)break;터미널글자그림(kgokagano_ya_x+현재위치,세로좌표,Letshwao_khoutufatso,색상,배경색);현재위치+=너비;}}
void 화면다시그림(int mong_selwana){
    if(!화면보임(mong_selwana))return;
    for(int 처리차례=1;처리차례<=5;처리차례++)for(int 순번=0;순번<32;순번++){
        wijete_kemo *너비값=&요소들[mong_selwana][순번];if(너비값->setlhopha_Boleng_4b6d6445!=처리차례||!표시됨(mong_selwana,너비값))continue;int kgokagano_ya_x,세로좌표;위치(mong_selwana,너비값,&kgokagano_ya_x,&세로좌표);
        if(처리차례==1){사각영역(kgokagano_ya_x,세로좌표,너비값->너비값,너비값->높이값,0xeee9e0);사각영역(kgokagano_ya_x,세로좌표,너비값->너비값,30,0x905020);SMS(kgokagano_ya_x+10,세로좌표+7,너비값,너비값->너비값-50,0xffffff,0x905020);사각영역(kgokagano_ya_x+너비값->너비값-28,세로좌표+4,24,22,0x5555b8);터미널글자그림(kgokagano_ya_x+너비값->너비값-20,세로좌표+7,'X',0xffffff,0x5555b8);}
        if(처리차례==2)사각영역(kgokagano_ya_x,세로좌표,너비값->너비값,너비값->높이값,0xeee9e0);
        if(처리차례>=3){unsigned 배경색=처리차례==4?0xc0ab86:처리차례==5?0xffffff:0xeee9e0;if(처리차례!=3)사각영역(kgokagano_ya_x,세로좌표,너비값->너비값,너비값->높이값,배경색);SMS(kgokagano_ya_x+4,세로좌표+4,너비값,너비값->너비값-8,0x201a15,배경색);if(처리차례==5&&Tlhomameng[mong_selwana]==순번+1)사각영역(kgokagano_ya_x,세로좌표+너비값->높이값-2,너비값->너비값,2,0x905020);}
    }
}
int 화면덮음(int mong_selwana,int kgokagano_ya_x,int 세로좌표){
    if(!화면보임(mong_selwana))return 0;
    for(int 순번=0;순번<32;순번++){
        wijete_kemo *fensetere=&요소들[mong_selwana][순번];
        if(fensetere->setlhopha_Boleng_4b6d6445==1&&fensetere->보이는지&&kgokagano_ya_x>=fensetere->kgokagano_ya_x&&세로좌표>=fensetere->세로좌표&&
           kgokagano_ya_x<fensetere->kgokagano_ya_x+fensetere->너비값&&세로좌표<fensetere->세로좌표+fensetere->높이값)return 1;
    }return 0;
}
int 화면가리킴(int mong_selwana,unsigned 눌림,int kgokagano_ya_x,int 세로좌표){
    if(!화면보임(mong_selwana))return 0;
    if(눌림&1)for(int 순번=31;순번>=0;순번--){wijete_kemo *너비값=&요소들[mong_selwana][순번];if(!너비값->setlhopha_Boleng_4b6d6445||!표시됨(mong_selwana,너비값))continue;int 창가로,창세로;위치(mong_selwana,너비값,&창가로,&창세로);
        if(kgokagano_ya_x<창가로||세로좌표<창세로||kgokagano_ya_x>=창가로+너비값->너비값||세로좌표>=창세로+너비값->높이값)continue;
        if(너비값->setlhopha_Boleng_4b6d6445==1&&세로좌표<창세로+30&&kgokagano_ya_x>=창가로+너비값->너비값-28){if(너비값->Boalo_pholisi!=0)너비값->보이는지=0;tiragalo(mong_selwana,0x10000+순번+1);보드터미널(3);return 1;}
        if(너비값->setlhopha_Boleng_4b6d6445==4){tiragalo(mong_selwana,순번+1);return 1;}if(너비값->setlhopha_Boleng_4b6d6445==5){Tlhomameng[mong_selwana]=순번+1;보드터미널(3);return 1;}
        if(너비값->setlhopha_Boleng_4b6d6445==1)return 1;
    }return 0;
}
void 화면누름(int mong_selwana,unsigned 둘째값){
    wijete_kemo *너비값=tlhakakaelo_Boleng(mong_selwana,Tlhomameng[mong_selwana]);if(!너비값||너비값->setlhopha_Boleng_4b6d6445!=5)return;
    if(둘째값==13||둘째값==10){tiragalo(mong_selwana,Tlhomameng[mong_selwana]);return;}
    if(둘째값==8||둘째값==127){if(너비값->boleele_Boleng)너비값->boleele_Boleng--;긴부호없는값[mong_selwana]=0;}
    else{
        unsigned Letshwao_khoutufatso=둘째값;
        if(긴부호없는값[mong_selwana]){if((둘째값&192)!=128){긴부호없는값[mong_selwana]=0;return;}부호없는결과[mong_selwana]=(부호없는결과[mong_selwana]<<6)|(둘째값&63);if(--긴부호없는값[mong_selwana])return;Letshwao_khoutufatso=부호없는결과[mong_selwana];}
        else if(둘째값>=0xc2&&둘째값<=0xf4){긴부호없는값[mong_selwana]=둘째값<0xe0?1:둘째값<0xf0?2:3;부호없는결과[mong_selwana]=둘째값&((1u<<(6-긴부호없는값[mong_selwana]))-1);return;}
        else if(둘째값<32||둘째값>=128)return;
        if(Letshwao_khoutufatso>0x10ffff||(Letshwao_khoutufatso>=0xd800&&Letshwao_khoutufatso<=0xdfff))return;if(너비값->boleele_Boleng<127)너비값->SMS[너비값->boleele_Boleng++]=Letshwao_khoutufatso;
    }
    보드터미널(3);
}
int 화면호출(int mong_selwana,unsigned tiro,int setlhaodi_Boleng,int 첫째값,int 둘째값,int khoutuletshwao,int bogorogelo_tshedimosetso){
    if(mong_selwana<0||mong_selwana>=4)return -22;wijete_kemo *너비값=tlhakakaelo_Boleng(mong_selwana,setlhaodi_Boleng);
    if(tiro==0){if(setlhaodi_Boleng<1||setlhaodi_Boleng>5)return -22;for(int 순번=0;순번<32;순번++)if(요소들[mong_selwana][순번].setlhopha_Boleng_4b6d6445==0){너비값=&요소들[mong_selwana][순번];memset(너비값,0,sizeof(*너비값));너비값->setlhopha_Boleng_4b6d6445=setlhaodi_Boleng;너비값->보이는지=setlhaodi_Boleng!=1;너비값->너비값=setlhaodi_Boleng==1?380:220;너비값->높이값=setlhaodi_Boleng==1?240:28;너비값->Boalo_pholisi=1;너비값->kgokagano_ya_x=setlhaodi_Boleng==1?130:16;너비값->세로좌표=setlhaodi_Boleng==1?110:16;return 순번+1;}return -28;}
    if(tiro==5){if(!항목수[mong_selwana])return 0;int 반환값=tiragalo_lenaane[mong_selwana][첫항목[mong_selwana]];첫항목[mong_selwana]=(첫항목[mong_selwana]+1)%16;항목수[mong_selwana]--;return 반환값;}
    if(tiro==6)return 화면보임(mong_selwana);
    if(!너비값)return -9;
    int 이전표시=표시됨(mong_selwana,너비값);
    if(tiro==1){int 바탕너비=보드화면너비(),바탕높이=보드화면높이();if(첫째값<0||둘째값<0||khoutuletshwao<1||bogorogelo_tshedimosetso<1||첫째값>바탕너비||둘째값>바탕높이||khoutuletshwao>바탕너비-첫째값||bogorogelo_tshedimosetso>바탕높이-둘째값)return -22;너비값->kgokagano_ya_x=첫째값;너비값->세로좌표=둘째값;너비값->너비값=khoutuletshwao;너비값->높이값=bogorogelo_tshedimosetso;너비값->kaela_tiriso_Boalo=1;}
    else if(tiro==2){wijete_kemo *ditlhakakaelopotlana=tlhakakaelo_Boleng(mong_selwana,첫째값);if(!ditlhakakaelopotlana||ditlhakakaelopotlana==너비값||ditlhakakaelopotlana->setlhopha_Boleng_4b6d6445==1)return -22;int 자료위치=setlhaodi_Boleng;for(int 깊이=0;자료위치&&깊이<32;깊이++){if(자료위치==첫째값)return -22;wijete_kemo *위쪽=tlhakakaelo_Boleng(mong_selwana,자료위치);자료위치=위쪽?위쪽->부모항목:0;}ditlhakakaelopotlana->부모항목=setlhaodi_Boleng;if(!ditlhakakaelopotlana->kaela_tiriso_Boalo){int 형제요소=0;for(int 순번=0;순번<32;순번++)if(&요소들[mong_selwana][순번]!=ditlhakakaelopotlana&&요소들[mong_selwana][순번].부모항목==setlhaodi_Boleng)형제요소++;ditlhakakaelopotlana->세로좌표=16+형제요소*36;}}
    else if(tiro==3)너비값->보이는지=첫째값!=0;
    else if(tiro==4)너비값->보이는지=0;
    else if(tiro==7)너비값->Boalo_pholisi=첫째값;
    else if(tiro==8)return 너비값->boleele_Boleng;
    else if(tiro==9)return 첫째값>=0&&(unsigned)첫째값<너비값->boleele_Boleng?너비값->SMS[첫째값]:-22;
    else return -22;
    if(이전표시||표시됨(mong_selwana,너비값))보드터미널(3);return 0;
}
int 화면글(int mong_selwana,int setlhaodi_Boleng,const uint32_t *tshedimosetso,unsigned 개수){wijete_kemo *너비값=tlhakakaelo_Boleng(mong_selwana,setlhaodi_Boleng);if(!너비값)return -9;if(개수>127)return -22;for(unsigned 순번=0;순번<개수;순번++){unsigned Letshwao_khoutufatso=tshedimosetso[순번];if(Letshwao_khoutufatso>0x10ffff||(Letshwao_khoutufatso>=0xd800&&Letshwao_khoutufatso<=0xdfff))return -22;}for(unsigned 순번=0;순번<개수;순번++)너비값->SMS[순번]=tshedimosetso[순번];너비값->boleele_Boleng=개수;if(표시됨(mong_selwana,너비값))보드터미널(3);return 0;}
