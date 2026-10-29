#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* Small native peer layer for the explicitly supported Swing subset. */
#include <stdint.h>
#include <stddef.h>
extern uintptr_t board_pel(uintptr_t,uintptr_t,uintptr_t),board_Terminal(uintptr_t);
extern void Terminal_glyph(unsigned,unsigned,unsigned,unsigned,unsigned);
extern void *memset(void *,int,size_t);
typedef struct { int kategorya_VALUE,부모항목,x_coordinate,Y_button_coordinate,너비값,높이값,보이는지,mano_mano_Layout,Layout_patakaran;unsigned SMS[128],haba_VALUE; } widget_katayuan;
static widget_katayuan 요소들[4][32];
static int Focused[4],kaganapan_list[4][16];static unsigned 첫항목[4],pagpasok_COUNT[4],부호없는결과[4],긴부호없는값[4];
static void kaganapan(int may_ari_bagay,int VALUE){if(pagpasok_COUNT[may_ari_bagay]<16){kaganapan_list[may_ari_bagay][(첫항목[may_ari_bagay]+pagpasok_COUNT[may_ari_bagay])%16]=VALUE;pagpasok_COUNT[may_ari_bagay]++;}}
static widget_katayuan *elemento_VALUE(int may_ari_bagay,int tagakilala_VALUE){return may_ari_bagay>=0&&may_ari_bagay<4&&tagakilala_VALUE>0&&tagakilala_VALUE<=32&&요소들[may_ari_bagay][tagakilala_VALUE-1].kategorya_VALUE?&요소들[may_ari_bagay][tagakilala_VALUE-1]:0;}
static void 사각영역(int x_coordinate,int Y_button_coordinate,int 너비값,int 높이값,unsigned 색상){보드사각그림(x_coordinate,Y_button_coordinate,너비값,높이값,색상);}
int 화면보임(int may_ari_bagay){if(may_ari_bagay<0||may_ari_bagay>=4)return 0;for(int 순번=0;순번<32;순번++)if(요소들[may_ari_bagay][순번].kategorya_VALUE==1&&요소들[may_ari_bagay][순번].보이는지)return 1;return 0;}
void 화면초기화(int may_ari_bagay){memset(요소들[may_ari_bagay],0,sizeof(요소들[may_ari_bagay]));pagpasok_COUNT[may_ari_bagay]=첫항목[may_ari_bagay]=Focused[may_ari_bagay]=긴부호없는값[may_ari_bagay]=0;}
static void posisyon(int may_ari_bagay,widget_katayuan *너비값,int *x_coordinate,int *Y_button_coordinate){*x_coordinate=너비값->x_coordinate;*Y_button_coordinate=너비값->Y_button_coordinate;int data_posisyon=너비값->부모항목;for(int item_COUNT=0;data_posisyon&&item_COUNT<32;item_COUNT++){widget_katayuan *위쪽=elemento_VALUE(may_ari_bagay,data_posisyon);if(!위쪽)break;*x_coordinate+=위쪽->x_coordinate;*Y_button_coordinate+=위쪽->Y_button_coordinate+(위쪽->kategorya_VALUE==1?30:0);data_posisyon=위쪽->부모항목;}}
static int 표시됨(int may_ari_bagay,widget_katayuan *너비값){for(int item_COUNT=0;item_COUNT<32;item_COUNT++){if(!너비값->보이는지)return 0;if(너비값->kategorya_VALUE==1)return 1;너비값=elemento_VALUE(may_ari_bagay,너비값->부모항목);if(!너비값)return 0;}return 0;}
static void SMS(int x_coordinate,int Y_button_coordinate,widget_katayuan *너비값,int 최대값,unsigned 색상,unsigned 배경색){int 현재위치=0;for(unsigned 순번=0;순번<너비값->haba_VALUE;순번++){unsigned karakter_pag_encode=너비값->SMS[순번],너비=karakter_pag_encode>=256?16:8;if(현재위치+(int)너비>최대값)break;Terminal_glyph(x_coordinate+현재위치,Y_button_coordinate,karakter_pag_encode,색상,배경색);현재위치+=너비;}}
void 화면다시그림(int may_ari_bagay){
    if(!화면보임(may_ari_bagay))return;
    for(int 처리차례=1;처리차례<=5;처리차례++)for(int 순번=0;순번<32;순번++){
        widget_katayuan *너비값=&요소들[may_ari_bagay][순번];if(너비값->kategorya_VALUE!=처리차례||!표시됨(may_ari_bagay,너비값))continue;int x_coordinate,Y_button_coordinate;posisyon(may_ari_bagay,너비값,&x_coordinate,&Y_button_coordinate);
        if(처리차례==1){사각영역(x_coordinate,Y_button_coordinate,너비값->너비값,너비값->높이값,0xeee9e0);사각영역(x_coordinate,Y_button_coordinate,너비값->너비값,30,0x905020);SMS(x_coordinate+10,Y_button_coordinate+7,너비값,너비값->너비값-50,0xffffff,0x905020);사각영역(x_coordinate+너비값->너비값-28,Y_button_coordinate+4,24,22,0x5555b8);Terminal_glyph(x_coordinate+너비값->너비값-20,Y_button_coordinate+7,'X',0xffffff,0x5555b8);}
        if(처리차례==2)사각영역(x_coordinate,Y_button_coordinate,너비값->너비값,너비값->높이값,0xeee9e0);
        if(처리차례>=3){unsigned 배경색=처리차례==4?0xc0ab86:처리차례==5?0xffffff:0xeee9e0;if(처리차례!=3)사각영역(x_coordinate,Y_button_coordinate,너비값->너비값,너비값->높이값,배경색);SMS(x_coordinate+4,Y_button_coordinate+4,너비값,너비값->너비값-8,0x201a15,배경색);if(처리차례==5&&Focused[may_ari_bagay]==순번+1)사각영역(x_coordinate,Y_button_coordinate+너비값->높이값-2,너비값->너비값,2,0x905020);}
    }
}
int 화면덮음(int may_ari_bagay,int x_coordinate,int Y_button_coordinate){
    if(!화면보임(may_ari_bagay))return 0;
    for(int 순번=0;순번<32;순번++){
        widget_katayuan *window=&요소들[may_ari_bagay][순번];
        if(window->kategorya_VALUE==1&&window->보이는지&&x_coordinate>=window->x_coordinate&&Y_button_coordinate>=window->Y_button_coordinate&&
           x_coordinate<window->x_coordinate+window->너비값&&Y_button_coordinate<window->Y_button_coordinate+window->높이값)return 1;
    }return 0;
}
int 화면가리킴(int may_ari_bagay,unsigned 눌림,int x_coordinate,int Y_button_coordinate){
    if(!화면보임(may_ari_bagay))return 0;
    if(눌림&1)for(int 순번=31;순번>=0;순번--){widget_katayuan *너비값=&요소들[may_ari_bagay][순번];if(!너비값->kategorya_VALUE||!표시됨(may_ari_bagay,너비값))continue;int window_X_button,window_Y_button;posisyon(may_ari_bagay,너비값,&window_X_button,&window_Y_button);
        if(x_coordinate<window_X_button||Y_button_coordinate<window_Y_button||x_coordinate>=window_X_button+너비값->너비값||Y_button_coordinate>=window_Y_button+너비값->높이값)continue;
        if(너비값->kategorya_VALUE==1&&Y_button_coordinate<window_Y_button+30&&x_coordinate>=window_X_button+너비값->너비값-28){if(너비값->Layout_patakaran!=0)너비값->보이는지=0;kaganapan(may_ari_bagay,0x10000+순번+1);board_Terminal(3);return 1;}
        if(너비값->kategorya_VALUE==4){kaganapan(may_ari_bagay,순번+1);return 1;}if(너비값->kategorya_VALUE==5){Focused[may_ari_bagay]=순번+1;board_Terminal(3);return 1;}
        if(너비값->kategorya_VALUE==1)return 1;
    }return 0;
}
void 화면누름(int may_ari_bagay,unsigned SECOND_VALUE){
    widget_katayuan *너비값=elemento_VALUE(may_ari_bagay,Focused[may_ari_bagay]);if(!너비값||너비값->kategorya_VALUE!=5)return;
    if(SECOND_VALUE==13||SECOND_VALUE==10){kaganapan(may_ari_bagay,Focused[may_ari_bagay]);return;}
    if(SECOND_VALUE==8||SECOND_VALUE==127){if(너비값->haba_VALUE)너비값->haba_VALUE--;긴부호없는값[may_ari_bagay]=0;}
    else{
        unsigned karakter_pag_encode=SECOND_VALUE;
        if(긴부호없는값[may_ari_bagay]){if((SECOND_VALUE&192)!=128){긴부호없는값[may_ari_bagay]=0;return;}부호없는결과[may_ari_bagay]=(부호없는결과[may_ari_bagay]<<6)|(SECOND_VALUE&63);if(--긴부호없는값[may_ari_bagay])return;karakter_pag_encode=부호없는결과[may_ari_bagay];}
        else if(SECOND_VALUE>=0xc2&&SECOND_VALUE<=0xf4){긴부호없는값[may_ari_bagay]=SECOND_VALUE<0xe0?1:SECOND_VALUE<0xf0?2:3;부호없는결과[may_ari_bagay]=SECOND_VALUE&((1u<<(6-긴부호없는값[may_ari_bagay]))-1);return;}
        else if(SECOND_VALUE<32||SECOND_VALUE>=128)return;
        if(karakter_pag_encode>0x10ffff||(karakter_pag_encode>=0xd800&&karakter_pag_encode<=0xdfff))return;if(너비값->haba_VALUE<127)너비값->SMS[너비값->haba_VALUE++]=karakter_pag_encode;
    }
    board_Terminal(3);
}
int 화면호출(int may_ari_bagay,unsigned aksyon,int tagakilala_VALUE,int 첫째값,int SECOND_VALUE,int character_code,int patutunguhan_data){
    if(may_ari_bagay<0||may_ari_bagay>=4)return -22;widget_katayuan *너비값=elemento_VALUE(may_ari_bagay,tagakilala_VALUE);
    if(aksyon==0){if(tagakilala_VALUE<1||tagakilala_VALUE>5)return -22;for(int 순번=0;순번<32;순번++)if(요소들[may_ari_bagay][순번].kategorya_VALUE==0){너비값=&요소들[may_ari_bagay][순번];memset(너비값,0,sizeof(*너비값));너비값->kategorya_VALUE=tagakilala_VALUE;너비값->보이는지=tagakilala_VALUE!=1;너비값->너비값=tagakilala_VALUE==1?380:220;너비값->높이값=tagakilala_VALUE==1?240:28;너비값->Layout_patakaran=1;너비값->x_coordinate=tagakilala_VALUE==1?130:16;너비값->Y_button_coordinate=tagakilala_VALUE==1?110:16;return 순번+1;}return -28;}
    if(aksyon==5){if(!pagpasok_COUNT[may_ari_bagay])return 0;int 반환값=kaganapan_list[may_ari_bagay][첫항목[may_ari_bagay]];첫항목[may_ari_bagay]=(첫항목[may_ari_bagay]+1)%16;pagpasok_COUNT[may_ari_bagay]--;return 반환값;}
    if(aksyon==6)return 화면보임(may_ari_bagay);
    if(!너비값)return -9;
    int 이전표시=표시됨(may_ari_bagay,너비값);
    if(aksyon==1){int 바탕너비=보드화면너비(),바탕높이=보드화면높이();if(첫째값<0||SECOND_VALUE<0||character_code<1||patutunguhan_data<1||첫째값>바탕너비||SECOND_VALUE>바탕높이||character_code>바탕너비-첫째값||patutunguhan_data>바탕높이-SECOND_VALUE)return -22;너비값->x_coordinate=첫째값;너비값->Y_button_coordinate=SECOND_VALUE;너비값->너비값=character_code;너비값->높이값=patutunguhan_data;너비값->mano_mano_Layout=1;}
    else if(aksyon==2){widget_katayuan *sekondaryang_elemento_pangalawang_elemento=elemento_VALUE(may_ari_bagay,첫째값);if(!sekondaryang_elemento_pangalawang_elemento||sekondaryang_elemento_pangalawang_elemento==너비값||sekondaryang_elemento_pangalawang_elemento->kategorya_VALUE==1)return -22;int data_posisyon=tagakilala_VALUE;for(int 깊이=0;data_posisyon&&깊이<32;깊이++){if(data_posisyon==첫째값)return -22;widget_katayuan *위쪽=elemento_VALUE(may_ari_bagay,data_posisyon);data_posisyon=위쪽?위쪽->부모항목:0;}sekondaryang_elemento_pangalawang_elemento->부모항목=tagakilala_VALUE;if(!sekondaryang_elemento_pangalawang_elemento->mano_mano_Layout){int 형제요소=0;for(int 순번=0;순번<32;순번++)if(&요소들[may_ari_bagay][순번]!=sekondaryang_elemento_pangalawang_elemento&&요소들[may_ari_bagay][순번].부모항목==tagakilala_VALUE)형제요소++;sekondaryang_elemento_pangalawang_elemento->Y_button_coordinate=16+형제요소*36;}}
    else if(aksyon==3)너비값->보이는지=첫째값!=0;
    else if(aksyon==4)너비값->보이는지=0;
    else if(aksyon==7)너비값->Layout_patakaran=첫째값;
    else if(aksyon==8)return 너비값->haba_VALUE;
    else if(aksyon==9)return 첫째값>=0&&(unsigned)첫째값<너비값->haba_VALUE?너비값->SMS[첫째값]:-22;
    else return -22;
    if(이전표시||표시됨(may_ari_bagay,너비값))board_Terminal(3);return 0;
}
int 화면글(int may_ari_bagay,int tagakilala_VALUE,const uint32_t *data,unsigned item_COUNT){widget_katayuan *너비값=elemento_VALUE(may_ari_bagay,tagakilala_VALUE);if(!너비값)return -9;if(item_COUNT>127)return -22;for(unsigned 순번=0;순번<item_COUNT;순번++){unsigned karakter_pag_encode=data[순번];if(karakter_pag_encode>0x10ffff||(karakter_pag_encode>=0xd800&&karakter_pag_encode<=0xdfff))return -22;}for(unsigned 순번=0;순번<item_COUNT;순번++)너비값->SMS[순번]=data[순번];너비값->haba_VALUE=item_COUNT;if(표시됨(may_ari_bagay,너비값))board_Terminal(3);return 0;}
