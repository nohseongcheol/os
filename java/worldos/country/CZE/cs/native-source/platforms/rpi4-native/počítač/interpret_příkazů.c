#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* vlastní 네 Okno 합성과 UTF-8 interpret_příkazů. 바뀐 영역의 dokončeno_HODNOTA 그림만 표시한다. */
#include <stdint.h>
#include <stddef.h>
typedef uintptr_t počítač_Word;
extern počítač_Word Panel_pixel(počítač_Word,počítač_Word,počítač_Word),보드화면기억공간(void);
extern void *memset(void *,int,size_t);
extern const unsigned char Terminál_písmo[];
#define 최대열수 237
#define Historie_čára_POČET 160
typedef struct {
    uint32_t 글자칸들[Historie_čára_POČET][최대열수]; uint8_t 모양들[Historie_čára_POČET][최대열수];
    unsigned 너비,výška_HODNOTA,SLOUPCE,ŘÁDEK_POČET,크기바뀜;
    unsigned 살아있음,souřadnice_x,Y_souřadnice,ŘÁDEK_pozice,SLOUPEC_pozice,맨위,posouvat,전경색,배경색,탈출상태,parametr_HODNOTA[4],parametr_INDEX,저장행,저장열;
    unsigned 부호없는결과,긴부호없는값,SMALL_HODNOTA,대체화면,가리개보임;
} Terminál;
static Terminál Windows_Seznam[4];
static int fokus=-1,výstup,pořadí_HODNOTA[4],položka_POČET,přetáhnout_HODNOTA=-1,přetáhnout_X,přetáhnout_Y;
static unsigned informační_systémy_probíhá,단추들,Plocha_pohled,한글입력;
static const uint32_t 색상들[16]={0x201a15,0x6060df,0x9dcc86,0x80cfea,0xefaf72,0xca96c9,0xceda76,0xede9df,0x858078,0x8888ff,0xb9eba7,0xa5eaff,0xffcc99,0xf0bef1,0xf0f0a0,0xffffff};
extern int 화면보임(int),화면가리킴(int,unsigned,int,int);
extern void 화면다시그림(int);
static Terminál *Terminál_položka;
static unsigned široký_znak(unsigned bod_kódu){return bod_kódu>=256?2:1;}
static void 사각영역(unsigned souřadnice_x,unsigned Y_souřadnice,unsigned 너비값,unsigned vyžádáno_výška_HODNOTA,unsigned 색상){
    Panel_obdélník_výplň(souřadnice_x,Y_souřadnice,너비값,vyžádáno_výška_HODNOTA,색상);
}
void Terminál_piktogram(unsigned souřadnice_x,unsigned Y_souřadnice,unsigned bod_kódu,unsigned 전경색,unsigned 배경색){
    unsigned 너비=široký_znak(bod_kódu)*8;if(bod_kódu==0xffffffffu)return;
    int 왼쪽=souřadnice_x,위쪽=Y_souřadnice,폭=너비,délka_HODNOTA=16;
    if(!보드그림범위(&왼쪽,&위쪽,&폭,&délka_HODNOTA))return;
    if(bod_kódu==' '){Panel_obdélník_výplň(왼쪽,위쪽,폭,délka_HODNOTA,배경색);return;}
    unsigned VYHLEDAT_INDEX=bod_kódu<65536?bod_kódu:bod_kódu>=0x1f600&&bod_kódu<0x1f650?65536+bod_kódu-0x1f600:0xfffd;
    const unsigned char *písmo_HODNOTA=Terminál_písmo+VYHLEDAT_INDEX*32;
    for(int vstupní_řádek=위쪽;vstupní_řádek<위쪽+délka_HODNOTA;vstupní_řádek++){unsigned BITS_Seznam=písmo_HODNOTA[(vstupní_řádek-Y_souřadnice)*2]*256+písmo_HODNOTA[(vstupní_řádek-Y_souřadnice)*2+1];for(int přihrádka_položka=왼쪽;přihrádka_položka<왼쪽+폭;přihrádka_položka++)Panel_pixel(přihrádka_položka,vstupní_řádek,(BITS_Seznam&(0x8000>>(přihrádka_položka-souřadnice_x)))?전경색:배경색);}
}
static void název_tabulka(unsigned souřadnice_x,unsigned Y_souřadnice,const char *řetězec_data,unsigned 전경색,unsigned 배경색){while(*řetězec_data){unsigned bod_kódu=(unsigned char)*řetězec_data++, 남은수=0;if(bod_kódu>=0xc0){남은수=bod_kódu<0xe0?1:bod_kódu<0xf0?2:3;bod_kódu&=(1u<<(6-남은수))-1;while(남은수--&&*řetězec_data)bod_kódu=(bod_kódu<<6)|((unsigned char)*řetězec_data++&63);}Terminál_piktogram(souřadnice_x,Y_souřadnice,bod_kódu,전경색,배경색);souřadnice_x+=široký_znak(bod_kódu)*8;}}
static unsigned 첫항목(void){return Terminál_položka->맨위;}
static int 보이는지(void){return Terminál_položka->살아있음&&fokus>=0&&Terminál_položka==&Windows_Seznam[fokus]&&!화면보임(fokus);}
static void 그리기(unsigned ŘÁDEK_pozice,unsigned SLOUPEC_pozice){
    if(!보이는지()||ŘÁDEK_pozice<첫항목()-Terminál_položka->posouvat||ŘÁDEK_pozice>=첫항목()-Terminál_položka->posouvat+Terminál_položka->ŘÁDEK_POČET||SLOUPEC_pozice>=Terminál_položka->SLOUPCE)return;
    unsigned bod_kódu=Terminál_položka->글자칸들[ŘÁDEK_pozice%Historie_čára_POČET][SLOUPEC_pozice],řetězec_data=Terminál_položka->모양들[ŘÁDEK_pozice%Historie_čára_POČET][SLOUPEC_pozice];
    if(široký_znak(bod_kódu)==2&&SLOUPEC_pozice+1>=Terminál_položka->SLOUPCE)bod_kódu=' ';
    Terminál_piktogram(Terminál_položka->souřadnice_x+12+SLOUPEC_pozice*8,Terminál_položka->Y_souřadnice+36+(ŘÁDEK_pozice-첫항목()+Terminál_položka->posouvat)*16,bod_kódu?bod_kódu:' ',색상들[řetězec_data&15],색상들[řetězec_data>>4]);
}
static void stříška_HODNOTA(int zobrazit_okno){if(!보이는지()||Terminál_položka->posouvat||Terminál_položka->SLOUPEC_pozice>=Terminál_položka->SLOUPCE||Terminál_položka->ŘÁDEK_pozice<Terminál_položka->맨위||Terminál_položka->ŘÁDEK_pozice>=Terminál_položka->맨위+Terminál_položka->ŘÁDEK_POČET)return;
    if(!zobrazit_okno||!Terminál_položka->가리개보임)그리기(Terminál_položka->ŘÁDEK_pozice,Terminál_položka->SLOUPEC_pozice);else 사각영역(Terminál_položka->souřadnice_x+12+Terminál_položka->SLOUPEC_pozice*8,Terminál_položka->Y_souřadnice+36+(Terminál_položka->ŘÁDEK_pozice-Terminál_položka->맨위)*16+14,8,2,색상들[Terminál_položka->전경색]);}
static void Obsah_HODNOTA(void){
    사각영역(Terminál_položka->souřadnice_x+12,Terminál_položka->Y_souřadnice+36,Terminál_položka->SLOUPCE*8,Terminál_položka->ŘÁDEK_POČET*16,색상들[0]);
    int 가로=Terminál_položka->souřadnice_x+12,Svislá_pozice=Terminál_položka->Y_souřadnice+36,폭=Terminál_položka->SLOUPCE*8,délka_HODNOTA=Terminál_položka->ŘÁDEK_POČET*16;
    if(보드그림범위(&가로,&Svislá_pozice,&폭,&délka_HODNOTA)){
    unsigned 첫줄=(Svislá_pozice-Terminál_položka->Y_souřadnice-36)/16,끝줄=(Svislá_pozice+délka_HODNOTA-Terminál_položka->Y_souřadnice-36+15)/16;
    unsigned 첫칸=(가로-Terminál_položka->souřadnice_x-12)/8,끝칸=(가로+폭-Terminál_položka->souřadnice_x-12+7)/8;
    if(첫칸)첫칸--; /* 잘림 mez_HODNOTA 왼쪽에서 시작한 두 přihrádka_položka 글자도 그린다. */
    for(unsigned 반환값=첫줄;반환값<끝줄;반환값++)for(unsigned bod_kódu=첫칸;bod_kódu<끝칸;bod_kódu++){
        unsigned ŘÁDEK_pozice=첫항목()-Terminál_položka->posouvat+반환값,znak_HODNOTA=Terminál_položka->글자칸들[ŘÁDEK_pozice%Historie_čára_POČET][bod_kódu],řetězec_data=Terminál_položka->모양들[ŘÁDEK_pozice%Historie_čára_POČET][bod_kódu];
        if(široký_znak(znak_HODNOTA)==2&&bod_kódu+1>=Terminál_položka->SLOUPCE)znak_HODNOTA=' ';
        if((znak_HODNOTA==0||znak_HODNOTA==' ')&&(řetězec_data>>4)==0)continue;
        Terminál_piktogram(Terminál_položka->souřadnice_x+12+bod_kódu*8,Terminál_položka->Y_souřadnice+36+반환값*16,znak_HODNOTA?znak_HODNOTA:' ',색상들[řetězec_data&15],색상들[řetězec_data>>4]);
    }}
    název_tabulka(Terminál_položka->souřadnice_x+12,Terminál_položka->Y_souřadnice+Terminál_položka->výška_HODNOTA-18,Terminál_položka->posouvat?"PgDn: recent output":Terminál_položka->너비>=500?"F6: next | Corner + left drag: resize":"Corner + left drag: resize",0xece8e2,0x403127);stříška_HODNOTA(1);
}
static void spuštění_rámec(int identifikátor_HODNOTA){
    Terminál_položka=&Windows_Seznam[identifikátor_HODNOTA];
    int 가로=Terminál_položka->souřadnice_x,Svislá_pozice=Terminál_položka->Y_souřadnice,폭=Terminál_položka->너비,délka_HODNOTA=Terminál_položka->výška_HODNOTA;
    if(!보드그림범위(&가로,&Svislá_pozice,&폭,&délka_HODNOTA))return;
    사각영역(Terminál_položka->souřadnice_x,Terminál_položka->Y_souřadnice,Terminál_položka->너비,Terminál_položka->výška_HODNOTA,0x403127);
    unsigned 색상=identifikátor_HODNOTA==fokus?0x905020:0x604438;사각영역(Terminál_položka->souřadnice_x,Terminál_položka->Y_souřadnice,Terminál_položka->너비,30,색상);
    název_tabulka(Terminál_položka->souřadnice_x+12,Terminál_položka->Y_souřadnice+7,"JKOROS Terminal",0xffffff,색상);
    char 수치[2]={(char)('1'+identifikátor_HODNOTA),0};název_tabulka(Terminál_položka->souřadnice_x+148,Terminál_položka->Y_souřadnice+7,수치,0xffffff,색상);
    název_tabulka(Terminál_položka->souřadnice_x+240,Terminál_položka->Y_souřadnice+7,Terminál_položka->너비>=500?(한글입력?"[CS] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[CS]":"[EN]"),0xffffff,색상);
    사각영역(Terminál_položka->souřadnice_x+Terminál_položka->너비-32,Terminál_položka->Y_souřadnice+4,26,22,0x5555b8);název_tabulka(Terminál_položka->souřadnice_x+Terminál_položka->너비-24,Terminál_položka->Y_souřadnice+7,"X",0xffffff,0x5555b8);
    Obsah_HODNOTA();
}
static void kreslit_scéna(void){
    if(!Plocha_pohled)return;사각영역(0,0,보드화면너비(),보드화면높이(),0x302018);사각영역(0,0,보드화면너비(),32,0x403127);
    사각영역(6,4,136,24,0x905020);název_tabulka(14,8,"+ New terminal",0xffffff,0x905020);
    for(int 순번=0;순번<4;순번++)if(Windows_Seznam[순번].살아있음){unsigned bod_kódu=fokus==순번?0x905020:0x604438;사각영역(154+순번*112,4,106,24,bod_kódu);název_tabulka(160+순번*112,8,"Terminal",0xffffff,bod_kódu);char řetězec_data[2]={(char)('1'+순번),0};název_tabulka(232+순번*112,8,řetězec_data,0xffffff,bod_kódu);}
    if(!položka_POČET)název_tabulka(140,210,"Click + New terminal to start",0xede9df,0x302018);
    for(int 순번=0;순번<položka_POČET;순번++)spuštění_rámec(pořadí_HODNOTA[순번]);화면다시그림(fokus);Terminál_položka=&Windows_Seznam[výstup];
}
static void Malování_oblast(int 가로,int Svislá_pozice,int 폭,int délka_HODNOTA){
    if(!Plocha_pohled||!보드그림범위(&가로,&Svislá_pozice,&폭,&délka_HODNOTA))return;
    for(int vstupní_řádek=Svislá_pozice;vstupní_řádek<Svislá_pozice+délka_HODNOTA;vstupní_řádek+=32){
        int pruh_výška=Svislá_pozice+délka_HODNOTA-vstupní_řádek;if(pruh_výška>32)pruh_výška=32;
        if(Panel_START_kreslení(가로,vstupní_řádek,폭,pruh_výška)){kreslit_scéna();Panel_Dokončit_kreslení();}
    }
}
static void 다시그리기(void){Malování_oblast(0,0,보드화면너비(),보드화면높이());}
/* 서로 겹치지 않는 새 Okno 영역과 Předchozí_zboží 자리의 네 띠를 복구한다. */
static void 창자리그리기(int 가로,int Svislá_pozice,int 폭,int délka_HODNOTA,Terminál *Okno){
    int 왼쪽=가로>(int)Okno->souřadnice_x?가로:(int)Okno->souřadnice_x;
    int 위쪽=Svislá_pozice>(int)Okno->Y_souřadnice?Svislá_pozice:(int)Okno->Y_souřadnice;
    int právo=가로+폭<(int)(Okno->souřadnice_x+Okno->너비)?가로+폭:(int)(Okno->souřadnice_x+Okno->너비);
    int 아래쪽=Svislá_pozice+délka_HODNOTA<(int)(Okno->Y_souřadnice+Okno->výška_HODNOTA)?Svislá_pozice+délka_HODNOTA:(int)(Okno->Y_souřadnice+Okno->výška_HODNOTA);
    Malování_oblast(Okno->souřadnice_x,Okno->Y_souřadnice,Okno->너비,Okno->výška_HODNOTA);
    if(왼쪽>=právo||위쪽>=아래쪽){Malování_oblast(가로,Svislá_pozice,폭,délka_HODNOTA);return;}
    Malování_oblast(가로,Svislá_pozice,폭,위쪽-Svislá_pozice);
    Malování_oblast(가로,아래쪽,폭,Svislá_pozice+délka_HODNOTA-아래쪽);
    Malování_oblast(가로,위쪽,왼쪽-가로,아래쪽-위쪽);
    Malování_oblast(právo,위쪽,가로+폭-právo,아래쪽-위쪽);
}
static void signál_fokus(void){informační_systémy_probíhá=(informační_systémy_probíhá&~15u)|(unsigned)(fokus+1)|0x10000;}
void Terminál_vstup_MODE(unsigned 한글여부){
    한글입력=한글여부!=0;
    /* Update title bars only: a mode switch must not erase an EL0 drawing. */
    if(fokus>=0){
        Terminál *okno_položka=&Windows_Seznam[fokus];
        název_tabulka(okno_položka->souřadnice_x+240,okno_položka->Y_souřadnice+7,okno_položka->너비>=500?(한글입력?"[CS] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[CS]":"[EN]"),0xffffff,0x905020);
    }
}
static void 앞으로올리기(int identifikátor_HODNOTA){if(identifikátor_HODNOTA<0||identifikátor_HODNOTA>=4||!Windows_Seznam[identifikátor_HODNOTA].살아있음)return;int dobrá_pozice=0;while(dobrá_pozice<položka_POČET&&pořadí_HODNOTA[dobrá_pozice]!=identifikátor_HODNOTA)dobrá_pozice++;for(;dobrá_pozice+1<položka_POČET;dobrá_pozice++)pořadí_HODNOTA[dobrá_pozice]=pořadí_HODNOTA[dobrá_pozice+1];pořadí_HODNOTA[položka_POČET-1]=identifikátor_HODNOTA;fokus=identifikátor_HODNOTA;signál_fokus();다시그리기();}
static void mezera(unsigned ŘÁDEK_pozice){for(unsigned bod_kódu=0;bod_kódu<최대열수;bod_kódu++){Terminál_položka->글자칸들[ŘÁDEK_pozice%Historie_čára_POČET][bod_kódu]=0;Terminál_položka->모양들[ŘÁDEK_pozice%Historie_čára_POČET][bod_kódu]=Terminál_položka->전경색|(Terminál_položka->배경색<<4);}}
static void vymazat_Obsah(void){Terminál_položka->ŘÁDEK_pozice=Terminál_položka->SLOUPEC_pozice=Terminál_položka->맨위=Terminál_položka->posouvat=0;for(unsigned 반환값=0;반환값<Historie_čára_POČET;반환값++)mezera(반환값);if(보이는지())Obsah_HODNOTA();}
static int Create_položka(void){
    if(!보드화면기억공간())return -19;int identifikátor_HODNOTA=0;while(identifikátor_HODNOTA<4&&Windows_Seznam[identifikátor_HODNOTA].살아있음)identifikátor_HODNOTA++;if(identifikátor_HODNOTA==4)return -28;
    Plocha_pohled=1;Terminál_položka=&Windows_Seznam[identifikátor_HODNOTA];memset(Terminál_položka,0,sizeof(*Terminál_položka));Terminál_položka->살아있음=1;Terminál_položka->너비=568;Terminál_položka->výška_HODNOTA=360;Terminál_položka->SLOUPCE=68;Terminál_položka->ŘÁDEK_POČET=19;Terminál_položka->souřadnice_x=12+identifikátor_HODNOTA*16;Terminál_položka->Y_souřadnice=48+identifikátor_HODNOTA*18;Terminál_položka->전경색=7;Terminál_položka->가리개보임=1;
    for(unsigned 반환값=0;반환값<Historie_čára_POČET;반환값++)mezera(반환값);pořadí_HODNOTA[položka_POČET++]=identifikátor_HODNOTA;fokus=identifikátor_HODNOTA;informační_systémy_probíhá|=1u<<(4+identifikátor_HODNOTA);signál_fokus();다시그리기();return identifikátor_HODNOTA+1;
}
static void Zavřít_okno(int identifikátor_HODNOTA){
    if(identifikátor_HODNOTA<0||identifikátor_HODNOTA>=4||!Windows_Seznam[identifikátor_HODNOTA].살아있음)return;Windows_Seznam[identifikátor_HODNOTA].살아있음=0;informační_systémy_probíhá|=1u<<(8+identifikátor_HODNOTA);
    int dobrá_pozice=0;while(dobrá_pozice<položka_POČET&&pořadí_HODNOTA[dobrá_pozice]!=identifikátor_HODNOTA)dobrá_pozice++;for(;dobrá_pozice+1<položka_POČET;dobrá_pozice++)pořadí_HODNOTA[dobrá_pozice]=pořadí_HODNOTA[dobrá_pozice+1];položka_POČET--;
    if(fokus==identifikátor_HODNOTA)fokus=položka_POČET?pořadí_HODNOTA[položka_POČET-1]:-1;signál_fokus();다시그리기();
}
static void 줄바꿈(void){Terminál_položka->SLOUPEC_pozice=0;Terminál_položka->ŘÁDEK_pozice++;if(Terminál_položka->ŘÁDEK_pozice>=Terminál_položka->맨위+Terminál_položka->ŘÁDEK_POČET){Terminál_položka->맨위++;mezera(Terminál_položka->ŘÁDEK_pozice);if(보이는지())Obsah_HODNOTA();}}
static void bod_kódu_451f2815(unsigned bod_kódu){
    if(bod_kódu==13){Terminál_položka->SLOUPEC_pozice=0;return;}if(bod_kódu==10){줄바꿈();return;}if(bod_kódu==8){if(Terminál_položka->SLOUPEC_pozice)Terminál_položka->SLOUPEC_pozice--;return;}
    if(bod_kódu==9){unsigned zboží_POČET=8-Terminál_položka->SLOUPEC_pozice%8;while(zboží_POČET--)bod_kódu_451f2815(' ');return;}if(bod_kódu<32||bod_kódu==127)return;
    unsigned 너비값=široký_znak(bod_kódu);if(Terminál_položka->SLOUPEC_pozice+너비값>Terminál_položka->SLOUPCE)줄바꿈();
    if(Terminál_položka->글자칸들[Terminál_položka->ŘÁDEK_pozice%Historie_čára_POČET][Terminál_položka->SLOUPEC_pozice]==0xffffffffu&&Terminál_položka->SLOUPEC_pozice){Terminál_položka->글자칸들[Terminál_položka->ŘÁDEK_pozice%Historie_čára_POČET][Terminál_položka->SLOUPEC_pozice-1]=' ';그리기(Terminál_položka->ŘÁDEK_pozice,Terminál_položka->SLOUPEC_pozice-1);}
    if(široký_znak(Terminál_položka->글자칸들[Terminál_položka->ŘÁDEK_pozice%Historie_čára_POČET][Terminál_položka->SLOUPEC_pozice])==2&&Terminál_položka->SLOUPEC_pozice+1<Terminál_položka->SLOUPCE){Terminál_položka->글자칸들[Terminál_položka->ŘÁDEK_pozice%Historie_čára_POČET][Terminál_položka->SLOUPEC_pozice+1]=' ';그리기(Terminál_položka->ŘÁDEK_pozice,Terminál_položka->SLOUPEC_pozice+1);}
    Terminál_položka->글자칸들[Terminál_položka->ŘÁDEK_pozice%Historie_čára_POČET][Terminál_položka->SLOUPEC_pozice]=bod_kódu;Terminál_položka->모양들[Terminál_položka->ŘÁDEK_pozice%Historie_čára_POČET][Terminál_položka->SLOUPEC_pozice]=Terminál_položka->전경색|(Terminál_položka->배경색<<4);
    if(너비값==2)Terminál_položka->글자칸들[Terminál_položka->ŘÁDEK_pozice%Historie_čára_POČET][Terminál_položka->SLOUPEC_pozice+1]=0xffffffffu;
    그리기(Terminál_položka->ŘÁDEK_pozice,Terminál_položka->SLOUPEC_pozice);Terminál_položka->SLOUPEC_pozice+=너비값;
}
static void úchyt_řízení_SEQUENCE(unsigned bod_kódu){
    unsigned zboží_POČET=Terminál_položka->parametr_HODNOTA[0]?Terminál_položka->parametr_HODNOTA[0]:1;
    if(bod_kódu=='m')for(unsigned 순번=0;순번<=Terminál_položka->parametr_INDEX;순번++){unsigned data_pozice=Terminál_položka->parametr_HODNOTA[순번];if(!data_pozice){Terminál_položka->전경색=7;Terminál_položka->배경색=0;}if(data_pozice==1&&Terminál_položka->전경색<8)Terminál_položka->전경색+=8;if(data_pozice==7){unsigned 유지=Terminál_položka->전경색;Terminál_položka->전경색=Terminál_položka->배경색;Terminál_položka->배경색=유지;}if(data_pozice>=30&&data_pozice<=37)Terminál_položka->전경색=data_pozice-30;if(data_pozice>=90&&data_pozice<=97)Terminál_položka->전경색=data_pozice-90+8;if(data_pozice>=40&&data_pozice<=47)Terminál_položka->배경색=data_pozice-40;if(data_pozice>=100&&data_pozice<=107)Terminál_položka->배경색=data_pozice-100+8;if(data_pozice==39)Terminál_položka->전경색=7;if(data_pozice==49)Terminál_položka->배경색=0;}
    if(bod_kódu=='J'&&(Terminál_položka->parametr_HODNOTA[0]==2||Terminál_položka->parametr_HODNOTA[0]==3))vymazat_Obsah();
    if(bod_kódu=='K'){unsigned 출발위치=Terminál_položka->parametr_HODNOTA[0]==2?0:Terminál_položka->SLOUPEC_pozice,도착위치=Terminál_položka->parametr_HODNOTA[0]==1?Terminál_položka->SLOUPEC_pozice+1:Terminál_položka->SLOUPCE;if(Terminál_položka->parametr_HODNOTA[0]==1)출발위치=0;for(unsigned 순번=출발위치;순번<도착위치&&순번<Terminál_položka->SLOUPCE;순번++){
        unsigned ŘÁDEK_HODNOTA=Terminál_položka->ŘÁDEK_pozice%Historie_čára_POČET,znak_HODNOTA=Terminál_položka->글자칸들[ŘÁDEK_HODNOTA][순번],tvar_HODNOTA=Terminál_položka->전경색|(Terminál_položka->배경색<<4);
        /* 넓은 vi 화면에서도 이미 빈 칸의 písmo_HODNOTA 화소를 되풀이해 칠하지 않는다. */
        int 바뀜=(znak_HODNOTA!=0&&znak_HODNOTA!=' ')||Terminál_položka->모양들[ŘÁDEK_HODNOTA][순번]!=tvar_HODNOTA;
        Terminál_položka->글자칸들[ŘÁDEK_HODNOTA][순번]=' ';Terminál_položka->모양들[ŘÁDEK_HODNOTA][순번]=tvar_HODNOTA;
        if(바뀜)그리기(Terminál_položka->ŘÁDEK_pozice,순번);
    }}
    if(bod_kódu=='D')Terminál_položka->SLOUPEC_pozice=zboží_POČET>Terminál_položka->SLOUPEC_pozice?0:Terminál_položka->SLOUPEC_pozice-zboží_POČET;if(bod_kódu=='C')Terminál_položka->SLOUPEC_pozice=Terminál_položka->SLOUPEC_pozice+zboží_POČET>=Terminál_položka->SLOUPCE?Terminál_položka->SLOUPCE-1:Terminál_položka->SLOUPEC_pozice+zboží_POČET;
    if(bod_kódu=='G')Terminál_položka->SLOUPEC_pozice=zboží_POČET>Terminál_položka->SLOUPCE?Terminál_položka->SLOUPCE-1:zboží_POČET-1;if(bod_kódu=='A')Terminál_položka->ŘÁDEK_pozice=zboží_POČET>Terminál_položka->ŘÁDEK_pozice-Terminál_položka->맨위?Terminál_položka->맨위:Terminál_položka->ŘÁDEK_pozice-zboží_POČET;
    if(bod_kódu=='B')Terminál_položka->ŘÁDEK_pozice=Terminál_položka->ŘÁDEK_pozice+zboží_POČET>=Terminál_položka->맨위+Terminál_položka->ŘÁDEK_POČET?Terminál_položka->맨위+Terminál_položka->ŘÁDEK_POČET-1:Terminál_položka->ŘÁDEK_pozice+zboží_POČET;
    if(bod_kódu=='H'||bod_kódu=='f'){Terminál_položka->ŘÁDEK_pozice=Terminál_položka->맨위+(zboží_POČET>Terminál_položka->ŘÁDEK_POČET?Terminál_položka->ŘÁDEK_POČET:zboží_POČET)-1;unsigned souřadnice_x=Terminál_položka->parametr_HODNOTA[1]?Terminál_položka->parametr_HODNOTA[1]:1;Terminál_položka->SLOUPEC_pozice=(souřadnice_x>Terminál_položka->SLOUPCE?Terminál_položka->SLOUPCE:souřadnice_x)-1;}
    if(bod_kódu=='s'){Terminál_položka->저장행=Terminál_položka->ŘÁDEK_pozice;Terminál_položka->저장열=Terminál_položka->SLOUPEC_pozice;}if(bod_kódu=='u'){Terminál_položka->ŘÁDEK_pozice=Terminál_položka->저장행;Terminál_položka->SLOUPEC_pozice=Terminál_položka->저장열<Terminál_položka->SLOUPCE?Terminál_položka->저장열:Terminál_položka->SLOUPCE-1;}
    if((bod_kódu=='h'||bod_kódu=='l')&&Terminál_položka->parametr_HODNOTA[0]==25)Terminál_položka->가리개보임=bod_kódu=='h';
}
void Terminál_bajt(unsigned SEKUNDA_HODNOTA){
    Terminál_položka=&Windows_Seznam[výstup];if(!Terminál_položka->살아있음)return;stříška_HODNOTA(0);if(Terminál_položka->posouvat){Terminál_položka->posouvat=0;if(보이는지())Obsah_HODNOTA();}
    if(Terminál_položka->탈출상태==1){Terminál_položka->탈출상태=SEKUNDA_HODNOTA=='['?2:0;Terminál_položka->parametr_INDEX=0;for(unsigned 순번=0;순번<4;순번++)Terminál_položka->parametr_HODNOTA[순번]=0;}
    else if(Terminál_položka->탈출상태==2){if(SEKUNDA_HODNOTA=='?'){}else if(SEKUNDA_HODNOTA>='0'&&SEKUNDA_HODNOTA<='9'){if(Terminál_položka->parametr_HODNOTA[Terminál_položka->parametr_INDEX]<10000)Terminál_položka->parametr_HODNOTA[Terminál_položka->parametr_INDEX]=Terminál_položka->parametr_HODNOTA[Terminál_položka->parametr_INDEX]*10+SEKUNDA_HODNOTA-'0';}else if(SEKUNDA_HODNOTA==';'&&Terminál_položka->parametr_INDEX<3)Terminál_položka->parametr_INDEX++;else{úchyt_řízení_SEQUENCE(SEKUNDA_HODNOTA);Terminál_položka->탈출상태=0;}}
    else if(SEKUNDA_HODNOTA==27){Terminál_položka->긴부호없는값=0;Terminál_položka->탈출상태=1;}else{
        if(Terminál_položka->긴부호없는값&&(SEKUNDA_HODNOTA&0xc0)!=0x80){Terminál_položka->긴부호없는값=0;bod_kódu_451f2815(0xfffd);}
        if(Terminál_položka->긴부호없는값){Terminál_položka->부호없는결과=Terminál_položka->부호없는결과*64+(SEKUNDA_HODNOTA&63);if(--Terminál_položka->긴부호없는값==0)bod_kódu_451f2815(Terminál_položka->부호없는결과<Terminál_položka->SMALL_HODNOTA||Terminál_položka->부호없는결과>0x10ffff||(Terminál_položka->부호없는결과>=0xd800&&Terminál_položka->부호없는결과<=0xdfff)?0xfffd:Terminál_položka->부호없는결과);}
        else if(SEKUNDA_HODNOTA<128)bod_kódu_451f2815(SEKUNDA_HODNOTA);else if(SEKUNDA_HODNOTA>=0xc2&&SEKUNDA_HODNOTA<=0xf4){Terminál_položka->긴부호없는값=SEKUNDA_HODNOTA<0xe0?1:SEKUNDA_HODNOTA<0xf0?2:3;Terminál_položka->부호없는결과=SEKUNDA_HODNOTA&((1u<<(6-Terminál_položka->긴부호없는값))-1);Terminál_položka->SMALL_HODNOTA=Terminál_položka->긴부호없는값==1?128:Terminál_položka->긴부호없는값==2?2048:65536;}else bod_kódu_451f2815(0xfffd);
    }stříška_HODNOTA(1);
}
int Terminál_probíhá(void){return informační_systémy_probíhá!=0;}
/* 모서리 INDEX: 1 좌상, 2 우상, 3 좌하, 4 우하. */
static int změnit_velikost_přetáhnout=-1,잡은모서리,잡은가로,잡은세로,처음가로,처음세로,처음너비,처음높이;
static int 가리킨창(int 가로,int Svislá_pozice) {
    for(int SEQUENCE_HODNOTA=položka_POČET-1;SEQUENCE_HODNOTA>=0;SEQUENCE_HODNOTA--){
        int identifikátor_HODNOTA=pořadí_HODNOTA[SEQUENCE_HODNOTA];Terminál *Okno=&Windows_Seznam[identifikátor_HODNOTA];
        if(가로>=(int)Okno->souřadnice_x&&Svislá_pozice>=(int)Okno->Y_souřadnice&&
           가로<(int)(Okno->souřadnice_x+Okno->너비)&&Svislá_pozice<(int)(Okno->Y_souřadnice+Okno->výška_HODNOTA))return identifikátor_HODNOTA;
    }return -1;
}
static int 모서리찾기(int identifikátor_HODNOTA,int 가로,int Svislá_pozice) {
    if(identifikátor_HODNOTA<0)return 0;Terminál *Okno=&Windows_Seznam[identifikátor_HODNOTA];
    int 왼쪽=가로<(int)Okno->souřadnice_x+8,právo=가로>=(int)(Okno->souřadnice_x+Okno->너비)-8;
    int 위쪽=Svislá_pozice<(int)Okno->Y_souřadnice+8,아래쪽=Svislá_pozice>=(int)(Okno->Y_souřadnice+Okno->výška_HODNOTA)-8;
    return (왼쪽||právo)&&(위쪽||아래쪽)?1+právo+아래쪽*2:0;
}
static int oddělovač_HODNOTA(int HODNOTA,int 최소,int 최대){return HODNOTA<최소?최소:HODNOTA>최대?최대:HODNOTA;}
static void přesunout_změnit_velikost(int 가로,int Svislá_pozice) {
    Terminál *Okno=&Windows_Seznam[změnit_velikost_přetáhnout];int 왼쪽=처음가로,위쪽=처음세로,právo=처음가로+처음너비,아래쪽=처음세로+처음높이;
    if(잡은모서리==1||잡은모서리==3)왼쪽=oddělovač_HODNOTA(처음가로+가로-잡은가로,0,právo-360);
    else právo=oddělovač_HODNOTA(처음가로+처음너비+가로-잡은가로,왼쪽+360,보드화면너비());
    if(잡은모서리<=2)위쪽=oddělovač_HODNOTA(처음세로+Svislá_pozice-잡은세로,34,아래쪽-216);
    else 아래쪽=oddělovač_HODNOTA(처음세로+처음높이+Svislá_pozice-잡은세로,위쪽+216,보드화면높이());
    unsigned SLOUPCE=(právo-왼쪽-24)/8,ŘÁDEK_POČET=(아래쪽-위쪽-56)/16;
    if(Okno->SLOUPCE!=SLOUPCE||Okno->ŘÁDEK_POČET!=ŘÁDEK_POČET){
        Okno->크기바뀜=1;Okno->SLOUPCE=SLOUPCE;Okno->ŘÁDEK_POČET=ŘÁDEK_POČET;
        if(Okno->SLOUPEC_pozice>=SLOUPCE)Okno->SLOUPEC_pozice=SLOUPCE-1;
        if(Okno->ŘÁDEK_pozice>=Okno->맨위+ŘÁDEK_POČET)Okno->맨위=Okno->ŘÁDEK_pozice-ŘÁDEK_POČET+1;
        unsigned 한도=Okno->맨위;if(한도>Historie_čára_POČET-ŘÁDEK_POČET)한도=Historie_čára_POČET-ŘÁDEK_POČET;
        if(Okno->posouvat>한도)Okno->posouvat=한도;
    }
    int 옛가로=Okno->souřadnice_x,옛세로=Okno->Y_souřadnice,옛폭=Okno->너비,옛길이=Okno->výška_HODNOTA;
    if(옛가로==왼쪽&&옛세로==위쪽&&옛폭==právo-왼쪽&&옛길이==아래쪽-위쪽)return;
    Okno->souřadnice_x=왼쪽;Okno->Y_souřadnice=위쪽;Okno->너비=právo-왼쪽;Okno->výška_HODNOTA=아래쪽-위쪽;
    창자리그리기(옛가로,옛세로,옛폭,옛길이,Okno);
}
void Terminál_ukazatel(unsigned Další_zboží,int souřadnice_x,int Y_souřadnice){
    unsigned 눌림=Další_zboží&~단추들;단추들=Další_zboží;
    if(!Plocha_pohled){přetáhnout_HODNOTA=-1;změnit_velikost_přetáhnout=-1;Panel_ukazatel(souřadnice_x,Y_souřadnice,1);return;}
    if(!(Další_zboží&1)){přetáhnout_HODNOTA=-1;změnit_velikost_přetáhnout=-1;}
    if(změnit_velikost_přetáhnout>=0&&!Windows_Seznam[změnit_velikost_přetáhnout].살아있음)změnit_velikost_přetáhnout=-1;
    if(přetáhnout_HODNOTA>=0&&!Windows_Seznam[přetáhnout_HODNOTA].살아있음)přetáhnout_HODNOTA=-1;
    if(změnit_velikost_přetáhnout>=0){
        přesunout_změnit_velikost(souřadnice_x,Y_souřadnice);Panel_ukazatel(souřadnice_x,Y_souřadnice,잡은모서리==1||잡은모서리==4?2:3);return;
    }
    Panel_ukazatel(souřadnice_x,Y_souřadnice,1);
    if(přetáhnout_HODNOTA>=0){
        Terminál *Okno=&Windows_Seznam[přetáhnout_HODNOTA];
        int 옛가로=Okno->souřadnice_x,옛세로=Okno->Y_souřadnice;
        Okno->souřadnice_x=oddělovač_HODNOTA(souřadnice_x-přetáhnout_X,0,보드화면너비()-Okno->너비);
        Okno->Y_souřadnice=oddělovač_HODNOTA(Y_souřadnice-přetáhnout_Y,34,보드화면높이()-Okno->výška_HODNOTA);
        if(옛가로!=(int)Okno->souřadnice_x||옛세로!=(int)Okno->Y_souřadnice)창자리그리기(옛가로,옛세로,Okno->너비,Okno->výška_HODNOTA,Okno);
        return;
    }
    extern int 화면덮음(int,int,int);
    if(화면덮음(fokus,souřadnice_x,Y_souřadnice)){화면가리킴(fokus,눌림,souřadnice_x,Y_souřadnice);return;}
    int identifikátor_HODNOTA=가리킨창(souřadnice_x,Y_souřadnice),모서리=모서리찾기(identifikátor_HODNOTA,souřadnice_x,Y_souřadnice);
    if(모서리)Panel_ukazatel(souřadnice_x,Y_souřadnice,모서리==1||모서리==4?2:3);
    if(눌림&1){
        if(모서리){
            Terminál *Okno=&Windows_Seznam[identifikátor_HODNOTA];změnit_velikost_přetáhnout=identifikátor_HODNOTA;잡은모서리=모서리;잡은가로=souřadnice_x;잡은세로=Y_souřadnice;
            처음가로=Okno->souřadnice_x;처음세로=Okno->Y_souřadnice;처음너비=Okno->너비;처음높이=Okno->výška_HODNOTA;
            if(identifikátor_HODNOTA!=fokus)앞으로올리기(identifikátor_HODNOTA);return;
        }
        if(Y_souřadnice<32&&souřadnice_x>=6&&souřadnice_x<142){Create_položka();return;}
        if(Y_souřadnice<32&&souřadnice_x>=154&&souřadnice_x<602){앞으로올리기((souřadnice_x-154)/112);return;}
        if(identifikátor_HODNOTA>=0){
            Terminál *Okno=&Windows_Seznam[identifikátor_HODNOTA];
            if(Y_souřadnice<(int)Okno->Y_souřadnice+30&&souřadnice_x>=(int)(Okno->souřadnice_x+Okno->너비)-32){Zavřít_okno(identifikátor_HODNOTA);return;}
            if(identifikátor_HODNOTA!=fokus)앞으로올리기(identifikátor_HODNOTA);
            if(Y_souřadnice<(int)Okno->Y_souřadnice+30){přetáhnout_HODNOTA=identifikátor_HODNOTA;přetáhnout_X=souřadnice_x-Okno->souřadnice_x;přetáhnout_Y=Y_souřadnice-Okno->Y_souřadnice;}return;
        }
    }
    if(fokus>=0&&(눌림&(8|16))){Terminál_položka=&Windows_Seznam[fokus];if(눌림&8){unsigned 한도=Terminál_položka->맨위;if(한도>Historie_čára_POČET-Terminál_položka->ŘÁDEK_POČET)한도=Historie_čára_POČET-Terminál_položka->ŘÁDEK_POČET;Terminál_položka->posouvat=Terminál_položka->posouvat+9>한도?한도:Terminál_položka->posouvat+9;}else Terminál_položka->posouvat=Terminál_položka->posouvat<9?0:Terminál_položka->posouvat-9;다시그리기();}
}
void 터미널바로가기키(unsigned 누름값){if(누름값==1)Create_položka();if(누름값==2&&položka_POČET)앞으로올리기(pořadí_HODNOTA[0]);if(누름값==3)Zavřít_okno(fokus);}
počítač_Word Panel_Terminál(počítač_Word Akce){
    if(Akce==300){if(!Windows_Seznam[výstup].살아있음)return Create_položka();Plocha_pohled=1;다시그리기();return 0;}
    if(Akce==0){Zavřít_okno(fokus);return 0;}if(Akce==1)return (uint32_t)Create_položka();if(Akce==2)return fokus>=0;
    if(Akce==9){Plocha_pohled=0;return 0;}if(Akce==7)return položka_POČET;if(Akce==10)return fokus+1;if(Akce==11)return výstup;
    if(Akce==13){Terminál *Okno=&Windows_Seznam[výstup];return Okno->살아있음?(Okno->ŘÁDEK_POČET<<16)|Okno->SLOUPCE:(19<<16)|68;}
    if(Akce==14){unsigned HODNOTA=Windows_Seznam[výstup].크기바뀜;Windows_Seznam[výstup].크기바뀜=0;return HODNOTA;}
    if(Akce==12){unsigned HODNOTA=informační_systémy_probíhá;informační_systémy_probíhá=0;return HODNOTA;}
    if(Akce>=20&&Akce<24)return Windows_Seznam[Akce-20].살아있음;
    if(Akce>=100&&Akce<104){výstup=Akce-100;Terminál_položka=&Windows_Seznam[výstup];return 0;}
    if(Akce>=200&&Akce<204){앞으로올리기(Akce-200);return 0;}
    if(Akce==3){다시그리기();return 0;}Terminál_položka=&Windows_Seznam[výstup];if(!Terminál_položka->살아있음)return 0;
    if(Akce==4)vymazat_Obsah();if(Akce==5||Akce==6){unsigned Předchozí_zboží=단추들;Terminál_ukazatel(Akce==5?8:16,0,0);단추들=Předchozí_zboží;}return 1;
}
