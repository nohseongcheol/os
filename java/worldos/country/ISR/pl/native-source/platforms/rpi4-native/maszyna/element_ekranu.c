#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* Small native peer layer for the explicitly supported Swing subset. */
#include <stdint.h>
#include <stddef.h>
extern uintptr_t Tablica_piksel(uintptr_t,uintptr_t,uintptr_t),Tablica_Terminal(uintptr_t);
extern void Terminal_symbol(unsigned,unsigned,unsigned,unsigned,unsigned);
extern void *memset(void *,int,size_t);
typedef struct { int obszar_WARTOŚĆ,nadrzędny,współrzędna_X,Y_współrzędna,너비값,wymagane_wysokość_WARTOŚĆ,보이는지,수동배치,Układ_Policy;unsigned tekst[128],długość_WARTOŚĆ; } widget_Stan;
static widget_Stan 요소들[4][32];
static int Priorytetowe[4],konkurs_Lista[4][16];static unsigned 첫항목[4],wpis_ILE_LICZB[4],부호없는결과[4],긴부호없는값[4];
static void Wydarzenie(int właściciel_obiekt,int WARTOŚĆ){if(wpis_ILE_LICZB[właściciel_obiekt]<16){konkurs_Lista[właściciel_obiekt][(첫항목[właściciel_obiekt]+wpis_ILE_LICZB[właściciel_obiekt])%16]=WARTOŚĆ;wpis_ILE_LICZB[właściciel_obiekt]++;}}
static widget_Stan *element_WARTOŚĆ(int właściciel_obiekt,int identyfikator_WARTOŚĆ){return właściciel_obiekt>=0&&właściciel_obiekt<4&&identyfikator_WARTOŚĆ>0&&identyfikator_WARTOŚĆ<=32&&요소들[właściciel_obiekt][identyfikator_WARTOŚĆ-1].obszar_WARTOŚĆ?&요소들[właściciel_obiekt][identyfikator_WARTOŚĆ-1]:0;}
static void 사각영역(int współrzędna_X,int Y_współrzędna,int 너비값,int wymagane_wysokość_WARTOŚĆ,unsigned 색상){Tablica_prostokąt_Wypełnij(współrzędna_X,Y_współrzędna,너비값,wymagane_wysokość_WARTOŚĆ,색상);}
int 화면보임(int właściciel_obiekt){if(właściciel_obiekt<0||właściciel_obiekt>=4)return 0;for(int 순번=0;순번<32;순번++)if(요소들[właściciel_obiekt][순번].obszar_WARTOŚĆ==1&&요소들[właściciel_obiekt][순번].보이는지)return 1;return 0;}
void 화면초기화(int właściciel_obiekt){memset(요소들[właściciel_obiekt],0,sizeof(요소들[właściciel_obiekt]));wpis_ILE_LICZB[właściciel_obiekt]=첫항목[właściciel_obiekt]=Priorytetowe[właściciel_obiekt]=긴부호없는값[właściciel_obiekt]=0;}
static void pozycja(int właściciel_obiekt,widget_Stan *너비값,int *współrzędna_X,int *Y_współrzędna){*współrzędna_X=너비값->współrzędna_X;*Y_współrzędna=너비값->Y_współrzędna;int dane_stanowisko=너비값->nadrzędny;for(int towar_ILE_LICZB=0;dane_stanowisko&&towar_ILE_LICZB<32;towar_ILE_LICZB++){widget_Stan *위쪽=element_WARTOŚĆ(właściciel_obiekt,dane_stanowisko);if(!위쪽)break;*współrzędna_X+=위쪽->współrzędna_X;*Y_współrzędna+=위쪽->Y_współrzędna+(위쪽->obszar_WARTOŚĆ==1?30:0);dane_stanowisko=위쪽->nadrzędny;}}
static int 표시됨(int właściciel_obiekt,widget_Stan *너비값){for(int towar_ILE_LICZB=0;towar_ILE_LICZB<32;towar_ILE_LICZB++){if(!너비값->보이는지)return 0;if(너비값->obszar_WARTOŚĆ==1)return 1;너비값=element_WARTOŚĆ(właściciel_obiekt,너비값->nadrzędny);if(!너비값)return 0;}return 0;}
static void tekst(int współrzędna_X,int Y_współrzędna,widget_Stan *너비값,int 최대값,unsigned 색상,unsigned 배경색){int bieżący_stanowisko=0;for(unsigned 순번=0;순번<너비값->długość_WARTOŚĆ;순번++){unsigned kodowanie_znaku=너비값->tekst[순번],너비=kodowanie_znaku>=256?16:8;if(bieżący_stanowisko+(int)너비>최대값)break;Terminal_symbol(współrzędna_X+bieżący_stanowisko,Y_współrzędna,kodowanie_znaku,색상,배경색);bieżący_stanowisko+=너비;}}
void 화면다시그림(int właściciel_obiekt){
    if(!화면보임(właściciel_obiekt))return;
    for(int przetwarzanie_zamówić=1;przetwarzanie_zamówić<=5;przetwarzanie_zamówić++)for(int 순번=0;순번<32;순번++){
        widget_Stan *너비값=&요소들[właściciel_obiekt][순번];if(너비값->obszar_WARTOŚĆ!=przetwarzanie_zamówić||!표시됨(właściciel_obiekt,너비값))continue;int współrzędna_X,Y_współrzędna;pozycja(właściciel_obiekt,너비값,&współrzędna_X,&Y_współrzędna);
        if(przetwarzanie_zamówić==1){사각영역(współrzędna_X,Y_współrzędna,너비값->너비값,너비값->wymagane_wysokość_WARTOŚĆ,0xeee9e0);사각영역(współrzędna_X,Y_współrzędna,너비값->너비값,30,0x905020);tekst(współrzędna_X+10,Y_współrzędna+7,너비값,너비값->너비값-50,0xffffff,0x905020);사각영역(współrzędna_X+너비값->너비값-28,Y_współrzędna+4,24,22,0x5555b8);Terminal_symbol(współrzędna_X+너비값->너비값-20,Y_współrzędna+7,'X',0xffffff,0x5555b8);}
        if(przetwarzanie_zamówić==2)사각영역(współrzędna_X,Y_współrzędna,너비값->너비값,너비값->wymagane_wysokość_WARTOŚĆ,0xeee9e0);
        if(przetwarzanie_zamówić>=3){unsigned 배경색=przetwarzanie_zamówić==4?0xc0ab86:przetwarzanie_zamówić==5?0xffffff:0xeee9e0;if(przetwarzanie_zamówić!=3)사각영역(współrzędna_X,Y_współrzędna,너비값->너비값,너비값->wymagane_wysokość_WARTOŚĆ,배경색);tekst(współrzędna_X+4,Y_współrzędna+4,너비값,너비값->너비값-8,0x201a15,배경색);if(przetwarzanie_zamówić==5&&Priorytetowe[właściciel_obiekt]==순번+1)사각영역(współrzędna_X,Y_współrzędna+너비값->wymagane_wysokość_WARTOŚĆ-2,너비값->너비값,2,0x905020);}
    }
}
int 화면덮음(int właściciel_obiekt,int współrzędna_X,int Y_współrzędna){
    if(!화면보임(właściciel_obiekt))return 0;
    for(int 순번=0;순번<32;순번++){
        widget_Stan *Okno=&요소들[właściciel_obiekt][순번];
        if(Okno->obszar_WARTOŚĆ==1&&Okno->보이는지&&współrzędna_X>=Okno->współrzędna_X&&Y_współrzędna>=Okno->Y_współrzędna&&
           współrzędna_X<Okno->współrzędna_X+Okno->너비값&&Y_współrzędna<Okno->Y_współrzędna+Okno->wymagane_wysokość_WARTOŚĆ)return 1;
    }return 0;
}
int 화면가리킴(int właściciel_obiekt,unsigned 눌림,int współrzędna_X,int Y_współrzędna){
    if(!화면보임(właściciel_obiekt))return 0;
    if(눌림&1)for(int 순번=31;순번>=0;순번--){widget_Stan *너비값=&요소들[właściciel_obiekt][순번];if(!너비값->obszar_WARTOŚĆ||!표시됨(właściciel_obiekt,너비값))continue;int okno_X,okno_Y;pozycja(właściciel_obiekt,너비값,&okno_X,&okno_Y);
        if(współrzędna_X<okno_X||Y_współrzędna<okno_Y||współrzędna_X>=okno_X+너비값->너비값||Y_współrzędna>=okno_Y+너비값->wymagane_wysokość_WARTOŚĆ)continue;
        if(너비값->obszar_WARTOŚĆ==1&&Y_współrzędna<okno_Y+30&&współrzędna_X>=okno_X+너비값->너비값-28){if(너비값->Układ_Policy!=0)너비값->보이는지=0;Wydarzenie(właściciel_obiekt,0x10000+순번+1);Tablica_Terminal(3);return 1;}
        if(너비값->obszar_WARTOŚĆ==4){Wydarzenie(właściciel_obiekt,순번+1);return 1;}if(너비값->obszar_WARTOŚĆ==5){Priorytetowe[właściciel_obiekt]=순번+1;Tablica_Terminal(3);return 1;}
        if(너비값->obszar_WARTOŚĆ==1)return 1;
    }return 0;
}
void 화면누름(int właściciel_obiekt,unsigned SEKUNDA_WARTOŚĆ){
    widget_Stan *너비값=element_WARTOŚĆ(właściciel_obiekt,Priorytetowe[właściciel_obiekt]);if(!너비값||너비값->obszar_WARTOŚĆ!=5)return;
    if(SEKUNDA_WARTOŚĆ==13||SEKUNDA_WARTOŚĆ==10){Wydarzenie(właściciel_obiekt,Priorytetowe[właściciel_obiekt]);return;}
    if(SEKUNDA_WARTOŚĆ==8||SEKUNDA_WARTOŚĆ==127){if(너비값->długość_WARTOŚĆ)너비값->długość_WARTOŚĆ--;긴부호없는값[właściciel_obiekt]=0;}
    else{
        unsigned kodowanie_znaku=SEKUNDA_WARTOŚĆ;
        if(긴부호없는값[właściciel_obiekt]){if((SEKUNDA_WARTOŚĆ&192)!=128){긴부호없는값[właściciel_obiekt]=0;return;}부호없는결과[właściciel_obiekt]=(부호없는결과[właściciel_obiekt]<<6)|(SEKUNDA_WARTOŚĆ&63);if(--긴부호없는값[właściciel_obiekt])return;kodowanie_znaku=부호없는결과[właściciel_obiekt];}
        else if(SEKUNDA_WARTOŚĆ>=0xc2&&SEKUNDA_WARTOŚĆ<=0xf4){긴부호없는값[właściciel_obiekt]=SEKUNDA_WARTOŚĆ<0xe0?1:SEKUNDA_WARTOŚĆ<0xf0?2:3;부호없는결과[właściciel_obiekt]=SEKUNDA_WARTOŚĆ&((1u<<(6-긴부호없는값[właściciel_obiekt]))-1);return;}
        else if(SEKUNDA_WARTOŚĆ<32||SEKUNDA_WARTOŚĆ>=128)return;
        if(kodowanie_znaku>0x10ffff||(kodowanie_znaku>=0xd800&&kodowanie_znaku<=0xdfff))return;if(너비값->długość_WARTOŚĆ<127)너비값->tekst[너비값->długość_WARTOŚĆ++]=kodowanie_znaku;
    }
    Tablica_Terminal(3);
}
int 화면호출(int właściciel_obiekt,unsigned Akcja,int identyfikator_WARTOŚĆ,int 첫째값,int SEKUNDA_WARTOŚĆ,int kod_znaku,int cel_dane){
    if(właściciel_obiekt<0||właściciel_obiekt>=4)return -22;widget_Stan *너비값=element_WARTOŚĆ(właściciel_obiekt,identyfikator_WARTOŚĆ);
    if(Akcja==0){if(identyfikator_WARTOŚĆ<1||identyfikator_WARTOŚĆ>5)return -22;for(int 순번=0;순번<32;순번++)if(요소들[właściciel_obiekt][순번].obszar_WARTOŚĆ==0){너비값=&요소들[właściciel_obiekt][순번];memset(너비값,0,sizeof(*너비값));너비값->obszar_WARTOŚĆ=identyfikator_WARTOŚĆ;너비값->보이는지=identyfikator_WARTOŚĆ!=1;너비값->너비값=identyfikator_WARTOŚĆ==1?380:220;너비값->wymagane_wysokość_WARTOŚĆ=identyfikator_WARTOŚĆ==1?240:28;너비값->Układ_Policy=1;너비값->współrzędna_X=identyfikator_WARTOŚĆ==1?130:16;너비값->Y_współrzędna=identyfikator_WARTOŚĆ==1?110:16;return 순번+1;}return -28;}
    if(Akcja==5){if(!wpis_ILE_LICZB[właściciel_obiekt])return 0;int 반환값=konkurs_Lista[właściciel_obiekt][첫항목[właściciel_obiekt]];첫항목[właściciel_obiekt]=(첫항목[właściciel_obiekt]+1)%16;wpis_ILE_LICZB[właściciel_obiekt]--;return 반환값;}
    if(Akcja==6)return 화면보임(właściciel_obiekt);
    if(!너비값)return -9;
    int 이전표시=표시됨(właściciel_obiekt,너비값);
    if(Akcja==1){int 바탕너비=보드화면너비(),Tło_wysokość=보드화면높이();if(첫째값<0||SEKUNDA_WARTOŚĆ<0||kod_znaku<1||cel_dane<1||첫째값>바탕너비||SEKUNDA_WARTOŚĆ>Tło_wysokość||kod_znaku>바탕너비-첫째값||cel_dane>Tło_wysokość-SEKUNDA_WARTOŚĆ)return -22;너비값->współrzędna_X=첫째값;너비값->Y_współrzędna=SEKUNDA_WARTOŚĆ;너비값->너비값=kod_znaku;너비값->wymagane_wysokość_WARTOŚĆ=cel_dane;너비값->수동배치=1;}
    else if(Akcja==2){widget_Stan *element_podrzędny=element_WARTOŚĆ(właściciel_obiekt,첫째값);if(!element_podrzędny||element_podrzędny==너비값||element_podrzędny->obszar_WARTOŚĆ==1)return -22;int dane_stanowisko=identyfikator_WARTOŚĆ;for(int 깊이=0;dane_stanowisko&&깊이<32;깊이++){if(dane_stanowisko==첫째값)return -22;widget_Stan *위쪽=element_WARTOŚĆ(właściciel_obiekt,dane_stanowisko);dane_stanowisko=위쪽?위쪽->nadrzędny:0;}element_podrzędny->nadrzędny=identyfikator_WARTOŚĆ;if(!element_podrzędny->수동배치){int 형제요소=0;for(int 순번=0;순번<32;순번++)if(&요소들[właściciel_obiekt][순번]!=element_podrzędny&&요소들[właściciel_obiekt][순번].nadrzędny==identyfikator_WARTOŚĆ)형제요소++;element_podrzędny->Y_współrzędna=16+형제요소*36;}}
    else if(Akcja==3)너비값->보이는지=첫째값!=0;
    else if(Akcja==4)너비값->보이는지=0;
    else if(Akcja==7)너비값->Układ_Policy=첫째값;
    else if(Akcja==8)return 너비값->długość_WARTOŚĆ;
    else if(Akcja==9)return 첫째값>=0&&(unsigned)첫째값<너비값->długość_WARTOŚĆ?너비값->tekst[첫째값]:-22;
    else return -22;
    if(이전표시||표시됨(właściciel_obiekt,너비값))Tablica_Terminal(3);return 0;
}
int 화면글(int właściciel_obiekt,int identyfikator_WARTOŚĆ,const uint32_t *dane,unsigned towar_ILE_LICZB){widget_Stan *너비값=element_WARTOŚĆ(właściciel_obiekt,identyfikator_WARTOŚĆ);if(!너비값)return -9;if(towar_ILE_LICZB>127)return -22;for(unsigned 순번=0;순번<towar_ILE_LICZB;순번++){unsigned kodowanie_znaku=dane[순번];if(kodowanie_znaku>0x10ffff||(kodowanie_znaku>=0xd800&&kodowanie_znaku<=0xdfff))return -22;}for(unsigned 순번=0;순번<towar_ILE_LICZB;순번++)너비값->tekst[순번]=dane[순번];너비값->długość_WARTOŚĆ=towar_ILE_LICZB;if(표시됨(właściciel_obiekt,너비값))Tablica_Terminal(3);return 0;}
