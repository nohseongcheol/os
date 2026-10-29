#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* 자체 네 fuinneog 합성과 UTF-8 Teirminéal. 바뀐 영역의 완성 그림만 표시한다. */
#include <stdint.h>
#include <stddef.h>
typedef uintptr_t meaisín_Word;
extern meaisín_Word clár_picteilín(meaisín_Word,meaisín_Word,meaisín_Word),보드화면기억공간(void);
extern void *memset(void *,int,size_t);
extern const unsigned char Teirminéal_clófhoireann[];
#define 최대열수 237
#define Stair_líne_COUNT 160
typedef struct {
    uint32_t 글자칸들[Stair_líne_COUNT][최대열수]; uint8_t 모양들[Stair_líne_COUNT][최대열수];
    unsigned 너비,높이,COLUMNS,ró_COUNT,크기바뀜;
    unsigned 살아있음,x_chomhordanáid,세로좌표,ró_suíomh,colún_suíomh,맨위,scrollaigh,전경색,배경색,탈출상태,paraiméadar_VALUE[4],paraiméadar_INDEX,저장행,저장열;
    unsigned 부호없는결과,긴부호없는값,SMALL_VALUE,대체화면,가리개보임;
} Teirminéal_d413d4bc;
static Teirminéal_d413d4bc Windows_Liosta[4];
static int Fócas=-1,출력결과,ord_VALUE[4],iontráil_COUNT,tarraing_VALUE=-1,끌기가로,끌기세로;
static unsigned teicneolaíocht_faisnéise_Ar_feitheamh,단추들,deasc_Amharc,한글입력;
static const uint32_t 색상들[16]={0x201a15,0x6060df,0x9dcc86,0x80cfea,0xefaf72,0xca96c9,0xceda76,0xede9df,0x858078,0x8888ff,0xb9eba7,0xa5eaff,0xffcc99,0xf0bef1,0xf0f0a0,0xffffff};
extern int 화면보임(int),화면가리킴(int,unsigned,int,int);
extern void 화면다시그림(int);
static Teirminéal_d413d4bc *Teirminéal_iontráil;
static unsigned 넓은글자(unsigned pointe_cóid){return pointe_cóid>=256?2:1;}
static void 사각영역(unsigned x_chomhordanáid,unsigned 세로좌표,unsigned 너비값,unsigned 높이값,unsigned 색상){
    보드사각그림(x_chomhordanáid,세로좌표,너비값,높이값,색상);
}
void Teirminéal_glif(unsigned x_chomhordanáid,unsigned 세로좌표,unsigned pointe_cóid,unsigned 전경색,unsigned 배경색){
    unsigned 너비=넓은글자(pointe_cóid)*8;if(pointe_cóid==0xffffffffu)return;
    int 왼쪽=x_chomhordanáid,위쪽=세로좌표,폭=너비,fad_VALUE=16;
    if(!보드그림범위(&왼쪽,&위쪽,&폭,&fad_VALUE))return;
    if(pointe_cóid==' '){보드사각그림(왼쪽,위쪽,폭,fad_VALUE,배경색);return;}
    unsigned LOOKUP_INDEX=pointe_cóid<65536?pointe_cóid:pointe_cóid>=0x1f600&&pointe_cóid<0x1f650?65536+pointe_cóid-0x1f600:0xfffd;
    const unsigned char *clófhoireann_VALUE=Teirminéal_clófhoireann+LOOKUP_INDEX*32;
    for(int Líne=위쪽;Líne<위쪽+fad_VALUE;Líne++){unsigned 비트들=clófhoireann_VALUE[(Líne-세로좌표)*2]*256+clófhoireann_VALUE[(Líne-세로좌표)*2+1];for(int spás_iontráil=왼쪽;spás_iontráil<왼쪽+폭;spás_iontráil++)clár_picteilín(spás_iontráil,Líne,(비트들&(0x8000>>(spás_iontráil-x_chomhordanáid)))?전경색:배경색);}
}
static void ainm_tábla(unsigned x_chomhordanáid,unsigned 세로좌표,const char *teaghrán_sonraí,unsigned 전경색,unsigned 배경색){while(*teaghrán_sonraí){unsigned pointe_cóid=(unsigned char)*teaghrán_sonraí++, 남은수=0;if(pointe_cóid>=0xc0){남은수=pointe_cóid<0xe0?1:pointe_cóid<0xf0?2:3;pointe_cóid&=(1u<<(6-남은수))-1;while(남은수--&&*teaghrán_sonraí)pointe_cóid=(pointe_cóid<<6)|((unsigned char)*teaghrán_sonraí++&63);}Teirminéal_glif(x_chomhordanáid,세로좌표,pointe_cóid,전경색,배경색);x_chomhordanáid+=넓은글자(pointe_cóid)*8;}}
static unsigned 첫항목(void){return Teirminéal_iontráil->맨위;}
static int 보이는지(void){return Teirminéal_iontráil->살아있음&&Fócas>=0&&Teirminéal_iontráil==&Windows_Liosta[Fócas]&&!화면보임(Fócas);}
static void 그리기(unsigned ró_suíomh,unsigned colún_suíomh){
    if(!보이는지()||ró_suíomh<첫항목()-Teirminéal_iontráil->scrollaigh||ró_suíomh>=첫항목()-Teirminéal_iontráil->scrollaigh+Teirminéal_iontráil->ró_COUNT||colún_suíomh>=Teirminéal_iontráil->COLUMNS)return;
    unsigned pointe_cóid=Teirminéal_iontráil->글자칸들[ró_suíomh%Stair_líne_COUNT][colún_suíomh],teaghrán_sonraí=Teirminéal_iontráil->모양들[ró_suíomh%Stair_líne_COUNT][colún_suíomh];
    if(넓은글자(pointe_cóid)==2&&colún_suíomh+1>=Teirminéal_iontráil->COLUMNS)pointe_cóid=' ';
    Teirminéal_glif(Teirminéal_iontráil->x_chomhordanáid+12+colún_suíomh*8,Teirminéal_iontráil->세로좌표+36+(ró_suíomh-첫항목()+Teirminéal_iontráil->scrollaigh)*16,pointe_cóid?pointe_cóid:' ',색상들[teaghrán_sonraí&15],색상들[teaghrán_sonraí>>4]);
}
static void carait_VALUE(int seó_fuinneog){if(!보이는지()||Teirminéal_iontráil->scrollaigh||Teirminéal_iontráil->colún_suíomh>=Teirminéal_iontráil->COLUMNS||Teirminéal_iontráil->ró_suíomh<Teirminéal_iontráil->맨위||Teirminéal_iontráil->ró_suíomh>=Teirminéal_iontráil->맨위+Teirminéal_iontráil->ró_COUNT)return;
    if(!seó_fuinneog||!Teirminéal_iontráil->가리개보임)그리기(Teirminéal_iontráil->ró_suíomh,Teirminéal_iontráil->colún_suíomh);else 사각영역(Teirminéal_iontráil->x_chomhordanáid+12+Teirminéal_iontráil->colún_suíomh*8,Teirminéal_iontráil->세로좌표+36+(Teirminéal_iontráil->ró_suíomh-Teirminéal_iontráil->맨위)*16+14,8,2,색상들[Teirminéal_iontráil->전경색]);}
static void Inneachar_VALUE(void){
    사각영역(Teirminéal_iontráil->x_chomhordanáid+12,Teirminéal_iontráil->세로좌표+36,Teirminéal_iontráil->COLUMNS*8,Teirminéal_iontráil->ró_COUNT*16,색상들[0]);
    int 가로=Teirminéal_iontráil->x_chomhordanáid+12,Ingearach_suíomh=Teirminéal_iontráil->세로좌표+36,폭=Teirminéal_iontráil->COLUMNS*8,fad_VALUE=Teirminéal_iontráil->ró_COUNT*16;
    if(보드그림범위(&가로,&Ingearach_suíomh,&폭,&fad_VALUE)){
    unsigned 첫줄=(Ingearach_suíomh-Teirminéal_iontráil->세로좌표-36)/16,끝줄=(Ingearach_suíomh+fad_VALUE-Teirminéal_iontráil->세로좌표-36+15)/16;
    unsigned 첫칸=(가로-Teirminéal_iontráil->x_chomhordanáid-12)/8,끝칸=(가로+폭-Teirminéal_iontráil->x_chomhordanáid-12+7)/8;
    if(첫칸)첫칸--; /* 잘림 경계 왼쪽에서 시작한 두 spás_iontráil 글자도 그린다. */
    for(unsigned 반환값=첫줄;반환값<끝줄;반환값++)for(unsigned pointe_cóid=첫칸;pointe_cóid<끝칸;pointe_cóid++){
        unsigned ró_suíomh=첫항목()-Teirminéal_iontráil->scrollaigh+반환값,carachtar_VALUE=Teirminéal_iontráil->글자칸들[ró_suíomh%Stair_líne_COUNT][pointe_cóid],teaghrán_sonraí=Teirminéal_iontráil->모양들[ró_suíomh%Stair_líne_COUNT][pointe_cóid];
        if(넓은글자(carachtar_VALUE)==2&&pointe_cóid+1>=Teirminéal_iontráil->COLUMNS)carachtar_VALUE=' ';
        if((carachtar_VALUE==0||carachtar_VALUE==' ')&&(teaghrán_sonraí>>4)==0)continue;
        Teirminéal_glif(Teirminéal_iontráil->x_chomhordanáid+12+pointe_cóid*8,Teirminéal_iontráil->세로좌표+36+반환값*16,carachtar_VALUE?carachtar_VALUE:' ',색상들[teaghrán_sonraí&15],색상들[teaghrán_sonraí>>4]);
    }}
    ainm_tábla(Teirminéal_iontráil->x_chomhordanáid+12,Teirminéal_iontráil->세로좌표+Teirminéal_iontráil->높이-18,Teirminéal_iontráil->scrollaigh?"PgDn: recent output":Teirminéal_iontráil->너비>=500?"F6: next | Corner + left drag: resize":"Corner + left drag: resize",0xece8e2,0x403127);carait_VALUE(1);
}
static void 실행틀(int aitheantóir_VALUE){
    Teirminéal_iontráil=&Windows_Liosta[aitheantóir_VALUE];
    int 가로=Teirminéal_iontráil->x_chomhordanáid,Ingearach_suíomh=Teirminéal_iontráil->세로좌표,폭=Teirminéal_iontráil->너비,fad_VALUE=Teirminéal_iontráil->높이;
    if(!보드그림범위(&가로,&Ingearach_suíomh,&폭,&fad_VALUE))return;
    사각영역(Teirminéal_iontráil->x_chomhordanáid,Teirminéal_iontráil->세로좌표,Teirminéal_iontráil->너비,Teirminéal_iontráil->높이,0x403127);
    unsigned 색상=aitheantóir_VALUE==Fócas?0x905020:0x604438;사각영역(Teirminéal_iontráil->x_chomhordanáid,Teirminéal_iontráil->세로좌표,Teirminéal_iontráil->너비,30,색상);
    ainm_tábla(Teirminéal_iontráil->x_chomhordanáid+12,Teirminéal_iontráil->세로좌표+7,"JKOROS Terminal",0xffffff,색상);
    char 수치[2]={(char)('1'+aitheantóir_VALUE),0};ainm_tábla(Teirminéal_iontráil->x_chomhordanáid+148,Teirminéal_iontráil->세로좌표+7,수치,0xffffff,색상);
    ainm_tábla(Teirminéal_iontráil->x_chomhordanáid+240,Teirminéal_iontráil->세로좌표+7,Teirminéal_iontráil->너비>=500?(한글입력?"[GA] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[GA]":"[EN]"),0xffffff,색상);
    사각영역(Teirminéal_iontráil->x_chomhordanáid+Teirminéal_iontráil->너비-32,Teirminéal_iontráil->세로좌표+4,26,22,0x5555b8);ainm_tábla(Teirminéal_iontráil->x_chomhordanáid+Teirminéal_iontráil->너비-24,Teirminéal_iontráil->세로좌표+7,"X",0xffffff,0x5555b8);
    Inneachar_VALUE();
}
static void 장면그리기(void){
    if(!deasc_Amharc)return;사각영역(0,0,보드화면너비(),보드화면높이(),0x302018);사각영역(0,0,보드화면너비(),32,0x403127);
    사각영역(6,4,136,24,0x905020);ainm_tábla(14,8,"+ New terminal",0xffffff,0x905020);
    for(int 순번=0;순번<4;순번++)if(Windows_Liosta[순번].살아있음){unsigned pointe_cóid=Fócas==순번?0x905020:0x604438;사각영역(154+순번*112,4,106,24,pointe_cóid);ainm_tábla(160+순번*112,8,"Terminal",0xffffff,pointe_cóid);char teaghrán_sonraí[2]={(char)('1'+순번),0};ainm_tábla(232+순번*112,8,teaghrán_sonraí,0xffffff,pointe_cóid);}
    if(!iontráil_COUNT)ainm_tábla(140,210,"Click + New terminal to start",0xede9df,0x302018);
    for(int 순번=0;순번<iontráil_COUNT;순번++)실행틀(ord_VALUE[순번]);화면다시그림(Fócas);Teirminéal_iontráil=&Windows_Liosta[출력결과];
}
static void 영역그리기(int 가로,int Ingearach_suíomh,int 폭,int fad_VALUE){
    if(!deasc_Amharc||!보드그림범위(&가로,&Ingearach_suíomh,&폭,&fad_VALUE))return;
    for(int Líne=Ingearach_suíomh;Líne<Ingearach_suíomh+fad_VALUE;Líne+=32){
        int 띠높이=Ingearach_suíomh+fad_VALUE-Líne;if(띠높이>32)띠높이=32;
        if(clár_Start_líníocht(가로,Líne,폭,띠높이)){장면그리기();clár_Críochnaigh_líníocht();}
    }
}
static void 다시그리기(void){영역그리기(0,0,보드화면너비(),보드화면높이());}
/* 서로 겹치지 않는 새 fuinneog 영역과 이전 자리의 네 띠를 복구한다. */
static void 창자리그리기(int 가로,int Ingearach_suíomh,int 폭,int fad_VALUE,Teirminéal_d413d4bc *fuinneog){
    int 왼쪽=가로>(int)fuinneog->x_chomhordanáid?가로:(int)fuinneog->x_chomhordanáid;
    int 위쪽=Ingearach_suíomh>(int)fuinneog->세로좌표?Ingearach_suíomh:(int)fuinneog->세로좌표;
    int RIGHT=가로+폭<(int)(fuinneog->x_chomhordanáid+fuinneog->너비)?가로+폭:(int)(fuinneog->x_chomhordanáid+fuinneog->너비);
    int 아래쪽=Ingearach_suíomh+fad_VALUE<(int)(fuinneog->세로좌표+fuinneog->높이)?Ingearach_suíomh+fad_VALUE:(int)(fuinneog->세로좌표+fuinneog->높이);
    영역그리기(fuinneog->x_chomhordanáid,fuinneog->세로좌표,fuinneog->너비,fuinneog->높이);
    if(왼쪽>=RIGHT||위쪽>=아래쪽){영역그리기(가로,Ingearach_suíomh,폭,fad_VALUE);return;}
    영역그리기(가로,Ingearach_suíomh,폭,위쪽-Ingearach_suíomh);
    영역그리기(가로,아래쪽,폭,Ingearach_suíomh+fad_VALUE-아래쪽);
    영역그리기(가로,위쪽,왼쪽-가로,아래쪽-위쪽);
    영역그리기(RIGHT,위쪽,가로+폭-RIGHT,아래쪽-위쪽);
}
static void 초점알리기(void){teicneolaíocht_faisnéise_Ar_feitheamh=(teicneolaíocht_faisnéise_Ar_feitheamh&~15u)|(unsigned)(Fócas+1)|0x10000;}
void 터미널입력방식(unsigned 한글여부){
    한글입력=한글여부!=0;
    /* Update title bars only: a mode switch must not erase an EL0 drawing. */
    if(Fócas>=0){
        Teirminéal_d413d4bc *fuinneog_iontráil=&Windows_Liosta[Fócas];
        ainm_tábla(fuinneog_iontráil->x_chomhordanáid+240,fuinneog_iontráil->세로좌표+7,fuinneog_iontráil->너비>=500?(한글입력?"[GA] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[GA]":"[EN]"),0xffffff,0x905020);
    }
}
static void 앞으로올리기(int aitheantóir_VALUE){if(aitheantóir_VALUE<0||aitheantóir_VALUE>=4||!Windows_Liosta[aitheantóir_VALUE].살아있음)return;int 현재위치=0;while(현재위치<iontráil_COUNT&&ord_VALUE[현재위치]!=aitheantóir_VALUE)현재위치++;for(;현재위치+1<iontráil_COUNT;현재위치++)ord_VALUE[현재위치]=ord_VALUE[현재위치+1];ord_VALUE[iontráil_COUNT-1]=aitheantóir_VALUE;Fócas=aitheantóir_VALUE;초점알리기();다시그리기();}
static void 빈칸채우기(unsigned ró_suíomh){for(unsigned pointe_cóid=0;pointe_cóid<최대열수;pointe_cóid++){Teirminéal_iontráil->글자칸들[ró_suíomh%Stair_líne_COUNT][pointe_cóid]=0;Teirminéal_iontráil->모양들[ró_suíomh%Stair_líne_COUNT][pointe_cóid]=Teirminéal_iontráil->전경색|(Teirminéal_iontráil->배경색<<4);}}
static void glan_TOC(void){Teirminéal_iontráil->ró_suíomh=Teirminéal_iontráil->colún_suíomh=Teirminéal_iontráil->맨위=Teirminéal_iontráil->scrollaigh=0;for(unsigned 반환값=0;반환값<Stair_líne_COUNT;반환값++)빈칸채우기(반환값);if(보이는지())Inneachar_VALUE();}
static int Create_iontráil(void){
    if(!보드화면기억공간())return -19;int aitheantóir_VALUE=0;while(aitheantóir_VALUE<4&&Windows_Liosta[aitheantóir_VALUE].살아있음)aitheantóir_VALUE++;if(aitheantóir_VALUE==4)return -28;
    deasc_Amharc=1;Teirminéal_iontráil=&Windows_Liosta[aitheantóir_VALUE];memset(Teirminéal_iontráil,0,sizeof(*Teirminéal_iontráil));Teirminéal_iontráil->살아있음=1;Teirminéal_iontráil->너비=568;Teirminéal_iontráil->높이=360;Teirminéal_iontráil->COLUMNS=68;Teirminéal_iontráil->ró_COUNT=19;Teirminéal_iontráil->x_chomhordanáid=12+aitheantóir_VALUE*16;Teirminéal_iontráil->세로좌표=48+aitheantóir_VALUE*18;Teirminéal_iontráil->전경색=7;Teirminéal_iontráil->가리개보임=1;
    for(unsigned 반환값=0;반환값<Stair_líne_COUNT;반환값++)빈칸채우기(반환값);ord_VALUE[iontráil_COUNT++]=aitheantóir_VALUE;Fócas=aitheantóir_VALUE;teicneolaíocht_faisnéise_Ar_feitheamh|=1u<<(4+aitheantóir_VALUE);초점알리기();다시그리기();return aitheantóir_VALUE+1;
}
static void dún_fuinneog(int aitheantóir_VALUE){
    if(aitheantóir_VALUE<0||aitheantóir_VALUE>=4||!Windows_Liosta[aitheantóir_VALUE].살아있음)return;Windows_Liosta[aitheantóir_VALUE].살아있음=0;teicneolaíocht_faisnéise_Ar_feitheamh|=1u<<(8+aitheantóir_VALUE);
    int 현재위치=0;while(현재위치<iontráil_COUNT&&ord_VALUE[현재위치]!=aitheantóir_VALUE)현재위치++;for(;현재위치+1<iontráil_COUNT;현재위치++)ord_VALUE[현재위치]=ord_VALUE[현재위치+1];iontráil_COUNT--;
    if(Fócas==aitheantóir_VALUE)Fócas=iontráil_COUNT?ord_VALUE[iontráil_COUNT-1]:-1;초점알리기();다시그리기();
}
static void 줄바꿈(void){Teirminéal_iontráil->colún_suíomh=0;Teirminéal_iontráil->ró_suíomh++;if(Teirminéal_iontráil->ró_suíomh>=Teirminéal_iontráil->맨위+Teirminéal_iontráil->ró_COUNT){Teirminéal_iontráil->맨위++;빈칸채우기(Teirminéal_iontráil->ró_suíomh);if(보이는지())Inneachar_VALUE();}}
static void pointe_cóid_451f2815(unsigned pointe_cóid){
    if(pointe_cóid==13){Teirminéal_iontráil->colún_suíomh=0;return;}if(pointe_cóid==10){줄바꿈();return;}if(pointe_cóid==8){if(Teirminéal_iontráil->colún_suíomh)Teirminéal_iontráil->colún_suíomh--;return;}
    if(pointe_cóid==9){unsigned mír_COUNT=8-Teirminéal_iontráil->colún_suíomh%8;while(mír_COUNT--)pointe_cóid_451f2815(' ');return;}if(pointe_cóid<32||pointe_cóid==127)return;
    unsigned 너비값=넓은글자(pointe_cóid);if(Teirminéal_iontráil->colún_suíomh+너비값>Teirminéal_iontráil->COLUMNS)줄바꿈();
    if(Teirminéal_iontráil->글자칸들[Teirminéal_iontráil->ró_suíomh%Stair_líne_COUNT][Teirminéal_iontráil->colún_suíomh]==0xffffffffu&&Teirminéal_iontráil->colún_suíomh){Teirminéal_iontráil->글자칸들[Teirminéal_iontráil->ró_suíomh%Stair_líne_COUNT][Teirminéal_iontráil->colún_suíomh-1]=' ';그리기(Teirminéal_iontráil->ró_suíomh,Teirminéal_iontráil->colún_suíomh-1);}
    if(넓은글자(Teirminéal_iontráil->글자칸들[Teirminéal_iontráil->ró_suíomh%Stair_líne_COUNT][Teirminéal_iontráil->colún_suíomh])==2&&Teirminéal_iontráil->colún_suíomh+1<Teirminéal_iontráil->COLUMNS){Teirminéal_iontráil->글자칸들[Teirminéal_iontráil->ró_suíomh%Stair_líne_COUNT][Teirminéal_iontráil->colún_suíomh+1]=' ';그리기(Teirminéal_iontráil->ró_suíomh,Teirminéal_iontráil->colún_suíomh+1);}
    Teirminéal_iontráil->글자칸들[Teirminéal_iontráil->ró_suíomh%Stair_líne_COUNT][Teirminéal_iontráil->colún_suíomh]=pointe_cóid;Teirminéal_iontráil->모양들[Teirminéal_iontráil->ró_suíomh%Stair_líne_COUNT][Teirminéal_iontráil->colún_suíomh]=Teirminéal_iontráil->전경색|(Teirminéal_iontráil->배경색<<4);
    if(너비값==2)Teirminéal_iontráil->글자칸들[Teirminéal_iontráil->ró_suíomh%Stair_líne_COUNT][Teirminéal_iontráil->colún_suíomh+1]=0xffffffffu;
    그리기(Teirminéal_iontráil->ró_suíomh,Teirminéal_iontráil->colún_suíomh);Teirminéal_iontráil->colún_suíomh+=너비값;
}
static void hanla_rialú_SEQUENCE(unsigned pointe_cóid){
    unsigned mír_COUNT=Teirminéal_iontráil->paraiméadar_VALUE[0]?Teirminéal_iontráil->paraiméadar_VALUE[0]:1;
    if(pointe_cóid=='m')for(unsigned 순번=0;순번<=Teirminéal_iontráil->paraiméadar_INDEX;순번++){unsigned sonraí_suíomh=Teirminéal_iontráil->paraiméadar_VALUE[순번];if(!sonraí_suíomh){Teirminéal_iontráil->전경색=7;Teirminéal_iontráil->배경색=0;}if(sonraí_suíomh==1&&Teirminéal_iontráil->전경색<8)Teirminéal_iontráil->전경색+=8;if(sonraí_suíomh==7){unsigned 유지=Teirminéal_iontráil->전경색;Teirminéal_iontráil->전경색=Teirminéal_iontráil->배경색;Teirminéal_iontráil->배경색=유지;}if(sonraí_suíomh>=30&&sonraí_suíomh<=37)Teirminéal_iontráil->전경색=sonraí_suíomh-30;if(sonraí_suíomh>=90&&sonraí_suíomh<=97)Teirminéal_iontráil->전경색=sonraí_suíomh-90+8;if(sonraí_suíomh>=40&&sonraí_suíomh<=47)Teirminéal_iontráil->배경색=sonraí_suíomh-40;if(sonraí_suíomh>=100&&sonraí_suíomh<=107)Teirminéal_iontráil->배경색=sonraí_suíomh-100+8;if(sonraí_suíomh==39)Teirminéal_iontráil->전경색=7;if(sonraí_suíomh==49)Teirminéal_iontráil->배경색=0;}
    if(pointe_cóid=='J'&&(Teirminéal_iontráil->paraiméadar_VALUE[0]==2||Teirminéal_iontráil->paraiméadar_VALUE[0]==3))glan_TOC();
    if(pointe_cóid=='K'){unsigned 출발위치=Teirminéal_iontráil->paraiméadar_VALUE[0]==2?0:Teirminéal_iontráil->colún_suíomh,도착위치=Teirminéal_iontráil->paraiméadar_VALUE[0]==1?Teirminéal_iontráil->colún_suíomh+1:Teirminéal_iontráil->COLUMNS;if(Teirminéal_iontráil->paraiméadar_VALUE[0]==1)출발위치=0;for(unsigned 순번=출발위치;순번<도착위치&&순번<Teirminéal_iontráil->COLUMNS;순번++){
        unsigned ró_VALUE=Teirminéal_iontráil->ró_suíomh%Stair_líne_COUNT,carachtar_VALUE=Teirminéal_iontráil->글자칸들[ró_VALUE][순번],cruth_VALUE=Teirminéal_iontráil->전경색|(Teirminéal_iontráil->배경색<<4);
        /* 넓은 vi 화면에서도 이미 빈 칸의 clófhoireann_VALUE 화소를 되풀이해 칠하지 않는다. */
        int 바뀜=(carachtar_VALUE!=0&&carachtar_VALUE!=' ')||Teirminéal_iontráil->모양들[ró_VALUE][순번]!=cruth_VALUE;
        Teirminéal_iontráil->글자칸들[ró_VALUE][순번]=' ';Teirminéal_iontráil->모양들[ró_VALUE][순번]=cruth_VALUE;
        if(바뀜)그리기(Teirminéal_iontráil->ró_suíomh,순번);
    }}
    if(pointe_cóid=='D')Teirminéal_iontráil->colún_suíomh=mír_COUNT>Teirminéal_iontráil->colún_suíomh?0:Teirminéal_iontráil->colún_suíomh-mír_COUNT;if(pointe_cóid=='C')Teirminéal_iontráil->colún_suíomh=Teirminéal_iontráil->colún_suíomh+mír_COUNT>=Teirminéal_iontráil->COLUMNS?Teirminéal_iontráil->COLUMNS-1:Teirminéal_iontráil->colún_suíomh+mír_COUNT;
    if(pointe_cóid=='G')Teirminéal_iontráil->colún_suíomh=mír_COUNT>Teirminéal_iontráil->COLUMNS?Teirminéal_iontráil->COLUMNS-1:mír_COUNT-1;if(pointe_cóid=='A')Teirminéal_iontráil->ró_suíomh=mír_COUNT>Teirminéal_iontráil->ró_suíomh-Teirminéal_iontráil->맨위?Teirminéal_iontráil->맨위:Teirminéal_iontráil->ró_suíomh-mír_COUNT;
    if(pointe_cóid=='B')Teirminéal_iontráil->ró_suíomh=Teirminéal_iontráil->ró_suíomh+mír_COUNT>=Teirminéal_iontráil->맨위+Teirminéal_iontráil->ró_COUNT?Teirminéal_iontráil->맨위+Teirminéal_iontráil->ró_COUNT-1:Teirminéal_iontráil->ró_suíomh+mír_COUNT;
    if(pointe_cóid=='H'||pointe_cóid=='f'){Teirminéal_iontráil->ró_suíomh=Teirminéal_iontráil->맨위+(mír_COUNT>Teirminéal_iontráil->ró_COUNT?Teirminéal_iontráil->ró_COUNT:mír_COUNT)-1;unsigned x_chomhordanáid=Teirminéal_iontráil->paraiméadar_VALUE[1]?Teirminéal_iontráil->paraiméadar_VALUE[1]:1;Teirminéal_iontráil->colún_suíomh=(x_chomhordanáid>Teirminéal_iontráil->COLUMNS?Teirminéal_iontráil->COLUMNS:x_chomhordanáid)-1;}
    if(pointe_cóid=='s'){Teirminéal_iontráil->저장행=Teirminéal_iontráil->ró_suíomh;Teirminéal_iontráil->저장열=Teirminéal_iontráil->colún_suíomh;}if(pointe_cóid=='u'){Teirminéal_iontráil->ró_suíomh=Teirminéal_iontráil->저장행;Teirminéal_iontráil->colún_suíomh=Teirminéal_iontráil->저장열<Teirminéal_iontráil->COLUMNS?Teirminéal_iontráil->저장열:Teirminéal_iontráil->COLUMNS-1;}
    if((pointe_cóid=='h'||pointe_cóid=='l')&&Teirminéal_iontráil->paraiméadar_VALUE[0]==25)Teirminéal_iontráil->가리개보임=pointe_cóid=='h';
}
void Teirminéal_beart(unsigned SECOND_VALUE){
    Teirminéal_iontráil=&Windows_Liosta[출력결과];if(!Teirminéal_iontráil->살아있음)return;carait_VALUE(0);if(Teirminéal_iontráil->scrollaigh){Teirminéal_iontráil->scrollaigh=0;if(보이는지())Inneachar_VALUE();}
    if(Teirminéal_iontráil->탈출상태==1){Teirminéal_iontráil->탈출상태=SECOND_VALUE=='['?2:0;Teirminéal_iontráil->paraiméadar_INDEX=0;for(unsigned 순번=0;순번<4;순번++)Teirminéal_iontráil->paraiméadar_VALUE[순번]=0;}
    else if(Teirminéal_iontráil->탈출상태==2){if(SECOND_VALUE=='?'){}else if(SECOND_VALUE>='0'&&SECOND_VALUE<='9'){if(Teirminéal_iontráil->paraiméadar_VALUE[Teirminéal_iontráil->paraiméadar_INDEX]<10000)Teirminéal_iontráil->paraiméadar_VALUE[Teirminéal_iontráil->paraiméadar_INDEX]=Teirminéal_iontráil->paraiméadar_VALUE[Teirminéal_iontráil->paraiméadar_INDEX]*10+SECOND_VALUE-'0';}else if(SECOND_VALUE==';'&&Teirminéal_iontráil->paraiméadar_INDEX<3)Teirminéal_iontráil->paraiméadar_INDEX++;else{hanla_rialú_SEQUENCE(SECOND_VALUE);Teirminéal_iontráil->탈출상태=0;}}
    else if(SECOND_VALUE==27){Teirminéal_iontráil->긴부호없는값=0;Teirminéal_iontráil->탈출상태=1;}else{
        if(Teirminéal_iontráil->긴부호없는값&&(SECOND_VALUE&0xc0)!=0x80){Teirminéal_iontráil->긴부호없는값=0;pointe_cóid_451f2815(0xfffd);}
        if(Teirminéal_iontráil->긴부호없는값){Teirminéal_iontráil->부호없는결과=Teirminéal_iontráil->부호없는결과*64+(SECOND_VALUE&63);if(--Teirminéal_iontráil->긴부호없는값==0)pointe_cóid_451f2815(Teirminéal_iontráil->부호없는결과<Teirminéal_iontráil->SMALL_VALUE||Teirminéal_iontráil->부호없는결과>0x10ffff||(Teirminéal_iontráil->부호없는결과>=0xd800&&Teirminéal_iontráil->부호없는결과<=0xdfff)?0xfffd:Teirminéal_iontráil->부호없는결과);}
        else if(SECOND_VALUE<128)pointe_cóid_451f2815(SECOND_VALUE);else if(SECOND_VALUE>=0xc2&&SECOND_VALUE<=0xf4){Teirminéal_iontráil->긴부호없는값=SECOND_VALUE<0xe0?1:SECOND_VALUE<0xf0?2:3;Teirminéal_iontráil->부호없는결과=SECOND_VALUE&((1u<<(6-Teirminéal_iontráil->긴부호없는값))-1);Teirminéal_iontráil->SMALL_VALUE=Teirminéal_iontráil->긴부호없는값==1?128:Teirminéal_iontráil->긴부호없는값==2?2048:65536;}else pointe_cóid_451f2815(0xfffd);
    }carait_VALUE(1);
}
int Teirminéal_Ar_feitheamh(void){return teicneolaíocht_faisnéise_Ar_feitheamh!=0;}
/* 모서리 INDEX: 1 좌상, 2 우상, 3 좌하, 4 우하. */
static int athraigh_méid_tarraing=-1,잡은모서리,잡은가로,잡은세로,처음가로,처음세로,처음너비,처음높이;
static int 가리킨창(int 가로,int Ingearach_suíomh) {
    for(int SEQUENCE_VALUE=iontráil_COUNT-1;SEQUENCE_VALUE>=0;SEQUENCE_VALUE--){
        int aitheantóir_VALUE=ord_VALUE[SEQUENCE_VALUE];Teirminéal_d413d4bc *fuinneog=&Windows_Liosta[aitheantóir_VALUE];
        if(가로>=(int)fuinneog->x_chomhordanáid&&Ingearach_suíomh>=(int)fuinneog->세로좌표&&
           가로<(int)(fuinneog->x_chomhordanáid+fuinneog->너비)&&Ingearach_suíomh<(int)(fuinneog->세로좌표+fuinneog->높이))return aitheantóir_VALUE;
    }return -1;
}
static int 모서리찾기(int aitheantóir_VALUE,int 가로,int Ingearach_suíomh) {
    if(aitheantóir_VALUE<0)return 0;Teirminéal_d413d4bc *fuinneog=&Windows_Liosta[aitheantóir_VALUE];
    int 왼쪽=가로<(int)fuinneog->x_chomhordanáid+8,RIGHT=가로>=(int)(fuinneog->x_chomhordanáid+fuinneog->너비)-8;
    int 위쪽=Ingearach_suíomh<(int)fuinneog->세로좌표+8,아래쪽=Ingearach_suíomh>=(int)(fuinneog->세로좌표+fuinneog->높이)-8;
    return (왼쪽||RIGHT)&&(위쪽||아래쪽)?1+RIGHT+아래쪽*2:0;
}
static int deighilteoir_VALUE(int VALUE,int 최소,int 최대){return VALUE<최소?최소:VALUE>최대?최대:VALUE;}
static void bog_athraigh_méid(int 가로,int Ingearach_suíomh) {
    Teirminéal_d413d4bc *fuinneog=&Windows_Liosta[athraigh_méid_tarraing];int 왼쪽=처음가로,위쪽=처음세로,RIGHT=처음가로+처음너비,아래쪽=처음세로+처음높이;
    if(잡은모서리==1||잡은모서리==3)왼쪽=deighilteoir_VALUE(처음가로+가로-잡은가로,0,RIGHT-360);
    else RIGHT=deighilteoir_VALUE(처음가로+처음너비+가로-잡은가로,왼쪽+360,보드화면너비());
    if(잡은모서리<=2)위쪽=deighilteoir_VALUE(처음세로+Ingearach_suíomh-잡은세로,34,아래쪽-216);
    else 아래쪽=deighilteoir_VALUE(처음세로+처음높이+Ingearach_suíomh-잡은세로,위쪽+216,보드화면높이());
    unsigned COLUMNS=(RIGHT-왼쪽-24)/8,ró_COUNT=(아래쪽-위쪽-56)/16;
    if(fuinneog->COLUMNS!=COLUMNS||fuinneog->ró_COUNT!=ró_COUNT){
        fuinneog->크기바뀜=1;fuinneog->COLUMNS=COLUMNS;fuinneog->ró_COUNT=ró_COUNT;
        if(fuinneog->colún_suíomh>=COLUMNS)fuinneog->colún_suíomh=COLUMNS-1;
        if(fuinneog->ró_suíomh>=fuinneog->맨위+ró_COUNT)fuinneog->맨위=fuinneog->ró_suíomh-ró_COUNT+1;
        unsigned 한도=fuinneog->맨위;if(한도>Stair_líne_COUNT-ró_COUNT)한도=Stair_líne_COUNT-ró_COUNT;
        if(fuinneog->scrollaigh>한도)fuinneog->scrollaigh=한도;
    }
    int 옛가로=fuinneog->x_chomhordanáid,옛세로=fuinneog->세로좌표,옛폭=fuinneog->너비,옛길이=fuinneog->높이;
    if(옛가로==왼쪽&&옛세로==위쪽&&옛폭==RIGHT-왼쪽&&옛길이==아래쪽-위쪽)return;
    fuinneog->x_chomhordanáid=왼쪽;fuinneog->세로좌표=위쪽;fuinneog->너비=RIGHT-왼쪽;fuinneog->높이=아래쪽-위쪽;
    창자리그리기(옛가로,옛세로,옛폭,옛길이,fuinneog);
}
void Teirminéal_pointeoir(unsigned Ar_aghaidh_mír,int x_chomhordanáid,int 세로좌표){
    unsigned 눌림=Ar_aghaidh_mír&~단추들;단추들=Ar_aghaidh_mír;
    if(!deasc_Amharc){tarraing_VALUE=-1;athraigh_méid_tarraing=-1;clár_pointeoir(x_chomhordanáid,세로좌표,1);return;}
    if(!(Ar_aghaidh_mír&1)){tarraing_VALUE=-1;athraigh_méid_tarraing=-1;}
    if(athraigh_méid_tarraing>=0&&!Windows_Liosta[athraigh_méid_tarraing].살아있음)athraigh_méid_tarraing=-1;
    if(tarraing_VALUE>=0&&!Windows_Liosta[tarraing_VALUE].살아있음)tarraing_VALUE=-1;
    if(athraigh_méid_tarraing>=0){
        bog_athraigh_méid(x_chomhordanáid,세로좌표);clár_pointeoir(x_chomhordanáid,세로좌표,잡은모서리==1||잡은모서리==4?2:3);return;
    }
    clár_pointeoir(x_chomhordanáid,세로좌표,1);
    if(tarraing_VALUE>=0){
        Teirminéal_d413d4bc *fuinneog=&Windows_Liosta[tarraing_VALUE];
        int 옛가로=fuinneog->x_chomhordanáid,옛세로=fuinneog->세로좌표;
        fuinneog->x_chomhordanáid=deighilteoir_VALUE(x_chomhordanáid-끌기가로,0,보드화면너비()-fuinneog->너비);
        fuinneog->세로좌표=deighilteoir_VALUE(세로좌표-끌기세로,34,보드화면높이()-fuinneog->높이);
        if(옛가로!=(int)fuinneog->x_chomhordanáid||옛세로!=(int)fuinneog->세로좌표)창자리그리기(옛가로,옛세로,fuinneog->너비,fuinneog->높이,fuinneog);
        return;
    }
    extern int 화면덮음(int,int,int);
    if(화면덮음(Fócas,x_chomhordanáid,세로좌표)){화면가리킴(Fócas,눌림,x_chomhordanáid,세로좌표);return;}
    int aitheantóir_VALUE=가리킨창(x_chomhordanáid,세로좌표),모서리=모서리찾기(aitheantóir_VALUE,x_chomhordanáid,세로좌표);
    if(모서리)clár_pointeoir(x_chomhordanáid,세로좌표,모서리==1||모서리==4?2:3);
    if(눌림&1){
        if(모서리){
            Teirminéal_d413d4bc *fuinneog=&Windows_Liosta[aitheantóir_VALUE];athraigh_méid_tarraing=aitheantóir_VALUE;잡은모서리=모서리;잡은가로=x_chomhordanáid;잡은세로=세로좌표;
            처음가로=fuinneog->x_chomhordanáid;처음세로=fuinneog->세로좌표;처음너비=fuinneog->너비;처음높이=fuinneog->높이;
            if(aitheantóir_VALUE!=Fócas)앞으로올리기(aitheantóir_VALUE);return;
        }
        if(세로좌표<32&&x_chomhordanáid>=6&&x_chomhordanáid<142){Create_iontráil();return;}
        if(세로좌표<32&&x_chomhordanáid>=154&&x_chomhordanáid<602){앞으로올리기((x_chomhordanáid-154)/112);return;}
        if(aitheantóir_VALUE>=0){
            Teirminéal_d413d4bc *fuinneog=&Windows_Liosta[aitheantóir_VALUE];
            if(세로좌표<(int)fuinneog->세로좌표+30&&x_chomhordanáid>=(int)(fuinneog->x_chomhordanáid+fuinneog->너비)-32){dún_fuinneog(aitheantóir_VALUE);return;}
            if(aitheantóir_VALUE!=Fócas)앞으로올리기(aitheantóir_VALUE);
            if(세로좌표<(int)fuinneog->세로좌표+30){tarraing_VALUE=aitheantóir_VALUE;끌기가로=x_chomhordanáid-fuinneog->x_chomhordanáid;끌기세로=세로좌표-fuinneog->세로좌표;}return;
        }
    }
    if(Fócas>=0&&(눌림&(8|16))){Teirminéal_iontráil=&Windows_Liosta[Fócas];if(눌림&8){unsigned 한도=Teirminéal_iontráil->맨위;if(한도>Stair_líne_COUNT-Teirminéal_iontráil->ró_COUNT)한도=Stair_líne_COUNT-Teirminéal_iontráil->ró_COUNT;Teirminéal_iontráil->scrollaigh=Teirminéal_iontráil->scrollaigh+9>한도?한도:Teirminéal_iontráil->scrollaigh+9;}else Teirminéal_iontráil->scrollaigh=Teirminéal_iontráil->scrollaigh<9?0:Teirminéal_iontráil->scrollaigh-9;다시그리기();}
}
void 터미널바로가기키(unsigned 누름값){if(누름값==1)Create_iontráil();if(누름값==2&&iontráil_COUNT)앞으로올리기(ord_VALUE[0]);if(누름값==3)dún_fuinneog(Fócas);}
meaisín_Word clár_Teirminéal(meaisín_Word Gníomh){
    if(Gníomh==300){if(!Windows_Liosta[출력결과].살아있음)return Create_iontráil();deasc_Amharc=1;다시그리기();return 0;}
    if(Gníomh==0){dún_fuinneog(Fócas);return 0;}if(Gníomh==1)return (uint32_t)Create_iontráil();if(Gníomh==2)return Fócas>=0;
    if(Gníomh==9){deasc_Amharc=0;return 0;}if(Gníomh==7)return iontráil_COUNT;if(Gníomh==10)return Fócas+1;if(Gníomh==11)return 출력결과;
    if(Gníomh==13){Teirminéal_d413d4bc *fuinneog=&Windows_Liosta[출력결과];return fuinneog->살아있음?(fuinneog->ró_COUNT<<16)|fuinneog->COLUMNS:(19<<16)|68;}
    if(Gníomh==14){unsigned VALUE=Windows_Liosta[출력결과].크기바뀜;Windows_Liosta[출력결과].크기바뀜=0;return VALUE;}
    if(Gníomh==12){unsigned VALUE=teicneolaíocht_faisnéise_Ar_feitheamh;teicneolaíocht_faisnéise_Ar_feitheamh=0;return VALUE;}
    if(Gníomh>=20&&Gníomh<24)return Windows_Liosta[Gníomh-20].살아있음;
    if(Gníomh>=100&&Gníomh<104){출력결과=Gníomh-100;Teirminéal_iontráil=&Windows_Liosta[출력결과];return 0;}
    if(Gníomh>=200&&Gníomh<204){앞으로올리기(Gníomh-200);return 0;}
    if(Gníomh==3){다시그리기();return 0;}Teirminéal_iontráil=&Windows_Liosta[출력결과];if(!Teirminéal_iontráil->살아있음)return 0;
    if(Gníomh==4)glan_TOC();if(Gníomh==5||Gníomh==6){unsigned 이전=단추들;Teirminéal_pointeoir(Gníomh==5?8:16,0,0);단추들=이전;}return 1;
}
