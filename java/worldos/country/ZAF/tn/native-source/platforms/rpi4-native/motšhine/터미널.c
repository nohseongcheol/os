#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* 자체 네 fensetere 합성과 UTF-8 터미널. 바뀐 영역의 완성 그림만 표시한다. */
#include <stdint.h>
#include <stddef.h>
typedef uintptr_t motšhine_Lefoko;
extern motšhine_Lefoko 보드화소(motšhine_Lefoko,motšhine_Lefoko,motšhine_Lefoko),보드화면기억공간(void);
extern void *memset(void *,int,size_t);
extern const unsigned char 터미널글꼴자료[];
#define 최대열수 237
#define 기록줄수 160
typedef struct {
    uint32_t 글자칸들[기록줄수][최대열수]; uint8_t 모양들[기록줄수][최대열수];
    unsigned 너비,높이,열수,행수,크기바뀜;
    unsigned 살아있음,kgokagano_ya_x,세로좌표,행위치,열위치,맨위,sekorola,전경색,배경색,탈출상태,매개값[4],매개색인,저장행,저장열;
    unsigned 부호없는결과,긴부호없는값,작은값,대체화면,가리개보임;
} 터미널상태;
static 터미널상태 창들[4];
static int Tsepamo=-1,출력결과,thulaganyo_Boleng[4],항목수,Goga_Boleng=-1,끌기가로,끌기세로;
static unsigned 대기중,단추들,desekethopo_Tebego,한글입력;
static const uint32_t 색상들[16]={0x201a15,0x6060df,0x9dcc86,0x80cfea,0xefaf72,0xca96c9,0xceda76,0xede9df,0x858078,0x8888ff,0xb9eba7,0xa5eaff,0xffcc99,0xf0bef1,0xf0f0a0,0xffffff};
extern int 화면보임(int),화면가리킴(int,unsigned,int,int);
extern void 화면다시그림(int);
static 터미널상태 *터미널항목;
static unsigned 넓은글자(unsigned khoutuletshwao){return khoutuletshwao>=256?2:1;}
static void 사각영역(unsigned kgokagano_ya_x,unsigned 세로좌표,unsigned 너비값,unsigned 높이값,unsigned 색상){
    보드사각그림(kgokagano_ya_x,세로좌표,너비값,높이값,색상);
}
void 터미널글자그림(unsigned kgokagano_ya_x,unsigned 세로좌표,unsigned khoutuletshwao,unsigned 전경색,unsigned 배경색){
    unsigned 너비=넓은글자(khoutuletshwao)*8;if(khoutuletshwao==0xffffffffu)return;
    int 왼쪽=kgokagano_ya_x,위쪽=세로좌표,폭=너비,boleele_Boleng=16;
    if(!보드그림범위(&왼쪽,&위쪽,&폭,&boleele_Boleng))return;
    if(khoutuletshwao==' '){보드사각그림(왼쪽,위쪽,폭,boleele_Boleng,배경색);return;}
    unsigned 색인=khoutuletshwao<65536?khoutuletshwao:khoutuletshwao>=0x1f600&&khoutuletshwao<0x1f650?65536+khoutuletshwao-0x1f600:0xfffd;
    const unsigned char *mofutatlhaka_Boleng=터미널글꼴자료+색인*32;
    for(int Mola=위쪽;Mola<위쪽+boleele_Boleng;Mola++){unsigned 비트들=mofutatlhaka_Boleng[(Mola-세로좌표)*2]*256+mofutatlhaka_Boleng[(Mola-세로좌표)*2+1];for(int sebaka_tsenyo=왼쪽;sebaka_tsenyo<왼쪽+폭;sebaka_tsenyo++)보드화소(sebaka_tsenyo,Mola,(비트들&(0x8000>>(sebaka_tsenyo-kgokagano_ya_x)))?전경색:배경색);}
}
static void leina_lenaneothalo(unsigned kgokagano_ya_x,unsigned 세로좌표,const char *dikwalwa_tshedimosetso,unsigned 전경색,unsigned 배경색){while(*dikwalwa_tshedimosetso){unsigned khoutuletshwao=(unsigned char)*dikwalwa_tshedimosetso++, 남은수=0;if(khoutuletshwao>=0xc0){남은수=khoutuletshwao<0xe0?1:khoutuletshwao<0xf0?2:3;khoutuletshwao&=(1u<<(6-남은수))-1;while(남은수--&&*dikwalwa_tshedimosetso)khoutuletshwao=(khoutuletshwao<<6)|((unsigned char)*dikwalwa_tshedimosetso++&63);}터미널글자그림(kgokagano_ya_x,세로좌표,khoutuletshwao,전경색,배경색);kgokagano_ya_x+=넓은글자(khoutuletshwao)*8;}}
static unsigned 첫항목(void){return 터미널항목->맨위;}
static int 보이는지(void){return 터미널항목->살아있음&&Tsepamo>=0&&터미널항목==&창들[Tsepamo]&&!화면보임(Tsepamo);}
static void 그리기(unsigned 행위치,unsigned 열위치){
    if(!보이는지()||행위치<첫항목()-터미널항목->sekorola||행위치>=첫항목()-터미널항목->sekorola+터미널항목->행수||열위치>=터미널항목->열수)return;
    unsigned khoutuletshwao=터미널항목->글자칸들[행위치%기록줄수][열위치],dikwalwa_tshedimosetso=터미널항목->모양들[행위치%기록줄수][열위치];
    if(넓은글자(khoutuletshwao)==2&&열위치+1>=터미널항목->열수)khoutuletshwao=' ';
    터미널글자그림(터미널항목->kgokagano_ya_x+12+열위치*8,터미널항목->세로좌표+36+(행위치-첫항목()+터미널항목->sekorola)*16,khoutuletshwao?khoutuletshwao:' ',색상들[dikwalwa_tshedimosetso&15],색상들[dikwalwa_tshedimosetso>>4]);
}
static void kharete_Boleng(int bontsha_fensetere){if(!보이는지()||터미널항목->sekorola||터미널항목->열위치>=터미널항목->열수||터미널항목->행위치<터미널항목->맨위||터미널항목->행위치>=터미널항목->맨위+터미널항목->행수)return;
    if(!bontsha_fensetere||!터미널항목->가리개보임)그리기(터미널항목->행위치,터미널항목->열위치);else 사각영역(터미널항목->kgokagano_ya_x+12+터미널항목->열위치*8,터미널항목->세로좌표+36+(터미널항목->행위치-터미널항목->맨위)*16+14,8,2,색상들[터미널항목->전경색]);}
static void Diteng_Boleng(void){
    사각영역(터미널항목->kgokagano_ya_x+12,터미널항목->세로좌표+36,터미널항목->열수*8,터미널항목->행수*16,색상들[0]);
    int 가로=터미널항목->kgokagano_ya_x+12,세로=터미널항목->세로좌표+36,폭=터미널항목->열수*8,boleele_Boleng=터미널항목->행수*16;
    if(보드그림범위(&가로,&세로,&폭,&boleele_Boleng)){
    unsigned 첫줄=(세로-터미널항목->세로좌표-36)/16,끝줄=(세로+boleele_Boleng-터미널항목->세로좌표-36+15)/16;
    unsigned 첫칸=(가로-터미널항목->kgokagano_ya_x-12)/8,끝칸=(가로+폭-터미널항목->kgokagano_ya_x-12+7)/8;
    if(첫칸)첫칸--; /* 잘림 경계 왼쪽에서 시작한 두 sebaka_tsenyo 글자도 그린다. */
    for(unsigned 반환값=첫줄;반환값<끝줄;반환값++)for(unsigned khoutuletshwao=첫칸;khoutuletshwao<끝칸;khoutuletshwao++){
        unsigned 행위치=첫항목()-터미널항목->sekorola+반환값,Letshwao_Boleng=터미널항목->글자칸들[행위치%기록줄수][khoutuletshwao],dikwalwa_tshedimosetso=터미널항목->모양들[행위치%기록줄수][khoutuletshwao];
        if(넓은글자(Letshwao_Boleng)==2&&khoutuletshwao+1>=터미널항목->열수)Letshwao_Boleng=' ';
        if((Letshwao_Boleng==0||Letshwao_Boleng==' ')&&(dikwalwa_tshedimosetso>>4)==0)continue;
        터미널글자그림(터미널항목->kgokagano_ya_x+12+khoutuletshwao*8,터미널항목->세로좌표+36+반환값*16,Letshwao_Boleng?Letshwao_Boleng:' ',색상들[dikwalwa_tshedimosetso&15],색상들[dikwalwa_tshedimosetso>>4]);
    }}
    leina_lenaneothalo(터미널항목->kgokagano_ya_x+12,터미널항목->세로좌표+터미널항목->높이-18,터미널항목->sekorola?"PgDn: recent output":터미널항목->너비>=500?"F6: next | Corner + left drag: resize":"Corner + left drag: resize",0xece8e2,0x403127);kharete_Boleng(1);
}
static void 실행틀(int setlhaodi_Boleng){
    터미널항목=&창들[setlhaodi_Boleng];
    int 가로=터미널항목->kgokagano_ya_x,세로=터미널항목->세로좌표,폭=터미널항목->너비,boleele_Boleng=터미널항목->높이;
    if(!보드그림범위(&가로,&세로,&폭,&boleele_Boleng))return;
    사각영역(터미널항목->kgokagano_ya_x,터미널항목->세로좌표,터미널항목->너비,터미널항목->높이,0x403127);
    unsigned 색상=setlhaodi_Boleng==Tsepamo?0x905020:0x604438;사각영역(터미널항목->kgokagano_ya_x,터미널항목->세로좌표,터미널항목->너비,30,색상);
    leina_lenaneothalo(터미널항목->kgokagano_ya_x+12,터미널항목->세로좌표+7,"JKOROS Terminal",0xffffff,색상);
    char 수치[2]={(char)('1'+setlhaodi_Boleng),0};leina_lenaneothalo(터미널항목->kgokagano_ya_x+148,터미널항목->세로좌표+7,수치,0xffffff,색상);
    leina_lenaneothalo(터미널항목->kgokagano_ya_x+240,터미널항목->세로좌표+7,터미널항목->너비>=500?(한글입력?"[TN] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[TN]":"[EN]"),0xffffff,색상);
    사각영역(터미널항목->kgokagano_ya_x+터미널항목->너비-32,터미널항목->세로좌표+4,26,22,0x5555b8);leina_lenaneothalo(터미널항목->kgokagano_ya_x+터미널항목->너비-24,터미널항목->세로좌표+7,"X",0xffffff,0x5555b8);
    Diteng_Boleng();
}
static void 장면그리기(void){
    if(!desekethopo_Tebego)return;사각영역(0,0,보드화면너비(),보드화면높이(),0x302018);사각영역(0,0,보드화면너비(),32,0x403127);
    사각영역(6,4,136,24,0x905020);leina_lenaneothalo(14,8,"+ New terminal",0xffffff,0x905020);
    for(int 순번=0;순번<4;순번++)if(창들[순번].살아있음){unsigned khoutuletshwao=Tsepamo==순번?0x905020:0x604438;사각영역(154+순번*112,4,106,24,khoutuletshwao);leina_lenaneothalo(160+순번*112,8,"Terminal",0xffffff,khoutuletshwao);char dikwalwa_tshedimosetso[2]={(char)('1'+순번),0};leina_lenaneothalo(232+순번*112,8,dikwalwa_tshedimosetso,0xffffff,khoutuletshwao);}
    if(!항목수)leina_lenaneothalo(140,210,"Click + New terminal to start",0xede9df,0x302018);
    for(int 순번=0;순번<항목수;순번++)실행틀(thulaganyo_Boleng[순번]);화면다시그림(Tsepamo);터미널항목=&창들[출력결과];
}
static void 영역그리기(int 가로,int 세로,int 폭,int boleele_Boleng){
    if(!desekethopo_Tebego||!보드그림범위(&가로,&세로,&폭,&boleele_Boleng))return;
    for(int Mola=세로;Mola<세로+boleele_Boleng;Mola+=32){
        int 띠높이=세로+boleele_Boleng-Mola;if(띠높이>32)띠높이=32;
        if(보드그림시작(가로,Mola,폭,띠높이)){장면그리기();보드그림마침();}
    }
}
static void 다시그리기(void){영역그리기(0,0,보드화면너비(),보드화면높이());}
/* 서로 겹치지 않는 새 fensetere 영역과 이전 자리의 네 띠를 복구한다. */
static void 창자리그리기(int 가로,int 세로,int 폭,int boleele_Boleng,터미널상태 *fensetere){
    int 왼쪽=가로>(int)fensetere->kgokagano_ya_x?가로:(int)fensetere->kgokagano_ya_x;
    int 위쪽=세로>(int)fensetere->세로좌표?세로:(int)fensetere->세로좌표;
    int 오른쪽=가로+폭<(int)(fensetere->kgokagano_ya_x+fensetere->너비)?가로+폭:(int)(fensetere->kgokagano_ya_x+fensetere->너비);
    int 아래쪽=세로+boleele_Boleng<(int)(fensetere->세로좌표+fensetere->높이)?세로+boleele_Boleng:(int)(fensetere->세로좌표+fensetere->높이);
    영역그리기(fensetere->kgokagano_ya_x,fensetere->세로좌표,fensetere->너비,fensetere->높이);
    if(왼쪽>=오른쪽||위쪽>=아래쪽){영역그리기(가로,세로,폭,boleele_Boleng);return;}
    영역그리기(가로,세로,폭,위쪽-세로);
    영역그리기(가로,아래쪽,폭,세로+boleele_Boleng-아래쪽);
    영역그리기(가로,위쪽,왼쪽-가로,아래쪽-위쪽);
    영역그리기(오른쪽,위쪽,가로+폭-오른쪽,아래쪽-위쪽);
}
static void 초점알리기(void){대기중=(대기중&~15u)|(unsigned)(Tsepamo+1)|0x10000;}
void 터미널입력방식(unsigned 한글여부){
    한글입력=한글여부!=0;
    /* Update title bars only: a mode switch must not erase an EL0 drawing. */
    if(Tsepamo>=0){
        터미널상태 *fensetere_tsenyo=&창들[Tsepamo];
        leina_lenaneothalo(fensetere_tsenyo->kgokagano_ya_x+240,fensetere_tsenyo->세로좌표+7,fensetere_tsenyo->너비>=500?(한글입력?"[TN] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[TN]":"[EN]"),0xffffff,0x905020);
    }
}
static void 앞으로올리기(int setlhaodi_Boleng){if(setlhaodi_Boleng<0||setlhaodi_Boleng>=4||!창들[setlhaodi_Boleng].살아있음)return;int 현재위치=0;while(현재위치<항목수&&thulaganyo_Boleng[현재위치]!=setlhaodi_Boleng)현재위치++;for(;현재위치+1<항목수;현재위치++)thulaganyo_Boleng[현재위치]=thulaganyo_Boleng[현재위치+1];thulaganyo_Boleng[항목수-1]=setlhaodi_Boleng;Tsepamo=setlhaodi_Boleng;초점알리기();다시그리기();}
static void 빈칸채우기(unsigned 행위치){for(unsigned khoutuletshwao=0;khoutuletshwao<최대열수;khoutuletshwao++){터미널항목->글자칸들[행위치%기록줄수][khoutuletshwao]=0;터미널항목->모양들[행위치%기록줄수][khoutuletshwao]=터미널항목->전경색|(터미널항목->배경색<<4);}}
static void phimola_TOC(void){터미널항목->행위치=터미널항목->열위치=터미널항목->맨위=터미널항목->sekorola=0;for(unsigned 반환값=0;반환값<기록줄수;반환값++)빈칸채우기(반환값);if(보이는지())Diteng_Boleng();}
static int tlhama_tsenyo(void){
    if(!보드화면기억공간())return -19;int setlhaodi_Boleng=0;while(setlhaodi_Boleng<4&&창들[setlhaodi_Boleng].살아있음)setlhaodi_Boleng++;if(setlhaodi_Boleng==4)return -28;
    desekethopo_Tebego=1;터미널항목=&창들[setlhaodi_Boleng];memset(터미널항목,0,sizeof(*터미널항목));터미널항목->살아있음=1;터미널항목->너비=568;터미널항목->높이=360;터미널항목->열수=68;터미널항목->행수=19;터미널항목->kgokagano_ya_x=12+setlhaodi_Boleng*16;터미널항목->세로좌표=48+setlhaodi_Boleng*18;터미널항목->전경색=7;터미널항목->가리개보임=1;
    for(unsigned 반환값=0;반환값<기록줄수;반환값++)빈칸채우기(반환값);thulaganyo_Boleng[항목수++]=setlhaodi_Boleng;Tsepamo=setlhaodi_Boleng;대기중|=1u<<(4+setlhaodi_Boleng);초점알리기();다시그리기();return setlhaodi_Boleng+1;
}
static void tswala_fensetere(int setlhaodi_Boleng){
    if(setlhaodi_Boleng<0||setlhaodi_Boleng>=4||!창들[setlhaodi_Boleng].살아있음)return;창들[setlhaodi_Boleng].살아있음=0;대기중|=1u<<(8+setlhaodi_Boleng);
    int 현재위치=0;while(현재위치<항목수&&thulaganyo_Boleng[현재위치]!=setlhaodi_Boleng)현재위치++;for(;현재위치+1<항목수;현재위치++)thulaganyo_Boleng[현재위치]=thulaganyo_Boleng[현재위치+1];항목수--;
    if(Tsepamo==setlhaodi_Boleng)Tsepamo=항목수?thulaganyo_Boleng[항목수-1]:-1;초점알리기();다시그리기();
}
static void 줄바꿈(void){터미널항목->열위치=0;터미널항목->행위치++;if(터미널항목->행위치>=터미널항목->맨위+터미널항목->행수){터미널항목->맨위++;빈칸채우기(터미널항목->행위치);if(보이는지())Diteng_Boleng();}}
static void khoutuletshwao_451f2815(unsigned khoutuletshwao){
    if(khoutuletshwao==13){터미널항목->열위치=0;return;}if(khoutuletshwao==10){줄바꿈();return;}if(khoutuletshwao==8){if(터미널항목->열위치)터미널항목->열위치--;return;}
    if(khoutuletshwao==9){unsigned 개수=8-터미널항목->열위치%8;while(개수--)khoutuletshwao_451f2815(' ');return;}if(khoutuletshwao<32||khoutuletshwao==127)return;
    unsigned 너비값=넓은글자(khoutuletshwao);if(터미널항목->열위치+너비값>터미널항목->열수)줄바꿈();
    if(터미널항목->글자칸들[터미널항목->행위치%기록줄수][터미널항목->열위치]==0xffffffffu&&터미널항목->열위치){터미널항목->글자칸들[터미널항목->행위치%기록줄수][터미널항목->열위치-1]=' ';그리기(터미널항목->행위치,터미널항목->열위치-1);}
    if(넓은글자(터미널항목->글자칸들[터미널항목->행위치%기록줄수][터미널항목->열위치])==2&&터미널항목->열위치+1<터미널항목->열수){터미널항목->글자칸들[터미널항목->행위치%기록줄수][터미널항목->열위치+1]=' ';그리기(터미널항목->행위치,터미널항목->열위치+1);}
    터미널항목->글자칸들[터미널항목->행위치%기록줄수][터미널항목->열위치]=khoutuletshwao;터미널항목->모양들[터미널항목->행위치%기록줄수][터미널항목->열위치]=터미널항목->전경색|(터미널항목->배경색<<4);
    if(너비값==2)터미널항목->글자칸들[터미널항목->행위치%기록줄수][터미널항목->열위치+1]=0xffffffffu;
    그리기(터미널항목->행위치,터미널항목->열위치);터미널항목->열위치+=너비값;
}
static void mokgwakamogelo_taolo_TATELANO(unsigned khoutuletshwao){
    unsigned 개수=터미널항목->매개값[0]?터미널항목->매개값[0]:1;
    if(khoutuletshwao=='m')for(unsigned 순번=0;순번<=터미널항목->매개색인;순번++){unsigned 자료위치=터미널항목->매개값[순번];if(!자료위치){터미널항목->전경색=7;터미널항목->배경색=0;}if(자료위치==1&&터미널항목->전경색<8)터미널항목->전경색+=8;if(자료위치==7){unsigned 유지=터미널항목->전경색;터미널항목->전경색=터미널항목->배경색;터미널항목->배경색=유지;}if(자료위치>=30&&자료위치<=37)터미널항목->전경색=자료위치-30;if(자료위치>=90&&자료위치<=97)터미널항목->전경색=자료위치-90+8;if(자료위치>=40&&자료위치<=47)터미널항목->배경색=자료위치-40;if(자료위치>=100&&자료위치<=107)터미널항목->배경색=자료위치-100+8;if(자료위치==39)터미널항목->전경색=7;if(자료위치==49)터미널항목->배경색=0;}
    if(khoutuletshwao=='J'&&(터미널항목->매개값[0]==2||터미널항목->매개값[0]==3))phimola_TOC();
    if(khoutuletshwao=='K'){unsigned 출발위치=터미널항목->매개값[0]==2?0:터미널항목->열위치,도착위치=터미널항목->매개값[0]==1?터미널항목->열위치+1:터미널항목->열수;if(터미널항목->매개값[0]==1)출발위치=0;for(unsigned 순번=출발위치;순번<도착위치&&순번<터미널항목->열수;순번++){
        unsigned mola_Boleng=터미널항목->행위치%기록줄수,Letshwao_Boleng=터미널항목->글자칸들[mola_Boleng][순번],popego_Boleng=터미널항목->전경색|(터미널항목->배경색<<4);
        /* 넓은 vi 화면에서도 이미 빈 칸의 mofutatlhaka_Boleng 화소를 되풀이해 칠하지 않는다. */
        int 바뀜=(Letshwao_Boleng!=0&&Letshwao_Boleng!=' ')||터미널항목->모양들[mola_Boleng][순번]!=popego_Boleng;
        터미널항목->글자칸들[mola_Boleng][순번]=' ';터미널항목->모양들[mola_Boleng][순번]=popego_Boleng;
        if(바뀜)그리기(터미널항목->행위치,순번);
    }}
    if(khoutuletshwao=='D')터미널항목->열위치=개수>터미널항목->열위치?0:터미널항목->열위치-개수;if(khoutuletshwao=='C')터미널항목->열위치=터미널항목->열위치+개수>=터미널항목->열수?터미널항목->열수-1:터미널항목->열위치+개수;
    if(khoutuletshwao=='G')터미널항목->열위치=개수>터미널항목->열수?터미널항목->열수-1:개수-1;if(khoutuletshwao=='A')터미널항목->행위치=개수>터미널항목->행위치-터미널항목->맨위?터미널항목->맨위:터미널항목->행위치-개수;
    if(khoutuletshwao=='B')터미널항목->행위치=터미널항목->행위치+개수>=터미널항목->맨위+터미널항목->행수?터미널항목->맨위+터미널항목->행수-1:터미널항목->행위치+개수;
    if(khoutuletshwao=='H'||khoutuletshwao=='f'){터미널항목->행위치=터미널항목->맨위+(개수>터미널항목->행수?터미널항목->행수:개수)-1;unsigned kgokagano_ya_x=터미널항목->매개값[1]?터미널항목->매개값[1]:1;터미널항목->열위치=(kgokagano_ya_x>터미널항목->열수?터미널항목->열수:kgokagano_ya_x)-1;}
    if(khoutuletshwao=='s'){터미널항목->저장행=터미널항목->행위치;터미널항목->저장열=터미널항목->열위치;}if(khoutuletshwao=='u'){터미널항목->행위치=터미널항목->저장행;터미널항목->열위치=터미널항목->저장열<터미널항목->열수?터미널항목->저장열:터미널항목->열수-1;}
    if((khoutuletshwao=='h'||khoutuletshwao=='l')&&터미널항목->매개값[0]==25)터미널항목->가리개보임=khoutuletshwao=='h';
}
void 터미널바이트(unsigned 둘째값){
    터미널항목=&창들[출력결과];if(!터미널항목->살아있음)return;kharete_Boleng(0);if(터미널항목->sekorola){터미널항목->sekorola=0;if(보이는지())Diteng_Boleng();}
    if(터미널항목->탈출상태==1){터미널항목->탈출상태=둘째값=='['?2:0;터미널항목->매개색인=0;for(unsigned 순번=0;순번<4;순번++)터미널항목->매개값[순번]=0;}
    else if(터미널항목->탈출상태==2){if(둘째값=='?'){}else if(둘째값>='0'&&둘째값<='9'){if(터미널항목->매개값[터미널항목->매개색인]<10000)터미널항목->매개값[터미널항목->매개색인]=터미널항목->매개값[터미널항목->매개색인]*10+둘째값-'0';}else if(둘째값==';'&&터미널항목->매개색인<3)터미널항목->매개색인++;else{mokgwakamogelo_taolo_TATELANO(둘째값);터미널항목->탈출상태=0;}}
    else if(둘째값==27){터미널항목->긴부호없는값=0;터미널항목->탈출상태=1;}else{
        if(터미널항목->긴부호없는값&&(둘째값&0xc0)!=0x80){터미널항목->긴부호없는값=0;khoutuletshwao_451f2815(0xfffd);}
        if(터미널항목->긴부호없는값){터미널항목->부호없는결과=터미널항목->부호없는결과*64+(둘째값&63);if(--터미널항목->긴부호없는값==0)khoutuletshwao_451f2815(터미널항목->부호없는결과<터미널항목->작은값||터미널항목->부호없는결과>0x10ffff||(터미널항목->부호없는결과>=0xd800&&터미널항목->부호없는결과<=0xdfff)?0xfffd:터미널항목->부호없는결과);}
        else if(둘째값<128)khoutuletshwao_451f2815(둘째값);else if(둘째값>=0xc2&&둘째값<=0xf4){터미널항목->긴부호없는값=둘째값<0xe0?1:둘째값<0xf0?2:3;터미널항목->부호없는결과=둘째값&((1u<<(6-터미널항목->긴부호없는값))-1);터미널항목->작은값=터미널항목->긴부호없는값==1?128:터미널항목->긴부호없는값==2?2048:65536;}else khoutuletshwao_451f2815(0xfffd);
    }kharete_Boleng(1);
}
int 터미널대기(void){return 대기중!=0;}
/* 모서리 tshupane: 1 좌상, 2 우상, 3 좌하, 4 우하. */
static int lekanyasešwa_Goga=-1,잡은모서리,잡은가로,잡은세로,처음가로,처음세로,처음너비,처음높이;
static int 가리킨창(int 가로,int 세로) {
    for(int TATELANO_Boleng=항목수-1;TATELANO_Boleng>=0;TATELANO_Boleng--){
        int setlhaodi_Boleng=thulaganyo_Boleng[TATELANO_Boleng];터미널상태 *fensetere=&창들[setlhaodi_Boleng];
        if(가로>=(int)fensetere->kgokagano_ya_x&&세로>=(int)fensetere->세로좌표&&
           가로<(int)(fensetere->kgokagano_ya_x+fensetere->너비)&&세로<(int)(fensetere->세로좌표+fensetere->높이))return setlhaodi_Boleng;
    }return -1;
}
static int 모서리찾기(int setlhaodi_Boleng,int 가로,int 세로) {
    if(setlhaodi_Boleng<0)return 0;터미널상태 *fensetere=&창들[setlhaodi_Boleng];
    int 왼쪽=가로<(int)fensetere->kgokagano_ya_x+8,오른쪽=가로>=(int)(fensetere->kgokagano_ya_x+fensetere->너비)-8;
    int 위쪽=세로<(int)fensetere->세로좌표+8,아래쪽=세로>=(int)(fensetere->세로좌표+fensetere->높이)-8;
    return (왼쪽||오른쪽)&&(위쪽||아래쪽)?1+오른쪽+아래쪽*2:0;
}
static int searoganyi_Boleng(int Boleng,int 최소,int 최대){return Boleng<최소?최소:Boleng>최대?최대:Boleng;}
static void sutisa_lekanyasešwa(int 가로,int 세로) {
    터미널상태 *fensetere=&창들[lekanyasešwa_Goga];int 왼쪽=처음가로,위쪽=처음세로,오른쪽=처음가로+처음너비,아래쪽=처음세로+처음높이;
    if(잡은모서리==1||잡은모서리==3)왼쪽=searoganyi_Boleng(처음가로+가로-잡은가로,0,오른쪽-360);
    else 오른쪽=searoganyi_Boleng(처음가로+처음너비+가로-잡은가로,왼쪽+360,보드화면너비());
    if(잡은모서리<=2)위쪽=searoganyi_Boleng(처음세로+세로-잡은세로,34,아래쪽-216);
    else 아래쪽=searoganyi_Boleng(처음세로+처음높이+세로-잡은세로,위쪽+216,보드화면높이());
    unsigned 열수=(오른쪽-왼쪽-24)/8,행수=(아래쪽-위쪽-56)/16;
    if(fensetere->열수!=열수||fensetere->행수!=행수){
        fensetere->크기바뀜=1;fensetere->열수=열수;fensetere->행수=행수;
        if(fensetere->열위치>=열수)fensetere->열위치=열수-1;
        if(fensetere->행위치>=fensetere->맨위+행수)fensetere->맨위=fensetere->행위치-행수+1;
        unsigned 한도=fensetere->맨위;if(한도>기록줄수-행수)한도=기록줄수-행수;
        if(fensetere->sekorola>한도)fensetere->sekorola=한도;
    }
    int 옛가로=fensetere->kgokagano_ya_x,옛세로=fensetere->세로좌표,옛폭=fensetere->너비,옛길이=fensetere->높이;
    if(옛가로==왼쪽&&옛세로==위쪽&&옛폭==오른쪽-왼쪽&&옛길이==아래쪽-위쪽)return;
    fensetere->kgokagano_ya_x=왼쪽;fensetere->세로좌표=위쪽;fensetere->너비=오른쪽-왼쪽;fensetere->높이=아래쪽-위쪽;
    창자리그리기(옛가로,옛세로,옛폭,옛길이,fensetere);
}
void 터미널가리킴(unsigned 다음,int kgokagano_ya_x,int 세로좌표){
    unsigned 눌림=다음&~단추들;단추들=다음;
    if(!desekethopo_Tebego){Goga_Boleng=-1;lekanyasešwa_Goga=-1;보드포인터(kgokagano_ya_x,세로좌표,1);return;}
    if(!(다음&1)){Goga_Boleng=-1;lekanyasešwa_Goga=-1;}
    if(lekanyasešwa_Goga>=0&&!창들[lekanyasešwa_Goga].살아있음)lekanyasešwa_Goga=-1;
    if(Goga_Boleng>=0&&!창들[Goga_Boleng].살아있음)Goga_Boleng=-1;
    if(lekanyasešwa_Goga>=0){
        sutisa_lekanyasešwa(kgokagano_ya_x,세로좌표);보드포인터(kgokagano_ya_x,세로좌표,잡은모서리==1||잡은모서리==4?2:3);return;
    }
    보드포인터(kgokagano_ya_x,세로좌표,1);
    if(Goga_Boleng>=0){
        터미널상태 *fensetere=&창들[Goga_Boleng];
        int 옛가로=fensetere->kgokagano_ya_x,옛세로=fensetere->세로좌표;
        fensetere->kgokagano_ya_x=searoganyi_Boleng(kgokagano_ya_x-끌기가로,0,보드화면너비()-fensetere->너비);
        fensetere->세로좌표=searoganyi_Boleng(세로좌표-끌기세로,34,보드화면높이()-fensetere->높이);
        if(옛가로!=(int)fensetere->kgokagano_ya_x||옛세로!=(int)fensetere->세로좌표)창자리그리기(옛가로,옛세로,fensetere->너비,fensetere->높이,fensetere);
        return;
    }
    extern int 화면덮음(int,int,int);
    if(화면덮음(Tsepamo,kgokagano_ya_x,세로좌표)){화면가리킴(Tsepamo,눌림,kgokagano_ya_x,세로좌표);return;}
    int setlhaodi_Boleng=가리킨창(kgokagano_ya_x,세로좌표),모서리=모서리찾기(setlhaodi_Boleng,kgokagano_ya_x,세로좌표);
    if(모서리)보드포인터(kgokagano_ya_x,세로좌표,모서리==1||모서리==4?2:3);
    if(눌림&1){
        if(모서리){
            터미널상태 *fensetere=&창들[setlhaodi_Boleng];lekanyasešwa_Goga=setlhaodi_Boleng;잡은모서리=모서리;잡은가로=kgokagano_ya_x;잡은세로=세로좌표;
            처음가로=fensetere->kgokagano_ya_x;처음세로=fensetere->세로좌표;처음너비=fensetere->너비;처음높이=fensetere->높이;
            if(setlhaodi_Boleng!=Tsepamo)앞으로올리기(setlhaodi_Boleng);return;
        }
        if(세로좌표<32&&kgokagano_ya_x>=6&&kgokagano_ya_x<142){tlhama_tsenyo();return;}
        if(세로좌표<32&&kgokagano_ya_x>=154&&kgokagano_ya_x<602){앞으로올리기((kgokagano_ya_x-154)/112);return;}
        if(setlhaodi_Boleng>=0){
            터미널상태 *fensetere=&창들[setlhaodi_Boleng];
            if(세로좌표<(int)fensetere->세로좌표+30&&kgokagano_ya_x>=(int)(fensetere->kgokagano_ya_x+fensetere->너비)-32){tswala_fensetere(setlhaodi_Boleng);return;}
            if(setlhaodi_Boleng!=Tsepamo)앞으로올리기(setlhaodi_Boleng);
            if(세로좌표<(int)fensetere->세로좌표+30){Goga_Boleng=setlhaodi_Boleng;끌기가로=kgokagano_ya_x-fensetere->kgokagano_ya_x;끌기세로=세로좌표-fensetere->세로좌표;}return;
        }
    }
    if(Tsepamo>=0&&(눌림&(8|16))){터미널항목=&창들[Tsepamo];if(눌림&8){unsigned 한도=터미널항목->맨위;if(한도>기록줄수-터미널항목->행수)한도=기록줄수-터미널항목->행수;터미널항목->sekorola=터미널항목->sekorola+9>한도?한도:터미널항목->sekorola+9;}else 터미널항목->sekorola=터미널항목->sekorola<9?0:터미널항목->sekorola-9;다시그리기();}
}
void 터미널바로가기키(unsigned 누름값){if(누름값==1)tlhama_tsenyo();if(누름값==2&&항목수)앞으로올리기(thulaganyo_Boleng[0]);if(누름값==3)tswala_fensetere(Tsepamo);}
motšhine_Lefoko 보드터미널(motšhine_Lefoko tiro){
    if(tiro==300){if(!창들[출력결과].살아있음)return tlhama_tsenyo();desekethopo_Tebego=1;다시그리기();return 0;}
    if(tiro==0){tswala_fensetere(Tsepamo);return 0;}if(tiro==1)return (uint32_t)tlhama_tsenyo();if(tiro==2)return Tsepamo>=0;
    if(tiro==9){desekethopo_Tebego=0;return 0;}if(tiro==7)return 항목수;if(tiro==10)return Tsepamo+1;if(tiro==11)return 출력결과;
    if(tiro==13){터미널상태 *fensetere=&창들[출력결과];return fensetere->살아있음?(fensetere->행수<<16)|fensetere->열수:(19<<16)|68;}
    if(tiro==14){unsigned Boleng=창들[출력결과].크기바뀜;창들[출력결과].크기바뀜=0;return Boleng;}
    if(tiro==12){unsigned Boleng=대기중;대기중=0;return Boleng;}
    if(tiro>=20&&tiro<24)return 창들[tiro-20].살아있음;
    if(tiro>=100&&tiro<104){출력결과=tiro-100;터미널항목=&창들[출력결과];return 0;}
    if(tiro>=200&&tiro<204){앞으로올리기(tiro-200);return 0;}
    if(tiro==3){다시그리기();return 0;}터미널항목=&창들[출력결과];if(!터미널항목->살아있음)return 0;
    if(tiro==4)phimola_TOC();if(tiro==5||tiro==6){unsigned 이전=단추들;터미널가리킴(tiro==5?8:16,0,0);단추들=이전;}return 1;
}
