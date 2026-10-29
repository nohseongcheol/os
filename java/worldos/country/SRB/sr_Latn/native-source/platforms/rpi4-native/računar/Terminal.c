#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* 자체 네 prozor 합성과 UTF-8 Terminal. 바뀐 영역의 Dovršeno_VALUE 그림만 표시한다. */
#include <stdint.h>
#include <stddef.h>
typedef uintptr_t računar_Word;
extern računar_Word Tabla_piksel(računar_Word,računar_Word,računar_Word),보드화면기억공간(void);
extern void *memset(void *,int,size_t);
extern const unsigned char Terminal_font[];
#define 최대열수 237
#define Istorija_red_COUNT 160
typedef struct {
    uint32_t 글자칸들[Istorija_red_COUNT][최대열수]; uint8_t 모양들[Istorija_red_COUNT][최대열수];
    unsigned 너비,높이,COLUMNS,ROW_COUNT,크기바뀜;
    unsigned 살아있음,x_koordinata,세로좌표,ROW_pozicija,COLUMN_pozicija,맨위,밀어올리기,전경색,배경색,탈출상태,parametar_VALUE[4],parametar_INDEX,저장행,저장열;
    unsigned 부호없는결과,긴부호없는값,SMALL_VALUE,대체화면,가리개보임;
} Terminal_d413d4bc;
static Terminal_d413d4bc Windows_Lista[4];
static int fokus=-1,출력결과,poručiti_VALUE[4],stavka_COUNT_8f7753a1,prevući_VALUE=-1,prevući_X,prevući_Y;
static unsigned informatičko_odeljenje_na_čekanju,단추들,desktop_Prikaz,한글입력;
static const uint32_t 색상들[16]={0x201a15,0x6060df,0x9dcc86,0x80cfea,0xefaf72,0xca96c9,0xceda76,0xede9df,0x858078,0x8888ff,0xb9eba7,0xa5eaff,0xffcc99,0xf0bef1,0xf0f0a0,0xffffff};
extern int 화면보임(int),화면가리킴(int,unsigned,int,int);
extern void 화면다시그림(int);
static Terminal_d413d4bc *Terminal_stavka;
static unsigned 넓은글자(unsigned kôd_znaka){return kôd_znaka>=256?2:1;}
static void 사각영역(unsigned x_koordinata,unsigned 세로좌표,unsigned 너비값,unsigned 높이값,unsigned 색상){
    보드사각그림(x_koordinata,세로좌표,너비값,높이값,색상);
}
void Terminal_glif(unsigned x_koordinata,unsigned 세로좌표,unsigned kôd_znaka,unsigned 전경색,unsigned 배경색){
    unsigned 너비=넓은글자(kôd_znaka)*8;if(kôd_znaka==0xffffffffu)return;
    int 왼쪽=x_koordinata,위쪽=세로좌표,폭=너비,길이=16;
    if(!보드그림범위(&왼쪽,&위쪽,&폭,&길이))return;
    if(kôd_znaka==' '){보드사각그림(왼쪽,위쪽,폭,길이,배경색);return;}
    unsigned LOOKUP_INDEX=kôd_znaka<65536?kôd_znaka:kôd_znaka>=0x1f600&&kôd_znaka<0x1f650?65536+kôd_znaka-0x1f600:0xfffd;
    const unsigned char *font_VALUE=Terminal_font+LOOKUP_INDEX*32;
    for(int red=위쪽;red<위쪽+길이;red++){unsigned Usluga_inteligentnog_prenosa_u_pozadini_Lista=font_VALUE[(red-세로좌표)*2]*256+font_VALUE[(red-세로좌표)*2+1];for(int 칸=왼쪽;칸<왼쪽+폭;칸++)Tabla_piksel(칸,red,(Usluga_inteligentnog_prenosa_u_pozadini_Lista&(0x8000>>(칸-x_koordinata)))?전경색:배경색);}
}
static void ime_tabela(unsigned x_koordinata,unsigned 세로좌표,const char *niska_podaci,unsigned 전경색,unsigned 배경색){while(*niska_podaci){unsigned kôd_znaka=(unsigned char)*niska_podaci++, 남은수=0;if(kôd_znaka>=0xc0){남은수=kôd_znaka<0xe0?1:kôd_znaka<0xf0?2:3;kôd_znaka&=(1u<<(6-남은수))-1;while(남은수--&&*niska_podaci)kôd_znaka=(kôd_znaka<<6)|((unsigned char)*niska_podaci++&63);}Terminal_glif(x_koordinata,세로좌표,kôd_znaka,전경색,배경색);x_koordinata+=넓은글자(kôd_znaka)*8;}}
static unsigned 첫항목(void){return Terminal_stavka->맨위;}
static int 보이는지(void){return Terminal_stavka->살아있음&&fokus>=0&&Terminal_stavka==&Windows_Lista[fokus]&&!화면보임(fokus);}
static void 그리기(unsigned ROW_pozicija,unsigned COLUMN_pozicija){
    if(!보이는지()||ROW_pozicija<첫항목()-Terminal_stavka->밀어올리기||ROW_pozicija>=첫항목()-Terminal_stavka->밀어올리기+Terminal_stavka->ROW_COUNT||COLUMN_pozicija>=Terminal_stavka->COLUMNS)return;
    unsigned kôd_znaka=Terminal_stavka->글자칸들[ROW_pozicija%Istorija_red_COUNT][COLUMN_pozicija],niska_podaci=Terminal_stavka->모양들[ROW_pozicija%Istorija_red_COUNT][COLUMN_pozicija];
    if(넓은글자(kôd_znaka)==2&&COLUMN_pozicija+1>=Terminal_stavka->COLUMNS)kôd_znaka=' ';
    Terminal_glif(Terminal_stavka->x_koordinata+12+COLUMN_pozicija*8,Terminal_stavka->세로좌표+36+(ROW_pozicija-첫항목()+Terminal_stavka->밀어올리기)*16,kôd_znaka?kôd_znaka:' ',색상들[niska_podaci&15],색상들[niska_podaci>>4]);
}
static void znak_karet_VALUE(int emisija_prozor){if(!보이는지()||Terminal_stavka->밀어올리기||Terminal_stavka->COLUMN_pozicija>=Terminal_stavka->COLUMNS||Terminal_stavka->ROW_pozicija<Terminal_stavka->맨위||Terminal_stavka->ROW_pozicija>=Terminal_stavka->맨위+Terminal_stavka->ROW_COUNT)return;
    if(!emisija_prozor||!Terminal_stavka->가리개보임)그리기(Terminal_stavka->ROW_pozicija,Terminal_stavka->COLUMN_pozicija);else 사각영역(Terminal_stavka->x_koordinata+12+Terminal_stavka->COLUMN_pozicija*8,Terminal_stavka->세로좌표+36+(Terminal_stavka->ROW_pozicija-Terminal_stavka->맨위)*16+14,8,2,색상들[Terminal_stavka->전경색]);}
static void Sadržaj_VALUE(void){
    사각영역(Terminal_stavka->x_koordinata+12,Terminal_stavka->세로좌표+36,Terminal_stavka->COLUMNS*8,Terminal_stavka->ROW_COUNT*16,색상들[0]);
    int 가로=Terminal_stavka->x_koordinata+12,vertikala_pozicija=Terminal_stavka->세로좌표+36,폭=Terminal_stavka->COLUMNS*8,길이=Terminal_stavka->ROW_COUNT*16;
    if(보드그림범위(&가로,&vertikala_pozicija,&폭,&길이)){
    unsigned 첫줄=(vertikala_pozicija-Terminal_stavka->세로좌표-36)/16,끝줄=(vertikala_pozicija+길이-Terminal_stavka->세로좌표-36+15)/16;
    unsigned 첫칸=(가로-Terminal_stavka->x_koordinata-12)/8,끝칸=(가로+폭-Terminal_stavka->x_koordinata-12+7)/8;
    if(첫칸)첫칸--; /* 잘림 경계 왼쪽에서 시작한 두 칸 글자도 그린다. */
    for(unsigned 반환값=첫줄;반환값<끝줄;반환값++)for(unsigned kôd_znaka=첫칸;kôd_znaka<끝칸;kôd_znaka++){
        unsigned ROW_pozicija=첫항목()-Terminal_stavka->밀어올리기+반환값,znak_VALUE=Terminal_stavka->글자칸들[ROW_pozicija%Istorija_red_COUNT][kôd_znaka],niska_podaci=Terminal_stavka->모양들[ROW_pozicija%Istorija_red_COUNT][kôd_znaka];
        if(넓은글자(znak_VALUE)==2&&kôd_znaka+1>=Terminal_stavka->COLUMNS)znak_VALUE=' ';
        if((znak_VALUE==0||znak_VALUE==' ')&&(niska_podaci>>4)==0)continue;
        Terminal_glif(Terminal_stavka->x_koordinata+12+kôd_znaka*8,Terminal_stavka->세로좌표+36+반환값*16,znak_VALUE?znak_VALUE:' ',색상들[niska_podaci&15],색상들[niska_podaci>>4]);
    }}
    ime_tabela(Terminal_stavka->x_koordinata+12,Terminal_stavka->세로좌표+Terminal_stavka->높이-18,Terminal_stavka->밀어올리기?"PgDn: recent output":Terminal_stavka->너비>=500?"F6: next | Corner + left drag: resize":"Corner + left drag: resize",0xece8e2,0x403127);znak_karet_VALUE(1);
}
static void 실행틀(int identifikator_VALUE){
    Terminal_stavka=&Windows_Lista[identifikator_VALUE];
    int 가로=Terminal_stavka->x_koordinata,vertikala_pozicija=Terminal_stavka->세로좌표,폭=Terminal_stavka->너비,길이=Terminal_stavka->높이;
    if(!보드그림범위(&가로,&vertikala_pozicija,&폭,&길이))return;
    사각영역(Terminal_stavka->x_koordinata,Terminal_stavka->세로좌표,Terminal_stavka->너비,Terminal_stavka->높이,0x403127);
    unsigned 색상=identifikator_VALUE==fokus?0x905020:0x604438;사각영역(Terminal_stavka->x_koordinata,Terminal_stavka->세로좌표,Terminal_stavka->너비,30,색상);
    ime_tabela(Terminal_stavka->x_koordinata+12,Terminal_stavka->세로좌표+7,"JKOROS Terminal",0xffffff,색상);
    char 수치[2]={(char)('1'+identifikator_VALUE),0};ime_tabela(Terminal_stavka->x_koordinata+148,Terminal_stavka->세로좌표+7,수치,0xffffff,색상);
    ime_tabela(Terminal_stavka->x_koordinata+240,Terminal_stavka->세로좌표+7,Terminal_stavka->너비>=500?(한글입력?"[SR] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[SR]":"[EN]"),0xffffff,색상);
    사각영역(Terminal_stavka->x_koordinata+Terminal_stavka->너비-32,Terminal_stavka->세로좌표+4,26,22,0x5555b8);ime_tabela(Terminal_stavka->x_koordinata+Terminal_stavka->너비-24,Terminal_stavka->세로좌표+7,"X",0xffffff,0x5555b8);
    Sadržaj_VALUE();
}
static void crtati_scena(void){
    if(!desktop_Prikaz)return;사각영역(0,0,보드화면너비(),보드화면높이(),0x302018);사각영역(0,0,보드화면너비(),32,0x403127);
    사각영역(6,4,136,24,0x905020);ime_tabela(14,8,"+ New terminal",0xffffff,0x905020);
    for(int 순번=0;순번<4;순번++)if(Windows_Lista[순번].살아있음){unsigned kôd_znaka=fokus==순번?0x905020:0x604438;사각영역(154+순번*112,4,106,24,kôd_znaka);ime_tabela(160+순번*112,8,"Terminal",0xffffff,kôd_znaka);char niska_podaci[2]={(char)('1'+순번),0};ime_tabela(232+순번*112,8,niska_podaci,0xffffff,kôd_znaka);}
    if(!stavka_COUNT_8f7753a1)ime_tabela(140,210,"Click + New terminal to start",0xede9df,0x302018);
    for(int 순번=0;순번<stavka_COUNT_8f7753a1;순번++)실행틀(poručiti_VALUE[순번]);화면다시그림(fokus);Terminal_stavka=&Windows_Lista[출력결과];
}
static void Bojanka_oblast(int 가로,int vertikala_pozicija,int 폭,int 길이){
    if(!desktop_Prikaz||!보드그림범위(&가로,&vertikala_pozicija,&폭,&길이))return;
    for(int red=vertikala_pozicija;red<vertikala_pozicija+길이;red+=32){
        int 띠높이=vertikala_pozicija+길이-red;if(띠높이>32)띠높이=32;
        if(Tabla_START_crtež(가로,red,폭,띠높이)){crtati_scena();Tabla_kraj_crtež();}
    }
}
static void 다시그리기(void){Bojanka_oblast(0,0,보드화면너비(),보드화면높이());}
/* 서로 겹치지 않는 새 prozor 영역과 이전 자리의 네 띠를 복구한다. */
static void 창자리그리기(int 가로,int vertikala_pozicija,int 폭,int 길이,Terminal_d413d4bc *prozor){
    int 왼쪽=가로>(int)prozor->x_koordinata?가로:(int)prozor->x_koordinata;
    int 위쪽=vertikala_pozicija>(int)prozor->세로좌표?vertikala_pozicija:(int)prozor->세로좌표;
    int RIGHT=가로+폭<(int)(prozor->x_koordinata+prozor->너비)?가로+폭:(int)(prozor->x_koordinata+prozor->너비);
    int 아래쪽=vertikala_pozicija+길이<(int)(prozor->세로좌표+prozor->높이)?vertikala_pozicija+길이:(int)(prozor->세로좌표+prozor->높이);
    Bojanka_oblast(prozor->x_koordinata,prozor->세로좌표,prozor->너비,prozor->높이);
    if(왼쪽>=RIGHT||위쪽>=아래쪽){Bojanka_oblast(가로,vertikala_pozicija,폭,길이);return;}
    Bojanka_oblast(가로,vertikala_pozicija,폭,위쪽-vertikala_pozicija);
    Bojanka_oblast(가로,아래쪽,폭,vertikala_pozicija+길이-아래쪽);
    Bojanka_oblast(가로,위쪽,왼쪽-가로,아래쪽-위쪽);
    Bojanka_oblast(RIGHT,위쪽,가로+폭-RIGHT,아래쪽-위쪽);
}
static void signal_fokus(void){informatičko_odeljenje_na_čekanju=(informatičko_odeljenje_na_čekanju&~15u)|(unsigned)(fokus+1)|0x10000;}
void 터미널입력방식(unsigned 한글여부){
    한글입력=한글여부!=0;
    /* Update title bars only: a mode switch must not erase an EL0 drawing. */
    if(fokus>=0){
        Terminal_d413d4bc *prozor_stavka=&Windows_Lista[fokus];
        ime_tabela(prozor_stavka->x_koordinata+240,prozor_stavka->세로좌표+7,prozor_stavka->너비>=500?(한글입력?"[SR] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[SR]":"[EN]"),0xffffff,0x905020);
    }
}
static void 앞으로올리기(int identifikator_VALUE){if(identifikator_VALUE<0||identifikator_VALUE>=4||!Windows_Lista[identifikator_VALUE].살아있음)return;int aktuelno_pozicija=0;while(aktuelno_pozicija<stavka_COUNT_8f7753a1&&poručiti_VALUE[aktuelno_pozicija]!=identifikator_VALUE)aktuelno_pozicija++;for(;aktuelno_pozicija+1<stavka_COUNT_8f7753a1;aktuelno_pozicija++)poručiti_VALUE[aktuelno_pozicija]=poručiti_VALUE[aktuelno_pozicija+1];poručiti_VALUE[stavka_COUNT_8f7753a1-1]=identifikator_VALUE;fokus=identifikator_VALUE;signal_fokus();다시그리기();}
static void 빈칸채우기(unsigned ROW_pozicija){for(unsigned kôd_znaka=0;kôd_znaka<최대열수;kôd_znaka++){Terminal_stavka->글자칸들[ROW_pozicija%Istorija_red_COUNT][kôd_znaka]=0;Terminal_stavka->모양들[ROW_pozicija%Istorija_red_COUNT][kôd_znaka]=Terminal_stavka->전경색|(Terminal_stavka->배경색<<4);}}
static void obrisati_Sadržaj(void){Terminal_stavka->ROW_pozicija=Terminal_stavka->COLUMN_pozicija=Terminal_stavka->맨위=Terminal_stavka->밀어올리기=0;for(unsigned 반환값=0;반환값<Istorija_red_COUNT;반환값++)빈칸채우기(반환값);if(보이는지())Sadržaj_VALUE();}
static int Create_stavka(void){
    if(!보드화면기억공간())return -19;int identifikator_VALUE=0;while(identifikator_VALUE<4&&Windows_Lista[identifikator_VALUE].살아있음)identifikator_VALUE++;if(identifikator_VALUE==4)return -28;
    desktop_Prikaz=1;Terminal_stavka=&Windows_Lista[identifikator_VALUE];memset(Terminal_stavka,0,sizeof(*Terminal_stavka));Terminal_stavka->살아있음=1;Terminal_stavka->너비=568;Terminal_stavka->높이=360;Terminal_stavka->COLUMNS=68;Terminal_stavka->ROW_COUNT=19;Terminal_stavka->x_koordinata=12+identifikator_VALUE*16;Terminal_stavka->세로좌표=48+identifikator_VALUE*18;Terminal_stavka->전경색=7;Terminal_stavka->가리개보임=1;
    for(unsigned 반환값=0;반환값<Istorija_red_COUNT;반환값++)빈칸채우기(반환값);poručiti_VALUE[stavka_COUNT_8f7753a1++]=identifikator_VALUE;fokus=identifikator_VALUE;informatičko_odeljenje_na_čekanju|=1u<<(4+identifikator_VALUE);signal_fokus();다시그리기();return identifikator_VALUE+1;
}
static void Zatvori_prozor(int identifikator_VALUE){
    if(identifikator_VALUE<0||identifikator_VALUE>=4||!Windows_Lista[identifikator_VALUE].살아있음)return;Windows_Lista[identifikator_VALUE].살아있음=0;informatičko_odeljenje_na_čekanju|=1u<<(8+identifikator_VALUE);
    int aktuelno_pozicija=0;while(aktuelno_pozicija<stavka_COUNT_8f7753a1&&poručiti_VALUE[aktuelno_pozicija]!=identifikator_VALUE)aktuelno_pozicija++;for(;aktuelno_pozicija+1<stavka_COUNT_8f7753a1;aktuelno_pozicija++)poručiti_VALUE[aktuelno_pozicija]=poručiti_VALUE[aktuelno_pozicija+1];stavka_COUNT_8f7753a1--;
    if(fokus==identifikator_VALUE)fokus=stavka_COUNT_8f7753a1?poručiti_VALUE[stavka_COUNT_8f7753a1-1]:-1;signal_fokus();다시그리기();
}
static void 줄바꿈(void){Terminal_stavka->COLUMN_pozicija=0;Terminal_stavka->ROW_pozicija++;if(Terminal_stavka->ROW_pozicija>=Terminal_stavka->맨위+Terminal_stavka->ROW_COUNT){Terminal_stavka->맨위++;빈칸채우기(Terminal_stavka->ROW_pozicija);if(보이는지())Sadržaj_VALUE();}}
static void kôd_znaka_451f2815(unsigned kôd_znaka){
    if(kôd_znaka==13){Terminal_stavka->COLUMN_pozicija=0;return;}if(kôd_znaka==10){줄바꿈();return;}if(kôd_znaka==8){if(Terminal_stavka->COLUMN_pozicija)Terminal_stavka->COLUMN_pozicija--;return;}
    if(kôd_znaka==9){unsigned stavka_COUNT=8-Terminal_stavka->COLUMN_pozicija%8;while(stavka_COUNT--)kôd_znaka_451f2815(' ');return;}if(kôd_znaka<32||kôd_znaka==127)return;
    unsigned 너비값=넓은글자(kôd_znaka);if(Terminal_stavka->COLUMN_pozicija+너비값>Terminal_stavka->COLUMNS)줄바꿈();
    if(Terminal_stavka->글자칸들[Terminal_stavka->ROW_pozicija%Istorija_red_COUNT][Terminal_stavka->COLUMN_pozicija]==0xffffffffu&&Terminal_stavka->COLUMN_pozicija){Terminal_stavka->글자칸들[Terminal_stavka->ROW_pozicija%Istorija_red_COUNT][Terminal_stavka->COLUMN_pozicija-1]=' ';그리기(Terminal_stavka->ROW_pozicija,Terminal_stavka->COLUMN_pozicija-1);}
    if(넓은글자(Terminal_stavka->글자칸들[Terminal_stavka->ROW_pozicija%Istorija_red_COUNT][Terminal_stavka->COLUMN_pozicija])==2&&Terminal_stavka->COLUMN_pozicija+1<Terminal_stavka->COLUMNS){Terminal_stavka->글자칸들[Terminal_stavka->ROW_pozicija%Istorija_red_COUNT][Terminal_stavka->COLUMN_pozicija+1]=' ';그리기(Terminal_stavka->ROW_pozicija,Terminal_stavka->COLUMN_pozicija+1);}
    Terminal_stavka->글자칸들[Terminal_stavka->ROW_pozicija%Istorija_red_COUNT][Terminal_stavka->COLUMN_pozicija]=kôd_znaka;Terminal_stavka->모양들[Terminal_stavka->ROW_pozicija%Istorija_red_COUNT][Terminal_stavka->COLUMN_pozicija]=Terminal_stavka->전경색|(Terminal_stavka->배경색<<4);
    if(너비값==2)Terminal_stavka->글자칸들[Terminal_stavka->ROW_pozicija%Istorija_red_COUNT][Terminal_stavka->COLUMN_pozicija+1]=0xffffffffu;
    그리기(Terminal_stavka->ROW_pozicija,Terminal_stavka->COLUMN_pozicija);Terminal_stavka->COLUMN_pozicija+=너비값;
}
static void pokazivač_kontrola_SEQUENCE(unsigned kôd_znaka){
    unsigned stavka_COUNT=Terminal_stavka->parametar_VALUE[0]?Terminal_stavka->parametar_VALUE[0]:1;
    if(kôd_znaka=='m')for(unsigned 순번=0;순번<=Terminal_stavka->parametar_INDEX;순번++){unsigned podaci_pozicija=Terminal_stavka->parametar_VALUE[순번];if(!podaci_pozicija){Terminal_stavka->전경색=7;Terminal_stavka->배경색=0;}if(podaci_pozicija==1&&Terminal_stavka->전경색<8)Terminal_stavka->전경색+=8;if(podaci_pozicija==7){unsigned 유지=Terminal_stavka->전경색;Terminal_stavka->전경색=Terminal_stavka->배경색;Terminal_stavka->배경색=유지;}if(podaci_pozicija>=30&&podaci_pozicija<=37)Terminal_stavka->전경색=podaci_pozicija-30;if(podaci_pozicija>=90&&podaci_pozicija<=97)Terminal_stavka->전경색=podaci_pozicija-90+8;if(podaci_pozicija>=40&&podaci_pozicija<=47)Terminal_stavka->배경색=podaci_pozicija-40;if(podaci_pozicija>=100&&podaci_pozicija<=107)Terminal_stavka->배경색=podaci_pozicija-100+8;if(podaci_pozicija==39)Terminal_stavka->전경색=7;if(podaci_pozicija==49)Terminal_stavka->배경색=0;}
    if(kôd_znaka=='J'&&(Terminal_stavka->parametar_VALUE[0]==2||Terminal_stavka->parametar_VALUE[0]==3))obrisati_Sadržaj();
    if(kôd_znaka=='K'){unsigned 출발위치=Terminal_stavka->parametar_VALUE[0]==2?0:Terminal_stavka->COLUMN_pozicija,도착위치=Terminal_stavka->parametar_VALUE[0]==1?Terminal_stavka->COLUMN_pozicija+1:Terminal_stavka->COLUMNS;if(Terminal_stavka->parametar_VALUE[0]==1)출발위치=0;for(unsigned 순번=출발위치;순번<도착위치&&순번<Terminal_stavka->COLUMNS;순번++){
        unsigned ROW_VALUE=Terminal_stavka->ROW_pozicija%Istorija_red_COUNT,znak_VALUE=Terminal_stavka->글자칸들[ROW_VALUE][순번],oblik_VALUE=Terminal_stavka->전경색|(Terminal_stavka->배경색<<4);
        /* 넓은 vi 화면에서도 이미 빈 칸의 font_VALUE 화소를 되풀이해 칠하지 않는다. */
        int 바뀜=(znak_VALUE!=0&&znak_VALUE!=' ')||Terminal_stavka->모양들[ROW_VALUE][순번]!=oblik_VALUE;
        Terminal_stavka->글자칸들[ROW_VALUE][순번]=' ';Terminal_stavka->모양들[ROW_VALUE][순번]=oblik_VALUE;
        if(바뀜)그리기(Terminal_stavka->ROW_pozicija,순번);
    }}
    if(kôd_znaka=='D')Terminal_stavka->COLUMN_pozicija=stavka_COUNT>Terminal_stavka->COLUMN_pozicija?0:Terminal_stavka->COLUMN_pozicija-stavka_COUNT;if(kôd_znaka=='C')Terminal_stavka->COLUMN_pozicija=Terminal_stavka->COLUMN_pozicija+stavka_COUNT>=Terminal_stavka->COLUMNS?Terminal_stavka->COLUMNS-1:Terminal_stavka->COLUMN_pozicija+stavka_COUNT;
    if(kôd_znaka=='G')Terminal_stavka->COLUMN_pozicija=stavka_COUNT>Terminal_stavka->COLUMNS?Terminal_stavka->COLUMNS-1:stavka_COUNT-1;if(kôd_znaka=='A')Terminal_stavka->ROW_pozicija=stavka_COUNT>Terminal_stavka->ROW_pozicija-Terminal_stavka->맨위?Terminal_stavka->맨위:Terminal_stavka->ROW_pozicija-stavka_COUNT;
    if(kôd_znaka=='B')Terminal_stavka->ROW_pozicija=Terminal_stavka->ROW_pozicija+stavka_COUNT>=Terminal_stavka->맨위+Terminal_stavka->ROW_COUNT?Terminal_stavka->맨위+Terminal_stavka->ROW_COUNT-1:Terminal_stavka->ROW_pozicija+stavka_COUNT;
    if(kôd_znaka=='H'||kôd_znaka=='f'){Terminal_stavka->ROW_pozicija=Terminal_stavka->맨위+(stavka_COUNT>Terminal_stavka->ROW_COUNT?Terminal_stavka->ROW_COUNT:stavka_COUNT)-1;unsigned x_koordinata=Terminal_stavka->parametar_VALUE[1]?Terminal_stavka->parametar_VALUE[1]:1;Terminal_stavka->COLUMN_pozicija=(x_koordinata>Terminal_stavka->COLUMNS?Terminal_stavka->COLUMNS:x_koordinata)-1;}
    if(kôd_znaka=='s'){Terminal_stavka->저장행=Terminal_stavka->ROW_pozicija;Terminal_stavka->저장열=Terminal_stavka->COLUMN_pozicija;}if(kôd_znaka=='u'){Terminal_stavka->ROW_pozicija=Terminal_stavka->저장행;Terminal_stavka->COLUMN_pozicija=Terminal_stavka->저장열<Terminal_stavka->COLUMNS?Terminal_stavka->저장열:Terminal_stavka->COLUMNS-1;}
    if((kôd_znaka=='h'||kôd_znaka=='l')&&Terminal_stavka->parametar_VALUE[0]==25)Terminal_stavka->가리개보임=kôd_znaka=='h';
}
void Terminal_bajt(unsigned SECOND_VALUE){
    Terminal_stavka=&Windows_Lista[출력결과];if(!Terminal_stavka->살아있음)return;znak_karet_VALUE(0);if(Terminal_stavka->밀어올리기){Terminal_stavka->밀어올리기=0;if(보이는지())Sadržaj_VALUE();}
    if(Terminal_stavka->탈출상태==1){Terminal_stavka->탈출상태=SECOND_VALUE=='['?2:0;Terminal_stavka->parametar_INDEX=0;for(unsigned 순번=0;순번<4;순번++)Terminal_stavka->parametar_VALUE[순번]=0;}
    else if(Terminal_stavka->탈출상태==2){if(SECOND_VALUE=='?'){}else if(SECOND_VALUE>='0'&&SECOND_VALUE<='9'){if(Terminal_stavka->parametar_VALUE[Terminal_stavka->parametar_INDEX]<10000)Terminal_stavka->parametar_VALUE[Terminal_stavka->parametar_INDEX]=Terminal_stavka->parametar_VALUE[Terminal_stavka->parametar_INDEX]*10+SECOND_VALUE-'0';}else if(SECOND_VALUE==';'&&Terminal_stavka->parametar_INDEX<3)Terminal_stavka->parametar_INDEX++;else{pokazivač_kontrola_SEQUENCE(SECOND_VALUE);Terminal_stavka->탈출상태=0;}}
    else if(SECOND_VALUE==27){Terminal_stavka->긴부호없는값=0;Terminal_stavka->탈출상태=1;}else{
        if(Terminal_stavka->긴부호없는값&&(SECOND_VALUE&0xc0)!=0x80){Terminal_stavka->긴부호없는값=0;kôd_znaka_451f2815(0xfffd);}
        if(Terminal_stavka->긴부호없는값){Terminal_stavka->부호없는결과=Terminal_stavka->부호없는결과*64+(SECOND_VALUE&63);if(--Terminal_stavka->긴부호없는값==0)kôd_znaka_451f2815(Terminal_stavka->부호없는결과<Terminal_stavka->SMALL_VALUE||Terminal_stavka->부호없는결과>0x10ffff||(Terminal_stavka->부호없는결과>=0xd800&&Terminal_stavka->부호없는결과<=0xdfff)?0xfffd:Terminal_stavka->부호없는결과);}
        else if(SECOND_VALUE<128)kôd_znaka_451f2815(SECOND_VALUE);else if(SECOND_VALUE>=0xc2&&SECOND_VALUE<=0xf4){Terminal_stavka->긴부호없는값=SECOND_VALUE<0xe0?1:SECOND_VALUE<0xf0?2:3;Terminal_stavka->부호없는결과=SECOND_VALUE&((1u<<(6-Terminal_stavka->긴부호없는값))-1);Terminal_stavka->SMALL_VALUE=Terminal_stavka->긴부호없는값==1?128:Terminal_stavka->긴부호없는값==2?2048:65536;}else kôd_znaka_451f2815(0xfffd);
    }znak_karet_VALUE(1);
}
int Terminal_na_čekanju(void){return informatičko_odeljenje_na_čekanju!=0;}
/* 모서리 INDEX: 1 좌상, 2 우상, 3 좌하, 4 우하. */
static int promeniti_veličinu_prevući=-1,잡은모서리,잡은가로,잡은세로,처음가로,처음세로,처음너비,처음높이;
static int 가리킨창(int 가로,int vertikala_pozicija) {
    for(int SEQUENCE_VALUE=stavka_COUNT_8f7753a1-1;SEQUENCE_VALUE>=0;SEQUENCE_VALUE--){
        int identifikator_VALUE=poručiti_VALUE[SEQUENCE_VALUE];Terminal_d413d4bc *prozor=&Windows_Lista[identifikator_VALUE];
        if(가로>=(int)prozor->x_koordinata&&vertikala_pozicija>=(int)prozor->세로좌표&&
           가로<(int)(prozor->x_koordinata+prozor->너비)&&vertikala_pozicija<(int)(prozor->세로좌표+prozor->높이))return identifikator_VALUE;
    }return -1;
}
static int 모서리찾기(int identifikator_VALUE,int 가로,int vertikala_pozicija) {
    if(identifikator_VALUE<0)return 0;Terminal_d413d4bc *prozor=&Windows_Lista[identifikator_VALUE];
    int 왼쪽=가로<(int)prozor->x_koordinata+8,RIGHT=가로>=(int)(prozor->x_koordinata+prozor->너비)-8;
    int 위쪽=vertikala_pozicija<(int)prozor->세로좌표+8,아래쪽=vertikala_pozicija>=(int)(prozor->세로좌표+prozor->높이)-8;
    return (왼쪽||RIGHT)&&(위쪽||아래쪽)?1+RIGHT+아래쪽*2:0;
}
static int razdelnik_VALUE(int VALUE,int 최소,int 최대){return VALUE<최소?최소:VALUE>최대?최대:VALUE;}
static void premestiti_promeniti_veličinu(int 가로,int vertikala_pozicija) {
    Terminal_d413d4bc *prozor=&Windows_Lista[promeniti_veličinu_prevući];int 왼쪽=처음가로,위쪽=처음세로,RIGHT=처음가로+처음너비,아래쪽=처음세로+처음높이;
    if(잡은모서리==1||잡은모서리==3)왼쪽=razdelnik_VALUE(처음가로+가로-잡은가로,0,RIGHT-360);
    else RIGHT=razdelnik_VALUE(처음가로+처음너비+가로-잡은가로,왼쪽+360,보드화면너비());
    if(잡은모서리<=2)위쪽=razdelnik_VALUE(처음세로+vertikala_pozicija-잡은세로,34,아래쪽-216);
    else 아래쪽=razdelnik_VALUE(처음세로+처음높이+vertikala_pozicija-잡은세로,위쪽+216,보드화면높이());
    unsigned COLUMNS=(RIGHT-왼쪽-24)/8,ROW_COUNT=(아래쪽-위쪽-56)/16;
    if(prozor->COLUMNS!=COLUMNS||prozor->ROW_COUNT!=ROW_COUNT){
        prozor->크기바뀜=1;prozor->COLUMNS=COLUMNS;prozor->ROW_COUNT=ROW_COUNT;
        if(prozor->COLUMN_pozicija>=COLUMNS)prozor->COLUMN_pozicija=COLUMNS-1;
        if(prozor->ROW_pozicija>=prozor->맨위+ROW_COUNT)prozor->맨위=prozor->ROW_pozicija-ROW_COUNT+1;
        unsigned 한도=prozor->맨위;if(한도>Istorija_red_COUNT-ROW_COUNT)한도=Istorija_red_COUNT-ROW_COUNT;
        if(prozor->밀어올리기>한도)prozor->밀어올리기=한도;
    }
    int 옛가로=prozor->x_koordinata,옛세로=prozor->세로좌표,옛폭=prozor->너비,옛길이=prozor->높이;
    if(옛가로==왼쪽&&옛세로==위쪽&&옛폭==RIGHT-왼쪽&&옛길이==아래쪽-위쪽)return;
    prozor->x_koordinata=왼쪽;prozor->세로좌표=위쪽;prozor->너비=RIGHT-왼쪽;prozor->높이=아래쪽-위쪽;
    창자리그리기(옛가로,옛세로,옛폭,옛길이,prozor);
}
void Terminal_pokazivač(unsigned Dalje_stavka,int x_koordinata,int 세로좌표){
    unsigned 눌림=Dalje_stavka&~단추들;단추들=Dalje_stavka;
    if(!desktop_Prikaz){prevući_VALUE=-1;promeniti_veličinu_prevući=-1;Tabla_pokazivač(x_koordinata,세로좌표,1);return;}
    if(!(Dalje_stavka&1)){prevući_VALUE=-1;promeniti_veličinu_prevući=-1;}
    if(promeniti_veličinu_prevući>=0&&!Windows_Lista[promeniti_veličinu_prevući].살아있음)promeniti_veličinu_prevući=-1;
    if(prevući_VALUE>=0&&!Windows_Lista[prevući_VALUE].살아있음)prevući_VALUE=-1;
    if(promeniti_veličinu_prevući>=0){
        premestiti_promeniti_veličinu(x_koordinata,세로좌표);Tabla_pokazivač(x_koordinata,세로좌표,잡은모서리==1||잡은모서리==4?2:3);return;
    }
    Tabla_pokazivač(x_koordinata,세로좌표,1);
    if(prevući_VALUE>=0){
        Terminal_d413d4bc *prozor=&Windows_Lista[prevući_VALUE];
        int 옛가로=prozor->x_koordinata,옛세로=prozor->세로좌표;
        prozor->x_koordinata=razdelnik_VALUE(x_koordinata-prevući_X,0,보드화면너비()-prozor->너비);
        prozor->세로좌표=razdelnik_VALUE(세로좌표-prevući_Y,34,보드화면높이()-prozor->높이);
        if(옛가로!=(int)prozor->x_koordinata||옛세로!=(int)prozor->세로좌표)창자리그리기(옛가로,옛세로,prozor->너비,prozor->높이,prozor);
        return;
    }
    extern int 화면덮음(int,int,int);
    if(화면덮음(fokus,x_koordinata,세로좌표)){화면가리킴(fokus,눌림,x_koordinata,세로좌표);return;}
    int identifikator_VALUE=가리킨창(x_koordinata,세로좌표),모서리=모서리찾기(identifikator_VALUE,x_koordinata,세로좌표);
    if(모서리)Tabla_pokazivač(x_koordinata,세로좌표,모서리==1||모서리==4?2:3);
    if(눌림&1){
        if(모서리){
            Terminal_d413d4bc *prozor=&Windows_Lista[identifikator_VALUE];promeniti_veličinu_prevući=identifikator_VALUE;잡은모서리=모서리;잡은가로=x_koordinata;잡은세로=세로좌표;
            처음가로=prozor->x_koordinata;처음세로=prozor->세로좌표;처음너비=prozor->너비;처음높이=prozor->높이;
            if(identifikator_VALUE!=fokus)앞으로올리기(identifikator_VALUE);return;
        }
        if(세로좌표<32&&x_koordinata>=6&&x_koordinata<142){Create_stavka();return;}
        if(세로좌표<32&&x_koordinata>=154&&x_koordinata<602){앞으로올리기((x_koordinata-154)/112);return;}
        if(identifikator_VALUE>=0){
            Terminal_d413d4bc *prozor=&Windows_Lista[identifikator_VALUE];
            if(세로좌표<(int)prozor->세로좌표+30&&x_koordinata>=(int)(prozor->x_koordinata+prozor->너비)-32){Zatvori_prozor(identifikator_VALUE);return;}
            if(identifikator_VALUE!=fokus)앞으로올리기(identifikator_VALUE);
            if(세로좌표<(int)prozor->세로좌표+30){prevući_VALUE=identifikator_VALUE;prevući_X=x_koordinata-prozor->x_koordinata;prevući_Y=세로좌표-prozor->세로좌표;}return;
        }
    }
    if(fokus>=0&&(눌림&(8|16))){Terminal_stavka=&Windows_Lista[fokus];if(눌림&8){unsigned 한도=Terminal_stavka->맨위;if(한도>Istorija_red_COUNT-Terminal_stavka->ROW_COUNT)한도=Istorija_red_COUNT-Terminal_stavka->ROW_COUNT;Terminal_stavka->밀어올리기=Terminal_stavka->밀어올리기+9>한도?한도:Terminal_stavka->밀어올리기+9;}else Terminal_stavka->밀어올리기=Terminal_stavka->밀어올리기<9?0:Terminal_stavka->밀어올리기-9;다시그리기();}
}
void 터미널바로가기키(unsigned 누름값){if(누름값==1)Create_stavka();if(누름값==2&&stavka_COUNT_8f7753a1)앞으로올리기(poručiti_VALUE[0]);if(누름값==3)Zatvori_prozor(fokus);}
računar_Word Tabla_Terminal(računar_Word radnja){
    if(radnja==300){if(!Windows_Lista[출력결과].살아있음)return Create_stavka();desktop_Prikaz=1;다시그리기();return 0;}
    if(radnja==0){Zatvori_prozor(fokus);return 0;}if(radnja==1)return (uint32_t)Create_stavka();if(radnja==2)return fokus>=0;
    if(radnja==9){desktop_Prikaz=0;return 0;}if(radnja==7)return stavka_COUNT_8f7753a1;if(radnja==10)return fokus+1;if(radnja==11)return 출력결과;
    if(radnja==13){Terminal_d413d4bc *prozor=&Windows_Lista[출력결과];return prozor->살아있음?(prozor->ROW_COUNT<<16)|prozor->COLUMNS:(19<<16)|68;}
    if(radnja==14){unsigned VALUE=Windows_Lista[출력결과].크기바뀜;Windows_Lista[출력결과].크기바뀜=0;return VALUE;}
    if(radnja==12){unsigned VALUE=informatičko_odeljenje_na_čekanju;informatičko_odeljenje_na_čekanju=0;return VALUE;}
    if(radnja>=20&&radnja<24)return Windows_Lista[radnja-20].살아있음;
    if(radnja>=100&&radnja<104){출력결과=radnja-100;Terminal_stavka=&Windows_Lista[출력결과];return 0;}
    if(radnja>=200&&radnja<204){앞으로올리기(radnja-200);return 0;}
    if(radnja==3){다시그리기();return 0;}Terminal_stavka=&Windows_Lista[출력결과];if(!Terminal_stavka->살아있음)return 0;
    if(radnja==4)obrisati_Sadržaj();if(radnja==5||radnja==6){unsigned 이전=단추들;Terminal_pokazivač(radnja==5?8:16,0,0);단추들=이전;}return 1;
}
