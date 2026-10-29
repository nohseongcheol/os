#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* 자체 네 tieqa 합성과 UTF-8 Terminal. 바뀐 영역의 완성 그림만 표시한다. */
#include <stdint.h>
#include <stddef.h>
typedef uintptr_t kompjuter_Word;
extern kompjuter_Word bord_pel(kompjuter_Word,kompjuter_Word,kompjuter_Word),보드화면기억공간(void);
extern void *memset(void *,int,size_t);
extern const unsigned char Terminal_font[];
#define 최대열수 237
#define Kronoloġija_linja_COUNT 160
typedef struct {
    uint32_t 글자칸들[Kronoloġija_linja_COUNT][최대열수]; uint8_t 모양들[Kronoloġija_linja_COUNT][최대열수];
    unsigned 너비,높이,COLUMNS,ROW_COUNT,크기바뀜;
    unsigned 살아있음,koordinat_x,세로좌표,ROW_pożizzjoni,COLUMN_pożizzjoni,맨위,skrollja,전경색,배경색,탈출상태,매개값[4],매개색인,저장행,저장열;
    unsigned 부호없는결과,긴부호없는값,SMALL_VALUE,대체화면,가리개보임;
} Terminal_d413d4bc;
static Terminal_d413d4bc Windows_Lista[4];
static int Fokus=-1,출력결과,ordni_VALUE[4],entrata_COUNT,dreggja_VALUE=-1,끌기가로,끌기세로;
static unsigned 대기중,단추들,desktop_wera,한글입력;
static const uint32_t 색상들[16]={0x201a15,0x6060df,0x9dcc86,0x80cfea,0xefaf72,0xca96c9,0xceda76,0xede9df,0x858078,0x8888ff,0xb9eba7,0xa5eaff,0xffcc99,0xf0bef1,0xf0f0a0,0xffffff};
extern int 화면보임(int),화면가리킴(int,unsigned,int,int);
extern void 화면다시그림(int);
static Terminal_d413d4bc *Terminal_entrata;
static unsigned 넓은글자(unsigned kodiċi_tal_karattru){return kodiċi_tal_karattru>=256?2:1;}
static void 사각영역(unsigned koordinat_x,unsigned 세로좌표,unsigned 너비값,unsigned 높이값,unsigned 색상){
    보드사각그림(koordinat_x,세로좌표,너비값,높이값,색상);
}
void Terminal_glyph(unsigned koordinat_x,unsigned 세로좌표,unsigned kodiċi_tal_karattru,unsigned 전경색,unsigned 배경색){
    unsigned 너비=넓은글자(kodiċi_tal_karattru)*8;if(kodiċi_tal_karattru==0xffffffffu)return;
    int 왼쪽=koordinat_x,위쪽=세로좌표,폭=너비,tul_VALUE=16;
    if(!보드그림범위(&왼쪽,&위쪽,&폭,&tul_VALUE))return;
    if(kodiċi_tal_karattru==' '){보드사각그림(왼쪽,위쪽,폭,tul_VALUE,배경색);return;}
    unsigned LOOKUP_INDEX=kodiċi_tal_karattru<65536?kodiċi_tal_karattru:kodiċi_tal_karattru>=0x1f600&&kodiċi_tal_karattru<0x1f650?65536+kodiċi_tal_karattru-0x1f600:0xfffd;
    const unsigned char *font_VALUE=Terminal_font+LOOKUP_INDEX*32;
    for(int linja=위쪽;linja<위쪽+tul_VALUE;linja++){unsigned 비트들=font_VALUE[(linja-세로좌표)*2]*256+font_VALUE[(linja-세로좌표)*2+1];for(int slott_entrata=왼쪽;slott_entrata<왼쪽+폭;slott_entrata++)bord_pel(slott_entrata,linja,(비트들&(0x8000>>(slott_entrata-koordinat_x)))?전경색:배경색);}
}
static void isem_tabella(unsigned koordinat_x,unsigned 세로좌표,const char *string_data,unsigned 전경색,unsigned 배경색){while(*string_data){unsigned kodiċi_tal_karattru=(unsigned char)*string_data++, 남은수=0;if(kodiċi_tal_karattru>=0xc0){남은수=kodiċi_tal_karattru<0xe0?1:kodiċi_tal_karattru<0xf0?2:3;kodiċi_tal_karattru&=(1u<<(6-남은수))-1;while(남은수--&&*string_data)kodiċi_tal_karattru=(kodiċi_tal_karattru<<6)|((unsigned char)*string_data++&63);}Terminal_glyph(koordinat_x,세로좌표,kodiċi_tal_karattru,전경색,배경색);koordinat_x+=넓은글자(kodiċi_tal_karattru)*8;}}
static unsigned 첫항목(void){return Terminal_entrata->맨위;}
static int 보이는지(void){return Terminal_entrata->살아있음&&Fokus>=0&&Terminal_entrata==&Windows_Lista[Fokus]&&!화면보임(Fokus);}
static void 그리기(unsigned ROW_pożizzjoni,unsigned COLUMN_pożizzjoni){
    if(!보이는지()||ROW_pożizzjoni<첫항목()-Terminal_entrata->skrollja||ROW_pożizzjoni>=첫항목()-Terminal_entrata->skrollja+Terminal_entrata->ROW_COUNT||COLUMN_pożizzjoni>=Terminal_entrata->COLUMNS)return;
    unsigned kodiċi_tal_karattru=Terminal_entrata->글자칸들[ROW_pożizzjoni%Kronoloġija_linja_COUNT][COLUMN_pożizzjoni],string_data=Terminal_entrata->모양들[ROW_pożizzjoni%Kronoloġija_linja_COUNT][COLUMN_pożizzjoni];
    if(넓은글자(kodiċi_tal_karattru)==2&&COLUMN_pożizzjoni+1>=Terminal_entrata->COLUMNS)kodiċi_tal_karattru=' ';
    Terminal_glyph(Terminal_entrata->koordinat_x+12+COLUMN_pożizzjoni*8,Terminal_entrata->세로좌표+36+(ROW_pożizzjoni-첫항목()+Terminal_entrata->skrollja)*16,kodiċi_tal_karattru?kodiċi_tal_karattru:' ',색상들[string_data&15],색상들[string_data>>4]);
}
static void kappell_VALUE(int wera_tieqa){if(!보이는지()||Terminal_entrata->skrollja||Terminal_entrata->COLUMN_pożizzjoni>=Terminal_entrata->COLUMNS||Terminal_entrata->ROW_pożizzjoni<Terminal_entrata->맨위||Terminal_entrata->ROW_pożizzjoni>=Terminal_entrata->맨위+Terminal_entrata->ROW_COUNT)return;
    if(!wera_tieqa||!Terminal_entrata->가리개보임)그리기(Terminal_entrata->ROW_pożizzjoni,Terminal_entrata->COLUMN_pożizzjoni);else 사각영역(Terminal_entrata->koordinat_x+12+Terminal_entrata->COLUMN_pożizzjoni*8,Terminal_entrata->세로좌표+36+(Terminal_entrata->ROW_pożizzjoni-Terminal_entrata->맨위)*16+14,8,2,색상들[Terminal_entrata->전경색]);}
static void Kontenut_VALUE(void){
    사각영역(Terminal_entrata->koordinat_x+12,Terminal_entrata->세로좌표+36,Terminal_entrata->COLUMNS*8,Terminal_entrata->ROW_COUNT*16,색상들[0]);
    int 가로=Terminal_entrata->koordinat_x+12,Vertikali_pożizzjoni=Terminal_entrata->세로좌표+36,폭=Terminal_entrata->COLUMNS*8,tul_VALUE=Terminal_entrata->ROW_COUNT*16;
    if(보드그림범위(&가로,&Vertikali_pożizzjoni,&폭,&tul_VALUE)){
    unsigned 첫줄=(Vertikali_pożizzjoni-Terminal_entrata->세로좌표-36)/16,끝줄=(Vertikali_pożizzjoni+tul_VALUE-Terminal_entrata->세로좌표-36+15)/16;
    unsigned 첫칸=(가로-Terminal_entrata->koordinat_x-12)/8,끝칸=(가로+폭-Terminal_entrata->koordinat_x-12+7)/8;
    if(첫칸)첫칸--; /* 잘림 경계 왼쪽에서 시작한 두 slott_entrata 글자도 그린다. */
    for(unsigned 반환값=첫줄;반환값<끝줄;반환값++)for(unsigned kodiċi_tal_karattru=첫칸;kodiċi_tal_karattru<끝칸;kodiċi_tal_karattru++){
        unsigned ROW_pożizzjoni=첫항목()-Terminal_entrata->skrollja+반환값,karattru_VALUE=Terminal_entrata->글자칸들[ROW_pożizzjoni%Kronoloġija_linja_COUNT][kodiċi_tal_karattru],string_data=Terminal_entrata->모양들[ROW_pożizzjoni%Kronoloġija_linja_COUNT][kodiċi_tal_karattru];
        if(넓은글자(karattru_VALUE)==2&&kodiċi_tal_karattru+1>=Terminal_entrata->COLUMNS)karattru_VALUE=' ';
        if((karattru_VALUE==0||karattru_VALUE==' ')&&(string_data>>4)==0)continue;
        Terminal_glyph(Terminal_entrata->koordinat_x+12+kodiċi_tal_karattru*8,Terminal_entrata->세로좌표+36+반환값*16,karattru_VALUE?karattru_VALUE:' ',색상들[string_data&15],색상들[string_data>>4]);
    }}
    isem_tabella(Terminal_entrata->koordinat_x+12,Terminal_entrata->세로좌표+Terminal_entrata->높이-18,Terminal_entrata->skrollja?"PgDn: recent output":Terminal_entrata->너비>=500?"F6: next | Corner + left drag: resize":"Corner + left drag: resize",0xece8e2,0x403127);kappell_VALUE(1);
}
static void 실행틀(int identifikatur_VALUE){
    Terminal_entrata=&Windows_Lista[identifikatur_VALUE];
    int 가로=Terminal_entrata->koordinat_x,Vertikali_pożizzjoni=Terminal_entrata->세로좌표,폭=Terminal_entrata->너비,tul_VALUE=Terminal_entrata->높이;
    if(!보드그림범위(&가로,&Vertikali_pożizzjoni,&폭,&tul_VALUE))return;
    사각영역(Terminal_entrata->koordinat_x,Terminal_entrata->세로좌표,Terminal_entrata->너비,Terminal_entrata->높이,0x403127);
    unsigned 색상=identifikatur_VALUE==Fokus?0x905020:0x604438;사각영역(Terminal_entrata->koordinat_x,Terminal_entrata->세로좌표,Terminal_entrata->너비,30,색상);
    isem_tabella(Terminal_entrata->koordinat_x+12,Terminal_entrata->세로좌표+7,"JKOROS Terminal",0xffffff,색상);
    char 수치[2]={(char)('1'+identifikatur_VALUE),0};isem_tabella(Terminal_entrata->koordinat_x+148,Terminal_entrata->세로좌표+7,수치,0xffffff,색상);
    isem_tabella(Terminal_entrata->koordinat_x+240,Terminal_entrata->세로좌표+7,Terminal_entrata->너비>=500?(한글입력?"[MT] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[MT]":"[EN]"),0xffffff,색상);
    사각영역(Terminal_entrata->koordinat_x+Terminal_entrata->너비-32,Terminal_entrata->세로좌표+4,26,22,0x5555b8);isem_tabella(Terminal_entrata->koordinat_x+Terminal_entrata->너비-24,Terminal_entrata->세로좌표+7,"X",0xffffff,0x5555b8);
    Kontenut_VALUE();
}
static void 장면그리기(void){
    if(!desktop_wera)return;사각영역(0,0,보드화면너비(),보드화면높이(),0x302018);사각영역(0,0,보드화면너비(),32,0x403127);
    사각영역(6,4,136,24,0x905020);isem_tabella(14,8,"+ New terminal",0xffffff,0x905020);
    for(int 순번=0;순번<4;순번++)if(Windows_Lista[순번].살아있음){unsigned kodiċi_tal_karattru=Fokus==순번?0x905020:0x604438;사각영역(154+순번*112,4,106,24,kodiċi_tal_karattru);isem_tabella(160+순번*112,8,"Terminal",0xffffff,kodiċi_tal_karattru);char string_data[2]={(char)('1'+순번),0};isem_tabella(232+순번*112,8,string_data,0xffffff,kodiċi_tal_karattru);}
    if(!entrata_COUNT)isem_tabella(140,210,"Click + New terminal to start",0xede9df,0x302018);
    for(int 순번=0;순번<entrata_COUNT;순번++)실행틀(ordni_VALUE[순번]);화면다시그림(Fokus);Terminal_entrata=&Windows_Lista[출력결과];
}
static void 영역그리기(int 가로,int Vertikali_pożizzjoni,int 폭,int tul_VALUE){
    if(!desktop_wera||!보드그림범위(&가로,&Vertikali_pożizzjoni,&폭,&tul_VALUE))return;
    for(int linja=Vertikali_pożizzjoni;linja<Vertikali_pożizzjoni+tul_VALUE;linja+=32){
        int 띠높이=Vertikali_pożizzjoni+tul_VALUE-linja;if(띠높이>32)띠높이=32;
        if(bord_Bidu_tpinġija(가로,linja,폭,띠높이)){장면그리기();bord_Tmiem_tpinġija();}
    }
}
static void 다시그리기(void){영역그리기(0,0,보드화면너비(),보드화면높이());}
/* 서로 겹치지 않는 새 tieqa 영역과 이전 자리의 네 띠를 복구한다. */
static void 창자리그리기(int 가로,int Vertikali_pożizzjoni,int 폭,int tul_VALUE,Terminal_d413d4bc *tieqa){
    int 왼쪽=가로>(int)tieqa->koordinat_x?가로:(int)tieqa->koordinat_x;
    int 위쪽=Vertikali_pożizzjoni>(int)tieqa->세로좌표?Vertikali_pożizzjoni:(int)tieqa->세로좌표;
    int RIGHT=가로+폭<(int)(tieqa->koordinat_x+tieqa->너비)?가로+폭:(int)(tieqa->koordinat_x+tieqa->너비);
    int 아래쪽=Vertikali_pożizzjoni+tul_VALUE<(int)(tieqa->세로좌표+tieqa->높이)?Vertikali_pożizzjoni+tul_VALUE:(int)(tieqa->세로좌표+tieqa->높이);
    영역그리기(tieqa->koordinat_x,tieqa->세로좌표,tieqa->너비,tieqa->높이);
    if(왼쪽>=RIGHT||위쪽>=아래쪽){영역그리기(가로,Vertikali_pożizzjoni,폭,tul_VALUE);return;}
    영역그리기(가로,Vertikali_pożizzjoni,폭,위쪽-Vertikali_pożizzjoni);
    영역그리기(가로,아래쪽,폭,Vertikali_pożizzjoni+tul_VALUE-아래쪽);
    영역그리기(가로,위쪽,왼쪽-가로,아래쪽-위쪽);
    영역그리기(RIGHT,위쪽,가로+폭-RIGHT,아래쪽-위쪽);
}
static void 초점알리기(void){대기중=(대기중&~15u)|(unsigned)(Fokus+1)|0x10000;}
void 터미널입력방식(unsigned 한글여부){
    한글입력=한글여부!=0;
    /* Update title bars only: a mode switch must not erase an EL0 drawing. */
    if(Fokus>=0){
        Terminal_d413d4bc *tieqa_entrata=&Windows_Lista[Fokus];
        isem_tabella(tieqa_entrata->koordinat_x+240,tieqa_entrata->세로좌표+7,tieqa_entrata->너비>=500?(한글입력?"[MT] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[MT]":"[EN]"),0xffffff,0x905020);
    }
}
static void 앞으로올리기(int identifikatur_VALUE){if(identifikatur_VALUE<0||identifikatur_VALUE>=4||!Windows_Lista[identifikatur_VALUE].살아있음)return;int 현재위치=0;while(현재위치<entrata_COUNT&&ordni_VALUE[현재위치]!=identifikatur_VALUE)현재위치++;for(;현재위치+1<entrata_COUNT;현재위치++)ordni_VALUE[현재위치]=ordni_VALUE[현재위치+1];ordni_VALUE[entrata_COUNT-1]=identifikatur_VALUE;Fokus=identifikatur_VALUE;초점알리기();다시그리기();}
static void 빈칸채우기(unsigned ROW_pożizzjoni){for(unsigned kodiċi_tal_karattru=0;kodiċi_tal_karattru<최대열수;kodiċi_tal_karattru++){Terminal_entrata->글자칸들[ROW_pożizzjoni%Kronoloġija_linja_COUNT][kodiċi_tal_karattru]=0;Terminal_entrata->모양들[ROW_pożizzjoni%Kronoloġija_linja_COUNT][kodiċi_tal_karattru]=Terminal_entrata->전경색|(Terminal_entrata->배경색<<4);}}
static void neħħa_TOC(void){Terminal_entrata->ROW_pożizzjoni=Terminal_entrata->COLUMN_pożizzjoni=Terminal_entrata->맨위=Terminal_entrata->skrollja=0;for(unsigned 반환값=0;반환값<Kronoloġija_linja_COUNT;반환값++)빈칸채우기(반환값);if(보이는지())Kontenut_VALUE();}
static int ħalaq_entrata(void){
    if(!보드화면기억공간())return -19;int identifikatur_VALUE=0;while(identifikatur_VALUE<4&&Windows_Lista[identifikatur_VALUE].살아있음)identifikatur_VALUE++;if(identifikatur_VALUE==4)return -28;
    desktop_wera=1;Terminal_entrata=&Windows_Lista[identifikatur_VALUE];memset(Terminal_entrata,0,sizeof(*Terminal_entrata));Terminal_entrata->살아있음=1;Terminal_entrata->너비=568;Terminal_entrata->높이=360;Terminal_entrata->COLUMNS=68;Terminal_entrata->ROW_COUNT=19;Terminal_entrata->koordinat_x=12+identifikatur_VALUE*16;Terminal_entrata->세로좌표=48+identifikatur_VALUE*18;Terminal_entrata->전경색=7;Terminal_entrata->가리개보임=1;
    for(unsigned 반환값=0;반환값<Kronoloġija_linja_COUNT;반환값++)빈칸채우기(반환값);ordni_VALUE[entrata_COUNT++]=identifikatur_VALUE;Fokus=identifikatur_VALUE;대기중|=1u<<(4+identifikatur_VALUE);초점알리기();다시그리기();return identifikatur_VALUE+1;
}
static void agħlaq_tieqa(int identifikatur_VALUE){
    if(identifikatur_VALUE<0||identifikatur_VALUE>=4||!Windows_Lista[identifikatur_VALUE].살아있음)return;Windows_Lista[identifikatur_VALUE].살아있음=0;대기중|=1u<<(8+identifikatur_VALUE);
    int 현재위치=0;while(현재위치<entrata_COUNT&&ordni_VALUE[현재위치]!=identifikatur_VALUE)현재위치++;for(;현재위치+1<entrata_COUNT;현재위치++)ordni_VALUE[현재위치]=ordni_VALUE[현재위치+1];entrata_COUNT--;
    if(Fokus==identifikatur_VALUE)Fokus=entrata_COUNT?ordni_VALUE[entrata_COUNT-1]:-1;초점알리기();다시그리기();
}
static void 줄바꿈(void){Terminal_entrata->COLUMN_pożizzjoni=0;Terminal_entrata->ROW_pożizzjoni++;if(Terminal_entrata->ROW_pożizzjoni>=Terminal_entrata->맨위+Terminal_entrata->ROW_COUNT){Terminal_entrata->맨위++;빈칸채우기(Terminal_entrata->ROW_pożizzjoni);if(보이는지())Kontenut_VALUE();}}
static void kodiċi_tal_karattru_451f2815(unsigned kodiċi_tal_karattru){
    if(kodiċi_tal_karattru==13){Terminal_entrata->COLUMN_pożizzjoni=0;return;}if(kodiċi_tal_karattru==10){줄바꿈();return;}if(kodiċi_tal_karattru==8){if(Terminal_entrata->COLUMN_pożizzjoni)Terminal_entrata->COLUMN_pożizzjoni--;return;}
    if(kodiċi_tal_karattru==9){unsigned element_COUNT=8-Terminal_entrata->COLUMN_pożizzjoni%8;while(element_COUNT--)kodiċi_tal_karattru_451f2815(' ');return;}if(kodiċi_tal_karattru<32||kodiċi_tal_karattru==127)return;
    unsigned 너비값=넓은글자(kodiċi_tal_karattru);if(Terminal_entrata->COLUMN_pożizzjoni+너비값>Terminal_entrata->COLUMNS)줄바꿈();
    if(Terminal_entrata->글자칸들[Terminal_entrata->ROW_pożizzjoni%Kronoloġija_linja_COUNT][Terminal_entrata->COLUMN_pożizzjoni]==0xffffffffu&&Terminal_entrata->COLUMN_pożizzjoni){Terminal_entrata->글자칸들[Terminal_entrata->ROW_pożizzjoni%Kronoloġija_linja_COUNT][Terminal_entrata->COLUMN_pożizzjoni-1]=' ';그리기(Terminal_entrata->ROW_pożizzjoni,Terminal_entrata->COLUMN_pożizzjoni-1);}
    if(넓은글자(Terminal_entrata->글자칸들[Terminal_entrata->ROW_pożizzjoni%Kronoloġija_linja_COUNT][Terminal_entrata->COLUMN_pożizzjoni])==2&&Terminal_entrata->COLUMN_pożizzjoni+1<Terminal_entrata->COLUMNS){Terminal_entrata->글자칸들[Terminal_entrata->ROW_pożizzjoni%Kronoloġija_linja_COUNT][Terminal_entrata->COLUMN_pożizzjoni+1]=' ';그리기(Terminal_entrata->ROW_pożizzjoni,Terminal_entrata->COLUMN_pożizzjoni+1);}
    Terminal_entrata->글자칸들[Terminal_entrata->ROW_pożizzjoni%Kronoloġija_linja_COUNT][Terminal_entrata->COLUMN_pożizzjoni]=kodiċi_tal_karattru;Terminal_entrata->모양들[Terminal_entrata->ROW_pożizzjoni%Kronoloġija_linja_COUNT][Terminal_entrata->COLUMN_pożizzjoni]=Terminal_entrata->전경색|(Terminal_entrata->배경색<<4);
    if(너비값==2)Terminal_entrata->글자칸들[Terminal_entrata->ROW_pożizzjoni%Kronoloġija_linja_COUNT][Terminal_entrata->COLUMN_pożizzjoni+1]=0xffffffffu;
    그리기(Terminal_entrata->ROW_pożizzjoni,Terminal_entrata->COLUMN_pożizzjoni);Terminal_entrata->COLUMN_pożizzjoni+=너비값;
}
static void handle_kontroll_SEQUENCE(unsigned kodiċi_tal_karattru){
    unsigned element_COUNT=Terminal_entrata->매개값[0]?Terminal_entrata->매개값[0]:1;
    if(kodiċi_tal_karattru=='m')for(unsigned 순번=0;순번<=Terminal_entrata->매개색인;순번++){unsigned data_pożizzjoni=Terminal_entrata->매개값[순번];if(!data_pożizzjoni){Terminal_entrata->전경색=7;Terminal_entrata->배경색=0;}if(data_pożizzjoni==1&&Terminal_entrata->전경색<8)Terminal_entrata->전경색+=8;if(data_pożizzjoni==7){unsigned 유지=Terminal_entrata->전경색;Terminal_entrata->전경색=Terminal_entrata->배경색;Terminal_entrata->배경색=유지;}if(data_pożizzjoni>=30&&data_pożizzjoni<=37)Terminal_entrata->전경색=data_pożizzjoni-30;if(data_pożizzjoni>=90&&data_pożizzjoni<=97)Terminal_entrata->전경색=data_pożizzjoni-90+8;if(data_pożizzjoni>=40&&data_pożizzjoni<=47)Terminal_entrata->배경색=data_pożizzjoni-40;if(data_pożizzjoni>=100&&data_pożizzjoni<=107)Terminal_entrata->배경색=data_pożizzjoni-100+8;if(data_pożizzjoni==39)Terminal_entrata->전경색=7;if(data_pożizzjoni==49)Terminal_entrata->배경색=0;}
    if(kodiċi_tal_karattru=='J'&&(Terminal_entrata->매개값[0]==2||Terminal_entrata->매개값[0]==3))neħħa_TOC();
    if(kodiċi_tal_karattru=='K'){unsigned 출발위치=Terminal_entrata->매개값[0]==2?0:Terminal_entrata->COLUMN_pożizzjoni,도착위치=Terminal_entrata->매개값[0]==1?Terminal_entrata->COLUMN_pożizzjoni+1:Terminal_entrata->COLUMNS;if(Terminal_entrata->매개값[0]==1)출발위치=0;for(unsigned 순번=출발위치;순번<도착위치&&순번<Terminal_entrata->COLUMNS;순번++){
        unsigned ROW_VALUE=Terminal_entrata->ROW_pożizzjoni%Kronoloġija_linja_COUNT,karattru_VALUE=Terminal_entrata->글자칸들[ROW_VALUE][순번],forma_VALUE=Terminal_entrata->전경색|(Terminal_entrata->배경색<<4);
        /* 넓은 vi 화면에서도 이미 빈 칸의 font_VALUE 화소를 되풀이해 칠하지 않는다. */
        int 바뀜=(karattru_VALUE!=0&&karattru_VALUE!=' ')||Terminal_entrata->모양들[ROW_VALUE][순번]!=forma_VALUE;
        Terminal_entrata->글자칸들[ROW_VALUE][순번]=' ';Terminal_entrata->모양들[ROW_VALUE][순번]=forma_VALUE;
        if(바뀜)그리기(Terminal_entrata->ROW_pożizzjoni,순번);
    }}
    if(kodiċi_tal_karattru=='D')Terminal_entrata->COLUMN_pożizzjoni=element_COUNT>Terminal_entrata->COLUMN_pożizzjoni?0:Terminal_entrata->COLUMN_pożizzjoni-element_COUNT;if(kodiċi_tal_karattru=='C')Terminal_entrata->COLUMN_pożizzjoni=Terminal_entrata->COLUMN_pożizzjoni+element_COUNT>=Terminal_entrata->COLUMNS?Terminal_entrata->COLUMNS-1:Terminal_entrata->COLUMN_pożizzjoni+element_COUNT;
    if(kodiċi_tal_karattru=='G')Terminal_entrata->COLUMN_pożizzjoni=element_COUNT>Terminal_entrata->COLUMNS?Terminal_entrata->COLUMNS-1:element_COUNT-1;if(kodiċi_tal_karattru=='A')Terminal_entrata->ROW_pożizzjoni=element_COUNT>Terminal_entrata->ROW_pożizzjoni-Terminal_entrata->맨위?Terminal_entrata->맨위:Terminal_entrata->ROW_pożizzjoni-element_COUNT;
    if(kodiċi_tal_karattru=='B')Terminal_entrata->ROW_pożizzjoni=Terminal_entrata->ROW_pożizzjoni+element_COUNT>=Terminal_entrata->맨위+Terminal_entrata->ROW_COUNT?Terminal_entrata->맨위+Terminal_entrata->ROW_COUNT-1:Terminal_entrata->ROW_pożizzjoni+element_COUNT;
    if(kodiċi_tal_karattru=='H'||kodiċi_tal_karattru=='f'){Terminal_entrata->ROW_pożizzjoni=Terminal_entrata->맨위+(element_COUNT>Terminal_entrata->ROW_COUNT?Terminal_entrata->ROW_COUNT:element_COUNT)-1;unsigned koordinat_x=Terminal_entrata->매개값[1]?Terminal_entrata->매개값[1]:1;Terminal_entrata->COLUMN_pożizzjoni=(koordinat_x>Terminal_entrata->COLUMNS?Terminal_entrata->COLUMNS:koordinat_x)-1;}
    if(kodiċi_tal_karattru=='s'){Terminal_entrata->저장행=Terminal_entrata->ROW_pożizzjoni;Terminal_entrata->저장열=Terminal_entrata->COLUMN_pożizzjoni;}if(kodiċi_tal_karattru=='u'){Terminal_entrata->ROW_pożizzjoni=Terminal_entrata->저장행;Terminal_entrata->COLUMN_pożizzjoni=Terminal_entrata->저장열<Terminal_entrata->COLUMNS?Terminal_entrata->저장열:Terminal_entrata->COLUMNS-1;}
    if((kodiċi_tal_karattru=='h'||kodiċi_tal_karattru=='l')&&Terminal_entrata->매개값[0]==25)Terminal_entrata->가리개보임=kodiċi_tal_karattru=='h';
}
void Terminal_byte(unsigned SECOND_VALUE){
    Terminal_entrata=&Windows_Lista[출력결과];if(!Terminal_entrata->살아있음)return;kappell_VALUE(0);if(Terminal_entrata->skrollja){Terminal_entrata->skrollja=0;if(보이는지())Kontenut_VALUE();}
    if(Terminal_entrata->탈출상태==1){Terminal_entrata->탈출상태=SECOND_VALUE=='['?2:0;Terminal_entrata->매개색인=0;for(unsigned 순번=0;순번<4;순번++)Terminal_entrata->매개값[순번]=0;}
    else if(Terminal_entrata->탈출상태==2){if(SECOND_VALUE=='?'){}else if(SECOND_VALUE>='0'&&SECOND_VALUE<='9'){if(Terminal_entrata->매개값[Terminal_entrata->매개색인]<10000)Terminal_entrata->매개값[Terminal_entrata->매개색인]=Terminal_entrata->매개값[Terminal_entrata->매개색인]*10+SECOND_VALUE-'0';}else if(SECOND_VALUE==';'&&Terminal_entrata->매개색인<3)Terminal_entrata->매개색인++;else{handle_kontroll_SEQUENCE(SECOND_VALUE);Terminal_entrata->탈출상태=0;}}
    else if(SECOND_VALUE==27){Terminal_entrata->긴부호없는값=0;Terminal_entrata->탈출상태=1;}else{
        if(Terminal_entrata->긴부호없는값&&(SECOND_VALUE&0xc0)!=0x80){Terminal_entrata->긴부호없는값=0;kodiċi_tal_karattru_451f2815(0xfffd);}
        if(Terminal_entrata->긴부호없는값){Terminal_entrata->부호없는결과=Terminal_entrata->부호없는결과*64+(SECOND_VALUE&63);if(--Terminal_entrata->긴부호없는값==0)kodiċi_tal_karattru_451f2815(Terminal_entrata->부호없는결과<Terminal_entrata->SMALL_VALUE||Terminal_entrata->부호없는결과>0x10ffff||(Terminal_entrata->부호없는결과>=0xd800&&Terminal_entrata->부호없는결과<=0xdfff)?0xfffd:Terminal_entrata->부호없는결과);}
        else if(SECOND_VALUE<128)kodiċi_tal_karattru_451f2815(SECOND_VALUE);else if(SECOND_VALUE>=0xc2&&SECOND_VALUE<=0xf4){Terminal_entrata->긴부호없는값=SECOND_VALUE<0xe0?1:SECOND_VALUE<0xf0?2:3;Terminal_entrata->부호없는결과=SECOND_VALUE&((1u<<(6-Terminal_entrata->긴부호없는값))-1);Terminal_entrata->SMALL_VALUE=Terminal_entrata->긴부호없는값==1?128:Terminal_entrata->긴부호없는값==2?2048:65536;}else kodiċi_tal_karattru_451f2815(0xfffd);
    }kappell_VALUE(1);
}
int Terminal_pendenti(void){return 대기중!=0;}
/* 모서리 INDEX: 1 좌상, 2 우상, 3 좌하, 4 우하. */
static int rridimensjona_dreggja=-1,잡은모서리,잡은가로,잡은세로,처음가로,처음세로,처음너비,처음높이;
static int 가리킨창(int 가로,int Vertikali_pożizzjoni) {
    for(int SEQUENCE_VALUE=entrata_COUNT-1;SEQUENCE_VALUE>=0;SEQUENCE_VALUE--){
        int identifikatur_VALUE=ordni_VALUE[SEQUENCE_VALUE];Terminal_d413d4bc *tieqa=&Windows_Lista[identifikatur_VALUE];
        if(가로>=(int)tieqa->koordinat_x&&Vertikali_pożizzjoni>=(int)tieqa->세로좌표&&
           가로<(int)(tieqa->koordinat_x+tieqa->너비)&&Vertikali_pożizzjoni<(int)(tieqa->세로좌표+tieqa->높이))return identifikatur_VALUE;
    }return -1;
}
static int 모서리찾기(int identifikatur_VALUE,int 가로,int Vertikali_pożizzjoni) {
    if(identifikatur_VALUE<0)return 0;Terminal_d413d4bc *tieqa=&Windows_Lista[identifikatur_VALUE];
    int 왼쪽=가로<(int)tieqa->koordinat_x+8,RIGHT=가로>=(int)(tieqa->koordinat_x+tieqa->너비)-8;
    int 위쪽=Vertikali_pożizzjoni<(int)tieqa->세로좌표+8,아래쪽=Vertikali_pożizzjoni>=(int)(tieqa->세로좌표+tieqa->높이)-8;
    return (왼쪽||RIGHT)&&(위쪽||아래쪽)?1+RIGHT+아래쪽*2:0;
}
static int separatur_VALUE(int VALUE,int 최소,int 최대){return VALUE<최소?최소:VALUE>최대?최대:VALUE;}
static void mexxi_rridimensjona(int 가로,int Vertikali_pożizzjoni) {
    Terminal_d413d4bc *tieqa=&Windows_Lista[rridimensjona_dreggja];int 왼쪽=처음가로,위쪽=처음세로,RIGHT=처음가로+처음너비,아래쪽=처음세로+처음높이;
    if(잡은모서리==1||잡은모서리==3)왼쪽=separatur_VALUE(처음가로+가로-잡은가로,0,RIGHT-360);
    else RIGHT=separatur_VALUE(처음가로+처음너비+가로-잡은가로,왼쪽+360,보드화면너비());
    if(잡은모서리<=2)위쪽=separatur_VALUE(처음세로+Vertikali_pożizzjoni-잡은세로,34,아래쪽-216);
    else 아래쪽=separatur_VALUE(처음세로+처음높이+Vertikali_pożizzjoni-잡은세로,위쪽+216,보드화면높이());
    unsigned COLUMNS=(RIGHT-왼쪽-24)/8,ROW_COUNT=(아래쪽-위쪽-56)/16;
    if(tieqa->COLUMNS!=COLUMNS||tieqa->ROW_COUNT!=ROW_COUNT){
        tieqa->크기바뀜=1;tieqa->COLUMNS=COLUMNS;tieqa->ROW_COUNT=ROW_COUNT;
        if(tieqa->COLUMN_pożizzjoni>=COLUMNS)tieqa->COLUMN_pożizzjoni=COLUMNS-1;
        if(tieqa->ROW_pożizzjoni>=tieqa->맨위+ROW_COUNT)tieqa->맨위=tieqa->ROW_pożizzjoni-ROW_COUNT+1;
        unsigned 한도=tieqa->맨위;if(한도>Kronoloġija_linja_COUNT-ROW_COUNT)한도=Kronoloġija_linja_COUNT-ROW_COUNT;
        if(tieqa->skrollja>한도)tieqa->skrollja=한도;
    }
    int 옛가로=tieqa->koordinat_x,옛세로=tieqa->세로좌표,옛폭=tieqa->너비,옛길이=tieqa->높이;
    if(옛가로==왼쪽&&옛세로==위쪽&&옛폭==RIGHT-왼쪽&&옛길이==아래쪽-위쪽)return;
    tieqa->koordinat_x=왼쪽;tieqa->세로좌표=위쪽;tieqa->너비=RIGHT-왼쪽;tieqa->높이=아래쪽-위쪽;
    창자리그리기(옛가로,옛세로,옛폭,옛길이,tieqa);
}
void Terminal_pointer(unsigned Li_Jmiss_element,int koordinat_x,int 세로좌표){
    unsigned 눌림=Li_Jmiss_element&~단추들;단추들=Li_Jmiss_element;
    if(!desktop_wera){dreggja_VALUE=-1;rridimensjona_dreggja=-1;bord_pointer(koordinat_x,세로좌표,1);return;}
    if(!(Li_Jmiss_element&1)){dreggja_VALUE=-1;rridimensjona_dreggja=-1;}
    if(rridimensjona_dreggja>=0&&!Windows_Lista[rridimensjona_dreggja].살아있음)rridimensjona_dreggja=-1;
    if(dreggja_VALUE>=0&&!Windows_Lista[dreggja_VALUE].살아있음)dreggja_VALUE=-1;
    if(rridimensjona_dreggja>=0){
        mexxi_rridimensjona(koordinat_x,세로좌표);bord_pointer(koordinat_x,세로좌표,잡은모서리==1||잡은모서리==4?2:3);return;
    }
    bord_pointer(koordinat_x,세로좌표,1);
    if(dreggja_VALUE>=0){
        Terminal_d413d4bc *tieqa=&Windows_Lista[dreggja_VALUE];
        int 옛가로=tieqa->koordinat_x,옛세로=tieqa->세로좌표;
        tieqa->koordinat_x=separatur_VALUE(koordinat_x-끌기가로,0,보드화면너비()-tieqa->너비);
        tieqa->세로좌표=separatur_VALUE(세로좌표-끌기세로,34,보드화면높이()-tieqa->높이);
        if(옛가로!=(int)tieqa->koordinat_x||옛세로!=(int)tieqa->세로좌표)창자리그리기(옛가로,옛세로,tieqa->너비,tieqa->높이,tieqa);
        return;
    }
    extern int 화면덮음(int,int,int);
    if(화면덮음(Fokus,koordinat_x,세로좌표)){화면가리킴(Fokus,눌림,koordinat_x,세로좌표);return;}
    int identifikatur_VALUE=가리킨창(koordinat_x,세로좌표),모서리=모서리찾기(identifikatur_VALUE,koordinat_x,세로좌표);
    if(모서리)bord_pointer(koordinat_x,세로좌표,모서리==1||모서리==4?2:3);
    if(눌림&1){
        if(모서리){
            Terminal_d413d4bc *tieqa=&Windows_Lista[identifikatur_VALUE];rridimensjona_dreggja=identifikatur_VALUE;잡은모서리=모서리;잡은가로=koordinat_x;잡은세로=세로좌표;
            처음가로=tieqa->koordinat_x;처음세로=tieqa->세로좌표;처음너비=tieqa->너비;처음높이=tieqa->높이;
            if(identifikatur_VALUE!=Fokus)앞으로올리기(identifikatur_VALUE);return;
        }
        if(세로좌표<32&&koordinat_x>=6&&koordinat_x<142){ħalaq_entrata();return;}
        if(세로좌표<32&&koordinat_x>=154&&koordinat_x<602){앞으로올리기((koordinat_x-154)/112);return;}
        if(identifikatur_VALUE>=0){
            Terminal_d413d4bc *tieqa=&Windows_Lista[identifikatur_VALUE];
            if(세로좌표<(int)tieqa->세로좌표+30&&koordinat_x>=(int)(tieqa->koordinat_x+tieqa->너비)-32){agħlaq_tieqa(identifikatur_VALUE);return;}
            if(identifikatur_VALUE!=Fokus)앞으로올리기(identifikatur_VALUE);
            if(세로좌표<(int)tieqa->세로좌표+30){dreggja_VALUE=identifikatur_VALUE;끌기가로=koordinat_x-tieqa->koordinat_x;끌기세로=세로좌표-tieqa->세로좌표;}return;
        }
    }
    if(Fokus>=0&&(눌림&(8|16))){Terminal_entrata=&Windows_Lista[Fokus];if(눌림&8){unsigned 한도=Terminal_entrata->맨위;if(한도>Kronoloġija_linja_COUNT-Terminal_entrata->ROW_COUNT)한도=Kronoloġija_linja_COUNT-Terminal_entrata->ROW_COUNT;Terminal_entrata->skrollja=Terminal_entrata->skrollja+9>한도?한도:Terminal_entrata->skrollja+9;}else Terminal_entrata->skrollja=Terminal_entrata->skrollja<9?0:Terminal_entrata->skrollja-9;다시그리기();}
}
void 터미널바로가기키(unsigned 누름값){if(누름값==1)ħalaq_entrata();if(누름값==2&&entrata_COUNT)앞으로올리기(ordni_VALUE[0]);if(누름값==3)agħlaq_tieqa(Fokus);}
kompjuter_Word bord_Terminal(kompjuter_Word azzjoni){
    if(azzjoni==300){if(!Windows_Lista[출력결과].살아있음)return ħalaq_entrata();desktop_wera=1;다시그리기();return 0;}
    if(azzjoni==0){agħlaq_tieqa(Fokus);return 0;}if(azzjoni==1)return (uint32_t)ħalaq_entrata();if(azzjoni==2)return Fokus>=0;
    if(azzjoni==9){desktop_wera=0;return 0;}if(azzjoni==7)return entrata_COUNT;if(azzjoni==10)return Fokus+1;if(azzjoni==11)return 출력결과;
    if(azzjoni==13){Terminal_d413d4bc *tieqa=&Windows_Lista[출력결과];return tieqa->살아있음?(tieqa->ROW_COUNT<<16)|tieqa->COLUMNS:(19<<16)|68;}
    if(azzjoni==14){unsigned VALUE=Windows_Lista[출력결과].크기바뀜;Windows_Lista[출력결과].크기바뀜=0;return VALUE;}
    if(azzjoni==12){unsigned VALUE=대기중;대기중=0;return VALUE;}
    if(azzjoni>=20&&azzjoni<24)return Windows_Lista[azzjoni-20].살아있음;
    if(azzjoni>=100&&azzjoni<104){출력결과=azzjoni-100;Terminal_entrata=&Windows_Lista[출력결과];return 0;}
    if(azzjoni>=200&&azzjoni<204){앞으로올리기(azzjoni-200);return 0;}
    if(azzjoni==3){다시그리기();return 0;}Terminal_entrata=&Windows_Lista[출력결과];if(!Terminal_entrata->살아있음)return 0;
    if(azzjoni==4)neħħa_TOC();if(azzjoni==5||azzjoni==6){unsigned 이전=단추들;Terminal_pointer(azzjoni==5?8:16,0,0);단추들=이전;}return 1;
}
