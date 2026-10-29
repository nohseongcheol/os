#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* Small native peer layer for the explicitly supported Swing subset. */
#include <stdint.h>
#include <stddef.h>
extern uintptr_t pano_slikovni_element(uintptr_t,uintptr_t,uintptr_t),pano_Terminal(uintptr_t);
extern void Terminal_glif(unsigned,unsigned,unsigned,unsigned,unsigned);
extern void *memset(void *,int,size_t);
typedef struct { int područje_VALUE,roditeljski,koordinata_x,세로좌표,너비값,높이값,보이는지,ručno_Raspored,Raspored_pravila;unsigned Tekst[128],길이; } widget_Stanje;
static widget_Stanje 요소들[4][32];
static int U_fokusu[4],događaj_Popis[4][16];static unsigned 첫항목[4],unos_COUNT[4],부호없는결과[4],긴부호없는값[4];
static void Događaj(int vlasnik_objekt,int VALUE){if(unos_COUNT[vlasnik_objekt]<16){događaj_Popis[vlasnik_objekt][(첫항목[vlasnik_objekt]+unos_COUNT[vlasnik_objekt])%16]=VALUE;unos_COUNT[vlasnik_objekt]++;}}
static widget_Stanje *element_VALUE(int vlasnik_objekt,int identifikator_VALUE){return vlasnik_objekt>=0&&vlasnik_objekt<4&&identifikator_VALUE>0&&identifikator_VALUE<=32&&요소들[vlasnik_objekt][identifikator_VALUE-1].područje_VALUE?&요소들[vlasnik_objekt][identifikator_VALUE-1]:0;}
static void 사각영역(int koordinata_x,int 세로좌표,int 너비값,int 높이값,unsigned 색상){pano_pravokutnik_ispuna(koordinata_x,세로좌표,너비값,높이값,색상);}
int 화면보임(int vlasnik_objekt){if(vlasnik_objekt<0||vlasnik_objekt>=4)return 0;for(int 순번=0;순번<32;순번++)if(요소들[vlasnik_objekt][순번].područje_VALUE==1&&요소들[vlasnik_objekt][순번].보이는지)return 1;return 0;}
void 화면초기화(int vlasnik_objekt){memset(요소들[vlasnik_objekt],0,sizeof(요소들[vlasnik_objekt]));unos_COUNT[vlasnik_objekt]=첫항목[vlasnik_objekt]=U_fokusu[vlasnik_objekt]=긴부호없는값[vlasnik_objekt]=0;}
static void Položaj(int vlasnik_objekt,widget_Stanje *너비값,int *koordinata_x,int *세로좌표){*koordinata_x=너비값->koordinata_x;*세로좌표=너비값->세로좌표;int podaci_položaj=너비값->roditeljski;for(int artikl_COUNT=0;podaci_položaj&&artikl_COUNT<32;artikl_COUNT++){widget_Stanje *위쪽=element_VALUE(vlasnik_objekt,podaci_položaj);if(!위쪽)break;*koordinata_x+=위쪽->koordinata_x;*세로좌표+=위쪽->세로좌표+(위쪽->područje_VALUE==1?30:0);podaci_položaj=위쪽->roditeljski;}}
static int 표시됨(int vlasnik_objekt,widget_Stanje *너비값){for(int artikl_COUNT=0;artikl_COUNT<32;artikl_COUNT++){if(!너비값->보이는지)return 0;if(너비값->područje_VALUE==1)return 1;너비값=element_VALUE(vlasnik_objekt,너비값->roditeljski);if(!너비값)return 0;}return 0;}
static void Tekst(int koordinata_x,int 세로좌표,widget_Stanje *너비값,int 최대값,unsigned 색상,unsigned 배경색){int redovno_položaj=0;for(unsigned 순번=0;순번<너비값->길이;순번++){unsigned kodiranje_znakova=너비값->Tekst[순번],너비=kodiranje_znakova>=256?16:8;if(redovno_položaj+(int)너비>최대값)break;Terminal_glif(koordinata_x+redovno_položaj,세로좌표,kodiranje_znakova,색상,배경색);redovno_položaj+=너비;}}
void 화면다시그림(int vlasnik_objekt){
    if(!화면보임(vlasnik_objekt))return;
    for(int obrada_narudžba=1;obrada_narudžba<=5;obrada_narudžba++)for(int 순번=0;순번<32;순번++){
        widget_Stanje *너비값=&요소들[vlasnik_objekt][순번];if(너비값->područje_VALUE!=obrada_narudžba||!표시됨(vlasnik_objekt,너비값))continue;int koordinata_x,세로좌표;Položaj(vlasnik_objekt,너비값,&koordinata_x,&세로좌표);
        if(obrada_narudžba==1){사각영역(koordinata_x,세로좌표,너비값->너비값,너비값->높이값,0xeee9e0);사각영역(koordinata_x,세로좌표,너비값->너비값,30,0x905020);Tekst(koordinata_x+10,세로좌표+7,너비값,너비값->너비값-50,0xffffff,0x905020);사각영역(koordinata_x+너비값->너비값-28,세로좌표+4,24,22,0x5555b8);Terminal_glif(koordinata_x+너비값->너비값-20,세로좌표+7,'X',0xffffff,0x5555b8);}
        if(obrada_narudžba==2)사각영역(koordinata_x,세로좌표,너비값->너비값,너비값->높이값,0xeee9e0);
        if(obrada_narudžba>=3){unsigned 배경색=obrada_narudžba==4?0xc0ab86:obrada_narudžba==5?0xffffff:0xeee9e0;if(obrada_narudžba!=3)사각영역(koordinata_x,세로좌표,너비값->너비값,너비값->높이값,배경색);Tekst(koordinata_x+4,세로좌표+4,너비값,너비값->너비값-8,0x201a15,배경색);if(obrada_narudžba==5&&U_fokusu[vlasnik_objekt]==순번+1)사각영역(koordinata_x,세로좌표+너비값->높이값-2,너비값->너비값,2,0x905020);}
    }
}
int 화면덮음(int vlasnik_objekt,int koordinata_x,int 세로좌표){
    if(!화면보임(vlasnik_objekt))return 0;
    for(int 순번=0;순번<32;순번++){
        widget_Stanje *Prozor=&요소들[vlasnik_objekt][순번];
        if(Prozor->područje_VALUE==1&&Prozor->보이는지&&koordinata_x>=Prozor->koordinata_x&&세로좌표>=Prozor->세로좌표&&
           koordinata_x<Prozor->koordinata_x+Prozor->너비값&&세로좌표<Prozor->세로좌표+Prozor->높이값)return 1;
    }return 0;
}
int 화면가리킴(int vlasnik_objekt,unsigned 눌림,int koordinata_x,int 세로좌표){
    if(!화면보임(vlasnik_objekt))return 0;
    if(눌림&1)for(int 순번=31;순번>=0;순번--){widget_Stanje *너비값=&요소들[vlasnik_objekt][순번];if(!너비값->područje_VALUE||!표시됨(vlasnik_objekt,너비값))continue;int prozor_X,prozor_Y;Položaj(vlasnik_objekt,너비값,&prozor_X,&prozor_Y);
        if(koordinata_x<prozor_X||세로좌표<prozor_Y||koordinata_x>=prozor_X+너비값->너비값||세로좌표>=prozor_Y+너비값->높이값)continue;
        if(너비값->područje_VALUE==1&&세로좌표<prozor_Y+30&&koordinata_x>=prozor_X+너비값->너비값-28){if(너비값->Raspored_pravila!=0)너비값->보이는지=0;Događaj(vlasnik_objekt,0x10000+순번+1);pano_Terminal(3);return 1;}
        if(너비값->područje_VALUE==4){Događaj(vlasnik_objekt,순번+1);return 1;}if(너비값->područje_VALUE==5){U_fokusu[vlasnik_objekt]=순번+1;pano_Terminal(3);return 1;}
        if(너비값->područje_VALUE==1)return 1;
    }return 0;
}
void 화면누름(int vlasnik_objekt,unsigned SECOND_VALUE){
    widget_Stanje *너비값=element_VALUE(vlasnik_objekt,U_fokusu[vlasnik_objekt]);if(!너비값||너비값->područje_VALUE!=5)return;
    if(SECOND_VALUE==13||SECOND_VALUE==10){Događaj(vlasnik_objekt,U_fokusu[vlasnik_objekt]);return;}
    if(SECOND_VALUE==8||SECOND_VALUE==127){if(너비값->길이)너비값->길이--;긴부호없는값[vlasnik_objekt]=0;}
    else{
        unsigned kodiranje_znakova=SECOND_VALUE;
        if(긴부호없는값[vlasnik_objekt]){if((SECOND_VALUE&192)!=128){긴부호없는값[vlasnik_objekt]=0;return;}부호없는결과[vlasnik_objekt]=(부호없는결과[vlasnik_objekt]<<6)|(SECOND_VALUE&63);if(--긴부호없는값[vlasnik_objekt])return;kodiranje_znakova=부호없는결과[vlasnik_objekt];}
        else if(SECOND_VALUE>=0xc2&&SECOND_VALUE<=0xf4){긴부호없는값[vlasnik_objekt]=SECOND_VALUE<0xe0?1:SECOND_VALUE<0xf0?2:3;부호없는결과[vlasnik_objekt]=SECOND_VALUE&((1u<<(6-긴부호없는값[vlasnik_objekt]))-1);return;}
        else if(SECOND_VALUE<32||SECOND_VALUE>=128)return;
        if(kodiranje_znakova>0x10ffff||(kodiranje_znakova>=0xd800&&kodiranje_znakova<=0xdfff))return;if(너비값->길이<127)너비값->Tekst[너비값->길이++]=kodiranje_znakova;
    }
    pano_Terminal(3);
}
int 화면호출(int vlasnik_objekt,unsigned Aktivnost,int identifikator_VALUE,int 첫째값,int SECOND_VALUE,int kodna_točka,int odredište_podaci){
    if(vlasnik_objekt<0||vlasnik_objekt>=4)return -22;widget_Stanje *너비값=element_VALUE(vlasnik_objekt,identifikator_VALUE);
    if(Aktivnost==0){if(identifikator_VALUE<1||identifikator_VALUE>5)return -22;for(int 순번=0;순번<32;순번++)if(요소들[vlasnik_objekt][순번].područje_VALUE==0){너비값=&요소들[vlasnik_objekt][순번];memset(너비값,0,sizeof(*너비값));너비값->područje_VALUE=identifikator_VALUE;너비값->보이는지=identifikator_VALUE!=1;너비값->너비값=identifikator_VALUE==1?380:220;너비값->높이값=identifikator_VALUE==1?240:28;너비값->Raspored_pravila=1;너비값->koordinata_x=identifikator_VALUE==1?130:16;너비값->세로좌표=identifikator_VALUE==1?110:16;return 순번+1;}return -28;}
    if(Aktivnost==5){if(!unos_COUNT[vlasnik_objekt])return 0;int 반환값=događaj_Popis[vlasnik_objekt][첫항목[vlasnik_objekt]];첫항목[vlasnik_objekt]=(첫항목[vlasnik_objekt]+1)%16;unos_COUNT[vlasnik_objekt]--;return 반환값;}
    if(Aktivnost==6)return 화면보임(vlasnik_objekt);
    if(!너비값)return -9;
    int 이전표시=표시됨(vlasnik_objekt,너비값);
    if(Aktivnost==1){int 바탕너비=보드화면너비(),바탕높이=보드화면높이();if(첫째값<0||SECOND_VALUE<0||kodna_točka<1||odredište_podaci<1||첫째값>바탕너비||SECOND_VALUE>바탕높이||kodna_točka>바탕너비-첫째값||odredište_podaci>바탕높이-SECOND_VALUE)return -22;너비값->koordinata_x=첫째값;너비값->세로좌표=SECOND_VALUE;너비값->너비값=kodna_točka;너비값->높이값=odredište_podaci;너비값->ručno_Raspored=1;}
    else if(Aktivnost==2){widget_Stanje *podređeni_element=element_VALUE(vlasnik_objekt,첫째값);if(!podređeni_element||podređeni_element==너비값||podređeni_element->područje_VALUE==1)return -22;int podaci_položaj=identifikator_VALUE;for(int 깊이=0;podaci_položaj&&깊이<32;깊이++){if(podaci_položaj==첫째값)return -22;widget_Stanje *위쪽=element_VALUE(vlasnik_objekt,podaci_položaj);podaci_položaj=위쪽?위쪽->roditeljski:0;}podređeni_element->roditeljski=identifikator_VALUE;if(!podređeni_element->ručno_Raspored){int 형제요소=0;for(int 순번=0;순번<32;순번++)if(&요소들[vlasnik_objekt][순번]!=podređeni_element&&요소들[vlasnik_objekt][순번].roditeljski==identifikator_VALUE)형제요소++;podređeni_element->세로좌표=16+형제요소*36;}}
    else if(Aktivnost==3)너비값->보이는지=첫째값!=0;
    else if(Aktivnost==4)너비값->보이는지=0;
    else if(Aktivnost==7)너비값->Raspored_pravila=첫째값;
    else if(Aktivnost==8)return 너비값->길이;
    else if(Aktivnost==9)return 첫째값>=0&&(unsigned)첫째값<너비값->길이?너비값->Tekst[첫째값]:-22;
    else return -22;
    if(이전표시||표시됨(vlasnik_objekt,너비값))pano_Terminal(3);return 0;
}
int 화면글(int vlasnik_objekt,int identifikator_VALUE,const uint32_t *podaci,unsigned artikl_COUNT){widget_Stanje *너비값=element_VALUE(vlasnik_objekt,identifikator_VALUE);if(!너비값)return -9;if(artikl_COUNT>127)return -22;for(unsigned 순번=0;순번<artikl_COUNT;순번++){unsigned kodiranje_znakova=podaci[순번];if(kodiranje_znakova>0x10ffff||(kodiranje_znakova>=0xd800&&kodiranje_znakova<=0xdfff))return -22;}for(unsigned 순번=0;순번<artikl_COUNT;순번++)너비값->Tekst[순번]=podaci[순번];너비값->길이=artikl_COUNT;if(표시됨(vlasnik_objekt,너비값))pano_Terminal(3);return 0;}
