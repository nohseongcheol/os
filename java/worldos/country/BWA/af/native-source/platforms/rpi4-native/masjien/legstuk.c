#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* Small native peer layer for the explicitly supported Swing subset. */
#include <stdint.h>
#include <stddef.h>
extern uintptr_t bord_pieksel(uintptr_t,uintptr_t,uintptr_t),bord_Terminaal(uintptr_t);
extern void Terminaal_glief(unsigned,unsigned,unsigned,unsigned,unsigned);
extern void *memset(void *,int,size_t);
typedef struct { int kategorie_VALUE,부모항목,x_koördinaat,Y_koördinaat,너비값,높이값,보이는지,handmatig_Uitleg,Uitleg_beleid;unsigned Teks[128],lengte_VALUE; } legstuk_stand;
static legstuk_stand 요소들[4][32];
static int Gefokus[4],gebeurtenis_Lys[4][16];static unsigned 첫항목[4],inskrywing_COUNT[4],부호없는결과[4],긴부호없는값[4];
static void gebeurtenis(int eienaar_objek,int VALUE){if(inskrywing_COUNT[eienaar_objek]<16){gebeurtenis_Lys[eienaar_objek][(첫항목[eienaar_objek]+inskrywing_COUNT[eienaar_objek])%16]=VALUE;inskrywing_COUNT[eienaar_objek]++;}}
static legstuk_stand *element_VALUE(int eienaar_objek,int waarde_VALUE){return eienaar_objek>=0&&eienaar_objek<4&&waarde_VALUE>0&&waarde_VALUE<=32&&요소들[eienaar_objek][waarde_VALUE-1].kategorie_VALUE?&요소들[eienaar_objek][waarde_VALUE-1]:0;}
static void 사각영역(int x_koördinaat,int Y_koördinaat,int 너비값,int 높이값,unsigned 색상){보드사각그림(x_koördinaat,Y_koördinaat,너비값,높이값,색상);}
int 화면보임(int eienaar_objek){if(eienaar_objek<0||eienaar_objek>=4)return 0;for(int 순번=0;순번<32;순번++)if(요소들[eienaar_objek][순번].kategorie_VALUE==1&&요소들[eienaar_objek][순번].보이는지)return 1;return 0;}
void 화면초기화(int eienaar_objek){memset(요소들[eienaar_objek],0,sizeof(요소들[eienaar_objek]));inskrywing_COUNT[eienaar_objek]=첫항목[eienaar_objek]=Gefokus[eienaar_objek]=긴부호없는값[eienaar_objek]=0;}
static void Posisie(int eienaar_objek,legstuk_stand *너비값,int *x_koördinaat,int *Y_koördinaat){*x_koördinaat=너비값->x_koördinaat;*Y_koördinaat=너비값->Y_koördinaat;int data_plaas=너비값->부모항목;for(int item_COUNT=0;data_plaas&&item_COUNT<32;item_COUNT++){legstuk_stand *위쪽=element_VALUE(eienaar_objek,data_plaas);if(!위쪽)break;*x_koördinaat+=위쪽->x_koördinaat;*Y_koördinaat+=위쪽->Y_koördinaat+(위쪽->kategorie_VALUE==1?30:0);data_plaas=위쪽->부모항목;}}
static int 표시됨(int eienaar_objek,legstuk_stand *너비값){for(int item_COUNT=0;item_COUNT<32;item_COUNT++){if(!너비값->보이는지)return 0;if(너비값->kategorie_VALUE==1)return 1;너비값=element_VALUE(eienaar_objek,너비값->부모항목);if(!너비값)return 0;}return 0;}
static void Teks(int x_koördinaat,int Y_koördinaat,legstuk_stand *너비값,int 최대값,unsigned 색상,unsigned 배경색){int 현재위치=0;for(unsigned 순번=0;순번<너비값->lengte_VALUE;순번++){unsigned karakter_enkodering=너비값->Teks[순번],너비=karakter_enkodering>=256?16:8;if(현재위치+(int)너비>최대값)break;Terminaal_glief(x_koördinaat+현재위치,Y_koördinaat,karakter_enkodering,색상,배경색);현재위치+=너비;}}
void 화면다시그림(int eienaar_objek){
    if(!화면보임(eienaar_objek))return;
    for(int 처리차례=1;처리차례<=5;처리차례++)for(int 순번=0;순번<32;순번++){
        legstuk_stand *너비값=&요소들[eienaar_objek][순번];if(너비값->kategorie_VALUE!=처리차례||!표시됨(eienaar_objek,너비값))continue;int x_koördinaat,Y_koördinaat;Posisie(eienaar_objek,너비값,&x_koördinaat,&Y_koördinaat);
        if(처리차례==1){사각영역(x_koördinaat,Y_koördinaat,너비값->너비값,너비값->높이값,0xeee9e0);사각영역(x_koördinaat,Y_koördinaat,너비값->너비값,30,0x905020);Teks(x_koördinaat+10,Y_koördinaat+7,너비값,너비값->너비값-50,0xffffff,0x905020);사각영역(x_koördinaat+너비값->너비값-28,Y_koördinaat+4,24,22,0x5555b8);Terminaal_glief(x_koördinaat+너비값->너비값-20,Y_koördinaat+7,'X',0xffffff,0x5555b8);}
        if(처리차례==2)사각영역(x_koördinaat,Y_koördinaat,너비값->너비값,너비값->높이값,0xeee9e0);
        if(처리차례>=3){unsigned 배경색=처리차례==4?0xc0ab86:처리차례==5?0xffffff:0xeee9e0;if(처리차례!=3)사각영역(x_koördinaat,Y_koördinaat,너비값->너비값,너비값->높이값,배경색);Teks(x_koördinaat+4,Y_koördinaat+4,너비값,너비값->너비값-8,0x201a15,배경색);if(처리차례==5&&Gefokus[eienaar_objek]==순번+1)사각영역(x_koördinaat,Y_koördinaat+너비값->높이값-2,너비값->너비값,2,0x905020);}
    }
}
int 화면덮음(int eienaar_objek,int x_koördinaat,int Y_koördinaat){
    if(!화면보임(eienaar_objek))return 0;
    for(int 순번=0;순번<32;순번++){
        legstuk_stand *venster=&요소들[eienaar_objek][순번];
        if(venster->kategorie_VALUE==1&&venster->보이는지&&x_koördinaat>=venster->x_koördinaat&&Y_koördinaat>=venster->Y_koördinaat&&
           x_koördinaat<venster->x_koördinaat+venster->너비값&&Y_koördinaat<venster->Y_koördinaat+venster->높이값)return 1;
    }return 0;
}
int 화면가리킴(int eienaar_objek,unsigned 눌림,int x_koördinaat,int Y_koördinaat){
    if(!화면보임(eienaar_objek))return 0;
    if(눌림&1)for(int 순번=31;순번>=0;순번--){legstuk_stand *너비값=&요소들[eienaar_objek][순번];if(!너비값->kategorie_VALUE||!표시됨(eienaar_objek,너비값))continue;int venster_X,venster_Y;Posisie(eienaar_objek,너비값,&venster_X,&venster_Y);
        if(x_koördinaat<venster_X||Y_koördinaat<venster_Y||x_koördinaat>=venster_X+너비값->너비값||Y_koördinaat>=venster_Y+너비값->높이값)continue;
        if(너비값->kategorie_VALUE==1&&Y_koördinaat<venster_Y+30&&x_koördinaat>=venster_X+너비값->너비값-28){if(너비값->Uitleg_beleid!=0)너비값->보이는지=0;gebeurtenis(eienaar_objek,0x10000+순번+1);bord_Terminaal(3);return 1;}
        if(너비값->kategorie_VALUE==4){gebeurtenis(eienaar_objek,순번+1);return 1;}if(너비값->kategorie_VALUE==5){Gefokus[eienaar_objek]=순번+1;bord_Terminaal(3);return 1;}
        if(너비값->kategorie_VALUE==1)return 1;
    }return 0;
}
void 화면누름(int eienaar_objek,unsigned SECOND_VALUE){
    legstuk_stand *너비값=element_VALUE(eienaar_objek,Gefokus[eienaar_objek]);if(!너비값||너비값->kategorie_VALUE!=5)return;
    if(SECOND_VALUE==13||SECOND_VALUE==10){gebeurtenis(eienaar_objek,Gefokus[eienaar_objek]);return;}
    if(SECOND_VALUE==8||SECOND_VALUE==127){if(너비값->lengte_VALUE)너비값->lengte_VALUE--;긴부호없는값[eienaar_objek]=0;}
    else{
        unsigned karakter_enkodering=SECOND_VALUE;
        if(긴부호없는값[eienaar_objek]){if((SECOND_VALUE&192)!=128){긴부호없는값[eienaar_objek]=0;return;}부호없는결과[eienaar_objek]=(부호없는결과[eienaar_objek]<<6)|(SECOND_VALUE&63);if(--긴부호없는값[eienaar_objek])return;karakter_enkodering=부호없는결과[eienaar_objek];}
        else if(SECOND_VALUE>=0xc2&&SECOND_VALUE<=0xf4){긴부호없는값[eienaar_objek]=SECOND_VALUE<0xe0?1:SECOND_VALUE<0xf0?2:3;부호없는결과[eienaar_objek]=SECOND_VALUE&((1u<<(6-긴부호없는값[eienaar_objek]))-1);return;}
        else if(SECOND_VALUE<32||SECOND_VALUE>=128)return;
        if(karakter_enkodering>0x10ffff||(karakter_enkodering>=0xd800&&karakter_enkodering<=0xdfff))return;if(너비값->lengte_VALUE<127)너비값->Teks[너비값->lengte_VALUE++]=karakter_enkodering;
    }
    bord_Terminaal(3);
}
int 화면호출(int eienaar_objek,unsigned Aksie,int waarde_VALUE,int 첫째값,int SECOND_VALUE,int karakterkode,int bestemming_data){
    if(eienaar_objek<0||eienaar_objek>=4)return -22;legstuk_stand *너비값=element_VALUE(eienaar_objek,waarde_VALUE);
    if(Aksie==0){if(waarde_VALUE<1||waarde_VALUE>5)return -22;for(int 순번=0;순번<32;순번++)if(요소들[eienaar_objek][순번].kategorie_VALUE==0){너비값=&요소들[eienaar_objek][순번];memset(너비값,0,sizeof(*너비값));너비값->kategorie_VALUE=waarde_VALUE;너비값->보이는지=waarde_VALUE!=1;너비값->너비값=waarde_VALUE==1?380:220;너비값->높이값=waarde_VALUE==1?240:28;너비값->Uitleg_beleid=1;너비값->x_koördinaat=waarde_VALUE==1?130:16;너비값->Y_koördinaat=waarde_VALUE==1?110:16;return 순번+1;}return -28;}
    if(Aksie==5){if(!inskrywing_COUNT[eienaar_objek])return 0;int 반환값=gebeurtenis_Lys[eienaar_objek][첫항목[eienaar_objek]];첫항목[eienaar_objek]=(첫항목[eienaar_objek]+1)%16;inskrywing_COUNT[eienaar_objek]--;return 반환값;}
    if(Aksie==6)return 화면보임(eienaar_objek);
    if(!너비값)return -9;
    int 이전표시=표시됨(eienaar_objek,너비값);
    if(Aksie==1){int 바탕너비=보드화면너비(),바탕높이=보드화면높이();if(첫째값<0||SECOND_VALUE<0||karakterkode<1||bestemming_data<1||첫째값>바탕너비||SECOND_VALUE>바탕높이||karakterkode>바탕너비-첫째값||bestemming_data>바탕높이-SECOND_VALUE)return -22;너비값->x_koördinaat=첫째값;너비값->Y_koördinaat=SECOND_VALUE;너비값->너비값=karakterkode;너비값->높이값=bestemming_data;너비값->handmatig_Uitleg=1;}
    else if(Aksie==2){legstuk_stand *kindelement=element_VALUE(eienaar_objek,첫째값);if(!kindelement||kindelement==너비값||kindelement->kategorie_VALUE==1)return -22;int data_plaas=waarde_VALUE;for(int 깊이=0;data_plaas&&깊이<32;깊이++){if(data_plaas==첫째값)return -22;legstuk_stand *위쪽=element_VALUE(eienaar_objek,data_plaas);data_plaas=위쪽?위쪽->부모항목:0;}kindelement->부모항목=waarde_VALUE;if(!kindelement->handmatig_Uitleg){int 형제요소=0;for(int 순번=0;순번<32;순번++)if(&요소들[eienaar_objek][순번]!=kindelement&&요소들[eienaar_objek][순번].부모항목==waarde_VALUE)형제요소++;kindelement->Y_koördinaat=16+형제요소*36;}}
    else if(Aksie==3)너비값->보이는지=첫째값!=0;
    else if(Aksie==4)너비값->보이는지=0;
    else if(Aksie==7)너비값->Uitleg_beleid=첫째값;
    else if(Aksie==8)return 너비값->lengte_VALUE;
    else if(Aksie==9)return 첫째값>=0&&(unsigned)첫째값<너비값->lengte_VALUE?너비값->Teks[첫째값]:-22;
    else return -22;
    if(이전표시||표시됨(eienaar_objek,너비값))bord_Terminaal(3);return 0;
}
int 화면글(int eienaar_objek,int waarde_VALUE,const uint32_t *data,unsigned item_COUNT){legstuk_stand *너비값=element_VALUE(eienaar_objek,waarde_VALUE);if(!너비값)return -9;if(item_COUNT>127)return -22;for(unsigned 순번=0;순번<item_COUNT;순번++){unsigned karakter_enkodering=data[순번];if(karakter_enkodering>0x10ffff||(karakter_enkodering>=0xd800&&karakter_enkodering<=0xdfff))return -22;}for(unsigned 순번=0;순번<item_COUNT;순번++)너비값->Teks[순번]=data[순번];너비값->lengte_VALUE=item_COUNT;if(표시됨(eienaar_objek,너비값))bord_Terminaal(3);return 0;}
