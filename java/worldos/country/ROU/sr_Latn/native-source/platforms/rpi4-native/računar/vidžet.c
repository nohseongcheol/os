#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* Small native peer layer for the explicitly supported Swing subset. */
#include <stdint.h>
#include <stddef.h>
extern uintptr_t Tabla_piksel(uintptr_t,uintptr_t,uintptr_t),Tabla_Terminal(uintptr_t);
extern void Terminal_glif(unsigned,unsigned,unsigned,unsigned,unsigned);
extern void *memset(void *,int,size_t);
typedef struct { int oblast_VALUE,nadređen,x_koordinata,세로좌표,너비값,높이값,보이는지,ručno_Raspored,Raspored_propis;unsigned SMS[128],길이; } vidžet_Status;
static vidžet_Status 요소들[4][32];
static int U_fokusu[4],događaj_Lista[4][16];static unsigned 첫항목[4],stavka_COUNT_8f7753a1[4],부호없는결과[4],긴부호없는값[4];
static void događaj(int vlasnik_objekat,int VALUE){if(stavka_COUNT_8f7753a1[vlasnik_objekat]<16){događaj_Lista[vlasnik_objekat][(첫항목[vlasnik_objekat]+stavka_COUNT_8f7753a1[vlasnik_objekat])%16]=VALUE;stavka_COUNT_8f7753a1[vlasnik_objekat]++;}}
static vidžet_Status *element_VALUE(int vlasnik_objekat,int identifikator_VALUE){return vlasnik_objekat>=0&&vlasnik_objekat<4&&identifikator_VALUE>0&&identifikator_VALUE<=32&&요소들[vlasnik_objekat][identifikator_VALUE-1].oblast_VALUE?&요소들[vlasnik_objekat][identifikator_VALUE-1]:0;}
static void 사각영역(int x_koordinata,int 세로좌표,int 너비값,int 높이값,unsigned 색상){보드사각그림(x_koordinata,세로좌표,너비값,높이값,색상);}
int 화면보임(int vlasnik_objekat){if(vlasnik_objekat<0||vlasnik_objekat>=4)return 0;for(int 순번=0;순번<32;순번++)if(요소들[vlasnik_objekat][순번].oblast_VALUE==1&&요소들[vlasnik_objekat][순번].보이는지)return 1;return 0;}
void 화면초기화(int vlasnik_objekat){memset(요소들[vlasnik_objekat],0,sizeof(요소들[vlasnik_objekat]));stavka_COUNT_8f7753a1[vlasnik_objekat]=첫항목[vlasnik_objekat]=U_fokusu[vlasnik_objekat]=긴부호없는값[vlasnik_objekat]=0;}
static void pozicija(int vlasnik_objekat,vidžet_Status *너비값,int *x_koordinata,int *세로좌표){*x_koordinata=너비값->x_koordinata;*세로좌표=너비값->세로좌표;int podaci_pozicija=너비값->nadređen;for(int stavka_COUNT=0;podaci_pozicija&&stavka_COUNT<32;stavka_COUNT++){vidžet_Status *위쪽=element_VALUE(vlasnik_objekat,podaci_pozicija);if(!위쪽)break;*x_koordinata+=위쪽->x_koordinata;*세로좌표+=위쪽->세로좌표+(위쪽->oblast_VALUE==1?30:0);podaci_pozicija=위쪽->nadređen;}}
static int 표시됨(int vlasnik_objekat,vidžet_Status *너비값){for(int stavka_COUNT=0;stavka_COUNT<32;stavka_COUNT++){if(!너비값->보이는지)return 0;if(너비값->oblast_VALUE==1)return 1;너비값=element_VALUE(vlasnik_objekat,너비값->nadređen);if(!너비값)return 0;}return 0;}
static void SMS(int x_koordinata,int 세로좌표,vidžet_Status *너비값,int 최대값,unsigned 색상,unsigned 배경색){int aktuelno_pozicija=0;for(unsigned 순번=0;순번<너비값->길이;순번++){unsigned kodiranje_znakova=너비값->SMS[순번],너비=kodiranje_znakova>=256?16:8;if(aktuelno_pozicija+(int)너비>최대값)break;Terminal_glif(x_koordinata+aktuelno_pozicija,세로좌표,kodiranje_znakova,색상,배경색);aktuelno_pozicija+=너비;}}
void 화면다시그림(int vlasnik_objekat){
    if(!화면보임(vlasnik_objekat))return;
    for(int obrada_poručiti=1;obrada_poručiti<=5;obrada_poručiti++)for(int 순번=0;순번<32;순번++){
        vidžet_Status *너비값=&요소들[vlasnik_objekat][순번];if(너비값->oblast_VALUE!=obrada_poručiti||!표시됨(vlasnik_objekat,너비값))continue;int x_koordinata,세로좌표;pozicija(vlasnik_objekat,너비값,&x_koordinata,&세로좌표);
        if(obrada_poručiti==1){사각영역(x_koordinata,세로좌표,너비값->너비값,너비값->높이값,0xeee9e0);사각영역(x_koordinata,세로좌표,너비값->너비값,30,0x905020);SMS(x_koordinata+10,세로좌표+7,너비값,너비값->너비값-50,0xffffff,0x905020);사각영역(x_koordinata+너비값->너비값-28,세로좌표+4,24,22,0x5555b8);Terminal_glif(x_koordinata+너비값->너비값-20,세로좌표+7,'X',0xffffff,0x5555b8);}
        if(obrada_poručiti==2)사각영역(x_koordinata,세로좌표,너비값->너비값,너비값->높이값,0xeee9e0);
        if(obrada_poručiti>=3){unsigned 배경색=obrada_poručiti==4?0xc0ab86:obrada_poručiti==5?0xffffff:0xeee9e0;if(obrada_poručiti!=3)사각영역(x_koordinata,세로좌표,너비값->너비값,너비값->높이값,배경색);SMS(x_koordinata+4,세로좌표+4,너비값,너비값->너비값-8,0x201a15,배경색);if(obrada_poručiti==5&&U_fokusu[vlasnik_objekat]==순번+1)사각영역(x_koordinata,세로좌표+너비값->높이값-2,너비값->너비값,2,0x905020);}
    }
}
int 화면덮음(int vlasnik_objekat,int x_koordinata,int 세로좌표){
    if(!화면보임(vlasnik_objekat))return 0;
    for(int 순번=0;순번<32;순번++){
        vidžet_Status *prozor=&요소들[vlasnik_objekat][순번];
        if(prozor->oblast_VALUE==1&&prozor->보이는지&&x_koordinata>=prozor->x_koordinata&&세로좌표>=prozor->세로좌표&&
           x_koordinata<prozor->x_koordinata+prozor->너비값&&세로좌표<prozor->세로좌표+prozor->높이값)return 1;
    }return 0;
}
int 화면가리킴(int vlasnik_objekat,unsigned 눌림,int x_koordinata,int 세로좌표){
    if(!화면보임(vlasnik_objekat))return 0;
    if(눌림&1)for(int 순번=31;순번>=0;순번--){vidžet_Status *너비값=&요소들[vlasnik_objekat][순번];if(!너비값->oblast_VALUE||!표시됨(vlasnik_objekat,너비값))continue;int prozor_X,prozor_Y;pozicija(vlasnik_objekat,너비값,&prozor_X,&prozor_Y);
        if(x_koordinata<prozor_X||세로좌표<prozor_Y||x_koordinata>=prozor_X+너비값->너비값||세로좌표>=prozor_Y+너비값->높이값)continue;
        if(너비값->oblast_VALUE==1&&세로좌표<prozor_Y+30&&x_koordinata>=prozor_X+너비값->너비값-28){if(너비값->Raspored_propis!=0)너비값->보이는지=0;događaj(vlasnik_objekat,0x10000+순번+1);Tabla_Terminal(3);return 1;}
        if(너비값->oblast_VALUE==4){događaj(vlasnik_objekat,순번+1);return 1;}if(너비값->oblast_VALUE==5){U_fokusu[vlasnik_objekat]=순번+1;Tabla_Terminal(3);return 1;}
        if(너비값->oblast_VALUE==1)return 1;
    }return 0;
}
void 화면누름(int vlasnik_objekat,unsigned SECOND_VALUE){
    vidžet_Status *너비값=element_VALUE(vlasnik_objekat,U_fokusu[vlasnik_objekat]);if(!너비값||너비값->oblast_VALUE!=5)return;
    if(SECOND_VALUE==13||SECOND_VALUE==10){događaj(vlasnik_objekat,U_fokusu[vlasnik_objekat]);return;}
    if(SECOND_VALUE==8||SECOND_VALUE==127){if(너비값->길이)너비값->길이--;긴부호없는값[vlasnik_objekat]=0;}
    else{
        unsigned kodiranje_znakova=SECOND_VALUE;
        if(긴부호없는값[vlasnik_objekat]){if((SECOND_VALUE&192)!=128){긴부호없는값[vlasnik_objekat]=0;return;}부호없는결과[vlasnik_objekat]=(부호없는결과[vlasnik_objekat]<<6)|(SECOND_VALUE&63);if(--긴부호없는값[vlasnik_objekat])return;kodiranje_znakova=부호없는결과[vlasnik_objekat];}
        else if(SECOND_VALUE>=0xc2&&SECOND_VALUE<=0xf4){긴부호없는값[vlasnik_objekat]=SECOND_VALUE<0xe0?1:SECOND_VALUE<0xf0?2:3;부호없는결과[vlasnik_objekat]=SECOND_VALUE&((1u<<(6-긴부호없는값[vlasnik_objekat]))-1);return;}
        else if(SECOND_VALUE<32||SECOND_VALUE>=128)return;
        if(kodiranje_znakova>0x10ffff||(kodiranje_znakova>=0xd800&&kodiranje_znakova<=0xdfff))return;if(너비값->길이<127)너비값->SMS[너비값->길이++]=kodiranje_znakova;
    }
    Tabla_Terminal(3);
}
int 화면호출(int vlasnik_objekat,unsigned radnja,int identifikator_VALUE,int 첫째값,int SECOND_VALUE,int kôd_znaka,int odredište_podaci){
    if(vlasnik_objekat<0||vlasnik_objekat>=4)return -22;vidžet_Status *너비값=element_VALUE(vlasnik_objekat,identifikator_VALUE);
    if(radnja==0){if(identifikator_VALUE<1||identifikator_VALUE>5)return -22;for(int 순번=0;순번<32;순번++)if(요소들[vlasnik_objekat][순번].oblast_VALUE==0){너비값=&요소들[vlasnik_objekat][순번];memset(너비값,0,sizeof(*너비값));너비값->oblast_VALUE=identifikator_VALUE;너비값->보이는지=identifikator_VALUE!=1;너비값->너비값=identifikator_VALUE==1?380:220;너비값->높이값=identifikator_VALUE==1?240:28;너비값->Raspored_propis=1;너비값->x_koordinata=identifikator_VALUE==1?130:16;너비값->세로좌표=identifikator_VALUE==1?110:16;return 순번+1;}return -28;}
    if(radnja==5){if(!stavka_COUNT_8f7753a1[vlasnik_objekat])return 0;int 반환값=događaj_Lista[vlasnik_objekat][첫항목[vlasnik_objekat]];첫항목[vlasnik_objekat]=(첫항목[vlasnik_objekat]+1)%16;stavka_COUNT_8f7753a1[vlasnik_objekat]--;return 반환값;}
    if(radnja==6)return 화면보임(vlasnik_objekat);
    if(!너비값)return -9;
    int 이전표시=표시됨(vlasnik_objekat,너비값);
    if(radnja==1){int 바탕너비=보드화면너비(),바탕높이=보드화면높이();if(첫째값<0||SECOND_VALUE<0||kôd_znaka<1||odredište_podaci<1||첫째값>바탕너비||SECOND_VALUE>바탕높이||kôd_znaka>바탕너비-첫째값||odredište_podaci>바탕높이-SECOND_VALUE)return -22;너비값->x_koordinata=첫째값;너비값->세로좌표=SECOND_VALUE;너비값->너비값=kôd_znaka;너비값->높이값=odredište_podaci;너비값->ručno_Raspored=1;}
    else if(radnja==2){vidžet_Status *podređeni_element=element_VALUE(vlasnik_objekat,첫째값);if(!podređeni_element||podređeni_element==너비값||podređeni_element->oblast_VALUE==1)return -22;int podaci_pozicija=identifikator_VALUE;for(int 깊이=0;podaci_pozicija&&깊이<32;깊이++){if(podaci_pozicija==첫째값)return -22;vidžet_Status *위쪽=element_VALUE(vlasnik_objekat,podaci_pozicija);podaci_pozicija=위쪽?위쪽->nadređen:0;}podređeni_element->nadređen=identifikator_VALUE;if(!podređeni_element->ručno_Raspored){int 형제요소=0;for(int 순번=0;순번<32;순번++)if(&요소들[vlasnik_objekat][순번]!=podređeni_element&&요소들[vlasnik_objekat][순번].nadređen==identifikator_VALUE)형제요소++;podređeni_element->세로좌표=16+형제요소*36;}}
    else if(radnja==3)너비값->보이는지=첫째값!=0;
    else if(radnja==4)너비값->보이는지=0;
    else if(radnja==7)너비값->Raspored_propis=첫째값;
    else if(radnja==8)return 너비값->길이;
    else if(radnja==9)return 첫째값>=0&&(unsigned)첫째값<너비값->길이?너비값->SMS[첫째값]:-22;
    else return -22;
    if(이전표시||표시됨(vlasnik_objekat,너비값))Tabla_Terminal(3);return 0;
}
int 화면글(int vlasnik_objekat,int identifikator_VALUE,const uint32_t *podaci,unsigned stavka_COUNT){vidžet_Status *너비값=element_VALUE(vlasnik_objekat,identifikator_VALUE);if(!너비값)return -9;if(stavka_COUNT>127)return -22;for(unsigned 순번=0;순번<stavka_COUNT;순번++){unsigned kodiranje_znakova=podaci[순번];if(kodiranje_znakova>0x10ffff||(kodiranje_znakova>=0xd800&&kodiranje_znakova<=0xdfff))return -22;}for(unsigned 순번=0;순번<stavka_COUNT;순번++)너비값->SMS[순번]=podaci[순번];너비값->길이=stavka_COUNT;if(표시됨(vlasnik_objekat,너비값))Tabla_Terminal(3);return 0;}
