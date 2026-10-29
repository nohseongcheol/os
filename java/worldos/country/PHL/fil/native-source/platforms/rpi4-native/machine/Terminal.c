#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* 자체 네 window 합성과 UTF-8 Terminal. 바뀐 영역의 완성 그림만 표시한다. */
#include <stdint.h>
#include <stddef.h>
typedef uintptr_t machine_Word;
extern machine_Word board_pel(machine_Word,machine_Word,machine_Word),보드화면기억공간(void);
extern void *memset(void *,int,size_t);
extern const unsigned char Terminal_font[];
#define 최대열수 237
#define Kasaysayan_linya_COUNT 160
typedef struct {
    uint32_t 글자칸들[Kasaysayan_linya_COUNT][최대열수]; uint8_t 모양들[Kasaysayan_linya_COUNT][최대열수];
    unsigned 너비,높이,COLUMNS,ROW_COUNT,크기바뀜;
    unsigned 살아있음,x_coordinate,Y_button_coordinate,ROW_posisyon,kolum_posisyon,맨위,iskrol,전경색,배경색,탈출상태,parameter_VALUE[4],parameter_INDEX,저장행,저장열;
    unsigned 부호없는결과,긴부호없는값,SMALL_VALUE,대체화면,가리개보임;
} Terminal_d413d4bc;
static Terminal_d413d4bc Windows_list[4];
static int Focus=-1,출력결과,pagkakasunud_sunod_VALUE[4],pagpasok_COUNT,mag_drag_VALUE=-1,mag_drag_X_button,mag_drag_Y_button;
static unsigned information_technology_pending,단추들,desktop_View,한글입력;
static const uint32_t 색상들[16]={0x201a15,0x6060df,0x9dcc86,0x80cfea,0xefaf72,0xca96c9,0xceda76,0xede9df,0x858078,0x8888ff,0xb9eba7,0xa5eaff,0xffcc99,0xf0bef1,0xf0f0a0,0xffffff};
extern int 화면보임(int),화면가리킴(int,unsigned,int,int);
extern void 화면다시그림(int);
static Terminal_d413d4bc *Terminal_pagpasok;
static unsigned 넓은글자(unsigned character_code){return character_code>=256?2:1;}
static void 사각영역(unsigned x_coordinate,unsigned Y_button_coordinate,unsigned 너비값,unsigned 높이값,unsigned 색상){
    보드사각그림(x_coordinate,Y_button_coordinate,너비값,높이값,색상);
}
void Terminal_glyph(unsigned x_coordinate,unsigned Y_button_coordinate,unsigned character_code,unsigned 전경색,unsigned 배경색){
    unsigned 너비=넓은글자(character_code)*8;if(character_code==0xffffffffu)return;
    int 왼쪽=x_coordinate,위쪽=Y_button_coordinate,폭=너비,haba_VALUE=16;
    if(!보드그림범위(&왼쪽,&위쪽,&폭,&haba_VALUE))return;
    if(character_code==' '){보드사각그림(왼쪽,위쪽,폭,haba_VALUE,배경색);return;}
    unsigned LOOKUP_INDEX=character_code<65536?character_code:character_code>=0x1f600&&character_code<0x1f650?65536+character_code-0x1f600:0xfffd;
    const unsigned char *font_VALUE=Terminal_font+LOOKUP_INDEX*32;
    for(int linya=위쪽;linya<위쪽+haba_VALUE;linya++){unsigned Background_Intelligent_Transfer_Service_list=font_VALUE[(linya-Y_button_coordinate)*2]*256+font_VALUE[(linya-Y_button_coordinate)*2+1];for(int espasyo_pagpasok=왼쪽;espasyo_pagpasok<왼쪽+폭;espasyo_pagpasok++)board_pel(espasyo_pagpasok,linya,(Background_Intelligent_Transfer_Service_list&(0x8000>>(espasyo_pagpasok-x_coordinate)))?전경색:배경색);}
}
static void pangalan_talahanayan(unsigned x_coordinate,unsigned Y_button_coordinate,const char *string_data,unsigned 전경색,unsigned 배경색){while(*string_data){unsigned character_code=(unsigned char)*string_data++, 남은수=0;if(character_code>=0xc0){남은수=character_code<0xe0?1:character_code<0xf0?2:3;character_code&=(1u<<(6-남은수))-1;while(남은수--&&*string_data)character_code=(character_code<<6)|((unsigned char)*string_data++&63);}Terminal_glyph(x_coordinate,Y_button_coordinate,character_code,전경색,배경색);x_coordinate+=넓은글자(character_code)*8;}}
static unsigned 첫항목(void){return Terminal_pagpasok->맨위;}
static int 보이는지(void){return Terminal_pagpasok->살아있음&&Focus>=0&&Terminal_pagpasok==&Windows_list[Focus]&&!화면보임(Focus);}
static void 그리기(unsigned ROW_posisyon,unsigned kolum_posisyon){
    if(!보이는지()||ROW_posisyon<첫항목()-Terminal_pagpasok->iskrol||ROW_posisyon>=첫항목()-Terminal_pagpasok->iskrol+Terminal_pagpasok->ROW_COUNT||kolum_posisyon>=Terminal_pagpasok->COLUMNS)return;
    unsigned character_code=Terminal_pagpasok->글자칸들[ROW_posisyon%Kasaysayan_linya_COUNT][kolum_posisyon],string_data=Terminal_pagpasok->모양들[ROW_posisyon%Kasaysayan_linya_COUNT][kolum_posisyon];
    if(넓은글자(character_code)==2&&kolum_posisyon+1>=Terminal_pagpasok->COLUMNS)character_code=' ';
    Terminal_glyph(Terminal_pagpasok->x_coordinate+12+kolum_posisyon*8,Terminal_pagpasok->Y_button_coordinate+36+(ROW_posisyon-첫항목()+Terminal_pagpasok->iskrol)*16,character_code?character_code:' ',색상들[string_data&15],색상들[string_data>>4]);
}
static void caret_VALUE(int ipakita_window){if(!보이는지()||Terminal_pagpasok->iskrol||Terminal_pagpasok->kolum_posisyon>=Terminal_pagpasok->COLUMNS||Terminal_pagpasok->ROW_posisyon<Terminal_pagpasok->맨위||Terminal_pagpasok->ROW_posisyon>=Terminal_pagpasok->맨위+Terminal_pagpasok->ROW_COUNT)return;
    if(!ipakita_window||!Terminal_pagpasok->가리개보임)그리기(Terminal_pagpasok->ROW_posisyon,Terminal_pagpasok->kolum_posisyon);else 사각영역(Terminal_pagpasok->x_coordinate+12+Terminal_pagpasok->kolum_posisyon*8,Terminal_pagpasok->Y_button_coordinate+36+(Terminal_pagpasok->ROW_posisyon-Terminal_pagpasok->맨위)*16+14,8,2,색상들[Terminal_pagpasok->전경색]);}
static void Nilalaman_VALUE(void){
    사각영역(Terminal_pagpasok->x_coordinate+12,Terminal_pagpasok->Y_button_coordinate+36,Terminal_pagpasok->COLUMNS*8,Terminal_pagpasok->ROW_COUNT*16,색상들[0]);
    int 가로=Terminal_pagpasok->x_coordinate+12,archive_posisyon=Terminal_pagpasok->Y_button_coordinate+36,폭=Terminal_pagpasok->COLUMNS*8,haba_VALUE=Terminal_pagpasok->ROW_COUNT*16;
    if(보드그림범위(&가로,&archive_posisyon,&폭,&haba_VALUE)){
    unsigned 첫줄=(archive_posisyon-Terminal_pagpasok->Y_button_coordinate-36)/16,끝줄=(archive_posisyon+haba_VALUE-Terminal_pagpasok->Y_button_coordinate-36+15)/16;
    unsigned 첫칸=(가로-Terminal_pagpasok->x_coordinate-12)/8,끝칸=(가로+폭-Terminal_pagpasok->x_coordinate-12+7)/8;
    if(첫칸)첫칸--; /* 잘림 경계 왼쪽에서 시작한 두 espasyo_pagpasok 글자도 그린다. */
    for(unsigned 반환값=첫줄;반환값<끝줄;반환값++)for(unsigned character_code=첫칸;character_code<끝칸;character_code++){
        unsigned ROW_posisyon=첫항목()-Terminal_pagpasok->iskrol+반환값,karakter_VALUE=Terminal_pagpasok->글자칸들[ROW_posisyon%Kasaysayan_linya_COUNT][character_code],string_data=Terminal_pagpasok->모양들[ROW_posisyon%Kasaysayan_linya_COUNT][character_code];
        if(넓은글자(karakter_VALUE)==2&&character_code+1>=Terminal_pagpasok->COLUMNS)karakter_VALUE=' ';
        if((karakter_VALUE==0||karakter_VALUE==' ')&&(string_data>>4)==0)continue;
        Terminal_glyph(Terminal_pagpasok->x_coordinate+12+character_code*8,Terminal_pagpasok->Y_button_coordinate+36+반환값*16,karakter_VALUE?karakter_VALUE:' ',색상들[string_data&15],색상들[string_data>>4]);
    }}
    pangalan_talahanayan(Terminal_pagpasok->x_coordinate+12,Terminal_pagpasok->Y_button_coordinate+Terminal_pagpasok->높이-18,Terminal_pagpasok->iskrol?"PgDn: recent output":Terminal_pagpasok->너비>=500?"F6: next | Corner + left drag: resize":"Corner + left drag: resize",0xece8e2,0x403127);caret_VALUE(1);
}
static void 실행틀(int tagakilala_VALUE){
    Terminal_pagpasok=&Windows_list[tagakilala_VALUE];
    int 가로=Terminal_pagpasok->x_coordinate,archive_posisyon=Terminal_pagpasok->Y_button_coordinate,폭=Terminal_pagpasok->너비,haba_VALUE=Terminal_pagpasok->높이;
    if(!보드그림범위(&가로,&archive_posisyon,&폭,&haba_VALUE))return;
    사각영역(Terminal_pagpasok->x_coordinate,Terminal_pagpasok->Y_button_coordinate,Terminal_pagpasok->너비,Terminal_pagpasok->높이,0x403127);
    unsigned 색상=tagakilala_VALUE==Focus?0x905020:0x604438;사각영역(Terminal_pagpasok->x_coordinate,Terminal_pagpasok->Y_button_coordinate,Terminal_pagpasok->너비,30,색상);
    pangalan_talahanayan(Terminal_pagpasok->x_coordinate+12,Terminal_pagpasok->Y_button_coordinate+7,"JKOROS Terminal",0xffffff,색상);
    char 수치[2]={(char)('1'+tagakilala_VALUE),0};pangalan_talahanayan(Terminal_pagpasok->x_coordinate+148,Terminal_pagpasok->Y_button_coordinate+7,수치,0xffffff,색상);
    pangalan_talahanayan(Terminal_pagpasok->x_coordinate+240,Terminal_pagpasok->Y_button_coordinate+7,Terminal_pagpasok->너비>=500?(한글입력?"[FIL] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[FIL]":"[EN]"),0xffffff,색상);
    사각영역(Terminal_pagpasok->x_coordinate+Terminal_pagpasok->너비-32,Terminal_pagpasok->Y_button_coordinate+4,26,22,0x5555b8);pangalan_talahanayan(Terminal_pagpasok->x_coordinate+Terminal_pagpasok->너비-24,Terminal_pagpasok->Y_button_coordinate+7,"X",0xffffff,0x5555b8);
    Nilalaman_VALUE();
}
static void 장면그리기(void){
    if(!desktop_View)return;사각영역(0,0,보드화면너비(),보드화면높이(),0x302018);사각영역(0,0,보드화면너비(),32,0x403127);
    사각영역(6,4,136,24,0x905020);pangalan_talahanayan(14,8,"+ New terminal",0xffffff,0x905020);
    for(int 순번=0;순번<4;순번++)if(Windows_list[순번].살아있음){unsigned character_code=Focus==순번?0x905020:0x604438;사각영역(154+순번*112,4,106,24,character_code);pangalan_talahanayan(160+순번*112,8,"Terminal",0xffffff,character_code);char string_data[2]={(char)('1'+순번),0};pangalan_talahanayan(232+순번*112,8,string_data,0xffffff,character_code);}
    if(!pagpasok_COUNT)pangalan_talahanayan(140,210,"Click + New terminal to start",0xede9df,0x302018);
    for(int 순번=0;순번<pagpasok_COUNT;순번++)실행틀(pagkakasunud_sunod_VALUE[순번]);화면다시그림(Focus);Terminal_pagpasok=&Windows_list[출력결과];
}
static void 영역그리기(int 가로,int archive_posisyon,int 폭,int haba_VALUE){
    if(!desktop_View||!보드그림범위(&가로,&archive_posisyon,&폭,&haba_VALUE))return;
    for(int linya=archive_posisyon;linya<archive_posisyon+haba_VALUE;linya+=32){
        int 띠높이=archive_posisyon+haba_VALUE-linya;if(띠높이>32)띠높이=32;
        if(board_Start_iginuhit(가로,linya,폭,띠높이)){장면그리기();board_Tapos_Na_iginuhit();}
    }
}
static void 다시그리기(void){영역그리기(0,0,보드화면너비(),보드화면높이());}
/* 서로 겹치지 않는 새 window 영역과 이전 자리의 네 띠를 복구한다. */
static void 창자리그리기(int 가로,int archive_posisyon,int 폭,int haba_VALUE,Terminal_d413d4bc *window){
    int 왼쪽=가로>(int)window->x_coordinate?가로:(int)window->x_coordinate;
    int 위쪽=archive_posisyon>(int)window->Y_button_coordinate?archive_posisyon:(int)window->Y_button_coordinate;
    int RIGHT=가로+폭<(int)(window->x_coordinate+window->너비)?가로+폭:(int)(window->x_coordinate+window->너비);
    int 아래쪽=archive_posisyon+haba_VALUE<(int)(window->Y_button_coordinate+window->높이)?archive_posisyon+haba_VALUE:(int)(window->Y_button_coordinate+window->높이);
    영역그리기(window->x_coordinate,window->Y_button_coordinate,window->너비,window->높이);
    if(왼쪽>=RIGHT||위쪽>=아래쪽){영역그리기(가로,archive_posisyon,폭,haba_VALUE);return;}
    영역그리기(가로,archive_posisyon,폭,위쪽-archive_posisyon);
    영역그리기(가로,아래쪽,폭,archive_posisyon+haba_VALUE-아래쪽);
    영역그리기(가로,위쪽,왼쪽-가로,아래쪽-위쪽);
    영역그리기(RIGHT,위쪽,가로+폭-RIGHT,아래쪽-위쪽);
}
static void 초점알리기(void){information_technology_pending=(information_technology_pending&~15u)|(unsigned)(Focus+1)|0x10000;}
void 터미널입력방식(unsigned 한글여부){
    한글입력=한글여부!=0;
    /* Update title bars only: a mode switch must not erase an EL0 drawing. */
    if(Focus>=0){
        Terminal_d413d4bc *window_pagpasok=&Windows_list[Focus];
        pangalan_talahanayan(window_pagpasok->x_coordinate+240,window_pagpasok->Y_button_coordinate+7,window_pagpasok->너비>=500?(한글입력?"[FIL] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[FIL]":"[EN]"),0xffffff,0x905020);
    }
}
static void 앞으로올리기(int tagakilala_VALUE){if(tagakilala_VALUE<0||tagakilala_VALUE>=4||!Windows_list[tagakilala_VALUE].살아있음)return;int 현재위치=0;while(현재위치<pagpasok_COUNT&&pagkakasunud_sunod_VALUE[현재위치]!=tagakilala_VALUE)현재위치++;for(;현재위치+1<pagpasok_COUNT;현재위치++)pagkakasunud_sunod_VALUE[현재위치]=pagkakasunud_sunod_VALUE[현재위치+1];pagkakasunud_sunod_VALUE[pagpasok_COUNT-1]=tagakilala_VALUE;Focus=tagakilala_VALUE;초점알리기();다시그리기();}
static void 빈칸채우기(unsigned ROW_posisyon){for(unsigned character_code=0;character_code<최대열수;character_code++){Terminal_pagpasok->글자칸들[ROW_posisyon%Kasaysayan_linya_COUNT][character_code]=0;Terminal_pagpasok->모양들[ROW_posisyon%Kasaysayan_linya_COUNT][character_code]=Terminal_pagpasok->전경색|(Terminal_pagpasok->배경색<<4);}}
static void i_clear_TOC(void){Terminal_pagpasok->ROW_posisyon=Terminal_pagpasok->kolum_posisyon=Terminal_pagpasok->맨위=Terminal_pagpasok->iskrol=0;for(unsigned 반환값=0;반환값<Kasaysayan_linya_COUNT;반환값++)빈칸채우기(반환값);if(보이는지())Nilalaman_VALUE();}
static int Create_pagpasok(void){
    if(!보드화면기억공간())return -19;int tagakilala_VALUE=0;while(tagakilala_VALUE<4&&Windows_list[tagakilala_VALUE].살아있음)tagakilala_VALUE++;if(tagakilala_VALUE==4)return -28;
    desktop_View=1;Terminal_pagpasok=&Windows_list[tagakilala_VALUE];memset(Terminal_pagpasok,0,sizeof(*Terminal_pagpasok));Terminal_pagpasok->살아있음=1;Terminal_pagpasok->너비=568;Terminal_pagpasok->높이=360;Terminal_pagpasok->COLUMNS=68;Terminal_pagpasok->ROW_COUNT=19;Terminal_pagpasok->x_coordinate=12+tagakilala_VALUE*16;Terminal_pagpasok->Y_button_coordinate=48+tagakilala_VALUE*18;Terminal_pagpasok->전경색=7;Terminal_pagpasok->가리개보임=1;
    for(unsigned 반환값=0;반환값<Kasaysayan_linya_COUNT;반환값++)빈칸채우기(반환값);pagkakasunud_sunod_VALUE[pagpasok_COUNT++]=tagakilala_VALUE;Focus=tagakilala_VALUE;information_technology_pending|=1u<<(4+tagakilala_VALUE);초점알리기();다시그리기();return tagakilala_VALUE+1;
}
static void isara_window(int tagakilala_VALUE){
    if(tagakilala_VALUE<0||tagakilala_VALUE>=4||!Windows_list[tagakilala_VALUE].살아있음)return;Windows_list[tagakilala_VALUE].살아있음=0;information_technology_pending|=1u<<(8+tagakilala_VALUE);
    int 현재위치=0;while(현재위치<pagpasok_COUNT&&pagkakasunud_sunod_VALUE[현재위치]!=tagakilala_VALUE)현재위치++;for(;현재위치+1<pagpasok_COUNT;현재위치++)pagkakasunud_sunod_VALUE[현재위치]=pagkakasunud_sunod_VALUE[현재위치+1];pagpasok_COUNT--;
    if(Focus==tagakilala_VALUE)Focus=pagpasok_COUNT?pagkakasunud_sunod_VALUE[pagpasok_COUNT-1]:-1;초점알리기();다시그리기();
}
static void 줄바꿈(void){Terminal_pagpasok->kolum_posisyon=0;Terminal_pagpasok->ROW_posisyon++;if(Terminal_pagpasok->ROW_posisyon>=Terminal_pagpasok->맨위+Terminal_pagpasok->ROW_COUNT){Terminal_pagpasok->맨위++;빈칸채우기(Terminal_pagpasok->ROW_posisyon);if(보이는지())Nilalaman_VALUE();}}
static void character_code_451f2815(unsigned character_code){
    if(character_code==13){Terminal_pagpasok->kolum_posisyon=0;return;}if(character_code==10){줄바꿈();return;}if(character_code==8){if(Terminal_pagpasok->kolum_posisyon)Terminal_pagpasok->kolum_posisyon--;return;}
    if(character_code==9){unsigned item_COUNT=8-Terminal_pagpasok->kolum_posisyon%8;while(item_COUNT--)character_code_451f2815(' ');return;}if(character_code<32||character_code==127)return;
    unsigned 너비값=넓은글자(character_code);if(Terminal_pagpasok->kolum_posisyon+너비값>Terminal_pagpasok->COLUMNS)줄바꿈();
    if(Terminal_pagpasok->글자칸들[Terminal_pagpasok->ROW_posisyon%Kasaysayan_linya_COUNT][Terminal_pagpasok->kolum_posisyon]==0xffffffffu&&Terminal_pagpasok->kolum_posisyon){Terminal_pagpasok->글자칸들[Terminal_pagpasok->ROW_posisyon%Kasaysayan_linya_COUNT][Terminal_pagpasok->kolum_posisyon-1]=' ';그리기(Terminal_pagpasok->ROW_posisyon,Terminal_pagpasok->kolum_posisyon-1);}
    if(넓은글자(Terminal_pagpasok->글자칸들[Terminal_pagpasok->ROW_posisyon%Kasaysayan_linya_COUNT][Terminal_pagpasok->kolum_posisyon])==2&&Terminal_pagpasok->kolum_posisyon+1<Terminal_pagpasok->COLUMNS){Terminal_pagpasok->글자칸들[Terminal_pagpasok->ROW_posisyon%Kasaysayan_linya_COUNT][Terminal_pagpasok->kolum_posisyon+1]=' ';그리기(Terminal_pagpasok->ROW_posisyon,Terminal_pagpasok->kolum_posisyon+1);}
    Terminal_pagpasok->글자칸들[Terminal_pagpasok->ROW_posisyon%Kasaysayan_linya_COUNT][Terminal_pagpasok->kolum_posisyon]=character_code;Terminal_pagpasok->모양들[Terminal_pagpasok->ROW_posisyon%Kasaysayan_linya_COUNT][Terminal_pagpasok->kolum_posisyon]=Terminal_pagpasok->전경색|(Terminal_pagpasok->배경색<<4);
    if(너비값==2)Terminal_pagpasok->글자칸들[Terminal_pagpasok->ROW_posisyon%Kasaysayan_linya_COUNT][Terminal_pagpasok->kolum_posisyon+1]=0xffffffffu;
    그리기(Terminal_pagpasok->ROW_posisyon,Terminal_pagpasok->kolum_posisyon);Terminal_pagpasok->kolum_posisyon+=너비값;
}
static void hawakán_control_SEQUENCE(unsigned character_code){
    unsigned item_COUNT=Terminal_pagpasok->parameter_VALUE[0]?Terminal_pagpasok->parameter_VALUE[0]:1;
    if(character_code=='m')for(unsigned 순번=0;순번<=Terminal_pagpasok->parameter_INDEX;순번++){unsigned data_posisyon=Terminal_pagpasok->parameter_VALUE[순번];if(!data_posisyon){Terminal_pagpasok->전경색=7;Terminal_pagpasok->배경색=0;}if(data_posisyon==1&&Terminal_pagpasok->전경색<8)Terminal_pagpasok->전경색+=8;if(data_posisyon==7){unsigned 유지=Terminal_pagpasok->전경색;Terminal_pagpasok->전경색=Terminal_pagpasok->배경색;Terminal_pagpasok->배경색=유지;}if(data_posisyon>=30&&data_posisyon<=37)Terminal_pagpasok->전경색=data_posisyon-30;if(data_posisyon>=90&&data_posisyon<=97)Terminal_pagpasok->전경색=data_posisyon-90+8;if(data_posisyon>=40&&data_posisyon<=47)Terminal_pagpasok->배경색=data_posisyon-40;if(data_posisyon>=100&&data_posisyon<=107)Terminal_pagpasok->배경색=data_posisyon-100+8;if(data_posisyon==39)Terminal_pagpasok->전경색=7;if(data_posisyon==49)Terminal_pagpasok->배경색=0;}
    if(character_code=='J'&&(Terminal_pagpasok->parameter_VALUE[0]==2||Terminal_pagpasok->parameter_VALUE[0]==3))i_clear_TOC();
    if(character_code=='K'){unsigned 출발위치=Terminal_pagpasok->parameter_VALUE[0]==2?0:Terminal_pagpasok->kolum_posisyon,도착위치=Terminal_pagpasok->parameter_VALUE[0]==1?Terminal_pagpasok->kolum_posisyon+1:Terminal_pagpasok->COLUMNS;if(Terminal_pagpasok->parameter_VALUE[0]==1)출발위치=0;for(unsigned 순번=출발위치;순번<도착위치&&순번<Terminal_pagpasok->COLUMNS;순번++){
        unsigned ROW_VALUE=Terminal_pagpasok->ROW_posisyon%Kasaysayan_linya_COUNT,karakter_VALUE=Terminal_pagpasok->글자칸들[ROW_VALUE][순번],hugis_VALUE=Terminal_pagpasok->전경색|(Terminal_pagpasok->배경색<<4);
        /* 넓은 vi 화면에서도 이미 빈 칸의 font_VALUE 화소를 되풀이해 칠하지 않는다. */
        int 바뀜=(karakter_VALUE!=0&&karakter_VALUE!=' ')||Terminal_pagpasok->모양들[ROW_VALUE][순번]!=hugis_VALUE;
        Terminal_pagpasok->글자칸들[ROW_VALUE][순번]=' ';Terminal_pagpasok->모양들[ROW_VALUE][순번]=hugis_VALUE;
        if(바뀜)그리기(Terminal_pagpasok->ROW_posisyon,순번);
    }}
    if(character_code=='D')Terminal_pagpasok->kolum_posisyon=item_COUNT>Terminal_pagpasok->kolum_posisyon?0:Terminal_pagpasok->kolum_posisyon-item_COUNT;if(character_code=='C')Terminal_pagpasok->kolum_posisyon=Terminal_pagpasok->kolum_posisyon+item_COUNT>=Terminal_pagpasok->COLUMNS?Terminal_pagpasok->COLUMNS-1:Terminal_pagpasok->kolum_posisyon+item_COUNT;
    if(character_code=='G')Terminal_pagpasok->kolum_posisyon=item_COUNT>Terminal_pagpasok->COLUMNS?Terminal_pagpasok->COLUMNS-1:item_COUNT-1;if(character_code=='A')Terminal_pagpasok->ROW_posisyon=item_COUNT>Terminal_pagpasok->ROW_posisyon-Terminal_pagpasok->맨위?Terminal_pagpasok->맨위:Terminal_pagpasok->ROW_posisyon-item_COUNT;
    if(character_code=='B')Terminal_pagpasok->ROW_posisyon=Terminal_pagpasok->ROW_posisyon+item_COUNT>=Terminal_pagpasok->맨위+Terminal_pagpasok->ROW_COUNT?Terminal_pagpasok->맨위+Terminal_pagpasok->ROW_COUNT-1:Terminal_pagpasok->ROW_posisyon+item_COUNT;
    if(character_code=='H'||character_code=='f'){Terminal_pagpasok->ROW_posisyon=Terminal_pagpasok->맨위+(item_COUNT>Terminal_pagpasok->ROW_COUNT?Terminal_pagpasok->ROW_COUNT:item_COUNT)-1;unsigned x_coordinate=Terminal_pagpasok->parameter_VALUE[1]?Terminal_pagpasok->parameter_VALUE[1]:1;Terminal_pagpasok->kolum_posisyon=(x_coordinate>Terminal_pagpasok->COLUMNS?Terminal_pagpasok->COLUMNS:x_coordinate)-1;}
    if(character_code=='s'){Terminal_pagpasok->저장행=Terminal_pagpasok->ROW_posisyon;Terminal_pagpasok->저장열=Terminal_pagpasok->kolum_posisyon;}if(character_code=='u'){Terminal_pagpasok->ROW_posisyon=Terminal_pagpasok->저장행;Terminal_pagpasok->kolum_posisyon=Terminal_pagpasok->저장열<Terminal_pagpasok->COLUMNS?Terminal_pagpasok->저장열:Terminal_pagpasok->COLUMNS-1;}
    if((character_code=='h'||character_code=='l')&&Terminal_pagpasok->parameter_VALUE[0]==25)Terminal_pagpasok->가리개보임=character_code=='h';
}
void Terminal_byte(unsigned SECOND_VALUE){
    Terminal_pagpasok=&Windows_list[출력결과];if(!Terminal_pagpasok->살아있음)return;caret_VALUE(0);if(Terminal_pagpasok->iskrol){Terminal_pagpasok->iskrol=0;if(보이는지())Nilalaman_VALUE();}
    if(Terminal_pagpasok->탈출상태==1){Terminal_pagpasok->탈출상태=SECOND_VALUE=='['?2:0;Terminal_pagpasok->parameter_INDEX=0;for(unsigned 순번=0;순번<4;순번++)Terminal_pagpasok->parameter_VALUE[순번]=0;}
    else if(Terminal_pagpasok->탈출상태==2){if(SECOND_VALUE=='?'){}else if(SECOND_VALUE>='0'&&SECOND_VALUE<='9'){if(Terminal_pagpasok->parameter_VALUE[Terminal_pagpasok->parameter_INDEX]<10000)Terminal_pagpasok->parameter_VALUE[Terminal_pagpasok->parameter_INDEX]=Terminal_pagpasok->parameter_VALUE[Terminal_pagpasok->parameter_INDEX]*10+SECOND_VALUE-'0';}else if(SECOND_VALUE==';'&&Terminal_pagpasok->parameter_INDEX<3)Terminal_pagpasok->parameter_INDEX++;else{hawakán_control_SEQUENCE(SECOND_VALUE);Terminal_pagpasok->탈출상태=0;}}
    else if(SECOND_VALUE==27){Terminal_pagpasok->긴부호없는값=0;Terminal_pagpasok->탈출상태=1;}else{
        if(Terminal_pagpasok->긴부호없는값&&(SECOND_VALUE&0xc0)!=0x80){Terminal_pagpasok->긴부호없는값=0;character_code_451f2815(0xfffd);}
        if(Terminal_pagpasok->긴부호없는값){Terminal_pagpasok->부호없는결과=Terminal_pagpasok->부호없는결과*64+(SECOND_VALUE&63);if(--Terminal_pagpasok->긴부호없는값==0)character_code_451f2815(Terminal_pagpasok->부호없는결과<Terminal_pagpasok->SMALL_VALUE||Terminal_pagpasok->부호없는결과>0x10ffff||(Terminal_pagpasok->부호없는결과>=0xd800&&Terminal_pagpasok->부호없는결과<=0xdfff)?0xfffd:Terminal_pagpasok->부호없는결과);}
        else if(SECOND_VALUE<128)character_code_451f2815(SECOND_VALUE);else if(SECOND_VALUE>=0xc2&&SECOND_VALUE<=0xf4){Terminal_pagpasok->긴부호없는값=SECOND_VALUE<0xe0?1:SECOND_VALUE<0xf0?2:3;Terminal_pagpasok->부호없는결과=SECOND_VALUE&((1u<<(6-Terminal_pagpasok->긴부호없는값))-1);Terminal_pagpasok->SMALL_VALUE=Terminal_pagpasok->긴부호없는값==1?128:Terminal_pagpasok->긴부호없는값==2?2048:65536;}else character_code_451f2815(0xfffd);
    }caret_VALUE(1);
}
int Terminal_pending(void){return information_technology_pending!=0;}
/* 모서리 INDEX: 1 좌상, 2 우상, 3 좌하, 4 우하. */
static int palitan_ang_laki_mag_drag=-1,잡은모서리,잡은가로,잡은세로,처음가로,처음세로,처음너비,처음높이;
static int 가리킨창(int 가로,int archive_posisyon) {
    for(int SEQUENCE_VALUE=pagpasok_COUNT-1;SEQUENCE_VALUE>=0;SEQUENCE_VALUE--){
        int tagakilala_VALUE=pagkakasunud_sunod_VALUE[SEQUENCE_VALUE];Terminal_d413d4bc *window=&Windows_list[tagakilala_VALUE];
        if(가로>=(int)window->x_coordinate&&archive_posisyon>=(int)window->Y_button_coordinate&&
           가로<(int)(window->x_coordinate+window->너비)&&archive_posisyon<(int)(window->Y_button_coordinate+window->높이))return tagakilala_VALUE;
    }return -1;
}
static int 모서리찾기(int tagakilala_VALUE,int 가로,int archive_posisyon) {
    if(tagakilala_VALUE<0)return 0;Terminal_d413d4bc *window=&Windows_list[tagakilala_VALUE];
    int 왼쪽=가로<(int)window->x_coordinate+8,RIGHT=가로>=(int)(window->x_coordinate+window->너비)-8;
    int 위쪽=archive_posisyon<(int)window->Y_button_coordinate+8,아래쪽=archive_posisyon>=(int)(window->Y_button_coordinate+window->높이)-8;
    return (왼쪽||RIGHT)&&(위쪽||아래쪽)?1+RIGHT+아래쪽*2:0;
}
static int tagahiwalay_VALUE(int VALUE,int 최소,int 최대){return VALUE<최소?최소:VALUE>최대?최대:VALUE;}
static void ilipat_palitan_ang_laki(int 가로,int archive_posisyon) {
    Terminal_d413d4bc *window=&Windows_list[palitan_ang_laki_mag_drag];int 왼쪽=처음가로,위쪽=처음세로,RIGHT=처음가로+처음너비,아래쪽=처음세로+처음높이;
    if(잡은모서리==1||잡은모서리==3)왼쪽=tagahiwalay_VALUE(처음가로+가로-잡은가로,0,RIGHT-360);
    else RIGHT=tagahiwalay_VALUE(처음가로+처음너비+가로-잡은가로,왼쪽+360,보드화면너비());
    if(잡은모서리<=2)위쪽=tagahiwalay_VALUE(처음세로+archive_posisyon-잡은세로,34,아래쪽-216);
    else 아래쪽=tagahiwalay_VALUE(처음세로+처음높이+archive_posisyon-잡은세로,위쪽+216,보드화면높이());
    unsigned COLUMNS=(RIGHT-왼쪽-24)/8,ROW_COUNT=(아래쪽-위쪽-56)/16;
    if(window->COLUMNS!=COLUMNS||window->ROW_COUNT!=ROW_COUNT){
        window->크기바뀜=1;window->COLUMNS=COLUMNS;window->ROW_COUNT=ROW_COUNT;
        if(window->kolum_posisyon>=COLUMNS)window->kolum_posisyon=COLUMNS-1;
        if(window->ROW_posisyon>=window->맨위+ROW_COUNT)window->맨위=window->ROW_posisyon-ROW_COUNT+1;
        unsigned 한도=window->맨위;if(한도>Kasaysayan_linya_COUNT-ROW_COUNT)한도=Kasaysayan_linya_COUNT-ROW_COUNT;
        if(window->iskrol>한도)window->iskrol=한도;
    }
    int 옛가로=window->x_coordinate,옛세로=window->Y_button_coordinate,옛폭=window->너비,옛길이=window->높이;
    if(옛가로==왼쪽&&옛세로==위쪽&&옛폭==RIGHT-왼쪽&&옛길이==아래쪽-위쪽)return;
    window->x_coordinate=왼쪽;window->Y_button_coordinate=위쪽;window->너비=RIGHT-왼쪽;window->높이=아래쪽-위쪽;
    창자리그리기(옛가로,옛세로,옛폭,옛길이,window);
}
void Terminal_pointer(unsigned Susunod_item,int x_coordinate,int Y_button_coordinate){
    unsigned 눌림=Susunod_item&~단추들;단추들=Susunod_item;
    if(!desktop_View){mag_drag_VALUE=-1;palitan_ang_laki_mag_drag=-1;board_pointer(x_coordinate,Y_button_coordinate,1);return;}
    if(!(Susunod_item&1)){mag_drag_VALUE=-1;palitan_ang_laki_mag_drag=-1;}
    if(palitan_ang_laki_mag_drag>=0&&!Windows_list[palitan_ang_laki_mag_drag].살아있음)palitan_ang_laki_mag_drag=-1;
    if(mag_drag_VALUE>=0&&!Windows_list[mag_drag_VALUE].살아있음)mag_drag_VALUE=-1;
    if(palitan_ang_laki_mag_drag>=0){
        ilipat_palitan_ang_laki(x_coordinate,Y_button_coordinate);board_pointer(x_coordinate,Y_button_coordinate,잡은모서리==1||잡은모서리==4?2:3);return;
    }
    board_pointer(x_coordinate,Y_button_coordinate,1);
    if(mag_drag_VALUE>=0){
        Terminal_d413d4bc *window=&Windows_list[mag_drag_VALUE];
        int 옛가로=window->x_coordinate,옛세로=window->Y_button_coordinate;
        window->x_coordinate=tagahiwalay_VALUE(x_coordinate-mag_drag_X_button,0,보드화면너비()-window->너비);
        window->Y_button_coordinate=tagahiwalay_VALUE(Y_button_coordinate-mag_drag_Y_button,34,보드화면높이()-window->높이);
        if(옛가로!=(int)window->x_coordinate||옛세로!=(int)window->Y_button_coordinate)창자리그리기(옛가로,옛세로,window->너비,window->높이,window);
        return;
    }
    extern int 화면덮음(int,int,int);
    if(화면덮음(Focus,x_coordinate,Y_button_coordinate)){화면가리킴(Focus,눌림,x_coordinate,Y_button_coordinate);return;}
    int tagakilala_VALUE=가리킨창(x_coordinate,Y_button_coordinate),모서리=모서리찾기(tagakilala_VALUE,x_coordinate,Y_button_coordinate);
    if(모서리)board_pointer(x_coordinate,Y_button_coordinate,모서리==1||모서리==4?2:3);
    if(눌림&1){
        if(모서리){
            Terminal_d413d4bc *window=&Windows_list[tagakilala_VALUE];palitan_ang_laki_mag_drag=tagakilala_VALUE;잡은모서리=모서리;잡은가로=x_coordinate;잡은세로=Y_button_coordinate;
            처음가로=window->x_coordinate;처음세로=window->Y_button_coordinate;처음너비=window->너비;처음높이=window->높이;
            if(tagakilala_VALUE!=Focus)앞으로올리기(tagakilala_VALUE);return;
        }
        if(Y_button_coordinate<32&&x_coordinate>=6&&x_coordinate<142){Create_pagpasok();return;}
        if(Y_button_coordinate<32&&x_coordinate>=154&&x_coordinate<602){앞으로올리기((x_coordinate-154)/112);return;}
        if(tagakilala_VALUE>=0){
            Terminal_d413d4bc *window=&Windows_list[tagakilala_VALUE];
            if(Y_button_coordinate<(int)window->Y_button_coordinate+30&&x_coordinate>=(int)(window->x_coordinate+window->너비)-32){isara_window(tagakilala_VALUE);return;}
            if(tagakilala_VALUE!=Focus)앞으로올리기(tagakilala_VALUE);
            if(Y_button_coordinate<(int)window->Y_button_coordinate+30){mag_drag_VALUE=tagakilala_VALUE;mag_drag_X_button=x_coordinate-window->x_coordinate;mag_drag_Y_button=Y_button_coordinate-window->Y_button_coordinate;}return;
        }
    }
    if(Focus>=0&&(눌림&(8|16))){Terminal_pagpasok=&Windows_list[Focus];if(눌림&8){unsigned 한도=Terminal_pagpasok->맨위;if(한도>Kasaysayan_linya_COUNT-Terminal_pagpasok->ROW_COUNT)한도=Kasaysayan_linya_COUNT-Terminal_pagpasok->ROW_COUNT;Terminal_pagpasok->iskrol=Terminal_pagpasok->iskrol+9>한도?한도:Terminal_pagpasok->iskrol+9;}else Terminal_pagpasok->iskrol=Terminal_pagpasok->iskrol<9?0:Terminal_pagpasok->iskrol-9;다시그리기();}
}
void 터미널바로가기키(unsigned 누름값){if(누름값==1)Create_pagpasok();if(누름값==2&&pagpasok_COUNT)앞으로올리기(pagkakasunud_sunod_VALUE[0]);if(누름값==3)isara_window(Focus);}
machine_Word board_Terminal(machine_Word aksyon){
    if(aksyon==300){if(!Windows_list[출력결과].살아있음)return Create_pagpasok();desktop_View=1;다시그리기();return 0;}
    if(aksyon==0){isara_window(Focus);return 0;}if(aksyon==1)return (uint32_t)Create_pagpasok();if(aksyon==2)return Focus>=0;
    if(aksyon==9){desktop_View=0;return 0;}if(aksyon==7)return pagpasok_COUNT;if(aksyon==10)return Focus+1;if(aksyon==11)return 출력결과;
    if(aksyon==13){Terminal_d413d4bc *window=&Windows_list[출력결과];return window->살아있음?(window->ROW_COUNT<<16)|window->COLUMNS:(19<<16)|68;}
    if(aksyon==14){unsigned VALUE=Windows_list[출력결과].크기바뀜;Windows_list[출력결과].크기바뀜=0;return VALUE;}
    if(aksyon==12){unsigned VALUE=information_technology_pending;information_technology_pending=0;return VALUE;}
    if(aksyon>=20&&aksyon<24)return Windows_list[aksyon-20].살아있음;
    if(aksyon>=100&&aksyon<104){출력결과=aksyon-100;Terminal_pagpasok=&Windows_list[출력결과];return 0;}
    if(aksyon>=200&&aksyon<204){앞으로올리기(aksyon-200);return 0;}
    if(aksyon==3){다시그리기();return 0;}Terminal_pagpasok=&Windows_list[출력결과];if(!Terminal_pagpasok->살아있음)return 0;
    if(aksyon==4)i_clear_TOC();if(aksyon==5||aksyon==6){unsigned 이전=단추들;Terminal_pointer(aksyon==5?8:16,0,0);단추들=이전;}return 1;
}
