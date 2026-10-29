#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* propriu 네 Fereastră 합성과 UTF-8 Terminal. 바뀐 영역의 Finalizate_VALUE 그림만 표시한다. */
#include <stdint.h>
#include <stddef.h>
typedef uintptr_t mașină_Word;
extern mașină_Word Avizier_element_imagine(mașină_Word,mașină_Word,mașină_Word),보드화면기억공간(void);
extern void *memset(void *,int,size_t);
extern const unsigned char Terminal_font[];
#define 최대열수 237
#define Istoric_linie_COUNT 160
typedef struct {
    uint32_t 글자칸들[Istoric_linie_COUNT][최대열수]; uint8_t 모양들[Istoric_linie_COUNT][최대열수];
    unsigned 너비,높이,COLUMNS,ROW_COUNT,크기바뀜;
    unsigned 살아있음,coordonata_X,세로좌표,ROW_poziție,COLUMN_poziție,맨위,밀어올리기,전경색,배경색,탈출상태,parametru_VALUE[4],parametru_INDEX,저장행,저장열;
    unsigned 부호없는결과,긴부호없는값,SMALL_VALUE,대체화면,가리개보임;
} Terminal_d413d4bc;
static Terminal_d413d4bc Windows_Listă[4];
static int Focalizat=-1,출력결과,ordine_VALUE[4],intrare_COUNT,glisa_VALUE=-1,glisa_X,glisa_Y;
static unsigned sisteme_de_informații_în_așteptare,단추들,desktop_vizualiza,한글입력;
static const uint32_t 색상들[16]={0x201a15,0x6060df,0x9dcc86,0x80cfea,0xefaf72,0xca96c9,0xceda76,0xede9df,0x858078,0x8888ff,0xb9eba7,0xa5eaff,0xffcc99,0xf0bef1,0xf0f0a0,0xffffff};
extern int 화면보임(int),화면가리킴(int,unsigned,int,int);
extern void 화면다시그림(int);
static Terminal_d413d4bc *Terminal_intrare;
static unsigned caracter_larg(unsigned cod_caracter){return cod_caracter>=256?2:1;}
static void 사각영역(unsigned coordonata_X,unsigned 세로좌표,unsigned 너비값,unsigned 높이값,unsigned 색상){
    Avizier_dreptunghi_umple(coordonata_X,세로좌표,너비값,높이값,색상);
}
void Terminal_glifă(unsigned coordonata_X,unsigned 세로좌표,unsigned cod_caracter,unsigned 전경색,unsigned 배경색){
    unsigned 너비=caracter_larg(cod_caracter)*8;if(cod_caracter==0xffffffffu)return;
    int 왼쪽=coordonata_X,위쪽=세로좌표,폭=너비,lungime_VALUE=16;
    if(!보드그림범위(&왼쪽,&위쪽,&폭,&lungime_VALUE))return;
    if(cod_caracter==' '){Avizier_dreptunghi_umple(왼쪽,위쪽,폭,lungime_VALUE,배경색);return;}
    unsigned LOOKUP_INDEX=cod_caracter<65536?cod_caracter:cod_caracter>=0x1f600&&cod_caracter<0x1f650?65536+cod_caracter-0x1f600:0xfffd;
    const unsigned char *font_VALUE=Terminal_font+LOOKUP_INDEX*32;
    for(int Linie=위쪽;Linie<위쪽+lungime_VALUE;Linie++){unsigned Serviciu_de_transfer_inteligent_în_fundal_Listă=font_VALUE[(Linie-세로좌표)*2]*256+font_VALUE[(Linie-세로좌표)*2+1];for(int 칸=왼쪽;칸<왼쪽+폭;칸++)Avizier_element_imagine(칸,Linie,(Serviciu_de_transfer_inteligent_în_fundal_Listă&(0x8000>>(칸-coordonata_X)))?전경색:배경색);}
}
static void nume_tabel(unsigned coordonata_X,unsigned 세로좌표,const char *șir_date,unsigned 전경색,unsigned 배경색){while(*șir_date){unsigned cod_caracter=(unsigned char)*șir_date++, 남은수=0;if(cod_caracter>=0xc0){남은수=cod_caracter<0xe0?1:cod_caracter<0xf0?2:3;cod_caracter&=(1u<<(6-남은수))-1;while(남은수--&&*șir_date)cod_caracter=(cod_caracter<<6)|((unsigned char)*șir_date++&63);}Terminal_glifă(coordonata_X,세로좌표,cod_caracter,전경색,배경색);coordonata_X+=caracter_larg(cod_caracter)*8;}}
static unsigned 첫항목(void){return Terminal_intrare->맨위;}
static int 보이는지(void){return Terminal_intrare->살아있음&&Focalizat>=0&&Terminal_intrare==&Windows_Listă[Focalizat]&&!화면보임(Focalizat);}
static void 그리기(unsigned ROW_poziție,unsigned COLUMN_poziție){
    if(!보이는지()||ROW_poziție<첫항목()-Terminal_intrare->밀어올리기||ROW_poziție>=첫항목()-Terminal_intrare->밀어올리기+Terminal_intrare->ROW_COUNT||COLUMN_poziție>=Terminal_intrare->COLUMNS)return;
    unsigned cod_caracter=Terminal_intrare->글자칸들[ROW_poziție%Istoric_linie_COUNT][COLUMN_poziție],șir_date=Terminal_intrare->모양들[ROW_poziție%Istoric_linie_COUNT][COLUMN_poziție];
    if(caracter_larg(cod_caracter)==2&&COLUMN_poziție+1>=Terminal_intrare->COLUMNS)cod_caracter=' ';
    Terminal_glifă(Terminal_intrare->coordonata_X+12+COLUMN_poziție*8,Terminal_intrare->세로좌표+36+(ROW_poziție-첫항목()+Terminal_intrare->밀어올리기)*16,cod_caracter?cod_caracter:' ',색상들[șir_date&15],색상들[șir_date>>4]);
}
static void cursor_text_VALUE(int afișa_fereastră){if(!보이는지()||Terminal_intrare->밀어올리기||Terminal_intrare->COLUMN_poziție>=Terminal_intrare->COLUMNS||Terminal_intrare->ROW_poziție<Terminal_intrare->맨위||Terminal_intrare->ROW_poziție>=Terminal_intrare->맨위+Terminal_intrare->ROW_COUNT)return;
    if(!afișa_fereastră||!Terminal_intrare->가리개보임)그리기(Terminal_intrare->ROW_poziție,Terminal_intrare->COLUMN_poziție);else 사각영역(Terminal_intrare->coordonata_X+12+Terminal_intrare->COLUMN_poziție*8,Terminal_intrare->세로좌표+36+(Terminal_intrare->ROW_poziție-Terminal_intrare->맨위)*16+14,8,2,색상들[Terminal_intrare->전경색]);}
static void Conținut_VALUE(void){
    사각영역(Terminal_intrare->coordonata_X+12,Terminal_intrare->세로좌표+36,Terminal_intrare->COLUMNS*8,Terminal_intrare->ROW_COUNT*16,색상들[0]);
    int 가로=Terminal_intrare->coordonata_X+12,Verticală_poziție=Terminal_intrare->세로좌표+36,폭=Terminal_intrare->COLUMNS*8,lungime_VALUE=Terminal_intrare->ROW_COUNT*16;
    if(보드그림범위(&가로,&Verticală_poziție,&폭,&lungime_VALUE)){
    unsigned 첫줄=(Verticală_poziție-Terminal_intrare->세로좌표-36)/16,끝줄=(Verticală_poziție+lungime_VALUE-Terminal_intrare->세로좌표-36+15)/16;
    unsigned 첫칸=(가로-Terminal_intrare->coordonata_X-12)/8,끝칸=(가로+폭-Terminal_intrare->coordonata_X-12+7)/8;
    if(첫칸)첫칸--; /* 잘림 경계 왼쪽에서 시작한 두 칸 글자도 그린다. */
    for(unsigned 반환값=첫줄;반환값<끝줄;반환값++)for(unsigned cod_caracter=첫칸;cod_caracter<끝칸;cod_caracter++){
        unsigned ROW_poziție=첫항목()-Terminal_intrare->밀어올리기+반환값,caracter_VALUE=Terminal_intrare->글자칸들[ROW_poziție%Istoric_linie_COUNT][cod_caracter],șir_date=Terminal_intrare->모양들[ROW_poziție%Istoric_linie_COUNT][cod_caracter];
        if(caracter_larg(caracter_VALUE)==2&&cod_caracter+1>=Terminal_intrare->COLUMNS)caracter_VALUE=' ';
        if((caracter_VALUE==0||caracter_VALUE==' ')&&(șir_date>>4)==0)continue;
        Terminal_glifă(Terminal_intrare->coordonata_X+12+cod_caracter*8,Terminal_intrare->세로좌표+36+반환값*16,caracter_VALUE?caracter_VALUE:' ',색상들[șir_date&15],색상들[șir_date>>4]);
    }}
    nume_tabel(Terminal_intrare->coordonata_X+12,Terminal_intrare->세로좌표+Terminal_intrare->높이-18,Terminal_intrare->밀어올리기?"PgDn: recent output":Terminal_intrare->너비>=500?"F6: next | Corner + left drag: resize":"Corner + left drag: resize",0xece8e2,0x403127);cursor_text_VALUE(1);
}
static void executare_cadru(int identificator_VALUE){
    Terminal_intrare=&Windows_Listă[identificator_VALUE];
    int 가로=Terminal_intrare->coordonata_X,Verticală_poziție=Terminal_intrare->세로좌표,폭=Terminal_intrare->너비,lungime_VALUE=Terminal_intrare->높이;
    if(!보드그림범위(&가로,&Verticală_poziție,&폭,&lungime_VALUE))return;
    사각영역(Terminal_intrare->coordonata_X,Terminal_intrare->세로좌표,Terminal_intrare->너비,Terminal_intrare->높이,0x403127);
    unsigned 색상=identificator_VALUE==Focalizat?0x905020:0x604438;사각영역(Terminal_intrare->coordonata_X,Terminal_intrare->세로좌표,Terminal_intrare->너비,30,색상);
    nume_tabel(Terminal_intrare->coordonata_X+12,Terminal_intrare->세로좌표+7,"JKOROS Terminal",0xffffff,색상);
    char 수치[2]={(char)('1'+identificator_VALUE),0};nume_tabel(Terminal_intrare->coordonata_X+148,Terminal_intrare->세로좌표+7,수치,0xffffff,색상);
    nume_tabel(Terminal_intrare->coordonata_X+240,Terminal_intrare->세로좌표+7,Terminal_intrare->너비>=500?(한글입력?"[RO] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[RO]":"[EN]"),0xffffff,색상);
    사각영역(Terminal_intrare->coordonata_X+Terminal_intrare->너비-32,Terminal_intrare->세로좌표+4,26,22,0x5555b8);nume_tabel(Terminal_intrare->coordonata_X+Terminal_intrare->너비-24,Terminal_intrare->세로좌표+7,"X",0xffffff,0x5555b8);
    Conținut_VALUE();
}
static void 장면그리기(void){
    if(!desktop_vizualiza)return;사각영역(0,0,보드화면너비(),보드화면높이(),0x302018);사각영역(0,0,보드화면너비(),32,0x403127);
    사각영역(6,4,136,24,0x905020);nume_tabel(14,8,"+ New terminal",0xffffff,0x905020);
    for(int 순번=0;순번<4;순번++)if(Windows_Listă[순번].살아있음){unsigned cod_caracter=Focalizat==순번?0x905020:0x604438;사각영역(154+순번*112,4,106,24,cod_caracter);nume_tabel(160+순번*112,8,"Terminal",0xffffff,cod_caracter);char șir_date[2]={(char)('1'+순번),0};nume_tabel(232+순번*112,8,șir_date,0xffffff,cod_caracter);}
    if(!intrare_COUNT)nume_tabel(140,210,"Click + New terminal to start",0xede9df,0x302018);
    for(int 순번=0;순번<intrare_COUNT;순번++)executare_cadru(ordine_VALUE[순번]);화면다시그림(Focalizat);Terminal_intrare=&Windows_Listă[출력결과];
}
static void Paint_regiune(int 가로,int Verticală_poziție,int 폭,int lungime_VALUE){
    if(!desktop_vizualiza||!보드그림범위(&가로,&Verticală_poziție,&폭,&lungime_VALUE))return;
    for(int Linie=Verticală_poziție;Linie<Verticală_poziție+lungime_VALUE;Linie+=32){
        int 띠높이=Verticală_poziție+lungime_VALUE-Linie;if(띠높이>32)띠높이=32;
        if(Avizier_buta_desen(가로,Linie,폭,띠높이)){장면그리기();Avizier_sfârșit_desen();}
    }
}
static void 다시그리기(void){Paint_regiune(0,0,보드화면너비(),보드화면높이());}
/* 서로 겹치지 않는 새 Fereastră 영역과 Anteriorul_element 자리의 네 띠를 복구한다. */
static void 창자리그리기(int 가로,int Verticală_poziție,int 폭,int lungime_VALUE,Terminal_d413d4bc *Fereastră){
    int 왼쪽=가로>(int)Fereastră->coordonata_X?가로:(int)Fereastră->coordonata_X;
    int 위쪽=Verticală_poziție>(int)Fereastră->세로좌표?Verticală_poziție:(int)Fereastră->세로좌표;
    int RIGHT=가로+폭<(int)(Fereastră->coordonata_X+Fereastră->너비)?가로+폭:(int)(Fereastră->coordonata_X+Fereastră->너비);
    int 아래쪽=Verticală_poziție+lungime_VALUE<(int)(Fereastră->세로좌표+Fereastră->높이)?Verticală_poziție+lungime_VALUE:(int)(Fereastră->세로좌표+Fereastră->높이);
    Paint_regiune(Fereastră->coordonata_X,Fereastră->세로좌표,Fereastră->너비,Fereastră->높이);
    if(왼쪽>=RIGHT||위쪽>=아래쪽){Paint_regiune(가로,Verticală_poziție,폭,lungime_VALUE);return;}
    Paint_regiune(가로,Verticală_poziție,폭,위쪽-Verticală_poziție);
    Paint_regiune(가로,아래쪽,폭,Verticală_poziție+lungime_VALUE-아래쪽);
    Paint_regiune(가로,위쪽,왼쪽-가로,아래쪽-위쪽);
    Paint_regiune(RIGHT,위쪽,가로+폭-RIGHT,아래쪽-위쪽);
}
static void semnal_Focalizat(void){sisteme_de_informații_în_așteptare=(sisteme_de_informații_în_așteptare&~15u)|(unsigned)(Focalizat+1)|0x10000;}
void 터미널입력방식(unsigned 한글여부){
    한글입력=한글여부!=0;
    /* Update title bars only: a mode switch must not erase an EL0 drawing. */
    if(Focalizat>=0){
        Terminal_d413d4bc *fereastră_intrare=&Windows_Listă[Focalizat];
        nume_tabel(fereastră_intrare->coordonata_X+240,fereastră_intrare->세로좌표+7,fereastră_intrare->너비>=500?(한글입력?"[RO] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[RO]":"[EN]"),0xffffff,0x905020);
    }
}
static void 앞으로올리기(int identificator_VALUE){if(identificator_VALUE<0||identificator_VALUE>=4||!Windows_Listă[identificator_VALUE].살아있음)return;int curent_poziție=0;while(curent_poziție<intrare_COUNT&&ordine_VALUE[curent_poziție]!=identificator_VALUE)curent_poziție++;for(;curent_poziție+1<intrare_COUNT;curent_poziție++)ordine_VALUE[curent_poziție]=ordine_VALUE[curent_poziție+1];ordine_VALUE[intrare_COUNT-1]=identificator_VALUE;Focalizat=identificator_VALUE;semnal_Focalizat();다시그리기();}
static void 빈칸채우기(unsigned ROW_poziție){for(unsigned cod_caracter=0;cod_caracter<최대열수;cod_caracter++){Terminal_intrare->글자칸들[ROW_poziție%Istoric_linie_COUNT][cod_caracter]=0;Terminal_intrare->모양들[ROW_poziție%Istoric_linie_COUNT][cod_caracter]=Terminal_intrare->전경색|(Terminal_intrare->배경색<<4);}}
static void goli_TOC(void){Terminal_intrare->ROW_poziție=Terminal_intrare->COLUMN_poziție=Terminal_intrare->맨위=Terminal_intrare->밀어올리기=0;for(unsigned 반환값=0;반환값<Istoric_linie_COUNT;반환값++)빈칸채우기(반환값);if(보이는지())Conținut_VALUE();}
static int crea_intrare(void){
    if(!보드화면기억공간())return -19;int identificator_VALUE=0;while(identificator_VALUE<4&&Windows_Listă[identificator_VALUE].살아있음)identificator_VALUE++;if(identificator_VALUE==4)return -28;
    desktop_vizualiza=1;Terminal_intrare=&Windows_Listă[identificator_VALUE];memset(Terminal_intrare,0,sizeof(*Terminal_intrare));Terminal_intrare->살아있음=1;Terminal_intrare->너비=568;Terminal_intrare->높이=360;Terminal_intrare->COLUMNS=68;Terminal_intrare->ROW_COUNT=19;Terminal_intrare->coordonata_X=12+identificator_VALUE*16;Terminal_intrare->세로좌표=48+identificator_VALUE*18;Terminal_intrare->전경색=7;Terminal_intrare->가리개보임=1;
    for(unsigned 반환값=0;반환값<Istoric_linie_COUNT;반환값++)빈칸채우기(반환값);ordine_VALUE[intrare_COUNT++]=identificator_VALUE;Focalizat=identificator_VALUE;sisteme_de_informații_în_așteptare|=1u<<(4+identificator_VALUE);semnal_Focalizat();다시그리기();return identificator_VALUE+1;
}
static void închide_fereastră(int identificator_VALUE){
    if(identificator_VALUE<0||identificator_VALUE>=4||!Windows_Listă[identificator_VALUE].살아있음)return;Windows_Listă[identificator_VALUE].살아있음=0;sisteme_de_informații_în_așteptare|=1u<<(8+identificator_VALUE);
    int curent_poziție=0;while(curent_poziție<intrare_COUNT&&ordine_VALUE[curent_poziție]!=identificator_VALUE)curent_poziție++;for(;curent_poziție+1<intrare_COUNT;curent_poziție++)ordine_VALUE[curent_poziție]=ordine_VALUE[curent_poziție+1];intrare_COUNT--;
    if(Focalizat==identificator_VALUE)Focalizat=intrare_COUNT?ordine_VALUE[intrare_COUNT-1]:-1;semnal_Focalizat();다시그리기();
}
static void 줄바꿈(void){Terminal_intrare->COLUMN_poziție=0;Terminal_intrare->ROW_poziție++;if(Terminal_intrare->ROW_poziție>=Terminal_intrare->맨위+Terminal_intrare->ROW_COUNT){Terminal_intrare->맨위++;빈칸채우기(Terminal_intrare->ROW_poziție);if(보이는지())Conținut_VALUE();}}
static void cod_caracter_451f2815(unsigned cod_caracter){
    if(cod_caracter==13){Terminal_intrare->COLUMN_poziție=0;return;}if(cod_caracter==10){줄바꿈();return;}if(cod_caracter==8){if(Terminal_intrare->COLUMN_poziție)Terminal_intrare->COLUMN_poziție--;return;}
    if(cod_caracter==9){unsigned element_COUNT=8-Terminal_intrare->COLUMN_poziție%8;while(element_COUNT--)cod_caracter_451f2815(' ');return;}if(cod_caracter<32||cod_caracter==127)return;
    unsigned 너비값=caracter_larg(cod_caracter);if(Terminal_intrare->COLUMN_poziție+너비값>Terminal_intrare->COLUMNS)줄바꿈();
    if(Terminal_intrare->글자칸들[Terminal_intrare->ROW_poziție%Istoric_linie_COUNT][Terminal_intrare->COLUMN_poziție]==0xffffffffu&&Terminal_intrare->COLUMN_poziție){Terminal_intrare->글자칸들[Terminal_intrare->ROW_poziție%Istoric_linie_COUNT][Terminal_intrare->COLUMN_poziție-1]=' ';그리기(Terminal_intrare->ROW_poziție,Terminal_intrare->COLUMN_poziție-1);}
    if(caracter_larg(Terminal_intrare->글자칸들[Terminal_intrare->ROW_poziție%Istoric_linie_COUNT][Terminal_intrare->COLUMN_poziție])==2&&Terminal_intrare->COLUMN_poziție+1<Terminal_intrare->COLUMNS){Terminal_intrare->글자칸들[Terminal_intrare->ROW_poziție%Istoric_linie_COUNT][Terminal_intrare->COLUMN_poziție+1]=' ';그리기(Terminal_intrare->ROW_poziție,Terminal_intrare->COLUMN_poziție+1);}
    Terminal_intrare->글자칸들[Terminal_intrare->ROW_poziție%Istoric_linie_COUNT][Terminal_intrare->COLUMN_poziție]=cod_caracter;Terminal_intrare->모양들[Terminal_intrare->ROW_poziție%Istoric_linie_COUNT][Terminal_intrare->COLUMN_poziție]=Terminal_intrare->전경색|(Terminal_intrare->배경색<<4);
    if(너비값==2)Terminal_intrare->글자칸들[Terminal_intrare->ROW_poziție%Istoric_linie_COUNT][Terminal_intrare->COLUMN_poziție+1]=0xffffffffu;
    그리기(Terminal_intrare->ROW_poziție,Terminal_intrare->COLUMN_poziție);Terminal_intrare->COLUMN_poziție+=너비값;
}
static void handle_control_SEQUENCE(unsigned cod_caracter){
    unsigned element_COUNT=Terminal_intrare->parametru_VALUE[0]?Terminal_intrare->parametru_VALUE[0]:1;
    if(cod_caracter=='m')for(unsigned 순번=0;순번<=Terminal_intrare->parametru_INDEX;순번++){unsigned date_poziție=Terminal_intrare->parametru_VALUE[순번];if(!date_poziție){Terminal_intrare->전경색=7;Terminal_intrare->배경색=0;}if(date_poziție==1&&Terminal_intrare->전경색<8)Terminal_intrare->전경색+=8;if(date_poziție==7){unsigned 유지=Terminal_intrare->전경색;Terminal_intrare->전경색=Terminal_intrare->배경색;Terminal_intrare->배경색=유지;}if(date_poziție>=30&&date_poziție<=37)Terminal_intrare->전경색=date_poziție-30;if(date_poziție>=90&&date_poziție<=97)Terminal_intrare->전경색=date_poziție-90+8;if(date_poziție>=40&&date_poziție<=47)Terminal_intrare->배경색=date_poziție-40;if(date_poziție>=100&&date_poziție<=107)Terminal_intrare->배경색=date_poziție-100+8;if(date_poziție==39)Terminal_intrare->전경색=7;if(date_poziție==49)Terminal_intrare->배경색=0;}
    if(cod_caracter=='J'&&(Terminal_intrare->parametru_VALUE[0]==2||Terminal_intrare->parametru_VALUE[0]==3))goli_TOC();
    if(cod_caracter=='K'){unsigned 출발위치=Terminal_intrare->parametru_VALUE[0]==2?0:Terminal_intrare->COLUMN_poziție,도착위치=Terminal_intrare->parametru_VALUE[0]==1?Terminal_intrare->COLUMN_poziție+1:Terminal_intrare->COLUMNS;if(Terminal_intrare->parametru_VALUE[0]==1)출발위치=0;for(unsigned 순번=출발위치;순번<도착위치&&순번<Terminal_intrare->COLUMNS;순번++){
        unsigned ROW_VALUE=Terminal_intrare->ROW_poziție%Istoric_linie_COUNT,caracter_VALUE=Terminal_intrare->글자칸들[ROW_VALUE][순번],formă_VALUE=Terminal_intrare->전경색|(Terminal_intrare->배경색<<4);
        /* 넓은 vi 화면에서도 이미 빈 칸의 font_VALUE 화소를 되풀이해 칠하지 않는다. */
        int 바뀜=(caracter_VALUE!=0&&caracter_VALUE!=' ')||Terminal_intrare->모양들[ROW_VALUE][순번]!=formă_VALUE;
        Terminal_intrare->글자칸들[ROW_VALUE][순번]=' ';Terminal_intrare->모양들[ROW_VALUE][순번]=formă_VALUE;
        if(바뀜)그리기(Terminal_intrare->ROW_poziție,순번);
    }}
    if(cod_caracter=='D')Terminal_intrare->COLUMN_poziție=element_COUNT>Terminal_intrare->COLUMN_poziție?0:Terminal_intrare->COLUMN_poziție-element_COUNT;if(cod_caracter=='C')Terminal_intrare->COLUMN_poziție=Terminal_intrare->COLUMN_poziție+element_COUNT>=Terminal_intrare->COLUMNS?Terminal_intrare->COLUMNS-1:Terminal_intrare->COLUMN_poziție+element_COUNT;
    if(cod_caracter=='G')Terminal_intrare->COLUMN_poziție=element_COUNT>Terminal_intrare->COLUMNS?Terminal_intrare->COLUMNS-1:element_COUNT-1;if(cod_caracter=='A')Terminal_intrare->ROW_poziție=element_COUNT>Terminal_intrare->ROW_poziție-Terminal_intrare->맨위?Terminal_intrare->맨위:Terminal_intrare->ROW_poziție-element_COUNT;
    if(cod_caracter=='B')Terminal_intrare->ROW_poziție=Terminal_intrare->ROW_poziție+element_COUNT>=Terminal_intrare->맨위+Terminal_intrare->ROW_COUNT?Terminal_intrare->맨위+Terminal_intrare->ROW_COUNT-1:Terminal_intrare->ROW_poziție+element_COUNT;
    if(cod_caracter=='H'||cod_caracter=='f'){Terminal_intrare->ROW_poziție=Terminal_intrare->맨위+(element_COUNT>Terminal_intrare->ROW_COUNT?Terminal_intrare->ROW_COUNT:element_COUNT)-1;unsigned coordonata_X=Terminal_intrare->parametru_VALUE[1]?Terminal_intrare->parametru_VALUE[1]:1;Terminal_intrare->COLUMN_poziție=(coordonata_X>Terminal_intrare->COLUMNS?Terminal_intrare->COLUMNS:coordonata_X)-1;}
    if(cod_caracter=='s'){Terminal_intrare->저장행=Terminal_intrare->ROW_poziție;Terminal_intrare->저장열=Terminal_intrare->COLUMN_poziție;}if(cod_caracter=='u'){Terminal_intrare->ROW_poziție=Terminal_intrare->저장행;Terminal_intrare->COLUMN_poziție=Terminal_intrare->저장열<Terminal_intrare->COLUMNS?Terminal_intrare->저장열:Terminal_intrare->COLUMNS-1;}
    if((cod_caracter=='h'||cod_caracter=='l')&&Terminal_intrare->parametru_VALUE[0]==25)Terminal_intrare->가리개보임=cod_caracter=='h';
}
void Terminal_byte(unsigned SECOND_VALUE){
    Terminal_intrare=&Windows_Listă[출력결과];if(!Terminal_intrare->살아있음)return;cursor_text_VALUE(0);if(Terminal_intrare->밀어올리기){Terminal_intrare->밀어올리기=0;if(보이는지())Conținut_VALUE();}
    if(Terminal_intrare->탈출상태==1){Terminal_intrare->탈출상태=SECOND_VALUE=='['?2:0;Terminal_intrare->parametru_INDEX=0;for(unsigned 순번=0;순번<4;순번++)Terminal_intrare->parametru_VALUE[순번]=0;}
    else if(Terminal_intrare->탈출상태==2){if(SECOND_VALUE=='?'){}else if(SECOND_VALUE>='0'&&SECOND_VALUE<='9'){if(Terminal_intrare->parametru_VALUE[Terminal_intrare->parametru_INDEX]<10000)Terminal_intrare->parametru_VALUE[Terminal_intrare->parametru_INDEX]=Terminal_intrare->parametru_VALUE[Terminal_intrare->parametru_INDEX]*10+SECOND_VALUE-'0';}else if(SECOND_VALUE==';'&&Terminal_intrare->parametru_INDEX<3)Terminal_intrare->parametru_INDEX++;else{handle_control_SEQUENCE(SECOND_VALUE);Terminal_intrare->탈출상태=0;}}
    else if(SECOND_VALUE==27){Terminal_intrare->긴부호없는값=0;Terminal_intrare->탈출상태=1;}else{
        if(Terminal_intrare->긴부호없는값&&(SECOND_VALUE&0xc0)!=0x80){Terminal_intrare->긴부호없는값=0;cod_caracter_451f2815(0xfffd);}
        if(Terminal_intrare->긴부호없는값){Terminal_intrare->부호없는결과=Terminal_intrare->부호없는결과*64+(SECOND_VALUE&63);if(--Terminal_intrare->긴부호없는값==0)cod_caracter_451f2815(Terminal_intrare->부호없는결과<Terminal_intrare->SMALL_VALUE||Terminal_intrare->부호없는결과>0x10ffff||(Terminal_intrare->부호없는결과>=0xd800&&Terminal_intrare->부호없는결과<=0xdfff)?0xfffd:Terminal_intrare->부호없는결과);}
        else if(SECOND_VALUE<128)cod_caracter_451f2815(SECOND_VALUE);else if(SECOND_VALUE>=0xc2&&SECOND_VALUE<=0xf4){Terminal_intrare->긴부호없는값=SECOND_VALUE<0xe0?1:SECOND_VALUE<0xf0?2:3;Terminal_intrare->부호없는결과=SECOND_VALUE&((1u<<(6-Terminal_intrare->긴부호없는값))-1);Terminal_intrare->SMALL_VALUE=Terminal_intrare->긴부호없는값==1?128:Terminal_intrare->긴부호없는값==2?2048:65536;}else cod_caracter_451f2815(0xfffd);
    }cursor_text_VALUE(1);
}
int Terminal_în_așteptare(void){return sisteme_de_informații_în_așteptare!=0;}
/* 모서리 INDEX: 1 좌상, 2 우상, 3 좌하, 4 우하. */
static int redimensiona_glisa=-1,잡은모서리,잡은가로,잡은세로,처음가로,처음세로,처음너비,처음높이;
static int 가리킨창(int 가로,int Verticală_poziție) {
    for(int SEQUENCE_VALUE=intrare_COUNT-1;SEQUENCE_VALUE>=0;SEQUENCE_VALUE--){
        int identificator_VALUE=ordine_VALUE[SEQUENCE_VALUE];Terminal_d413d4bc *Fereastră=&Windows_Listă[identificator_VALUE];
        if(가로>=(int)Fereastră->coordonata_X&&Verticală_poziție>=(int)Fereastră->세로좌표&&
           가로<(int)(Fereastră->coordonata_X+Fereastră->너비)&&Verticală_poziție<(int)(Fereastră->세로좌표+Fereastră->높이))return identificator_VALUE;
    }return -1;
}
static int 모서리찾기(int identificator_VALUE,int 가로,int Verticală_poziție) {
    if(identificator_VALUE<0)return 0;Terminal_d413d4bc *Fereastră=&Windows_Listă[identificator_VALUE];
    int 왼쪽=가로<(int)Fereastră->coordonata_X+8,RIGHT=가로>=(int)(Fereastră->coordonata_X+Fereastră->너비)-8;
    int 위쪽=Verticală_poziție<(int)Fereastră->세로좌표+8,아래쪽=Verticală_poziție>=(int)(Fereastră->세로좌표+Fereastră->높이)-8;
    return (왼쪽||RIGHT)&&(위쪽||아래쪽)?1+RIGHT+아래쪽*2:0;
}
static int separator_VALUE(int VALUE,int 최소,int 최대){return VALUE<최소?최소:VALUE>최대?최대:VALUE;}
static void muta_redimensiona(int 가로,int Verticală_poziție) {
    Terminal_d413d4bc *Fereastră=&Windows_Listă[redimensiona_glisa];int 왼쪽=처음가로,위쪽=처음세로,RIGHT=처음가로+처음너비,아래쪽=처음세로+처음높이;
    if(잡은모서리==1||잡은모서리==3)왼쪽=separator_VALUE(처음가로+가로-잡은가로,0,RIGHT-360);
    else RIGHT=separator_VALUE(처음가로+처음너비+가로-잡은가로,왼쪽+360,보드화면너비());
    if(잡은모서리<=2)위쪽=separator_VALUE(처음세로+Verticală_poziție-잡은세로,34,아래쪽-216);
    else 아래쪽=separator_VALUE(처음세로+처음높이+Verticală_poziție-잡은세로,위쪽+216,보드화면높이());
    unsigned COLUMNS=(RIGHT-왼쪽-24)/8,ROW_COUNT=(아래쪽-위쪽-56)/16;
    if(Fereastră->COLUMNS!=COLUMNS||Fereastră->ROW_COUNT!=ROW_COUNT){
        Fereastră->크기바뀜=1;Fereastră->COLUMNS=COLUMNS;Fereastră->ROW_COUNT=ROW_COUNT;
        if(Fereastră->COLUMN_poziție>=COLUMNS)Fereastră->COLUMN_poziție=COLUMNS-1;
        if(Fereastră->ROW_poziție>=Fereastră->맨위+ROW_COUNT)Fereastră->맨위=Fereastră->ROW_poziție-ROW_COUNT+1;
        unsigned 한도=Fereastră->맨위;if(한도>Istoric_linie_COUNT-ROW_COUNT)한도=Istoric_linie_COUNT-ROW_COUNT;
        if(Fereastră->밀어올리기>한도)Fereastră->밀어올리기=한도;
    }
    int 옛가로=Fereastră->coordonata_X,옛세로=Fereastră->세로좌표,옛폭=Fereastră->너비,옛길이=Fereastră->높이;
    if(옛가로==왼쪽&&옛세로==위쪽&&옛폭==RIGHT-왼쪽&&옛길이==아래쪽-위쪽)return;
    Fereastră->coordonata_X=왼쪽;Fereastră->세로좌표=위쪽;Fereastră->너비=RIGHT-왼쪽;Fereastră->높이=아래쪽-위쪽;
    창자리그리기(옛가로,옛세로,옛폭,옛길이,Fereastră);
}
void Terminal_cursor(unsigned Următorul_element,int coordonata_X,int 세로좌표){
    unsigned 눌림=Următorul_element&~단추들;단추들=Următorul_element;
    if(!desktop_vizualiza){glisa_VALUE=-1;redimensiona_glisa=-1;Avizier_cursor(coordonata_X,세로좌표,1);return;}
    if(!(Următorul_element&1)){glisa_VALUE=-1;redimensiona_glisa=-1;}
    if(redimensiona_glisa>=0&&!Windows_Listă[redimensiona_glisa].살아있음)redimensiona_glisa=-1;
    if(glisa_VALUE>=0&&!Windows_Listă[glisa_VALUE].살아있음)glisa_VALUE=-1;
    if(redimensiona_glisa>=0){
        muta_redimensiona(coordonata_X,세로좌표);Avizier_cursor(coordonata_X,세로좌표,잡은모서리==1||잡은모서리==4?2:3);return;
    }
    Avizier_cursor(coordonata_X,세로좌표,1);
    if(glisa_VALUE>=0){
        Terminal_d413d4bc *Fereastră=&Windows_Listă[glisa_VALUE];
        int 옛가로=Fereastră->coordonata_X,옛세로=Fereastră->세로좌표;
        Fereastră->coordonata_X=separator_VALUE(coordonata_X-glisa_X,0,보드화면너비()-Fereastră->너비);
        Fereastră->세로좌표=separator_VALUE(세로좌표-glisa_Y,34,보드화면높이()-Fereastră->높이);
        if(옛가로!=(int)Fereastră->coordonata_X||옛세로!=(int)Fereastră->세로좌표)창자리그리기(옛가로,옛세로,Fereastră->너비,Fereastră->높이,Fereastră);
        return;
    }
    extern int 화면덮음(int,int,int);
    if(화면덮음(Focalizat,coordonata_X,세로좌표)){화면가리킴(Focalizat,눌림,coordonata_X,세로좌표);return;}
    int identificator_VALUE=가리킨창(coordonata_X,세로좌표),모서리=모서리찾기(identificator_VALUE,coordonata_X,세로좌표);
    if(모서리)Avizier_cursor(coordonata_X,세로좌표,모서리==1||모서리==4?2:3);
    if(눌림&1){
        if(모서리){
            Terminal_d413d4bc *Fereastră=&Windows_Listă[identificator_VALUE];redimensiona_glisa=identificator_VALUE;잡은모서리=모서리;잡은가로=coordonata_X;잡은세로=세로좌표;
            처음가로=Fereastră->coordonata_X;처음세로=Fereastră->세로좌표;처음너비=Fereastră->너비;처음높이=Fereastră->높이;
            if(identificator_VALUE!=Focalizat)앞으로올리기(identificator_VALUE);return;
        }
        if(세로좌표<32&&coordonata_X>=6&&coordonata_X<142){crea_intrare();return;}
        if(세로좌표<32&&coordonata_X>=154&&coordonata_X<602){앞으로올리기((coordonata_X-154)/112);return;}
        if(identificator_VALUE>=0){
            Terminal_d413d4bc *Fereastră=&Windows_Listă[identificator_VALUE];
            if(세로좌표<(int)Fereastră->세로좌표+30&&coordonata_X>=(int)(Fereastră->coordonata_X+Fereastră->너비)-32){închide_fereastră(identificator_VALUE);return;}
            if(identificator_VALUE!=Focalizat)앞으로올리기(identificator_VALUE);
            if(세로좌표<(int)Fereastră->세로좌표+30){glisa_VALUE=identificator_VALUE;glisa_X=coordonata_X-Fereastră->coordonata_X;glisa_Y=세로좌표-Fereastră->세로좌표;}return;
        }
    }
    if(Focalizat>=0&&(눌림&(8|16))){Terminal_intrare=&Windows_Listă[Focalizat];if(눌림&8){unsigned 한도=Terminal_intrare->맨위;if(한도>Istoric_linie_COUNT-Terminal_intrare->ROW_COUNT)한도=Istoric_linie_COUNT-Terminal_intrare->ROW_COUNT;Terminal_intrare->밀어올리기=Terminal_intrare->밀어올리기+9>한도?한도:Terminal_intrare->밀어올리기+9;}else Terminal_intrare->밀어올리기=Terminal_intrare->밀어올리기<9?0:Terminal_intrare->밀어올리기-9;다시그리기();}
}
void 터미널바로가기키(unsigned 누름값){if(누름값==1)crea_intrare();if(누름값==2&&intrare_COUNT)앞으로올리기(ordine_VALUE[0]);if(누름값==3)închide_fereastră(Focalizat);}
mașină_Word Avizier_Terminal(mașină_Word Acțiuni){
    if(Acțiuni==300){if(!Windows_Listă[출력결과].살아있음)return crea_intrare();desktop_vizualiza=1;다시그리기();return 0;}
    if(Acțiuni==0){închide_fereastră(Focalizat);return 0;}if(Acțiuni==1)return (uint32_t)crea_intrare();if(Acțiuni==2)return Focalizat>=0;
    if(Acțiuni==9){desktop_vizualiza=0;return 0;}if(Acțiuni==7)return intrare_COUNT;if(Acțiuni==10)return Focalizat+1;if(Acțiuni==11)return 출력결과;
    if(Acțiuni==13){Terminal_d413d4bc *Fereastră=&Windows_Listă[출력결과];return Fereastră->살아있음?(Fereastră->ROW_COUNT<<16)|Fereastră->COLUMNS:(19<<16)|68;}
    if(Acțiuni==14){unsigned VALUE=Windows_Listă[출력결과].크기바뀜;Windows_Listă[출력결과].크기바뀜=0;return VALUE;}
    if(Acțiuni==12){unsigned VALUE=sisteme_de_informații_în_așteptare;sisteme_de_informații_în_așteptare=0;return VALUE;}
    if(Acțiuni>=20&&Acțiuni<24)return Windows_Listă[Acțiuni-20].살아있음;
    if(Acțiuni>=100&&Acțiuni<104){출력결과=Acțiuni-100;Terminal_intrare=&Windows_Listă[출력결과];return 0;}
    if(Acțiuni>=200&&Acțiuni<204){앞으로올리기(Acțiuni-200);return 0;}
    if(Acțiuni==3){다시그리기();return 0;}Terminal_intrare=&Windows_Listă[출력결과];if(!Terminal_intrare->살아있음)return 0;
    if(Acțiuni==4)goli_TOC();if(Acțiuni==5||Acțiuni==6){unsigned Anteriorul_element=단추들;Terminal_cursor(Acțiuni==5?8:16,0,0);단추들=Anteriorul_element;}return 1;
}
