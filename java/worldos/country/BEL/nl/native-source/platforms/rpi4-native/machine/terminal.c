#include "../명명/기계연결이름.h"
#include "scherm_info.h"
/* Eigen 네 Venster 합성과 UTF-8 terminal. 바뀐 영역의 Voltooid_WAARDE 그림만 표시한다. */
#include <stdint.h>
#include <stddef.h>
typedef uintptr_t machine_Word;
extern machine_Word Bord_pixel(machine_Word,machine_Word,machine_Word),보드화면기억공간(void);
extern void *memset(void *,int,size_t);
extern const unsigned char Terminal_lettertype[];
#define 최대열수 237
#define Geschiedenis_lijn_AANTAL 160
typedef struct {
    uint32_t 글자칸들[Geschiedenis_lijn_AANTAL][최대열수]; uint8_t 모양들[Geschiedenis_lijn_AANTAL][최대열수];
    unsigned 너비,hoogte_WAARDE,KOLOMMEN,RIJ_AANTAL,크기바뀜;
    unsigned 살아있음,x_coördinaat,Y_coördinaat,RIJ_functie,KOLOM_functie,맨위,schuiven,전경색,배경색,탈출상태,parameter_WAARDE[4],parameter_INDEX,저장행,저장열;
    unsigned 부호없는결과,긴부호없는값,KLEINSTE_WAARDE,대체화면,가리개보임;
} Terminal;
static Terminal Windows_Lijst[4];
static int Focus=-1,uitvoer,order_WAARDE[4],invoer_AANTAL_8f7753a1,slepen_WAARDE=-1,slepen_X,slepen_Y;
static unsigned informatie_In_behandeling,단추들,pc_Weergave,한글입력;
static const uint32_t 색상들[16]={0x201a15,0x6060df,0x9dcc86,0x80cfea,0xefaf72,0xca96c9,0xceda76,0xede9df,0x858078,0x8888ff,0xb9eba7,0xa5eaff,0xffcc99,0xf0bef1,0xf0f0a0,0xffffff};
extern int 화면보임(int),scherm_wijzer(int,unsigned,int,int);
extern void 화면다시그림(int);
static Terminal *Terminal_invoer;
static unsigned breed_teken(unsigned codepoint){return codepoint>=256?2:1;}
static void 사각영역(unsigned x_coördinaat,unsigned Y_coördinaat,unsigned 너비값,unsigned aangevraagd_hoogte_WAARDE,unsigned 색상){
    Bord_rechthoek_vullen(x_coördinaat,Y_coördinaat,너비값,aangevraagd_hoogte_WAARDE,색상);
}
void Terminal_symbool(unsigned x_coördinaat,unsigned Y_coördinaat,unsigned codepoint,unsigned 전경색,unsigned 배경색){
    unsigned 너비=breed_teken(codepoint)*8;if(codepoint==0xffffffffu)return;
    int 왼쪽=x_coördinaat,위쪽=Y_coördinaat,폭=너비,tijdsduur_WAARDE=16;
    if(!보드그림범위(&왼쪽,&위쪽,&폭,&tijdsduur_WAARDE))return;
    if(codepoint==' '){Bord_rechthoek_vullen(왼쪽,위쪽,폭,tijdsduur_WAARDE,배경색);return;}
    unsigned ZOEKEN_INDEX=codepoint<65536?codepoint:codepoint>=0x1f600&&codepoint<0x1f650?65536+codepoint-0x1f600:0xfffd;
    const unsigned char *lettertype_WAARDE=Terminal_lettertype+ZOEKEN_INDEX*32;
    for(int invoerregel=위쪽;invoerregel<위쪽+tijdsduur_WAARDE;invoerregel++){unsigned BITS_Lijst=lettertype_WAARDE[(invoerregel-Y_coördinaat)*2]*256+lettertype_WAARDE[(invoerregel-Y_coördinaat)*2+1];for(int sleuf_invoer=왼쪽;sleuf_invoer<왼쪽+폭;sleuf_invoer++)Bord_pixel(sleuf_invoer,invoerregel,(BITS_Lijst&(0x8000>>(sleuf_invoer-x_coördinaat)))?전경색:배경색);}
}
static void naam_tabel(unsigned x_coördinaat,unsigned Y_coördinaat,const char *tekenreeks_gegevens,unsigned 전경색,unsigned 배경색){while(*tekenreeks_gegevens){unsigned codepoint=(unsigned char)*tekenreeks_gegevens++, 남은수=0;if(codepoint>=0xc0){남은수=codepoint<0xe0?1:codepoint<0xf0?2:3;codepoint&=(1u<<(6-남은수))-1;while(남은수--&&*tekenreeks_gegevens)codepoint=(codepoint<<6)|((unsigned char)*tekenreeks_gegevens++&63);}Terminal_symbool(x_coördinaat,Y_coördinaat,codepoint,전경색,배경색);x_coördinaat+=breed_teken(codepoint)*8;}}
static unsigned 첫항목(void){return Terminal_invoer->맨위;}
static int 보이는지(void){return Terminal_invoer->살아있음&&Focus>=0&&Terminal_invoer==&Windows_Lijst[Focus]&&!화면보임(Focus);}
static void Paint_scherm(unsigned RIJ_functie,unsigned KOLOM_functie){
    if(!보이는지()||RIJ_functie<첫항목()-Terminal_invoer->schuiven||RIJ_functie>=첫항목()-Terminal_invoer->schuiven+Terminal_invoer->RIJ_AANTAL||KOLOM_functie>=Terminal_invoer->KOLOMMEN)return;
    unsigned codepoint=Terminal_invoer->글자칸들[RIJ_functie%Geschiedenis_lijn_AANTAL][KOLOM_functie],tekenreeks_gegevens=Terminal_invoer->모양들[RIJ_functie%Geschiedenis_lijn_AANTAL][KOLOM_functie];
    if(breed_teken(codepoint)==2&&KOLOM_functie+1>=Terminal_invoer->KOLOMMEN)codepoint=' ';
    Terminal_symbool(Terminal_invoer->x_coördinaat+12+KOLOM_functie*8,Terminal_invoer->Y_coördinaat+36+(RIJ_functie-첫항목()+Terminal_invoer->schuiven)*16,codepoint?codepoint:' ',색상들[tekenreeks_gegevens&15],색상들[tekenreeks_gegevens>>4]);
}
static void caret_teken_WAARDE(int weergeven_venster){if(!보이는지()||Terminal_invoer->schuiven||Terminal_invoer->KOLOM_functie>=Terminal_invoer->KOLOMMEN||Terminal_invoer->RIJ_functie<Terminal_invoer->맨위||Terminal_invoer->RIJ_functie>=Terminal_invoer->맨위+Terminal_invoer->RIJ_AANTAL)return;
    if(!weergeven_venster||!Terminal_invoer->가리개보임)Paint_scherm(Terminal_invoer->RIJ_functie,Terminal_invoer->KOLOM_functie);else 사각영역(Terminal_invoer->x_coördinaat+12+Terminal_invoer->KOLOM_functie*8,Terminal_invoer->Y_coördinaat+36+(Terminal_invoer->RIJ_functie-Terminal_invoer->맨위)*16+14,8,2,색상들[Terminal_invoer->전경색]);}
static void Inhoud_WAARDE(void){
    사각영역(Terminal_invoer->x_coördinaat+12,Terminal_invoer->Y_coördinaat+36,Terminal_invoer->KOLOMMEN*8,Terminal_invoer->RIJ_AANTAL*16,색상들[0]);
    int 가로=Terminal_invoer->x_coördinaat+12,Verticaal_functie=Terminal_invoer->Y_coördinaat+36,폭=Terminal_invoer->KOLOMMEN*8,tijdsduur_WAARDE=Terminal_invoer->RIJ_AANTAL*16;
    if(보드그림범위(&가로,&Verticaal_functie,&폭,&tijdsduur_WAARDE)){
    unsigned 첫줄=(Verticaal_functie-Terminal_invoer->Y_coördinaat-36)/16,끝줄=(Verticaal_functie+tijdsduur_WAARDE-Terminal_invoer->Y_coördinaat-36+15)/16;
    unsigned 첫칸=(가로-Terminal_invoer->x_coördinaat-12)/8,끝칸=(가로+폭-Terminal_invoer->x_coördinaat-12+7)/8;
    if(첫칸)첫칸--; /* 잘림 grens_WAARDE 왼쪽에서 시작한 두 sleuf_invoer 글자도 그린다. */
    for(unsigned 반환값=첫줄;반환값<끝줄;반환값++)for(unsigned codepoint=첫칸;codepoint<끝칸;codepoint++){
        unsigned RIJ_functie=첫항목()-Terminal_invoer->schuiven+반환값,teken_WAARDE=Terminal_invoer->글자칸들[RIJ_functie%Geschiedenis_lijn_AANTAL][codepoint],tekenreeks_gegevens=Terminal_invoer->모양들[RIJ_functie%Geschiedenis_lijn_AANTAL][codepoint];
        if(breed_teken(teken_WAARDE)==2&&codepoint+1>=Terminal_invoer->KOLOMMEN)teken_WAARDE=' ';
        if((teken_WAARDE==0||teken_WAARDE==' ')&&(tekenreeks_gegevens>>4)==0)continue;
        Terminal_symbool(Terminal_invoer->x_coördinaat+12+codepoint*8,Terminal_invoer->Y_coördinaat+36+반환값*16,teken_WAARDE?teken_WAARDE:' ',색상들[tekenreeks_gegevens&15],색상들[tekenreeks_gegevens>>4]);
    }}
    naam_tabel(Terminal_invoer->x_coördinaat+12,Terminal_invoer->Y_coördinaat+Terminal_invoer->hoogte_WAARDE-18,Terminal_invoer->schuiven?"PgDn: recent output":Terminal_invoer->너비>=500?"F6: next | Corner + left drag: resize":"Corner + left drag: resize",0xece8e2,0x403127);caret_teken_WAARDE(1);
}
static void uitvoerbewerking_frame(int id_WAARDE){
    Terminal_invoer=&Windows_Lijst[id_WAARDE];
    int 가로=Terminal_invoer->x_coördinaat,Verticaal_functie=Terminal_invoer->Y_coördinaat,폭=Terminal_invoer->너비,tijdsduur_WAARDE=Terminal_invoer->hoogte_WAARDE;
    if(!보드그림범위(&가로,&Verticaal_functie,&폭,&tijdsduur_WAARDE))return;
    사각영역(Terminal_invoer->x_coördinaat,Terminal_invoer->Y_coördinaat,Terminal_invoer->너비,Terminal_invoer->hoogte_WAARDE,0x403127);
    unsigned 색상=id_WAARDE==Focus?0x905020:0x604438;사각영역(Terminal_invoer->x_coördinaat,Terminal_invoer->Y_coördinaat,Terminal_invoer->너비,30,색상);
    naam_tabel(Terminal_invoer->x_coördinaat+12,Terminal_invoer->Y_coördinaat+7,"JKOROS Terminal",0xffffff,색상);
    char 수치[2]={(char)('1'+id_WAARDE),0};naam_tabel(Terminal_invoer->x_coördinaat+148,Terminal_invoer->Y_coördinaat+7,수치,0xffffff,색상);
    naam_tabel(Terminal_invoer->x_coördinaat+240,Terminal_invoer->Y_coördinaat+7,Terminal_invoer->너비>=500?(한글입력?"[NL] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[NL]":"[EN]"),0xffffff,색상);
    사각영역(Terminal_invoer->x_coördinaat+Terminal_invoer->너비-32,Terminal_invoer->Y_coördinaat+4,26,22,0x5555b8);naam_tabel(Terminal_invoer->x_coördinaat+Terminal_invoer->너비-24,Terminal_invoer->Y_coördinaat+7,"X",0xffffff,0x5555b8);
    Inhoud_WAARDE();
}
static void Tekenen_thema(void){
    if(!pc_Weergave)return;사각영역(0,0,보드화면너비(),Bord_scherm_hoogte(),0x302018);사각영역(0,0,보드화면너비(),32,0x403127);
    사각영역(6,4,136,24,0x905020);naam_tabel(14,8,"+ New terminal",0xffffff,0x905020);
    for(int 순번=0;순번<4;순번++)if(Windows_Lijst[순번].살아있음){unsigned codepoint=Focus==순번?0x905020:0x604438;사각영역(154+순번*112,4,106,24,codepoint);naam_tabel(160+순번*112,8,"Terminal",0xffffff,codepoint);char tekenreeks_gegevens[2]={(char)('1'+순번),0};naam_tabel(232+순번*112,8,tekenreeks_gegevens,0xffffff,codepoint);}
    if(!invoer_AANTAL_8f7753a1)naam_tabel(140,210,"Click + New terminal to start",0xede9df,0x302018);
    for(int 순번=0;순번<invoer_AANTAL_8f7753a1;순번++)uitvoerbewerking_frame(order_WAARDE[순번]);화면다시그림(Focus);Terminal_invoer=&Windows_Lijst[uitvoer];
}
static void Paint_regio(int 가로,int Verticaal_functie,int 폭,int tijdsduur_WAARDE){
    if(!pc_Weergave||!보드그림범위(&가로,&Verticaal_functie,&폭,&tijdsduur_WAARDE))return;
    for(int invoerregel=Verticaal_functie;invoerregel<Verticaal_functie+tijdsduur_WAARDE;invoerregel+=32){
        int band_hoogte=Verticaal_functie+tijdsduur_WAARDE-invoerregel;if(band_hoogte>32)band_hoogte=32;
        if(Bord_START_tekening(가로,invoerregel,폭,band_hoogte)){Tekenen_thema();Bord_Voltooien_tekening();}
    }
}
static void 다시그리기(void){Paint_regio(0,0,보드화면너비(),Bord_scherm_hoogte());}
/* 서로 겹치지 않는 새 Venster 영역과 Vorige_item 자리의 네 띠를 복구한다. */
static void 창자리그리기(int 가로,int Verticaal_functie,int 폭,int tijdsduur_WAARDE,Terminal *Venster){
    int 왼쪽=가로>(int)Venster->x_coördinaat?가로:(int)Venster->x_coördinaat;
    int 위쪽=Verticaal_functie>(int)Venster->Y_coördinaat?Verticaal_functie:(int)Venster->Y_coördinaat;
    int recht=가로+폭<(int)(Venster->x_coördinaat+Venster->너비)?가로+폭:(int)(Venster->x_coördinaat+Venster->너비);
    int 아래쪽=Verticaal_functie+tijdsduur_WAARDE<(int)(Venster->Y_coördinaat+Venster->hoogte_WAARDE)?Verticaal_functie+tijdsduur_WAARDE:(int)(Venster->Y_coördinaat+Venster->hoogte_WAARDE);
    Paint_regio(Venster->x_coördinaat,Venster->Y_coördinaat,Venster->너비,Venster->hoogte_WAARDE);
    if(왼쪽>=recht||위쪽>=아래쪽){Paint_regio(가로,Verticaal_functie,폭,tijdsduur_WAARDE);return;}
    Paint_regio(가로,Verticaal_functie,폭,위쪽-Verticaal_functie);
    Paint_regio(가로,아래쪽,폭,Verticaal_functie+tijdsduur_WAARDE-아래쪽);
    Paint_regio(가로,위쪽,왼쪽-가로,아래쪽-위쪽);
    Paint_regio(recht,위쪽,가로+폭-recht,아래쪽-위쪽);
}
static void signaal_Focus(void){informatie_In_behandeling=(informatie_In_behandeling&~15u)|(unsigned)(Focus+1)|0x10000;}
void Terminal_invoer_MODUS(unsigned 한글여부){
    한글입력=한글여부!=0;
    /* Update title bars only: a mode switch must not erase an EL0 drawing. */
    if(Focus>=0){
        Terminal *venster_invoer=&Windows_Lijst[Focus];
        naam_tabel(venster_invoer->x_coördinaat+240,venster_invoer->Y_coördinaat+7,venster_invoer->너비>=500?(한글입력?"[NL] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[NL]":"[EN]"),0xffffff,0x905020);
    }
}
static void 앞으로올리기(int id_WAARDE){if(id_WAARDE<0||id_WAARDE>=4||!Windows_Lijst[id_WAARDE].살아있음)return;int actueel_functie=0;while(actueel_functie<invoer_AANTAL_8f7753a1&&order_WAARDE[actueel_functie]!=id_WAARDE)actueel_functie++;for(;actueel_functie+1<invoer_AANTAL_8f7753a1;actueel_functie++)order_WAARDE[actueel_functie]=order_WAARDE[actueel_functie+1];order_WAARDE[invoer_AANTAL_8f7753a1-1]=id_WAARDE;Focus=id_WAARDE;signaal_Focus();다시그리기();}
static void spatie(unsigned RIJ_functie){for(unsigned codepoint=0;codepoint<최대열수;codepoint++){Terminal_invoer->글자칸들[RIJ_functie%Geschiedenis_lijn_AANTAL][codepoint]=0;Terminal_invoer->모양들[RIJ_functie%Geschiedenis_lijn_AANTAL][codepoint]=Terminal_invoer->전경색|(Terminal_invoer->배경색<<4);}}
static void wissen_Inhoud(void){Terminal_invoer->RIJ_functie=Terminal_invoer->KOLOM_functie=Terminal_invoer->맨위=Terminal_invoer->schuiven=0;for(unsigned 반환값=0;반환값<Geschiedenis_lijn_AANTAL;반환값++)spatie(반환값);if(보이는지())Inhoud_WAARDE();}
static int maken_invoer(void){
    if(!보드화면기억공간())return -19;int id_WAARDE=0;while(id_WAARDE<4&&Windows_Lijst[id_WAARDE].살아있음)id_WAARDE++;if(id_WAARDE==4)return -28;
    pc_Weergave=1;Terminal_invoer=&Windows_Lijst[id_WAARDE];memset(Terminal_invoer,0,sizeof(*Terminal_invoer));Terminal_invoer->살아있음=1;Terminal_invoer->너비=568;Terminal_invoer->hoogte_WAARDE=360;Terminal_invoer->KOLOMMEN=68;Terminal_invoer->RIJ_AANTAL=19;Terminal_invoer->x_coördinaat=12+id_WAARDE*16;Terminal_invoer->Y_coördinaat=48+id_WAARDE*18;Terminal_invoer->전경색=7;Terminal_invoer->가리개보임=1;
    for(unsigned 반환값=0;반환값<Geschiedenis_lijn_AANTAL;반환값++)spatie(반환값);order_WAARDE[invoer_AANTAL_8f7753a1++]=id_WAARDE;Focus=id_WAARDE;informatie_In_behandeling|=1u<<(4+id_WAARDE);signaal_Focus();다시그리기();return id_WAARDE+1;
}
static void Sluiten_venster(int id_WAARDE){
    if(id_WAARDE<0||id_WAARDE>=4||!Windows_Lijst[id_WAARDE].살아있음)return;Windows_Lijst[id_WAARDE].살아있음=0;informatie_In_behandeling|=1u<<(8+id_WAARDE);
    int actueel_functie=0;while(actueel_functie<invoer_AANTAL_8f7753a1&&order_WAARDE[actueel_functie]!=id_WAARDE)actueel_functie++;for(;actueel_functie+1<invoer_AANTAL_8f7753a1;actueel_functie++)order_WAARDE[actueel_functie]=order_WAARDE[actueel_functie+1];invoer_AANTAL_8f7753a1--;
    if(Focus==id_WAARDE)Focus=invoer_AANTAL_8f7753a1?order_WAARDE[invoer_AANTAL_8f7753a1-1]:-1;signaal_Focus();다시그리기();
}
static void 줄바꿈(void){Terminal_invoer->KOLOM_functie=0;Terminal_invoer->RIJ_functie++;if(Terminal_invoer->RIJ_functie>=Terminal_invoer->맨위+Terminal_invoer->RIJ_AANTAL){Terminal_invoer->맨위++;spatie(Terminal_invoer->RIJ_functie);if(보이는지())Inhoud_WAARDE();}}
static void codepoint_451f2815(unsigned codepoint){
    if(codepoint==13){Terminal_invoer->KOLOM_functie=0;return;}if(codepoint==10){줄바꿈();return;}if(codepoint==8){if(Terminal_invoer->KOLOM_functie)Terminal_invoer->KOLOM_functie--;return;}
    if(codepoint==9){unsigned item_AANTAL=8-Terminal_invoer->KOLOM_functie%8;while(item_AANTAL--)codepoint_451f2815(' ');return;}if(codepoint<32||codepoint==127)return;
    unsigned 너비값=breed_teken(codepoint);if(Terminal_invoer->KOLOM_functie+너비값>Terminal_invoer->KOLOMMEN)줄바꿈();
    if(Terminal_invoer->글자칸들[Terminal_invoer->RIJ_functie%Geschiedenis_lijn_AANTAL][Terminal_invoer->KOLOM_functie]==0xffffffffu&&Terminal_invoer->KOLOM_functie){Terminal_invoer->글자칸들[Terminal_invoer->RIJ_functie%Geschiedenis_lijn_AANTAL][Terminal_invoer->KOLOM_functie-1]=' ';Paint_scherm(Terminal_invoer->RIJ_functie,Terminal_invoer->KOLOM_functie-1);}
    if(breed_teken(Terminal_invoer->글자칸들[Terminal_invoer->RIJ_functie%Geschiedenis_lijn_AANTAL][Terminal_invoer->KOLOM_functie])==2&&Terminal_invoer->KOLOM_functie+1<Terminal_invoer->KOLOMMEN){Terminal_invoer->글자칸들[Terminal_invoer->RIJ_functie%Geschiedenis_lijn_AANTAL][Terminal_invoer->KOLOM_functie+1]=' ';Paint_scherm(Terminal_invoer->RIJ_functie,Terminal_invoer->KOLOM_functie+1);}
    Terminal_invoer->글자칸들[Terminal_invoer->RIJ_functie%Geschiedenis_lijn_AANTAL][Terminal_invoer->KOLOM_functie]=codepoint;Terminal_invoer->모양들[Terminal_invoer->RIJ_functie%Geschiedenis_lijn_AANTAL][Terminal_invoer->KOLOM_functie]=Terminal_invoer->전경색|(Terminal_invoer->배경색<<4);
    if(너비값==2)Terminal_invoer->글자칸들[Terminal_invoer->RIJ_functie%Geschiedenis_lijn_AANTAL][Terminal_invoer->KOLOM_functie+1]=0xffffffffu;
    Paint_scherm(Terminal_invoer->RIJ_functie,Terminal_invoer->KOLOM_functie);Terminal_invoer->KOLOM_functie+=너비값;
}
static void greep_controle_REEKS(unsigned codepoint){
    unsigned item_AANTAL=Terminal_invoer->parameter_WAARDE[0]?Terminal_invoer->parameter_WAARDE[0]:1;
    if(codepoint=='m')for(unsigned 순번=0;순번<=Terminal_invoer->parameter_INDEX;순번++){unsigned gegevens_functie=Terminal_invoer->parameter_WAARDE[순번];if(!gegevens_functie){Terminal_invoer->전경색=7;Terminal_invoer->배경색=0;}if(gegevens_functie==1&&Terminal_invoer->전경색<8)Terminal_invoer->전경색+=8;if(gegevens_functie==7){unsigned behouden_WAARDE=Terminal_invoer->전경색;Terminal_invoer->전경색=Terminal_invoer->배경색;Terminal_invoer->배경색=behouden_WAARDE;}if(gegevens_functie>=30&&gegevens_functie<=37)Terminal_invoer->전경색=gegevens_functie-30;if(gegevens_functie>=90&&gegevens_functie<=97)Terminal_invoer->전경색=gegevens_functie-90+8;if(gegevens_functie>=40&&gegevens_functie<=47)Terminal_invoer->배경색=gegevens_functie-40;if(gegevens_functie>=100&&gegevens_functie<=107)Terminal_invoer->배경색=gegevens_functie-100+8;if(gegevens_functie==39)Terminal_invoer->전경색=7;if(gegevens_functie==49)Terminal_invoer->배경색=0;}
    if(codepoint=='J'&&(Terminal_invoer->parameter_WAARDE[0]==2||Terminal_invoer->parameter_WAARDE[0]==3))wissen_Inhoud();
    if(codepoint=='K'){unsigned 출발위치=Terminal_invoer->parameter_WAARDE[0]==2?0:Terminal_invoer->KOLOM_functie,도착위치=Terminal_invoer->parameter_WAARDE[0]==1?Terminal_invoer->KOLOM_functie+1:Terminal_invoer->KOLOMMEN;if(Terminal_invoer->parameter_WAARDE[0]==1)출발위치=0;for(unsigned 순번=출발위치;순번<도착위치&&순번<Terminal_invoer->KOLOMMEN;순번++){
        unsigned RIJ_WAARDE=Terminal_invoer->RIJ_functie%Geschiedenis_lijn_AANTAL,teken_WAARDE=Terminal_invoer->글자칸들[RIJ_WAARDE][순번],vorm_WAARDE=Terminal_invoer->전경색|(Terminal_invoer->배경색<<4);
        /* 넓은 vi 화면에서도 이미 빈 칸의 lettertype_WAARDE 화소를 되풀이해 칠하지 않는다. */
        int 바뀜=(teken_WAARDE!=0&&teken_WAARDE!=' ')||Terminal_invoer->모양들[RIJ_WAARDE][순번]!=vorm_WAARDE;
        Terminal_invoer->글자칸들[RIJ_WAARDE][순번]=' ';Terminal_invoer->모양들[RIJ_WAARDE][순번]=vorm_WAARDE;
        if(바뀜)Paint_scherm(Terminal_invoer->RIJ_functie,순번);
    }}
    if(codepoint=='D')Terminal_invoer->KOLOM_functie=item_AANTAL>Terminal_invoer->KOLOM_functie?0:Terminal_invoer->KOLOM_functie-item_AANTAL;if(codepoint=='C')Terminal_invoer->KOLOM_functie=Terminal_invoer->KOLOM_functie+item_AANTAL>=Terminal_invoer->KOLOMMEN?Terminal_invoer->KOLOMMEN-1:Terminal_invoer->KOLOM_functie+item_AANTAL;
    if(codepoint=='G')Terminal_invoer->KOLOM_functie=item_AANTAL>Terminal_invoer->KOLOMMEN?Terminal_invoer->KOLOMMEN-1:item_AANTAL-1;if(codepoint=='A')Terminal_invoer->RIJ_functie=item_AANTAL>Terminal_invoer->RIJ_functie-Terminal_invoer->맨위?Terminal_invoer->맨위:Terminal_invoer->RIJ_functie-item_AANTAL;
    if(codepoint=='B')Terminal_invoer->RIJ_functie=Terminal_invoer->RIJ_functie+item_AANTAL>=Terminal_invoer->맨위+Terminal_invoer->RIJ_AANTAL?Terminal_invoer->맨위+Terminal_invoer->RIJ_AANTAL-1:Terminal_invoer->RIJ_functie+item_AANTAL;
    if(codepoint=='H'||codepoint=='f'){Terminal_invoer->RIJ_functie=Terminal_invoer->맨위+(item_AANTAL>Terminal_invoer->RIJ_AANTAL?Terminal_invoer->RIJ_AANTAL:item_AANTAL)-1;unsigned x_coördinaat=Terminal_invoer->parameter_WAARDE[1]?Terminal_invoer->parameter_WAARDE[1]:1;Terminal_invoer->KOLOM_functie=(x_coördinaat>Terminal_invoer->KOLOMMEN?Terminal_invoer->KOLOMMEN:x_coördinaat)-1;}
    if(codepoint=='s'){Terminal_invoer->저장행=Terminal_invoer->RIJ_functie;Terminal_invoer->저장열=Terminal_invoer->KOLOM_functie;}if(codepoint=='u'){Terminal_invoer->RIJ_functie=Terminal_invoer->저장행;Terminal_invoer->KOLOM_functie=Terminal_invoer->저장열<Terminal_invoer->KOLOMMEN?Terminal_invoer->저장열:Terminal_invoer->KOLOMMEN-1;}
    if((codepoint=='h'||codepoint=='l')&&Terminal_invoer->parameter_WAARDE[0]==25)Terminal_invoer->가리개보임=codepoint=='h';
}
void Terminal_byte(unsigned SECONDE_WAARDE){
    Terminal_invoer=&Windows_Lijst[uitvoer];if(!Terminal_invoer->살아있음)return;caret_teken_WAARDE(0);if(Terminal_invoer->schuiven){Terminal_invoer->schuiven=0;if(보이는지())Inhoud_WAARDE();}
    if(Terminal_invoer->탈출상태==1){Terminal_invoer->탈출상태=SECONDE_WAARDE=='['?2:0;Terminal_invoer->parameter_INDEX=0;for(unsigned 순번=0;순번<4;순번++)Terminal_invoer->parameter_WAARDE[순번]=0;}
    else if(Terminal_invoer->탈출상태==2){if(SECONDE_WAARDE=='?'){}else if(SECONDE_WAARDE>='0'&&SECONDE_WAARDE<='9'){if(Terminal_invoer->parameter_WAARDE[Terminal_invoer->parameter_INDEX]<10000)Terminal_invoer->parameter_WAARDE[Terminal_invoer->parameter_INDEX]=Terminal_invoer->parameter_WAARDE[Terminal_invoer->parameter_INDEX]*10+SECONDE_WAARDE-'0';}else if(SECONDE_WAARDE==';'&&Terminal_invoer->parameter_INDEX<3)Terminal_invoer->parameter_INDEX++;else{greep_controle_REEKS(SECONDE_WAARDE);Terminal_invoer->탈출상태=0;}}
    else if(SECONDE_WAARDE==27){Terminal_invoer->긴부호없는값=0;Terminal_invoer->탈출상태=1;}else{
        if(Terminal_invoer->긴부호없는값&&(SECONDE_WAARDE&0xc0)!=0x80){Terminal_invoer->긴부호없는값=0;codepoint_451f2815(0xfffd);}
        if(Terminal_invoer->긴부호없는값){Terminal_invoer->부호없는결과=Terminal_invoer->부호없는결과*64+(SECONDE_WAARDE&63);if(--Terminal_invoer->긴부호없는값==0)codepoint_451f2815(Terminal_invoer->부호없는결과<Terminal_invoer->KLEINSTE_WAARDE||Terminal_invoer->부호없는결과>0x10ffff||(Terminal_invoer->부호없는결과>=0xd800&&Terminal_invoer->부호없는결과<=0xdfff)?0xfffd:Terminal_invoer->부호없는결과);}
        else if(SECONDE_WAARDE<128)codepoint_451f2815(SECONDE_WAARDE);else if(SECONDE_WAARDE>=0xc2&&SECONDE_WAARDE<=0xf4){Terminal_invoer->긴부호없는값=SECONDE_WAARDE<0xe0?1:SECONDE_WAARDE<0xf0?2:3;Terminal_invoer->부호없는결과=SECONDE_WAARDE&((1u<<(6-Terminal_invoer->긴부호없는값))-1);Terminal_invoer->KLEINSTE_WAARDE=Terminal_invoer->긴부호없는값==1?128:Terminal_invoer->긴부호없는값==2?2048:65536;}else codepoint_451f2815(0xfffd);
    }caret_teken_WAARDE(1);
}
int Terminal_In_behandeling(void){return informatie_In_behandeling!=0;}
/* 모서리 INDEX: 1 좌상, 2 우상, 3 좌하, 4 우하. */
static int formaat_wijzigen_slepen=-1,잡은모서리,잡은가로,잡은세로,처음가로,처음세로,처음너비,처음높이;
static int 가리킨창(int 가로,int Verticaal_functie) {
    for(int REEKS_WAARDE=invoer_AANTAL_8f7753a1-1;REEKS_WAARDE>=0;REEKS_WAARDE--){
        int id_WAARDE=order_WAARDE[REEKS_WAARDE];Terminal *Venster=&Windows_Lijst[id_WAARDE];
        if(가로>=(int)Venster->x_coördinaat&&Verticaal_functie>=(int)Venster->Y_coördinaat&&
           가로<(int)(Venster->x_coördinaat+Venster->너비)&&Verticaal_functie<(int)(Venster->Y_coördinaat+Venster->hoogte_WAARDE))return id_WAARDE;
    }return -1;
}
static int 모서리찾기(int id_WAARDE,int 가로,int Verticaal_functie) {
    if(id_WAARDE<0)return 0;Terminal *Venster=&Windows_Lijst[id_WAARDE];
    int 왼쪽=가로<(int)Venster->x_coördinaat+8,recht=가로>=(int)(Venster->x_coördinaat+Venster->너비)-8;
    int 위쪽=Verticaal_functie<(int)Venster->Y_coördinaat+8,아래쪽=Verticaal_functie>=(int)(Venster->Y_coördinaat+Venster->hoogte_WAARDE)-8;
    return (왼쪽||recht)&&(위쪽||아래쪽)?1+recht+아래쪽*2:0;
}
static int scheidingsbalk_WAARDE(int WAARDE,int 최소,int 최대){return WAARDE<최소?최소:WAARDE>최대?최대:WAARDE;}
static void verplaatsen_formaat_wijzigen(int 가로,int Verticaal_functie) {
    Terminal *Venster=&Windows_Lijst[formaat_wijzigen_slepen];int 왼쪽=처음가로,위쪽=처음세로,recht=처음가로+처음너비,아래쪽=처음세로+처음높이;
    if(잡은모서리==1||잡은모서리==3)왼쪽=scheidingsbalk_WAARDE(처음가로+가로-잡은가로,0,recht-360);
    else recht=scheidingsbalk_WAARDE(처음가로+처음너비+가로-잡은가로,왼쪽+360,보드화면너비());
    if(잡은모서리<=2)위쪽=scheidingsbalk_WAARDE(처음세로+Verticaal_functie-잡은세로,34,아래쪽-216);
    else 아래쪽=scheidingsbalk_WAARDE(처음세로+처음높이+Verticaal_functie-잡은세로,위쪽+216,Bord_scherm_hoogte());
    unsigned KOLOMMEN=(recht-왼쪽-24)/8,RIJ_AANTAL=(아래쪽-위쪽-56)/16;
    if(Venster->KOLOMMEN!=KOLOMMEN||Venster->RIJ_AANTAL!=RIJ_AANTAL){
        Venster->크기바뀜=1;Venster->KOLOMMEN=KOLOMMEN;Venster->RIJ_AANTAL=RIJ_AANTAL;
        if(Venster->KOLOM_functie>=KOLOMMEN)Venster->KOLOM_functie=KOLOMMEN-1;
        if(Venster->RIJ_functie>=Venster->맨위+RIJ_AANTAL)Venster->맨위=Venster->RIJ_functie-RIJ_AANTAL+1;
        unsigned 한도=Venster->맨위;if(한도>Geschiedenis_lijn_AANTAL-RIJ_AANTAL)한도=Geschiedenis_lijn_AANTAL-RIJ_AANTAL;
        if(Venster->schuiven>한도)Venster->schuiven=한도;
    }
    int 옛가로=Venster->x_coördinaat,옛세로=Venster->Y_coördinaat,옛폭=Venster->너비,옛길이=Venster->hoogte_WAARDE;
    if(옛가로==왼쪽&&옛세로==위쪽&&옛폭==recht-왼쪽&&옛길이==아래쪽-위쪽)return;
    Venster->x_coördinaat=왼쪽;Venster->Y_coördinaat=위쪽;Venster->너비=recht-왼쪽;Venster->hoogte_WAARDE=아래쪽-위쪽;
    창자리그리기(옛가로,옛세로,옛폭,옛길이,Venster);
}
void Terminal_wijzer(unsigned Volgende_item,int x_coördinaat,int Y_coördinaat){
    unsigned 눌림=Volgende_item&~단추들;단추들=Volgende_item;
    if(!pc_Weergave){slepen_WAARDE=-1;formaat_wijzigen_slepen=-1;Bord_wijzer(x_coördinaat,Y_coördinaat,1);return;}
    if(!(Volgende_item&1)){slepen_WAARDE=-1;formaat_wijzigen_slepen=-1;}
    if(formaat_wijzigen_slepen>=0&&!Windows_Lijst[formaat_wijzigen_slepen].살아있음)formaat_wijzigen_slepen=-1;
    if(slepen_WAARDE>=0&&!Windows_Lijst[slepen_WAARDE].살아있음)slepen_WAARDE=-1;
    if(formaat_wijzigen_slepen>=0){
        verplaatsen_formaat_wijzigen(x_coördinaat,Y_coördinaat);Bord_wijzer(x_coördinaat,Y_coördinaat,잡은모서리==1||잡은모서리==4?2:3);return;
    }
    Bord_wijzer(x_coördinaat,Y_coördinaat,1);
    if(slepen_WAARDE>=0){
        Terminal *Venster=&Windows_Lijst[slepen_WAARDE];
        int 옛가로=Venster->x_coördinaat,옛세로=Venster->Y_coördinaat;
        Venster->x_coördinaat=scheidingsbalk_WAARDE(x_coördinaat-slepen_X,0,보드화면너비()-Venster->너비);
        Venster->Y_coördinaat=scheidingsbalk_WAARDE(Y_coördinaat-slepen_Y,34,Bord_scherm_hoogte()-Venster->hoogte_WAARDE);
        if(옛가로!=(int)Venster->x_coördinaat||옛세로!=(int)Venster->Y_coördinaat)창자리그리기(옛가로,옛세로,Venster->너비,Venster->hoogte_WAARDE,Venster);
        return;
    }
    extern int scherm_overlay(int,int,int);
    if(scherm_overlay(Focus,x_coördinaat,Y_coördinaat)){scherm_wijzer(Focus,눌림,x_coördinaat,Y_coördinaat);return;}
    int id_WAARDE=가리킨창(x_coördinaat,Y_coördinaat),모서리=모서리찾기(id_WAARDE,x_coördinaat,Y_coördinaat);
    if(모서리)Bord_wijzer(x_coördinaat,Y_coördinaat,모서리==1||모서리==4?2:3);
    if(눌림&1){
        if(모서리){
            Terminal *Venster=&Windows_Lijst[id_WAARDE];formaat_wijzigen_slepen=id_WAARDE;잡은모서리=모서리;잡은가로=x_coördinaat;잡은세로=Y_coördinaat;
            처음가로=Venster->x_coördinaat;처음세로=Venster->Y_coördinaat;처음너비=Venster->너비;처음높이=Venster->hoogte_WAARDE;
            if(id_WAARDE!=Focus)앞으로올리기(id_WAARDE);return;
        }
        if(Y_coördinaat<32&&x_coördinaat>=6&&x_coördinaat<142){maken_invoer();return;}
        if(Y_coördinaat<32&&x_coördinaat>=154&&x_coördinaat<602){앞으로올리기((x_coördinaat-154)/112);return;}
        if(id_WAARDE>=0){
            Terminal *Venster=&Windows_Lijst[id_WAARDE];
            if(Y_coördinaat<(int)Venster->Y_coördinaat+30&&x_coördinaat>=(int)(Venster->x_coördinaat+Venster->너비)-32){Sluiten_venster(id_WAARDE);return;}
            if(id_WAARDE!=Focus)앞으로올리기(id_WAARDE);
            if(Y_coördinaat<(int)Venster->Y_coördinaat+30){slepen_WAARDE=id_WAARDE;slepen_X=x_coördinaat-Venster->x_coördinaat;slepen_Y=Y_coördinaat-Venster->Y_coördinaat;}return;
        }
    }
    if(Focus>=0&&(눌림&(8|16))){Terminal_invoer=&Windows_Lijst[Focus];if(눌림&8){unsigned 한도=Terminal_invoer->맨위;if(한도>Geschiedenis_lijn_AANTAL-Terminal_invoer->RIJ_AANTAL)한도=Geschiedenis_lijn_AANTAL-Terminal_invoer->RIJ_AANTAL;Terminal_invoer->schuiven=Terminal_invoer->schuiven+9>한도?한도:Terminal_invoer->schuiven+9;}else Terminal_invoer->schuiven=Terminal_invoer->schuiven<9?0:Terminal_invoer->schuiven-9;다시그리기();}
}
void 터미널바로가기키(unsigned 누름값){if(누름값==1)maken_invoer();if(누름값==2&&invoer_AANTAL_8f7753a1)앞으로올리기(order_WAARDE[0]);if(누름값==3)Sluiten_venster(Focus);}
machine_Word Bord_Terminal(machine_Word Actie){
    if(Actie==300){if(!Windows_Lijst[uitvoer].살아있음)return maken_invoer();pc_Weergave=1;다시그리기();return 0;}
    if(Actie==0){Sluiten_venster(Focus);return 0;}if(Actie==1)return (uint32_t)maken_invoer();if(Actie==2)return Focus>=0;
    if(Actie==9){pc_Weergave=0;return 0;}if(Actie==7)return invoer_AANTAL_8f7753a1;if(Actie==10)return Focus+1;if(Actie==11)return uitvoer;
    if(Actie==13){Terminal *Venster=&Windows_Lijst[uitvoer];return Venster->살아있음?(Venster->RIJ_AANTAL<<16)|Venster->KOLOMMEN:(19<<16)|68;}
    if(Actie==14){unsigned WAARDE=Windows_Lijst[uitvoer].크기바뀜;Windows_Lijst[uitvoer].크기바뀜=0;return WAARDE;}
    if(Actie==12){unsigned WAARDE=informatie_In_behandeling;informatie_In_behandeling=0;return WAARDE;}
    if(Actie>=20&&Actie<24)return Windows_Lijst[Actie-20].살아있음;
    if(Actie>=100&&Actie<104){uitvoer=Actie-100;Terminal_invoer=&Windows_Lijst[uitvoer];return 0;}
    if(Actie>=200&&Actie<204){앞으로올리기(Actie-200);return 0;}
    if(Actie==3){다시그리기();return 0;}Terminal_invoer=&Windows_Lijst[uitvoer];if(!Terminal_invoer->살아있음)return 0;
    if(Actie==4)wissen_Inhoud();if(Actie==5||Actie==6){unsigned Vorige_item=단추들;Terminal_wijzer(Actie==5?8:16,0,0);단추들=Vorige_item;}return 1;
}
