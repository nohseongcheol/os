#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* savs 네 Logs 합성과 UTF-8 Terminālis. 바뀐 영역의 Pabeigti_VALUE 그림만 표시한다. */
#include <stdint.h>
#include <stddef.h>
typedef uintptr_t mašīna_Word;
extern mašīna_Word Panelis_attēla_elements(mašīna_Word,mašīna_Word,mašīna_Word),보드화면기억공간(void);
extern void *memset(void *,int,size_t);
extern const unsigned char Terminālis_fonts[];
#define 최대열수 237
#define Vēsture_līnija_COUNT 160
typedef struct {
    uint32_t 글자칸들[Vēsture_līnija_COUNT][최대열수]; uint8_t 모양들[Vēsture_līnija_COUNT][최대열수];
    unsigned 너비,높이,COLUMNS,ROW_COUNT,크기바뀜;
    unsigned 살아있음,x_koordināta,세로좌표,ROW_amats,COLUMN_amats,맨위,밀어올리기,전경색,배경색,탈출상태,parametrs_VALUE[4],parametrs_INDEX,저장행,저장열;
    unsigned 부호없는결과,긴부호없는값,SMALL_VALUE,대체화면,가리개보임;
} Terminālis_d413d4bc;
static Terminālis_d413d4bc Windows_Saraksts[4];
static int Fokuss=-1,ražojums,secība_VALUE[4],ievade_COUNT,vilkt_VALUE=-1,vilkt_X,vilkt_Y;
static unsigned informācijas_tehnoloģija_gaida,단추들,dators_Skats,한글입력;
static const uint32_t 색상들[16]={0x201a15,0x6060df,0x9dcc86,0x80cfea,0xefaf72,0xca96c9,0xceda76,0xede9df,0x858078,0x8888ff,0xb9eba7,0xa5eaff,0xffcc99,0xf0bef1,0xf0f0a0,0xffffff};
extern int 화면보임(int),화면가리킴(int,unsigned,int,int);
extern void 화면다시그림(int);
static Terminālis_d413d4bc *Terminālis_ievade;
static unsigned paplašināta_rakstzīme(unsigned koda_punkts){return koda_punkts>=256?2:1;}
static void 사각영역(unsigned x_koordināta,unsigned 세로좌표,unsigned 너비값,unsigned 높이값,unsigned 색상){
    Panelis_taisnstūris_aizpildīt(x_koordināta,세로좌표,너비값,높이값,색상);
}
void Terminālis_glifs(unsigned x_koordināta,unsigned 세로좌표,unsigned koda_punkts,unsigned 전경색,unsigned 배경색){
    unsigned 너비=paplašināta_rakstzīme(koda_punkts)*8;if(koda_punkts==0xffffffffu)return;
    int 왼쪽=x_koordināta,위쪽=세로좌표,폭=너비,길이=16;
    if(!보드그림범위(&왼쪽,&위쪽,&폭,&길이))return;
    if(koda_punkts==' '){Panelis_taisnstūris_aizpildīt(왼쪽,위쪽,폭,길이,배경색);return;}
    unsigned LOOKUP_INDEX=koda_punkts<65536?koda_punkts:koda_punkts>=0x1f600&&koda_punkts<0x1f650?65536+koda_punkts-0x1f600:0xfffd;
    const unsigned char *fonts_VALUE=Terminālis_fonts+LOOKUP_INDEX*32;
    for(int Līniju=위쪽;Līniju<위쪽+길이;Līniju++){unsigned Background_Intelligent_Transfer_Service_Saraksts=fonts_VALUE[(Līniju-세로좌표)*2]*256+fonts_VALUE[(Līniju-세로좌표)*2+1];for(int 칸=왼쪽;칸<왼쪽+폭;칸++)Panelis_attēla_elements(칸,Līniju,(Background_Intelligent_Transfer_Service_Saraksts&(0x8000>>(칸-x_koordināta)))?전경색:배경색);}
}
static void nosaukums_tabula(unsigned x_koordināta,unsigned 세로좌표,const char *virkne_dati,unsigned 전경색,unsigned 배경색){while(*virkne_dati){unsigned koda_punkts=(unsigned char)*virkne_dati++, 남은수=0;if(koda_punkts>=0xc0){남은수=koda_punkts<0xe0?1:koda_punkts<0xf0?2:3;koda_punkts&=(1u<<(6-남은수))-1;while(남은수--&&*virkne_dati)koda_punkts=(koda_punkts<<6)|((unsigned char)*virkne_dati++&63);}Terminālis_glifs(x_koordināta,세로좌표,koda_punkts,전경색,배경색);x_koordināta+=paplašināta_rakstzīme(koda_punkts)*8;}}
static unsigned 첫항목(void){return Terminālis_ievade->맨위;}
static int 보이는지(void){return Terminālis_ievade->살아있음&&Fokuss>=0&&Terminālis_ievade==&Windows_Saraksts[Fokuss]&&!화면보임(Fokuss);}
static void 그리기(unsigned ROW_amats,unsigned COLUMN_amats){
    if(!보이는지()||ROW_amats<첫항목()-Terminālis_ievade->밀어올리기||ROW_amats>=첫항목()-Terminālis_ievade->밀어올리기+Terminālis_ievade->ROW_COUNT||COLUMN_amats>=Terminālis_ievade->COLUMNS)return;
    unsigned koda_punkts=Terminālis_ievade->글자칸들[ROW_amats%Vēsture_līnija_COUNT][COLUMN_amats],virkne_dati=Terminālis_ievade->모양들[ROW_amats%Vēsture_līnija_COUNT][COLUMN_amats];
    if(paplašināta_rakstzīme(koda_punkts)==2&&COLUMN_amats+1>=Terminālis_ievade->COLUMNS)koda_punkts=' ';
    Terminālis_glifs(Terminālis_ievade->x_koordināta+12+COLUMN_amats*8,Terminālis_ievade->세로좌표+36+(ROW_amats-첫항목()+Terminālis_ievade->밀어올리기)*16,koda_punkts?koda_punkts:' ',색상들[virkne_dati&15],색상들[virkne_dati>>4]);
}
static void jumtiņš_VALUE(int rādīt_logs){if(!보이는지()||Terminālis_ievade->밀어올리기||Terminālis_ievade->COLUMN_amats>=Terminālis_ievade->COLUMNS||Terminālis_ievade->ROW_amats<Terminālis_ievade->맨위||Terminālis_ievade->ROW_amats>=Terminālis_ievade->맨위+Terminālis_ievade->ROW_COUNT)return;
    if(!rādīt_logs||!Terminālis_ievade->가리개보임)그리기(Terminālis_ievade->ROW_amats,Terminālis_ievade->COLUMN_amats);else 사각영역(Terminālis_ievade->x_koordināta+12+Terminālis_ievade->COLUMN_amats*8,Terminālis_ievade->세로좌표+36+(Terminālis_ievade->ROW_amats-Terminālis_ievade->맨위)*16+14,8,2,색상들[Terminālis_ievade->전경색]);}
static void Saturs_VALUE(void){
    사각영역(Terminālis_ievade->x_koordināta+12,Terminālis_ievade->세로좌표+36,Terminālis_ievade->COLUMNS*8,Terminālis_ievade->ROW_COUNT*16,색상들[0]);
    int 가로=Terminālis_ievade->x_koordināta+12,vertikāle_amats=Terminālis_ievade->세로좌표+36,폭=Terminālis_ievade->COLUMNS*8,길이=Terminālis_ievade->ROW_COUNT*16;
    if(보드그림범위(&가로,&vertikāle_amats,&폭,&길이)){
    unsigned 첫줄=(vertikāle_amats-Terminālis_ievade->세로좌표-36)/16,끝줄=(vertikāle_amats+길이-Terminālis_ievade->세로좌표-36+15)/16;
    unsigned 첫칸=(가로-Terminālis_ievade->x_koordināta-12)/8,끝칸=(가로+폭-Terminālis_ievade->x_koordināta-12+7)/8;
    if(첫칸)첫칸--; /* 잘림 경계 왼쪽에서 시작한 두 칸 글자도 그린다. */
    for(unsigned 반환값=첫줄;반환값<끝줄;반환값++)for(unsigned koda_punkts=첫칸;koda_punkts<끝칸;koda_punkts++){
        unsigned ROW_amats=첫항목()-Terminālis_ievade->밀어올리기+반환값,rakstzīme_VALUE=Terminālis_ievade->글자칸들[ROW_amats%Vēsture_līnija_COUNT][koda_punkts],virkne_dati=Terminālis_ievade->모양들[ROW_amats%Vēsture_līnija_COUNT][koda_punkts];
        if(paplašināta_rakstzīme(rakstzīme_VALUE)==2&&koda_punkts+1>=Terminālis_ievade->COLUMNS)rakstzīme_VALUE=' ';
        if((rakstzīme_VALUE==0||rakstzīme_VALUE==' ')&&(virkne_dati>>4)==0)continue;
        Terminālis_glifs(Terminālis_ievade->x_koordināta+12+koda_punkts*8,Terminālis_ievade->세로좌표+36+반환값*16,rakstzīme_VALUE?rakstzīme_VALUE:' ',색상들[virkne_dati&15],색상들[virkne_dati>>4]);
    }}
    nosaukums_tabula(Terminālis_ievade->x_koordināta+12,Terminālis_ievade->세로좌표+Terminālis_ievade->높이-18,Terminālis_ievade->밀어올리기?"PgDn: recent output":Terminālis_ievade->너비>=500?"F6: next | Corner + left drag: resize":"Corner + left drag: resize",0xece8e2,0x403127);jumtiņš_VALUE(1);
}
static void 실행틀(int identifikators_VALUE){
    Terminālis_ievade=&Windows_Saraksts[identifikators_VALUE];
    int 가로=Terminālis_ievade->x_koordināta,vertikāle_amats=Terminālis_ievade->세로좌표,폭=Terminālis_ievade->너비,길이=Terminālis_ievade->높이;
    if(!보드그림범위(&가로,&vertikāle_amats,&폭,&길이))return;
    사각영역(Terminālis_ievade->x_koordināta,Terminālis_ievade->세로좌표,Terminālis_ievade->너비,Terminālis_ievade->높이,0x403127);
    unsigned 색상=identifikators_VALUE==Fokuss?0x905020:0x604438;사각영역(Terminālis_ievade->x_koordināta,Terminālis_ievade->세로좌표,Terminālis_ievade->너비,30,색상);
    nosaukums_tabula(Terminālis_ievade->x_koordināta+12,Terminālis_ievade->세로좌표+7,"JKOROS Terminal",0xffffff,색상);
    char 수치[2]={(char)('1'+identifikators_VALUE),0};nosaukums_tabula(Terminālis_ievade->x_koordināta+148,Terminālis_ievade->세로좌표+7,수치,0xffffff,색상);
    nosaukums_tabula(Terminālis_ievade->x_koordināta+240,Terminālis_ievade->세로좌표+7,Terminālis_ievade->너비>=500?(한글입력?"[LV] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[LV]":"[EN]"),0xffffff,색상);
    사각영역(Terminālis_ievade->x_koordināta+Terminālis_ievade->너비-32,Terminālis_ievade->세로좌표+4,26,22,0x5555b8);nosaukums_tabula(Terminālis_ievade->x_koordināta+Terminālis_ievade->너비-24,Terminālis_ievade->세로좌표+7,"X",0xffffff,0x5555b8);
    Saturs_VALUE();
}
static void zīmēt_aina(void){
    if(!dators_Skats)return;사각영역(0,0,보드화면너비(),보드화면높이(),0x302018);사각영역(0,0,보드화면너비(),32,0x403127);
    사각영역(6,4,136,24,0x905020);nosaukums_tabula(14,8,"+ New terminal",0xffffff,0x905020);
    for(int 순번=0;순번<4;순번++)if(Windows_Saraksts[순번].살아있음){unsigned koda_punkts=Fokuss==순번?0x905020:0x604438;사각영역(154+순번*112,4,106,24,koda_punkts);nosaukums_tabula(160+순번*112,8,"Terminal",0xffffff,koda_punkts);char virkne_dati[2]={(char)('1'+순번),0};nosaukums_tabula(232+순번*112,8,virkne_dati,0xffffff,koda_punkts);}
    if(!ievade_COUNT)nosaukums_tabula(140,210,"Click + New terminal to start",0xede9df,0x302018);
    for(int 순번=0;순번<ievade_COUNT;순번++)실행틀(secība_VALUE[순번]);화면다시그림(Fokuss);Terminālis_ievade=&Windows_Saraksts[ražojums];
}
static void Molberts_reģions(int 가로,int vertikāle_amats,int 폭,int 길이){
    if(!dators_Skats||!보드그림범위(&가로,&vertikāle_amats,&폭,&길이))return;
    for(int Līniju=vertikāle_amats;Līniju<vertikāle_amats+길이;Līniju+=32){
        int 띠높이=vertikāle_amats+길이-Līniju;if(띠높이>32)띠높이=32;
        if(Panelis_Sākt_zīmējums(가로,Līniju,폭,띠높이)){zīmēt_aina();Panelis_beigas_zīmējums();}
    }
}
static void 다시그리기(void){Molberts_reģions(0,0,보드화면너비(),보드화면높이());}
/* 서로 겹치지 않는 새 Logs 영역과 이전 자리의 네 띠를 복구한다. */
static void 창자리그리기(int 가로,int vertikāle_amats,int 폭,int 길이,Terminālis_d413d4bc *Logs){
    int 왼쪽=가로>(int)Logs->x_koordināta?가로:(int)Logs->x_koordināta;
    int 위쪽=vertikāle_amats>(int)Logs->세로좌표?vertikāle_amats:(int)Logs->세로좌표;
    int RIGHT=가로+폭<(int)(Logs->x_koordināta+Logs->너비)?가로+폭:(int)(Logs->x_koordināta+Logs->너비);
    int 아래쪽=vertikāle_amats+길이<(int)(Logs->세로좌표+Logs->높이)?vertikāle_amats+길이:(int)(Logs->세로좌표+Logs->높이);
    Molberts_reģions(Logs->x_koordināta,Logs->세로좌표,Logs->너비,Logs->높이);
    if(왼쪽>=RIGHT||위쪽>=아래쪽){Molberts_reģions(가로,vertikāle_amats,폭,길이);return;}
    Molberts_reģions(가로,vertikāle_amats,폭,위쪽-vertikāle_amats);
    Molberts_reģions(가로,아래쪽,폭,vertikāle_amats+길이-아래쪽);
    Molberts_reģions(가로,위쪽,왼쪽-가로,아래쪽-위쪽);
    Molberts_reģions(RIGHT,위쪽,가로+폭-RIGHT,아래쪽-위쪽);
}
static void signāls_Fokuss(void){informācijas_tehnoloģija_gaida=(informācijas_tehnoloģija_gaida&~15u)|(unsigned)(Fokuss+1)|0x10000;}
void 터미널입력방식(unsigned 한글여부){
    한글입력=한글여부!=0;
    /* Update title bars only: a mode switch must not erase an EL0 drawing. */
    if(Fokuss>=0){
        Terminālis_d413d4bc *logs_ievade=&Windows_Saraksts[Fokuss];
        nosaukums_tabula(logs_ievade->x_koordināta+240,logs_ievade->세로좌표+7,logs_ievade->너비>=500?(한글입력?"[LV] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[LV]":"[EN]"),0xffffff,0x905020);
    }
}
static void 앞으로올리기(int identifikators_VALUE){if(identifikators_VALUE<0||identifikators_VALUE>=4||!Windows_Saraksts[identifikators_VALUE].살아있음)return;int pašreizējais_amats=0;while(pašreizējais_amats<ievade_COUNT&&secība_VALUE[pašreizējais_amats]!=identifikators_VALUE)pašreizējais_amats++;for(;pašreizējais_amats+1<ievade_COUNT;pašreizējais_amats++)secība_VALUE[pašreizējais_amats]=secība_VALUE[pašreizējais_amats+1];secība_VALUE[ievade_COUNT-1]=identifikators_VALUE;Fokuss=identifikators_VALUE;signāls_Fokuss();다시그리기();}
static void 빈칸채우기(unsigned ROW_amats){for(unsigned koda_punkts=0;koda_punkts<최대열수;koda_punkts++){Terminālis_ievade->글자칸들[ROW_amats%Vēsture_līnija_COUNT][koda_punkts]=0;Terminālis_ievade->모양들[ROW_amats%Vēsture_līnija_COUNT][koda_punkts]=Terminālis_ievade->전경색|(Terminālis_ievade->배경색<<4);}}
static void nodzēst_Satura_rādītājs(void){Terminālis_ievade->ROW_amats=Terminālis_ievade->COLUMN_amats=Terminālis_ievade->맨위=Terminālis_ievade->밀어올리기=0;for(unsigned 반환값=0;반환값<Vēsture_līnija_COUNT;반환값++)빈칸채우기(반환값);if(보이는지())Saturs_VALUE();}
static int atvērt_ievade(void){
    if(!보드화면기억공간())return -19;int identifikators_VALUE=0;while(identifikators_VALUE<4&&Windows_Saraksts[identifikators_VALUE].살아있음)identifikators_VALUE++;if(identifikators_VALUE==4)return -28;
    dators_Skats=1;Terminālis_ievade=&Windows_Saraksts[identifikators_VALUE];memset(Terminālis_ievade,0,sizeof(*Terminālis_ievade));Terminālis_ievade->살아있음=1;Terminālis_ievade->너비=568;Terminālis_ievade->높이=360;Terminālis_ievade->COLUMNS=68;Terminālis_ievade->ROW_COUNT=19;Terminālis_ievade->x_koordināta=12+identifikators_VALUE*16;Terminālis_ievade->세로좌표=48+identifikators_VALUE*18;Terminālis_ievade->전경색=7;Terminālis_ievade->가리개보임=1;
    for(unsigned 반환값=0;반환값<Vēsture_līnija_COUNT;반환값++)빈칸채우기(반환값);secība_VALUE[ievade_COUNT++]=identifikators_VALUE;Fokuss=identifikators_VALUE;informācijas_tehnoloģija_gaida|=1u<<(4+identifikators_VALUE);signāls_Fokuss();다시그리기();return identifikators_VALUE+1;
}
static void Aizvērt_logs(int identifikators_VALUE){
    if(identifikators_VALUE<0||identifikators_VALUE>=4||!Windows_Saraksts[identifikators_VALUE].살아있음)return;Windows_Saraksts[identifikators_VALUE].살아있음=0;informācijas_tehnoloģija_gaida|=1u<<(8+identifikators_VALUE);
    int pašreizējais_amats=0;while(pašreizējais_amats<ievade_COUNT&&secība_VALUE[pašreizējais_amats]!=identifikators_VALUE)pašreizējais_amats++;for(;pašreizējais_amats+1<ievade_COUNT;pašreizējais_amats++)secība_VALUE[pašreizējais_amats]=secība_VALUE[pašreizējais_amats+1];ievade_COUNT--;
    if(Fokuss==identifikators_VALUE)Fokuss=ievade_COUNT?secība_VALUE[ievade_COUNT-1]:-1;signāls_Fokuss();다시그리기();
}
static void 줄바꿈(void){Terminālis_ievade->COLUMN_amats=0;Terminālis_ievade->ROW_amats++;if(Terminālis_ievade->ROW_amats>=Terminālis_ievade->맨위+Terminālis_ievade->ROW_COUNT){Terminālis_ievade->맨위++;빈칸채우기(Terminālis_ievade->ROW_amats);if(보이는지())Saturs_VALUE();}}
static void koda_punkts_451f2815(unsigned koda_punkts){
    if(koda_punkts==13){Terminālis_ievade->COLUMN_amats=0;return;}if(koda_punkts==10){줄바꿈();return;}if(koda_punkts==8){if(Terminālis_ievade->COLUMN_amats)Terminālis_ievade->COLUMN_amats--;return;}
    if(koda_punkts==9){unsigned krājums_COUNT=8-Terminālis_ievade->COLUMN_amats%8;while(krājums_COUNT--)koda_punkts_451f2815(' ');return;}if(koda_punkts<32||koda_punkts==127)return;
    unsigned 너비값=paplašināta_rakstzīme(koda_punkts);if(Terminālis_ievade->COLUMN_amats+너비값>Terminālis_ievade->COLUMNS)줄바꿈();
    if(Terminālis_ievade->글자칸들[Terminālis_ievade->ROW_amats%Vēsture_līnija_COUNT][Terminālis_ievade->COLUMN_amats]==0xffffffffu&&Terminālis_ievade->COLUMN_amats){Terminālis_ievade->글자칸들[Terminālis_ievade->ROW_amats%Vēsture_līnija_COUNT][Terminālis_ievade->COLUMN_amats-1]=' ';그리기(Terminālis_ievade->ROW_amats,Terminālis_ievade->COLUMN_amats-1);}
    if(paplašināta_rakstzīme(Terminālis_ievade->글자칸들[Terminālis_ievade->ROW_amats%Vēsture_līnija_COUNT][Terminālis_ievade->COLUMN_amats])==2&&Terminālis_ievade->COLUMN_amats+1<Terminālis_ievade->COLUMNS){Terminālis_ievade->글자칸들[Terminālis_ievade->ROW_amats%Vēsture_līnija_COUNT][Terminālis_ievade->COLUMN_amats+1]=' ';그리기(Terminālis_ievade->ROW_amats,Terminālis_ievade->COLUMN_amats+1);}
    Terminālis_ievade->글자칸들[Terminālis_ievade->ROW_amats%Vēsture_līnija_COUNT][Terminālis_ievade->COLUMN_amats]=koda_punkts;Terminālis_ievade->모양들[Terminālis_ievade->ROW_amats%Vēsture_līnija_COUNT][Terminālis_ievade->COLUMN_amats]=Terminālis_ievade->전경색|(Terminālis_ievade->배경색<<4);
    if(너비값==2)Terminālis_ievade->글자칸들[Terminālis_ievade->ROW_amats%Vēsture_līnija_COUNT][Terminālis_ievade->COLUMN_amats+1]=0xffffffffu;
    그리기(Terminālis_ievade->ROW_amats,Terminālis_ievade->COLUMN_amats);Terminālis_ievade->COLUMN_amats+=너비값;
}
static void turis_vadība_SEQUENCE(unsigned koda_punkts){
    unsigned krājums_COUNT=Terminālis_ievade->parametrs_VALUE[0]?Terminālis_ievade->parametrs_VALUE[0]:1;
    if(koda_punkts=='m')for(unsigned 순번=0;순번<=Terminālis_ievade->parametrs_INDEX;순번++){unsigned dati_amats=Terminālis_ievade->parametrs_VALUE[순번];if(!dati_amats){Terminālis_ievade->전경색=7;Terminālis_ievade->배경색=0;}if(dati_amats==1&&Terminālis_ievade->전경색<8)Terminālis_ievade->전경색+=8;if(dati_amats==7){unsigned 유지=Terminālis_ievade->전경색;Terminālis_ievade->전경색=Terminālis_ievade->배경색;Terminālis_ievade->배경색=유지;}if(dati_amats>=30&&dati_amats<=37)Terminālis_ievade->전경색=dati_amats-30;if(dati_amats>=90&&dati_amats<=97)Terminālis_ievade->전경색=dati_amats-90+8;if(dati_amats>=40&&dati_amats<=47)Terminālis_ievade->배경색=dati_amats-40;if(dati_amats>=100&&dati_amats<=107)Terminālis_ievade->배경색=dati_amats-100+8;if(dati_amats==39)Terminālis_ievade->전경색=7;if(dati_amats==49)Terminālis_ievade->배경색=0;}
    if(koda_punkts=='J'&&(Terminālis_ievade->parametrs_VALUE[0]==2||Terminālis_ievade->parametrs_VALUE[0]==3))nodzēst_Satura_rādītājs();
    if(koda_punkts=='K'){unsigned 출발위치=Terminālis_ievade->parametrs_VALUE[0]==2?0:Terminālis_ievade->COLUMN_amats,도착위치=Terminālis_ievade->parametrs_VALUE[0]==1?Terminālis_ievade->COLUMN_amats+1:Terminālis_ievade->COLUMNS;if(Terminālis_ievade->parametrs_VALUE[0]==1)출발위치=0;for(unsigned 순번=출발위치;순번<도착위치&&순번<Terminālis_ievade->COLUMNS;순번++){
        unsigned ROW_VALUE=Terminālis_ievade->ROW_amats%Vēsture_līnija_COUNT,rakstzīme_VALUE=Terminālis_ievade->글자칸들[ROW_VALUE][순번],forma_VALUE=Terminālis_ievade->전경색|(Terminālis_ievade->배경색<<4);
        /* 넓은 vi 화면에서도 이미 빈 칸의 fonts_VALUE 화소를 되풀이해 칠하지 않는다. */
        int 바뀜=(rakstzīme_VALUE!=0&&rakstzīme_VALUE!=' ')||Terminālis_ievade->모양들[ROW_VALUE][순번]!=forma_VALUE;
        Terminālis_ievade->글자칸들[ROW_VALUE][순번]=' ';Terminālis_ievade->모양들[ROW_VALUE][순번]=forma_VALUE;
        if(바뀜)그리기(Terminālis_ievade->ROW_amats,순번);
    }}
    if(koda_punkts=='D')Terminālis_ievade->COLUMN_amats=krājums_COUNT>Terminālis_ievade->COLUMN_amats?0:Terminālis_ievade->COLUMN_amats-krājums_COUNT;if(koda_punkts=='C')Terminālis_ievade->COLUMN_amats=Terminālis_ievade->COLUMN_amats+krājums_COUNT>=Terminālis_ievade->COLUMNS?Terminālis_ievade->COLUMNS-1:Terminālis_ievade->COLUMN_amats+krājums_COUNT;
    if(koda_punkts=='G')Terminālis_ievade->COLUMN_amats=krājums_COUNT>Terminālis_ievade->COLUMNS?Terminālis_ievade->COLUMNS-1:krājums_COUNT-1;if(koda_punkts=='A')Terminālis_ievade->ROW_amats=krājums_COUNT>Terminālis_ievade->ROW_amats-Terminālis_ievade->맨위?Terminālis_ievade->맨위:Terminālis_ievade->ROW_amats-krājums_COUNT;
    if(koda_punkts=='B')Terminālis_ievade->ROW_amats=Terminālis_ievade->ROW_amats+krājums_COUNT>=Terminālis_ievade->맨위+Terminālis_ievade->ROW_COUNT?Terminālis_ievade->맨위+Terminālis_ievade->ROW_COUNT-1:Terminālis_ievade->ROW_amats+krājums_COUNT;
    if(koda_punkts=='H'||koda_punkts=='f'){Terminālis_ievade->ROW_amats=Terminālis_ievade->맨위+(krājums_COUNT>Terminālis_ievade->ROW_COUNT?Terminālis_ievade->ROW_COUNT:krājums_COUNT)-1;unsigned x_koordināta=Terminālis_ievade->parametrs_VALUE[1]?Terminālis_ievade->parametrs_VALUE[1]:1;Terminālis_ievade->COLUMN_amats=(x_koordināta>Terminālis_ievade->COLUMNS?Terminālis_ievade->COLUMNS:x_koordināta)-1;}
    if(koda_punkts=='s'){Terminālis_ievade->저장행=Terminālis_ievade->ROW_amats;Terminālis_ievade->저장열=Terminālis_ievade->COLUMN_amats;}if(koda_punkts=='u'){Terminālis_ievade->ROW_amats=Terminālis_ievade->저장행;Terminālis_ievade->COLUMN_amats=Terminālis_ievade->저장열<Terminālis_ievade->COLUMNS?Terminālis_ievade->저장열:Terminālis_ievade->COLUMNS-1;}
    if((koda_punkts=='h'||koda_punkts=='l')&&Terminālis_ievade->parametrs_VALUE[0]==25)Terminālis_ievade->가리개보임=koda_punkts=='h';
}
void Terminālis_byte(unsigned SECOND_VALUE){
    Terminālis_ievade=&Windows_Saraksts[ražojums];if(!Terminālis_ievade->살아있음)return;jumtiņš_VALUE(0);if(Terminālis_ievade->밀어올리기){Terminālis_ievade->밀어올리기=0;if(보이는지())Saturs_VALUE();}
    if(Terminālis_ievade->탈출상태==1){Terminālis_ievade->탈출상태=SECOND_VALUE=='['?2:0;Terminālis_ievade->parametrs_INDEX=0;for(unsigned 순번=0;순번<4;순번++)Terminālis_ievade->parametrs_VALUE[순번]=0;}
    else if(Terminālis_ievade->탈출상태==2){if(SECOND_VALUE=='?'){}else if(SECOND_VALUE>='0'&&SECOND_VALUE<='9'){if(Terminālis_ievade->parametrs_VALUE[Terminālis_ievade->parametrs_INDEX]<10000)Terminālis_ievade->parametrs_VALUE[Terminālis_ievade->parametrs_INDEX]=Terminālis_ievade->parametrs_VALUE[Terminālis_ievade->parametrs_INDEX]*10+SECOND_VALUE-'0';}else if(SECOND_VALUE==';'&&Terminālis_ievade->parametrs_INDEX<3)Terminālis_ievade->parametrs_INDEX++;else{turis_vadība_SEQUENCE(SECOND_VALUE);Terminālis_ievade->탈출상태=0;}}
    else if(SECOND_VALUE==27){Terminālis_ievade->긴부호없는값=0;Terminālis_ievade->탈출상태=1;}else{
        if(Terminālis_ievade->긴부호없는값&&(SECOND_VALUE&0xc0)!=0x80){Terminālis_ievade->긴부호없는값=0;koda_punkts_451f2815(0xfffd);}
        if(Terminālis_ievade->긴부호없는값){Terminālis_ievade->부호없는결과=Terminālis_ievade->부호없는결과*64+(SECOND_VALUE&63);if(--Terminālis_ievade->긴부호없는값==0)koda_punkts_451f2815(Terminālis_ievade->부호없는결과<Terminālis_ievade->SMALL_VALUE||Terminālis_ievade->부호없는결과>0x10ffff||(Terminālis_ievade->부호없는결과>=0xd800&&Terminālis_ievade->부호없는결과<=0xdfff)?0xfffd:Terminālis_ievade->부호없는결과);}
        else if(SECOND_VALUE<128)koda_punkts_451f2815(SECOND_VALUE);else if(SECOND_VALUE>=0xc2&&SECOND_VALUE<=0xf4){Terminālis_ievade->긴부호없는값=SECOND_VALUE<0xe0?1:SECOND_VALUE<0xf0?2:3;Terminālis_ievade->부호없는결과=SECOND_VALUE&((1u<<(6-Terminālis_ievade->긴부호없는값))-1);Terminālis_ievade->SMALL_VALUE=Terminālis_ievade->긴부호없는값==1?128:Terminālis_ievade->긴부호없는값==2?2048:65536;}else koda_punkts_451f2815(0xfffd);
    }jumtiņš_VALUE(1);
}
int Terminālis_gaida(void){return informācijas_tehnoloģija_gaida!=0;}
/* 모서리 INDEX: 1 좌상, 2 우상, 3 좌하, 4 우하. */
static int mainīt_izmērus_vilkt=-1,잡은모서리,잡은가로,잡은세로,처음가로,처음세로,처음너비,처음높이;
static int 가리킨창(int 가로,int vertikāle_amats) {
    for(int SEQUENCE_VALUE=ievade_COUNT-1;SEQUENCE_VALUE>=0;SEQUENCE_VALUE--){
        int identifikators_VALUE=secība_VALUE[SEQUENCE_VALUE];Terminālis_d413d4bc *Logs=&Windows_Saraksts[identifikators_VALUE];
        if(가로>=(int)Logs->x_koordināta&&vertikāle_amats>=(int)Logs->세로좌표&&
           가로<(int)(Logs->x_koordināta+Logs->너비)&&vertikāle_amats<(int)(Logs->세로좌표+Logs->높이))return identifikators_VALUE;
    }return -1;
}
static int 모서리찾기(int identifikators_VALUE,int 가로,int vertikāle_amats) {
    if(identifikators_VALUE<0)return 0;Terminālis_d413d4bc *Logs=&Windows_Saraksts[identifikators_VALUE];
    int 왼쪽=가로<(int)Logs->x_koordināta+8,RIGHT=가로>=(int)(Logs->x_koordināta+Logs->너비)-8;
    int 위쪽=vertikāle_amats<(int)Logs->세로좌표+8,아래쪽=vertikāle_amats>=(int)(Logs->세로좌표+Logs->높이)-8;
    return (왼쪽||RIGHT)&&(위쪽||아래쪽)?1+RIGHT+아래쪽*2:0;
}
static int atdalītājs_VALUE(int VALUE,int 최소,int 최대){return VALUE<최소?최소:VALUE>최대?최대:VALUE;}
static void pārvietot_mainīt_izmērus(int 가로,int vertikāle_amats) {
    Terminālis_d413d4bc *Logs=&Windows_Saraksts[mainīt_izmērus_vilkt];int 왼쪽=처음가로,위쪽=처음세로,RIGHT=처음가로+처음너비,아래쪽=처음세로+처음높이;
    if(잡은모서리==1||잡은모서리==3)왼쪽=atdalītājs_VALUE(처음가로+가로-잡은가로,0,RIGHT-360);
    else RIGHT=atdalītājs_VALUE(처음가로+처음너비+가로-잡은가로,왼쪽+360,보드화면너비());
    if(잡은모서리<=2)위쪽=atdalītājs_VALUE(처음세로+vertikāle_amats-잡은세로,34,아래쪽-216);
    else 아래쪽=atdalītājs_VALUE(처음세로+처음높이+vertikāle_amats-잡은세로,위쪽+216,보드화면높이());
    unsigned COLUMNS=(RIGHT-왼쪽-24)/8,ROW_COUNT=(아래쪽-위쪽-56)/16;
    if(Logs->COLUMNS!=COLUMNS||Logs->ROW_COUNT!=ROW_COUNT){
        Logs->크기바뀜=1;Logs->COLUMNS=COLUMNS;Logs->ROW_COUNT=ROW_COUNT;
        if(Logs->COLUMN_amats>=COLUMNS)Logs->COLUMN_amats=COLUMNS-1;
        if(Logs->ROW_amats>=Logs->맨위+ROW_COUNT)Logs->맨위=Logs->ROW_amats-ROW_COUNT+1;
        unsigned 한도=Logs->맨위;if(한도>Vēsture_līnija_COUNT-ROW_COUNT)한도=Vēsture_līnija_COUNT-ROW_COUNT;
        if(Logs->밀어올리기>한도)Logs->밀어올리기=한도;
    }
    int 옛가로=Logs->x_koordināta,옛세로=Logs->세로좌표,옛폭=Logs->너비,옛길이=Logs->높이;
    if(옛가로==왼쪽&&옛세로==위쪽&&옛폭==RIGHT-왼쪽&&옛길이==아래쪽-위쪽)return;
    Logs->x_koordināta=왼쪽;Logs->세로좌표=위쪽;Logs->너비=RIGHT-왼쪽;Logs->높이=아래쪽-위쪽;
    창자리그리기(옛가로,옛세로,옛폭,옛길이,Logs);
}
void Terminālis_rādītājs(unsigned Tālāk_krājums,int x_koordināta,int 세로좌표){
    unsigned 눌림=Tālāk_krājums&~단추들;단추들=Tālāk_krājums;
    if(!dators_Skats){vilkt_VALUE=-1;mainīt_izmērus_vilkt=-1;Panelis_rādītājs(x_koordināta,세로좌표,1);return;}
    if(!(Tālāk_krājums&1)){vilkt_VALUE=-1;mainīt_izmērus_vilkt=-1;}
    if(mainīt_izmērus_vilkt>=0&&!Windows_Saraksts[mainīt_izmērus_vilkt].살아있음)mainīt_izmērus_vilkt=-1;
    if(vilkt_VALUE>=0&&!Windows_Saraksts[vilkt_VALUE].살아있음)vilkt_VALUE=-1;
    if(mainīt_izmērus_vilkt>=0){
        pārvietot_mainīt_izmērus(x_koordināta,세로좌표);Panelis_rādītājs(x_koordināta,세로좌표,잡은모서리==1||잡은모서리==4?2:3);return;
    }
    Panelis_rādītājs(x_koordināta,세로좌표,1);
    if(vilkt_VALUE>=0){
        Terminālis_d413d4bc *Logs=&Windows_Saraksts[vilkt_VALUE];
        int 옛가로=Logs->x_koordināta,옛세로=Logs->세로좌표;
        Logs->x_koordināta=atdalītājs_VALUE(x_koordināta-vilkt_X,0,보드화면너비()-Logs->너비);
        Logs->세로좌표=atdalītājs_VALUE(세로좌표-vilkt_Y,34,보드화면높이()-Logs->높이);
        if(옛가로!=(int)Logs->x_koordināta||옛세로!=(int)Logs->세로좌표)창자리그리기(옛가로,옛세로,Logs->너비,Logs->높이,Logs);
        return;
    }
    extern int 화면덮음(int,int,int);
    if(화면덮음(Fokuss,x_koordināta,세로좌표)){화면가리킴(Fokuss,눌림,x_koordināta,세로좌표);return;}
    int identifikators_VALUE=가리킨창(x_koordināta,세로좌표),모서리=모서리찾기(identifikators_VALUE,x_koordināta,세로좌표);
    if(모서리)Panelis_rādītājs(x_koordināta,세로좌표,모서리==1||모서리==4?2:3);
    if(눌림&1){
        if(모서리){
            Terminālis_d413d4bc *Logs=&Windows_Saraksts[identifikators_VALUE];mainīt_izmērus_vilkt=identifikators_VALUE;잡은모서리=모서리;잡은가로=x_koordināta;잡은세로=세로좌표;
            처음가로=Logs->x_koordināta;처음세로=Logs->세로좌표;처음너비=Logs->너비;처음높이=Logs->높이;
            if(identifikators_VALUE!=Fokuss)앞으로올리기(identifikators_VALUE);return;
        }
        if(세로좌표<32&&x_koordināta>=6&&x_koordināta<142){atvērt_ievade();return;}
        if(세로좌표<32&&x_koordināta>=154&&x_koordināta<602){앞으로올리기((x_koordināta-154)/112);return;}
        if(identifikators_VALUE>=0){
            Terminālis_d413d4bc *Logs=&Windows_Saraksts[identifikators_VALUE];
            if(세로좌표<(int)Logs->세로좌표+30&&x_koordināta>=(int)(Logs->x_koordināta+Logs->너비)-32){Aizvērt_logs(identifikators_VALUE);return;}
            if(identifikators_VALUE!=Fokuss)앞으로올리기(identifikators_VALUE);
            if(세로좌표<(int)Logs->세로좌표+30){vilkt_VALUE=identifikators_VALUE;vilkt_X=x_koordināta-Logs->x_koordināta;vilkt_Y=세로좌표-Logs->세로좌표;}return;
        }
    }
    if(Fokuss>=0&&(눌림&(8|16))){Terminālis_ievade=&Windows_Saraksts[Fokuss];if(눌림&8){unsigned 한도=Terminālis_ievade->맨위;if(한도>Vēsture_līnija_COUNT-Terminālis_ievade->ROW_COUNT)한도=Vēsture_līnija_COUNT-Terminālis_ievade->ROW_COUNT;Terminālis_ievade->밀어올리기=Terminālis_ievade->밀어올리기+9>한도?한도:Terminālis_ievade->밀어올리기+9;}else Terminālis_ievade->밀어올리기=Terminālis_ievade->밀어올리기<9?0:Terminālis_ievade->밀어올리기-9;다시그리기();}
}
void 터미널바로가기키(unsigned 누름값){if(누름값==1)atvērt_ievade();if(누름값==2&&ievade_COUNT)앞으로올리기(secība_VALUE[0]);if(누름값==3)Aizvērt_logs(Fokuss);}
mašīna_Word Panelis_Terminālis(mašīna_Word Darbība){
    if(Darbība==300){if(!Windows_Saraksts[ražojums].살아있음)return atvērt_ievade();dators_Skats=1;다시그리기();return 0;}
    if(Darbība==0){Aizvērt_logs(Fokuss);return 0;}if(Darbība==1)return (uint32_t)atvērt_ievade();if(Darbība==2)return Fokuss>=0;
    if(Darbība==9){dators_Skats=0;return 0;}if(Darbība==7)return ievade_COUNT;if(Darbība==10)return Fokuss+1;if(Darbība==11)return ražojums;
    if(Darbība==13){Terminālis_d413d4bc *Logs=&Windows_Saraksts[ražojums];return Logs->살아있음?(Logs->ROW_COUNT<<16)|Logs->COLUMNS:(19<<16)|68;}
    if(Darbība==14){unsigned VALUE=Windows_Saraksts[ražojums].크기바뀜;Windows_Saraksts[ražojums].크기바뀜=0;return VALUE;}
    if(Darbība==12){unsigned VALUE=informācijas_tehnoloģija_gaida;informācijas_tehnoloģija_gaida=0;return VALUE;}
    if(Darbība>=20&&Darbība<24)return Windows_Saraksts[Darbība-20].살아있음;
    if(Darbība>=100&&Darbība<104){ražojums=Darbība-100;Terminālis_ievade=&Windows_Saraksts[ražojums];return 0;}
    if(Darbība>=200&&Darbība<204){앞으로올리기(Darbība-200);return 0;}
    if(Darbība==3){다시그리기();return 0;}Terminālis_ievade=&Windows_Saraksts[ražojums];if(!Terminālis_ievade->살아있음)return 0;
    if(Darbība==4)nodzēst_Satura_rādītājs();if(Darbība==5||Darbība==6){unsigned 이전=단추들;Terminālis_rādītājs(Darbība==5?8:16,0,0);단추들=이전;}return 1;
}
