#include "../명명/기계연결이름.h"
#include "skjermbilde_info.h"
/* eget 네 Vindu 합성과 UTF-8 Terminal. 바뀐 영역의 Fullført_VERDI 그림만 표시한다. */
#include <stdint.h>
#include <stddef.h>
typedef uintptr_t maskin_ord;
extern maskin_ord Tavle_piksel(maskin_ord,maskin_ord,maskin_ord),보드화면기억공간(void);
extern void *memset(void *,int,size_t);
extern const unsigned char Terminal_skrift[];
#define 최대열수 237
#define Logg_linje_ANTALL 160
typedef struct {
    uint32_t 글자칸들[Logg_linje_ANTALL][최대열수]; uint8_t 모양들[Logg_linje_ANTALL][최대열수];
    unsigned 너비,높이,KOLONNER,RAD_ANTALL,크기바뀜;
    unsigned 살아있음,x_koordinat,Y_koordinat,RAD_plassere,spalte_plassere,맨위,rulle,전경색,배경색,탈출상태,parameter_VERDI[4],parameter_INDEKS,저장행,저장열;
    unsigned 부호없는결과,긴부호없는값,N_MINST_VERDI,대체화면,가리개보임;
} Terminal_d413d4bc;
static Terminal_d413d4bc Windows_Liste[4];
static int Fokus=-1,produksjon,ordre_VERDI[4],oppføring_ANTALL,dra_VERDI=-1,dra_X,dra_Y;
static unsigned informasjonssystemer_Venter,단추들,stasjonær_vise,한글입력;
static const uint32_t 색상들[16]={0x201a15,0x6060df,0x9dcc86,0x80cfea,0xefaf72,0xca96c9,0xceda76,0xede9df,0x858078,0x8888ff,0xb9eba7,0xa5eaff,0xffcc99,0xf0bef1,0xf0f0a0,0xffffff};
extern int 화면보임(int),skjermbilde_peker(int,unsigned,int,int);
extern void 화면다시그림(int);
static Terminal_d413d4bc *Terminal_oppføring;
static unsigned 넓은글자(unsigned tegnkode){return tegnkode>=256?2:1;}
static void 사각영역(unsigned x_koordinat,unsigned Y_koordinat,unsigned 너비값,unsigned 높이값,unsigned 색상){
    Tavle_rektangel_fyll(x_koordinat,Y_koordinat,너비값,높이값,색상);
}
void Terminal_figur(unsigned x_koordinat,unsigned Y_koordinat,unsigned tegnkode,unsigned 전경색,unsigned 배경색){
    unsigned 너비=넓은글자(tegnkode)*8;if(tegnkode==0xffffffffu)return;
    int 왼쪽=x_koordinat,위쪽=Y_koordinat,폭=너비,lengde_VERDI=16;
    if(!보드그림범위(&왼쪽,&위쪽,&폭,&lengde_VERDI))return;
    if(tegnkode==' '){Tavle_rektangel_fyll(왼쪽,위쪽,폭,lengde_VERDI,배경색);return;}
    unsigned Oppslag_INDEKS=tegnkode<65536?tegnkode:tegnkode>=0x1f600&&tegnkode<0x1f650?65536+tegnkode-0x1f600:0xfffd;
    const unsigned char *skrift_VERDI=Terminal_skrift+Oppslag_INDEKS*32;
    for(int Linje=위쪽;Linje<위쪽+lengde_VERDI;Linje++){unsigned BITS_Liste=skrift_VERDI[(Linje-Y_koordinat)*2]*256+skrift_VERDI[(Linje-Y_koordinat)*2+1];for(int åpning_oppføring=왼쪽;åpning_oppføring<왼쪽+폭;åpning_oppføring++)Tavle_piksel(åpning_oppføring,Linje,(BITS_Liste&(0x8000>>(åpning_oppføring-x_koordinat)))?전경색:배경색);}
}
static void navn_tabell(unsigned x_koordinat,unsigned Y_koordinat,const char *streng_data,unsigned 전경색,unsigned 배경색){while(*streng_data){unsigned tegnkode=(unsigned char)*streng_data++, 남은수=0;if(tegnkode>=0xc0){남은수=tegnkode<0xe0?1:tegnkode<0xf0?2:3;tegnkode&=(1u<<(6-남은수))-1;while(남은수--&&*streng_data)tegnkode=(tegnkode<<6)|((unsigned char)*streng_data++&63);}Terminal_figur(x_koordinat,Y_koordinat,tegnkode,전경색,배경색);x_koordinat+=넓은글자(tegnkode)*8;}}
static unsigned 첫항목(void){return Terminal_oppføring->맨위;}
static int 보이는지(void){return Terminal_oppføring->살아있음&&Fokus>=0&&Terminal_oppføring==&Windows_Liste[Fokus]&&!화면보임(Fokus);}
static void Paint_skjermbilde(unsigned RAD_plassere,unsigned spalte_plassere){
    if(!보이는지()||RAD_plassere<첫항목()-Terminal_oppføring->rulle||RAD_plassere>=첫항목()-Terminal_oppføring->rulle+Terminal_oppføring->RAD_ANTALL||spalte_plassere>=Terminal_oppføring->KOLONNER)return;
    unsigned tegnkode=Terminal_oppføring->글자칸들[RAD_plassere%Logg_linje_ANTALL][spalte_plassere],streng_data=Terminal_oppføring->모양들[RAD_plassere%Logg_linje_ANTALL][spalte_plassere];
    if(넓은글자(tegnkode)==2&&spalte_plassere+1>=Terminal_oppføring->KOLONNER)tegnkode=' ';
    Terminal_figur(Terminal_oppføring->x_koordinat+12+spalte_plassere*8,Terminal_oppføring->Y_koordinat+36+(RAD_plassere-첫항목()+Terminal_oppføring->rulle)*16,tegnkode?tegnkode:' ',색상들[streng_data&15],색상들[streng_data>>4]);
}
static void cirkumflekstegn_VERDI(int vise_vindu){if(!보이는지()||Terminal_oppføring->rulle||Terminal_oppføring->spalte_plassere>=Terminal_oppføring->KOLONNER||Terminal_oppføring->RAD_plassere<Terminal_oppføring->맨위||Terminal_oppføring->RAD_plassere>=Terminal_oppføring->맨위+Terminal_oppføring->RAD_ANTALL)return;
    if(!vise_vindu||!Terminal_oppføring->가리개보임)Paint_skjermbilde(Terminal_oppføring->RAD_plassere,Terminal_oppføring->spalte_plassere);else 사각영역(Terminal_oppføring->x_koordinat+12+Terminal_oppføring->spalte_plassere*8,Terminal_oppføring->Y_koordinat+36+(Terminal_oppføring->RAD_plassere-Terminal_oppføring->맨위)*16+14,8,2,색상들[Terminal_oppføring->전경색]);}
static void Innhold_VERDI(void){
    사각영역(Terminal_oppføring->x_koordinat+12,Terminal_oppføring->Y_koordinat+36,Terminal_oppføring->KOLONNER*8,Terminal_oppføring->RAD_ANTALL*16,색상들[0]);
    int 가로=Terminal_oppføring->x_koordinat+12,vertikal_plassere=Terminal_oppføring->Y_koordinat+36,폭=Terminal_oppføring->KOLONNER*8,lengde_VERDI=Terminal_oppføring->RAD_ANTALL*16;
    if(보드그림범위(&가로,&vertikal_plassere,&폭,&lengde_VERDI)){
    unsigned 첫줄=(vertikal_plassere-Terminal_oppføring->Y_koordinat-36)/16,끝줄=(vertikal_plassere+lengde_VERDI-Terminal_oppføring->Y_koordinat-36+15)/16;
    unsigned 첫칸=(가로-Terminal_oppføring->x_koordinat-12)/8,끝칸=(가로+폭-Terminal_oppføring->x_koordinat-12+7)/8;
    if(첫칸)첫칸--; /* 잘림 grense_VERDI 왼쪽에서 시작한 두 åpning_oppføring 글자도 그린다. */
    for(unsigned 반환값=첫줄;반환값<끝줄;반환값++)for(unsigned tegnkode=첫칸;tegnkode<끝칸;tegnkode++){
        unsigned RAD_plassere=첫항목()-Terminal_oppføring->rulle+반환값,tegn_VERDI=Terminal_oppføring->글자칸들[RAD_plassere%Logg_linje_ANTALL][tegnkode],streng_data=Terminal_oppføring->모양들[RAD_plassere%Logg_linje_ANTALL][tegnkode];
        if(넓은글자(tegn_VERDI)==2&&tegnkode+1>=Terminal_oppføring->KOLONNER)tegn_VERDI=' ';
        if((tegn_VERDI==0||tegn_VERDI==' ')&&(streng_data>>4)==0)continue;
        Terminal_figur(Terminal_oppføring->x_koordinat+12+tegnkode*8,Terminal_oppføring->Y_koordinat+36+반환값*16,tegn_VERDI?tegn_VERDI:' ',색상들[streng_data&15],색상들[streng_data>>4]);
    }}
    navn_tabell(Terminal_oppføring->x_koordinat+12,Terminal_oppføring->Y_koordinat+Terminal_oppføring->높이-18,Terminal_oppføring->rulle?"PgDn: recent output":Terminal_oppføring->너비>=500?"F6: next | Corner + left drag: resize":"Corner + left drag: resize",0xece8e2,0x403127);cirkumflekstegn_VERDI(1);
}
static void kjøring_bilde(int identifikator_VERDI){
    Terminal_oppføring=&Windows_Liste[identifikator_VERDI];
    int 가로=Terminal_oppføring->x_koordinat,vertikal_plassere=Terminal_oppføring->Y_koordinat,폭=Terminal_oppføring->너비,lengde_VERDI=Terminal_oppføring->높이;
    if(!보드그림범위(&가로,&vertikal_plassere,&폭,&lengde_VERDI))return;
    사각영역(Terminal_oppføring->x_koordinat,Terminal_oppføring->Y_koordinat,Terminal_oppføring->너비,Terminal_oppføring->높이,0x403127);
    unsigned 색상=identifikator_VERDI==Fokus?0x905020:0x604438;사각영역(Terminal_oppføring->x_koordinat,Terminal_oppføring->Y_koordinat,Terminal_oppføring->너비,30,색상);
    navn_tabell(Terminal_oppføring->x_koordinat+12,Terminal_oppføring->Y_koordinat+7,"JKOROS Terminal",0xffffff,색상);
    char 수치[2]={(char)('1'+identifikator_VERDI),0};navn_tabell(Terminal_oppføring->x_koordinat+148,Terminal_oppføring->Y_koordinat+7,수치,0xffffff,색상);
    navn_tabell(Terminal_oppføring->x_koordinat+240,Terminal_oppføring->Y_koordinat+7,Terminal_oppføring->너비>=500?(한글입력?"[NB] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[NB]":"[EN]"),0xffffff,색상);
    사각영역(Terminal_oppføring->x_koordinat+Terminal_oppføring->너비-32,Terminal_oppføring->Y_koordinat+4,26,22,0x5555b8);navn_tabell(Terminal_oppføring->x_koordinat+Terminal_oppføring->너비-24,Terminal_oppføring->Y_koordinat+7,"X",0xffffff,0x5555b8);
    Innhold_VERDI();
}
static void Tegn_scene(void){
    if(!stasjonær_vise)return;사각영역(0,0,보드화면너비(),보드화면높이(),0x302018);사각영역(0,0,보드화면너비(),32,0x403127);
    사각영역(6,4,136,24,0x905020);navn_tabell(14,8,"+ New terminal",0xffffff,0x905020);
    for(int 순번=0;순번<4;순번++)if(Windows_Liste[순번].살아있음){unsigned tegnkode=Fokus==순번?0x905020:0x604438;사각영역(154+순번*112,4,106,24,tegnkode);navn_tabell(160+순번*112,8,"Terminal",0xffffff,tegnkode);char streng_data[2]={(char)('1'+순번),0};navn_tabell(232+순번*112,8,streng_data,0xffffff,tegnkode);}
    if(!oppføring_ANTALL)navn_tabell(140,210,"Click + New terminal to start",0xede9df,0x302018);
    for(int 순번=0;순번<oppføring_ANTALL;순번++)kjøring_bilde(ordre_VERDI[순번]);화면다시그림(Fokus);Terminal_oppføring=&Windows_Liste[produksjon];
}
static void Paint_område(int 가로,int vertikal_plassere,int 폭,int lengde_VERDI){
    if(!stasjonær_vise||!보드그림범위(&가로,&vertikal_plassere,&폭,&lengde_VERDI))return;
    for(int Linje=vertikal_plassere;Linje<vertikal_plassere+lengde_VERDI;Linje+=32){
        int 띠높이=vertikal_plassere+lengde_VERDI-Linje;if(띠높이>32)띠높이=32;
        if(Tavle_START_tegning(가로,Linje,폭,띠높이)){Tegn_scene();Tavle_slutt_tegning();}
    }
}
static void 다시그리기(void){Paint_område(0,0,보드화면너비(),보드화면높이());}
/* 서로 겹치지 않는 새 Vindu 영역과 Forrige_vare 자리의 네 띠를 복구한다. */
static void 창자리그리기(int 가로,int vertikal_plassere,int 폭,int lengde_VERDI,Terminal_d413d4bc *Vindu){
    int 왼쪽=가로>(int)Vindu->x_koordinat?가로:(int)Vindu->x_koordinat;
    int 위쪽=vertikal_plassere>(int)Vindu->Y_koordinat?vertikal_plassere:(int)Vindu->Y_koordinat;
    int HØYRE=가로+폭<(int)(Vindu->x_koordinat+Vindu->너비)?가로+폭:(int)(Vindu->x_koordinat+Vindu->너비);
    int 아래쪽=vertikal_plassere+lengde_VERDI<(int)(Vindu->Y_koordinat+Vindu->높이)?vertikal_plassere+lengde_VERDI:(int)(Vindu->Y_koordinat+Vindu->높이);
    Paint_område(Vindu->x_koordinat,Vindu->Y_koordinat,Vindu->너비,Vindu->높이);
    if(왼쪽>=HØYRE||위쪽>=아래쪽){Paint_område(가로,vertikal_plassere,폭,lengde_VERDI);return;}
    Paint_område(가로,vertikal_plassere,폭,위쪽-vertikal_plassere);
    Paint_område(가로,아래쪽,폭,vertikal_plassere+lengde_VERDI-아래쪽);
    Paint_område(가로,위쪽,왼쪽-가로,아래쪽-위쪽);
    Paint_område(HØYRE,위쪽,가로+폭-HØYRE,아래쪽-위쪽);
}
static void signal_Fokus(void){informasjonssystemer_Venter=(informasjonssystemer_Venter&~15u)|(unsigned)(Fokus+1)|0x10000;}
void Terminal_inndata_MODUS(unsigned 한글여부){
    한글입력=한글여부!=0;
    /* Update title bars only: a mode switch must not erase an EL0 drawing. */
    if(Fokus>=0){
        Terminal_d413d4bc *vindu_oppføring=&Windows_Liste[Fokus];
        navn_tabell(vindu_oppføring->x_koordinat+240,vindu_oppføring->Y_koordinat+7,vindu_oppføring->너비>=500?(한글입력?"[NB] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[NB]":"[EN]"),0xffffff,0x905020);
    }
}
static void 앞으로올리기(int identifikator_VERDI){if(identifikator_VERDI<0||identifikator_VERDI>=4||!Windows_Liste[identifikator_VERDI].살아있음)return;int betalt_plassere=0;while(betalt_plassere<oppføring_ANTALL&&ordre_VERDI[betalt_plassere]!=identifikator_VERDI)betalt_plassere++;for(;betalt_plassere+1<oppføring_ANTALL;betalt_plassere++)ordre_VERDI[betalt_plassere]=ordre_VERDI[betalt_plassere+1];ordre_VERDI[oppføring_ANTALL-1]=identifikator_VERDI;Fokus=identifikator_VERDI;signal_Fokus();다시그리기();}
static void 빈칸채우기(unsigned RAD_plassere){for(unsigned tegnkode=0;tegnkode<최대열수;tegnkode++){Terminal_oppføring->글자칸들[RAD_plassere%Logg_linje_ANTALL][tegnkode]=0;Terminal_oppføring->모양들[RAD_plassere%Logg_linje_ANTALL][tegnkode]=Terminal_oppføring->전경색|(Terminal_oppføring->배경색<<4);}}
static void tømme_Innhold(void){Terminal_oppføring->RAD_plassere=Terminal_oppføring->spalte_plassere=Terminal_oppføring->맨위=Terminal_oppføring->rulle=0;for(unsigned 반환값=0;반환값<Logg_linje_ANTALL;반환값++)빈칸채우기(반환값);if(보이는지())Innhold_VERDI();}
static int åpne_oppføring(void){
    if(!보드화면기억공간())return -19;int identifikator_VERDI=0;while(identifikator_VERDI<4&&Windows_Liste[identifikator_VERDI].살아있음)identifikator_VERDI++;if(identifikator_VERDI==4)return -28;
    stasjonær_vise=1;Terminal_oppføring=&Windows_Liste[identifikator_VERDI];memset(Terminal_oppføring,0,sizeof(*Terminal_oppføring));Terminal_oppføring->살아있음=1;Terminal_oppføring->너비=568;Terminal_oppføring->높이=360;Terminal_oppføring->KOLONNER=68;Terminal_oppføring->RAD_ANTALL=19;Terminal_oppføring->x_koordinat=12+identifikator_VERDI*16;Terminal_oppføring->Y_koordinat=48+identifikator_VERDI*18;Terminal_oppføring->전경색=7;Terminal_oppføring->가리개보임=1;
    for(unsigned 반환값=0;반환값<Logg_linje_ANTALL;반환값++)빈칸채우기(반환값);ordre_VERDI[oppføring_ANTALL++]=identifikator_VERDI;Fokus=identifikator_VERDI;informasjonssystemer_Venter|=1u<<(4+identifikator_VERDI);signal_Fokus();다시그리기();return identifikator_VERDI+1;
}
static void Lukk_vindu(int identifikator_VERDI){
    if(identifikator_VERDI<0||identifikator_VERDI>=4||!Windows_Liste[identifikator_VERDI].살아있음)return;Windows_Liste[identifikator_VERDI].살아있음=0;informasjonssystemer_Venter|=1u<<(8+identifikator_VERDI);
    int betalt_plassere=0;while(betalt_plassere<oppføring_ANTALL&&ordre_VERDI[betalt_plassere]!=identifikator_VERDI)betalt_plassere++;for(;betalt_plassere+1<oppføring_ANTALL;betalt_plassere++)ordre_VERDI[betalt_plassere]=ordre_VERDI[betalt_plassere+1];oppføring_ANTALL--;
    if(Fokus==identifikator_VERDI)Fokus=oppføring_ANTALL?ordre_VERDI[oppføring_ANTALL-1]:-1;signal_Fokus();다시그리기();
}
static void 줄바꿈(void){Terminal_oppføring->spalte_plassere=0;Terminal_oppføring->RAD_plassere++;if(Terminal_oppføring->RAD_plassere>=Terminal_oppføring->맨위+Terminal_oppføring->RAD_ANTALL){Terminal_oppføring->맨위++;빈칸채우기(Terminal_oppføring->RAD_plassere);if(보이는지())Innhold_VERDI();}}
static void tegnkode_451f2815(unsigned tegnkode){
    if(tegnkode==13){Terminal_oppføring->spalte_plassere=0;return;}if(tegnkode==10){줄바꿈();return;}if(tegnkode==8){if(Terminal_oppføring->spalte_plassere)Terminal_oppføring->spalte_plassere--;return;}
    if(tegnkode==9){unsigned vare_ANTALL=8-Terminal_oppføring->spalte_plassere%8;while(vare_ANTALL--)tegnkode_451f2815(' ');return;}if(tegnkode<32||tegnkode==127)return;
    unsigned 너비값=넓은글자(tegnkode);if(Terminal_oppføring->spalte_plassere+너비값>Terminal_oppføring->KOLONNER)줄바꿈();
    if(Terminal_oppføring->글자칸들[Terminal_oppføring->RAD_plassere%Logg_linje_ANTALL][Terminal_oppføring->spalte_plassere]==0xffffffffu&&Terminal_oppføring->spalte_plassere){Terminal_oppføring->글자칸들[Terminal_oppføring->RAD_plassere%Logg_linje_ANTALL][Terminal_oppføring->spalte_plassere-1]=' ';Paint_skjermbilde(Terminal_oppføring->RAD_plassere,Terminal_oppføring->spalte_plassere-1);}
    if(넓은글자(Terminal_oppføring->글자칸들[Terminal_oppføring->RAD_plassere%Logg_linje_ANTALL][Terminal_oppføring->spalte_plassere])==2&&Terminal_oppføring->spalte_plassere+1<Terminal_oppføring->KOLONNER){Terminal_oppføring->글자칸들[Terminal_oppføring->RAD_plassere%Logg_linje_ANTALL][Terminal_oppføring->spalte_plassere+1]=' ';Paint_skjermbilde(Terminal_oppføring->RAD_plassere,Terminal_oppføring->spalte_plassere+1);}
    Terminal_oppføring->글자칸들[Terminal_oppføring->RAD_plassere%Logg_linje_ANTALL][Terminal_oppføring->spalte_plassere]=tegnkode;Terminal_oppføring->모양들[Terminal_oppføring->RAD_plassere%Logg_linje_ANTALL][Terminal_oppføring->spalte_plassere]=Terminal_oppføring->전경색|(Terminal_oppføring->배경색<<4);
    if(너비값==2)Terminal_oppføring->글자칸들[Terminal_oppføring->RAD_plassere%Logg_linje_ANTALL][Terminal_oppføring->spalte_plassere+1]=0xffffffffu;
    Paint_skjermbilde(Terminal_oppføring->RAD_plassere,Terminal_oppføring->spalte_plassere);Terminal_oppføring->spalte_plassere+=너비값;
}
static void håndtak_kontroll_SEKVENS(unsigned tegnkode){
    unsigned vare_ANTALL=Terminal_oppføring->parameter_VERDI[0]?Terminal_oppføring->parameter_VERDI[0]:1;
    if(tegnkode=='m')for(unsigned 순번=0;순번<=Terminal_oppføring->parameter_INDEKS;순번++){unsigned data_plassere=Terminal_oppføring->parameter_VERDI[순번];if(!data_plassere){Terminal_oppføring->전경색=7;Terminal_oppføring->배경색=0;}if(data_plassere==1&&Terminal_oppføring->전경색<8)Terminal_oppføring->전경색+=8;if(data_plassere==7){unsigned 유지=Terminal_oppføring->전경색;Terminal_oppføring->전경색=Terminal_oppføring->배경색;Terminal_oppføring->배경색=유지;}if(data_plassere>=30&&data_plassere<=37)Terminal_oppføring->전경색=data_plassere-30;if(data_plassere>=90&&data_plassere<=97)Terminal_oppføring->전경색=data_plassere-90+8;if(data_plassere>=40&&data_plassere<=47)Terminal_oppføring->배경색=data_plassere-40;if(data_plassere>=100&&data_plassere<=107)Terminal_oppføring->배경색=data_plassere-100+8;if(data_plassere==39)Terminal_oppføring->전경색=7;if(data_plassere==49)Terminal_oppføring->배경색=0;}
    if(tegnkode=='J'&&(Terminal_oppføring->parameter_VERDI[0]==2||Terminal_oppføring->parameter_VERDI[0]==3))tømme_Innhold();
    if(tegnkode=='K'){unsigned 출발위치=Terminal_oppføring->parameter_VERDI[0]==2?0:Terminal_oppføring->spalte_plassere,도착위치=Terminal_oppføring->parameter_VERDI[0]==1?Terminal_oppføring->spalte_plassere+1:Terminal_oppføring->KOLONNER;if(Terminal_oppføring->parameter_VERDI[0]==1)출발위치=0;for(unsigned 순번=출발위치;순번<도착위치&&순번<Terminal_oppføring->KOLONNER;순번++){
        unsigned RAD_VERDI=Terminal_oppføring->RAD_plassere%Logg_linje_ANTALL,tegn_VERDI=Terminal_oppføring->글자칸들[RAD_VERDI][순번],figur_VERDI=Terminal_oppføring->전경색|(Terminal_oppføring->배경색<<4);
        /* 넓은 vi 화면에서도 이미 빈 칸의 skrift_VERDI 화소를 되풀이해 칠하지 않는다. */
        int 바뀜=(tegn_VERDI!=0&&tegn_VERDI!=' ')||Terminal_oppføring->모양들[RAD_VERDI][순번]!=figur_VERDI;
        Terminal_oppføring->글자칸들[RAD_VERDI][순번]=' ';Terminal_oppføring->모양들[RAD_VERDI][순번]=figur_VERDI;
        if(바뀜)Paint_skjermbilde(Terminal_oppføring->RAD_plassere,순번);
    }}
    if(tegnkode=='D')Terminal_oppføring->spalte_plassere=vare_ANTALL>Terminal_oppføring->spalte_plassere?0:Terminal_oppføring->spalte_plassere-vare_ANTALL;if(tegnkode=='C')Terminal_oppføring->spalte_plassere=Terminal_oppføring->spalte_plassere+vare_ANTALL>=Terminal_oppføring->KOLONNER?Terminal_oppføring->KOLONNER-1:Terminal_oppføring->spalte_plassere+vare_ANTALL;
    if(tegnkode=='G')Terminal_oppføring->spalte_plassere=vare_ANTALL>Terminal_oppføring->KOLONNER?Terminal_oppføring->KOLONNER-1:vare_ANTALL-1;if(tegnkode=='A')Terminal_oppføring->RAD_plassere=vare_ANTALL>Terminal_oppføring->RAD_plassere-Terminal_oppføring->맨위?Terminal_oppføring->맨위:Terminal_oppføring->RAD_plassere-vare_ANTALL;
    if(tegnkode=='B')Terminal_oppføring->RAD_plassere=Terminal_oppføring->RAD_plassere+vare_ANTALL>=Terminal_oppføring->맨위+Terminal_oppføring->RAD_ANTALL?Terminal_oppføring->맨위+Terminal_oppføring->RAD_ANTALL-1:Terminal_oppføring->RAD_plassere+vare_ANTALL;
    if(tegnkode=='H'||tegnkode=='f'){Terminal_oppføring->RAD_plassere=Terminal_oppføring->맨위+(vare_ANTALL>Terminal_oppføring->RAD_ANTALL?Terminal_oppføring->RAD_ANTALL:vare_ANTALL)-1;unsigned x_koordinat=Terminal_oppføring->parameter_VERDI[1]?Terminal_oppføring->parameter_VERDI[1]:1;Terminal_oppføring->spalte_plassere=(x_koordinat>Terminal_oppføring->KOLONNER?Terminal_oppføring->KOLONNER:x_koordinat)-1;}
    if(tegnkode=='s'){Terminal_oppføring->저장행=Terminal_oppføring->RAD_plassere;Terminal_oppføring->저장열=Terminal_oppføring->spalte_plassere;}if(tegnkode=='u'){Terminal_oppføring->RAD_plassere=Terminal_oppføring->저장행;Terminal_oppføring->spalte_plassere=Terminal_oppføring->저장열<Terminal_oppføring->KOLONNER?Terminal_oppføring->저장열:Terminal_oppføring->KOLONNER-1;}
    if((tegnkode=='h'||tegnkode=='l')&&Terminal_oppføring->parameter_VERDI[0]==25)Terminal_oppføring->가리개보임=tegnkode=='h';
}
void Terminal_byte(unsigned SEKUND_VERDI){
    Terminal_oppføring=&Windows_Liste[produksjon];if(!Terminal_oppføring->살아있음)return;cirkumflekstegn_VERDI(0);if(Terminal_oppføring->rulle){Terminal_oppføring->rulle=0;if(보이는지())Innhold_VERDI();}
    if(Terminal_oppføring->탈출상태==1){Terminal_oppføring->탈출상태=SEKUND_VERDI=='['?2:0;Terminal_oppføring->parameter_INDEKS=0;for(unsigned 순번=0;순번<4;순번++)Terminal_oppføring->parameter_VERDI[순번]=0;}
    else if(Terminal_oppføring->탈출상태==2){if(SEKUND_VERDI=='?'){}else if(SEKUND_VERDI>='0'&&SEKUND_VERDI<='9'){if(Terminal_oppføring->parameter_VERDI[Terminal_oppføring->parameter_INDEKS]<10000)Terminal_oppføring->parameter_VERDI[Terminal_oppføring->parameter_INDEKS]=Terminal_oppføring->parameter_VERDI[Terminal_oppføring->parameter_INDEKS]*10+SEKUND_VERDI-'0';}else if(SEKUND_VERDI==';'&&Terminal_oppføring->parameter_INDEKS<3)Terminal_oppføring->parameter_INDEKS++;else{håndtak_kontroll_SEKVENS(SEKUND_VERDI);Terminal_oppføring->탈출상태=0;}}
    else if(SEKUND_VERDI==27){Terminal_oppføring->긴부호없는값=0;Terminal_oppføring->탈출상태=1;}else{
        if(Terminal_oppføring->긴부호없는값&&(SEKUND_VERDI&0xc0)!=0x80){Terminal_oppføring->긴부호없는값=0;tegnkode_451f2815(0xfffd);}
        if(Terminal_oppføring->긴부호없는값){Terminal_oppføring->부호없는결과=Terminal_oppføring->부호없는결과*64+(SEKUND_VERDI&63);if(--Terminal_oppføring->긴부호없는값==0)tegnkode_451f2815(Terminal_oppføring->부호없는결과<Terminal_oppføring->N_MINST_VERDI||Terminal_oppføring->부호없는결과>0x10ffff||(Terminal_oppføring->부호없는결과>=0xd800&&Terminal_oppføring->부호없는결과<=0xdfff)?0xfffd:Terminal_oppføring->부호없는결과);}
        else if(SEKUND_VERDI<128)tegnkode_451f2815(SEKUND_VERDI);else if(SEKUND_VERDI>=0xc2&&SEKUND_VERDI<=0xf4){Terminal_oppføring->긴부호없는값=SEKUND_VERDI<0xe0?1:SEKUND_VERDI<0xf0?2:3;Terminal_oppføring->부호없는결과=SEKUND_VERDI&((1u<<(6-Terminal_oppføring->긴부호없는값))-1);Terminal_oppføring->N_MINST_VERDI=Terminal_oppføring->긴부호없는값==1?128:Terminal_oppføring->긴부호없는값==2?2048:65536;}else tegnkode_451f2815(0xfffd);
    }cirkumflekstegn_VERDI(1);
}
int Terminal_Venter(void){return informasjonssystemer_Venter!=0;}
/* 모서리 INDEKS: 1 좌상, 2 우상, 3 좌하, 4 우하. */
static int endre_størrelse_på_dra=-1,잡은모서리,잡은가로,잡은세로,처음가로,처음세로,처음너비,처음높이;
static int 가리킨창(int 가로,int vertikal_plassere) {
    for(int SEKVENS_VERDI=oppføring_ANTALL-1;SEKVENS_VERDI>=0;SEKVENS_VERDI--){
        int identifikator_VERDI=ordre_VERDI[SEKVENS_VERDI];Terminal_d413d4bc *Vindu=&Windows_Liste[identifikator_VERDI];
        if(가로>=(int)Vindu->x_koordinat&&vertikal_plassere>=(int)Vindu->Y_koordinat&&
           가로<(int)(Vindu->x_koordinat+Vindu->너비)&&vertikal_plassere<(int)(Vindu->Y_koordinat+Vindu->높이))return identifikator_VERDI;
    }return -1;
}
static int 모서리찾기(int identifikator_VERDI,int 가로,int vertikal_plassere) {
    if(identifikator_VERDI<0)return 0;Terminal_d413d4bc *Vindu=&Windows_Liste[identifikator_VERDI];
    int 왼쪽=가로<(int)Vindu->x_koordinat+8,HØYRE=가로>=(int)(Vindu->x_koordinat+Vindu->너비)-8;
    int 위쪽=vertikal_plassere<(int)Vindu->Y_koordinat+8,아래쪽=vertikal_plassere>=(int)(Vindu->Y_koordinat+Vindu->높이)-8;
    return (왼쪽||HØYRE)&&(위쪽||아래쪽)?1+HØYRE+아래쪽*2:0;
}
static int skillelinje_VERDI(int VERDI,int 최소,int 최대){return VERDI<최소?최소:VERDI>최대?최대:VERDI;}
static void flytte_endre_størrelse_på(int 가로,int vertikal_plassere) {
    Terminal_d413d4bc *Vindu=&Windows_Liste[endre_størrelse_på_dra];int 왼쪽=처음가로,위쪽=처음세로,HØYRE=처음가로+처음너비,아래쪽=처음세로+처음높이;
    if(잡은모서리==1||잡은모서리==3)왼쪽=skillelinje_VERDI(처음가로+가로-잡은가로,0,HØYRE-360);
    else HØYRE=skillelinje_VERDI(처음가로+처음너비+가로-잡은가로,왼쪽+360,보드화면너비());
    if(잡은모서리<=2)위쪽=skillelinje_VERDI(처음세로+vertikal_plassere-잡은세로,34,아래쪽-216);
    else 아래쪽=skillelinje_VERDI(처음세로+처음높이+vertikal_plassere-잡은세로,위쪽+216,보드화면높이());
    unsigned KOLONNER=(HØYRE-왼쪽-24)/8,RAD_ANTALL=(아래쪽-위쪽-56)/16;
    if(Vindu->KOLONNER!=KOLONNER||Vindu->RAD_ANTALL!=RAD_ANTALL){
        Vindu->크기바뀜=1;Vindu->KOLONNER=KOLONNER;Vindu->RAD_ANTALL=RAD_ANTALL;
        if(Vindu->spalte_plassere>=KOLONNER)Vindu->spalte_plassere=KOLONNER-1;
        if(Vindu->RAD_plassere>=Vindu->맨위+RAD_ANTALL)Vindu->맨위=Vindu->RAD_plassere-RAD_ANTALL+1;
        unsigned 한도=Vindu->맨위;if(한도>Logg_linje_ANTALL-RAD_ANTALL)한도=Logg_linje_ANTALL-RAD_ANTALL;
        if(Vindu->rulle>한도)Vindu->rulle=한도;
    }
    int 옛가로=Vindu->x_koordinat,옛세로=Vindu->Y_koordinat,옛폭=Vindu->너비,옛길이=Vindu->높이;
    if(옛가로==왼쪽&&옛세로==위쪽&&옛폭==HØYRE-왼쪽&&옛길이==아래쪽-위쪽)return;
    Vindu->x_koordinat=왼쪽;Vindu->Y_koordinat=위쪽;Vindu->너비=HØYRE-왼쪽;Vindu->높이=아래쪽-위쪽;
    창자리그리기(옛가로,옛세로,옛폭,옛길이,Vindu);
}
void Terminal_peker(unsigned Neste_vare,int x_koordinat,int Y_koordinat){
    unsigned 눌림=Neste_vare&~단추들;단추들=Neste_vare;
    if(!stasjonær_vise){dra_VERDI=-1;endre_størrelse_på_dra=-1;Tavle_peker(x_koordinat,Y_koordinat,1);return;}
    if(!(Neste_vare&1)){dra_VERDI=-1;endre_størrelse_på_dra=-1;}
    if(endre_størrelse_på_dra>=0&&!Windows_Liste[endre_størrelse_på_dra].살아있음)endre_størrelse_på_dra=-1;
    if(dra_VERDI>=0&&!Windows_Liste[dra_VERDI].살아있음)dra_VERDI=-1;
    if(endre_størrelse_på_dra>=0){
        flytte_endre_størrelse_på(x_koordinat,Y_koordinat);Tavle_peker(x_koordinat,Y_koordinat,잡은모서리==1||잡은모서리==4?2:3);return;
    }
    Tavle_peker(x_koordinat,Y_koordinat,1);
    if(dra_VERDI>=0){
        Terminal_d413d4bc *Vindu=&Windows_Liste[dra_VERDI];
        int 옛가로=Vindu->x_koordinat,옛세로=Vindu->Y_koordinat;
        Vindu->x_koordinat=skillelinje_VERDI(x_koordinat-dra_X,0,보드화면너비()-Vindu->너비);
        Vindu->Y_koordinat=skillelinje_VERDI(Y_koordinat-dra_Y,34,보드화면높이()-Vindu->높이);
        if(옛가로!=(int)Vindu->x_koordinat||옛세로!=(int)Vindu->Y_koordinat)창자리그리기(옛가로,옛세로,Vindu->너비,Vindu->높이,Vindu);
        return;
    }
    extern int skjermbilde_overlegg(int,int,int);
    if(skjermbilde_overlegg(Fokus,x_koordinat,Y_koordinat)){skjermbilde_peker(Fokus,눌림,x_koordinat,Y_koordinat);return;}
    int identifikator_VERDI=가리킨창(x_koordinat,Y_koordinat),모서리=모서리찾기(identifikator_VERDI,x_koordinat,Y_koordinat);
    if(모서리)Tavle_peker(x_koordinat,Y_koordinat,모서리==1||모서리==4?2:3);
    if(눌림&1){
        if(모서리){
            Terminal_d413d4bc *Vindu=&Windows_Liste[identifikator_VERDI];endre_størrelse_på_dra=identifikator_VERDI;잡은모서리=모서리;잡은가로=x_koordinat;잡은세로=Y_koordinat;
            처음가로=Vindu->x_koordinat;처음세로=Vindu->Y_koordinat;처음너비=Vindu->너비;처음높이=Vindu->높이;
            if(identifikator_VERDI!=Fokus)앞으로올리기(identifikator_VERDI);return;
        }
        if(Y_koordinat<32&&x_koordinat>=6&&x_koordinat<142){åpne_oppføring();return;}
        if(Y_koordinat<32&&x_koordinat>=154&&x_koordinat<602){앞으로올리기((x_koordinat-154)/112);return;}
        if(identifikator_VERDI>=0){
            Terminal_d413d4bc *Vindu=&Windows_Liste[identifikator_VERDI];
            if(Y_koordinat<(int)Vindu->Y_koordinat+30&&x_koordinat>=(int)(Vindu->x_koordinat+Vindu->너비)-32){Lukk_vindu(identifikator_VERDI);return;}
            if(identifikator_VERDI!=Fokus)앞으로올리기(identifikator_VERDI);
            if(Y_koordinat<(int)Vindu->Y_koordinat+30){dra_VERDI=identifikator_VERDI;dra_X=x_koordinat-Vindu->x_koordinat;dra_Y=Y_koordinat-Vindu->Y_koordinat;}return;
        }
    }
    if(Fokus>=0&&(눌림&(8|16))){Terminal_oppføring=&Windows_Liste[Fokus];if(눌림&8){unsigned 한도=Terminal_oppføring->맨위;if(한도>Logg_linje_ANTALL-Terminal_oppføring->RAD_ANTALL)한도=Logg_linje_ANTALL-Terminal_oppføring->RAD_ANTALL;Terminal_oppføring->rulle=Terminal_oppføring->rulle+9>한도?한도:Terminal_oppføring->rulle+9;}else Terminal_oppføring->rulle=Terminal_oppføring->rulle<9?0:Terminal_oppføring->rulle-9;다시그리기();}
}
void 터미널바로가기키(unsigned 누름값){if(누름값==1)åpne_oppføring();if(누름값==2&&oppføring_ANTALL)앞으로올리기(ordre_VERDI[0]);if(누름값==3)Lukk_vindu(Fokus);}
maskin_ord Tavle_Terminal(maskin_ord Handling){
    if(Handling==300){if(!Windows_Liste[produksjon].살아있음)return åpne_oppføring();stasjonær_vise=1;다시그리기();return 0;}
    if(Handling==0){Lukk_vindu(Fokus);return 0;}if(Handling==1)return (uint32_t)åpne_oppføring();if(Handling==2)return Fokus>=0;
    if(Handling==9){stasjonær_vise=0;return 0;}if(Handling==7)return oppføring_ANTALL;if(Handling==10)return Fokus+1;if(Handling==11)return produksjon;
    if(Handling==13){Terminal_d413d4bc *Vindu=&Windows_Liste[produksjon];return Vindu->살아있음?(Vindu->RAD_ANTALL<<16)|Vindu->KOLONNER:(19<<16)|68;}
    if(Handling==14){unsigned VERDI=Windows_Liste[produksjon].크기바뀜;Windows_Liste[produksjon].크기바뀜=0;return VERDI;}
    if(Handling==12){unsigned VERDI=informasjonssystemer_Venter;informasjonssystemer_Venter=0;return VERDI;}
    if(Handling>=20&&Handling<24)return Windows_Liste[Handling-20].살아있음;
    if(Handling>=100&&Handling<104){produksjon=Handling-100;Terminal_oppføring=&Windows_Liste[produksjon];return 0;}
    if(Handling>=200&&Handling<204){앞으로올리기(Handling-200);return 0;}
    if(Handling==3){다시그리기();return 0;}Terminal_oppføring=&Windows_Liste[produksjon];if(!Terminal_oppføring->살아있음)return 0;
    if(Handling==4)tømme_Innhold();if(Handling==5||Handling==6){unsigned Forrige_vare=단추들;Terminal_peker(Handling==5?8:16,0,0);단추들=Forrige_vare;}return 1;
}
