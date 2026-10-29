#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* Small native peer layer for the explicitly supported Swing subset. */
#include <stdint.h>
#include <stddef.h>
extern uintptr_t Panel_pixel(uintptr_t,uintptr_t,uintptr_t),Panel_Terminál(uintptr_t);
extern void Terminál_piktogram(unsigned,unsigned,unsigned,unsigned,unsigned);
extern void *memset(void *,int,size_t);
typedef struct { int oblast_HODNOTA,nadřazený,souřadnice_x,Y_souřadnice,너비값,vyžádáno_výška_HODNOTA,보이는지,ruční_Navigace,Navigace_Policy;unsigned text[128],délka_HODNOTA; } widget_Stav;
static widget_Stav 요소들[4][32];
static int Prioritní[4],událost_Seznam[4][16];static unsigned 첫항목[4],položka_POČET[4],부호없는결과[4],긴부호없는값[4];
static void Události(int vlastník_objekt,int HODNOTA){if(položka_POČET[vlastník_objekt]<16){událost_Seznam[vlastník_objekt][(첫항목[vlastník_objekt]+položka_POČET[vlastník_objekt])%16]=HODNOTA;položka_POČET[vlastník_objekt]++;}}
static widget_Stav *prvek_HODNOTA(int vlastník_objekt,int identifikátor_HODNOTA){return vlastník_objekt>=0&&vlastník_objekt<4&&identifikátor_HODNOTA>0&&identifikátor_HODNOTA<=32&&요소들[vlastník_objekt][identifikátor_HODNOTA-1].oblast_HODNOTA?&요소들[vlastník_objekt][identifikátor_HODNOTA-1]:0;}
static void 사각영역(int souřadnice_x,int Y_souřadnice,int 너비값,int vyžádáno_výška_HODNOTA,unsigned 색상){Panel_obdélník_výplň(souřadnice_x,Y_souřadnice,너비값,vyžádáno_výška_HODNOTA,색상);}
int 화면보임(int vlastník_objekt){if(vlastník_objekt<0||vlastník_objekt>=4)return 0;for(int 순번=0;순번<32;순번++)if(요소들[vlastník_objekt][순번].oblast_HODNOTA==1&&요소들[vlastník_objekt][순번].보이는지)return 1;return 0;}
void 화면초기화(int vlastník_objekt){memset(요소들[vlastník_objekt],0,sizeof(요소들[vlastník_objekt]));položka_POČET[vlastník_objekt]=첫항목[vlastník_objekt]=Prioritní[vlastník_objekt]=긴부호없는값[vlastník_objekt]=0;}
static void pozice(int vlastník_objekt,widget_Stav *너비값,int *souřadnice_x,int *Y_souřadnice){*souřadnice_x=너비값->souřadnice_x;*Y_souřadnice=너비값->Y_souřadnice;int data_pozice=너비값->nadřazený;for(int zboží_POČET=0;data_pozice&&zboží_POČET<32;zboží_POČET++){widget_Stav *위쪽=prvek_HODNOTA(vlastník_objekt,data_pozice);if(!위쪽)break;*souřadnice_x+=위쪽->souřadnice_x;*Y_souřadnice+=위쪽->Y_souřadnice+(위쪽->oblast_HODNOTA==1?30:0);data_pozice=위쪽->nadřazený;}}
static int 표시됨(int vlastník_objekt,widget_Stav *너비값){for(int zboží_POČET=0;zboží_POČET<32;zboží_POČET++){if(!너비값->보이는지)return 0;if(너비값->oblast_HODNOTA==1)return 1;너비값=prvek_HODNOTA(vlastník_objekt,너비값->nadřazený);if(!너비값)return 0;}return 0;}
static void text(int souřadnice_x,int Y_souřadnice,widget_Stav *너비값,int 최대값,unsigned 색상,unsigned 배경색){int dobrá_pozice=0;for(unsigned 순번=0;순번<너비값->délka_HODNOTA;순번++){unsigned kódování_znaků=너비값->text[순번],너비=kódování_znaků>=256?16:8;if(dobrá_pozice+(int)너비>최대값)break;Terminál_piktogram(souřadnice_x+dobrá_pozice,Y_souřadnice,kódování_znaků,색상,배경색);dobrá_pozice+=너비;}}
void 화면다시그림(int vlastník_objekt){
    if(!화면보임(vlastník_objekt))return;
    for(int zpracování_pořadí=1;zpracování_pořadí<=5;zpracování_pořadí++)for(int 순번=0;순번<32;순번++){
        widget_Stav *너비값=&요소들[vlastník_objekt][순번];if(너비값->oblast_HODNOTA!=zpracování_pořadí||!표시됨(vlastník_objekt,너비값))continue;int souřadnice_x,Y_souřadnice;pozice(vlastník_objekt,너비값,&souřadnice_x,&Y_souřadnice);
        if(zpracování_pořadí==1){사각영역(souřadnice_x,Y_souřadnice,너비값->너비값,너비값->vyžádáno_výška_HODNOTA,0xeee9e0);사각영역(souřadnice_x,Y_souřadnice,너비값->너비값,30,0x905020);text(souřadnice_x+10,Y_souřadnice+7,너비값,너비값->너비값-50,0xffffff,0x905020);사각영역(souřadnice_x+너비값->너비값-28,Y_souřadnice+4,24,22,0x5555b8);Terminál_piktogram(souřadnice_x+너비값->너비값-20,Y_souřadnice+7,'X',0xffffff,0x5555b8);}
        if(zpracování_pořadí==2)사각영역(souřadnice_x,Y_souřadnice,너비값->너비값,너비값->vyžádáno_výška_HODNOTA,0xeee9e0);
        if(zpracování_pořadí>=3){unsigned 배경색=zpracování_pořadí==4?0xc0ab86:zpracování_pořadí==5?0xffffff:0xeee9e0;if(zpracování_pořadí!=3)사각영역(souřadnice_x,Y_souřadnice,너비값->너비값,너비값->vyžádáno_výška_HODNOTA,배경색);text(souřadnice_x+4,Y_souřadnice+4,너비값,너비값->너비값-8,0x201a15,배경색);if(zpracování_pořadí==5&&Prioritní[vlastník_objekt]==순번+1)사각영역(souřadnice_x,Y_souřadnice+너비값->vyžádáno_výška_HODNOTA-2,너비값->너비값,2,0x905020);}
    }
}
int 화면덮음(int vlastník_objekt,int souřadnice_x,int Y_souřadnice){
    if(!화면보임(vlastník_objekt))return 0;
    for(int 순번=0;순번<32;순번++){
        widget_Stav *Okno=&요소들[vlastník_objekt][순번];
        if(Okno->oblast_HODNOTA==1&&Okno->보이는지&&souřadnice_x>=Okno->souřadnice_x&&Y_souřadnice>=Okno->Y_souřadnice&&
           souřadnice_x<Okno->souřadnice_x+Okno->너비값&&Y_souřadnice<Okno->Y_souřadnice+Okno->vyžádáno_výška_HODNOTA)return 1;
    }return 0;
}
int 화면가리킴(int vlastník_objekt,unsigned 눌림,int souřadnice_x,int Y_souřadnice){
    if(!화면보임(vlastník_objekt))return 0;
    if(눌림&1)for(int 순번=31;순번>=0;순번--){widget_Stav *너비값=&요소들[vlastník_objekt][순번];if(!너비값->oblast_HODNOTA||!표시됨(vlastník_objekt,너비값))continue;int okno_X,okno_Y;pozice(vlastník_objekt,너비값,&okno_X,&okno_Y);
        if(souřadnice_x<okno_X||Y_souřadnice<okno_Y||souřadnice_x>=okno_X+너비값->너비값||Y_souřadnice>=okno_Y+너비값->vyžádáno_výška_HODNOTA)continue;
        if(너비값->oblast_HODNOTA==1&&Y_souřadnice<okno_Y+30&&souřadnice_x>=okno_X+너비값->너비값-28){if(너비값->Navigace_Policy!=0)너비값->보이는지=0;Události(vlastník_objekt,0x10000+순번+1);Panel_Terminál(3);return 1;}
        if(너비값->oblast_HODNOTA==4){Události(vlastník_objekt,순번+1);return 1;}if(너비값->oblast_HODNOTA==5){Prioritní[vlastník_objekt]=순번+1;Panel_Terminál(3);return 1;}
        if(너비값->oblast_HODNOTA==1)return 1;
    }return 0;
}
void 화면누름(int vlastník_objekt,unsigned SEKUNDA_HODNOTA){
    widget_Stav *너비값=prvek_HODNOTA(vlastník_objekt,Prioritní[vlastník_objekt]);if(!너비값||너비값->oblast_HODNOTA!=5)return;
    if(SEKUNDA_HODNOTA==13||SEKUNDA_HODNOTA==10){Události(vlastník_objekt,Prioritní[vlastník_objekt]);return;}
    if(SEKUNDA_HODNOTA==8||SEKUNDA_HODNOTA==127){if(너비값->délka_HODNOTA)너비값->délka_HODNOTA--;긴부호없는값[vlastník_objekt]=0;}
    else{
        unsigned kódování_znaků=SEKUNDA_HODNOTA;
        if(긴부호없는값[vlastník_objekt]){if((SEKUNDA_HODNOTA&192)!=128){긴부호없는값[vlastník_objekt]=0;return;}부호없는결과[vlastník_objekt]=(부호없는결과[vlastník_objekt]<<6)|(SEKUNDA_HODNOTA&63);if(--긴부호없는값[vlastník_objekt])return;kódování_znaků=부호없는결과[vlastník_objekt];}
        else if(SEKUNDA_HODNOTA>=0xc2&&SEKUNDA_HODNOTA<=0xf4){긴부호없는값[vlastník_objekt]=SEKUNDA_HODNOTA<0xe0?1:SEKUNDA_HODNOTA<0xf0?2:3;부호없는결과[vlastník_objekt]=SEKUNDA_HODNOTA&((1u<<(6-긴부호없는값[vlastník_objekt]))-1);return;}
        else if(SEKUNDA_HODNOTA<32||SEKUNDA_HODNOTA>=128)return;
        if(kódování_znaků>0x10ffff||(kódování_znaků>=0xd800&&kódování_znaků<=0xdfff))return;if(너비값->délka_HODNOTA<127)너비값->text[너비값->délka_HODNOTA++]=kódování_znaků;
    }
    Panel_Terminál(3);
}
int 화면호출(int vlastník_objekt,unsigned Akce,int identifikátor_HODNOTA,int 첫째값,int SEKUNDA_HODNOTA,int bod_kódu,int cíl_data){
    if(vlastník_objekt<0||vlastník_objekt>=4)return -22;widget_Stav *너비값=prvek_HODNOTA(vlastník_objekt,identifikátor_HODNOTA);
    if(Akce==0){if(identifikátor_HODNOTA<1||identifikátor_HODNOTA>5)return -22;for(int 순번=0;순번<32;순번++)if(요소들[vlastník_objekt][순번].oblast_HODNOTA==0){너비값=&요소들[vlastník_objekt][순번];memset(너비값,0,sizeof(*너비값));너비값->oblast_HODNOTA=identifikátor_HODNOTA;너비값->보이는지=identifikátor_HODNOTA!=1;너비값->너비값=identifikátor_HODNOTA==1?380:220;너비값->vyžádáno_výška_HODNOTA=identifikátor_HODNOTA==1?240:28;너비값->Navigace_Policy=1;너비값->souřadnice_x=identifikátor_HODNOTA==1?130:16;너비값->Y_souřadnice=identifikátor_HODNOTA==1?110:16;return 순번+1;}return -28;}
    if(Akce==5){if(!položka_POČET[vlastník_objekt])return 0;int 반환값=událost_Seznam[vlastník_objekt][첫항목[vlastník_objekt]];첫항목[vlastník_objekt]=(첫항목[vlastník_objekt]+1)%16;položka_POČET[vlastník_objekt]--;return 반환값;}
    if(Akce==6)return 화면보임(vlastník_objekt);
    if(!너비값)return -9;
    int 이전표시=표시됨(vlastník_objekt,너비값);
    if(Akce==1){int 바탕너비=보드화면너비(),Pozadí_výška=보드화면높이();if(첫째값<0||SEKUNDA_HODNOTA<0||bod_kódu<1||cíl_data<1||첫째값>바탕너비||SEKUNDA_HODNOTA>Pozadí_výška||bod_kódu>바탕너비-첫째값||cíl_data>Pozadí_výška-SEKUNDA_HODNOTA)return -22;너비값->souřadnice_x=첫째값;너비값->Y_souřadnice=SEKUNDA_HODNOTA;너비값->너비값=bod_kódu;너비값->vyžádáno_výška_HODNOTA=cíl_data;너비값->ruční_Navigace=1;}
    else if(Akce==2){widget_Stav *podřízený=prvek_HODNOTA(vlastník_objekt,첫째값);if(!podřízený||podřízený==너비값||podřízený->oblast_HODNOTA==1)return -22;int data_pozice=identifikátor_HODNOTA;for(int 깊이=0;data_pozice&&깊이<32;깊이++){if(data_pozice==첫째값)return -22;widget_Stav *위쪽=prvek_HODNOTA(vlastník_objekt,data_pozice);data_pozice=위쪽?위쪽->nadřazený:0;}podřízený->nadřazený=identifikátor_HODNOTA;if(!podřízený->ruční_Navigace){int 형제요소=0;for(int 순번=0;순번<32;순번++)if(&요소들[vlastník_objekt][순번]!=podřízený&&요소들[vlastník_objekt][순번].nadřazený==identifikátor_HODNOTA)형제요소++;podřízený->Y_souřadnice=16+형제요소*36;}}
    else if(Akce==3)너비값->보이는지=첫째값!=0;
    else if(Akce==4)너비값->보이는지=0;
    else if(Akce==7)너비값->Navigace_Policy=첫째값;
    else if(Akce==8)return 너비값->délka_HODNOTA;
    else if(Akce==9)return 첫째값>=0&&(unsigned)첫째값<너비값->délka_HODNOTA?너비값->text[첫째값]:-22;
    else return -22;
    if(이전표시||표시됨(vlastník_objekt,너비값))Panel_Terminál(3);return 0;
}
int 화면글(int vlastník_objekt,int identifikátor_HODNOTA,const uint32_t *data,unsigned zboží_POČET){widget_Stav *너비값=prvek_HODNOTA(vlastník_objekt,identifikátor_HODNOTA);if(!너비값)return -9;if(zboží_POČET>127)return -22;for(unsigned 순번=0;순번<zboží_POČET;순번++){unsigned kódování_znaků=data[순번];if(kódování_znaků>0x10ffff||(kódování_znaků>=0xd800&&kódování_znaků<=0xdfff))return -22;}for(unsigned 순번=0;순번<zboží_POČET;순번++)너비값->text[순번]=data[순번];너비값->délka_HODNOTA=zboží_POČET;if(표시됨(vlastník_objekt,너비값))Panel_Terminál(3);return 0;}
