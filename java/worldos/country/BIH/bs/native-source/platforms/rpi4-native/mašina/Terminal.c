#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* 자체 네 prozor 합성과 UTF-8 Terminal. 바뀐 영역의 완성 그림만 표시한다. */
#include <stdint.h>
#include <stddef.h>
typedef uintptr_t mašina_Word;
extern mašina_Word ploča_pel(mašina_Word,mašina_Word,mašina_Word),보드화면기억공간(void);
extern void *memset(void *,int,size_t);
extern const unsigned char Terminal_font[];
#define 최대열수 237
#define Historija_redak_COUNT 160
typedef struct {
    uint32_t 글자칸들[Historija_redak_COUNT][최대열수]; uint8_t 모양들[Historija_redak_COUNT][최대열수];
    unsigned 너비,높이,Kolone,ROW_COUNT,크기바뀜;
    unsigned 살아있음,koordinata_x,Y_koordinata,ROW_položaj,COLUMN_položaj,맨위,klizati,전경색,배경색,탈출상태,parametar_VALUE[4],parametar_INDEX,저장행,저장열;
    unsigned 부호없는결과,긴부호없는값,SMALL_VALUE,대체화면,가리개보임;
} Terminal_d413d4bc;
static Terminal_d413d4bc Windows_spisak[4];
static int Fokus=-1,출력결과,redoslijed_VALUE[4],unos_COUNT,prevući_VALUE=-1,prevući_X,prevući_Y;
static unsigned odjel_za_informacijske_tehnologije_na_čekanju,단추들,desktop_Prikaz,한글입력;
static const uint32_t 색상들[16]={0x201a15,0x6060df,0x9dcc86,0x80cfea,0xefaf72,0xca96c9,0xceda76,0xede9df,0x858078,0x8888ff,0xb9eba7,0xa5eaff,0xffcc99,0xf0bef1,0xf0f0a0,0xffffff};
extern int 화면보임(int),화면가리킴(int,unsigned,int,int);
extern void 화면다시그림(int);
static Terminal_d413d4bc *Terminal_unos;
static unsigned 넓은글자(unsigned kôd_znaka){return kôd_znaka>=256?2:1;}
static void 사각영역(unsigned koordinata_x,unsigned Y_koordinata,unsigned 너비값,unsigned 높이값,unsigned 색상){
    보드사각그림(koordinata_x,Y_koordinata,너비값,높이값,색상);
}
void Terminal_glif(unsigned koordinata_x,unsigned Y_koordinata,unsigned kôd_znaka,unsigned 전경색,unsigned 배경색){
    unsigned 너비=넓은글자(kôd_znaka)*8;if(kôd_znaka==0xffffffffu)return;
    int 왼쪽=koordinata_x,위쪽=Y_koordinata,폭=너비,dužina_VALUE=16;
    if(!보드그림범위(&왼쪽,&위쪽,&폭,&dužina_VALUE))return;
    if(kôd_znaka==' '){보드사각그림(왼쪽,위쪽,폭,dužina_VALUE,배경색);return;}
    unsigned LOOKUP_INDEX=kôd_znaka<65536?kôd_znaka:kôd_znaka>=0x1f600&&kôd_znaka<0x1f650?65536+kôd_znaka-0x1f600:0xfffd;
    const unsigned char *font_VALUE=Terminal_font+LOOKUP_INDEX*32;
    for(int Linija=위쪽;Linija<위쪽+dužina_VALUE;Linija++){unsigned 비트들=font_VALUE[(Linija-Y_koordinata)*2]*256+font_VALUE[(Linija-Y_koordinata)*2+1];for(int prostor_za_unos_unos=왼쪽;prostor_za_unos_unos<왼쪽+폭;prostor_za_unos_unos++)ploča_pel(prostor_za_unos_unos,Linija,(비트들&(0x8000>>(prostor_za_unos_unos-koordinata_x)))?전경색:배경색);}
}
static void naziv_tabela(unsigned koordinata_x,unsigned Y_koordinata,const char *string_podaci,unsigned 전경색,unsigned 배경색){while(*string_podaci){unsigned kôd_znaka=(unsigned char)*string_podaci++, 남은수=0;if(kôd_znaka>=0xc0){남은수=kôd_znaka<0xe0?1:kôd_znaka<0xf0?2:3;kôd_znaka&=(1u<<(6-남은수))-1;while(남은수--&&*string_podaci)kôd_znaka=(kôd_znaka<<6)|((unsigned char)*string_podaci++&63);}Terminal_glif(koordinata_x,Y_koordinata,kôd_znaka,전경색,배경색);koordinata_x+=넓은글자(kôd_znaka)*8;}}
static unsigned 첫항목(void){return Terminal_unos->맨위;}
static int 보이는지(void){return Terminal_unos->살아있음&&Fokus>=0&&Terminal_unos==&Windows_spisak[Fokus]&&!화면보임(Fokus);}
static void 그리기(unsigned ROW_položaj,unsigned COLUMN_položaj){
    if(!보이는지()||ROW_položaj<첫항목()-Terminal_unos->klizati||ROW_položaj>=첫항목()-Terminal_unos->klizati+Terminal_unos->ROW_COUNT||COLUMN_položaj>=Terminal_unos->Kolone)return;
    unsigned kôd_znaka=Terminal_unos->글자칸들[ROW_položaj%Historija_redak_COUNT][COLUMN_položaj],string_podaci=Terminal_unos->모양들[ROW_položaj%Historija_redak_COUNT][COLUMN_položaj];
    if(넓은글자(kôd_znaka)==2&&COLUMN_položaj+1>=Terminal_unos->Kolone)kôd_znaka=' ';
    Terminal_glif(Terminal_unos->koordinata_x+12+COLUMN_položaj*8,Terminal_unos->Y_koordinata+36+(ROW_položaj-첫항목()+Terminal_unos->klizati)*16,kôd_znaka?kôd_znaka:' ',색상들[string_podaci&15],색상들[string_podaci>>4]);
}
static void simbol_VALUE_be8150db(int program_prozor){if(!보이는지()||Terminal_unos->klizati||Terminal_unos->COLUMN_položaj>=Terminal_unos->Kolone||Terminal_unos->ROW_položaj<Terminal_unos->맨위||Terminal_unos->ROW_položaj>=Terminal_unos->맨위+Terminal_unos->ROW_COUNT)return;
    if(!program_prozor||!Terminal_unos->가리개보임)그리기(Terminal_unos->ROW_položaj,Terminal_unos->COLUMN_položaj);else 사각영역(Terminal_unos->koordinata_x+12+Terminal_unos->COLUMN_položaj*8,Terminal_unos->Y_koordinata+36+(Terminal_unos->ROW_položaj-Terminal_unos->맨위)*16+14,8,2,색상들[Terminal_unos->전경색]);}
static void Sadržaj_VALUE(void){
    사각영역(Terminal_unos->koordinata_x+12,Terminal_unos->Y_koordinata+36,Terminal_unos->Kolone*8,Terminal_unos->ROW_COUNT*16,색상들[0]);
    int 가로=Terminal_unos->koordinata_x+12,Vertikalno_položaj=Terminal_unos->Y_koordinata+36,폭=Terminal_unos->Kolone*8,dužina_VALUE=Terminal_unos->ROW_COUNT*16;
    if(보드그림범위(&가로,&Vertikalno_položaj,&폭,&dužina_VALUE)){
    unsigned 첫줄=(Vertikalno_položaj-Terminal_unos->Y_koordinata-36)/16,끝줄=(Vertikalno_položaj+dužina_VALUE-Terminal_unos->Y_koordinata-36+15)/16;
    unsigned 첫칸=(가로-Terminal_unos->koordinata_x-12)/8,끝칸=(가로+폭-Terminal_unos->koordinata_x-12+7)/8;
    if(첫칸)첫칸--; /* 잘림 경계 왼쪽에서 시작한 두 prostor_za_unos_unos 글자도 그린다. */
    for(unsigned 반환값=첫줄;반환값<끝줄;반환값++)for(unsigned kôd_znaka=첫칸;kôd_znaka<끝칸;kôd_znaka++){
        unsigned ROW_položaj=첫항목()-Terminal_unos->klizati+반환값,znak_VALUE=Terminal_unos->글자칸들[ROW_položaj%Historija_redak_COUNT][kôd_znaka],string_podaci=Terminal_unos->모양들[ROW_položaj%Historija_redak_COUNT][kôd_znaka];
        if(넓은글자(znak_VALUE)==2&&kôd_znaka+1>=Terminal_unos->Kolone)znak_VALUE=' ';
        if((znak_VALUE==0||znak_VALUE==' ')&&(string_podaci>>4)==0)continue;
        Terminal_glif(Terminal_unos->koordinata_x+12+kôd_znaka*8,Terminal_unos->Y_koordinata+36+반환값*16,znak_VALUE?znak_VALUE:' ',색상들[string_podaci&15],색상들[string_podaci>>4]);
    }}
    naziv_tabela(Terminal_unos->koordinata_x+12,Terminal_unos->Y_koordinata+Terminal_unos->높이-18,Terminal_unos->klizati?"PgDn: recent output":Terminal_unos->너비>=500?"F6: next | Corner + left drag: resize":"Corner + left drag: resize",0xece8e2,0x403127);simbol_VALUE_be8150db(1);
}
static void 실행틀(int identifikator_VALUE){
    Terminal_unos=&Windows_spisak[identifikator_VALUE];
    int 가로=Terminal_unos->koordinata_x,Vertikalno_položaj=Terminal_unos->Y_koordinata,폭=Terminal_unos->너비,dužina_VALUE=Terminal_unos->높이;
    if(!보드그림범위(&가로,&Vertikalno_položaj,&폭,&dužina_VALUE))return;
    사각영역(Terminal_unos->koordinata_x,Terminal_unos->Y_koordinata,Terminal_unos->너비,Terminal_unos->높이,0x403127);
    unsigned 색상=identifikator_VALUE==Fokus?0x905020:0x604438;사각영역(Terminal_unos->koordinata_x,Terminal_unos->Y_koordinata,Terminal_unos->너비,30,색상);
    naziv_tabela(Terminal_unos->koordinata_x+12,Terminal_unos->Y_koordinata+7,"JKOROS Terminal",0xffffff,색상);
    char 수치[2]={(char)('1'+identifikator_VALUE),0};naziv_tabela(Terminal_unos->koordinata_x+148,Terminal_unos->Y_koordinata+7,수치,0xffffff,색상);
    naziv_tabela(Terminal_unos->koordinata_x+240,Terminal_unos->Y_koordinata+7,Terminal_unos->너비>=500?(한글입력?"[BS] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[BS]":"[EN]"),0xffffff,색상);
    사각영역(Terminal_unos->koordinata_x+Terminal_unos->너비-32,Terminal_unos->Y_koordinata+4,26,22,0x5555b8);naziv_tabela(Terminal_unos->koordinata_x+Terminal_unos->너비-24,Terminal_unos->Y_koordinata+7,"X",0xffffff,0x5555b8);
    Sadržaj_VALUE();
}
static void 장면그리기(void){
    if(!desktop_Prikaz)return;사각영역(0,0,보드화면너비(),보드화면높이(),0x302018);사각영역(0,0,보드화면너비(),32,0x403127);
    사각영역(6,4,136,24,0x905020);naziv_tabela(14,8,"+ New terminal",0xffffff,0x905020);
    for(int 순번=0;순번<4;순번++)if(Windows_spisak[순번].살아있음){unsigned kôd_znaka=Fokus==순번?0x905020:0x604438;사각영역(154+순번*112,4,106,24,kôd_znaka);naziv_tabela(160+순번*112,8,"Terminal",0xffffff,kôd_znaka);char string_podaci[2]={(char)('1'+순번),0};naziv_tabela(232+순번*112,8,string_podaci,0xffffff,kôd_znaka);}
    if(!unos_COUNT)naziv_tabela(140,210,"Click + New terminal to start",0xede9df,0x302018);
    for(int 순번=0;순번<unos_COUNT;순번++)실행틀(redoslijed_VALUE[순번]);화면다시그림(Fokus);Terminal_unos=&Windows_spisak[출력결과];
}
static void 영역그리기(int 가로,int Vertikalno_položaj,int 폭,int dužina_VALUE){
    if(!desktop_Prikaz||!보드그림범위(&가로,&Vertikalno_položaj,&폭,&dužina_VALUE))return;
    for(int Linija=Vertikalno_položaj;Linija<Vertikalno_položaj+dužina_VALUE;Linija+=32){
        int 띠높이=Vertikalno_položaj+dužina_VALUE-Linija;if(띠높이>32)띠높이=32;
        if(ploča_START_ucrtavanje(가로,Linija,폭,띠높이)){장면그리기();ploča_Kraj_ucrtavanje();}
    }
}
static void 다시그리기(void){영역그리기(0,0,보드화면너비(),보드화면높이());}
/* 서로 겹치지 않는 새 prozor 영역과 이전 자리의 네 띠를 복구한다. */
static void 창자리그리기(int 가로,int Vertikalno_položaj,int 폭,int dužina_VALUE,Terminal_d413d4bc *prozor){
    int 왼쪽=가로>(int)prozor->koordinata_x?가로:(int)prozor->koordinata_x;
    int 위쪽=Vertikalno_položaj>(int)prozor->Y_koordinata?Vertikalno_položaj:(int)prozor->Y_koordinata;
    int RIGHT=가로+폭<(int)(prozor->koordinata_x+prozor->너비)?가로+폭:(int)(prozor->koordinata_x+prozor->너비);
    int 아래쪽=Vertikalno_položaj+dužina_VALUE<(int)(prozor->Y_koordinata+prozor->높이)?Vertikalno_položaj+dužina_VALUE:(int)(prozor->Y_koordinata+prozor->높이);
    영역그리기(prozor->koordinata_x,prozor->Y_koordinata,prozor->너비,prozor->높이);
    if(왼쪽>=RIGHT||위쪽>=아래쪽){영역그리기(가로,Vertikalno_položaj,폭,dužina_VALUE);return;}
    영역그리기(가로,Vertikalno_položaj,폭,위쪽-Vertikalno_položaj);
    영역그리기(가로,아래쪽,폭,Vertikalno_položaj+dužina_VALUE-아래쪽);
    영역그리기(가로,위쪽,왼쪽-가로,아래쪽-위쪽);
    영역그리기(RIGHT,위쪽,가로+폭-RIGHT,아래쪽-위쪽);
}
static void 초점알리기(void){odjel_za_informacijske_tehnologije_na_čekanju=(odjel_za_informacijske_tehnologije_na_čekanju&~15u)|(unsigned)(Fokus+1)|0x10000;}
void 터미널입력방식(unsigned 한글여부){
    한글입력=한글여부!=0;
    /* Update title bars only: a mode switch must not erase an EL0 drawing. */
    if(Fokus>=0){
        Terminal_d413d4bc *prozor_unos=&Windows_spisak[Fokus];
        naziv_tabela(prozor_unos->koordinata_x+240,prozor_unos->Y_koordinata+7,prozor_unos->너비>=500?(한글입력?"[BS] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[BS]":"[EN]"),0xffffff,0x905020);
    }
}
static void 앞으로올리기(int identifikator_VALUE){if(identifikator_VALUE<0||identifikator_VALUE>=4||!Windows_spisak[identifikator_VALUE].살아있음)return;int trenutno_položaj=0;while(trenutno_položaj<unos_COUNT&&redoslijed_VALUE[trenutno_položaj]!=identifikator_VALUE)trenutno_položaj++;for(;trenutno_položaj+1<unos_COUNT;trenutno_položaj++)redoslijed_VALUE[trenutno_položaj]=redoslijed_VALUE[trenutno_položaj+1];redoslijed_VALUE[unos_COUNT-1]=identifikator_VALUE;Fokus=identifikator_VALUE;초점알리기();다시그리기();}
static void 빈칸채우기(unsigned ROW_položaj){for(unsigned kôd_znaka=0;kôd_znaka<최대열수;kôd_znaka++){Terminal_unos->글자칸들[ROW_položaj%Historija_redak_COUNT][kôd_znaka]=0;Terminal_unos->모양들[ROW_položaj%Historija_redak_COUNT][kôd_znaka]=Terminal_unos->전경색|(Terminal_unos->배경색<<4);}}
static void obrisati_TOC(void){Terminal_unos->ROW_položaj=Terminal_unos->COLUMN_položaj=Terminal_unos->맨위=Terminal_unos->klizati=0;for(unsigned 반환값=0;반환값<Historija_redak_COUNT;반환값++)빈칸채우기(반환값);if(보이는지())Sadržaj_VALUE();}
static int Create_unos(void){
    if(!보드화면기억공간())return -19;int identifikator_VALUE=0;while(identifikator_VALUE<4&&Windows_spisak[identifikator_VALUE].살아있음)identifikator_VALUE++;if(identifikator_VALUE==4)return -28;
    desktop_Prikaz=1;Terminal_unos=&Windows_spisak[identifikator_VALUE];memset(Terminal_unos,0,sizeof(*Terminal_unos));Terminal_unos->살아있음=1;Terminal_unos->너비=568;Terminal_unos->높이=360;Terminal_unos->Kolone=68;Terminal_unos->ROW_COUNT=19;Terminal_unos->koordinata_x=12+identifikator_VALUE*16;Terminal_unos->Y_koordinata=48+identifikator_VALUE*18;Terminal_unos->전경색=7;Terminal_unos->가리개보임=1;
    for(unsigned 반환값=0;반환값<Historija_redak_COUNT;반환값++)빈칸채우기(반환값);redoslijed_VALUE[unos_COUNT++]=identifikator_VALUE;Fokus=identifikator_VALUE;odjel_za_informacijske_tehnologije_na_čekanju|=1u<<(4+identifikator_VALUE);초점알리기();다시그리기();return identifikator_VALUE+1;
}
static void zatvoriti_prozor(int identifikator_VALUE){
    if(identifikator_VALUE<0||identifikator_VALUE>=4||!Windows_spisak[identifikator_VALUE].살아있음)return;Windows_spisak[identifikator_VALUE].살아있음=0;odjel_za_informacijske_tehnologije_na_čekanju|=1u<<(8+identifikator_VALUE);
    int trenutno_položaj=0;while(trenutno_položaj<unos_COUNT&&redoslijed_VALUE[trenutno_položaj]!=identifikator_VALUE)trenutno_položaj++;for(;trenutno_položaj+1<unos_COUNT;trenutno_položaj++)redoslijed_VALUE[trenutno_položaj]=redoslijed_VALUE[trenutno_položaj+1];unos_COUNT--;
    if(Fokus==identifikator_VALUE)Fokus=unos_COUNT?redoslijed_VALUE[unos_COUNT-1]:-1;초점알리기();다시그리기();
}
static void 줄바꿈(void){Terminal_unos->COLUMN_položaj=0;Terminal_unos->ROW_položaj++;if(Terminal_unos->ROW_položaj>=Terminal_unos->맨위+Terminal_unos->ROW_COUNT){Terminal_unos->맨위++;빈칸채우기(Terminal_unos->ROW_položaj);if(보이는지())Sadržaj_VALUE();}}
static void kôd_znaka_451f2815(unsigned kôd_znaka){
    if(kôd_znaka==13){Terminal_unos->COLUMN_položaj=0;return;}if(kôd_znaka==10){줄바꿈();return;}if(kôd_znaka==8){if(Terminal_unos->COLUMN_položaj)Terminal_unos->COLUMN_položaj--;return;}
    if(kôd_znaka==9){unsigned stavka_COUNT=8-Terminal_unos->COLUMN_položaj%8;while(stavka_COUNT--)kôd_znaka_451f2815(' ');return;}if(kôd_znaka<32||kôd_znaka==127)return;
    unsigned 너비값=넓은글자(kôd_znaka);if(Terminal_unos->COLUMN_položaj+너비값>Terminal_unos->Kolone)줄바꿈();
    if(Terminal_unos->글자칸들[Terminal_unos->ROW_položaj%Historija_redak_COUNT][Terminal_unos->COLUMN_položaj]==0xffffffffu&&Terminal_unos->COLUMN_položaj){Terminal_unos->글자칸들[Terminal_unos->ROW_položaj%Historija_redak_COUNT][Terminal_unos->COLUMN_položaj-1]=' ';그리기(Terminal_unos->ROW_položaj,Terminal_unos->COLUMN_položaj-1);}
    if(넓은글자(Terminal_unos->글자칸들[Terminal_unos->ROW_položaj%Historija_redak_COUNT][Terminal_unos->COLUMN_položaj])==2&&Terminal_unos->COLUMN_položaj+1<Terminal_unos->Kolone){Terminal_unos->글자칸들[Terminal_unos->ROW_položaj%Historija_redak_COUNT][Terminal_unos->COLUMN_položaj+1]=' ';그리기(Terminal_unos->ROW_položaj,Terminal_unos->COLUMN_položaj+1);}
    Terminal_unos->글자칸들[Terminal_unos->ROW_položaj%Historija_redak_COUNT][Terminal_unos->COLUMN_položaj]=kôd_znaka;Terminal_unos->모양들[Terminal_unos->ROW_položaj%Historija_redak_COUNT][Terminal_unos->COLUMN_položaj]=Terminal_unos->전경색|(Terminal_unos->배경색<<4);
    if(너비값==2)Terminal_unos->글자칸들[Terminal_unos->ROW_položaj%Historija_redak_COUNT][Terminal_unos->COLUMN_položaj+1]=0xffffffffu;
    그리기(Terminal_unos->ROW_položaj,Terminal_unos->COLUMN_položaj);Terminal_unos->COLUMN_položaj+=너비값;
}
static void hvatište_kontrola_SEQUENCE(unsigned kôd_znaka){
    unsigned stavka_COUNT=Terminal_unos->parametar_VALUE[0]?Terminal_unos->parametar_VALUE[0]:1;
    if(kôd_znaka=='m')for(unsigned 순번=0;순번<=Terminal_unos->parametar_INDEX;순번++){unsigned podaci_položaj=Terminal_unos->parametar_VALUE[순번];if(!podaci_položaj){Terminal_unos->전경색=7;Terminal_unos->배경색=0;}if(podaci_položaj==1&&Terminal_unos->전경색<8)Terminal_unos->전경색+=8;if(podaci_položaj==7){unsigned 유지=Terminal_unos->전경색;Terminal_unos->전경색=Terminal_unos->배경색;Terminal_unos->배경색=유지;}if(podaci_položaj>=30&&podaci_položaj<=37)Terminal_unos->전경색=podaci_položaj-30;if(podaci_položaj>=90&&podaci_položaj<=97)Terminal_unos->전경색=podaci_položaj-90+8;if(podaci_položaj>=40&&podaci_položaj<=47)Terminal_unos->배경색=podaci_položaj-40;if(podaci_položaj>=100&&podaci_položaj<=107)Terminal_unos->배경색=podaci_položaj-100+8;if(podaci_položaj==39)Terminal_unos->전경색=7;if(podaci_položaj==49)Terminal_unos->배경색=0;}
    if(kôd_znaka=='J'&&(Terminal_unos->parametar_VALUE[0]==2||Terminal_unos->parametar_VALUE[0]==3))obrisati_TOC();
    if(kôd_znaka=='K'){unsigned 출발위치=Terminal_unos->parametar_VALUE[0]==2?0:Terminal_unos->COLUMN_položaj,도착위치=Terminal_unos->parametar_VALUE[0]==1?Terminal_unos->COLUMN_položaj+1:Terminal_unos->Kolone;if(Terminal_unos->parametar_VALUE[0]==1)출발위치=0;for(unsigned 순번=출발위치;순번<도착위치&&순번<Terminal_unos->Kolone;순번++){
        unsigned ROW_VALUE=Terminal_unos->ROW_položaj%Historija_redak_COUNT,znak_VALUE=Terminal_unos->글자칸들[ROW_VALUE][순번],oblik_VALUE=Terminal_unos->전경색|(Terminal_unos->배경색<<4);
        /* 넓은 vi 화면에서도 이미 빈 칸의 font_VALUE 화소를 되풀이해 칠하지 않는다. */
        int 바뀜=(znak_VALUE!=0&&znak_VALUE!=' ')||Terminal_unos->모양들[ROW_VALUE][순번]!=oblik_VALUE;
        Terminal_unos->글자칸들[ROW_VALUE][순번]=' ';Terminal_unos->모양들[ROW_VALUE][순번]=oblik_VALUE;
        if(바뀜)그리기(Terminal_unos->ROW_položaj,순번);
    }}
    if(kôd_znaka=='D')Terminal_unos->COLUMN_položaj=stavka_COUNT>Terminal_unos->COLUMN_položaj?0:Terminal_unos->COLUMN_položaj-stavka_COUNT;if(kôd_znaka=='C')Terminal_unos->COLUMN_položaj=Terminal_unos->COLUMN_položaj+stavka_COUNT>=Terminal_unos->Kolone?Terminal_unos->Kolone-1:Terminal_unos->COLUMN_položaj+stavka_COUNT;
    if(kôd_znaka=='G')Terminal_unos->COLUMN_položaj=stavka_COUNT>Terminal_unos->Kolone?Terminal_unos->Kolone-1:stavka_COUNT-1;if(kôd_znaka=='A')Terminal_unos->ROW_položaj=stavka_COUNT>Terminal_unos->ROW_položaj-Terminal_unos->맨위?Terminal_unos->맨위:Terminal_unos->ROW_položaj-stavka_COUNT;
    if(kôd_znaka=='B')Terminal_unos->ROW_položaj=Terminal_unos->ROW_položaj+stavka_COUNT>=Terminal_unos->맨위+Terminal_unos->ROW_COUNT?Terminal_unos->맨위+Terminal_unos->ROW_COUNT-1:Terminal_unos->ROW_položaj+stavka_COUNT;
    if(kôd_znaka=='H'||kôd_znaka=='f'){Terminal_unos->ROW_položaj=Terminal_unos->맨위+(stavka_COUNT>Terminal_unos->ROW_COUNT?Terminal_unos->ROW_COUNT:stavka_COUNT)-1;unsigned koordinata_x=Terminal_unos->parametar_VALUE[1]?Terminal_unos->parametar_VALUE[1]:1;Terminal_unos->COLUMN_položaj=(koordinata_x>Terminal_unos->Kolone?Terminal_unos->Kolone:koordinata_x)-1;}
    if(kôd_znaka=='s'){Terminal_unos->저장행=Terminal_unos->ROW_položaj;Terminal_unos->저장열=Terminal_unos->COLUMN_položaj;}if(kôd_znaka=='u'){Terminal_unos->ROW_položaj=Terminal_unos->저장행;Terminal_unos->COLUMN_položaj=Terminal_unos->저장열<Terminal_unos->Kolone?Terminal_unos->저장열:Terminal_unos->Kolone-1;}
    if((kôd_znaka=='h'||kôd_znaka=='l')&&Terminal_unos->parametar_VALUE[0]==25)Terminal_unos->가리개보임=kôd_znaka=='h';
}
void Terminal_bajt(unsigned SECOND_VALUE){
    Terminal_unos=&Windows_spisak[출력결과];if(!Terminal_unos->살아있음)return;simbol_VALUE_be8150db(0);if(Terminal_unos->klizati){Terminal_unos->klizati=0;if(보이는지())Sadržaj_VALUE();}
    if(Terminal_unos->탈출상태==1){Terminal_unos->탈출상태=SECOND_VALUE=='['?2:0;Terminal_unos->parametar_INDEX=0;for(unsigned 순번=0;순번<4;순번++)Terminal_unos->parametar_VALUE[순번]=0;}
    else if(Terminal_unos->탈출상태==2){if(SECOND_VALUE=='?'){}else if(SECOND_VALUE>='0'&&SECOND_VALUE<='9'){if(Terminal_unos->parametar_VALUE[Terminal_unos->parametar_INDEX]<10000)Terminal_unos->parametar_VALUE[Terminal_unos->parametar_INDEX]=Terminal_unos->parametar_VALUE[Terminal_unos->parametar_INDEX]*10+SECOND_VALUE-'0';}else if(SECOND_VALUE==';'&&Terminal_unos->parametar_INDEX<3)Terminal_unos->parametar_INDEX++;else{hvatište_kontrola_SEQUENCE(SECOND_VALUE);Terminal_unos->탈출상태=0;}}
    else if(SECOND_VALUE==27){Terminal_unos->긴부호없는값=0;Terminal_unos->탈출상태=1;}else{
        if(Terminal_unos->긴부호없는값&&(SECOND_VALUE&0xc0)!=0x80){Terminal_unos->긴부호없는값=0;kôd_znaka_451f2815(0xfffd);}
        if(Terminal_unos->긴부호없는값){Terminal_unos->부호없는결과=Terminal_unos->부호없는결과*64+(SECOND_VALUE&63);if(--Terminal_unos->긴부호없는값==0)kôd_znaka_451f2815(Terminal_unos->부호없는결과<Terminal_unos->SMALL_VALUE||Terminal_unos->부호없는결과>0x10ffff||(Terminal_unos->부호없는결과>=0xd800&&Terminal_unos->부호없는결과<=0xdfff)?0xfffd:Terminal_unos->부호없는결과);}
        else if(SECOND_VALUE<128)kôd_znaka_451f2815(SECOND_VALUE);else if(SECOND_VALUE>=0xc2&&SECOND_VALUE<=0xf4){Terminal_unos->긴부호없는값=SECOND_VALUE<0xe0?1:SECOND_VALUE<0xf0?2:3;Terminal_unos->부호없는결과=SECOND_VALUE&((1u<<(6-Terminal_unos->긴부호없는값))-1);Terminal_unos->SMALL_VALUE=Terminal_unos->긴부호없는값==1?128:Terminal_unos->긴부호없는값==2?2048:65536;}else kôd_znaka_451f2815(0xfffd);
    }simbol_VALUE_be8150db(1);
}
int Terminal_na_čekanju(void){return odjel_za_informacijske_tehnologije_na_čekanju!=0;}
/* 모서리 INDEX: 1 좌상, 2 우상, 3 좌하, 4 우하. */
static int promijeniti_veličinu_prevući=-1,잡은모서리,잡은가로,잡은세로,처음가로,처음세로,처음너비,처음높이;
static int 가리킨창(int 가로,int Vertikalno_položaj) {
    for(int SEQUENCE_VALUE=unos_COUNT-1;SEQUENCE_VALUE>=0;SEQUENCE_VALUE--){
        int identifikator_VALUE=redoslijed_VALUE[SEQUENCE_VALUE];Terminal_d413d4bc *prozor=&Windows_spisak[identifikator_VALUE];
        if(가로>=(int)prozor->koordinata_x&&Vertikalno_položaj>=(int)prozor->Y_koordinata&&
           가로<(int)(prozor->koordinata_x+prozor->너비)&&Vertikalno_položaj<(int)(prozor->Y_koordinata+prozor->높이))return identifikator_VALUE;
    }return -1;
}
static int 모서리찾기(int identifikator_VALUE,int 가로,int Vertikalno_položaj) {
    if(identifikator_VALUE<0)return 0;Terminal_d413d4bc *prozor=&Windows_spisak[identifikator_VALUE];
    int 왼쪽=가로<(int)prozor->koordinata_x+8,RIGHT=가로>=(int)(prozor->koordinata_x+prozor->너비)-8;
    int 위쪽=Vertikalno_položaj<(int)prozor->Y_koordinata+8,아래쪽=Vertikalno_položaj>=(int)(prozor->Y_koordinata+prozor->높이)-8;
    return (왼쪽||RIGHT)&&(위쪽||아래쪽)?1+RIGHT+아래쪽*2:0;
}
static int razdjelnik_VALUE(int VALUE,int 최소,int 최대){return VALUE<최소?최소:VALUE>최대?최대:VALUE;}
static void pomaći_promijeniti_veličinu(int 가로,int Vertikalno_položaj) {
    Terminal_d413d4bc *prozor=&Windows_spisak[promijeniti_veličinu_prevući];int 왼쪽=처음가로,위쪽=처음세로,RIGHT=처음가로+처음너비,아래쪽=처음세로+처음높이;
    if(잡은모서리==1||잡은모서리==3)왼쪽=razdjelnik_VALUE(처음가로+가로-잡은가로,0,RIGHT-360);
    else RIGHT=razdjelnik_VALUE(처음가로+처음너비+가로-잡은가로,왼쪽+360,보드화면너비());
    if(잡은모서리<=2)위쪽=razdjelnik_VALUE(처음세로+Vertikalno_položaj-잡은세로,34,아래쪽-216);
    else 아래쪽=razdjelnik_VALUE(처음세로+처음높이+Vertikalno_položaj-잡은세로,위쪽+216,보드화면높이());
    unsigned Kolone=(RIGHT-왼쪽-24)/8,ROW_COUNT=(아래쪽-위쪽-56)/16;
    if(prozor->Kolone!=Kolone||prozor->ROW_COUNT!=ROW_COUNT){
        prozor->크기바뀜=1;prozor->Kolone=Kolone;prozor->ROW_COUNT=ROW_COUNT;
        if(prozor->COLUMN_položaj>=Kolone)prozor->COLUMN_položaj=Kolone-1;
        if(prozor->ROW_položaj>=prozor->맨위+ROW_COUNT)prozor->맨위=prozor->ROW_položaj-ROW_COUNT+1;
        unsigned 한도=prozor->맨위;if(한도>Historija_redak_COUNT-ROW_COUNT)한도=Historija_redak_COUNT-ROW_COUNT;
        if(prozor->klizati>한도)prozor->klizati=한도;
    }
    int 옛가로=prozor->koordinata_x,옛세로=prozor->Y_koordinata,옛폭=prozor->너비,옛길이=prozor->높이;
    if(옛가로==왼쪽&&옛세로==위쪽&&옛폭==RIGHT-왼쪽&&옛길이==아래쪽-위쪽)return;
    prozor->koordinata_x=왼쪽;prozor->Y_koordinata=위쪽;prozor->너비=RIGHT-왼쪽;prozor->높이=아래쪽-위쪽;
    창자리그리기(옛가로,옛세로,옛폭,옛길이,prozor);
}
void Terminal_pokazivač(unsigned Dalje_stavka,int koordinata_x,int Y_koordinata){
    unsigned 눌림=Dalje_stavka&~단추들;단추들=Dalje_stavka;
    if(!desktop_Prikaz){prevući_VALUE=-1;promijeniti_veličinu_prevući=-1;ploča_pokazivač(koordinata_x,Y_koordinata,1);return;}
    if(!(Dalje_stavka&1)){prevući_VALUE=-1;promijeniti_veličinu_prevući=-1;}
    if(promijeniti_veličinu_prevući>=0&&!Windows_spisak[promijeniti_veličinu_prevući].살아있음)promijeniti_veličinu_prevući=-1;
    if(prevući_VALUE>=0&&!Windows_spisak[prevući_VALUE].살아있음)prevući_VALUE=-1;
    if(promijeniti_veličinu_prevući>=0){
        pomaći_promijeniti_veličinu(koordinata_x,Y_koordinata);ploča_pokazivač(koordinata_x,Y_koordinata,잡은모서리==1||잡은모서리==4?2:3);return;
    }
    ploča_pokazivač(koordinata_x,Y_koordinata,1);
    if(prevući_VALUE>=0){
        Terminal_d413d4bc *prozor=&Windows_spisak[prevući_VALUE];
        int 옛가로=prozor->koordinata_x,옛세로=prozor->Y_koordinata;
        prozor->koordinata_x=razdjelnik_VALUE(koordinata_x-prevući_X,0,보드화면너비()-prozor->너비);
        prozor->Y_koordinata=razdjelnik_VALUE(Y_koordinata-prevući_Y,34,보드화면높이()-prozor->높이);
        if(옛가로!=(int)prozor->koordinata_x||옛세로!=(int)prozor->Y_koordinata)창자리그리기(옛가로,옛세로,prozor->너비,prozor->높이,prozor);
        return;
    }
    extern int 화면덮음(int,int,int);
    if(화면덮음(Fokus,koordinata_x,Y_koordinata)){화면가리킴(Fokus,눌림,koordinata_x,Y_koordinata);return;}
    int identifikator_VALUE=가리킨창(koordinata_x,Y_koordinata),모서리=모서리찾기(identifikator_VALUE,koordinata_x,Y_koordinata);
    if(모서리)ploča_pokazivač(koordinata_x,Y_koordinata,모서리==1||모서리==4?2:3);
    if(눌림&1){
        if(모서리){
            Terminal_d413d4bc *prozor=&Windows_spisak[identifikator_VALUE];promijeniti_veličinu_prevući=identifikator_VALUE;잡은모서리=모서리;잡은가로=koordinata_x;잡은세로=Y_koordinata;
            처음가로=prozor->koordinata_x;처음세로=prozor->Y_koordinata;처음너비=prozor->너비;처음높이=prozor->높이;
            if(identifikator_VALUE!=Fokus)앞으로올리기(identifikator_VALUE);return;
        }
        if(Y_koordinata<32&&koordinata_x>=6&&koordinata_x<142){Create_unos();return;}
        if(Y_koordinata<32&&koordinata_x>=154&&koordinata_x<602){앞으로올리기((koordinata_x-154)/112);return;}
        if(identifikator_VALUE>=0){
            Terminal_d413d4bc *prozor=&Windows_spisak[identifikator_VALUE];
            if(Y_koordinata<(int)prozor->Y_koordinata+30&&koordinata_x>=(int)(prozor->koordinata_x+prozor->너비)-32){zatvoriti_prozor(identifikator_VALUE);return;}
            if(identifikator_VALUE!=Fokus)앞으로올리기(identifikator_VALUE);
            if(Y_koordinata<(int)prozor->Y_koordinata+30){prevući_VALUE=identifikator_VALUE;prevući_X=koordinata_x-prozor->koordinata_x;prevući_Y=Y_koordinata-prozor->Y_koordinata;}return;
        }
    }
    if(Fokus>=0&&(눌림&(8|16))){Terminal_unos=&Windows_spisak[Fokus];if(눌림&8){unsigned 한도=Terminal_unos->맨위;if(한도>Historija_redak_COUNT-Terminal_unos->ROW_COUNT)한도=Historija_redak_COUNT-Terminal_unos->ROW_COUNT;Terminal_unos->klizati=Terminal_unos->klizati+9>한도?한도:Terminal_unos->klizati+9;}else Terminal_unos->klizati=Terminal_unos->klizati<9?0:Terminal_unos->klizati-9;다시그리기();}
}
void 터미널바로가기키(unsigned 누름값){if(누름값==1)Create_unos();if(누름값==2&&unos_COUNT)앞으로올리기(redoslijed_VALUE[0]);if(누름값==3)zatvoriti_prozor(Fokus);}
mašina_Word ploča_Terminal(mašina_Word radnja){
    if(radnja==300){if(!Windows_spisak[출력결과].살아있음)return Create_unos();desktop_Prikaz=1;다시그리기();return 0;}
    if(radnja==0){zatvoriti_prozor(Fokus);return 0;}if(radnja==1)return (uint32_t)Create_unos();if(radnja==2)return Fokus>=0;
    if(radnja==9){desktop_Prikaz=0;return 0;}if(radnja==7)return unos_COUNT;if(radnja==10)return Fokus+1;if(radnja==11)return 출력결과;
    if(radnja==13){Terminal_d413d4bc *prozor=&Windows_spisak[출력결과];return prozor->살아있음?(prozor->ROW_COUNT<<16)|prozor->Kolone:(19<<16)|68;}
    if(radnja==14){unsigned VALUE=Windows_spisak[출력결과].크기바뀜;Windows_spisak[출력결과].크기바뀜=0;return VALUE;}
    if(radnja==12){unsigned VALUE=odjel_za_informacijske_tehnologije_na_čekanju;odjel_za_informacijske_tehnologije_na_čekanju=0;return VALUE;}
    if(radnja>=20&&radnja<24)return Windows_spisak[radnja-20].살아있음;
    if(radnja>=100&&radnja<104){출력결과=radnja-100;Terminal_unos=&Windows_spisak[출력결과];return 0;}
    if(radnja>=200&&radnja<204){앞으로올리기(radnja-200);return 0;}
    if(radnja==3){다시그리기();return 0;}Terminal_unos=&Windows_spisak[출력결과];if(!Terminal_unos->살아있음)return 0;
    if(radnja==4)obrisati_TOC();if(radnja==5||radnja==6){unsigned 이전=단추들;Terminal_pokazivač(radnja==5?8:16,0,0);단추들=이전;}return 1;
}
