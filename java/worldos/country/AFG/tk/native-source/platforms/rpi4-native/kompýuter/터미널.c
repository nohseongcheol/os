#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* 자체 네 penjire 합성과 UTF-8 터미널. 바뀐 영역의 완성 그림만 표시한다. */
#include <stdint.h>
#include <stddef.h>
typedef uintptr_t kompýuter_Söz;
extern kompýuter_Söz 보드화소(kompýuter_Söz,kompýuter_Söz,kompýuter_Söz),보드화면기억공간(void);
extern void *memset(void *,int,size_t);
extern const unsigned char 터미널글꼴자료[];
#define 최대열수 237
#define 기록줄수 160
typedef struct {
    uint32_t 글자칸들[기록줄수][최대열수]; uint8_t 모양들[기록줄수][최대열수];
    unsigned 너비,높이,열수,행수,크기바뀜;
    unsigned 살아있음,x_koordinatasy,세로좌표,행위치,열위치,맨위,towla,전경색,배경색,탈출상태,매개값[4],매개색인,저장행,저장열;
    unsigned 부호없는결과,긴부호없는값,작은값,대체화면,가리개보임;
} 터미널상태;
static 터미널상태 Windows_Sanaw[4];
static int Fokus=-1,출력결과,tertip_baha[4],항목수,süýşür_baha=-1,끌기가로,끌기세로;
static unsigned 대기중,단추들,iş_stoly_görkez,한글입력;
static const uint32_t 색상들[16]={0x201a15,0x6060df,0x9dcc86,0x80cfea,0xefaf72,0xca96c9,0xceda76,0xede9df,0x858078,0x8888ff,0xb9eba7,0xa5eaff,0xffcc99,0xf0bef1,0xf0f0a0,0xffffff};
extern int 화면보임(int),화면가리킴(int,unsigned,int,int);
extern void 화면다시그림(int);
static 터미널상태 *터미널항목;
static unsigned 넓은글자(unsigned nyşanyň_kody){return nyşanyň_kody>=256?2:1;}
static void 사각영역(unsigned x_koordinatasy,unsigned 세로좌표,unsigned 너비값,unsigned 높이값,unsigned 색상){
    보드사각그림(x_koordinatasy,세로좌표,너비값,높이값,색상);
}
void 터미널글자그림(unsigned x_koordinatasy,unsigned 세로좌표,unsigned nyşanyň_kody,unsigned 전경색,unsigned 배경색){
    unsigned 너비=넓은글자(nyşanyň_kody)*8;if(nyşanyň_kody==0xffffffffu)return;
    int 왼쪽=x_koordinatasy,위쪽=세로좌표,폭=너비,dowamlylyk_baha=16;
    if(!보드그림범위(&왼쪽,&위쪽,&폭,&dowamlylyk_baha))return;
    if(nyşanyň_kody==' '){보드사각그림(왼쪽,위쪽,폭,dowamlylyk_baha,배경색);return;}
    unsigned 색인=nyşanyň_kody<65536?nyşanyň_kody:nyşanyň_kody>=0x1f600&&nyşanyň_kody<0x1f650?65536+nyşanyň_kody-0x1f600:0xfffd;
    const unsigned char *şrift_baha=터미널글꼴자료+색인*32;
    for(int setir=위쪽;setir<위쪽+dowamlylyk_baha;setir++){unsigned 비트들=şrift_baha[(setir-세로좌표)*2]*256+şrift_baha[(setir-세로좌표)*2+1];for(int ýer_girizmeklik=왼쪽;ýer_girizmeklik<왼쪽+폭;ýer_girizmeklik++)보드화소(ýer_girizmeklik,setir,(비트들&(0x8000>>(ýer_girizmeklik-x_koordinatasy)))?전경색:배경색);}
}
static void at_tablisa(unsigned x_koordinatasy,unsigned 세로좌표,const char *setir_maglumat,unsigned 전경색,unsigned 배경색){while(*setir_maglumat){unsigned nyşanyň_kody=(unsigned char)*setir_maglumat++, 남은수=0;if(nyşanyň_kody>=0xc0){남은수=nyşanyň_kody<0xe0?1:nyşanyň_kody<0xf0?2:3;nyşanyň_kody&=(1u<<(6-남은수))-1;while(남은수--&&*setir_maglumat)nyşanyň_kody=(nyşanyň_kody<<6)|((unsigned char)*setir_maglumat++&63);}터미널글자그림(x_koordinatasy,세로좌표,nyşanyň_kody,전경색,배경색);x_koordinatasy+=넓은글자(nyşanyň_kody)*8;}}
static unsigned 첫항목(void){return 터미널항목->맨위;}
static int 보이는지(void){return 터미널항목->살아있음&&Fokus>=0&&터미널항목==&Windows_Sanaw[Fokus]&&!화면보임(Fokus);}
static void 그리기(unsigned 행위치,unsigned 열위치){
    if(!보이는지()||행위치<첫항목()-터미널항목->towla||행위치>=첫항목()-터미널항목->towla+터미널항목->행수||열위치>=터미널항목->열수)return;
    unsigned nyşanyň_kody=터미널항목->글자칸들[행위치%기록줄수][열위치],setir_maglumat=터미널항목->모양들[행위치%기록줄수][열위치];
    if(넓은글자(nyşanyň_kody)==2&&열위치+1>=터미널항목->열수)nyşanyň_kody=' ';
    터미널글자그림(터미널항목->x_koordinatasy+12+열위치*8,터미널항목->세로좌표+36+(행위치-첫항목()+터미널항목->towla)*16,nyşanyň_kody?nyşanyň_kody:' ',색상들[setir_maglumat&15],색상들[setir_maglumat>>4]);
}
static void derejä_göterme_baha(int görkez_penjire){if(!보이는지()||터미널항목->towla||터미널항목->열위치>=터미널항목->열수||터미널항목->행위치<터미널항목->맨위||터미널항목->행위치>=터미널항목->맨위+터미널항목->행수)return;
    if(!görkez_penjire||!터미널항목->가리개보임)그리기(터미널항목->행위치,터미널항목->열위치);else 사각영역(터미널항목->x_koordinatasy+12+터미널항목->열위치*8,터미널항목->세로좌표+36+(터미널항목->행위치-터미널항목->맨위)*16+14,8,2,색상들[터미널항목->전경색]);}
static void Mazmun_baha(void){
    사각영역(터미널항목->x_koordinatasy+12,터미널항목->세로좌표+36,터미널항목->열수*8,터미널항목->행수*16,색상들[0]);
    int 가로=터미널항목->x_koordinatasy+12,세로=터미널항목->세로좌표+36,폭=터미널항목->열수*8,dowamlylyk_baha=터미널항목->행수*16;
    if(보드그림범위(&가로,&세로,&폭,&dowamlylyk_baha)){
    unsigned 첫줄=(세로-터미널항목->세로좌표-36)/16,끝줄=(세로+dowamlylyk_baha-터미널항목->세로좌표-36+15)/16;
    unsigned 첫칸=(가로-터미널항목->x_koordinatasy-12)/8,끝칸=(가로+폭-터미널항목->x_koordinatasy-12+7)/8;
    if(첫칸)첫칸--; /* 잘림 경계 왼쪽에서 시작한 두 ýer_girizmeklik 글자도 그린다. */
    for(unsigned 반환값=첫줄;반환값<끝줄;반환값++)for(unsigned nyşanyň_kody=첫칸;nyşanyň_kody<끝칸;nyşanyň_kody++){
        unsigned 행위치=첫항목()-터미널항목->towla+반환값,nyşan_baha_068c2631=터미널항목->글자칸들[행위치%기록줄수][nyşanyň_kody],setir_maglumat=터미널항목->모양들[행위치%기록줄수][nyşanyň_kody];
        if(넓은글자(nyşan_baha_068c2631)==2&&nyşanyň_kody+1>=터미널항목->열수)nyşan_baha_068c2631=' ';
        if((nyşan_baha_068c2631==0||nyşan_baha_068c2631==' ')&&(setir_maglumat>>4)==0)continue;
        터미널글자그림(터미널항목->x_koordinatasy+12+nyşanyň_kody*8,터미널항목->세로좌표+36+반환값*16,nyşan_baha_068c2631?nyşan_baha_068c2631:' ',색상들[setir_maglumat&15],색상들[setir_maglumat>>4]);
    }}
    at_tablisa(터미널항목->x_koordinatasy+12,터미널항목->세로좌표+터미널항목->높이-18,터미널항목->towla?"PgDn: recent output":터미널항목->너비>=500?"F6: next | Corner + left drag: resize":"Corner + left drag: resize",0xece8e2,0x403127);derejä_göterme_baha(1);
}
static void 실행틀(int tanaýjy_baha){
    터미널항목=&Windows_Sanaw[tanaýjy_baha];
    int 가로=터미널항목->x_koordinatasy,세로=터미널항목->세로좌표,폭=터미널항목->너비,dowamlylyk_baha=터미널항목->높이;
    if(!보드그림범위(&가로,&세로,&폭,&dowamlylyk_baha))return;
    사각영역(터미널항목->x_koordinatasy,터미널항목->세로좌표,터미널항목->너비,터미널항목->높이,0x403127);
    unsigned 색상=tanaýjy_baha==Fokus?0x905020:0x604438;사각영역(터미널항목->x_koordinatasy,터미널항목->세로좌표,터미널항목->너비,30,색상);
    at_tablisa(터미널항목->x_koordinatasy+12,터미널항목->세로좌표+7,"JKOROS Terminal",0xffffff,색상);
    char 수치[2]={(char)('1'+tanaýjy_baha),0};at_tablisa(터미널항목->x_koordinatasy+148,터미널항목->세로좌표+7,수치,0xffffff,색상);
    at_tablisa(터미널항목->x_koordinatasy+240,터미널항목->세로좌표+7,터미널항목->너비>=500?(한글입력?"[TK] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[TK]":"[EN]"),0xffffff,색상);
    사각영역(터미널항목->x_koordinatasy+터미널항목->너비-32,터미널항목->세로좌표+4,26,22,0x5555b8);at_tablisa(터미널항목->x_koordinatasy+터미널항목->너비-24,터미널항목->세로좌표+7,"X",0xffffff,0x5555b8);
    Mazmun_baha();
}
static void 장면그리기(void){
    if(!iş_stoly_görkez)return;사각영역(0,0,보드화면너비(),보드화면높이(),0x302018);사각영역(0,0,보드화면너비(),32,0x403127);
    사각영역(6,4,136,24,0x905020);at_tablisa(14,8,"+ New terminal",0xffffff,0x905020);
    for(int 순번=0;순번<4;순번++)if(Windows_Sanaw[순번].살아있음){unsigned nyşanyň_kody=Fokus==순번?0x905020:0x604438;사각영역(154+순번*112,4,106,24,nyşanyň_kody);at_tablisa(160+순번*112,8,"Terminal",0xffffff,nyşanyň_kody);char setir_maglumat[2]={(char)('1'+순번),0};at_tablisa(232+순번*112,8,setir_maglumat,0xffffff,nyşanyň_kody);}
    if(!항목수)at_tablisa(140,210,"Click + New terminal to start",0xede9df,0x302018);
    for(int 순번=0;순번<항목수;순번++)실행틀(tertip_baha[순번]);화면다시그림(Fokus);터미널항목=&Windows_Sanaw[출력결과];
}
static void 영역그리기(int 가로,int 세로,int 폭,int dowamlylyk_baha){
    if(!iş_stoly_görkez||!보드그림범위(&가로,&세로,&폭,&dowamlylyk_baha))return;
    for(int setir=세로;setir<세로+dowamlylyk_baha;setir+=32){
        int 띠높이=세로+dowamlylyk_baha-setir;if(띠높이>32)띠높이=32;
        if(보드그림시작(가로,setir,폭,띠높이)){장면그리기();보드그림마침();}
    }
}
static void 다시그리기(void){영역그리기(0,0,보드화면너비(),보드화면높이());}
/* 서로 겹치지 않는 새 penjire 영역과 이전 자리의 네 띠를 복구한다. */
static void 창자리그리기(int 가로,int 세로,int 폭,int dowamlylyk_baha,터미널상태 *penjire){
    int 왼쪽=가로>(int)penjire->x_koordinatasy?가로:(int)penjire->x_koordinatasy;
    int 위쪽=세로>(int)penjire->세로좌표?세로:(int)penjire->세로좌표;
    int 오른쪽=가로+폭<(int)(penjire->x_koordinatasy+penjire->너비)?가로+폭:(int)(penjire->x_koordinatasy+penjire->너비);
    int 아래쪽=세로+dowamlylyk_baha<(int)(penjire->세로좌표+penjire->높이)?세로+dowamlylyk_baha:(int)(penjire->세로좌표+penjire->높이);
    영역그리기(penjire->x_koordinatasy,penjire->세로좌표,penjire->너비,penjire->높이);
    if(왼쪽>=오른쪽||위쪽>=아래쪽){영역그리기(가로,세로,폭,dowamlylyk_baha);return;}
    영역그리기(가로,세로,폭,위쪽-세로);
    영역그리기(가로,아래쪽,폭,세로+dowamlylyk_baha-아래쪽);
    영역그리기(가로,위쪽,왼쪽-가로,아래쪽-위쪽);
    영역그리기(오른쪽,위쪽,가로+폭-오른쪽,아래쪽-위쪽);
}
static void 초점알리기(void){대기중=(대기중&~15u)|(unsigned)(Fokus+1)|0x10000;}
void 터미널입력방식(unsigned 한글여부){
    한글입력=한글여부!=0;
    /* Update title bars only: a mode switch must not erase an EL0 drawing. */
    if(Fokus>=0){
        터미널상태 *penjire_girizmeklik=&Windows_Sanaw[Fokus];
        at_tablisa(penjire_girizmeklik->x_koordinatasy+240,penjire_girizmeklik->세로좌표+7,penjire_girizmeklik->너비>=500?(한글입력?"[TK] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[TK]":"[EN]"),0xffffff,0x905020);
    }
}
static void 앞으로올리기(int tanaýjy_baha){if(tanaýjy_baha<0||tanaýjy_baha>=4||!Windows_Sanaw[tanaýjy_baha].살아있음)return;int 현재위치=0;while(현재위치<항목수&&tertip_baha[현재위치]!=tanaýjy_baha)현재위치++;for(;현재위치+1<항목수;현재위치++)tertip_baha[현재위치]=tertip_baha[현재위치+1];tertip_baha[항목수-1]=tanaýjy_baha;Fokus=tanaýjy_baha;초점알리기();다시그리기();}
static void 빈칸채우기(unsigned 행위치){for(unsigned nyşanyň_kody=0;nyşanyň_kody<최대열수;nyşanyň_kody++){터미널항목->글자칸들[행위치%기록줄수][nyşanyň_kody]=0;터미널항목->모양들[행위치%기록줄수][nyşanyň_kody]=터미널항목->전경색|(터미널항목->배경색<<4);}}
static void arassala_TOC(void){터미널항목->행위치=터미널항목->열위치=터미널항목->맨위=터미널항목->towla=0;for(unsigned 반환값=0;반환값<기록줄수;반환값++)빈칸채우기(반환값);if(보이는지())Mazmun_baha();}
static int döretmek_girizmeklik(void){
    if(!보드화면기억공간())return -19;int tanaýjy_baha=0;while(tanaýjy_baha<4&&Windows_Sanaw[tanaýjy_baha].살아있음)tanaýjy_baha++;if(tanaýjy_baha==4)return -28;
    iş_stoly_görkez=1;터미널항목=&Windows_Sanaw[tanaýjy_baha];memset(터미널항목,0,sizeof(*터미널항목));터미널항목->살아있음=1;터미널항목->너비=568;터미널항목->높이=360;터미널항목->열수=68;터미널항목->행수=19;터미널항목->x_koordinatasy=12+tanaýjy_baha*16;터미널항목->세로좌표=48+tanaýjy_baha*18;터미널항목->전경색=7;터미널항목->가리개보임=1;
    for(unsigned 반환값=0;반환값<기록줄수;반환값++)빈칸채우기(반환값);tertip_baha[항목수++]=tanaýjy_baha;Fokus=tanaýjy_baha;대기중|=1u<<(4+tanaýjy_baha);초점알리기();다시그리기();return tanaýjy_baha+1;
}
static void ýap_penjire(int tanaýjy_baha){
    if(tanaýjy_baha<0||tanaýjy_baha>=4||!Windows_Sanaw[tanaýjy_baha].살아있음)return;Windows_Sanaw[tanaýjy_baha].살아있음=0;대기중|=1u<<(8+tanaýjy_baha);
    int 현재위치=0;while(현재위치<항목수&&tertip_baha[현재위치]!=tanaýjy_baha)현재위치++;for(;현재위치+1<항목수;현재위치++)tertip_baha[현재위치]=tertip_baha[현재위치+1];항목수--;
    if(Fokus==tanaýjy_baha)Fokus=항목수?tertip_baha[항목수-1]:-1;초점알리기();다시그리기();
}
static void 줄바꿈(void){터미널항목->열위치=0;터미널항목->행위치++;if(터미널항목->행위치>=터미널항목->맨위+터미널항목->행수){터미널항목->맨위++;빈칸채우기(터미널항목->행위치);if(보이는지())Mazmun_baha();}}
static void nyşanyň_kody_451f2815(unsigned nyşanyň_kody){
    if(nyşanyň_kody==13){터미널항목->열위치=0;return;}if(nyşanyň_kody==10){줄바꿈();return;}if(nyşanyň_kody==8){if(터미널항목->열위치)터미널항목->열위치--;return;}
    if(nyşanyň_kody==9){unsigned 개수=8-터미널항목->열위치%8;while(개수--)nyşanyň_kody_451f2815(' ');return;}if(nyşanyň_kody<32||nyşanyň_kody==127)return;
    unsigned 너비값=넓은글자(nyşanyň_kody);if(터미널항목->열위치+너비값>터미널항목->열수)줄바꿈();
    if(터미널항목->글자칸들[터미널항목->행위치%기록줄수][터미널항목->열위치]==0xffffffffu&&터미널항목->열위치){터미널항목->글자칸들[터미널항목->행위치%기록줄수][터미널항목->열위치-1]=' ';그리기(터미널항목->행위치,터미널항목->열위치-1);}
    if(넓은글자(터미널항목->글자칸들[터미널항목->행위치%기록줄수][터미널항목->열위치])==2&&터미널항목->열위치+1<터미널항목->열수){터미널항목->글자칸들[터미널항목->행위치%기록줄수][터미널항목->열위치+1]=' ';그리기(터미널항목->행위치,터미널항목->열위치+1);}
    터미널항목->글자칸들[터미널항목->행위치%기록줄수][터미널항목->열위치]=nyşanyň_kody;터미널항목->모양들[터미널항목->행위치%기록줄수][터미널항목->열위치]=터미널항목->전경색|(터미널항목->배경색<<4);
    if(너비값==2)터미널항목->글자칸들[터미널항목->행위치%기록줄수][터미널항목->열위치+1]=0xffffffffu;
    그리기(터미널항목->행위치,터미널항목->열위치);터미널항목->열위치+=너비값;
}
static void ryçag_dolandyryş_SEQUENCE(unsigned nyşanyň_kody){
    unsigned 개수=터미널항목->매개값[0]?터미널항목->매개값[0]:1;
    if(nyşanyň_kody=='m')for(unsigned 순번=0;순번<=터미널항목->매개색인;순번++){unsigned 자료위치=터미널항목->매개값[순번];if(!자료위치){터미널항목->전경색=7;터미널항목->배경색=0;}if(자료위치==1&&터미널항목->전경색<8)터미널항목->전경색+=8;if(자료위치==7){unsigned 유지=터미널항목->전경색;터미널항목->전경색=터미널항목->배경색;터미널항목->배경색=유지;}if(자료위치>=30&&자료위치<=37)터미널항목->전경색=자료위치-30;if(자료위치>=90&&자료위치<=97)터미널항목->전경색=자료위치-90+8;if(자료위치>=40&&자료위치<=47)터미널항목->배경색=자료위치-40;if(자료위치>=100&&자료위치<=107)터미널항목->배경색=자료위치-100+8;if(자료위치==39)터미널항목->전경색=7;if(자료위치==49)터미널항목->배경색=0;}
    if(nyşanyň_kody=='J'&&(터미널항목->매개값[0]==2||터미널항목->매개값[0]==3))arassala_TOC();
    if(nyşanyň_kody=='K'){unsigned 출발위치=터미널항목->매개값[0]==2?0:터미널항목->열위치,도착위치=터미널항목->매개값[0]==1?터미널항목->열위치+1:터미널항목->열수;if(터미널항목->매개값[0]==1)출발위치=0;for(unsigned 순번=출발위치;순번<도착위치&&순번<터미널항목->열수;순번++){
        unsigned setir_baha=터미널항목->행위치%기록줄수,nyşan_baha_068c2631=터미널항목->글자칸들[setir_baha][순번],şekil_baha=터미널항목->전경색|(터미널항목->배경색<<4);
        /* 넓은 vi 화면에서도 이미 빈 칸의 şrift_baha 화소를 되풀이해 칠하지 않는다. */
        int 바뀜=(nyşan_baha_068c2631!=0&&nyşan_baha_068c2631!=' ')||터미널항목->모양들[setir_baha][순번]!=şekil_baha;
        터미널항목->글자칸들[setir_baha][순번]=' ';터미널항목->모양들[setir_baha][순번]=şekil_baha;
        if(바뀜)그리기(터미널항목->행위치,순번);
    }}
    if(nyşanyň_kody=='D')터미널항목->열위치=개수>터미널항목->열위치?0:터미널항목->열위치-개수;if(nyşanyň_kody=='C')터미널항목->열위치=터미널항목->열위치+개수>=터미널항목->열수?터미널항목->열수-1:터미널항목->열위치+개수;
    if(nyşanyň_kody=='G')터미널항목->열위치=개수>터미널항목->열수?터미널항목->열수-1:개수-1;if(nyşanyň_kody=='A')터미널항목->행위치=개수>터미널항목->행위치-터미널항목->맨위?터미널항목->맨위:터미널항목->행위치-개수;
    if(nyşanyň_kody=='B')터미널항목->행위치=터미널항목->행위치+개수>=터미널항목->맨위+터미널항목->행수?터미널항목->맨위+터미널항목->행수-1:터미널항목->행위치+개수;
    if(nyşanyň_kody=='H'||nyşanyň_kody=='f'){터미널항목->행위치=터미널항목->맨위+(개수>터미널항목->행수?터미널항목->행수:개수)-1;unsigned x_koordinatasy=터미널항목->매개값[1]?터미널항목->매개값[1]:1;터미널항목->열위치=(x_koordinatasy>터미널항목->열수?터미널항목->열수:x_koordinatasy)-1;}
    if(nyşanyň_kody=='s'){터미널항목->저장행=터미널항목->행위치;터미널항목->저장열=터미널항목->열위치;}if(nyşanyň_kody=='u'){터미널항목->행위치=터미널항목->저장행;터미널항목->열위치=터미널항목->저장열<터미널항목->열수?터미널항목->저장열:터미널항목->열수-1;}
    if((nyşanyň_kody=='h'||nyşanyň_kody=='l')&&터미널항목->매개값[0]==25)터미널항목->가리개보임=nyşanyň_kody=='h';
}
void 터미널바이트(unsigned 둘째값){
    터미널항목=&Windows_Sanaw[출력결과];if(!터미널항목->살아있음)return;derejä_göterme_baha(0);if(터미널항목->towla){터미널항목->towla=0;if(보이는지())Mazmun_baha();}
    if(터미널항목->탈출상태==1){터미널항목->탈출상태=둘째값=='['?2:0;터미널항목->매개색인=0;for(unsigned 순번=0;순번<4;순번++)터미널항목->매개값[순번]=0;}
    else if(터미널항목->탈출상태==2){if(둘째값=='?'){}else if(둘째값>='0'&&둘째값<='9'){if(터미널항목->매개값[터미널항목->매개색인]<10000)터미널항목->매개값[터미널항목->매개색인]=터미널항목->매개값[터미널항목->매개색인]*10+둘째값-'0';}else if(둘째값==';'&&터미널항목->매개색인<3)터미널항목->매개색인++;else{ryçag_dolandyryş_SEQUENCE(둘째값);터미널항목->탈출상태=0;}}
    else if(둘째값==27){터미널항목->긴부호없는값=0;터미널항목->탈출상태=1;}else{
        if(터미널항목->긴부호없는값&&(둘째값&0xc0)!=0x80){터미널항목->긴부호없는값=0;nyşanyň_kody_451f2815(0xfffd);}
        if(터미널항목->긴부호없는값){터미널항목->부호없는결과=터미널항목->부호없는결과*64+(둘째값&63);if(--터미널항목->긴부호없는값==0)nyşanyň_kody_451f2815(터미널항목->부호없는결과<터미널항목->작은값||터미널항목->부호없는결과>0x10ffff||(터미널항목->부호없는결과>=0xd800&&터미널항목->부호없는결과<=0xdfff)?0xfffd:터미널항목->부호없는결과);}
        else if(둘째값<128)nyşanyň_kody_451f2815(둘째값);else if(둘째값>=0xc2&&둘째값<=0xf4){터미널항목->긴부호없는값=둘째값<0xe0?1:둘째값<0xf0?2:3;터미널항목->부호없는결과=둘째값&((1u<<(6-터미널항목->긴부호없는값))-1);터미널항목->작은값=터미널항목->긴부호없는값==1?128:터미널항목->긴부호없는값==2?2048:65536;}else nyşanyň_kody_451f2815(0xfffd);
    }derejä_göterme_baha(1);
}
int 터미널대기(void){return 대기중!=0;}
/* 모서리 indeks: 1 좌상, 2 우상, 3 좌하, 4 우하. */
static int ölçegi_üýtget_süýşür=-1,잡은모서리,잡은가로,잡은세로,처음가로,처음세로,처음너비,처음높이;
static int 가리킨창(int 가로,int 세로) {
    for(int SEQUENCE_baha=항목수-1;SEQUENCE_baha>=0;SEQUENCE_baha--){
        int tanaýjy_baha=tertip_baha[SEQUENCE_baha];터미널상태 *penjire=&Windows_Sanaw[tanaýjy_baha];
        if(가로>=(int)penjire->x_koordinatasy&&세로>=(int)penjire->세로좌표&&
           가로<(int)(penjire->x_koordinatasy+penjire->너비)&&세로<(int)(penjire->세로좌표+penjire->높이))return tanaýjy_baha;
    }return -1;
}
static int 모서리찾기(int tanaýjy_baha,int 가로,int 세로) {
    if(tanaýjy_baha<0)return 0;터미널상태 *penjire=&Windows_Sanaw[tanaýjy_baha];
    int 왼쪽=가로<(int)penjire->x_koordinatasy+8,오른쪽=가로>=(int)(penjire->x_koordinatasy+penjire->너비)-8;
    int 위쪽=세로<(int)penjire->세로좌표+8,아래쪽=세로>=(int)(penjire->세로좌표+penjire->높이)-8;
    return (왼쪽||오른쪽)&&(위쪽||아래쪽)?1+오른쪽+아래쪽*2:0;
}
static int bölüji_baha(int baha,int 최소,int 최대){return baha<최소?최소:baha>최대?최대:baha;}
static void ýerini_üýtget_ölçegi_üýtget(int 가로,int 세로) {
    터미널상태 *penjire=&Windows_Sanaw[ölçegi_üýtget_süýşür];int 왼쪽=처음가로,위쪽=처음세로,오른쪽=처음가로+처음너비,아래쪽=처음세로+처음높이;
    if(잡은모서리==1||잡은모서리==3)왼쪽=bölüji_baha(처음가로+가로-잡은가로,0,오른쪽-360);
    else 오른쪽=bölüji_baha(처음가로+처음너비+가로-잡은가로,왼쪽+360,보드화면너비());
    if(잡은모서리<=2)위쪽=bölüji_baha(처음세로+세로-잡은세로,34,아래쪽-216);
    else 아래쪽=bölüji_baha(처음세로+처음높이+세로-잡은세로,위쪽+216,보드화면높이());
    unsigned 열수=(오른쪽-왼쪽-24)/8,행수=(아래쪽-위쪽-56)/16;
    if(penjire->열수!=열수||penjire->행수!=행수){
        penjire->크기바뀜=1;penjire->열수=열수;penjire->행수=행수;
        if(penjire->열위치>=열수)penjire->열위치=열수-1;
        if(penjire->행위치>=penjire->맨위+행수)penjire->맨위=penjire->행위치-행수+1;
        unsigned 한도=penjire->맨위;if(한도>기록줄수-행수)한도=기록줄수-행수;
        if(penjire->towla>한도)penjire->towla=한도;
    }
    int 옛가로=penjire->x_koordinatasy,옛세로=penjire->세로좌표,옛폭=penjire->너비,옛길이=penjire->높이;
    if(옛가로==왼쪽&&옛세로==위쪽&&옛폭==오른쪽-왼쪽&&옛길이==아래쪽-위쪽)return;
    penjire->x_koordinatasy=왼쪽;penjire->세로좌표=위쪽;penjire->너비=오른쪽-왼쪽;penjire->높이=아래쪽-위쪽;
    창자리그리기(옛가로,옛세로,옛폭,옛길이,penjire);
}
void 터미널가리킴(unsigned 다음,int x_koordinatasy,int 세로좌표){
    unsigned 눌림=다음&~단추들;단추들=다음;
    if(!iş_stoly_görkez){süýşür_baha=-1;ölçegi_üýtget_süýşür=-1;보드포인터(x_koordinatasy,세로좌표,1);return;}
    if(!(다음&1)){süýşür_baha=-1;ölçegi_üýtget_süýşür=-1;}
    if(ölçegi_üýtget_süýşür>=0&&!Windows_Sanaw[ölçegi_üýtget_süýşür].살아있음)ölçegi_üýtget_süýşür=-1;
    if(süýşür_baha>=0&&!Windows_Sanaw[süýşür_baha].살아있음)süýşür_baha=-1;
    if(ölçegi_üýtget_süýşür>=0){
        ýerini_üýtget_ölçegi_üýtget(x_koordinatasy,세로좌표);보드포인터(x_koordinatasy,세로좌표,잡은모서리==1||잡은모서리==4?2:3);return;
    }
    보드포인터(x_koordinatasy,세로좌표,1);
    if(süýşür_baha>=0){
        터미널상태 *penjire=&Windows_Sanaw[süýşür_baha];
        int 옛가로=penjire->x_koordinatasy,옛세로=penjire->세로좌표;
        penjire->x_koordinatasy=bölüji_baha(x_koordinatasy-끌기가로,0,보드화면너비()-penjire->너비);
        penjire->세로좌표=bölüji_baha(세로좌표-끌기세로,34,보드화면높이()-penjire->높이);
        if(옛가로!=(int)penjire->x_koordinatasy||옛세로!=(int)penjire->세로좌표)창자리그리기(옛가로,옛세로,penjire->너비,penjire->높이,penjire);
        return;
    }
    extern int 화면덮음(int,int,int);
    if(화면덮음(Fokus,x_koordinatasy,세로좌표)){화면가리킴(Fokus,눌림,x_koordinatasy,세로좌표);return;}
    int tanaýjy_baha=가리킨창(x_koordinatasy,세로좌표),모서리=모서리찾기(tanaýjy_baha,x_koordinatasy,세로좌표);
    if(모서리)보드포인터(x_koordinatasy,세로좌표,모서리==1||모서리==4?2:3);
    if(눌림&1){
        if(모서리){
            터미널상태 *penjire=&Windows_Sanaw[tanaýjy_baha];ölçegi_üýtget_süýşür=tanaýjy_baha;잡은모서리=모서리;잡은가로=x_koordinatasy;잡은세로=세로좌표;
            처음가로=penjire->x_koordinatasy;처음세로=penjire->세로좌표;처음너비=penjire->너비;처음높이=penjire->높이;
            if(tanaýjy_baha!=Fokus)앞으로올리기(tanaýjy_baha);return;
        }
        if(세로좌표<32&&x_koordinatasy>=6&&x_koordinatasy<142){döretmek_girizmeklik();return;}
        if(세로좌표<32&&x_koordinatasy>=154&&x_koordinatasy<602){앞으로올리기((x_koordinatasy-154)/112);return;}
        if(tanaýjy_baha>=0){
            터미널상태 *penjire=&Windows_Sanaw[tanaýjy_baha];
            if(세로좌표<(int)penjire->세로좌표+30&&x_koordinatasy>=(int)(penjire->x_koordinatasy+penjire->너비)-32){ýap_penjire(tanaýjy_baha);return;}
            if(tanaýjy_baha!=Fokus)앞으로올리기(tanaýjy_baha);
            if(세로좌표<(int)penjire->세로좌표+30){süýşür_baha=tanaýjy_baha;끌기가로=x_koordinatasy-penjire->x_koordinatasy;끌기세로=세로좌표-penjire->세로좌표;}return;
        }
    }
    if(Fokus>=0&&(눌림&(8|16))){터미널항목=&Windows_Sanaw[Fokus];if(눌림&8){unsigned 한도=터미널항목->맨위;if(한도>기록줄수-터미널항목->행수)한도=기록줄수-터미널항목->행수;터미널항목->towla=터미널항목->towla+9>한도?한도:터미널항목->towla+9;}else 터미널항목->towla=터미널항목->towla<9?0:터미널항목->towla-9;다시그리기();}
}
void 터미널바로가기키(unsigned 누름값){if(누름값==1)döretmek_girizmeklik();if(누름값==2&&항목수)앞으로올리기(tertip_baha[0]);if(누름값==3)ýap_penjire(Fokus);}
kompýuter_Söz 보드터미널(kompýuter_Söz iş){
    if(iş==300){if(!Windows_Sanaw[출력결과].살아있음)return döretmek_girizmeklik();iş_stoly_görkez=1;다시그리기();return 0;}
    if(iş==0){ýap_penjire(Fokus);return 0;}if(iş==1)return (uint32_t)döretmek_girizmeklik();if(iş==2)return Fokus>=0;
    if(iş==9){iş_stoly_görkez=0;return 0;}if(iş==7)return 항목수;if(iş==10)return Fokus+1;if(iş==11)return 출력결과;
    if(iş==13){터미널상태 *penjire=&Windows_Sanaw[출력결과];return penjire->살아있음?(penjire->행수<<16)|penjire->열수:(19<<16)|68;}
    if(iş==14){unsigned baha=Windows_Sanaw[출력결과].크기바뀜;Windows_Sanaw[출력결과].크기바뀜=0;return baha;}
    if(iş==12){unsigned baha=대기중;대기중=0;return baha;}
    if(iş>=20&&iş<24)return Windows_Sanaw[iş-20].살아있음;
    if(iş>=100&&iş<104){출력결과=iş-100;터미널항목=&Windows_Sanaw[출력결과];return 0;}
    if(iş>=200&&iş<204){앞으로올리기(iş-200);return 0;}
    if(iş==3){다시그리기();return 0;}터미널항목=&Windows_Sanaw[출력결과];if(!터미널항목->살아있음)return 0;
    if(iş==4)arassala_TOC();if(iş==5||iş==6){unsigned 이전=단추들;터미널가리킴(iş==5?8:16,0,0);단추들=이전;}return 1;
}
