#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* 자체 네 Dritare 합성과 UTF-8 Terminali. 바뀐 영역의 완성 그림만 표시한다. */
#include <stdint.h>
#include <stddef.h>
typedef uintptr_t makinë_Word;
extern makinë_Word panel_pikëz(makinë_Word,makinë_Word,makinë_Word),보드화면기억공간(void);
extern void *memset(void *,int,size_t);
extern const unsigned char Terminali_font[];
#define 최대열수 237
#define histori_linjë_COUNT 160
typedef struct {
    uint32_t 글자칸들[histori_linjë_COUNT][최대열수]; uint8_t 모양들[histori_linjë_COUNT][최대열수];
    unsigned 너비,높이,COLUMNS,ROW_COUNT,크기바뀜;
    unsigned 살아있음,koordinata_x,Y_koordinatë,ROW_pozicioni,COLUMN_pozicioni,맨위,lëviz,전경색,배경색,탈출상태,parametër_VALUE[4],parametër_INDEX,저장행,저장열;
    unsigned 부호없는결과,긴부호없는값,SMALL_VALUE,대체화면,가리개보임;
} Terminali_d413d4bc;
static Terminali_d413d4bc Windows_Listë[4];
static int Fokus=-1,출력결과,renditja_VALUE[4],futje_COUNT,zvarrit_VALUE=-1,zvarrit_X,zvarrit_Y;
static unsigned teknologjia_e_informacionit_në_pritje,단추들,desktop_Pamja,한글입력;
static const uint32_t 색상들[16]={0x201a15,0x6060df,0x9dcc86,0x80cfea,0xefaf72,0xca96c9,0xceda76,0xede9df,0x858078,0x8888ff,0xb9eba7,0xa5eaff,0xffcc99,0xf0bef1,0xf0f0a0,0xffffff};
extern int 화면보임(int),화면가리킴(int,unsigned,int,int);
extern void 화면다시그림(int);
static Terminali_d413d4bc *Terminali_futje;
static unsigned 넓은글자(unsigned kodi_i_karakterit){return kodi_i_karakterit>=256?2:1;}
static void 사각영역(unsigned koordinata_x,unsigned Y_koordinatë,unsigned 너비값,unsigned 높이값,unsigned 색상){
    보드사각그림(koordinata_x,Y_koordinatë,너비값,높이값,색상);
}
void Terminali_glif(unsigned koordinata_x,unsigned Y_koordinatë,unsigned kodi_i_karakterit,unsigned 전경색,unsigned 배경색){
    unsigned 너비=넓은글자(kodi_i_karakterit)*8;if(kodi_i_karakterit==0xffffffffu)return;
    int 왼쪽=koordinata_x,위쪽=Y_koordinatë,폭=너비,gjatësi_VALUE=16;
    if(!보드그림범위(&왼쪽,&위쪽,&폭,&gjatësi_VALUE))return;
    if(kodi_i_karakterit==' '){보드사각그림(왼쪽,위쪽,폭,gjatësi_VALUE,배경색);return;}
    unsigned LOOKUP_INDEX=kodi_i_karakterit<65536?kodi_i_karakterit:kodi_i_karakterit>=0x1f600&&kodi_i_karakterit<0x1f650?65536+kodi_i_karakterit-0x1f600:0xfffd;
    const unsigned char *font_VALUE=Terminali_font+LOOKUP_INDEX*32;
    for(int linjë=위쪽;linjë<위쪽+gjatësi_VALUE;linjë++){unsigned Shërbimi_i_transferimit_inteligjent_në_sfond_Listë=font_VALUE[(linjë-Y_koordinatë)*2]*256+font_VALUE[(linjë-Y_koordinatë)*2+1];for(int hapësirë_për_tekst_futje=왼쪽;hapësirë_për_tekst_futje<왼쪽+폭;hapësirë_për_tekst_futje++)panel_pikëz(hapësirë_për_tekst_futje,linjë,(Shërbimi_i_transferimit_inteligjent_në_sfond_Listë&(0x8000>>(hapësirë_për_tekst_futje-koordinata_x)))?전경색:배경색);}
}
static void emër_tabelë(unsigned koordinata_x,unsigned Y_koordinatë,const char *varg_të_dhëna,unsigned 전경색,unsigned 배경색){while(*varg_të_dhëna){unsigned kodi_i_karakterit=(unsigned char)*varg_të_dhëna++, 남은수=0;if(kodi_i_karakterit>=0xc0){남은수=kodi_i_karakterit<0xe0?1:kodi_i_karakterit<0xf0?2:3;kodi_i_karakterit&=(1u<<(6-남은수))-1;while(남은수--&&*varg_të_dhëna)kodi_i_karakterit=(kodi_i_karakterit<<6)|((unsigned char)*varg_të_dhëna++&63);}Terminali_glif(koordinata_x,Y_koordinatë,kodi_i_karakterit,전경색,배경색);koordinata_x+=넓은글자(kodi_i_karakterit)*8;}}
static unsigned 첫항목(void){return Terminali_futje->맨위;}
static int 보이는지(void){return Terminali_futje->살아있음&&Fokus>=0&&Terminali_futje==&Windows_Listë[Fokus]&&!화면보임(Fokus);}
static void 그리기(unsigned ROW_pozicioni,unsigned COLUMN_pozicioni){
    if(!보이는지()||ROW_pozicioni<첫항목()-Terminali_futje->lëviz||ROW_pozicioni>=첫항목()-Terminali_futje->lëviz+Terminali_futje->ROW_COUNT||COLUMN_pozicioni>=Terminali_futje->COLUMNS)return;
    unsigned kodi_i_karakterit=Terminali_futje->글자칸들[ROW_pozicioni%histori_linjë_COUNT][COLUMN_pozicioni],varg_të_dhëna=Terminali_futje->모양들[ROW_pozicioni%histori_linjë_COUNT][COLUMN_pozicioni];
    if(넓은글자(kodi_i_karakterit)==2&&COLUMN_pozicioni+1>=Terminali_futje->COLUMNS)kodi_i_karakterit=' ';
    Terminali_glif(Terminali_futje->koordinata_x+12+COLUMN_pozicioni*8,Terminali_futje->Y_koordinatë+36+(ROW_pozicioni-첫항목()+Terminali_futje->lëviz)*16,kodi_i_karakterit?kodi_i_karakterit:' ',색상들[varg_të_dhëna&15],색상들[varg_të_dhëna>>4]);
}
static void karet_VALUE(int shfaq_dritare){if(!보이는지()||Terminali_futje->lëviz||Terminali_futje->COLUMN_pozicioni>=Terminali_futje->COLUMNS||Terminali_futje->ROW_pozicioni<Terminali_futje->맨위||Terminali_futje->ROW_pozicioni>=Terminali_futje->맨위+Terminali_futje->ROW_COUNT)return;
    if(!shfaq_dritare||!Terminali_futje->가리개보임)그리기(Terminali_futje->ROW_pozicioni,Terminali_futje->COLUMN_pozicioni);else 사각영역(Terminali_futje->koordinata_x+12+Terminali_futje->COLUMN_pozicioni*8,Terminali_futje->Y_koordinatë+36+(Terminali_futje->ROW_pozicioni-Terminali_futje->맨위)*16+14,8,2,색상들[Terminali_futje->전경색]);}
static void Përmbajtje_VALUE(void){
    사각영역(Terminali_futje->koordinata_x+12,Terminali_futje->Y_koordinatë+36,Terminali_futje->COLUMNS*8,Terminali_futje->ROW_COUNT*16,색상들[0]);
    int 가로=Terminali_futje->koordinata_x+12,Vertikal_pozicioni=Terminali_futje->Y_koordinatë+36,폭=Terminali_futje->COLUMNS*8,gjatësi_VALUE=Terminali_futje->ROW_COUNT*16;
    if(보드그림범위(&가로,&Vertikal_pozicioni,&폭,&gjatësi_VALUE)){
    unsigned 첫줄=(Vertikal_pozicioni-Terminali_futje->Y_koordinatë-36)/16,끝줄=(Vertikal_pozicioni+gjatësi_VALUE-Terminali_futje->Y_koordinatë-36+15)/16;
    unsigned 첫칸=(가로-Terminali_futje->koordinata_x-12)/8,끝칸=(가로+폭-Terminali_futje->koordinata_x-12+7)/8;
    if(첫칸)첫칸--; /* 잘림 경계 왼쪽에서 시작한 두 hapësirë_për_tekst_futje 글자도 그린다. */
    for(unsigned 반환값=첫줄;반환값<끝줄;반환값++)for(unsigned kodi_i_karakterit=첫칸;kodi_i_karakterit<끝칸;kodi_i_karakterit++){
        unsigned ROW_pozicioni=첫항목()-Terminali_futje->lëviz+반환값,karakter_VALUE=Terminali_futje->글자칸들[ROW_pozicioni%histori_linjë_COUNT][kodi_i_karakterit],varg_të_dhëna=Terminali_futje->모양들[ROW_pozicioni%histori_linjë_COUNT][kodi_i_karakterit];
        if(넓은글자(karakter_VALUE)==2&&kodi_i_karakterit+1>=Terminali_futje->COLUMNS)karakter_VALUE=' ';
        if((karakter_VALUE==0||karakter_VALUE==' ')&&(varg_të_dhëna>>4)==0)continue;
        Terminali_glif(Terminali_futje->koordinata_x+12+kodi_i_karakterit*8,Terminali_futje->Y_koordinatë+36+반환값*16,karakter_VALUE?karakter_VALUE:' ',색상들[varg_të_dhëna&15],색상들[varg_të_dhëna>>4]);
    }}
    emër_tabelë(Terminali_futje->koordinata_x+12,Terminali_futje->Y_koordinatë+Terminali_futje->높이-18,Terminali_futje->lëviz?"PgDn: recent output":Terminali_futje->너비>=500?"F6: next | Corner + left drag: resize":"Corner + left drag: resize",0xece8e2,0x403127);karet_VALUE(1);
}
static void 실행틀(int identifikues_VALUE){
    Terminali_futje=&Windows_Listë[identifikues_VALUE];
    int 가로=Terminali_futje->koordinata_x,Vertikal_pozicioni=Terminali_futje->Y_koordinatë,폭=Terminali_futje->너비,gjatësi_VALUE=Terminali_futje->높이;
    if(!보드그림범위(&가로,&Vertikal_pozicioni,&폭,&gjatësi_VALUE))return;
    사각영역(Terminali_futje->koordinata_x,Terminali_futje->Y_koordinatë,Terminali_futje->너비,Terminali_futje->높이,0x403127);
    unsigned 색상=identifikues_VALUE==Fokus?0x905020:0x604438;사각영역(Terminali_futje->koordinata_x,Terminali_futje->Y_koordinatë,Terminali_futje->너비,30,색상);
    emër_tabelë(Terminali_futje->koordinata_x+12,Terminali_futje->Y_koordinatë+7,"JKOROS Terminal",0xffffff,색상);
    char 수치[2]={(char)('1'+identifikues_VALUE),0};emër_tabelë(Terminali_futje->koordinata_x+148,Terminali_futje->Y_koordinatë+7,수치,0xffffff,색상);
    emër_tabelë(Terminali_futje->koordinata_x+240,Terminali_futje->Y_koordinatë+7,Terminali_futje->너비>=500?(한글입력?"[SQ] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[SQ]":"[EN]"),0xffffff,색상);
    사각영역(Terminali_futje->koordinata_x+Terminali_futje->너비-32,Terminali_futje->Y_koordinatë+4,26,22,0x5555b8);emër_tabelë(Terminali_futje->koordinata_x+Terminali_futje->너비-24,Terminali_futje->Y_koordinatë+7,"X",0xffffff,0x5555b8);
    Përmbajtje_VALUE();
}
static void 장면그리기(void){
    if(!desktop_Pamja)return;사각영역(0,0,보드화면너비(),보드화면높이(),0x302018);사각영역(0,0,보드화면너비(),32,0x403127);
    사각영역(6,4,136,24,0x905020);emër_tabelë(14,8,"+ New terminal",0xffffff,0x905020);
    for(int 순번=0;순번<4;순번++)if(Windows_Listë[순번].살아있음){unsigned kodi_i_karakterit=Fokus==순번?0x905020:0x604438;사각영역(154+순번*112,4,106,24,kodi_i_karakterit);emër_tabelë(160+순번*112,8,"Terminal",0xffffff,kodi_i_karakterit);char varg_të_dhëna[2]={(char)('1'+순번),0};emër_tabelë(232+순번*112,8,varg_të_dhëna,0xffffff,kodi_i_karakterit);}
    if(!futje_COUNT)emër_tabelë(140,210,"Click + New terminal to start",0xede9df,0x302018);
    for(int 순번=0;순번<futje_COUNT;순번++)실행틀(renditja_VALUE[순번]);화면다시그림(Fokus);Terminali_futje=&Windows_Listë[출력결과];
}
static void 영역그리기(int 가로,int Vertikal_pozicioni,int 폭,int gjatësi_VALUE){
    if(!desktop_Pamja||!보드그림범위(&가로,&Vertikal_pozicioni,&폭,&gjatësi_VALUE))return;
    for(int linjë=Vertikal_pozicioni;linjë<Vertikal_pozicioni+gjatësi_VALUE;linjë+=32){
        int 띠높이=Vertikal_pozicioni+gjatësi_VALUE-linjë;if(띠높이>32)띠높이=32;
        if(panel_nis_vizatim(가로,linjë,폭,띠높이)){장면그리기();panel_Përfundo_vizatim();}
    }
}
static void 다시그리기(void){영역그리기(0,0,보드화면너비(),보드화면높이());}
/* 서로 겹치지 않는 새 Dritare 영역과 이전 자리의 네 띠를 복구한다. */
static void 창자리그리기(int 가로,int Vertikal_pozicioni,int 폭,int gjatësi_VALUE,Terminali_d413d4bc *Dritare){
    int 왼쪽=가로>(int)Dritare->koordinata_x?가로:(int)Dritare->koordinata_x;
    int 위쪽=Vertikal_pozicioni>(int)Dritare->Y_koordinatë?Vertikal_pozicioni:(int)Dritare->Y_koordinatë;
    int RIGHT=가로+폭<(int)(Dritare->koordinata_x+Dritare->너비)?가로+폭:(int)(Dritare->koordinata_x+Dritare->너비);
    int 아래쪽=Vertikal_pozicioni+gjatësi_VALUE<(int)(Dritare->Y_koordinatë+Dritare->높이)?Vertikal_pozicioni+gjatësi_VALUE:(int)(Dritare->Y_koordinatë+Dritare->높이);
    영역그리기(Dritare->koordinata_x,Dritare->Y_koordinatë,Dritare->너비,Dritare->높이);
    if(왼쪽>=RIGHT||위쪽>=아래쪽){영역그리기(가로,Vertikal_pozicioni,폭,gjatësi_VALUE);return;}
    영역그리기(가로,Vertikal_pozicioni,폭,위쪽-Vertikal_pozicioni);
    영역그리기(가로,아래쪽,폭,Vertikal_pozicioni+gjatësi_VALUE-아래쪽);
    영역그리기(가로,위쪽,왼쪽-가로,아래쪽-위쪽);
    영역그리기(RIGHT,위쪽,가로+폭-RIGHT,아래쪽-위쪽);
}
static void 초점알리기(void){teknologjia_e_informacionit_në_pritje=(teknologjia_e_informacionit_në_pritje&~15u)|(unsigned)(Fokus+1)|0x10000;}
void 터미널입력방식(unsigned 한글여부){
    한글입력=한글여부!=0;
    /* Update title bars only: a mode switch must not erase an EL0 drawing. */
    if(Fokus>=0){
        Terminali_d413d4bc *dritare_futje=&Windows_Listë[Fokus];
        emër_tabelë(dritare_futje->koordinata_x+240,dritare_futje->Y_koordinatë+7,dritare_futje->너비>=500?(한글입력?"[SQ] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[SQ]":"[EN]"),0xffffff,0x905020);
    }
}
static void 앞으로올리기(int identifikues_VALUE){if(identifikues_VALUE<0||identifikues_VALUE>=4||!Windows_Listë[identifikues_VALUE].살아있음)return;int 현재위치=0;while(현재위치<futje_COUNT&&renditja_VALUE[현재위치]!=identifikues_VALUE)현재위치++;for(;현재위치+1<futje_COUNT;현재위치++)renditja_VALUE[현재위치]=renditja_VALUE[현재위치+1];renditja_VALUE[futje_COUNT-1]=identifikues_VALUE;Fokus=identifikues_VALUE;초점알리기();다시그리기();}
static void 빈칸채우기(unsigned ROW_pozicioni){for(unsigned kodi_i_karakterit=0;kodi_i_karakterit<최대열수;kodi_i_karakterit++){Terminali_futje->글자칸들[ROW_pozicioni%histori_linjë_COUNT][kodi_i_karakterit]=0;Terminali_futje->모양들[ROW_pozicioni%histori_linjë_COUNT][kodi_i_karakterit]=Terminali_futje->전경색|(Terminali_futje->배경색<<4);}}
static void pastroj_TOC(void){Terminali_futje->ROW_pozicioni=Terminali_futje->COLUMN_pozicioni=Terminali_futje->맨위=Terminali_futje->lëviz=0;for(unsigned 반환값=0;반환값<histori_linjë_COUNT;반환값++)빈칸채우기(반환값);if(보이는지())Përmbajtje_VALUE();}
static int Krijo_futje(void){
    if(!보드화면기억공간())return -19;int identifikues_VALUE=0;while(identifikues_VALUE<4&&Windows_Listë[identifikues_VALUE].살아있음)identifikues_VALUE++;if(identifikues_VALUE==4)return -28;
    desktop_Pamja=1;Terminali_futje=&Windows_Listë[identifikues_VALUE];memset(Terminali_futje,0,sizeof(*Terminali_futje));Terminali_futje->살아있음=1;Terminali_futje->너비=568;Terminali_futje->높이=360;Terminali_futje->COLUMNS=68;Terminali_futje->ROW_COUNT=19;Terminali_futje->koordinata_x=12+identifikues_VALUE*16;Terminali_futje->Y_koordinatë=48+identifikues_VALUE*18;Terminali_futje->전경색=7;Terminali_futje->가리개보임=1;
    for(unsigned 반환값=0;반환값<histori_linjë_COUNT;반환값++)빈칸채우기(반환값);renditja_VALUE[futje_COUNT++]=identifikues_VALUE;Fokus=identifikues_VALUE;teknologjia_e_informacionit_në_pritje|=1u<<(4+identifikues_VALUE);초점알리기();다시그리기();return identifikues_VALUE+1;
}
static void mbyll_dritare(int identifikues_VALUE){
    if(identifikues_VALUE<0||identifikues_VALUE>=4||!Windows_Listë[identifikues_VALUE].살아있음)return;Windows_Listë[identifikues_VALUE].살아있음=0;teknologjia_e_informacionit_në_pritje|=1u<<(8+identifikues_VALUE);
    int 현재위치=0;while(현재위치<futje_COUNT&&renditja_VALUE[현재위치]!=identifikues_VALUE)현재위치++;for(;현재위치+1<futje_COUNT;현재위치++)renditja_VALUE[현재위치]=renditja_VALUE[현재위치+1];futje_COUNT--;
    if(Fokus==identifikues_VALUE)Fokus=futje_COUNT?renditja_VALUE[futje_COUNT-1]:-1;초점알리기();다시그리기();
}
static void 줄바꿈(void){Terminali_futje->COLUMN_pozicioni=0;Terminali_futje->ROW_pozicioni++;if(Terminali_futje->ROW_pozicioni>=Terminali_futje->맨위+Terminali_futje->ROW_COUNT){Terminali_futje->맨위++;빈칸채우기(Terminali_futje->ROW_pozicioni);if(보이는지())Përmbajtje_VALUE();}}
static void kodi_i_karakterit_451f2815(unsigned kodi_i_karakterit){
    if(kodi_i_karakterit==13){Terminali_futje->COLUMN_pozicioni=0;return;}if(kodi_i_karakterit==10){줄바꿈();return;}if(kodi_i_karakterit==8){if(Terminali_futje->COLUMN_pozicioni)Terminali_futje->COLUMN_pozicioni--;return;}
    if(kodi_i_karakterit==9){unsigned njësi_COUNT=8-Terminali_futje->COLUMN_pozicioni%8;while(njësi_COUNT--)kodi_i_karakterit_451f2815(' ');return;}if(kodi_i_karakterit<32||kodi_i_karakterit==127)return;
    unsigned 너비값=넓은글자(kodi_i_karakterit);if(Terminali_futje->COLUMN_pozicioni+너비값>Terminali_futje->COLUMNS)줄바꿈();
    if(Terminali_futje->글자칸들[Terminali_futje->ROW_pozicioni%histori_linjë_COUNT][Terminali_futje->COLUMN_pozicioni]==0xffffffffu&&Terminali_futje->COLUMN_pozicioni){Terminali_futje->글자칸들[Terminali_futje->ROW_pozicioni%histori_linjë_COUNT][Terminali_futje->COLUMN_pozicioni-1]=' ';그리기(Terminali_futje->ROW_pozicioni,Terminali_futje->COLUMN_pozicioni-1);}
    if(넓은글자(Terminali_futje->글자칸들[Terminali_futje->ROW_pozicioni%histori_linjë_COUNT][Terminali_futje->COLUMN_pozicioni])==2&&Terminali_futje->COLUMN_pozicioni+1<Terminali_futje->COLUMNS){Terminali_futje->글자칸들[Terminali_futje->ROW_pozicioni%histori_linjë_COUNT][Terminali_futje->COLUMN_pozicioni+1]=' ';그리기(Terminali_futje->ROW_pozicioni,Terminali_futje->COLUMN_pozicioni+1);}
    Terminali_futje->글자칸들[Terminali_futje->ROW_pozicioni%histori_linjë_COUNT][Terminali_futje->COLUMN_pozicioni]=kodi_i_karakterit;Terminali_futje->모양들[Terminali_futje->ROW_pozicioni%histori_linjë_COUNT][Terminali_futje->COLUMN_pozicioni]=Terminali_futje->전경색|(Terminali_futje->배경색<<4);
    if(너비값==2)Terminali_futje->글자칸들[Terminali_futje->ROW_pozicioni%histori_linjë_COUNT][Terminali_futje->COLUMN_pozicioni+1]=0xffffffffu;
    그리기(Terminali_futje->ROW_pozicioni,Terminali_futje->COLUMN_pozicioni);Terminali_futje->COLUMN_pozicioni+=너비값;
}
static void dorezë_kontroll_SEQUENCE(unsigned kodi_i_karakterit){
    unsigned njësi_COUNT=Terminali_futje->parametër_VALUE[0]?Terminali_futje->parametër_VALUE[0]:1;
    if(kodi_i_karakterit=='m')for(unsigned 순번=0;순번<=Terminali_futje->parametër_INDEX;순번++){unsigned të_dhëna_pozicioni=Terminali_futje->parametër_VALUE[순번];if(!të_dhëna_pozicioni){Terminali_futje->전경색=7;Terminali_futje->배경색=0;}if(të_dhëna_pozicioni==1&&Terminali_futje->전경색<8)Terminali_futje->전경색+=8;if(të_dhëna_pozicioni==7){unsigned 유지=Terminali_futje->전경색;Terminali_futje->전경색=Terminali_futje->배경색;Terminali_futje->배경색=유지;}if(të_dhëna_pozicioni>=30&&të_dhëna_pozicioni<=37)Terminali_futje->전경색=të_dhëna_pozicioni-30;if(të_dhëna_pozicioni>=90&&të_dhëna_pozicioni<=97)Terminali_futje->전경색=të_dhëna_pozicioni-90+8;if(të_dhëna_pozicioni>=40&&të_dhëna_pozicioni<=47)Terminali_futje->배경색=të_dhëna_pozicioni-40;if(të_dhëna_pozicioni>=100&&të_dhëna_pozicioni<=107)Terminali_futje->배경색=të_dhëna_pozicioni-100+8;if(të_dhëna_pozicioni==39)Terminali_futje->전경색=7;if(të_dhëna_pozicioni==49)Terminali_futje->배경색=0;}
    if(kodi_i_karakterit=='J'&&(Terminali_futje->parametër_VALUE[0]==2||Terminali_futje->parametër_VALUE[0]==3))pastroj_TOC();
    if(kodi_i_karakterit=='K'){unsigned 출발위치=Terminali_futje->parametër_VALUE[0]==2?0:Terminali_futje->COLUMN_pozicioni,도착위치=Terminali_futje->parametër_VALUE[0]==1?Terminali_futje->COLUMN_pozicioni+1:Terminali_futje->COLUMNS;if(Terminali_futje->parametër_VALUE[0]==1)출발위치=0;for(unsigned 순번=출발위치;순번<도착위치&&순번<Terminali_futje->COLUMNS;순번++){
        unsigned ROW_VALUE=Terminali_futje->ROW_pozicioni%histori_linjë_COUNT,karakter_VALUE=Terminali_futje->글자칸들[ROW_VALUE][순번],formë_VALUE=Terminali_futje->전경색|(Terminali_futje->배경색<<4);
        /* 넓은 vi 화면에서도 이미 빈 칸의 font_VALUE 화소를 되풀이해 칠하지 않는다. */
        int 바뀜=(karakter_VALUE!=0&&karakter_VALUE!=' ')||Terminali_futje->모양들[ROW_VALUE][순번]!=formë_VALUE;
        Terminali_futje->글자칸들[ROW_VALUE][순번]=' ';Terminali_futje->모양들[ROW_VALUE][순번]=formë_VALUE;
        if(바뀜)그리기(Terminali_futje->ROW_pozicioni,순번);
    }}
    if(kodi_i_karakterit=='D')Terminali_futje->COLUMN_pozicioni=njësi_COUNT>Terminali_futje->COLUMN_pozicioni?0:Terminali_futje->COLUMN_pozicioni-njësi_COUNT;if(kodi_i_karakterit=='C')Terminali_futje->COLUMN_pozicioni=Terminali_futje->COLUMN_pozicioni+njësi_COUNT>=Terminali_futje->COLUMNS?Terminali_futje->COLUMNS-1:Terminali_futje->COLUMN_pozicioni+njësi_COUNT;
    if(kodi_i_karakterit=='G')Terminali_futje->COLUMN_pozicioni=njësi_COUNT>Terminali_futje->COLUMNS?Terminali_futje->COLUMNS-1:njësi_COUNT-1;if(kodi_i_karakterit=='A')Terminali_futje->ROW_pozicioni=njësi_COUNT>Terminali_futje->ROW_pozicioni-Terminali_futje->맨위?Terminali_futje->맨위:Terminali_futje->ROW_pozicioni-njësi_COUNT;
    if(kodi_i_karakterit=='B')Terminali_futje->ROW_pozicioni=Terminali_futje->ROW_pozicioni+njësi_COUNT>=Terminali_futje->맨위+Terminali_futje->ROW_COUNT?Terminali_futje->맨위+Terminali_futje->ROW_COUNT-1:Terminali_futje->ROW_pozicioni+njësi_COUNT;
    if(kodi_i_karakterit=='H'||kodi_i_karakterit=='f'){Terminali_futje->ROW_pozicioni=Terminali_futje->맨위+(njësi_COUNT>Terminali_futje->ROW_COUNT?Terminali_futje->ROW_COUNT:njësi_COUNT)-1;unsigned koordinata_x=Terminali_futje->parametër_VALUE[1]?Terminali_futje->parametër_VALUE[1]:1;Terminali_futje->COLUMN_pozicioni=(koordinata_x>Terminali_futje->COLUMNS?Terminali_futje->COLUMNS:koordinata_x)-1;}
    if(kodi_i_karakterit=='s'){Terminali_futje->저장행=Terminali_futje->ROW_pozicioni;Terminali_futje->저장열=Terminali_futje->COLUMN_pozicioni;}if(kodi_i_karakterit=='u'){Terminali_futje->ROW_pozicioni=Terminali_futje->저장행;Terminali_futje->COLUMN_pozicioni=Terminali_futje->저장열<Terminali_futje->COLUMNS?Terminali_futje->저장열:Terminali_futje->COLUMNS-1;}
    if((kodi_i_karakterit=='h'||kodi_i_karakterit=='l')&&Terminali_futje->parametër_VALUE[0]==25)Terminali_futje->가리개보임=kodi_i_karakterit=='h';
}
void Terminali_bajt(unsigned SECOND_VALUE){
    Terminali_futje=&Windows_Listë[출력결과];if(!Terminali_futje->살아있음)return;karet_VALUE(0);if(Terminali_futje->lëviz){Terminali_futje->lëviz=0;if(보이는지())Përmbajtje_VALUE();}
    if(Terminali_futje->탈출상태==1){Terminali_futje->탈출상태=SECOND_VALUE=='['?2:0;Terminali_futje->parametër_INDEX=0;for(unsigned 순번=0;순번<4;순번++)Terminali_futje->parametër_VALUE[순번]=0;}
    else if(Terminali_futje->탈출상태==2){if(SECOND_VALUE=='?'){}else if(SECOND_VALUE>='0'&&SECOND_VALUE<='9'){if(Terminali_futje->parametër_VALUE[Terminali_futje->parametër_INDEX]<10000)Terminali_futje->parametër_VALUE[Terminali_futje->parametër_INDEX]=Terminali_futje->parametër_VALUE[Terminali_futje->parametër_INDEX]*10+SECOND_VALUE-'0';}else if(SECOND_VALUE==';'&&Terminali_futje->parametër_INDEX<3)Terminali_futje->parametër_INDEX++;else{dorezë_kontroll_SEQUENCE(SECOND_VALUE);Terminali_futje->탈출상태=0;}}
    else if(SECOND_VALUE==27){Terminali_futje->긴부호없는값=0;Terminali_futje->탈출상태=1;}else{
        if(Terminali_futje->긴부호없는값&&(SECOND_VALUE&0xc0)!=0x80){Terminali_futje->긴부호없는값=0;kodi_i_karakterit_451f2815(0xfffd);}
        if(Terminali_futje->긴부호없는값){Terminali_futje->부호없는결과=Terminali_futje->부호없는결과*64+(SECOND_VALUE&63);if(--Terminali_futje->긴부호없는값==0)kodi_i_karakterit_451f2815(Terminali_futje->부호없는결과<Terminali_futje->SMALL_VALUE||Terminali_futje->부호없는결과>0x10ffff||(Terminali_futje->부호없는결과>=0xd800&&Terminali_futje->부호없는결과<=0xdfff)?0xfffd:Terminali_futje->부호없는결과);}
        else if(SECOND_VALUE<128)kodi_i_karakterit_451f2815(SECOND_VALUE);else if(SECOND_VALUE>=0xc2&&SECOND_VALUE<=0xf4){Terminali_futje->긴부호없는값=SECOND_VALUE<0xe0?1:SECOND_VALUE<0xf0?2:3;Terminali_futje->부호없는결과=SECOND_VALUE&((1u<<(6-Terminali_futje->긴부호없는값))-1);Terminali_futje->SMALL_VALUE=Terminali_futje->긴부호없는값==1?128:Terminali_futje->긴부호없는값==2?2048:65536;}else kodi_i_karakterit_451f2815(0xfffd);
    }karet_VALUE(1);
}
int Terminali_në_pritje(void){return teknologjia_e_informacionit_në_pritje!=0;}
/* 모서리 INDEX: 1 좌상, 2 우상, 3 좌하, 4 우하. */
static int ndrysho_madhësinë_zvarrit=-1,잡은모서리,잡은가로,잡은세로,처음가로,처음세로,처음너비,처음높이;
static int 가리킨창(int 가로,int Vertikal_pozicioni) {
    for(int SEQUENCE_VALUE=futje_COUNT-1;SEQUENCE_VALUE>=0;SEQUENCE_VALUE--){
        int identifikues_VALUE=renditja_VALUE[SEQUENCE_VALUE];Terminali_d413d4bc *Dritare=&Windows_Listë[identifikues_VALUE];
        if(가로>=(int)Dritare->koordinata_x&&Vertikal_pozicioni>=(int)Dritare->Y_koordinatë&&
           가로<(int)(Dritare->koordinata_x+Dritare->너비)&&Vertikal_pozicioni<(int)(Dritare->Y_koordinatë+Dritare->높이))return identifikues_VALUE;
    }return -1;
}
static int 모서리찾기(int identifikues_VALUE,int 가로,int Vertikal_pozicioni) {
    if(identifikues_VALUE<0)return 0;Terminali_d413d4bc *Dritare=&Windows_Listë[identifikues_VALUE];
    int 왼쪽=가로<(int)Dritare->koordinata_x+8,RIGHT=가로>=(int)(Dritare->koordinata_x+Dritare->너비)-8;
    int 위쪽=Vertikal_pozicioni<(int)Dritare->Y_koordinatë+8,아래쪽=Vertikal_pozicioni>=(int)(Dritare->Y_koordinatë+Dritare->높이)-8;
    return (왼쪽||RIGHT)&&(위쪽||아래쪽)?1+RIGHT+아래쪽*2:0;
}
static int ndarësi_VALUE(int VALUE,int 최소,int 최대){return VALUE<최소?최소:VALUE>최대?최대:VALUE;}
static void lëviz_ndrysho_madhësinë(int 가로,int Vertikal_pozicioni) {
    Terminali_d413d4bc *Dritare=&Windows_Listë[ndrysho_madhësinë_zvarrit];int 왼쪽=처음가로,위쪽=처음세로,RIGHT=처음가로+처음너비,아래쪽=처음세로+처음높이;
    if(잡은모서리==1||잡은모서리==3)왼쪽=ndarësi_VALUE(처음가로+가로-잡은가로,0,RIGHT-360);
    else RIGHT=ndarësi_VALUE(처음가로+처음너비+가로-잡은가로,왼쪽+360,보드화면너비());
    if(잡은모서리<=2)위쪽=ndarësi_VALUE(처음세로+Vertikal_pozicioni-잡은세로,34,아래쪽-216);
    else 아래쪽=ndarësi_VALUE(처음세로+처음높이+Vertikal_pozicioni-잡은세로,위쪽+216,보드화면높이());
    unsigned COLUMNS=(RIGHT-왼쪽-24)/8,ROW_COUNT=(아래쪽-위쪽-56)/16;
    if(Dritare->COLUMNS!=COLUMNS||Dritare->ROW_COUNT!=ROW_COUNT){
        Dritare->크기바뀜=1;Dritare->COLUMNS=COLUMNS;Dritare->ROW_COUNT=ROW_COUNT;
        if(Dritare->COLUMN_pozicioni>=COLUMNS)Dritare->COLUMN_pozicioni=COLUMNS-1;
        if(Dritare->ROW_pozicioni>=Dritare->맨위+ROW_COUNT)Dritare->맨위=Dritare->ROW_pozicioni-ROW_COUNT+1;
        unsigned 한도=Dritare->맨위;if(한도>histori_linjë_COUNT-ROW_COUNT)한도=histori_linjë_COUNT-ROW_COUNT;
        if(Dritare->lëviz>한도)Dritare->lëviz=한도;
    }
    int 옛가로=Dritare->koordinata_x,옛세로=Dritare->Y_koordinatë,옛폭=Dritare->너비,옛길이=Dritare->높이;
    if(옛가로==왼쪽&&옛세로==위쪽&&옛폭==RIGHT-왼쪽&&옛길이==아래쪽-위쪽)return;
    Dritare->koordinata_x=왼쪽;Dritare->Y_koordinatë=위쪽;Dritare->너비=RIGHT-왼쪽;Dritare->높이=아래쪽-위쪽;
    창자리그리기(옛가로,옛세로,옛폭,옛길이,Dritare);
}
void Terminali_tregues(unsigned Tjetër_njësi,int koordinata_x,int Y_koordinatë){
    unsigned 눌림=Tjetër_njësi&~단추들;단추들=Tjetër_njësi;
    if(!desktop_Pamja){zvarrit_VALUE=-1;ndrysho_madhësinë_zvarrit=-1;panel_tregues(koordinata_x,Y_koordinatë,1);return;}
    if(!(Tjetër_njësi&1)){zvarrit_VALUE=-1;ndrysho_madhësinë_zvarrit=-1;}
    if(ndrysho_madhësinë_zvarrit>=0&&!Windows_Listë[ndrysho_madhësinë_zvarrit].살아있음)ndrysho_madhësinë_zvarrit=-1;
    if(zvarrit_VALUE>=0&&!Windows_Listë[zvarrit_VALUE].살아있음)zvarrit_VALUE=-1;
    if(ndrysho_madhësinë_zvarrit>=0){
        lëviz_ndrysho_madhësinë(koordinata_x,Y_koordinatë);panel_tregues(koordinata_x,Y_koordinatë,잡은모서리==1||잡은모서리==4?2:3);return;
    }
    panel_tregues(koordinata_x,Y_koordinatë,1);
    if(zvarrit_VALUE>=0){
        Terminali_d413d4bc *Dritare=&Windows_Listë[zvarrit_VALUE];
        int 옛가로=Dritare->koordinata_x,옛세로=Dritare->Y_koordinatë;
        Dritare->koordinata_x=ndarësi_VALUE(koordinata_x-zvarrit_X,0,보드화면너비()-Dritare->너비);
        Dritare->Y_koordinatë=ndarësi_VALUE(Y_koordinatë-zvarrit_Y,34,보드화면높이()-Dritare->높이);
        if(옛가로!=(int)Dritare->koordinata_x||옛세로!=(int)Dritare->Y_koordinatë)창자리그리기(옛가로,옛세로,Dritare->너비,Dritare->높이,Dritare);
        return;
    }
    extern int 화면덮음(int,int,int);
    if(화면덮음(Fokus,koordinata_x,Y_koordinatë)){화면가리킴(Fokus,눌림,koordinata_x,Y_koordinatë);return;}
    int identifikues_VALUE=가리킨창(koordinata_x,Y_koordinatë),모서리=모서리찾기(identifikues_VALUE,koordinata_x,Y_koordinatë);
    if(모서리)panel_tregues(koordinata_x,Y_koordinatë,모서리==1||모서리==4?2:3);
    if(눌림&1){
        if(모서리){
            Terminali_d413d4bc *Dritare=&Windows_Listë[identifikues_VALUE];ndrysho_madhësinë_zvarrit=identifikues_VALUE;잡은모서리=모서리;잡은가로=koordinata_x;잡은세로=Y_koordinatë;
            처음가로=Dritare->koordinata_x;처음세로=Dritare->Y_koordinatë;처음너비=Dritare->너비;처음높이=Dritare->높이;
            if(identifikues_VALUE!=Fokus)앞으로올리기(identifikues_VALUE);return;
        }
        if(Y_koordinatë<32&&koordinata_x>=6&&koordinata_x<142){Krijo_futje();return;}
        if(Y_koordinatë<32&&koordinata_x>=154&&koordinata_x<602){앞으로올리기((koordinata_x-154)/112);return;}
        if(identifikues_VALUE>=0){
            Terminali_d413d4bc *Dritare=&Windows_Listë[identifikues_VALUE];
            if(Y_koordinatë<(int)Dritare->Y_koordinatë+30&&koordinata_x>=(int)(Dritare->koordinata_x+Dritare->너비)-32){mbyll_dritare(identifikues_VALUE);return;}
            if(identifikues_VALUE!=Fokus)앞으로올리기(identifikues_VALUE);
            if(Y_koordinatë<(int)Dritare->Y_koordinatë+30){zvarrit_VALUE=identifikues_VALUE;zvarrit_X=koordinata_x-Dritare->koordinata_x;zvarrit_Y=Y_koordinatë-Dritare->Y_koordinatë;}return;
        }
    }
    if(Fokus>=0&&(눌림&(8|16))){Terminali_futje=&Windows_Listë[Fokus];if(눌림&8){unsigned 한도=Terminali_futje->맨위;if(한도>histori_linjë_COUNT-Terminali_futje->ROW_COUNT)한도=histori_linjë_COUNT-Terminali_futje->ROW_COUNT;Terminali_futje->lëviz=Terminali_futje->lëviz+9>한도?한도:Terminali_futje->lëviz+9;}else Terminali_futje->lëviz=Terminali_futje->lëviz<9?0:Terminali_futje->lëviz-9;다시그리기();}
}
void 터미널바로가기키(unsigned 누름값){if(누름값==1)Krijo_futje();if(누름값==2&&futje_COUNT)앞으로올리기(renditja_VALUE[0]);if(누름값==3)mbyll_dritare(Fokus);}
makinë_Word panel_Terminali(makinë_Word Veprim){
    if(Veprim==300){if(!Windows_Listë[출력결과].살아있음)return Krijo_futje();desktop_Pamja=1;다시그리기();return 0;}
    if(Veprim==0){mbyll_dritare(Fokus);return 0;}if(Veprim==1)return (uint32_t)Krijo_futje();if(Veprim==2)return Fokus>=0;
    if(Veprim==9){desktop_Pamja=0;return 0;}if(Veprim==7)return futje_COUNT;if(Veprim==10)return Fokus+1;if(Veprim==11)return 출력결과;
    if(Veprim==13){Terminali_d413d4bc *Dritare=&Windows_Listë[출력결과];return Dritare->살아있음?(Dritare->ROW_COUNT<<16)|Dritare->COLUMNS:(19<<16)|68;}
    if(Veprim==14){unsigned VALUE=Windows_Listë[출력결과].크기바뀜;Windows_Listë[출력결과].크기바뀜=0;return VALUE;}
    if(Veprim==12){unsigned VALUE=teknologjia_e_informacionit_në_pritje;teknologjia_e_informacionit_në_pritje=0;return VALUE;}
    if(Veprim>=20&&Veprim<24)return Windows_Listë[Veprim-20].살아있음;
    if(Veprim>=100&&Veprim<104){출력결과=Veprim-100;Terminali_futje=&Windows_Listë[출력결과];return 0;}
    if(Veprim>=200&&Veprim<204){앞으로올리기(Veprim-200);return 0;}
    if(Veprim==3){다시그리기();return 0;}Terminali_futje=&Windows_Listë[출력결과];if(!Terminali_futje->살아있음)return 0;
    if(Veprim==4)pastroj_TOC();if(Veprim==5||Veprim==6){unsigned 이전=단추들;Terminali_tregues(Veprim==5?8:16,0,0);단추들=이전;}return 1;
}
