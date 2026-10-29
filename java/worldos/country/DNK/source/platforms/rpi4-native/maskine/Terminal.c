#include "../명명/기계연결이름.h"
#include "skærmbillede_info.h"
/* eget 네 Vindue 합성과 UTF-8 Terminal. 바뀐 영역의 fuldført_VÆRDI 그림만 표시한다. */
#include <stdint.h>
#include <stddef.h>
typedef uintptr_t maskine_Ord;
extern maskine_Ord Tavle_pixel(maskine_Ord,maskine_Ord,maskine_Ord),보드화면기억공간(void);
extern void *memset(void *,int,size_t);
extern const unsigned char Terminal_skrifttype[];
#define 최대열수 237
#define Historik_linje_TÆL 160
typedef struct {
    uint32_t 글자칸들[Historik_linje_TÆL][최대열수]; uint8_t 모양들[Historik_linje_TÆL][최대열수];
    unsigned 너비,높이,KOLONNER,post_TÆL,크기바뀜;
    unsigned 살아있음,X_koordinat,Y_koordinat,post_placere,KOLONNE_placere,맨위,rulle,전경색,배경색,탈출상태,parameter_VÆRDI[4],parameter_INDEKS,저장행,저장열;
    unsigned 부호없는결과,긴부호없는값,MINDSTE_VÆRDI,대체화면,가리개보임;
} Terminal_d413d4bc;
static Terminal_d413d4bc Windows_Liste[4];
static int Fokus=-1,produktoutput,ordre_VÆRDI[4],post_TÆL_8f7753a1,trække_VÆRDI=-1,trække_X,trække_Y;
static unsigned it_Afventer,단추들,desktop_Visning,한글입력;
static const uint32_t 색상들[16]={0x201a15,0x6060df,0x9dcc86,0x80cfea,0xefaf72,0xca96c9,0xceda76,0xede9df,0x858078,0x8888ff,0xb9eba7,0xa5eaff,0xffcc99,0xf0bef1,0xf0f0a0,0xffffff};
extern int 화면보임(int),skærmbillede_markør(int,unsigned,int,int);
extern void 화면다시그림(int);
static Terminal_d413d4bc *Terminal_post;
static unsigned bredt_tegn(unsigned tegnkode){return tegnkode>=256?2:1;}
static void 사각영역(unsigned X_koordinat,unsigned Y_koordinat,unsigned 너비값,unsigned 높이값,unsigned 색상){
    Tavle_rektangel_udfyld(X_koordinat,Y_koordinat,너비값,높이값,색상);
}
void Terminal_specialtegn(unsigned X_koordinat,unsigned Y_koordinat,unsigned tegnkode,unsigned 전경색,unsigned 배경색){
    unsigned 너비=bredt_tegn(tegnkode)*8;if(tegnkode==0xffffffffu)return;
    int 왼쪽=X_koordinat,위쪽=Y_koordinat,폭=너비,varighed_VÆRDI=16;
    if(!보드그림범위(&왼쪽,&위쪽,&폭,&varighed_VÆRDI))return;
    if(tegnkode==' '){Tavle_rektangel_udfyld(왼쪽,위쪽,폭,varighed_VÆRDI,배경색);return;}
    unsigned Opslag_INDEKS=tegnkode<65536?tegnkode:tegnkode>=0x1f600&&tegnkode<0x1f650?65536+tegnkode-0x1f600:0xfffd;
    const unsigned char *skrifttype_VÆRDI=Terminal_skrifttype+Opslag_INDEKS*32;
    for(int Linje=위쪽;Linje<위쪽+varighed_VÆRDI;Linje++){unsigned BITS_Liste=skrifttype_VÆRDI[(Linje-Y_koordinat)*2]*256+skrifttype_VÆRDI[(Linje-Y_koordinat)*2+1];for(int udvidelsesstik_post=왼쪽;udvidelsesstik_post<왼쪽+폭;udvidelsesstik_post++)Tavle_pixel(udvidelsesstik_post,Linje,(BITS_Liste&(0x8000>>(udvidelsesstik_post-X_koordinat)))?전경색:배경색);}
}
static void navn_tabel(unsigned X_koordinat,unsigned Y_koordinat,const char *streng_data,unsigned 전경색,unsigned 배경색){while(*streng_data){unsigned tegnkode=(unsigned char)*streng_data++, 남은수=0;if(tegnkode>=0xc0){남은수=tegnkode<0xe0?1:tegnkode<0xf0?2:3;tegnkode&=(1u<<(6-남은수))-1;while(남은수--&&*streng_data)tegnkode=(tegnkode<<6)|((unsigned char)*streng_data++&63);}Terminal_specialtegn(X_koordinat,Y_koordinat,tegnkode,전경색,배경색);X_koordinat+=bredt_tegn(tegnkode)*8;}}
static unsigned 첫항목(void){return Terminal_post->맨위;}
static int 보이는지(void){return Terminal_post->살아있음&&Fokus>=0&&Terminal_post==&Windows_Liste[Fokus]&&!화면보임(Fokus);}
static void Paint_skærmbillede(unsigned post_placere,unsigned KOLONNE_placere){
    if(!보이는지()||post_placere<첫항목()-Terminal_post->rulle||post_placere>=첫항목()-Terminal_post->rulle+Terminal_post->post_TÆL||KOLONNE_placere>=Terminal_post->KOLONNER)return;
    unsigned tegnkode=Terminal_post->글자칸들[post_placere%Historik_linje_TÆL][KOLONNE_placere],streng_data=Terminal_post->모양들[post_placere%Historik_linje_TÆL][KOLONNE_placere];
    if(bredt_tegn(tegnkode)==2&&KOLONNE_placere+1>=Terminal_post->KOLONNER)tegnkode=' ';
    Terminal_specialtegn(Terminal_post->X_koordinat+12+KOLONNE_placere*8,Terminal_post->Y_koordinat+36+(post_placere-첫항목()+Terminal_post->rulle)*16,tegnkode?tegnkode:' ',색상들[streng_data&15],색상들[streng_data>>4]);
}
static void cirkumfleks_VÆRDI(int vise_vindue){if(!보이는지()||Terminal_post->rulle||Terminal_post->KOLONNE_placere>=Terminal_post->KOLONNER||Terminal_post->post_placere<Terminal_post->맨위||Terminal_post->post_placere>=Terminal_post->맨위+Terminal_post->post_TÆL)return;
    if(!vise_vindue||!Terminal_post->가리개보임)Paint_skærmbillede(Terminal_post->post_placere,Terminal_post->KOLONNE_placere);else 사각영역(Terminal_post->X_koordinat+12+Terminal_post->KOLONNE_placere*8,Terminal_post->Y_koordinat+36+(Terminal_post->post_placere-Terminal_post->맨위)*16+14,8,2,색상들[Terminal_post->전경색]);}
static void Indhold_VÆRDI(void){
    사각영역(Terminal_post->X_koordinat+12,Terminal_post->Y_koordinat+36,Terminal_post->KOLONNER*8,Terminal_post->post_TÆL*16,색상들[0]);
    int 가로=Terminal_post->X_koordinat+12,Lodret_placere=Terminal_post->Y_koordinat+36,폭=Terminal_post->KOLONNER*8,varighed_VÆRDI=Terminal_post->post_TÆL*16;
    if(보드그림범위(&가로,&Lodret_placere,&폭,&varighed_VÆRDI)){
    unsigned 첫줄=(Lodret_placere-Terminal_post->Y_koordinat-36)/16,끝줄=(Lodret_placere+varighed_VÆRDI-Terminal_post->Y_koordinat-36+15)/16;
    unsigned 첫칸=(가로-Terminal_post->X_koordinat-12)/8,끝칸=(가로+폭-Terminal_post->X_koordinat-12+7)/8;
    if(첫칸)첫칸--; /* 잘림 grænse_VÆRDI 왼쪽에서 시작한 두 udvidelsesstik_post 글자도 그린다. */
    for(unsigned 반환값=첫줄;반환값<끝줄;반환값++)for(unsigned tegnkode=첫칸;tegnkode<끝칸;tegnkode++){
        unsigned post_placere=첫항목()-Terminal_post->rulle+반환값,tegn_VÆRDI=Terminal_post->글자칸들[post_placere%Historik_linje_TÆL][tegnkode],streng_data=Terminal_post->모양들[post_placere%Historik_linje_TÆL][tegnkode];
        if(bredt_tegn(tegn_VÆRDI)==2&&tegnkode+1>=Terminal_post->KOLONNER)tegn_VÆRDI=' ';
        if((tegn_VÆRDI==0||tegn_VÆRDI==' ')&&(streng_data>>4)==0)continue;
        Terminal_specialtegn(Terminal_post->X_koordinat+12+tegnkode*8,Terminal_post->Y_koordinat+36+반환값*16,tegn_VÆRDI?tegn_VÆRDI:' ',색상들[streng_data&15],색상들[streng_data>>4]);
    }}
    navn_tabel(Terminal_post->X_koordinat+12,Terminal_post->Y_koordinat+Terminal_post->높이-18,Terminal_post->rulle?"PgDn: recent output":Terminal_post->너비>=500?"F6: next | Corner + left drag: resize":"Corner + left drag: resize",0xece8e2,0x403127);cirkumfleks_VÆRDI(1);
}
static void udførelse_ramme(int identifikator_VÆRDI){
    Terminal_post=&Windows_Liste[identifikator_VÆRDI];
    int 가로=Terminal_post->X_koordinat,Lodret_placere=Terminal_post->Y_koordinat,폭=Terminal_post->너비,varighed_VÆRDI=Terminal_post->높이;
    if(!보드그림범위(&가로,&Lodret_placere,&폭,&varighed_VÆRDI))return;
    사각영역(Terminal_post->X_koordinat,Terminal_post->Y_koordinat,Terminal_post->너비,Terminal_post->높이,0x403127);
    unsigned 색상=identifikator_VÆRDI==Fokus?0x905020:0x604438;사각영역(Terminal_post->X_koordinat,Terminal_post->Y_koordinat,Terminal_post->너비,30,색상);
    navn_tabel(Terminal_post->X_koordinat+12,Terminal_post->Y_koordinat+7,"JKOROS Terminal",0xffffff,색상);
    char 수치[2]={(char)('1'+identifikator_VÆRDI),0};navn_tabel(Terminal_post->X_koordinat+148,Terminal_post->Y_koordinat+7,수치,0xffffff,색상);
    navn_tabel(Terminal_post->X_koordinat+240,Terminal_post->Y_koordinat+7,Terminal_post->너비>=500?(한글입력?"[DA] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[DA]":"[EN]"),0xffffff,색상);
    사각영역(Terminal_post->X_koordinat+Terminal_post->너비-32,Terminal_post->Y_koordinat+4,26,22,0x5555b8);navn_tabel(Terminal_post->X_koordinat+Terminal_post->너비-24,Terminal_post->Y_koordinat+7,"X",0xffffff,0x5555b8);
    Indhold_VÆRDI();
}
static void tegne_scene(void){
    if(!desktop_Visning)return;사각영역(0,0,보드화면너비(),보드화면높이(),0x302018);사각영역(0,0,보드화면너비(),32,0x403127);
    사각영역(6,4,136,24,0x905020);navn_tabel(14,8,"+ New terminal",0xffffff,0x905020);
    for(int 순번=0;순번<4;순번++)if(Windows_Liste[순번].살아있음){unsigned tegnkode=Fokus==순번?0x905020:0x604438;사각영역(154+순번*112,4,106,24,tegnkode);navn_tabel(160+순번*112,8,"Terminal",0xffffff,tegnkode);char streng_data[2]={(char)('1'+순번),0};navn_tabel(232+순번*112,8,streng_data,0xffffff,tegnkode);}
    if(!post_TÆL_8f7753a1)navn_tabel(140,210,"Click + New terminal to start",0xede9df,0x302018);
    for(int 순번=0;순번<post_TÆL_8f7753a1;순번++)udførelse_ramme(ordre_VÆRDI[순번]);화면다시그림(Fokus);Terminal_post=&Windows_Liste[produktoutput];
}
static void Paint_område(int 가로,int Lodret_placere,int 폭,int varighed_VÆRDI){
    if(!desktop_Visning||!보드그림범위(&가로,&Lodret_placere,&폭,&varighed_VÆRDI))return;
    for(int Linje=Lodret_placere;Linje<Lodret_placere+varighed_VÆRDI;Linje+=32){
        int 띠높이=Lodret_placere+varighed_VÆRDI-Linje;if(띠높이>32)띠높이=32;
        if(Tavle_START_tegning(가로,Linje,폭,띠높이)){tegne_scene();Tavle_Udfør_tegning();}
    }
}
static void 다시그리기(void){Paint_område(0,0,보드화면너비(),보드화면높이());}
/* 서로 겹치지 않는 새 Vindue 영역과 Forrige_vare 자리의 네 띠를 복구한다. */
static void 창자리그리기(int 가로,int Lodret_placere,int 폭,int varighed_VÆRDI,Terminal_d413d4bc *Vindue){
    int 왼쪽=가로>(int)Vindue->X_koordinat?가로:(int)Vindue->X_koordinat;
    int 위쪽=Lodret_placere>(int)Vindue->Y_koordinat?Lodret_placere:(int)Vindue->Y_koordinat;
    int HØJRE=가로+폭<(int)(Vindue->X_koordinat+Vindue->너비)?가로+폭:(int)(Vindue->X_koordinat+Vindue->너비);
    int 아래쪽=Lodret_placere+varighed_VÆRDI<(int)(Vindue->Y_koordinat+Vindue->높이)?Lodret_placere+varighed_VÆRDI:(int)(Vindue->Y_koordinat+Vindue->높이);
    Paint_område(Vindue->X_koordinat,Vindue->Y_koordinat,Vindue->너비,Vindue->높이);
    if(왼쪽>=HØJRE||위쪽>=아래쪽){Paint_område(가로,Lodret_placere,폭,varighed_VÆRDI);return;}
    Paint_område(가로,Lodret_placere,폭,위쪽-Lodret_placere);
    Paint_område(가로,아래쪽,폭,Lodret_placere+varighed_VÆRDI-아래쪽);
    Paint_område(가로,위쪽,왼쪽-가로,아래쪽-위쪽);
    Paint_område(HØJRE,위쪽,가로+폭-HØJRE,아래쪽-위쪽);
}
static void signal_Fokus(void){it_Afventer=(it_Afventer&~15u)|(unsigned)(Fokus+1)|0x10000;}
void Terminal_input_HYPPIGST(unsigned 한글여부){
    한글입력=한글여부!=0;
    /* Update title bars only: a mode switch must not erase an EL0 drawing. */
    if(Fokus>=0){
        Terminal_d413d4bc *vindue_post=&Windows_Liste[Fokus];
        navn_tabel(vindue_post->X_koordinat+240,vindue_post->Y_koordinat+7,vindue_post->너비>=500?(한글입력?"[DA] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[DA]":"[EN]"),0xffffff,0x905020);
    }
}
static void 앞으로올리기(int identifikator_VÆRDI){if(identifikator_VÆRDI<0||identifikator_VÆRDI>=4||!Windows_Liste[identifikator_VÆRDI].살아있음)return;int aktuel_placere=0;while(aktuel_placere<post_TÆL_8f7753a1&&ordre_VÆRDI[aktuel_placere]!=identifikator_VÆRDI)aktuel_placere++;for(;aktuel_placere+1<post_TÆL_8f7753a1;aktuel_placere++)ordre_VÆRDI[aktuel_placere]=ordre_VÆRDI[aktuel_placere+1];ordre_VÆRDI[post_TÆL_8f7753a1-1]=identifikator_VÆRDI;Fokus=identifikator_VÆRDI;signal_Fokus();다시그리기();}
static void 빈칸채우기(unsigned post_placere){for(unsigned tegnkode=0;tegnkode<최대열수;tegnkode++){Terminal_post->글자칸들[post_placere%Historik_linje_TÆL][tegnkode]=0;Terminal_post->모양들[post_placere%Historik_linje_TÆL][tegnkode]=Terminal_post->전경색|(Terminal_post->배경색<<4);}}
static void rydde_Indhold(void){Terminal_post->post_placere=Terminal_post->KOLONNE_placere=Terminal_post->맨위=Terminal_post->rulle=0;for(unsigned 반환값=0;반환값<Historik_linje_TÆL;반환값++)빈칸채우기(반환값);if(보이는지())Indhold_VÆRDI();}
static int åbne_post_81b8d99b(void){
    if(!보드화면기억공간())return -19;int identifikator_VÆRDI=0;while(identifikator_VÆRDI<4&&Windows_Liste[identifikator_VÆRDI].살아있음)identifikator_VÆRDI++;if(identifikator_VÆRDI==4)return -28;
    desktop_Visning=1;Terminal_post=&Windows_Liste[identifikator_VÆRDI];memset(Terminal_post,0,sizeof(*Terminal_post));Terminal_post->살아있음=1;Terminal_post->너비=568;Terminal_post->높이=360;Terminal_post->KOLONNER=68;Terminal_post->post_TÆL=19;Terminal_post->X_koordinat=12+identifikator_VÆRDI*16;Terminal_post->Y_koordinat=48+identifikator_VÆRDI*18;Terminal_post->전경색=7;Terminal_post->가리개보임=1;
    for(unsigned 반환값=0;반환값<Historik_linje_TÆL;반환값++)빈칸채우기(반환값);ordre_VÆRDI[post_TÆL_8f7753a1++]=identifikator_VÆRDI;Fokus=identifikator_VÆRDI;it_Afventer|=1u<<(4+identifikator_VÆRDI);signal_Fokus();다시그리기();return identifikator_VÆRDI+1;
}
static void Luk_vindue(int identifikator_VÆRDI){
    if(identifikator_VÆRDI<0||identifikator_VÆRDI>=4||!Windows_Liste[identifikator_VÆRDI].살아있음)return;Windows_Liste[identifikator_VÆRDI].살아있음=0;it_Afventer|=1u<<(8+identifikator_VÆRDI);
    int aktuel_placere=0;while(aktuel_placere<post_TÆL_8f7753a1&&ordre_VÆRDI[aktuel_placere]!=identifikator_VÆRDI)aktuel_placere++;for(;aktuel_placere+1<post_TÆL_8f7753a1;aktuel_placere++)ordre_VÆRDI[aktuel_placere]=ordre_VÆRDI[aktuel_placere+1];post_TÆL_8f7753a1--;
    if(Fokus==identifikator_VÆRDI)Fokus=post_TÆL_8f7753a1?ordre_VÆRDI[post_TÆL_8f7753a1-1]:-1;signal_Fokus();다시그리기();
}
static void 줄바꿈(void){Terminal_post->KOLONNE_placere=0;Terminal_post->post_placere++;if(Terminal_post->post_placere>=Terminal_post->맨위+Terminal_post->post_TÆL){Terminal_post->맨위++;빈칸채우기(Terminal_post->post_placere);if(보이는지())Indhold_VÆRDI();}}
static void tegnkode_451f2815(unsigned tegnkode){
    if(tegnkode==13){Terminal_post->KOLONNE_placere=0;return;}if(tegnkode==10){줄바꿈();return;}if(tegnkode==8){if(Terminal_post->KOLONNE_placere)Terminal_post->KOLONNE_placere--;return;}
    if(tegnkode==9){unsigned vare_TÆL=8-Terminal_post->KOLONNE_placere%8;while(vare_TÆL--)tegnkode_451f2815(' ');return;}if(tegnkode<32||tegnkode==127)return;
    unsigned 너비값=bredt_tegn(tegnkode);if(Terminal_post->KOLONNE_placere+너비값>Terminal_post->KOLONNER)줄바꿈();
    if(Terminal_post->글자칸들[Terminal_post->post_placere%Historik_linje_TÆL][Terminal_post->KOLONNE_placere]==0xffffffffu&&Terminal_post->KOLONNE_placere){Terminal_post->글자칸들[Terminal_post->post_placere%Historik_linje_TÆL][Terminal_post->KOLONNE_placere-1]=' ';Paint_skærmbillede(Terminal_post->post_placere,Terminal_post->KOLONNE_placere-1);}
    if(bredt_tegn(Terminal_post->글자칸들[Terminal_post->post_placere%Historik_linje_TÆL][Terminal_post->KOLONNE_placere])==2&&Terminal_post->KOLONNE_placere+1<Terminal_post->KOLONNER){Terminal_post->글자칸들[Terminal_post->post_placere%Historik_linje_TÆL][Terminal_post->KOLONNE_placere+1]=' ';Paint_skærmbillede(Terminal_post->post_placere,Terminal_post->KOLONNE_placere+1);}
    Terminal_post->글자칸들[Terminal_post->post_placere%Historik_linje_TÆL][Terminal_post->KOLONNE_placere]=tegnkode;Terminal_post->모양들[Terminal_post->post_placere%Historik_linje_TÆL][Terminal_post->KOLONNE_placere]=Terminal_post->전경색|(Terminal_post->배경색<<4);
    if(너비값==2)Terminal_post->글자칸들[Terminal_post->post_placere%Historik_linje_TÆL][Terminal_post->KOLONNE_placere+1]=0xffffffffu;
    Paint_skærmbillede(Terminal_post->post_placere,Terminal_post->KOLONNE_placere);Terminal_post->KOLONNE_placere+=너비값;
}
static void handle_kontrol_SEKVENS(unsigned tegnkode){
    unsigned vare_TÆL=Terminal_post->parameter_VÆRDI[0]?Terminal_post->parameter_VÆRDI[0]:1;
    if(tegnkode=='m')for(unsigned 순번=0;순번<=Terminal_post->parameter_INDEKS;순번++){unsigned data_placere=Terminal_post->parameter_VÆRDI[순번];if(!data_placere){Terminal_post->전경색=7;Terminal_post->배경색=0;}if(data_placere==1&&Terminal_post->전경색<8)Terminal_post->전경색+=8;if(data_placere==7){unsigned 유지=Terminal_post->전경색;Terminal_post->전경색=Terminal_post->배경색;Terminal_post->배경색=유지;}if(data_placere>=30&&data_placere<=37)Terminal_post->전경색=data_placere-30;if(data_placere>=90&&data_placere<=97)Terminal_post->전경색=data_placere-90+8;if(data_placere>=40&&data_placere<=47)Terminal_post->배경색=data_placere-40;if(data_placere>=100&&data_placere<=107)Terminal_post->배경색=data_placere-100+8;if(data_placere==39)Terminal_post->전경색=7;if(data_placere==49)Terminal_post->배경색=0;}
    if(tegnkode=='J'&&(Terminal_post->parameter_VÆRDI[0]==2||Terminal_post->parameter_VÆRDI[0]==3))rydde_Indhold();
    if(tegnkode=='K'){unsigned 출발위치=Terminal_post->parameter_VÆRDI[0]==2?0:Terminal_post->KOLONNE_placere,도착위치=Terminal_post->parameter_VÆRDI[0]==1?Terminal_post->KOLONNE_placere+1:Terminal_post->KOLONNER;if(Terminal_post->parameter_VÆRDI[0]==1)출발위치=0;for(unsigned 순번=출발위치;순번<도착위치&&순번<Terminal_post->KOLONNER;순번++){
        unsigned post_VÆRDI=Terminal_post->post_placere%Historik_linje_TÆL,tegn_VÆRDI=Terminal_post->글자칸들[post_VÆRDI][순번],figur_VÆRDI=Terminal_post->전경색|(Terminal_post->배경색<<4);
        /* 넓은 vi 화면에서도 이미 빈 칸의 skrifttype_VÆRDI 화소를 되풀이해 칠하지 않는다. */
        int 바뀜=(tegn_VÆRDI!=0&&tegn_VÆRDI!=' ')||Terminal_post->모양들[post_VÆRDI][순번]!=figur_VÆRDI;
        Terminal_post->글자칸들[post_VÆRDI][순번]=' ';Terminal_post->모양들[post_VÆRDI][순번]=figur_VÆRDI;
        if(바뀜)Paint_skærmbillede(Terminal_post->post_placere,순번);
    }}
    if(tegnkode=='D')Terminal_post->KOLONNE_placere=vare_TÆL>Terminal_post->KOLONNE_placere?0:Terminal_post->KOLONNE_placere-vare_TÆL;if(tegnkode=='C')Terminal_post->KOLONNE_placere=Terminal_post->KOLONNE_placere+vare_TÆL>=Terminal_post->KOLONNER?Terminal_post->KOLONNER-1:Terminal_post->KOLONNE_placere+vare_TÆL;
    if(tegnkode=='G')Terminal_post->KOLONNE_placere=vare_TÆL>Terminal_post->KOLONNER?Terminal_post->KOLONNER-1:vare_TÆL-1;if(tegnkode=='A')Terminal_post->post_placere=vare_TÆL>Terminal_post->post_placere-Terminal_post->맨위?Terminal_post->맨위:Terminal_post->post_placere-vare_TÆL;
    if(tegnkode=='B')Terminal_post->post_placere=Terminal_post->post_placere+vare_TÆL>=Terminal_post->맨위+Terminal_post->post_TÆL?Terminal_post->맨위+Terminal_post->post_TÆL-1:Terminal_post->post_placere+vare_TÆL;
    if(tegnkode=='H'||tegnkode=='f'){Terminal_post->post_placere=Terminal_post->맨위+(vare_TÆL>Terminal_post->post_TÆL?Terminal_post->post_TÆL:vare_TÆL)-1;unsigned X_koordinat=Terminal_post->parameter_VÆRDI[1]?Terminal_post->parameter_VÆRDI[1]:1;Terminal_post->KOLONNE_placere=(X_koordinat>Terminal_post->KOLONNER?Terminal_post->KOLONNER:X_koordinat)-1;}
    if(tegnkode=='s'){Terminal_post->저장행=Terminal_post->post_placere;Terminal_post->저장열=Terminal_post->KOLONNE_placere;}if(tegnkode=='u'){Terminal_post->post_placere=Terminal_post->저장행;Terminal_post->KOLONNE_placere=Terminal_post->저장열<Terminal_post->KOLONNER?Terminal_post->저장열:Terminal_post->KOLONNER-1;}
    if((tegnkode=='h'||tegnkode=='l')&&Terminal_post->parameter_VÆRDI[0]==25)Terminal_post->가리개보임=tegnkode=='h';
}
void Terminal_byte(unsigned SEKUND_VÆRDI){
    Terminal_post=&Windows_Liste[produktoutput];if(!Terminal_post->살아있음)return;cirkumfleks_VÆRDI(0);if(Terminal_post->rulle){Terminal_post->rulle=0;if(보이는지())Indhold_VÆRDI();}
    if(Terminal_post->탈출상태==1){Terminal_post->탈출상태=SEKUND_VÆRDI=='['?2:0;Terminal_post->parameter_INDEKS=0;for(unsigned 순번=0;순번<4;순번++)Terminal_post->parameter_VÆRDI[순번]=0;}
    else if(Terminal_post->탈출상태==2){if(SEKUND_VÆRDI=='?'){}else if(SEKUND_VÆRDI>='0'&&SEKUND_VÆRDI<='9'){if(Terminal_post->parameter_VÆRDI[Terminal_post->parameter_INDEKS]<10000)Terminal_post->parameter_VÆRDI[Terminal_post->parameter_INDEKS]=Terminal_post->parameter_VÆRDI[Terminal_post->parameter_INDEKS]*10+SEKUND_VÆRDI-'0';}else if(SEKUND_VÆRDI==';'&&Terminal_post->parameter_INDEKS<3)Terminal_post->parameter_INDEKS++;else{handle_kontrol_SEKVENS(SEKUND_VÆRDI);Terminal_post->탈출상태=0;}}
    else if(SEKUND_VÆRDI==27){Terminal_post->긴부호없는값=0;Terminal_post->탈출상태=1;}else{
        if(Terminal_post->긴부호없는값&&(SEKUND_VÆRDI&0xc0)!=0x80){Terminal_post->긴부호없는값=0;tegnkode_451f2815(0xfffd);}
        if(Terminal_post->긴부호없는값){Terminal_post->부호없는결과=Terminal_post->부호없는결과*64+(SEKUND_VÆRDI&63);if(--Terminal_post->긴부호없는값==0)tegnkode_451f2815(Terminal_post->부호없는결과<Terminal_post->MINDSTE_VÆRDI||Terminal_post->부호없는결과>0x10ffff||(Terminal_post->부호없는결과>=0xd800&&Terminal_post->부호없는결과<=0xdfff)?0xfffd:Terminal_post->부호없는결과);}
        else if(SEKUND_VÆRDI<128)tegnkode_451f2815(SEKUND_VÆRDI);else if(SEKUND_VÆRDI>=0xc2&&SEKUND_VÆRDI<=0xf4){Terminal_post->긴부호없는값=SEKUND_VÆRDI<0xe0?1:SEKUND_VÆRDI<0xf0?2:3;Terminal_post->부호없는결과=SEKUND_VÆRDI&((1u<<(6-Terminal_post->긴부호없는값))-1);Terminal_post->MINDSTE_VÆRDI=Terminal_post->긴부호없는값==1?128:Terminal_post->긴부호없는값==2?2048:65536;}else tegnkode_451f2815(0xfffd);
    }cirkumfleks_VÆRDI(1);
}
int Terminal_Afventer(void){return it_Afventer!=0;}
/* 모서리 INDEKS: 1 좌상, 2 우상, 3 좌하, 4 우하. */
static int tilpasse_størrelsen_trække=-1,잡은모서리,잡은가로,잡은세로,처음가로,처음세로,처음너비,처음높이;
static int 가리킨창(int 가로,int Lodret_placere) {
    for(int SEKVENS_VÆRDI=post_TÆL_8f7753a1-1;SEKVENS_VÆRDI>=0;SEKVENS_VÆRDI--){
        int identifikator_VÆRDI=ordre_VÆRDI[SEKVENS_VÆRDI];Terminal_d413d4bc *Vindue=&Windows_Liste[identifikator_VÆRDI];
        if(가로>=(int)Vindue->X_koordinat&&Lodret_placere>=(int)Vindue->Y_koordinat&&
           가로<(int)(Vindue->X_koordinat+Vindue->너비)&&Lodret_placere<(int)(Vindue->Y_koordinat+Vindue->높이))return identifikator_VÆRDI;
    }return -1;
}
static int 모서리찾기(int identifikator_VÆRDI,int 가로,int Lodret_placere) {
    if(identifikator_VÆRDI<0)return 0;Terminal_d413d4bc *Vindue=&Windows_Liste[identifikator_VÆRDI];
    int 왼쪽=가로<(int)Vindue->X_koordinat+8,HØJRE=가로>=(int)(Vindue->X_koordinat+Vindue->너비)-8;
    int 위쪽=Lodret_placere<(int)Vindue->Y_koordinat+8,아래쪽=Lodret_placere>=(int)(Vindue->Y_koordinat+Vindue->높이)-8;
    return (왼쪽||HØJRE)&&(위쪽||아래쪽)?1+HØJRE+아래쪽*2:0;
}
static int separator_VÆRDI(int VÆRDI,int 최소,int 최대){return VÆRDI<최소?최소:VÆRDI>최대?최대:VÆRDI;}
static void flytte_tilpasse_størrelsen(int 가로,int Lodret_placere) {
    Terminal_d413d4bc *Vindue=&Windows_Liste[tilpasse_størrelsen_trække];int 왼쪽=처음가로,위쪽=처음세로,HØJRE=처음가로+처음너비,아래쪽=처음세로+처음높이;
    if(잡은모서리==1||잡은모서리==3)왼쪽=separator_VÆRDI(처음가로+가로-잡은가로,0,HØJRE-360);
    else HØJRE=separator_VÆRDI(처음가로+처음너비+가로-잡은가로,왼쪽+360,보드화면너비());
    if(잡은모서리<=2)위쪽=separator_VÆRDI(처음세로+Lodret_placere-잡은세로,34,아래쪽-216);
    else 아래쪽=separator_VÆRDI(처음세로+처음높이+Lodret_placere-잡은세로,위쪽+216,보드화면높이());
    unsigned KOLONNER=(HØJRE-왼쪽-24)/8,post_TÆL=(아래쪽-위쪽-56)/16;
    if(Vindue->KOLONNER!=KOLONNER||Vindue->post_TÆL!=post_TÆL){
        Vindue->크기바뀜=1;Vindue->KOLONNER=KOLONNER;Vindue->post_TÆL=post_TÆL;
        if(Vindue->KOLONNE_placere>=KOLONNER)Vindue->KOLONNE_placere=KOLONNER-1;
        if(Vindue->post_placere>=Vindue->맨위+post_TÆL)Vindue->맨위=Vindue->post_placere-post_TÆL+1;
        unsigned 한도=Vindue->맨위;if(한도>Historik_linje_TÆL-post_TÆL)한도=Historik_linje_TÆL-post_TÆL;
        if(Vindue->rulle>한도)Vindue->rulle=한도;
    }
    int 옛가로=Vindue->X_koordinat,옛세로=Vindue->Y_koordinat,옛폭=Vindue->너비,옛길이=Vindue->높이;
    if(옛가로==왼쪽&&옛세로==위쪽&&옛폭==HØJRE-왼쪽&&옛길이==아래쪽-위쪽)return;
    Vindue->X_koordinat=왼쪽;Vindue->Y_koordinat=위쪽;Vindue->너비=HØJRE-왼쪽;Vindue->높이=아래쪽-위쪽;
    창자리그리기(옛가로,옛세로,옛폭,옛길이,Vindue);
}
void Terminal_markør(unsigned Næste_vare,int X_koordinat,int Y_koordinat){
    unsigned 눌림=Næste_vare&~단추들;단추들=Næste_vare;
    if(!desktop_Visning){trække_VÆRDI=-1;tilpasse_størrelsen_trække=-1;Tavle_markør(X_koordinat,Y_koordinat,1);return;}
    if(!(Næste_vare&1)){trække_VÆRDI=-1;tilpasse_størrelsen_trække=-1;}
    if(tilpasse_størrelsen_trække>=0&&!Windows_Liste[tilpasse_størrelsen_trække].살아있음)tilpasse_størrelsen_trække=-1;
    if(trække_VÆRDI>=0&&!Windows_Liste[trække_VÆRDI].살아있음)trække_VÆRDI=-1;
    if(tilpasse_størrelsen_trække>=0){
        flytte_tilpasse_størrelsen(X_koordinat,Y_koordinat);Tavle_markør(X_koordinat,Y_koordinat,잡은모서리==1||잡은모서리==4?2:3);return;
    }
    Tavle_markør(X_koordinat,Y_koordinat,1);
    if(trække_VÆRDI>=0){
        Terminal_d413d4bc *Vindue=&Windows_Liste[trække_VÆRDI];
        int 옛가로=Vindue->X_koordinat,옛세로=Vindue->Y_koordinat;
        Vindue->X_koordinat=separator_VÆRDI(X_koordinat-trække_X,0,보드화면너비()-Vindue->너비);
        Vindue->Y_koordinat=separator_VÆRDI(Y_koordinat-trække_Y,34,보드화면높이()-Vindue->높이);
        if(옛가로!=(int)Vindue->X_koordinat||옛세로!=(int)Vindue->Y_koordinat)창자리그리기(옛가로,옛세로,Vindue->너비,Vindue->높이,Vindue);
        return;
    }
    extern int skærmbillede_overlejring(int,int,int);
    if(skærmbillede_overlejring(Fokus,X_koordinat,Y_koordinat)){skærmbillede_markør(Fokus,눌림,X_koordinat,Y_koordinat);return;}
    int identifikator_VÆRDI=가리킨창(X_koordinat,Y_koordinat),모서리=모서리찾기(identifikator_VÆRDI,X_koordinat,Y_koordinat);
    if(모서리)Tavle_markør(X_koordinat,Y_koordinat,모서리==1||모서리==4?2:3);
    if(눌림&1){
        if(모서리){
            Terminal_d413d4bc *Vindue=&Windows_Liste[identifikator_VÆRDI];tilpasse_størrelsen_trække=identifikator_VÆRDI;잡은모서리=모서리;잡은가로=X_koordinat;잡은세로=Y_koordinat;
            처음가로=Vindue->X_koordinat;처음세로=Vindue->Y_koordinat;처음너비=Vindue->너비;처음높이=Vindue->높이;
            if(identifikator_VÆRDI!=Fokus)앞으로올리기(identifikator_VÆRDI);return;
        }
        if(Y_koordinat<32&&X_koordinat>=6&&X_koordinat<142){åbne_post_81b8d99b();return;}
        if(Y_koordinat<32&&X_koordinat>=154&&X_koordinat<602){앞으로올리기((X_koordinat-154)/112);return;}
        if(identifikator_VÆRDI>=0){
            Terminal_d413d4bc *Vindue=&Windows_Liste[identifikator_VÆRDI];
            if(Y_koordinat<(int)Vindue->Y_koordinat+30&&X_koordinat>=(int)(Vindue->X_koordinat+Vindue->너비)-32){Luk_vindue(identifikator_VÆRDI);return;}
            if(identifikator_VÆRDI!=Fokus)앞으로올리기(identifikator_VÆRDI);
            if(Y_koordinat<(int)Vindue->Y_koordinat+30){trække_VÆRDI=identifikator_VÆRDI;trække_X=X_koordinat-Vindue->X_koordinat;trække_Y=Y_koordinat-Vindue->Y_koordinat;}return;
        }
    }
    if(Fokus>=0&&(눌림&(8|16))){Terminal_post=&Windows_Liste[Fokus];if(눌림&8){unsigned 한도=Terminal_post->맨위;if(한도>Historik_linje_TÆL-Terminal_post->post_TÆL)한도=Historik_linje_TÆL-Terminal_post->post_TÆL;Terminal_post->rulle=Terminal_post->rulle+9>한도?한도:Terminal_post->rulle+9;}else Terminal_post->rulle=Terminal_post->rulle<9?0:Terminal_post->rulle-9;다시그리기();}
}
void 터미널바로가기키(unsigned 누름값){if(누름값==1)åbne_post_81b8d99b();if(누름값==2&&post_TÆL_8f7753a1)앞으로올리기(ordre_VÆRDI[0]);if(누름값==3)Luk_vindue(Fokus);}
maskine_Ord Tavle_Terminal(maskine_Ord Handling){
    if(Handling==300){if(!Windows_Liste[produktoutput].살아있음)return åbne_post_81b8d99b();desktop_Visning=1;다시그리기();return 0;}
    if(Handling==0){Luk_vindue(Fokus);return 0;}if(Handling==1)return (uint32_t)åbne_post_81b8d99b();if(Handling==2)return Fokus>=0;
    if(Handling==9){desktop_Visning=0;return 0;}if(Handling==7)return post_TÆL_8f7753a1;if(Handling==10)return Fokus+1;if(Handling==11)return produktoutput;
    if(Handling==13){Terminal_d413d4bc *Vindue=&Windows_Liste[produktoutput];return Vindue->살아있음?(Vindue->post_TÆL<<16)|Vindue->KOLONNER:(19<<16)|68;}
    if(Handling==14){unsigned VÆRDI=Windows_Liste[produktoutput].크기바뀜;Windows_Liste[produktoutput].크기바뀜=0;return VÆRDI;}
    if(Handling==12){unsigned VÆRDI=it_Afventer;it_Afventer=0;return VÆRDI;}
    if(Handling>=20&&Handling<24)return Windows_Liste[Handling-20].살아있음;
    if(Handling>=100&&Handling<104){produktoutput=Handling-100;Terminal_post=&Windows_Liste[produktoutput];return 0;}
    if(Handling>=200&&Handling<204){앞으로올리기(Handling-200);return 0;}
    if(Handling==3){다시그리기();return 0;}Terminal_post=&Windows_Liste[produktoutput];if(!Terminal_post->살아있음)return 0;
    if(Handling==4)rydde_Indhold();if(Handling==5||Handling==6){unsigned Forrige_vare=단추들;Terminal_markør(Handling==5?8:16,0,0);단추들=Forrige_vare;}return 1;
}
