#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* lastno 네 okno 합성과 UTF-8 Terminal. 바뀐 영역의 Dokončano_VALUE 그림만 표시한다. */
#include <stdint.h>
#include <stddef.h>
typedef uintptr_t računalnik_Word;
extern računalnik_Word Tabla_slikovna_pika(računalnik_Word,računalnik_Word,računalnik_Word),보드화면기억공간(void);
extern void *memset(void *,int,size_t);
extern const unsigned char Terminal_pisava[];
#define 최대열수 237
#define Zgodovina_linija_COUNT 160
typedef struct {
    uint32_t 글자칸들[Zgodovina_linija_COUNT][최대열수]; uint8_t 모양들[Zgodovina_linija_COUNT][최대열수];
    unsigned 너비,višina_VALUE,COLUMNS,ROW_COUNT,크기바뀜;
    unsigned 살아있음,koordinata_x,세로좌표,ROW_položaj,COLUMN_položaj,맨위,drseti,전경색,배경색,탈출상태,parameter_VALUE[4],parameter_INDEX,저장행,저장열;
    unsigned 부호없는결과,긴부호없는값,SMALL_VALUE,대체화면,가리개보임;
} Terminal_d413d4bc;
static Terminal_d413d4bc Windows_Seznam[4];
static int Fokus=-1,출력결과,naročilo_VALUE[4],vnos_COUNT,povleči_VALUE=-1,povleči_X,povleči_Y;
static unsigned informacijska_tehnologija_čakajoče,단추들,namizje_Pogled,한글입력;
static const uint32_t 색상들[16]={0x201a15,0x6060df,0x9dcc86,0x80cfea,0xefaf72,0xca96c9,0xceda76,0xede9df,0x858078,0x8888ff,0xb9eba7,0xa5eaff,0xffcc99,0xf0bef1,0xf0f0a0,0xffffff};
extern int 화면보임(int),화면가리킴(int,unsigned,int,int);
extern void 화면다시그림(int);
static Terminal_d413d4bc *Terminal_vnos;
static unsigned širok_znak(unsigned koda_znaka){return koda_znaka>=256?2:1;}
static void 사각영역(unsigned koordinata_x,unsigned 세로좌표,unsigned 너비값,unsigned 높이값,unsigned 색상){
    Tabla_pravokotnik_polnilo(koordinata_x,세로좌표,너비값,높이값,색상);
}
void Terminal_glif(unsigned koordinata_x,unsigned 세로좌표,unsigned koda_znaka,unsigned 전경색,unsigned 배경색){
    unsigned 너비=širok_znak(koda_znaka)*8;if(koda_znaka==0xffffffffu)return;
    int 왼쪽=koordinata_x,위쪽=세로좌표,폭=너비,길이=16;
    if(!보드그림범위(&왼쪽,&위쪽,&폭,&길이))return;
    if(koda_znaka==' '){Tabla_pravokotnik_polnilo(왼쪽,위쪽,폭,길이,배경색);return;}
    unsigned LOOKUP_INDEX=koda_znaka<65536?koda_znaka:koda_znaka>=0x1f600&&koda_znaka<0x1f650?65536+koda_znaka-0x1f600:0xfffd;
    const unsigned char *pisava_VALUE=Terminal_pisava+LOOKUP_INDEX*32;
    for(int Črtni=위쪽;Črtni<위쪽+길이;Črtni++){unsigned storitev_Background_Intelligent_Transfer_Service_Seznam=pisava_VALUE[(Črtni-세로좌표)*2]*256+pisava_VALUE[(Črtni-세로좌표)*2+1];for(int 칸=왼쪽;칸<왼쪽+폭;칸++)Tabla_slikovna_pika(칸,Črtni,(storitev_Background_Intelligent_Transfer_Service_Seznam&(0x8000>>(칸-koordinata_x)))?전경색:배경색);}
}
static void ime_tabela(unsigned koordinata_x,unsigned 세로좌표,const char *niz_podatki,unsigned 전경색,unsigned 배경색){while(*niz_podatki){unsigned koda_znaka=(unsigned char)*niz_podatki++, 남은수=0;if(koda_znaka>=0xc0){남은수=koda_znaka<0xe0?1:koda_znaka<0xf0?2:3;koda_znaka&=(1u<<(6-남은수))-1;while(남은수--&&*niz_podatki)koda_znaka=(koda_znaka<<6)|((unsigned char)*niz_podatki++&63);}Terminal_glif(koordinata_x,세로좌표,koda_znaka,전경색,배경색);koordinata_x+=širok_znak(koda_znaka)*8;}}
static unsigned 첫항목(void){return Terminal_vnos->맨위;}
static int 보이는지(void){return Terminal_vnos->살아있음&&Fokus>=0&&Terminal_vnos==&Windows_Seznam[Fokus]&&!화면보임(Fokus);}
static void 그리기(unsigned ROW_položaj,unsigned COLUMN_položaj){
    if(!보이는지()||ROW_položaj<첫항목()-Terminal_vnos->drseti||ROW_položaj>=첫항목()-Terminal_vnos->drseti+Terminal_vnos->ROW_COUNT||COLUMN_položaj>=Terminal_vnos->COLUMNS)return;
    unsigned koda_znaka=Terminal_vnos->글자칸들[ROW_položaj%Zgodovina_linija_COUNT][COLUMN_položaj],niz_podatki=Terminal_vnos->모양들[ROW_položaj%Zgodovina_linija_COUNT][COLUMN_položaj];
    if(širok_znak(koda_znaka)==2&&COLUMN_položaj+1>=Terminal_vnos->COLUMNS)koda_znaka=' ';
    Terminal_glif(Terminal_vnos->koordinata_x+12+COLUMN_položaj*8,Terminal_vnos->세로좌표+36+(ROW_položaj-첫항목()+Terminal_vnos->drseti)*16,koda_znaka?koda_znaka:' ',색상들[niz_podatki&15],색상들[niz_podatki>>4]);
}
static void znak_manjka_VALUE(int oddaja_okno){if(!보이는지()||Terminal_vnos->drseti||Terminal_vnos->COLUMN_položaj>=Terminal_vnos->COLUMNS||Terminal_vnos->ROW_položaj<Terminal_vnos->맨위||Terminal_vnos->ROW_položaj>=Terminal_vnos->맨위+Terminal_vnos->ROW_COUNT)return;
    if(!oddaja_okno||!Terminal_vnos->가리개보임)그리기(Terminal_vnos->ROW_položaj,Terminal_vnos->COLUMN_položaj);else 사각영역(Terminal_vnos->koordinata_x+12+Terminal_vnos->COLUMN_položaj*8,Terminal_vnos->세로좌표+36+(Terminal_vnos->ROW_položaj-Terminal_vnos->맨위)*16+14,8,2,색상들[Terminal_vnos->전경색]);}
static void vsebina_VALUE(void){
    사각영역(Terminal_vnos->koordinata_x+12,Terminal_vnos->세로좌표+36,Terminal_vnos->COLUMNS*8,Terminal_vnos->ROW_COUNT*16,색상들[0]);
    int 가로=Terminal_vnos->koordinata_x+12,Navpično_položaj=Terminal_vnos->세로좌표+36,폭=Terminal_vnos->COLUMNS*8,길이=Terminal_vnos->ROW_COUNT*16;
    if(보드그림범위(&가로,&Navpično_položaj,&폭,&길이)){
    unsigned 첫줄=(Navpično_položaj-Terminal_vnos->세로좌표-36)/16,끝줄=(Navpično_položaj+길이-Terminal_vnos->세로좌표-36+15)/16;
    unsigned 첫칸=(가로-Terminal_vnos->koordinata_x-12)/8,끝칸=(가로+폭-Terminal_vnos->koordinata_x-12+7)/8;
    if(첫칸)첫칸--; /* 잘림 경계 왼쪽에서 시작한 두 칸 글자도 그린다. */
    for(unsigned 반환값=첫줄;반환값<끝줄;반환값++)for(unsigned koda_znaka=첫칸;koda_znaka<끝칸;koda_znaka++){
        unsigned ROW_položaj=첫항목()-Terminal_vnos->drseti+반환값,znak_VALUE=Terminal_vnos->글자칸들[ROW_položaj%Zgodovina_linija_COUNT][koda_znaka],niz_podatki=Terminal_vnos->모양들[ROW_položaj%Zgodovina_linija_COUNT][koda_znaka];
        if(širok_znak(znak_VALUE)==2&&koda_znaka+1>=Terminal_vnos->COLUMNS)znak_VALUE=' ';
        if((znak_VALUE==0||znak_VALUE==' ')&&(niz_podatki>>4)==0)continue;
        Terminal_glif(Terminal_vnos->koordinata_x+12+koda_znaka*8,Terminal_vnos->세로좌표+36+반환값*16,znak_VALUE?znak_VALUE:' ',색상들[niz_podatki&15],색상들[niz_podatki>>4]);
    }}
    ime_tabela(Terminal_vnos->koordinata_x+12,Terminal_vnos->세로좌표+Terminal_vnos->višina_VALUE-18,Terminal_vnos->drseti?"PgDn: recent output":Terminal_vnos->너비>=500?"F6: next | Corner + left drag: resize":"Corner + left drag: resize",0xece8e2,0x403127);znak_manjka_VALUE(1);
}
static void 실행틀(int identifikator_VALUE){
    Terminal_vnos=&Windows_Seznam[identifikator_VALUE];
    int 가로=Terminal_vnos->koordinata_x,Navpično_položaj=Terminal_vnos->세로좌표,폭=Terminal_vnos->너비,길이=Terminal_vnos->višina_VALUE;
    if(!보드그림범위(&가로,&Navpično_položaj,&폭,&길이))return;
    사각영역(Terminal_vnos->koordinata_x,Terminal_vnos->세로좌표,Terminal_vnos->너비,Terminal_vnos->višina_VALUE,0x403127);
    unsigned 색상=identifikator_VALUE==Fokus?0x905020:0x604438;사각영역(Terminal_vnos->koordinata_x,Terminal_vnos->세로좌표,Terminal_vnos->너비,30,색상);
    ime_tabela(Terminal_vnos->koordinata_x+12,Terminal_vnos->세로좌표+7,"JKOROS Terminal",0xffffff,색상);
    char 수치[2]={(char)('1'+identifikator_VALUE),0};ime_tabela(Terminal_vnos->koordinata_x+148,Terminal_vnos->세로좌표+7,수치,0xffffff,색상);
    ime_tabela(Terminal_vnos->koordinata_x+240,Terminal_vnos->세로좌표+7,Terminal_vnos->너비>=500?(한글입력?"[SL] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[SL]":"[EN]"),0xffffff,색상);
    사각영역(Terminal_vnos->koordinata_x+Terminal_vnos->너비-32,Terminal_vnos->세로좌표+4,26,22,0x5555b8);ime_tabela(Terminal_vnos->koordinata_x+Terminal_vnos->너비-24,Terminal_vnos->세로좌표+7,"X",0xffffff,0x5555b8);
    vsebina_VALUE();
}
static void risati_prizor(void){
    if(!namizje_Pogled)return;사각영역(0,0,보드화면너비(),보드화면높이(),0x302018);사각영역(0,0,보드화면너비(),32,0x403127);
    사각영역(6,4,136,24,0x905020);ime_tabela(14,8,"+ New terminal",0xffffff,0x905020);
    for(int 순번=0;순번<4;순번++)if(Windows_Seznam[순번].살아있음){unsigned koda_znaka=Fokus==순번?0x905020:0x604438;사각영역(154+순번*112,4,106,24,koda_znaka);ime_tabela(160+순번*112,8,"Terminal",0xffffff,koda_znaka);char niz_podatki[2]={(char)('1'+순번),0};ime_tabela(232+순번*112,8,niz_podatki,0xffffff,koda_znaka);}
    if(!vnos_COUNT)ime_tabela(140,210,"Click + New terminal to start",0xede9df,0x302018);
    for(int 순번=0;순번<vnos_COUNT;순번++)실행틀(naročilo_VALUE[순번]);화면다시그림(Fokus);Terminal_vnos=&Windows_Seznam[출력결과];
}
static void Slikar_območje(int 가로,int Navpično_položaj,int 폭,int 길이){
    if(!namizje_Pogled||!보드그림범위(&가로,&Navpično_položaj,&폭,&길이))return;
    for(int Črtni=Navpično_položaj;Črtni<Navpično_položaj+길이;Črtni+=32){
        int pas_višina=Navpično_položaj+길이-Črtni;if(pas_višina>32)pas_višina=32;
        if(Tabla_Start_risba(가로,Črtni,폭,pas_višina)){risati_prizor();Tabla_konec_risba();}
    }
}
static void 다시그리기(void){Slikar_območje(0,0,보드화면너비(),보드화면높이());}
/* 서로 겹치지 않는 새 okno 영역과 이전 자리의 네 띠를 복구한다. */
static void 창자리그리기(int 가로,int Navpično_položaj,int 폭,int 길이,Terminal_d413d4bc *okno){
    int 왼쪽=가로>(int)okno->koordinata_x?가로:(int)okno->koordinata_x;
    int 위쪽=Navpično_položaj>(int)okno->세로좌표?Navpično_položaj:(int)okno->세로좌표;
    int RIGHT=가로+폭<(int)(okno->koordinata_x+okno->너비)?가로+폭:(int)(okno->koordinata_x+okno->너비);
    int 아래쪽=Navpično_položaj+길이<(int)(okno->세로좌표+okno->višina_VALUE)?Navpično_položaj+길이:(int)(okno->세로좌표+okno->višina_VALUE);
    Slikar_območje(okno->koordinata_x,okno->세로좌표,okno->너비,okno->višina_VALUE);
    if(왼쪽>=RIGHT||위쪽>=아래쪽){Slikar_območje(가로,Navpično_položaj,폭,길이);return;}
    Slikar_območje(가로,Navpično_položaj,폭,위쪽-Navpično_položaj);
    Slikar_območje(가로,아래쪽,폭,Navpično_položaj+길이-아래쪽);
    Slikar_območje(가로,위쪽,왼쪽-가로,아래쪽-위쪽);
    Slikar_območje(RIGHT,위쪽,가로+폭-RIGHT,아래쪽-위쪽);
}
static void signal_Fokus(void){informacijska_tehnologija_čakajoče=(informacijska_tehnologija_čakajoče&~15u)|(unsigned)(Fokus+1)|0x10000;}
void 터미널입력방식(unsigned 한글여부){
    한글입력=한글여부!=0;
    /* Update title bars only: a mode switch must not erase an EL0 drawing. */
    if(Fokus>=0){
        Terminal_d413d4bc *okno_vnos=&Windows_Seznam[Fokus];
        ime_tabela(okno_vnos->koordinata_x+240,okno_vnos->세로좌표+7,okno_vnos->너비>=500?(한글입력?"[SL] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[SL]":"[EN]"),0xffffff,0x905020);
    }
}
static void 앞으로올리기(int identifikator_VALUE){if(identifikator_VALUE<0||identifikator_VALUE>=4||!Windows_Seznam[identifikator_VALUE].살아있음)return;int sprotno_položaj=0;while(sprotno_položaj<vnos_COUNT&&naročilo_VALUE[sprotno_položaj]!=identifikator_VALUE)sprotno_položaj++;for(;sprotno_položaj+1<vnos_COUNT;sprotno_položaj++)naročilo_VALUE[sprotno_položaj]=naročilo_VALUE[sprotno_položaj+1];naročilo_VALUE[vnos_COUNT-1]=identifikator_VALUE;Fokus=identifikator_VALUE;signal_Fokus();다시그리기();}
static void 빈칸채우기(unsigned ROW_položaj){for(unsigned koda_znaka=0;koda_znaka<최대열수;koda_znaka++){Terminal_vnos->글자칸들[ROW_položaj%Zgodovina_linija_COUNT][koda_znaka]=0;Terminal_vnos->모양들[ROW_položaj%Zgodovina_linija_COUNT][koda_znaka]=Terminal_vnos->전경색|(Terminal_vnos->배경색<<4);}}
static void počistiti_Vsebina(void){Terminal_vnos->ROW_položaj=Terminal_vnos->COLUMN_položaj=Terminal_vnos->맨위=Terminal_vnos->drseti=0;for(unsigned 반환값=0;반환값<Zgodovina_linija_COUNT;반환값++)빈칸채우기(반환값);if(보이는지())vsebina_VALUE();}
static int Ustvari_vnos(void){
    if(!보드화면기억공간())return -19;int identifikator_VALUE=0;while(identifikator_VALUE<4&&Windows_Seznam[identifikator_VALUE].살아있음)identifikator_VALUE++;if(identifikator_VALUE==4)return -28;
    namizje_Pogled=1;Terminal_vnos=&Windows_Seznam[identifikator_VALUE];memset(Terminal_vnos,0,sizeof(*Terminal_vnos));Terminal_vnos->살아있음=1;Terminal_vnos->너비=568;Terminal_vnos->višina_VALUE=360;Terminal_vnos->COLUMNS=68;Terminal_vnos->ROW_COUNT=19;Terminal_vnos->koordinata_x=12+identifikator_VALUE*16;Terminal_vnos->세로좌표=48+identifikator_VALUE*18;Terminal_vnos->전경색=7;Terminal_vnos->가리개보임=1;
    for(unsigned 반환값=0;반환값<Zgodovina_linija_COUNT;반환값++)빈칸채우기(반환값);naročilo_VALUE[vnos_COUNT++]=identifikator_VALUE;Fokus=identifikator_VALUE;informacijska_tehnologija_čakajoče|=1u<<(4+identifikator_VALUE);signal_Fokus();다시그리기();return identifikator_VALUE+1;
}
static void Zapri_okno(int identifikator_VALUE){
    if(identifikator_VALUE<0||identifikator_VALUE>=4||!Windows_Seznam[identifikator_VALUE].살아있음)return;Windows_Seznam[identifikator_VALUE].살아있음=0;informacijska_tehnologija_čakajoče|=1u<<(8+identifikator_VALUE);
    int sprotno_položaj=0;while(sprotno_položaj<vnos_COUNT&&naročilo_VALUE[sprotno_položaj]!=identifikator_VALUE)sprotno_položaj++;for(;sprotno_položaj+1<vnos_COUNT;sprotno_položaj++)naročilo_VALUE[sprotno_položaj]=naročilo_VALUE[sprotno_položaj+1];vnos_COUNT--;
    if(Fokus==identifikator_VALUE)Fokus=vnos_COUNT?naročilo_VALUE[vnos_COUNT-1]:-1;signal_Fokus();다시그리기();
}
static void 줄바꿈(void){Terminal_vnos->COLUMN_položaj=0;Terminal_vnos->ROW_položaj++;if(Terminal_vnos->ROW_položaj>=Terminal_vnos->맨위+Terminal_vnos->ROW_COUNT){Terminal_vnos->맨위++;빈칸채우기(Terminal_vnos->ROW_položaj);if(보이는지())vsebina_VALUE();}}
static void koda_znaka_451f2815(unsigned koda_znaka){
    if(koda_znaka==13){Terminal_vnos->COLUMN_položaj=0;return;}if(koda_znaka==10){줄바꿈();return;}if(koda_znaka==8){if(Terminal_vnos->COLUMN_položaj)Terminal_vnos->COLUMN_položaj--;return;}
    if(koda_znaka==9){unsigned element_COUNT=8-Terminal_vnos->COLUMN_položaj%8;while(element_COUNT--)koda_znaka_451f2815(' ');return;}if(koda_znaka<32||koda_znaka==127)return;
    unsigned 너비값=širok_znak(koda_znaka);if(Terminal_vnos->COLUMN_položaj+너비값>Terminal_vnos->COLUMNS)줄바꿈();
    if(Terminal_vnos->글자칸들[Terminal_vnos->ROW_položaj%Zgodovina_linija_COUNT][Terminal_vnos->COLUMN_položaj]==0xffffffffu&&Terminal_vnos->COLUMN_položaj){Terminal_vnos->글자칸들[Terminal_vnos->ROW_položaj%Zgodovina_linija_COUNT][Terminal_vnos->COLUMN_položaj-1]=' ';그리기(Terminal_vnos->ROW_položaj,Terminal_vnos->COLUMN_položaj-1);}
    if(širok_znak(Terminal_vnos->글자칸들[Terminal_vnos->ROW_položaj%Zgodovina_linija_COUNT][Terminal_vnos->COLUMN_položaj])==2&&Terminal_vnos->COLUMN_položaj+1<Terminal_vnos->COLUMNS){Terminal_vnos->글자칸들[Terminal_vnos->ROW_položaj%Zgodovina_linija_COUNT][Terminal_vnos->COLUMN_položaj+1]=' ';그리기(Terminal_vnos->ROW_položaj,Terminal_vnos->COLUMN_položaj+1);}
    Terminal_vnos->글자칸들[Terminal_vnos->ROW_položaj%Zgodovina_linija_COUNT][Terminal_vnos->COLUMN_položaj]=koda_znaka;Terminal_vnos->모양들[Terminal_vnos->ROW_položaj%Zgodovina_linija_COUNT][Terminal_vnos->COLUMN_položaj]=Terminal_vnos->전경색|(Terminal_vnos->배경색<<4);
    if(너비값==2)Terminal_vnos->글자칸들[Terminal_vnos->ROW_položaj%Zgodovina_linija_COUNT][Terminal_vnos->COLUMN_položaj+1]=0xffffffffu;
    그리기(Terminal_vnos->ROW_položaj,Terminal_vnos->COLUMN_položaj);Terminal_vnos->COLUMN_položaj+=너비값;
}
static void ročica_nadzor_SEQUENCE(unsigned koda_znaka){
    unsigned element_COUNT=Terminal_vnos->parameter_VALUE[0]?Terminal_vnos->parameter_VALUE[0]:1;
    if(koda_znaka=='m')for(unsigned 순번=0;순번<=Terminal_vnos->parameter_INDEX;순번++){unsigned podatki_položaj=Terminal_vnos->parameter_VALUE[순번];if(!podatki_položaj){Terminal_vnos->전경색=7;Terminal_vnos->배경색=0;}if(podatki_položaj==1&&Terminal_vnos->전경색<8)Terminal_vnos->전경색+=8;if(podatki_položaj==7){unsigned 유지=Terminal_vnos->전경색;Terminal_vnos->전경색=Terminal_vnos->배경색;Terminal_vnos->배경색=유지;}if(podatki_položaj>=30&&podatki_položaj<=37)Terminal_vnos->전경색=podatki_položaj-30;if(podatki_položaj>=90&&podatki_položaj<=97)Terminal_vnos->전경색=podatki_položaj-90+8;if(podatki_položaj>=40&&podatki_položaj<=47)Terminal_vnos->배경색=podatki_položaj-40;if(podatki_položaj>=100&&podatki_položaj<=107)Terminal_vnos->배경색=podatki_položaj-100+8;if(podatki_položaj==39)Terminal_vnos->전경색=7;if(podatki_položaj==49)Terminal_vnos->배경색=0;}
    if(koda_znaka=='J'&&(Terminal_vnos->parameter_VALUE[0]==2||Terminal_vnos->parameter_VALUE[0]==3))počistiti_Vsebina();
    if(koda_znaka=='K'){unsigned 출발위치=Terminal_vnos->parameter_VALUE[0]==2?0:Terminal_vnos->COLUMN_položaj,도착위치=Terminal_vnos->parameter_VALUE[0]==1?Terminal_vnos->COLUMN_položaj+1:Terminal_vnos->COLUMNS;if(Terminal_vnos->parameter_VALUE[0]==1)출발위치=0;for(unsigned 순번=출발위치;순번<도착위치&&순번<Terminal_vnos->COLUMNS;순번++){
        unsigned ROW_VALUE=Terminal_vnos->ROW_položaj%Zgodovina_linija_COUNT,znak_VALUE=Terminal_vnos->글자칸들[ROW_VALUE][순번],oblika_VALUE_f1cd655a=Terminal_vnos->전경색|(Terminal_vnos->배경색<<4);
        /* 넓은 vi 화면에서도 이미 빈 칸의 pisava_VALUE 화소를 되풀이해 칠하지 않는다. */
        int 바뀜=(znak_VALUE!=0&&znak_VALUE!=' ')||Terminal_vnos->모양들[ROW_VALUE][순번]!=oblika_VALUE_f1cd655a;
        Terminal_vnos->글자칸들[ROW_VALUE][순번]=' ';Terminal_vnos->모양들[ROW_VALUE][순번]=oblika_VALUE_f1cd655a;
        if(바뀜)그리기(Terminal_vnos->ROW_položaj,순번);
    }}
    if(koda_znaka=='D')Terminal_vnos->COLUMN_položaj=element_COUNT>Terminal_vnos->COLUMN_položaj?0:Terminal_vnos->COLUMN_položaj-element_COUNT;if(koda_znaka=='C')Terminal_vnos->COLUMN_položaj=Terminal_vnos->COLUMN_položaj+element_COUNT>=Terminal_vnos->COLUMNS?Terminal_vnos->COLUMNS-1:Terminal_vnos->COLUMN_položaj+element_COUNT;
    if(koda_znaka=='G')Terminal_vnos->COLUMN_položaj=element_COUNT>Terminal_vnos->COLUMNS?Terminal_vnos->COLUMNS-1:element_COUNT-1;if(koda_znaka=='A')Terminal_vnos->ROW_položaj=element_COUNT>Terminal_vnos->ROW_položaj-Terminal_vnos->맨위?Terminal_vnos->맨위:Terminal_vnos->ROW_položaj-element_COUNT;
    if(koda_znaka=='B')Terminal_vnos->ROW_položaj=Terminal_vnos->ROW_položaj+element_COUNT>=Terminal_vnos->맨위+Terminal_vnos->ROW_COUNT?Terminal_vnos->맨위+Terminal_vnos->ROW_COUNT-1:Terminal_vnos->ROW_položaj+element_COUNT;
    if(koda_znaka=='H'||koda_znaka=='f'){Terminal_vnos->ROW_položaj=Terminal_vnos->맨위+(element_COUNT>Terminal_vnos->ROW_COUNT?Terminal_vnos->ROW_COUNT:element_COUNT)-1;unsigned koordinata_x=Terminal_vnos->parameter_VALUE[1]?Terminal_vnos->parameter_VALUE[1]:1;Terminal_vnos->COLUMN_položaj=(koordinata_x>Terminal_vnos->COLUMNS?Terminal_vnos->COLUMNS:koordinata_x)-1;}
    if(koda_znaka=='s'){Terminal_vnos->저장행=Terminal_vnos->ROW_položaj;Terminal_vnos->저장열=Terminal_vnos->COLUMN_položaj;}if(koda_znaka=='u'){Terminal_vnos->ROW_položaj=Terminal_vnos->저장행;Terminal_vnos->COLUMN_položaj=Terminal_vnos->저장열<Terminal_vnos->COLUMNS?Terminal_vnos->저장열:Terminal_vnos->COLUMNS-1;}
    if((koda_znaka=='h'||koda_znaka=='l')&&Terminal_vnos->parameter_VALUE[0]==25)Terminal_vnos->가리개보임=koda_znaka=='h';
}
void Terminal_bajt(unsigned SECOND_VALUE){
    Terminal_vnos=&Windows_Seznam[출력결과];if(!Terminal_vnos->살아있음)return;znak_manjka_VALUE(0);if(Terminal_vnos->drseti){Terminal_vnos->drseti=0;if(보이는지())vsebina_VALUE();}
    if(Terminal_vnos->탈출상태==1){Terminal_vnos->탈출상태=SECOND_VALUE=='['?2:0;Terminal_vnos->parameter_INDEX=0;for(unsigned 순번=0;순번<4;순번++)Terminal_vnos->parameter_VALUE[순번]=0;}
    else if(Terminal_vnos->탈출상태==2){if(SECOND_VALUE=='?'){}else if(SECOND_VALUE>='0'&&SECOND_VALUE<='9'){if(Terminal_vnos->parameter_VALUE[Terminal_vnos->parameter_INDEX]<10000)Terminal_vnos->parameter_VALUE[Terminal_vnos->parameter_INDEX]=Terminal_vnos->parameter_VALUE[Terminal_vnos->parameter_INDEX]*10+SECOND_VALUE-'0';}else if(SECOND_VALUE==';'&&Terminal_vnos->parameter_INDEX<3)Terminal_vnos->parameter_INDEX++;else{ročica_nadzor_SEQUENCE(SECOND_VALUE);Terminal_vnos->탈출상태=0;}}
    else if(SECOND_VALUE==27){Terminal_vnos->긴부호없는값=0;Terminal_vnos->탈출상태=1;}else{
        if(Terminal_vnos->긴부호없는값&&(SECOND_VALUE&0xc0)!=0x80){Terminal_vnos->긴부호없는값=0;koda_znaka_451f2815(0xfffd);}
        if(Terminal_vnos->긴부호없는값){Terminal_vnos->부호없는결과=Terminal_vnos->부호없는결과*64+(SECOND_VALUE&63);if(--Terminal_vnos->긴부호없는값==0)koda_znaka_451f2815(Terminal_vnos->부호없는결과<Terminal_vnos->SMALL_VALUE||Terminal_vnos->부호없는결과>0x10ffff||(Terminal_vnos->부호없는결과>=0xd800&&Terminal_vnos->부호없는결과<=0xdfff)?0xfffd:Terminal_vnos->부호없는결과);}
        else if(SECOND_VALUE<128)koda_znaka_451f2815(SECOND_VALUE);else if(SECOND_VALUE>=0xc2&&SECOND_VALUE<=0xf4){Terminal_vnos->긴부호없는값=SECOND_VALUE<0xe0?1:SECOND_VALUE<0xf0?2:3;Terminal_vnos->부호없는결과=SECOND_VALUE&((1u<<(6-Terminal_vnos->긴부호없는값))-1);Terminal_vnos->SMALL_VALUE=Terminal_vnos->긴부호없는값==1?128:Terminal_vnos->긴부호없는값==2?2048:65536;}else koda_znaka_451f2815(0xfffd);
    }znak_manjka_VALUE(1);
}
int Terminal_čakajoče(void){return informacijska_tehnologija_čakajoče!=0;}
/* 모서리 INDEX: 1 좌상, 2 우상, 3 좌하, 4 우하. */
static int spreminjati_velikost_povleči=-1,잡은모서리,잡은가로,잡은세로,처음가로,처음세로,처음너비,처음높이;
static int 가리킨창(int 가로,int Navpično_položaj) {
    for(int SEQUENCE_VALUE=vnos_COUNT-1;SEQUENCE_VALUE>=0;SEQUENCE_VALUE--){
        int identifikator_VALUE=naročilo_VALUE[SEQUENCE_VALUE];Terminal_d413d4bc *okno=&Windows_Seznam[identifikator_VALUE];
        if(가로>=(int)okno->koordinata_x&&Navpično_položaj>=(int)okno->세로좌표&&
           가로<(int)(okno->koordinata_x+okno->너비)&&Navpično_položaj<(int)(okno->세로좌표+okno->višina_VALUE))return identifikator_VALUE;
    }return -1;
}
static int 모서리찾기(int identifikator_VALUE,int 가로,int Navpično_položaj) {
    if(identifikator_VALUE<0)return 0;Terminal_d413d4bc *okno=&Windows_Seznam[identifikator_VALUE];
    int 왼쪽=가로<(int)okno->koordinata_x+8,RIGHT=가로>=(int)(okno->koordinata_x+okno->너비)-8;
    int 위쪽=Navpično_položaj<(int)okno->세로좌표+8,아래쪽=Navpično_položaj>=(int)(okno->세로좌표+okno->višina_VALUE)-8;
    return (왼쪽||RIGHT)&&(위쪽||아래쪽)?1+RIGHT+아래쪽*2:0;
}
static int ločilo_VALUE(int VALUE,int 최소,int 최대){return VALUE<최소?최소:VALUE>최대?최대:VALUE;}
static void premikati_spreminjati_velikost(int 가로,int Navpično_položaj) {
    Terminal_d413d4bc *okno=&Windows_Seznam[spreminjati_velikost_povleči];int 왼쪽=처음가로,위쪽=처음세로,RIGHT=처음가로+처음너비,아래쪽=처음세로+처음높이;
    if(잡은모서리==1||잡은모서리==3)왼쪽=ločilo_VALUE(처음가로+가로-잡은가로,0,RIGHT-360);
    else RIGHT=ločilo_VALUE(처음가로+처음너비+가로-잡은가로,왼쪽+360,보드화면너비());
    if(잡은모서리<=2)위쪽=ločilo_VALUE(처음세로+Navpično_položaj-잡은세로,34,아래쪽-216);
    else 아래쪽=ločilo_VALUE(처음세로+처음높이+Navpično_položaj-잡은세로,위쪽+216,보드화면높이());
    unsigned COLUMNS=(RIGHT-왼쪽-24)/8,ROW_COUNT=(아래쪽-위쪽-56)/16;
    if(okno->COLUMNS!=COLUMNS||okno->ROW_COUNT!=ROW_COUNT){
        okno->크기바뀜=1;okno->COLUMNS=COLUMNS;okno->ROW_COUNT=ROW_COUNT;
        if(okno->COLUMN_položaj>=COLUMNS)okno->COLUMN_položaj=COLUMNS-1;
        if(okno->ROW_položaj>=okno->맨위+ROW_COUNT)okno->맨위=okno->ROW_položaj-ROW_COUNT+1;
        unsigned 한도=okno->맨위;if(한도>Zgodovina_linija_COUNT-ROW_COUNT)한도=Zgodovina_linija_COUNT-ROW_COUNT;
        if(okno->drseti>한도)okno->drseti=한도;
    }
    int 옛가로=okno->koordinata_x,옛세로=okno->세로좌표,옛폭=okno->너비,옛길이=okno->višina_VALUE;
    if(옛가로==왼쪽&&옛세로==위쪽&&옛폭==RIGHT-왼쪽&&옛길이==아래쪽-위쪽)return;
    okno->koordinata_x=왼쪽;okno->세로좌표=위쪽;okno->너비=RIGHT-왼쪽;okno->višina_VALUE=아래쪽-위쪽;
    창자리그리기(옛가로,옛세로,옛폭,옛길이,okno);
}
void Terminal_kazalec(unsigned Naprej_element,int koordinata_x,int 세로좌표){
    unsigned 눌림=Naprej_element&~단추들;단추들=Naprej_element;
    if(!namizje_Pogled){povleči_VALUE=-1;spreminjati_velikost_povleči=-1;Tabla_kazalec(koordinata_x,세로좌표,1);return;}
    if(!(Naprej_element&1)){povleči_VALUE=-1;spreminjati_velikost_povleči=-1;}
    if(spreminjati_velikost_povleči>=0&&!Windows_Seznam[spreminjati_velikost_povleči].살아있음)spreminjati_velikost_povleči=-1;
    if(povleči_VALUE>=0&&!Windows_Seznam[povleči_VALUE].살아있음)povleči_VALUE=-1;
    if(spreminjati_velikost_povleči>=0){
        premikati_spreminjati_velikost(koordinata_x,세로좌표);Tabla_kazalec(koordinata_x,세로좌표,잡은모서리==1||잡은모서리==4?2:3);return;
    }
    Tabla_kazalec(koordinata_x,세로좌표,1);
    if(povleči_VALUE>=0){
        Terminal_d413d4bc *okno=&Windows_Seznam[povleči_VALUE];
        int 옛가로=okno->koordinata_x,옛세로=okno->세로좌표;
        okno->koordinata_x=ločilo_VALUE(koordinata_x-povleči_X,0,보드화면너비()-okno->너비);
        okno->세로좌표=ločilo_VALUE(세로좌표-povleči_Y,34,보드화면높이()-okno->višina_VALUE);
        if(옛가로!=(int)okno->koordinata_x||옛세로!=(int)okno->세로좌표)창자리그리기(옛가로,옛세로,okno->너비,okno->višina_VALUE,okno);
        return;
    }
    extern int 화면덮음(int,int,int);
    if(화면덮음(Fokus,koordinata_x,세로좌표)){화면가리킴(Fokus,눌림,koordinata_x,세로좌표);return;}
    int identifikator_VALUE=가리킨창(koordinata_x,세로좌표),모서리=모서리찾기(identifikator_VALUE,koordinata_x,세로좌표);
    if(모서리)Tabla_kazalec(koordinata_x,세로좌표,모서리==1||모서리==4?2:3);
    if(눌림&1){
        if(모서리){
            Terminal_d413d4bc *okno=&Windows_Seznam[identifikator_VALUE];spreminjati_velikost_povleči=identifikator_VALUE;잡은모서리=모서리;잡은가로=koordinata_x;잡은세로=세로좌표;
            처음가로=okno->koordinata_x;처음세로=okno->세로좌표;처음너비=okno->너비;처음높이=okno->višina_VALUE;
            if(identifikator_VALUE!=Fokus)앞으로올리기(identifikator_VALUE);return;
        }
        if(세로좌표<32&&koordinata_x>=6&&koordinata_x<142){Ustvari_vnos();return;}
        if(세로좌표<32&&koordinata_x>=154&&koordinata_x<602){앞으로올리기((koordinata_x-154)/112);return;}
        if(identifikator_VALUE>=0){
            Terminal_d413d4bc *okno=&Windows_Seznam[identifikator_VALUE];
            if(세로좌표<(int)okno->세로좌표+30&&koordinata_x>=(int)(okno->koordinata_x+okno->너비)-32){Zapri_okno(identifikator_VALUE);return;}
            if(identifikator_VALUE!=Fokus)앞으로올리기(identifikator_VALUE);
            if(세로좌표<(int)okno->세로좌표+30){povleči_VALUE=identifikator_VALUE;povleči_X=koordinata_x-okno->koordinata_x;povleči_Y=세로좌표-okno->세로좌표;}return;
        }
    }
    if(Fokus>=0&&(눌림&(8|16))){Terminal_vnos=&Windows_Seznam[Fokus];if(눌림&8){unsigned 한도=Terminal_vnos->맨위;if(한도>Zgodovina_linija_COUNT-Terminal_vnos->ROW_COUNT)한도=Zgodovina_linija_COUNT-Terminal_vnos->ROW_COUNT;Terminal_vnos->drseti=Terminal_vnos->drseti+9>한도?한도:Terminal_vnos->drseti+9;}else Terminal_vnos->drseti=Terminal_vnos->drseti<9?0:Terminal_vnos->drseti-9;다시그리기();}
}
void 터미널바로가기키(unsigned 누름값){if(누름값==1)Ustvari_vnos();if(누름값==2&&vnos_COUNT)앞으로올리기(naročilo_VALUE[0]);if(누름값==3)Zapri_okno(Fokus);}
računalnik_Word Tabla_Terminal(računalnik_Word Dejanje){
    if(Dejanje==300){if(!Windows_Seznam[출력결과].살아있음)return Ustvari_vnos();namizje_Pogled=1;다시그리기();return 0;}
    if(Dejanje==0){Zapri_okno(Fokus);return 0;}if(Dejanje==1)return (uint32_t)Ustvari_vnos();if(Dejanje==2)return Fokus>=0;
    if(Dejanje==9){namizje_Pogled=0;return 0;}if(Dejanje==7)return vnos_COUNT;if(Dejanje==10)return Fokus+1;if(Dejanje==11)return 출력결과;
    if(Dejanje==13){Terminal_d413d4bc *okno=&Windows_Seznam[출력결과];return okno->살아있음?(okno->ROW_COUNT<<16)|okno->COLUMNS:(19<<16)|68;}
    if(Dejanje==14){unsigned VALUE=Windows_Seznam[출력결과].크기바뀜;Windows_Seznam[출력결과].크기바뀜=0;return VALUE;}
    if(Dejanje==12){unsigned VALUE=informacijska_tehnologija_čakajoče;informacijska_tehnologija_čakajoče=0;return VALUE;}
    if(Dejanje>=20&&Dejanje<24)return Windows_Seznam[Dejanje-20].살아있음;
    if(Dejanje>=100&&Dejanje<104){출력결과=Dejanje-100;Terminal_vnos=&Windows_Seznam[출력결과];return 0;}
    if(Dejanje>=200&&Dejanje<204){앞으로올리기(Dejanje-200);return 0;}
    if(Dejanje==3){다시그리기();return 0;}Terminal_vnos=&Windows_Seznam[출력결과];if(!Terminal_vnos->살아있음)return 0;
    if(Dejanje==4)počistiti_Vsebina();if(Dejanje==5||Dejanje==6){unsigned 이전=단추들;Terminal_kazalec(Dejanje==5?8:16,0,0);단추들=이전;}return 1;
}
