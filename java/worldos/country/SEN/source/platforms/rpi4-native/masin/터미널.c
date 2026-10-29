#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* 자체 네 palanteer 합성과 UTF-8 터미널. 바뀐 영역의 완성 그림만 표시한다. */
#include <stdint.h>
#include <stddef.h>
typedef uintptr_t masin_Word;
extern masin_Word 보드화소(masin_Word,masin_Word,masin_Word),보드화면기억공간(void);
extern void *memset(void *,int,size_t);
extern const unsigned char 터미널글꼴자료[];
#define 최대열수 237
#define 기록줄수 160
typedef struct {
    uint32_t 글자칸들[기록줄수][최대열수]; uint8_t 모양들[기록줄수][최대열수];
    unsigned 너비,높이,열수,행수,크기바뀜;
    unsigned 살아있음,rëddu_iks_yi,세로좌표,행위치,열위치,맨위,Xélal,전경색,배경색,탈출상태,매개값[4],매개색인,저장행,저장열;
    unsigned 부호없는결과,긴부호없는값,작은값,대체화면,가리개보임;
} 터미널상태;
static 터미널상태 창들[4];
static int Fës=-1,출력결과,toftale_xëyma[4],항목수,randal_xëyma=-1,끌기가로,끌기세로;
static unsigned 대기중,단추들,Biro_wonin,한글입력;
static const uint32_t 색상들[16]={0x201a15,0x6060df,0x9dcc86,0x80cfea,0xefaf72,0xca96c9,0xceda76,0xede9df,0x858078,0x8888ff,0xb9eba7,0xa5eaff,0xffcc99,0xf0bef1,0xf0f0a0,0xffffff};
extern int 화면보임(int),화면가리킴(int,unsigned,int,int);
extern void 화면다시그림(int);
static 터미널상태 *터미널항목;
static unsigned 넓은글자(unsigned kotu_araf){return kotu_araf>=256?2:1;}
static void 사각영역(unsigned rëddu_iks_yi,unsigned 세로좌표,unsigned 너비값,unsigned 높이값,unsigned 색상){
    보드사각그림(rëddu_iks_yi,세로좌표,너비값,높이값,색상);
}
void 터미널글자그림(unsigned rëddu_iks_yi,unsigned 세로좌표,unsigned kotu_araf,unsigned 전경색,unsigned 배경색){
    unsigned 너비=넓은글자(kotu_araf)*8;if(kotu_araf==0xffffffffu)return;
    int 왼쪽=rëddu_iks_yi,위쪽=세로좌표,폭=너비,diir_xëyma=16;
    if(!보드그림범위(&왼쪽,&위쪽,&폭,&diir_xëyma))return;
    if(kotu_araf==' '){보드사각그림(왼쪽,위쪽,폭,diir_xëyma,배경색);return;}
    unsigned 색인=kotu_araf<65536?kotu_araf:kotu_araf>=0x1f600&&kotu_araf<0x1f650?65536+kotu_araf-0x1f600:0xfffd;
    const unsigned char *mbindin_xëyma=터미널글꼴자료+색인*32;
    for(int buum=위쪽;buum<위쪽+diir_xëyma;buum++){unsigned 비트들=mbindin_xëyma[(buum-세로좌표)*2]*256+mbindin_xëyma[(buum-세로좌표)*2+1];for(int xar_xar_dugal_xabaar=왼쪽;xar_xar_dugal_xabaar<왼쪽+폭;xar_xar_dugal_xabaar++)보드화소(xar_xar_dugal_xabaar,buum,(비트들&(0x8000>>(xar_xar_dugal_xabaar-rëddu_iks_yi)))?전경색:배경색);}
}
static void tur_àlluwa(unsigned rëddu_iks_yi,unsigned 세로좌표,const char *araf_yu_bennoo_mbir,unsigned 전경색,unsigned 배경색){while(*araf_yu_bennoo_mbir){unsigned kotu_araf=(unsigned char)*araf_yu_bennoo_mbir++, 남은수=0;if(kotu_araf>=0xc0){남은수=kotu_araf<0xe0?1:kotu_araf<0xf0?2:3;kotu_araf&=(1u<<(6-남은수))-1;while(남은수--&&*araf_yu_bennoo_mbir)kotu_araf=(kotu_araf<<6)|((unsigned char)*araf_yu_bennoo_mbir++&63);}터미널글자그림(rëddu_iks_yi,세로좌표,kotu_araf,전경색,배경색);rëddu_iks_yi+=넓은글자(kotu_araf)*8;}}
static unsigned 첫항목(void){return 터미널항목->맨위;}
static int 보이는지(void){return 터미널항목->살아있음&&Fës>=0&&터미널항목==&창들[Fës]&&!화면보임(Fës);}
static void 그리기(unsigned 행위치,unsigned 열위치){
    if(!보이는지()||행위치<첫항목()-터미널항목->Xélal||행위치>=첫항목()-터미널항목->Xélal+터미널항목->행수||열위치>=터미널항목->열수)return;
    unsigned kotu_araf=터미널항목->글자칸들[행위치%기록줄수][열위치],araf_yu_bennoo_mbir=터미널항목->모양들[행위치%기록줄수][열위치];
    if(넓은글자(kotu_araf)==2&&열위치+1>=터미널항목->열수)kotu_araf=' ';
    터미널글자그림(터미널항목->rëddu_iks_yi+12+열위치*8,터미널항목->세로좌표+36+(행위치-첫항목()+터미널항목->Xélal)*16,kotu_araf?kotu_araf:' ',색상들[araf_yu_bennoo_mbir&15],색상들[araf_yu_bennoo_mbir>>4]);
}
static void kaare_xëyma(int féeñal_palanteer){if(!보이는지()||터미널항목->Xélal||터미널항목->열위치>=터미널항목->열수||터미널항목->행위치<터미널항목->맨위||터미널항목->행위치>=터미널항목->맨위+터미널항목->행수)return;
    if(!féeñal_palanteer||!터미널항목->가리개보임)그리기(터미널항목->행위치,터미널항목->열위치);else 사각영역(터미널항목->rëddu_iks_yi+12+터미널항목->열위치*8,터미널항목->세로좌표+36+(터미널항목->행위치-터미널항목->맨위)*16+14,8,2,색상들[터미널항목->전경색]);}
static void Këmb_xëyma(void){
    사각영역(터미널항목->rëddu_iks_yi+12,터미널항목->세로좌표+36,터미널항목->열수*8,터미널항목->행수*16,색상들[0]);
    int 가로=터미널항목->rëddu_iks_yi+12,세로=터미널항목->세로좌표+36,폭=터미널항목->열수*8,diir_xëyma=터미널항목->행수*16;
    if(보드그림범위(&가로,&세로,&폭,&diir_xëyma)){
    unsigned 첫줄=(세로-터미널항목->세로좌표-36)/16,끝줄=(세로+diir_xëyma-터미널항목->세로좌표-36+15)/16;
    unsigned 첫칸=(가로-터미널항목->rëddu_iks_yi-12)/8,끝칸=(가로+폭-터미널항목->rëddu_iks_yi-12+7)/8;
    if(첫칸)첫칸--; /* 잘림 경계 왼쪽에서 시작한 두 xar_xar_dugal_xabaar 글자도 그린다. */
    for(unsigned 반환값=첫줄;반환값<끝줄;반환값++)for(unsigned kotu_araf=첫칸;kotu_araf<끝칸;kotu_araf++){
        unsigned 행위치=첫항목()-터미널항목->Xélal+반환값,Araf_xëyma=터미널항목->글자칸들[행위치%기록줄수][kotu_araf],araf_yu_bennoo_mbir=터미널항목->모양들[행위치%기록줄수][kotu_araf];
        if(넓은글자(Araf_xëyma)==2&&kotu_araf+1>=터미널항목->열수)Araf_xëyma=' ';
        if((Araf_xëyma==0||Araf_xëyma==' ')&&(araf_yu_bennoo_mbir>>4)==0)continue;
        터미널글자그림(터미널항목->rëddu_iks_yi+12+kotu_araf*8,터미널항목->세로좌표+36+반환값*16,Araf_xëyma?Araf_xëyma:' ',색상들[araf_yu_bennoo_mbir&15],색상들[araf_yu_bennoo_mbir>>4]);
    }}
    tur_àlluwa(터미널항목->rëddu_iks_yi+12,터미널항목->세로좌표+터미널항목->높이-18,터미널항목->Xélal?"PgDn: recent output":터미널항목->너비>=500?"F6: next | Corner + left drag: resize":"Corner + left drag: resize",0xece8e2,0x403127);kaare_xëyma(1);
}
static void 실행틀(int raññeekaay_xëyma){
    터미널항목=&창들[raññeekaay_xëyma];
    int 가로=터미널항목->rëddu_iks_yi,세로=터미널항목->세로좌표,폭=터미널항목->너비,diir_xëyma=터미널항목->높이;
    if(!보드그림범위(&가로,&세로,&폭,&diir_xëyma))return;
    사각영역(터미널항목->rëddu_iks_yi,터미널항목->세로좌표,터미널항목->너비,터미널항목->높이,0x403127);
    unsigned 색상=raññeekaay_xëyma==Fës?0x905020:0x604438;사각영역(터미널항목->rëddu_iks_yi,터미널항목->세로좌표,터미널항목->너비,30,색상);
    tur_àlluwa(터미널항목->rëddu_iks_yi+12,터미널항목->세로좌표+7,"JKOROS Terminal",0xffffff,색상);
    char 수치[2]={(char)('1'+raññeekaay_xëyma),0};tur_àlluwa(터미널항목->rëddu_iks_yi+148,터미널항목->세로좌표+7,수치,0xffffff,색상);
    tur_àlluwa(터미널항목->rëddu_iks_yi+240,터미널항목->세로좌표+7,터미널항목->너비>=500?(한글입력?"[WO] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[WO]":"[EN]"),0xffffff,색상);
    사각영역(터미널항목->rëddu_iks_yi+터미널항목->너비-32,터미널항목->세로좌표+4,26,22,0x5555b8);tur_àlluwa(터미널항목->rëddu_iks_yi+터미널항목->너비-24,터미널항목->세로좌표+7,"X",0xffffff,0x5555b8);
    Këmb_xëyma();
}
static void 장면그리기(void){
    if(!Biro_wonin)return;사각영역(0,0,보드화면너비(),보드화면높이(),0x302018);사각영역(0,0,보드화면너비(),32,0x403127);
    사각영역(6,4,136,24,0x905020);tur_àlluwa(14,8,"+ New terminal",0xffffff,0x905020);
    for(int 순번=0;순번<4;순번++)if(창들[순번].살아있음){unsigned kotu_araf=Fës==순번?0x905020:0x604438;사각영역(154+순번*112,4,106,24,kotu_araf);tur_àlluwa(160+순번*112,8,"Terminal",0xffffff,kotu_araf);char araf_yu_bennoo_mbir[2]={(char)('1'+순번),0};tur_àlluwa(232+순번*112,8,araf_yu_bennoo_mbir,0xffffff,kotu_araf);}
    if(!항목수)tur_àlluwa(140,210,"Click + New terminal to start",0xede9df,0x302018);
    for(int 순번=0;순번<항목수;순번++)실행틀(toftale_xëyma[순번]);화면다시그림(Fës);터미널항목=&창들[출력결과];
}
static void 영역그리기(int 가로,int 세로,int 폭,int diir_xëyma){
    if(!Biro_wonin||!보드그림범위(&가로,&세로,&폭,&diir_xëyma))return;
    for(int buum=세로;buum<세로+diir_xëyma;buum+=32){
        int 띠높이=세로+diir_xëyma-buum;if(띠높이>32)띠높이=32;
        if(보드그림시작(가로,buum,폭,띠높이)){장면그리기();보드그림마침();}
    }
}
static void 다시그리기(void){영역그리기(0,0,보드화면너비(),보드화면높이());}
/* 서로 겹치지 않는 새 palanteer 영역과 이전 자리의 네 띠를 복구한다. */
static void 창자리그리기(int 가로,int 세로,int 폭,int diir_xëyma,터미널상태 *palanteer){
    int 왼쪽=가로>(int)palanteer->rëddu_iks_yi?가로:(int)palanteer->rëddu_iks_yi;
    int 위쪽=세로>(int)palanteer->세로좌표?세로:(int)palanteer->세로좌표;
    int 오른쪽=가로+폭<(int)(palanteer->rëddu_iks_yi+palanteer->너비)?가로+폭:(int)(palanteer->rëddu_iks_yi+palanteer->너비);
    int 아래쪽=세로+diir_xëyma<(int)(palanteer->세로좌표+palanteer->높이)?세로+diir_xëyma:(int)(palanteer->세로좌표+palanteer->높이);
    영역그리기(palanteer->rëddu_iks_yi,palanteer->세로좌표,palanteer->너비,palanteer->높이);
    if(왼쪽>=오른쪽||위쪽>=아래쪽){영역그리기(가로,세로,폭,diir_xëyma);return;}
    영역그리기(가로,세로,폭,위쪽-세로);
    영역그리기(가로,아래쪽,폭,세로+diir_xëyma-아래쪽);
    영역그리기(가로,위쪽,왼쪽-가로,아래쪽-위쪽);
    영역그리기(오른쪽,위쪽,가로+폭-오른쪽,아래쪽-위쪽);
}
static void 초점알리기(void){대기중=(대기중&~15u)|(unsigned)(Fës+1)|0x10000;}
void 터미널입력방식(unsigned 한글여부){
    한글입력=한글여부!=0;
    /* Update title bars only: a mode switch must not erase an EL0 drawing. */
    if(Fës>=0){
        터미널상태 *palanteer_dugal_xabaar=&창들[Fës];
        tur_àlluwa(palanteer_dugal_xabaar->rëddu_iks_yi+240,palanteer_dugal_xabaar->세로좌표+7,palanteer_dugal_xabaar->너비>=500?(한글입력?"[WO] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[WO]":"[EN]"),0xffffff,0x905020);
    }
}
static void 앞으로올리기(int raññeekaay_xëyma){if(raññeekaay_xëyma<0||raññeekaay_xëyma>=4||!창들[raññeekaay_xëyma].살아있음)return;int 현재위치=0;while(현재위치<항목수&&toftale_xëyma[현재위치]!=raññeekaay_xëyma)현재위치++;for(;현재위치+1<항목수;현재위치++)toftale_xëyma[현재위치]=toftale_xëyma[현재위치+1];toftale_xëyma[항목수-1]=raññeekaay_xëyma;Fës=raññeekaay_xëyma;초점알리기();다시그리기();}
static void 빈칸채우기(unsigned 행위치){for(unsigned kotu_araf=0;kotu_araf<최대열수;kotu_araf++){터미널항목->글자칸들[행위치%기록줄수][kotu_araf]=0;터미널항목->모양들[행위치%기록줄수][kotu_araf]=터미널항목->전경색|(터미널항목->배경색<<4);}}
static void efaase_TOC(void){터미널항목->행위치=터미널항목->열위치=터미널항목->맨위=터미널항목->Xélal=0;for(unsigned 반환값=0;반환값<기록줄수;반환값++)빈칸채우기(반환값);if(보이는지())Këmb_xëyma();}
static int sos_dugal_xabaar(void){
    if(!보드화면기억공간())return -19;int raññeekaay_xëyma=0;while(raññeekaay_xëyma<4&&창들[raññeekaay_xëyma].살아있음)raññeekaay_xëyma++;if(raññeekaay_xëyma==4)return -28;
    Biro_wonin=1;터미널항목=&창들[raññeekaay_xëyma];memset(터미널항목,0,sizeof(*터미널항목));터미널항목->살아있음=1;터미널항목->너비=568;터미널항목->높이=360;터미널항목->열수=68;터미널항목->행수=19;터미널항목->rëddu_iks_yi=12+raññeekaay_xëyma*16;터미널항목->세로좌표=48+raññeekaay_xëyma*18;터미널항목->전경색=7;터미널항목->가리개보임=1;
    for(unsigned 반환값=0;반환값<기록줄수;반환값++)빈칸채우기(반환값);toftale_xëyma[항목수++]=raññeekaay_xëyma;Fës=raññeekaay_xëyma;대기중|=1u<<(4+raññeekaay_xëyma);초점알리기();다시그리기();return raññeekaay_xëyma+1;
}
static void Tej_palanteer(int raññeekaay_xëyma){
    if(raññeekaay_xëyma<0||raññeekaay_xëyma>=4||!창들[raññeekaay_xëyma].살아있음)return;창들[raññeekaay_xëyma].살아있음=0;대기중|=1u<<(8+raññeekaay_xëyma);
    int 현재위치=0;while(현재위치<항목수&&toftale_xëyma[현재위치]!=raññeekaay_xëyma)현재위치++;for(;현재위치+1<항목수;현재위치++)toftale_xëyma[현재위치]=toftale_xëyma[현재위치+1];항목수--;
    if(Fës==raññeekaay_xëyma)Fës=항목수?toftale_xëyma[항목수-1]:-1;초점알리기();다시그리기();
}
static void 줄바꿈(void){터미널항목->열위치=0;터미널항목->행위치++;if(터미널항목->행위치>=터미널항목->맨위+터미널항목->행수){터미널항목->맨위++;빈칸채우기(터미널항목->행위치);if(보이는지())Këmb_xëyma();}}
static void kotu_araf_451f2815(unsigned kotu_araf){
    if(kotu_araf==13){터미널항목->열위치=0;return;}if(kotu_araf==10){줄바꿈();return;}if(kotu_araf==8){if(터미널항목->열위치)터미널항목->열위치--;return;}
    if(kotu_araf==9){unsigned 개수=8-터미널항목->열위치%8;while(개수--)kotu_araf_451f2815(' ');return;}if(kotu_araf<32||kotu_araf==127)return;
    unsigned 너비값=넓은글자(kotu_araf);if(터미널항목->열위치+너비값>터미널항목->열수)줄바꿈();
    if(터미널항목->글자칸들[터미널항목->행위치%기록줄수][터미널항목->열위치]==0xffffffffu&&터미널항목->열위치){터미널항목->글자칸들[터미널항목->행위치%기록줄수][터미널항목->열위치-1]=' ';그리기(터미널항목->행위치,터미널항목->열위치-1);}
    if(넓은글자(터미널항목->글자칸들[터미널항목->행위치%기록줄수][터미널항목->열위치])==2&&터미널항목->열위치+1<터미널항목->열수){터미널항목->글자칸들[터미널항목->행위치%기록줄수][터미널항목->열위치+1]=' ';그리기(터미널항목->행위치,터미널항목->열위치+1);}
    터미널항목->글자칸들[터미널항목->행위치%기록줄수][터미널항목->열위치]=kotu_araf;터미널항목->모양들[터미널항목->행위치%기록줄수][터미널항목->열위치]=터미널항목->전경색|(터미널항목->배경색<<4);
    if(너비값==2)터미널항목->글자칸들[터미널항목->행위치%기록줄수][터미널항목->열위치+1]=0xffffffffu;
    그리기(터미널항목->행위치,터미널항목->열위치);터미널항목->열위치+=너비값;
}
static void yombal_Saytu_doxinu_ordinateur_SEQUENCE(unsigned kotu_araf){
    unsigned 개수=터미널항목->매개값[0]?터미널항목->매개값[0]:1;
    if(kotu_araf=='m')for(unsigned 순번=0;순번<=터미널항목->매개색인;순번++){unsigned 자료위치=터미널항목->매개값[순번];if(!자료위치){터미널항목->전경색=7;터미널항목->배경색=0;}if(자료위치==1&&터미널항목->전경색<8)터미널항목->전경색+=8;if(자료위치==7){unsigned 유지=터미널항목->전경색;터미널항목->전경색=터미널항목->배경색;터미널항목->배경색=유지;}if(자료위치>=30&&자료위치<=37)터미널항목->전경색=자료위치-30;if(자료위치>=90&&자료위치<=97)터미널항목->전경색=자료위치-90+8;if(자료위치>=40&&자료위치<=47)터미널항목->배경색=자료위치-40;if(자료위치>=100&&자료위치<=107)터미널항목->배경색=자료위치-100+8;if(자료위치==39)터미널항목->전경색=7;if(자료위치==49)터미널항목->배경색=0;}
    if(kotu_araf=='J'&&(터미널항목->매개값[0]==2||터미널항목->매개값[0]==3))efaase_TOC();
    if(kotu_araf=='K'){unsigned 출발위치=터미널항목->매개값[0]==2?0:터미널항목->열위치,도착위치=터미널항목->매개값[0]==1?터미널항목->열위치+1:터미널항목->열수;if(터미널항목->매개값[0]==1)출발위치=0;for(unsigned 순번=출발위치;순번<도착위치&&순번<터미널항목->열수;순번++){
        unsigned Dënk_xëyma=터미널항목->행위치%기록줄수,Araf_xëyma=터미널항목->글자칸들[Dënk_xëyma][순번],mélokaan_xëyma=터미널항목->전경색|(터미널항목->배경색<<4);
        /* 넓은 vi 화면에서도 이미 빈 칸의 mbindin_xëyma 화소를 되풀이해 칠하지 않는다. */
        int 바뀜=(Araf_xëyma!=0&&Araf_xëyma!=' ')||터미널항목->모양들[Dënk_xëyma][순번]!=mélokaan_xëyma;
        터미널항목->글자칸들[Dënk_xëyma][순번]=' ';터미널항목->모양들[Dënk_xëyma][순번]=mélokaan_xëyma;
        if(바뀜)그리기(터미널항목->행위치,순번);
    }}
    if(kotu_araf=='D')터미널항목->열위치=개수>터미널항목->열위치?0:터미널항목->열위치-개수;if(kotu_araf=='C')터미널항목->열위치=터미널항목->열위치+개수>=터미널항목->열수?터미널항목->열수-1:터미널항목->열위치+개수;
    if(kotu_araf=='G')터미널항목->열위치=개수>터미널항목->열수?터미널항목->열수-1:개수-1;if(kotu_araf=='A')터미널항목->행위치=개수>터미널항목->행위치-터미널항목->맨위?터미널항목->맨위:터미널항목->행위치-개수;
    if(kotu_araf=='B')터미널항목->행위치=터미널항목->행위치+개수>=터미널항목->맨위+터미널항목->행수?터미널항목->맨위+터미널항목->행수-1:터미널항목->행위치+개수;
    if(kotu_araf=='H'||kotu_araf=='f'){터미널항목->행위치=터미널항목->맨위+(개수>터미널항목->행수?터미널항목->행수:개수)-1;unsigned rëddu_iks_yi=터미널항목->매개값[1]?터미널항목->매개값[1]:1;터미널항목->열위치=(rëddu_iks_yi>터미널항목->열수?터미널항목->열수:rëddu_iks_yi)-1;}
    if(kotu_araf=='s'){터미널항목->저장행=터미널항목->행위치;터미널항목->저장열=터미널항목->열위치;}if(kotu_araf=='u'){터미널항목->행위치=터미널항목->저장행;터미널항목->열위치=터미널항목->저장열<터미널항목->열수?터미널항목->저장열:터미널항목->열수-1;}
    if((kotu_araf=='h'||kotu_araf=='l')&&터미널항목->매개값[0]==25)터미널항목->가리개보임=kotu_araf=='h';
}
void 터미널바이트(unsigned 둘째값){
    터미널항목=&창들[출력결과];if(!터미널항목->살아있음)return;kaare_xëyma(0);if(터미널항목->Xélal){터미널항목->Xélal=0;if(보이는지())Këmb_xëyma();}
    if(터미널항목->탈출상태==1){터미널항목->탈출상태=둘째값=='['?2:0;터미널항목->매개색인=0;for(unsigned 순번=0;순번<4;순번++)터미널항목->매개값[순번]=0;}
    else if(터미널항목->탈출상태==2){if(둘째값=='?'){}else if(둘째값>='0'&&둘째값<='9'){if(터미널항목->매개값[터미널항목->매개색인]<10000)터미널항목->매개값[터미널항목->매개색인]=터미널항목->매개값[터미널항목->매개색인]*10+둘째값-'0';}else if(둘째값==';'&&터미널항목->매개색인<3)터미널항목->매개색인++;else{yombal_Saytu_doxinu_ordinateur_SEQUENCE(둘째값);터미널항목->탈출상태=0;}}
    else if(둘째값==27){터미널항목->긴부호없는값=0;터미널항목->탈출상태=1;}else{
        if(터미널항목->긴부호없는값&&(둘째값&0xc0)!=0x80){터미널항목->긴부호없는값=0;kotu_araf_451f2815(0xfffd);}
        if(터미널항목->긴부호없는값){터미널항목->부호없는결과=터미널항목->부호없는결과*64+(둘째값&63);if(--터미널항목->긴부호없는값==0)kotu_araf_451f2815(터미널항목->부호없는결과<터미널항목->작은값||터미널항목->부호없는결과>0x10ffff||(터미널항목->부호없는결과>=0xd800&&터미널항목->부호없는결과<=0xdfff)?0xfffd:터미널항목->부호없는결과);}
        else if(둘째값<128)kotu_araf_451f2815(둘째값);else if(둘째값>=0xc2&&둘째값<=0xf4){터미널항목->긴부호없는값=둘째값<0xe0?1:둘째값<0xf0?2:3;터미널항목->부호없는결과=둘째값&((1u<<(6-터미널항목->긴부호없는값))-1);터미널항목->작은값=터미널항목->긴부호없는값==1?128:터미널항목->긴부호없는값==2?2048:65536;}else kotu_araf_451f2815(0xfffd);
    }kaare_xëyma(1);
}
int 터미널대기(void){return 대기중!=0;}
/* 모서리 àlluwa_tur: 1 좌상, 2 우상, 3 좌하, 4 우하. */
static int nattaat_randal=-1,잡은모서리,잡은가로,잡은세로,처음가로,처음세로,처음너비,처음높이;
static int 가리킨창(int 가로,int 세로) {
    for(int SEQUENCE_xëyma=항목수-1;SEQUENCE_xëyma>=0;SEQUENCE_xëyma--){
        int raññeekaay_xëyma=toftale_xëyma[SEQUENCE_xëyma];터미널상태 *palanteer=&창들[raññeekaay_xëyma];
        if(가로>=(int)palanteer->rëddu_iks_yi&&세로>=(int)palanteer->세로좌표&&
           가로<(int)(palanteer->rëddu_iks_yi+palanteer->너비)&&세로<(int)(palanteer->세로좌표+palanteer->높이))return raññeekaay_xëyma;
    }return -1;
}
static int 모서리찾기(int raññeekaay_xëyma,int 가로,int 세로) {
    if(raññeekaay_xëyma<0)return 0;터미널상태 *palanteer=&창들[raññeekaay_xëyma];
    int 왼쪽=가로<(int)palanteer->rëddu_iks_yi+8,오른쪽=가로>=(int)(palanteer->rëddu_iks_yi+palanteer->너비)-8;
    int 위쪽=세로<(int)palanteer->세로좌표+8,아래쪽=세로>=(int)(palanteer->세로좌표+palanteer->높이)-8;
    return (왼쪽||오른쪽)&&(위쪽||아래쪽)?1+오른쪽+아래쪽*2:0;
}
static int xàjjalekat_xëyma(int xëyma,int 최소,int 최대){return xëyma<최소?최소:xëyma>최대?최대:xëyma;}
static void toxal_nattaat(int 가로,int 세로) {
    터미널상태 *palanteer=&창들[nattaat_randal];int 왼쪽=처음가로,위쪽=처음세로,오른쪽=처음가로+처음너비,아래쪽=처음세로+처음높이;
    if(잡은모서리==1||잡은모서리==3)왼쪽=xàjjalekat_xëyma(처음가로+가로-잡은가로,0,오른쪽-360);
    else 오른쪽=xàjjalekat_xëyma(처음가로+처음너비+가로-잡은가로,왼쪽+360,보드화면너비());
    if(잡은모서리<=2)위쪽=xàjjalekat_xëyma(처음세로+세로-잡은세로,34,아래쪽-216);
    else 아래쪽=xàjjalekat_xëyma(처음세로+처음높이+세로-잡은세로,위쪽+216,보드화면높이());
    unsigned 열수=(오른쪽-왼쪽-24)/8,행수=(아래쪽-위쪽-56)/16;
    if(palanteer->열수!=열수||palanteer->행수!=행수){
        palanteer->크기바뀜=1;palanteer->열수=열수;palanteer->행수=행수;
        if(palanteer->열위치>=열수)palanteer->열위치=열수-1;
        if(palanteer->행위치>=palanteer->맨위+행수)palanteer->맨위=palanteer->행위치-행수+1;
        unsigned 한도=palanteer->맨위;if(한도>기록줄수-행수)한도=기록줄수-행수;
        if(palanteer->Xélal>한도)palanteer->Xélal=한도;
    }
    int 옛가로=palanteer->rëddu_iks_yi,옛세로=palanteer->세로좌표,옛폭=palanteer->너비,옛길이=palanteer->높이;
    if(옛가로==왼쪽&&옛세로==위쪽&&옛폭==오른쪽-왼쪽&&옛길이==아래쪽-위쪽)return;
    palanteer->rëddu_iks_yi=왼쪽;palanteer->세로좌표=위쪽;palanteer->너비=오른쪽-왼쪽;palanteer->높이=아래쪽-위쪽;
    창자리그리기(옛가로,옛세로,옛폭,옛길이,palanteer);
}
void 터미널가리킴(unsigned 다음,int rëddu_iks_yi,int 세로좌표){
    unsigned 눌림=다음&~단추들;단추들=다음;
    if(!Biro_wonin){randal_xëyma=-1;nattaat_randal=-1;보드포인터(rëddu_iks_yi,세로좌표,1);return;}
    if(!(다음&1)){randal_xëyma=-1;nattaat_randal=-1;}
    if(nattaat_randal>=0&&!창들[nattaat_randal].살아있음)nattaat_randal=-1;
    if(randal_xëyma>=0&&!창들[randal_xëyma].살아있음)randal_xëyma=-1;
    if(nattaat_randal>=0){
        toxal_nattaat(rëddu_iks_yi,세로좌표);보드포인터(rëddu_iks_yi,세로좌표,잡은모서리==1||잡은모서리==4?2:3);return;
    }
    보드포인터(rëddu_iks_yi,세로좌표,1);
    if(randal_xëyma>=0){
        터미널상태 *palanteer=&창들[randal_xëyma];
        int 옛가로=palanteer->rëddu_iks_yi,옛세로=palanteer->세로좌표;
        palanteer->rëddu_iks_yi=xàjjalekat_xëyma(rëddu_iks_yi-끌기가로,0,보드화면너비()-palanteer->너비);
        palanteer->세로좌표=xàjjalekat_xëyma(세로좌표-끌기세로,34,보드화면높이()-palanteer->높이);
        if(옛가로!=(int)palanteer->rëddu_iks_yi||옛세로!=(int)palanteer->세로좌표)창자리그리기(옛가로,옛세로,palanteer->너비,palanteer->높이,palanteer);
        return;
    }
    extern int 화면덮음(int,int,int);
    if(화면덮음(Fës,rëddu_iks_yi,세로좌표)){화면가리킴(Fës,눌림,rëddu_iks_yi,세로좌표);return;}
    int raññeekaay_xëyma=가리킨창(rëddu_iks_yi,세로좌표),모서리=모서리찾기(raññeekaay_xëyma,rëddu_iks_yi,세로좌표);
    if(모서리)보드포인터(rëddu_iks_yi,세로좌표,모서리==1||모서리==4?2:3);
    if(눌림&1){
        if(모서리){
            터미널상태 *palanteer=&창들[raññeekaay_xëyma];nattaat_randal=raññeekaay_xëyma;잡은모서리=모서리;잡은가로=rëddu_iks_yi;잡은세로=세로좌표;
            처음가로=palanteer->rëddu_iks_yi;처음세로=palanteer->세로좌표;처음너비=palanteer->너비;처음높이=palanteer->높이;
            if(raññeekaay_xëyma!=Fës)앞으로올리기(raññeekaay_xëyma);return;
        }
        if(세로좌표<32&&rëddu_iks_yi>=6&&rëddu_iks_yi<142){sos_dugal_xabaar();return;}
        if(세로좌표<32&&rëddu_iks_yi>=154&&rëddu_iks_yi<602){앞으로올리기((rëddu_iks_yi-154)/112);return;}
        if(raññeekaay_xëyma>=0){
            터미널상태 *palanteer=&창들[raññeekaay_xëyma];
            if(세로좌표<(int)palanteer->세로좌표+30&&rëddu_iks_yi>=(int)(palanteer->rëddu_iks_yi+palanteer->너비)-32){Tej_palanteer(raññeekaay_xëyma);return;}
            if(raññeekaay_xëyma!=Fës)앞으로올리기(raññeekaay_xëyma);
            if(세로좌표<(int)palanteer->세로좌표+30){randal_xëyma=raññeekaay_xëyma;끌기가로=rëddu_iks_yi-palanteer->rëddu_iks_yi;끌기세로=세로좌표-palanteer->세로좌표;}return;
        }
    }
    if(Fës>=0&&(눌림&(8|16))){터미널항목=&창들[Fës];if(눌림&8){unsigned 한도=터미널항목->맨위;if(한도>기록줄수-터미널항목->행수)한도=기록줄수-터미널항목->행수;터미널항목->Xélal=터미널항목->Xélal+9>한도?한도:터미널항목->Xélal+9;}else 터미널항목->Xélal=터미널항목->Xélal<9?0:터미널항목->Xélal-9;다시그리기();}
}
void 터미널바로가기키(unsigned 누름값){if(누름값==1)sos_dugal_xabaar();if(누름값==2&&항목수)앞으로올리기(toftale_xëyma[0]);if(누름값==3)Tej_palanteer(Fës);}
masin_Word 보드터미널(masin_Word jëf){
    if(jëf==300){if(!창들[출력결과].살아있음)return sos_dugal_xabaar();Biro_wonin=1;다시그리기();return 0;}
    if(jëf==0){Tej_palanteer(Fës);return 0;}if(jëf==1)return (uint32_t)sos_dugal_xabaar();if(jëf==2)return Fës>=0;
    if(jëf==9){Biro_wonin=0;return 0;}if(jëf==7)return 항목수;if(jëf==10)return Fës+1;if(jëf==11)return 출력결과;
    if(jëf==13){터미널상태 *palanteer=&창들[출력결과];return palanteer->살아있음?(palanteer->행수<<16)|palanteer->열수:(19<<16)|68;}
    if(jëf==14){unsigned xëyma=창들[출력결과].크기바뀜;창들[출력결과].크기바뀜=0;return xëyma;}
    if(jëf==12){unsigned xëyma=대기중;대기중=0;return xëyma;}
    if(jëf>=20&&jëf<24)return 창들[jëf-20].살아있음;
    if(jëf>=100&&jëf<104){출력결과=jëf-100;터미널항목=&창들[출력결과];return 0;}
    if(jëf>=200&&jëf<204){앞으로올리기(jëf-200);return 0;}
    if(jëf==3){다시그리기();return 0;}터미널항목=&창들[출력결과];if(!터미널항목->살아있음)return 0;
    if(jëf==4)efaase_TOC();if(jëf==5||jëf==6){unsigned 이전=단추들;터미널가리킴(jëf==5?8:16,0,0);단추들=이전;}return 1;
}
