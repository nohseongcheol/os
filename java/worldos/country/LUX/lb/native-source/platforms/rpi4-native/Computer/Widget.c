#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* Small native peer layer for the explicitly supported Swing subset. */
#include <stdint.h>
#include <stddef.h>
extern uintptr_t Board_Pel(uintptr_t,uintptr_t,uintptr_t),Board_Terminal(uintptr_t);
extern void Terminal_Symbol(unsigned,unsigned,unsigned,unsigned,unsigned);
extern void *memset(void *,int,size_t);
typedef struct { int Kategorie_VALUE,부모항목,X_Koordinat,세로좌표,너비값,높이값,보이는지,manuell_Layout,Layout_Richtlinn;unsigned SMS[128],Längt_VALUE; } Widget_Status;
static Widget_Status 요소들[4][32];
static int Wichteg[4],Evenement_Lëscht[4][16];static unsigned 첫항목[4],Agab_COUNT[4],부호없는결과[4],긴부호없는값[4];
static void Evenement(int Besëtzer_Objet,int VALUE){if(Agab_COUNT[Besëtzer_Objet]<16){Evenement_Lëscht[Besëtzer_Objet][(첫항목[Besëtzer_Objet]+Agab_COUNT[Besëtzer_Objet])%16]=VALUE;Agab_COUNT[Besëtzer_Objet]++;}}
static Widget_Status *Element_VALUE(int Besëtzer_Objet,int Identifikateur_VALUE){return Besëtzer_Objet>=0&&Besëtzer_Objet<4&&Identifikateur_VALUE>0&&Identifikateur_VALUE<=32&&요소들[Besëtzer_Objet][Identifikateur_VALUE-1].Kategorie_VALUE?&요소들[Besëtzer_Objet][Identifikateur_VALUE-1]:0;}
static void 사각영역(int X_Koordinat,int 세로좌표,int 너비값,int 높이값,unsigned 색상){보드사각그림(X_Koordinat,세로좌표,너비값,높이값,색상);}
int 화면보임(int Besëtzer_Objet){if(Besëtzer_Objet<0||Besëtzer_Objet>=4)return 0;for(int 순번=0;순번<32;순번++)if(요소들[Besëtzer_Objet][순번].Kategorie_VALUE==1&&요소들[Besëtzer_Objet][순번].보이는지)return 1;return 0;}
void 화면초기화(int Besëtzer_Objet){memset(요소들[Besëtzer_Objet],0,sizeof(요소들[Besëtzer_Objet]));Agab_COUNT[Besëtzer_Objet]=첫항목[Besëtzer_Objet]=Wichteg[Besëtzer_Objet]=긴부호없는값[Besëtzer_Objet]=0;}
static void positionéieren(int Besëtzer_Objet,Widget_Status *너비값,int *X_Koordinat,int *세로좌표){*X_Koordinat=너비값->X_Koordinat;*세로좌표=너비값->세로좌표;int Daten_positionéieren=너비값->부모항목;for(int Element_COUNT=0;Daten_positionéieren&&Element_COUNT<32;Element_COUNT++){Widget_Status *위쪽=Element_VALUE(Besëtzer_Objet,Daten_positionéieren);if(!위쪽)break;*X_Koordinat+=위쪽->X_Koordinat;*세로좌표+=위쪽->세로좌표+(위쪽->Kategorie_VALUE==1?30:0);Daten_positionéieren=위쪽->부모항목;}}
static int 표시됨(int Besëtzer_Objet,Widget_Status *너비값){for(int Element_COUNT=0;Element_COUNT<32;Element_COUNT++){if(!너비값->보이는지)return 0;if(너비값->Kategorie_VALUE==1)return 1;너비값=Element_VALUE(Besëtzer_Objet,너비값->부모항목);if(!너비값)return 0;}return 0;}
static void SMS(int X_Koordinat,int 세로좌표,Widget_Status *너비값,int 최대값,unsigned 색상,unsigned 배경색){int 현재위치=0;for(unsigned 순번=0;순번<너비값->Längt_VALUE;순번++){unsigned Zeechen_Codéierung=너비값->SMS[순번],너비=Zeechen_Codéierung>=256?16:8;if(현재위치+(int)너비>최대값)break;Terminal_Symbol(X_Koordinat+현재위치,세로좌표,Zeechen_Codéierung,색상,배경색);현재위치+=너비;}}
void 화면다시그림(int Besëtzer_Objet){
    if(!화면보임(Besëtzer_Objet))return;
    for(int 처리차례=1;처리차례<=5;처리차례++)for(int 순번=0;순번<32;순번++){
        Widget_Status *너비값=&요소들[Besëtzer_Objet][순번];if(너비값->Kategorie_VALUE!=처리차례||!표시됨(Besëtzer_Objet,너비값))continue;int X_Koordinat,세로좌표;positionéieren(Besëtzer_Objet,너비값,&X_Koordinat,&세로좌표);
        if(처리차례==1){사각영역(X_Koordinat,세로좌표,너비값->너비값,너비값->높이값,0xeee9e0);사각영역(X_Koordinat,세로좌표,너비값->너비값,30,0x905020);SMS(X_Koordinat+10,세로좌표+7,너비값,너비값->너비값-50,0xffffff,0x905020);사각영역(X_Koordinat+너비값->너비값-28,세로좌표+4,24,22,0x5555b8);Terminal_Symbol(X_Koordinat+너비값->너비값-20,세로좌표+7,'X',0xffffff,0x5555b8);}
        if(처리차례==2)사각영역(X_Koordinat,세로좌표,너비값->너비값,너비값->높이값,0xeee9e0);
        if(처리차례>=3){unsigned 배경색=처리차례==4?0xc0ab86:처리차례==5?0xffffff:0xeee9e0;if(처리차례!=3)사각영역(X_Koordinat,세로좌표,너비값->너비값,너비값->높이값,배경색);SMS(X_Koordinat+4,세로좌표+4,너비값,너비값->너비값-8,0x201a15,배경색);if(처리차례==5&&Wichteg[Besëtzer_Objet]==순번+1)사각영역(X_Koordinat,세로좌표+너비값->높이값-2,너비값->너비값,2,0x905020);}
    }
}
int 화면덮음(int Besëtzer_Objet,int X_Koordinat,int 세로좌표){
    if(!화면보임(Besëtzer_Objet))return 0;
    for(int 순번=0;순번<32;순번++){
        Widget_Status *Fënster=&요소들[Besëtzer_Objet][순번];
        if(Fënster->Kategorie_VALUE==1&&Fënster->보이는지&&X_Koordinat>=Fënster->X_Koordinat&&세로좌표>=Fënster->세로좌표&&
           X_Koordinat<Fënster->X_Koordinat+Fënster->너비값&&세로좌표<Fënster->세로좌표+Fënster->높이값)return 1;
    }return 0;
}
int 화면가리킴(int Besëtzer_Objet,unsigned 눌림,int X_Koordinat,int 세로좌표){
    if(!화면보임(Besëtzer_Objet))return 0;
    if(눌림&1)for(int 순번=31;순번>=0;순번--){Widget_Status *너비값=&요소들[Besëtzer_Objet][순번];if(!너비값->Kategorie_VALUE||!표시됨(Besëtzer_Objet,너비값))continue;int 창가로,창세로;positionéieren(Besëtzer_Objet,너비값,&창가로,&창세로);
        if(X_Koordinat<창가로||세로좌표<창세로||X_Koordinat>=창가로+너비값->너비값||세로좌표>=창세로+너비값->높이값)continue;
        if(너비값->Kategorie_VALUE==1&&세로좌표<창세로+30&&X_Koordinat>=창가로+너비값->너비값-28){if(너비값->Layout_Richtlinn!=0)너비값->보이는지=0;Evenement(Besëtzer_Objet,0x10000+순번+1);Board_Terminal(3);return 1;}
        if(너비값->Kategorie_VALUE==4){Evenement(Besëtzer_Objet,순번+1);return 1;}if(너비값->Kategorie_VALUE==5){Wichteg[Besëtzer_Objet]=순번+1;Board_Terminal(3);return 1;}
        if(너비값->Kategorie_VALUE==1)return 1;
    }return 0;
}
void 화면누름(int Besëtzer_Objet,unsigned SECOND_VALUE){
    Widget_Status *너비값=Element_VALUE(Besëtzer_Objet,Wichteg[Besëtzer_Objet]);if(!너비값||너비값->Kategorie_VALUE!=5)return;
    if(SECOND_VALUE==13||SECOND_VALUE==10){Evenement(Besëtzer_Objet,Wichteg[Besëtzer_Objet]);return;}
    if(SECOND_VALUE==8||SECOND_VALUE==127){if(너비값->Längt_VALUE)너비값->Längt_VALUE--;긴부호없는값[Besëtzer_Objet]=0;}
    else{
        unsigned Zeechen_Codéierung=SECOND_VALUE;
        if(긴부호없는값[Besëtzer_Objet]){if((SECOND_VALUE&192)!=128){긴부호없는값[Besëtzer_Objet]=0;return;}부호없는결과[Besëtzer_Objet]=(부호없는결과[Besëtzer_Objet]<<6)|(SECOND_VALUE&63);if(--긴부호없는값[Besëtzer_Objet])return;Zeechen_Codéierung=부호없는결과[Besëtzer_Objet];}
        else if(SECOND_VALUE>=0xc2&&SECOND_VALUE<=0xf4){긴부호없는값[Besëtzer_Objet]=SECOND_VALUE<0xe0?1:SECOND_VALUE<0xf0?2:3;부호없는결과[Besëtzer_Objet]=SECOND_VALUE&((1u<<(6-긴부호없는값[Besëtzer_Objet]))-1);return;}
        else if(SECOND_VALUE<32||SECOND_VALUE>=128)return;
        if(Zeechen_Codéierung>0x10ffff||(Zeechen_Codéierung>=0xd800&&Zeechen_Codéierung<=0xdfff))return;if(너비값->Längt_VALUE<127)너비값->SMS[너비값->Längt_VALUE++]=Zeechen_Codéierung;
    }
    Board_Terminal(3);
}
int 화면호출(int Besëtzer_Objet,unsigned Aktioun,int Identifikateur_VALUE,int 첫째값,int SECOND_VALUE,int Zeechecode,int Zil_Daten){
    if(Besëtzer_Objet<0||Besëtzer_Objet>=4)return -22;Widget_Status *너비값=Element_VALUE(Besëtzer_Objet,Identifikateur_VALUE);
    if(Aktioun==0){if(Identifikateur_VALUE<1||Identifikateur_VALUE>5)return -22;for(int 순번=0;순번<32;순번++)if(요소들[Besëtzer_Objet][순번].Kategorie_VALUE==0){너비값=&요소들[Besëtzer_Objet][순번];memset(너비값,0,sizeof(*너비값));너비값->Kategorie_VALUE=Identifikateur_VALUE;너비값->보이는지=Identifikateur_VALUE!=1;너비값->너비값=Identifikateur_VALUE==1?380:220;너비값->높이값=Identifikateur_VALUE==1?240:28;너비값->Layout_Richtlinn=1;너비값->X_Koordinat=Identifikateur_VALUE==1?130:16;너비값->세로좌표=Identifikateur_VALUE==1?110:16;return 순번+1;}return -28;}
    if(Aktioun==5){if(!Agab_COUNT[Besëtzer_Objet])return 0;int 반환값=Evenement_Lëscht[Besëtzer_Objet][첫항목[Besëtzer_Objet]];첫항목[Besëtzer_Objet]=(첫항목[Besëtzer_Objet]+1)%16;Agab_COUNT[Besëtzer_Objet]--;return 반환값;}
    if(Aktioun==6)return 화면보임(Besëtzer_Objet);
    if(!너비값)return -9;
    int 이전표시=표시됨(Besëtzer_Objet,너비값);
    if(Aktioun==1){int 바탕너비=보드화면너비(),바탕높이=보드화면높이();if(첫째값<0||SECOND_VALUE<0||Zeechecode<1||Zil_Daten<1||첫째값>바탕너비||SECOND_VALUE>바탕높이||Zeechecode>바탕너비-첫째값||Zil_Daten>바탕높이-SECOND_VALUE)return -22;너비값->X_Koordinat=첫째값;너비값->세로좌표=SECOND_VALUE;너비값->너비값=Zeechecode;너비값->높이값=Zil_Daten;너비값->manuell_Layout=1;}
    else if(Aktioun==2){Widget_Status *Kandelement=Element_VALUE(Besëtzer_Objet,첫째값);if(!Kandelement||Kandelement==너비값||Kandelement->Kategorie_VALUE==1)return -22;int Daten_positionéieren=Identifikateur_VALUE;for(int 깊이=0;Daten_positionéieren&&깊이<32;깊이++){if(Daten_positionéieren==첫째값)return -22;Widget_Status *위쪽=Element_VALUE(Besëtzer_Objet,Daten_positionéieren);Daten_positionéieren=위쪽?위쪽->부모항목:0;}Kandelement->부모항목=Identifikateur_VALUE;if(!Kandelement->manuell_Layout){int 형제요소=0;for(int 순번=0;순번<32;순번++)if(&요소들[Besëtzer_Objet][순번]!=Kandelement&&요소들[Besëtzer_Objet][순번].부모항목==Identifikateur_VALUE)형제요소++;Kandelement->세로좌표=16+형제요소*36;}}
    else if(Aktioun==3)너비값->보이는지=첫째값!=0;
    else if(Aktioun==4)너비값->보이는지=0;
    else if(Aktioun==7)너비값->Layout_Richtlinn=첫째값;
    else if(Aktioun==8)return 너비값->Längt_VALUE;
    else if(Aktioun==9)return 첫째값>=0&&(unsigned)첫째값<너비값->Längt_VALUE?너비값->SMS[첫째값]:-22;
    else return -22;
    if(이전표시||표시됨(Besëtzer_Objet,너비값))Board_Terminal(3);return 0;
}
int 화면글(int Besëtzer_Objet,int Identifikateur_VALUE,const uint32_t *Daten,unsigned Element_COUNT){Widget_Status *너비값=Element_VALUE(Besëtzer_Objet,Identifikateur_VALUE);if(!너비값)return -9;if(Element_COUNT>127)return -22;for(unsigned 순번=0;순번<Element_COUNT;순번++){unsigned Zeechen_Codéierung=Daten[순번];if(Zeechen_Codéierung>0x10ffff||(Zeechen_Codéierung>=0xd800&&Zeechen_Codéierung<=0xdfff))return -22;}for(unsigned 순번=0;순번<Element_COUNT;순번++)너비값->SMS[순번]=Daten[순번];너비값->Längt_VALUE=Element_COUNT;if(표시됨(Besëtzer_Objet,너비값))Board_Terminal(3);return 0;}
