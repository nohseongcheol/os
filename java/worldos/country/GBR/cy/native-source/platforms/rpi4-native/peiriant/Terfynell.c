#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* 자체 네 ffenestr 합성과 UTF-8 Terfynell. 바뀐 영역의 완성 그림만 표시한다. */
#include <stdint.h>
#include <stddef.h>
typedef uintptr_t peiriant_Word;
extern peiriant_Word bwrdd_pel(peiriant_Word,peiriant_Word,peiriant_Word),보드화면기억공간(void);
extern void *memset(void *,int,size_t);
extern const unsigned char Terfynell_ffont[];
#define 최대열수 237
#define Hanes_llinell_COUNT 160
typedef struct {
    uint32_t 글자칸들[Hanes_llinell_COUNT][최대열수]; uint8_t 모양들[Hanes_llinell_COUNT][최대열수];
    unsigned 너비,높이,COLUMNS,ROW_COUNT,크기바뀜;
    unsigned 살아있음,cyfesuryn_x,Y_cyfesuryn,ROW_safle,COLUMN_safle,맨위,sgrolio,전경색,배경색,탈출상태,paramedr_VALUE[4],paramedr_INDEX,저장행,저장열;
    unsigned 부호없는결과,긴부호없는값,SMALL_VALUE,대체화면,가리개보임;
} Terfynell_d413d4bc;
static Terfynell_d413d4bc Windows_Rhestr[4];
static int Ffocws=-1,출력결과,trefn_VALUE[4],cofnod_COUNT,llusgo_VALUE=-1,llusgo_X,llusgo_Y;
static unsigned technoleg_gwybodaeth_yn_disgwyl,단추들,bwrdd_gwaith_Gwedd,한글입력;
static const uint32_t 색상들[16]={0x201a15,0x6060df,0x9dcc86,0x80cfea,0xefaf72,0xca96c9,0xceda76,0xede9df,0x858078,0x8888ff,0xb9eba7,0xa5eaff,0xffcc99,0xf0bef1,0xf0f0a0,0xffffff};
extern int 화면보임(int),화면가리킴(int,unsigned,int,int);
extern void 화면다시그림(int);
static Terfynell_d413d4bc *Terfynell_cofnod;
static unsigned 넓은글자(unsigned cod_nod){return cod_nod>=256?2:1;}
static void 사각영역(unsigned cyfesuryn_x,unsigned Y_cyfesuryn,unsigned 너비값,unsigned 높이값,unsigned 색상){
    보드사각그림(cyfesuryn_x,Y_cyfesuryn,너비값,높이값,색상);
}
void Terfynell_glyff(unsigned cyfesuryn_x,unsigned Y_cyfesuryn,unsigned cod_nod,unsigned 전경색,unsigned 배경색){
    unsigned 너비=넓은글자(cod_nod)*8;if(cod_nod==0xffffffffu)return;
    int 왼쪽=cyfesuryn_x,위쪽=Y_cyfesuryn,폭=너비,hyd_VALUE=16;
    if(!보드그림범위(&왼쪽,&위쪽,&폭,&hyd_VALUE))return;
    if(cod_nod==' '){보드사각그림(왼쪽,위쪽,폭,hyd_VALUE,배경색);return;}
    unsigned LOOKUP_INDEX=cod_nod<65536?cod_nod:cod_nod>=0x1f600&&cod_nod<0x1f650?65536+cod_nod-0x1f600:0xfffd;
    const unsigned char *ffont_VALUE=Terfynell_ffont+LOOKUP_INDEX*32;
    for(int llinell=위쪽;llinell<위쪽+hyd_VALUE;llinell++){unsigned 비트들=ffont_VALUE[(llinell-Y_cyfesuryn)*2]*256+ffont_VALUE[(llinell-Y_cyfesuryn)*2+1];for(int slot_cofnod=왼쪽;slot_cofnod<왼쪽+폭;slot_cofnod++)bwrdd_pel(slot_cofnod,llinell,(비트들&(0x8000>>(slot_cofnod-cyfesuryn_x)))?전경색:배경색);}
}
static void enw_tabl(unsigned cyfesuryn_x,unsigned Y_cyfesuryn,const char *testun_data,unsigned 전경색,unsigned 배경색){while(*testun_data){unsigned cod_nod=(unsigned char)*testun_data++, 남은수=0;if(cod_nod>=0xc0){남은수=cod_nod<0xe0?1:cod_nod<0xf0?2:3;cod_nod&=(1u<<(6-남은수))-1;while(남은수--&&*testun_data)cod_nod=(cod_nod<<6)|((unsigned char)*testun_data++&63);}Terfynell_glyff(cyfesuryn_x,Y_cyfesuryn,cod_nod,전경색,배경색);cyfesuryn_x+=넓은글자(cod_nod)*8;}}
static unsigned 첫항목(void){return Terfynell_cofnod->맨위;}
static int 보이는지(void){return Terfynell_cofnod->살아있음&&Ffocws>=0&&Terfynell_cofnod==&Windows_Rhestr[Ffocws]&&!화면보임(Ffocws);}
static void 그리기(unsigned ROW_safle,unsigned COLUMN_safle){
    if(!보이는지()||ROW_safle<첫항목()-Terfynell_cofnod->sgrolio||ROW_safle>=첫항목()-Terfynell_cofnod->sgrolio+Terfynell_cofnod->ROW_COUNT||COLUMN_safle>=Terfynell_cofnod->COLUMNS)return;
    unsigned cod_nod=Terfynell_cofnod->글자칸들[ROW_safle%Hanes_llinell_COUNT][COLUMN_safle],testun_data=Terfynell_cofnod->모양들[ROW_safle%Hanes_llinell_COUNT][COLUMN_safle];
    if(넓은글자(cod_nod)==2&&COLUMN_safle+1>=Terfynell_cofnod->COLUMNS)cod_nod=' ';
    Terfynell_glyff(Terfynell_cofnod->cyfesuryn_x+12+COLUMN_safle*8,Terfynell_cofnod->Y_cyfesuryn+36+(ROW_safle-첫항목()+Terfynell_cofnod->sgrolio)*16,cod_nod?cod_nod:' ',색상들[testun_data&15],색상들[testun_data>>4]);
}
static void to_bach_VALUE(int sioe_ffenestr){if(!보이는지()||Terfynell_cofnod->sgrolio||Terfynell_cofnod->COLUMN_safle>=Terfynell_cofnod->COLUMNS||Terfynell_cofnod->ROW_safle<Terfynell_cofnod->맨위||Terfynell_cofnod->ROW_safle>=Terfynell_cofnod->맨위+Terfynell_cofnod->ROW_COUNT)return;
    if(!sioe_ffenestr||!Terfynell_cofnod->가리개보임)그리기(Terfynell_cofnod->ROW_safle,Terfynell_cofnod->COLUMN_safle);else 사각영역(Terfynell_cofnod->cyfesuryn_x+12+Terfynell_cofnod->COLUMN_safle*8,Terfynell_cofnod->Y_cyfesuryn+36+(Terfynell_cofnod->ROW_safle-Terfynell_cofnod->맨위)*16+14,8,2,색상들[Terfynell_cofnod->전경색]);}
static void Cynnwys_VALUE(void){
    사각영역(Terfynell_cofnod->cyfesuryn_x+12,Terfynell_cofnod->Y_cyfesuryn+36,Terfynell_cofnod->COLUMNS*8,Terfynell_cofnod->ROW_COUNT*16,색상들[0]);
    int 가로=Terfynell_cofnod->cyfesuryn_x+12,Ar_i_fyny_safle=Terfynell_cofnod->Y_cyfesuryn+36,폭=Terfynell_cofnod->COLUMNS*8,hyd_VALUE=Terfynell_cofnod->ROW_COUNT*16;
    if(보드그림범위(&가로,&Ar_i_fyny_safle,&폭,&hyd_VALUE)){
    unsigned 첫줄=(Ar_i_fyny_safle-Terfynell_cofnod->Y_cyfesuryn-36)/16,끝줄=(Ar_i_fyny_safle+hyd_VALUE-Terfynell_cofnod->Y_cyfesuryn-36+15)/16;
    unsigned 첫칸=(가로-Terfynell_cofnod->cyfesuryn_x-12)/8,끝칸=(가로+폭-Terfynell_cofnod->cyfesuryn_x-12+7)/8;
    if(첫칸)첫칸--; /* 잘림 경계 왼쪽에서 시작한 두 slot_cofnod 글자도 그린다. */
    for(unsigned 반환값=첫줄;반환값<끝줄;반환값++)for(unsigned cod_nod=첫칸;cod_nod<끝칸;cod_nod++){
        unsigned ROW_safle=첫항목()-Terfynell_cofnod->sgrolio+반환값,nod_VALUE=Terfynell_cofnod->글자칸들[ROW_safle%Hanes_llinell_COUNT][cod_nod],testun_data=Terfynell_cofnod->모양들[ROW_safle%Hanes_llinell_COUNT][cod_nod];
        if(넓은글자(nod_VALUE)==2&&cod_nod+1>=Terfynell_cofnod->COLUMNS)nod_VALUE=' ';
        if((nod_VALUE==0||nod_VALUE==' ')&&(testun_data>>4)==0)continue;
        Terfynell_glyff(Terfynell_cofnod->cyfesuryn_x+12+cod_nod*8,Terfynell_cofnod->Y_cyfesuryn+36+반환값*16,nod_VALUE?nod_VALUE:' ',색상들[testun_data&15],색상들[testun_data>>4]);
    }}
    enw_tabl(Terfynell_cofnod->cyfesuryn_x+12,Terfynell_cofnod->Y_cyfesuryn+Terfynell_cofnod->높이-18,Terfynell_cofnod->sgrolio?"PgDn: recent output":Terfynell_cofnod->너비>=500?"F6: next | Corner + left drag: resize":"Corner + left drag: resize",0xece8e2,0x403127);to_bach_VALUE(1);
}
static void 실행틀(int dynodwr_VALUE){
    Terfynell_cofnod=&Windows_Rhestr[dynodwr_VALUE];
    int 가로=Terfynell_cofnod->cyfesuryn_x,Ar_i_fyny_safle=Terfynell_cofnod->Y_cyfesuryn,폭=Terfynell_cofnod->너비,hyd_VALUE=Terfynell_cofnod->높이;
    if(!보드그림범위(&가로,&Ar_i_fyny_safle,&폭,&hyd_VALUE))return;
    사각영역(Terfynell_cofnod->cyfesuryn_x,Terfynell_cofnod->Y_cyfesuryn,Terfynell_cofnod->너비,Terfynell_cofnod->높이,0x403127);
    unsigned 색상=dynodwr_VALUE==Ffocws?0x905020:0x604438;사각영역(Terfynell_cofnod->cyfesuryn_x,Terfynell_cofnod->Y_cyfesuryn,Terfynell_cofnod->너비,30,색상);
    enw_tabl(Terfynell_cofnod->cyfesuryn_x+12,Terfynell_cofnod->Y_cyfesuryn+7,"JKOROS Terminal",0xffffff,색상);
    char 수치[2]={(char)('1'+dynodwr_VALUE),0};enw_tabl(Terfynell_cofnod->cyfesuryn_x+148,Terfynell_cofnod->Y_cyfesuryn+7,수치,0xffffff,색상);
    enw_tabl(Terfynell_cofnod->cyfesuryn_x+240,Terfynell_cofnod->Y_cyfesuryn+7,Terfynell_cofnod->너비>=500?(한글입력?"[CY] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[CY]":"[EN]"),0xffffff,색상);
    사각영역(Terfynell_cofnod->cyfesuryn_x+Terfynell_cofnod->너비-32,Terfynell_cofnod->Y_cyfesuryn+4,26,22,0x5555b8);enw_tabl(Terfynell_cofnod->cyfesuryn_x+Terfynell_cofnod->너비-24,Terfynell_cofnod->Y_cyfesuryn+7,"X",0xffffff,0x5555b8);
    Cynnwys_VALUE();
}
static void 장면그리기(void){
    if(!bwrdd_gwaith_Gwedd)return;사각영역(0,0,보드화면너비(),보드화면높이(),0x302018);사각영역(0,0,보드화면너비(),32,0x403127);
    사각영역(6,4,136,24,0x905020);enw_tabl(14,8,"+ New terminal",0xffffff,0x905020);
    for(int 순번=0;순번<4;순번++)if(Windows_Rhestr[순번].살아있음){unsigned cod_nod=Ffocws==순번?0x905020:0x604438;사각영역(154+순번*112,4,106,24,cod_nod);enw_tabl(160+순번*112,8,"Terminal",0xffffff,cod_nod);char testun_data[2]={(char)('1'+순번),0};enw_tabl(232+순번*112,8,testun_data,0xffffff,cod_nod);}
    if(!cofnod_COUNT)enw_tabl(140,210,"Click + New terminal to start",0xede9df,0x302018);
    for(int 순번=0;순번<cofnod_COUNT;순번++)실행틀(trefn_VALUE[순번]);화면다시그림(Ffocws);Terfynell_cofnod=&Windows_Rhestr[출력결과];
}
static void 영역그리기(int 가로,int Ar_i_fyny_safle,int 폭,int hyd_VALUE){
    if(!bwrdd_gwaith_Gwedd||!보드그림범위(&가로,&Ar_i_fyny_safle,&폭,&hyd_VALUE))return;
    for(int llinell=Ar_i_fyny_safle;llinell<Ar_i_fyny_safle+hyd_VALUE;llinell+=32){
        int 띠높이=Ar_i_fyny_safle+hyd_VALUE-llinell;if(띠높이>32)띠높이=32;
        if(bwrdd_START_lluniad(가로,llinell,폭,띠높이)){장면그리기();bwrdd_Gorffen_lluniad();}
    }
}
static void 다시그리기(void){영역그리기(0,0,보드화면너비(),보드화면높이());}
/* 서로 겹치지 않는 새 ffenestr 영역과 이전 자리의 네 띠를 복구한다. */
static void 창자리그리기(int 가로,int Ar_i_fyny_safle,int 폭,int hyd_VALUE,Terfynell_d413d4bc *ffenestr){
    int 왼쪽=가로>(int)ffenestr->cyfesuryn_x?가로:(int)ffenestr->cyfesuryn_x;
    int 위쪽=Ar_i_fyny_safle>(int)ffenestr->Y_cyfesuryn?Ar_i_fyny_safle:(int)ffenestr->Y_cyfesuryn;
    int RIGHT=가로+폭<(int)(ffenestr->cyfesuryn_x+ffenestr->너비)?가로+폭:(int)(ffenestr->cyfesuryn_x+ffenestr->너비);
    int 아래쪽=Ar_i_fyny_safle+hyd_VALUE<(int)(ffenestr->Y_cyfesuryn+ffenestr->높이)?Ar_i_fyny_safle+hyd_VALUE:(int)(ffenestr->Y_cyfesuryn+ffenestr->높이);
    영역그리기(ffenestr->cyfesuryn_x,ffenestr->Y_cyfesuryn,ffenestr->너비,ffenestr->높이);
    if(왼쪽>=RIGHT||위쪽>=아래쪽){영역그리기(가로,Ar_i_fyny_safle,폭,hyd_VALUE);return;}
    영역그리기(가로,Ar_i_fyny_safle,폭,위쪽-Ar_i_fyny_safle);
    영역그리기(가로,아래쪽,폭,Ar_i_fyny_safle+hyd_VALUE-아래쪽);
    영역그리기(가로,위쪽,왼쪽-가로,아래쪽-위쪽);
    영역그리기(RIGHT,위쪽,가로+폭-RIGHT,아래쪽-위쪽);
}
static void 초점알리기(void){technoleg_gwybodaeth_yn_disgwyl=(technoleg_gwybodaeth_yn_disgwyl&~15u)|(unsigned)(Ffocws+1)|0x10000;}
void 터미널입력방식(unsigned 한글여부){
    한글입력=한글여부!=0;
    /* Update title bars only: a mode switch must not erase an EL0 drawing. */
    if(Ffocws>=0){
        Terfynell_d413d4bc *ffenestr_cofnod=&Windows_Rhestr[Ffocws];
        enw_tabl(ffenestr_cofnod->cyfesuryn_x+240,ffenestr_cofnod->Y_cyfesuryn+7,ffenestr_cofnod->너비>=500?(한글입력?"[CY] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[CY]":"[EN]"),0xffffff,0x905020);
    }
}
static void 앞으로올리기(int dynodwr_VALUE){if(dynodwr_VALUE<0||dynodwr_VALUE>=4||!Windows_Rhestr[dynodwr_VALUE].살아있음)return;int 현재위치=0;while(현재위치<cofnod_COUNT&&trefn_VALUE[현재위치]!=dynodwr_VALUE)현재위치++;for(;현재위치+1<cofnod_COUNT;현재위치++)trefn_VALUE[현재위치]=trefn_VALUE[현재위치+1];trefn_VALUE[cofnod_COUNT-1]=dynodwr_VALUE;Ffocws=dynodwr_VALUE;초점알리기();다시그리기();}
static void 빈칸채우기(unsigned ROW_safle){for(unsigned cod_nod=0;cod_nod<최대열수;cod_nod++){Terfynell_cofnod->글자칸들[ROW_safle%Hanes_llinell_COUNT][cod_nod]=0;Terfynell_cofnod->모양들[ROW_safle%Hanes_llinell_COUNT][cod_nod]=Terfynell_cofnod->전경색|(Terfynell_cofnod->배경색<<4);}}
static void clirio_Cynnwys(void){Terfynell_cofnod->ROW_safle=Terfynell_cofnod->COLUMN_safle=Terfynell_cofnod->맨위=Terfynell_cofnod->sgrolio=0;for(unsigned 반환값=0;반환값<Hanes_llinell_COUNT;반환값++)빈칸채우기(반환값);if(보이는지())Cynnwys_VALUE();}
static int Creu_cofnod(void){
    if(!보드화면기억공간())return -19;int dynodwr_VALUE=0;while(dynodwr_VALUE<4&&Windows_Rhestr[dynodwr_VALUE].살아있음)dynodwr_VALUE++;if(dynodwr_VALUE==4)return -28;
    bwrdd_gwaith_Gwedd=1;Terfynell_cofnod=&Windows_Rhestr[dynodwr_VALUE];memset(Terfynell_cofnod,0,sizeof(*Terfynell_cofnod));Terfynell_cofnod->살아있음=1;Terfynell_cofnod->너비=568;Terfynell_cofnod->높이=360;Terfynell_cofnod->COLUMNS=68;Terfynell_cofnod->ROW_COUNT=19;Terfynell_cofnod->cyfesuryn_x=12+dynodwr_VALUE*16;Terfynell_cofnod->Y_cyfesuryn=48+dynodwr_VALUE*18;Terfynell_cofnod->전경색=7;Terfynell_cofnod->가리개보임=1;
    for(unsigned 반환값=0;반환값<Hanes_llinell_COUNT;반환값++)빈칸채우기(반환값);trefn_VALUE[cofnod_COUNT++]=dynodwr_VALUE;Ffocws=dynodwr_VALUE;technoleg_gwybodaeth_yn_disgwyl|=1u<<(4+dynodwr_VALUE);초점알리기();다시그리기();return dynodwr_VALUE+1;
}
static void cau_ffenestr(int dynodwr_VALUE){
    if(dynodwr_VALUE<0||dynodwr_VALUE>=4||!Windows_Rhestr[dynodwr_VALUE].살아있음)return;Windows_Rhestr[dynodwr_VALUE].살아있음=0;technoleg_gwybodaeth_yn_disgwyl|=1u<<(8+dynodwr_VALUE);
    int 현재위치=0;while(현재위치<cofnod_COUNT&&trefn_VALUE[현재위치]!=dynodwr_VALUE)현재위치++;for(;현재위치+1<cofnod_COUNT;현재위치++)trefn_VALUE[현재위치]=trefn_VALUE[현재위치+1];cofnod_COUNT--;
    if(Ffocws==dynodwr_VALUE)Ffocws=cofnod_COUNT?trefn_VALUE[cofnod_COUNT-1]:-1;초점알리기();다시그리기();
}
static void 줄바꿈(void){Terfynell_cofnod->COLUMN_safle=0;Terfynell_cofnod->ROW_safle++;if(Terfynell_cofnod->ROW_safle>=Terfynell_cofnod->맨위+Terfynell_cofnod->ROW_COUNT){Terfynell_cofnod->맨위++;빈칸채우기(Terfynell_cofnod->ROW_safle);if(보이는지())Cynnwys_VALUE();}}
static void cod_nod_451f2815(unsigned cod_nod){
    if(cod_nod==13){Terfynell_cofnod->COLUMN_safle=0;return;}if(cod_nod==10){줄바꿈();return;}if(cod_nod==8){if(Terfynell_cofnod->COLUMN_safle)Terfynell_cofnod->COLUMN_safle--;return;}
    if(cod_nod==9){unsigned eitem_COUNT=8-Terfynell_cofnod->COLUMN_safle%8;while(eitem_COUNT--)cod_nod_451f2815(' ');return;}if(cod_nod<32||cod_nod==127)return;
    unsigned 너비값=넓은글자(cod_nod);if(Terfynell_cofnod->COLUMN_safle+너비값>Terfynell_cofnod->COLUMNS)줄바꿈();
    if(Terfynell_cofnod->글자칸들[Terfynell_cofnod->ROW_safle%Hanes_llinell_COUNT][Terfynell_cofnod->COLUMN_safle]==0xffffffffu&&Terfynell_cofnod->COLUMN_safle){Terfynell_cofnod->글자칸들[Terfynell_cofnod->ROW_safle%Hanes_llinell_COUNT][Terfynell_cofnod->COLUMN_safle-1]=' ';그리기(Terfynell_cofnod->ROW_safle,Terfynell_cofnod->COLUMN_safle-1);}
    if(넓은글자(Terfynell_cofnod->글자칸들[Terfynell_cofnod->ROW_safle%Hanes_llinell_COUNT][Terfynell_cofnod->COLUMN_safle])==2&&Terfynell_cofnod->COLUMN_safle+1<Terfynell_cofnod->COLUMNS){Terfynell_cofnod->글자칸들[Terfynell_cofnod->ROW_safle%Hanes_llinell_COUNT][Terfynell_cofnod->COLUMN_safle+1]=' ';그리기(Terfynell_cofnod->ROW_safle,Terfynell_cofnod->COLUMN_safle+1);}
    Terfynell_cofnod->글자칸들[Terfynell_cofnod->ROW_safle%Hanes_llinell_COUNT][Terfynell_cofnod->COLUMN_safle]=cod_nod;Terfynell_cofnod->모양들[Terfynell_cofnod->ROW_safle%Hanes_llinell_COUNT][Terfynell_cofnod->COLUMN_safle]=Terfynell_cofnod->전경색|(Terfynell_cofnod->배경색<<4);
    if(너비값==2)Terfynell_cofnod->글자칸들[Terfynell_cofnod->ROW_safle%Hanes_llinell_COUNT][Terfynell_cofnod->COLUMN_safle+1]=0xffffffffu;
    그리기(Terfynell_cofnod->ROW_safle,Terfynell_cofnod->COLUMN_safle);Terfynell_cofnod->COLUMN_safle+=너비값;
}
static void dolen_rheoli_SEQUENCE(unsigned cod_nod){
    unsigned eitem_COUNT=Terfynell_cofnod->paramedr_VALUE[0]?Terfynell_cofnod->paramedr_VALUE[0]:1;
    if(cod_nod=='m')for(unsigned 순번=0;순번<=Terfynell_cofnod->paramedr_INDEX;순번++){unsigned data_safle=Terfynell_cofnod->paramedr_VALUE[순번];if(!data_safle){Terfynell_cofnod->전경색=7;Terfynell_cofnod->배경색=0;}if(data_safle==1&&Terfynell_cofnod->전경색<8)Terfynell_cofnod->전경색+=8;if(data_safle==7){unsigned 유지=Terfynell_cofnod->전경색;Terfynell_cofnod->전경색=Terfynell_cofnod->배경색;Terfynell_cofnod->배경색=유지;}if(data_safle>=30&&data_safle<=37)Terfynell_cofnod->전경색=data_safle-30;if(data_safle>=90&&data_safle<=97)Terfynell_cofnod->전경색=data_safle-90+8;if(data_safle>=40&&data_safle<=47)Terfynell_cofnod->배경색=data_safle-40;if(data_safle>=100&&data_safle<=107)Terfynell_cofnod->배경색=data_safle-100+8;if(data_safle==39)Terfynell_cofnod->전경색=7;if(data_safle==49)Terfynell_cofnod->배경색=0;}
    if(cod_nod=='J'&&(Terfynell_cofnod->paramedr_VALUE[0]==2||Terfynell_cofnod->paramedr_VALUE[0]==3))clirio_Cynnwys();
    if(cod_nod=='K'){unsigned 출발위치=Terfynell_cofnod->paramedr_VALUE[0]==2?0:Terfynell_cofnod->COLUMN_safle,도착위치=Terfynell_cofnod->paramedr_VALUE[0]==1?Terfynell_cofnod->COLUMN_safle+1:Terfynell_cofnod->COLUMNS;if(Terfynell_cofnod->paramedr_VALUE[0]==1)출발위치=0;for(unsigned 순번=출발위치;순번<도착위치&&순번<Terfynell_cofnod->COLUMNS;순번++){
        unsigned ROW_VALUE=Terfynell_cofnod->ROW_safle%Hanes_llinell_COUNT,nod_VALUE=Terfynell_cofnod->글자칸들[ROW_VALUE][순번],siâp_VALUE=Terfynell_cofnod->전경색|(Terfynell_cofnod->배경색<<4);
        /* 넓은 vi 화면에서도 이미 빈 칸의 ffont_VALUE 화소를 되풀이해 칠하지 않는다. */
        int 바뀜=(nod_VALUE!=0&&nod_VALUE!=' ')||Terfynell_cofnod->모양들[ROW_VALUE][순번]!=siâp_VALUE;
        Terfynell_cofnod->글자칸들[ROW_VALUE][순번]=' ';Terfynell_cofnod->모양들[ROW_VALUE][순번]=siâp_VALUE;
        if(바뀜)그리기(Terfynell_cofnod->ROW_safle,순번);
    }}
    if(cod_nod=='D')Terfynell_cofnod->COLUMN_safle=eitem_COUNT>Terfynell_cofnod->COLUMN_safle?0:Terfynell_cofnod->COLUMN_safle-eitem_COUNT;if(cod_nod=='C')Terfynell_cofnod->COLUMN_safle=Terfynell_cofnod->COLUMN_safle+eitem_COUNT>=Terfynell_cofnod->COLUMNS?Terfynell_cofnod->COLUMNS-1:Terfynell_cofnod->COLUMN_safle+eitem_COUNT;
    if(cod_nod=='G')Terfynell_cofnod->COLUMN_safle=eitem_COUNT>Terfynell_cofnod->COLUMNS?Terfynell_cofnod->COLUMNS-1:eitem_COUNT-1;if(cod_nod=='A')Terfynell_cofnod->ROW_safle=eitem_COUNT>Terfynell_cofnod->ROW_safle-Terfynell_cofnod->맨위?Terfynell_cofnod->맨위:Terfynell_cofnod->ROW_safle-eitem_COUNT;
    if(cod_nod=='B')Terfynell_cofnod->ROW_safle=Terfynell_cofnod->ROW_safle+eitem_COUNT>=Terfynell_cofnod->맨위+Terfynell_cofnod->ROW_COUNT?Terfynell_cofnod->맨위+Terfynell_cofnod->ROW_COUNT-1:Terfynell_cofnod->ROW_safle+eitem_COUNT;
    if(cod_nod=='H'||cod_nod=='f'){Terfynell_cofnod->ROW_safle=Terfynell_cofnod->맨위+(eitem_COUNT>Terfynell_cofnod->ROW_COUNT?Terfynell_cofnod->ROW_COUNT:eitem_COUNT)-1;unsigned cyfesuryn_x=Terfynell_cofnod->paramedr_VALUE[1]?Terfynell_cofnod->paramedr_VALUE[1]:1;Terfynell_cofnod->COLUMN_safle=(cyfesuryn_x>Terfynell_cofnod->COLUMNS?Terfynell_cofnod->COLUMNS:cyfesuryn_x)-1;}
    if(cod_nod=='s'){Terfynell_cofnod->저장행=Terfynell_cofnod->ROW_safle;Terfynell_cofnod->저장열=Terfynell_cofnod->COLUMN_safle;}if(cod_nod=='u'){Terfynell_cofnod->ROW_safle=Terfynell_cofnod->저장행;Terfynell_cofnod->COLUMN_safle=Terfynell_cofnod->저장열<Terfynell_cofnod->COLUMNS?Terfynell_cofnod->저장열:Terfynell_cofnod->COLUMNS-1;}
    if((cod_nod=='h'||cod_nod=='l')&&Terfynell_cofnod->paramedr_VALUE[0]==25)Terfynell_cofnod->가리개보임=cod_nod=='h';
}
void Terfynell_beit(unsigned SECOND_VALUE){
    Terfynell_cofnod=&Windows_Rhestr[출력결과];if(!Terfynell_cofnod->살아있음)return;to_bach_VALUE(0);if(Terfynell_cofnod->sgrolio){Terfynell_cofnod->sgrolio=0;if(보이는지())Cynnwys_VALUE();}
    if(Terfynell_cofnod->탈출상태==1){Terfynell_cofnod->탈출상태=SECOND_VALUE=='['?2:0;Terfynell_cofnod->paramedr_INDEX=0;for(unsigned 순번=0;순번<4;순번++)Terfynell_cofnod->paramedr_VALUE[순번]=0;}
    else if(Terfynell_cofnod->탈출상태==2){if(SECOND_VALUE=='?'){}else if(SECOND_VALUE>='0'&&SECOND_VALUE<='9'){if(Terfynell_cofnod->paramedr_VALUE[Terfynell_cofnod->paramedr_INDEX]<10000)Terfynell_cofnod->paramedr_VALUE[Terfynell_cofnod->paramedr_INDEX]=Terfynell_cofnod->paramedr_VALUE[Terfynell_cofnod->paramedr_INDEX]*10+SECOND_VALUE-'0';}else if(SECOND_VALUE==';'&&Terfynell_cofnod->paramedr_INDEX<3)Terfynell_cofnod->paramedr_INDEX++;else{dolen_rheoli_SEQUENCE(SECOND_VALUE);Terfynell_cofnod->탈출상태=0;}}
    else if(SECOND_VALUE==27){Terfynell_cofnod->긴부호없는값=0;Terfynell_cofnod->탈출상태=1;}else{
        if(Terfynell_cofnod->긴부호없는값&&(SECOND_VALUE&0xc0)!=0x80){Terfynell_cofnod->긴부호없는값=0;cod_nod_451f2815(0xfffd);}
        if(Terfynell_cofnod->긴부호없는값){Terfynell_cofnod->부호없는결과=Terfynell_cofnod->부호없는결과*64+(SECOND_VALUE&63);if(--Terfynell_cofnod->긴부호없는값==0)cod_nod_451f2815(Terfynell_cofnod->부호없는결과<Terfynell_cofnod->SMALL_VALUE||Terfynell_cofnod->부호없는결과>0x10ffff||(Terfynell_cofnod->부호없는결과>=0xd800&&Terfynell_cofnod->부호없는결과<=0xdfff)?0xfffd:Terfynell_cofnod->부호없는결과);}
        else if(SECOND_VALUE<128)cod_nod_451f2815(SECOND_VALUE);else if(SECOND_VALUE>=0xc2&&SECOND_VALUE<=0xf4){Terfynell_cofnod->긴부호없는값=SECOND_VALUE<0xe0?1:SECOND_VALUE<0xf0?2:3;Terfynell_cofnod->부호없는결과=SECOND_VALUE&((1u<<(6-Terfynell_cofnod->긴부호없는값))-1);Terfynell_cofnod->SMALL_VALUE=Terfynell_cofnod->긴부호없는값==1?128:Terfynell_cofnod->긴부호없는값==2?2048:65536;}else cod_nod_451f2815(0xfffd);
    }to_bach_VALUE(1);
}
int Terfynell_yn_disgwyl(void){return technoleg_gwybodaeth_yn_disgwyl!=0;}
/* 모서리 INDEX: 1 좌상, 2 우상, 3 좌하, 4 우하. */
static int ailfeintio_llusgo=-1,잡은모서리,잡은가로,잡은세로,처음가로,처음세로,처음너비,처음높이;
static int 가리킨창(int 가로,int Ar_i_fyny_safle) {
    for(int SEQUENCE_VALUE=cofnod_COUNT-1;SEQUENCE_VALUE>=0;SEQUENCE_VALUE--){
        int dynodwr_VALUE=trefn_VALUE[SEQUENCE_VALUE];Terfynell_d413d4bc *ffenestr=&Windows_Rhestr[dynodwr_VALUE];
        if(가로>=(int)ffenestr->cyfesuryn_x&&Ar_i_fyny_safle>=(int)ffenestr->Y_cyfesuryn&&
           가로<(int)(ffenestr->cyfesuryn_x+ffenestr->너비)&&Ar_i_fyny_safle<(int)(ffenestr->Y_cyfesuryn+ffenestr->높이))return dynodwr_VALUE;
    }return -1;
}
static int 모서리찾기(int dynodwr_VALUE,int 가로,int Ar_i_fyny_safle) {
    if(dynodwr_VALUE<0)return 0;Terfynell_d413d4bc *ffenestr=&Windows_Rhestr[dynodwr_VALUE];
    int 왼쪽=가로<(int)ffenestr->cyfesuryn_x+8,RIGHT=가로>=(int)(ffenestr->cyfesuryn_x+ffenestr->너비)-8;
    int 위쪽=Ar_i_fyny_safle<(int)ffenestr->Y_cyfesuryn+8,아래쪽=Ar_i_fyny_safle>=(int)(ffenestr->Y_cyfesuryn+ffenestr->높이)-8;
    return (왼쪽||RIGHT)&&(위쪽||아래쪽)?1+RIGHT+아래쪽*2:0;
}
static int gwahanydd_VALUE(int VALUE,int 최소,int 최대){return VALUE<최소?최소:VALUE>최대?최대:VALUE;}
static void symud_ailfeintio(int 가로,int Ar_i_fyny_safle) {
    Terfynell_d413d4bc *ffenestr=&Windows_Rhestr[ailfeintio_llusgo];int 왼쪽=처음가로,위쪽=처음세로,RIGHT=처음가로+처음너비,아래쪽=처음세로+처음높이;
    if(잡은모서리==1||잡은모서리==3)왼쪽=gwahanydd_VALUE(처음가로+가로-잡은가로,0,RIGHT-360);
    else RIGHT=gwahanydd_VALUE(처음가로+처음너비+가로-잡은가로,왼쪽+360,보드화면너비());
    if(잡은모서리<=2)위쪽=gwahanydd_VALUE(처음세로+Ar_i_fyny_safle-잡은세로,34,아래쪽-216);
    else 아래쪽=gwahanydd_VALUE(처음세로+처음높이+Ar_i_fyny_safle-잡은세로,위쪽+216,보드화면높이());
    unsigned COLUMNS=(RIGHT-왼쪽-24)/8,ROW_COUNT=(아래쪽-위쪽-56)/16;
    if(ffenestr->COLUMNS!=COLUMNS||ffenestr->ROW_COUNT!=ROW_COUNT){
        ffenestr->크기바뀜=1;ffenestr->COLUMNS=COLUMNS;ffenestr->ROW_COUNT=ROW_COUNT;
        if(ffenestr->COLUMN_safle>=COLUMNS)ffenestr->COLUMN_safle=COLUMNS-1;
        if(ffenestr->ROW_safle>=ffenestr->맨위+ROW_COUNT)ffenestr->맨위=ffenestr->ROW_safle-ROW_COUNT+1;
        unsigned 한도=ffenestr->맨위;if(한도>Hanes_llinell_COUNT-ROW_COUNT)한도=Hanes_llinell_COUNT-ROW_COUNT;
        if(ffenestr->sgrolio>한도)ffenestr->sgrolio=한도;
    }
    int 옛가로=ffenestr->cyfesuryn_x,옛세로=ffenestr->Y_cyfesuryn,옛폭=ffenestr->너비,옛길이=ffenestr->높이;
    if(옛가로==왼쪽&&옛세로==위쪽&&옛폭==RIGHT-왼쪽&&옛길이==아래쪽-위쪽)return;
    ffenestr->cyfesuryn_x=왼쪽;ffenestr->Y_cyfesuryn=위쪽;ffenestr->너비=RIGHT-왼쪽;ffenestr->높이=아래쪽-위쪽;
    창자리그리기(옛가로,옛세로,옛폭,옛길이,ffenestr);
}
void Terfynell_pwyntydd(unsigned Nesaf_eitem,int cyfesuryn_x,int Y_cyfesuryn){
    unsigned 눌림=Nesaf_eitem&~단추들;단추들=Nesaf_eitem;
    if(!bwrdd_gwaith_Gwedd){llusgo_VALUE=-1;ailfeintio_llusgo=-1;bwrdd_pwyntydd(cyfesuryn_x,Y_cyfesuryn,1);return;}
    if(!(Nesaf_eitem&1)){llusgo_VALUE=-1;ailfeintio_llusgo=-1;}
    if(ailfeintio_llusgo>=0&&!Windows_Rhestr[ailfeintio_llusgo].살아있음)ailfeintio_llusgo=-1;
    if(llusgo_VALUE>=0&&!Windows_Rhestr[llusgo_VALUE].살아있음)llusgo_VALUE=-1;
    if(ailfeintio_llusgo>=0){
        symud_ailfeintio(cyfesuryn_x,Y_cyfesuryn);bwrdd_pwyntydd(cyfesuryn_x,Y_cyfesuryn,잡은모서리==1||잡은모서리==4?2:3);return;
    }
    bwrdd_pwyntydd(cyfesuryn_x,Y_cyfesuryn,1);
    if(llusgo_VALUE>=0){
        Terfynell_d413d4bc *ffenestr=&Windows_Rhestr[llusgo_VALUE];
        int 옛가로=ffenestr->cyfesuryn_x,옛세로=ffenestr->Y_cyfesuryn;
        ffenestr->cyfesuryn_x=gwahanydd_VALUE(cyfesuryn_x-llusgo_X,0,보드화면너비()-ffenestr->너비);
        ffenestr->Y_cyfesuryn=gwahanydd_VALUE(Y_cyfesuryn-llusgo_Y,34,보드화면높이()-ffenestr->높이);
        if(옛가로!=(int)ffenestr->cyfesuryn_x||옛세로!=(int)ffenestr->Y_cyfesuryn)창자리그리기(옛가로,옛세로,ffenestr->너비,ffenestr->높이,ffenestr);
        return;
    }
    extern int 화면덮음(int,int,int);
    if(화면덮음(Ffocws,cyfesuryn_x,Y_cyfesuryn)){화면가리킴(Ffocws,눌림,cyfesuryn_x,Y_cyfesuryn);return;}
    int dynodwr_VALUE=가리킨창(cyfesuryn_x,Y_cyfesuryn),모서리=모서리찾기(dynodwr_VALUE,cyfesuryn_x,Y_cyfesuryn);
    if(모서리)bwrdd_pwyntydd(cyfesuryn_x,Y_cyfesuryn,모서리==1||모서리==4?2:3);
    if(눌림&1){
        if(모서리){
            Terfynell_d413d4bc *ffenestr=&Windows_Rhestr[dynodwr_VALUE];ailfeintio_llusgo=dynodwr_VALUE;잡은모서리=모서리;잡은가로=cyfesuryn_x;잡은세로=Y_cyfesuryn;
            처음가로=ffenestr->cyfesuryn_x;처음세로=ffenestr->Y_cyfesuryn;처음너비=ffenestr->너비;처음높이=ffenestr->높이;
            if(dynodwr_VALUE!=Ffocws)앞으로올리기(dynodwr_VALUE);return;
        }
        if(Y_cyfesuryn<32&&cyfesuryn_x>=6&&cyfesuryn_x<142){Creu_cofnod();return;}
        if(Y_cyfesuryn<32&&cyfesuryn_x>=154&&cyfesuryn_x<602){앞으로올리기((cyfesuryn_x-154)/112);return;}
        if(dynodwr_VALUE>=0){
            Terfynell_d413d4bc *ffenestr=&Windows_Rhestr[dynodwr_VALUE];
            if(Y_cyfesuryn<(int)ffenestr->Y_cyfesuryn+30&&cyfesuryn_x>=(int)(ffenestr->cyfesuryn_x+ffenestr->너비)-32){cau_ffenestr(dynodwr_VALUE);return;}
            if(dynodwr_VALUE!=Ffocws)앞으로올리기(dynodwr_VALUE);
            if(Y_cyfesuryn<(int)ffenestr->Y_cyfesuryn+30){llusgo_VALUE=dynodwr_VALUE;llusgo_X=cyfesuryn_x-ffenestr->cyfesuryn_x;llusgo_Y=Y_cyfesuryn-ffenestr->Y_cyfesuryn;}return;
        }
    }
    if(Ffocws>=0&&(눌림&(8|16))){Terfynell_cofnod=&Windows_Rhestr[Ffocws];if(눌림&8){unsigned 한도=Terfynell_cofnod->맨위;if(한도>Hanes_llinell_COUNT-Terfynell_cofnod->ROW_COUNT)한도=Hanes_llinell_COUNT-Terfynell_cofnod->ROW_COUNT;Terfynell_cofnod->sgrolio=Terfynell_cofnod->sgrolio+9>한도?한도:Terfynell_cofnod->sgrolio+9;}else Terfynell_cofnod->sgrolio=Terfynell_cofnod->sgrolio<9?0:Terfynell_cofnod->sgrolio-9;다시그리기();}
}
void 터미널바로가기키(unsigned 누름값){if(누름값==1)Creu_cofnod();if(누름값==2&&cofnod_COUNT)앞으로올리기(trefn_VALUE[0]);if(누름값==3)cau_ffenestr(Ffocws);}
peiriant_Word bwrdd_Terfynell(peiriant_Word Gweithrediad){
    if(Gweithrediad==300){if(!Windows_Rhestr[출력결과].살아있음)return Creu_cofnod();bwrdd_gwaith_Gwedd=1;다시그리기();return 0;}
    if(Gweithrediad==0){cau_ffenestr(Ffocws);return 0;}if(Gweithrediad==1)return (uint32_t)Creu_cofnod();if(Gweithrediad==2)return Ffocws>=0;
    if(Gweithrediad==9){bwrdd_gwaith_Gwedd=0;return 0;}if(Gweithrediad==7)return cofnod_COUNT;if(Gweithrediad==10)return Ffocws+1;if(Gweithrediad==11)return 출력결과;
    if(Gweithrediad==13){Terfynell_d413d4bc *ffenestr=&Windows_Rhestr[출력결과];return ffenestr->살아있음?(ffenestr->ROW_COUNT<<16)|ffenestr->COLUMNS:(19<<16)|68;}
    if(Gweithrediad==14){unsigned VALUE=Windows_Rhestr[출력결과].크기바뀜;Windows_Rhestr[출력결과].크기바뀜=0;return VALUE;}
    if(Gweithrediad==12){unsigned VALUE=technoleg_gwybodaeth_yn_disgwyl;technoleg_gwybodaeth_yn_disgwyl=0;return VALUE;}
    if(Gweithrediad>=20&&Gweithrediad<24)return Windows_Rhestr[Gweithrediad-20].살아있음;
    if(Gweithrediad>=100&&Gweithrediad<104){출력결과=Gweithrediad-100;Terfynell_cofnod=&Windows_Rhestr[출력결과];return 0;}
    if(Gweithrediad>=200&&Gweithrediad<204){앞으로올리기(Gweithrediad-200);return 0;}
    if(Gweithrediad==3){다시그리기();return 0;}Terfynell_cofnod=&Windows_Rhestr[출력결과];if(!Terfynell_cofnod->살아있음)return 0;
    if(Gweithrediad==4)clirio_Cynnwys();if(Gweithrediad==5||Gweithrediad==6){unsigned 이전=단추들;Terfynell_pwyntydd(Gweithrediad==5?8:16,0,0);단추들=이전;}return 1;
}
