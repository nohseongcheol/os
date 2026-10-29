#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* Small native peer layer for the explicitly supported Swing subset. */
#include <stdint.h>
#include <stddef.h>
extern uintptr_t ploča_pel(uintptr_t,uintptr_t,uintptr_t),ploča_Terminal(uintptr_t);
extern void Terminal_glif(unsigned,unsigned,unsigned,unsigned,unsigned);
extern void *memset(void *,int,size_t);
typedef struct { int oblast_VALUE,roditelj,koordinata_x,Y_koordinata,너비값,높이값,보이는지,ručno_izgled,izgled_pravilo;unsigned Tekst[128],dužina_VALUE; } vidžet_stanje;
static vidžet_stanje 요소들[4][32];
static int U_fokusu[4],događaj_spisak[4][16];static unsigned 첫항목[4],unos_COUNT[4],부호없는결과[4],긴부호없는값[4];
static void događaj(int vlasnik_objekt,int VALUE){if(unos_COUNT[vlasnik_objekt]<16){događaj_spisak[vlasnik_objekt][(첫항목[vlasnik_objekt]+unos_COUNT[vlasnik_objekt])%16]=VALUE;unos_COUNT[vlasnik_objekt]++;}}
static vidžet_stanje *element_VALUE(int vlasnik_objekt,int identifikator_VALUE){return vlasnik_objekt>=0&&vlasnik_objekt<4&&identifikator_VALUE>0&&identifikator_VALUE<=32&&요소들[vlasnik_objekt][identifikator_VALUE-1].oblast_VALUE?&요소들[vlasnik_objekt][identifikator_VALUE-1]:0;}
static void 사각영역(int koordinata_x,int Y_koordinata,int 너비값,int 높이값,unsigned 색상){보드사각그림(koordinata_x,Y_koordinata,너비값,높이값,색상);}
int 화면보임(int vlasnik_objekt){if(vlasnik_objekt<0||vlasnik_objekt>=4)return 0;for(int 순번=0;순번<32;순번++)if(요소들[vlasnik_objekt][순번].oblast_VALUE==1&&요소들[vlasnik_objekt][순번].보이는지)return 1;return 0;}
void 화면초기화(int vlasnik_objekt){memset(요소들[vlasnik_objekt],0,sizeof(요소들[vlasnik_objekt]));unos_COUNT[vlasnik_objekt]=첫항목[vlasnik_objekt]=U_fokusu[vlasnik_objekt]=긴부호없는값[vlasnik_objekt]=0;}
static void Pozicija(int vlasnik_objekt,vidžet_stanje *너비값,int *koordinata_x,int *Y_koordinata){*koordinata_x=너비값->koordinata_x;*Y_koordinata=너비값->Y_koordinata;int podaci_položaj=너비값->roditelj;for(int stavka_COUNT=0;podaci_položaj&&stavka_COUNT<32;stavka_COUNT++){vidžet_stanje *위쪽=element_VALUE(vlasnik_objekt,podaci_položaj);if(!위쪽)break;*koordinata_x+=위쪽->koordinata_x;*Y_koordinata+=위쪽->Y_koordinata+(위쪽->oblast_VALUE==1?30:0);podaci_položaj=위쪽->roditelj;}}
static int 표시됨(int vlasnik_objekt,vidžet_stanje *너비값){for(int stavka_COUNT=0;stavka_COUNT<32;stavka_COUNT++){if(!너비값->보이는지)return 0;if(너비값->oblast_VALUE==1)return 1;너비값=element_VALUE(vlasnik_objekt,너비값->roditelj);if(!너비값)return 0;}return 0;}
static void Tekst(int koordinata_x,int Y_koordinata,vidžet_stanje *너비값,int 최대값,unsigned 색상,unsigned 배경색){int trenutno_položaj=0;for(unsigned 순번=0;순번<너비값->dužina_VALUE;순번++){unsigned znak_kodiranje=너비값->Tekst[순번],너비=znak_kodiranje>=256?16:8;if(trenutno_položaj+(int)너비>최대값)break;Terminal_glif(koordinata_x+trenutno_položaj,Y_koordinata,znak_kodiranje,색상,배경색);trenutno_položaj+=너비;}}
void 화면다시그림(int vlasnik_objekt){
    if(!화면보임(vlasnik_objekt))return;
    for(int 처리차례=1;처리차례<=5;처리차례++)for(int 순번=0;순번<32;순번++){
        vidžet_stanje *너비값=&요소들[vlasnik_objekt][순번];if(너비값->oblast_VALUE!=처리차례||!표시됨(vlasnik_objekt,너비값))continue;int koordinata_x,Y_koordinata;Pozicija(vlasnik_objekt,너비값,&koordinata_x,&Y_koordinata);
        if(처리차례==1){사각영역(koordinata_x,Y_koordinata,너비값->너비값,너비값->높이값,0xeee9e0);사각영역(koordinata_x,Y_koordinata,너비값->너비값,30,0x905020);Tekst(koordinata_x+10,Y_koordinata+7,너비값,너비값->너비값-50,0xffffff,0x905020);사각영역(koordinata_x+너비값->너비값-28,Y_koordinata+4,24,22,0x5555b8);Terminal_glif(koordinata_x+너비값->너비값-20,Y_koordinata+7,'X',0xffffff,0x5555b8);}
        if(처리차례==2)사각영역(koordinata_x,Y_koordinata,너비값->너비값,너비값->높이값,0xeee9e0);
        if(처리차례>=3){unsigned 배경색=처리차례==4?0xc0ab86:처리차례==5?0xffffff:0xeee9e0;if(처리차례!=3)사각영역(koordinata_x,Y_koordinata,너비값->너비값,너비값->높이값,배경색);Tekst(koordinata_x+4,Y_koordinata+4,너비값,너비값->너비값-8,0x201a15,배경색);if(처리차례==5&&U_fokusu[vlasnik_objekt]==순번+1)사각영역(koordinata_x,Y_koordinata+너비값->높이값-2,너비값->너비값,2,0x905020);}
    }
}
int 화면덮음(int vlasnik_objekt,int koordinata_x,int Y_koordinata){
    if(!화면보임(vlasnik_objekt))return 0;
    for(int 순번=0;순번<32;순번++){
        vidžet_stanje *prozor=&요소들[vlasnik_objekt][순번];
        if(prozor->oblast_VALUE==1&&prozor->보이는지&&koordinata_x>=prozor->koordinata_x&&Y_koordinata>=prozor->Y_koordinata&&
           koordinata_x<prozor->koordinata_x+prozor->너비값&&Y_koordinata<prozor->Y_koordinata+prozor->높이값)return 1;
    }return 0;
}
int 화면가리킴(int vlasnik_objekt,unsigned 눌림,int koordinata_x,int Y_koordinata){
    if(!화면보임(vlasnik_objekt))return 0;
    if(눌림&1)for(int 순번=31;순번>=0;순번--){vidžet_stanje *너비값=&요소들[vlasnik_objekt][순번];if(!너비값->oblast_VALUE||!표시됨(vlasnik_objekt,너비값))continue;int prozor_X,prozor_Y;Pozicija(vlasnik_objekt,너비값,&prozor_X,&prozor_Y);
        if(koordinata_x<prozor_X||Y_koordinata<prozor_Y||koordinata_x>=prozor_X+너비값->너비값||Y_koordinata>=prozor_Y+너비값->높이값)continue;
        if(너비값->oblast_VALUE==1&&Y_koordinata<prozor_Y+30&&koordinata_x>=prozor_X+너비값->너비값-28){if(너비값->izgled_pravilo!=0)너비값->보이는지=0;događaj(vlasnik_objekt,0x10000+순번+1);ploča_Terminal(3);return 1;}
        if(너비값->oblast_VALUE==4){događaj(vlasnik_objekt,순번+1);return 1;}if(너비값->oblast_VALUE==5){U_fokusu[vlasnik_objekt]=순번+1;ploča_Terminal(3);return 1;}
        if(너비값->oblast_VALUE==1)return 1;
    }return 0;
}
void 화면누름(int vlasnik_objekt,unsigned SECOND_VALUE){
    vidžet_stanje *너비값=element_VALUE(vlasnik_objekt,U_fokusu[vlasnik_objekt]);if(!너비값||너비값->oblast_VALUE!=5)return;
    if(SECOND_VALUE==13||SECOND_VALUE==10){događaj(vlasnik_objekt,U_fokusu[vlasnik_objekt]);return;}
    if(SECOND_VALUE==8||SECOND_VALUE==127){if(너비값->dužina_VALUE)너비값->dužina_VALUE--;긴부호없는값[vlasnik_objekt]=0;}
    else{
        unsigned znak_kodiranje=SECOND_VALUE;
        if(긴부호없는값[vlasnik_objekt]){if((SECOND_VALUE&192)!=128){긴부호없는값[vlasnik_objekt]=0;return;}부호없는결과[vlasnik_objekt]=(부호없는결과[vlasnik_objekt]<<6)|(SECOND_VALUE&63);if(--긴부호없는값[vlasnik_objekt])return;znak_kodiranje=부호없는결과[vlasnik_objekt];}
        else if(SECOND_VALUE>=0xc2&&SECOND_VALUE<=0xf4){긴부호없는값[vlasnik_objekt]=SECOND_VALUE<0xe0?1:SECOND_VALUE<0xf0?2:3;부호없는결과[vlasnik_objekt]=SECOND_VALUE&((1u<<(6-긴부호없는값[vlasnik_objekt]))-1);return;}
        else if(SECOND_VALUE<32||SECOND_VALUE>=128)return;
        if(znak_kodiranje>0x10ffff||(znak_kodiranje>=0xd800&&znak_kodiranje<=0xdfff))return;if(너비값->dužina_VALUE<127)너비값->Tekst[너비값->dužina_VALUE++]=znak_kodiranje;
    }
    ploča_Terminal(3);
}
int 화면호출(int vlasnik_objekt,unsigned radnja,int identifikator_VALUE,int 첫째값,int SECOND_VALUE,int kôd_znaka,int odredište_podaci){
    if(vlasnik_objekt<0||vlasnik_objekt>=4)return -22;vidžet_stanje *너비값=element_VALUE(vlasnik_objekt,identifikator_VALUE);
    if(radnja==0){if(identifikator_VALUE<1||identifikator_VALUE>5)return -22;for(int 순번=0;순번<32;순번++)if(요소들[vlasnik_objekt][순번].oblast_VALUE==0){너비값=&요소들[vlasnik_objekt][순번];memset(너비값,0,sizeof(*너비값));너비값->oblast_VALUE=identifikator_VALUE;너비값->보이는지=identifikator_VALUE!=1;너비값->너비값=identifikator_VALUE==1?380:220;너비값->높이값=identifikator_VALUE==1?240:28;너비값->izgled_pravilo=1;너비값->koordinata_x=identifikator_VALUE==1?130:16;너비값->Y_koordinata=identifikator_VALUE==1?110:16;return 순번+1;}return -28;}
    if(radnja==5){if(!unos_COUNT[vlasnik_objekt])return 0;int 반환값=događaj_spisak[vlasnik_objekt][첫항목[vlasnik_objekt]];첫항목[vlasnik_objekt]=(첫항목[vlasnik_objekt]+1)%16;unos_COUNT[vlasnik_objekt]--;return 반환값;}
    if(radnja==6)return 화면보임(vlasnik_objekt);
    if(!너비값)return -9;
    int 이전표시=표시됨(vlasnik_objekt,너비값);
    if(radnja==1){int 바탕너비=보드화면너비(),바탕높이=보드화면높이();if(첫째값<0||SECOND_VALUE<0||kôd_znaka<1||odredište_podaci<1||첫째값>바탕너비||SECOND_VALUE>바탕높이||kôd_znaka>바탕너비-첫째값||odredište_podaci>바탕높이-SECOND_VALUE)return -22;너비값->koordinata_x=첫째값;너비값->Y_koordinata=SECOND_VALUE;너비값->너비값=kôd_znaka;너비값->높이값=odredište_podaci;너비값->ručno_izgled=1;}
    else if(radnja==2){vidžet_stanje *podređeni_element=element_VALUE(vlasnik_objekt,첫째값);if(!podređeni_element||podređeni_element==너비값||podređeni_element->oblast_VALUE==1)return -22;int podaci_položaj=identifikator_VALUE;for(int 깊이=0;podaci_položaj&&깊이<32;깊이++){if(podaci_položaj==첫째값)return -22;vidžet_stanje *위쪽=element_VALUE(vlasnik_objekt,podaci_položaj);podaci_položaj=위쪽?위쪽->roditelj:0;}podređeni_element->roditelj=identifikator_VALUE;if(!podređeni_element->ručno_izgled){int 형제요소=0;for(int 순번=0;순번<32;순번++)if(&요소들[vlasnik_objekt][순번]!=podređeni_element&&요소들[vlasnik_objekt][순번].roditelj==identifikator_VALUE)형제요소++;podređeni_element->Y_koordinata=16+형제요소*36;}}
    else if(radnja==3)너비값->보이는지=첫째값!=0;
    else if(radnja==4)너비값->보이는지=0;
    else if(radnja==7)너비값->izgled_pravilo=첫째값;
    else if(radnja==8)return 너비값->dužina_VALUE;
    else if(radnja==9)return 첫째값>=0&&(unsigned)첫째값<너비값->dužina_VALUE?너비값->Tekst[첫째값]:-22;
    else return -22;
    if(이전표시||표시됨(vlasnik_objekt,너비값))ploča_Terminal(3);return 0;
}
int 화면글(int vlasnik_objekt,int identifikator_VALUE,const uint32_t *podaci,unsigned stavka_COUNT){vidžet_stanje *너비값=element_VALUE(vlasnik_objekt,identifikator_VALUE);if(!너비값)return -9;if(stavka_COUNT>127)return -22;for(unsigned 순번=0;순번<stavka_COUNT;순번++){unsigned znak_kodiranje=podaci[순번];if(znak_kodiranje>0x10ffff||(znak_kodiranje>=0xd800&&znak_kodiranje<=0xdfff))return -22;}for(unsigned 순번=0;순번<stavka_COUNT;순번++)너비값->Tekst[순번]=podaci[순번];너비값->dužina_VALUE=stavka_COUNT;if(표시됨(vlasnik_objekt,너비값))ploča_Terminal(3);return 0;}
