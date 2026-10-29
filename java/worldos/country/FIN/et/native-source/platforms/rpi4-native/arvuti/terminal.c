#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* oma 네 aken 합성과 UTF-8 terminal. 바뀐 영역의 Lõpetatud_VALUE 그림만 표시한다. */
#include <stdint.h>
#include <stddef.h>
typedef uintptr_t arvuti_Word;
extern arvuti_Word Tahvel_piksel(arvuti_Word,arvuti_Word,arvuti_Word),보드화면기억공간(void);
extern void *memset(void *,int,size_t);
extern const unsigned char terminal_font[];
#define 최대열수 237
#define Ajalugu_liin_COUNT 160
typedef struct {
    uint32_t 글자칸들[Ajalugu_liin_COUNT][최대열수]; uint8_t 모양들[Ajalugu_liin_COUNT][최대열수];
    unsigned 너비,높이,COLUMNS,ROW_COUNT,크기바뀜;
    unsigned 살아있음,가로좌표,세로좌표,ROW_ametikoht,veerg_ametikoht,맨위,밀어올리기,전경색,배경색,탈출상태,parameeter_VALUE[4],parameeter_INDEX,저장행,저장열;
    unsigned 부호없는결과,긴부호없는값,SMALL_VALUE,대체화면,가리개보임;
} terminal_d413d4bc;
static terminal_d413d4bc Windows_Loend[4];
static int süvenemine=-1,toodang,tellimus_VALUE[4],kirje_COUNT,lohistama_VALUE=-1,lohistama_X,lohistama_Y;
static unsigned infotehnoloogia_ootel,단추들,töölaud_Kuva,한글입력;
static const uint32_t 색상들[16]={0x201a15,0x6060df,0x9dcc86,0x80cfea,0xefaf72,0xca96c9,0xceda76,0xede9df,0x858078,0x8888ff,0xb9eba7,0xa5eaff,0xffcc99,0xf0bef1,0xf0f0a0,0xffffff};
extern int 화면보임(int),화면가리킴(int,unsigned,int,int);
extern void 화면다시그림(int);
static terminal_d413d4bc *terminal_kirje;
static unsigned lai_tähemärk(unsigned koodipunkt){return koodipunkt>=256?2:1;}
static void 사각영역(unsigned 가로좌표,unsigned 세로좌표,unsigned 너비값,unsigned 높이값,unsigned 색상){
    Tahvel_ristkülik_täide(가로좌표,세로좌표,너비값,높이값,색상);
}
void terminal_glüüf(unsigned 가로좌표,unsigned 세로좌표,unsigned koodipunkt,unsigned 전경색,unsigned 배경색){
    unsigned 너비=lai_tähemärk(koodipunkt)*8;if(koodipunkt==0xffffffffu)return;
    int 왼쪽=가로좌표,위쪽=세로좌표,폭=너비,길이=16;
    if(!보드그림범위(&왼쪽,&위쪽,&폭,&길이))return;
    if(koodipunkt==' '){Tahvel_ristkülik_täide(왼쪽,위쪽,폭,길이,배경색);return;}
    unsigned LOOKUP_INDEX=koodipunkt<65536?koodipunkt:koodipunkt>=0x1f600&&koodipunkt<0x1f650?65536+koodipunkt-0x1f600:0xfffd;
    const unsigned char *font_VALUE=terminal_font+LOOKUP_INDEX*32;
    for(int Joon=위쪽;Joon<위쪽+길이;Joon++){unsigned Taustal_töötav_intelligentne_edastusteenus_Loend=font_VALUE[(Joon-세로좌표)*2]*256+font_VALUE[(Joon-세로좌표)*2+1];for(int 칸=왼쪽;칸<왼쪽+폭;칸++)Tahvel_piksel(칸,Joon,(Taustal_töötav_intelligentne_edastusteenus_Loend&(0x8000>>(칸-가로좌표)))?전경색:배경색);}
}
static void nimetus_tabel(unsigned 가로좌표,unsigned 세로좌표,const char *string_andmed,unsigned 전경색,unsigned 배경색){while(*string_andmed){unsigned koodipunkt=(unsigned char)*string_andmed++, 남은수=0;if(koodipunkt>=0xc0){남은수=koodipunkt<0xe0?1:koodipunkt<0xf0?2:3;koodipunkt&=(1u<<(6-남은수))-1;while(남은수--&&*string_andmed)koodipunkt=(koodipunkt<<6)|((unsigned char)*string_andmed++&63);}terminal_glüüf(가로좌표,세로좌표,koodipunkt,전경색,배경색);가로좌표+=lai_tähemärk(koodipunkt)*8;}}
static unsigned 첫항목(void){return terminal_kirje->맨위;}
static int 보이는지(void){return terminal_kirje->살아있음&&süvenemine>=0&&terminal_kirje==&Windows_Loend[süvenemine]&&!화면보임(süvenemine);}
static void 그리기(unsigned ROW_ametikoht,unsigned veerg_ametikoht){
    if(!보이는지()||ROW_ametikoht<첫항목()-terminal_kirje->밀어올리기||ROW_ametikoht>=첫항목()-terminal_kirje->밀어올리기+terminal_kirje->ROW_COUNT||veerg_ametikoht>=terminal_kirje->COLUMNS)return;
    unsigned koodipunkt=terminal_kirje->글자칸들[ROW_ametikoht%Ajalugu_liin_COUNT][veerg_ametikoht],string_andmed=terminal_kirje->모양들[ROW_ametikoht%Ajalugu_liin_COUNT][veerg_ametikoht];
    if(lai_tähemärk(koodipunkt)==2&&veerg_ametikoht+1>=terminal_kirje->COLUMNS)koodipunkt=' ';
    terminal_glüüf(terminal_kirje->가로좌표+12+veerg_ametikoht*8,terminal_kirje->세로좌표+36+(ROW_ametikoht-첫항목()+terminal_kirje->밀어올리기)*16,koodipunkt?koodipunkt:' ',색상들[string_andmed&15],색상들[string_andmed>>4]);
}
static void katus_VALUE(int saade_aken){if(!보이는지()||terminal_kirje->밀어올리기||terminal_kirje->veerg_ametikoht>=terminal_kirje->COLUMNS||terminal_kirje->ROW_ametikoht<terminal_kirje->맨위||terminal_kirje->ROW_ametikoht>=terminal_kirje->맨위+terminal_kirje->ROW_COUNT)return;
    if(!saade_aken||!terminal_kirje->가리개보임)그리기(terminal_kirje->ROW_ametikoht,terminal_kirje->veerg_ametikoht);else 사각영역(terminal_kirje->가로좌표+12+terminal_kirje->veerg_ametikoht*8,terminal_kirje->세로좌표+36+(terminal_kirje->ROW_ametikoht-terminal_kirje->맨위)*16+14,8,2,색상들[terminal_kirje->전경색]);}
static void Sisu_VALUE(void){
    사각영역(terminal_kirje->가로좌표+12,terminal_kirje->세로좌표+36,terminal_kirje->COLUMNS*8,terminal_kirje->ROW_COUNT*16,색상들[0]);
    int 가로=terminal_kirje->가로좌표+12,vertikaal_ametikoht=terminal_kirje->세로좌표+36,폭=terminal_kirje->COLUMNS*8,길이=terminal_kirje->ROW_COUNT*16;
    if(보드그림범위(&가로,&vertikaal_ametikoht,&폭,&길이)){
    unsigned 첫줄=(vertikaal_ametikoht-terminal_kirje->세로좌표-36)/16,끝줄=(vertikaal_ametikoht+길이-terminal_kirje->세로좌표-36+15)/16;
    unsigned 첫칸=(가로-terminal_kirje->가로좌표-12)/8,끝칸=(가로+폭-terminal_kirje->가로좌표-12+7)/8;
    if(첫칸)첫칸--; /* 잘림 경계 왼쪽에서 시작한 두 칸 글자도 그린다. */
    for(unsigned 반환값=첫줄;반환값<끝줄;반환값++)for(unsigned koodipunkt=첫칸;koodipunkt<끝칸;koodipunkt++){
        unsigned ROW_ametikoht=첫항목()-terminal_kirje->밀어올리기+반환값,märk_VALUE=terminal_kirje->글자칸들[ROW_ametikoht%Ajalugu_liin_COUNT][koodipunkt],string_andmed=terminal_kirje->모양들[ROW_ametikoht%Ajalugu_liin_COUNT][koodipunkt];
        if(lai_tähemärk(märk_VALUE)==2&&koodipunkt+1>=terminal_kirje->COLUMNS)märk_VALUE=' ';
        if((märk_VALUE==0||märk_VALUE==' ')&&(string_andmed>>4)==0)continue;
        terminal_glüüf(terminal_kirje->가로좌표+12+koodipunkt*8,terminal_kirje->세로좌표+36+반환값*16,märk_VALUE?märk_VALUE:' ',색상들[string_andmed&15],색상들[string_andmed>>4]);
    }}
    nimetus_tabel(terminal_kirje->가로좌표+12,terminal_kirje->세로좌표+terminal_kirje->높이-18,terminal_kirje->밀어올리기?"PgDn: recent output":terminal_kirje->너비>=500?"F6: next | Corner + left drag: resize":"Corner + left drag: resize",0xece8e2,0x403127);katus_VALUE(1);
}
static void 실행틀(int identifikaator_VALUE){
    terminal_kirje=&Windows_Loend[identifikaator_VALUE];
    int 가로=terminal_kirje->가로좌표,vertikaal_ametikoht=terminal_kirje->세로좌표,폭=terminal_kirje->너비,길이=terminal_kirje->높이;
    if(!보드그림범위(&가로,&vertikaal_ametikoht,&폭,&길이))return;
    사각영역(terminal_kirje->가로좌표,terminal_kirje->세로좌표,terminal_kirje->너비,terminal_kirje->높이,0x403127);
    unsigned 색상=identifikaator_VALUE==süvenemine?0x905020:0x604438;사각영역(terminal_kirje->가로좌표,terminal_kirje->세로좌표,terminal_kirje->너비,30,색상);
    nimetus_tabel(terminal_kirje->가로좌표+12,terminal_kirje->세로좌표+7,"JKOROS Terminal",0xffffff,색상);
    char 수치[2]={(char)('1'+identifikaator_VALUE),0};nimetus_tabel(terminal_kirje->가로좌표+148,terminal_kirje->세로좌표+7,수치,0xffffff,색상);
    nimetus_tabel(terminal_kirje->가로좌표+240,terminal_kirje->세로좌표+7,terminal_kirje->너비>=500?(한글입력?"[ET] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[ET]":"[EN]"),0xffffff,색상);
    사각영역(terminal_kirje->가로좌표+terminal_kirje->너비-32,terminal_kirje->세로좌표+4,26,22,0x5555b8);nimetus_tabel(terminal_kirje->가로좌표+terminal_kirje->너비-24,terminal_kirje->세로좌표+7,"X",0xffffff,0x5555b8);
    Sisu_VALUE();
}
static void Joonista_stseen(void){
    if(!töölaud_Kuva)return;사각영역(0,0,보드화면너비(),보드화면높이(),0x302018);사각영역(0,0,보드화면너비(),32,0x403127);
    사각영역(6,4,136,24,0x905020);nimetus_tabel(14,8,"+ New terminal",0xffffff,0x905020);
    for(int 순번=0;순번<4;순번++)if(Windows_Loend[순번].살아있음){unsigned koodipunkt=süvenemine==순번?0x905020:0x604438;사각영역(154+순번*112,4,106,24,koodipunkt);nimetus_tabel(160+순번*112,8,"Terminal",0xffffff,koodipunkt);char string_andmed[2]={(char)('1'+순번),0};nimetus_tabel(232+순번*112,8,string_andmed,0xffffff,koodipunkt);}
    if(!kirje_COUNT)nimetus_tabel(140,210,"Click + New terminal to start",0xede9df,0x302018);
    for(int 순번=0;순번<kirje_COUNT;순번++)실행틀(tellimus_VALUE[순번]);화면다시그림(süvenemine);terminal_kirje=&Windows_Loend[toodang];
}
static void Paint_regioon(int 가로,int vertikaal_ametikoht,int 폭,int 길이){
    if(!töölaud_Kuva||!보드그림범위(&가로,&vertikaal_ametikoht,&폭,&길이))return;
    for(int Joon=vertikaal_ametikoht;Joon<vertikaal_ametikoht+길이;Joon+=32){
        int 띠높이=vertikaal_ametikoht+길이-Joon;if(띠높이>32)띠높이=32;
        if(Tahvel_START_joonis(가로,Joon,폭,띠높이)){Joonista_stseen();Tahvel_lõpp_joonis();}
    }
}
static void 다시그리기(void){Paint_regioon(0,0,보드화면너비(),보드화면높이());}
/* 서로 겹치지 않는 새 aken 영역과 이전 자리의 네 띠를 복구한다. */
static void 창자리그리기(int 가로,int vertikaal_ametikoht,int 폭,int 길이,terminal_d413d4bc *aken){
    int 왼쪽=가로>(int)aken->가로좌표?가로:(int)aken->가로좌표;
    int 위쪽=vertikaal_ametikoht>(int)aken->세로좌표?vertikaal_ametikoht:(int)aken->세로좌표;
    int RIGHT=가로+폭<(int)(aken->가로좌표+aken->너비)?가로+폭:(int)(aken->가로좌표+aken->너비);
    int 아래쪽=vertikaal_ametikoht+길이<(int)(aken->세로좌표+aken->높이)?vertikaal_ametikoht+길이:(int)(aken->세로좌표+aken->높이);
    Paint_regioon(aken->가로좌표,aken->세로좌표,aken->너비,aken->높이);
    if(왼쪽>=RIGHT||위쪽>=아래쪽){Paint_regioon(가로,vertikaal_ametikoht,폭,길이);return;}
    Paint_regioon(가로,vertikaal_ametikoht,폭,위쪽-vertikaal_ametikoht);
    Paint_regioon(가로,아래쪽,폭,vertikaal_ametikoht+길이-아래쪽);
    Paint_regioon(가로,위쪽,왼쪽-가로,아래쪽-위쪽);
    Paint_regioon(RIGHT,위쪽,가로+폭-RIGHT,아래쪽-위쪽);
}
static void signaal_süvenemine(void){infotehnoloogia_ootel=(infotehnoloogia_ootel&~15u)|(unsigned)(süvenemine+1)|0x10000;}
void 터미널입력방식(unsigned 한글여부){
    한글입력=한글여부!=0;
    /* Update title bars only: a mode switch must not erase an EL0 drawing. */
    if(süvenemine>=0){
        terminal_d413d4bc *aken_kirje=&Windows_Loend[süvenemine];
        nimetus_tabel(aken_kirje->가로좌표+240,aken_kirje->세로좌표+7,aken_kirje->너비>=500?(한글입력?"[ET] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[ET]":"[EN]"),0xffffff,0x905020);
    }
}
static void 앞으로올리기(int identifikaator_VALUE){if(identifikaator_VALUE<0||identifikaator_VALUE>=4||!Windows_Loend[identifikaator_VALUE].살아있음)return;int tähtaja_piires_ametikoht=0;while(tähtaja_piires_ametikoht<kirje_COUNT&&tellimus_VALUE[tähtaja_piires_ametikoht]!=identifikaator_VALUE)tähtaja_piires_ametikoht++;for(;tähtaja_piires_ametikoht+1<kirje_COUNT;tähtaja_piires_ametikoht++)tellimus_VALUE[tähtaja_piires_ametikoht]=tellimus_VALUE[tähtaja_piires_ametikoht+1];tellimus_VALUE[kirje_COUNT-1]=identifikaator_VALUE;süvenemine=identifikaator_VALUE;signaal_süvenemine();다시그리기();}
static void 빈칸채우기(unsigned ROW_ametikoht){for(unsigned koodipunkt=0;koodipunkt<최대열수;koodipunkt++){terminal_kirje->글자칸들[ROW_ametikoht%Ajalugu_liin_COUNT][koodipunkt]=0;terminal_kirje->모양들[ROW_ametikoht%Ajalugu_liin_COUNT][koodipunkt]=terminal_kirje->전경색|(terminal_kirje->배경색<<4);}}
static void eemaldama_Sisu(void){terminal_kirje->ROW_ametikoht=terminal_kirje->veerg_ametikoht=terminal_kirje->맨위=terminal_kirje->밀어올리기=0;for(unsigned 반환값=0;반환값<Ajalugu_liin_COUNT;반환값++)빈칸채우기(반환값);if(보이는지())Sisu_VALUE();}
static int avama_kirje(void){
    if(!보드화면기억공간())return -19;int identifikaator_VALUE=0;while(identifikaator_VALUE<4&&Windows_Loend[identifikaator_VALUE].살아있음)identifikaator_VALUE++;if(identifikaator_VALUE==4)return -28;
    töölaud_Kuva=1;terminal_kirje=&Windows_Loend[identifikaator_VALUE];memset(terminal_kirje,0,sizeof(*terminal_kirje));terminal_kirje->살아있음=1;terminal_kirje->너비=568;terminal_kirje->높이=360;terminal_kirje->COLUMNS=68;terminal_kirje->ROW_COUNT=19;terminal_kirje->가로좌표=12+identifikaator_VALUE*16;terminal_kirje->세로좌표=48+identifikaator_VALUE*18;terminal_kirje->전경색=7;terminal_kirje->가리개보임=1;
    for(unsigned 반환값=0;반환값<Ajalugu_liin_COUNT;반환값++)빈칸채우기(반환값);tellimus_VALUE[kirje_COUNT++]=identifikaator_VALUE;süvenemine=identifikaator_VALUE;infotehnoloogia_ootel|=1u<<(4+identifikaator_VALUE);signaal_süvenemine();다시그리기();return identifikaator_VALUE+1;
}
static void Sule_aken(int identifikaator_VALUE){
    if(identifikaator_VALUE<0||identifikaator_VALUE>=4||!Windows_Loend[identifikaator_VALUE].살아있음)return;Windows_Loend[identifikaator_VALUE].살아있음=0;infotehnoloogia_ootel|=1u<<(8+identifikaator_VALUE);
    int tähtaja_piires_ametikoht=0;while(tähtaja_piires_ametikoht<kirje_COUNT&&tellimus_VALUE[tähtaja_piires_ametikoht]!=identifikaator_VALUE)tähtaja_piires_ametikoht++;for(;tähtaja_piires_ametikoht+1<kirje_COUNT;tähtaja_piires_ametikoht++)tellimus_VALUE[tähtaja_piires_ametikoht]=tellimus_VALUE[tähtaja_piires_ametikoht+1];kirje_COUNT--;
    if(süvenemine==identifikaator_VALUE)süvenemine=kirje_COUNT?tellimus_VALUE[kirje_COUNT-1]:-1;signaal_süvenemine();다시그리기();
}
static void 줄바꿈(void){terminal_kirje->veerg_ametikoht=0;terminal_kirje->ROW_ametikoht++;if(terminal_kirje->ROW_ametikoht>=terminal_kirje->맨위+terminal_kirje->ROW_COUNT){terminal_kirje->맨위++;빈칸채우기(terminal_kirje->ROW_ametikoht);if(보이는지())Sisu_VALUE();}}
static void koodipunkt_451f2815(unsigned koodipunkt){
    if(koodipunkt==13){terminal_kirje->veerg_ametikoht=0;return;}if(koodipunkt==10){줄바꿈();return;}if(koodipunkt==8){if(terminal_kirje->veerg_ametikoht)terminal_kirje->veerg_ametikoht--;return;}
    if(koodipunkt==9){unsigned kaup_COUNT=8-terminal_kirje->veerg_ametikoht%8;while(kaup_COUNT--)koodipunkt_451f2815(' ');return;}if(koodipunkt<32||koodipunkt==127)return;
    unsigned 너비값=lai_tähemärk(koodipunkt);if(terminal_kirje->veerg_ametikoht+너비값>terminal_kirje->COLUMNS)줄바꿈();
    if(terminal_kirje->글자칸들[terminal_kirje->ROW_ametikoht%Ajalugu_liin_COUNT][terminal_kirje->veerg_ametikoht]==0xffffffffu&&terminal_kirje->veerg_ametikoht){terminal_kirje->글자칸들[terminal_kirje->ROW_ametikoht%Ajalugu_liin_COUNT][terminal_kirje->veerg_ametikoht-1]=' ';그리기(terminal_kirje->ROW_ametikoht,terminal_kirje->veerg_ametikoht-1);}
    if(lai_tähemärk(terminal_kirje->글자칸들[terminal_kirje->ROW_ametikoht%Ajalugu_liin_COUNT][terminal_kirje->veerg_ametikoht])==2&&terminal_kirje->veerg_ametikoht+1<terminal_kirje->COLUMNS){terminal_kirje->글자칸들[terminal_kirje->ROW_ametikoht%Ajalugu_liin_COUNT][terminal_kirje->veerg_ametikoht+1]=' ';그리기(terminal_kirje->ROW_ametikoht,terminal_kirje->veerg_ametikoht+1);}
    terminal_kirje->글자칸들[terminal_kirje->ROW_ametikoht%Ajalugu_liin_COUNT][terminal_kirje->veerg_ametikoht]=koodipunkt;terminal_kirje->모양들[terminal_kirje->ROW_ametikoht%Ajalugu_liin_COUNT][terminal_kirje->veerg_ametikoht]=terminal_kirje->전경색|(terminal_kirje->배경색<<4);
    if(너비값==2)terminal_kirje->글자칸들[terminal_kirje->ROW_ametikoht%Ajalugu_liin_COUNT][terminal_kirje->veerg_ametikoht+1]=0xffffffffu;
    그리기(terminal_kirje->ROW_ametikoht,terminal_kirje->veerg_ametikoht);terminal_kirje->veerg_ametikoht+=너비값;
}
static void pide_meede_SEQUENCE(unsigned koodipunkt){
    unsigned kaup_COUNT=terminal_kirje->parameeter_VALUE[0]?terminal_kirje->parameeter_VALUE[0]:1;
    if(koodipunkt=='m')for(unsigned 순번=0;순번<=terminal_kirje->parameeter_INDEX;순번++){unsigned andmed_ametikoht=terminal_kirje->parameeter_VALUE[순번];if(!andmed_ametikoht){terminal_kirje->전경색=7;terminal_kirje->배경색=0;}if(andmed_ametikoht==1&&terminal_kirje->전경색<8)terminal_kirje->전경색+=8;if(andmed_ametikoht==7){unsigned 유지=terminal_kirje->전경색;terminal_kirje->전경색=terminal_kirje->배경색;terminal_kirje->배경색=유지;}if(andmed_ametikoht>=30&&andmed_ametikoht<=37)terminal_kirje->전경색=andmed_ametikoht-30;if(andmed_ametikoht>=90&&andmed_ametikoht<=97)terminal_kirje->전경색=andmed_ametikoht-90+8;if(andmed_ametikoht>=40&&andmed_ametikoht<=47)terminal_kirje->배경색=andmed_ametikoht-40;if(andmed_ametikoht>=100&&andmed_ametikoht<=107)terminal_kirje->배경색=andmed_ametikoht-100+8;if(andmed_ametikoht==39)terminal_kirje->전경색=7;if(andmed_ametikoht==49)terminal_kirje->배경색=0;}
    if(koodipunkt=='J'&&(terminal_kirje->parameeter_VALUE[0]==2||terminal_kirje->parameeter_VALUE[0]==3))eemaldama_Sisu();
    if(koodipunkt=='K'){unsigned 출발위치=terminal_kirje->parameeter_VALUE[0]==2?0:terminal_kirje->veerg_ametikoht,도착위치=terminal_kirje->parameeter_VALUE[0]==1?terminal_kirje->veerg_ametikoht+1:terminal_kirje->COLUMNS;if(terminal_kirje->parameeter_VALUE[0]==1)출발위치=0;for(unsigned 순번=출발위치;순번<도착위치&&순번<terminal_kirje->COLUMNS;순번++){
        unsigned ROW_VALUE=terminal_kirje->ROW_ametikoht%Ajalugu_liin_COUNT,märk_VALUE=terminal_kirje->글자칸들[ROW_VALUE][순번],kujund_VALUE=terminal_kirje->전경색|(terminal_kirje->배경색<<4);
        /* 넓은 vi 화면에서도 이미 빈 칸의 font_VALUE 화소를 되풀이해 칠하지 않는다. */
        int 바뀜=(märk_VALUE!=0&&märk_VALUE!=' ')||terminal_kirje->모양들[ROW_VALUE][순번]!=kujund_VALUE;
        terminal_kirje->글자칸들[ROW_VALUE][순번]=' ';terminal_kirje->모양들[ROW_VALUE][순번]=kujund_VALUE;
        if(바뀜)그리기(terminal_kirje->ROW_ametikoht,순번);
    }}
    if(koodipunkt=='D')terminal_kirje->veerg_ametikoht=kaup_COUNT>terminal_kirje->veerg_ametikoht?0:terminal_kirje->veerg_ametikoht-kaup_COUNT;if(koodipunkt=='C')terminal_kirje->veerg_ametikoht=terminal_kirje->veerg_ametikoht+kaup_COUNT>=terminal_kirje->COLUMNS?terminal_kirje->COLUMNS-1:terminal_kirje->veerg_ametikoht+kaup_COUNT;
    if(koodipunkt=='G')terminal_kirje->veerg_ametikoht=kaup_COUNT>terminal_kirje->COLUMNS?terminal_kirje->COLUMNS-1:kaup_COUNT-1;if(koodipunkt=='A')terminal_kirje->ROW_ametikoht=kaup_COUNT>terminal_kirje->ROW_ametikoht-terminal_kirje->맨위?terminal_kirje->맨위:terminal_kirje->ROW_ametikoht-kaup_COUNT;
    if(koodipunkt=='B')terminal_kirje->ROW_ametikoht=terminal_kirje->ROW_ametikoht+kaup_COUNT>=terminal_kirje->맨위+terminal_kirje->ROW_COUNT?terminal_kirje->맨위+terminal_kirje->ROW_COUNT-1:terminal_kirje->ROW_ametikoht+kaup_COUNT;
    if(koodipunkt=='H'||koodipunkt=='f'){terminal_kirje->ROW_ametikoht=terminal_kirje->맨위+(kaup_COUNT>terminal_kirje->ROW_COUNT?terminal_kirje->ROW_COUNT:kaup_COUNT)-1;unsigned 가로좌표=terminal_kirje->parameeter_VALUE[1]?terminal_kirje->parameeter_VALUE[1]:1;terminal_kirje->veerg_ametikoht=(가로좌표>terminal_kirje->COLUMNS?terminal_kirje->COLUMNS:가로좌표)-1;}
    if(koodipunkt=='s'){terminal_kirje->저장행=terminal_kirje->ROW_ametikoht;terminal_kirje->저장열=terminal_kirje->veerg_ametikoht;}if(koodipunkt=='u'){terminal_kirje->ROW_ametikoht=terminal_kirje->저장행;terminal_kirje->veerg_ametikoht=terminal_kirje->저장열<terminal_kirje->COLUMNS?terminal_kirje->저장열:terminal_kirje->COLUMNS-1;}
    if((koodipunkt=='h'||koodipunkt=='l')&&terminal_kirje->parameeter_VALUE[0]==25)terminal_kirje->가리개보임=koodipunkt=='h';
}
void terminal_bait(unsigned SECOND_VALUE){
    terminal_kirje=&Windows_Loend[toodang];if(!terminal_kirje->살아있음)return;katus_VALUE(0);if(terminal_kirje->밀어올리기){terminal_kirje->밀어올리기=0;if(보이는지())Sisu_VALUE();}
    if(terminal_kirje->탈출상태==1){terminal_kirje->탈출상태=SECOND_VALUE=='['?2:0;terminal_kirje->parameeter_INDEX=0;for(unsigned 순번=0;순번<4;순번++)terminal_kirje->parameeter_VALUE[순번]=0;}
    else if(terminal_kirje->탈출상태==2){if(SECOND_VALUE=='?'){}else if(SECOND_VALUE>='0'&&SECOND_VALUE<='9'){if(terminal_kirje->parameeter_VALUE[terminal_kirje->parameeter_INDEX]<10000)terminal_kirje->parameeter_VALUE[terminal_kirje->parameeter_INDEX]=terminal_kirje->parameeter_VALUE[terminal_kirje->parameeter_INDEX]*10+SECOND_VALUE-'0';}else if(SECOND_VALUE==';'&&terminal_kirje->parameeter_INDEX<3)terminal_kirje->parameeter_INDEX++;else{pide_meede_SEQUENCE(SECOND_VALUE);terminal_kirje->탈출상태=0;}}
    else if(SECOND_VALUE==27){terminal_kirje->긴부호없는값=0;terminal_kirje->탈출상태=1;}else{
        if(terminal_kirje->긴부호없는값&&(SECOND_VALUE&0xc0)!=0x80){terminal_kirje->긴부호없는값=0;koodipunkt_451f2815(0xfffd);}
        if(terminal_kirje->긴부호없는값){terminal_kirje->부호없는결과=terminal_kirje->부호없는결과*64+(SECOND_VALUE&63);if(--terminal_kirje->긴부호없는값==0)koodipunkt_451f2815(terminal_kirje->부호없는결과<terminal_kirje->SMALL_VALUE||terminal_kirje->부호없는결과>0x10ffff||(terminal_kirje->부호없는결과>=0xd800&&terminal_kirje->부호없는결과<=0xdfff)?0xfffd:terminal_kirje->부호없는결과);}
        else if(SECOND_VALUE<128)koodipunkt_451f2815(SECOND_VALUE);else if(SECOND_VALUE>=0xc2&&SECOND_VALUE<=0xf4){terminal_kirje->긴부호없는값=SECOND_VALUE<0xe0?1:SECOND_VALUE<0xf0?2:3;terminal_kirje->부호없는결과=SECOND_VALUE&((1u<<(6-terminal_kirje->긴부호없는값))-1);terminal_kirje->SMALL_VALUE=terminal_kirje->긴부호없는값==1?128:terminal_kirje->긴부호없는값==2?2048:65536;}else koodipunkt_451f2815(0xfffd);
    }katus_VALUE(1);
}
int terminal_ootel(void){return infotehnoloogia_ootel!=0;}
/* 모서리 INDEX: 1 좌상, 2 우상, 3 좌하, 4 우하. */
static int suurust_muutma_lohistama=-1,잡은모서리,잡은가로,잡은세로,처음가로,처음세로,처음너비,처음높이;
static int 가리킨창(int 가로,int vertikaal_ametikoht) {
    for(int SEQUENCE_VALUE=kirje_COUNT-1;SEQUENCE_VALUE>=0;SEQUENCE_VALUE--){
        int identifikaator_VALUE=tellimus_VALUE[SEQUENCE_VALUE];terminal_d413d4bc *aken=&Windows_Loend[identifikaator_VALUE];
        if(가로>=(int)aken->가로좌표&&vertikaal_ametikoht>=(int)aken->세로좌표&&
           가로<(int)(aken->가로좌표+aken->너비)&&vertikaal_ametikoht<(int)(aken->세로좌표+aken->높이))return identifikaator_VALUE;
    }return -1;
}
static int 모서리찾기(int identifikaator_VALUE,int 가로,int vertikaal_ametikoht) {
    if(identifikaator_VALUE<0)return 0;terminal_d413d4bc *aken=&Windows_Loend[identifikaator_VALUE];
    int 왼쪽=가로<(int)aken->가로좌표+8,RIGHT=가로>=(int)(aken->가로좌표+aken->너비)-8;
    int 위쪽=vertikaal_ametikoht<(int)aken->세로좌표+8,아래쪽=vertikaal_ametikoht>=(int)(aken->세로좌표+aken->높이)-8;
    return (왼쪽||RIGHT)&&(위쪽||아래쪽)?1+RIGHT+아래쪽*2:0;
}
static int eraldaja_VALUE(int VALUE,int 최소,int 최대){return VALUE<최소?최소:VALUE>최대?최대:VALUE;}
static void liigutama_suurust_muutma(int 가로,int vertikaal_ametikoht) {
    terminal_d413d4bc *aken=&Windows_Loend[suurust_muutma_lohistama];int 왼쪽=처음가로,위쪽=처음세로,RIGHT=처음가로+처음너비,아래쪽=처음세로+처음높이;
    if(잡은모서리==1||잡은모서리==3)왼쪽=eraldaja_VALUE(처음가로+가로-잡은가로,0,RIGHT-360);
    else RIGHT=eraldaja_VALUE(처음가로+처음너비+가로-잡은가로,왼쪽+360,보드화면너비());
    if(잡은모서리<=2)위쪽=eraldaja_VALUE(처음세로+vertikaal_ametikoht-잡은세로,34,아래쪽-216);
    else 아래쪽=eraldaja_VALUE(처음세로+처음높이+vertikaal_ametikoht-잡은세로,위쪽+216,보드화면높이());
    unsigned COLUMNS=(RIGHT-왼쪽-24)/8,ROW_COUNT=(아래쪽-위쪽-56)/16;
    if(aken->COLUMNS!=COLUMNS||aken->ROW_COUNT!=ROW_COUNT){
        aken->크기바뀜=1;aken->COLUMNS=COLUMNS;aken->ROW_COUNT=ROW_COUNT;
        if(aken->veerg_ametikoht>=COLUMNS)aken->veerg_ametikoht=COLUMNS-1;
        if(aken->ROW_ametikoht>=aken->맨위+ROW_COUNT)aken->맨위=aken->ROW_ametikoht-ROW_COUNT+1;
        unsigned 한도=aken->맨위;if(한도>Ajalugu_liin_COUNT-ROW_COUNT)한도=Ajalugu_liin_COUNT-ROW_COUNT;
        if(aken->밀어올리기>한도)aken->밀어올리기=한도;
    }
    int 옛가로=aken->가로좌표,옛세로=aken->세로좌표,옛폭=aken->너비,옛길이=aken->높이;
    if(옛가로==왼쪽&&옛세로==위쪽&&옛폭==RIGHT-왼쪽&&옛길이==아래쪽-위쪽)return;
    aken->가로좌표=왼쪽;aken->세로좌표=위쪽;aken->너비=RIGHT-왼쪽;aken->높이=아래쪽-위쪽;
    창자리그리기(옛가로,옛세로,옛폭,옛길이,aken);
}
void terminal_kursor(unsigned Edasi_kaup,int 가로좌표,int 세로좌표){
    unsigned 눌림=Edasi_kaup&~단추들;단추들=Edasi_kaup;
    if(!töölaud_Kuva){lohistama_VALUE=-1;suurust_muutma_lohistama=-1;Tahvel_kursor(가로좌표,세로좌표,1);return;}
    if(!(Edasi_kaup&1)){lohistama_VALUE=-1;suurust_muutma_lohistama=-1;}
    if(suurust_muutma_lohistama>=0&&!Windows_Loend[suurust_muutma_lohistama].살아있음)suurust_muutma_lohistama=-1;
    if(lohistama_VALUE>=0&&!Windows_Loend[lohistama_VALUE].살아있음)lohistama_VALUE=-1;
    if(suurust_muutma_lohistama>=0){
        liigutama_suurust_muutma(가로좌표,세로좌표);Tahvel_kursor(가로좌표,세로좌표,잡은모서리==1||잡은모서리==4?2:3);return;
    }
    Tahvel_kursor(가로좌표,세로좌표,1);
    if(lohistama_VALUE>=0){
        terminal_d413d4bc *aken=&Windows_Loend[lohistama_VALUE];
        int 옛가로=aken->가로좌표,옛세로=aken->세로좌표;
        aken->가로좌표=eraldaja_VALUE(가로좌표-lohistama_X,0,보드화면너비()-aken->너비);
        aken->세로좌표=eraldaja_VALUE(세로좌표-lohistama_Y,34,보드화면높이()-aken->높이);
        if(옛가로!=(int)aken->가로좌표||옛세로!=(int)aken->세로좌표)창자리그리기(옛가로,옛세로,aken->너비,aken->높이,aken);
        return;
    }
    extern int 화면덮음(int,int,int);
    if(화면덮음(süvenemine,가로좌표,세로좌표)){화면가리킴(süvenemine,눌림,가로좌표,세로좌표);return;}
    int identifikaator_VALUE=가리킨창(가로좌표,세로좌표),모서리=모서리찾기(identifikaator_VALUE,가로좌표,세로좌표);
    if(모서리)Tahvel_kursor(가로좌표,세로좌표,모서리==1||모서리==4?2:3);
    if(눌림&1){
        if(모서리){
            terminal_d413d4bc *aken=&Windows_Loend[identifikaator_VALUE];suurust_muutma_lohistama=identifikaator_VALUE;잡은모서리=모서리;잡은가로=가로좌표;잡은세로=세로좌표;
            처음가로=aken->가로좌표;처음세로=aken->세로좌표;처음너비=aken->너비;처음높이=aken->높이;
            if(identifikaator_VALUE!=süvenemine)앞으로올리기(identifikaator_VALUE);return;
        }
        if(세로좌표<32&&가로좌표>=6&&가로좌표<142){avama_kirje();return;}
        if(세로좌표<32&&가로좌표>=154&&가로좌표<602){앞으로올리기((가로좌표-154)/112);return;}
        if(identifikaator_VALUE>=0){
            terminal_d413d4bc *aken=&Windows_Loend[identifikaator_VALUE];
            if(세로좌표<(int)aken->세로좌표+30&&가로좌표>=(int)(aken->가로좌표+aken->너비)-32){Sule_aken(identifikaator_VALUE);return;}
            if(identifikaator_VALUE!=süvenemine)앞으로올리기(identifikaator_VALUE);
            if(세로좌표<(int)aken->세로좌표+30){lohistama_VALUE=identifikaator_VALUE;lohistama_X=가로좌표-aken->가로좌표;lohistama_Y=세로좌표-aken->세로좌표;}return;
        }
    }
    if(süvenemine>=0&&(눌림&(8|16))){terminal_kirje=&Windows_Loend[süvenemine];if(눌림&8){unsigned 한도=terminal_kirje->맨위;if(한도>Ajalugu_liin_COUNT-terminal_kirje->ROW_COUNT)한도=Ajalugu_liin_COUNT-terminal_kirje->ROW_COUNT;terminal_kirje->밀어올리기=terminal_kirje->밀어올리기+9>한도?한도:terminal_kirje->밀어올리기+9;}else terminal_kirje->밀어올리기=terminal_kirje->밀어올리기<9?0:terminal_kirje->밀어올리기-9;다시그리기();}
}
void 터미널바로가기키(unsigned 누름값){if(누름값==1)avama_kirje();if(누름값==2&&kirje_COUNT)앞으로올리기(tellimus_VALUE[0]);if(누름값==3)Sule_aken(süvenemine);}
arvuti_Word Tahvel_terminal(arvuti_Word Nimi){
    if(Nimi==300){if(!Windows_Loend[toodang].살아있음)return avama_kirje();töölaud_Kuva=1;다시그리기();return 0;}
    if(Nimi==0){Sule_aken(süvenemine);return 0;}if(Nimi==1)return (uint32_t)avama_kirje();if(Nimi==2)return süvenemine>=0;
    if(Nimi==9){töölaud_Kuva=0;return 0;}if(Nimi==7)return kirje_COUNT;if(Nimi==10)return süvenemine+1;if(Nimi==11)return toodang;
    if(Nimi==13){terminal_d413d4bc *aken=&Windows_Loend[toodang];return aken->살아있음?(aken->ROW_COUNT<<16)|aken->COLUMNS:(19<<16)|68;}
    if(Nimi==14){unsigned VALUE=Windows_Loend[toodang].크기바뀜;Windows_Loend[toodang].크기바뀜=0;return VALUE;}
    if(Nimi==12){unsigned VALUE=infotehnoloogia_ootel;infotehnoloogia_ootel=0;return VALUE;}
    if(Nimi>=20&&Nimi<24)return Windows_Loend[Nimi-20].살아있음;
    if(Nimi>=100&&Nimi<104){toodang=Nimi-100;terminal_kirje=&Windows_Loend[toodang];return 0;}
    if(Nimi>=200&&Nimi<204){앞으로올리기(Nimi-200);return 0;}
    if(Nimi==3){다시그리기();return 0;}terminal_kirje=&Windows_Loend[toodang];if(!terminal_kirje->살아있음)return 0;
    if(Nimi==4)eemaldama_Sisu();if(Nimi==5||Nimi==6){unsigned 이전=단추들;terminal_kursor(Nimi==5?8:16,0,0);단추들=이전;}return 1;
}
