#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* eigin 네 Gluggi 합성과 UTF-8 Skjáhermir. 바뀐 영역의 lokið_VALUE 그림만 표시한다. */
#include <stdint.h>
#include <stddef.h>
typedef uintptr_t vél_Word;
extern vél_Word bretti_díll(vél_Word,vél_Word,vél_Word),보드화면기억공간(void);
extern void *memset(void *,int,size_t);
extern const unsigned char Endastöð_leturgerð[];
#define 최대열수 237
#define ferill_lína_COUNT 160
typedef struct {
    uint32_t 글자칸들[ferill_lína_COUNT][최대열수]; uint8_t 모양들[ferill_lína_COUNT][최대열수];
    unsigned 너비,높이,COLUMNS,ROW_COUNT,크기바뀜;
    unsigned 살아있음,x_hnit,Y_hnit,ROW_staða,COLUMN_staða,맨위,fletta,전경색,배경색,탈출상태,færibreyta_VALUE[4],færibreyta_INDEX,저장행,저장열;
    unsigned 부호없는결과,긴부호없는값,SMALL_VALUE,대체화면,가리개보임;
} Endastöð;
static Endastöð Windows_Listi[4];
static int Fókus=-1,úttak_54cd5e1d,röð_VALUE[4],færsla_COUNT,draga_VALUE=-1,draga_X,draga_Y;
static unsigned upplýsingatækni_Í_bið,단추들,skjáborð_Sýn,한글입력;
static const uint32_t 색상들[16]={0x201a15,0x6060df,0x9dcc86,0x80cfea,0xefaf72,0xca96c9,0xceda76,0xede9df,0x858078,0x8888ff,0xb9eba7,0xa5eaff,0xffcc99,0xf0bef1,0xf0f0a0,0xffffff};
extern int 화면보임(int),화면가리킴(int,unsigned,int,int);
extern void 화면다시그림(int);
static Endastöð *Endastöð_færsla;
static unsigned 넓은글자(unsigned stafkóði){return stafkóði>=256?2:1;}
static void 사각영역(unsigned x_hnit,unsigned Y_hnit,unsigned 너비값,unsigned 높이값,unsigned 색상){
    보드사각그림(x_hnit,Y_hnit,너비값,높이값,색상);
}
void Endastöð_stafbrigði(unsigned x_hnit,unsigned Y_hnit,unsigned stafkóði,unsigned 전경색,unsigned 배경색){
    unsigned 너비=넓은글자(stafkóði)*8;if(stafkóði==0xffffffffu)return;
    int 왼쪽=x_hnit,위쪽=Y_hnit,폭=너비,lengd_VALUE=16;
    if(!보드그림범위(&왼쪽,&위쪽,&폭,&lengd_VALUE))return;
    if(stafkóði==' '){보드사각그림(왼쪽,위쪽,폭,lengd_VALUE,배경색);return;}
    unsigned LOOKUP_INDEX=stafkóði<65536?stafkóði:stafkóði>=0x1f600&&stafkóði<0x1f650?65536+stafkóði-0x1f600:0xfffd;
    const unsigned char *leturgerð_VALUE=Endastöð_leturgerð+LOOKUP_INDEX*32;
    for(int Lína=위쪽;Lína<위쪽+lengd_VALUE;Lína++){unsigned Background_Intelligent_Transfer_Service_Listi=leturgerð_VALUE[(Lína-Y_hnit)*2]*256+leturgerð_VALUE[(Lína-Y_hnit)*2+1];for(int rauf_færsla=왼쪽;rauf_færsla<왼쪽+폭;rauf_færsla++)bretti_díll(rauf_færsla,Lína,(Background_Intelligent_Transfer_Service_Listi&(0x8000>>(rauf_færsla-x_hnit)))?전경색:배경색);}
}
static void heiti_tafla(unsigned x_hnit,unsigned Y_hnit,const char *strengur_gögn,unsigned 전경색,unsigned 배경색){while(*strengur_gögn){unsigned stafkóði=(unsigned char)*strengur_gögn++, 남은수=0;if(stafkóði>=0xc0){남은수=stafkóði<0xe0?1:stafkóði<0xf0?2:3;stafkóði&=(1u<<(6-남은수))-1;while(남은수--&&*strengur_gögn)stafkóði=(stafkóði<<6)|((unsigned char)*strengur_gögn++&63);}Endastöð_stafbrigði(x_hnit,Y_hnit,stafkóði,전경색,배경색);x_hnit+=넓은글자(stafkóði)*8;}}
static unsigned 첫항목(void){return Endastöð_færsla->맨위;}
static int 보이는지(void){return Endastöð_færsla->살아있음&&Fókus>=0&&Endastöð_færsla==&Windows_Listi[Fókus]&&!화면보임(Fókus);}
static void 그리기(unsigned ROW_staða,unsigned COLUMN_staða){
    if(!보이는지()||ROW_staða<첫항목()-Endastöð_færsla->fletta||ROW_staða>=첫항목()-Endastöð_færsla->fletta+Endastöð_færsla->ROW_COUNT||COLUMN_staða>=Endastöð_færsla->COLUMNS)return;
    unsigned stafkóði=Endastöð_færsla->글자칸들[ROW_staða%ferill_lína_COUNT][COLUMN_staða],strengur_gögn=Endastöð_færsla->모양들[ROW_staða%ferill_lína_COUNT][COLUMN_staða];
    if(넓은글자(stafkóði)==2&&COLUMN_staða+1>=Endastöð_færsla->COLUMNS)stafkóði=' ';
    Endastöð_stafbrigði(Endastöð_færsla->x_hnit+12+COLUMN_staða*8,Endastöð_færsla->Y_hnit+36+(ROW_staða-첫항목()+Endastöð_færsla->fletta)*16,stafkóði?stafkóði:' ',색상들[strengur_gögn&15],색상들[strengur_gögn>>4]);
}
static void innskotsmerki_VALUE(int sýna_gluggi){if(!보이는지()||Endastöð_færsla->fletta||Endastöð_færsla->COLUMN_staða>=Endastöð_færsla->COLUMNS||Endastöð_færsla->ROW_staða<Endastöð_færsla->맨위||Endastöð_færsla->ROW_staða>=Endastöð_færsla->맨위+Endastöð_færsla->ROW_COUNT)return;
    if(!sýna_gluggi||!Endastöð_færsla->가리개보임)그리기(Endastöð_færsla->ROW_staða,Endastöð_færsla->COLUMN_staða);else 사각영역(Endastöð_færsla->x_hnit+12+Endastöð_færsla->COLUMN_staða*8,Endastöð_færsla->Y_hnit+36+(Endastöð_færsla->ROW_staða-Endastöð_færsla->맨위)*16+14,8,2,색상들[Endastöð_færsla->전경색]);}
static void Efni_VALUE(void){
    사각영역(Endastöð_færsla->x_hnit+12,Endastöð_færsla->Y_hnit+36,Endastöð_færsla->COLUMNS*8,Endastöð_færsla->ROW_COUNT*16,색상들[0]);
    int 가로=Endastöð_færsla->x_hnit+12,Lóðrétt_staða=Endastöð_færsla->Y_hnit+36,폭=Endastöð_færsla->COLUMNS*8,lengd_VALUE=Endastöð_færsla->ROW_COUNT*16;
    if(보드그림범위(&가로,&Lóðrétt_staða,&폭,&lengd_VALUE)){
    unsigned 첫줄=(Lóðrétt_staða-Endastöð_færsla->Y_hnit-36)/16,끝줄=(Lóðrétt_staða+lengd_VALUE-Endastöð_færsla->Y_hnit-36+15)/16;
    unsigned 첫칸=(가로-Endastöð_færsla->x_hnit-12)/8,끝칸=(가로+폭-Endastöð_færsla->x_hnit-12+7)/8;
    if(첫칸)첫칸--; /* 잘림 경계 왼쪽에서 시작한 두 rauf_færsla 글자도 그린다. */
    for(unsigned 반환값=첫줄;반환값<끝줄;반환값++)for(unsigned stafkóði=첫칸;stafkóði<끝칸;stafkóði++){
        unsigned ROW_staða=첫항목()-Endastöð_færsla->fletta+반환값,stafur_VALUE=Endastöð_færsla->글자칸들[ROW_staða%ferill_lína_COUNT][stafkóði],strengur_gögn=Endastöð_færsla->모양들[ROW_staða%ferill_lína_COUNT][stafkóði];
        if(넓은글자(stafur_VALUE)==2&&stafkóði+1>=Endastöð_færsla->COLUMNS)stafur_VALUE=' ';
        if((stafur_VALUE==0||stafur_VALUE==' ')&&(strengur_gögn>>4)==0)continue;
        Endastöð_stafbrigði(Endastöð_færsla->x_hnit+12+stafkóði*8,Endastöð_færsla->Y_hnit+36+반환값*16,stafur_VALUE?stafur_VALUE:' ',색상들[strengur_gögn&15],색상들[strengur_gögn>>4]);
    }}
    heiti_tafla(Endastöð_færsla->x_hnit+12,Endastöð_færsla->Y_hnit+Endastöð_færsla->높이-18,Endastöð_færsla->fletta?"PgDn: recent output":Endastöð_færsla->너비>=500?"F6: next | Corner + left drag: resize":"Corner + left drag: resize",0xece8e2,0x403127);innskotsmerki_VALUE(1);
}
static void 실행틀(int auðkenni_VALUE){
    Endastöð_færsla=&Windows_Listi[auðkenni_VALUE];
    int 가로=Endastöð_færsla->x_hnit,Lóðrétt_staða=Endastöð_færsla->Y_hnit,폭=Endastöð_færsla->너비,lengd_VALUE=Endastöð_færsla->높이;
    if(!보드그림범위(&가로,&Lóðrétt_staða,&폭,&lengd_VALUE))return;
    사각영역(Endastöð_færsla->x_hnit,Endastöð_færsla->Y_hnit,Endastöð_færsla->너비,Endastöð_færsla->높이,0x403127);
    unsigned 색상=auðkenni_VALUE==Fókus?0x905020:0x604438;사각영역(Endastöð_færsla->x_hnit,Endastöð_færsla->Y_hnit,Endastöð_færsla->너비,30,색상);
    heiti_tafla(Endastöð_færsla->x_hnit+12,Endastöð_færsla->Y_hnit+7,"JKOROS Terminal",0xffffff,색상);
    char 수치[2]={(char)('1'+auðkenni_VALUE),0};heiti_tafla(Endastöð_færsla->x_hnit+148,Endastöð_færsla->Y_hnit+7,수치,0xffffff,색상);
    heiti_tafla(Endastöð_færsla->x_hnit+240,Endastöð_færsla->Y_hnit+7,Endastöð_færsla->너비>=500?(한글입력?"[IS] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[IS]":"[EN]"),0xffffff,색상);
    사각영역(Endastöð_færsla->x_hnit+Endastöð_færsla->너비-32,Endastöð_færsla->Y_hnit+4,26,22,0x5555b8);heiti_tafla(Endastöð_færsla->x_hnit+Endastöð_færsla->너비-24,Endastöð_færsla->Y_hnit+7,"X",0xffffff,0x5555b8);
    Efni_VALUE();
}
static void 장면그리기(void){
    if(!skjáborð_Sýn)return;사각영역(0,0,보드화면너비(),보드화면높이(),0x302018);사각영역(0,0,보드화면너비(),32,0x403127);
    사각영역(6,4,136,24,0x905020);heiti_tafla(14,8,"+ New terminal",0xffffff,0x905020);
    for(int 순번=0;순번<4;순번++)if(Windows_Listi[순번].살아있음){unsigned stafkóði=Fókus==순번?0x905020:0x604438;사각영역(154+순번*112,4,106,24,stafkóði);heiti_tafla(160+순번*112,8,"Terminal",0xffffff,stafkóði);char strengur_gögn[2]={(char)('1'+순번),0};heiti_tafla(232+순번*112,8,strengur_gögn,0xffffff,stafkóði);}
    if(!færsla_COUNT)heiti_tafla(140,210,"Click + New terminal to start",0xede9df,0x302018);
    for(int 순번=0;순번<færsla_COUNT;순번++)실행틀(röð_VALUE[순번]);화면다시그림(Fókus);Endastöð_færsla=&Windows_Listi[úttak_54cd5e1d];
}
static void 영역그리기(int 가로,int Lóðrétt_staða,int 폭,int lengd_VALUE){
    if(!skjáborð_Sýn||!보드그림범위(&가로,&Lóðrétt_staða,&폭,&lengd_VALUE))return;
    for(int Lína=Lóðrétt_staða;Lína<Lóðrétt_staða+lengd_VALUE;Lína+=32){
        int 띠높이=Lóðrétt_staða+lengd_VALUE-Lína;if(띠높이>32)띠높이=32;
        if(bretti_Opna_teikning(가로,Lína,폭,띠높이)){장면그리기();bretti_Ljúka_teikning();}
    }
}
static void 다시그리기(void){영역그리기(0,0,보드화면너비(),보드화면높이());}
/* 서로 겹치지 않는 새 Gluggi 영역과 이전 자리의 네 띠를 복구한다. */
static void 창자리그리기(int 가로,int Lóðrétt_staða,int 폭,int lengd_VALUE,Endastöð *Gluggi){
    int 왼쪽=가로>(int)Gluggi->x_hnit?가로:(int)Gluggi->x_hnit;
    int 위쪽=Lóðrétt_staða>(int)Gluggi->Y_hnit?Lóðrétt_staða:(int)Gluggi->Y_hnit;
    int RIGHT=가로+폭<(int)(Gluggi->x_hnit+Gluggi->너비)?가로+폭:(int)(Gluggi->x_hnit+Gluggi->너비);
    int 아래쪽=Lóðrétt_staða+lengd_VALUE<(int)(Gluggi->Y_hnit+Gluggi->높이)?Lóðrétt_staða+lengd_VALUE:(int)(Gluggi->Y_hnit+Gluggi->높이);
    영역그리기(Gluggi->x_hnit,Gluggi->Y_hnit,Gluggi->너비,Gluggi->높이);
    if(왼쪽>=RIGHT||위쪽>=아래쪽){영역그리기(가로,Lóðrétt_staða,폭,lengd_VALUE);return;}
    영역그리기(가로,Lóðrétt_staða,폭,위쪽-Lóðrétt_staða);
    영역그리기(가로,아래쪽,폭,Lóðrétt_staða+lengd_VALUE-아래쪽);
    영역그리기(가로,위쪽,왼쪽-가로,아래쪽-위쪽);
    영역그리기(RIGHT,위쪽,가로+폭-RIGHT,아래쪽-위쪽);
}
static void merki_Fókus(void){upplýsingatækni_Í_bið=(upplýsingatækni_Í_bið&~15u)|(unsigned)(Fókus+1)|0x10000;}
void 터미널입력방식(unsigned 한글여부){
    한글입력=한글여부!=0;
    /* Update title bars only: a mode switch must not erase an EL0 drawing. */
    if(Fókus>=0){
        Endastöð *gluggi_færsla=&Windows_Listi[Fókus];
        heiti_tafla(gluggi_færsla->x_hnit+240,gluggi_færsla->Y_hnit+7,gluggi_færsla->너비>=500?(한글입력?"[IS] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[IS]":"[EN]"),0xffffff,0x905020);
    }
}
static void 앞으로올리기(int auðkenni_VALUE){if(auðkenni_VALUE<0||auðkenni_VALUE>=4||!Windows_Listi[auðkenni_VALUE].살아있음)return;int 현재위치=0;while(현재위치<færsla_COUNT&&röð_VALUE[현재위치]!=auðkenni_VALUE)현재위치++;for(;현재위치+1<færsla_COUNT;현재위치++)röð_VALUE[현재위치]=röð_VALUE[현재위치+1];röð_VALUE[færsla_COUNT-1]=auðkenni_VALUE;Fókus=auðkenni_VALUE;merki_Fókus();다시그리기();}
static void 빈칸채우기(unsigned ROW_staða){for(unsigned stafkóði=0;stafkóði<최대열수;stafkóði++){Endastöð_færsla->글자칸들[ROW_staða%ferill_lína_COUNT][stafkóði]=0;Endastöð_færsla->모양들[ROW_staða%ferill_lína_COUNT][stafkóði]=Endastöð_færsla->전경색|(Endastöð_færsla->배경색<<4);}}
static void hreinsa_Innihald(void){Endastöð_færsla->ROW_staða=Endastöð_færsla->COLUMN_staða=Endastöð_færsla->맨위=Endastöð_færsla->fletta=0;for(unsigned 반환값=0;반환값<ferill_lína_COUNT;반환값++)빈칸채우기(반환값);if(보이는지())Efni_VALUE();}
static int stofna_færsla(void){
    if(!보드화면기억공간())return -19;int auðkenni_VALUE=0;while(auðkenni_VALUE<4&&Windows_Listi[auðkenni_VALUE].살아있음)auðkenni_VALUE++;if(auðkenni_VALUE==4)return -28;
    skjáborð_Sýn=1;Endastöð_færsla=&Windows_Listi[auðkenni_VALUE];memset(Endastöð_færsla,0,sizeof(*Endastöð_færsla));Endastöð_færsla->살아있음=1;Endastöð_færsla->너비=568;Endastöð_færsla->높이=360;Endastöð_færsla->COLUMNS=68;Endastöð_færsla->ROW_COUNT=19;Endastöð_færsla->x_hnit=12+auðkenni_VALUE*16;Endastöð_færsla->Y_hnit=48+auðkenni_VALUE*18;Endastöð_færsla->전경색=7;Endastöð_færsla->가리개보임=1;
    for(unsigned 반환값=0;반환값<ferill_lína_COUNT;반환값++)빈칸채우기(반환값);röð_VALUE[færsla_COUNT++]=auðkenni_VALUE;Fókus=auðkenni_VALUE;upplýsingatækni_Í_bið|=1u<<(4+auðkenni_VALUE);merki_Fókus();다시그리기();return auðkenni_VALUE+1;
}
static void loka_gluggi(int auðkenni_VALUE){
    if(auðkenni_VALUE<0||auðkenni_VALUE>=4||!Windows_Listi[auðkenni_VALUE].살아있음)return;Windows_Listi[auðkenni_VALUE].살아있음=0;upplýsingatækni_Í_bið|=1u<<(8+auðkenni_VALUE);
    int 현재위치=0;while(현재위치<færsla_COUNT&&röð_VALUE[현재위치]!=auðkenni_VALUE)현재위치++;for(;현재위치+1<færsla_COUNT;현재위치++)röð_VALUE[현재위치]=röð_VALUE[현재위치+1];færsla_COUNT--;
    if(Fókus==auðkenni_VALUE)Fókus=færsla_COUNT?röð_VALUE[færsla_COUNT-1]:-1;merki_Fókus();다시그리기();
}
static void 줄바꿈(void){Endastöð_færsla->COLUMN_staða=0;Endastöð_færsla->ROW_staða++;if(Endastöð_færsla->ROW_staða>=Endastöð_færsla->맨위+Endastöð_færsla->ROW_COUNT){Endastöð_færsla->맨위++;빈칸채우기(Endastöð_færsla->ROW_staða);if(보이는지())Efni_VALUE();}}
static void stafkóði_451f2815(unsigned stafkóði){
    if(stafkóði==13){Endastöð_færsla->COLUMN_staða=0;return;}if(stafkóði==10){줄바꿈();return;}if(stafkóði==8){if(Endastöð_færsla->COLUMN_staða)Endastöð_færsla->COLUMN_staða--;return;}
    if(stafkóði==9){unsigned vara_COUNT=8-Endastöð_færsla->COLUMN_staða%8;while(vara_COUNT--)stafkóði_451f2815(' ');return;}if(stafkóði<32||stafkóði==127)return;
    unsigned 너비값=넓은글자(stafkóði);if(Endastöð_færsla->COLUMN_staða+너비값>Endastöð_færsla->COLUMNS)줄바꿈();
    if(Endastöð_færsla->글자칸들[Endastöð_færsla->ROW_staða%ferill_lína_COUNT][Endastöð_færsla->COLUMN_staða]==0xffffffffu&&Endastöð_færsla->COLUMN_staða){Endastöð_færsla->글자칸들[Endastöð_færsla->ROW_staða%ferill_lína_COUNT][Endastöð_færsla->COLUMN_staða-1]=' ';그리기(Endastöð_færsla->ROW_staða,Endastöð_færsla->COLUMN_staða-1);}
    if(넓은글자(Endastöð_færsla->글자칸들[Endastöð_færsla->ROW_staða%ferill_lína_COUNT][Endastöð_færsla->COLUMN_staða])==2&&Endastöð_færsla->COLUMN_staða+1<Endastöð_færsla->COLUMNS){Endastöð_færsla->글자칸들[Endastöð_færsla->ROW_staða%ferill_lína_COUNT][Endastöð_færsla->COLUMN_staða+1]=' ';그리기(Endastöð_færsla->ROW_staða,Endastöð_færsla->COLUMN_staða+1);}
    Endastöð_færsla->글자칸들[Endastöð_færsla->ROW_staða%ferill_lína_COUNT][Endastöð_færsla->COLUMN_staða]=stafkóði;Endastöð_færsla->모양들[Endastöð_færsla->ROW_staða%ferill_lína_COUNT][Endastöð_færsla->COLUMN_staða]=Endastöð_færsla->전경색|(Endastöð_færsla->배경색<<4);
    if(너비값==2)Endastöð_færsla->글자칸들[Endastöð_færsla->ROW_staða%ferill_lína_COUNT][Endastöð_færsla->COLUMN_staða+1]=0xffffffffu;
    그리기(Endastöð_færsla->ROW_staða,Endastöð_færsla->COLUMN_staða);Endastöð_færsla->COLUMN_staða+=너비값;
}
static void hald_stýring_SEQUENCE(unsigned stafkóði){
    unsigned vara_COUNT=Endastöð_færsla->færibreyta_VALUE[0]?Endastöð_færsla->færibreyta_VALUE[0]:1;
    if(stafkóði=='m')for(unsigned 순번=0;순번<=Endastöð_færsla->færibreyta_INDEX;순번++){unsigned gögn_staða=Endastöð_færsla->færibreyta_VALUE[순번];if(!gögn_staða){Endastöð_færsla->전경색=7;Endastöð_færsla->배경색=0;}if(gögn_staða==1&&Endastöð_færsla->전경색<8)Endastöð_færsla->전경색+=8;if(gögn_staða==7){unsigned 유지=Endastöð_færsla->전경색;Endastöð_færsla->전경색=Endastöð_færsla->배경색;Endastöð_færsla->배경색=유지;}if(gögn_staða>=30&&gögn_staða<=37)Endastöð_færsla->전경색=gögn_staða-30;if(gögn_staða>=90&&gögn_staða<=97)Endastöð_færsla->전경색=gögn_staða-90+8;if(gögn_staða>=40&&gögn_staða<=47)Endastöð_færsla->배경색=gögn_staða-40;if(gögn_staða>=100&&gögn_staða<=107)Endastöð_færsla->배경색=gögn_staða-100+8;if(gögn_staða==39)Endastöð_færsla->전경색=7;if(gögn_staða==49)Endastöð_færsla->배경색=0;}
    if(stafkóði=='J'&&(Endastöð_færsla->færibreyta_VALUE[0]==2||Endastöð_færsla->færibreyta_VALUE[0]==3))hreinsa_Innihald();
    if(stafkóði=='K'){unsigned 출발위치=Endastöð_færsla->færibreyta_VALUE[0]==2?0:Endastöð_færsla->COLUMN_staða,도착위치=Endastöð_færsla->færibreyta_VALUE[0]==1?Endastöð_færsla->COLUMN_staða+1:Endastöð_færsla->COLUMNS;if(Endastöð_færsla->færibreyta_VALUE[0]==1)출발위치=0;for(unsigned 순번=출발위치;순번<도착위치&&순번<Endastöð_færsla->COLUMNS;순번++){
        unsigned ROW_VALUE=Endastöð_færsla->ROW_staða%ferill_lína_COUNT,stafur_VALUE=Endastöð_færsla->글자칸들[ROW_VALUE][순번],form_VALUE=Endastöð_færsla->전경색|(Endastöð_færsla->배경색<<4);
        /* 넓은 vi 화면에서도 이미 빈 칸의 leturgerð_VALUE 화소를 되풀이해 칠하지 않는다. */
        int 바뀜=(stafur_VALUE!=0&&stafur_VALUE!=' ')||Endastöð_færsla->모양들[ROW_VALUE][순번]!=form_VALUE;
        Endastöð_færsla->글자칸들[ROW_VALUE][순번]=' ';Endastöð_færsla->모양들[ROW_VALUE][순번]=form_VALUE;
        if(바뀜)그리기(Endastöð_færsla->ROW_staða,순번);
    }}
    if(stafkóði=='D')Endastöð_færsla->COLUMN_staða=vara_COUNT>Endastöð_færsla->COLUMN_staða?0:Endastöð_færsla->COLUMN_staða-vara_COUNT;if(stafkóði=='C')Endastöð_færsla->COLUMN_staða=Endastöð_færsla->COLUMN_staða+vara_COUNT>=Endastöð_færsla->COLUMNS?Endastöð_færsla->COLUMNS-1:Endastöð_færsla->COLUMN_staða+vara_COUNT;
    if(stafkóði=='G')Endastöð_færsla->COLUMN_staða=vara_COUNT>Endastöð_færsla->COLUMNS?Endastöð_færsla->COLUMNS-1:vara_COUNT-1;if(stafkóði=='A')Endastöð_færsla->ROW_staða=vara_COUNT>Endastöð_færsla->ROW_staða-Endastöð_færsla->맨위?Endastöð_færsla->맨위:Endastöð_færsla->ROW_staða-vara_COUNT;
    if(stafkóði=='B')Endastöð_færsla->ROW_staða=Endastöð_færsla->ROW_staða+vara_COUNT>=Endastöð_færsla->맨위+Endastöð_færsla->ROW_COUNT?Endastöð_færsla->맨위+Endastöð_færsla->ROW_COUNT-1:Endastöð_færsla->ROW_staða+vara_COUNT;
    if(stafkóði=='H'||stafkóði=='f'){Endastöð_færsla->ROW_staða=Endastöð_færsla->맨위+(vara_COUNT>Endastöð_færsla->ROW_COUNT?Endastöð_færsla->ROW_COUNT:vara_COUNT)-1;unsigned x_hnit=Endastöð_færsla->færibreyta_VALUE[1]?Endastöð_færsla->færibreyta_VALUE[1]:1;Endastöð_færsla->COLUMN_staða=(x_hnit>Endastöð_færsla->COLUMNS?Endastöð_færsla->COLUMNS:x_hnit)-1;}
    if(stafkóði=='s'){Endastöð_færsla->저장행=Endastöð_færsla->ROW_staða;Endastöð_færsla->저장열=Endastöð_færsla->COLUMN_staða;}if(stafkóði=='u'){Endastöð_færsla->ROW_staða=Endastöð_færsla->저장행;Endastöð_færsla->COLUMN_staða=Endastöð_færsla->저장열<Endastöð_færsla->COLUMNS?Endastöð_færsla->저장열:Endastöð_færsla->COLUMNS-1;}
    if((stafkóði=='h'||stafkóði=='l')&&Endastöð_færsla->færibreyta_VALUE[0]==25)Endastöð_færsla->가리개보임=stafkóði=='h';
}
void Endastöð_bæti(unsigned SECOND_VALUE){
    Endastöð_færsla=&Windows_Listi[úttak_54cd5e1d];if(!Endastöð_færsla->살아있음)return;innskotsmerki_VALUE(0);if(Endastöð_færsla->fletta){Endastöð_færsla->fletta=0;if(보이는지())Efni_VALUE();}
    if(Endastöð_færsla->탈출상태==1){Endastöð_færsla->탈출상태=SECOND_VALUE=='['?2:0;Endastöð_færsla->færibreyta_INDEX=0;for(unsigned 순번=0;순번<4;순번++)Endastöð_færsla->færibreyta_VALUE[순번]=0;}
    else if(Endastöð_færsla->탈출상태==2){if(SECOND_VALUE=='?'){}else if(SECOND_VALUE>='0'&&SECOND_VALUE<='9'){if(Endastöð_færsla->færibreyta_VALUE[Endastöð_færsla->færibreyta_INDEX]<10000)Endastöð_færsla->færibreyta_VALUE[Endastöð_færsla->færibreyta_INDEX]=Endastöð_færsla->færibreyta_VALUE[Endastöð_færsla->færibreyta_INDEX]*10+SECOND_VALUE-'0';}else if(SECOND_VALUE==';'&&Endastöð_færsla->færibreyta_INDEX<3)Endastöð_færsla->færibreyta_INDEX++;else{hald_stýring_SEQUENCE(SECOND_VALUE);Endastöð_færsla->탈출상태=0;}}
    else if(SECOND_VALUE==27){Endastöð_færsla->긴부호없는값=0;Endastöð_færsla->탈출상태=1;}else{
        if(Endastöð_færsla->긴부호없는값&&(SECOND_VALUE&0xc0)!=0x80){Endastöð_færsla->긴부호없는값=0;stafkóði_451f2815(0xfffd);}
        if(Endastöð_færsla->긴부호없는값){Endastöð_færsla->부호없는결과=Endastöð_færsla->부호없는결과*64+(SECOND_VALUE&63);if(--Endastöð_færsla->긴부호없는값==0)stafkóði_451f2815(Endastöð_færsla->부호없는결과<Endastöð_færsla->SMALL_VALUE||Endastöð_færsla->부호없는결과>0x10ffff||(Endastöð_færsla->부호없는결과>=0xd800&&Endastöð_færsla->부호없는결과<=0xdfff)?0xfffd:Endastöð_færsla->부호없는결과);}
        else if(SECOND_VALUE<128)stafkóði_451f2815(SECOND_VALUE);else if(SECOND_VALUE>=0xc2&&SECOND_VALUE<=0xf4){Endastöð_færsla->긴부호없는값=SECOND_VALUE<0xe0?1:SECOND_VALUE<0xf0?2:3;Endastöð_færsla->부호없는결과=SECOND_VALUE&((1u<<(6-Endastöð_færsla->긴부호없는값))-1);Endastöð_færsla->SMALL_VALUE=Endastöð_færsla->긴부호없는값==1?128:Endastöð_færsla->긴부호없는값==2?2048:65536;}else stafkóði_451f2815(0xfffd);
    }innskotsmerki_VALUE(1);
}
int Endastöð_Í_bið(void){return upplýsingatækni_Í_bið!=0;}
/* 모서리 INDEX: 1 좌상, 2 우상, 3 좌하, 4 우하. */
static int breyta_stærð_draga=-1,잡은모서리,잡은가로,잡은세로,처음가로,처음세로,처음너비,처음높이;
static int 가리킨창(int 가로,int Lóðrétt_staða) {
    for(int SEQUENCE_VALUE=færsla_COUNT-1;SEQUENCE_VALUE>=0;SEQUENCE_VALUE--){
        int auðkenni_VALUE=röð_VALUE[SEQUENCE_VALUE];Endastöð *Gluggi=&Windows_Listi[auðkenni_VALUE];
        if(가로>=(int)Gluggi->x_hnit&&Lóðrétt_staða>=(int)Gluggi->Y_hnit&&
           가로<(int)(Gluggi->x_hnit+Gluggi->너비)&&Lóðrétt_staða<(int)(Gluggi->Y_hnit+Gluggi->높이))return auðkenni_VALUE;
    }return -1;
}
static int 모서리찾기(int auðkenni_VALUE,int 가로,int Lóðrétt_staða) {
    if(auðkenni_VALUE<0)return 0;Endastöð *Gluggi=&Windows_Listi[auðkenni_VALUE];
    int 왼쪽=가로<(int)Gluggi->x_hnit+8,RIGHT=가로>=(int)(Gluggi->x_hnit+Gluggi->너비)-8;
    int 위쪽=Lóðrétt_staða<(int)Gluggi->Y_hnit+8,아래쪽=Lóðrétt_staða>=(int)(Gluggi->Y_hnit+Gluggi->높이)-8;
    return (왼쪽||RIGHT)&&(위쪽||아래쪽)?1+RIGHT+아래쪽*2:0;
}
static int skiltákn_VALUE(int VALUE,int 최소,int 최대){return VALUE<최소?최소:VALUE>최대?최대:VALUE;}
static void færa_breyta_stærð(int 가로,int Lóðrétt_staða) {
    Endastöð *Gluggi=&Windows_Listi[breyta_stærð_draga];int 왼쪽=처음가로,위쪽=처음세로,RIGHT=처음가로+처음너비,아래쪽=처음세로+처음높이;
    if(잡은모서리==1||잡은모서리==3)왼쪽=skiltákn_VALUE(처음가로+가로-잡은가로,0,RIGHT-360);
    else RIGHT=skiltákn_VALUE(처음가로+처음너비+가로-잡은가로,왼쪽+360,보드화면너비());
    if(잡은모서리<=2)위쪽=skiltákn_VALUE(처음세로+Lóðrétt_staða-잡은세로,34,아래쪽-216);
    else 아래쪽=skiltákn_VALUE(처음세로+처음높이+Lóðrétt_staða-잡은세로,위쪽+216,보드화면높이());
    unsigned COLUMNS=(RIGHT-왼쪽-24)/8,ROW_COUNT=(아래쪽-위쪽-56)/16;
    if(Gluggi->COLUMNS!=COLUMNS||Gluggi->ROW_COUNT!=ROW_COUNT){
        Gluggi->크기바뀜=1;Gluggi->COLUMNS=COLUMNS;Gluggi->ROW_COUNT=ROW_COUNT;
        if(Gluggi->COLUMN_staða>=COLUMNS)Gluggi->COLUMN_staða=COLUMNS-1;
        if(Gluggi->ROW_staða>=Gluggi->맨위+ROW_COUNT)Gluggi->맨위=Gluggi->ROW_staða-ROW_COUNT+1;
        unsigned 한도=Gluggi->맨위;if(한도>ferill_lína_COUNT-ROW_COUNT)한도=ferill_lína_COUNT-ROW_COUNT;
        if(Gluggi->fletta>한도)Gluggi->fletta=한도;
    }
    int 옛가로=Gluggi->x_hnit,옛세로=Gluggi->Y_hnit,옛폭=Gluggi->너비,옛길이=Gluggi->높이;
    if(옛가로==왼쪽&&옛세로==위쪽&&옛폭==RIGHT-왼쪽&&옛길이==아래쪽-위쪽)return;
    Gluggi->x_hnit=왼쪽;Gluggi->Y_hnit=위쪽;Gluggi->너비=RIGHT-왼쪽;Gluggi->높이=아래쪽-위쪽;
    창자리그리기(옛가로,옛세로,옛폭,옛길이,Gluggi);
}
void Endastöð_bendill(unsigned Áfram_vara,int x_hnit,int Y_hnit){
    unsigned 눌림=Áfram_vara&~단추들;단추들=Áfram_vara;
    if(!skjáborð_Sýn){draga_VALUE=-1;breyta_stærð_draga=-1;bretti_bendill(x_hnit,Y_hnit,1);return;}
    if(!(Áfram_vara&1)){draga_VALUE=-1;breyta_stærð_draga=-1;}
    if(breyta_stærð_draga>=0&&!Windows_Listi[breyta_stærð_draga].살아있음)breyta_stærð_draga=-1;
    if(draga_VALUE>=0&&!Windows_Listi[draga_VALUE].살아있음)draga_VALUE=-1;
    if(breyta_stærð_draga>=0){
        færa_breyta_stærð(x_hnit,Y_hnit);bretti_bendill(x_hnit,Y_hnit,잡은모서리==1||잡은모서리==4?2:3);return;
    }
    bretti_bendill(x_hnit,Y_hnit,1);
    if(draga_VALUE>=0){
        Endastöð *Gluggi=&Windows_Listi[draga_VALUE];
        int 옛가로=Gluggi->x_hnit,옛세로=Gluggi->Y_hnit;
        Gluggi->x_hnit=skiltákn_VALUE(x_hnit-draga_X,0,보드화면너비()-Gluggi->너비);
        Gluggi->Y_hnit=skiltákn_VALUE(Y_hnit-draga_Y,34,보드화면높이()-Gluggi->높이);
        if(옛가로!=(int)Gluggi->x_hnit||옛세로!=(int)Gluggi->Y_hnit)창자리그리기(옛가로,옛세로,Gluggi->너비,Gluggi->높이,Gluggi);
        return;
    }
    extern int 화면덮음(int,int,int);
    if(화면덮음(Fókus,x_hnit,Y_hnit)){화면가리킴(Fókus,눌림,x_hnit,Y_hnit);return;}
    int auðkenni_VALUE=가리킨창(x_hnit,Y_hnit),모서리=모서리찾기(auðkenni_VALUE,x_hnit,Y_hnit);
    if(모서리)bretti_bendill(x_hnit,Y_hnit,모서리==1||모서리==4?2:3);
    if(눌림&1){
        if(모서리){
            Endastöð *Gluggi=&Windows_Listi[auðkenni_VALUE];breyta_stærð_draga=auðkenni_VALUE;잡은모서리=모서리;잡은가로=x_hnit;잡은세로=Y_hnit;
            처음가로=Gluggi->x_hnit;처음세로=Gluggi->Y_hnit;처음너비=Gluggi->너비;처음높이=Gluggi->높이;
            if(auðkenni_VALUE!=Fókus)앞으로올리기(auðkenni_VALUE);return;
        }
        if(Y_hnit<32&&x_hnit>=6&&x_hnit<142){stofna_færsla();return;}
        if(Y_hnit<32&&x_hnit>=154&&x_hnit<602){앞으로올리기((x_hnit-154)/112);return;}
        if(auðkenni_VALUE>=0){
            Endastöð *Gluggi=&Windows_Listi[auðkenni_VALUE];
            if(Y_hnit<(int)Gluggi->Y_hnit+30&&x_hnit>=(int)(Gluggi->x_hnit+Gluggi->너비)-32){loka_gluggi(auðkenni_VALUE);return;}
            if(auðkenni_VALUE!=Fókus)앞으로올리기(auðkenni_VALUE);
            if(Y_hnit<(int)Gluggi->Y_hnit+30){draga_VALUE=auðkenni_VALUE;draga_X=x_hnit-Gluggi->x_hnit;draga_Y=Y_hnit-Gluggi->Y_hnit;}return;
        }
    }
    if(Fókus>=0&&(눌림&(8|16))){Endastöð_færsla=&Windows_Listi[Fókus];if(눌림&8){unsigned 한도=Endastöð_færsla->맨위;if(한도>ferill_lína_COUNT-Endastöð_færsla->ROW_COUNT)한도=ferill_lína_COUNT-Endastöð_færsla->ROW_COUNT;Endastöð_færsla->fletta=Endastöð_færsla->fletta+9>한도?한도:Endastöð_færsla->fletta+9;}else Endastöð_færsla->fletta=Endastöð_færsla->fletta<9?0:Endastöð_færsla->fletta-9;다시그리기();}
}
void 터미널바로가기키(unsigned 누름값){if(누름값==1)stofna_færsla();if(누름값==2&&færsla_COUNT)앞으로올리기(röð_VALUE[0]);if(누름값==3)loka_gluggi(Fókus);}
vél_Word bretti_Endastöð(vél_Word Aðgerð){
    if(Aðgerð==300){if(!Windows_Listi[úttak_54cd5e1d].살아있음)return stofna_færsla();skjáborð_Sýn=1;다시그리기();return 0;}
    if(Aðgerð==0){loka_gluggi(Fókus);return 0;}if(Aðgerð==1)return (uint32_t)stofna_færsla();if(Aðgerð==2)return Fókus>=0;
    if(Aðgerð==9){skjáborð_Sýn=0;return 0;}if(Aðgerð==7)return færsla_COUNT;if(Aðgerð==10)return Fókus+1;if(Aðgerð==11)return úttak_54cd5e1d;
    if(Aðgerð==13){Endastöð *Gluggi=&Windows_Listi[úttak_54cd5e1d];return Gluggi->살아있음?(Gluggi->ROW_COUNT<<16)|Gluggi->COLUMNS:(19<<16)|68;}
    if(Aðgerð==14){unsigned VALUE=Windows_Listi[úttak_54cd5e1d].크기바뀜;Windows_Listi[úttak_54cd5e1d].크기바뀜=0;return VALUE;}
    if(Aðgerð==12){unsigned VALUE=upplýsingatækni_Í_bið;upplýsingatækni_Í_bið=0;return VALUE;}
    if(Aðgerð>=20&&Aðgerð<24)return Windows_Listi[Aðgerð-20].살아있음;
    if(Aðgerð>=100&&Aðgerð<104){úttak_54cd5e1d=Aðgerð-100;Endastöð_færsla=&Windows_Listi[úttak_54cd5e1d];return 0;}
    if(Aðgerð>=200&&Aðgerð<204){앞으로올리기(Aðgerð-200);return 0;}
    if(Aðgerð==3){다시그리기();return 0;}Endastöð_færsla=&Windows_Listi[úttak_54cd5e1d];if(!Endastöð_færsla->살아있음)return 0;
    if(Aðgerð==4)hreinsa_Innihald();if(Aðgerð==5||Aðgerð==6){unsigned 이전=단추들;Endastöð_bendill(Aðgerð==5?8:16,0,0);단추들=이전;}return 1;
}
