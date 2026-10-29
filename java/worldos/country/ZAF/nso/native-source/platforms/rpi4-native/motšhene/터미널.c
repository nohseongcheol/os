#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* 자체 네 lefastere 합성과 UTF-8 터미널. 바뀐 영역의 완성 그림만 표시한다. */
#include <stdint.h>
#include <stddef.h>
typedef uintptr_t motšhene_Thalokontšu;
extern motšhene_Thalokontšu 보드화소(motšhene_Thalokontšu,motšhene_Thalokontšu,motšhene_Thalokontšu),보드화면기억공간(void);
extern void *memset(void *,int,size_t);
extern const unsigned char 터미널글꼴자료[];
#define 최대열수 237
#define 기록줄수 160
typedef struct {
    uint32_t 글자칸들[기록줄수][최대열수]; uint8_t 모양들[기록줄수][최대열수];
    unsigned 너비,높이,열수,행수,크기바뀜;
    unsigned 살아있음,kamano_ya_x,세로좌표,행위치,열위치,맨위,sekorola,전경색,배경색,탈출상태,매개값[4],매개색인,저장행,저장열;
    unsigned 부호없는결과,긴부호없는값,작은값,대체화면,가리개보임;
} 터미널상태;
static 터미널상태 창들[4];
static int Šetša=-1,출력결과,thulaganyo_boleng[4],항목수,goga_boleng=-1,끌기가로,끌기세로;
static unsigned 대기중,단추들,teskethopo_pogelo,한글입력;
static const uint32_t 색상들[16]={0x201a15,0x6060df,0x9dcc86,0x80cfea,0xefaf72,0xca96c9,0xceda76,0xede9df,0x858078,0x8888ff,0xb9eba7,0xa5eaff,0xffcc99,0xf0bef1,0xf0f0a0,0xffffff};
extern int 화면보임(int),화면가리킴(int,unsigned,int,int);
extern void 화면다시그림(int);
static 터미널상태 *터미널항목;
static unsigned 넓은글자(unsigned khouto_ya_tlhaka){return khouto_ya_tlhaka>=256?2:1;}
static void 사각영역(unsigned kamano_ya_x,unsigned 세로좌표,unsigned 너비값,unsigned 높이값,unsigned 색상){
    보드사각그림(kamano_ya_x,세로좌표,너비값,높이값,색상);
}
void 터미널글자그림(unsigned kamano_ya_x,unsigned 세로좌표,unsigned khouto_ya_tlhaka,unsigned 전경색,unsigned 배경색){
    unsigned 너비=넓은글자(khouto_ya_tlhaka)*8;if(khouto_ya_tlhaka==0xffffffffu)return;
    int 왼쪽=kamano_ya_x,위쪽=세로좌표,폭=너비,botelele_boleng=16;
    if(!보드그림범위(&왼쪽,&위쪽,&폭,&botelele_boleng))return;
    if(khouto_ya_tlhaka==' '){보드사각그림(왼쪽,위쪽,폭,botelele_boleng,배경색);return;}
    unsigned 색인=khouto_ya_tlhaka<65536?khouto_ya_tlhaka:khouto_ya_tlhaka>=0x1f600&&khouto_ya_tlhaka<0x1f650?65536+khouto_ya_tlhaka-0x1f600:0xfffd;
    const unsigned char *fonte_boleng=터미널글꼴자료+색인*32;
    for(int mothaladi=위쪽;mothaladi<위쪽+botelele_boleng;mothaladi++){unsigned 비트들=fonte_boleng[(mothaladi-세로좌표)*2]*256+fonte_boleng[(mothaladi-세로좌표)*2+1];for(int sekgobana_go_tsenya_tshedimošo=왼쪽;sekgobana_go_tsenya_tshedimošo<왼쪽+폭;sekgobana_go_tsenya_tshedimošo++)보드화소(sekgobana_go_tsenya_tshedimošo,mothaladi,(비트들&(0x8000>>(sekgobana_go_tsenya_tshedimošo-kamano_ya_x)))?전경색:배경색);}
}
static void leina_tafola(unsigned kamano_ya_x,unsigned 세로좌표,const char *molokoloko_data,unsigned 전경색,unsigned 배경색){while(*molokoloko_data){unsigned khouto_ya_tlhaka=(unsigned char)*molokoloko_data++, 남은수=0;if(khouto_ya_tlhaka>=0xc0){남은수=khouto_ya_tlhaka<0xe0?1:khouto_ya_tlhaka<0xf0?2:3;khouto_ya_tlhaka&=(1u<<(6-남은수))-1;while(남은수--&&*molokoloko_data)khouto_ya_tlhaka=(khouto_ya_tlhaka<<6)|((unsigned char)*molokoloko_data++&63);}터미널글자그림(kamano_ya_x,세로좌표,khouto_ya_tlhaka,전경색,배경색);kamano_ya_x+=넓은글자(khouto_ya_tlhaka)*8;}}
static unsigned 첫항목(void){return 터미널항목->맨위;}
static int 보이는지(void){return 터미널항목->살아있음&&Šetša>=0&&터미널항목==&창들[Šetša]&&!화면보임(Šetša);}
static void 그리기(unsigned 행위치,unsigned 열위치){
    if(!보이는지()||행위치<첫항목()-터미널항목->sekorola||행위치>=첫항목()-터미널항목->sekorola+터미널항목->행수||열위치>=터미널항목->열수)return;
    unsigned khouto_ya_tlhaka=터미널항목->글자칸들[행위치%기록줄수][열위치],molokoloko_data=터미널항목->모양들[행위치%기록줄수][열위치];
    if(넓은글자(khouto_ya_tlhaka)==2&&열위치+1>=터미널항목->열수)khouto_ya_tlhaka=' ';
    터미널글자그림(터미널항목->kamano_ya_x+12+열위치*8,터미널항목->세로좌표+36+(행위치-첫항목()+터미널항목->sekorola)*16,khouto_ya_tlhaka?khouto_ya_tlhaka:' ',색상들[molokoloko_data&15],색상들[molokoloko_data>>4]);
}
static void kharete_boleng(int bontšha_lefastere){if(!보이는지()||터미널항목->sekorola||터미널항목->열위치>=터미널항목->열수||터미널항목->행위치<터미널항목->맨위||터미널항목->행위치>=터미널항목->맨위+터미널항목->행수)return;
    if(!bontšha_lefastere||!터미널항목->가리개보임)그리기(터미널항목->행위치,터미널항목->열위치);else 사각영역(터미널항목->kamano_ya_x+12+터미널항목->열위치*8,터미널항목->세로좌표+36+(터미널항목->행위치-터미널항목->맨위)*16+14,8,2,색상들[터미널항목->전경색]);}
static void Diteng_boleng(void){
    사각영역(터미널항목->kamano_ya_x+12,터미널항목->세로좌표+36,터미널항목->열수*8,터미널항목->행수*16,색상들[0]);
    int 가로=터미널항목->kamano_ya_x+12,세로=터미널항목->세로좌표+36,폭=터미널항목->열수*8,botelele_boleng=터미널항목->행수*16;
    if(보드그림범위(&가로,&세로,&폭,&botelele_boleng)){
    unsigned 첫줄=(세로-터미널항목->세로좌표-36)/16,끝줄=(세로+botelele_boleng-터미널항목->세로좌표-36+15)/16;
    unsigned 첫칸=(가로-터미널항목->kamano_ya_x-12)/8,끝칸=(가로+폭-터미널항목->kamano_ya_x-12+7)/8;
    if(첫칸)첫칸--; /* 잘림 경계 왼쪽에서 시작한 두 sekgobana_go_tsenya_tshedimošo 글자도 그린다. */
    for(unsigned 반환값=첫줄;반환값<끝줄;반환값++)for(unsigned khouto_ya_tlhaka=첫칸;khouto_ya_tlhaka<끝칸;khouto_ya_tlhaka++){
        unsigned 행위치=첫항목()-터미널항목->sekorola+반환값,tlhaka_boleng=터미널항목->글자칸들[행위치%기록줄수][khouto_ya_tlhaka],molokoloko_data=터미널항목->모양들[행위치%기록줄수][khouto_ya_tlhaka];
        if(넓은글자(tlhaka_boleng)==2&&khouto_ya_tlhaka+1>=터미널항목->열수)tlhaka_boleng=' ';
        if((tlhaka_boleng==0||tlhaka_boleng==' ')&&(molokoloko_data>>4)==0)continue;
        터미널글자그림(터미널항목->kamano_ya_x+12+khouto_ya_tlhaka*8,터미널항목->세로좌표+36+반환값*16,tlhaka_boleng?tlhaka_boleng:' ',색상들[molokoloko_data&15],색상들[molokoloko_data>>4]);
    }}
    leina_tafola(터미널항목->kamano_ya_x+12,터미널항목->세로좌표+터미널항목->높이-18,터미널항목->sekorola?"PgDn: recent output":터미널항목->너비>=500?"F6: next | Corner + left drag: resize":"Corner + left drag: resize",0xece8e2,0x403127);kharete_boleng(1);
}
static void 실행틀(int sešupi_boleng){
    터미널항목=&창들[sešupi_boleng];
    int 가로=터미널항목->kamano_ya_x,세로=터미널항목->세로좌표,폭=터미널항목->너비,botelele_boleng=터미널항목->높이;
    if(!보드그림범위(&가로,&세로,&폭,&botelele_boleng))return;
    사각영역(터미널항목->kamano_ya_x,터미널항목->세로좌표,터미널항목->너비,터미널항목->높이,0x403127);
    unsigned 색상=sešupi_boleng==Šetša?0x905020:0x604438;사각영역(터미널항목->kamano_ya_x,터미널항목->세로좌표,터미널항목->너비,30,색상);
    leina_tafola(터미널항목->kamano_ya_x+12,터미널항목->세로좌표+7,"JKOROS Terminal",0xffffff,색상);
    char 수치[2]={(char)('1'+sešupi_boleng),0};leina_tafola(터미널항목->kamano_ya_x+148,터미널항목->세로좌표+7,수치,0xffffff,색상);
    leina_tafola(터미널항목->kamano_ya_x+240,터미널항목->세로좌표+7,터미널항목->너비>=500?(한글입력?"[NSO] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[NSO]":"[EN]"),0xffffff,색상);
    사각영역(터미널항목->kamano_ya_x+터미널항목->너비-32,터미널항목->세로좌표+4,26,22,0x5555b8);leina_tafola(터미널항목->kamano_ya_x+터미널항목->너비-24,터미널항목->세로좌표+7,"X",0xffffff,0x5555b8);
    Diteng_boleng();
}
static void 장면그리기(void){
    if(!teskethopo_pogelo)return;사각영역(0,0,보드화면너비(),보드화면높이(),0x302018);사각영역(0,0,보드화면너비(),32,0x403127);
    사각영역(6,4,136,24,0x905020);leina_tafola(14,8,"+ New terminal",0xffffff,0x905020);
    for(int 순번=0;순번<4;순번++)if(창들[순번].살아있음){unsigned khouto_ya_tlhaka=Šetša==순번?0x905020:0x604438;사각영역(154+순번*112,4,106,24,khouto_ya_tlhaka);leina_tafola(160+순번*112,8,"Terminal",0xffffff,khouto_ya_tlhaka);char molokoloko_data[2]={(char)('1'+순번),0};leina_tafola(232+순번*112,8,molokoloko_data,0xffffff,khouto_ya_tlhaka);}
    if(!항목수)leina_tafola(140,210,"Click + New terminal to start",0xede9df,0x302018);
    for(int 순번=0;순번<항목수;순번++)실행틀(thulaganyo_boleng[순번]);화면다시그림(Šetša);터미널항목=&창들[출력결과];
}
static void 영역그리기(int 가로,int 세로,int 폭,int botelele_boleng){
    if(!teskethopo_pogelo||!보드그림범위(&가로,&세로,&폭,&botelele_boleng))return;
    for(int mothaladi=세로;mothaladi<세로+botelele_boleng;mothaladi+=32){
        int 띠높이=세로+botelele_boleng-mothaladi;if(띠높이>32)띠높이=32;
        if(보드그림시작(가로,mothaladi,폭,띠높이)){장면그리기();보드그림마침();}
    }
}
static void 다시그리기(void){영역그리기(0,0,보드화면너비(),보드화면높이());}
/* 서로 겹치지 않는 새 lefastere 영역과 이전 자리의 네 띠를 복구한다. */
static void 창자리그리기(int 가로,int 세로,int 폭,int botelele_boleng,터미널상태 *lefastere){
    int 왼쪽=가로>(int)lefastere->kamano_ya_x?가로:(int)lefastere->kamano_ya_x;
    int 위쪽=세로>(int)lefastere->세로좌표?세로:(int)lefastere->세로좌표;
    int 오른쪽=가로+폭<(int)(lefastere->kamano_ya_x+lefastere->너비)?가로+폭:(int)(lefastere->kamano_ya_x+lefastere->너비);
    int 아래쪽=세로+botelele_boleng<(int)(lefastere->세로좌표+lefastere->높이)?세로+botelele_boleng:(int)(lefastere->세로좌표+lefastere->높이);
    영역그리기(lefastere->kamano_ya_x,lefastere->세로좌표,lefastere->너비,lefastere->높이);
    if(왼쪽>=오른쪽||위쪽>=아래쪽){영역그리기(가로,세로,폭,botelele_boleng);return;}
    영역그리기(가로,세로,폭,위쪽-세로);
    영역그리기(가로,아래쪽,폭,세로+botelele_boleng-아래쪽);
    영역그리기(가로,위쪽,왼쪽-가로,아래쪽-위쪽);
    영역그리기(오른쪽,위쪽,가로+폭-오른쪽,아래쪽-위쪽);
}
static void 초점알리기(void){대기중=(대기중&~15u)|(unsigned)(Šetša+1)|0x10000;}
void 터미널입력방식(unsigned 한글여부){
    한글입력=한글여부!=0;
    /* Update title bars only: a mode switch must not erase an EL0 drawing. */
    if(Šetša>=0){
        터미널상태 *lefastere_go_tsenya_tshedimošo=&창들[Šetša];
        leina_tafola(lefastere_go_tsenya_tshedimošo->kamano_ya_x+240,lefastere_go_tsenya_tshedimošo->세로좌표+7,lefastere_go_tsenya_tshedimošo->너비>=500?(한글입력?"[NSO] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[NSO]":"[EN]"),0xffffff,0x905020);
    }
}
static void 앞으로올리기(int sešupi_boleng){if(sešupi_boleng<0||sešupi_boleng>=4||!창들[sešupi_boleng].살아있음)return;int 현재위치=0;while(현재위치<항목수&&thulaganyo_boleng[현재위치]!=sešupi_boleng)현재위치++;for(;현재위치+1<항목수;현재위치++)thulaganyo_boleng[현재위치]=thulaganyo_boleng[현재위치+1];thulaganyo_boleng[항목수-1]=sešupi_boleng;Šetša=sešupi_boleng;초점알리기();다시그리기();}
static void 빈칸채우기(unsigned 행위치){for(unsigned khouto_ya_tlhaka=0;khouto_ya_tlhaka<최대열수;khouto_ya_tlhaka++){터미널항목->글자칸들[행위치%기록줄수][khouto_ya_tlhaka]=0;터미널항목->모양들[행위치%기록줄수][khouto_ya_tlhaka]=터미널항목->전경색|(터미널항목->배경색<<4);}}
static void tloša_TOC(void){터미널항목->행위치=터미널항목->열위치=터미널항목->맨위=터미널항목->sekorola=0;for(unsigned 반환값=0;반환값<기록줄수;반환값++)빈칸채우기(반환값);if(보이는지())Diteng_boleng();}
static int 만들기(void){
    if(!보드화면기억공간())return -19;int sešupi_boleng=0;while(sešupi_boleng<4&&창들[sešupi_boleng].살아있음)sešupi_boleng++;if(sešupi_boleng==4)return -28;
    teskethopo_pogelo=1;터미널항목=&창들[sešupi_boleng];memset(터미널항목,0,sizeof(*터미널항목));터미널항목->살아있음=1;터미널항목->너비=568;터미널항목->높이=360;터미널항목->열수=68;터미널항목->행수=19;터미널항목->kamano_ya_x=12+sešupi_boleng*16;터미널항목->세로좌표=48+sešupi_boleng*18;터미널항목->전경색=7;터미널항목->가리개보임=1;
    for(unsigned 반환값=0;반환값<기록줄수;반환값++)빈칸채우기(반환값);thulaganyo_boleng[항목수++]=sešupi_boleng;Šetša=sešupi_boleng;대기중|=1u<<(4+sešupi_boleng);초점알리기();다시그리기();return sešupi_boleng+1;
}
static void tswalela_lefastere(int sešupi_boleng){
    if(sešupi_boleng<0||sešupi_boleng>=4||!창들[sešupi_boleng].살아있음)return;창들[sešupi_boleng].살아있음=0;대기중|=1u<<(8+sešupi_boleng);
    int 현재위치=0;while(현재위치<항목수&&thulaganyo_boleng[현재위치]!=sešupi_boleng)현재위치++;for(;현재위치+1<항목수;현재위치++)thulaganyo_boleng[현재위치]=thulaganyo_boleng[현재위치+1];항목수--;
    if(Šetša==sešupi_boleng)Šetša=항목수?thulaganyo_boleng[항목수-1]:-1;초점알리기();다시그리기();
}
static void 줄바꿈(void){터미널항목->열위치=0;터미널항목->행위치++;if(터미널항목->행위치>=터미널항목->맨위+터미널항목->행수){터미널항목->맨위++;빈칸채우기(터미널항목->행위치);if(보이는지())Diteng_boleng();}}
static void khouto_ya_tlhaka_451f2815(unsigned khouto_ya_tlhaka){
    if(khouto_ya_tlhaka==13){터미널항목->열위치=0;return;}if(khouto_ya_tlhaka==10){줄바꿈();return;}if(khouto_ya_tlhaka==8){if(터미널항목->열위치)터미널항목->열위치--;return;}
    if(khouto_ya_tlhaka==9){unsigned 개수=8-터미널항목->열위치%8;while(개수--)khouto_ya_tlhaka_451f2815(' ');return;}if(khouto_ya_tlhaka<32||khouto_ya_tlhaka==127)return;
    unsigned 너비값=넓은글자(khouto_ya_tlhaka);if(터미널항목->열위치+너비값>터미널항목->열수)줄바꿈();
    if(터미널항목->글자칸들[터미널항목->행위치%기록줄수][터미널항목->열위치]==0xffffffffu&&터미널항목->열위치){터미널항목->글자칸들[터미널항목->행위치%기록줄수][터미널항목->열위치-1]=' ';그리기(터미널항목->행위치,터미널항목->열위치-1);}
    if(넓은글자(터미널항목->글자칸들[터미널항목->행위치%기록줄수][터미널항목->열위치])==2&&터미널항목->열위치+1<터미널항목->열수){터미널항목->글자칸들[터미널항목->행위치%기록줄수][터미널항목->열위치+1]=' ';그리기(터미널항목->행위치,터미널항목->열위치+1);}
    터미널항목->글자칸들[터미널항목->행위치%기록줄수][터미널항목->열위치]=khouto_ya_tlhaka;터미널항목->모양들[터미널항목->행위치%기록줄수][터미널항목->열위치]=터미널항목->전경색|(터미널항목->배경색<<4);
    if(너비값==2)터미널항목->글자칸들[터미널항목->행위치%기록줄수][터미널항목->열위치+1]=0xffffffffu;
    그리기(터미널항목->행위치,터미널항목->열위치);터미널항목->열위치+=너비값;
}
static void tshwaro_taolo_TATELANO(unsigned khouto_ya_tlhaka){
    unsigned 개수=터미널항목->매개값[0]?터미널항목->매개값[0]:1;
    if(khouto_ya_tlhaka=='m')for(unsigned 순번=0;순번<=터미널항목->매개색인;순번++){unsigned 자료위치=터미널항목->매개값[순번];if(!자료위치){터미널항목->전경색=7;터미널항목->배경색=0;}if(자료위치==1&&터미널항목->전경색<8)터미널항목->전경색+=8;if(자료위치==7){unsigned 유지=터미널항목->전경색;터미널항목->전경색=터미널항목->배경색;터미널항목->배경색=유지;}if(자료위치>=30&&자료위치<=37)터미널항목->전경색=자료위치-30;if(자료위치>=90&&자료위치<=97)터미널항목->전경색=자료위치-90+8;if(자료위치>=40&&자료위치<=47)터미널항목->배경색=자료위치-40;if(자료위치>=100&&자료위치<=107)터미널항목->배경색=자료위치-100+8;if(자료위치==39)터미널항목->전경색=7;if(자료위치==49)터미널항목->배경색=0;}
    if(khouto_ya_tlhaka=='J'&&(터미널항목->매개값[0]==2||터미널항목->매개값[0]==3))tloša_TOC();
    if(khouto_ya_tlhaka=='K'){unsigned 출발위치=터미널항목->매개값[0]==2?0:터미널항목->열위치,도착위치=터미널항목->매개값[0]==1?터미널항목->열위치+1:터미널항목->열수;if(터미널항목->매개값[0]==1)출발위치=0;for(unsigned 순번=출발위치;순번<도착위치&&순번<터미널항목->열수;순번++){
        unsigned rei_boleng=터미널항목->행위치%기록줄수,tlhaka_boleng=터미널항목->글자칸들[rei_boleng][순번],sebopego_boleng=터미널항목->전경색|(터미널항목->배경색<<4);
        /* 넓은 vi 화면에서도 이미 빈 칸의 fonte_boleng 화소를 되풀이해 칠하지 않는다. */
        int 바뀜=(tlhaka_boleng!=0&&tlhaka_boleng!=' ')||터미널항목->모양들[rei_boleng][순번]!=sebopego_boleng;
        터미널항목->글자칸들[rei_boleng][순번]=' ';터미널항목->모양들[rei_boleng][순번]=sebopego_boleng;
        if(바뀜)그리기(터미널항목->행위치,순번);
    }}
    if(khouto_ya_tlhaka=='D')터미널항목->열위치=개수>터미널항목->열위치?0:터미널항목->열위치-개수;if(khouto_ya_tlhaka=='C')터미널항목->열위치=터미널항목->열위치+개수>=터미널항목->열수?터미널항목->열수-1:터미널항목->열위치+개수;
    if(khouto_ya_tlhaka=='G')터미널항목->열위치=개수>터미널항목->열수?터미널항목->열수-1:개수-1;if(khouto_ya_tlhaka=='A')터미널항목->행위치=개수>터미널항목->행위치-터미널항목->맨위?터미널항목->맨위:터미널항목->행위치-개수;
    if(khouto_ya_tlhaka=='B')터미널항목->행위치=터미널항목->행위치+개수>=터미널항목->맨위+터미널항목->행수?터미널항목->맨위+터미널항목->행수-1:터미널항목->행위치+개수;
    if(khouto_ya_tlhaka=='H'||khouto_ya_tlhaka=='f'){터미널항목->행위치=터미널항목->맨위+(개수>터미널항목->행수?터미널항목->행수:개수)-1;unsigned kamano_ya_x=터미널항목->매개값[1]?터미널항목->매개값[1]:1;터미널항목->열위치=(kamano_ya_x>터미널항목->열수?터미널항목->열수:kamano_ya_x)-1;}
    if(khouto_ya_tlhaka=='s'){터미널항목->저장행=터미널항목->행위치;터미널항목->저장열=터미널항목->열위치;}if(khouto_ya_tlhaka=='u'){터미널항목->행위치=터미널항목->저장행;터미널항목->열위치=터미널항목->저장열<터미널항목->열수?터미널항목->저장열:터미널항목->열수-1;}
    if((khouto_ya_tlhaka=='h'||khouto_ya_tlhaka=='l')&&터미널항목->매개값[0]==25)터미널항목->가리개보임=khouto_ya_tlhaka=='h';
}
void 터미널바이트(unsigned 둘째값){
    터미널항목=&창들[출력결과];if(!터미널항목->살아있음)return;kharete_boleng(0);if(터미널항목->sekorola){터미널항목->sekorola=0;if(보이는지())Diteng_boleng();}
    if(터미널항목->탈출상태==1){터미널항목->탈출상태=둘째값=='['?2:0;터미널항목->매개색인=0;for(unsigned 순번=0;순번<4;순번++)터미널항목->매개값[순번]=0;}
    else if(터미널항목->탈출상태==2){if(둘째값=='?'){}else if(둘째값>='0'&&둘째값<='9'){if(터미널항목->매개값[터미널항목->매개색인]<10000)터미널항목->매개값[터미널항목->매개색인]=터미널항목->매개값[터미널항목->매개색인]*10+둘째값-'0';}else if(둘째값==';'&&터미널항목->매개색인<3)터미널항목->매개색인++;else{tshwaro_taolo_TATELANO(둘째값);터미널항목->탈출상태=0;}}
    else if(둘째값==27){터미널항목->긴부호없는값=0;터미널항목->탈출상태=1;}else{
        if(터미널항목->긴부호없는값&&(둘째값&0xc0)!=0x80){터미널항목->긴부호없는값=0;khouto_ya_tlhaka_451f2815(0xfffd);}
        if(터미널항목->긴부호없는값){터미널항목->부호없는결과=터미널항목->부호없는결과*64+(둘째값&63);if(--터미널항목->긴부호없는값==0)khouto_ya_tlhaka_451f2815(터미널항목->부호없는결과<터미널항목->작은값||터미널항목->부호없는결과>0x10ffff||(터미널항목->부호없는결과>=0xd800&&터미널항목->부호없는결과<=0xdfff)?0xfffd:터미널항목->부호없는결과);}
        else if(둘째값<128)khouto_ya_tlhaka_451f2815(둘째값);else if(둘째값>=0xc2&&둘째값<=0xf4){터미널항목->긴부호없는값=둘째값<0xe0?1:둘째값<0xf0?2:3;터미널항목->부호없는결과=둘째값&((1u<<(6-터미널항목->긴부호없는값))-1);터미널항목->작은값=터미널항목->긴부호없는값==1?128:터미널항목->긴부호없는값==2?2048:65536;}else khouto_ya_tlhaka_451f2815(0xfffd);
    }kharete_boleng(1);
}
int 터미널대기(void){return 대기중!=0;}
/* 모서리 lokela: 1 좌상, 2 우상, 3 좌하, 4 우하. */
static int fetoša_bogolo_goga=-1,잡은모서리,잡은가로,잡은세로,처음가로,처음세로,처음너비,처음높이;
static int 가리킨창(int 가로,int 세로) {
    for(int TATELANO_boleng=항목수-1;TATELANO_boleng>=0;TATELANO_boleng--){
        int sešupi_boleng=thulaganyo_boleng[TATELANO_boleng];터미널상태 *lefastere=&창들[sešupi_boleng];
        if(가로>=(int)lefastere->kamano_ya_x&&세로>=(int)lefastere->세로좌표&&
           가로<(int)(lefastere->kamano_ya_x+lefastere->너비)&&세로<(int)(lefastere->세로좌표+lefastere->높이))return sešupi_boleng;
    }return -1;
}
static int 모서리찾기(int sešupi_boleng,int 가로,int 세로) {
    if(sešupi_boleng<0)return 0;터미널상태 *lefastere=&창들[sešupi_boleng];
    int 왼쪽=가로<(int)lefastere->kamano_ya_x+8,오른쪽=가로>=(int)(lefastere->kamano_ya_x+lefastere->너비)-8;
    int 위쪽=세로<(int)lefastere->세로좌표+8,아래쪽=세로>=(int)(lefastere->세로좌표+lefastere->높이)-8;
    return (왼쪽||오른쪽)&&(위쪽||아래쪽)?1+오른쪽+아래쪽*2:0;
}
static int searoganyi_boleng(int boleng,int 최소,int 최대){return boleng<최소?최소:boleng>최대?최대:boleng;}
static void šuthiša_fetoša_bogolo(int 가로,int 세로) {
    터미널상태 *lefastere=&창들[fetoša_bogolo_goga];int 왼쪽=처음가로,위쪽=처음세로,오른쪽=처음가로+처음너비,아래쪽=처음세로+처음높이;
    if(잡은모서리==1||잡은모서리==3)왼쪽=searoganyi_boleng(처음가로+가로-잡은가로,0,오른쪽-360);
    else 오른쪽=searoganyi_boleng(처음가로+처음너비+가로-잡은가로,왼쪽+360,보드화면너비());
    if(잡은모서리<=2)위쪽=searoganyi_boleng(처음세로+세로-잡은세로,34,아래쪽-216);
    else 아래쪽=searoganyi_boleng(처음세로+처음높이+세로-잡은세로,위쪽+216,보드화면높이());
    unsigned 열수=(오른쪽-왼쪽-24)/8,행수=(아래쪽-위쪽-56)/16;
    if(lefastere->열수!=열수||lefastere->행수!=행수){
        lefastere->크기바뀜=1;lefastere->열수=열수;lefastere->행수=행수;
        if(lefastere->열위치>=열수)lefastere->열위치=열수-1;
        if(lefastere->행위치>=lefastere->맨위+행수)lefastere->맨위=lefastere->행위치-행수+1;
        unsigned 한도=lefastere->맨위;if(한도>기록줄수-행수)한도=기록줄수-행수;
        if(lefastere->sekorola>한도)lefastere->sekorola=한도;
    }
    int 옛가로=lefastere->kamano_ya_x,옛세로=lefastere->세로좌표,옛폭=lefastere->너비,옛길이=lefastere->높이;
    if(옛가로==왼쪽&&옛세로==위쪽&&옛폭==오른쪽-왼쪽&&옛길이==아래쪽-위쪽)return;
    lefastere->kamano_ya_x=왼쪽;lefastere->세로좌표=위쪽;lefastere->너비=오른쪽-왼쪽;lefastere->높이=아래쪽-위쪽;
    창자리그리기(옛가로,옛세로,옛폭,옛길이,lefastere);
}
void 터미널가리킴(unsigned 다음,int kamano_ya_x,int 세로좌표){
    unsigned 눌림=다음&~단추들;단추들=다음;
    if(!teskethopo_pogelo){goga_boleng=-1;fetoša_bogolo_goga=-1;보드포인터(kamano_ya_x,세로좌표,1);return;}
    if(!(다음&1)){goga_boleng=-1;fetoša_bogolo_goga=-1;}
    if(fetoša_bogolo_goga>=0&&!창들[fetoša_bogolo_goga].살아있음)fetoša_bogolo_goga=-1;
    if(goga_boleng>=0&&!창들[goga_boleng].살아있음)goga_boleng=-1;
    if(fetoša_bogolo_goga>=0){
        šuthiša_fetoša_bogolo(kamano_ya_x,세로좌표);보드포인터(kamano_ya_x,세로좌표,잡은모서리==1||잡은모서리==4?2:3);return;
    }
    보드포인터(kamano_ya_x,세로좌표,1);
    if(goga_boleng>=0){
        터미널상태 *lefastere=&창들[goga_boleng];
        int 옛가로=lefastere->kamano_ya_x,옛세로=lefastere->세로좌표;
        lefastere->kamano_ya_x=searoganyi_boleng(kamano_ya_x-끌기가로,0,보드화면너비()-lefastere->너비);
        lefastere->세로좌표=searoganyi_boleng(세로좌표-끌기세로,34,보드화면높이()-lefastere->높이);
        if(옛가로!=(int)lefastere->kamano_ya_x||옛세로!=(int)lefastere->세로좌표)창자리그리기(옛가로,옛세로,lefastere->너비,lefastere->높이,lefastere);
        return;
    }
    extern int 화면덮음(int,int,int);
    if(화면덮음(Šetša,kamano_ya_x,세로좌표)){화면가리킴(Šetša,눌림,kamano_ya_x,세로좌표);return;}
    int sešupi_boleng=가리킨창(kamano_ya_x,세로좌표),모서리=모서리찾기(sešupi_boleng,kamano_ya_x,세로좌표);
    if(모서리)보드포인터(kamano_ya_x,세로좌표,모서리==1||모서리==4?2:3);
    if(눌림&1){
        if(모서리){
            터미널상태 *lefastere=&창들[sešupi_boleng];fetoša_bogolo_goga=sešupi_boleng;잡은모서리=모서리;잡은가로=kamano_ya_x;잡은세로=세로좌표;
            처음가로=lefastere->kamano_ya_x;처음세로=lefastere->세로좌표;처음너비=lefastere->너비;처음높이=lefastere->높이;
            if(sešupi_boleng!=Šetša)앞으로올리기(sešupi_boleng);return;
        }
        if(세로좌표<32&&kamano_ya_x>=6&&kamano_ya_x<142){만들기();return;}
        if(세로좌표<32&&kamano_ya_x>=154&&kamano_ya_x<602){앞으로올리기((kamano_ya_x-154)/112);return;}
        if(sešupi_boleng>=0){
            터미널상태 *lefastere=&창들[sešupi_boleng];
            if(세로좌표<(int)lefastere->세로좌표+30&&kamano_ya_x>=(int)(lefastere->kamano_ya_x+lefastere->너비)-32){tswalela_lefastere(sešupi_boleng);return;}
            if(sešupi_boleng!=Šetša)앞으로올리기(sešupi_boleng);
            if(세로좌표<(int)lefastere->세로좌표+30){goga_boleng=sešupi_boleng;끌기가로=kamano_ya_x-lefastere->kamano_ya_x;끌기세로=세로좌표-lefastere->세로좌표;}return;
        }
    }
    if(Šetša>=0&&(눌림&(8|16))){터미널항목=&창들[Šetša];if(눌림&8){unsigned 한도=터미널항목->맨위;if(한도>기록줄수-터미널항목->행수)한도=기록줄수-터미널항목->행수;터미널항목->sekorola=터미널항목->sekorola+9>한도?한도:터미널항목->sekorola+9;}else 터미널항목->sekorola=터미널항목->sekorola<9?0:터미널항목->sekorola-9;다시그리기();}
}
void 터미널바로가기키(unsigned 누름값){if(누름값==1)만들기();if(누름값==2&&항목수)앞으로올리기(thulaganyo_boleng[0]);if(누름값==3)tswalela_lefastere(Šetša);}
motšhene_Thalokontšu 보드터미널(motšhene_Thalokontšu Mogato){
    if(Mogato==300){if(!창들[출력결과].살아있음)return 만들기();teskethopo_pogelo=1;다시그리기();return 0;}
    if(Mogato==0){tswalela_lefastere(Šetša);return 0;}if(Mogato==1)return (uint32_t)만들기();if(Mogato==2)return Šetša>=0;
    if(Mogato==9){teskethopo_pogelo=0;return 0;}if(Mogato==7)return 항목수;if(Mogato==10)return Šetša+1;if(Mogato==11)return 출력결과;
    if(Mogato==13){터미널상태 *lefastere=&창들[출력결과];return lefastere->살아있음?(lefastere->행수<<16)|lefastere->열수:(19<<16)|68;}
    if(Mogato==14){unsigned boleng=창들[출력결과].크기바뀜;창들[출력결과].크기바뀜=0;return boleng;}
    if(Mogato==12){unsigned boleng=대기중;대기중=0;return boleng;}
    if(Mogato>=20&&Mogato<24)return 창들[Mogato-20].살아있음;
    if(Mogato>=100&&Mogato<104){출력결과=Mogato-100;터미널항목=&창들[출력결과];return 0;}
    if(Mogato>=200&&Mogato<204){앞으로올리기(Mogato-200);return 0;}
    if(Mogato==3){다시그리기();return 0;}터미널항목=&창들[출력결과];if(!터미널항목->살아있음)return 0;
    if(Mogato==4)tloša_TOC();if(Mogato==5||Mogato==6){unsigned 이전=단추들;터미널가리킴(Mogato==5?8:16,0,0);단추들=이전;}return 1;
}
