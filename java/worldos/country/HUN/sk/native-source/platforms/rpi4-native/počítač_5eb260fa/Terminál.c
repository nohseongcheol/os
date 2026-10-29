#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* vlastné 네 Okno 합성과 UTF-8 Terminál. 바뀐 영역의 Dokončené_úlohy_VALUE 그림만 표시한다. */
#include <stdint.h>
#include <stddef.h>
typedef uintptr_t počítač_Word;
extern počítač_Word Panel_pixel(počítač_Word,počítač_Word,počítač_Word),보드화면기억공간(void);
extern void *memset(void *,int,size_t);
extern const unsigned char Terminál_písmo[];
#define 최대열수 237
#define História_linka_COUNT 160
typedef struct {
    uint32_t 글자칸들[História_linka_COUNT][최대열수]; uint8_t 모양들[História_linka_COUNT][최대열수];
    unsigned 너비,výška_VALUE,COLUMNS,ROW_COUNT,크기바뀜;
    unsigned 살아있음,X_súradnica,Y_súradnica,ROW_pozícia,COLUMN_pozícia,맨위,posúvať,전경색,배경색,탈출상태,parameter_VALUE[4],parameter_INDEX,저장행,저장열;
    unsigned 부호없는결과,긴부호없는값,SMALL_VALUE,대체화면,가리개보임;
} Terminál_d413d4bc;
static Terminál_d413d4bc Windows_Zoznam[4];
static int ohnisko=-1,출력결과,poradie_VALUE[4],položka_COUNT_8f7753a1,presunúť_VALUE=-1,presunúť_X,presunúť_Y;
static unsigned Informačné_systémy_čakajúci,단추들,počítač_zobraziť,한글입력;
static const uint32_t 색상들[16]={0x201a15,0x6060df,0x9dcc86,0x80cfea,0xefaf72,0xca96c9,0xceda76,0xede9df,0x858078,0x8888ff,0xb9eba7,0xa5eaff,0xffcc99,0xf0bef1,0xf0f0a0,0xffffff};
extern int 화면보임(int),화면가리킴(int,unsigned,int,int);
extern void 화면다시그림(int);
static Terminál_d413d4bc *Terminál_položka;
static unsigned 넓은글자(unsigned bod_kódu){return bod_kódu>=256?2:1;}
static void 사각영역(unsigned X_súradnica,unsigned Y_súradnica,unsigned 너비값,unsigned 높이값,unsigned 색상){
    Panel_obdĺžnik_výplň(X_súradnica,Y_súradnica,너비값,높이값,색상);
}
void Terminál_piktogram(unsigned X_súradnica,unsigned Y_súradnica,unsigned bod_kódu,unsigned 전경색,unsigned 배경색){
    unsigned 너비=넓은글자(bod_kódu)*8;if(bod_kódu==0xffffffffu)return;
    int 왼쪽=X_súradnica,위쪽=Y_súradnica,폭=너비,dĺžka_VALUE=16;
    if(!보드그림범위(&왼쪽,&위쪽,&폭,&dĺžka_VALUE))return;
    if(bod_kódu==' '){Panel_obdĺžnik_výplň(왼쪽,위쪽,폭,dĺžka_VALUE,배경색);return;}
    unsigned LOOKUP_INDEX=bod_kódu<65536?bod_kódu:bod_kódu>=0x1f600&&bod_kódu<0x1f650?65536+bod_kódu-0x1f600:0xfffd;
    const unsigned char *písmo_VALUE=Terminál_písmo+LOOKUP_INDEX*32;
    for(int riadok=위쪽;riadok<위쪽+dĺžka_VALUE;riadok++){unsigned Background_Intelligent_Transfer_Service_Zoznam=písmo_VALUE[(riadok-Y_súradnica)*2]*256+písmo_VALUE[(riadok-Y_súradnica)*2+1];for(int 칸=왼쪽;칸<왼쪽+폭;칸++)Panel_pixel(칸,riadok,(Background_Intelligent_Transfer_Service_Zoznam&(0x8000>>(칸-X_súradnica)))?전경색:배경색);}
}
static void názov_tabuľka(unsigned X_súradnica,unsigned Y_súradnica,const char *reťazec_údaje,unsigned 전경색,unsigned 배경색){while(*reťazec_údaje){unsigned bod_kódu=(unsigned char)*reťazec_údaje++, 남은수=0;if(bod_kódu>=0xc0){남은수=bod_kódu<0xe0?1:bod_kódu<0xf0?2:3;bod_kódu&=(1u<<(6-남은수))-1;while(남은수--&&*reťazec_údaje)bod_kódu=(bod_kódu<<6)|((unsigned char)*reťazec_údaje++&63);}Terminál_piktogram(X_súradnica,Y_súradnica,bod_kódu,전경색,배경색);X_súradnica+=넓은글자(bod_kódu)*8;}}
static unsigned 첫항목(void){return Terminál_položka->맨위;}
static int 보이는지(void){return Terminál_položka->살아있음&&ohnisko>=0&&Terminál_položka==&Windows_Zoznam[ohnisko]&&!화면보임(ohnisko);}
static void 그리기(unsigned ROW_pozícia,unsigned COLUMN_pozícia){
    if(!보이는지()||ROW_pozícia<첫항목()-Terminál_položka->posúvať||ROW_pozícia>=첫항목()-Terminál_položka->posúvať+Terminál_položka->ROW_COUNT||COLUMN_pozícia>=Terminál_položka->COLUMNS)return;
    unsigned bod_kódu=Terminál_položka->글자칸들[ROW_pozícia%História_linka_COUNT][COLUMN_pozícia],reťazec_údaje=Terminál_položka->모양들[ROW_pozícia%História_linka_COUNT][COLUMN_pozícia];
    if(넓은글자(bod_kódu)==2&&COLUMN_pozícia+1>=Terminál_položka->COLUMNS)bod_kódu=' ';
    Terminál_piktogram(Terminál_položka->X_súradnica+12+COLUMN_pozícia*8,Terminál_položka->Y_súradnica+36+(ROW_pozícia-첫항목()+Terminál_položka->posúvať)*16,bod_kódu?bod_kódu:' ',색상들[reťazec_údaje&15],색상들[reťazec_údaje>>4]);
}
static void znak_VALUE_be8150db(int zobraziť_okno){if(!보이는지()||Terminál_položka->posúvať||Terminál_položka->COLUMN_pozícia>=Terminál_položka->COLUMNS||Terminál_položka->ROW_pozícia<Terminál_položka->맨위||Terminál_položka->ROW_pozícia>=Terminál_položka->맨위+Terminál_položka->ROW_COUNT)return;
    if(!zobraziť_okno||!Terminál_položka->가리개보임)그리기(Terminál_položka->ROW_pozícia,Terminál_položka->COLUMN_pozícia);else 사각영역(Terminál_položka->X_súradnica+12+Terminál_položka->COLUMN_pozícia*8,Terminál_položka->Y_súradnica+36+(Terminál_položka->ROW_pozícia-Terminál_položka->맨위)*16+14,8,2,색상들[Terminál_položka->전경색]);}
static void obsah_VALUE(void){
    사각영역(Terminál_položka->X_súradnica+12,Terminál_položka->Y_súradnica+36,Terminál_položka->COLUMNS*8,Terminál_položka->ROW_COUNT*16,색상들[0]);
    int 가로=Terminál_položka->X_súradnica+12,vertikála_pozícia=Terminál_položka->Y_súradnica+36,폭=Terminál_položka->COLUMNS*8,dĺžka_VALUE=Terminál_položka->ROW_COUNT*16;
    if(보드그림범위(&가로,&vertikála_pozícia,&폭,&dĺžka_VALUE)){
    unsigned 첫줄=(vertikála_pozícia-Terminál_položka->Y_súradnica-36)/16,끝줄=(vertikála_pozícia+dĺžka_VALUE-Terminál_položka->Y_súradnica-36+15)/16;
    unsigned 첫칸=(가로-Terminál_položka->X_súradnica-12)/8,끝칸=(가로+폭-Terminál_položka->X_súradnica-12+7)/8;
    if(첫칸)첫칸--; /* 잘림 경계 왼쪽에서 시작한 두 칸 글자도 그린다. */
    for(unsigned 반환값=첫줄;반환값<끝줄;반환값++)for(unsigned bod_kódu=첫칸;bod_kódu<끝칸;bod_kódu++){
        unsigned ROW_pozícia=첫항목()-Terminál_položka->posúvať+반환값,znak_VALUE=Terminál_položka->글자칸들[ROW_pozícia%História_linka_COUNT][bod_kódu],reťazec_údaje=Terminál_položka->모양들[ROW_pozícia%História_linka_COUNT][bod_kódu];
        if(넓은글자(znak_VALUE)==2&&bod_kódu+1>=Terminál_položka->COLUMNS)znak_VALUE=' ';
        if((znak_VALUE==0||znak_VALUE==' ')&&(reťazec_údaje>>4)==0)continue;
        Terminál_piktogram(Terminál_položka->X_súradnica+12+bod_kódu*8,Terminál_položka->Y_súradnica+36+반환값*16,znak_VALUE?znak_VALUE:' ',색상들[reťazec_údaje&15],색상들[reťazec_údaje>>4]);
    }}
    názov_tabuľka(Terminál_položka->X_súradnica+12,Terminál_položka->Y_súradnica+Terminál_položka->výška_VALUE-18,Terminál_položka->posúvať?"PgDn: recent output":Terminál_položka->너비>=500?"F6: next | Corner + left drag: resize":"Corner + left drag: resize",0xece8e2,0x403127);znak_VALUE_be8150db(1);
}
static void 실행틀(int identifikátor_VALUE){
    Terminál_položka=&Windows_Zoznam[identifikátor_VALUE];
    int 가로=Terminál_položka->X_súradnica,vertikála_pozícia=Terminál_položka->Y_súradnica,폭=Terminál_položka->너비,dĺžka_VALUE=Terminál_položka->výška_VALUE;
    if(!보드그림범위(&가로,&vertikála_pozícia,&폭,&dĺžka_VALUE))return;
    사각영역(Terminál_položka->X_súradnica,Terminál_položka->Y_súradnica,Terminál_položka->너비,Terminál_položka->výška_VALUE,0x403127);
    unsigned 색상=identifikátor_VALUE==ohnisko?0x905020:0x604438;사각영역(Terminál_položka->X_súradnica,Terminál_položka->Y_súradnica,Terminál_položka->너비,30,색상);
    názov_tabuľka(Terminál_položka->X_súradnica+12,Terminál_položka->Y_súradnica+7,"JKOROS Terminal",0xffffff,색상);
    char 수치[2]={(char)('1'+identifikátor_VALUE),0};názov_tabuľka(Terminál_položka->X_súradnica+148,Terminál_položka->Y_súradnica+7,수치,0xffffff,색상);
    názov_tabuľka(Terminál_položka->X_súradnica+240,Terminál_položka->Y_súradnica+7,Terminál_položka->너비>=500?(한글입력?"[SK] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[SK]":"[EN]"),0xffffff,색상);
    사각영역(Terminál_položka->X_súradnica+Terminál_položka->너비-32,Terminál_položka->Y_súradnica+4,26,22,0x5555b8);názov_tabuľka(Terminál_položka->X_súradnica+Terminál_položka->너비-24,Terminál_položka->Y_súradnica+7,"X",0xffffff,0x5555b8);
    obsah_VALUE();
}
static void kresliť_scéna(void){
    if(!počítač_zobraziť)return;사각영역(0,0,보드화면너비(),보드화면높이(),0x302018);사각영역(0,0,보드화면너비(),32,0x403127);
    사각영역(6,4,136,24,0x905020);názov_tabuľka(14,8,"+ New terminal",0xffffff,0x905020);
    for(int 순번=0;순번<4;순번++)if(Windows_Zoznam[순번].살아있음){unsigned bod_kódu=ohnisko==순번?0x905020:0x604438;사각영역(154+순번*112,4,106,24,bod_kódu);názov_tabuľka(160+순번*112,8,"Terminal",0xffffff,bod_kódu);char reťazec_údaje[2]={(char)('1'+순번),0};názov_tabuľka(232+순번*112,8,reťazec_údaje,0xffffff,bod_kódu);}
    if(!položka_COUNT_8f7753a1)názov_tabuľka(140,210,"Click + New terminal to start",0xede9df,0x302018);
    for(int 순번=0;순번<položka_COUNT_8f7753a1;순번++)실행틀(poradie_VALUE[순번]);화면다시그림(ohnisko);Terminál_položka=&Windows_Zoznam[출력결과];
}
static void Skicár_oblasť(int 가로,int vertikála_pozícia,int 폭,int dĺžka_VALUE){
    if(!počítač_zobraziť||!보드그림범위(&가로,&vertikála_pozícia,&폭,&dĺžka_VALUE))return;
    for(int riadok=vertikála_pozícia;riadok<vertikála_pozícia+dĺžka_VALUE;riadok+=32){
        int pruh_výška=vertikála_pozícia+dĺžka_VALUE-riadok;if(pruh_výška>32)pruh_výška=32;
        if(Panel_START_kresba(가로,riadok,폭,pruh_výška)){kresliť_scéna();Panel_Dokončiť_kresba();}
    }
}
static void 다시그리기(void){Skicár_oblasť(0,0,보드화면너비(),보드화면높이());}
/* 서로 겹치지 않는 새 Okno 영역과 이전 자리의 네 띠를 복구한다. */
static void 창자리그리기(int 가로,int vertikála_pozícia,int 폭,int dĺžka_VALUE,Terminál_d413d4bc *Okno){
    int 왼쪽=가로>(int)Okno->X_súradnica?가로:(int)Okno->X_súradnica;
    int 위쪽=vertikála_pozícia>(int)Okno->Y_súradnica?vertikála_pozícia:(int)Okno->Y_súradnica;
    int RIGHT=가로+폭<(int)(Okno->X_súradnica+Okno->너비)?가로+폭:(int)(Okno->X_súradnica+Okno->너비);
    int 아래쪽=vertikála_pozícia+dĺžka_VALUE<(int)(Okno->Y_súradnica+Okno->výška_VALUE)?vertikála_pozícia+dĺžka_VALUE:(int)(Okno->Y_súradnica+Okno->výška_VALUE);
    Skicár_oblasť(Okno->X_súradnica,Okno->Y_súradnica,Okno->너비,Okno->výška_VALUE);
    if(왼쪽>=RIGHT||위쪽>=아래쪽){Skicár_oblasť(가로,vertikála_pozícia,폭,dĺžka_VALUE);return;}
    Skicár_oblasť(가로,vertikála_pozícia,폭,위쪽-vertikála_pozícia);
    Skicár_oblasť(가로,아래쪽,폭,vertikála_pozícia+dĺžka_VALUE-아래쪽);
    Skicár_oblasť(가로,위쪽,왼쪽-가로,아래쪽-위쪽);
    Skicár_oblasť(RIGHT,위쪽,가로+폭-RIGHT,아래쪽-위쪽);
}
static void signál_ohnisko(void){Informačné_systémy_čakajúci=(Informačné_systémy_čakajúci&~15u)|(unsigned)(ohnisko+1)|0x10000;}
void Terminál_vstup_MODE(unsigned 한글여부){
    한글입력=한글여부!=0;
    /* Update title bars only: a mode switch must not erase an EL0 drawing. */
    if(ohnisko>=0){
        Terminál_d413d4bc *okno_položka=&Windows_Zoznam[ohnisko];
        názov_tabuľka(okno_položka->X_súradnica+240,okno_položka->Y_súradnica+7,okno_položka->너비>=500?(한글입력?"[SK] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[SK]":"[EN]"),0xffffff,0x905020);
    }
}
static void 앞으로올리기(int identifikátor_VALUE){if(identifikátor_VALUE<0||identifikátor_VALUE>=4||!Windows_Zoznam[identifikátor_VALUE].살아있음)return;int v_termíne_splatnosti_pozícia=0;while(v_termíne_splatnosti_pozícia<položka_COUNT_8f7753a1&&poradie_VALUE[v_termíne_splatnosti_pozícia]!=identifikátor_VALUE)v_termíne_splatnosti_pozícia++;for(;v_termíne_splatnosti_pozícia+1<položka_COUNT_8f7753a1;v_termíne_splatnosti_pozícia++)poradie_VALUE[v_termíne_splatnosti_pozícia]=poradie_VALUE[v_termíne_splatnosti_pozícia+1];poradie_VALUE[položka_COUNT_8f7753a1-1]=identifikátor_VALUE;ohnisko=identifikátor_VALUE;signál_ohnisko();다시그리기();}
static void 빈칸채우기(unsigned ROW_pozícia){for(unsigned bod_kódu=0;bod_kódu<최대열수;bod_kódu++){Terminál_položka->글자칸들[ROW_pozícia%História_linka_COUNT][bod_kódu]=0;Terminál_položka->모양들[ROW_pozícia%História_linka_COUNT][bod_kódu]=Terminál_položka->전경색|(Terminál_položka->배경색<<4);}}
static void vymazať_Obsah(void){Terminál_položka->ROW_pozícia=Terminál_položka->COLUMN_pozícia=Terminál_položka->맨위=Terminál_položka->posúvať=0;for(unsigned 반환값=0;반환값<História_linka_COUNT;반환값++)빈칸채우기(반환값);if(보이는지())obsah_VALUE();}
static int Create_položka(void){
    if(!보드화면기억공간())return -19;int identifikátor_VALUE=0;while(identifikátor_VALUE<4&&Windows_Zoznam[identifikátor_VALUE].살아있음)identifikátor_VALUE++;if(identifikátor_VALUE==4)return -28;
    počítač_zobraziť=1;Terminál_položka=&Windows_Zoznam[identifikátor_VALUE];memset(Terminál_položka,0,sizeof(*Terminál_položka));Terminál_položka->살아있음=1;Terminál_položka->너비=568;Terminál_položka->výška_VALUE=360;Terminál_položka->COLUMNS=68;Terminál_položka->ROW_COUNT=19;Terminál_položka->X_súradnica=12+identifikátor_VALUE*16;Terminál_položka->Y_súradnica=48+identifikátor_VALUE*18;Terminál_položka->전경색=7;Terminál_položka->가리개보임=1;
    for(unsigned 반환값=0;반환값<História_linka_COUNT;반환값++)빈칸채우기(반환값);poradie_VALUE[položka_COUNT_8f7753a1++]=identifikátor_VALUE;ohnisko=identifikátor_VALUE;Informačné_systémy_čakajúci|=1u<<(4+identifikátor_VALUE);signál_ohnisko();다시그리기();return identifikátor_VALUE+1;
}
static void Zavrieť_okno(int identifikátor_VALUE){
    if(identifikátor_VALUE<0||identifikátor_VALUE>=4||!Windows_Zoznam[identifikátor_VALUE].살아있음)return;Windows_Zoznam[identifikátor_VALUE].살아있음=0;Informačné_systémy_čakajúci|=1u<<(8+identifikátor_VALUE);
    int v_termíne_splatnosti_pozícia=0;while(v_termíne_splatnosti_pozícia<položka_COUNT_8f7753a1&&poradie_VALUE[v_termíne_splatnosti_pozícia]!=identifikátor_VALUE)v_termíne_splatnosti_pozícia++;for(;v_termíne_splatnosti_pozícia+1<položka_COUNT_8f7753a1;v_termíne_splatnosti_pozícia++)poradie_VALUE[v_termíne_splatnosti_pozícia]=poradie_VALUE[v_termíne_splatnosti_pozícia+1];položka_COUNT_8f7753a1--;
    if(ohnisko==identifikátor_VALUE)ohnisko=položka_COUNT_8f7753a1?poradie_VALUE[položka_COUNT_8f7753a1-1]:-1;signál_ohnisko();다시그리기();
}
static void 줄바꿈(void){Terminál_položka->COLUMN_pozícia=0;Terminál_položka->ROW_pozícia++;if(Terminál_položka->ROW_pozícia>=Terminál_položka->맨위+Terminál_položka->ROW_COUNT){Terminál_položka->맨위++;빈칸채우기(Terminál_položka->ROW_pozícia);if(보이는지())obsah_VALUE();}}
static void bod_kódu_451f2815(unsigned bod_kódu){
    if(bod_kódu==13){Terminál_položka->COLUMN_pozícia=0;return;}if(bod_kódu==10){줄바꿈();return;}if(bod_kódu==8){if(Terminál_položka->COLUMN_pozícia)Terminál_položka->COLUMN_pozícia--;return;}
    if(bod_kódu==9){unsigned položka_COUNT=8-Terminál_položka->COLUMN_pozícia%8;while(položka_COUNT--)bod_kódu_451f2815(' ');return;}if(bod_kódu<32||bod_kódu==127)return;
    unsigned 너비값=넓은글자(bod_kódu);if(Terminál_položka->COLUMN_pozícia+너비값>Terminál_položka->COLUMNS)줄바꿈();
    if(Terminál_položka->글자칸들[Terminál_položka->ROW_pozícia%História_linka_COUNT][Terminál_položka->COLUMN_pozícia]==0xffffffffu&&Terminál_položka->COLUMN_pozícia){Terminál_položka->글자칸들[Terminál_položka->ROW_pozícia%História_linka_COUNT][Terminál_položka->COLUMN_pozícia-1]=' ';그리기(Terminál_položka->ROW_pozícia,Terminál_položka->COLUMN_pozícia-1);}
    if(넓은글자(Terminál_položka->글자칸들[Terminál_položka->ROW_pozícia%História_linka_COUNT][Terminál_položka->COLUMN_pozícia])==2&&Terminál_položka->COLUMN_pozícia+1<Terminál_položka->COLUMNS){Terminál_položka->글자칸들[Terminál_položka->ROW_pozícia%História_linka_COUNT][Terminál_položka->COLUMN_pozícia+1]=' ';그리기(Terminál_položka->ROW_pozícia,Terminál_položka->COLUMN_pozícia+1);}
    Terminál_položka->글자칸들[Terminál_položka->ROW_pozícia%História_linka_COUNT][Terminál_položka->COLUMN_pozícia]=bod_kódu;Terminál_položka->모양들[Terminál_položka->ROW_pozícia%História_linka_COUNT][Terminál_položka->COLUMN_pozícia]=Terminál_položka->전경색|(Terminál_položka->배경색<<4);
    if(너비값==2)Terminál_položka->글자칸들[Terminál_položka->ROW_pozícia%História_linka_COUNT][Terminál_položka->COLUMN_pozícia+1]=0xffffffffu;
    그리기(Terminál_položka->ROW_pozícia,Terminál_položka->COLUMN_pozícia);Terminál_položka->COLUMN_pozícia+=너비값;
}
static void rukoväť_riadenie_SEQUENCE(unsigned bod_kódu){
    unsigned položka_COUNT=Terminál_položka->parameter_VALUE[0]?Terminál_položka->parameter_VALUE[0]:1;
    if(bod_kódu=='m')for(unsigned 순번=0;순번<=Terminál_položka->parameter_INDEX;순번++){unsigned údaje_pozícia=Terminál_položka->parameter_VALUE[순번];if(!údaje_pozícia){Terminál_položka->전경색=7;Terminál_položka->배경색=0;}if(údaje_pozícia==1&&Terminál_položka->전경색<8)Terminál_položka->전경색+=8;if(údaje_pozícia==7){unsigned 유지=Terminál_položka->전경색;Terminál_položka->전경색=Terminál_položka->배경색;Terminál_položka->배경색=유지;}if(údaje_pozícia>=30&&údaje_pozícia<=37)Terminál_položka->전경색=údaje_pozícia-30;if(údaje_pozícia>=90&&údaje_pozícia<=97)Terminál_položka->전경색=údaje_pozícia-90+8;if(údaje_pozícia>=40&&údaje_pozícia<=47)Terminál_položka->배경색=údaje_pozícia-40;if(údaje_pozícia>=100&&údaje_pozícia<=107)Terminál_položka->배경색=údaje_pozícia-100+8;if(údaje_pozícia==39)Terminál_položka->전경색=7;if(údaje_pozícia==49)Terminál_položka->배경색=0;}
    if(bod_kódu=='J'&&(Terminál_položka->parameter_VALUE[0]==2||Terminál_položka->parameter_VALUE[0]==3))vymazať_Obsah();
    if(bod_kódu=='K'){unsigned 출발위치=Terminál_položka->parameter_VALUE[0]==2?0:Terminál_položka->COLUMN_pozícia,도착위치=Terminál_položka->parameter_VALUE[0]==1?Terminál_položka->COLUMN_pozícia+1:Terminál_položka->COLUMNS;if(Terminál_položka->parameter_VALUE[0]==1)출발위치=0;for(unsigned 순번=출발위치;순번<도착위치&&순번<Terminál_položka->COLUMNS;순번++){
        unsigned ROW_VALUE=Terminál_položka->ROW_pozícia%História_linka_COUNT,znak_VALUE=Terminál_položka->글자칸들[ROW_VALUE][순번],tvar_VALUE=Terminál_položka->전경색|(Terminál_položka->배경색<<4);
        /* 넓은 vi 화면에서도 이미 빈 칸의 písmo_VALUE 화소를 되풀이해 칠하지 않는다. */
        int 바뀜=(znak_VALUE!=0&&znak_VALUE!=' ')||Terminál_položka->모양들[ROW_VALUE][순번]!=tvar_VALUE;
        Terminál_položka->글자칸들[ROW_VALUE][순번]=' ';Terminál_položka->모양들[ROW_VALUE][순번]=tvar_VALUE;
        if(바뀜)그리기(Terminál_položka->ROW_pozícia,순번);
    }}
    if(bod_kódu=='D')Terminál_položka->COLUMN_pozícia=položka_COUNT>Terminál_položka->COLUMN_pozícia?0:Terminál_položka->COLUMN_pozícia-položka_COUNT;if(bod_kódu=='C')Terminál_položka->COLUMN_pozícia=Terminál_položka->COLUMN_pozícia+položka_COUNT>=Terminál_položka->COLUMNS?Terminál_položka->COLUMNS-1:Terminál_položka->COLUMN_pozícia+položka_COUNT;
    if(bod_kódu=='G')Terminál_položka->COLUMN_pozícia=položka_COUNT>Terminál_položka->COLUMNS?Terminál_položka->COLUMNS-1:položka_COUNT-1;if(bod_kódu=='A')Terminál_položka->ROW_pozícia=položka_COUNT>Terminál_položka->ROW_pozícia-Terminál_položka->맨위?Terminál_položka->맨위:Terminál_položka->ROW_pozícia-položka_COUNT;
    if(bod_kódu=='B')Terminál_položka->ROW_pozícia=Terminál_položka->ROW_pozícia+položka_COUNT>=Terminál_položka->맨위+Terminál_položka->ROW_COUNT?Terminál_položka->맨위+Terminál_položka->ROW_COUNT-1:Terminál_položka->ROW_pozícia+položka_COUNT;
    if(bod_kódu=='H'||bod_kódu=='f'){Terminál_položka->ROW_pozícia=Terminál_položka->맨위+(položka_COUNT>Terminál_položka->ROW_COUNT?Terminál_položka->ROW_COUNT:položka_COUNT)-1;unsigned X_súradnica=Terminál_položka->parameter_VALUE[1]?Terminál_položka->parameter_VALUE[1]:1;Terminál_položka->COLUMN_pozícia=(X_súradnica>Terminál_položka->COLUMNS?Terminál_položka->COLUMNS:X_súradnica)-1;}
    if(bod_kódu=='s'){Terminál_položka->저장행=Terminál_položka->ROW_pozícia;Terminál_položka->저장열=Terminál_položka->COLUMN_pozícia;}if(bod_kódu=='u'){Terminál_položka->ROW_pozícia=Terminál_položka->저장행;Terminál_položka->COLUMN_pozícia=Terminál_položka->저장열<Terminál_položka->COLUMNS?Terminál_položka->저장열:Terminál_položka->COLUMNS-1;}
    if((bod_kódu=='h'||bod_kódu=='l')&&Terminál_položka->parameter_VALUE[0]==25)Terminál_položka->가리개보임=bod_kódu=='h';
}
void Terminál_Byte(unsigned SECOND_VALUE){
    Terminál_položka=&Windows_Zoznam[출력결과];if(!Terminál_položka->살아있음)return;znak_VALUE_be8150db(0);if(Terminál_položka->posúvať){Terminál_položka->posúvať=0;if(보이는지())obsah_VALUE();}
    if(Terminál_položka->탈출상태==1){Terminál_položka->탈출상태=SECOND_VALUE=='['?2:0;Terminál_položka->parameter_INDEX=0;for(unsigned 순번=0;순번<4;순번++)Terminál_položka->parameter_VALUE[순번]=0;}
    else if(Terminál_položka->탈출상태==2){if(SECOND_VALUE=='?'){}else if(SECOND_VALUE>='0'&&SECOND_VALUE<='9'){if(Terminál_položka->parameter_VALUE[Terminál_položka->parameter_INDEX]<10000)Terminál_položka->parameter_VALUE[Terminál_položka->parameter_INDEX]=Terminál_položka->parameter_VALUE[Terminál_položka->parameter_INDEX]*10+SECOND_VALUE-'0';}else if(SECOND_VALUE==';'&&Terminál_položka->parameter_INDEX<3)Terminál_položka->parameter_INDEX++;else{rukoväť_riadenie_SEQUENCE(SECOND_VALUE);Terminál_položka->탈출상태=0;}}
    else if(SECOND_VALUE==27){Terminál_položka->긴부호없는값=0;Terminál_položka->탈출상태=1;}else{
        if(Terminál_položka->긴부호없는값&&(SECOND_VALUE&0xc0)!=0x80){Terminál_položka->긴부호없는값=0;bod_kódu_451f2815(0xfffd);}
        if(Terminál_položka->긴부호없는값){Terminál_položka->부호없는결과=Terminál_položka->부호없는결과*64+(SECOND_VALUE&63);if(--Terminál_položka->긴부호없는값==0)bod_kódu_451f2815(Terminál_položka->부호없는결과<Terminál_položka->SMALL_VALUE||Terminál_položka->부호없는결과>0x10ffff||(Terminál_položka->부호없는결과>=0xd800&&Terminál_položka->부호없는결과<=0xdfff)?0xfffd:Terminál_položka->부호없는결과);}
        else if(SECOND_VALUE<128)bod_kódu_451f2815(SECOND_VALUE);else if(SECOND_VALUE>=0xc2&&SECOND_VALUE<=0xf4){Terminál_položka->긴부호없는값=SECOND_VALUE<0xe0?1:SECOND_VALUE<0xf0?2:3;Terminál_položka->부호없는결과=SECOND_VALUE&((1u<<(6-Terminál_položka->긴부호없는값))-1);Terminál_položka->SMALL_VALUE=Terminál_položka->긴부호없는값==1?128:Terminál_položka->긴부호없는값==2?2048:65536;}else bod_kódu_451f2815(0xfffd);
    }znak_VALUE_be8150db(1);
}
int Terminál_čakajúci(void){return Informačné_systémy_čakajúci!=0;}
/* 모서리 INDEX: 1 좌상, 2 우상, 3 좌하, 4 우하. */
static int zmeniť_veľkosť_presunúť=-1,잡은모서리,잡은가로,잡은세로,처음가로,처음세로,처음너비,처음높이;
static int 가리킨창(int 가로,int vertikála_pozícia) {
    for(int SEQUENCE_VALUE=položka_COUNT_8f7753a1-1;SEQUENCE_VALUE>=0;SEQUENCE_VALUE--){
        int identifikátor_VALUE=poradie_VALUE[SEQUENCE_VALUE];Terminál_d413d4bc *Okno=&Windows_Zoznam[identifikátor_VALUE];
        if(가로>=(int)Okno->X_súradnica&&vertikála_pozícia>=(int)Okno->Y_súradnica&&
           가로<(int)(Okno->X_súradnica+Okno->너비)&&vertikála_pozícia<(int)(Okno->Y_súradnica+Okno->výška_VALUE))return identifikátor_VALUE;
    }return -1;
}
static int 모서리찾기(int identifikátor_VALUE,int 가로,int vertikála_pozícia) {
    if(identifikátor_VALUE<0)return 0;Terminál_d413d4bc *Okno=&Windows_Zoznam[identifikátor_VALUE];
    int 왼쪽=가로<(int)Okno->X_súradnica+8,RIGHT=가로>=(int)(Okno->X_súradnica+Okno->너비)-8;
    int 위쪽=vertikála_pozícia<(int)Okno->Y_súradnica+8,아래쪽=vertikála_pozícia>=(int)(Okno->Y_súradnica+Okno->výška_VALUE)-8;
    return (왼쪽||RIGHT)&&(위쪽||아래쪽)?1+RIGHT+아래쪽*2:0;
}
static int oddeľovač_VALUE(int VALUE,int 최소,int 최대){return VALUE<최소?최소:VALUE>최대?최대:VALUE;}
static void premiestniť_zmeniť_veľkosť(int 가로,int vertikála_pozícia) {
    Terminál_d413d4bc *Okno=&Windows_Zoznam[zmeniť_veľkosť_presunúť];int 왼쪽=처음가로,위쪽=처음세로,RIGHT=처음가로+처음너비,아래쪽=처음세로+처음높이;
    if(잡은모서리==1||잡은모서리==3)왼쪽=oddeľovač_VALUE(처음가로+가로-잡은가로,0,RIGHT-360);
    else RIGHT=oddeľovač_VALUE(처음가로+처음너비+가로-잡은가로,왼쪽+360,보드화면너비());
    if(잡은모서리<=2)위쪽=oddeľovač_VALUE(처음세로+vertikála_pozícia-잡은세로,34,아래쪽-216);
    else 아래쪽=oddeľovač_VALUE(처음세로+처음높이+vertikála_pozícia-잡은세로,위쪽+216,보드화면높이());
    unsigned COLUMNS=(RIGHT-왼쪽-24)/8,ROW_COUNT=(아래쪽-위쪽-56)/16;
    if(Okno->COLUMNS!=COLUMNS||Okno->ROW_COUNT!=ROW_COUNT){
        Okno->크기바뀜=1;Okno->COLUMNS=COLUMNS;Okno->ROW_COUNT=ROW_COUNT;
        if(Okno->COLUMN_pozícia>=COLUMNS)Okno->COLUMN_pozícia=COLUMNS-1;
        if(Okno->ROW_pozícia>=Okno->맨위+ROW_COUNT)Okno->맨위=Okno->ROW_pozícia-ROW_COUNT+1;
        unsigned 한도=Okno->맨위;if(한도>História_linka_COUNT-ROW_COUNT)한도=História_linka_COUNT-ROW_COUNT;
        if(Okno->posúvať>한도)Okno->posúvať=한도;
    }
    int 옛가로=Okno->X_súradnica,옛세로=Okno->Y_súradnica,옛폭=Okno->너비,옛길이=Okno->výška_VALUE;
    if(옛가로==왼쪽&&옛세로==위쪽&&옛폭==RIGHT-왼쪽&&옛길이==아래쪽-위쪽)return;
    Okno->X_súradnica=왼쪽;Okno->Y_súradnica=위쪽;Okno->너비=RIGHT-왼쪽;Okno->výška_VALUE=아래쪽-위쪽;
    창자리그리기(옛가로,옛세로,옛폭,옛길이,Okno);
}
void Terminál_ukazovateľ(unsigned Ďalej_položka,int X_súradnica,int Y_súradnica){
    unsigned 눌림=Ďalej_položka&~단추들;단추들=Ďalej_položka;
    if(!počítač_zobraziť){presunúť_VALUE=-1;zmeniť_veľkosť_presunúť=-1;Panel_ukazovateľ(X_súradnica,Y_súradnica,1);return;}
    if(!(Ďalej_položka&1)){presunúť_VALUE=-1;zmeniť_veľkosť_presunúť=-1;}
    if(zmeniť_veľkosť_presunúť>=0&&!Windows_Zoznam[zmeniť_veľkosť_presunúť].살아있음)zmeniť_veľkosť_presunúť=-1;
    if(presunúť_VALUE>=0&&!Windows_Zoznam[presunúť_VALUE].살아있음)presunúť_VALUE=-1;
    if(zmeniť_veľkosť_presunúť>=0){
        premiestniť_zmeniť_veľkosť(X_súradnica,Y_súradnica);Panel_ukazovateľ(X_súradnica,Y_súradnica,잡은모서리==1||잡은모서리==4?2:3);return;
    }
    Panel_ukazovateľ(X_súradnica,Y_súradnica,1);
    if(presunúť_VALUE>=0){
        Terminál_d413d4bc *Okno=&Windows_Zoznam[presunúť_VALUE];
        int 옛가로=Okno->X_súradnica,옛세로=Okno->Y_súradnica;
        Okno->X_súradnica=oddeľovač_VALUE(X_súradnica-presunúť_X,0,보드화면너비()-Okno->너비);
        Okno->Y_súradnica=oddeľovač_VALUE(Y_súradnica-presunúť_Y,34,보드화면높이()-Okno->výška_VALUE);
        if(옛가로!=(int)Okno->X_súradnica||옛세로!=(int)Okno->Y_súradnica)창자리그리기(옛가로,옛세로,Okno->너비,Okno->výška_VALUE,Okno);
        return;
    }
    extern int 화면덮음(int,int,int);
    if(화면덮음(ohnisko,X_súradnica,Y_súradnica)){화면가리킴(ohnisko,눌림,X_súradnica,Y_súradnica);return;}
    int identifikátor_VALUE=가리킨창(X_súradnica,Y_súradnica),모서리=모서리찾기(identifikátor_VALUE,X_súradnica,Y_súradnica);
    if(모서리)Panel_ukazovateľ(X_súradnica,Y_súradnica,모서리==1||모서리==4?2:3);
    if(눌림&1){
        if(모서리){
            Terminál_d413d4bc *Okno=&Windows_Zoznam[identifikátor_VALUE];zmeniť_veľkosť_presunúť=identifikátor_VALUE;잡은모서리=모서리;잡은가로=X_súradnica;잡은세로=Y_súradnica;
            처음가로=Okno->X_súradnica;처음세로=Okno->Y_súradnica;처음너비=Okno->너비;처음높이=Okno->výška_VALUE;
            if(identifikátor_VALUE!=ohnisko)앞으로올리기(identifikátor_VALUE);return;
        }
        if(Y_súradnica<32&&X_súradnica>=6&&X_súradnica<142){Create_položka();return;}
        if(Y_súradnica<32&&X_súradnica>=154&&X_súradnica<602){앞으로올리기((X_súradnica-154)/112);return;}
        if(identifikátor_VALUE>=0){
            Terminál_d413d4bc *Okno=&Windows_Zoznam[identifikátor_VALUE];
            if(Y_súradnica<(int)Okno->Y_súradnica+30&&X_súradnica>=(int)(Okno->X_súradnica+Okno->너비)-32){Zavrieť_okno(identifikátor_VALUE);return;}
            if(identifikátor_VALUE!=ohnisko)앞으로올리기(identifikátor_VALUE);
            if(Y_súradnica<(int)Okno->Y_súradnica+30){presunúť_VALUE=identifikátor_VALUE;presunúť_X=X_súradnica-Okno->X_súradnica;presunúť_Y=Y_súradnica-Okno->Y_súradnica;}return;
        }
    }
    if(ohnisko>=0&&(눌림&(8|16))){Terminál_položka=&Windows_Zoznam[ohnisko];if(눌림&8){unsigned 한도=Terminál_položka->맨위;if(한도>História_linka_COUNT-Terminál_položka->ROW_COUNT)한도=História_linka_COUNT-Terminál_položka->ROW_COUNT;Terminál_položka->posúvať=Terminál_položka->posúvať+9>한도?한도:Terminál_položka->posúvať+9;}else Terminál_položka->posúvať=Terminál_položka->posúvať<9?0:Terminál_položka->posúvať-9;다시그리기();}
}
void 터미널바로가기키(unsigned 누름값){if(누름값==1)Create_položka();if(누름값==2&&položka_COUNT_8f7753a1)앞으로올리기(poradie_VALUE[0]);if(누름값==3)Zavrieť_okno(ohnisko);}
počítač_Word Panel_Terminál(počítač_Word Akcia){
    if(Akcia==300){if(!Windows_Zoznam[출력결과].살아있음)return Create_položka();počítač_zobraziť=1;다시그리기();return 0;}
    if(Akcia==0){Zavrieť_okno(ohnisko);return 0;}if(Akcia==1)return (uint32_t)Create_položka();if(Akcia==2)return ohnisko>=0;
    if(Akcia==9){počítač_zobraziť=0;return 0;}if(Akcia==7)return položka_COUNT_8f7753a1;if(Akcia==10)return ohnisko+1;if(Akcia==11)return 출력결과;
    if(Akcia==13){Terminál_d413d4bc *Okno=&Windows_Zoznam[출력결과];return Okno->살아있음?(Okno->ROW_COUNT<<16)|Okno->COLUMNS:(19<<16)|68;}
    if(Akcia==14){unsigned VALUE=Windows_Zoznam[출력결과].크기바뀜;Windows_Zoznam[출력결과].크기바뀜=0;return VALUE;}
    if(Akcia==12){unsigned VALUE=Informačné_systémy_čakajúci;Informačné_systémy_čakajúci=0;return VALUE;}
    if(Akcia>=20&&Akcia<24)return Windows_Zoznam[Akcia-20].살아있음;
    if(Akcia>=100&&Akcia<104){출력결과=Akcia-100;Terminál_položka=&Windows_Zoznam[출력결과];return 0;}
    if(Akcia>=200&&Akcia<204){앞으로올리기(Akcia-200);return 0;}
    if(Akcia==3){다시그리기();return 0;}Terminál_položka=&Windows_Zoznam[출력결과];if(!Terminál_položka->살아있음)return 0;
    if(Akcia==4)vymazať_Obsah();if(Akcia==5||Akcia==6){unsigned 이전=단추들;Terminál_ukazovateľ(Akcia==5?8:16,0,0);단추들=이전;}return 1;
}
