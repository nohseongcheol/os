#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* Small native peer layer for the explicitly supported Swing subset. */
#include <stdint.h>
#include <stddef.h>
extern uintptr_t Lenta_pikselis(uintptr_t,uintptr_t,uintptr_t),Lenta_Terminalas(uintptr_t);
extern void Terminalas_glifas(unsigned,unsigned,unsigned,unsigned,unsigned);
extern void *memset(void *,int,size_t);
typedef struct { int sritis_VALUE,pirminis,x_koordinatė,세로좌표,너비값,높이값,보이는지,rankinis_schema,schema_strategija;unsigned Tekstas[128],길이; } valdiklis_Būsena;
static valdiklis_Būsena 요소들[4][32];
static int Reikšmingiausi[4],įvykis_Sąrašas[4][16];static unsigned 첫항목[4],įrašas_COUNT[4],부호없는결과[4],긴부호없는값[4];
static void Įvykis(int savininkas_objektas,int VALUE){if(įrašas_COUNT[savininkas_objektas]<16){įvykis_Sąrašas[savininkas_objektas][(첫항목[savininkas_objektas]+įrašas_COUNT[savininkas_objektas])%16]=VALUE;įrašas_COUNT[savininkas_objektas]++;}}
static valdiklis_Būsena *elementas_VALUE(int savininkas_objektas,int identifikatorius_VALUE){return savininkas_objektas>=0&&savininkas_objektas<4&&identifikatorius_VALUE>0&&identifikatorius_VALUE<=32&&요소들[savininkas_objektas][identifikatorius_VALUE-1].sritis_VALUE?&요소들[savininkas_objektas][identifikatorius_VALUE-1]:0;}
static void 사각영역(int x_koordinatė,int 세로좌표,int 너비값,int 높이값,unsigned 색상){Lenta_stačiakampis_užpildas(x_koordinatė,세로좌표,너비값,높이값,색상);}
int 화면보임(int savininkas_objektas){if(savininkas_objektas<0||savininkas_objektas>=4)return 0;for(int 순번=0;순번<32;순번++)if(요소들[savininkas_objektas][순번].sritis_VALUE==1&&요소들[savininkas_objektas][순번].보이는지)return 1;return 0;}
void 화면초기화(int savininkas_objektas){memset(요소들[savininkas_objektas],0,sizeof(요소들[savininkas_objektas]));įrašas_COUNT[savininkas_objektas]=첫항목[savininkas_objektas]=Reikšmingiausi[savininkas_objektas]=긴부호없는값[savininkas_objektas]=0;}
static void Pozicija(int savininkas_objektas,valdiklis_Būsena *너비값,int *x_koordinatė,int *세로좌표){*x_koordinatė=너비값->x_koordinatė;*세로좌표=너비값->세로좌표;int duomenys_padėtis=너비값->pirminis;for(int prekė_COUNT=0;duomenys_padėtis&&prekė_COUNT<32;prekė_COUNT++){valdiklis_Būsena *위쪽=elementas_VALUE(savininkas_objektas,duomenys_padėtis);if(!위쪽)break;*x_koordinatė+=위쪽->x_koordinatė;*세로좌표+=위쪽->세로좌표+(위쪽->sritis_VALUE==1?30:0);duomenys_padėtis=위쪽->pirminis;}}
static int 표시됨(int savininkas_objektas,valdiklis_Būsena *너비값){for(int prekė_COUNT=0;prekė_COUNT<32;prekė_COUNT++){if(!너비값->보이는지)return 0;if(너비값->sritis_VALUE==1)return 1;너비값=elementas_VALUE(savininkas_objektas,너비값->pirminis);if(!너비값)return 0;}return 0;}
static void Tekstas(int x_koordinatė,int 세로좌표,valdiklis_Būsena *너비값,int 최대값,unsigned 색상,unsigned 배경색){int dabartinis_padėtis=0;for(unsigned 순번=0;순번<너비값->길이;순번++){unsigned simbolių_koduotė=너비값->Tekstas[순번],너비=simbolių_koduotė>=256?16:8;if(dabartinis_padėtis+(int)너비>최대값)break;Terminalas_glifas(x_koordinatė+dabartinis_padėtis,세로좌표,simbolių_koduotė,색상,배경색);dabartinis_padėtis+=너비;}}
void 화면다시그림(int savininkas_objektas){
    if(!화면보임(savininkas_objektas))return;
    for(int apdorojimas_tvarka=1;apdorojimas_tvarka<=5;apdorojimas_tvarka++)for(int 순번=0;순번<32;순번++){
        valdiklis_Būsena *너비값=&요소들[savininkas_objektas][순번];if(너비값->sritis_VALUE!=apdorojimas_tvarka||!표시됨(savininkas_objektas,너비값))continue;int x_koordinatė,세로좌표;Pozicija(savininkas_objektas,너비값,&x_koordinatė,&세로좌표);
        if(apdorojimas_tvarka==1){사각영역(x_koordinatė,세로좌표,너비값->너비값,너비값->높이값,0xeee9e0);사각영역(x_koordinatė,세로좌표,너비값->너비값,30,0x905020);Tekstas(x_koordinatė+10,세로좌표+7,너비값,너비값->너비값-50,0xffffff,0x905020);사각영역(x_koordinatė+너비값->너비값-28,세로좌표+4,24,22,0x5555b8);Terminalas_glifas(x_koordinatė+너비값->너비값-20,세로좌표+7,'X',0xffffff,0x5555b8);}
        if(apdorojimas_tvarka==2)사각영역(x_koordinatė,세로좌표,너비값->너비값,너비값->높이값,0xeee9e0);
        if(apdorojimas_tvarka>=3){unsigned 배경색=apdorojimas_tvarka==4?0xc0ab86:apdorojimas_tvarka==5?0xffffff:0xeee9e0;if(apdorojimas_tvarka!=3)사각영역(x_koordinatė,세로좌표,너비값->너비값,너비값->높이값,배경색);Tekstas(x_koordinatė+4,세로좌표+4,너비값,너비값->너비값-8,0x201a15,배경색);if(apdorojimas_tvarka==5&&Reikšmingiausi[savininkas_objektas]==순번+1)사각영역(x_koordinatė,세로좌표+너비값->높이값-2,너비값->너비값,2,0x905020);}
    }
}
int 화면덮음(int savininkas_objektas,int x_koordinatė,int 세로좌표){
    if(!화면보임(savininkas_objektas))return 0;
    for(int 순번=0;순번<32;순번++){
        valdiklis_Būsena *Langas=&요소들[savininkas_objektas][순번];
        if(Langas->sritis_VALUE==1&&Langas->보이는지&&x_koordinatė>=Langas->x_koordinatė&&세로좌표>=Langas->세로좌표&&
           x_koordinatė<Langas->x_koordinatė+Langas->너비값&&세로좌표<Langas->세로좌표+Langas->높이값)return 1;
    }return 0;
}
int 화면가리킴(int savininkas_objektas,unsigned 눌림,int x_koordinatė,int 세로좌표){
    if(!화면보임(savininkas_objektas))return 0;
    if(눌림&1)for(int 순번=31;순번>=0;순번--){valdiklis_Būsena *너비값=&요소들[savininkas_objektas][순번];if(!너비값->sritis_VALUE||!표시됨(savininkas_objektas,너비값))continue;int langas_X,langas_Y;Pozicija(savininkas_objektas,너비값,&langas_X,&langas_Y);
        if(x_koordinatė<langas_X||세로좌표<langas_Y||x_koordinatė>=langas_X+너비값->너비값||세로좌표>=langas_Y+너비값->높이값)continue;
        if(너비값->sritis_VALUE==1&&세로좌표<langas_Y+30&&x_koordinatė>=langas_X+너비값->너비값-28){if(너비값->schema_strategija!=0)너비값->보이는지=0;Įvykis(savininkas_objektas,0x10000+순번+1);Lenta_Terminalas(3);return 1;}
        if(너비값->sritis_VALUE==4){Įvykis(savininkas_objektas,순번+1);return 1;}if(너비값->sritis_VALUE==5){Reikšmingiausi[savininkas_objektas]=순번+1;Lenta_Terminalas(3);return 1;}
        if(너비값->sritis_VALUE==1)return 1;
    }return 0;
}
void 화면누름(int savininkas_objektas,unsigned SECOND_VALUE){
    valdiklis_Būsena *너비값=elementas_VALUE(savininkas_objektas,Reikšmingiausi[savininkas_objektas]);if(!너비값||너비값->sritis_VALUE!=5)return;
    if(SECOND_VALUE==13||SECOND_VALUE==10){Įvykis(savininkas_objektas,Reikšmingiausi[savininkas_objektas]);return;}
    if(SECOND_VALUE==8||SECOND_VALUE==127){if(너비값->길이)너비값->길이--;긴부호없는값[savininkas_objektas]=0;}
    else{
        unsigned simbolių_koduotė=SECOND_VALUE;
        if(긴부호없는값[savininkas_objektas]){if((SECOND_VALUE&192)!=128){긴부호없는값[savininkas_objektas]=0;return;}부호없는결과[savininkas_objektas]=(부호없는결과[savininkas_objektas]<<6)|(SECOND_VALUE&63);if(--긴부호없는값[savininkas_objektas])return;simbolių_koduotė=부호없는결과[savininkas_objektas];}
        else if(SECOND_VALUE>=0xc2&&SECOND_VALUE<=0xf4){긴부호없는값[savininkas_objektas]=SECOND_VALUE<0xe0?1:SECOND_VALUE<0xf0?2:3;부호없는결과[savininkas_objektas]=SECOND_VALUE&((1u<<(6-긴부호없는값[savininkas_objektas]))-1);return;}
        else if(SECOND_VALUE<32||SECOND_VALUE>=128)return;
        if(simbolių_koduotė>0x10ffff||(simbolių_koduotė>=0xd800&&simbolių_koduotė<=0xdfff))return;if(너비값->길이<127)너비값->Tekstas[너비값->길이++]=simbolių_koduotė;
    }
    Lenta_Terminalas(3);
}
int 화면호출(int savininkas_objektas,unsigned Veiksmas,int identifikatorius_VALUE,int 첫째값,int SECOND_VALUE,int simbolio_kodas,int vieta_duomenys){
    if(savininkas_objektas<0||savininkas_objektas>=4)return -22;valdiklis_Būsena *너비값=elementas_VALUE(savininkas_objektas,identifikatorius_VALUE);
    if(Veiksmas==0){if(identifikatorius_VALUE<1||identifikatorius_VALUE>5)return -22;for(int 순번=0;순번<32;순번++)if(요소들[savininkas_objektas][순번].sritis_VALUE==0){너비값=&요소들[savininkas_objektas][순번];memset(너비값,0,sizeof(*너비값));너비값->sritis_VALUE=identifikatorius_VALUE;너비값->보이는지=identifikatorius_VALUE!=1;너비값->너비값=identifikatorius_VALUE==1?380:220;너비값->높이값=identifikatorius_VALUE==1?240:28;너비값->schema_strategija=1;너비값->x_koordinatė=identifikatorius_VALUE==1?130:16;너비값->세로좌표=identifikatorius_VALUE==1?110:16;return 순번+1;}return -28;}
    if(Veiksmas==5){if(!įrašas_COUNT[savininkas_objektas])return 0;int 반환값=įvykis_Sąrašas[savininkas_objektas][첫항목[savininkas_objektas]];첫항목[savininkas_objektas]=(첫항목[savininkas_objektas]+1)%16;įrašas_COUNT[savininkas_objektas]--;return 반환값;}
    if(Veiksmas==6)return 화면보임(savininkas_objektas);
    if(!너비값)return -9;
    int 이전표시=표시됨(savininkas_objektas,너비값);
    if(Veiksmas==1){int 바탕너비=보드화면너비(),바탕높이=보드화면높이();if(첫째값<0||SECOND_VALUE<0||simbolio_kodas<1||vieta_duomenys<1||첫째값>바탕너비||SECOND_VALUE>바탕높이||simbolio_kodas>바탕너비-첫째값||vieta_duomenys>바탕높이-SECOND_VALUE)return -22;너비값->x_koordinatė=첫째값;너비값->세로좌표=SECOND_VALUE;너비값->너비값=simbolio_kodas;너비값->높이값=vieta_duomenys;너비값->rankinis_schema=1;}
    else if(Veiksmas==2){valdiklis_Būsena *antrinis=elementas_VALUE(savininkas_objektas,첫째값);if(!antrinis||antrinis==너비값||antrinis->sritis_VALUE==1)return -22;int duomenys_padėtis=identifikatorius_VALUE;for(int 깊이=0;duomenys_padėtis&&깊이<32;깊이++){if(duomenys_padėtis==첫째값)return -22;valdiklis_Būsena *위쪽=elementas_VALUE(savininkas_objektas,duomenys_padėtis);duomenys_padėtis=위쪽?위쪽->pirminis:0;}antrinis->pirminis=identifikatorius_VALUE;if(!antrinis->rankinis_schema){int 형제요소=0;for(int 순번=0;순번<32;순번++)if(&요소들[savininkas_objektas][순번]!=antrinis&&요소들[savininkas_objektas][순번].pirminis==identifikatorius_VALUE)형제요소++;antrinis->세로좌표=16+형제요소*36;}}
    else if(Veiksmas==3)너비값->보이는지=첫째값!=0;
    else if(Veiksmas==4)너비값->보이는지=0;
    else if(Veiksmas==7)너비값->schema_strategija=첫째값;
    else if(Veiksmas==8)return 너비값->길이;
    else if(Veiksmas==9)return 첫째값>=0&&(unsigned)첫째값<너비값->길이?너비값->Tekstas[첫째값]:-22;
    else return -22;
    if(이전표시||표시됨(savininkas_objektas,너비값))Lenta_Terminalas(3);return 0;
}
int 화면글(int savininkas_objektas,int identifikatorius_VALUE,const uint32_t *duomenys,unsigned prekė_COUNT){valdiklis_Būsena *너비값=elementas_VALUE(savininkas_objektas,identifikatorius_VALUE);if(!너비값)return -9;if(prekė_COUNT>127)return -22;for(unsigned 순번=0;순번<prekė_COUNT;순번++){unsigned simbolių_koduotė=duomenys[순번];if(simbolių_koduotė>0x10ffff||(simbolių_koduotė>=0xd800&&simbolių_koduotė<=0xdfff))return -22;}for(unsigned 순번=0;순번<prekė_COUNT;순번++)너비값->Tekstas[순번]=duomenys[순번];너비값->길이=prekė_COUNT;if(표시됨(savininkas_objektas,너비값))Lenta_Terminalas(3);return 0;}
