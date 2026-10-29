#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* Small native peer layer for the explicitly supported Swing subset. */
#include <stdint.h>
#include <stddef.h>
extern uintptr_t Avizier_element_imagine(uintptr_t,uintptr_t,uintptr_t),Avizier_Terminal(uintptr_t);
extern void Terminal_glifă(unsigned,unsigned,unsigned,unsigned,unsigned);
extern void *memset(void *,int,size_t);
typedef struct { int zonă_VALUE,părinte,coordonata_X,세로좌표,너비값,높이값,보이는지,manual_Aspect,Aspect_Policy;unsigned SMS[128],lungime_VALUE; } widget_Stare;
static widget_Stare 요소들[4][32];
static int Prioritare[4],eveniment_Listă[4][16];static unsigned 첫항목[4],intrare_COUNT[4],부호없는결과[4],긴부호없는값[4];
static void Eveniment(int proprietar_obiect,int VALUE){if(intrare_COUNT[proprietar_obiect]<16){eveniment_Listă[proprietar_obiect][(첫항목[proprietar_obiect]+intrare_COUNT[proprietar_obiect])%16]=VALUE;intrare_COUNT[proprietar_obiect]++;}}
static widget_Stare *element_VALUE(int proprietar_obiect,int identificator_VALUE){return proprietar_obiect>=0&&proprietar_obiect<4&&identificator_VALUE>0&&identificator_VALUE<=32&&요소들[proprietar_obiect][identificator_VALUE-1].zonă_VALUE?&요소들[proprietar_obiect][identificator_VALUE-1]:0;}
static void 사각영역(int coordonata_X,int 세로좌표,int 너비값,int 높이값,unsigned 색상){Avizier_dreptunghi_umple(coordonata_X,세로좌표,너비값,높이값,색상);}
int 화면보임(int proprietar_obiect){if(proprietar_obiect<0||proprietar_obiect>=4)return 0;for(int 순번=0;순번<32;순번++)if(요소들[proprietar_obiect][순번].zonă_VALUE==1&&요소들[proprietar_obiect][순번].보이는지)return 1;return 0;}
void 화면초기화(int proprietar_obiect){memset(요소들[proprietar_obiect],0,sizeof(요소들[proprietar_obiect]));intrare_COUNT[proprietar_obiect]=첫항목[proprietar_obiect]=Prioritare[proprietar_obiect]=긴부호없는값[proprietar_obiect]=0;}
static void Poziție(int proprietar_obiect,widget_Stare *너비값,int *coordonata_X,int *세로좌표){*coordonata_X=너비값->coordonata_X;*세로좌표=너비값->세로좌표;int date_poziție=너비값->părinte;for(int element_COUNT=0;date_poziție&&element_COUNT<32;element_COUNT++){widget_Stare *위쪽=element_VALUE(proprietar_obiect,date_poziție);if(!위쪽)break;*coordonata_X+=위쪽->coordonata_X;*세로좌표+=위쪽->세로좌표+(위쪽->zonă_VALUE==1?30:0);date_poziție=위쪽->părinte;}}
static int 표시됨(int proprietar_obiect,widget_Stare *너비값){for(int element_COUNT=0;element_COUNT<32;element_COUNT++){if(!너비값->보이는지)return 0;if(너비값->zonă_VALUE==1)return 1;너비값=element_VALUE(proprietar_obiect,너비값->părinte);if(!너비값)return 0;}return 0;}
static void SMS(int coordonata_X,int 세로좌표,widget_Stare *너비값,int 최대값,unsigned 색상,unsigned 배경색){int curent_poziție=0;for(unsigned 순번=0;순번<너비값->lungime_VALUE;순번++){unsigned codificare_caractere=너비값->SMS[순번],너비=codificare_caractere>=256?16:8;if(curent_poziție+(int)너비>최대값)break;Terminal_glifă(coordonata_X+curent_poziție,세로좌표,codificare_caractere,색상,배경색);curent_poziție+=너비;}}
void 화면다시그림(int proprietar_obiect){
    if(!화면보임(proprietar_obiect))return;
    for(int procesare_ordine=1;procesare_ordine<=5;procesare_ordine++)for(int 순번=0;순번<32;순번++){
        widget_Stare *너비값=&요소들[proprietar_obiect][순번];if(너비값->zonă_VALUE!=procesare_ordine||!표시됨(proprietar_obiect,너비값))continue;int coordonata_X,세로좌표;Poziție(proprietar_obiect,너비값,&coordonata_X,&세로좌표);
        if(procesare_ordine==1){사각영역(coordonata_X,세로좌표,너비값->너비값,너비값->높이값,0xeee9e0);사각영역(coordonata_X,세로좌표,너비값->너비값,30,0x905020);SMS(coordonata_X+10,세로좌표+7,너비값,너비값->너비값-50,0xffffff,0x905020);사각영역(coordonata_X+너비값->너비값-28,세로좌표+4,24,22,0x5555b8);Terminal_glifă(coordonata_X+너비값->너비값-20,세로좌표+7,'X',0xffffff,0x5555b8);}
        if(procesare_ordine==2)사각영역(coordonata_X,세로좌표,너비값->너비값,너비값->높이값,0xeee9e0);
        if(procesare_ordine>=3){unsigned 배경색=procesare_ordine==4?0xc0ab86:procesare_ordine==5?0xffffff:0xeee9e0;if(procesare_ordine!=3)사각영역(coordonata_X,세로좌표,너비값->너비값,너비값->높이값,배경색);SMS(coordonata_X+4,세로좌표+4,너비값,너비값->너비값-8,0x201a15,배경색);if(procesare_ordine==5&&Prioritare[proprietar_obiect]==순번+1)사각영역(coordonata_X,세로좌표+너비값->높이값-2,너비값->너비값,2,0x905020);}
    }
}
int 화면덮음(int proprietar_obiect,int coordonata_X,int 세로좌표){
    if(!화면보임(proprietar_obiect))return 0;
    for(int 순번=0;순번<32;순번++){
        widget_Stare *Fereastră=&요소들[proprietar_obiect][순번];
        if(Fereastră->zonă_VALUE==1&&Fereastră->보이는지&&coordonata_X>=Fereastră->coordonata_X&&세로좌표>=Fereastră->세로좌표&&
           coordonata_X<Fereastră->coordonata_X+Fereastră->너비값&&세로좌표<Fereastră->세로좌표+Fereastră->높이값)return 1;
    }return 0;
}
int 화면가리킴(int proprietar_obiect,unsigned 눌림,int coordonata_X,int 세로좌표){
    if(!화면보임(proprietar_obiect))return 0;
    if(눌림&1)for(int 순번=31;순번>=0;순번--){widget_Stare *너비값=&요소들[proprietar_obiect][순번];if(!너비값->zonă_VALUE||!표시됨(proprietar_obiect,너비값))continue;int fereastră_X,fereastră_Y;Poziție(proprietar_obiect,너비값,&fereastră_X,&fereastră_Y);
        if(coordonata_X<fereastră_X||세로좌표<fereastră_Y||coordonata_X>=fereastră_X+너비값->너비값||세로좌표>=fereastră_Y+너비값->높이값)continue;
        if(너비값->zonă_VALUE==1&&세로좌표<fereastră_Y+30&&coordonata_X>=fereastră_X+너비값->너비값-28){if(너비값->Aspect_Policy!=0)너비값->보이는지=0;Eveniment(proprietar_obiect,0x10000+순번+1);Avizier_Terminal(3);return 1;}
        if(너비값->zonă_VALUE==4){Eveniment(proprietar_obiect,순번+1);return 1;}if(너비값->zonă_VALUE==5){Prioritare[proprietar_obiect]=순번+1;Avizier_Terminal(3);return 1;}
        if(너비값->zonă_VALUE==1)return 1;
    }return 0;
}
void 화면누름(int proprietar_obiect,unsigned SECOND_VALUE){
    widget_Stare *너비값=element_VALUE(proprietar_obiect,Prioritare[proprietar_obiect]);if(!너비값||너비값->zonă_VALUE!=5)return;
    if(SECOND_VALUE==13||SECOND_VALUE==10){Eveniment(proprietar_obiect,Prioritare[proprietar_obiect]);return;}
    if(SECOND_VALUE==8||SECOND_VALUE==127){if(너비값->lungime_VALUE)너비값->lungime_VALUE--;긴부호없는값[proprietar_obiect]=0;}
    else{
        unsigned codificare_caractere=SECOND_VALUE;
        if(긴부호없는값[proprietar_obiect]){if((SECOND_VALUE&192)!=128){긴부호없는값[proprietar_obiect]=0;return;}부호없는결과[proprietar_obiect]=(부호없는결과[proprietar_obiect]<<6)|(SECOND_VALUE&63);if(--긴부호없는값[proprietar_obiect])return;codificare_caractere=부호없는결과[proprietar_obiect];}
        else if(SECOND_VALUE>=0xc2&&SECOND_VALUE<=0xf4){긴부호없는값[proprietar_obiect]=SECOND_VALUE<0xe0?1:SECOND_VALUE<0xf0?2:3;부호없는결과[proprietar_obiect]=SECOND_VALUE&((1u<<(6-긴부호없는값[proprietar_obiect]))-1);return;}
        else if(SECOND_VALUE<32||SECOND_VALUE>=128)return;
        if(codificare_caractere>0x10ffff||(codificare_caractere>=0xd800&&codificare_caractere<=0xdfff))return;if(너비값->lungime_VALUE<127)너비값->SMS[너비값->lungime_VALUE++]=codificare_caractere;
    }
    Avizier_Terminal(3);
}
int 화면호출(int proprietar_obiect,unsigned Acțiuni,int identificator_VALUE,int 첫째값,int SECOND_VALUE,int cod_caracter,int destinație_date){
    if(proprietar_obiect<0||proprietar_obiect>=4)return -22;widget_Stare *너비값=element_VALUE(proprietar_obiect,identificator_VALUE);
    if(Acțiuni==0){if(identificator_VALUE<1||identificator_VALUE>5)return -22;for(int 순번=0;순번<32;순번++)if(요소들[proprietar_obiect][순번].zonă_VALUE==0){너비값=&요소들[proprietar_obiect][순번];memset(너비값,0,sizeof(*너비값));너비값->zonă_VALUE=identificator_VALUE;너비값->보이는지=identificator_VALUE!=1;너비값->너비값=identificator_VALUE==1?380:220;너비값->높이값=identificator_VALUE==1?240:28;너비값->Aspect_Policy=1;너비값->coordonata_X=identificator_VALUE==1?130:16;너비값->세로좌표=identificator_VALUE==1?110:16;return 순번+1;}return -28;}
    if(Acțiuni==5){if(!intrare_COUNT[proprietar_obiect])return 0;int 반환값=eveniment_Listă[proprietar_obiect][첫항목[proprietar_obiect]];첫항목[proprietar_obiect]=(첫항목[proprietar_obiect]+1)%16;intrare_COUNT[proprietar_obiect]--;return 반환값;}
    if(Acțiuni==6)return 화면보임(proprietar_obiect);
    if(!너비값)return -9;
    int 이전표시=표시됨(proprietar_obiect,너비값);
    if(Acțiuni==1){int 바탕너비=보드화면너비(),바탕높이=보드화면높이();if(첫째값<0||SECOND_VALUE<0||cod_caracter<1||destinație_date<1||첫째값>바탕너비||SECOND_VALUE>바탕높이||cod_caracter>바탕너비-첫째값||destinație_date>바탕높이-SECOND_VALUE)return -22;너비값->coordonata_X=첫째값;너비값->세로좌표=SECOND_VALUE;너비값->너비값=cod_caracter;너비값->높이값=destinație_date;너비값->manual_Aspect=1;}
    else if(Acțiuni==2){widget_Stare *descendent=element_VALUE(proprietar_obiect,첫째값);if(!descendent||descendent==너비값||descendent->zonă_VALUE==1)return -22;int date_poziție=identificator_VALUE;for(int 깊이=0;date_poziție&&깊이<32;깊이++){if(date_poziție==첫째값)return -22;widget_Stare *위쪽=element_VALUE(proprietar_obiect,date_poziție);date_poziție=위쪽?위쪽->părinte:0;}descendent->părinte=identificator_VALUE;if(!descendent->manual_Aspect){int 형제요소=0;for(int 순번=0;순번<32;순번++)if(&요소들[proprietar_obiect][순번]!=descendent&&요소들[proprietar_obiect][순번].părinte==identificator_VALUE)형제요소++;descendent->세로좌표=16+형제요소*36;}}
    else if(Acțiuni==3)너비값->보이는지=첫째값!=0;
    else if(Acțiuni==4)너비값->보이는지=0;
    else if(Acțiuni==7)너비값->Aspect_Policy=첫째값;
    else if(Acțiuni==8)return 너비값->lungime_VALUE;
    else if(Acțiuni==9)return 첫째값>=0&&(unsigned)첫째값<너비값->lungime_VALUE?너비값->SMS[첫째값]:-22;
    else return -22;
    if(이전표시||표시됨(proprietar_obiect,너비값))Avizier_Terminal(3);return 0;
}
int 화면글(int proprietar_obiect,int identificator_VALUE,const uint32_t *date,unsigned element_COUNT){widget_Stare *너비값=element_VALUE(proprietar_obiect,identificator_VALUE);if(!너비값)return -9;if(element_COUNT>127)return -22;for(unsigned 순번=0;순번<element_COUNT;순번++){unsigned codificare_caractere=date[순번];if(codificare_caractere>0x10ffff||(codificare_caractere>=0xd800&&codificare_caractere<=0xdfff))return -22;}for(unsigned 순번=0;순번<element_COUNT;순번++)너비값->SMS[순번]=date[순번];너비값->lungime_VALUE=element_COUNT;if(표시됨(proprietar_obiect,너비값))Avizier_Terminal(3);return 0;}
