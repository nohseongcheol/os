#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* Small native peer layer for the explicitly supported Swing subset. */
#include <stdint.h>
#include <stddef.h>
extern uintptr_t Panelis_attēla_elements(uintptr_t,uintptr_t,uintptr_t),Panelis_Terminālis(uintptr_t);
extern void Terminālis_glifs(unsigned,unsigned,unsigned,unsigned,unsigned);
extern void *memset(void *,int,size_t);
typedef struct { int joma_VALUE,vecākobjekts,x_koordināta,세로좌표,너비값,높이값,보이는지,roku_shēma,shēma_politika;unsigned Teksts[128],길이; } logrīks_Statuss;
static logrīks_Statuss 요소들[4][32];
static int Svarīgie[4],notikums_Saraksts[4][16];static unsigned 첫항목[4],ievade_COUNT[4],부호없는결과[4],긴부호없는값[4];
static void Notikums(int īpašnieks_objekts,int VALUE){if(ievade_COUNT[īpašnieks_objekts]<16){notikums_Saraksts[īpašnieks_objekts][(첫항목[īpašnieks_objekts]+ievade_COUNT[īpašnieks_objekts])%16]=VALUE;ievade_COUNT[īpašnieks_objekts]++;}}
static logrīks_Statuss *elements_VALUE(int īpašnieks_objekts,int identifikators_VALUE){return īpašnieks_objekts>=0&&īpašnieks_objekts<4&&identifikators_VALUE>0&&identifikators_VALUE<=32&&요소들[īpašnieks_objekts][identifikators_VALUE-1].joma_VALUE?&요소들[īpašnieks_objekts][identifikators_VALUE-1]:0;}
static void 사각영역(int x_koordināta,int 세로좌표,int 너비값,int 높이값,unsigned 색상){Panelis_taisnstūris_aizpildīt(x_koordināta,세로좌표,너비값,높이값,색상);}
int 화면보임(int īpašnieks_objekts){if(īpašnieks_objekts<0||īpašnieks_objekts>=4)return 0;for(int 순번=0;순번<32;순번++)if(요소들[īpašnieks_objekts][순번].joma_VALUE==1&&요소들[īpašnieks_objekts][순번].보이는지)return 1;return 0;}
void 화면초기화(int īpašnieks_objekts){memset(요소들[īpašnieks_objekts],0,sizeof(요소들[īpašnieks_objekts]));ievade_COUNT[īpašnieks_objekts]=첫항목[īpašnieks_objekts]=Svarīgie[īpašnieks_objekts]=긴부호없는값[īpašnieks_objekts]=0;}
static void Novietojums(int īpašnieks_objekts,logrīks_Statuss *너비값,int *x_koordināta,int *세로좌표){*x_koordināta=너비값->x_koordināta;*세로좌표=너비값->세로좌표;int dati_amats=너비값->vecākobjekts;for(int krājums_COUNT=0;dati_amats&&krājums_COUNT<32;krājums_COUNT++){logrīks_Statuss *위쪽=elements_VALUE(īpašnieks_objekts,dati_amats);if(!위쪽)break;*x_koordināta+=위쪽->x_koordināta;*세로좌표+=위쪽->세로좌표+(위쪽->joma_VALUE==1?30:0);dati_amats=위쪽->vecākobjekts;}}
static int 표시됨(int īpašnieks_objekts,logrīks_Statuss *너비값){for(int krājums_COUNT=0;krājums_COUNT<32;krājums_COUNT++){if(!너비값->보이는지)return 0;if(너비값->joma_VALUE==1)return 1;너비값=elements_VALUE(īpašnieks_objekts,너비값->vecākobjekts);if(!너비값)return 0;}return 0;}
static void Teksts(int x_koordināta,int 세로좌표,logrīks_Statuss *너비값,int 최대값,unsigned 색상,unsigned 배경색){int pašreizējais_amats=0;for(unsigned 순번=0;순번<너비값->길이;순번++){unsigned rakstzīmju_kodēšana=너비값->Teksts[순번],너비=rakstzīmju_kodēšana>=256?16:8;if(pašreizējais_amats+(int)너비>최대값)break;Terminālis_glifs(x_koordināta+pašreizējais_amats,세로좌표,rakstzīmju_kodēšana,색상,배경색);pašreizējais_amats+=너비;}}
void 화면다시그림(int īpašnieks_objekts){
    if(!화면보임(īpašnieks_objekts))return;
    for(int apstrāde_secība=1;apstrāde_secība<=5;apstrāde_secība++)for(int 순번=0;순번<32;순번++){
        logrīks_Statuss *너비값=&요소들[īpašnieks_objekts][순번];if(너비값->joma_VALUE!=apstrāde_secība||!표시됨(īpašnieks_objekts,너비값))continue;int x_koordināta,세로좌표;Novietojums(īpašnieks_objekts,너비값,&x_koordināta,&세로좌표);
        if(apstrāde_secība==1){사각영역(x_koordināta,세로좌표,너비값->너비값,너비값->높이값,0xeee9e0);사각영역(x_koordināta,세로좌표,너비값->너비값,30,0x905020);Teksts(x_koordināta+10,세로좌표+7,너비값,너비값->너비값-50,0xffffff,0x905020);사각영역(x_koordināta+너비값->너비값-28,세로좌표+4,24,22,0x5555b8);Terminālis_glifs(x_koordināta+너비값->너비값-20,세로좌표+7,'X',0xffffff,0x5555b8);}
        if(apstrāde_secība==2)사각영역(x_koordināta,세로좌표,너비값->너비값,너비값->높이값,0xeee9e0);
        if(apstrāde_secība>=3){unsigned 배경색=apstrāde_secība==4?0xc0ab86:apstrāde_secība==5?0xffffff:0xeee9e0;if(apstrāde_secība!=3)사각영역(x_koordināta,세로좌표,너비값->너비값,너비값->높이값,배경색);Teksts(x_koordināta+4,세로좌표+4,너비값,너비값->너비값-8,0x201a15,배경색);if(apstrāde_secība==5&&Svarīgie[īpašnieks_objekts]==순번+1)사각영역(x_koordināta,세로좌표+너비값->높이값-2,너비값->너비값,2,0x905020);}
    }
}
int 화면덮음(int īpašnieks_objekts,int x_koordināta,int 세로좌표){
    if(!화면보임(īpašnieks_objekts))return 0;
    for(int 순번=0;순번<32;순번++){
        logrīks_Statuss *Logs=&요소들[īpašnieks_objekts][순번];
        if(Logs->joma_VALUE==1&&Logs->보이는지&&x_koordināta>=Logs->x_koordināta&&세로좌표>=Logs->세로좌표&&
           x_koordināta<Logs->x_koordināta+Logs->너비값&&세로좌표<Logs->세로좌표+Logs->높이값)return 1;
    }return 0;
}
int 화면가리킴(int īpašnieks_objekts,unsigned 눌림,int x_koordināta,int 세로좌표){
    if(!화면보임(īpašnieks_objekts))return 0;
    if(눌림&1)for(int 순번=31;순번>=0;순번--){logrīks_Statuss *너비값=&요소들[īpašnieks_objekts][순번];if(!너비값->joma_VALUE||!표시됨(īpašnieks_objekts,너비값))continue;int logs_X,logs_Y;Novietojums(īpašnieks_objekts,너비값,&logs_X,&logs_Y);
        if(x_koordināta<logs_X||세로좌표<logs_Y||x_koordināta>=logs_X+너비값->너비값||세로좌표>=logs_Y+너비값->높이값)continue;
        if(너비값->joma_VALUE==1&&세로좌표<logs_Y+30&&x_koordināta>=logs_X+너비값->너비값-28){if(너비값->shēma_politika!=0)너비값->보이는지=0;Notikums(īpašnieks_objekts,0x10000+순번+1);Panelis_Terminālis(3);return 1;}
        if(너비값->joma_VALUE==4){Notikums(īpašnieks_objekts,순번+1);return 1;}if(너비값->joma_VALUE==5){Svarīgie[īpašnieks_objekts]=순번+1;Panelis_Terminālis(3);return 1;}
        if(너비값->joma_VALUE==1)return 1;
    }return 0;
}
void 화면누름(int īpašnieks_objekts,unsigned SECOND_VALUE){
    logrīks_Statuss *너비값=elements_VALUE(īpašnieks_objekts,Svarīgie[īpašnieks_objekts]);if(!너비값||너비값->joma_VALUE!=5)return;
    if(SECOND_VALUE==13||SECOND_VALUE==10){Notikums(īpašnieks_objekts,Svarīgie[īpašnieks_objekts]);return;}
    if(SECOND_VALUE==8||SECOND_VALUE==127){if(너비값->길이)너비값->길이--;긴부호없는값[īpašnieks_objekts]=0;}
    else{
        unsigned rakstzīmju_kodēšana=SECOND_VALUE;
        if(긴부호없는값[īpašnieks_objekts]){if((SECOND_VALUE&192)!=128){긴부호없는값[īpašnieks_objekts]=0;return;}부호없는결과[īpašnieks_objekts]=(부호없는결과[īpašnieks_objekts]<<6)|(SECOND_VALUE&63);if(--긴부호없는값[īpašnieks_objekts])return;rakstzīmju_kodēšana=부호없는결과[īpašnieks_objekts];}
        else if(SECOND_VALUE>=0xc2&&SECOND_VALUE<=0xf4){긴부호없는값[īpašnieks_objekts]=SECOND_VALUE<0xe0?1:SECOND_VALUE<0xf0?2:3;부호없는결과[īpašnieks_objekts]=SECOND_VALUE&((1u<<(6-긴부호없는값[īpašnieks_objekts]))-1);return;}
        else if(SECOND_VALUE<32||SECOND_VALUE>=128)return;
        if(rakstzīmju_kodēšana>0x10ffff||(rakstzīmju_kodēšana>=0xd800&&rakstzīmju_kodēšana<=0xdfff))return;if(너비값->길이<127)너비값->Teksts[너비값->길이++]=rakstzīmju_kodēšana;
    }
    Panelis_Terminālis(3);
}
int 화면호출(int īpašnieks_objekts,unsigned Darbība,int identifikators_VALUE,int 첫째값,int SECOND_VALUE,int koda_punkts,int mērķis_dati){
    if(īpašnieks_objekts<0||īpašnieks_objekts>=4)return -22;logrīks_Statuss *너비값=elements_VALUE(īpašnieks_objekts,identifikators_VALUE);
    if(Darbība==0){if(identifikators_VALUE<1||identifikators_VALUE>5)return -22;for(int 순번=0;순번<32;순번++)if(요소들[īpašnieks_objekts][순번].joma_VALUE==0){너비값=&요소들[īpašnieks_objekts][순번];memset(너비값,0,sizeof(*너비값));너비값->joma_VALUE=identifikators_VALUE;너비값->보이는지=identifikators_VALUE!=1;너비값->너비값=identifikators_VALUE==1?380:220;너비값->높이값=identifikators_VALUE==1?240:28;너비값->shēma_politika=1;너비값->x_koordināta=identifikators_VALUE==1?130:16;너비값->세로좌표=identifikators_VALUE==1?110:16;return 순번+1;}return -28;}
    if(Darbība==5){if(!ievade_COUNT[īpašnieks_objekts])return 0;int 반환값=notikums_Saraksts[īpašnieks_objekts][첫항목[īpašnieks_objekts]];첫항목[īpašnieks_objekts]=(첫항목[īpašnieks_objekts]+1)%16;ievade_COUNT[īpašnieks_objekts]--;return 반환값;}
    if(Darbība==6)return 화면보임(īpašnieks_objekts);
    if(!너비값)return -9;
    int 이전표시=표시됨(īpašnieks_objekts,너비값);
    if(Darbība==1){int 바탕너비=보드화면너비(),바탕높이=보드화면높이();if(첫째값<0||SECOND_VALUE<0||koda_punkts<1||mērķis_dati<1||첫째값>바탕너비||SECOND_VALUE>바탕높이||koda_punkts>바탕너비-첫째값||mērķis_dati>바탕높이-SECOND_VALUE)return -22;너비값->x_koordināta=첫째값;너비값->세로좌표=SECOND_VALUE;너비값->너비값=koda_punkts;너비값->높이값=mērķis_dati;너비값->roku_shēma=1;}
    else if(Darbība==2){logrīks_Statuss *bērnelements=elements_VALUE(īpašnieks_objekts,첫째값);if(!bērnelements||bērnelements==너비값||bērnelements->joma_VALUE==1)return -22;int dati_amats=identifikators_VALUE;for(int 깊이=0;dati_amats&&깊이<32;깊이++){if(dati_amats==첫째값)return -22;logrīks_Statuss *위쪽=elements_VALUE(īpašnieks_objekts,dati_amats);dati_amats=위쪽?위쪽->vecākobjekts:0;}bērnelements->vecākobjekts=identifikators_VALUE;if(!bērnelements->roku_shēma){int 형제요소=0;for(int 순번=0;순번<32;순번++)if(&요소들[īpašnieks_objekts][순번]!=bērnelements&&요소들[īpašnieks_objekts][순번].vecākobjekts==identifikators_VALUE)형제요소++;bērnelements->세로좌표=16+형제요소*36;}}
    else if(Darbība==3)너비값->보이는지=첫째값!=0;
    else if(Darbība==4)너비값->보이는지=0;
    else if(Darbība==7)너비값->shēma_politika=첫째값;
    else if(Darbība==8)return 너비값->길이;
    else if(Darbība==9)return 첫째값>=0&&(unsigned)첫째값<너비값->길이?너비값->Teksts[첫째값]:-22;
    else return -22;
    if(이전표시||표시됨(īpašnieks_objekts,너비값))Panelis_Terminālis(3);return 0;
}
int 화면글(int īpašnieks_objekts,int identifikators_VALUE,const uint32_t *dati,unsigned krājums_COUNT){logrīks_Statuss *너비값=elements_VALUE(īpašnieks_objekts,identifikators_VALUE);if(!너비값)return -9;if(krājums_COUNT>127)return -22;for(unsigned 순번=0;순번<krājums_COUNT;순번++){unsigned rakstzīmju_kodēšana=dati[순번];if(rakstzīmju_kodēšana>0x10ffff||(rakstzīmju_kodēšana>=0xd800&&rakstzīmju_kodēšana<=0xdfff))return -22;}for(unsigned 순번=0;순번<krājums_COUNT;순번++)너비값->Teksts[순번]=dati[순번];너비값->길이=krājums_COUNT;if(표시됨(īpašnieks_objekts,너비값))Panelis_Terminālis(3);return 0;}
