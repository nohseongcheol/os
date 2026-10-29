#include "../명명/기계연결이름.h"
#include "skärmbild_info.h"
/* eget 네 Fönster 합성과 UTF-8 kommandotolk. 바뀐 영역의 Slutfört_värde 그림만 표시한다. */
#include <stdint.h>
#include <stddef.h>
typedef uintptr_t dator_Ord;
extern dator_Ord Tavla_bildpunkt(dator_Ord,dator_Ord,dator_Ord),보드화면기억공간(void);
extern void *memset(void *,int,size_t);
extern const unsigned char Terminal_teckensnitt[];
#define 최대열수 237
#define Historik_rad_ANTAL 160
typedef struct {
    uint32_t 글자칸들[Historik_rad_ANTAL][최대열수]; uint8_t 모양들[Historik_rad_ANTAL][최대열수];
    unsigned 너비,높이,KOLUMNER,RAD_ANTAL,크기바뀜;
    unsigned 살아있음,x_koordinat,Y_koordinat,RAD_placera,spalt_placera,맨위,rulla,전경색,배경색,탈출상태,parameter_värde[4],parameter_INDEX,저장행,저장열;
    unsigned 부호없는결과,긴부호없는값,MINSTA_värde,대체화면,가리개보임;
} Terminal;
static Terminal Windows_ange[4];
static int Fokus=-1,utleverans,order_värde[4],post_ANTAL,dra_värde=-1,dra_X,dra_Y;
static unsigned informationsteknik_väntar,단추들,Dator_vy,한글입력;
static const uint32_t 색상들[16]={0x201a15,0x6060df,0x9dcc86,0x80cfea,0xefaf72,0xca96c9,0xceda76,0xede9df,0x858078,0x8888ff,0xb9eba7,0xa5eaff,0xffcc99,0xf0bef1,0xf0f0a0,0xffffff};
extern int 화면보임(int),skärmbild_markör(int,unsigned,int,int);
extern void 화면다시그림(int);
static Terminal *Terminal_post;
static unsigned brett_tecken(unsigned kodpunkt){return kodpunkt>=256?2:1;}
static void 사각영역(unsigned x_koordinat,unsigned Y_koordinat,unsigned 너비값,unsigned 높이값,unsigned 색상){
    Tavla_rektangel_Fyll(x_koordinat,Y_koordinat,너비값,높이값,색상);
}
void Terminal_glyf(unsigned x_koordinat,unsigned Y_koordinat,unsigned kodpunkt,unsigned 전경색,unsigned 배경색){
    unsigned 너비=brett_tecken(kodpunkt)*8;if(kodpunkt==0xffffffffu)return;
    int 왼쪽=x_koordinat,위쪽=Y_koordinat,폭=너비,längd_värde=16;
    if(!보드그림범위(&왼쪽,&위쪽,&폭,&längd_värde))return;
    if(kodpunkt==' '){Tavla_rektangel_Fyll(왼쪽,위쪽,폭,längd_värde,배경색);return;}
    unsigned LETAUPP_INDEX=kodpunkt<65536?kodpunkt:kodpunkt>=0x1f600&&kodpunkt<0x1f650?65536+kodpunkt-0x1f600:0xfffd;
    const unsigned char *teckensnitt_värde=Terminal_teckensnitt+LETAUPP_INDEX*32;
    for(int inmatningsrad=위쪽;inmatningsrad<위쪽+längd_värde;inmatningsrad++){unsigned BITS_ange=teckensnitt_värde[(inmatningsrad-Y_koordinat)*2]*256+teckensnitt_värde[(inmatningsrad-Y_koordinat)*2+1];for(int fack_post=왼쪽;fack_post<왼쪽+폭;fack_post++)Tavla_bildpunkt(fack_post,inmatningsrad,(BITS_ange&(0x8000>>(fack_post-x_koordinat)))?전경색:배경색);}
}
static void namn_tabell(unsigned x_koordinat,unsigned Y_koordinat,const char *sträng_data,unsigned 전경색,unsigned 배경색){while(*sträng_data){unsigned kodpunkt=(unsigned char)*sträng_data++, 남은수=0;if(kodpunkt>=0xc0){남은수=kodpunkt<0xe0?1:kodpunkt<0xf0?2:3;kodpunkt&=(1u<<(6-남은수))-1;while(남은수--&&*sträng_data)kodpunkt=(kodpunkt<<6)|((unsigned char)*sträng_data++&63);}Terminal_glyf(x_koordinat,Y_koordinat,kodpunkt,전경색,배경색);x_koordinat+=brett_tecken(kodpunkt)*8;}}
static unsigned 첫항목(void){return Terminal_post->맨위;}
static int 보이는지(void){return Terminal_post->살아있음&&Fokus>=0&&Terminal_post==&Windows_ange[Fokus]&&!화면보임(Fokus);}
static void Paint_skärmbild(unsigned RAD_placera,unsigned spalt_placera){
    if(!보이는지()||RAD_placera<첫항목()-Terminal_post->rulla||RAD_placera>=첫항목()-Terminal_post->rulla+Terminal_post->RAD_ANTAL||spalt_placera>=Terminal_post->KOLUMNER)return;
    unsigned kodpunkt=Terminal_post->글자칸들[RAD_placera%Historik_rad_ANTAL][spalt_placera],sträng_data=Terminal_post->모양들[RAD_placera%Historik_rad_ANTAL][spalt_placera];
    if(brett_tecken(kodpunkt)==2&&spalt_placera+1>=Terminal_post->KOLUMNER)kodpunkt=' ';
    Terminal_glyf(Terminal_post->x_koordinat+12+spalt_placera*8,Terminal_post->Y_koordinat+36+(RAD_placera-첫항목()+Terminal_post->rulla)*16,kodpunkt?kodpunkt:' ',색상들[sträng_data&15],색상들[sträng_data>>4]);
}
static void cirkumflex_värde(int visa_fönster){if(!보이는지()||Terminal_post->rulla||Terminal_post->spalt_placera>=Terminal_post->KOLUMNER||Terminal_post->RAD_placera<Terminal_post->맨위||Terminal_post->RAD_placera>=Terminal_post->맨위+Terminal_post->RAD_ANTAL)return;
    if(!visa_fönster||!Terminal_post->가리개보임)Paint_skärmbild(Terminal_post->RAD_placera,Terminal_post->spalt_placera);else 사각영역(Terminal_post->x_koordinat+12+Terminal_post->spalt_placera*8,Terminal_post->Y_koordinat+36+(Terminal_post->RAD_placera-Terminal_post->맨위)*16+14,8,2,색상들[Terminal_post->전경색]);}
static void Innehåll_värde(void){
    사각영역(Terminal_post->x_koordinat+12,Terminal_post->Y_koordinat+36,Terminal_post->KOLUMNER*8,Terminal_post->RAD_ANTAL*16,색상들[0]);
    int 가로=Terminal_post->x_koordinat+12,bransch_placera=Terminal_post->Y_koordinat+36,폭=Terminal_post->KOLUMNER*8,längd_värde=Terminal_post->RAD_ANTAL*16;
    if(보드그림범위(&가로,&bransch_placera,&폭,&längd_värde)){
    unsigned 첫줄=(bransch_placera-Terminal_post->Y_koordinat-36)/16,끝줄=(bransch_placera+längd_värde-Terminal_post->Y_koordinat-36+15)/16;
    unsigned 첫칸=(가로-Terminal_post->x_koordinat-12)/8,끝칸=(가로+폭-Terminal_post->x_koordinat-12+7)/8;
    if(첫칸)첫칸--; /* 잘림 gräns_värde 왼쪽에서 시작한 두 fack_post 글자도 그린다. */
    for(unsigned 반환값=첫줄;반환값<끝줄;반환값++)for(unsigned kodpunkt=첫칸;kodpunkt<끝칸;kodpunkt++){
        unsigned RAD_placera=첫항목()-Terminal_post->rulla+반환값,tecken_värde=Terminal_post->글자칸들[RAD_placera%Historik_rad_ANTAL][kodpunkt],sträng_data=Terminal_post->모양들[RAD_placera%Historik_rad_ANTAL][kodpunkt];
        if(brett_tecken(tecken_värde)==2&&kodpunkt+1>=Terminal_post->KOLUMNER)tecken_värde=' ';
        if((tecken_värde==0||tecken_värde==' ')&&(sträng_data>>4)==0)continue;
        Terminal_glyf(Terminal_post->x_koordinat+12+kodpunkt*8,Terminal_post->Y_koordinat+36+반환값*16,tecken_värde?tecken_värde:' ',색상들[sträng_data&15],색상들[sträng_data>>4]);
    }}
    namn_tabell(Terminal_post->x_koordinat+12,Terminal_post->Y_koordinat+Terminal_post->높이-18,Terminal_post->rulla?"PgDn: recent output":Terminal_post->너비>=500?"F6: next | Corner + left drag: resize":"Corner + left drag: resize",0xece8e2,0x403127);cirkumflex_värde(1);
}
static void körning_ram(int identifierare_värde){
    Terminal_post=&Windows_ange[identifierare_värde];
    int 가로=Terminal_post->x_koordinat,bransch_placera=Terminal_post->Y_koordinat,폭=Terminal_post->너비,längd_värde=Terminal_post->높이;
    if(!보드그림범위(&가로,&bransch_placera,&폭,&längd_värde))return;
    사각영역(Terminal_post->x_koordinat,Terminal_post->Y_koordinat,Terminal_post->너비,Terminal_post->높이,0x403127);
    unsigned 색상=identifierare_värde==Fokus?0x905020:0x604438;사각영역(Terminal_post->x_koordinat,Terminal_post->Y_koordinat,Terminal_post->너비,30,색상);
    namn_tabell(Terminal_post->x_koordinat+12,Terminal_post->Y_koordinat+7,"JKOROS Terminal",0xffffff,색상);
    char 수치[2]={(char)('1'+identifierare_värde),0};namn_tabell(Terminal_post->x_koordinat+148,Terminal_post->Y_koordinat+7,수치,0xffffff,색상);
    namn_tabell(Terminal_post->x_koordinat+240,Terminal_post->Y_koordinat+7,Terminal_post->너비>=500?(한글입력?"[SV] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[SV]":"[EN]"),0xffffff,색상);
    사각영역(Terminal_post->x_koordinat+Terminal_post->너비-32,Terminal_post->Y_koordinat+4,26,22,0x5555b8);namn_tabell(Terminal_post->x_koordinat+Terminal_post->너비-24,Terminal_post->Y_koordinat+7,"X",0xffffff,0x5555b8);
    Innehåll_värde();
}
static void Rita_scen(void){
    if(!Dator_vy)return;사각영역(0,0,보드화면너비(),보드화면높이(),0x302018);사각영역(0,0,보드화면너비(),32,0x403127);
    사각영역(6,4,136,24,0x905020);namn_tabell(14,8,"+ New terminal",0xffffff,0x905020);
    for(int 순번=0;순번<4;순번++)if(Windows_ange[순번].살아있음){unsigned kodpunkt=Fokus==순번?0x905020:0x604438;사각영역(154+순번*112,4,106,24,kodpunkt);namn_tabell(160+순번*112,8,"Terminal",0xffffff,kodpunkt);char sträng_data[2]={(char)('1'+순번),0};namn_tabell(232+순번*112,8,sträng_data,0xffffff,kodpunkt);}
    if(!post_ANTAL)namn_tabell(140,210,"Click + New terminal to start",0xede9df,0x302018);
    for(int 순번=0;순번<post_ANTAL;순번++)körning_ram(order_värde[순번]);화면다시그림(Fokus);Terminal_post=&Windows_ange[utleverans];
}
static void Paint_område(int 가로,int bransch_placera,int 폭,int längd_värde){
    if(!Dator_vy||!보드그림범위(&가로,&bransch_placera,&폭,&längd_värde))return;
    for(int inmatningsrad=bransch_placera;inmatningsrad<bransch_placera+längd_värde;inmatningsrad+=32){
        int 띠높이=bransch_placera+längd_värde-inmatningsrad;if(띠높이>32)띠높이=32;
        if(Tavla_START_ritning(가로,inmatningsrad,폭,띠높이)){Rita_scen();Tavla_slut_ritning();}
    }
}
static void 다시그리기(void){Paint_område(0,0,보드화면너비(),보드화면높이());}
/* 서로 겹치지 않는 새 Fönster 영역과 Föregående_objekt 자리의 네 띠를 복구한다. */
static void 창자리그리기(int 가로,int bransch_placera,int 폭,int längd_värde,Terminal *Fönster){
    int 왼쪽=가로>(int)Fönster->x_koordinat?가로:(int)Fönster->x_koordinat;
    int 위쪽=bransch_placera>(int)Fönster->Y_koordinat?bransch_placera:(int)Fönster->Y_koordinat;
    int HÖGER=가로+폭<(int)(Fönster->x_koordinat+Fönster->너비)?가로+폭:(int)(Fönster->x_koordinat+Fönster->너비);
    int 아래쪽=bransch_placera+längd_värde<(int)(Fönster->Y_koordinat+Fönster->높이)?bransch_placera+längd_värde:(int)(Fönster->Y_koordinat+Fönster->높이);
    Paint_område(Fönster->x_koordinat,Fönster->Y_koordinat,Fönster->너비,Fönster->높이);
    if(왼쪽>=HÖGER||위쪽>=아래쪽){Paint_område(가로,bransch_placera,폭,längd_värde);return;}
    Paint_område(가로,bransch_placera,폭,위쪽-bransch_placera);
    Paint_område(가로,아래쪽,폭,bransch_placera+längd_värde-아래쪽);
    Paint_område(가로,위쪽,왼쪽-가로,아래쪽-위쪽);
    Paint_område(HÖGER,위쪽,가로+폭-HÖGER,아래쪽-위쪽);
}
static void signal_Fokus(void){informationsteknik_väntar=(informationsteknik_väntar&~15u)|(unsigned)(Fokus+1)|0x10000;}
void Terminal_indata_läge(unsigned 한글여부){
    한글입력=한글여부!=0;
    /* Update title bars only: a mode switch must not erase an EL0 drawing. */
    if(Fokus>=0){
        Terminal *fönster_post=&Windows_ange[Fokus];
        namn_tabell(fönster_post->x_koordinat+240,fönster_post->Y_koordinat+7,fönster_post->너비>=500?(한글입력?"[SV] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[SV]":"[EN]"),0xffffff,0x905020);
    }
}
static void 앞으로올리기(int identifierare_värde){if(identifierare_värde<0||identifierare_värde>=4||!Windows_ange[identifierare_värde].살아있음)return;int aktuellt_placera=0;while(aktuellt_placera<post_ANTAL&&order_värde[aktuellt_placera]!=identifierare_värde)aktuellt_placera++;for(;aktuellt_placera+1<post_ANTAL;aktuellt_placera++)order_värde[aktuellt_placera]=order_värde[aktuellt_placera+1];order_värde[post_ANTAL-1]=identifierare_värde;Fokus=identifierare_värde;signal_Fokus();다시그리기();}
static void 빈칸채우기(unsigned RAD_placera){for(unsigned kodpunkt=0;kodpunkt<최대열수;kodpunkt++){Terminal_post->글자칸들[RAD_placera%Historik_rad_ANTAL][kodpunkt]=0;Terminal_post->모양들[RAD_placera%Historik_rad_ANTAL][kodpunkt]=Terminal_post->전경색|(Terminal_post->배경색<<4);}}
static void rensa_Innehåll(void){Terminal_post->RAD_placera=Terminal_post->spalt_placera=Terminal_post->맨위=Terminal_post->rulla=0;for(unsigned 반환값=0;반환값<Historik_rad_ANTAL;반환값++)빈칸채우기(반환값);if(보이는지())Innehåll_värde();}
static int Skapa_post(void){
    if(!보드화면기억공간())return -19;int identifierare_värde=0;while(identifierare_värde<4&&Windows_ange[identifierare_värde].살아있음)identifierare_värde++;if(identifierare_värde==4)return -28;
    Dator_vy=1;Terminal_post=&Windows_ange[identifierare_värde];memset(Terminal_post,0,sizeof(*Terminal_post));Terminal_post->살아있음=1;Terminal_post->너비=568;Terminal_post->높이=360;Terminal_post->KOLUMNER=68;Terminal_post->RAD_ANTAL=19;Terminal_post->x_koordinat=12+identifierare_värde*16;Terminal_post->Y_koordinat=48+identifierare_värde*18;Terminal_post->전경색=7;Terminal_post->가리개보임=1;
    for(unsigned 반환값=0;반환값<Historik_rad_ANTAL;반환값++)빈칸채우기(반환값);order_värde[post_ANTAL++]=identifierare_värde;Fokus=identifierare_värde;informationsteknik_väntar|=1u<<(4+identifierare_värde);signal_Fokus();다시그리기();return identifierare_värde+1;
}
static void Stäng_fönster(int identifierare_värde){
    if(identifierare_värde<0||identifierare_värde>=4||!Windows_ange[identifierare_värde].살아있음)return;Windows_ange[identifierare_värde].살아있음=0;informationsteknik_väntar|=1u<<(8+identifierare_värde);
    int aktuellt_placera=0;while(aktuellt_placera<post_ANTAL&&order_värde[aktuellt_placera]!=identifierare_värde)aktuellt_placera++;for(;aktuellt_placera+1<post_ANTAL;aktuellt_placera++)order_värde[aktuellt_placera]=order_värde[aktuellt_placera+1];post_ANTAL--;
    if(Fokus==identifierare_värde)Fokus=post_ANTAL?order_värde[post_ANTAL-1]:-1;signal_Fokus();다시그리기();
}
static void 줄바꿈(void){Terminal_post->spalt_placera=0;Terminal_post->RAD_placera++;if(Terminal_post->RAD_placera>=Terminal_post->맨위+Terminal_post->RAD_ANTAL){Terminal_post->맨위++;빈칸채우기(Terminal_post->RAD_placera);if(보이는지())Innehåll_värde();}}
static void kodpunkt_451f2815(unsigned kodpunkt){
    if(kodpunkt==13){Terminal_post->spalt_placera=0;return;}if(kodpunkt==10){줄바꿈();return;}if(kodpunkt==8){if(Terminal_post->spalt_placera)Terminal_post->spalt_placera--;return;}
    if(kodpunkt==9){unsigned objekt_ANTAL=8-Terminal_post->spalt_placera%8;while(objekt_ANTAL--)kodpunkt_451f2815(' ');return;}if(kodpunkt<32||kodpunkt==127)return;
    unsigned 너비값=brett_tecken(kodpunkt);if(Terminal_post->spalt_placera+너비값>Terminal_post->KOLUMNER)줄바꿈();
    if(Terminal_post->글자칸들[Terminal_post->RAD_placera%Historik_rad_ANTAL][Terminal_post->spalt_placera]==0xffffffffu&&Terminal_post->spalt_placera){Terminal_post->글자칸들[Terminal_post->RAD_placera%Historik_rad_ANTAL][Terminal_post->spalt_placera-1]=' ';Paint_skärmbild(Terminal_post->RAD_placera,Terminal_post->spalt_placera-1);}
    if(brett_tecken(Terminal_post->글자칸들[Terminal_post->RAD_placera%Historik_rad_ANTAL][Terminal_post->spalt_placera])==2&&Terminal_post->spalt_placera+1<Terminal_post->KOLUMNER){Terminal_post->글자칸들[Terminal_post->RAD_placera%Historik_rad_ANTAL][Terminal_post->spalt_placera+1]=' ';Paint_skärmbild(Terminal_post->RAD_placera,Terminal_post->spalt_placera+1);}
    Terminal_post->글자칸들[Terminal_post->RAD_placera%Historik_rad_ANTAL][Terminal_post->spalt_placera]=kodpunkt;Terminal_post->모양들[Terminal_post->RAD_placera%Historik_rad_ANTAL][Terminal_post->spalt_placera]=Terminal_post->전경색|(Terminal_post->배경색<<4);
    if(너비값==2)Terminal_post->글자칸들[Terminal_post->RAD_placera%Historik_rad_ANTAL][Terminal_post->spalt_placera+1]=0xffffffffu;
    Paint_skärmbild(Terminal_post->RAD_placera,Terminal_post->spalt_placera);Terminal_post->spalt_placera+=너비값;
}
static void handtag_kontroll_SEKVENS(unsigned kodpunkt){
    unsigned objekt_ANTAL=Terminal_post->parameter_värde[0]?Terminal_post->parameter_värde[0]:1;
    if(kodpunkt=='m')for(unsigned 순번=0;순번<=Terminal_post->parameter_INDEX;순번++){unsigned data_placera=Terminal_post->parameter_värde[순번];if(!data_placera){Terminal_post->전경색=7;Terminal_post->배경색=0;}if(data_placera==1&&Terminal_post->전경색<8)Terminal_post->전경색+=8;if(data_placera==7){unsigned 유지=Terminal_post->전경색;Terminal_post->전경색=Terminal_post->배경색;Terminal_post->배경색=유지;}if(data_placera>=30&&data_placera<=37)Terminal_post->전경색=data_placera-30;if(data_placera>=90&&data_placera<=97)Terminal_post->전경색=data_placera-90+8;if(data_placera>=40&&data_placera<=47)Terminal_post->배경색=data_placera-40;if(data_placera>=100&&data_placera<=107)Terminal_post->배경색=data_placera-100+8;if(data_placera==39)Terminal_post->전경색=7;if(data_placera==49)Terminal_post->배경색=0;}
    if(kodpunkt=='J'&&(Terminal_post->parameter_värde[0]==2||Terminal_post->parameter_värde[0]==3))rensa_Innehåll();
    if(kodpunkt=='K'){unsigned 출발위치=Terminal_post->parameter_värde[0]==2?0:Terminal_post->spalt_placera,도착위치=Terminal_post->parameter_värde[0]==1?Terminal_post->spalt_placera+1:Terminal_post->KOLUMNER;if(Terminal_post->parameter_värde[0]==1)출발위치=0;for(unsigned 순번=출발위치;순번<도착위치&&순번<Terminal_post->KOLUMNER;순번++){
        unsigned RAD_värde=Terminal_post->RAD_placera%Historik_rad_ANTAL,tecken_värde=Terminal_post->글자칸들[RAD_värde][순번],form_värde=Terminal_post->전경색|(Terminal_post->배경색<<4);
        /* 넓은 vi 화면에서도 이미 빈 칸의 teckensnitt_värde 화소를 되풀이해 칠하지 않는다. */
        int 바뀜=(tecken_värde!=0&&tecken_värde!=' ')||Terminal_post->모양들[RAD_värde][순번]!=form_värde;
        Terminal_post->글자칸들[RAD_värde][순번]=' ';Terminal_post->모양들[RAD_värde][순번]=form_värde;
        if(바뀜)Paint_skärmbild(Terminal_post->RAD_placera,순번);
    }}
    if(kodpunkt=='D')Terminal_post->spalt_placera=objekt_ANTAL>Terminal_post->spalt_placera?0:Terminal_post->spalt_placera-objekt_ANTAL;if(kodpunkt=='C')Terminal_post->spalt_placera=Terminal_post->spalt_placera+objekt_ANTAL>=Terminal_post->KOLUMNER?Terminal_post->KOLUMNER-1:Terminal_post->spalt_placera+objekt_ANTAL;
    if(kodpunkt=='G')Terminal_post->spalt_placera=objekt_ANTAL>Terminal_post->KOLUMNER?Terminal_post->KOLUMNER-1:objekt_ANTAL-1;if(kodpunkt=='A')Terminal_post->RAD_placera=objekt_ANTAL>Terminal_post->RAD_placera-Terminal_post->맨위?Terminal_post->맨위:Terminal_post->RAD_placera-objekt_ANTAL;
    if(kodpunkt=='B')Terminal_post->RAD_placera=Terminal_post->RAD_placera+objekt_ANTAL>=Terminal_post->맨위+Terminal_post->RAD_ANTAL?Terminal_post->맨위+Terminal_post->RAD_ANTAL-1:Terminal_post->RAD_placera+objekt_ANTAL;
    if(kodpunkt=='H'||kodpunkt=='f'){Terminal_post->RAD_placera=Terminal_post->맨위+(objekt_ANTAL>Terminal_post->RAD_ANTAL?Terminal_post->RAD_ANTAL:objekt_ANTAL)-1;unsigned x_koordinat=Terminal_post->parameter_värde[1]?Terminal_post->parameter_värde[1]:1;Terminal_post->spalt_placera=(x_koordinat>Terminal_post->KOLUMNER?Terminal_post->KOLUMNER:x_koordinat)-1;}
    if(kodpunkt=='s'){Terminal_post->저장행=Terminal_post->RAD_placera;Terminal_post->저장열=Terminal_post->spalt_placera;}if(kodpunkt=='u'){Terminal_post->RAD_placera=Terminal_post->저장행;Terminal_post->spalt_placera=Terminal_post->저장열<Terminal_post->KOLUMNER?Terminal_post->저장열:Terminal_post->KOLUMNER-1;}
    if((kodpunkt=='h'||kodpunkt=='l')&&Terminal_post->parameter_värde[0]==25)Terminal_post->가리개보임=kodpunkt=='h';
}
void Terminal_byte(unsigned SEKUND_värde){
    Terminal_post=&Windows_ange[utleverans];if(!Terminal_post->살아있음)return;cirkumflex_värde(0);if(Terminal_post->rulla){Terminal_post->rulla=0;if(보이는지())Innehåll_värde();}
    if(Terminal_post->탈출상태==1){Terminal_post->탈출상태=SEKUND_värde=='['?2:0;Terminal_post->parameter_INDEX=0;for(unsigned 순번=0;순번<4;순번++)Terminal_post->parameter_värde[순번]=0;}
    else if(Terminal_post->탈출상태==2){if(SEKUND_värde=='?'){}else if(SEKUND_värde>='0'&&SEKUND_värde<='9'){if(Terminal_post->parameter_värde[Terminal_post->parameter_INDEX]<10000)Terminal_post->parameter_värde[Terminal_post->parameter_INDEX]=Terminal_post->parameter_värde[Terminal_post->parameter_INDEX]*10+SEKUND_värde-'0';}else if(SEKUND_värde==';'&&Terminal_post->parameter_INDEX<3)Terminal_post->parameter_INDEX++;else{handtag_kontroll_SEKVENS(SEKUND_värde);Terminal_post->탈출상태=0;}}
    else if(SEKUND_värde==27){Terminal_post->긴부호없는값=0;Terminal_post->탈출상태=1;}else{
        if(Terminal_post->긴부호없는값&&(SEKUND_värde&0xc0)!=0x80){Terminal_post->긴부호없는값=0;kodpunkt_451f2815(0xfffd);}
        if(Terminal_post->긴부호없는값){Terminal_post->부호없는결과=Terminal_post->부호없는결과*64+(SEKUND_värde&63);if(--Terminal_post->긴부호없는값==0)kodpunkt_451f2815(Terminal_post->부호없는결과<Terminal_post->MINSTA_värde||Terminal_post->부호없는결과>0x10ffff||(Terminal_post->부호없는결과>=0xd800&&Terminal_post->부호없는결과<=0xdfff)?0xfffd:Terminal_post->부호없는결과);}
        else if(SEKUND_värde<128)kodpunkt_451f2815(SEKUND_värde);else if(SEKUND_värde>=0xc2&&SEKUND_värde<=0xf4){Terminal_post->긴부호없는값=SEKUND_värde<0xe0?1:SEKUND_värde<0xf0?2:3;Terminal_post->부호없는결과=SEKUND_värde&((1u<<(6-Terminal_post->긴부호없는값))-1);Terminal_post->MINSTA_värde=Terminal_post->긴부호없는값==1?128:Terminal_post->긴부호없는값==2?2048:65536;}else kodpunkt_451f2815(0xfffd);
    }cirkumflex_värde(1);
}
int Terminal_väntar(void){return informationsteknik_väntar!=0;}
/* 모서리 INDEX: 1 좌상, 2 우상, 3 좌하, 4 우하. */
static int ändra_storlek_dra=-1,잡은모서리,잡은가로,잡은세로,처음가로,처음세로,처음너비,처음높이;
static int 가리킨창(int 가로,int bransch_placera) {
    for(int SEKVENS_värde=post_ANTAL-1;SEKVENS_värde>=0;SEKVENS_värde--){
        int identifierare_värde=order_värde[SEKVENS_värde];Terminal *Fönster=&Windows_ange[identifierare_värde];
        if(가로>=(int)Fönster->x_koordinat&&bransch_placera>=(int)Fönster->Y_koordinat&&
           가로<(int)(Fönster->x_koordinat+Fönster->너비)&&bransch_placera<(int)(Fönster->Y_koordinat+Fönster->높이))return identifierare_värde;
    }return -1;
}
static int 모서리찾기(int identifierare_värde,int 가로,int bransch_placera) {
    if(identifierare_värde<0)return 0;Terminal *Fönster=&Windows_ange[identifierare_värde];
    int 왼쪽=가로<(int)Fönster->x_koordinat+8,HÖGER=가로>=(int)(Fönster->x_koordinat+Fönster->너비)-8;
    int 위쪽=bransch_placera<(int)Fönster->Y_koordinat+8,아래쪽=bransch_placera>=(int)(Fönster->Y_koordinat+Fönster->높이)-8;
    return (왼쪽||HÖGER)&&(위쪽||아래쪽)?1+HÖGER+아래쪽*2:0;
}
static int avgränsare_värde(int värde,int 최소,int 최대){return värde<최소?최소:värde>최대?최대:värde;}
static void flytta_ändra_storlek(int 가로,int bransch_placera) {
    Terminal *Fönster=&Windows_ange[ändra_storlek_dra];int 왼쪽=처음가로,위쪽=처음세로,HÖGER=처음가로+처음너비,아래쪽=처음세로+처음높이;
    if(잡은모서리==1||잡은모서리==3)왼쪽=avgränsare_värde(처음가로+가로-잡은가로,0,HÖGER-360);
    else HÖGER=avgränsare_värde(처음가로+처음너비+가로-잡은가로,왼쪽+360,보드화면너비());
    if(잡은모서리<=2)위쪽=avgränsare_värde(처음세로+bransch_placera-잡은세로,34,아래쪽-216);
    else 아래쪽=avgränsare_värde(처음세로+처음높이+bransch_placera-잡은세로,위쪽+216,보드화면높이());
    unsigned KOLUMNER=(HÖGER-왼쪽-24)/8,RAD_ANTAL=(아래쪽-위쪽-56)/16;
    if(Fönster->KOLUMNER!=KOLUMNER||Fönster->RAD_ANTAL!=RAD_ANTAL){
        Fönster->크기바뀜=1;Fönster->KOLUMNER=KOLUMNER;Fönster->RAD_ANTAL=RAD_ANTAL;
        if(Fönster->spalt_placera>=KOLUMNER)Fönster->spalt_placera=KOLUMNER-1;
        if(Fönster->RAD_placera>=Fönster->맨위+RAD_ANTAL)Fönster->맨위=Fönster->RAD_placera-RAD_ANTAL+1;
        unsigned 한도=Fönster->맨위;if(한도>Historik_rad_ANTAL-RAD_ANTAL)한도=Historik_rad_ANTAL-RAD_ANTAL;
        if(Fönster->rulla>한도)Fönster->rulla=한도;
    }
    int 옛가로=Fönster->x_koordinat,옛세로=Fönster->Y_koordinat,옛폭=Fönster->너비,옛길이=Fönster->높이;
    if(옛가로==왼쪽&&옛세로==위쪽&&옛폭==HÖGER-왼쪽&&옛길이==아래쪽-위쪽)return;
    Fönster->x_koordinat=왼쪽;Fönster->Y_koordinat=위쪽;Fönster->너비=HÖGER-왼쪽;Fönster->높이=아래쪽-위쪽;
    창자리그리기(옛가로,옛세로,옛폭,옛길이,Fönster);
}
void Terminal_markör(unsigned Nästa_objekt,int x_koordinat,int Y_koordinat){
    unsigned 눌림=Nästa_objekt&~단추들;단추들=Nästa_objekt;
    if(!Dator_vy){dra_värde=-1;ändra_storlek_dra=-1;Tavla_markör(x_koordinat,Y_koordinat,1);return;}
    if(!(Nästa_objekt&1)){dra_värde=-1;ändra_storlek_dra=-1;}
    if(ändra_storlek_dra>=0&&!Windows_ange[ändra_storlek_dra].살아있음)ändra_storlek_dra=-1;
    if(dra_värde>=0&&!Windows_ange[dra_värde].살아있음)dra_värde=-1;
    if(ändra_storlek_dra>=0){
        flytta_ändra_storlek(x_koordinat,Y_koordinat);Tavla_markör(x_koordinat,Y_koordinat,잡은모서리==1||잡은모서리==4?2:3);return;
    }
    Tavla_markör(x_koordinat,Y_koordinat,1);
    if(dra_värde>=0){
        Terminal *Fönster=&Windows_ange[dra_värde];
        int 옛가로=Fönster->x_koordinat,옛세로=Fönster->Y_koordinat;
        Fönster->x_koordinat=avgränsare_värde(x_koordinat-dra_X,0,보드화면너비()-Fönster->너비);
        Fönster->Y_koordinat=avgränsare_värde(Y_koordinat-dra_Y,34,보드화면높이()-Fönster->높이);
        if(옛가로!=(int)Fönster->x_koordinat||옛세로!=(int)Fönster->Y_koordinat)창자리그리기(옛가로,옛세로,Fönster->너비,Fönster->높이,Fönster);
        return;
    }
    extern int skärmbild_överlägg(int,int,int);
    if(skärmbild_överlägg(Fokus,x_koordinat,Y_koordinat)){skärmbild_markör(Fokus,눌림,x_koordinat,Y_koordinat);return;}
    int identifierare_värde=가리킨창(x_koordinat,Y_koordinat),모서리=모서리찾기(identifierare_värde,x_koordinat,Y_koordinat);
    if(모서리)Tavla_markör(x_koordinat,Y_koordinat,모서리==1||모서리==4?2:3);
    if(눌림&1){
        if(모서리){
            Terminal *Fönster=&Windows_ange[identifierare_värde];ändra_storlek_dra=identifierare_värde;잡은모서리=모서리;잡은가로=x_koordinat;잡은세로=Y_koordinat;
            처음가로=Fönster->x_koordinat;처음세로=Fönster->Y_koordinat;처음너비=Fönster->너비;처음높이=Fönster->높이;
            if(identifierare_värde!=Fokus)앞으로올리기(identifierare_värde);return;
        }
        if(Y_koordinat<32&&x_koordinat>=6&&x_koordinat<142){Skapa_post();return;}
        if(Y_koordinat<32&&x_koordinat>=154&&x_koordinat<602){앞으로올리기((x_koordinat-154)/112);return;}
        if(identifierare_värde>=0){
            Terminal *Fönster=&Windows_ange[identifierare_värde];
            if(Y_koordinat<(int)Fönster->Y_koordinat+30&&x_koordinat>=(int)(Fönster->x_koordinat+Fönster->너비)-32){Stäng_fönster(identifierare_värde);return;}
            if(identifierare_värde!=Fokus)앞으로올리기(identifierare_värde);
            if(Y_koordinat<(int)Fönster->Y_koordinat+30){dra_värde=identifierare_värde;dra_X=x_koordinat-Fönster->x_koordinat;dra_Y=Y_koordinat-Fönster->Y_koordinat;}return;
        }
    }
    if(Fokus>=0&&(눌림&(8|16))){Terminal_post=&Windows_ange[Fokus];if(눌림&8){unsigned 한도=Terminal_post->맨위;if(한도>Historik_rad_ANTAL-Terminal_post->RAD_ANTAL)한도=Historik_rad_ANTAL-Terminal_post->RAD_ANTAL;Terminal_post->rulla=Terminal_post->rulla+9>한도?한도:Terminal_post->rulla+9;}else Terminal_post->rulla=Terminal_post->rulla<9?0:Terminal_post->rulla-9;다시그리기();}
}
void 터미널바로가기키(unsigned 누름값){if(누름값==1)Skapa_post();if(누름값==2&&post_ANTAL)앞으로올리기(order_värde[0]);if(누름값==3)Stäng_fönster(Fokus);}
dator_Ord Tavla_Terminal(dator_Ord Åtgärd){
    if(Åtgärd==300){if(!Windows_ange[utleverans].살아있음)return Skapa_post();Dator_vy=1;다시그리기();return 0;}
    if(Åtgärd==0){Stäng_fönster(Fokus);return 0;}if(Åtgärd==1)return (uint32_t)Skapa_post();if(Åtgärd==2)return Fokus>=0;
    if(Åtgärd==9){Dator_vy=0;return 0;}if(Åtgärd==7)return post_ANTAL;if(Åtgärd==10)return Fokus+1;if(Åtgärd==11)return utleverans;
    if(Åtgärd==13){Terminal *Fönster=&Windows_ange[utleverans];return Fönster->살아있음?(Fönster->RAD_ANTAL<<16)|Fönster->KOLUMNER:(19<<16)|68;}
    if(Åtgärd==14){unsigned värde=Windows_ange[utleverans].크기바뀜;Windows_ange[utleverans].크기바뀜=0;return värde;}
    if(Åtgärd==12){unsigned värde=informationsteknik_väntar;informationsteknik_väntar=0;return värde;}
    if(Åtgärd>=20&&Åtgärd<24)return Windows_ange[Åtgärd-20].살아있음;
    if(Åtgärd>=100&&Åtgärd<104){utleverans=Åtgärd-100;Terminal_post=&Windows_ange[utleverans];return 0;}
    if(Åtgärd>=200&&Åtgärd<204){앞으로올리기(Åtgärd-200);return 0;}
    if(Åtgärd==3){다시그리기();return 0;}Terminal_post=&Windows_ange[utleverans];if(!Terminal_post->살아있음)return 0;
    if(Åtgärd==4)rensa_Innehåll();if(Åtgärd==5||Åtgärd==6){unsigned Föregående_objekt=단추들;Terminal_markör(Åtgärd==5?8:16,0,0);단추들=Föregående_objekt;}return 1;
}
