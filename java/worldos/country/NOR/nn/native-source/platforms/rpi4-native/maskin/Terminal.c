#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* 자체 네 vindauge 합성과 UTF-8 Terminal. 바뀐 영역의 완성 그림만 표시한다. */
#include <stdint.h>
#include <stddef.h>
typedef uintptr_t maskin_Word;
extern maskin_Word Tavle_piksel(maskin_Word,maskin_Word,maskin_Word),보드화면기억공간(void);
extern void *memset(void *,int,size_t);
extern const unsigned char Terminal_skrift[];
#define 최대열수 237
#define Logg_line_COUNT 160
typedef struct {
    uint32_t 글자칸들[Logg_line_COUNT][최대열수]; uint8_t 모양들[Logg_line_COUNT][최대열수];
    unsigned 너비,높이,COLUMNS,ROW_COUNT,크기바뀜;
    unsigned 살아있음,x_koordinat,Y_koordinat,ROW_plassere,COLUMN_plassere,맨위,rulle,전경색,배경색,탈출상태,parameter_VALUE[4],parameter_INDEX,저장행,저장열;
    unsigned 부호없는결과,긴부호없는값,SMALL_VALUE,대체화면,가리개보임;
} Terminal_d413d4bc;
static Terminal_d413d4bc Windows_Liste[4];
static int Fokus=-1,출력결과,rekkjefølgje_VALUE[4],oppføring_COUNT,dra_VALUE=-1,dra_X,dra_Y;
static unsigned informasjonsteknologi_ventande,단추들,stasjonær_vise,한글입력;
static const uint32_t 색상들[16]={0x201a15,0x6060df,0x9dcc86,0x80cfea,0xefaf72,0xca96c9,0xceda76,0xede9df,0x858078,0x8888ff,0xb9eba7,0xa5eaff,0xffcc99,0xf0bef1,0xf0f0a0,0xffffff};
extern int 화면보임(int),화면가리킴(int,unsigned,int,int);
extern void 화면다시그림(int);
static Terminal_d413d4bc *Terminal_oppføring;
static unsigned 넓은글자(unsigned teiknkode){return teiknkode>=256?2:1;}
static void 사각영역(unsigned x_koordinat,unsigned Y_koordinat,unsigned 너비값,unsigned 높이값,unsigned 색상){
    보드사각그림(x_koordinat,Y_koordinat,너비값,높이값,색상);
}
void Terminal_figur(unsigned x_koordinat,unsigned Y_koordinat,unsigned teiknkode,unsigned 전경색,unsigned 배경색){
    unsigned 너비=넓은글자(teiknkode)*8;if(teiknkode==0xffffffffu)return;
    int 왼쪽=x_koordinat,위쪽=Y_koordinat,폭=너비,lengd_VALUE=16;
    if(!보드그림범위(&왼쪽,&위쪽,&폭,&lengd_VALUE))return;
    if(teiknkode==' '){보드사각그림(왼쪽,위쪽,폭,lengd_VALUE,배경색);return;}
    unsigned LOOKUP_INDEX=teiknkode<65536?teiknkode:teiknkode>=0x1f600&&teiknkode<0x1f650?65536+teiknkode-0x1f600:0xfffd;
    const unsigned char *skrift_VALUE=Terminal_skrift+LOOKUP_INDEX*32;
    for(int linje=위쪽;linje<위쪽+lengd_VALUE;linje++){unsigned 비트들=skrift_VALUE[(linje-Y_koordinat)*2]*256+skrift_VALUE[(linje-Y_koordinat)*2+1];for(int felt_oppføring=왼쪽;felt_oppføring<왼쪽+폭;felt_oppføring++)Tavle_piksel(felt_oppføring,linje,(비트들&(0x8000>>(felt_oppføring-x_koordinat)))?전경색:배경색);}
}
static void namn_tabell(unsigned x_koordinat,unsigned Y_koordinat,const char *streng_data,unsigned 전경색,unsigned 배경색){while(*streng_data){unsigned teiknkode=(unsigned char)*streng_data++, 남은수=0;if(teiknkode>=0xc0){남은수=teiknkode<0xe0?1:teiknkode<0xf0?2:3;teiknkode&=(1u<<(6-남은수))-1;while(남은수--&&*streng_data)teiknkode=(teiknkode<<6)|((unsigned char)*streng_data++&63);}Terminal_figur(x_koordinat,Y_koordinat,teiknkode,전경색,배경색);x_koordinat+=넓은글자(teiknkode)*8;}}
static unsigned 첫항목(void){return Terminal_oppføring->맨위;}
static int 보이는지(void){return Terminal_oppføring->살아있음&&Fokus>=0&&Terminal_oppføring==&Windows_Liste[Fokus]&&!화면보임(Fokus);}
static void 그리기(unsigned ROW_plassere,unsigned COLUMN_plassere){
    if(!보이는지()||ROW_plassere<첫항목()-Terminal_oppføring->rulle||ROW_plassere>=첫항목()-Terminal_oppføring->rulle+Terminal_oppføring->ROW_COUNT||COLUMN_plassere>=Terminal_oppføring->COLUMNS)return;
    unsigned teiknkode=Terminal_oppføring->글자칸들[ROW_plassere%Logg_line_COUNT][COLUMN_plassere],streng_data=Terminal_oppføring->모양들[ROW_plassere%Logg_line_COUNT][COLUMN_plassere];
    if(넓은글자(teiknkode)==2&&COLUMN_plassere+1>=Terminal_oppføring->COLUMNS)teiknkode=' ';
    Terminal_figur(Terminal_oppføring->x_koordinat+12+COLUMN_plassere*8,Terminal_oppføring->Y_koordinat+36+(ROW_plassere-첫항목()+Terminal_oppføring->rulle)*16,teiknkode?teiknkode:' ',색상들[streng_data&15],색상들[streng_data>>4]);
}
static void cirkumfleks_VALUE(int vise_vindauge){if(!보이는지()||Terminal_oppføring->rulle||Terminal_oppføring->COLUMN_plassere>=Terminal_oppføring->COLUMNS||Terminal_oppføring->ROW_plassere<Terminal_oppføring->맨위||Terminal_oppføring->ROW_plassere>=Terminal_oppføring->맨위+Terminal_oppføring->ROW_COUNT)return;
    if(!vise_vindauge||!Terminal_oppføring->가리개보임)그리기(Terminal_oppføring->ROW_plassere,Terminal_oppføring->COLUMN_plassere);else 사각영역(Terminal_oppføring->x_koordinat+12+Terminal_oppføring->COLUMN_plassere*8,Terminal_oppføring->Y_koordinat+36+(Terminal_oppføring->ROW_plassere-Terminal_oppføring->맨위)*16+14,8,2,색상들[Terminal_oppføring->전경색]);}
static void Innhald_VALUE(void){
    사각영역(Terminal_oppføring->x_koordinat+12,Terminal_oppføring->Y_koordinat+36,Terminal_oppføring->COLUMNS*8,Terminal_oppføring->ROW_COUNT*16,색상들[0]);
    int 가로=Terminal_oppføring->x_koordinat+12,vertikalvising_plassere=Terminal_oppføring->Y_koordinat+36,폭=Terminal_oppføring->COLUMNS*8,lengd_VALUE=Terminal_oppføring->ROW_COUNT*16;
    if(보드그림범위(&가로,&vertikalvising_plassere,&폭,&lengd_VALUE)){
    unsigned 첫줄=(vertikalvising_plassere-Terminal_oppføring->Y_koordinat-36)/16,끝줄=(vertikalvising_plassere+lengd_VALUE-Terminal_oppføring->Y_koordinat-36+15)/16;
    unsigned 첫칸=(가로-Terminal_oppføring->x_koordinat-12)/8,끝칸=(가로+폭-Terminal_oppføring->x_koordinat-12+7)/8;
    if(첫칸)첫칸--; /* 잘림 경계 왼쪽에서 시작한 두 felt_oppføring 글자도 그린다. */
    for(unsigned 반환값=첫줄;반환값<끝줄;반환값++)for(unsigned teiknkode=첫칸;teiknkode<끝칸;teiknkode++){
        unsigned ROW_plassere=첫항목()-Terminal_oppføring->rulle+반환값,teikn_VALUE=Terminal_oppføring->글자칸들[ROW_plassere%Logg_line_COUNT][teiknkode],streng_data=Terminal_oppføring->모양들[ROW_plassere%Logg_line_COUNT][teiknkode];
        if(넓은글자(teikn_VALUE)==2&&teiknkode+1>=Terminal_oppføring->COLUMNS)teikn_VALUE=' ';
        if((teikn_VALUE==0||teikn_VALUE==' ')&&(streng_data>>4)==0)continue;
        Terminal_figur(Terminal_oppføring->x_koordinat+12+teiknkode*8,Terminal_oppføring->Y_koordinat+36+반환값*16,teikn_VALUE?teikn_VALUE:' ',색상들[streng_data&15],색상들[streng_data>>4]);
    }}
    namn_tabell(Terminal_oppføring->x_koordinat+12,Terminal_oppføring->Y_koordinat+Terminal_oppføring->높이-18,Terminal_oppføring->rulle?"PgDn: recent output":Terminal_oppføring->너비>=500?"F6: next | Corner + left drag: resize":"Corner + left drag: resize",0xece8e2,0x403127);cirkumfleks_VALUE(1);
}
static void 실행틀(int identifikator_VALUE){
    Terminal_oppføring=&Windows_Liste[identifikator_VALUE];
    int 가로=Terminal_oppføring->x_koordinat,vertikalvising_plassere=Terminal_oppføring->Y_koordinat,폭=Terminal_oppføring->너비,lengd_VALUE=Terminal_oppføring->높이;
    if(!보드그림범위(&가로,&vertikalvising_plassere,&폭,&lengd_VALUE))return;
    사각영역(Terminal_oppføring->x_koordinat,Terminal_oppføring->Y_koordinat,Terminal_oppføring->너비,Terminal_oppføring->높이,0x403127);
    unsigned 색상=identifikator_VALUE==Fokus?0x905020:0x604438;사각영역(Terminal_oppføring->x_koordinat,Terminal_oppføring->Y_koordinat,Terminal_oppføring->너비,30,색상);
    namn_tabell(Terminal_oppføring->x_koordinat+12,Terminal_oppføring->Y_koordinat+7,"JKOROS Terminal",0xffffff,색상);
    char 수치[2]={(char)('1'+identifikator_VALUE),0};namn_tabell(Terminal_oppføring->x_koordinat+148,Terminal_oppføring->Y_koordinat+7,수치,0xffffff,색상);
    namn_tabell(Terminal_oppføring->x_koordinat+240,Terminal_oppføring->Y_koordinat+7,Terminal_oppføring->너비>=500?(한글입력?"[NN] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[NN]":"[EN]"),0xffffff,색상);
    사각영역(Terminal_oppføring->x_koordinat+Terminal_oppføring->너비-32,Terminal_oppføring->Y_koordinat+4,26,22,0x5555b8);namn_tabell(Terminal_oppføring->x_koordinat+Terminal_oppføring->너비-24,Terminal_oppføring->Y_koordinat+7,"X",0xffffff,0x5555b8);
    Innhald_VALUE();
}
static void 장면그리기(void){
    if(!stasjonær_vise)return;사각영역(0,0,보드화면너비(),보드화면높이(),0x302018);사각영역(0,0,보드화면너비(),32,0x403127);
    사각영역(6,4,136,24,0x905020);namn_tabell(14,8,"+ New terminal",0xffffff,0x905020);
    for(int 순번=0;순번<4;순번++)if(Windows_Liste[순번].살아있음){unsigned teiknkode=Fokus==순번?0x905020:0x604438;사각영역(154+순번*112,4,106,24,teiknkode);namn_tabell(160+순번*112,8,"Terminal",0xffffff,teiknkode);char streng_data[2]={(char)('1'+순번),0};namn_tabell(232+순번*112,8,streng_data,0xffffff,teiknkode);}
    if(!oppføring_COUNT)namn_tabell(140,210,"Click + New terminal to start",0xede9df,0x302018);
    for(int 순번=0;순번<oppføring_COUNT;순번++)실행틀(rekkjefølgje_VALUE[순번]);화면다시그림(Fokus);Terminal_oppføring=&Windows_Liste[출력결과];
}
static void 영역그리기(int 가로,int vertikalvising_plassere,int 폭,int lengd_VALUE){
    if(!stasjonær_vise||!보드그림범위(&가로,&vertikalvising_plassere,&폭,&lengd_VALUE))return;
    for(int linje=vertikalvising_plassere;linje<vertikalvising_plassere+lengd_VALUE;linje+=32){
        int 띠높이=vertikalvising_plassere+lengd_VALUE-linje;if(띠높이>32)띠높이=32;
        if(Tavle_START_teikning(가로,linje,폭,띠높이)){장면그리기();Tavle_Ferdig_teikning();}
    }
}
static void 다시그리기(void){영역그리기(0,0,보드화면너비(),보드화면높이());}
/* 서로 겹치지 않는 새 vindauge 영역과 이전 자리의 네 띠를 복구한다. */
static void 창자리그리기(int 가로,int vertikalvising_plassere,int 폭,int lengd_VALUE,Terminal_d413d4bc *vindauge){
    int 왼쪽=가로>(int)vindauge->x_koordinat?가로:(int)vindauge->x_koordinat;
    int 위쪽=vertikalvising_plassere>(int)vindauge->Y_koordinat?vertikalvising_plassere:(int)vindauge->Y_koordinat;
    int RIGHT=가로+폭<(int)(vindauge->x_koordinat+vindauge->너비)?가로+폭:(int)(vindauge->x_koordinat+vindauge->너비);
    int 아래쪽=vertikalvising_plassere+lengd_VALUE<(int)(vindauge->Y_koordinat+vindauge->높이)?vertikalvising_plassere+lengd_VALUE:(int)(vindauge->Y_koordinat+vindauge->높이);
    영역그리기(vindauge->x_koordinat,vindauge->Y_koordinat,vindauge->너비,vindauge->높이);
    if(왼쪽>=RIGHT||위쪽>=아래쪽){영역그리기(가로,vertikalvising_plassere,폭,lengd_VALUE);return;}
    영역그리기(가로,vertikalvising_plassere,폭,위쪽-vertikalvising_plassere);
    영역그리기(가로,아래쪽,폭,vertikalvising_plassere+lengd_VALUE-아래쪽);
    영역그리기(가로,위쪽,왼쪽-가로,아래쪽-위쪽);
    영역그리기(RIGHT,위쪽,가로+폭-RIGHT,아래쪽-위쪽);
}
static void 초점알리기(void){informasjonsteknologi_ventande=(informasjonsteknologi_ventande&~15u)|(unsigned)(Fokus+1)|0x10000;}
void 터미널입력방식(unsigned 한글여부){
    한글입력=한글여부!=0;
    /* Update title bars only: a mode switch must not erase an EL0 drawing. */
    if(Fokus>=0){
        Terminal_d413d4bc *vindauge_oppføring=&Windows_Liste[Fokus];
        namn_tabell(vindauge_oppføring->x_koordinat+240,vindauge_oppføring->Y_koordinat+7,vindauge_oppføring->너비>=500?(한글입력?"[NN] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[NN]":"[EN]"),0xffffff,0x905020);
    }
}
static void 앞으로올리기(int identifikator_VALUE){if(identifikator_VALUE<0||identifikator_VALUE>=4||!Windows_Liste[identifikator_VALUE].살아있음)return;int betalt_plassere=0;while(betalt_plassere<oppføring_COUNT&&rekkjefølgje_VALUE[betalt_plassere]!=identifikator_VALUE)betalt_plassere++;for(;betalt_plassere+1<oppføring_COUNT;betalt_plassere++)rekkjefølgje_VALUE[betalt_plassere]=rekkjefølgje_VALUE[betalt_plassere+1];rekkjefølgje_VALUE[oppføring_COUNT-1]=identifikator_VALUE;Fokus=identifikator_VALUE;초점알리기();다시그리기();}
static void 빈칸채우기(unsigned ROW_plassere){for(unsigned teiknkode=0;teiknkode<최대열수;teiknkode++){Terminal_oppføring->글자칸들[ROW_plassere%Logg_line_COUNT][teiknkode]=0;Terminal_oppføring->모양들[ROW_plassere%Logg_line_COUNT][teiknkode]=Terminal_oppføring->전경색|(Terminal_oppføring->배경색<<4);}}
static void fjerne_Innhald(void){Terminal_oppføring->ROW_plassere=Terminal_oppføring->COLUMN_plassere=Terminal_oppføring->맨위=Terminal_oppføring->rulle=0;for(unsigned 반환값=0;반환값<Logg_line_COUNT;반환값++)빈칸채우기(반환값);if(보이는지())Innhald_VALUE();}
static int Opprett_oppføring(void){
    if(!보드화면기억공간())return -19;int identifikator_VALUE=0;while(identifikator_VALUE<4&&Windows_Liste[identifikator_VALUE].살아있음)identifikator_VALUE++;if(identifikator_VALUE==4)return -28;
    stasjonær_vise=1;Terminal_oppføring=&Windows_Liste[identifikator_VALUE];memset(Terminal_oppføring,0,sizeof(*Terminal_oppføring));Terminal_oppføring->살아있음=1;Terminal_oppføring->너비=568;Terminal_oppføring->높이=360;Terminal_oppføring->COLUMNS=68;Terminal_oppføring->ROW_COUNT=19;Terminal_oppføring->x_koordinat=12+identifikator_VALUE*16;Terminal_oppføring->Y_koordinat=48+identifikator_VALUE*18;Terminal_oppføring->전경색=7;Terminal_oppføring->가리개보임=1;
    for(unsigned 반환값=0;반환값<Logg_line_COUNT;반환값++)빈칸채우기(반환값);rekkjefølgje_VALUE[oppføring_COUNT++]=identifikator_VALUE;Fokus=identifikator_VALUE;informasjonsteknologi_ventande|=1u<<(4+identifikator_VALUE);초점알리기();다시그리기();return identifikator_VALUE+1;
}
static void Lukk_vindauge(int identifikator_VALUE){
    if(identifikator_VALUE<0||identifikator_VALUE>=4||!Windows_Liste[identifikator_VALUE].살아있음)return;Windows_Liste[identifikator_VALUE].살아있음=0;informasjonsteknologi_ventande|=1u<<(8+identifikator_VALUE);
    int betalt_plassere=0;while(betalt_plassere<oppføring_COUNT&&rekkjefølgje_VALUE[betalt_plassere]!=identifikator_VALUE)betalt_plassere++;for(;betalt_plassere+1<oppføring_COUNT;betalt_plassere++)rekkjefølgje_VALUE[betalt_plassere]=rekkjefølgje_VALUE[betalt_plassere+1];oppføring_COUNT--;
    if(Fokus==identifikator_VALUE)Fokus=oppføring_COUNT?rekkjefølgje_VALUE[oppføring_COUNT-1]:-1;초점알리기();다시그리기();
}
static void 줄바꿈(void){Terminal_oppføring->COLUMN_plassere=0;Terminal_oppføring->ROW_plassere++;if(Terminal_oppføring->ROW_plassere>=Terminal_oppføring->맨위+Terminal_oppføring->ROW_COUNT){Terminal_oppføring->맨위++;빈칸채우기(Terminal_oppføring->ROW_plassere);if(보이는지())Innhald_VALUE();}}
static void teiknkode_451f2815(unsigned teiknkode){
    if(teiknkode==13){Terminal_oppføring->COLUMN_plassere=0;return;}if(teiknkode==10){줄바꿈();return;}if(teiknkode==8){if(Terminal_oppføring->COLUMN_plassere)Terminal_oppføring->COLUMN_plassere--;return;}
    if(teiknkode==9){unsigned vare_COUNT=8-Terminal_oppføring->COLUMN_plassere%8;while(vare_COUNT--)teiknkode_451f2815(' ');return;}if(teiknkode<32||teiknkode==127)return;
    unsigned 너비값=넓은글자(teiknkode);if(Terminal_oppføring->COLUMN_plassere+너비값>Terminal_oppføring->COLUMNS)줄바꿈();
    if(Terminal_oppføring->글자칸들[Terminal_oppføring->ROW_plassere%Logg_line_COUNT][Terminal_oppføring->COLUMN_plassere]==0xffffffffu&&Terminal_oppføring->COLUMN_plassere){Terminal_oppføring->글자칸들[Terminal_oppføring->ROW_plassere%Logg_line_COUNT][Terminal_oppføring->COLUMN_plassere-1]=' ';그리기(Terminal_oppføring->ROW_plassere,Terminal_oppføring->COLUMN_plassere-1);}
    if(넓은글자(Terminal_oppføring->글자칸들[Terminal_oppføring->ROW_plassere%Logg_line_COUNT][Terminal_oppføring->COLUMN_plassere])==2&&Terminal_oppføring->COLUMN_plassere+1<Terminal_oppføring->COLUMNS){Terminal_oppføring->글자칸들[Terminal_oppføring->ROW_plassere%Logg_line_COUNT][Terminal_oppføring->COLUMN_plassere+1]=' ';그리기(Terminal_oppføring->ROW_plassere,Terminal_oppføring->COLUMN_plassere+1);}
    Terminal_oppføring->글자칸들[Terminal_oppføring->ROW_plassere%Logg_line_COUNT][Terminal_oppføring->COLUMN_plassere]=teiknkode;Terminal_oppføring->모양들[Terminal_oppføring->ROW_plassere%Logg_line_COUNT][Terminal_oppføring->COLUMN_plassere]=Terminal_oppføring->전경색|(Terminal_oppføring->배경색<<4);
    if(너비값==2)Terminal_oppføring->글자칸들[Terminal_oppføring->ROW_plassere%Logg_line_COUNT][Terminal_oppføring->COLUMN_plassere+1]=0xffffffffu;
    그리기(Terminal_oppføring->ROW_plassere,Terminal_oppføring->COLUMN_plassere);Terminal_oppføring->COLUMN_plassere+=너비값;
}
static void handtak_styring_SEQUENCE(unsigned teiknkode){
    unsigned vare_COUNT=Terminal_oppføring->parameter_VALUE[0]?Terminal_oppføring->parameter_VALUE[0]:1;
    if(teiknkode=='m')for(unsigned 순번=0;순번<=Terminal_oppføring->parameter_INDEX;순번++){unsigned data_plassere=Terminal_oppføring->parameter_VALUE[순번];if(!data_plassere){Terminal_oppføring->전경색=7;Terminal_oppføring->배경색=0;}if(data_plassere==1&&Terminal_oppføring->전경색<8)Terminal_oppføring->전경색+=8;if(data_plassere==7){unsigned 유지=Terminal_oppføring->전경색;Terminal_oppføring->전경색=Terminal_oppføring->배경색;Terminal_oppføring->배경색=유지;}if(data_plassere>=30&&data_plassere<=37)Terminal_oppføring->전경색=data_plassere-30;if(data_plassere>=90&&data_plassere<=97)Terminal_oppføring->전경색=data_plassere-90+8;if(data_plassere>=40&&data_plassere<=47)Terminal_oppføring->배경색=data_plassere-40;if(data_plassere>=100&&data_plassere<=107)Terminal_oppføring->배경색=data_plassere-100+8;if(data_plassere==39)Terminal_oppføring->전경색=7;if(data_plassere==49)Terminal_oppføring->배경색=0;}
    if(teiknkode=='J'&&(Terminal_oppføring->parameter_VALUE[0]==2||Terminal_oppføring->parameter_VALUE[0]==3))fjerne_Innhald();
    if(teiknkode=='K'){unsigned 출발위치=Terminal_oppføring->parameter_VALUE[0]==2?0:Terminal_oppføring->COLUMN_plassere,도착위치=Terminal_oppføring->parameter_VALUE[0]==1?Terminal_oppføring->COLUMN_plassere+1:Terminal_oppføring->COLUMNS;if(Terminal_oppføring->parameter_VALUE[0]==1)출발위치=0;for(unsigned 순번=출발위치;순번<도착위치&&순번<Terminal_oppføring->COLUMNS;순번++){
        unsigned ROW_VALUE=Terminal_oppføring->ROW_plassere%Logg_line_COUNT,teikn_VALUE=Terminal_oppføring->글자칸들[ROW_VALUE][순번],figur_VALUE=Terminal_oppføring->전경색|(Terminal_oppføring->배경색<<4);
        /* 넓은 vi 화면에서도 이미 빈 칸의 skrift_VALUE 화소를 되풀이해 칠하지 않는다. */
        int 바뀜=(teikn_VALUE!=0&&teikn_VALUE!=' ')||Terminal_oppføring->모양들[ROW_VALUE][순번]!=figur_VALUE;
        Terminal_oppføring->글자칸들[ROW_VALUE][순번]=' ';Terminal_oppføring->모양들[ROW_VALUE][순번]=figur_VALUE;
        if(바뀜)그리기(Terminal_oppføring->ROW_plassere,순번);
    }}
    if(teiknkode=='D')Terminal_oppføring->COLUMN_plassere=vare_COUNT>Terminal_oppføring->COLUMN_plassere?0:Terminal_oppføring->COLUMN_plassere-vare_COUNT;if(teiknkode=='C')Terminal_oppføring->COLUMN_plassere=Terminal_oppføring->COLUMN_plassere+vare_COUNT>=Terminal_oppføring->COLUMNS?Terminal_oppføring->COLUMNS-1:Terminal_oppføring->COLUMN_plassere+vare_COUNT;
    if(teiknkode=='G')Terminal_oppføring->COLUMN_plassere=vare_COUNT>Terminal_oppføring->COLUMNS?Terminal_oppføring->COLUMNS-1:vare_COUNT-1;if(teiknkode=='A')Terminal_oppføring->ROW_plassere=vare_COUNT>Terminal_oppføring->ROW_plassere-Terminal_oppføring->맨위?Terminal_oppføring->맨위:Terminal_oppføring->ROW_plassere-vare_COUNT;
    if(teiknkode=='B')Terminal_oppføring->ROW_plassere=Terminal_oppføring->ROW_plassere+vare_COUNT>=Terminal_oppføring->맨위+Terminal_oppføring->ROW_COUNT?Terminal_oppføring->맨위+Terminal_oppføring->ROW_COUNT-1:Terminal_oppføring->ROW_plassere+vare_COUNT;
    if(teiknkode=='H'||teiknkode=='f'){Terminal_oppføring->ROW_plassere=Terminal_oppføring->맨위+(vare_COUNT>Terminal_oppføring->ROW_COUNT?Terminal_oppføring->ROW_COUNT:vare_COUNT)-1;unsigned x_koordinat=Terminal_oppføring->parameter_VALUE[1]?Terminal_oppføring->parameter_VALUE[1]:1;Terminal_oppføring->COLUMN_plassere=(x_koordinat>Terminal_oppføring->COLUMNS?Terminal_oppføring->COLUMNS:x_koordinat)-1;}
    if(teiknkode=='s'){Terminal_oppføring->저장행=Terminal_oppføring->ROW_plassere;Terminal_oppføring->저장열=Terminal_oppføring->COLUMN_plassere;}if(teiknkode=='u'){Terminal_oppføring->ROW_plassere=Terminal_oppføring->저장행;Terminal_oppføring->COLUMN_plassere=Terminal_oppføring->저장열<Terminal_oppføring->COLUMNS?Terminal_oppføring->저장열:Terminal_oppføring->COLUMNS-1;}
    if((teiknkode=='h'||teiknkode=='l')&&Terminal_oppføring->parameter_VALUE[0]==25)Terminal_oppføring->가리개보임=teiknkode=='h';
}
void Terminal_byte(unsigned SECOND_VALUE){
    Terminal_oppføring=&Windows_Liste[출력결과];if(!Terminal_oppføring->살아있음)return;cirkumfleks_VALUE(0);if(Terminal_oppføring->rulle){Terminal_oppføring->rulle=0;if(보이는지())Innhald_VALUE();}
    if(Terminal_oppføring->탈출상태==1){Terminal_oppføring->탈출상태=SECOND_VALUE=='['?2:0;Terminal_oppføring->parameter_INDEX=0;for(unsigned 순번=0;순번<4;순번++)Terminal_oppføring->parameter_VALUE[순번]=0;}
    else if(Terminal_oppføring->탈출상태==2){if(SECOND_VALUE=='?'){}else if(SECOND_VALUE>='0'&&SECOND_VALUE<='9'){if(Terminal_oppføring->parameter_VALUE[Terminal_oppføring->parameter_INDEX]<10000)Terminal_oppføring->parameter_VALUE[Terminal_oppføring->parameter_INDEX]=Terminal_oppføring->parameter_VALUE[Terminal_oppføring->parameter_INDEX]*10+SECOND_VALUE-'0';}else if(SECOND_VALUE==';'&&Terminal_oppføring->parameter_INDEX<3)Terminal_oppføring->parameter_INDEX++;else{handtak_styring_SEQUENCE(SECOND_VALUE);Terminal_oppføring->탈출상태=0;}}
    else if(SECOND_VALUE==27){Terminal_oppføring->긴부호없는값=0;Terminal_oppføring->탈출상태=1;}else{
        if(Terminal_oppføring->긴부호없는값&&(SECOND_VALUE&0xc0)!=0x80){Terminal_oppføring->긴부호없는값=0;teiknkode_451f2815(0xfffd);}
        if(Terminal_oppføring->긴부호없는값){Terminal_oppføring->부호없는결과=Terminal_oppføring->부호없는결과*64+(SECOND_VALUE&63);if(--Terminal_oppføring->긴부호없는값==0)teiknkode_451f2815(Terminal_oppføring->부호없는결과<Terminal_oppføring->SMALL_VALUE||Terminal_oppføring->부호없는결과>0x10ffff||(Terminal_oppføring->부호없는결과>=0xd800&&Terminal_oppføring->부호없는결과<=0xdfff)?0xfffd:Terminal_oppføring->부호없는결과);}
        else if(SECOND_VALUE<128)teiknkode_451f2815(SECOND_VALUE);else if(SECOND_VALUE>=0xc2&&SECOND_VALUE<=0xf4){Terminal_oppføring->긴부호없는값=SECOND_VALUE<0xe0?1:SECOND_VALUE<0xf0?2:3;Terminal_oppføring->부호없는결과=SECOND_VALUE&((1u<<(6-Terminal_oppføring->긴부호없는값))-1);Terminal_oppføring->SMALL_VALUE=Terminal_oppføring->긴부호없는값==1?128:Terminal_oppføring->긴부호없는값==2?2048:65536;}else teiknkode_451f2815(0xfffd);
    }cirkumfleks_VALUE(1);
}
int Terminal_ventande(void){return informasjonsteknologi_ventande!=0;}
/* 모서리 INDEX: 1 좌상, 2 우상, 3 좌하, 4 우하. */
static int endre_storleik_dra=-1,잡은모서리,잡은가로,잡은세로,처음가로,처음세로,처음너비,처음높이;
static int 가리킨창(int 가로,int vertikalvising_plassere) {
    for(int SEQUENCE_VALUE=oppføring_COUNT-1;SEQUENCE_VALUE>=0;SEQUENCE_VALUE--){
        int identifikator_VALUE=rekkjefølgje_VALUE[SEQUENCE_VALUE];Terminal_d413d4bc *vindauge=&Windows_Liste[identifikator_VALUE];
        if(가로>=(int)vindauge->x_koordinat&&vertikalvising_plassere>=(int)vindauge->Y_koordinat&&
           가로<(int)(vindauge->x_koordinat+vindauge->너비)&&vertikalvising_plassere<(int)(vindauge->Y_koordinat+vindauge->높이))return identifikator_VALUE;
    }return -1;
}
static int 모서리찾기(int identifikator_VALUE,int 가로,int vertikalvising_plassere) {
    if(identifikator_VALUE<0)return 0;Terminal_d413d4bc *vindauge=&Windows_Liste[identifikator_VALUE];
    int 왼쪽=가로<(int)vindauge->x_koordinat+8,RIGHT=가로>=(int)(vindauge->x_koordinat+vindauge->너비)-8;
    int 위쪽=vertikalvising_plassere<(int)vindauge->Y_koordinat+8,아래쪽=vertikalvising_plassere>=(int)(vindauge->Y_koordinat+vindauge->높이)-8;
    return (왼쪽||RIGHT)&&(위쪽||아래쪽)?1+RIGHT+아래쪽*2:0;
}
static int skiljeline_VALUE(int VALUE,int 최소,int 최대){return VALUE<최소?최소:VALUE>최대?최대:VALUE;}
static void flytte_endre_storleik(int 가로,int vertikalvising_plassere) {
    Terminal_d413d4bc *vindauge=&Windows_Liste[endre_storleik_dra];int 왼쪽=처음가로,위쪽=처음세로,RIGHT=처음가로+처음너비,아래쪽=처음세로+처음높이;
    if(잡은모서리==1||잡은모서리==3)왼쪽=skiljeline_VALUE(처음가로+가로-잡은가로,0,RIGHT-360);
    else RIGHT=skiljeline_VALUE(처음가로+처음너비+가로-잡은가로,왼쪽+360,보드화면너비());
    if(잡은모서리<=2)위쪽=skiljeline_VALUE(처음세로+vertikalvising_plassere-잡은세로,34,아래쪽-216);
    else 아래쪽=skiljeline_VALUE(처음세로+처음높이+vertikalvising_plassere-잡은세로,위쪽+216,보드화면높이());
    unsigned COLUMNS=(RIGHT-왼쪽-24)/8,ROW_COUNT=(아래쪽-위쪽-56)/16;
    if(vindauge->COLUMNS!=COLUMNS||vindauge->ROW_COUNT!=ROW_COUNT){
        vindauge->크기바뀜=1;vindauge->COLUMNS=COLUMNS;vindauge->ROW_COUNT=ROW_COUNT;
        if(vindauge->COLUMN_plassere>=COLUMNS)vindauge->COLUMN_plassere=COLUMNS-1;
        if(vindauge->ROW_plassere>=vindauge->맨위+ROW_COUNT)vindauge->맨위=vindauge->ROW_plassere-ROW_COUNT+1;
        unsigned 한도=vindauge->맨위;if(한도>Logg_line_COUNT-ROW_COUNT)한도=Logg_line_COUNT-ROW_COUNT;
        if(vindauge->rulle>한도)vindauge->rulle=한도;
    }
    int 옛가로=vindauge->x_koordinat,옛세로=vindauge->Y_koordinat,옛폭=vindauge->너비,옛길이=vindauge->높이;
    if(옛가로==왼쪽&&옛세로==위쪽&&옛폭==RIGHT-왼쪽&&옛길이==아래쪽-위쪽)return;
    vindauge->x_koordinat=왼쪽;vindauge->Y_koordinat=위쪽;vindauge->너비=RIGHT-왼쪽;vindauge->높이=아래쪽-위쪽;
    창자리그리기(옛가로,옛세로,옛폭,옛길이,vindauge);
}
void Terminal_peikar(unsigned Neste_vare,int x_koordinat,int Y_koordinat){
    unsigned 눌림=Neste_vare&~단추들;단추들=Neste_vare;
    if(!stasjonær_vise){dra_VALUE=-1;endre_storleik_dra=-1;Tavle_peikar(x_koordinat,Y_koordinat,1);return;}
    if(!(Neste_vare&1)){dra_VALUE=-1;endre_storleik_dra=-1;}
    if(endre_storleik_dra>=0&&!Windows_Liste[endre_storleik_dra].살아있음)endre_storleik_dra=-1;
    if(dra_VALUE>=0&&!Windows_Liste[dra_VALUE].살아있음)dra_VALUE=-1;
    if(endre_storleik_dra>=0){
        flytte_endre_storleik(x_koordinat,Y_koordinat);Tavle_peikar(x_koordinat,Y_koordinat,잡은모서리==1||잡은모서리==4?2:3);return;
    }
    Tavle_peikar(x_koordinat,Y_koordinat,1);
    if(dra_VALUE>=0){
        Terminal_d413d4bc *vindauge=&Windows_Liste[dra_VALUE];
        int 옛가로=vindauge->x_koordinat,옛세로=vindauge->Y_koordinat;
        vindauge->x_koordinat=skiljeline_VALUE(x_koordinat-dra_X,0,보드화면너비()-vindauge->너비);
        vindauge->Y_koordinat=skiljeline_VALUE(Y_koordinat-dra_Y,34,보드화면높이()-vindauge->높이);
        if(옛가로!=(int)vindauge->x_koordinat||옛세로!=(int)vindauge->Y_koordinat)창자리그리기(옛가로,옛세로,vindauge->너비,vindauge->높이,vindauge);
        return;
    }
    extern int 화면덮음(int,int,int);
    if(화면덮음(Fokus,x_koordinat,Y_koordinat)){화면가리킴(Fokus,눌림,x_koordinat,Y_koordinat);return;}
    int identifikator_VALUE=가리킨창(x_koordinat,Y_koordinat),모서리=모서리찾기(identifikator_VALUE,x_koordinat,Y_koordinat);
    if(모서리)Tavle_peikar(x_koordinat,Y_koordinat,모서리==1||모서리==4?2:3);
    if(눌림&1){
        if(모서리){
            Terminal_d413d4bc *vindauge=&Windows_Liste[identifikator_VALUE];endre_storleik_dra=identifikator_VALUE;잡은모서리=모서리;잡은가로=x_koordinat;잡은세로=Y_koordinat;
            처음가로=vindauge->x_koordinat;처음세로=vindauge->Y_koordinat;처음너비=vindauge->너비;처음높이=vindauge->높이;
            if(identifikator_VALUE!=Fokus)앞으로올리기(identifikator_VALUE);return;
        }
        if(Y_koordinat<32&&x_koordinat>=6&&x_koordinat<142){Opprett_oppføring();return;}
        if(Y_koordinat<32&&x_koordinat>=154&&x_koordinat<602){앞으로올리기((x_koordinat-154)/112);return;}
        if(identifikator_VALUE>=0){
            Terminal_d413d4bc *vindauge=&Windows_Liste[identifikator_VALUE];
            if(Y_koordinat<(int)vindauge->Y_koordinat+30&&x_koordinat>=(int)(vindauge->x_koordinat+vindauge->너비)-32){Lukk_vindauge(identifikator_VALUE);return;}
            if(identifikator_VALUE!=Fokus)앞으로올리기(identifikator_VALUE);
            if(Y_koordinat<(int)vindauge->Y_koordinat+30){dra_VALUE=identifikator_VALUE;dra_X=x_koordinat-vindauge->x_koordinat;dra_Y=Y_koordinat-vindauge->Y_koordinat;}return;
        }
    }
    if(Fokus>=0&&(눌림&(8|16))){Terminal_oppføring=&Windows_Liste[Fokus];if(눌림&8){unsigned 한도=Terminal_oppføring->맨위;if(한도>Logg_line_COUNT-Terminal_oppføring->ROW_COUNT)한도=Logg_line_COUNT-Terminal_oppføring->ROW_COUNT;Terminal_oppføring->rulle=Terminal_oppføring->rulle+9>한도?한도:Terminal_oppføring->rulle+9;}else Terminal_oppføring->rulle=Terminal_oppføring->rulle<9?0:Terminal_oppføring->rulle-9;다시그리기();}
}
void 터미널바로가기키(unsigned 누름값){if(누름값==1)Opprett_oppføring();if(누름값==2&&oppføring_COUNT)앞으로올리기(rekkjefølgje_VALUE[0]);if(누름값==3)Lukk_vindauge(Fokus);}
maskin_Word Tavle_Terminal(maskin_Word Handling){
    if(Handling==300){if(!Windows_Liste[출력결과].살아있음)return Opprett_oppføring();stasjonær_vise=1;다시그리기();return 0;}
    if(Handling==0){Lukk_vindauge(Fokus);return 0;}if(Handling==1)return (uint32_t)Opprett_oppføring();if(Handling==2)return Fokus>=0;
    if(Handling==9){stasjonær_vise=0;return 0;}if(Handling==7)return oppføring_COUNT;if(Handling==10)return Fokus+1;if(Handling==11)return 출력결과;
    if(Handling==13){Terminal_d413d4bc *vindauge=&Windows_Liste[출력결과];return vindauge->살아있음?(vindauge->ROW_COUNT<<16)|vindauge->COLUMNS:(19<<16)|68;}
    if(Handling==14){unsigned VALUE=Windows_Liste[출력결과].크기바뀜;Windows_Liste[출력결과].크기바뀜=0;return VALUE;}
    if(Handling==12){unsigned VALUE=informasjonsteknologi_ventande;informasjonsteknologi_ventande=0;return VALUE;}
    if(Handling>=20&&Handling<24)return Windows_Liste[Handling-20].살아있음;
    if(Handling>=100&&Handling<104){출력결과=Handling-100;Terminal_oppføring=&Windows_Liste[출력결과];return 0;}
    if(Handling>=200&&Handling<204){앞으로올리기(Handling-200);return 0;}
    if(Handling==3){다시그리기();return 0;}Terminal_oppføring=&Windows_Liste[출력결과];if(!Terminal_oppføring->살아있음)return 0;
    if(Handling==4)fjerne_Innhald();if(Handling==5||Handling==6){unsigned 이전=단추들;Terminal_peikar(Handling==5?8:16,0,0);단추들=이전;}return 1;
}
