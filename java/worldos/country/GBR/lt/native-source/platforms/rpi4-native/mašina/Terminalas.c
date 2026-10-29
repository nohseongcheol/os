#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* savas 네 Langas 합성과 UTF-8 Terminalas. 바뀐 영역의 baigta_VALUE 그림만 표시한다. */
#include <stdint.h>
#include <stddef.h>
typedef uintptr_t mašina_Word;
extern mašina_Word Lenta_pikselis(mašina_Word,mašina_Word,mašina_Word),보드화면기억공간(void);
extern void *memset(void *,int,size_t);
extern const unsigned char Terminalas_šriftas[];
#define 최대열수 237
#define istorija_eilutė_COUNT 160
typedef struct {
    uint32_t 글자칸들[istorija_eilutė_COUNT][최대열수]; uint8_t 모양들[istorija_eilutė_COUNT][최대열수];
    unsigned 너비,높이,COLUMNS,ROW_COUNT,크기바뀜;
    unsigned 살아있음,x_koordinatė,세로좌표,ROW_padėtis,COLUMN_padėtis,맨위,slinkti,전경색,배경색,탈출상태,parametras_VALUE[4],parametras_INDEX,저장행,저장열;
    unsigned 부호없는결과,긴부호없는값,SMALL_VALUE,대체화면,가리개보임;
} Terminalas_d413d4bc;
static Terminalas_d413d4bc Windows_Sąrašas[4];
static int Fokusavimas=-1,išeiga,tvarka_VALUE[4],įrašas_COUNT,vilkti_VALUE=-1,vilkti_X,vilkti_Y;
static unsigned informacinės_technologijos_laukiama,단추들,darbalaukis_rodyti,한글입력;
static const uint32_t 색상들[16]={0x201a15,0x6060df,0x9dcc86,0x80cfea,0xefaf72,0xca96c9,0xceda76,0xede9df,0x858078,0x8888ff,0xb9eba7,0xa5eaff,0xffcc99,0xf0bef1,0xf0f0a0,0xffffff};
extern int 화면보임(int),화면가리킴(int,unsigned,int,int);
extern void 화면다시그림(int);
static Terminalas_d413d4bc *Terminalas_įrašas;
static unsigned platusis_simbolis(unsigned simbolio_kodas){return simbolio_kodas>=256?2:1;}
static void 사각영역(unsigned x_koordinatė,unsigned 세로좌표,unsigned 너비값,unsigned 높이값,unsigned 색상){
    Lenta_stačiakampis_užpildas(x_koordinatė,세로좌표,너비값,높이값,색상);
}
void Terminalas_glifas(unsigned x_koordinatė,unsigned 세로좌표,unsigned simbolio_kodas,unsigned 전경색,unsigned 배경색){
    unsigned 너비=platusis_simbolis(simbolio_kodas)*8;if(simbolio_kodas==0xffffffffu)return;
    int 왼쪽=x_koordinatė,위쪽=세로좌표,폭=너비,길이=16;
    if(!보드그림범위(&왼쪽,&위쪽,&폭,&길이))return;
    if(simbolio_kodas==' '){Lenta_stačiakampis_užpildas(왼쪽,위쪽,폭,길이,배경색);return;}
    unsigned LOOKUP_INDEX=simbolio_kodas<65536?simbolio_kodas:simbolio_kodas>=0x1f600&&simbolio_kodas<0x1f650?65536+simbolio_kodas-0x1f600:0xfffd;
    const unsigned char *šriftas_VALUE=Terminalas_šriftas+LOOKUP_INDEX*32;
    for(int Eilutė=위쪽;Eilutė<위쪽+길이;Eilutė++){unsigned foninio_intelektualiojo_perdavimo_tarnyba_Sąrašas=šriftas_VALUE[(Eilutė-세로좌표)*2]*256+šriftas_VALUE[(Eilutė-세로좌표)*2+1];for(int 칸=왼쪽;칸<왼쪽+폭;칸++)Lenta_pikselis(칸,Eilutė,(foninio_intelektualiojo_perdavimo_tarnyba_Sąrašas&(0x8000>>(칸-x_koordinatė)))?전경색:배경색);}
}
static void pavadinimas_lentelė(unsigned x_koordinatė,unsigned 세로좌표,const char *eilutė_duomenys,unsigned 전경색,unsigned 배경색){while(*eilutė_duomenys){unsigned simbolio_kodas=(unsigned char)*eilutė_duomenys++, 남은수=0;if(simbolio_kodas>=0xc0){남은수=simbolio_kodas<0xe0?1:simbolio_kodas<0xf0?2:3;simbolio_kodas&=(1u<<(6-남은수))-1;while(남은수--&&*eilutė_duomenys)simbolio_kodas=(simbolio_kodas<<6)|((unsigned char)*eilutė_duomenys++&63);}Terminalas_glifas(x_koordinatė,세로좌표,simbolio_kodas,전경색,배경색);x_koordinatė+=platusis_simbolis(simbolio_kodas)*8;}}
static unsigned 첫항목(void){return Terminalas_įrašas->맨위;}
static int 보이는지(void){return Terminalas_įrašas->살아있음&&Fokusavimas>=0&&Terminalas_įrašas==&Windows_Sąrašas[Fokusavimas]&&!화면보임(Fokusavimas);}
static void 그리기(unsigned ROW_padėtis,unsigned COLUMN_padėtis){
    if(!보이는지()||ROW_padėtis<첫항목()-Terminalas_įrašas->slinkti||ROW_padėtis>=첫항목()-Terminalas_įrašas->slinkti+Terminalas_įrašas->ROW_COUNT||COLUMN_padėtis>=Terminalas_įrašas->COLUMNS)return;
    unsigned simbolio_kodas=Terminalas_įrašas->글자칸들[ROW_padėtis%istorija_eilutė_COUNT][COLUMN_padėtis],eilutė_duomenys=Terminalas_įrašas->모양들[ROW_padėtis%istorija_eilutė_COUNT][COLUMN_padėtis];
    if(platusis_simbolis(simbolio_kodas)==2&&COLUMN_padėtis+1>=Terminalas_įrašas->COLUMNS)simbolio_kodas=' ';
    Terminalas_glifas(Terminalas_įrašas->x_koordinatė+12+COLUMN_padėtis*8,Terminalas_įrašas->세로좌표+36+(ROW_padėtis-첫항목()+Terminalas_įrašas->slinkti)*16,simbolio_kodas?simbolio_kodas:' ',색상들[eilutė_duomenys&15],색상들[eilutė_duomenys>>4]);
}
static void stogelio_simbolis_VALUE(int laida_langas){if(!보이는지()||Terminalas_įrašas->slinkti||Terminalas_įrašas->COLUMN_padėtis>=Terminalas_įrašas->COLUMNS||Terminalas_įrašas->ROW_padėtis<Terminalas_įrašas->맨위||Terminalas_įrašas->ROW_padėtis>=Terminalas_įrašas->맨위+Terminalas_įrašas->ROW_COUNT)return;
    if(!laida_langas||!Terminalas_įrašas->가리개보임)그리기(Terminalas_įrašas->ROW_padėtis,Terminalas_įrašas->COLUMN_padėtis);else 사각영역(Terminalas_įrašas->x_koordinatė+12+Terminalas_įrašas->COLUMN_padėtis*8,Terminalas_įrašas->세로좌표+36+(Terminalas_įrašas->ROW_padėtis-Terminalas_įrašas->맨위)*16+14,8,2,색상들[Terminalas_įrašas->전경색]);}
static void Turinys_VALUE(void){
    사각영역(Terminalas_įrašas->x_koordinatė+12,Terminalas_įrašas->세로좌표+36,Terminalas_įrašas->COLUMNS*8,Terminalas_įrašas->ROW_COUNT*16,색상들[0]);
    int 가로=Terminalas_įrašas->x_koordinatė+12,segmentas_padėtis=Terminalas_įrašas->세로좌표+36,폭=Terminalas_įrašas->COLUMNS*8,길이=Terminalas_įrašas->ROW_COUNT*16;
    if(보드그림범위(&가로,&segmentas_padėtis,&폭,&길이)){
    unsigned 첫줄=(segmentas_padėtis-Terminalas_įrašas->세로좌표-36)/16,끝줄=(segmentas_padėtis+길이-Terminalas_įrašas->세로좌표-36+15)/16;
    unsigned 첫칸=(가로-Terminalas_įrašas->x_koordinatė-12)/8,끝칸=(가로+폭-Terminalas_įrašas->x_koordinatė-12+7)/8;
    if(첫칸)첫칸--; /* 잘림 경계 왼쪽에서 시작한 두 칸 글자도 그린다. */
    for(unsigned 반환값=첫줄;반환값<끝줄;반환값++)for(unsigned simbolio_kodas=첫칸;simbolio_kodas<끝칸;simbolio_kodas++){
        unsigned ROW_padėtis=첫항목()-Terminalas_įrašas->slinkti+반환값,simbolis_VALUE_068c2631=Terminalas_įrašas->글자칸들[ROW_padėtis%istorija_eilutė_COUNT][simbolio_kodas],eilutė_duomenys=Terminalas_įrašas->모양들[ROW_padėtis%istorija_eilutė_COUNT][simbolio_kodas];
        if(platusis_simbolis(simbolis_VALUE_068c2631)==2&&simbolio_kodas+1>=Terminalas_įrašas->COLUMNS)simbolis_VALUE_068c2631=' ';
        if((simbolis_VALUE_068c2631==0||simbolis_VALUE_068c2631==' ')&&(eilutė_duomenys>>4)==0)continue;
        Terminalas_glifas(Terminalas_įrašas->x_koordinatė+12+simbolio_kodas*8,Terminalas_įrašas->세로좌표+36+반환값*16,simbolis_VALUE_068c2631?simbolis_VALUE_068c2631:' ',색상들[eilutė_duomenys&15],색상들[eilutė_duomenys>>4]);
    }}
    pavadinimas_lentelė(Terminalas_įrašas->x_koordinatė+12,Terminalas_įrašas->세로좌표+Terminalas_įrašas->높이-18,Terminalas_įrašas->slinkti?"PgDn: recent output":Terminalas_įrašas->너비>=500?"F6: next | Corner + left drag: resize":"Corner + left drag: resize",0xece8e2,0x403127);stogelio_simbolis_VALUE(1);
}
static void 실행틀(int identifikatorius_VALUE){
    Terminalas_įrašas=&Windows_Sąrašas[identifikatorius_VALUE];
    int 가로=Terminalas_įrašas->x_koordinatė,segmentas_padėtis=Terminalas_įrašas->세로좌표,폭=Terminalas_įrašas->너비,길이=Terminalas_įrašas->높이;
    if(!보드그림범위(&가로,&segmentas_padėtis,&폭,&길이))return;
    사각영역(Terminalas_įrašas->x_koordinatė,Terminalas_įrašas->세로좌표,Terminalas_įrašas->너비,Terminalas_įrašas->높이,0x403127);
    unsigned 색상=identifikatorius_VALUE==Fokusavimas?0x905020:0x604438;사각영역(Terminalas_įrašas->x_koordinatė,Terminalas_įrašas->세로좌표,Terminalas_įrašas->너비,30,색상);
    pavadinimas_lentelė(Terminalas_įrašas->x_koordinatė+12,Terminalas_įrašas->세로좌표+7,"JKOROS Terminal",0xffffff,색상);
    char 수치[2]={(char)('1'+identifikatorius_VALUE),0};pavadinimas_lentelė(Terminalas_įrašas->x_koordinatė+148,Terminalas_įrašas->세로좌표+7,수치,0xffffff,색상);
    pavadinimas_lentelė(Terminalas_įrašas->x_koordinatė+240,Terminalas_įrašas->세로좌표+7,Terminalas_įrašas->너비>=500?(한글입력?"[LT] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[LT]":"[EN]"),0xffffff,색상);
    사각영역(Terminalas_įrašas->x_koordinatė+Terminalas_įrašas->너비-32,Terminalas_įrašas->세로좌표+4,26,22,0x5555b8);pavadinimas_lentelė(Terminalas_įrašas->x_koordinatė+Terminalas_įrašas->너비-24,Terminalas_įrašas->세로좌표+7,"X",0xffffff,0x5555b8);
    Turinys_VALUE();
}
static void piešti_scena(void){
    if(!darbalaukis_rodyti)return;사각영역(0,0,보드화면너비(),보드화면높이(),0x302018);사각영역(0,0,보드화면너비(),32,0x403127);
    사각영역(6,4,136,24,0x905020);pavadinimas_lentelė(14,8,"+ New terminal",0xffffff,0x905020);
    for(int 순번=0;순번<4;순번++)if(Windows_Sąrašas[순번].살아있음){unsigned simbolio_kodas=Fokusavimas==순번?0x905020:0x604438;사각영역(154+순번*112,4,106,24,simbolio_kodas);pavadinimas_lentelė(160+순번*112,8,"Terminal",0xffffff,simbolio_kodas);char eilutė_duomenys[2]={(char)('1'+순번),0};pavadinimas_lentelė(232+순번*112,8,eilutė_duomenys,0xffffff,simbolio_kodas);}
    if(!įrašas_COUNT)pavadinimas_lentelė(140,210,"Click + New terminal to start",0xede9df,0x302018);
    for(int 순번=0;순번<įrašas_COUNT;순번++)실행틀(tvarka_VALUE[순번]);화면다시그림(Fokusavimas);Terminalas_įrašas=&Windows_Sąrašas[išeiga];
}
static void Piešimas_sritis(int 가로,int segmentas_padėtis,int 폭,int 길이){
    if(!darbalaukis_rodyti||!보드그림범위(&가로,&segmentas_padėtis,&폭,&길이))return;
    for(int Eilutė=segmentas_padėtis;Eilutė<segmentas_padėtis+길이;Eilutė+=32){
        int 띠높이=segmentas_padėtis+길이-Eilutė;if(띠높이>32)띠높이=32;
        if(Lenta_Start_piešinys(가로,Eilutė,폭,띠높이)){piešti_scena();Lenta_Baigti_piešinys();}
    }
}
static void 다시그리기(void){Piešimas_sritis(0,0,보드화면너비(),보드화면높이());}
/* 서로 겹치지 않는 새 Langas 영역과 이전 자리의 네 띠를 복구한다. */
static void 창자리그리기(int 가로,int segmentas_padėtis,int 폭,int 길이,Terminalas_d413d4bc *Langas){
    int 왼쪽=가로>(int)Langas->x_koordinatė?가로:(int)Langas->x_koordinatė;
    int 위쪽=segmentas_padėtis>(int)Langas->세로좌표?segmentas_padėtis:(int)Langas->세로좌표;
    int RIGHT=가로+폭<(int)(Langas->x_koordinatė+Langas->너비)?가로+폭:(int)(Langas->x_koordinatė+Langas->너비);
    int 아래쪽=segmentas_padėtis+길이<(int)(Langas->세로좌표+Langas->높이)?segmentas_padėtis+길이:(int)(Langas->세로좌표+Langas->높이);
    Piešimas_sritis(Langas->x_koordinatė,Langas->세로좌표,Langas->너비,Langas->높이);
    if(왼쪽>=RIGHT||위쪽>=아래쪽){Piešimas_sritis(가로,segmentas_padėtis,폭,길이);return;}
    Piešimas_sritis(가로,segmentas_padėtis,폭,위쪽-segmentas_padėtis);
    Piešimas_sritis(가로,아래쪽,폭,segmentas_padėtis+길이-아래쪽);
    Piešimas_sritis(가로,위쪽,왼쪽-가로,아래쪽-위쪽);
    Piešimas_sritis(RIGHT,위쪽,가로+폭-RIGHT,아래쪽-위쪽);
}
static void signalas_Fokusavimas(void){informacinės_technologijos_laukiama=(informacinės_technologijos_laukiama&~15u)|(unsigned)(Fokusavimas+1)|0x10000;}
void 터미널입력방식(unsigned 한글여부){
    한글입력=한글여부!=0;
    /* Update title bars only: a mode switch must not erase an EL0 drawing. */
    if(Fokusavimas>=0){
        Terminalas_d413d4bc *langas_įrašas=&Windows_Sąrašas[Fokusavimas];
        pavadinimas_lentelė(langas_įrašas->x_koordinatė+240,langas_įrašas->세로좌표+7,langas_įrašas->너비>=500?(한글입력?"[LT] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[LT]":"[EN]"),0xffffff,0x905020);
    }
}
static void 앞으로올리기(int identifikatorius_VALUE){if(identifikatorius_VALUE<0||identifikatorius_VALUE>=4||!Windows_Sąrašas[identifikatorius_VALUE].살아있음)return;int dabartinis_padėtis=0;while(dabartinis_padėtis<įrašas_COUNT&&tvarka_VALUE[dabartinis_padėtis]!=identifikatorius_VALUE)dabartinis_padėtis++;for(;dabartinis_padėtis+1<įrašas_COUNT;dabartinis_padėtis++)tvarka_VALUE[dabartinis_padėtis]=tvarka_VALUE[dabartinis_padėtis+1];tvarka_VALUE[įrašas_COUNT-1]=identifikatorius_VALUE;Fokusavimas=identifikatorius_VALUE;signalas_Fokusavimas();다시그리기();}
static void 빈칸채우기(unsigned ROW_padėtis){for(unsigned simbolio_kodas=0;simbolio_kodas<최대열수;simbolio_kodas++){Terminalas_įrašas->글자칸들[ROW_padėtis%istorija_eilutė_COUNT][simbolio_kodas]=0;Terminalas_įrašas->모양들[ROW_padėtis%istorija_eilutė_COUNT][simbolio_kodas]=Terminalas_įrašas->전경색|(Terminalas_įrašas->배경색<<4);}}
static void apmokėti_Turinys(void){Terminalas_įrašas->ROW_padėtis=Terminalas_įrašas->COLUMN_padėtis=Terminalas_įrašas->맨위=Terminalas_įrašas->slinkti=0;for(unsigned 반환값=0;반환값<istorija_eilutė_COUNT;반환값++)빈칸채우기(반환값);if(보이는지())Turinys_VALUE();}
static int kurti_įrašas(void){
    if(!보드화면기억공간())return -19;int identifikatorius_VALUE=0;while(identifikatorius_VALUE<4&&Windows_Sąrašas[identifikatorius_VALUE].살아있음)identifikatorius_VALUE++;if(identifikatorius_VALUE==4)return -28;
    darbalaukis_rodyti=1;Terminalas_įrašas=&Windows_Sąrašas[identifikatorius_VALUE];memset(Terminalas_įrašas,0,sizeof(*Terminalas_įrašas));Terminalas_įrašas->살아있음=1;Terminalas_įrašas->너비=568;Terminalas_įrašas->높이=360;Terminalas_įrašas->COLUMNS=68;Terminalas_įrašas->ROW_COUNT=19;Terminalas_įrašas->x_koordinatė=12+identifikatorius_VALUE*16;Terminalas_įrašas->세로좌표=48+identifikatorius_VALUE*18;Terminalas_įrašas->전경색=7;Terminalas_įrašas->가리개보임=1;
    for(unsigned 반환값=0;반환값<istorija_eilutė_COUNT;반환값++)빈칸채우기(반환값);tvarka_VALUE[įrašas_COUNT++]=identifikatorius_VALUE;Fokusavimas=identifikatorius_VALUE;informacinės_technologijos_laukiama|=1u<<(4+identifikatorius_VALUE);signalas_Fokusavimas();다시그리기();return identifikatorius_VALUE+1;
}
static void Uždaryti_langas(int identifikatorius_VALUE){
    if(identifikatorius_VALUE<0||identifikatorius_VALUE>=4||!Windows_Sąrašas[identifikatorius_VALUE].살아있음)return;Windows_Sąrašas[identifikatorius_VALUE].살아있음=0;informacinės_technologijos_laukiama|=1u<<(8+identifikatorius_VALUE);
    int dabartinis_padėtis=0;while(dabartinis_padėtis<įrašas_COUNT&&tvarka_VALUE[dabartinis_padėtis]!=identifikatorius_VALUE)dabartinis_padėtis++;for(;dabartinis_padėtis+1<įrašas_COUNT;dabartinis_padėtis++)tvarka_VALUE[dabartinis_padėtis]=tvarka_VALUE[dabartinis_padėtis+1];įrašas_COUNT--;
    if(Fokusavimas==identifikatorius_VALUE)Fokusavimas=įrašas_COUNT?tvarka_VALUE[įrašas_COUNT-1]:-1;signalas_Fokusavimas();다시그리기();
}
static void 줄바꿈(void){Terminalas_įrašas->COLUMN_padėtis=0;Terminalas_įrašas->ROW_padėtis++;if(Terminalas_įrašas->ROW_padėtis>=Terminalas_įrašas->맨위+Terminalas_įrašas->ROW_COUNT){Terminalas_įrašas->맨위++;빈칸채우기(Terminalas_įrašas->ROW_padėtis);if(보이는지())Turinys_VALUE();}}
static void kodo_elementas(unsigned simbolio_kodas){
    if(simbolio_kodas==13){Terminalas_įrašas->COLUMN_padėtis=0;return;}if(simbolio_kodas==10){줄바꿈();return;}if(simbolio_kodas==8){if(Terminalas_įrašas->COLUMN_padėtis)Terminalas_įrašas->COLUMN_padėtis--;return;}
    if(simbolio_kodas==9){unsigned prekė_COUNT=8-Terminalas_įrašas->COLUMN_padėtis%8;while(prekė_COUNT--)kodo_elementas(' ');return;}if(simbolio_kodas<32||simbolio_kodas==127)return;
    unsigned 너비값=platusis_simbolis(simbolio_kodas);if(Terminalas_įrašas->COLUMN_padėtis+너비값>Terminalas_įrašas->COLUMNS)줄바꿈();
    if(Terminalas_įrašas->글자칸들[Terminalas_įrašas->ROW_padėtis%istorija_eilutė_COUNT][Terminalas_įrašas->COLUMN_padėtis]==0xffffffffu&&Terminalas_įrašas->COLUMN_padėtis){Terminalas_įrašas->글자칸들[Terminalas_įrašas->ROW_padėtis%istorija_eilutė_COUNT][Terminalas_įrašas->COLUMN_padėtis-1]=' ';그리기(Terminalas_įrašas->ROW_padėtis,Terminalas_įrašas->COLUMN_padėtis-1);}
    if(platusis_simbolis(Terminalas_įrašas->글자칸들[Terminalas_įrašas->ROW_padėtis%istorija_eilutė_COUNT][Terminalas_įrašas->COLUMN_padėtis])==2&&Terminalas_įrašas->COLUMN_padėtis+1<Terminalas_įrašas->COLUMNS){Terminalas_įrašas->글자칸들[Terminalas_įrašas->ROW_padėtis%istorija_eilutė_COUNT][Terminalas_įrašas->COLUMN_padėtis+1]=' ';그리기(Terminalas_įrašas->ROW_padėtis,Terminalas_įrašas->COLUMN_padėtis+1);}
    Terminalas_įrašas->글자칸들[Terminalas_įrašas->ROW_padėtis%istorija_eilutė_COUNT][Terminalas_įrašas->COLUMN_padėtis]=simbolio_kodas;Terminalas_įrašas->모양들[Terminalas_įrašas->ROW_padėtis%istorija_eilutė_COUNT][Terminalas_įrašas->COLUMN_padėtis]=Terminalas_įrašas->전경색|(Terminalas_įrašas->배경색<<4);
    if(너비값==2)Terminalas_įrašas->글자칸들[Terminalas_įrašas->ROW_padėtis%istorija_eilutė_COUNT][Terminalas_įrašas->COLUMN_padėtis+1]=0xffffffffu;
    그리기(Terminalas_įrašas->ROW_padėtis,Terminalas_įrašas->COLUMN_padėtis);Terminalas_įrašas->COLUMN_padėtis+=너비값;
}
static void rodyklė_valdymas_SEQUENCE(unsigned simbolio_kodas){
    unsigned prekė_COUNT=Terminalas_įrašas->parametras_VALUE[0]?Terminalas_įrašas->parametras_VALUE[0]:1;
    if(simbolio_kodas=='m')for(unsigned 순번=0;순번<=Terminalas_įrašas->parametras_INDEX;순번++){unsigned duomenys_padėtis=Terminalas_įrašas->parametras_VALUE[순번];if(!duomenys_padėtis){Terminalas_įrašas->전경색=7;Terminalas_įrašas->배경색=0;}if(duomenys_padėtis==1&&Terminalas_įrašas->전경색<8)Terminalas_įrašas->전경색+=8;if(duomenys_padėtis==7){unsigned 유지=Terminalas_įrašas->전경색;Terminalas_įrašas->전경색=Terminalas_įrašas->배경색;Terminalas_įrašas->배경색=유지;}if(duomenys_padėtis>=30&&duomenys_padėtis<=37)Terminalas_įrašas->전경색=duomenys_padėtis-30;if(duomenys_padėtis>=90&&duomenys_padėtis<=97)Terminalas_įrašas->전경색=duomenys_padėtis-90+8;if(duomenys_padėtis>=40&&duomenys_padėtis<=47)Terminalas_įrašas->배경색=duomenys_padėtis-40;if(duomenys_padėtis>=100&&duomenys_padėtis<=107)Terminalas_įrašas->배경색=duomenys_padėtis-100+8;if(duomenys_padėtis==39)Terminalas_įrašas->전경색=7;if(duomenys_padėtis==49)Terminalas_įrašas->배경색=0;}
    if(simbolio_kodas=='J'&&(Terminalas_įrašas->parametras_VALUE[0]==2||Terminalas_įrašas->parametras_VALUE[0]==3))apmokėti_Turinys();
    if(simbolio_kodas=='K'){unsigned 출발위치=Terminalas_įrašas->parametras_VALUE[0]==2?0:Terminalas_įrašas->COLUMN_padėtis,도착위치=Terminalas_įrašas->parametras_VALUE[0]==1?Terminalas_įrašas->COLUMN_padėtis+1:Terminalas_įrašas->COLUMNS;if(Terminalas_įrašas->parametras_VALUE[0]==1)출발위치=0;for(unsigned 순번=출발위치;순번<도착위치&&순번<Terminalas_įrašas->COLUMNS;순번++){
        unsigned ROW_VALUE=Terminalas_įrašas->ROW_padėtis%istorija_eilutė_COUNT,simbolis_VALUE_068c2631=Terminalas_įrašas->글자칸들[ROW_VALUE][순번],figūra_VALUE=Terminalas_įrašas->전경색|(Terminalas_įrašas->배경색<<4);
        /* 넓은 vi 화면에서도 이미 빈 칸의 šriftas_VALUE 화소를 되풀이해 칠하지 않는다. */
        int 바뀜=(simbolis_VALUE_068c2631!=0&&simbolis_VALUE_068c2631!=' ')||Terminalas_įrašas->모양들[ROW_VALUE][순번]!=figūra_VALUE;
        Terminalas_įrašas->글자칸들[ROW_VALUE][순번]=' ';Terminalas_įrašas->모양들[ROW_VALUE][순번]=figūra_VALUE;
        if(바뀜)그리기(Terminalas_įrašas->ROW_padėtis,순번);
    }}
    if(simbolio_kodas=='D')Terminalas_įrašas->COLUMN_padėtis=prekė_COUNT>Terminalas_įrašas->COLUMN_padėtis?0:Terminalas_įrašas->COLUMN_padėtis-prekė_COUNT;if(simbolio_kodas=='C')Terminalas_įrašas->COLUMN_padėtis=Terminalas_įrašas->COLUMN_padėtis+prekė_COUNT>=Terminalas_įrašas->COLUMNS?Terminalas_įrašas->COLUMNS-1:Terminalas_įrašas->COLUMN_padėtis+prekė_COUNT;
    if(simbolio_kodas=='G')Terminalas_įrašas->COLUMN_padėtis=prekė_COUNT>Terminalas_įrašas->COLUMNS?Terminalas_įrašas->COLUMNS-1:prekė_COUNT-1;if(simbolio_kodas=='A')Terminalas_įrašas->ROW_padėtis=prekė_COUNT>Terminalas_įrašas->ROW_padėtis-Terminalas_įrašas->맨위?Terminalas_įrašas->맨위:Terminalas_įrašas->ROW_padėtis-prekė_COUNT;
    if(simbolio_kodas=='B')Terminalas_įrašas->ROW_padėtis=Terminalas_įrašas->ROW_padėtis+prekė_COUNT>=Terminalas_įrašas->맨위+Terminalas_įrašas->ROW_COUNT?Terminalas_įrašas->맨위+Terminalas_įrašas->ROW_COUNT-1:Terminalas_įrašas->ROW_padėtis+prekė_COUNT;
    if(simbolio_kodas=='H'||simbolio_kodas=='f'){Terminalas_įrašas->ROW_padėtis=Terminalas_įrašas->맨위+(prekė_COUNT>Terminalas_įrašas->ROW_COUNT?Terminalas_įrašas->ROW_COUNT:prekė_COUNT)-1;unsigned x_koordinatė=Terminalas_įrašas->parametras_VALUE[1]?Terminalas_įrašas->parametras_VALUE[1]:1;Terminalas_įrašas->COLUMN_padėtis=(x_koordinatė>Terminalas_įrašas->COLUMNS?Terminalas_įrašas->COLUMNS:x_koordinatė)-1;}
    if(simbolio_kodas=='s'){Terminalas_įrašas->저장행=Terminalas_įrašas->ROW_padėtis;Terminalas_įrašas->저장열=Terminalas_įrašas->COLUMN_padėtis;}if(simbolio_kodas=='u'){Terminalas_įrašas->ROW_padėtis=Terminalas_įrašas->저장행;Terminalas_įrašas->COLUMN_padėtis=Terminalas_įrašas->저장열<Terminalas_įrašas->COLUMNS?Terminalas_įrašas->저장열:Terminalas_įrašas->COLUMNS-1;}
    if((simbolio_kodas=='h'||simbolio_kodas=='l')&&Terminalas_įrašas->parametras_VALUE[0]==25)Terminalas_įrašas->가리개보임=simbolio_kodas=='h';
}
void Terminalas_baitas(unsigned SECOND_VALUE){
    Terminalas_įrašas=&Windows_Sąrašas[išeiga];if(!Terminalas_įrašas->살아있음)return;stogelio_simbolis_VALUE(0);if(Terminalas_įrašas->slinkti){Terminalas_įrašas->slinkti=0;if(보이는지())Turinys_VALUE();}
    if(Terminalas_įrašas->탈출상태==1){Terminalas_įrašas->탈출상태=SECOND_VALUE=='['?2:0;Terminalas_įrašas->parametras_INDEX=0;for(unsigned 순번=0;순번<4;순번++)Terminalas_įrašas->parametras_VALUE[순번]=0;}
    else if(Terminalas_įrašas->탈출상태==2){if(SECOND_VALUE=='?'){}else if(SECOND_VALUE>='0'&&SECOND_VALUE<='9'){if(Terminalas_įrašas->parametras_VALUE[Terminalas_įrašas->parametras_INDEX]<10000)Terminalas_įrašas->parametras_VALUE[Terminalas_įrašas->parametras_INDEX]=Terminalas_įrašas->parametras_VALUE[Terminalas_įrašas->parametras_INDEX]*10+SECOND_VALUE-'0';}else if(SECOND_VALUE==';'&&Terminalas_įrašas->parametras_INDEX<3)Terminalas_įrašas->parametras_INDEX++;else{rodyklė_valdymas_SEQUENCE(SECOND_VALUE);Terminalas_įrašas->탈출상태=0;}}
    else if(SECOND_VALUE==27){Terminalas_įrašas->긴부호없는값=0;Terminalas_įrašas->탈출상태=1;}else{
        if(Terminalas_įrašas->긴부호없는값&&(SECOND_VALUE&0xc0)!=0x80){Terminalas_įrašas->긴부호없는값=0;kodo_elementas(0xfffd);}
        if(Terminalas_įrašas->긴부호없는값){Terminalas_įrašas->부호없는결과=Terminalas_įrašas->부호없는결과*64+(SECOND_VALUE&63);if(--Terminalas_įrašas->긴부호없는값==0)kodo_elementas(Terminalas_įrašas->부호없는결과<Terminalas_įrašas->SMALL_VALUE||Terminalas_įrašas->부호없는결과>0x10ffff||(Terminalas_įrašas->부호없는결과>=0xd800&&Terminalas_įrašas->부호없는결과<=0xdfff)?0xfffd:Terminalas_įrašas->부호없는결과);}
        else if(SECOND_VALUE<128)kodo_elementas(SECOND_VALUE);else if(SECOND_VALUE>=0xc2&&SECOND_VALUE<=0xf4){Terminalas_įrašas->긴부호없는값=SECOND_VALUE<0xe0?1:SECOND_VALUE<0xf0?2:3;Terminalas_įrašas->부호없는결과=SECOND_VALUE&((1u<<(6-Terminalas_įrašas->긴부호없는값))-1);Terminalas_įrašas->SMALL_VALUE=Terminalas_įrašas->긴부호없는값==1?128:Terminalas_įrašas->긴부호없는값==2?2048:65536;}else kodo_elementas(0xfffd);
    }stogelio_simbolis_VALUE(1);
}
int Terminalas_laukiama(void){return informacinės_technologijos_laukiama!=0;}
/* 모서리 INDEX: 1 좌상, 2 우상, 3 좌하, 4 우하. */
static int keisti_dydį_vilkti=-1,잡은모서리,잡은가로,잡은세로,처음가로,처음세로,처음너비,처음높이;
static int 가리킨창(int 가로,int segmentas_padėtis) {
    for(int SEQUENCE_VALUE=įrašas_COUNT-1;SEQUENCE_VALUE>=0;SEQUENCE_VALUE--){
        int identifikatorius_VALUE=tvarka_VALUE[SEQUENCE_VALUE];Terminalas_d413d4bc *Langas=&Windows_Sąrašas[identifikatorius_VALUE];
        if(가로>=(int)Langas->x_koordinatė&&segmentas_padėtis>=(int)Langas->세로좌표&&
           가로<(int)(Langas->x_koordinatė+Langas->너비)&&segmentas_padėtis<(int)(Langas->세로좌표+Langas->높이))return identifikatorius_VALUE;
    }return -1;
}
static int 모서리찾기(int identifikatorius_VALUE,int 가로,int segmentas_padėtis) {
    if(identifikatorius_VALUE<0)return 0;Terminalas_d413d4bc *Langas=&Windows_Sąrašas[identifikatorius_VALUE];
    int 왼쪽=가로<(int)Langas->x_koordinatė+8,RIGHT=가로>=(int)(Langas->x_koordinatė+Langas->너비)-8;
    int 위쪽=segmentas_padėtis<(int)Langas->세로좌표+8,아래쪽=segmentas_padėtis>=(int)(Langas->세로좌표+Langas->높이)-8;
    return (왼쪽||RIGHT)&&(위쪽||아래쪽)?1+RIGHT+아래쪽*2:0;
}
static int skyriklis_VALUE(int VALUE,int 최소,int 최대){return VALUE<최소?최소:VALUE>최대?최대:VALUE;}
static void judėti_keisti_dydį(int 가로,int segmentas_padėtis) {
    Terminalas_d413d4bc *Langas=&Windows_Sąrašas[keisti_dydį_vilkti];int 왼쪽=처음가로,위쪽=처음세로,RIGHT=처음가로+처음너비,아래쪽=처음세로+처음높이;
    if(잡은모서리==1||잡은모서리==3)왼쪽=skyriklis_VALUE(처음가로+가로-잡은가로,0,RIGHT-360);
    else RIGHT=skyriklis_VALUE(처음가로+처음너비+가로-잡은가로,왼쪽+360,보드화면너비());
    if(잡은모서리<=2)위쪽=skyriklis_VALUE(처음세로+segmentas_padėtis-잡은세로,34,아래쪽-216);
    else 아래쪽=skyriklis_VALUE(처음세로+처음높이+segmentas_padėtis-잡은세로,위쪽+216,보드화면높이());
    unsigned COLUMNS=(RIGHT-왼쪽-24)/8,ROW_COUNT=(아래쪽-위쪽-56)/16;
    if(Langas->COLUMNS!=COLUMNS||Langas->ROW_COUNT!=ROW_COUNT){
        Langas->크기바뀜=1;Langas->COLUMNS=COLUMNS;Langas->ROW_COUNT=ROW_COUNT;
        if(Langas->COLUMN_padėtis>=COLUMNS)Langas->COLUMN_padėtis=COLUMNS-1;
        if(Langas->ROW_padėtis>=Langas->맨위+ROW_COUNT)Langas->맨위=Langas->ROW_padėtis-ROW_COUNT+1;
        unsigned 한도=Langas->맨위;if(한도>istorija_eilutė_COUNT-ROW_COUNT)한도=istorija_eilutė_COUNT-ROW_COUNT;
        if(Langas->slinkti>한도)Langas->slinkti=한도;
    }
    int 옛가로=Langas->x_koordinatė,옛세로=Langas->세로좌표,옛폭=Langas->너비,옛길이=Langas->높이;
    if(옛가로==왼쪽&&옛세로==위쪽&&옛폭==RIGHT-왼쪽&&옛길이==아래쪽-위쪽)return;
    Langas->x_koordinatė=왼쪽;Langas->세로좌표=위쪽;Langas->너비=RIGHT-왼쪽;Langas->높이=아래쪽-위쪽;
    창자리그리기(옛가로,옛세로,옛폭,옛길이,Langas);
}
void Terminalas_rodyklė(unsigned toliau_prekė,int x_koordinatė,int 세로좌표){
    unsigned 눌림=toliau_prekė&~단추들;단추들=toliau_prekė;
    if(!darbalaukis_rodyti){vilkti_VALUE=-1;keisti_dydį_vilkti=-1;Lenta_rodyklė(x_koordinatė,세로좌표,1);return;}
    if(!(toliau_prekė&1)){vilkti_VALUE=-1;keisti_dydį_vilkti=-1;}
    if(keisti_dydį_vilkti>=0&&!Windows_Sąrašas[keisti_dydį_vilkti].살아있음)keisti_dydį_vilkti=-1;
    if(vilkti_VALUE>=0&&!Windows_Sąrašas[vilkti_VALUE].살아있음)vilkti_VALUE=-1;
    if(keisti_dydį_vilkti>=0){
        judėti_keisti_dydį(x_koordinatė,세로좌표);Lenta_rodyklė(x_koordinatė,세로좌표,잡은모서리==1||잡은모서리==4?2:3);return;
    }
    Lenta_rodyklė(x_koordinatė,세로좌표,1);
    if(vilkti_VALUE>=0){
        Terminalas_d413d4bc *Langas=&Windows_Sąrašas[vilkti_VALUE];
        int 옛가로=Langas->x_koordinatė,옛세로=Langas->세로좌표;
        Langas->x_koordinatė=skyriklis_VALUE(x_koordinatė-vilkti_X,0,보드화면너비()-Langas->너비);
        Langas->세로좌표=skyriklis_VALUE(세로좌표-vilkti_Y,34,보드화면높이()-Langas->높이);
        if(옛가로!=(int)Langas->x_koordinatė||옛세로!=(int)Langas->세로좌표)창자리그리기(옛가로,옛세로,Langas->너비,Langas->높이,Langas);
        return;
    }
    extern int 화면덮음(int,int,int);
    if(화면덮음(Fokusavimas,x_koordinatė,세로좌표)){화면가리킴(Fokusavimas,눌림,x_koordinatė,세로좌표);return;}
    int identifikatorius_VALUE=가리킨창(x_koordinatė,세로좌표),모서리=모서리찾기(identifikatorius_VALUE,x_koordinatė,세로좌표);
    if(모서리)Lenta_rodyklė(x_koordinatė,세로좌표,모서리==1||모서리==4?2:3);
    if(눌림&1){
        if(모서리){
            Terminalas_d413d4bc *Langas=&Windows_Sąrašas[identifikatorius_VALUE];keisti_dydį_vilkti=identifikatorius_VALUE;잡은모서리=모서리;잡은가로=x_koordinatė;잡은세로=세로좌표;
            처음가로=Langas->x_koordinatė;처음세로=Langas->세로좌표;처음너비=Langas->너비;처음높이=Langas->높이;
            if(identifikatorius_VALUE!=Fokusavimas)앞으로올리기(identifikatorius_VALUE);return;
        }
        if(세로좌표<32&&x_koordinatė>=6&&x_koordinatė<142){kurti_įrašas();return;}
        if(세로좌표<32&&x_koordinatė>=154&&x_koordinatė<602){앞으로올리기((x_koordinatė-154)/112);return;}
        if(identifikatorius_VALUE>=0){
            Terminalas_d413d4bc *Langas=&Windows_Sąrašas[identifikatorius_VALUE];
            if(세로좌표<(int)Langas->세로좌표+30&&x_koordinatė>=(int)(Langas->x_koordinatė+Langas->너비)-32){Uždaryti_langas(identifikatorius_VALUE);return;}
            if(identifikatorius_VALUE!=Fokusavimas)앞으로올리기(identifikatorius_VALUE);
            if(세로좌표<(int)Langas->세로좌표+30){vilkti_VALUE=identifikatorius_VALUE;vilkti_X=x_koordinatė-Langas->x_koordinatė;vilkti_Y=세로좌표-Langas->세로좌표;}return;
        }
    }
    if(Fokusavimas>=0&&(눌림&(8|16))){Terminalas_įrašas=&Windows_Sąrašas[Fokusavimas];if(눌림&8){unsigned 한도=Terminalas_įrašas->맨위;if(한도>istorija_eilutė_COUNT-Terminalas_įrašas->ROW_COUNT)한도=istorija_eilutė_COUNT-Terminalas_įrašas->ROW_COUNT;Terminalas_įrašas->slinkti=Terminalas_įrašas->slinkti+9>한도?한도:Terminalas_įrašas->slinkti+9;}else Terminalas_įrašas->slinkti=Terminalas_įrašas->slinkti<9?0:Terminalas_įrašas->slinkti-9;다시그리기();}
}
void 터미널바로가기키(unsigned 누름값){if(누름값==1)kurti_įrašas();if(누름값==2&&įrašas_COUNT)앞으로올리기(tvarka_VALUE[0]);if(누름값==3)Uždaryti_langas(Fokusavimas);}
mašina_Word Lenta_Terminalas(mašina_Word Veiksmas){
    if(Veiksmas==300){if(!Windows_Sąrašas[išeiga].살아있음)return kurti_įrašas();darbalaukis_rodyti=1;다시그리기();return 0;}
    if(Veiksmas==0){Uždaryti_langas(Fokusavimas);return 0;}if(Veiksmas==1)return (uint32_t)kurti_įrašas();if(Veiksmas==2)return Fokusavimas>=0;
    if(Veiksmas==9){darbalaukis_rodyti=0;return 0;}if(Veiksmas==7)return įrašas_COUNT;if(Veiksmas==10)return Fokusavimas+1;if(Veiksmas==11)return išeiga;
    if(Veiksmas==13){Terminalas_d413d4bc *Langas=&Windows_Sąrašas[išeiga];return Langas->살아있음?(Langas->ROW_COUNT<<16)|Langas->COLUMNS:(19<<16)|68;}
    if(Veiksmas==14){unsigned VALUE=Windows_Sąrašas[išeiga].크기바뀜;Windows_Sąrašas[išeiga].크기바뀜=0;return VALUE;}
    if(Veiksmas==12){unsigned VALUE=informacinės_technologijos_laukiama;informacinės_technologijos_laukiama=0;return VALUE;}
    if(Veiksmas>=20&&Veiksmas<24)return Windows_Sąrašas[Veiksmas-20].살아있음;
    if(Veiksmas>=100&&Veiksmas<104){išeiga=Veiksmas-100;Terminalas_įrašas=&Windows_Sąrašas[išeiga];return 0;}
    if(Veiksmas>=200&&Veiksmas<204){앞으로올리기(Veiksmas-200);return 0;}
    if(Veiksmas==3){다시그리기();return 0;}Terminalas_įrašas=&Windows_Sąrašas[išeiga];if(!Terminalas_įrašas->살아있음)return 0;
    if(Veiksmas==4)apmokėti_Turinys();if(Veiksmas==5||Veiksmas==6){unsigned 이전=단추들;Terminalas_rodyklė(Veiksmas==5?8:16,0,0);단추들=이전;}return 1;
}
