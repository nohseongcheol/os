#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* Small native peer layer for the explicitly supported Swing subset. */
#include <stdint.h>
#include <stddef.h>
extern uintptr_t Tabla_slikovna_pika(uintptr_t,uintptr_t,uintptr_t),Tabla_Terminal(uintptr_t);
extern void Terminal_glif(unsigned,unsigned,unsigned,unsigned,unsigned);
extern void *memset(void *,int,size_t);
typedef struct { int območje_VALUE,nadrejen,koordinata_x,세로좌표,너비값,높이값,보이는지,ročno_Krmarjenje,Krmarjenje_pravilnik;unsigned Besedilo[128],길이; } pripomoček_stanje;
static pripomoček_stanje 요소들[4][32];
static int V_fokusu[4],dogodek_Seznam[4][16];static unsigned 첫항목[4],vnos_COUNT[4],부호없는결과[4],긴부호없는값[4];
static void dogodek(int lastnik_predmet,int VALUE){if(vnos_COUNT[lastnik_predmet]<16){dogodek_Seznam[lastnik_predmet][(첫항목[lastnik_predmet]+vnos_COUNT[lastnik_predmet])%16]=VALUE;vnos_COUNT[lastnik_predmet]++;}}
static pripomoček_stanje *element_VALUE(int lastnik_predmet,int identifikator_VALUE){return lastnik_predmet>=0&&lastnik_predmet<4&&identifikator_VALUE>0&&identifikator_VALUE<=32&&요소들[lastnik_predmet][identifikator_VALUE-1].območje_VALUE?&요소들[lastnik_predmet][identifikator_VALUE-1]:0;}
static void 사각영역(int koordinata_x,int 세로좌표,int 너비값,int 높이값,unsigned 색상){Tabla_pravokotnik_polnilo(koordinata_x,세로좌표,너비값,높이값,색상);}
int 화면보임(int lastnik_predmet){if(lastnik_predmet<0||lastnik_predmet>=4)return 0;for(int 순번=0;순번<32;순번++)if(요소들[lastnik_predmet][순번].območje_VALUE==1&&요소들[lastnik_predmet][순번].보이는지)return 1;return 0;}
void 화면초기화(int lastnik_predmet){memset(요소들[lastnik_predmet],0,sizeof(요소들[lastnik_predmet]));vnos_COUNT[lastnik_predmet]=첫항목[lastnik_predmet]=V_fokusu[lastnik_predmet]=긴부호없는값[lastnik_predmet]=0;}
static void Položaj(int lastnik_predmet,pripomoček_stanje *너비값,int *koordinata_x,int *세로좌표){*koordinata_x=너비값->koordinata_x;*세로좌표=너비값->세로좌표;int podatki_položaj=너비값->nadrejen;for(int element_COUNT=0;podatki_položaj&&element_COUNT<32;element_COUNT++){pripomoček_stanje *위쪽=element_VALUE(lastnik_predmet,podatki_položaj);if(!위쪽)break;*koordinata_x+=위쪽->koordinata_x;*세로좌표+=위쪽->세로좌표+(위쪽->območje_VALUE==1?30:0);podatki_položaj=위쪽->nadrejen;}}
static int 표시됨(int lastnik_predmet,pripomoček_stanje *너비값){for(int element_COUNT=0;element_COUNT<32;element_COUNT++){if(!너비값->보이는지)return 0;if(너비값->območje_VALUE==1)return 1;너비값=element_VALUE(lastnik_predmet,너비값->nadrejen);if(!너비값)return 0;}return 0;}
static void Besedilo(int koordinata_x,int 세로좌표,pripomoček_stanje *너비값,int 최대값,unsigned 색상,unsigned 배경색){int sprotno_položaj=0;for(unsigned 순번=0;순번<너비값->길이;순번++){unsigned kodiranje_znakov=너비값->Besedilo[순번],너비=kodiranje_znakov>=256?16:8;if(sprotno_položaj+(int)너비>최대값)break;Terminal_glif(koordinata_x+sprotno_položaj,세로좌표,kodiranje_znakov,색상,배경색);sprotno_položaj+=너비;}}
void 화면다시그림(int lastnik_predmet){
    if(!화면보임(lastnik_predmet))return;
    for(int obdelava_naročilo=1;obdelava_naročilo<=5;obdelava_naročilo++)for(int 순번=0;순번<32;순번++){
        pripomoček_stanje *너비값=&요소들[lastnik_predmet][순번];if(너비값->območje_VALUE!=obdelava_naročilo||!표시됨(lastnik_predmet,너비값))continue;int koordinata_x,세로좌표;Položaj(lastnik_predmet,너비값,&koordinata_x,&세로좌표);
        if(obdelava_naročilo==1){사각영역(koordinata_x,세로좌표,너비값->너비값,너비값->높이값,0xeee9e0);사각영역(koordinata_x,세로좌표,너비값->너비값,30,0x905020);Besedilo(koordinata_x+10,세로좌표+7,너비값,너비값->너비값-50,0xffffff,0x905020);사각영역(koordinata_x+너비값->너비값-28,세로좌표+4,24,22,0x5555b8);Terminal_glif(koordinata_x+너비값->너비값-20,세로좌표+7,'X',0xffffff,0x5555b8);}
        if(obdelava_naročilo==2)사각영역(koordinata_x,세로좌표,너비값->너비값,너비값->높이값,0xeee9e0);
        if(obdelava_naročilo>=3){unsigned 배경색=obdelava_naročilo==4?0xc0ab86:obdelava_naročilo==5?0xffffff:0xeee9e0;if(obdelava_naročilo!=3)사각영역(koordinata_x,세로좌표,너비값->너비값,너비값->높이값,배경색);Besedilo(koordinata_x+4,세로좌표+4,너비값,너비값->너비값-8,0x201a15,배경색);if(obdelava_naročilo==5&&V_fokusu[lastnik_predmet]==순번+1)사각영역(koordinata_x,세로좌표+너비값->높이값-2,너비값->너비값,2,0x905020);}
    }
}
int 화면덮음(int lastnik_predmet,int koordinata_x,int 세로좌표){
    if(!화면보임(lastnik_predmet))return 0;
    for(int 순번=0;순번<32;순번++){
        pripomoček_stanje *okno=&요소들[lastnik_predmet][순번];
        if(okno->območje_VALUE==1&&okno->보이는지&&koordinata_x>=okno->koordinata_x&&세로좌표>=okno->세로좌표&&
           koordinata_x<okno->koordinata_x+okno->너비값&&세로좌표<okno->세로좌표+okno->높이값)return 1;
    }return 0;
}
int 화면가리킴(int lastnik_predmet,unsigned 눌림,int koordinata_x,int 세로좌표){
    if(!화면보임(lastnik_predmet))return 0;
    if(눌림&1)for(int 순번=31;순번>=0;순번--){pripomoček_stanje *너비값=&요소들[lastnik_predmet][순번];if(!너비값->območje_VALUE||!표시됨(lastnik_predmet,너비값))continue;int okno_X,okno_Y;Položaj(lastnik_predmet,너비값,&okno_X,&okno_Y);
        if(koordinata_x<okno_X||세로좌표<okno_Y||koordinata_x>=okno_X+너비값->너비값||세로좌표>=okno_Y+너비값->높이값)continue;
        if(너비값->območje_VALUE==1&&세로좌표<okno_Y+30&&koordinata_x>=okno_X+너비값->너비값-28){if(너비값->Krmarjenje_pravilnik!=0)너비값->보이는지=0;dogodek(lastnik_predmet,0x10000+순번+1);Tabla_Terminal(3);return 1;}
        if(너비값->območje_VALUE==4){dogodek(lastnik_predmet,순번+1);return 1;}if(너비값->območje_VALUE==5){V_fokusu[lastnik_predmet]=순번+1;Tabla_Terminal(3);return 1;}
        if(너비값->območje_VALUE==1)return 1;
    }return 0;
}
void 화면누름(int lastnik_predmet,unsigned SECOND_VALUE){
    pripomoček_stanje *너비값=element_VALUE(lastnik_predmet,V_fokusu[lastnik_predmet]);if(!너비값||너비값->območje_VALUE!=5)return;
    if(SECOND_VALUE==13||SECOND_VALUE==10){dogodek(lastnik_predmet,V_fokusu[lastnik_predmet]);return;}
    if(SECOND_VALUE==8||SECOND_VALUE==127){if(너비값->길이)너비값->길이--;긴부호없는값[lastnik_predmet]=0;}
    else{
        unsigned kodiranje_znakov=SECOND_VALUE;
        if(긴부호없는값[lastnik_predmet]){if((SECOND_VALUE&192)!=128){긴부호없는값[lastnik_predmet]=0;return;}부호없는결과[lastnik_predmet]=(부호없는결과[lastnik_predmet]<<6)|(SECOND_VALUE&63);if(--긴부호없는값[lastnik_predmet])return;kodiranje_znakov=부호없는결과[lastnik_predmet];}
        else if(SECOND_VALUE>=0xc2&&SECOND_VALUE<=0xf4){긴부호없는값[lastnik_predmet]=SECOND_VALUE<0xe0?1:SECOND_VALUE<0xf0?2:3;부호없는결과[lastnik_predmet]=SECOND_VALUE&((1u<<(6-긴부호없는값[lastnik_predmet]))-1);return;}
        else if(SECOND_VALUE<32||SECOND_VALUE>=128)return;
        if(kodiranje_znakov>0x10ffff||(kodiranje_znakov>=0xd800&&kodiranje_znakov<=0xdfff))return;if(너비값->길이<127)너비값->Besedilo[너비값->길이++]=kodiranje_znakov;
    }
    Tabla_Terminal(3);
}
int 화면호출(int lastnik_predmet,unsigned Dejanje,int identifikator_VALUE,int 첫째값,int SECOND_VALUE,int koda_znaka,int cilj_podatki){
    if(lastnik_predmet<0||lastnik_predmet>=4)return -22;pripomoček_stanje *너비값=element_VALUE(lastnik_predmet,identifikator_VALUE);
    if(Dejanje==0){if(identifikator_VALUE<1||identifikator_VALUE>5)return -22;for(int 순번=0;순번<32;순번++)if(요소들[lastnik_predmet][순번].območje_VALUE==0){너비값=&요소들[lastnik_predmet][순번];memset(너비값,0,sizeof(*너비값));너비값->območje_VALUE=identifikator_VALUE;너비값->보이는지=identifikator_VALUE!=1;너비값->너비값=identifikator_VALUE==1?380:220;너비값->높이값=identifikator_VALUE==1?240:28;너비값->Krmarjenje_pravilnik=1;너비값->koordinata_x=identifikator_VALUE==1?130:16;너비값->세로좌표=identifikator_VALUE==1?110:16;return 순번+1;}return -28;}
    if(Dejanje==5){if(!vnos_COUNT[lastnik_predmet])return 0;int 반환값=dogodek_Seznam[lastnik_predmet][첫항목[lastnik_predmet]];첫항목[lastnik_predmet]=(첫항목[lastnik_predmet]+1)%16;vnos_COUNT[lastnik_predmet]--;return 반환값;}
    if(Dejanje==6)return 화면보임(lastnik_predmet);
    if(!너비값)return -9;
    int 이전표시=표시됨(lastnik_predmet,너비값);
    if(Dejanje==1){int 바탕너비=보드화면너비(),Ozadje_višina=보드화면높이();if(첫째값<0||SECOND_VALUE<0||koda_znaka<1||cilj_podatki<1||첫째값>바탕너비||SECOND_VALUE>Ozadje_višina||koda_znaka>바탕너비-첫째값||cilj_podatki>Ozadje_višina-SECOND_VALUE)return -22;너비값->koordinata_x=첫째값;너비값->세로좌표=SECOND_VALUE;너비값->너비값=koda_znaka;너비값->높이값=cilj_podatki;너비값->ročno_Krmarjenje=1;}
    else if(Dejanje==2){pripomoček_stanje *podrejeni=element_VALUE(lastnik_predmet,첫째값);if(!podrejeni||podrejeni==너비값||podrejeni->območje_VALUE==1)return -22;int podatki_položaj=identifikator_VALUE;for(int 깊이=0;podatki_položaj&&깊이<32;깊이++){if(podatki_položaj==첫째값)return -22;pripomoček_stanje *위쪽=element_VALUE(lastnik_predmet,podatki_položaj);podatki_položaj=위쪽?위쪽->nadrejen:0;}podrejeni->nadrejen=identifikator_VALUE;if(!podrejeni->ročno_Krmarjenje){int 형제요소=0;for(int 순번=0;순번<32;순번++)if(&요소들[lastnik_predmet][순번]!=podrejeni&&요소들[lastnik_predmet][순번].nadrejen==identifikator_VALUE)형제요소++;podrejeni->세로좌표=16+형제요소*36;}}
    else if(Dejanje==3)너비값->보이는지=첫째값!=0;
    else if(Dejanje==4)너비값->보이는지=0;
    else if(Dejanje==7)너비값->Krmarjenje_pravilnik=첫째값;
    else if(Dejanje==8)return 너비값->길이;
    else if(Dejanje==9)return 첫째값>=0&&(unsigned)첫째값<너비값->길이?너비값->Besedilo[첫째값]:-22;
    else return -22;
    if(이전표시||표시됨(lastnik_predmet,너비값))Tabla_Terminal(3);return 0;
}
int 화면글(int lastnik_predmet,int identifikator_VALUE,const uint32_t *podatki,unsigned element_COUNT){pripomoček_stanje *너비값=element_VALUE(lastnik_predmet,identifikator_VALUE);if(!너비값)return -9;if(element_COUNT>127)return -22;for(unsigned 순번=0;순번<element_COUNT;순번++){unsigned kodiranje_znakov=podatki[순번];if(kodiranje_znakov>0x10ffff||(kodiranje_znakov>=0xd800&&kodiranje_znakov<=0xdfff))return -22;}for(unsigned 순번=0;순번<element_COUNT;순번++)너비값->Besedilo[순번]=podatki[순번];너비값->길이=element_COUNT;if(표시됨(lastnik_predmet,너비값))Tabla_Terminal(3);return 0;}
