#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* vlastiti 네 Prozor 합성과 UTF-8 Terminal. 바뀐 영역의 Dovršeno_VALUE 그림만 표시한다. */
#include <stdint.h>
#include <stddef.h>
typedef uintptr_t stroj_Word;
extern stroj_Word pano_slikovni_element(stroj_Word,stroj_Word,stroj_Word),보드화면기억공간(void);
extern void *memset(void *,int,size_t);
extern const unsigned char Terminal_font[];
#define 최대열수 237
#define Povijest_red_COUNT 160
typedef struct {
    uint32_t 글자칸들[Povijest_red_COUNT][최대열수]; uint8_t 모양들[Povijest_red_COUNT][최대열수];
    unsigned 너비,높이,COLUMNS,ROW_COUNT,크기바뀜;
    unsigned 살아있음,koordinata_x,세로좌표,ROW_položaj,COLUMN_položaj,맨위,밀어올리기,전경색,배경색,탈출상태,parametar_VALUE[4],parametar_INDEX,저장행,저장열;
    unsigned 부호없는결과,긴부호없는값,SMALL_VALUE,대체화면,가리개보임;
} Terminal_d413d4bc;
static Terminal_d413d4bc Windows_Popis[4];
static int Fokus=-1,출력결과,narudžba_VALUE[4],unos_COUNT,vući_VALUE=-1,vući_X,vući_Y;
static unsigned odjel_informacijske_tehnologije_na_čekanju,단추들,stolni_Prikaz,한글입력;
static const uint32_t 색상들[16]={0x201a15,0x6060df,0x9dcc86,0x80cfea,0xefaf72,0xca96c9,0xceda76,0xede9df,0x858078,0x8888ff,0xb9eba7,0xa5eaff,0xffcc99,0xf0bef1,0xf0f0a0,0xffffff};
extern int 화면보임(int),화면가리킴(int,unsigned,int,int);
extern void 화면다시그림(int);
static Terminal_d413d4bc *Terminal_unos;
static unsigned široki_znak(unsigned kodna_točka){return kodna_točka>=256?2:1;}
static void 사각영역(unsigned koordinata_x,unsigned 세로좌표,unsigned 너비값,unsigned 높이값,unsigned 색상){
    pano_pravokutnik_ispuna(koordinata_x,세로좌표,너비값,높이값,색상);
}
void Terminal_glif(unsigned koordinata_x,unsigned 세로좌표,unsigned kodna_točka,unsigned 전경색,unsigned 배경색){
    unsigned 너비=široki_znak(kodna_točka)*8;if(kodna_točka==0xffffffffu)return;
    int 왼쪽=koordinata_x,위쪽=세로좌표,폭=너비,길이=16;
    if(!보드그림범위(&왼쪽,&위쪽,&폭,&길이))return;
    if(kodna_točka==' '){pano_pravokutnik_ispuna(왼쪽,위쪽,폭,길이,배경색);return;}
    unsigned LOOKUP_INDEX=kodna_točka<65536?kodna_točka:kodna_točka>=0x1f600&&kodna_točka<0x1f650?65536+kodna_točka-0x1f600:0xfffd;
    const unsigned char *font_VALUE=Terminal_font+LOOKUP_INDEX*32;
    for(int red=위쪽;red<위쪽+길이;red++){unsigned Pozadinski_pametni_servis_za_transfer_Popis=font_VALUE[(red-세로좌표)*2]*256+font_VALUE[(red-세로좌표)*2+1];for(int 칸=왼쪽;칸<왼쪽+폭;칸++)pano_slikovni_element(칸,red,(Pozadinski_pametni_servis_za_transfer_Popis&(0x8000>>(칸-koordinata_x)))?전경색:배경색);}
}
static void naziv_tablica(unsigned koordinata_x,unsigned 세로좌표,const char *niz_podaci,unsigned 전경색,unsigned 배경색){while(*niz_podaci){unsigned kodna_točka=(unsigned char)*niz_podaci++, 남은수=0;if(kodna_točka>=0xc0){남은수=kodna_točka<0xe0?1:kodna_točka<0xf0?2:3;kodna_točka&=(1u<<(6-남은수))-1;while(남은수--&&*niz_podaci)kodna_točka=(kodna_točka<<6)|((unsigned char)*niz_podaci++&63);}Terminal_glif(koordinata_x,세로좌표,kodna_točka,전경색,배경색);koordinata_x+=široki_znak(kodna_točka)*8;}}
static unsigned 첫항목(void){return Terminal_unos->맨위;}
static int 보이는지(void){return Terminal_unos->살아있음&&Fokus>=0&&Terminal_unos==&Windows_Popis[Fokus]&&!화면보임(Fokus);}
static void 그리기(unsigned ROW_položaj,unsigned COLUMN_položaj){
    if(!보이는지()||ROW_položaj<첫항목()-Terminal_unos->밀어올리기||ROW_položaj>=첫항목()-Terminal_unos->밀어올리기+Terminal_unos->ROW_COUNT||COLUMN_položaj>=Terminal_unos->COLUMNS)return;
    unsigned kodna_točka=Terminal_unos->글자칸들[ROW_položaj%Povijest_red_COUNT][COLUMN_položaj],niz_podaci=Terminal_unos->모양들[ROW_položaj%Povijest_red_COUNT][COLUMN_položaj];
    if(široki_znak(kodna_točka)==2&&COLUMN_položaj+1>=Terminal_unos->COLUMNS)kodna_točka=' ';
    Terminal_glif(Terminal_unos->koordinata_x+12+COLUMN_položaj*8,Terminal_unos->세로좌표+36+(ROW_položaj-첫항목()+Terminal_unos->밀어올리기)*16,kodna_točka?kodna_točka:' ',색상들[niz_podaci&15],색상들[niz_podaci>>4]);
}
static void karet_VALUE(int emisija_prozor){if(!보이는지()||Terminal_unos->밀어올리기||Terminal_unos->COLUMN_položaj>=Terminal_unos->COLUMNS||Terminal_unos->ROW_položaj<Terminal_unos->맨위||Terminal_unos->ROW_položaj>=Terminal_unos->맨위+Terminal_unos->ROW_COUNT)return;
    if(!emisija_prozor||!Terminal_unos->가리개보임)그리기(Terminal_unos->ROW_položaj,Terminal_unos->COLUMN_položaj);else 사각영역(Terminal_unos->koordinata_x+12+Terminal_unos->COLUMN_položaj*8,Terminal_unos->세로좌표+36+(Terminal_unos->ROW_položaj-Terminal_unos->맨위)*16+14,8,2,색상들[Terminal_unos->전경색]);}
static void Sadržaj_VALUE(void){
    사각영역(Terminal_unos->koordinata_x+12,Terminal_unos->세로좌표+36,Terminal_unos->COLUMNS*8,Terminal_unos->ROW_COUNT*16,색상들[0]);
    int 가로=Terminal_unos->koordinata_x+12,Okomito_položaj=Terminal_unos->세로좌표+36,폭=Terminal_unos->COLUMNS*8,길이=Terminal_unos->ROW_COUNT*16;
    if(보드그림범위(&가로,&Okomito_položaj,&폭,&길이)){
    unsigned 첫줄=(Okomito_položaj-Terminal_unos->세로좌표-36)/16,끝줄=(Okomito_položaj+길이-Terminal_unos->세로좌표-36+15)/16;
    unsigned 첫칸=(가로-Terminal_unos->koordinata_x-12)/8,끝칸=(가로+폭-Terminal_unos->koordinata_x-12+7)/8;
    if(첫칸)첫칸--; /* 잘림 경계 왼쪽에서 시작한 두 칸 글자도 그린다. */
    for(unsigned 반환값=첫줄;반환값<끝줄;반환값++)for(unsigned kodna_točka=첫칸;kodna_točka<끝칸;kodna_točka++){
        unsigned ROW_položaj=첫항목()-Terminal_unos->밀어올리기+반환값,znak_VALUE=Terminal_unos->글자칸들[ROW_položaj%Povijest_red_COUNT][kodna_točka],niz_podaci=Terminal_unos->모양들[ROW_položaj%Povijest_red_COUNT][kodna_točka];
        if(široki_znak(znak_VALUE)==2&&kodna_točka+1>=Terminal_unos->COLUMNS)znak_VALUE=' ';
        if((znak_VALUE==0||znak_VALUE==' ')&&(niz_podaci>>4)==0)continue;
        Terminal_glif(Terminal_unos->koordinata_x+12+kodna_točka*8,Terminal_unos->세로좌표+36+반환값*16,znak_VALUE?znak_VALUE:' ',색상들[niz_podaci&15],색상들[niz_podaci>>4]);
    }}
    naziv_tablica(Terminal_unos->koordinata_x+12,Terminal_unos->세로좌표+Terminal_unos->높이-18,Terminal_unos->밀어올리기?"PgDn: recent output":Terminal_unos->너비>=500?"F6: next | Corner + left drag: resize":"Corner + left drag: resize",0xece8e2,0x403127);karet_VALUE(1);
}
static void 실행틀(int identifikator_VALUE){
    Terminal_unos=&Windows_Popis[identifikator_VALUE];
    int 가로=Terminal_unos->koordinata_x,Okomito_položaj=Terminal_unos->세로좌표,폭=Terminal_unos->너비,길이=Terminal_unos->높이;
    if(!보드그림범위(&가로,&Okomito_položaj,&폭,&길이))return;
    사각영역(Terminal_unos->koordinata_x,Terminal_unos->세로좌표,Terminal_unos->너비,Terminal_unos->높이,0x403127);
    unsigned 색상=identifikator_VALUE==Fokus?0x905020:0x604438;사각영역(Terminal_unos->koordinata_x,Terminal_unos->세로좌표,Terminal_unos->너비,30,색상);
    naziv_tablica(Terminal_unos->koordinata_x+12,Terminal_unos->세로좌표+7,"JKOROS Terminal",0xffffff,색상);
    char 수치[2]={(char)('1'+identifikator_VALUE),0};naziv_tablica(Terminal_unos->koordinata_x+148,Terminal_unos->세로좌표+7,수치,0xffffff,색상);
    naziv_tablica(Terminal_unos->koordinata_x+240,Terminal_unos->세로좌표+7,Terminal_unos->너비>=500?(한글입력?"[HR] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[HR]":"[EN]"),0xffffff,색상);
    사각영역(Terminal_unos->koordinata_x+Terminal_unos->너비-32,Terminal_unos->세로좌표+4,26,22,0x5555b8);naziv_tablica(Terminal_unos->koordinata_x+Terminal_unos->너비-24,Terminal_unos->세로좌표+7,"X",0xffffff,0x5555b8);
    Sadržaj_VALUE();
}
static void Crtanje_tema(void){
    if(!stolni_Prikaz)return;사각영역(0,0,보드화면너비(),보드화면높이(),0x302018);사각영역(0,0,보드화면너비(),32,0x403127);
    사각영역(6,4,136,24,0x905020);naziv_tablica(14,8,"+ New terminal",0xffffff,0x905020);
    for(int 순번=0;순번<4;순번++)if(Windows_Popis[순번].살아있음){unsigned kodna_točka=Fokus==순번?0x905020:0x604438;사각영역(154+순번*112,4,106,24,kodna_točka);naziv_tablica(160+순번*112,8,"Terminal",0xffffff,kodna_točka);char niz_podaci[2]={(char)('1'+순번),0};naziv_tablica(232+순번*112,8,niz_podaci,0xffffff,kodna_točka);}
    if(!unos_COUNT)naziv_tablica(140,210,"Click + New terminal to start",0xede9df,0x302018);
    for(int 순번=0;순번<unos_COUNT;순번++)실행틀(narudžba_VALUE[순번]);화면다시그림(Fokus);Terminal_unos=&Windows_Popis[출력결과];
}
static void Bojanje_regije(int 가로,int Okomito_položaj,int 폭,int 길이){
    if(!stolni_Prikaz||!보드그림범위(&가로,&Okomito_položaj,&폭,&길이))return;
    for(int red=Okomito_položaj;red<Okomito_položaj+길이;red+=32){
        int 띠높이=Okomito_položaj+길이-red;if(띠높이>32)띠높이=32;
        if(pano_START_crtež(가로,red,폭,띠높이)){Crtanje_tema();pano_Završi_crtež();}
    }
}
static void 다시그리기(void){Bojanje_regije(0,0,보드화면너비(),보드화면높이());}
/* 서로 겹치지 않는 새 Prozor 영역과 이전 자리의 네 띠를 복구한다. */
static void 창자리그리기(int 가로,int Okomito_položaj,int 폭,int 길이,Terminal_d413d4bc *Prozor){
    int 왼쪽=가로>(int)Prozor->koordinata_x?가로:(int)Prozor->koordinata_x;
    int 위쪽=Okomito_položaj>(int)Prozor->세로좌표?Okomito_položaj:(int)Prozor->세로좌표;
    int RIGHT=가로+폭<(int)(Prozor->koordinata_x+Prozor->너비)?가로+폭:(int)(Prozor->koordinata_x+Prozor->너비);
    int 아래쪽=Okomito_položaj+길이<(int)(Prozor->세로좌표+Prozor->높이)?Okomito_položaj+길이:(int)(Prozor->세로좌표+Prozor->높이);
    Bojanje_regije(Prozor->koordinata_x,Prozor->세로좌표,Prozor->너비,Prozor->높이);
    if(왼쪽>=RIGHT||위쪽>=아래쪽){Bojanje_regije(가로,Okomito_položaj,폭,길이);return;}
    Bojanje_regije(가로,Okomito_položaj,폭,위쪽-Okomito_položaj);
    Bojanje_regije(가로,아래쪽,폭,Okomito_položaj+길이-아래쪽);
    Bojanje_regije(가로,위쪽,왼쪽-가로,아래쪽-위쪽);
    Bojanje_regije(RIGHT,위쪽,가로+폭-RIGHT,아래쪽-위쪽);
}
static void signal_Fokus(void){odjel_informacijske_tehnologije_na_čekanju=(odjel_informacijske_tehnologije_na_čekanju&~15u)|(unsigned)(Fokus+1)|0x10000;}
void 터미널입력방식(unsigned 한글여부){
    한글입력=한글여부!=0;
    /* Update title bars only: a mode switch must not erase an EL0 drawing. */
    if(Fokus>=0){
        Terminal_d413d4bc *prozor_unos=&Windows_Popis[Fokus];
        naziv_tablica(prozor_unos->koordinata_x+240,prozor_unos->세로좌표+7,prozor_unos->너비>=500?(한글입력?"[HR] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[HR]":"[EN]"),0xffffff,0x905020);
    }
}
static void 앞으로올리기(int identifikator_VALUE){if(identifikator_VALUE<0||identifikator_VALUE>=4||!Windows_Popis[identifikator_VALUE].살아있음)return;int redovno_položaj=0;while(redovno_položaj<unos_COUNT&&narudžba_VALUE[redovno_položaj]!=identifikator_VALUE)redovno_položaj++;for(;redovno_položaj+1<unos_COUNT;redovno_položaj++)narudžba_VALUE[redovno_položaj]=narudžba_VALUE[redovno_položaj+1];narudžba_VALUE[unos_COUNT-1]=identifikator_VALUE;Fokus=identifikator_VALUE;signal_Fokus();다시그리기();}
static void 빈칸채우기(unsigned ROW_položaj){for(unsigned kodna_točka=0;kodna_točka<최대열수;kodna_točka++){Terminal_unos->글자칸들[ROW_položaj%Povijest_red_COUNT][kodna_točka]=0;Terminal_unos->모양들[ROW_položaj%Povijest_red_COUNT][kodna_točka]=Terminal_unos->전경색|(Terminal_unos->배경색<<4);}}
static void očistiti_Sadržaj(void){Terminal_unos->ROW_položaj=Terminal_unos->COLUMN_položaj=Terminal_unos->맨위=Terminal_unos->밀어올리기=0;for(unsigned 반환값=0;반환값<Povijest_red_COUNT;반환값++)빈칸채우기(반환값);if(보이는지())Sadržaj_VALUE();}
static int Create_unos(void){
    if(!보드화면기억공간())return -19;int identifikator_VALUE=0;while(identifikator_VALUE<4&&Windows_Popis[identifikator_VALUE].살아있음)identifikator_VALUE++;if(identifikator_VALUE==4)return -28;
    stolni_Prikaz=1;Terminal_unos=&Windows_Popis[identifikator_VALUE];memset(Terminal_unos,0,sizeof(*Terminal_unos));Terminal_unos->살아있음=1;Terminal_unos->너비=568;Terminal_unos->높이=360;Terminal_unos->COLUMNS=68;Terminal_unos->ROW_COUNT=19;Terminal_unos->koordinata_x=12+identifikator_VALUE*16;Terminal_unos->세로좌표=48+identifikator_VALUE*18;Terminal_unos->전경색=7;Terminal_unos->가리개보임=1;
    for(unsigned 반환값=0;반환값<Povijest_red_COUNT;반환값++)빈칸채우기(반환값);narudžba_VALUE[unos_COUNT++]=identifikator_VALUE;Fokus=identifikator_VALUE;odjel_informacijske_tehnologije_na_čekanju|=1u<<(4+identifikator_VALUE);signal_Fokus();다시그리기();return identifikator_VALUE+1;
}
static void Zatvori_prozor(int identifikator_VALUE){
    if(identifikator_VALUE<0||identifikator_VALUE>=4||!Windows_Popis[identifikator_VALUE].살아있음)return;Windows_Popis[identifikator_VALUE].살아있음=0;odjel_informacijske_tehnologije_na_čekanju|=1u<<(8+identifikator_VALUE);
    int redovno_položaj=0;while(redovno_položaj<unos_COUNT&&narudžba_VALUE[redovno_položaj]!=identifikator_VALUE)redovno_položaj++;for(;redovno_položaj+1<unos_COUNT;redovno_položaj++)narudžba_VALUE[redovno_položaj]=narudžba_VALUE[redovno_položaj+1];unos_COUNT--;
    if(Fokus==identifikator_VALUE)Fokus=unos_COUNT?narudžba_VALUE[unos_COUNT-1]:-1;signal_Fokus();다시그리기();
}
static void 줄바꿈(void){Terminal_unos->COLUMN_položaj=0;Terminal_unos->ROW_položaj++;if(Terminal_unos->ROW_položaj>=Terminal_unos->맨위+Terminal_unos->ROW_COUNT){Terminal_unos->맨위++;빈칸채우기(Terminal_unos->ROW_položaj);if(보이는지())Sadržaj_VALUE();}}
static void točka_koda(unsigned kodna_točka){
    if(kodna_točka==13){Terminal_unos->COLUMN_položaj=0;return;}if(kodna_točka==10){줄바꿈();return;}if(kodna_točka==8){if(Terminal_unos->COLUMN_položaj)Terminal_unos->COLUMN_položaj--;return;}
    if(kodna_točka==9){unsigned artikl_COUNT=8-Terminal_unos->COLUMN_položaj%8;while(artikl_COUNT--)točka_koda(' ');return;}if(kodna_točka<32||kodna_točka==127)return;
    unsigned 너비값=široki_znak(kodna_točka);if(Terminal_unos->COLUMN_položaj+너비값>Terminal_unos->COLUMNS)줄바꿈();
    if(Terminal_unos->글자칸들[Terminal_unos->ROW_položaj%Povijest_red_COUNT][Terminal_unos->COLUMN_položaj]==0xffffffffu&&Terminal_unos->COLUMN_položaj){Terminal_unos->글자칸들[Terminal_unos->ROW_položaj%Povijest_red_COUNT][Terminal_unos->COLUMN_položaj-1]=' ';그리기(Terminal_unos->ROW_položaj,Terminal_unos->COLUMN_položaj-1);}
    if(široki_znak(Terminal_unos->글자칸들[Terminal_unos->ROW_položaj%Povijest_red_COUNT][Terminal_unos->COLUMN_položaj])==2&&Terminal_unos->COLUMN_položaj+1<Terminal_unos->COLUMNS){Terminal_unos->글자칸들[Terminal_unos->ROW_položaj%Povijest_red_COUNT][Terminal_unos->COLUMN_položaj+1]=' ';그리기(Terminal_unos->ROW_položaj,Terminal_unos->COLUMN_položaj+1);}
    Terminal_unos->글자칸들[Terminal_unos->ROW_položaj%Povijest_red_COUNT][Terminal_unos->COLUMN_položaj]=kodna_točka;Terminal_unos->모양들[Terminal_unos->ROW_položaj%Povijest_red_COUNT][Terminal_unos->COLUMN_položaj]=Terminal_unos->전경색|(Terminal_unos->배경색<<4);
    if(너비값==2)Terminal_unos->글자칸들[Terminal_unos->ROW_položaj%Povijest_red_COUNT][Terminal_unos->COLUMN_položaj+1]=0xffffffffu;
    그리기(Terminal_unos->ROW_položaj,Terminal_unos->COLUMN_položaj);Terminal_unos->COLUMN_položaj+=너비값;
}
static void ustroj_kontrola_SEQUENCE(unsigned kodna_točka){
    unsigned artikl_COUNT=Terminal_unos->parametar_VALUE[0]?Terminal_unos->parametar_VALUE[0]:1;
    if(kodna_točka=='m')for(unsigned 순번=0;순번<=Terminal_unos->parametar_INDEX;순번++){unsigned podaci_položaj=Terminal_unos->parametar_VALUE[순번];if(!podaci_položaj){Terminal_unos->전경색=7;Terminal_unos->배경색=0;}if(podaci_položaj==1&&Terminal_unos->전경색<8)Terminal_unos->전경색+=8;if(podaci_položaj==7){unsigned 유지=Terminal_unos->전경색;Terminal_unos->전경색=Terminal_unos->배경색;Terminal_unos->배경색=유지;}if(podaci_položaj>=30&&podaci_položaj<=37)Terminal_unos->전경색=podaci_položaj-30;if(podaci_položaj>=90&&podaci_položaj<=97)Terminal_unos->전경색=podaci_položaj-90+8;if(podaci_položaj>=40&&podaci_položaj<=47)Terminal_unos->배경색=podaci_položaj-40;if(podaci_položaj>=100&&podaci_položaj<=107)Terminal_unos->배경색=podaci_položaj-100+8;if(podaci_položaj==39)Terminal_unos->전경색=7;if(podaci_položaj==49)Terminal_unos->배경색=0;}
    if(kodna_točka=='J'&&(Terminal_unos->parametar_VALUE[0]==2||Terminal_unos->parametar_VALUE[0]==3))očistiti_Sadržaj();
    if(kodna_točka=='K'){unsigned 출발위치=Terminal_unos->parametar_VALUE[0]==2?0:Terminal_unos->COLUMN_položaj,도착위치=Terminal_unos->parametar_VALUE[0]==1?Terminal_unos->COLUMN_položaj+1:Terminal_unos->COLUMNS;if(Terminal_unos->parametar_VALUE[0]==1)출발위치=0;for(unsigned 순번=출발위치;순번<도착위치&&순번<Terminal_unos->COLUMNS;순번++){
        unsigned ROW_VALUE=Terminal_unos->ROW_položaj%Povijest_red_COUNT,znak_VALUE=Terminal_unos->글자칸들[ROW_VALUE][순번],oblik_VALUE_f1cd655a=Terminal_unos->전경색|(Terminal_unos->배경색<<4);
        /* 넓은 vi 화면에서도 이미 빈 칸의 font_VALUE 화소를 되풀이해 칠하지 않는다. */
        int 바뀜=(znak_VALUE!=0&&znak_VALUE!=' ')||Terminal_unos->모양들[ROW_VALUE][순번]!=oblik_VALUE_f1cd655a;
        Terminal_unos->글자칸들[ROW_VALUE][순번]=' ';Terminal_unos->모양들[ROW_VALUE][순번]=oblik_VALUE_f1cd655a;
        if(바뀜)그리기(Terminal_unos->ROW_položaj,순번);
    }}
    if(kodna_točka=='D')Terminal_unos->COLUMN_položaj=artikl_COUNT>Terminal_unos->COLUMN_položaj?0:Terminal_unos->COLUMN_položaj-artikl_COUNT;if(kodna_točka=='C')Terminal_unos->COLUMN_položaj=Terminal_unos->COLUMN_položaj+artikl_COUNT>=Terminal_unos->COLUMNS?Terminal_unos->COLUMNS-1:Terminal_unos->COLUMN_položaj+artikl_COUNT;
    if(kodna_točka=='G')Terminal_unos->COLUMN_položaj=artikl_COUNT>Terminal_unos->COLUMNS?Terminal_unos->COLUMNS-1:artikl_COUNT-1;if(kodna_točka=='A')Terminal_unos->ROW_položaj=artikl_COUNT>Terminal_unos->ROW_položaj-Terminal_unos->맨위?Terminal_unos->맨위:Terminal_unos->ROW_položaj-artikl_COUNT;
    if(kodna_točka=='B')Terminal_unos->ROW_položaj=Terminal_unos->ROW_položaj+artikl_COUNT>=Terminal_unos->맨위+Terminal_unos->ROW_COUNT?Terminal_unos->맨위+Terminal_unos->ROW_COUNT-1:Terminal_unos->ROW_položaj+artikl_COUNT;
    if(kodna_točka=='H'||kodna_točka=='f'){Terminal_unos->ROW_položaj=Terminal_unos->맨위+(artikl_COUNT>Terminal_unos->ROW_COUNT?Terminal_unos->ROW_COUNT:artikl_COUNT)-1;unsigned koordinata_x=Terminal_unos->parametar_VALUE[1]?Terminal_unos->parametar_VALUE[1]:1;Terminal_unos->COLUMN_položaj=(koordinata_x>Terminal_unos->COLUMNS?Terminal_unos->COLUMNS:koordinata_x)-1;}
    if(kodna_točka=='s'){Terminal_unos->저장행=Terminal_unos->ROW_položaj;Terminal_unos->저장열=Terminal_unos->COLUMN_položaj;}if(kodna_točka=='u'){Terminal_unos->ROW_položaj=Terminal_unos->저장행;Terminal_unos->COLUMN_položaj=Terminal_unos->저장열<Terminal_unos->COLUMNS?Terminal_unos->저장열:Terminal_unos->COLUMNS-1;}
    if((kodna_točka=='h'||kodna_točka=='l')&&Terminal_unos->parametar_VALUE[0]==25)Terminal_unos->가리개보임=kodna_točka=='h';
}
void Terminal_bajt(unsigned SECOND_VALUE){
    Terminal_unos=&Windows_Popis[출력결과];if(!Terminal_unos->살아있음)return;karet_VALUE(0);if(Terminal_unos->밀어올리기){Terminal_unos->밀어올리기=0;if(보이는지())Sadržaj_VALUE();}
    if(Terminal_unos->탈출상태==1){Terminal_unos->탈출상태=SECOND_VALUE=='['?2:0;Terminal_unos->parametar_INDEX=0;for(unsigned 순번=0;순번<4;순번++)Terminal_unos->parametar_VALUE[순번]=0;}
    else if(Terminal_unos->탈출상태==2){if(SECOND_VALUE=='?'){}else if(SECOND_VALUE>='0'&&SECOND_VALUE<='9'){if(Terminal_unos->parametar_VALUE[Terminal_unos->parametar_INDEX]<10000)Terminal_unos->parametar_VALUE[Terminal_unos->parametar_INDEX]=Terminal_unos->parametar_VALUE[Terminal_unos->parametar_INDEX]*10+SECOND_VALUE-'0';}else if(SECOND_VALUE==';'&&Terminal_unos->parametar_INDEX<3)Terminal_unos->parametar_INDEX++;else{ustroj_kontrola_SEQUENCE(SECOND_VALUE);Terminal_unos->탈출상태=0;}}
    else if(SECOND_VALUE==27){Terminal_unos->긴부호없는값=0;Terminal_unos->탈출상태=1;}else{
        if(Terminal_unos->긴부호없는값&&(SECOND_VALUE&0xc0)!=0x80){Terminal_unos->긴부호없는값=0;točka_koda(0xfffd);}
        if(Terminal_unos->긴부호없는값){Terminal_unos->부호없는결과=Terminal_unos->부호없는결과*64+(SECOND_VALUE&63);if(--Terminal_unos->긴부호없는값==0)točka_koda(Terminal_unos->부호없는결과<Terminal_unos->SMALL_VALUE||Terminal_unos->부호없는결과>0x10ffff||(Terminal_unos->부호없는결과>=0xd800&&Terminal_unos->부호없는결과<=0xdfff)?0xfffd:Terminal_unos->부호없는결과);}
        else if(SECOND_VALUE<128)točka_koda(SECOND_VALUE);else if(SECOND_VALUE>=0xc2&&SECOND_VALUE<=0xf4){Terminal_unos->긴부호없는값=SECOND_VALUE<0xe0?1:SECOND_VALUE<0xf0?2:3;Terminal_unos->부호없는결과=SECOND_VALUE&((1u<<(6-Terminal_unos->긴부호없는값))-1);Terminal_unos->SMALL_VALUE=Terminal_unos->긴부호없는값==1?128:Terminal_unos->긴부호없는값==2?2048:65536;}else točka_koda(0xfffd);
    }karet_VALUE(1);
}
int Terminal_na_čekanju(void){return odjel_informacijske_tehnologije_na_čekanju!=0;}
/* 모서리 INDEX: 1 좌상, 2 우상, 3 좌하, 4 우하. */
static int promijeniti_veličinu_vući=-1,잡은모서리,잡은가로,잡은세로,처음가로,처음세로,처음너비,처음높이;
static int 가리킨창(int 가로,int Okomito_položaj) {
    for(int SEQUENCE_VALUE=unos_COUNT-1;SEQUENCE_VALUE>=0;SEQUENCE_VALUE--){
        int identifikator_VALUE=narudžba_VALUE[SEQUENCE_VALUE];Terminal_d413d4bc *Prozor=&Windows_Popis[identifikator_VALUE];
        if(가로>=(int)Prozor->koordinata_x&&Okomito_položaj>=(int)Prozor->세로좌표&&
           가로<(int)(Prozor->koordinata_x+Prozor->너비)&&Okomito_položaj<(int)(Prozor->세로좌표+Prozor->높이))return identifikator_VALUE;
    }return -1;
}
static int 모서리찾기(int identifikator_VALUE,int 가로,int Okomito_položaj) {
    if(identifikator_VALUE<0)return 0;Terminal_d413d4bc *Prozor=&Windows_Popis[identifikator_VALUE];
    int 왼쪽=가로<(int)Prozor->koordinata_x+8,RIGHT=가로>=(int)(Prozor->koordinata_x+Prozor->너비)-8;
    int 위쪽=Okomito_položaj<(int)Prozor->세로좌표+8,아래쪽=Okomito_položaj>=(int)(Prozor->세로좌표+Prozor->높이)-8;
    return (왼쪽||RIGHT)&&(위쪽||아래쪽)?1+RIGHT+아래쪽*2:0;
}
static int razdjelnik_VALUE(int VALUE,int 최소,int 최대){return VALUE<최소?최소:VALUE>최대?최대:VALUE;}
static void pomicati_se_promijeniti_veličinu(int 가로,int Okomito_položaj) {
    Terminal_d413d4bc *Prozor=&Windows_Popis[promijeniti_veličinu_vući];int 왼쪽=처음가로,위쪽=처음세로,RIGHT=처음가로+처음너비,아래쪽=처음세로+처음높이;
    if(잡은모서리==1||잡은모서리==3)왼쪽=razdjelnik_VALUE(처음가로+가로-잡은가로,0,RIGHT-360);
    else RIGHT=razdjelnik_VALUE(처음가로+처음너비+가로-잡은가로,왼쪽+360,보드화면너비());
    if(잡은모서리<=2)위쪽=razdjelnik_VALUE(처음세로+Okomito_položaj-잡은세로,34,아래쪽-216);
    else 아래쪽=razdjelnik_VALUE(처음세로+처음높이+Okomito_položaj-잡은세로,위쪽+216,보드화면높이());
    unsigned COLUMNS=(RIGHT-왼쪽-24)/8,ROW_COUNT=(아래쪽-위쪽-56)/16;
    if(Prozor->COLUMNS!=COLUMNS||Prozor->ROW_COUNT!=ROW_COUNT){
        Prozor->크기바뀜=1;Prozor->COLUMNS=COLUMNS;Prozor->ROW_COUNT=ROW_COUNT;
        if(Prozor->COLUMN_položaj>=COLUMNS)Prozor->COLUMN_položaj=COLUMNS-1;
        if(Prozor->ROW_položaj>=Prozor->맨위+ROW_COUNT)Prozor->맨위=Prozor->ROW_položaj-ROW_COUNT+1;
        unsigned 한도=Prozor->맨위;if(한도>Povijest_red_COUNT-ROW_COUNT)한도=Povijest_red_COUNT-ROW_COUNT;
        if(Prozor->밀어올리기>한도)Prozor->밀어올리기=한도;
    }
    int 옛가로=Prozor->koordinata_x,옛세로=Prozor->세로좌표,옛폭=Prozor->너비,옛길이=Prozor->높이;
    if(옛가로==왼쪽&&옛세로==위쪽&&옛폭==RIGHT-왼쪽&&옛길이==아래쪽-위쪽)return;
    Prozor->koordinata_x=왼쪽;Prozor->세로좌표=위쪽;Prozor->너비=RIGHT-왼쪽;Prozor->높이=아래쪽-위쪽;
    창자리그리기(옛가로,옛세로,옛폭,옛길이,Prozor);
}
void Terminal_pokazivač(unsigned Dalje_artikl,int koordinata_x,int 세로좌표){
    unsigned 눌림=Dalje_artikl&~단추들;단추들=Dalje_artikl;
    if(!stolni_Prikaz){vući_VALUE=-1;promijeniti_veličinu_vući=-1;pano_pokazivač(koordinata_x,세로좌표,1);return;}
    if(!(Dalje_artikl&1)){vući_VALUE=-1;promijeniti_veličinu_vući=-1;}
    if(promijeniti_veličinu_vući>=0&&!Windows_Popis[promijeniti_veličinu_vući].살아있음)promijeniti_veličinu_vući=-1;
    if(vući_VALUE>=0&&!Windows_Popis[vući_VALUE].살아있음)vući_VALUE=-1;
    if(promijeniti_veličinu_vući>=0){
        pomicati_se_promijeniti_veličinu(koordinata_x,세로좌표);pano_pokazivač(koordinata_x,세로좌표,잡은모서리==1||잡은모서리==4?2:3);return;
    }
    pano_pokazivač(koordinata_x,세로좌표,1);
    if(vući_VALUE>=0){
        Terminal_d413d4bc *Prozor=&Windows_Popis[vući_VALUE];
        int 옛가로=Prozor->koordinata_x,옛세로=Prozor->세로좌표;
        Prozor->koordinata_x=razdjelnik_VALUE(koordinata_x-vući_X,0,보드화면너비()-Prozor->너비);
        Prozor->세로좌표=razdjelnik_VALUE(세로좌표-vući_Y,34,보드화면높이()-Prozor->높이);
        if(옛가로!=(int)Prozor->koordinata_x||옛세로!=(int)Prozor->세로좌표)창자리그리기(옛가로,옛세로,Prozor->너비,Prozor->높이,Prozor);
        return;
    }
    extern int 화면덮음(int,int,int);
    if(화면덮음(Fokus,koordinata_x,세로좌표)){화면가리킴(Fokus,눌림,koordinata_x,세로좌표);return;}
    int identifikator_VALUE=가리킨창(koordinata_x,세로좌표),모서리=모서리찾기(identifikator_VALUE,koordinata_x,세로좌표);
    if(모서리)pano_pokazivač(koordinata_x,세로좌표,모서리==1||모서리==4?2:3);
    if(눌림&1){
        if(모서리){
            Terminal_d413d4bc *Prozor=&Windows_Popis[identifikator_VALUE];promijeniti_veličinu_vući=identifikator_VALUE;잡은모서리=모서리;잡은가로=koordinata_x;잡은세로=세로좌표;
            처음가로=Prozor->koordinata_x;처음세로=Prozor->세로좌표;처음너비=Prozor->너비;처음높이=Prozor->높이;
            if(identifikator_VALUE!=Fokus)앞으로올리기(identifikator_VALUE);return;
        }
        if(세로좌표<32&&koordinata_x>=6&&koordinata_x<142){Create_unos();return;}
        if(세로좌표<32&&koordinata_x>=154&&koordinata_x<602){앞으로올리기((koordinata_x-154)/112);return;}
        if(identifikator_VALUE>=0){
            Terminal_d413d4bc *Prozor=&Windows_Popis[identifikator_VALUE];
            if(세로좌표<(int)Prozor->세로좌표+30&&koordinata_x>=(int)(Prozor->koordinata_x+Prozor->너비)-32){Zatvori_prozor(identifikator_VALUE);return;}
            if(identifikator_VALUE!=Fokus)앞으로올리기(identifikator_VALUE);
            if(세로좌표<(int)Prozor->세로좌표+30){vući_VALUE=identifikator_VALUE;vući_X=koordinata_x-Prozor->koordinata_x;vući_Y=세로좌표-Prozor->세로좌표;}return;
        }
    }
    if(Fokus>=0&&(눌림&(8|16))){Terminal_unos=&Windows_Popis[Fokus];if(눌림&8){unsigned 한도=Terminal_unos->맨위;if(한도>Povijest_red_COUNT-Terminal_unos->ROW_COUNT)한도=Povijest_red_COUNT-Terminal_unos->ROW_COUNT;Terminal_unos->밀어올리기=Terminal_unos->밀어올리기+9>한도?한도:Terminal_unos->밀어올리기+9;}else Terminal_unos->밀어올리기=Terminal_unos->밀어올리기<9?0:Terminal_unos->밀어올리기-9;다시그리기();}
}
void 터미널바로가기키(unsigned 누름값){if(누름값==1)Create_unos();if(누름값==2&&unos_COUNT)앞으로올리기(narudžba_VALUE[0]);if(누름값==3)Zatvori_prozor(Fokus);}
stroj_Word pano_Terminal(stroj_Word Aktivnost){
    if(Aktivnost==300){if(!Windows_Popis[출력결과].살아있음)return Create_unos();stolni_Prikaz=1;다시그리기();return 0;}
    if(Aktivnost==0){Zatvori_prozor(Fokus);return 0;}if(Aktivnost==1)return (uint32_t)Create_unos();if(Aktivnost==2)return Fokus>=0;
    if(Aktivnost==9){stolni_Prikaz=0;return 0;}if(Aktivnost==7)return unos_COUNT;if(Aktivnost==10)return Fokus+1;if(Aktivnost==11)return 출력결과;
    if(Aktivnost==13){Terminal_d413d4bc *Prozor=&Windows_Popis[출력결과];return Prozor->살아있음?(Prozor->ROW_COUNT<<16)|Prozor->COLUMNS:(19<<16)|68;}
    if(Aktivnost==14){unsigned VALUE=Windows_Popis[출력결과].크기바뀜;Windows_Popis[출력결과].크기바뀜=0;return VALUE;}
    if(Aktivnost==12){unsigned VALUE=odjel_informacijske_tehnologije_na_čekanju;odjel_informacijske_tehnologije_na_čekanju=0;return VALUE;}
    if(Aktivnost>=20&&Aktivnost<24)return Windows_Popis[Aktivnost-20].살아있음;
    if(Aktivnost>=100&&Aktivnost<104){출력결과=Aktivnost-100;Terminal_unos=&Windows_Popis[출력결과];return 0;}
    if(Aktivnost>=200&&Aktivnost<204){앞으로올리기(Aktivnost-200);return 0;}
    if(Aktivnost==3){다시그리기();return 0;}Terminal_unos=&Windows_Popis[출력결과];if(!Terminal_unos->살아있음)return 0;
    if(Aktivnost==4)očistiti_Sadržaj();if(Aktivnost==5||Aktivnost==6){unsigned 이전=단추들;Terminal_pokazivač(Aktivnost==5?8:16,0,0);단추들=이전;}return 1;
}
