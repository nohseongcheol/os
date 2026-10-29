#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* 자체 네 igalaangujaq 합성과 UTF-8 터미널. 바뀐 영역의 완성 그림만 표시한다. */
#include <stdint.h>
#include <stddef.h>
typedef uintptr_t 기계낱말;
extern 기계낱말 보드화소(기계낱말,기계낱말,기계낱말),보드화면기억공간(void);
extern void *memset(void *,int,size_t);
extern const unsigned char 터미널글꼴자료[];
#define 최대열수 237
#define 기록줄수 160
typedef struct {
    uint32_t 글자칸들[기록줄수][최대열수]; uint8_t 모양들[기록줄수][최대열수];
    unsigned 너비,높이,열수,행수,크기바뀜;
    unsigned 살아있음,가로좌표,세로좌표,행위치,열위치,맨위,ingirratilli,전경색,배경색,탈출상태,매개값[4],매개색인,저장행,저장열;
    unsigned 부호없는결과,긴부호없는값,작은값,대체화면,가리개보임;
} 터미널상태;
static 터미널상태 창들[4];
static int 초점=-1,출력결과,agguijjut_atuutilik[4],항목수,Nusuarli_atuutilik=-1,끌기가로,끌기세로;
static unsigned 대기중,단추들,igalaujaq_takussarurli,한글입력;
static const uint32_t 색상들[16]={0x201a15,0x6060df,0x9dcc86,0x80cfea,0xefaf72,0xca96c9,0xceda76,0xede9df,0x858078,0x8888ff,0xb9eba7,0xa5eaff,0xffcc99,0xf0bef1,0xf0f0a0,0xffffff};
extern int 화면보임(int),화면가리킴(int,unsigned,int,int);
extern void 화면다시그림(int);
static 터미널상태 *터미널항목;
static unsigned 넓은글자(unsigned immikkuuqtumut_nalunaikkut){return immikkuuqtumut_nalunaikkut>=256?2:1;}
static void 사각영역(unsigned 가로좌표,unsigned 세로좌표,unsigned 너비값,unsigned 높이값,unsigned 색상){
    보드사각그림(가로좌표,세로좌표,너비값,높이값,색상);
}
void 터미널글자그림(unsigned 가로좌표,unsigned 세로좌표,unsigned immikkuuqtumut_nalunaikkut,unsigned 전경색,unsigned 배경색){
    unsigned 너비=넓은글자(immikkuuqtumut_nalunaikkut)*8;if(immikkuuqtumut_nalunaikkut==0xffffffffu)return;
    int 왼쪽=가로좌표,위쪽=세로좌표,폭=너비,takininga_atuutilik=16;
    if(!보드그림범위(&왼쪽,&위쪽,&폭,&takininga_atuutilik))return;
    if(immikkuuqtumut_nalunaikkut==' '){보드사각그림(왼쪽,위쪽,폭,takininga_atuutilik,배경색);return;}
    unsigned 색인=immikkuuqtumut_nalunaikkut<65536?immikkuuqtumut_nalunaikkut:immikkuuqtumut_nalunaikkut>=0x1f600&&immikkuuqtumut_nalunaikkut<0x1f650?65536+immikkuuqtumut_nalunaikkut-0x1f600:0xfffd;
    const unsigned char *titirausiq_atuutilik=터미널글꼴자료+색인*32;
    for(int titikutaak=위쪽;titikutaak<위쪽+takininga_atuutilik;titikutaak++){unsigned 비트들=titirausiq_atuutilik[(titikutaak-세로좌표)*2]*256+titirausiq_atuutilik[(titikutaak-세로좌표)*2+1];for(int 칸=왼쪽;칸<왼쪽+폭;칸++)보드화소(칸,titikutaak,(비트들&(0x8000>>(칸-가로좌표)))?전경색:배경색);}
}
static void atiq_kipu(unsigned 가로좌표,unsigned 세로좌표,const char *qimiaq_titiqqat,unsigned 전경색,unsigned 배경색){while(*qimiaq_titiqqat){unsigned immikkuuqtumut_nalunaikkut=(unsigned char)*qimiaq_titiqqat++, 남은수=0;if(immikkuuqtumut_nalunaikkut>=0xc0){남은수=immikkuuqtumut_nalunaikkut<0xe0?1:immikkuuqtumut_nalunaikkut<0xf0?2:3;immikkuuqtumut_nalunaikkut&=(1u<<(6-남은수))-1;while(남은수--&&*qimiaq_titiqqat)immikkuuqtumut_nalunaikkut=(immikkuuqtumut_nalunaikkut<<6)|((unsigned char)*qimiaq_titiqqat++&63);}터미널글자그림(가로좌표,세로좌표,immikkuuqtumut_nalunaikkut,전경색,배경색);가로좌표+=넓은글자(immikkuuqtumut_nalunaikkut)*8;}}
static unsigned 첫항목(void){return 터미널항목->맨위;}
static int 보이는지(void){return 터미널항목->살아있음&&초점>=0&&터미널항목==&창들[초점]&&!화면보임(초점);}
static void 그리기(unsigned 행위치,unsigned 열위치){
    if(!보이는지()||행위치<첫항목()-터미널항목->ingirratilli||행위치>=첫항목()-터미널항목->ingirratilli+터미널항목->행수||열위치>=터미널항목->열수)return;
    unsigned immikkuuqtumut_nalunaikkut=터미널항목->글자칸들[행위치%기록줄수][열위치],qimiaq_titiqqat=터미널항목->모양들[행위치%기록줄수][열위치];
    if(넓은글자(immikkuuqtumut_nalunaikkut)==2&&열위치+1>=터미널항목->열수)immikkuuqtumut_nalunaikkut=' ';
    터미널글자그림(터미널항목->가로좌표+12+열위치*8,터미널항목->세로좌표+36+(행위치-첫항목()+터미널항목->ingirratilli)*16,immikkuuqtumut_nalunaikkut?immikkuuqtumut_nalunaikkut:' ',색상들[qimiaq_titiqqat&15],색상들[qimiaq_titiqqat>>4]);
}
static void kukukpaannguaq_atuutilik(int saqqilli_igalaangujaq){if(!보이는지()||터미널항목->ingirratilli||터미널항목->열위치>=터미널항목->열수||터미널항목->행위치<터미널항목->맨위||터미널항목->행위치>=터미널항목->맨위+터미널항목->행수)return;
    if(!saqqilli_igalaangujaq||!터미널항목->가리개보임)그리기(터미널항목->행위치,터미널항목->열위치);else 사각영역(터미널항목->가로좌표+12+터미널항목->열위치*8,터미널항목->세로좌표+36+(터미널항목->행위치-터미널항목->맨위)*16+14,8,2,색상들[터미널항목->전경색]);}
static void Ilulingit_atuutilik(void){
    사각영역(터미널항목->가로좌표+12,터미널항목->세로좌표+36,터미널항목->열수*8,터미널항목->행수*16,색상들[0]);
    int 가로=터미널항목->가로좌표+12,세로=터미널항목->세로좌표+36,폭=터미널항목->열수*8,takininga_atuutilik=터미널항목->행수*16;
    if(보드그림범위(&가로,&세로,&폭,&takininga_atuutilik)){
    unsigned 첫줄=(세로-터미널항목->세로좌표-36)/16,끝줄=(세로+takininga_atuutilik-터미널항목->세로좌표-36+15)/16;
    unsigned 첫칸=(가로-터미널항목->가로좌표-12)/8,끝칸=(가로+폭-터미널항목->가로좌표-12+7)/8;
    if(첫칸)첫칸--; /* 잘림 경계 왼쪽에서 시작한 두 칸 글자도 그린다. */
    for(unsigned 반환값=첫줄;반환값<끝줄;반환값++)for(unsigned immikkuuqtumut_nalunaikkut=첫칸;immikkuuqtumut_nalunaikkut<끝칸;immikkuuqtumut_nalunaikkut++){
        unsigned 행위치=첫항목()-터미널항목->ingirratilli+반환값,immikkuuqtuq_atuutilik=터미널항목->글자칸들[행위치%기록줄수][immikkuuqtumut_nalunaikkut],qimiaq_titiqqat=터미널항목->모양들[행위치%기록줄수][immikkuuqtumut_nalunaikkut];
        if(넓은글자(immikkuuqtuq_atuutilik)==2&&immikkuuqtumut_nalunaikkut+1>=터미널항목->열수)immikkuuqtuq_atuutilik=' ';
        if((immikkuuqtuq_atuutilik==0||immikkuuqtuq_atuutilik==' ')&&(qimiaq_titiqqat>>4)==0)continue;
        터미널글자그림(터미널항목->가로좌표+12+immikkuuqtumut_nalunaikkut*8,터미널항목->세로좌표+36+반환값*16,immikkuuqtuq_atuutilik?immikkuuqtuq_atuutilik:' ',색상들[qimiaq_titiqqat&15],색상들[qimiaq_titiqqat>>4]);
    }}
    atiq_kipu(터미널항목->가로좌표+12,터미널항목->세로좌표+터미널항목->높이-18,터미널항목->ingirratilli?"PgDn: recent output":터미널항목->너비>=500?"F6: next | Corner + left drag: resize":"Corner + left drag: resize",0xece8e2,0x403127);kukukpaannguaq_atuutilik(1);
}
static void 실행틀(int 식별자){
    터미널항목=&창들[식별자];
    int 가로=터미널항목->가로좌표,세로=터미널항목->세로좌표,폭=터미널항목->너비,takininga_atuutilik=터미널항목->높이;
    if(!보드그림범위(&가로,&세로,&폭,&takininga_atuutilik))return;
    사각영역(터미널항목->가로좌표,터미널항목->세로좌표,터미널항목->너비,터미널항목->높이,0x403127);
    unsigned 색상=식별자==초점?0x905020:0x604438;사각영역(터미널항목->가로좌표,터미널항목->세로좌표,터미널항목->너비,30,색상);
    atiq_kipu(터미널항목->가로좌표+12,터미널항목->세로좌표+7,"JKOROS Terminal",0xffffff,색상);
    char 수치[2]={(char)('1'+식별자),0};atiq_kipu(터미널항목->가로좌표+148,터미널항목->세로좌표+7,수치,0xffffff,색상);
    atiq_kipu(터미널항목->가로좌표+240,터미널항목->세로좌표+7,터미널항목->너비>=500?(한글입력?"[IU] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[IU]":"[EN]"),0xffffff,색상);
    사각영역(터미널항목->가로좌표+터미널항목->너비-32,터미널항목->세로좌표+4,26,22,0x5555b8);atiq_kipu(터미널항목->가로좌표+터미널항목->너비-24,터미널항목->세로좌표+7,"X",0xffffff,0x5555b8);
    Ilulingit_atuutilik();
}
static void 장면그리기(void){
    if(!igalaujaq_takussarurli)return;사각영역(0,0,보드화면너비(),보드화면높이(),0x302018);사각영역(0,0,보드화면너비(),32,0x403127);
    사각영역(6,4,136,24,0x905020);atiq_kipu(14,8,"+ New terminal",0xffffff,0x905020);
    for(int 순번=0;순번<4;순번++)if(창들[순번].살아있음){unsigned immikkuuqtumut_nalunaikkut=초점==순번?0x905020:0x604438;사각영역(154+순번*112,4,106,24,immikkuuqtumut_nalunaikkut);atiq_kipu(160+순번*112,8,"Terminal",0xffffff,immikkuuqtumut_nalunaikkut);char qimiaq_titiqqat[2]={(char)('1'+순번),0};atiq_kipu(232+순번*112,8,qimiaq_titiqqat,0xffffff,immikkuuqtumut_nalunaikkut);}
    if(!항목수)atiq_kipu(140,210,"Click + New terminal to start",0xede9df,0x302018);
    for(int 순번=0;순번<항목수;순번++)실행틀(agguijjut_atuutilik[순번]);화면다시그림(초점);터미널항목=&창들[출력결과];
}
static void 영역그리기(int 가로,int 세로,int 폭,int takininga_atuutilik){
    if(!igalaujaq_takussarurli||!보드그림범위(&가로,&세로,&폭,&takininga_atuutilik))return;
    for(int titikutaak=세로;titikutaak<세로+takininga_atuutilik;titikutaak+=32){
        int 띠높이=세로+takininga_atuutilik-titikutaak;if(띠높이>32)띠높이=32;
        if(보드그림시작(가로,titikutaak,폭,띠높이)){장면그리기();보드그림마침();}
    }
}
static void 다시그리기(void){영역그리기(0,0,보드화면너비(),보드화면높이());}
/* 서로 겹치지 않는 새 igalaangujaq 영역과 이전 자리의 네 띠를 복구한다. */
static void 창자리그리기(int 가로,int 세로,int 폭,int takininga_atuutilik,터미널상태 *igalaangujaq){
    int 왼쪽=가로>(int)igalaangujaq->가로좌표?가로:(int)igalaangujaq->가로좌표;
    int 위쪽=세로>(int)igalaangujaq->세로좌표?세로:(int)igalaangujaq->세로좌표;
    int 오른쪽=가로+폭<(int)(igalaangujaq->가로좌표+igalaangujaq->너비)?가로+폭:(int)(igalaangujaq->가로좌표+igalaangujaq->너비);
    int 아래쪽=세로+takininga_atuutilik<(int)(igalaangujaq->세로좌표+igalaangujaq->높이)?세로+takininga_atuutilik:(int)(igalaangujaq->세로좌표+igalaangujaq->높이);
    영역그리기(igalaangujaq->가로좌표,igalaangujaq->세로좌표,igalaangujaq->너비,igalaangujaq->높이);
    if(왼쪽>=오른쪽||위쪽>=아래쪽){영역그리기(가로,세로,폭,takininga_atuutilik);return;}
    영역그리기(가로,세로,폭,위쪽-세로);
    영역그리기(가로,아래쪽,폭,세로+takininga_atuutilik-아래쪽);
    영역그리기(가로,위쪽,왼쪽-가로,아래쪽-위쪽);
    영역그리기(오른쪽,위쪽,가로+폭-오른쪽,아래쪽-위쪽);
}
static void 초점알리기(void){대기중=(대기중&~15u)|(unsigned)(초점+1)|0x10000;}
void 터미널입력방식(unsigned 한글여부){
    한글입력=한글여부!=0;
    /* Update title bars only: a mode switch must not erase an EL0 drawing. */
    if(초점>=0){
        터미널상태 *igalaangujaq_Iliniku=&창들[초점];
        atiq_kipu(igalaangujaq_Iliniku->가로좌표+240,igalaangujaq_Iliniku->세로좌표+7,igalaangujaq_Iliniku->너비>=500?(한글입력?"[IU] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[IU]":"[EN]"),0xffffff,0x905020);
    }
}
static void 앞으로올리기(int 식별자){if(식별자<0||식별자>=4||!창들[식별자].살아있음)return;int 현재위치=0;while(현재위치<항목수&&agguijjut_atuutilik[현재위치]!=식별자)현재위치++;for(;현재위치+1<항목수;현재위치++)agguijjut_atuutilik[현재위치]=agguijjut_atuutilik[현재위치+1];agguijjut_atuutilik[항목수-1]=식별자;초점=식별자;초점알리기();다시그리기();}
static void 빈칸채우기(unsigned 행위치){for(unsigned immikkuuqtumut_nalunaikkut=0;immikkuuqtumut_nalunaikkut<최대열수;immikkuuqtumut_nalunaikkut++){터미널항목->글자칸들[행위치%기록줄수][immikkuuqtumut_nalunaikkut]=0;터미널항목->모양들[행위치%기록줄수][immikkuuqtumut_nalunaikkut]=터미널항목->전경색|(터미널항목->배경색<<4);}}
static void piijarli_TOC(void){터미널항목->행위치=터미널항목->열위치=터미널항목->맨위=터미널항목->ingirratilli=0;for(unsigned 반환값=0;반환값<기록줄수;반환값++)빈칸채우기(반환값);if(보이는지())Ilulingit_atuutilik();}
static int 만들기(void){
    if(!보드화면기억공간())return -19;int 식별자=0;while(식별자<4&&창들[식별자].살아있음)식별자++;if(식별자==4)return -28;
    igalaujaq_takussarurli=1;터미널항목=&창들[식별자];memset(터미널항목,0,sizeof(*터미널항목));터미널항목->살아있음=1;터미널항목->너비=568;터미널항목->높이=360;터미널항목->열수=68;터미널항목->행수=19;터미널항목->가로좌표=12+식별자*16;터미널항목->세로좌표=48+식별자*18;터미널항목->전경색=7;터미널항목->가리개보임=1;
    for(unsigned 반환값=0;반환값<기록줄수;반환값++)빈칸채우기(반환값);agguijjut_atuutilik[항목수++]=식별자;초점=식별자;대기중|=1u<<(4+식별자);초점알리기();다시그리기();return 식별자+1;
}
static void matuli_igalaangujaq(int 식별자){
    if(식별자<0||식별자>=4||!창들[식별자].살아있음)return;창들[식별자].살아있음=0;대기중|=1u<<(8+식별자);
    int 현재위치=0;while(현재위치<항목수&&agguijjut_atuutilik[현재위치]!=식별자)현재위치++;for(;현재위치+1<항목수;현재위치++)agguijjut_atuutilik[현재위치]=agguijjut_atuutilik[현재위치+1];항목수--;
    if(초점==식별자)초점=항목수?agguijjut_atuutilik[항목수-1]:-1;초점알리기();다시그리기();
}
static void 줄바꿈(void){터미널항목->열위치=0;터미널항목->행위치++;if(터미널항목->행위치>=터미널항목->맨위+터미널항목->행수){터미널항목->맨위++;빈칸채우기(터미널항목->행위치);if(보이는지())Ilulingit_atuutilik();}}
static void immikkuuqtumut_nalunaikkut_451f2815(unsigned immikkuuqtumut_nalunaikkut){
    if(immikkuuqtumut_nalunaikkut==13){터미널항목->열위치=0;return;}if(immikkuuqtumut_nalunaikkut==10){줄바꿈();return;}if(immikkuuqtumut_nalunaikkut==8){if(터미널항목->열위치)터미널항목->열위치--;return;}
    if(immikkuuqtumut_nalunaikkut==9){unsigned 개수=8-터미널항목->열위치%8;while(개수--)immikkuuqtumut_nalunaikkut_451f2815(' ');return;}if(immikkuuqtumut_nalunaikkut<32||immikkuuqtumut_nalunaikkut==127)return;
    unsigned 너비값=넓은글자(immikkuuqtumut_nalunaikkut);if(터미널항목->열위치+너비값>터미널항목->열수)줄바꿈();
    if(터미널항목->글자칸들[터미널항목->행위치%기록줄수][터미널항목->열위치]==0xffffffffu&&터미널항목->열위치){터미널항목->글자칸들[터미널항목->행위치%기록줄수][터미널항목->열위치-1]=' ';그리기(터미널항목->행위치,터미널항목->열위치-1);}
    if(넓은글자(터미널항목->글자칸들[터미널항목->행위치%기록줄수][터미널항목->열위치])==2&&터미널항목->열위치+1<터미널항목->열수){터미널항목->글자칸들[터미널항목->행위치%기록줄수][터미널항목->열위치+1]=' ';그리기(터미널항목->행위치,터미널항목->열위치+1);}
    터미널항목->글자칸들[터미널항목->행위치%기록줄수][터미널항목->열위치]=immikkuuqtumut_nalunaikkut;터미널항목->모양들[터미널항목->행위치%기록줄수][터미널항목->열위치]=터미널항목->전경색|(터미널항목->배경색<<4);
    if(너비값==2)터미널항목->글자칸들[터미널항목->행위치%기록줄수][터미널항목->열위치+1]=0xffffffffu;
    그리기(터미널항목->행위치,터미널항목->열위치);터미널항목->열위치+=너비값;
}
static void 제어열처리(unsigned immikkuuqtumut_nalunaikkut){
    unsigned 개수=터미널항목->매개값[0]?터미널항목->매개값[0]:1;
    if(immikkuuqtumut_nalunaikkut=='m')for(unsigned 순번=0;순번<=터미널항목->매개색인;순번++){unsigned 자료위치=터미널항목->매개값[순번];if(!자료위치){터미널항목->전경색=7;터미널항목->배경색=0;}if(자료위치==1&&터미널항목->전경색<8)터미널항목->전경색+=8;if(자료위치==7){unsigned 유지=터미널항목->전경색;터미널항목->전경색=터미널항목->배경색;터미널항목->배경색=유지;}if(자료위치>=30&&자료위치<=37)터미널항목->전경색=자료위치-30;if(자료위치>=90&&자료위치<=97)터미널항목->전경색=자료위치-90+8;if(자료위치>=40&&자료위치<=47)터미널항목->배경색=자료위치-40;if(자료위치>=100&&자료위치<=107)터미널항목->배경색=자료위치-100+8;if(자료위치==39)터미널항목->전경색=7;if(자료위치==49)터미널항목->배경색=0;}
    if(immikkuuqtumut_nalunaikkut=='J'&&(터미널항목->매개값[0]==2||터미널항목->매개값[0]==3))piijarli_TOC();
    if(immikkuuqtumut_nalunaikkut=='K'){unsigned 출발위치=터미널항목->매개값[0]==2?0:터미널항목->열위치,도착위치=터미널항목->매개값[0]==1?터미널항목->열위치+1:터미널항목->열수;if(터미널항목->매개값[0]==1)출발위치=0;for(unsigned 순번=출발위치;순번<도착위치&&순번<터미널항목->열수;순번++){
        unsigned sanimukutaak_atuutilik=터미널항목->행위치%기록줄수,immikkuuqtuq_atuutilik=터미널항목->글자칸들[sanimukutaak_atuutilik][순번],kittuaq_atuutilik=터미널항목->전경색|(터미널항목->배경색<<4);
        /* 넓은 vi 화면에서도 이미 빈 칸의 titirausiq_atuutilik 화소를 되풀이해 칠하지 않는다. */
        int 바뀜=(immikkuuqtuq_atuutilik!=0&&immikkuuqtuq_atuutilik!=' ')||터미널항목->모양들[sanimukutaak_atuutilik][순번]!=kittuaq_atuutilik;
        터미널항목->글자칸들[sanimukutaak_atuutilik][순번]=' ';터미널항목->모양들[sanimukutaak_atuutilik][순번]=kittuaq_atuutilik;
        if(바뀜)그리기(터미널항목->행위치,순번);
    }}
    if(immikkuuqtumut_nalunaikkut=='D')터미널항목->열위치=개수>터미널항목->열위치?0:터미널항목->열위치-개수;if(immikkuuqtumut_nalunaikkut=='C')터미널항목->열위치=터미널항목->열위치+개수>=터미널항목->열수?터미널항목->열수-1:터미널항목->열위치+개수;
    if(immikkuuqtumut_nalunaikkut=='G')터미널항목->열위치=개수>터미널항목->열수?터미널항목->열수-1:개수-1;if(immikkuuqtumut_nalunaikkut=='A')터미널항목->행위치=개수>터미널항목->행위치-터미널항목->맨위?터미널항목->맨위:터미널항목->행위치-개수;
    if(immikkuuqtumut_nalunaikkut=='B')터미널항목->행위치=터미널항목->행위치+개수>=터미널항목->맨위+터미널항목->행수?터미널항목->맨위+터미널항목->행수-1:터미널항목->행위치+개수;
    if(immikkuuqtumut_nalunaikkut=='H'||immikkuuqtumut_nalunaikkut=='f'){터미널항목->행위치=터미널항목->맨위+(개수>터미널항목->행수?터미널항목->행수:개수)-1;unsigned 가로좌표=터미널항목->매개값[1]?터미널항목->매개값[1]:1;터미널항목->열위치=(가로좌표>터미널항목->열수?터미널항목->열수:가로좌표)-1;}
    if(immikkuuqtumut_nalunaikkut=='s'){터미널항목->저장행=터미널항목->행위치;터미널항목->저장열=터미널항목->열위치;}if(immikkuuqtumut_nalunaikkut=='u'){터미널항목->행위치=터미널항목->저장행;터미널항목->열위치=터미널항목->저장열<터미널항목->열수?터미널항목->저장열:터미널항목->열수-1;}
    if((immikkuuqtumut_nalunaikkut=='h'||immikkuuqtumut_nalunaikkut=='l')&&터미널항목->매개값[0]==25)터미널항목->가리개보임=immikkuuqtumut_nalunaikkut=='h';
}
void 터미널바이트(unsigned 둘째값){
    터미널항목=&창들[출력결과];if(!터미널항목->살아있음)return;kukukpaannguaq_atuutilik(0);if(터미널항목->ingirratilli){터미널항목->ingirratilli=0;if(보이는지())Ilulingit_atuutilik();}
    if(터미널항목->탈출상태==1){터미널항목->탈출상태=둘째값=='['?2:0;터미널항목->매개색인=0;for(unsigned 순번=0;순번<4;순번++)터미널항목->매개값[순번]=0;}
    else if(터미널항목->탈출상태==2){if(둘째값=='?'){}else if(둘째값>='0'&&둘째값<='9'){if(터미널항목->매개값[터미널항목->매개색인]<10000)터미널항목->매개값[터미널항목->매개색인]=터미널항목->매개값[터미널항목->매개색인]*10+둘째값-'0';}else if(둘째값==';'&&터미널항목->매개색인<3)터미널항목->매개색인++;else{제어열처리(둘째값);터미널항목->탈출상태=0;}}
    else if(둘째값==27){터미널항목->긴부호없는값=0;터미널항목->탈출상태=1;}else{
        if(터미널항목->긴부호없는값&&(둘째값&0xc0)!=0x80){터미널항목->긴부호없는값=0;immikkuuqtumut_nalunaikkut_451f2815(0xfffd);}
        if(터미널항목->긴부호없는값){터미널항목->부호없는결과=터미널항목->부호없는결과*64+(둘째값&63);if(--터미널항목->긴부호없는값==0)immikkuuqtumut_nalunaikkut_451f2815(터미널항목->부호없는결과<터미널항목->작은값||터미널항목->부호없는결과>0x10ffff||(터미널항목->부호없는결과>=0xd800&&터미널항목->부호없는결과<=0xdfff)?0xfffd:터미널항목->부호없는결과);}
        else if(둘째값<128)immikkuuqtumut_nalunaikkut_451f2815(둘째값);else if(둘째값>=0xc2&&둘째값<=0xf4){터미널항목->긴부호없는값=둘째값<0xe0?1:둘째값<0xf0?2:3;터미널항목->부호없는결과=둘째값&((1u<<(6-터미널항목->긴부호없는값))-1);터미널항목->작은값=터미널항목->긴부호없는값==1?128:터미널항목->긴부호없는값==2?2048:65536;}else immikkuuqtumut_nalunaikkut_451f2815(0xfffd);
    }kukukpaannguaq_atuutilik(1);
}
int 터미널대기(void){return 대기중!=0;}
/* 모서리 nalunaiqsimavik: 1 좌상, 2 우상, 3 좌하, 4 우하. */
static int anginga_aaqqigiarli_Nusuarli=-1,잡은모서리,잡은가로,잡은세로,처음가로,처음세로,처음너비,처음높이;
static int 가리킨창(int 가로,int 세로) {
    for(int 차례=항목수-1;차례>=0;차례--){
        int 식별자=agguijjut_atuutilik[차례];터미널상태 *igalaangujaq=&창들[식별자];
        if(가로>=(int)igalaangujaq->가로좌표&&세로>=(int)igalaangujaq->세로좌표&&
           가로<(int)(igalaangujaq->가로좌표+igalaangujaq->너비)&&세로<(int)(igalaangujaq->세로좌표+igalaangujaq->높이))return 식별자;
    }return -1;
}
static int 모서리찾기(int 식별자,int 가로,int 세로) {
    if(식별자<0)return 0;터미널상태 *igalaangujaq=&창들[식별자];
    int 왼쪽=가로<(int)igalaangujaq->가로좌표+8,오른쪽=가로>=(int)(igalaangujaq->가로좌표+igalaangujaq->너비)-8;
    int 위쪽=세로<(int)igalaangujaq->세로좌표+8,아래쪽=세로>=(int)(igalaangujaq->세로좌표+igalaangujaq->높이)-8;
    return (왼쪽||오른쪽)&&(위쪽||아래쪽)?1+오른쪽+아래쪽*2:0;
}
static int 사이값(int atuutilik,int 최소,int 최대){return atuutilik<최소?최소:atuutilik>최대?최대:atuutilik;}
static void nuulli_anginga_aaqqigiarli(int 가로,int 세로) {
    터미널상태 *igalaangujaq=&창들[anginga_aaqqigiarli_Nusuarli];int 왼쪽=처음가로,위쪽=처음세로,오른쪽=처음가로+처음너비,아래쪽=처음세로+처음높이;
    if(잡은모서리==1||잡은모서리==3)왼쪽=사이값(처음가로+가로-잡은가로,0,오른쪽-360);
    else 오른쪽=사이값(처음가로+처음너비+가로-잡은가로,왼쪽+360,보드화면너비());
    if(잡은모서리<=2)위쪽=사이값(처음세로+세로-잡은세로,34,아래쪽-216);
    else 아래쪽=사이값(처음세로+처음높이+세로-잡은세로,위쪽+216,보드화면높이());
    unsigned 열수=(오른쪽-왼쪽-24)/8,행수=(아래쪽-위쪽-56)/16;
    if(igalaangujaq->열수!=열수||igalaangujaq->행수!=행수){
        igalaangujaq->크기바뀜=1;igalaangujaq->열수=열수;igalaangujaq->행수=행수;
        if(igalaangujaq->열위치>=열수)igalaangujaq->열위치=열수-1;
        if(igalaangujaq->행위치>=igalaangujaq->맨위+행수)igalaangujaq->맨위=igalaangujaq->행위치-행수+1;
        unsigned 한도=igalaangujaq->맨위;if(한도>기록줄수-행수)한도=기록줄수-행수;
        if(igalaangujaq->ingirratilli>한도)igalaangujaq->ingirratilli=한도;
    }
    int 옛가로=igalaangujaq->가로좌표,옛세로=igalaangujaq->세로좌표,옛폭=igalaangujaq->너비,옛길이=igalaangujaq->높이;
    if(옛가로==왼쪽&&옛세로==위쪽&&옛폭==오른쪽-왼쪽&&옛길이==아래쪽-위쪽)return;
    igalaangujaq->가로좌표=왼쪽;igalaangujaq->세로좌표=위쪽;igalaangujaq->너비=오른쪽-왼쪽;igalaangujaq->높이=아래쪽-위쪽;
    창자리그리기(옛가로,옛세로,옛폭,옛길이,igalaangujaq);
}
void 터미널가리킴(unsigned 다음,int 가로좌표,int 세로좌표){
    unsigned 눌림=다음&~단추들;단추들=다음;
    if(!igalaujaq_takussarurli){Nusuarli_atuutilik=-1;anginga_aaqqigiarli_Nusuarli=-1;보드포인터(가로좌표,세로좌표,1);return;}
    if(!(다음&1)){Nusuarli_atuutilik=-1;anginga_aaqqigiarli_Nusuarli=-1;}
    if(anginga_aaqqigiarli_Nusuarli>=0&&!창들[anginga_aaqqigiarli_Nusuarli].살아있음)anginga_aaqqigiarli_Nusuarli=-1;
    if(Nusuarli_atuutilik>=0&&!창들[Nusuarli_atuutilik].살아있음)Nusuarli_atuutilik=-1;
    if(anginga_aaqqigiarli_Nusuarli>=0){
        nuulli_anginga_aaqqigiarli(가로좌표,세로좌표);보드포인터(가로좌표,세로좌표,잡은모서리==1||잡은모서리==4?2:3);return;
    }
    보드포인터(가로좌표,세로좌표,1);
    if(Nusuarli_atuutilik>=0){
        터미널상태 *igalaangujaq=&창들[Nusuarli_atuutilik];
        int 옛가로=igalaangujaq->가로좌표,옛세로=igalaangujaq->세로좌표;
        igalaangujaq->가로좌표=사이값(가로좌표-끌기가로,0,보드화면너비()-igalaangujaq->너비);
        igalaangujaq->세로좌표=사이값(세로좌표-끌기세로,34,보드화면높이()-igalaangujaq->높이);
        if(옛가로!=(int)igalaangujaq->가로좌표||옛세로!=(int)igalaangujaq->세로좌표)창자리그리기(옛가로,옛세로,igalaangujaq->너비,igalaangujaq->높이,igalaangujaq);
        return;
    }
    extern int 화면덮음(int,int,int);
    if(화면덮음(초점,가로좌표,세로좌표)){화면가리킴(초점,눌림,가로좌표,세로좌표);return;}
    int 식별자=가리킨창(가로좌표,세로좌표),모서리=모서리찾기(식별자,가로좌표,세로좌표);
    if(모서리)보드포인터(가로좌표,세로좌표,모서리==1||모서리==4?2:3);
    if(눌림&1){
        if(모서리){
            터미널상태 *igalaangujaq=&창들[식별자];anginga_aaqqigiarli_Nusuarli=식별자;잡은모서리=모서리;잡은가로=가로좌표;잡은세로=세로좌표;
            처음가로=igalaangujaq->가로좌표;처음세로=igalaangujaq->세로좌표;처음너비=igalaangujaq->너비;처음높이=igalaangujaq->높이;
            if(식별자!=초점)앞으로올리기(식별자);return;
        }
        if(세로좌표<32&&가로좌표>=6&&가로좌표<142){만들기();return;}
        if(세로좌표<32&&가로좌표>=154&&가로좌표<602){앞으로올리기((가로좌표-154)/112);return;}
        if(식별자>=0){
            터미널상태 *igalaangujaq=&창들[식별자];
            if(세로좌표<(int)igalaangujaq->세로좌표+30&&가로좌표>=(int)(igalaangujaq->가로좌표+igalaangujaq->너비)-32){matuli_igalaangujaq(식별자);return;}
            if(식별자!=초점)앞으로올리기(식별자);
            if(세로좌표<(int)igalaangujaq->세로좌표+30){Nusuarli_atuutilik=식별자;끌기가로=가로좌표-igalaangujaq->가로좌표;끌기세로=세로좌표-igalaangujaq->세로좌표;}return;
        }
    }
    if(초점>=0&&(눌림&(8|16))){터미널항목=&창들[초점];if(눌림&8){unsigned 한도=터미널항목->맨위;if(한도>기록줄수-터미널항목->행수)한도=기록줄수-터미널항목->행수;터미널항목->ingirratilli=터미널항목->ingirratilli+9>한도?한도:터미널항목->ingirratilli+9;}else 터미널항목->ingirratilli=터미널항목->ingirratilli<9?0:터미널항목->ingirratilli-9;다시그리기();}
}
void 터미널바로가기키(unsigned 누름값){if(누름값==1)만들기();if(누름값==2&&항목수)앞으로올리기(agguijjut_atuutilik[0]);if(누름값==3)matuli_igalaangujaq(초점);}
기계낱말 보드터미널(기계낱말 sugiarut){
    if(sugiarut==300){if(!창들[출력결과].살아있음)return 만들기();igalaujaq_takussarurli=1;다시그리기();return 0;}
    if(sugiarut==0){matuli_igalaangujaq(초점);return 0;}if(sugiarut==1)return (uint32_t)만들기();if(sugiarut==2)return 초점>=0;
    if(sugiarut==9){igalaujaq_takussarurli=0;return 0;}if(sugiarut==7)return 항목수;if(sugiarut==10)return 초점+1;if(sugiarut==11)return 출력결과;
    if(sugiarut==13){터미널상태 *igalaangujaq=&창들[출력결과];return igalaangujaq->살아있음?(igalaangujaq->행수<<16)|igalaangujaq->열수:(19<<16)|68;}
    if(sugiarut==14){unsigned atuutilik=창들[출력결과].크기바뀜;창들[출력결과].크기바뀜=0;return atuutilik;}
    if(sugiarut==12){unsigned atuutilik=대기중;대기중=0;return atuutilik;}
    if(sugiarut>=20&&sugiarut<24)return 창들[sugiarut-20].살아있음;
    if(sugiarut>=100&&sugiarut<104){출력결과=sugiarut-100;터미널항목=&창들[출력결과];return 0;}
    if(sugiarut>=200&&sugiarut<204){앞으로올리기(sugiarut-200);return 0;}
    if(sugiarut==3){다시그리기();return 0;}터미널항목=&창들[출력결과];if(!터미널항목->살아있음)return 0;
    if(sugiarut==4)piijarli_TOC();if(sugiarut==5||sugiarut==6){unsigned 이전=단추들;터미널가리킴(sugiarut==5?8:16,0,0);단추들=이전;}return 1;
}
