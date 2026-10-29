#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* 자체 네 pəncərə 합성과 UTF-8 Terminal. 바뀐 영역의 완성 그림만 표시한다. */
#include <stdint.h>
#include <stddef.h>
typedef uintptr_t maşın_Söz;
extern maşın_Söz lövhə_piksel(maşın_Söz,maşın_Söz,maşın_Söz),보드화면기억공간(void);
extern void *memset(void *,int,size_t);
extern const unsigned char Terminal_şrift[];
#define 최대열수 237
#define Tarixçə_xətt_COUNT 160
typedef struct {
    uint32_t 글자칸들[Tarixçə_xətt_COUNT][최대열수]; uint8_t 모양들[Tarixçə_xətt_COUNT][최대열수];
    unsigned 너비,높이,COLUMNS,ROW_COUNT,크기바뀜;
    unsigned 살아있음,x_koordinatı,Y_koordinat,ROW_yerinə_qoymaq,sütun_yerinə_qoymaq,맨위,sürüşdürmək,전경색,배경색,탈출상태,매개값[4],매개색인,저장행,저장열;
    unsigned 부호없는결과,긴부호없는값,SMALL_VALUE,대체화면,가리개보임;
} Terminal_d413d4bc;
static Terminal_d413d4bc Windows_Siyahı[4];
static int Fokus=-1,출력결과,ardıcıllıq_VALUE[4],daxiletmə_COUNT,sürükləmək_VALUE=-1,sürükləmək_X,sürükləmək_Y;
static unsigned 대기중,단추들,iş_masası_baxmaq,한글입력;
static const uint32_t 색상들[16]={0x201a15,0x6060df,0x9dcc86,0x80cfea,0xefaf72,0xca96c9,0xceda76,0xede9df,0x858078,0x8888ff,0xb9eba7,0xa5eaff,0xffcc99,0xf0bef1,0xf0f0a0,0xffffff};
extern int 화면보임(int),화면가리킴(int,unsigned,int,int);
extern void 화면다시그림(int);
static Terminal_d413d4bc *Terminal_daxiletmə;
static unsigned 넓은글자(unsigned simvol_kodu){return simvol_kodu>=256?2:1;}
static void 사각영역(unsigned x_koordinatı,unsigned Y_koordinat,unsigned 너비값,unsigned 높이값,unsigned 색상){
    보드사각그림(x_koordinatı,Y_koordinat,너비값,높이값,색상);
}
void Terminal_qlif(unsigned x_koordinatı,unsigned Y_koordinat,unsigned simvol_kodu,unsigned 전경색,unsigned 배경색){
    unsigned 너비=넓은글자(simvol_kodu)*8;if(simvol_kodu==0xffffffffu)return;
    int 왼쪽=x_koordinatı,위쪽=Y_koordinat,폭=너비,uzunluq_VALUE=16;
    if(!보드그림범위(&왼쪽,&위쪽,&폭,&uzunluq_VALUE))return;
    if(simvol_kodu==' '){보드사각그림(왼쪽,위쪽,폭,uzunluq_VALUE,배경색);return;}
    unsigned LOOKUP_INDEX=simvol_kodu<65536?simvol_kodu:simvol_kodu>=0x1f600&&simvol_kodu<0x1f650?65536+simvol_kodu-0x1f600:0xfffd;
    const unsigned char *şrift_VALUE=Terminal_şrift+LOOKUP_INDEX*32;
    for(int Giriş=위쪽;Giriş<위쪽+uzunluq_VALUE;Giriş++){unsigned Fon_Ağıllı_Ötürmə_Xidməti_Siyahı=şrift_VALUE[(Giriş-Y_koordinat)*2]*256+şrift_VALUE[(Giriş-Y_koordinat)*2+1];for(int slot_daxiletmə=왼쪽;slot_daxiletmə<왼쪽+폭;slot_daxiletmə++)lövhə_piksel(slot_daxiletmə,Giriş,(Fon_Ağıllı_Ötürmə_Xidməti_Siyahı&(0x8000>>(slot_daxiletmə-x_koordinatı)))?전경색:배경색);}
}
static void ad_cədvəl(unsigned x_koordinatı,unsigned Y_koordinat,const char *sətir_verilənlər,unsigned 전경색,unsigned 배경색){while(*sətir_verilənlər){unsigned simvol_kodu=(unsigned char)*sətir_verilənlər++, 남은수=0;if(simvol_kodu>=0xc0){남은수=simvol_kodu<0xe0?1:simvol_kodu<0xf0?2:3;simvol_kodu&=(1u<<(6-남은수))-1;while(남은수--&&*sətir_verilənlər)simvol_kodu=(simvol_kodu<<6)|((unsigned char)*sətir_verilənlər++&63);}Terminal_qlif(x_koordinatı,Y_koordinat,simvol_kodu,전경색,배경색);x_koordinatı+=넓은글자(simvol_kodu)*8;}}
static unsigned 첫항목(void){return Terminal_daxiletmə->맨위;}
static int 보이는지(void){return Terminal_daxiletmə->살아있음&&Fokus>=0&&Terminal_daxiletmə==&Windows_Siyahı[Fokus]&&!화면보임(Fokus);}
static void 그리기(unsigned ROW_yerinə_qoymaq,unsigned sütun_yerinə_qoymaq){
    if(!보이는지()||ROW_yerinə_qoymaq<첫항목()-Terminal_daxiletmə->sürüşdürmək||ROW_yerinə_qoymaq>=첫항목()-Terminal_daxiletmə->sürüşdürmək+Terminal_daxiletmə->ROW_COUNT||sütun_yerinə_qoymaq>=Terminal_daxiletmə->COLUMNS)return;
    unsigned simvol_kodu=Terminal_daxiletmə->글자칸들[ROW_yerinə_qoymaq%Tarixçə_xətt_COUNT][sütun_yerinə_qoymaq],sətir_verilənlər=Terminal_daxiletmə->모양들[ROW_yerinə_qoymaq%Tarixçə_xətt_COUNT][sütun_yerinə_qoymaq];
    if(넓은글자(simvol_kodu)==2&&sütun_yerinə_qoymaq+1>=Terminal_daxiletmə->COLUMNS)simvol_kodu=' ';
    Terminal_qlif(Terminal_daxiletmə->x_koordinatı+12+sütun_yerinə_qoymaq*8,Terminal_daxiletmə->Y_koordinat+36+(ROW_yerinə_qoymaq-첫항목()+Terminal_daxiletmə->sürüşdürmək)*16,simvol_kodu?simvol_kodu:' ',색상들[sətir_verilənlər&15],색상들[sətir_verilənlər>>4]);
}
static void daxiletmə_işarəsi_VALUE(int göstərmək_pəncərə){if(!보이는지()||Terminal_daxiletmə->sürüşdürmək||Terminal_daxiletmə->sütun_yerinə_qoymaq>=Terminal_daxiletmə->COLUMNS||Terminal_daxiletmə->ROW_yerinə_qoymaq<Terminal_daxiletmə->맨위||Terminal_daxiletmə->ROW_yerinə_qoymaq>=Terminal_daxiletmə->맨위+Terminal_daxiletmə->ROW_COUNT)return;
    if(!göstərmək_pəncərə||!Terminal_daxiletmə->가리개보임)그리기(Terminal_daxiletmə->ROW_yerinə_qoymaq,Terminal_daxiletmə->sütun_yerinə_qoymaq);else 사각영역(Terminal_daxiletmə->x_koordinatı+12+Terminal_daxiletmə->sütun_yerinə_qoymaq*8,Terminal_daxiletmə->Y_koordinat+36+(Terminal_daxiletmə->ROW_yerinə_qoymaq-Terminal_daxiletmə->맨위)*16+14,8,2,색상들[Terminal_daxiletmə->전경색]);}
static void Məzmun_VALUE(void){
    사각영역(Terminal_daxiletmə->x_koordinatı+12,Terminal_daxiletmə->Y_koordinat+36,Terminal_daxiletmə->COLUMNS*8,Terminal_daxiletmə->ROW_COUNT*16,색상들[0]);
    int 가로=Terminal_daxiletmə->x_koordinatı+12,Şaquli_yerinə_qoymaq=Terminal_daxiletmə->Y_koordinat+36,폭=Terminal_daxiletmə->COLUMNS*8,uzunluq_VALUE=Terminal_daxiletmə->ROW_COUNT*16;
    if(보드그림범위(&가로,&Şaquli_yerinə_qoymaq,&폭,&uzunluq_VALUE)){
    unsigned 첫줄=(Şaquli_yerinə_qoymaq-Terminal_daxiletmə->Y_koordinat-36)/16,끝줄=(Şaquli_yerinə_qoymaq+uzunluq_VALUE-Terminal_daxiletmə->Y_koordinat-36+15)/16;
    unsigned 첫칸=(가로-Terminal_daxiletmə->x_koordinatı-12)/8,끝칸=(가로+폭-Terminal_daxiletmə->x_koordinatı-12+7)/8;
    if(첫칸)첫칸--; /* 잘림 경계 왼쪽에서 시작한 두 slot_daxiletmə 글자도 그린다. */
    for(unsigned 반환값=첫줄;반환값<끝줄;반환값++)for(unsigned simvol_kodu=첫칸;simvol_kodu<끝칸;simvol_kodu++){
        unsigned ROW_yerinə_qoymaq=첫항목()-Terminal_daxiletmə->sürüşdürmək+반환값,simvol_VALUE_068c2631=Terminal_daxiletmə->글자칸들[ROW_yerinə_qoymaq%Tarixçə_xətt_COUNT][simvol_kodu],sətir_verilənlər=Terminal_daxiletmə->모양들[ROW_yerinə_qoymaq%Tarixçə_xətt_COUNT][simvol_kodu];
        if(넓은글자(simvol_VALUE_068c2631)==2&&simvol_kodu+1>=Terminal_daxiletmə->COLUMNS)simvol_VALUE_068c2631=' ';
        if((simvol_VALUE_068c2631==0||simvol_VALUE_068c2631==' ')&&(sətir_verilənlər>>4)==0)continue;
        Terminal_qlif(Terminal_daxiletmə->x_koordinatı+12+simvol_kodu*8,Terminal_daxiletmə->Y_koordinat+36+반환값*16,simvol_VALUE_068c2631?simvol_VALUE_068c2631:' ',색상들[sətir_verilənlər&15],색상들[sətir_verilənlər>>4]);
    }}
    ad_cədvəl(Terminal_daxiletmə->x_koordinatı+12,Terminal_daxiletmə->Y_koordinat+Terminal_daxiletmə->높이-18,Terminal_daxiletmə->sürüşdürmək?"PgDn: recent output":Terminal_daxiletmə->너비>=500?"F6: next | Corner + left drag: resize":"Corner + left drag: resize",0xece8e2,0x403127);daxiletmə_işarəsi_VALUE(1);
}
static void 실행틀(int identifikator_VALUE){
    Terminal_daxiletmə=&Windows_Siyahı[identifikator_VALUE];
    int 가로=Terminal_daxiletmə->x_koordinatı,Şaquli_yerinə_qoymaq=Terminal_daxiletmə->Y_koordinat,폭=Terminal_daxiletmə->너비,uzunluq_VALUE=Terminal_daxiletmə->높이;
    if(!보드그림범위(&가로,&Şaquli_yerinə_qoymaq,&폭,&uzunluq_VALUE))return;
    사각영역(Terminal_daxiletmə->x_koordinatı,Terminal_daxiletmə->Y_koordinat,Terminal_daxiletmə->너비,Terminal_daxiletmə->높이,0x403127);
    unsigned 색상=identifikator_VALUE==Fokus?0x905020:0x604438;사각영역(Terminal_daxiletmə->x_koordinatı,Terminal_daxiletmə->Y_koordinat,Terminal_daxiletmə->너비,30,색상);
    ad_cədvəl(Terminal_daxiletmə->x_koordinatı+12,Terminal_daxiletmə->Y_koordinat+7,"JKOROS Terminal",0xffffff,색상);
    char 수치[2]={(char)('1'+identifikator_VALUE),0};ad_cədvəl(Terminal_daxiletmə->x_koordinatı+148,Terminal_daxiletmə->Y_koordinat+7,수치,0xffffff,색상);
    ad_cədvəl(Terminal_daxiletmə->x_koordinatı+240,Terminal_daxiletmə->Y_koordinat+7,Terminal_daxiletmə->너비>=500?(한글입력?"[AZ] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[AZ]":"[EN]"),0xffffff,색상);
    사각영역(Terminal_daxiletmə->x_koordinatı+Terminal_daxiletmə->너비-32,Terminal_daxiletmə->Y_koordinat+4,26,22,0x5555b8);ad_cədvəl(Terminal_daxiletmə->x_koordinatı+Terminal_daxiletmə->너비-24,Terminal_daxiletmə->Y_koordinat+7,"X",0xffffff,0x5555b8);
    Məzmun_VALUE();
}
static void 장면그리기(void){
    if(!iş_masası_baxmaq)return;사각영역(0,0,보드화면너비(),보드화면높이(),0x302018);사각영역(0,0,보드화면너비(),32,0x403127);
    사각영역(6,4,136,24,0x905020);ad_cədvəl(14,8,"+ New terminal",0xffffff,0x905020);
    for(int 순번=0;순번<4;순번++)if(Windows_Siyahı[순번].살아있음){unsigned simvol_kodu=Fokus==순번?0x905020:0x604438;사각영역(154+순번*112,4,106,24,simvol_kodu);ad_cədvəl(160+순번*112,8,"Terminal",0xffffff,simvol_kodu);char sətir_verilənlər[2]={(char)('1'+순번),0};ad_cədvəl(232+순번*112,8,sətir_verilənlər,0xffffff,simvol_kodu);}
    if(!daxiletmə_COUNT)ad_cədvəl(140,210,"Click + New terminal to start",0xede9df,0x302018);
    for(int 순번=0;순번<daxiletmə_COUNT;순번++)실행틀(ardıcıllıq_VALUE[순번]);화면다시그림(Fokus);Terminal_daxiletmə=&Windows_Siyahı[출력결과];
}
static void 영역그리기(int 가로,int Şaquli_yerinə_qoymaq,int 폭,int uzunluq_VALUE){
    if(!iş_masası_baxmaq||!보드그림범위(&가로,&Şaquli_yerinə_qoymaq,&폭,&uzunluq_VALUE))return;
    for(int Giriş=Şaquli_yerinə_qoymaq;Giriş<Şaquli_yerinə_qoymaq+uzunluq_VALUE;Giriş+=32){
        int 띠높이=Şaquli_yerinə_qoymaq+uzunluq_VALUE-Giriş;if(띠높이>32)띠높이=32;
        if(lövhə_Başla_rəsm(가로,Giriş,폭,띠높이)){장면그리기();lövhə_Bitir_rəsm();}
    }
}
static void 다시그리기(void){영역그리기(0,0,보드화면너비(),보드화면높이());}
/* 서로 겹치지 않는 새 pəncərə 영역과 이전 자리의 네 띠를 복구한다. */
static void 창자리그리기(int 가로,int Şaquli_yerinə_qoymaq,int 폭,int uzunluq_VALUE,Terminal_d413d4bc *pəncərə){
    int 왼쪽=가로>(int)pəncərə->x_koordinatı?가로:(int)pəncərə->x_koordinatı;
    int 위쪽=Şaquli_yerinə_qoymaq>(int)pəncərə->Y_koordinat?Şaquli_yerinə_qoymaq:(int)pəncərə->Y_koordinat;
    int RIGHT=가로+폭<(int)(pəncərə->x_koordinatı+pəncərə->너비)?가로+폭:(int)(pəncərə->x_koordinatı+pəncərə->너비);
    int 아래쪽=Şaquli_yerinə_qoymaq+uzunluq_VALUE<(int)(pəncərə->Y_koordinat+pəncərə->높이)?Şaquli_yerinə_qoymaq+uzunluq_VALUE:(int)(pəncərə->Y_koordinat+pəncərə->높이);
    영역그리기(pəncərə->x_koordinatı,pəncərə->Y_koordinat,pəncərə->너비,pəncərə->높이);
    if(왼쪽>=RIGHT||위쪽>=아래쪽){영역그리기(가로,Şaquli_yerinə_qoymaq,폭,uzunluq_VALUE);return;}
    영역그리기(가로,Şaquli_yerinə_qoymaq,폭,위쪽-Şaquli_yerinə_qoymaq);
    영역그리기(가로,아래쪽,폭,Şaquli_yerinə_qoymaq+uzunluq_VALUE-아래쪽);
    영역그리기(가로,위쪽,왼쪽-가로,아래쪽-위쪽);
    영역그리기(RIGHT,위쪽,가로+폭-RIGHT,아래쪽-위쪽);
}
static void 초점알리기(void){대기중=(대기중&~15u)|(unsigned)(Fokus+1)|0x10000;}
void 터미널입력방식(unsigned 한글여부){
    한글입력=한글여부!=0;
    /* Update title bars only: a mode switch must not erase an EL0 drawing. */
    if(Fokus>=0){
        Terminal_d413d4bc *pəncərə_daxiletmə=&Windows_Siyahı[Fokus];
        ad_cədvəl(pəncərə_daxiletmə->x_koordinatı+240,pəncərə_daxiletmə->Y_koordinat+7,pəncərə_daxiletmə->너비>=500?(한글입력?"[AZ] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[AZ]":"[EN]"),0xffffff,0x905020);
    }
}
static void 앞으로올리기(int identifikator_VALUE){if(identifikator_VALUE<0||identifikator_VALUE>=4||!Windows_Siyahı[identifikator_VALUE].살아있음)return;int 현재위치=0;while(현재위치<daxiletmə_COUNT&&ardıcıllıq_VALUE[현재위치]!=identifikator_VALUE)현재위치++;for(;현재위치+1<daxiletmə_COUNT;현재위치++)ardıcıllıq_VALUE[현재위치]=ardıcıllıq_VALUE[현재위치+1];ardıcıllıq_VALUE[daxiletmə_COUNT-1]=identifikator_VALUE;Fokus=identifikator_VALUE;초점알리기();다시그리기();}
static void 빈칸채우기(unsigned ROW_yerinə_qoymaq){for(unsigned simvol_kodu=0;simvol_kodu<최대열수;simvol_kodu++){Terminal_daxiletmə->글자칸들[ROW_yerinə_qoymaq%Tarixçə_xətt_COUNT][simvol_kodu]=0;Terminal_daxiletmə->모양들[ROW_yerinə_qoymaq%Tarixçə_xətt_COUNT][simvol_kodu]=Terminal_daxiletmə->전경색|(Terminal_daxiletmə->배경색<<4);}}
static void təmizləmək_TOC(void){Terminal_daxiletmə->ROW_yerinə_qoymaq=Terminal_daxiletmə->sütun_yerinə_qoymaq=Terminal_daxiletmə->맨위=Terminal_daxiletmə->sürüşdürmək=0;for(unsigned 반환값=0;반환값<Tarixçə_xətt_COUNT;반환값++)빈칸채우기(반환값);if(보이는지())Məzmun_VALUE();}
static int yarat_daxiletmə(void){
    if(!보드화면기억공간())return -19;int identifikator_VALUE=0;while(identifikator_VALUE<4&&Windows_Siyahı[identifikator_VALUE].살아있음)identifikator_VALUE++;if(identifikator_VALUE==4)return -28;
    iş_masası_baxmaq=1;Terminal_daxiletmə=&Windows_Siyahı[identifikator_VALUE];memset(Terminal_daxiletmə,0,sizeof(*Terminal_daxiletmə));Terminal_daxiletmə->살아있음=1;Terminal_daxiletmə->너비=568;Terminal_daxiletmə->높이=360;Terminal_daxiletmə->COLUMNS=68;Terminal_daxiletmə->ROW_COUNT=19;Terminal_daxiletmə->x_koordinatı=12+identifikator_VALUE*16;Terminal_daxiletmə->Y_koordinat=48+identifikator_VALUE*18;Terminal_daxiletmə->전경색=7;Terminal_daxiletmə->가리개보임=1;
    for(unsigned 반환값=0;반환값<Tarixçə_xətt_COUNT;반환값++)빈칸채우기(반환값);ardıcıllıq_VALUE[daxiletmə_COUNT++]=identifikator_VALUE;Fokus=identifikator_VALUE;대기중|=1u<<(4+identifikator_VALUE);초점알리기();다시그리기();return identifikator_VALUE+1;
}
static void bağlamaq_pəncərə(int identifikator_VALUE){
    if(identifikator_VALUE<0||identifikator_VALUE>=4||!Windows_Siyahı[identifikator_VALUE].살아있음)return;Windows_Siyahı[identifikator_VALUE].살아있음=0;대기중|=1u<<(8+identifikator_VALUE);
    int 현재위치=0;while(현재위치<daxiletmə_COUNT&&ardıcıllıq_VALUE[현재위치]!=identifikator_VALUE)현재위치++;for(;현재위치+1<daxiletmə_COUNT;현재위치++)ardıcıllıq_VALUE[현재위치]=ardıcıllıq_VALUE[현재위치+1];daxiletmə_COUNT--;
    if(Fokus==identifikator_VALUE)Fokus=daxiletmə_COUNT?ardıcıllıq_VALUE[daxiletmə_COUNT-1]:-1;초점알리기();다시그리기();
}
static void 줄바꿈(void){Terminal_daxiletmə->sütun_yerinə_qoymaq=0;Terminal_daxiletmə->ROW_yerinə_qoymaq++;if(Terminal_daxiletmə->ROW_yerinə_qoymaq>=Terminal_daxiletmə->맨위+Terminal_daxiletmə->ROW_COUNT){Terminal_daxiletmə->맨위++;빈칸채우기(Terminal_daxiletmə->ROW_yerinə_qoymaq);if(보이는지())Məzmun_VALUE();}}
static void simvol_kodu_451f2815(unsigned simvol_kodu){
    if(simvol_kodu==13){Terminal_daxiletmə->sütun_yerinə_qoymaq=0;return;}if(simvol_kodu==10){줄바꿈();return;}if(simvol_kodu==8){if(Terminal_daxiletmə->sütun_yerinə_qoymaq)Terminal_daxiletmə->sütun_yerinə_qoymaq--;return;}
    if(simvol_kodu==9){unsigned element_COUNT=8-Terminal_daxiletmə->sütun_yerinə_qoymaq%8;while(element_COUNT--)simvol_kodu_451f2815(' ');return;}if(simvol_kodu<32||simvol_kodu==127)return;
    unsigned 너비값=넓은글자(simvol_kodu);if(Terminal_daxiletmə->sütun_yerinə_qoymaq+너비값>Terminal_daxiletmə->COLUMNS)줄바꿈();
    if(Terminal_daxiletmə->글자칸들[Terminal_daxiletmə->ROW_yerinə_qoymaq%Tarixçə_xətt_COUNT][Terminal_daxiletmə->sütun_yerinə_qoymaq]==0xffffffffu&&Terminal_daxiletmə->sütun_yerinə_qoymaq){Terminal_daxiletmə->글자칸들[Terminal_daxiletmə->ROW_yerinə_qoymaq%Tarixçə_xətt_COUNT][Terminal_daxiletmə->sütun_yerinə_qoymaq-1]=' ';그리기(Terminal_daxiletmə->ROW_yerinə_qoymaq,Terminal_daxiletmə->sütun_yerinə_qoymaq-1);}
    if(넓은글자(Terminal_daxiletmə->글자칸들[Terminal_daxiletmə->ROW_yerinə_qoymaq%Tarixçə_xətt_COUNT][Terminal_daxiletmə->sütun_yerinə_qoymaq])==2&&Terminal_daxiletmə->sütun_yerinə_qoymaq+1<Terminal_daxiletmə->COLUMNS){Terminal_daxiletmə->글자칸들[Terminal_daxiletmə->ROW_yerinə_qoymaq%Tarixçə_xətt_COUNT][Terminal_daxiletmə->sütun_yerinə_qoymaq+1]=' ';그리기(Terminal_daxiletmə->ROW_yerinə_qoymaq,Terminal_daxiletmə->sütun_yerinə_qoymaq+1);}
    Terminal_daxiletmə->글자칸들[Terminal_daxiletmə->ROW_yerinə_qoymaq%Tarixçə_xətt_COUNT][Terminal_daxiletmə->sütun_yerinə_qoymaq]=simvol_kodu;Terminal_daxiletmə->모양들[Terminal_daxiletmə->ROW_yerinə_qoymaq%Tarixçə_xətt_COUNT][Terminal_daxiletmə->sütun_yerinə_qoymaq]=Terminal_daxiletmə->전경색|(Terminal_daxiletmə->배경색<<4);
    if(너비값==2)Terminal_daxiletmə->글자칸들[Terminal_daxiletmə->ROW_yerinə_qoymaq%Tarixçə_xətt_COUNT][Terminal_daxiletmə->sütun_yerinə_qoymaq+1]=0xffffffffu;
    그리기(Terminal_daxiletmə->ROW_yerinə_qoymaq,Terminal_daxiletmə->sütun_yerinə_qoymaq);Terminal_daxiletmə->sütun_yerinə_qoymaq+=너비값;
}
static void tutacaq_nəzarət_SEQUENCE(unsigned simvol_kodu){
    unsigned element_COUNT=Terminal_daxiletmə->매개값[0]?Terminal_daxiletmə->매개값[0]:1;
    if(simvol_kodu=='m')for(unsigned 순번=0;순번<=Terminal_daxiletmə->매개색인;순번++){unsigned verilənlər_yerinə_qoymaq=Terminal_daxiletmə->매개값[순번];if(!verilənlər_yerinə_qoymaq){Terminal_daxiletmə->전경색=7;Terminal_daxiletmə->배경색=0;}if(verilənlər_yerinə_qoymaq==1&&Terminal_daxiletmə->전경색<8)Terminal_daxiletmə->전경색+=8;if(verilənlər_yerinə_qoymaq==7){unsigned 유지=Terminal_daxiletmə->전경색;Terminal_daxiletmə->전경색=Terminal_daxiletmə->배경색;Terminal_daxiletmə->배경색=유지;}if(verilənlər_yerinə_qoymaq>=30&&verilənlər_yerinə_qoymaq<=37)Terminal_daxiletmə->전경색=verilənlər_yerinə_qoymaq-30;if(verilənlər_yerinə_qoymaq>=90&&verilənlər_yerinə_qoymaq<=97)Terminal_daxiletmə->전경색=verilənlər_yerinə_qoymaq-90+8;if(verilənlər_yerinə_qoymaq>=40&&verilənlər_yerinə_qoymaq<=47)Terminal_daxiletmə->배경색=verilənlər_yerinə_qoymaq-40;if(verilənlər_yerinə_qoymaq>=100&&verilənlər_yerinə_qoymaq<=107)Terminal_daxiletmə->배경색=verilənlər_yerinə_qoymaq-100+8;if(verilənlər_yerinə_qoymaq==39)Terminal_daxiletmə->전경색=7;if(verilənlər_yerinə_qoymaq==49)Terminal_daxiletmə->배경색=0;}
    if(simvol_kodu=='J'&&(Terminal_daxiletmə->매개값[0]==2||Terminal_daxiletmə->매개값[0]==3))təmizləmək_TOC();
    if(simvol_kodu=='K'){unsigned 출발위치=Terminal_daxiletmə->매개값[0]==2?0:Terminal_daxiletmə->sütun_yerinə_qoymaq,도착위치=Terminal_daxiletmə->매개값[0]==1?Terminal_daxiletmə->sütun_yerinə_qoymaq+1:Terminal_daxiletmə->COLUMNS;if(Terminal_daxiletmə->매개값[0]==1)출발위치=0;for(unsigned 순번=출발위치;순번<도착위치&&순번<Terminal_daxiletmə->COLUMNS;순번++){
        unsigned ROW_VALUE=Terminal_daxiletmə->ROW_yerinə_qoymaq%Tarixçə_xətt_COUNT,simvol_VALUE_068c2631=Terminal_daxiletmə->글자칸들[ROW_VALUE][순번],fiqur_VALUE=Terminal_daxiletmə->전경색|(Terminal_daxiletmə->배경색<<4);
        /* 넓은 vi 화면에서도 이미 빈 칸의 şrift_VALUE 화소를 되풀이해 칠하지 않는다. */
        int 바뀜=(simvol_VALUE_068c2631!=0&&simvol_VALUE_068c2631!=' ')||Terminal_daxiletmə->모양들[ROW_VALUE][순번]!=fiqur_VALUE;
        Terminal_daxiletmə->글자칸들[ROW_VALUE][순번]=' ';Terminal_daxiletmə->모양들[ROW_VALUE][순번]=fiqur_VALUE;
        if(바뀜)그리기(Terminal_daxiletmə->ROW_yerinə_qoymaq,순번);
    }}
    if(simvol_kodu=='D')Terminal_daxiletmə->sütun_yerinə_qoymaq=element_COUNT>Terminal_daxiletmə->sütun_yerinə_qoymaq?0:Terminal_daxiletmə->sütun_yerinə_qoymaq-element_COUNT;if(simvol_kodu=='C')Terminal_daxiletmə->sütun_yerinə_qoymaq=Terminal_daxiletmə->sütun_yerinə_qoymaq+element_COUNT>=Terminal_daxiletmə->COLUMNS?Terminal_daxiletmə->COLUMNS-1:Terminal_daxiletmə->sütun_yerinə_qoymaq+element_COUNT;
    if(simvol_kodu=='G')Terminal_daxiletmə->sütun_yerinə_qoymaq=element_COUNT>Terminal_daxiletmə->COLUMNS?Terminal_daxiletmə->COLUMNS-1:element_COUNT-1;if(simvol_kodu=='A')Terminal_daxiletmə->ROW_yerinə_qoymaq=element_COUNT>Terminal_daxiletmə->ROW_yerinə_qoymaq-Terminal_daxiletmə->맨위?Terminal_daxiletmə->맨위:Terminal_daxiletmə->ROW_yerinə_qoymaq-element_COUNT;
    if(simvol_kodu=='B')Terminal_daxiletmə->ROW_yerinə_qoymaq=Terminal_daxiletmə->ROW_yerinə_qoymaq+element_COUNT>=Terminal_daxiletmə->맨위+Terminal_daxiletmə->ROW_COUNT?Terminal_daxiletmə->맨위+Terminal_daxiletmə->ROW_COUNT-1:Terminal_daxiletmə->ROW_yerinə_qoymaq+element_COUNT;
    if(simvol_kodu=='H'||simvol_kodu=='f'){Terminal_daxiletmə->ROW_yerinə_qoymaq=Terminal_daxiletmə->맨위+(element_COUNT>Terminal_daxiletmə->ROW_COUNT?Terminal_daxiletmə->ROW_COUNT:element_COUNT)-1;unsigned x_koordinatı=Terminal_daxiletmə->매개값[1]?Terminal_daxiletmə->매개값[1]:1;Terminal_daxiletmə->sütun_yerinə_qoymaq=(x_koordinatı>Terminal_daxiletmə->COLUMNS?Terminal_daxiletmə->COLUMNS:x_koordinatı)-1;}
    if(simvol_kodu=='s'){Terminal_daxiletmə->저장행=Terminal_daxiletmə->ROW_yerinə_qoymaq;Terminal_daxiletmə->저장열=Terminal_daxiletmə->sütun_yerinə_qoymaq;}if(simvol_kodu=='u'){Terminal_daxiletmə->ROW_yerinə_qoymaq=Terminal_daxiletmə->저장행;Terminal_daxiletmə->sütun_yerinə_qoymaq=Terminal_daxiletmə->저장열<Terminal_daxiletmə->COLUMNS?Terminal_daxiletmə->저장열:Terminal_daxiletmə->COLUMNS-1;}
    if((simvol_kodu=='h'||simvol_kodu=='l')&&Terminal_daxiletmə->매개값[0]==25)Terminal_daxiletmə->가리개보임=simvol_kodu=='h';
}
void Terminal_bayt(unsigned SECOND_VALUE){
    Terminal_daxiletmə=&Windows_Siyahı[출력결과];if(!Terminal_daxiletmə->살아있음)return;daxiletmə_işarəsi_VALUE(0);if(Terminal_daxiletmə->sürüşdürmək){Terminal_daxiletmə->sürüşdürmək=0;if(보이는지())Məzmun_VALUE();}
    if(Terminal_daxiletmə->탈출상태==1){Terminal_daxiletmə->탈출상태=SECOND_VALUE=='['?2:0;Terminal_daxiletmə->매개색인=0;for(unsigned 순번=0;순번<4;순번++)Terminal_daxiletmə->매개값[순번]=0;}
    else if(Terminal_daxiletmə->탈출상태==2){if(SECOND_VALUE=='?'){}else if(SECOND_VALUE>='0'&&SECOND_VALUE<='9'){if(Terminal_daxiletmə->매개값[Terminal_daxiletmə->매개색인]<10000)Terminal_daxiletmə->매개값[Terminal_daxiletmə->매개색인]=Terminal_daxiletmə->매개값[Terminal_daxiletmə->매개색인]*10+SECOND_VALUE-'0';}else if(SECOND_VALUE==';'&&Terminal_daxiletmə->매개색인<3)Terminal_daxiletmə->매개색인++;else{tutacaq_nəzarət_SEQUENCE(SECOND_VALUE);Terminal_daxiletmə->탈출상태=0;}}
    else if(SECOND_VALUE==27){Terminal_daxiletmə->긴부호없는값=0;Terminal_daxiletmə->탈출상태=1;}else{
        if(Terminal_daxiletmə->긴부호없는값&&(SECOND_VALUE&0xc0)!=0x80){Terminal_daxiletmə->긴부호없는값=0;simvol_kodu_451f2815(0xfffd);}
        if(Terminal_daxiletmə->긴부호없는값){Terminal_daxiletmə->부호없는결과=Terminal_daxiletmə->부호없는결과*64+(SECOND_VALUE&63);if(--Terminal_daxiletmə->긴부호없는값==0)simvol_kodu_451f2815(Terminal_daxiletmə->부호없는결과<Terminal_daxiletmə->SMALL_VALUE||Terminal_daxiletmə->부호없는결과>0x10ffff||(Terminal_daxiletmə->부호없는결과>=0xd800&&Terminal_daxiletmə->부호없는결과<=0xdfff)?0xfffd:Terminal_daxiletmə->부호없는결과);}
        else if(SECOND_VALUE<128)simvol_kodu_451f2815(SECOND_VALUE);else if(SECOND_VALUE>=0xc2&&SECOND_VALUE<=0xf4){Terminal_daxiletmə->긴부호없는값=SECOND_VALUE<0xe0?1:SECOND_VALUE<0xf0?2:3;Terminal_daxiletmə->부호없는결과=SECOND_VALUE&((1u<<(6-Terminal_daxiletmə->긴부호없는값))-1);Terminal_daxiletmə->SMALL_VALUE=Terminal_daxiletmə->긴부호없는값==1?128:Terminal_daxiletmə->긴부호없는값==2?2048:65536;}else simvol_kodu_451f2815(0xfffd);
    }daxiletmə_işarəsi_VALUE(1);
}
int Terminal_gözləyir(void){return 대기중!=0;}
/* 모서리 INDEX: 1 좌상, 2 우상, 3 좌하, 4 우하. */
static int ölçüsünü_dəyişmək_sürükləmək=-1,잡은모서리,잡은가로,잡은세로,처음가로,처음세로,처음너비,처음높이;
static int 가리킨창(int 가로,int Şaquli_yerinə_qoymaq) {
    for(int SEQUENCE_VALUE=daxiletmə_COUNT-1;SEQUENCE_VALUE>=0;SEQUENCE_VALUE--){
        int identifikator_VALUE=ardıcıllıq_VALUE[SEQUENCE_VALUE];Terminal_d413d4bc *pəncərə=&Windows_Siyahı[identifikator_VALUE];
        if(가로>=(int)pəncərə->x_koordinatı&&Şaquli_yerinə_qoymaq>=(int)pəncərə->Y_koordinat&&
           가로<(int)(pəncərə->x_koordinatı+pəncərə->너비)&&Şaquli_yerinə_qoymaq<(int)(pəncərə->Y_koordinat+pəncərə->높이))return identifikator_VALUE;
    }return -1;
}
static int 모서리찾기(int identifikator_VALUE,int 가로,int Şaquli_yerinə_qoymaq) {
    if(identifikator_VALUE<0)return 0;Terminal_d413d4bc *pəncərə=&Windows_Siyahı[identifikator_VALUE];
    int 왼쪽=가로<(int)pəncərə->x_koordinatı+8,RIGHT=가로>=(int)(pəncərə->x_koordinatı+pəncərə->너비)-8;
    int 위쪽=Şaquli_yerinə_qoymaq<(int)pəncərə->Y_koordinat+8,아래쪽=Şaquli_yerinə_qoymaq>=(int)(pəncərə->Y_koordinat+pəncərə->높이)-8;
    return (왼쪽||RIGHT)&&(위쪽||아래쪽)?1+RIGHT+아래쪽*2:0;
}
static int ayırıcı_VALUE(int VALUE,int 최소,int 최대){return VALUE<최소?최소:VALUE>최대?최대:VALUE;}
static void hərəkət_etdir_ölçüsünü_dəyişmək(int 가로,int Şaquli_yerinə_qoymaq) {
    Terminal_d413d4bc *pəncərə=&Windows_Siyahı[ölçüsünü_dəyişmək_sürükləmək];int 왼쪽=처음가로,위쪽=처음세로,RIGHT=처음가로+처음너비,아래쪽=처음세로+처음높이;
    if(잡은모서리==1||잡은모서리==3)왼쪽=ayırıcı_VALUE(처음가로+가로-잡은가로,0,RIGHT-360);
    else RIGHT=ayırıcı_VALUE(처음가로+처음너비+가로-잡은가로,왼쪽+360,보드화면너비());
    if(잡은모서리<=2)위쪽=ayırıcı_VALUE(처음세로+Şaquli_yerinə_qoymaq-잡은세로,34,아래쪽-216);
    else 아래쪽=ayırıcı_VALUE(처음세로+처음높이+Şaquli_yerinə_qoymaq-잡은세로,위쪽+216,보드화면높이());
    unsigned COLUMNS=(RIGHT-왼쪽-24)/8,ROW_COUNT=(아래쪽-위쪽-56)/16;
    if(pəncərə->COLUMNS!=COLUMNS||pəncərə->ROW_COUNT!=ROW_COUNT){
        pəncərə->크기바뀜=1;pəncərə->COLUMNS=COLUMNS;pəncərə->ROW_COUNT=ROW_COUNT;
        if(pəncərə->sütun_yerinə_qoymaq>=COLUMNS)pəncərə->sütun_yerinə_qoymaq=COLUMNS-1;
        if(pəncərə->ROW_yerinə_qoymaq>=pəncərə->맨위+ROW_COUNT)pəncərə->맨위=pəncərə->ROW_yerinə_qoymaq-ROW_COUNT+1;
        unsigned 한도=pəncərə->맨위;if(한도>Tarixçə_xətt_COUNT-ROW_COUNT)한도=Tarixçə_xətt_COUNT-ROW_COUNT;
        if(pəncərə->sürüşdürmək>한도)pəncərə->sürüşdürmək=한도;
    }
    int 옛가로=pəncərə->x_koordinatı,옛세로=pəncərə->Y_koordinat,옛폭=pəncərə->너비,옛길이=pəncərə->높이;
    if(옛가로==왼쪽&&옛세로==위쪽&&옛폭==RIGHT-왼쪽&&옛길이==아래쪽-위쪽)return;
    pəncərə->x_koordinatı=왼쪽;pəncərə->Y_koordinat=위쪽;pəncərə->너비=RIGHT-왼쪽;pəncərə->높이=아래쪽-위쪽;
    창자리그리기(옛가로,옛세로,옛폭,옛길이,pəncərə);
}
void Terminal_göstərici(unsigned Sonrakı_element,int x_koordinatı,int Y_koordinat){
    unsigned 눌림=Sonrakı_element&~단추들;단추들=Sonrakı_element;
    if(!iş_masası_baxmaq){sürükləmək_VALUE=-1;ölçüsünü_dəyişmək_sürükləmək=-1;lövhə_göstərici(x_koordinatı,Y_koordinat,1);return;}
    if(!(Sonrakı_element&1)){sürükləmək_VALUE=-1;ölçüsünü_dəyişmək_sürükləmək=-1;}
    if(ölçüsünü_dəyişmək_sürükləmək>=0&&!Windows_Siyahı[ölçüsünü_dəyişmək_sürükləmək].살아있음)ölçüsünü_dəyişmək_sürükləmək=-1;
    if(sürükləmək_VALUE>=0&&!Windows_Siyahı[sürükləmək_VALUE].살아있음)sürükləmək_VALUE=-1;
    if(ölçüsünü_dəyişmək_sürükləmək>=0){
        hərəkət_etdir_ölçüsünü_dəyişmək(x_koordinatı,Y_koordinat);lövhə_göstərici(x_koordinatı,Y_koordinat,잡은모서리==1||잡은모서리==4?2:3);return;
    }
    lövhə_göstərici(x_koordinatı,Y_koordinat,1);
    if(sürükləmək_VALUE>=0){
        Terminal_d413d4bc *pəncərə=&Windows_Siyahı[sürükləmək_VALUE];
        int 옛가로=pəncərə->x_koordinatı,옛세로=pəncərə->Y_koordinat;
        pəncərə->x_koordinatı=ayırıcı_VALUE(x_koordinatı-sürükləmək_X,0,보드화면너비()-pəncərə->너비);
        pəncərə->Y_koordinat=ayırıcı_VALUE(Y_koordinat-sürükləmək_Y,34,보드화면높이()-pəncərə->높이);
        if(옛가로!=(int)pəncərə->x_koordinatı||옛세로!=(int)pəncərə->Y_koordinat)창자리그리기(옛가로,옛세로,pəncərə->너비,pəncərə->높이,pəncərə);
        return;
    }
    extern int 화면덮음(int,int,int);
    if(화면덮음(Fokus,x_koordinatı,Y_koordinat)){화면가리킴(Fokus,눌림,x_koordinatı,Y_koordinat);return;}
    int identifikator_VALUE=가리킨창(x_koordinatı,Y_koordinat),모서리=모서리찾기(identifikator_VALUE,x_koordinatı,Y_koordinat);
    if(모서리)lövhə_göstərici(x_koordinatı,Y_koordinat,모서리==1||모서리==4?2:3);
    if(눌림&1){
        if(모서리){
            Terminal_d413d4bc *pəncərə=&Windows_Siyahı[identifikator_VALUE];ölçüsünü_dəyişmək_sürükləmək=identifikator_VALUE;잡은모서리=모서리;잡은가로=x_koordinatı;잡은세로=Y_koordinat;
            처음가로=pəncərə->x_koordinatı;처음세로=pəncərə->Y_koordinat;처음너비=pəncərə->너비;처음높이=pəncərə->높이;
            if(identifikator_VALUE!=Fokus)앞으로올리기(identifikator_VALUE);return;
        }
        if(Y_koordinat<32&&x_koordinatı>=6&&x_koordinatı<142){yarat_daxiletmə();return;}
        if(Y_koordinat<32&&x_koordinatı>=154&&x_koordinatı<602){앞으로올리기((x_koordinatı-154)/112);return;}
        if(identifikator_VALUE>=0){
            Terminal_d413d4bc *pəncərə=&Windows_Siyahı[identifikator_VALUE];
            if(Y_koordinat<(int)pəncərə->Y_koordinat+30&&x_koordinatı>=(int)(pəncərə->x_koordinatı+pəncərə->너비)-32){bağlamaq_pəncərə(identifikator_VALUE);return;}
            if(identifikator_VALUE!=Fokus)앞으로올리기(identifikator_VALUE);
            if(Y_koordinat<(int)pəncərə->Y_koordinat+30){sürükləmək_VALUE=identifikator_VALUE;sürükləmək_X=x_koordinatı-pəncərə->x_koordinatı;sürükləmək_Y=Y_koordinat-pəncərə->Y_koordinat;}return;
        }
    }
    if(Fokus>=0&&(눌림&(8|16))){Terminal_daxiletmə=&Windows_Siyahı[Fokus];if(눌림&8){unsigned 한도=Terminal_daxiletmə->맨위;if(한도>Tarixçə_xətt_COUNT-Terminal_daxiletmə->ROW_COUNT)한도=Tarixçə_xətt_COUNT-Terminal_daxiletmə->ROW_COUNT;Terminal_daxiletmə->sürüşdürmək=Terminal_daxiletmə->sürüşdürmək+9>한도?한도:Terminal_daxiletmə->sürüşdürmək+9;}else Terminal_daxiletmə->sürüşdürmək=Terminal_daxiletmə->sürüşdürmək<9?0:Terminal_daxiletmə->sürüşdürmək-9;다시그리기();}
}
void 터미널바로가기키(unsigned 누름값){if(누름값==1)yarat_daxiletmə();if(누름값==2&&daxiletmə_COUNT)앞으로올리기(ardıcıllıq_VALUE[0]);if(누름값==3)bağlamaq_pəncərə(Fokus);}
maşın_Söz lövhə_Terminal(maşın_Söz Gedişat){
    if(Gedişat==300){if(!Windows_Siyahı[출력결과].살아있음)return yarat_daxiletmə();iş_masası_baxmaq=1;다시그리기();return 0;}
    if(Gedişat==0){bağlamaq_pəncərə(Fokus);return 0;}if(Gedişat==1)return (uint32_t)yarat_daxiletmə();if(Gedişat==2)return Fokus>=0;
    if(Gedişat==9){iş_masası_baxmaq=0;return 0;}if(Gedişat==7)return daxiletmə_COUNT;if(Gedişat==10)return Fokus+1;if(Gedişat==11)return 출력결과;
    if(Gedişat==13){Terminal_d413d4bc *pəncərə=&Windows_Siyahı[출력결과];return pəncərə->살아있음?(pəncərə->ROW_COUNT<<16)|pəncərə->COLUMNS:(19<<16)|68;}
    if(Gedişat==14){unsigned VALUE=Windows_Siyahı[출력결과].크기바뀜;Windows_Siyahı[출력결과].크기바뀜=0;return VALUE;}
    if(Gedişat==12){unsigned VALUE=대기중;대기중=0;return VALUE;}
    if(Gedişat>=20&&Gedişat<24)return Windows_Siyahı[Gedişat-20].살아있음;
    if(Gedişat>=100&&Gedişat<104){출력결과=Gedişat-100;Terminal_daxiletmə=&Windows_Siyahı[출력결과];return 0;}
    if(Gedişat>=200&&Gedişat<204){앞으로올리기(Gedişat-200);return 0;}
    if(Gedişat==3){다시그리기();return 0;}Terminal_daxiletmə=&Windows_Siyahı[출력결과];if(!Terminal_daxiletmə->살아있음)return 0;
    if(Gedişat==4)təmizləmək_TOC();if(Gedişat==5||Gedişat==6){unsigned 이전=단추들;Terminal_göstərici(Gedişat==5?8:16,0,0);단추들=이전;}return 1;
}
