#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* 자체 네 Leihoa 합성과 UTF-8 Terminala. 바뀐 영역의 Osatutakoak_balio 그림만 표시한다. */
#include <stdint.h>
#include <stddef.h>
typedef uintptr_t gailu_Word;
extern gailu_Word arbel_pixel(gailu_Word,gailu_Word,gailu_Word),보드화면기억공간(void);
extern void *memset(void *,int,size_t);
extern const unsigned char Terminal_letra_tipo[];
#define 최대열수 237
#define Historia_lerro_ZENBATU 160
typedef struct {
    uint32_t 글자칸들[Historia_lerro_ZENBATU][최대열수]; uint8_t 모양들[Historia_lerro_ZENBATU][최대열수];
    unsigned 너비,높이,ZUTABEAK,ERRENKADA_ZENBATU,크기바뀜;
    unsigned 살아있음,X_koordenatu,Y_koordenatu,ERRENKADA_kargu,zutabe_kargu,맨위,korritu,전경색,배경색,탈출상태,parametro_balio[4],parametro_INDIZE,저장행,저장열;
    unsigned 부호없는결과,긴부호없는값,K_TXIKIENA_balio,대체화면,가리개보임;
} Terminal;
static Terminal Windows_Zerrenda[4];
static int Fokuratua=-1,출력결과,ordena_balio[4],sarrera_ZENBATU,arrastatu_balio=-1,arrastatu_X,arrastatu_Y;
static unsigned informatika_zain,단추들,mahaigain_ikusi,한글입력;
static const uint32_t 색상들[16]={0x201a15,0x6060df,0x9dcc86,0x80cfea,0xefaf72,0xca96c9,0xceda76,0xede9df,0x858078,0x8888ff,0xb9eba7,0xa5eaff,0xffcc99,0xf0bef1,0xf0f0a0,0xffffff};
extern int 화면보임(int),화면가리킴(int,unsigned,int,int);
extern void 화면다시그림(int);
static Terminal *Terminal_sarrera;
static unsigned 넓은글자(unsigned karaktere_kode){return karaktere_kode>=256?2:1;}
static void 사각영역(unsigned X_koordenatu,unsigned Y_koordenatu,unsigned 너비값,unsigned 높이값,unsigned 색상){
    보드사각그림(X_koordenatu,Y_koordenatu,너비값,높이값,색상);
}
void Terminal_glifo(unsigned X_koordenatu,unsigned Y_koordenatu,unsigned karaktere_kode,unsigned 전경색,unsigned 배경색){
    unsigned 너비=넓은글자(karaktere_kode)*8;if(karaktere_kode==0xffffffffu)return;
    int 왼쪽=X_koordenatu,위쪽=Y_koordenatu,폭=너비,luzera_balio=16;
    if(!보드그림범위(&왼쪽,&위쪽,&폭,&luzera_balio))return;
    if(karaktere_kode==' '){보드사각그림(왼쪽,위쪽,폭,luzera_balio,배경색);return;}
    unsigned BEGIRATU_INDIZE=karaktere_kode<65536?karaktere_kode:karaktere_kode>=0x1f600&&karaktere_kode<0x1f650?65536+karaktere_kode-0x1f600:0xfffd;
    const unsigned char *letra_tipo_balio=Terminal_letra_tipo+BEGIRATU_INDIZE*32;
    for(int Marra=위쪽;Marra<위쪽+luzera_balio;Marra++){unsigned Atzeko_planoko_transferentzia_zerbitzu_adimenduna_Zerrenda=letra_tipo_balio[(Marra-Y_koordenatu)*2]*256+letra_tipo_balio[(Marra-Y_koordenatu)*2+1];for(int 칸=왼쪽;칸<왼쪽+폭;칸++)arbel_pixel(칸,Marra,(Atzeko_planoko_transferentzia_zerbitzu_adimenduna_Zerrenda&(0x8000>>(칸-X_koordenatu)))?전경색:배경색);}
}
static void izen_taula(unsigned X_koordenatu,unsigned Y_koordenatu,const char *kate_datuak,unsigned 전경색,unsigned 배경색){while(*kate_datuak){unsigned karaktere_kode=(unsigned char)*kate_datuak++, 남은수=0;if(karaktere_kode>=0xc0){남은수=karaktere_kode<0xe0?1:karaktere_kode<0xf0?2:3;karaktere_kode&=(1u<<(6-남은수))-1;while(남은수--&&*kate_datuak)karaktere_kode=(karaktere_kode<<6)|((unsigned char)*kate_datuak++&63);}Terminal_glifo(X_koordenatu,Y_koordenatu,karaktere_kode,전경색,배경색);X_koordenatu+=넓은글자(karaktere_kode)*8;}}
static unsigned 첫항목(void){return Terminal_sarrera->맨위;}
static int 보이는지(void){return Terminal_sarrera->살아있음&&Fokuratua>=0&&Terminal_sarrera==&Windows_Zerrenda[Fokuratua]&&!화면보임(Fokuratua);}
static void 그리기(unsigned ERRENKADA_kargu,unsigned zutabe_kargu){
    if(!보이는지()||ERRENKADA_kargu<첫항목()-Terminal_sarrera->korritu||ERRENKADA_kargu>=첫항목()-Terminal_sarrera->korritu+Terminal_sarrera->ERRENKADA_ZENBATU||zutabe_kargu>=Terminal_sarrera->ZUTABEAK)return;
    unsigned karaktere_kode=Terminal_sarrera->글자칸들[ERRENKADA_kargu%Historia_lerro_ZENBATU][zutabe_kargu],kate_datuak=Terminal_sarrera->모양들[ERRENKADA_kargu%Historia_lerro_ZENBATU][zutabe_kargu];
    if(넓은글자(karaktere_kode)==2&&zutabe_kargu+1>=Terminal_sarrera->ZUTABEAK)karaktere_kode=' ';
    Terminal_glifo(Terminal_sarrera->X_koordenatu+12+zutabe_kargu*8,Terminal_sarrera->Y_koordenatu+36+(ERRENKADA_kargu-첫항목()+Terminal_sarrera->korritu)*16,karaktere_kode?karaktere_kode:' ',색상들[kate_datuak&15],색상들[kate_datuak>>4]);
}
static void berreketa_ikur_balio(int erakutsi_leiho){if(!보이는지()||Terminal_sarrera->korritu||Terminal_sarrera->zutabe_kargu>=Terminal_sarrera->ZUTABEAK||Terminal_sarrera->ERRENKADA_kargu<Terminal_sarrera->맨위||Terminal_sarrera->ERRENKADA_kargu>=Terminal_sarrera->맨위+Terminal_sarrera->ERRENKADA_ZENBATU)return;
    if(!erakutsi_leiho||!Terminal_sarrera->가리개보임)그리기(Terminal_sarrera->ERRENKADA_kargu,Terminal_sarrera->zutabe_kargu);else 사각영역(Terminal_sarrera->X_koordenatu+12+Terminal_sarrera->zutabe_kargu*8,Terminal_sarrera->Y_koordenatu+36+(Terminal_sarrera->ERRENKADA_kargu-Terminal_sarrera->맨위)*16+14,8,2,색상들[Terminal_sarrera->전경색]);}
static void eduki_balio(void){
    사각영역(Terminal_sarrera->X_koordenatu+12,Terminal_sarrera->Y_koordenatu+36,Terminal_sarrera->ZUTABEAK*8,Terminal_sarrera->ERRENKADA_ZENBATU*16,색상들[0]);
    int 가로=Terminal_sarrera->X_koordenatu+12,Bertikala_kargu=Terminal_sarrera->Y_koordenatu+36,폭=Terminal_sarrera->ZUTABEAK*8,luzera_balio=Terminal_sarrera->ERRENKADA_ZENBATU*16;
    if(보드그림범위(&가로,&Bertikala_kargu,&폭,&luzera_balio)){
    unsigned 첫줄=(Bertikala_kargu-Terminal_sarrera->Y_koordenatu-36)/16,끝줄=(Bertikala_kargu+luzera_balio-Terminal_sarrera->Y_koordenatu-36+15)/16;
    unsigned 첫칸=(가로-Terminal_sarrera->X_koordenatu-12)/8,끝칸=(가로+폭-Terminal_sarrera->X_koordenatu-12+7)/8;
    if(첫칸)첫칸--; /* 잘림 경계 왼쪽에서 시작한 두 칸 글자도 그린다. */
    for(unsigned 반환값=첫줄;반환값<끝줄;반환값++)for(unsigned karaktere_kode=첫칸;karaktere_kode<끝칸;karaktere_kode++){
        unsigned ERRENKADA_kargu=첫항목()-Terminal_sarrera->korritu+반환값,karaktere_balio=Terminal_sarrera->글자칸들[ERRENKADA_kargu%Historia_lerro_ZENBATU][karaktere_kode],kate_datuak=Terminal_sarrera->모양들[ERRENKADA_kargu%Historia_lerro_ZENBATU][karaktere_kode];
        if(넓은글자(karaktere_balio)==2&&karaktere_kode+1>=Terminal_sarrera->ZUTABEAK)karaktere_balio=' ';
        if((karaktere_balio==0||karaktere_balio==' ')&&(kate_datuak>>4)==0)continue;
        Terminal_glifo(Terminal_sarrera->X_koordenatu+12+karaktere_kode*8,Terminal_sarrera->Y_koordenatu+36+반환값*16,karaktere_balio?karaktere_balio:' ',색상들[kate_datuak&15],색상들[kate_datuak>>4]);
    }}
    izen_taula(Terminal_sarrera->X_koordenatu+12,Terminal_sarrera->Y_koordenatu+Terminal_sarrera->높이-18,Terminal_sarrera->korritu?"PgDn: recent output":Terminal_sarrera->너비>=500?"F6: next | Corner + left drag: resize":"Corner + left drag: resize",0xece8e2,0x403127);berreketa_ikur_balio(1);
}
static void 실행틀(int identifikatzaile_balio){
    Terminal_sarrera=&Windows_Zerrenda[identifikatzaile_balio];
    int 가로=Terminal_sarrera->X_koordenatu,Bertikala_kargu=Terminal_sarrera->Y_koordenatu,폭=Terminal_sarrera->너비,luzera_balio=Terminal_sarrera->높이;
    if(!보드그림범위(&가로,&Bertikala_kargu,&폭,&luzera_balio))return;
    사각영역(Terminal_sarrera->X_koordenatu,Terminal_sarrera->Y_koordenatu,Terminal_sarrera->너비,Terminal_sarrera->높이,0x403127);
    unsigned 색상=identifikatzaile_balio==Fokuratua?0x905020:0x604438;사각영역(Terminal_sarrera->X_koordenatu,Terminal_sarrera->Y_koordenatu,Terminal_sarrera->너비,30,색상);
    izen_taula(Terminal_sarrera->X_koordenatu+12,Terminal_sarrera->Y_koordenatu+7,"JKOROS Terminal",0xffffff,색상);
    char 수치[2]={(char)('1'+identifikatzaile_balio),0};izen_taula(Terminal_sarrera->X_koordenatu+148,Terminal_sarrera->Y_koordenatu+7,수치,0xffffff,색상);
    izen_taula(Terminal_sarrera->X_koordenatu+240,Terminal_sarrera->Y_koordenatu+7,Terminal_sarrera->너비>=500?(한글입력?"[EU] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[EU]":"[EN]"),0xffffff,색상);
    사각영역(Terminal_sarrera->X_koordenatu+Terminal_sarrera->너비-32,Terminal_sarrera->Y_koordenatu+4,26,22,0x5555b8);izen_taula(Terminal_sarrera->X_koordenatu+Terminal_sarrera->너비-24,Terminal_sarrera->Y_koordenatu+7,"X",0xffffff,0x5555b8);
    eduki_balio();
}
static void Trazua_eszena(void){
    if(!mahaigain_ikusi)return;사각영역(0,0,보드화면너비(),보드화면높이(),0x302018);사각영역(0,0,보드화면너비(),32,0x403127);
    사각영역(6,4,136,24,0x905020);izen_taula(14,8,"+ New terminal",0xffffff,0x905020);
    for(int 순번=0;순번<4;순번++)if(Windows_Zerrenda[순번].살아있음){unsigned karaktere_kode=Fokuratua==순번?0x905020:0x604438;사각영역(154+순번*112,4,106,24,karaktere_kode);izen_taula(160+순번*112,8,"Terminal",0xffffff,karaktere_kode);char kate_datuak[2]={(char)('1'+순번),0};izen_taula(232+순번*112,8,kate_datuak,0xffffff,karaktere_kode);}
    if(!sarrera_ZENBATU)izen_taula(140,210,"Click + New terminal to start",0xede9df,0x302018);
    for(int 순번=0;순번<sarrera_ZENBATU;순번++)실행틀(ordena_balio[순번]);화면다시그림(Fokuratua);Terminal_sarrera=&Windows_Zerrenda[출력결과];
}
static void 영역그리기(int 가로,int Bertikala_kargu,int 폭,int luzera_balio){
    if(!mahaigain_ikusi||!보드그림범위(&가로,&Bertikala_kargu,&폭,&luzera_balio))return;
    for(int Marra=Bertikala_kargu;Marra<Bertikala_kargu+luzera_balio;Marra+=32){
        int 띠높이=Bertikala_kargu+luzera_balio-Marra;if(띠높이>32)띠높이=32;
        if(보드그림시작(가로,Marra,폭,띠높이)){Trazua_eszena();보드그림마침();}
    }
}
static void 다시그리기(void){영역그리기(0,0,보드화면너비(),보드화면높이());}
/* 서로 겹치지 않는 새 Leihoa 영역과 이전 자리의 네 띠를 복구한다. */
static void 창자리그리기(int 가로,int Bertikala_kargu,int 폭,int luzera_balio,Terminal *Leihoa){
    int 왼쪽=가로>(int)Leihoa->X_koordenatu?가로:(int)Leihoa->X_koordenatu;
    int 위쪽=Bertikala_kargu>(int)Leihoa->Y_koordenatu?Bertikala_kargu:(int)Leihoa->Y_koordenatu;
    int ESKUIN=가로+폭<(int)(Leihoa->X_koordenatu+Leihoa->너비)?가로+폭:(int)(Leihoa->X_koordenatu+Leihoa->너비);
    int 아래쪽=Bertikala_kargu+luzera_balio<(int)(Leihoa->Y_koordenatu+Leihoa->높이)?Bertikala_kargu+luzera_balio:(int)(Leihoa->Y_koordenatu+Leihoa->높이);
    영역그리기(Leihoa->X_koordenatu,Leihoa->Y_koordenatu,Leihoa->너비,Leihoa->높이);
    if(왼쪽>=ESKUIN||위쪽>=아래쪽){영역그리기(가로,Bertikala_kargu,폭,luzera_balio);return;}
    영역그리기(가로,Bertikala_kargu,폭,위쪽-Bertikala_kargu);
    영역그리기(가로,아래쪽,폭,Bertikala_kargu+luzera_balio-아래쪽);
    영역그리기(가로,위쪽,왼쪽-가로,아래쪽-위쪽);
    영역그리기(ESKUIN,위쪽,가로+폭-ESKUIN,아래쪽-위쪽);
}
static void seinale_Fokuratua(void){informatika_zain=(informatika_zain&~15u)|(unsigned)(Fokuratua+1)|0x10000;}
void 터미널입력방식(unsigned 한글여부){
    한글입력=한글여부!=0;
    /* Update title bars only: a mode switch must not erase an EL0 drawing. */
    if(Fokuratua>=0){
        Terminal *leiho_sarrera=&Windows_Zerrenda[Fokuratua];
        izen_taula(leiho_sarrera->X_koordenatu+240,leiho_sarrera->Y_koordenatu+7,leiho_sarrera->너비>=500?(한글입력?"[EU] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[EU]":"[EN]"),0xffffff,0x905020);
    }
}
static void 앞으로올리기(int identifikatzaile_balio){if(identifikatzaile_balio<0||identifikatzaile_balio>=4||!Windows_Zerrenda[identifikatzaile_balio].살아있음)return;int 현재위치=0;while(현재위치<sarrera_ZENBATU&&ordena_balio[현재위치]!=identifikatzaile_balio)현재위치++;for(;현재위치+1<sarrera_ZENBATU;현재위치++)ordena_balio[현재위치]=ordena_balio[현재위치+1];ordena_balio[sarrera_ZENBATU-1]=identifikatzaile_balio;Fokuratua=identifikatzaile_balio;seinale_Fokuratua();다시그리기();}
static void 빈칸채우기(unsigned ERRENKADA_kargu){for(unsigned karaktere_kode=0;karaktere_kode<최대열수;karaktere_kode++){Terminal_sarrera->글자칸들[ERRENKADA_kargu%Historia_lerro_ZENBATU][karaktere_kode]=0;Terminal_sarrera->모양들[ERRENKADA_kargu%Historia_lerro_ZENBATU][karaktere_kode]=Terminal_sarrera->전경색|(Terminal_sarrera->배경색<<4);}}
static void garbitu_Edukia(void){Terminal_sarrera->ERRENKADA_kargu=Terminal_sarrera->zutabe_kargu=Terminal_sarrera->맨위=Terminal_sarrera->korritu=0;for(unsigned 반환값=0;반환값<Historia_lerro_ZENBATU;반환값++)빈칸채우기(반환값);if(보이는지())eduki_balio();}
static int sortu_sarrera(void){
    if(!보드화면기억공간())return -19;int identifikatzaile_balio=0;while(identifikatzaile_balio<4&&Windows_Zerrenda[identifikatzaile_balio].살아있음)identifikatzaile_balio++;if(identifikatzaile_balio==4)return -28;
    mahaigain_ikusi=1;Terminal_sarrera=&Windows_Zerrenda[identifikatzaile_balio];memset(Terminal_sarrera,0,sizeof(*Terminal_sarrera));Terminal_sarrera->살아있음=1;Terminal_sarrera->너비=568;Terminal_sarrera->높이=360;Terminal_sarrera->ZUTABEAK=68;Terminal_sarrera->ERRENKADA_ZENBATU=19;Terminal_sarrera->X_koordenatu=12+identifikatzaile_balio*16;Terminal_sarrera->Y_koordenatu=48+identifikatzaile_balio*18;Terminal_sarrera->전경색=7;Terminal_sarrera->가리개보임=1;
    for(unsigned 반환값=0;반환값<Historia_lerro_ZENBATU;반환값++)빈칸채우기(반환값);ordena_balio[sarrera_ZENBATU++]=identifikatzaile_balio;Fokuratua=identifikatzaile_balio;informatika_zain|=1u<<(4+identifikatzaile_balio);seinale_Fokuratua();다시그리기();return identifikatzaile_balio+1;
}
static void itxi_leiho(int identifikatzaile_balio){
    if(identifikatzaile_balio<0||identifikatzaile_balio>=4||!Windows_Zerrenda[identifikatzaile_balio].살아있음)return;Windows_Zerrenda[identifikatzaile_balio].살아있음=0;informatika_zain|=1u<<(8+identifikatzaile_balio);
    int 현재위치=0;while(현재위치<sarrera_ZENBATU&&ordena_balio[현재위치]!=identifikatzaile_balio)현재위치++;for(;현재위치+1<sarrera_ZENBATU;현재위치++)ordena_balio[현재위치]=ordena_balio[현재위치+1];sarrera_ZENBATU--;
    if(Fokuratua==identifikatzaile_balio)Fokuratua=sarrera_ZENBATU?ordena_balio[sarrera_ZENBATU-1]:-1;seinale_Fokuratua();다시그리기();
}
static void 줄바꿈(void){Terminal_sarrera->zutabe_kargu=0;Terminal_sarrera->ERRENKADA_kargu++;if(Terminal_sarrera->ERRENKADA_kargu>=Terminal_sarrera->맨위+Terminal_sarrera->ERRENKADA_ZENBATU){Terminal_sarrera->맨위++;빈칸채우기(Terminal_sarrera->ERRENKADA_kargu);if(보이는지())eduki_balio();}}
static void karaktere_kode_451f2815(unsigned karaktere_kode){
    if(karaktere_kode==13){Terminal_sarrera->zutabe_kargu=0;return;}if(karaktere_kode==10){줄바꿈();return;}if(karaktere_kode==8){if(Terminal_sarrera->zutabe_kargu)Terminal_sarrera->zutabe_kargu--;return;}
    if(karaktere_kode==9){unsigned elementu_ZENBATU=8-Terminal_sarrera->zutabe_kargu%8;while(elementu_ZENBATU--)karaktere_kode_451f2815(' ');return;}if(karaktere_kode<32||karaktere_kode==127)return;
    unsigned 너비값=넓은글자(karaktere_kode);if(Terminal_sarrera->zutabe_kargu+너비값>Terminal_sarrera->ZUTABEAK)줄바꿈();
    if(Terminal_sarrera->글자칸들[Terminal_sarrera->ERRENKADA_kargu%Historia_lerro_ZENBATU][Terminal_sarrera->zutabe_kargu]==0xffffffffu&&Terminal_sarrera->zutabe_kargu){Terminal_sarrera->글자칸들[Terminal_sarrera->ERRENKADA_kargu%Historia_lerro_ZENBATU][Terminal_sarrera->zutabe_kargu-1]=' ';그리기(Terminal_sarrera->ERRENKADA_kargu,Terminal_sarrera->zutabe_kargu-1);}
    if(넓은글자(Terminal_sarrera->글자칸들[Terminal_sarrera->ERRENKADA_kargu%Historia_lerro_ZENBATU][Terminal_sarrera->zutabe_kargu])==2&&Terminal_sarrera->zutabe_kargu+1<Terminal_sarrera->ZUTABEAK){Terminal_sarrera->글자칸들[Terminal_sarrera->ERRENKADA_kargu%Historia_lerro_ZENBATU][Terminal_sarrera->zutabe_kargu+1]=' ';그리기(Terminal_sarrera->ERRENKADA_kargu,Terminal_sarrera->zutabe_kargu+1);}
    Terminal_sarrera->글자칸들[Terminal_sarrera->ERRENKADA_kargu%Historia_lerro_ZENBATU][Terminal_sarrera->zutabe_kargu]=karaktere_kode;Terminal_sarrera->모양들[Terminal_sarrera->ERRENKADA_kargu%Historia_lerro_ZENBATU][Terminal_sarrera->zutabe_kargu]=Terminal_sarrera->전경색|(Terminal_sarrera->배경색<<4);
    if(너비값==2)Terminal_sarrera->글자칸들[Terminal_sarrera->ERRENKADA_kargu%Historia_lerro_ZENBATU][Terminal_sarrera->zutabe_kargu+1]=0xffffffffu;
    그리기(Terminal_sarrera->ERRENKADA_kargu,Terminal_sarrera->zutabe_kargu);Terminal_sarrera->zutabe_kargu+=너비값;
}
static void helduleku_kontrol_SEKUENTZIA(unsigned karaktere_kode){
    unsigned elementu_ZENBATU=Terminal_sarrera->parametro_balio[0]?Terminal_sarrera->parametro_balio[0]:1;
    if(karaktere_kode=='m')for(unsigned 순번=0;순번<=Terminal_sarrera->parametro_INDIZE;순번++){unsigned datuak_kargu=Terminal_sarrera->parametro_balio[순번];if(!datuak_kargu){Terminal_sarrera->전경색=7;Terminal_sarrera->배경색=0;}if(datuak_kargu==1&&Terminal_sarrera->전경색<8)Terminal_sarrera->전경색+=8;if(datuak_kargu==7){unsigned 유지=Terminal_sarrera->전경색;Terminal_sarrera->전경색=Terminal_sarrera->배경색;Terminal_sarrera->배경색=유지;}if(datuak_kargu>=30&&datuak_kargu<=37)Terminal_sarrera->전경색=datuak_kargu-30;if(datuak_kargu>=90&&datuak_kargu<=97)Terminal_sarrera->전경색=datuak_kargu-90+8;if(datuak_kargu>=40&&datuak_kargu<=47)Terminal_sarrera->배경색=datuak_kargu-40;if(datuak_kargu>=100&&datuak_kargu<=107)Terminal_sarrera->배경색=datuak_kargu-100+8;if(datuak_kargu==39)Terminal_sarrera->전경색=7;if(datuak_kargu==49)Terminal_sarrera->배경색=0;}
    if(karaktere_kode=='J'&&(Terminal_sarrera->parametro_balio[0]==2||Terminal_sarrera->parametro_balio[0]==3))garbitu_Edukia();
    if(karaktere_kode=='K'){unsigned 출발위치=Terminal_sarrera->parametro_balio[0]==2?0:Terminal_sarrera->zutabe_kargu,도착위치=Terminal_sarrera->parametro_balio[0]==1?Terminal_sarrera->zutabe_kargu+1:Terminal_sarrera->ZUTABEAK;if(Terminal_sarrera->parametro_balio[0]==1)출발위치=0;for(unsigned 순번=출발위치;순번<도착위치&&순번<Terminal_sarrera->ZUTABEAK;순번++){
        unsigned ERRENKADA_balio=Terminal_sarrera->ERRENKADA_kargu%Historia_lerro_ZENBATU,karaktere_balio=Terminal_sarrera->글자칸들[ERRENKADA_balio][순번],forma_balio=Terminal_sarrera->전경색|(Terminal_sarrera->배경색<<4);
        /* 넓은 vi 화면에서도 이미 빈 칸의 letra_tipo_balio 화소를 되풀이해 칠하지 않는다. */
        int 바뀜=(karaktere_balio!=0&&karaktere_balio!=' ')||Terminal_sarrera->모양들[ERRENKADA_balio][순번]!=forma_balio;
        Terminal_sarrera->글자칸들[ERRENKADA_balio][순번]=' ';Terminal_sarrera->모양들[ERRENKADA_balio][순번]=forma_balio;
        if(바뀜)그리기(Terminal_sarrera->ERRENKADA_kargu,순번);
    }}
    if(karaktere_kode=='D')Terminal_sarrera->zutabe_kargu=elementu_ZENBATU>Terminal_sarrera->zutabe_kargu?0:Terminal_sarrera->zutabe_kargu-elementu_ZENBATU;if(karaktere_kode=='C')Terminal_sarrera->zutabe_kargu=Terminal_sarrera->zutabe_kargu+elementu_ZENBATU>=Terminal_sarrera->ZUTABEAK?Terminal_sarrera->ZUTABEAK-1:Terminal_sarrera->zutabe_kargu+elementu_ZENBATU;
    if(karaktere_kode=='G')Terminal_sarrera->zutabe_kargu=elementu_ZENBATU>Terminal_sarrera->ZUTABEAK?Terminal_sarrera->ZUTABEAK-1:elementu_ZENBATU-1;if(karaktere_kode=='A')Terminal_sarrera->ERRENKADA_kargu=elementu_ZENBATU>Terminal_sarrera->ERRENKADA_kargu-Terminal_sarrera->맨위?Terminal_sarrera->맨위:Terminal_sarrera->ERRENKADA_kargu-elementu_ZENBATU;
    if(karaktere_kode=='B')Terminal_sarrera->ERRENKADA_kargu=Terminal_sarrera->ERRENKADA_kargu+elementu_ZENBATU>=Terminal_sarrera->맨위+Terminal_sarrera->ERRENKADA_ZENBATU?Terminal_sarrera->맨위+Terminal_sarrera->ERRENKADA_ZENBATU-1:Terminal_sarrera->ERRENKADA_kargu+elementu_ZENBATU;
    if(karaktere_kode=='H'||karaktere_kode=='f'){Terminal_sarrera->ERRENKADA_kargu=Terminal_sarrera->맨위+(elementu_ZENBATU>Terminal_sarrera->ERRENKADA_ZENBATU?Terminal_sarrera->ERRENKADA_ZENBATU:elementu_ZENBATU)-1;unsigned X_koordenatu=Terminal_sarrera->parametro_balio[1]?Terminal_sarrera->parametro_balio[1]:1;Terminal_sarrera->zutabe_kargu=(X_koordenatu>Terminal_sarrera->ZUTABEAK?Terminal_sarrera->ZUTABEAK:X_koordenatu)-1;}
    if(karaktere_kode=='s'){Terminal_sarrera->저장행=Terminal_sarrera->ERRENKADA_kargu;Terminal_sarrera->저장열=Terminal_sarrera->zutabe_kargu;}if(karaktere_kode=='u'){Terminal_sarrera->ERRENKADA_kargu=Terminal_sarrera->저장행;Terminal_sarrera->zutabe_kargu=Terminal_sarrera->저장열<Terminal_sarrera->ZUTABEAK?Terminal_sarrera->저장열:Terminal_sarrera->ZUTABEAK-1;}
    if((karaktere_kode=='h'||karaktere_kode=='l')&&Terminal_sarrera->parametro_balio[0]==25)Terminal_sarrera->가리개보임=karaktere_kode=='h';
}
void Terminal_byte(unsigned SEGUNDOA_balio){
    Terminal_sarrera=&Windows_Zerrenda[출력결과];if(!Terminal_sarrera->살아있음)return;berreketa_ikur_balio(0);if(Terminal_sarrera->korritu){Terminal_sarrera->korritu=0;if(보이는지())eduki_balio();}
    if(Terminal_sarrera->탈출상태==1){Terminal_sarrera->탈출상태=SEGUNDOA_balio=='['?2:0;Terminal_sarrera->parametro_INDIZE=0;for(unsigned 순번=0;순번<4;순번++)Terminal_sarrera->parametro_balio[순번]=0;}
    else if(Terminal_sarrera->탈출상태==2){if(SEGUNDOA_balio=='?'){}else if(SEGUNDOA_balio>='0'&&SEGUNDOA_balio<='9'){if(Terminal_sarrera->parametro_balio[Terminal_sarrera->parametro_INDIZE]<10000)Terminal_sarrera->parametro_balio[Terminal_sarrera->parametro_INDIZE]=Terminal_sarrera->parametro_balio[Terminal_sarrera->parametro_INDIZE]*10+SEGUNDOA_balio-'0';}else if(SEGUNDOA_balio==';'&&Terminal_sarrera->parametro_INDIZE<3)Terminal_sarrera->parametro_INDIZE++;else{helduleku_kontrol_SEKUENTZIA(SEGUNDOA_balio);Terminal_sarrera->탈출상태=0;}}
    else if(SEGUNDOA_balio==27){Terminal_sarrera->긴부호없는값=0;Terminal_sarrera->탈출상태=1;}else{
        if(Terminal_sarrera->긴부호없는값&&(SEGUNDOA_balio&0xc0)!=0x80){Terminal_sarrera->긴부호없는값=0;karaktere_kode_451f2815(0xfffd);}
        if(Terminal_sarrera->긴부호없는값){Terminal_sarrera->부호없는결과=Terminal_sarrera->부호없는결과*64+(SEGUNDOA_balio&63);if(--Terminal_sarrera->긴부호없는값==0)karaktere_kode_451f2815(Terminal_sarrera->부호없는결과<Terminal_sarrera->K_TXIKIENA_balio||Terminal_sarrera->부호없는결과>0x10ffff||(Terminal_sarrera->부호없는결과>=0xd800&&Terminal_sarrera->부호없는결과<=0xdfff)?0xfffd:Terminal_sarrera->부호없는결과);}
        else if(SEGUNDOA_balio<128)karaktere_kode_451f2815(SEGUNDOA_balio);else if(SEGUNDOA_balio>=0xc2&&SEGUNDOA_balio<=0xf4){Terminal_sarrera->긴부호없는값=SEGUNDOA_balio<0xe0?1:SEGUNDOA_balio<0xf0?2:3;Terminal_sarrera->부호없는결과=SEGUNDOA_balio&((1u<<(6-Terminal_sarrera->긴부호없는값))-1);Terminal_sarrera->K_TXIKIENA_balio=Terminal_sarrera->긴부호없는값==1?128:Terminal_sarrera->긴부호없는값==2?2048:65536;}else karaktere_kode_451f2815(0xfffd);
    }berreketa_ikur_balio(1);
}
int Terminal_zain(void){return informatika_zain!=0;}
/* 모서리 INDIZE: 1 좌상, 2 우상, 3 좌하, 4 우하. */
static int aldatu_tamaina_arrastatu=-1,잡은모서리,잡은가로,잡은세로,처음가로,처음세로,처음너비,처음높이;
static int 가리킨창(int 가로,int Bertikala_kargu) {
    for(int SEKUENTZIA_balio=sarrera_ZENBATU-1;SEKUENTZIA_balio>=0;SEKUENTZIA_balio--){
        int identifikatzaile_balio=ordena_balio[SEKUENTZIA_balio];Terminal *Leihoa=&Windows_Zerrenda[identifikatzaile_balio];
        if(가로>=(int)Leihoa->X_koordenatu&&Bertikala_kargu>=(int)Leihoa->Y_koordenatu&&
           가로<(int)(Leihoa->X_koordenatu+Leihoa->너비)&&Bertikala_kargu<(int)(Leihoa->Y_koordenatu+Leihoa->높이))return identifikatzaile_balio;
    }return -1;
}
static int 모서리찾기(int identifikatzaile_balio,int 가로,int Bertikala_kargu) {
    if(identifikatzaile_balio<0)return 0;Terminal *Leihoa=&Windows_Zerrenda[identifikatzaile_balio];
    int 왼쪽=가로<(int)Leihoa->X_koordenatu+8,ESKUIN=가로>=(int)(Leihoa->X_koordenatu+Leihoa->너비)-8;
    int 위쪽=Bertikala_kargu<(int)Leihoa->Y_koordenatu+8,아래쪽=Bertikala_kargu>=(int)(Leihoa->Y_koordenatu+Leihoa->높이)-8;
    return (왼쪽||ESKUIN)&&(위쪽||아래쪽)?1+ESKUIN+아래쪽*2:0;
}
static int 사이값(int balio,int 최소,int 최대){return balio<최소?최소:balio>최대?최대:balio;}
static void eraman_aldatu_tamaina(int 가로,int Bertikala_kargu) {
    Terminal *Leihoa=&Windows_Zerrenda[aldatu_tamaina_arrastatu];int 왼쪽=처음가로,위쪽=처음세로,ESKUIN=처음가로+처음너비,아래쪽=처음세로+처음높이;
    if(잡은모서리==1||잡은모서리==3)왼쪽=사이값(처음가로+가로-잡은가로,0,ESKUIN-360);
    else ESKUIN=사이값(처음가로+처음너비+가로-잡은가로,왼쪽+360,보드화면너비());
    if(잡은모서리<=2)위쪽=사이값(처음세로+Bertikala_kargu-잡은세로,34,아래쪽-216);
    else 아래쪽=사이값(처음세로+처음높이+Bertikala_kargu-잡은세로,위쪽+216,보드화면높이());
    unsigned ZUTABEAK=(ESKUIN-왼쪽-24)/8,ERRENKADA_ZENBATU=(아래쪽-위쪽-56)/16;
    if(Leihoa->ZUTABEAK!=ZUTABEAK||Leihoa->ERRENKADA_ZENBATU!=ERRENKADA_ZENBATU){
        Leihoa->크기바뀜=1;Leihoa->ZUTABEAK=ZUTABEAK;Leihoa->ERRENKADA_ZENBATU=ERRENKADA_ZENBATU;
        if(Leihoa->zutabe_kargu>=ZUTABEAK)Leihoa->zutabe_kargu=ZUTABEAK-1;
        if(Leihoa->ERRENKADA_kargu>=Leihoa->맨위+ERRENKADA_ZENBATU)Leihoa->맨위=Leihoa->ERRENKADA_kargu-ERRENKADA_ZENBATU+1;
        unsigned 한도=Leihoa->맨위;if(한도>Historia_lerro_ZENBATU-ERRENKADA_ZENBATU)한도=Historia_lerro_ZENBATU-ERRENKADA_ZENBATU;
        if(Leihoa->korritu>한도)Leihoa->korritu=한도;
    }
    int 옛가로=Leihoa->X_koordenatu,옛세로=Leihoa->Y_koordenatu,옛폭=Leihoa->너비,옛길이=Leihoa->높이;
    if(옛가로==왼쪽&&옛세로==위쪽&&옛폭==ESKUIN-왼쪽&&옛길이==아래쪽-위쪽)return;
    Leihoa->X_koordenatu=왼쪽;Leihoa->Y_koordenatu=위쪽;Leihoa->너비=ESKUIN-왼쪽;Leihoa->높이=아래쪽-위쪽;
    창자리그리기(옛가로,옛세로,옛폭,옛길이,Leihoa);
}
void Terminal_erakusle(unsigned Hurrengoa_elementu,int X_koordenatu,int Y_koordenatu){
    unsigned 눌림=Hurrengoa_elementu&~단추들;단추들=Hurrengoa_elementu;
    if(!mahaigain_ikusi){arrastatu_balio=-1;aldatu_tamaina_arrastatu=-1;arbel_erakusle(X_koordenatu,Y_koordenatu,1);return;}
    if(!(Hurrengoa_elementu&1)){arrastatu_balio=-1;aldatu_tamaina_arrastatu=-1;}
    if(aldatu_tamaina_arrastatu>=0&&!Windows_Zerrenda[aldatu_tamaina_arrastatu].살아있음)aldatu_tamaina_arrastatu=-1;
    if(arrastatu_balio>=0&&!Windows_Zerrenda[arrastatu_balio].살아있음)arrastatu_balio=-1;
    if(aldatu_tamaina_arrastatu>=0){
        eraman_aldatu_tamaina(X_koordenatu,Y_koordenatu);arbel_erakusle(X_koordenatu,Y_koordenatu,잡은모서리==1||잡은모서리==4?2:3);return;
    }
    arbel_erakusle(X_koordenatu,Y_koordenatu,1);
    if(arrastatu_balio>=0){
        Terminal *Leihoa=&Windows_Zerrenda[arrastatu_balio];
        int 옛가로=Leihoa->X_koordenatu,옛세로=Leihoa->Y_koordenatu;
        Leihoa->X_koordenatu=사이값(X_koordenatu-arrastatu_X,0,보드화면너비()-Leihoa->너비);
        Leihoa->Y_koordenatu=사이값(Y_koordenatu-arrastatu_Y,34,보드화면높이()-Leihoa->높이);
        if(옛가로!=(int)Leihoa->X_koordenatu||옛세로!=(int)Leihoa->Y_koordenatu)창자리그리기(옛가로,옛세로,Leihoa->너비,Leihoa->높이,Leihoa);
        return;
    }
    extern int 화면덮음(int,int,int);
    if(화면덮음(Fokuratua,X_koordenatu,Y_koordenatu)){화면가리킴(Fokuratua,눌림,X_koordenatu,Y_koordenatu);return;}
    int identifikatzaile_balio=가리킨창(X_koordenatu,Y_koordenatu),모서리=모서리찾기(identifikatzaile_balio,X_koordenatu,Y_koordenatu);
    if(모서리)arbel_erakusle(X_koordenatu,Y_koordenatu,모서리==1||모서리==4?2:3);
    if(눌림&1){
        if(모서리){
            Terminal *Leihoa=&Windows_Zerrenda[identifikatzaile_balio];aldatu_tamaina_arrastatu=identifikatzaile_balio;잡은모서리=모서리;잡은가로=X_koordenatu;잡은세로=Y_koordenatu;
            처음가로=Leihoa->X_koordenatu;처음세로=Leihoa->Y_koordenatu;처음너비=Leihoa->너비;처음높이=Leihoa->높이;
            if(identifikatzaile_balio!=Fokuratua)앞으로올리기(identifikatzaile_balio);return;
        }
        if(Y_koordenatu<32&&X_koordenatu>=6&&X_koordenatu<142){sortu_sarrera();return;}
        if(Y_koordenatu<32&&X_koordenatu>=154&&X_koordenatu<602){앞으로올리기((X_koordenatu-154)/112);return;}
        if(identifikatzaile_balio>=0){
            Terminal *Leihoa=&Windows_Zerrenda[identifikatzaile_balio];
            if(Y_koordenatu<(int)Leihoa->Y_koordenatu+30&&X_koordenatu>=(int)(Leihoa->X_koordenatu+Leihoa->너비)-32){itxi_leiho(identifikatzaile_balio);return;}
            if(identifikatzaile_balio!=Fokuratua)앞으로올리기(identifikatzaile_balio);
            if(Y_koordenatu<(int)Leihoa->Y_koordenatu+30){arrastatu_balio=identifikatzaile_balio;arrastatu_X=X_koordenatu-Leihoa->X_koordenatu;arrastatu_Y=Y_koordenatu-Leihoa->Y_koordenatu;}return;
        }
    }
    if(Fokuratua>=0&&(눌림&(8|16))){Terminal_sarrera=&Windows_Zerrenda[Fokuratua];if(눌림&8){unsigned 한도=Terminal_sarrera->맨위;if(한도>Historia_lerro_ZENBATU-Terminal_sarrera->ERRENKADA_ZENBATU)한도=Historia_lerro_ZENBATU-Terminal_sarrera->ERRENKADA_ZENBATU;Terminal_sarrera->korritu=Terminal_sarrera->korritu+9>한도?한도:Terminal_sarrera->korritu+9;}else Terminal_sarrera->korritu=Terminal_sarrera->korritu<9?0:Terminal_sarrera->korritu-9;다시그리기();}
}
void 터미널바로가기키(unsigned 누름값){if(누름값==1)sortu_sarrera();if(누름값==2&&sarrera_ZENBATU)앞으로올리기(ordena_balio[0]);if(누름값==3)itxi_leiho(Fokuratua);}
gailu_Word arbel_Terminal(gailu_Word Ekintza){
    if(Ekintza==300){if(!Windows_Zerrenda[출력결과].살아있음)return sortu_sarrera();mahaigain_ikusi=1;다시그리기();return 0;}
    if(Ekintza==0){itxi_leiho(Fokuratua);return 0;}if(Ekintza==1)return (uint32_t)sortu_sarrera();if(Ekintza==2)return Fokuratua>=0;
    if(Ekintza==9){mahaigain_ikusi=0;return 0;}if(Ekintza==7)return sarrera_ZENBATU;if(Ekintza==10)return Fokuratua+1;if(Ekintza==11)return 출력결과;
    if(Ekintza==13){Terminal *Leihoa=&Windows_Zerrenda[출력결과];return Leihoa->살아있음?(Leihoa->ERRENKADA_ZENBATU<<16)|Leihoa->ZUTABEAK:(19<<16)|68;}
    if(Ekintza==14){unsigned balio=Windows_Zerrenda[출력결과].크기바뀜;Windows_Zerrenda[출력결과].크기바뀜=0;return balio;}
    if(Ekintza==12){unsigned balio=informatika_zain;informatika_zain=0;return balio;}
    if(Ekintza>=20&&Ekintza<24)return Windows_Zerrenda[Ekintza-20].살아있음;
    if(Ekintza>=100&&Ekintza<104){출력결과=Ekintza-100;Terminal_sarrera=&Windows_Zerrenda[출력결과];return 0;}
    if(Ekintza>=200&&Ekintza<204){앞으로올리기(Ekintza-200);return 0;}
    if(Ekintza==3){다시그리기();return 0;}Terminal_sarrera=&Windows_Zerrenda[출력결과];if(!Terminal_sarrera->살아있음)return 0;
    if(Ekintza==4)garbitu_Edukia();if(Ekintza==5||Ekintza==6){unsigned 이전=단추들;Terminal_erakusle(Ekintza==5?8:16,0,0);단추들=이전;}return 1;
}
