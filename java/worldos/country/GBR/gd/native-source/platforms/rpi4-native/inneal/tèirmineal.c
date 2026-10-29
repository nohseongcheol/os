#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* 자체 네 uinneag 합성과 UTF-8 tèirmineal. 바뀐 영역의 완성 그림만 표시한다. */
#include <stdint.h>
#include <stddef.h>
typedef uintptr_t inneal_Word;
extern inneal_Word bòrd_pel(inneal_Word,inneal_Word,inneal_Word),보드화면기억공간(void);
extern void *memset(void *,int,size_t);
extern const unsigned char tèirmineal_cruth_clò[];
#define 최대열수 237
#define eachdraidh_loidhne_COUNT 160
typedef struct {
    uint32_t 글자칸들[eachdraidh_loidhne_COUNT][최대열수]; uint8_t 모양들[eachdraidh_loidhne_COUNT][최대열수];
    unsigned 너비,높이,COLUMNS,ROW_COUNT,크기바뀜;
    unsigned 살아있음,co_chomharra_x,세로좌표,ROW_suidhich,colbh_suidhich,맨위,sgrolaich,전경색,배경색,탈출상태,매개값[4],매개색인,저장행,저장열;
    unsigned 부호없는결과,긴부호없는값,SMALL_VALUE,대체화면,가리개보임;
} tèirmineal_d413d4bc;
static tèirmineal_d413d4bc Windows_Liosta[4];
static int Focus=-1,출력결과,òrdugh_VALUE[4],cur_a_steach_COUNT,slaod_VALUE=-1,끌기가로,끌기세로;
static unsigned 대기중,단추들,deasg_seall,한글입력;
static const uint32_t 색상들[16]={0x201a15,0x6060df,0x9dcc86,0x80cfea,0xefaf72,0xca96c9,0xceda76,0xede9df,0x858078,0x8888ff,0xb9eba7,0xa5eaff,0xffcc99,0xf0bef1,0xf0f0a0,0xffffff};
extern int 화면보임(int),화면가리킴(int,unsigned,int,int);
extern void 화면다시그림(int);
static tèirmineal_d413d4bc *tèirmineal_cur_a_steach;
static unsigned 넓은글자(unsigned còd_a_charactair){return còd_a_charactair>=256?2:1;}
static void 사각영역(unsigned co_chomharra_x,unsigned 세로좌표,unsigned 너비값,unsigned 높이값,unsigned 색상){
    보드사각그림(co_chomharra_x,세로좌표,너비값,높이값,색상);
}
void 터미널글자그림(unsigned co_chomharra_x,unsigned 세로좌표,unsigned còd_a_charactair,unsigned 전경색,unsigned 배경색){
    unsigned 너비=넓은글자(còd_a_charactair)*8;if(còd_a_charactair==0xffffffffu)return;
    int 왼쪽=co_chomharra_x,위쪽=세로좌표,폭=너비,faid_VALUE=16;
    if(!보드그림범위(&왼쪽,&위쪽,&폭,&faid_VALUE))return;
    if(còd_a_charactair==' '){보드사각그림(왼쪽,위쪽,폭,faid_VALUE,배경색);return;}
    unsigned LOOKUP_INDEX=còd_a_charactair<65536?còd_a_charactair:còd_a_charactair>=0x1f600&&còd_a_charactair<0x1f650?65536+còd_a_charactair-0x1f600:0xfffd;
    const unsigned char *cruth_clò_VALUE=tèirmineal_cruth_clò+LOOKUP_INDEX*32;
    for(int loidhne=위쪽;loidhne<위쪽+faid_VALUE;loidhne++){unsigned 비트들=cruth_clò_VALUE[(loidhne-세로좌표)*2]*256+cruth_clò_VALUE[(loidhne-세로좌표)*2+1];for(int slot_cur_a_steach=왼쪽;slot_cur_a_steach<왼쪽+폭;slot_cur_a_steach++)bòrd_pel(slot_cur_a_steach,loidhne,(비트들&(0x8000>>(slot_cur_a_steach-co_chomharra_x)))?전경색:배경색);}
}
static void ainm_clàr(unsigned co_chomharra_x,unsigned 세로좌표,const char *sreang_dàta,unsigned 전경색,unsigned 배경색){while(*sreang_dàta){unsigned còd_a_charactair=(unsigned char)*sreang_dàta++, 남은수=0;if(còd_a_charactair>=0xc0){남은수=còd_a_charactair<0xe0?1:còd_a_charactair<0xf0?2:3;còd_a_charactair&=(1u<<(6-남은수))-1;while(남은수--&&*sreang_dàta)còd_a_charactair=(còd_a_charactair<<6)|((unsigned char)*sreang_dàta++&63);}터미널글자그림(co_chomharra_x,세로좌표,còd_a_charactair,전경색,배경색);co_chomharra_x+=넓은글자(còd_a_charactair)*8;}}
static unsigned 첫항목(void){return tèirmineal_cur_a_steach->맨위;}
static int 보이는지(void){return tèirmineal_cur_a_steach->살아있음&&Focus>=0&&tèirmineal_cur_a_steach==&Windows_Liosta[Focus]&&!화면보임(Focus);}
static void 그리기(unsigned ROW_suidhich,unsigned colbh_suidhich){
    if(!보이는지()||ROW_suidhich<첫항목()-tèirmineal_cur_a_steach->sgrolaich||ROW_suidhich>=첫항목()-tèirmineal_cur_a_steach->sgrolaich+tèirmineal_cur_a_steach->ROW_COUNT||colbh_suidhich>=tèirmineal_cur_a_steach->COLUMNS)return;
    unsigned còd_a_charactair=tèirmineal_cur_a_steach->글자칸들[ROW_suidhich%eachdraidh_loidhne_COUNT][colbh_suidhich],sreang_dàta=tèirmineal_cur_a_steach->모양들[ROW_suidhich%eachdraidh_loidhne_COUNT][colbh_suidhich];
    if(넓은글자(còd_a_charactair)==2&&colbh_suidhich+1>=tèirmineal_cur_a_steach->COLUMNS)còd_a_charactair=' ';
    터미널글자그림(tèirmineal_cur_a_steach->co_chomharra_x+12+colbh_suidhich*8,tèirmineal_cur_a_steach->세로좌표+36+(ROW_suidhich-첫항목()+tèirmineal_cur_a_steach->sgrolaich)*16,còd_a_charactair?còd_a_charactair:' ',색상들[sreang_dàta&15],색상들[sreang_dàta>>4]);
}
static void carait_VALUE(int show_uinneag){if(!보이는지()||tèirmineal_cur_a_steach->sgrolaich||tèirmineal_cur_a_steach->colbh_suidhich>=tèirmineal_cur_a_steach->COLUMNS||tèirmineal_cur_a_steach->ROW_suidhich<tèirmineal_cur_a_steach->맨위||tèirmineal_cur_a_steach->ROW_suidhich>=tèirmineal_cur_a_steach->맨위+tèirmineal_cur_a_steach->ROW_COUNT)return;
    if(!show_uinneag||!tèirmineal_cur_a_steach->가리개보임)그리기(tèirmineal_cur_a_steach->ROW_suidhich,tèirmineal_cur_a_steach->colbh_suidhich);else 사각영역(tèirmineal_cur_a_steach->co_chomharra_x+12+tèirmineal_cur_a_steach->colbh_suidhich*8,tèirmineal_cur_a_steach->세로좌표+36+(tèirmineal_cur_a_steach->ROW_suidhich-tèirmineal_cur_a_steach->맨위)*16+14,8,2,색상들[tèirmineal_cur_a_steach->전경색]);}
static void susbaint_VALUE(void){
    사각영역(tèirmineal_cur_a_steach->co_chomharra_x+12,tèirmineal_cur_a_steach->세로좌표+36,tèirmineal_cur_a_steach->COLUMNS*8,tèirmineal_cur_a_steach->ROW_COUNT*16,색상들[0]);
    int 가로=tèirmineal_cur_a_steach->co_chomharra_x+12,inghearach_suidhich=tèirmineal_cur_a_steach->세로좌표+36,폭=tèirmineal_cur_a_steach->COLUMNS*8,faid_VALUE=tèirmineal_cur_a_steach->ROW_COUNT*16;
    if(보드그림범위(&가로,&inghearach_suidhich,&폭,&faid_VALUE)){
    unsigned 첫줄=(inghearach_suidhich-tèirmineal_cur_a_steach->세로좌표-36)/16,끝줄=(inghearach_suidhich+faid_VALUE-tèirmineal_cur_a_steach->세로좌표-36+15)/16;
    unsigned 첫칸=(가로-tèirmineal_cur_a_steach->co_chomharra_x-12)/8,끝칸=(가로+폭-tèirmineal_cur_a_steach->co_chomharra_x-12+7)/8;
    if(첫칸)첫칸--; /* 잘림 경계 왼쪽에서 시작한 두 slot_cur_a_steach 글자도 그린다. */
    for(unsigned 반환값=첫줄;반환값<끝줄;반환값++)for(unsigned còd_a_charactair=첫칸;còd_a_charactair<끝칸;còd_a_charactair++){
        unsigned ROW_suidhich=첫항목()-tèirmineal_cur_a_steach->sgrolaich+반환값,caractar_VALUE=tèirmineal_cur_a_steach->글자칸들[ROW_suidhich%eachdraidh_loidhne_COUNT][còd_a_charactair],sreang_dàta=tèirmineal_cur_a_steach->모양들[ROW_suidhich%eachdraidh_loidhne_COUNT][còd_a_charactair];
        if(넓은글자(caractar_VALUE)==2&&còd_a_charactair+1>=tèirmineal_cur_a_steach->COLUMNS)caractar_VALUE=' ';
        if((caractar_VALUE==0||caractar_VALUE==' ')&&(sreang_dàta>>4)==0)continue;
        터미널글자그림(tèirmineal_cur_a_steach->co_chomharra_x+12+còd_a_charactair*8,tèirmineal_cur_a_steach->세로좌표+36+반환값*16,caractar_VALUE?caractar_VALUE:' ',색상들[sreang_dàta&15],색상들[sreang_dàta>>4]);
    }}
    ainm_clàr(tèirmineal_cur_a_steach->co_chomharra_x+12,tèirmineal_cur_a_steach->세로좌표+tèirmineal_cur_a_steach->높이-18,tèirmineal_cur_a_steach->sgrolaich?"PgDn: recent output":tèirmineal_cur_a_steach->너비>=500?"F6: next | Corner + left drag: resize":"Corner + left drag: resize",0xece8e2,0x403127);carait_VALUE(1);
}
static void 실행틀(int aithnichear_VALUE){
    tèirmineal_cur_a_steach=&Windows_Liosta[aithnichear_VALUE];
    int 가로=tèirmineal_cur_a_steach->co_chomharra_x,inghearach_suidhich=tèirmineal_cur_a_steach->세로좌표,폭=tèirmineal_cur_a_steach->너비,faid_VALUE=tèirmineal_cur_a_steach->높이;
    if(!보드그림범위(&가로,&inghearach_suidhich,&폭,&faid_VALUE))return;
    사각영역(tèirmineal_cur_a_steach->co_chomharra_x,tèirmineal_cur_a_steach->세로좌표,tèirmineal_cur_a_steach->너비,tèirmineal_cur_a_steach->높이,0x403127);
    unsigned 색상=aithnichear_VALUE==Focus?0x905020:0x604438;사각영역(tèirmineal_cur_a_steach->co_chomharra_x,tèirmineal_cur_a_steach->세로좌표,tèirmineal_cur_a_steach->너비,30,색상);
    ainm_clàr(tèirmineal_cur_a_steach->co_chomharra_x+12,tèirmineal_cur_a_steach->세로좌표+7,"JKOROS Terminal",0xffffff,색상);
    char 수치[2]={(char)('1'+aithnichear_VALUE),0};ainm_clàr(tèirmineal_cur_a_steach->co_chomharra_x+148,tèirmineal_cur_a_steach->세로좌표+7,수치,0xffffff,색상);
    ainm_clàr(tèirmineal_cur_a_steach->co_chomharra_x+240,tèirmineal_cur_a_steach->세로좌표+7,tèirmineal_cur_a_steach->너비>=500?(한글입력?"[GD] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[GD]":"[EN]"),0xffffff,색상);
    사각영역(tèirmineal_cur_a_steach->co_chomharra_x+tèirmineal_cur_a_steach->너비-32,tèirmineal_cur_a_steach->세로좌표+4,26,22,0x5555b8);ainm_clàr(tèirmineal_cur_a_steach->co_chomharra_x+tèirmineal_cur_a_steach->너비-24,tèirmineal_cur_a_steach->세로좌표+7,"X",0xffffff,0x5555b8);
    susbaint_VALUE();
}
static void 장면그리기(void){
    if(!deasg_seall)return;사각영역(0,0,보드화면너비(),보드화면높이(),0x302018);사각영역(0,0,보드화면너비(),32,0x403127);
    사각영역(6,4,136,24,0x905020);ainm_clàr(14,8,"+ New terminal",0xffffff,0x905020);
    for(int 순번=0;순번<4;순번++)if(Windows_Liosta[순번].살아있음){unsigned còd_a_charactair=Focus==순번?0x905020:0x604438;사각영역(154+순번*112,4,106,24,còd_a_charactair);ainm_clàr(160+순번*112,8,"Terminal",0xffffff,còd_a_charactair);char sreang_dàta[2]={(char)('1'+순번),0};ainm_clàr(232+순번*112,8,sreang_dàta,0xffffff,còd_a_charactair);}
    if(!cur_a_steach_COUNT)ainm_clàr(140,210,"Click + New terminal to start",0xede9df,0x302018);
    for(int 순번=0;순번<cur_a_steach_COUNT;순번++)실행틀(òrdugh_VALUE[순번]);화면다시그림(Focus);tèirmineal_cur_a_steach=&Windows_Liosta[출력결과];
}
static void 영역그리기(int 가로,int inghearach_suidhich,int 폭,int faid_VALUE){
    if(!deasg_seall||!보드그림범위(&가로,&inghearach_suidhich,&폭,&faid_VALUE))return;
    for(int loidhne=inghearach_suidhich;loidhne<inghearach_suidhich+faid_VALUE;loidhne+=32){
        int 띠높이=inghearach_suidhich+faid_VALUE-loidhne;if(띠높이>32)띠높이=32;
        if(bòrd_Start_tarraing(가로,loidhne,폭,띠높이)){장면그리기();bòrd_Coilean_tarraing();}
    }
}
static void 다시그리기(void){영역그리기(0,0,보드화면너비(),보드화면높이());}
/* 서로 겹치지 않는 새 uinneag 영역과 이전 자리의 네 띠를 복구한다. */
static void 창자리그리기(int 가로,int inghearach_suidhich,int 폭,int faid_VALUE,tèirmineal_d413d4bc *uinneag){
    int 왼쪽=가로>(int)uinneag->co_chomharra_x?가로:(int)uinneag->co_chomharra_x;
    int 위쪽=inghearach_suidhich>(int)uinneag->세로좌표?inghearach_suidhich:(int)uinneag->세로좌표;
    int RIGHT=가로+폭<(int)(uinneag->co_chomharra_x+uinneag->너비)?가로+폭:(int)(uinneag->co_chomharra_x+uinneag->너비);
    int 아래쪽=inghearach_suidhich+faid_VALUE<(int)(uinneag->세로좌표+uinneag->높이)?inghearach_suidhich+faid_VALUE:(int)(uinneag->세로좌표+uinneag->높이);
    영역그리기(uinneag->co_chomharra_x,uinneag->세로좌표,uinneag->너비,uinneag->높이);
    if(왼쪽>=RIGHT||위쪽>=아래쪽){영역그리기(가로,inghearach_suidhich,폭,faid_VALUE);return;}
    영역그리기(가로,inghearach_suidhich,폭,위쪽-inghearach_suidhich);
    영역그리기(가로,아래쪽,폭,inghearach_suidhich+faid_VALUE-아래쪽);
    영역그리기(가로,위쪽,왼쪽-가로,아래쪽-위쪽);
    영역그리기(RIGHT,위쪽,가로+폭-RIGHT,아래쪽-위쪽);
}
static void 초점알리기(void){대기중=(대기중&~15u)|(unsigned)(Focus+1)|0x10000;}
void 터미널입력방식(unsigned 한글여부){
    한글입력=한글여부!=0;
    /* Update title bars only: a mode switch must not erase an EL0 drawing. */
    if(Focus>=0){
        tèirmineal_d413d4bc *uinneag_cur_a_steach=&Windows_Liosta[Focus];
        ainm_clàr(uinneag_cur_a_steach->co_chomharra_x+240,uinneag_cur_a_steach->세로좌표+7,uinneag_cur_a_steach->너비>=500?(한글입력?"[GD] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[GD]":"[EN]"),0xffffff,0x905020);
    }
}
static void 앞으로올리기(int aithnichear_VALUE){if(aithnichear_VALUE<0||aithnichear_VALUE>=4||!Windows_Liosta[aithnichear_VALUE].살아있음)return;int 현재위치=0;while(현재위치<cur_a_steach_COUNT&&òrdugh_VALUE[현재위치]!=aithnichear_VALUE)현재위치++;for(;현재위치+1<cur_a_steach_COUNT;현재위치++)òrdugh_VALUE[현재위치]=òrdugh_VALUE[현재위치+1];òrdugh_VALUE[cur_a_steach_COUNT-1]=aithnichear_VALUE;Focus=aithnichear_VALUE;초점알리기();다시그리기();}
static void 빈칸채우기(unsigned ROW_suidhich){for(unsigned còd_a_charactair=0;còd_a_charactair<최대열수;còd_a_charactair++){tèirmineal_cur_a_steach->글자칸들[ROW_suidhich%eachdraidh_loidhne_COUNT][còd_a_charactair]=0;tèirmineal_cur_a_steach->모양들[ROW_suidhich%eachdraidh_loidhne_COUNT][còd_a_charactair]=tèirmineal_cur_a_steach->전경색|(tèirmineal_cur_a_steach->배경색<<4);}}
static void glan_susbaint(void){tèirmineal_cur_a_steach->ROW_suidhich=tèirmineal_cur_a_steach->colbh_suidhich=tèirmineal_cur_a_steach->맨위=tèirmineal_cur_a_steach->sgrolaich=0;for(unsigned 반환값=0;반환값<eachdraidh_loidhne_COUNT;반환값++)빈칸채우기(반환값);if(보이는지())susbaint_VALUE();}
static int Create_cur_a_steach(void){
    if(!보드화면기억공간())return -19;int aithnichear_VALUE=0;while(aithnichear_VALUE<4&&Windows_Liosta[aithnichear_VALUE].살아있음)aithnichear_VALUE++;if(aithnichear_VALUE==4)return -28;
    deasg_seall=1;tèirmineal_cur_a_steach=&Windows_Liosta[aithnichear_VALUE];memset(tèirmineal_cur_a_steach,0,sizeof(*tèirmineal_cur_a_steach));tèirmineal_cur_a_steach->살아있음=1;tèirmineal_cur_a_steach->너비=568;tèirmineal_cur_a_steach->높이=360;tèirmineal_cur_a_steach->COLUMNS=68;tèirmineal_cur_a_steach->ROW_COUNT=19;tèirmineal_cur_a_steach->co_chomharra_x=12+aithnichear_VALUE*16;tèirmineal_cur_a_steach->세로좌표=48+aithnichear_VALUE*18;tèirmineal_cur_a_steach->전경색=7;tèirmineal_cur_a_steach->가리개보임=1;
    for(unsigned 반환값=0;반환값<eachdraidh_loidhne_COUNT;반환값++)빈칸채우기(반환값);òrdugh_VALUE[cur_a_steach_COUNT++]=aithnichear_VALUE;Focus=aithnichear_VALUE;대기중|=1u<<(4+aithnichear_VALUE);초점알리기();다시그리기();return aithnichear_VALUE+1;
}
static void dùin_uinneag(int aithnichear_VALUE){
    if(aithnichear_VALUE<0||aithnichear_VALUE>=4||!Windows_Liosta[aithnichear_VALUE].살아있음)return;Windows_Liosta[aithnichear_VALUE].살아있음=0;대기중|=1u<<(8+aithnichear_VALUE);
    int 현재위치=0;while(현재위치<cur_a_steach_COUNT&&òrdugh_VALUE[현재위치]!=aithnichear_VALUE)현재위치++;for(;현재위치+1<cur_a_steach_COUNT;현재위치++)òrdugh_VALUE[현재위치]=òrdugh_VALUE[현재위치+1];cur_a_steach_COUNT--;
    if(Focus==aithnichear_VALUE)Focus=cur_a_steach_COUNT?òrdugh_VALUE[cur_a_steach_COUNT-1]:-1;초점알리기();다시그리기();
}
static void 줄바꿈(void){tèirmineal_cur_a_steach->colbh_suidhich=0;tèirmineal_cur_a_steach->ROW_suidhich++;if(tèirmineal_cur_a_steach->ROW_suidhich>=tèirmineal_cur_a_steach->맨위+tèirmineal_cur_a_steach->ROW_COUNT){tèirmineal_cur_a_steach->맨위++;빈칸채우기(tèirmineal_cur_a_steach->ROW_suidhich);if(보이는지())susbaint_VALUE();}}
static void còd_a_charactair_451f2815(unsigned còd_a_charactair){
    if(còd_a_charactair==13){tèirmineal_cur_a_steach->colbh_suidhich=0;return;}if(còd_a_charactair==10){줄바꿈();return;}if(còd_a_charactair==8){if(tèirmineal_cur_a_steach->colbh_suidhich)tèirmineal_cur_a_steach->colbh_suidhich--;return;}
    if(còd_a_charactair==9){unsigned nì_COUNT=8-tèirmineal_cur_a_steach->colbh_suidhich%8;while(nì_COUNT--)còd_a_charactair_451f2815(' ');return;}if(còd_a_charactair<32||còd_a_charactair==127)return;
    unsigned 너비값=넓은글자(còd_a_charactair);if(tèirmineal_cur_a_steach->colbh_suidhich+너비값>tèirmineal_cur_a_steach->COLUMNS)줄바꿈();
    if(tèirmineal_cur_a_steach->글자칸들[tèirmineal_cur_a_steach->ROW_suidhich%eachdraidh_loidhne_COUNT][tèirmineal_cur_a_steach->colbh_suidhich]==0xffffffffu&&tèirmineal_cur_a_steach->colbh_suidhich){tèirmineal_cur_a_steach->글자칸들[tèirmineal_cur_a_steach->ROW_suidhich%eachdraidh_loidhne_COUNT][tèirmineal_cur_a_steach->colbh_suidhich-1]=' ';그리기(tèirmineal_cur_a_steach->ROW_suidhich,tèirmineal_cur_a_steach->colbh_suidhich-1);}
    if(넓은글자(tèirmineal_cur_a_steach->글자칸들[tèirmineal_cur_a_steach->ROW_suidhich%eachdraidh_loidhne_COUNT][tèirmineal_cur_a_steach->colbh_suidhich])==2&&tèirmineal_cur_a_steach->colbh_suidhich+1<tèirmineal_cur_a_steach->COLUMNS){tèirmineal_cur_a_steach->글자칸들[tèirmineal_cur_a_steach->ROW_suidhich%eachdraidh_loidhne_COUNT][tèirmineal_cur_a_steach->colbh_suidhich+1]=' ';그리기(tèirmineal_cur_a_steach->ROW_suidhich,tèirmineal_cur_a_steach->colbh_suidhich+1);}
    tèirmineal_cur_a_steach->글자칸들[tèirmineal_cur_a_steach->ROW_suidhich%eachdraidh_loidhne_COUNT][tèirmineal_cur_a_steach->colbh_suidhich]=còd_a_charactair;tèirmineal_cur_a_steach->모양들[tèirmineal_cur_a_steach->ROW_suidhich%eachdraidh_loidhne_COUNT][tèirmineal_cur_a_steach->colbh_suidhich]=tèirmineal_cur_a_steach->전경색|(tèirmineal_cur_a_steach->배경색<<4);
    if(너비값==2)tèirmineal_cur_a_steach->글자칸들[tèirmineal_cur_a_steach->ROW_suidhich%eachdraidh_loidhne_COUNT][tèirmineal_cur_a_steach->colbh_suidhich+1]=0xffffffffu;
    그리기(tèirmineal_cur_a_steach->ROW_suidhich,tèirmineal_cur_a_steach->colbh_suidhich);tèirmineal_cur_a_steach->colbh_suidhich+=너비값;
}
static void làmhrachan_smachd_SEQUENCE(unsigned còd_a_charactair){
    unsigned nì_COUNT=tèirmineal_cur_a_steach->매개값[0]?tèirmineal_cur_a_steach->매개값[0]:1;
    if(còd_a_charactair=='m')for(unsigned 순번=0;순번<=tèirmineal_cur_a_steach->매개색인;순번++){unsigned dàta_suidhich=tèirmineal_cur_a_steach->매개값[순번];if(!dàta_suidhich){tèirmineal_cur_a_steach->전경색=7;tèirmineal_cur_a_steach->배경색=0;}if(dàta_suidhich==1&&tèirmineal_cur_a_steach->전경색<8)tèirmineal_cur_a_steach->전경색+=8;if(dàta_suidhich==7){unsigned 유지=tèirmineal_cur_a_steach->전경색;tèirmineal_cur_a_steach->전경색=tèirmineal_cur_a_steach->배경색;tèirmineal_cur_a_steach->배경색=유지;}if(dàta_suidhich>=30&&dàta_suidhich<=37)tèirmineal_cur_a_steach->전경색=dàta_suidhich-30;if(dàta_suidhich>=90&&dàta_suidhich<=97)tèirmineal_cur_a_steach->전경색=dàta_suidhich-90+8;if(dàta_suidhich>=40&&dàta_suidhich<=47)tèirmineal_cur_a_steach->배경색=dàta_suidhich-40;if(dàta_suidhich>=100&&dàta_suidhich<=107)tèirmineal_cur_a_steach->배경색=dàta_suidhich-100+8;if(dàta_suidhich==39)tèirmineal_cur_a_steach->전경색=7;if(dàta_suidhich==49)tèirmineal_cur_a_steach->배경색=0;}
    if(còd_a_charactair=='J'&&(tèirmineal_cur_a_steach->매개값[0]==2||tèirmineal_cur_a_steach->매개값[0]==3))glan_susbaint();
    if(còd_a_charactair=='K'){unsigned 출발위치=tèirmineal_cur_a_steach->매개값[0]==2?0:tèirmineal_cur_a_steach->colbh_suidhich,도착위치=tèirmineal_cur_a_steach->매개값[0]==1?tèirmineal_cur_a_steach->colbh_suidhich+1:tèirmineal_cur_a_steach->COLUMNS;if(tèirmineal_cur_a_steach->매개값[0]==1)출발위치=0;for(unsigned 순번=출발위치;순번<도착위치&&순번<tèirmineal_cur_a_steach->COLUMNS;순번++){
        unsigned ROW_VALUE=tèirmineal_cur_a_steach->ROW_suidhich%eachdraidh_loidhne_COUNT,caractar_VALUE=tèirmineal_cur_a_steach->글자칸들[ROW_VALUE][순번],cruth_VALUE=tèirmineal_cur_a_steach->전경색|(tèirmineal_cur_a_steach->배경색<<4);
        /* 넓은 vi 화면에서도 이미 빈 칸의 cruth_clò_VALUE 화소를 되풀이해 칠하지 않는다. */
        int 바뀜=(caractar_VALUE!=0&&caractar_VALUE!=' ')||tèirmineal_cur_a_steach->모양들[ROW_VALUE][순번]!=cruth_VALUE;
        tèirmineal_cur_a_steach->글자칸들[ROW_VALUE][순번]=' ';tèirmineal_cur_a_steach->모양들[ROW_VALUE][순번]=cruth_VALUE;
        if(바뀜)그리기(tèirmineal_cur_a_steach->ROW_suidhich,순번);
    }}
    if(còd_a_charactair=='D')tèirmineal_cur_a_steach->colbh_suidhich=nì_COUNT>tèirmineal_cur_a_steach->colbh_suidhich?0:tèirmineal_cur_a_steach->colbh_suidhich-nì_COUNT;if(còd_a_charactair=='C')tèirmineal_cur_a_steach->colbh_suidhich=tèirmineal_cur_a_steach->colbh_suidhich+nì_COUNT>=tèirmineal_cur_a_steach->COLUMNS?tèirmineal_cur_a_steach->COLUMNS-1:tèirmineal_cur_a_steach->colbh_suidhich+nì_COUNT;
    if(còd_a_charactair=='G')tèirmineal_cur_a_steach->colbh_suidhich=nì_COUNT>tèirmineal_cur_a_steach->COLUMNS?tèirmineal_cur_a_steach->COLUMNS-1:nì_COUNT-1;if(còd_a_charactair=='A')tèirmineal_cur_a_steach->ROW_suidhich=nì_COUNT>tèirmineal_cur_a_steach->ROW_suidhich-tèirmineal_cur_a_steach->맨위?tèirmineal_cur_a_steach->맨위:tèirmineal_cur_a_steach->ROW_suidhich-nì_COUNT;
    if(còd_a_charactair=='B')tèirmineal_cur_a_steach->ROW_suidhich=tèirmineal_cur_a_steach->ROW_suidhich+nì_COUNT>=tèirmineal_cur_a_steach->맨위+tèirmineal_cur_a_steach->ROW_COUNT?tèirmineal_cur_a_steach->맨위+tèirmineal_cur_a_steach->ROW_COUNT-1:tèirmineal_cur_a_steach->ROW_suidhich+nì_COUNT;
    if(còd_a_charactair=='H'||còd_a_charactair=='f'){tèirmineal_cur_a_steach->ROW_suidhich=tèirmineal_cur_a_steach->맨위+(nì_COUNT>tèirmineal_cur_a_steach->ROW_COUNT?tèirmineal_cur_a_steach->ROW_COUNT:nì_COUNT)-1;unsigned co_chomharra_x=tèirmineal_cur_a_steach->매개값[1]?tèirmineal_cur_a_steach->매개값[1]:1;tèirmineal_cur_a_steach->colbh_suidhich=(co_chomharra_x>tèirmineal_cur_a_steach->COLUMNS?tèirmineal_cur_a_steach->COLUMNS:co_chomharra_x)-1;}
    if(còd_a_charactair=='s'){tèirmineal_cur_a_steach->저장행=tèirmineal_cur_a_steach->ROW_suidhich;tèirmineal_cur_a_steach->저장열=tèirmineal_cur_a_steach->colbh_suidhich;}if(còd_a_charactair=='u'){tèirmineal_cur_a_steach->ROW_suidhich=tèirmineal_cur_a_steach->저장행;tèirmineal_cur_a_steach->colbh_suidhich=tèirmineal_cur_a_steach->저장열<tèirmineal_cur_a_steach->COLUMNS?tèirmineal_cur_a_steach->저장열:tèirmineal_cur_a_steach->COLUMNS-1;}
    if((còd_a_charactair=='h'||còd_a_charactair=='l')&&tèirmineal_cur_a_steach->매개값[0]==25)tèirmineal_cur_a_steach->가리개보임=còd_a_charactair=='h';
}
void tèirmineal_baidht(unsigned SECOND_VALUE){
    tèirmineal_cur_a_steach=&Windows_Liosta[출력결과];if(!tèirmineal_cur_a_steach->살아있음)return;carait_VALUE(0);if(tèirmineal_cur_a_steach->sgrolaich){tèirmineal_cur_a_steach->sgrolaich=0;if(보이는지())susbaint_VALUE();}
    if(tèirmineal_cur_a_steach->탈출상태==1){tèirmineal_cur_a_steach->탈출상태=SECOND_VALUE=='['?2:0;tèirmineal_cur_a_steach->매개색인=0;for(unsigned 순번=0;순번<4;순번++)tèirmineal_cur_a_steach->매개값[순번]=0;}
    else if(tèirmineal_cur_a_steach->탈출상태==2){if(SECOND_VALUE=='?'){}else if(SECOND_VALUE>='0'&&SECOND_VALUE<='9'){if(tèirmineal_cur_a_steach->매개값[tèirmineal_cur_a_steach->매개색인]<10000)tèirmineal_cur_a_steach->매개값[tèirmineal_cur_a_steach->매개색인]=tèirmineal_cur_a_steach->매개값[tèirmineal_cur_a_steach->매개색인]*10+SECOND_VALUE-'0';}else if(SECOND_VALUE==';'&&tèirmineal_cur_a_steach->매개색인<3)tèirmineal_cur_a_steach->매개색인++;else{làmhrachan_smachd_SEQUENCE(SECOND_VALUE);tèirmineal_cur_a_steach->탈출상태=0;}}
    else if(SECOND_VALUE==27){tèirmineal_cur_a_steach->긴부호없는값=0;tèirmineal_cur_a_steach->탈출상태=1;}else{
        if(tèirmineal_cur_a_steach->긴부호없는값&&(SECOND_VALUE&0xc0)!=0x80){tèirmineal_cur_a_steach->긴부호없는값=0;còd_a_charactair_451f2815(0xfffd);}
        if(tèirmineal_cur_a_steach->긴부호없는값){tèirmineal_cur_a_steach->부호없는결과=tèirmineal_cur_a_steach->부호없는결과*64+(SECOND_VALUE&63);if(--tèirmineal_cur_a_steach->긴부호없는값==0)còd_a_charactair_451f2815(tèirmineal_cur_a_steach->부호없는결과<tèirmineal_cur_a_steach->SMALL_VALUE||tèirmineal_cur_a_steach->부호없는결과>0x10ffff||(tèirmineal_cur_a_steach->부호없는결과>=0xd800&&tèirmineal_cur_a_steach->부호없는결과<=0xdfff)?0xfffd:tèirmineal_cur_a_steach->부호없는결과);}
        else if(SECOND_VALUE<128)còd_a_charactair_451f2815(SECOND_VALUE);else if(SECOND_VALUE>=0xc2&&SECOND_VALUE<=0xf4){tèirmineal_cur_a_steach->긴부호없는값=SECOND_VALUE<0xe0?1:SECOND_VALUE<0xf0?2:3;tèirmineal_cur_a_steach->부호없는결과=SECOND_VALUE&((1u<<(6-tèirmineal_cur_a_steach->긴부호없는값))-1);tèirmineal_cur_a_steach->SMALL_VALUE=tèirmineal_cur_a_steach->긴부호없는값==1?128:tèirmineal_cur_a_steach->긴부호없는값==2?2048:65536;}else còd_a_charactair_451f2815(0xfffd);
    }carait_VALUE(1);
}
int tèirmineal_ri_dhèiligeadh(void){return 대기중!=0;}
/* 모서리 INDEX: 1 좌상, 2 우상, 3 좌하, 4 우하. */
static int atharraich_am_meud_slaod=-1,잡은모서리,잡은가로,잡은세로,처음가로,처음세로,처음너비,처음높이;
static int 가리킨창(int 가로,int inghearach_suidhich) {
    for(int SEQUENCE_VALUE=cur_a_steach_COUNT-1;SEQUENCE_VALUE>=0;SEQUENCE_VALUE--){
        int aithnichear_VALUE=òrdugh_VALUE[SEQUENCE_VALUE];tèirmineal_d413d4bc *uinneag=&Windows_Liosta[aithnichear_VALUE];
        if(가로>=(int)uinneag->co_chomharra_x&&inghearach_suidhich>=(int)uinneag->세로좌표&&
           가로<(int)(uinneag->co_chomharra_x+uinneag->너비)&&inghearach_suidhich<(int)(uinneag->세로좌표+uinneag->높이))return aithnichear_VALUE;
    }return -1;
}
static int 모서리찾기(int aithnichear_VALUE,int 가로,int inghearach_suidhich) {
    if(aithnichear_VALUE<0)return 0;tèirmineal_d413d4bc *uinneag=&Windows_Liosta[aithnichear_VALUE];
    int 왼쪽=가로<(int)uinneag->co_chomharra_x+8,RIGHT=가로>=(int)(uinneag->co_chomharra_x+uinneag->너비)-8;
    int 위쪽=inghearach_suidhich<(int)uinneag->세로좌표+8,아래쪽=inghearach_suidhich>=(int)(uinneag->세로좌표+uinneag->높이)-8;
    return (왼쪽||RIGHT)&&(위쪽||아래쪽)?1+RIGHT+아래쪽*2:0;
}
static int sgaradair_VALUE(int VALUE,int 최소,int 최대){return VALUE<최소?최소:VALUE>최대?최대:VALUE;}
static void gluais_atharraich_am_meud(int 가로,int inghearach_suidhich) {
    tèirmineal_d413d4bc *uinneag=&Windows_Liosta[atharraich_am_meud_slaod];int 왼쪽=처음가로,위쪽=처음세로,RIGHT=처음가로+처음너비,아래쪽=처음세로+처음높이;
    if(잡은모서리==1||잡은모서리==3)왼쪽=sgaradair_VALUE(처음가로+가로-잡은가로,0,RIGHT-360);
    else RIGHT=sgaradair_VALUE(처음가로+처음너비+가로-잡은가로,왼쪽+360,보드화면너비());
    if(잡은모서리<=2)위쪽=sgaradair_VALUE(처음세로+inghearach_suidhich-잡은세로,34,아래쪽-216);
    else 아래쪽=sgaradair_VALUE(처음세로+처음높이+inghearach_suidhich-잡은세로,위쪽+216,보드화면높이());
    unsigned COLUMNS=(RIGHT-왼쪽-24)/8,ROW_COUNT=(아래쪽-위쪽-56)/16;
    if(uinneag->COLUMNS!=COLUMNS||uinneag->ROW_COUNT!=ROW_COUNT){
        uinneag->크기바뀜=1;uinneag->COLUMNS=COLUMNS;uinneag->ROW_COUNT=ROW_COUNT;
        if(uinneag->colbh_suidhich>=COLUMNS)uinneag->colbh_suidhich=COLUMNS-1;
        if(uinneag->ROW_suidhich>=uinneag->맨위+ROW_COUNT)uinneag->맨위=uinneag->ROW_suidhich-ROW_COUNT+1;
        unsigned 한도=uinneag->맨위;if(한도>eachdraidh_loidhne_COUNT-ROW_COUNT)한도=eachdraidh_loidhne_COUNT-ROW_COUNT;
        if(uinneag->sgrolaich>한도)uinneag->sgrolaich=한도;
    }
    int 옛가로=uinneag->co_chomharra_x,옛세로=uinneag->세로좌표,옛폭=uinneag->너비,옛길이=uinneag->높이;
    if(옛가로==왼쪽&&옛세로==위쪽&&옛폭==RIGHT-왼쪽&&옛길이==아래쪽-위쪽)return;
    uinneag->co_chomharra_x=왼쪽;uinneag->세로좌표=위쪽;uinneag->너비=RIGHT-왼쪽;uinneag->높이=아래쪽-위쪽;
    창자리그리기(옛가로,옛세로,옛폭,옛길이,uinneag);
}
void tèirmineal_tomhaire(unsigned air_adhart_nì,int co_chomharra_x,int 세로좌표){
    unsigned 눌림=air_adhart_nì&~단추들;단추들=air_adhart_nì;
    if(!deasg_seall){slaod_VALUE=-1;atharraich_am_meud_slaod=-1;bòrd_tomhaire(co_chomharra_x,세로좌표,1);return;}
    if(!(air_adhart_nì&1)){slaod_VALUE=-1;atharraich_am_meud_slaod=-1;}
    if(atharraich_am_meud_slaod>=0&&!Windows_Liosta[atharraich_am_meud_slaod].살아있음)atharraich_am_meud_slaod=-1;
    if(slaod_VALUE>=0&&!Windows_Liosta[slaod_VALUE].살아있음)slaod_VALUE=-1;
    if(atharraich_am_meud_slaod>=0){
        gluais_atharraich_am_meud(co_chomharra_x,세로좌표);bòrd_tomhaire(co_chomharra_x,세로좌표,잡은모서리==1||잡은모서리==4?2:3);return;
    }
    bòrd_tomhaire(co_chomharra_x,세로좌표,1);
    if(slaod_VALUE>=0){
        tèirmineal_d413d4bc *uinneag=&Windows_Liosta[slaod_VALUE];
        int 옛가로=uinneag->co_chomharra_x,옛세로=uinneag->세로좌표;
        uinneag->co_chomharra_x=sgaradair_VALUE(co_chomharra_x-끌기가로,0,보드화면너비()-uinneag->너비);
        uinneag->세로좌표=sgaradair_VALUE(세로좌표-끌기세로,34,보드화면높이()-uinneag->높이);
        if(옛가로!=(int)uinneag->co_chomharra_x||옛세로!=(int)uinneag->세로좌표)창자리그리기(옛가로,옛세로,uinneag->너비,uinneag->높이,uinneag);
        return;
    }
    extern int 화면덮음(int,int,int);
    if(화면덮음(Focus,co_chomharra_x,세로좌표)){화면가리킴(Focus,눌림,co_chomharra_x,세로좌표);return;}
    int aithnichear_VALUE=가리킨창(co_chomharra_x,세로좌표),모서리=모서리찾기(aithnichear_VALUE,co_chomharra_x,세로좌표);
    if(모서리)bòrd_tomhaire(co_chomharra_x,세로좌표,모서리==1||모서리==4?2:3);
    if(눌림&1){
        if(모서리){
            tèirmineal_d413d4bc *uinneag=&Windows_Liosta[aithnichear_VALUE];atharraich_am_meud_slaod=aithnichear_VALUE;잡은모서리=모서리;잡은가로=co_chomharra_x;잡은세로=세로좌표;
            처음가로=uinneag->co_chomharra_x;처음세로=uinneag->세로좌표;처음너비=uinneag->너비;처음높이=uinneag->높이;
            if(aithnichear_VALUE!=Focus)앞으로올리기(aithnichear_VALUE);return;
        }
        if(세로좌표<32&&co_chomharra_x>=6&&co_chomharra_x<142){Create_cur_a_steach();return;}
        if(세로좌표<32&&co_chomharra_x>=154&&co_chomharra_x<602){앞으로올리기((co_chomharra_x-154)/112);return;}
        if(aithnichear_VALUE>=0){
            tèirmineal_d413d4bc *uinneag=&Windows_Liosta[aithnichear_VALUE];
            if(세로좌표<(int)uinneag->세로좌표+30&&co_chomharra_x>=(int)(uinneag->co_chomharra_x+uinneag->너비)-32){dùin_uinneag(aithnichear_VALUE);return;}
            if(aithnichear_VALUE!=Focus)앞으로올리기(aithnichear_VALUE);
            if(세로좌표<(int)uinneag->세로좌표+30){slaod_VALUE=aithnichear_VALUE;끌기가로=co_chomharra_x-uinneag->co_chomharra_x;끌기세로=세로좌표-uinneag->세로좌표;}return;
        }
    }
    if(Focus>=0&&(눌림&(8|16))){tèirmineal_cur_a_steach=&Windows_Liosta[Focus];if(눌림&8){unsigned 한도=tèirmineal_cur_a_steach->맨위;if(한도>eachdraidh_loidhne_COUNT-tèirmineal_cur_a_steach->ROW_COUNT)한도=eachdraidh_loidhne_COUNT-tèirmineal_cur_a_steach->ROW_COUNT;tèirmineal_cur_a_steach->sgrolaich=tèirmineal_cur_a_steach->sgrolaich+9>한도?한도:tèirmineal_cur_a_steach->sgrolaich+9;}else tèirmineal_cur_a_steach->sgrolaich=tèirmineal_cur_a_steach->sgrolaich<9?0:tèirmineal_cur_a_steach->sgrolaich-9;다시그리기();}
}
void 터미널바로가기키(unsigned 누름값){if(누름값==1)Create_cur_a_steach();if(누름값==2&&cur_a_steach_COUNT)앞으로올리기(òrdugh_VALUE[0]);if(누름값==3)dùin_uinneag(Focus);}
inneal_Word bòrd_tèirmineal(inneal_Word Gnìomh){
    if(Gnìomh==300){if(!Windows_Liosta[출력결과].살아있음)return Create_cur_a_steach();deasg_seall=1;다시그리기();return 0;}
    if(Gnìomh==0){dùin_uinneag(Focus);return 0;}if(Gnìomh==1)return (uint32_t)Create_cur_a_steach();if(Gnìomh==2)return Focus>=0;
    if(Gnìomh==9){deasg_seall=0;return 0;}if(Gnìomh==7)return cur_a_steach_COUNT;if(Gnìomh==10)return Focus+1;if(Gnìomh==11)return 출력결과;
    if(Gnìomh==13){tèirmineal_d413d4bc *uinneag=&Windows_Liosta[출력결과];return uinneag->살아있음?(uinneag->ROW_COUNT<<16)|uinneag->COLUMNS:(19<<16)|68;}
    if(Gnìomh==14){unsigned VALUE=Windows_Liosta[출력결과].크기바뀜;Windows_Liosta[출력결과].크기바뀜=0;return VALUE;}
    if(Gnìomh==12){unsigned VALUE=대기중;대기중=0;return VALUE;}
    if(Gnìomh>=20&&Gnìomh<24)return Windows_Liosta[Gnìomh-20].살아있음;
    if(Gnìomh>=100&&Gnìomh<104){출력결과=Gnìomh-100;tèirmineal_cur_a_steach=&Windows_Liosta[출력결과];return 0;}
    if(Gnìomh>=200&&Gnìomh<204){앞으로올리기(Gnìomh-200);return 0;}
    if(Gnìomh==3){다시그리기();return 0;}tèirmineal_cur_a_steach=&Windows_Liosta[출력결과];if(!tèirmineal_cur_a_steach->살아있음)return 0;
    if(Gnìomh==4)glan_susbaint();if(Gnìomh==5||Gnìomh==6){unsigned 이전=단추들;tèirmineal_tomhaire(Gnìomh==5?8:16,0,0);단추들=이전;}return 1;
}
