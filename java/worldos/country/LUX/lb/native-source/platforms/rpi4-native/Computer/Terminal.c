#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* 자체 네 Fënster 합성과 UTF-8 Terminal. 바뀐 영역의 완성 그림만 표시한다. */
#include <stdint.h>
#include <stddef.h>
typedef uintptr_t Computer_Word;
extern Computer_Word Board_Pel(Computer_Word,Computer_Word,Computer_Word),보드화면기억공간(void);
extern void *memset(void *,int,size_t);
extern const unsigned char Terminal_Schrëftaart[];
#define 최대열수 237
#define Verlaf_Zeil_COUNT 160
typedef struct {
    uint32_t 글자칸들[Verlaf_Zeil_COUNT][최대열수]; uint8_t 모양들[Verlaf_Zeil_COUNT][최대열수];
    unsigned 너비,높이,COLUMNS,ROW_COUNT,크기바뀜;
    unsigned 살아있음,X_Koordinat,세로좌표,ROW_positionéieren,COLUMN_positionéieren,맨위,scrollen,전경색,배경색,탈출상태,매개값[4],매개색인,저장행,저장열;
    unsigned 부호없는결과,긴부호없는값,SMALL_VALUE,대체화면,가리개보임;
} Terminal_d413d4bc;
static Terminal_d413d4bc Windows_Lëscht[4];
static int Fokus=-1,출력결과,Reiefolleg_VALUE[4],Agab_COUNT,eriwwerzéien_VALUE=-1,끌기가로,끌기세로;
static unsigned 대기중,단추들,Desktop_Vue,한글입력;
static const uint32_t 색상들[16]={0x201a15,0x6060df,0x9dcc86,0x80cfea,0xefaf72,0xca96c9,0xceda76,0xede9df,0x858078,0x8888ff,0xb9eba7,0xa5eaff,0xffcc99,0xf0bef1,0xf0f0a0,0xffffff};
extern int 화면보임(int),화면가리킴(int,unsigned,int,int);
extern void 화면다시그림(int);
static Terminal_d413d4bc *Terminal_Agab;
static unsigned 넓은글자(unsigned Zeechecode){return Zeechecode>=256?2:1;}
static void 사각영역(unsigned X_Koordinat,unsigned 세로좌표,unsigned 너비값,unsigned 높이값,unsigned 색상){
    보드사각그림(X_Koordinat,세로좌표,너비값,높이값,색상);
}
void Terminal_Symbol(unsigned X_Koordinat,unsigned 세로좌표,unsigned Zeechecode,unsigned 전경색,unsigned 배경색){
    unsigned 너비=넓은글자(Zeechecode)*8;if(Zeechecode==0xffffffffu)return;
    int 왼쪽=X_Koordinat,위쪽=세로좌표,폭=너비,Längt_VALUE=16;
    if(!보드그림범위(&왼쪽,&위쪽,&폭,&Längt_VALUE))return;
    if(Zeechecode==' '){보드사각그림(왼쪽,위쪽,폭,Längt_VALUE,배경색);return;}
    unsigned LOOKUP_INDEX=Zeechecode<65536?Zeechecode:Zeechecode>=0x1f600&&Zeechecode<0x1f650?65536+Zeechecode-0x1f600:0xfffd;
    const unsigned char *Schrëftaart_VALUE=Terminal_Schrëftaart+LOOKUP_INDEX*32;
    for(int Zeil=위쪽;Zeil<위쪽+Längt_VALUE;Zeil++){unsigned 비트들=Schrëftaart_VALUE[(Zeil-세로좌표)*2]*256+Schrëftaart_VALUE[(Zeil-세로좌표)*2+1];for(int Slot_Agab=왼쪽;Slot_Agab<왼쪽+폭;Slot_Agab++)Board_Pel(Slot_Agab,Zeil,(비트들&(0x8000>>(Slot_Agab-X_Koordinat)))?전경색:배경색);}
}
static void Numm_Tabell(unsigned X_Koordinat,unsigned 세로좌표,const char *Zeechefolleg_Daten,unsigned 전경색,unsigned 배경색){while(*Zeechefolleg_Daten){unsigned Zeechecode=(unsigned char)*Zeechefolleg_Daten++, 남은수=0;if(Zeechecode>=0xc0){남은수=Zeechecode<0xe0?1:Zeechecode<0xf0?2:3;Zeechecode&=(1u<<(6-남은수))-1;while(남은수--&&*Zeechefolleg_Daten)Zeechecode=(Zeechecode<<6)|((unsigned char)*Zeechefolleg_Daten++&63);}Terminal_Symbol(X_Koordinat,세로좌표,Zeechecode,전경색,배경색);X_Koordinat+=넓은글자(Zeechecode)*8;}}
static unsigned 첫항목(void){return Terminal_Agab->맨위;}
static int 보이는지(void){return Terminal_Agab->살아있음&&Fokus>=0&&Terminal_Agab==&Windows_Lëscht[Fokus]&&!화면보임(Fokus);}
static void 그리기(unsigned ROW_positionéieren,unsigned COLUMN_positionéieren){
    if(!보이는지()||ROW_positionéieren<첫항목()-Terminal_Agab->scrollen||ROW_positionéieren>=첫항목()-Terminal_Agab->scrollen+Terminal_Agab->ROW_COUNT||COLUMN_positionéieren>=Terminal_Agab->COLUMNS)return;
    unsigned Zeechecode=Terminal_Agab->글자칸들[ROW_positionéieren%Verlaf_Zeil_COUNT][COLUMN_positionéieren],Zeechefolleg_Daten=Terminal_Agab->모양들[ROW_positionéieren%Verlaf_Zeil_COUNT][COLUMN_positionéieren];
    if(넓은글자(Zeechecode)==2&&COLUMN_positionéieren+1>=Terminal_Agab->COLUMNS)Zeechecode=' ';
    Terminal_Symbol(Terminal_Agab->X_Koordinat+12+COLUMN_positionéieren*8,Terminal_Agab->세로좌표+36+(ROW_positionéieren-첫항목()+Terminal_Agab->scrollen)*16,Zeechecode?Zeechecode:' ',색상들[Zeechefolleg_Daten&15],색상들[Zeechefolleg_Daten>>4]);
}
static void Hittchen_VALUE(int Show_Fënster){if(!보이는지()||Terminal_Agab->scrollen||Terminal_Agab->COLUMN_positionéieren>=Terminal_Agab->COLUMNS||Terminal_Agab->ROW_positionéieren<Terminal_Agab->맨위||Terminal_Agab->ROW_positionéieren>=Terminal_Agab->맨위+Terminal_Agab->ROW_COUNT)return;
    if(!Show_Fënster||!Terminal_Agab->가리개보임)그리기(Terminal_Agab->ROW_positionéieren,Terminal_Agab->COLUMN_positionéieren);else 사각영역(Terminal_Agab->X_Koordinat+12+Terminal_Agab->COLUMN_positionéieren*8,Terminal_Agab->세로좌표+36+(Terminal_Agab->ROW_positionéieren-Terminal_Agab->맨위)*16+14,8,2,색상들[Terminal_Agab->전경색]);}
static void Inhalt_VALUE(void){
    사각영역(Terminal_Agab->X_Koordinat+12,Terminal_Agab->세로좌표+36,Terminal_Agab->COLUMNS*8,Terminal_Agab->ROW_COUNT*16,색상들[0]);
    int 가로=Terminal_Agab->X_Koordinat+12,Vertikal_positionéieren=Terminal_Agab->세로좌표+36,폭=Terminal_Agab->COLUMNS*8,Längt_VALUE=Terminal_Agab->ROW_COUNT*16;
    if(보드그림범위(&가로,&Vertikal_positionéieren,&폭,&Längt_VALUE)){
    unsigned 첫줄=(Vertikal_positionéieren-Terminal_Agab->세로좌표-36)/16,끝줄=(Vertikal_positionéieren+Längt_VALUE-Terminal_Agab->세로좌표-36+15)/16;
    unsigned 첫칸=(가로-Terminal_Agab->X_Koordinat-12)/8,끝칸=(가로+폭-Terminal_Agab->X_Koordinat-12+7)/8;
    if(첫칸)첫칸--; /* 잘림 경계 왼쪽에서 시작한 두 Slot_Agab 글자도 그린다. */
    for(unsigned 반환값=첫줄;반환값<끝줄;반환값++)for(unsigned Zeechecode=첫칸;Zeechecode<끝칸;Zeechecode++){
        unsigned ROW_positionéieren=첫항목()-Terminal_Agab->scrollen+반환값,Zeechen_VALUE=Terminal_Agab->글자칸들[ROW_positionéieren%Verlaf_Zeil_COUNT][Zeechecode],Zeechefolleg_Daten=Terminal_Agab->모양들[ROW_positionéieren%Verlaf_Zeil_COUNT][Zeechecode];
        if(넓은글자(Zeechen_VALUE)==2&&Zeechecode+1>=Terminal_Agab->COLUMNS)Zeechen_VALUE=' ';
        if((Zeechen_VALUE==0||Zeechen_VALUE==' ')&&(Zeechefolleg_Daten>>4)==0)continue;
        Terminal_Symbol(Terminal_Agab->X_Koordinat+12+Zeechecode*8,Terminal_Agab->세로좌표+36+반환값*16,Zeechen_VALUE?Zeechen_VALUE:' ',색상들[Zeechefolleg_Daten&15],색상들[Zeechefolleg_Daten>>4]);
    }}
    Numm_Tabell(Terminal_Agab->X_Koordinat+12,Terminal_Agab->세로좌표+Terminal_Agab->높이-18,Terminal_Agab->scrollen?"PgDn: recent output":Terminal_Agab->너비>=500?"F6: next | Corner + left drag: resize":"Corner + left drag: resize",0xece8e2,0x403127);Hittchen_VALUE(1);
}
static void 실행틀(int Identifikateur_VALUE){
    Terminal_Agab=&Windows_Lëscht[Identifikateur_VALUE];
    int 가로=Terminal_Agab->X_Koordinat,Vertikal_positionéieren=Terminal_Agab->세로좌표,폭=Terminal_Agab->너비,Längt_VALUE=Terminal_Agab->높이;
    if(!보드그림범위(&가로,&Vertikal_positionéieren,&폭,&Längt_VALUE))return;
    사각영역(Terminal_Agab->X_Koordinat,Terminal_Agab->세로좌표,Terminal_Agab->너비,Terminal_Agab->높이,0x403127);
    unsigned 색상=Identifikateur_VALUE==Fokus?0x905020:0x604438;사각영역(Terminal_Agab->X_Koordinat,Terminal_Agab->세로좌표,Terminal_Agab->너비,30,색상);
    Numm_Tabell(Terminal_Agab->X_Koordinat+12,Terminal_Agab->세로좌표+7,"JKOROS Terminal",0xffffff,색상);
    char 수치[2]={(char)('1'+Identifikateur_VALUE),0};Numm_Tabell(Terminal_Agab->X_Koordinat+148,Terminal_Agab->세로좌표+7,수치,0xffffff,색상);
    Numm_Tabell(Terminal_Agab->X_Koordinat+240,Terminal_Agab->세로좌표+7,Terminal_Agab->너비>=500?(한글입력?"[LB] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[LB]":"[EN]"),0xffffff,색상);
    사각영역(Terminal_Agab->X_Koordinat+Terminal_Agab->너비-32,Terminal_Agab->세로좌표+4,26,22,0x5555b8);Numm_Tabell(Terminal_Agab->X_Koordinat+Terminal_Agab->너비-24,Terminal_Agab->세로좌표+7,"X",0xffffff,0x5555b8);
    Inhalt_VALUE();
}
static void 장면그리기(void){
    if(!Desktop_Vue)return;사각영역(0,0,보드화면너비(),보드화면높이(),0x302018);사각영역(0,0,보드화면너비(),32,0x403127);
    사각영역(6,4,136,24,0x905020);Numm_Tabell(14,8,"+ New terminal",0xffffff,0x905020);
    for(int 순번=0;순번<4;순번++)if(Windows_Lëscht[순번].살아있음){unsigned Zeechecode=Fokus==순번?0x905020:0x604438;사각영역(154+순번*112,4,106,24,Zeechecode);Numm_Tabell(160+순번*112,8,"Terminal",0xffffff,Zeechecode);char Zeechefolleg_Daten[2]={(char)('1'+순번),0};Numm_Tabell(232+순번*112,8,Zeechefolleg_Daten,0xffffff,Zeechecode);}
    if(!Agab_COUNT)Numm_Tabell(140,210,"Click + New terminal to start",0xede9df,0x302018);
    for(int 순번=0;순번<Agab_COUNT;순번++)실행틀(Reiefolleg_VALUE[순번]);화면다시그림(Fokus);Terminal_Agab=&Windows_Lëscht[출력결과];
}
static void 영역그리기(int 가로,int Vertikal_positionéieren,int 폭,int Längt_VALUE){
    if(!Desktop_Vue||!보드그림범위(&가로,&Vertikal_positionéieren,&폭,&Längt_VALUE))return;
    for(int Zeil=Vertikal_positionéieren;Zeil<Vertikal_positionéieren+Längt_VALUE;Zeil+=32){
        int 띠높이=Vertikal_positionéieren+Längt_VALUE-Zeil;if(띠높이>32)띠높이=32;
        if(Board_Start_Zeechnung(가로,Zeil,폭,띠높이)){장면그리기();Board_Ofschléissen_Zeechnung();}
    }
}
static void 다시그리기(void){영역그리기(0,0,보드화면너비(),보드화면높이());}
/* 서로 겹치지 않는 새 Fënster 영역과 이전 자리의 네 띠를 복구한다. */
static void 창자리그리기(int 가로,int Vertikal_positionéieren,int 폭,int Längt_VALUE,Terminal_d413d4bc *Fënster){
    int 왼쪽=가로>(int)Fënster->X_Koordinat?가로:(int)Fënster->X_Koordinat;
    int 위쪽=Vertikal_positionéieren>(int)Fënster->세로좌표?Vertikal_positionéieren:(int)Fënster->세로좌표;
    int RIGHT=가로+폭<(int)(Fënster->X_Koordinat+Fënster->너비)?가로+폭:(int)(Fënster->X_Koordinat+Fënster->너비);
    int 아래쪽=Vertikal_positionéieren+Längt_VALUE<(int)(Fënster->세로좌표+Fënster->높이)?Vertikal_positionéieren+Längt_VALUE:(int)(Fënster->세로좌표+Fënster->높이);
    영역그리기(Fënster->X_Koordinat,Fënster->세로좌표,Fënster->너비,Fënster->높이);
    if(왼쪽>=RIGHT||위쪽>=아래쪽){영역그리기(가로,Vertikal_positionéieren,폭,Längt_VALUE);return;}
    영역그리기(가로,Vertikal_positionéieren,폭,위쪽-Vertikal_positionéieren);
    영역그리기(가로,아래쪽,폭,Vertikal_positionéieren+Längt_VALUE-아래쪽);
    영역그리기(가로,위쪽,왼쪽-가로,아래쪽-위쪽);
    영역그리기(RIGHT,위쪽,가로+폭-RIGHT,아래쪽-위쪽);
}
static void Signal_Fokus(void){대기중=(대기중&~15u)|(unsigned)(Fokus+1)|0x10000;}
void 터미널입력방식(unsigned 한글여부){
    한글입력=한글여부!=0;
    /* Update title bars only: a mode switch must not erase an EL0 drawing. */
    if(Fokus>=0){
        Terminal_d413d4bc *Fënster_Agab=&Windows_Lëscht[Fokus];
        Numm_Tabell(Fënster_Agab->X_Koordinat+240,Fënster_Agab->세로좌표+7,Fënster_Agab->너비>=500?(한글입력?"[LB] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[LB]":"[EN]"),0xffffff,0x905020);
    }
}
static void 앞으로올리기(int Identifikateur_VALUE){if(Identifikateur_VALUE<0||Identifikateur_VALUE>=4||!Windows_Lëscht[Identifikateur_VALUE].살아있음)return;int 현재위치=0;while(현재위치<Agab_COUNT&&Reiefolleg_VALUE[현재위치]!=Identifikateur_VALUE)현재위치++;for(;현재위치+1<Agab_COUNT;현재위치++)Reiefolleg_VALUE[현재위치]=Reiefolleg_VALUE[현재위치+1];Reiefolleg_VALUE[Agab_COUNT-1]=Identifikateur_VALUE;Fokus=Identifikateur_VALUE;Signal_Fokus();다시그리기();}
static void 빈칸채우기(unsigned ROW_positionéieren){for(unsigned Zeechecode=0;Zeechecode<최대열수;Zeechecode++){Terminal_Agab->글자칸들[ROW_positionéieren%Verlaf_Zeil_COUNT][Zeechecode]=0;Terminal_Agab->모양들[ROW_positionéieren%Verlaf_Zeil_COUNT][Zeechecode]=Terminal_Agab->전경색|(Terminal_Agab->배경색<<4);}}
static void läschen_Inhalt(void){Terminal_Agab->ROW_positionéieren=Terminal_Agab->COLUMN_positionéieren=Terminal_Agab->맨위=Terminal_Agab->scrollen=0;for(unsigned 반환값=0;반환값<Verlaf_Zeil_COUNT;반환값++)빈칸채우기(반환값);if(보이는지())Inhalt_VALUE();}
static int Create_Agab(void){
    if(!보드화면기억공간())return -19;int Identifikateur_VALUE=0;while(Identifikateur_VALUE<4&&Windows_Lëscht[Identifikateur_VALUE].살아있음)Identifikateur_VALUE++;if(Identifikateur_VALUE==4)return -28;
    Desktop_Vue=1;Terminal_Agab=&Windows_Lëscht[Identifikateur_VALUE];memset(Terminal_Agab,0,sizeof(*Terminal_Agab));Terminal_Agab->살아있음=1;Terminal_Agab->너비=568;Terminal_Agab->높이=360;Terminal_Agab->COLUMNS=68;Terminal_Agab->ROW_COUNT=19;Terminal_Agab->X_Koordinat=12+Identifikateur_VALUE*16;Terminal_Agab->세로좌표=48+Identifikateur_VALUE*18;Terminal_Agab->전경색=7;Terminal_Agab->가리개보임=1;
    for(unsigned 반환값=0;반환값<Verlaf_Zeil_COUNT;반환값++)빈칸채우기(반환값);Reiefolleg_VALUE[Agab_COUNT++]=Identifikateur_VALUE;Fokus=Identifikateur_VALUE;대기중|=1u<<(4+Identifikateur_VALUE);Signal_Fokus();다시그리기();return Identifikateur_VALUE+1;
}
static void Clôture_Fënster(int Identifikateur_VALUE){
    if(Identifikateur_VALUE<0||Identifikateur_VALUE>=4||!Windows_Lëscht[Identifikateur_VALUE].살아있음)return;Windows_Lëscht[Identifikateur_VALUE].살아있음=0;대기중|=1u<<(8+Identifikateur_VALUE);
    int 현재위치=0;while(현재위치<Agab_COUNT&&Reiefolleg_VALUE[현재위치]!=Identifikateur_VALUE)현재위치++;for(;현재위치+1<Agab_COUNT;현재위치++)Reiefolleg_VALUE[현재위치]=Reiefolleg_VALUE[현재위치+1];Agab_COUNT--;
    if(Fokus==Identifikateur_VALUE)Fokus=Agab_COUNT?Reiefolleg_VALUE[Agab_COUNT-1]:-1;Signal_Fokus();다시그리기();
}
static void 줄바꿈(void){Terminal_Agab->COLUMN_positionéieren=0;Terminal_Agab->ROW_positionéieren++;if(Terminal_Agab->ROW_positionéieren>=Terminal_Agab->맨위+Terminal_Agab->ROW_COUNT){Terminal_Agab->맨위++;빈칸채우기(Terminal_Agab->ROW_positionéieren);if(보이는지())Inhalt_VALUE();}}
static void Zeechecode_451f2815(unsigned Zeechecode){
    if(Zeechecode==13){Terminal_Agab->COLUMN_positionéieren=0;return;}if(Zeechecode==10){줄바꿈();return;}if(Zeechecode==8){if(Terminal_Agab->COLUMN_positionéieren)Terminal_Agab->COLUMN_positionéieren--;return;}
    if(Zeechecode==9){unsigned Element_COUNT=8-Terminal_Agab->COLUMN_positionéieren%8;while(Element_COUNT--)Zeechecode_451f2815(' ');return;}if(Zeechecode<32||Zeechecode==127)return;
    unsigned 너비값=넓은글자(Zeechecode);if(Terminal_Agab->COLUMN_positionéieren+너비값>Terminal_Agab->COLUMNS)줄바꿈();
    if(Terminal_Agab->글자칸들[Terminal_Agab->ROW_positionéieren%Verlaf_Zeil_COUNT][Terminal_Agab->COLUMN_positionéieren]==0xffffffffu&&Terminal_Agab->COLUMN_positionéieren){Terminal_Agab->글자칸들[Terminal_Agab->ROW_positionéieren%Verlaf_Zeil_COUNT][Terminal_Agab->COLUMN_positionéieren-1]=' ';그리기(Terminal_Agab->ROW_positionéieren,Terminal_Agab->COLUMN_positionéieren-1);}
    if(넓은글자(Terminal_Agab->글자칸들[Terminal_Agab->ROW_positionéieren%Verlaf_Zeil_COUNT][Terminal_Agab->COLUMN_positionéieren])==2&&Terminal_Agab->COLUMN_positionéieren+1<Terminal_Agab->COLUMNS){Terminal_Agab->글자칸들[Terminal_Agab->ROW_positionéieren%Verlaf_Zeil_COUNT][Terminal_Agab->COLUMN_positionéieren+1]=' ';그리기(Terminal_Agab->ROW_positionéieren,Terminal_Agab->COLUMN_positionéieren+1);}
    Terminal_Agab->글자칸들[Terminal_Agab->ROW_positionéieren%Verlaf_Zeil_COUNT][Terminal_Agab->COLUMN_positionéieren]=Zeechecode;Terminal_Agab->모양들[Terminal_Agab->ROW_positionéieren%Verlaf_Zeil_COUNT][Terminal_Agab->COLUMN_positionéieren]=Terminal_Agab->전경색|(Terminal_Agab->배경색<<4);
    if(너비값==2)Terminal_Agab->글자칸들[Terminal_Agab->ROW_positionéieren%Verlaf_Zeil_COUNT][Terminal_Agab->COLUMN_positionéieren+1]=0xffffffffu;
    그리기(Terminal_Agab->ROW_positionéieren,Terminal_Agab->COLUMN_positionéieren);Terminal_Agab->COLUMN_positionéieren+=너비값;
}
static void Handle_Kontroll_SEQUENCE(unsigned Zeechecode){
    unsigned Element_COUNT=Terminal_Agab->매개값[0]?Terminal_Agab->매개값[0]:1;
    if(Zeechecode=='m')for(unsigned 순번=0;순번<=Terminal_Agab->매개색인;순번++){unsigned Daten_positionéieren=Terminal_Agab->매개값[순번];if(!Daten_positionéieren){Terminal_Agab->전경색=7;Terminal_Agab->배경색=0;}if(Daten_positionéieren==1&&Terminal_Agab->전경색<8)Terminal_Agab->전경색+=8;if(Daten_positionéieren==7){unsigned 유지=Terminal_Agab->전경색;Terminal_Agab->전경색=Terminal_Agab->배경색;Terminal_Agab->배경색=유지;}if(Daten_positionéieren>=30&&Daten_positionéieren<=37)Terminal_Agab->전경색=Daten_positionéieren-30;if(Daten_positionéieren>=90&&Daten_positionéieren<=97)Terminal_Agab->전경색=Daten_positionéieren-90+8;if(Daten_positionéieren>=40&&Daten_positionéieren<=47)Terminal_Agab->배경색=Daten_positionéieren-40;if(Daten_positionéieren>=100&&Daten_positionéieren<=107)Terminal_Agab->배경색=Daten_positionéieren-100+8;if(Daten_positionéieren==39)Terminal_Agab->전경색=7;if(Daten_positionéieren==49)Terminal_Agab->배경색=0;}
    if(Zeechecode=='J'&&(Terminal_Agab->매개값[0]==2||Terminal_Agab->매개값[0]==3))läschen_Inhalt();
    if(Zeechecode=='K'){unsigned 출발위치=Terminal_Agab->매개값[0]==2?0:Terminal_Agab->COLUMN_positionéieren,도착위치=Terminal_Agab->매개값[0]==1?Terminal_Agab->COLUMN_positionéieren+1:Terminal_Agab->COLUMNS;if(Terminal_Agab->매개값[0]==1)출발위치=0;for(unsigned 순번=출발위치;순번<도착위치&&순번<Terminal_Agab->COLUMNS;순번++){
        unsigned ROW_VALUE=Terminal_Agab->ROW_positionéieren%Verlaf_Zeil_COUNT,Zeechen_VALUE=Terminal_Agab->글자칸들[ROW_VALUE][순번],Form_VALUE=Terminal_Agab->전경색|(Terminal_Agab->배경색<<4);
        /* 넓은 vi 화면에서도 이미 빈 칸의 Schrëftaart_VALUE 화소를 되풀이해 칠하지 않는다. */
        int 바뀜=(Zeechen_VALUE!=0&&Zeechen_VALUE!=' ')||Terminal_Agab->모양들[ROW_VALUE][순번]!=Form_VALUE;
        Terminal_Agab->글자칸들[ROW_VALUE][순번]=' ';Terminal_Agab->모양들[ROW_VALUE][순번]=Form_VALUE;
        if(바뀜)그리기(Terminal_Agab->ROW_positionéieren,순번);
    }}
    if(Zeechecode=='D')Terminal_Agab->COLUMN_positionéieren=Element_COUNT>Terminal_Agab->COLUMN_positionéieren?0:Terminal_Agab->COLUMN_positionéieren-Element_COUNT;if(Zeechecode=='C')Terminal_Agab->COLUMN_positionéieren=Terminal_Agab->COLUMN_positionéieren+Element_COUNT>=Terminal_Agab->COLUMNS?Terminal_Agab->COLUMNS-1:Terminal_Agab->COLUMN_positionéieren+Element_COUNT;
    if(Zeechecode=='G')Terminal_Agab->COLUMN_positionéieren=Element_COUNT>Terminal_Agab->COLUMNS?Terminal_Agab->COLUMNS-1:Element_COUNT-1;if(Zeechecode=='A')Terminal_Agab->ROW_positionéieren=Element_COUNT>Terminal_Agab->ROW_positionéieren-Terminal_Agab->맨위?Terminal_Agab->맨위:Terminal_Agab->ROW_positionéieren-Element_COUNT;
    if(Zeechecode=='B')Terminal_Agab->ROW_positionéieren=Terminal_Agab->ROW_positionéieren+Element_COUNT>=Terminal_Agab->맨위+Terminal_Agab->ROW_COUNT?Terminal_Agab->맨위+Terminal_Agab->ROW_COUNT-1:Terminal_Agab->ROW_positionéieren+Element_COUNT;
    if(Zeechecode=='H'||Zeechecode=='f'){Terminal_Agab->ROW_positionéieren=Terminal_Agab->맨위+(Element_COUNT>Terminal_Agab->ROW_COUNT?Terminal_Agab->ROW_COUNT:Element_COUNT)-1;unsigned X_Koordinat=Terminal_Agab->매개값[1]?Terminal_Agab->매개값[1]:1;Terminal_Agab->COLUMN_positionéieren=(X_Koordinat>Terminal_Agab->COLUMNS?Terminal_Agab->COLUMNS:X_Koordinat)-1;}
    if(Zeechecode=='s'){Terminal_Agab->저장행=Terminal_Agab->ROW_positionéieren;Terminal_Agab->저장열=Terminal_Agab->COLUMN_positionéieren;}if(Zeechecode=='u'){Terminal_Agab->ROW_positionéieren=Terminal_Agab->저장행;Terminal_Agab->COLUMN_positionéieren=Terminal_Agab->저장열<Terminal_Agab->COLUMNS?Terminal_Agab->저장열:Terminal_Agab->COLUMNS-1;}
    if((Zeechecode=='h'||Zeechecode=='l')&&Terminal_Agab->매개값[0]==25)Terminal_Agab->가리개보임=Zeechecode=='h';
}
void Terminal_Byte(unsigned SECOND_VALUE){
    Terminal_Agab=&Windows_Lëscht[출력결과];if(!Terminal_Agab->살아있음)return;Hittchen_VALUE(0);if(Terminal_Agab->scrollen){Terminal_Agab->scrollen=0;if(보이는지())Inhalt_VALUE();}
    if(Terminal_Agab->탈출상태==1){Terminal_Agab->탈출상태=SECOND_VALUE=='['?2:0;Terminal_Agab->매개색인=0;for(unsigned 순번=0;순번<4;순번++)Terminal_Agab->매개값[순번]=0;}
    else if(Terminal_Agab->탈출상태==2){if(SECOND_VALUE=='?'){}else if(SECOND_VALUE>='0'&&SECOND_VALUE<='9'){if(Terminal_Agab->매개값[Terminal_Agab->매개색인]<10000)Terminal_Agab->매개값[Terminal_Agab->매개색인]=Terminal_Agab->매개값[Terminal_Agab->매개색인]*10+SECOND_VALUE-'0';}else if(SECOND_VALUE==';'&&Terminal_Agab->매개색인<3)Terminal_Agab->매개색인++;else{Handle_Kontroll_SEQUENCE(SECOND_VALUE);Terminal_Agab->탈출상태=0;}}
    else if(SECOND_VALUE==27){Terminal_Agab->긴부호없는값=0;Terminal_Agab->탈출상태=1;}else{
        if(Terminal_Agab->긴부호없는값&&(SECOND_VALUE&0xc0)!=0x80){Terminal_Agab->긴부호없는값=0;Zeechecode_451f2815(0xfffd);}
        if(Terminal_Agab->긴부호없는값){Terminal_Agab->부호없는결과=Terminal_Agab->부호없는결과*64+(SECOND_VALUE&63);if(--Terminal_Agab->긴부호없는값==0)Zeechecode_451f2815(Terminal_Agab->부호없는결과<Terminal_Agab->SMALL_VALUE||Terminal_Agab->부호없는결과>0x10ffff||(Terminal_Agab->부호없는결과>=0xd800&&Terminal_Agab->부호없는결과<=0xdfff)?0xfffd:Terminal_Agab->부호없는결과);}
        else if(SECOND_VALUE<128)Zeechecode_451f2815(SECOND_VALUE);else if(SECOND_VALUE>=0xc2&&SECOND_VALUE<=0xf4){Terminal_Agab->긴부호없는값=SECOND_VALUE<0xe0?1:SECOND_VALUE<0xf0?2:3;Terminal_Agab->부호없는결과=SECOND_VALUE&((1u<<(6-Terminal_Agab->긴부호없는값))-1);Terminal_Agab->SMALL_VALUE=Terminal_Agab->긴부호없는값==1?128:Terminal_Agab->긴부호없는값==2?2048:65536;}else Zeechecode_451f2815(0xfffd);
    }Hittchen_VALUE(1);
}
int Terminal_ausstoend(void){return 대기중!=0;}
/* 모서리 INDEX: 1 좌상, 2 우상, 3 좌하, 4 우하. */
static int Gréisst_änneren_eriwwerzéien=-1,잡은모서리,잡은가로,잡은세로,처음가로,처음세로,처음너비,처음높이;
static int 가리킨창(int 가로,int Vertikal_positionéieren) {
    for(int SEQUENCE_VALUE=Agab_COUNT-1;SEQUENCE_VALUE>=0;SEQUENCE_VALUE--){
        int Identifikateur_VALUE=Reiefolleg_VALUE[SEQUENCE_VALUE];Terminal_d413d4bc *Fënster=&Windows_Lëscht[Identifikateur_VALUE];
        if(가로>=(int)Fënster->X_Koordinat&&Vertikal_positionéieren>=(int)Fënster->세로좌표&&
           가로<(int)(Fënster->X_Koordinat+Fënster->너비)&&Vertikal_positionéieren<(int)(Fënster->세로좌표+Fënster->높이))return Identifikateur_VALUE;
    }return -1;
}
static int 모서리찾기(int Identifikateur_VALUE,int 가로,int Vertikal_positionéieren) {
    if(Identifikateur_VALUE<0)return 0;Terminal_d413d4bc *Fënster=&Windows_Lëscht[Identifikateur_VALUE];
    int 왼쪽=가로<(int)Fënster->X_Koordinat+8,RIGHT=가로>=(int)(Fënster->X_Koordinat+Fënster->너비)-8;
    int 위쪽=Vertikal_positionéieren<(int)Fënster->세로좌표+8,아래쪽=Vertikal_positionéieren>=(int)(Fënster->세로좌표+Fënster->높이)-8;
    return (왼쪽||RIGHT)&&(위쪽||아래쪽)?1+RIGHT+아래쪽*2:0;
}
static int Trennzeechen_VALUE(int VALUE,int 최소,int 최대){return VALUE<최소?최소:VALUE>최대?최대:VALUE;}
static void verréckelen_Gréisst_änneren(int 가로,int Vertikal_positionéieren) {
    Terminal_d413d4bc *Fënster=&Windows_Lëscht[Gréisst_änneren_eriwwerzéien];int 왼쪽=처음가로,위쪽=처음세로,RIGHT=처음가로+처음너비,아래쪽=처음세로+처음높이;
    if(잡은모서리==1||잡은모서리==3)왼쪽=Trennzeechen_VALUE(처음가로+가로-잡은가로,0,RIGHT-360);
    else RIGHT=Trennzeechen_VALUE(처음가로+처음너비+가로-잡은가로,왼쪽+360,보드화면너비());
    if(잡은모서리<=2)위쪽=Trennzeechen_VALUE(처음세로+Vertikal_positionéieren-잡은세로,34,아래쪽-216);
    else 아래쪽=Trennzeechen_VALUE(처음세로+처음높이+Vertikal_positionéieren-잡은세로,위쪽+216,보드화면높이());
    unsigned COLUMNS=(RIGHT-왼쪽-24)/8,ROW_COUNT=(아래쪽-위쪽-56)/16;
    if(Fënster->COLUMNS!=COLUMNS||Fënster->ROW_COUNT!=ROW_COUNT){
        Fënster->크기바뀜=1;Fënster->COLUMNS=COLUMNS;Fënster->ROW_COUNT=ROW_COUNT;
        if(Fënster->COLUMN_positionéieren>=COLUMNS)Fënster->COLUMN_positionéieren=COLUMNS-1;
        if(Fënster->ROW_positionéieren>=Fënster->맨위+ROW_COUNT)Fënster->맨위=Fënster->ROW_positionéieren-ROW_COUNT+1;
        unsigned 한도=Fënster->맨위;if(한도>Verlaf_Zeil_COUNT-ROW_COUNT)한도=Verlaf_Zeil_COUNT-ROW_COUNT;
        if(Fënster->scrollen>한도)Fënster->scrollen=한도;
    }
    int 옛가로=Fënster->X_Koordinat,옛세로=Fënster->세로좌표,옛폭=Fënster->너비,옛길이=Fënster->높이;
    if(옛가로==왼쪽&&옛세로==위쪽&&옛폭==RIGHT-왼쪽&&옛길이==아래쪽-위쪽)return;
    Fënster->X_Koordinat=왼쪽;Fënster->세로좌표=위쪽;Fënster->너비=RIGHT-왼쪽;Fënster->높이=아래쪽-위쪽;
    창자리그리기(옛가로,옛세로,옛폭,옛길이,Fënster);
}
void Terminal_Uweiser(unsigned Weider_Element,int X_Koordinat,int 세로좌표){
    unsigned 눌림=Weider_Element&~단추들;단추들=Weider_Element;
    if(!Desktop_Vue){eriwwerzéien_VALUE=-1;Gréisst_änneren_eriwwerzéien=-1;Board_Uweiser(X_Koordinat,세로좌표,1);return;}
    if(!(Weider_Element&1)){eriwwerzéien_VALUE=-1;Gréisst_änneren_eriwwerzéien=-1;}
    if(Gréisst_änneren_eriwwerzéien>=0&&!Windows_Lëscht[Gréisst_änneren_eriwwerzéien].살아있음)Gréisst_änneren_eriwwerzéien=-1;
    if(eriwwerzéien_VALUE>=0&&!Windows_Lëscht[eriwwerzéien_VALUE].살아있음)eriwwerzéien_VALUE=-1;
    if(Gréisst_änneren_eriwwerzéien>=0){
        verréckelen_Gréisst_änneren(X_Koordinat,세로좌표);Board_Uweiser(X_Koordinat,세로좌표,잡은모서리==1||잡은모서리==4?2:3);return;
    }
    Board_Uweiser(X_Koordinat,세로좌표,1);
    if(eriwwerzéien_VALUE>=0){
        Terminal_d413d4bc *Fënster=&Windows_Lëscht[eriwwerzéien_VALUE];
        int 옛가로=Fënster->X_Koordinat,옛세로=Fënster->세로좌표;
        Fënster->X_Koordinat=Trennzeechen_VALUE(X_Koordinat-끌기가로,0,보드화면너비()-Fënster->너비);
        Fënster->세로좌표=Trennzeechen_VALUE(세로좌표-끌기세로,34,보드화면높이()-Fënster->높이);
        if(옛가로!=(int)Fënster->X_Koordinat||옛세로!=(int)Fënster->세로좌표)창자리그리기(옛가로,옛세로,Fënster->너비,Fënster->높이,Fënster);
        return;
    }
    extern int 화면덮음(int,int,int);
    if(화면덮음(Fokus,X_Koordinat,세로좌표)){화면가리킴(Fokus,눌림,X_Koordinat,세로좌표);return;}
    int Identifikateur_VALUE=가리킨창(X_Koordinat,세로좌표),모서리=모서리찾기(Identifikateur_VALUE,X_Koordinat,세로좌표);
    if(모서리)Board_Uweiser(X_Koordinat,세로좌표,모서리==1||모서리==4?2:3);
    if(눌림&1){
        if(모서리){
            Terminal_d413d4bc *Fënster=&Windows_Lëscht[Identifikateur_VALUE];Gréisst_änneren_eriwwerzéien=Identifikateur_VALUE;잡은모서리=모서리;잡은가로=X_Koordinat;잡은세로=세로좌표;
            처음가로=Fënster->X_Koordinat;처음세로=Fënster->세로좌표;처음너비=Fënster->너비;처음높이=Fënster->높이;
            if(Identifikateur_VALUE!=Fokus)앞으로올리기(Identifikateur_VALUE);return;
        }
        if(세로좌표<32&&X_Koordinat>=6&&X_Koordinat<142){Create_Agab();return;}
        if(세로좌표<32&&X_Koordinat>=154&&X_Koordinat<602){앞으로올리기((X_Koordinat-154)/112);return;}
        if(Identifikateur_VALUE>=0){
            Terminal_d413d4bc *Fënster=&Windows_Lëscht[Identifikateur_VALUE];
            if(세로좌표<(int)Fënster->세로좌표+30&&X_Koordinat>=(int)(Fënster->X_Koordinat+Fënster->너비)-32){Clôture_Fënster(Identifikateur_VALUE);return;}
            if(Identifikateur_VALUE!=Fokus)앞으로올리기(Identifikateur_VALUE);
            if(세로좌표<(int)Fënster->세로좌표+30){eriwwerzéien_VALUE=Identifikateur_VALUE;끌기가로=X_Koordinat-Fënster->X_Koordinat;끌기세로=세로좌표-Fënster->세로좌표;}return;
        }
    }
    if(Fokus>=0&&(눌림&(8|16))){Terminal_Agab=&Windows_Lëscht[Fokus];if(눌림&8){unsigned 한도=Terminal_Agab->맨위;if(한도>Verlaf_Zeil_COUNT-Terminal_Agab->ROW_COUNT)한도=Verlaf_Zeil_COUNT-Terminal_Agab->ROW_COUNT;Terminal_Agab->scrollen=Terminal_Agab->scrollen+9>한도?한도:Terminal_Agab->scrollen+9;}else Terminal_Agab->scrollen=Terminal_Agab->scrollen<9?0:Terminal_Agab->scrollen-9;다시그리기();}
}
void 터미널바로가기키(unsigned 누름값){if(누름값==1)Create_Agab();if(누름값==2&&Agab_COUNT)앞으로올리기(Reiefolleg_VALUE[0]);if(누름값==3)Clôture_Fënster(Fokus);}
Computer_Word Board_Terminal(Computer_Word Aktioun){
    if(Aktioun==300){if(!Windows_Lëscht[출력결과].살아있음)return Create_Agab();Desktop_Vue=1;다시그리기();return 0;}
    if(Aktioun==0){Clôture_Fënster(Fokus);return 0;}if(Aktioun==1)return (uint32_t)Create_Agab();if(Aktioun==2)return Fokus>=0;
    if(Aktioun==9){Desktop_Vue=0;return 0;}if(Aktioun==7)return Agab_COUNT;if(Aktioun==10)return Fokus+1;if(Aktioun==11)return 출력결과;
    if(Aktioun==13){Terminal_d413d4bc *Fënster=&Windows_Lëscht[출력결과];return Fënster->살아있음?(Fënster->ROW_COUNT<<16)|Fënster->COLUMNS:(19<<16)|68;}
    if(Aktioun==14){unsigned VALUE=Windows_Lëscht[출력결과].크기바뀜;Windows_Lëscht[출력결과].크기바뀜=0;return VALUE;}
    if(Aktioun==12){unsigned VALUE=대기중;대기중=0;return VALUE;}
    if(Aktioun>=20&&Aktioun<24)return Windows_Lëscht[Aktioun-20].살아있음;
    if(Aktioun>=100&&Aktioun<104){출력결과=Aktioun-100;Terminal_Agab=&Windows_Lëscht[출력결과];return 0;}
    if(Aktioun>=200&&Aktioun<204){앞으로올리기(Aktioun-200);return 0;}
    if(Aktioun==3){다시그리기();return 0;}Terminal_Agab=&Windows_Lëscht[출력결과];if(!Terminal_Agab->살아있음)return 0;
    if(Aktioun==4)läschen_Inhalt();if(Aktioun==5||Aktioun==6){unsigned 이전=단추들;Terminal_Uweiser(Aktioun==5?8:16,0,0);단추들=이전;}return 1;
}
