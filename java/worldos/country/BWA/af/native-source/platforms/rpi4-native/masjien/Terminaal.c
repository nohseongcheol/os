#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* 자체 네 venster 합성과 UTF-8 Terminaal. 바뀐 영역의 완성 그림만 표시한다. */
#include <stdint.h>
#include <stddef.h>
typedef uintptr_t masjien_Word;
extern masjien_Word bord_pieksel(masjien_Word,masjien_Word,masjien_Word),보드화면기억공간(void);
extern void *memset(void *,int,size_t);
extern const unsigned char Terminaal_font[];
#define 최대열수 237
#define Geskiedenis_lyn_COUNT 160
typedef struct {
    uint32_t 글자칸들[Geskiedenis_lyn_COUNT][최대열수]; uint8_t 모양들[Geskiedenis_lyn_COUNT][최대열수];
    unsigned 너비,높이,COLUMNS,ry_COUNT,크기바뀜;
    unsigned 살아있음,x_koördinaat,Y_koördinaat,ry_plaas,kolom_plaas,맨위,rol,전경색,배경색,탈출상태,매개값[4],매개색인,저장행,저장열;
    unsigned 부호없는결과,긴부호없는값,SMALL_VALUE,대체화면,가리개보임;
} Terminaal_d413d4bc;
static Terminaal_d413d4bc Windows_Lys[4];
static int Fokus=-1,출력결과,volgorde_VALUE[4],inskrywing_COUNT,sleep_VALUE=-1,sleep_X,sleep_Y;
static unsigned 대기중,단추들,werkskerm_bekyk,한글입력;
static const uint32_t 색상들[16]={0x201a15,0x6060df,0x9dcc86,0x80cfea,0xefaf72,0xca96c9,0xceda76,0xede9df,0x858078,0x8888ff,0xb9eba7,0xa5eaff,0xffcc99,0xf0bef1,0xf0f0a0,0xffffff};
extern int 화면보임(int),화면가리킴(int,unsigned,int,int);
extern void 화면다시그림(int);
static Terminaal_d413d4bc *Terminaal_inskrywing;
static unsigned 넓은글자(unsigned karakterkode){return karakterkode>=256?2:1;}
static void 사각영역(unsigned x_koördinaat,unsigned Y_koördinaat,unsigned 너비값,unsigned 높이값,unsigned 색상){
    보드사각그림(x_koördinaat,Y_koördinaat,너비값,높이값,색상);
}
void Terminaal_glief(unsigned x_koördinaat,unsigned Y_koördinaat,unsigned karakterkode,unsigned 전경색,unsigned 배경색){
    unsigned 너비=넓은글자(karakterkode)*8;if(karakterkode==0xffffffffu)return;
    int 왼쪽=x_koördinaat,위쪽=Y_koördinaat,폭=너비,lengte_VALUE=16;
    if(!보드그림범위(&왼쪽,&위쪽,&폭,&lengte_VALUE))return;
    if(karakterkode==' '){보드사각그림(왼쪽,위쪽,폭,lengte_VALUE,배경색);return;}
    unsigned LOOKUP_INDEX=karakterkode<65536?karakterkode:karakterkode>=0x1f600&&karakterkode<0x1f650?65536+karakterkode-0x1f600:0xfffd;
    const unsigned char *font_VALUE=Terminaal_font+LOOKUP_INDEX*32;
    for(int lyn=위쪽;lyn<위쪽+lengte_VALUE;lyn++){unsigned Agtergrond_intelligente_oordragdiens_Lys=font_VALUE[(lyn-Y_koördinaat)*2]*256+font_VALUE[(lyn-Y_koördinaat)*2+1];for(int gleuf_inskrywing=왼쪽;gleuf_inskrywing<왼쪽+폭;gleuf_inskrywing++)bord_pieksel(gleuf_inskrywing,lyn,(Agtergrond_intelligente_oordragdiens_Lys&(0x8000>>(gleuf_inskrywing-x_koördinaat)))?전경색:배경색);}
}
static void naam_tabel(unsigned x_koördinaat,unsigned Y_koördinaat,const char *string_data,unsigned 전경색,unsigned 배경색){while(*string_data){unsigned karakterkode=(unsigned char)*string_data++, 남은수=0;if(karakterkode>=0xc0){남은수=karakterkode<0xe0?1:karakterkode<0xf0?2:3;karakterkode&=(1u<<(6-남은수))-1;while(남은수--&&*string_data)karakterkode=(karakterkode<<6)|((unsigned char)*string_data++&63);}Terminaal_glief(x_koördinaat,Y_koördinaat,karakterkode,전경색,배경색);x_koördinaat+=넓은글자(karakterkode)*8;}}
static unsigned 첫항목(void){return Terminaal_inskrywing->맨위;}
static int 보이는지(void){return Terminaal_inskrywing->살아있음&&Fokus>=0&&Terminaal_inskrywing==&Windows_Lys[Fokus]&&!화면보임(Fokus);}
static void 그리기(unsigned ry_plaas,unsigned kolom_plaas){
    if(!보이는지()||ry_plaas<첫항목()-Terminaal_inskrywing->rol||ry_plaas>=첫항목()-Terminaal_inskrywing->rol+Terminaal_inskrywing->ry_COUNT||kolom_plaas>=Terminaal_inskrywing->COLUMNS)return;
    unsigned karakterkode=Terminaal_inskrywing->글자칸들[ry_plaas%Geskiedenis_lyn_COUNT][kolom_plaas],string_data=Terminaal_inskrywing->모양들[ry_plaas%Geskiedenis_lyn_COUNT][kolom_plaas];
    if(넓은글자(karakterkode)==2&&kolom_plaas+1>=Terminaal_inskrywing->COLUMNS)karakterkode=' ';
    Terminaal_glief(Terminaal_inskrywing->x_koördinaat+12+kolom_plaas*8,Terminaal_inskrywing->Y_koördinaat+36+(ry_plaas-첫항목()+Terminaal_inskrywing->rol)*16,karakterkode?karakterkode:' ',색상들[string_data&15],색상들[string_data>>4]);
}
static void kappie_VALUE(int wys_venster){if(!보이는지()||Terminaal_inskrywing->rol||Terminaal_inskrywing->kolom_plaas>=Terminaal_inskrywing->COLUMNS||Terminaal_inskrywing->ry_plaas<Terminaal_inskrywing->맨위||Terminaal_inskrywing->ry_plaas>=Terminaal_inskrywing->맨위+Terminaal_inskrywing->ry_COUNT)return;
    if(!wys_venster||!Terminaal_inskrywing->가리개보임)그리기(Terminaal_inskrywing->ry_plaas,Terminaal_inskrywing->kolom_plaas);else 사각영역(Terminaal_inskrywing->x_koördinaat+12+Terminaal_inskrywing->kolom_plaas*8,Terminaal_inskrywing->Y_koördinaat+36+(Terminaal_inskrywing->ry_plaas-Terminaal_inskrywing->맨위)*16+14,8,2,색상들[Terminaal_inskrywing->전경색]);}
static void Inhoud_VALUE(void){
    사각영역(Terminaal_inskrywing->x_koördinaat+12,Terminaal_inskrywing->Y_koördinaat+36,Terminaal_inskrywing->COLUMNS*8,Terminaal_inskrywing->ry_COUNT*16,색상들[0]);
    int 가로=Terminaal_inskrywing->x_koördinaat+12,Vertikaal_plaas=Terminaal_inskrywing->Y_koördinaat+36,폭=Terminaal_inskrywing->COLUMNS*8,lengte_VALUE=Terminaal_inskrywing->ry_COUNT*16;
    if(보드그림범위(&가로,&Vertikaal_plaas,&폭,&lengte_VALUE)){
    unsigned 첫줄=(Vertikaal_plaas-Terminaal_inskrywing->Y_koördinaat-36)/16,끝줄=(Vertikaal_plaas+lengte_VALUE-Terminaal_inskrywing->Y_koördinaat-36+15)/16;
    unsigned 첫칸=(가로-Terminaal_inskrywing->x_koördinaat-12)/8,끝칸=(가로+폭-Terminaal_inskrywing->x_koördinaat-12+7)/8;
    if(첫칸)첫칸--; /* 잘림 경계 왼쪽에서 시작한 두 gleuf_inskrywing 글자도 그린다. */
    for(unsigned 반환값=첫줄;반환값<끝줄;반환값++)for(unsigned karakterkode=첫칸;karakterkode<끝칸;karakterkode++){
        unsigned ry_plaas=첫항목()-Terminaal_inskrywing->rol+반환값,karakter_VALUE=Terminaal_inskrywing->글자칸들[ry_plaas%Geskiedenis_lyn_COUNT][karakterkode],string_data=Terminaal_inskrywing->모양들[ry_plaas%Geskiedenis_lyn_COUNT][karakterkode];
        if(넓은글자(karakter_VALUE)==2&&karakterkode+1>=Terminaal_inskrywing->COLUMNS)karakter_VALUE=' ';
        if((karakter_VALUE==0||karakter_VALUE==' ')&&(string_data>>4)==0)continue;
        Terminaal_glief(Terminaal_inskrywing->x_koördinaat+12+karakterkode*8,Terminaal_inskrywing->Y_koördinaat+36+반환값*16,karakter_VALUE?karakter_VALUE:' ',색상들[string_data&15],색상들[string_data>>4]);
    }}
    naam_tabel(Terminaal_inskrywing->x_koördinaat+12,Terminaal_inskrywing->Y_koördinaat+Terminaal_inskrywing->높이-18,Terminaal_inskrywing->rol?"PgDn: recent output":Terminaal_inskrywing->너비>=500?"F6: next | Corner + left drag: resize":"Corner + left drag: resize",0xece8e2,0x403127);kappie_VALUE(1);
}
static void 실행틀(int waarde_VALUE){
    Terminaal_inskrywing=&Windows_Lys[waarde_VALUE];
    int 가로=Terminaal_inskrywing->x_koördinaat,Vertikaal_plaas=Terminaal_inskrywing->Y_koördinaat,폭=Terminaal_inskrywing->너비,lengte_VALUE=Terminaal_inskrywing->높이;
    if(!보드그림범위(&가로,&Vertikaal_plaas,&폭,&lengte_VALUE))return;
    사각영역(Terminaal_inskrywing->x_koördinaat,Terminaal_inskrywing->Y_koördinaat,Terminaal_inskrywing->너비,Terminaal_inskrywing->높이,0x403127);
    unsigned 색상=waarde_VALUE==Fokus?0x905020:0x604438;사각영역(Terminaal_inskrywing->x_koördinaat,Terminaal_inskrywing->Y_koördinaat,Terminaal_inskrywing->너비,30,색상);
    naam_tabel(Terminaal_inskrywing->x_koördinaat+12,Terminaal_inskrywing->Y_koördinaat+7,"JKOROS Terminal",0xffffff,색상);
    char 수치[2]={(char)('1'+waarde_VALUE),0};naam_tabel(Terminaal_inskrywing->x_koördinaat+148,Terminaal_inskrywing->Y_koördinaat+7,수치,0xffffff,색상);
    naam_tabel(Terminaal_inskrywing->x_koördinaat+240,Terminaal_inskrywing->Y_koördinaat+7,Terminaal_inskrywing->너비>=500?(한글입력?"[AF] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[AF]":"[EN]"),0xffffff,색상);
    사각영역(Terminaal_inskrywing->x_koördinaat+Terminaal_inskrywing->너비-32,Terminaal_inskrywing->Y_koördinaat+4,26,22,0x5555b8);naam_tabel(Terminaal_inskrywing->x_koördinaat+Terminaal_inskrywing->너비-24,Terminaal_inskrywing->Y_koördinaat+7,"X",0xffffff,0x5555b8);
    Inhoud_VALUE();
}
static void 장면그리기(void){
    if(!werkskerm_bekyk)return;사각영역(0,0,보드화면너비(),보드화면높이(),0x302018);사각영역(0,0,보드화면너비(),32,0x403127);
    사각영역(6,4,136,24,0x905020);naam_tabel(14,8,"+ New terminal",0xffffff,0x905020);
    for(int 순번=0;순번<4;순번++)if(Windows_Lys[순번].살아있음){unsigned karakterkode=Fokus==순번?0x905020:0x604438;사각영역(154+순번*112,4,106,24,karakterkode);naam_tabel(160+순번*112,8,"Terminal",0xffffff,karakterkode);char string_data[2]={(char)('1'+순번),0};naam_tabel(232+순번*112,8,string_data,0xffffff,karakterkode);}
    if(!inskrywing_COUNT)naam_tabel(140,210,"Click + New terminal to start",0xede9df,0x302018);
    for(int 순번=0;순번<inskrywing_COUNT;순번++)실행틀(volgorde_VALUE[순번]);화면다시그림(Fokus);Terminaal_inskrywing=&Windows_Lys[출력결과];
}
static void 영역그리기(int 가로,int Vertikaal_plaas,int 폭,int lengte_VALUE){
    if(!werkskerm_bekyk||!보드그림범위(&가로,&Vertikaal_plaas,&폭,&lengte_VALUE))return;
    for(int lyn=Vertikaal_plaas;lyn<Vertikaal_plaas+lengte_VALUE;lyn+=32){
        int 띠높이=Vertikaal_plaas+lengte_VALUE-lyn;if(띠높이>32)띠높이=32;
        if(bord_BEGIN_tekening(가로,lyn,폭,띠높이)){장면그리기();bord_Klaar_tekening();}
    }
}
static void 다시그리기(void){영역그리기(0,0,보드화면너비(),보드화면높이());}
/* 서로 겹치지 않는 새 venster 영역과 이전 자리의 네 띠를 복구한다. */
static void 창자리그리기(int 가로,int Vertikaal_plaas,int 폭,int lengte_VALUE,Terminaal_d413d4bc *venster){
    int 왼쪽=가로>(int)venster->x_koördinaat?가로:(int)venster->x_koördinaat;
    int 위쪽=Vertikaal_plaas>(int)venster->Y_koördinaat?Vertikaal_plaas:(int)venster->Y_koördinaat;
    int RIGHT=가로+폭<(int)(venster->x_koördinaat+venster->너비)?가로+폭:(int)(venster->x_koördinaat+venster->너비);
    int 아래쪽=Vertikaal_plaas+lengte_VALUE<(int)(venster->Y_koördinaat+venster->높이)?Vertikaal_plaas+lengte_VALUE:(int)(venster->Y_koördinaat+venster->높이);
    영역그리기(venster->x_koördinaat,venster->Y_koördinaat,venster->너비,venster->높이);
    if(왼쪽>=RIGHT||위쪽>=아래쪽){영역그리기(가로,Vertikaal_plaas,폭,lengte_VALUE);return;}
    영역그리기(가로,Vertikaal_plaas,폭,위쪽-Vertikaal_plaas);
    영역그리기(가로,아래쪽,폭,Vertikaal_plaas+lengte_VALUE-아래쪽);
    영역그리기(가로,위쪽,왼쪽-가로,아래쪽-위쪽);
    영역그리기(RIGHT,위쪽,가로+폭-RIGHT,아래쪽-위쪽);
}
static void 초점알리기(void){대기중=(대기중&~15u)|(unsigned)(Fokus+1)|0x10000;}
void 터미널입력방식(unsigned 한글여부){
    한글입력=한글여부!=0;
    /* Update title bars only: a mode switch must not erase an EL0 drawing. */
    if(Fokus>=0){
        Terminaal_d413d4bc *venster_inskrywing=&Windows_Lys[Fokus];
        naam_tabel(venster_inskrywing->x_koördinaat+240,venster_inskrywing->Y_koördinaat+7,venster_inskrywing->너비>=500?(한글입력?"[AF] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[AF]":"[EN]"),0xffffff,0x905020);
    }
}
static void 앞으로올리기(int waarde_VALUE){if(waarde_VALUE<0||waarde_VALUE>=4||!Windows_Lys[waarde_VALUE].살아있음)return;int 현재위치=0;while(현재위치<inskrywing_COUNT&&volgorde_VALUE[현재위치]!=waarde_VALUE)현재위치++;for(;현재위치+1<inskrywing_COUNT;현재위치++)volgorde_VALUE[현재위치]=volgorde_VALUE[현재위치+1];volgorde_VALUE[inskrywing_COUNT-1]=waarde_VALUE;Fokus=waarde_VALUE;초점알리기();다시그리기();}
static void 빈칸채우기(unsigned ry_plaas){for(unsigned karakterkode=0;karakterkode<최대열수;karakterkode++){Terminaal_inskrywing->글자칸들[ry_plaas%Geskiedenis_lyn_COUNT][karakterkode]=0;Terminaal_inskrywing->모양들[ry_plaas%Geskiedenis_lyn_COUNT][karakterkode]=Terminaal_inskrywing->전경색|(Terminaal_inskrywing->배경색<<4);}}
static void vee_uit_inhoud(void){Terminaal_inskrywing->ry_plaas=Terminaal_inskrywing->kolom_plaas=Terminaal_inskrywing->맨위=Terminaal_inskrywing->rol=0;for(unsigned 반환값=0;반환값<Geskiedenis_lyn_COUNT;반환값++)빈칸채우기(반환값);if(보이는지())Inhoud_VALUE();}
static int Skep_inskrywing(void){
    if(!보드화면기억공간())return -19;int waarde_VALUE=0;while(waarde_VALUE<4&&Windows_Lys[waarde_VALUE].살아있음)waarde_VALUE++;if(waarde_VALUE==4)return -28;
    werkskerm_bekyk=1;Terminaal_inskrywing=&Windows_Lys[waarde_VALUE];memset(Terminaal_inskrywing,0,sizeof(*Terminaal_inskrywing));Terminaal_inskrywing->살아있음=1;Terminaal_inskrywing->너비=568;Terminaal_inskrywing->높이=360;Terminaal_inskrywing->COLUMNS=68;Terminaal_inskrywing->ry_COUNT=19;Terminaal_inskrywing->x_koördinaat=12+waarde_VALUE*16;Terminaal_inskrywing->Y_koördinaat=48+waarde_VALUE*18;Terminaal_inskrywing->전경색=7;Terminaal_inskrywing->가리개보임=1;
    for(unsigned 반환값=0;반환값<Geskiedenis_lyn_COUNT;반환값++)빈칸채우기(반환값);volgorde_VALUE[inskrywing_COUNT++]=waarde_VALUE;Fokus=waarde_VALUE;대기중|=1u<<(4+waarde_VALUE);초점알리기();다시그리기();return waarde_VALUE+1;
}
static void sluit_venster(int waarde_VALUE){
    if(waarde_VALUE<0||waarde_VALUE>=4||!Windows_Lys[waarde_VALUE].살아있음)return;Windows_Lys[waarde_VALUE].살아있음=0;대기중|=1u<<(8+waarde_VALUE);
    int 현재위치=0;while(현재위치<inskrywing_COUNT&&volgorde_VALUE[현재위치]!=waarde_VALUE)현재위치++;for(;현재위치+1<inskrywing_COUNT;현재위치++)volgorde_VALUE[현재위치]=volgorde_VALUE[현재위치+1];inskrywing_COUNT--;
    if(Fokus==waarde_VALUE)Fokus=inskrywing_COUNT?volgorde_VALUE[inskrywing_COUNT-1]:-1;초점알리기();다시그리기();
}
static void 줄바꿈(void){Terminaal_inskrywing->kolom_plaas=0;Terminaal_inskrywing->ry_plaas++;if(Terminaal_inskrywing->ry_plaas>=Terminaal_inskrywing->맨위+Terminaal_inskrywing->ry_COUNT){Terminaal_inskrywing->맨위++;빈칸채우기(Terminaal_inskrywing->ry_plaas);if(보이는지())Inhoud_VALUE();}}
static void karakterkode_451f2815(unsigned karakterkode){
    if(karakterkode==13){Terminaal_inskrywing->kolom_plaas=0;return;}if(karakterkode==10){줄바꿈();return;}if(karakterkode==8){if(Terminaal_inskrywing->kolom_plaas)Terminaal_inskrywing->kolom_plaas--;return;}
    if(karakterkode==9){unsigned item_COUNT=8-Terminaal_inskrywing->kolom_plaas%8;while(item_COUNT--)karakterkode_451f2815(' ');return;}if(karakterkode<32||karakterkode==127)return;
    unsigned 너비값=넓은글자(karakterkode);if(Terminaal_inskrywing->kolom_plaas+너비값>Terminaal_inskrywing->COLUMNS)줄바꿈();
    if(Terminaal_inskrywing->글자칸들[Terminaal_inskrywing->ry_plaas%Geskiedenis_lyn_COUNT][Terminaal_inskrywing->kolom_plaas]==0xffffffffu&&Terminaal_inskrywing->kolom_plaas){Terminaal_inskrywing->글자칸들[Terminaal_inskrywing->ry_plaas%Geskiedenis_lyn_COUNT][Terminaal_inskrywing->kolom_plaas-1]=' ';그리기(Terminaal_inskrywing->ry_plaas,Terminaal_inskrywing->kolom_plaas-1);}
    if(넓은글자(Terminaal_inskrywing->글자칸들[Terminaal_inskrywing->ry_plaas%Geskiedenis_lyn_COUNT][Terminaal_inskrywing->kolom_plaas])==2&&Terminaal_inskrywing->kolom_plaas+1<Terminaal_inskrywing->COLUMNS){Terminaal_inskrywing->글자칸들[Terminaal_inskrywing->ry_plaas%Geskiedenis_lyn_COUNT][Terminaal_inskrywing->kolom_plaas+1]=' ';그리기(Terminaal_inskrywing->ry_plaas,Terminaal_inskrywing->kolom_plaas+1);}
    Terminaal_inskrywing->글자칸들[Terminaal_inskrywing->ry_plaas%Geskiedenis_lyn_COUNT][Terminaal_inskrywing->kolom_plaas]=karakterkode;Terminaal_inskrywing->모양들[Terminaal_inskrywing->ry_plaas%Geskiedenis_lyn_COUNT][Terminaal_inskrywing->kolom_plaas]=Terminaal_inskrywing->전경색|(Terminaal_inskrywing->배경색<<4);
    if(너비값==2)Terminaal_inskrywing->글자칸들[Terminaal_inskrywing->ry_plaas%Geskiedenis_lyn_COUNT][Terminaal_inskrywing->kolom_plaas+1]=0xffffffffu;
    그리기(Terminaal_inskrywing->ry_plaas,Terminaal_inskrywing->kolom_plaas);Terminaal_inskrywing->kolom_plaas+=너비값;
}
static void handvatsel_kontrole_SEQUENCE(unsigned karakterkode){
    unsigned item_COUNT=Terminaal_inskrywing->매개값[0]?Terminaal_inskrywing->매개값[0]:1;
    if(karakterkode=='m')for(unsigned 순번=0;순번<=Terminaal_inskrywing->매개색인;순번++){unsigned data_plaas=Terminaal_inskrywing->매개값[순번];if(!data_plaas){Terminaal_inskrywing->전경색=7;Terminaal_inskrywing->배경색=0;}if(data_plaas==1&&Terminaal_inskrywing->전경색<8)Terminaal_inskrywing->전경색+=8;if(data_plaas==7){unsigned 유지=Terminaal_inskrywing->전경색;Terminaal_inskrywing->전경색=Terminaal_inskrywing->배경색;Terminaal_inskrywing->배경색=유지;}if(data_plaas>=30&&data_plaas<=37)Terminaal_inskrywing->전경색=data_plaas-30;if(data_plaas>=90&&data_plaas<=97)Terminaal_inskrywing->전경색=data_plaas-90+8;if(data_plaas>=40&&data_plaas<=47)Terminaal_inskrywing->배경색=data_plaas-40;if(data_plaas>=100&&data_plaas<=107)Terminaal_inskrywing->배경색=data_plaas-100+8;if(data_plaas==39)Terminaal_inskrywing->전경색=7;if(data_plaas==49)Terminaal_inskrywing->배경색=0;}
    if(karakterkode=='J'&&(Terminaal_inskrywing->매개값[0]==2||Terminaal_inskrywing->매개값[0]==3))vee_uit_inhoud();
    if(karakterkode=='K'){unsigned 출발위치=Terminaal_inskrywing->매개값[0]==2?0:Terminaal_inskrywing->kolom_plaas,도착위치=Terminaal_inskrywing->매개값[0]==1?Terminaal_inskrywing->kolom_plaas+1:Terminaal_inskrywing->COLUMNS;if(Terminaal_inskrywing->매개값[0]==1)출발위치=0;for(unsigned 순번=출발위치;순번<도착위치&&순번<Terminaal_inskrywing->COLUMNS;순번++){
        unsigned ry_VALUE=Terminaal_inskrywing->ry_plaas%Geskiedenis_lyn_COUNT,karakter_VALUE=Terminaal_inskrywing->글자칸들[ry_VALUE][순번],vorm_VALUE=Terminaal_inskrywing->전경색|(Terminaal_inskrywing->배경색<<4);
        /* 넓은 vi 화면에서도 이미 빈 칸의 font_VALUE 화소를 되풀이해 칠하지 않는다. */
        int 바뀜=(karakter_VALUE!=0&&karakter_VALUE!=' ')||Terminaal_inskrywing->모양들[ry_VALUE][순번]!=vorm_VALUE;
        Terminaal_inskrywing->글자칸들[ry_VALUE][순번]=' ';Terminaal_inskrywing->모양들[ry_VALUE][순번]=vorm_VALUE;
        if(바뀜)그리기(Terminaal_inskrywing->ry_plaas,순번);
    }}
    if(karakterkode=='D')Terminaal_inskrywing->kolom_plaas=item_COUNT>Terminaal_inskrywing->kolom_plaas?0:Terminaal_inskrywing->kolom_plaas-item_COUNT;if(karakterkode=='C')Terminaal_inskrywing->kolom_plaas=Terminaal_inskrywing->kolom_plaas+item_COUNT>=Terminaal_inskrywing->COLUMNS?Terminaal_inskrywing->COLUMNS-1:Terminaal_inskrywing->kolom_plaas+item_COUNT;
    if(karakterkode=='G')Terminaal_inskrywing->kolom_plaas=item_COUNT>Terminaal_inskrywing->COLUMNS?Terminaal_inskrywing->COLUMNS-1:item_COUNT-1;if(karakterkode=='A')Terminaal_inskrywing->ry_plaas=item_COUNT>Terminaal_inskrywing->ry_plaas-Terminaal_inskrywing->맨위?Terminaal_inskrywing->맨위:Terminaal_inskrywing->ry_plaas-item_COUNT;
    if(karakterkode=='B')Terminaal_inskrywing->ry_plaas=Terminaal_inskrywing->ry_plaas+item_COUNT>=Terminaal_inskrywing->맨위+Terminaal_inskrywing->ry_COUNT?Terminaal_inskrywing->맨위+Terminaal_inskrywing->ry_COUNT-1:Terminaal_inskrywing->ry_plaas+item_COUNT;
    if(karakterkode=='H'||karakterkode=='f'){Terminaal_inskrywing->ry_plaas=Terminaal_inskrywing->맨위+(item_COUNT>Terminaal_inskrywing->ry_COUNT?Terminaal_inskrywing->ry_COUNT:item_COUNT)-1;unsigned x_koördinaat=Terminaal_inskrywing->매개값[1]?Terminaal_inskrywing->매개값[1]:1;Terminaal_inskrywing->kolom_plaas=(x_koördinaat>Terminaal_inskrywing->COLUMNS?Terminaal_inskrywing->COLUMNS:x_koördinaat)-1;}
    if(karakterkode=='s'){Terminaal_inskrywing->저장행=Terminaal_inskrywing->ry_plaas;Terminaal_inskrywing->저장열=Terminaal_inskrywing->kolom_plaas;}if(karakterkode=='u'){Terminaal_inskrywing->ry_plaas=Terminaal_inskrywing->저장행;Terminaal_inskrywing->kolom_plaas=Terminaal_inskrywing->저장열<Terminaal_inskrywing->COLUMNS?Terminaal_inskrywing->저장열:Terminaal_inskrywing->COLUMNS-1;}
    if((karakterkode=='h'||karakterkode=='l')&&Terminaal_inskrywing->매개값[0]==25)Terminaal_inskrywing->가리개보임=karakterkode=='h';
}
void Terminaal_greep(unsigned SECOND_VALUE){
    Terminaal_inskrywing=&Windows_Lys[출력결과];if(!Terminaal_inskrywing->살아있음)return;kappie_VALUE(0);if(Terminaal_inskrywing->rol){Terminaal_inskrywing->rol=0;if(보이는지())Inhoud_VALUE();}
    if(Terminaal_inskrywing->탈출상태==1){Terminaal_inskrywing->탈출상태=SECOND_VALUE=='['?2:0;Terminaal_inskrywing->매개색인=0;for(unsigned 순번=0;순번<4;순번++)Terminaal_inskrywing->매개값[순번]=0;}
    else if(Terminaal_inskrywing->탈출상태==2){if(SECOND_VALUE=='?'){}else if(SECOND_VALUE>='0'&&SECOND_VALUE<='9'){if(Terminaal_inskrywing->매개값[Terminaal_inskrywing->매개색인]<10000)Terminaal_inskrywing->매개값[Terminaal_inskrywing->매개색인]=Terminaal_inskrywing->매개값[Terminaal_inskrywing->매개색인]*10+SECOND_VALUE-'0';}else if(SECOND_VALUE==';'&&Terminaal_inskrywing->매개색인<3)Terminaal_inskrywing->매개색인++;else{handvatsel_kontrole_SEQUENCE(SECOND_VALUE);Terminaal_inskrywing->탈출상태=0;}}
    else if(SECOND_VALUE==27){Terminaal_inskrywing->긴부호없는값=0;Terminaal_inskrywing->탈출상태=1;}else{
        if(Terminaal_inskrywing->긴부호없는값&&(SECOND_VALUE&0xc0)!=0x80){Terminaal_inskrywing->긴부호없는값=0;karakterkode_451f2815(0xfffd);}
        if(Terminaal_inskrywing->긴부호없는값){Terminaal_inskrywing->부호없는결과=Terminaal_inskrywing->부호없는결과*64+(SECOND_VALUE&63);if(--Terminaal_inskrywing->긴부호없는값==0)karakterkode_451f2815(Terminaal_inskrywing->부호없는결과<Terminaal_inskrywing->SMALL_VALUE||Terminaal_inskrywing->부호없는결과>0x10ffff||(Terminaal_inskrywing->부호없는결과>=0xd800&&Terminaal_inskrywing->부호없는결과<=0xdfff)?0xfffd:Terminaal_inskrywing->부호없는결과);}
        else if(SECOND_VALUE<128)karakterkode_451f2815(SECOND_VALUE);else if(SECOND_VALUE>=0xc2&&SECOND_VALUE<=0xf4){Terminaal_inskrywing->긴부호없는값=SECOND_VALUE<0xe0?1:SECOND_VALUE<0xf0?2:3;Terminaal_inskrywing->부호없는결과=SECOND_VALUE&((1u<<(6-Terminaal_inskrywing->긴부호없는값))-1);Terminaal_inskrywing->SMALL_VALUE=Terminaal_inskrywing->긴부호없는값==1?128:Terminaal_inskrywing->긴부호없는값==2?2048:65536;}else karakterkode_451f2815(0xfffd);
    }kappie_VALUE(1);
}
int Terminaal_hangend(void){return 대기중!=0;}
/* 모서리 INDEX: 1 좌상, 2 우상, 3 좌하, 4 우하. */
static int herskaleer_sleep=-1,잡은모서리,잡은가로,잡은세로,처음가로,처음세로,처음너비,처음높이;
static int 가리킨창(int 가로,int Vertikaal_plaas) {
    for(int SEQUENCE_VALUE=inskrywing_COUNT-1;SEQUENCE_VALUE>=0;SEQUENCE_VALUE--){
        int waarde_VALUE=volgorde_VALUE[SEQUENCE_VALUE];Terminaal_d413d4bc *venster=&Windows_Lys[waarde_VALUE];
        if(가로>=(int)venster->x_koördinaat&&Vertikaal_plaas>=(int)venster->Y_koördinaat&&
           가로<(int)(venster->x_koördinaat+venster->너비)&&Vertikaal_plaas<(int)(venster->Y_koördinaat+venster->높이))return waarde_VALUE;
    }return -1;
}
static int 모서리찾기(int waarde_VALUE,int 가로,int Vertikaal_plaas) {
    if(waarde_VALUE<0)return 0;Terminaal_d413d4bc *venster=&Windows_Lys[waarde_VALUE];
    int 왼쪽=가로<(int)venster->x_koördinaat+8,RIGHT=가로>=(int)(venster->x_koördinaat+venster->너비)-8;
    int 위쪽=Vertikaal_plaas<(int)venster->Y_koördinaat+8,아래쪽=Vertikaal_plaas>=(int)(venster->Y_koördinaat+venster->높이)-8;
    return (왼쪽||RIGHT)&&(위쪽||아래쪽)?1+RIGHT+아래쪽*2:0;
}
static int verdeelstreep_VALUE(int VALUE,int 최소,int 최대){return VALUE<최소?최소:VALUE>최대?최대:VALUE;}
static void skuif_herskaleer(int 가로,int Vertikaal_plaas) {
    Terminaal_d413d4bc *venster=&Windows_Lys[herskaleer_sleep];int 왼쪽=처음가로,위쪽=처음세로,RIGHT=처음가로+처음너비,아래쪽=처음세로+처음높이;
    if(잡은모서리==1||잡은모서리==3)왼쪽=verdeelstreep_VALUE(처음가로+가로-잡은가로,0,RIGHT-360);
    else RIGHT=verdeelstreep_VALUE(처음가로+처음너비+가로-잡은가로,왼쪽+360,보드화면너비());
    if(잡은모서리<=2)위쪽=verdeelstreep_VALUE(처음세로+Vertikaal_plaas-잡은세로,34,아래쪽-216);
    else 아래쪽=verdeelstreep_VALUE(처음세로+처음높이+Vertikaal_plaas-잡은세로,위쪽+216,보드화면높이());
    unsigned COLUMNS=(RIGHT-왼쪽-24)/8,ry_COUNT=(아래쪽-위쪽-56)/16;
    if(venster->COLUMNS!=COLUMNS||venster->ry_COUNT!=ry_COUNT){
        venster->크기바뀜=1;venster->COLUMNS=COLUMNS;venster->ry_COUNT=ry_COUNT;
        if(venster->kolom_plaas>=COLUMNS)venster->kolom_plaas=COLUMNS-1;
        if(venster->ry_plaas>=venster->맨위+ry_COUNT)venster->맨위=venster->ry_plaas-ry_COUNT+1;
        unsigned 한도=venster->맨위;if(한도>Geskiedenis_lyn_COUNT-ry_COUNT)한도=Geskiedenis_lyn_COUNT-ry_COUNT;
        if(venster->rol>한도)venster->rol=한도;
    }
    int 옛가로=venster->x_koördinaat,옛세로=venster->Y_koördinaat,옛폭=venster->너비,옛길이=venster->높이;
    if(옛가로==왼쪽&&옛세로==위쪽&&옛폭==RIGHT-왼쪽&&옛길이==아래쪽-위쪽)return;
    venster->x_koördinaat=왼쪽;venster->Y_koördinaat=위쪽;venster->너비=RIGHT-왼쪽;venster->높이=아래쪽-위쪽;
    창자리그리기(옛가로,옛세로,옛폭,옛길이,venster);
}
void Terminaal_wyser(unsigned Volgende_item,int x_koördinaat,int Y_koördinaat){
    unsigned 눌림=Volgende_item&~단추들;단추들=Volgende_item;
    if(!werkskerm_bekyk){sleep_VALUE=-1;herskaleer_sleep=-1;bord_wyser(x_koördinaat,Y_koördinaat,1);return;}
    if(!(Volgende_item&1)){sleep_VALUE=-1;herskaleer_sleep=-1;}
    if(herskaleer_sleep>=0&&!Windows_Lys[herskaleer_sleep].살아있음)herskaleer_sleep=-1;
    if(sleep_VALUE>=0&&!Windows_Lys[sleep_VALUE].살아있음)sleep_VALUE=-1;
    if(herskaleer_sleep>=0){
        skuif_herskaleer(x_koördinaat,Y_koördinaat);bord_wyser(x_koördinaat,Y_koördinaat,잡은모서리==1||잡은모서리==4?2:3);return;
    }
    bord_wyser(x_koördinaat,Y_koördinaat,1);
    if(sleep_VALUE>=0){
        Terminaal_d413d4bc *venster=&Windows_Lys[sleep_VALUE];
        int 옛가로=venster->x_koördinaat,옛세로=venster->Y_koördinaat;
        venster->x_koördinaat=verdeelstreep_VALUE(x_koördinaat-sleep_X,0,보드화면너비()-venster->너비);
        venster->Y_koördinaat=verdeelstreep_VALUE(Y_koördinaat-sleep_Y,34,보드화면높이()-venster->높이);
        if(옛가로!=(int)venster->x_koördinaat||옛세로!=(int)venster->Y_koördinaat)창자리그리기(옛가로,옛세로,venster->너비,venster->높이,venster);
        return;
    }
    extern int 화면덮음(int,int,int);
    if(화면덮음(Fokus,x_koördinaat,Y_koördinaat)){화면가리킴(Fokus,눌림,x_koördinaat,Y_koördinaat);return;}
    int waarde_VALUE=가리킨창(x_koördinaat,Y_koördinaat),모서리=모서리찾기(waarde_VALUE,x_koördinaat,Y_koördinaat);
    if(모서리)bord_wyser(x_koördinaat,Y_koördinaat,모서리==1||모서리==4?2:3);
    if(눌림&1){
        if(모서리){
            Terminaal_d413d4bc *venster=&Windows_Lys[waarde_VALUE];herskaleer_sleep=waarde_VALUE;잡은모서리=모서리;잡은가로=x_koördinaat;잡은세로=Y_koördinaat;
            처음가로=venster->x_koördinaat;처음세로=venster->Y_koördinaat;처음너비=venster->너비;처음높이=venster->높이;
            if(waarde_VALUE!=Fokus)앞으로올리기(waarde_VALUE);return;
        }
        if(Y_koördinaat<32&&x_koördinaat>=6&&x_koördinaat<142){Skep_inskrywing();return;}
        if(Y_koördinaat<32&&x_koördinaat>=154&&x_koördinaat<602){앞으로올리기((x_koördinaat-154)/112);return;}
        if(waarde_VALUE>=0){
            Terminaal_d413d4bc *venster=&Windows_Lys[waarde_VALUE];
            if(Y_koördinaat<(int)venster->Y_koördinaat+30&&x_koördinaat>=(int)(venster->x_koördinaat+venster->너비)-32){sluit_venster(waarde_VALUE);return;}
            if(waarde_VALUE!=Fokus)앞으로올리기(waarde_VALUE);
            if(Y_koördinaat<(int)venster->Y_koördinaat+30){sleep_VALUE=waarde_VALUE;sleep_X=x_koördinaat-venster->x_koördinaat;sleep_Y=Y_koördinaat-venster->Y_koördinaat;}return;
        }
    }
    if(Fokus>=0&&(눌림&(8|16))){Terminaal_inskrywing=&Windows_Lys[Fokus];if(눌림&8){unsigned 한도=Terminaal_inskrywing->맨위;if(한도>Geskiedenis_lyn_COUNT-Terminaal_inskrywing->ry_COUNT)한도=Geskiedenis_lyn_COUNT-Terminaal_inskrywing->ry_COUNT;Terminaal_inskrywing->rol=Terminaal_inskrywing->rol+9>한도?한도:Terminaal_inskrywing->rol+9;}else Terminaal_inskrywing->rol=Terminaal_inskrywing->rol<9?0:Terminaal_inskrywing->rol-9;다시그리기();}
}
void 터미널바로가기키(unsigned 누름값){if(누름값==1)Skep_inskrywing();if(누름값==2&&inskrywing_COUNT)앞으로올리기(volgorde_VALUE[0]);if(누름값==3)sluit_venster(Fokus);}
masjien_Word bord_Terminaal(masjien_Word Aksie){
    if(Aksie==300){if(!Windows_Lys[출력결과].살아있음)return Skep_inskrywing();werkskerm_bekyk=1;다시그리기();return 0;}
    if(Aksie==0){sluit_venster(Fokus);return 0;}if(Aksie==1)return (uint32_t)Skep_inskrywing();if(Aksie==2)return Fokus>=0;
    if(Aksie==9){werkskerm_bekyk=0;return 0;}if(Aksie==7)return inskrywing_COUNT;if(Aksie==10)return Fokus+1;if(Aksie==11)return 출력결과;
    if(Aksie==13){Terminaal_d413d4bc *venster=&Windows_Lys[출력결과];return venster->살아있음?(venster->ry_COUNT<<16)|venster->COLUMNS:(19<<16)|68;}
    if(Aksie==14){unsigned VALUE=Windows_Lys[출력결과].크기바뀜;Windows_Lys[출력결과].크기바뀜=0;return VALUE;}
    if(Aksie==12){unsigned VALUE=대기중;대기중=0;return VALUE;}
    if(Aksie>=20&&Aksie<24)return Windows_Lys[Aksie-20].살아있음;
    if(Aksie>=100&&Aksie<104){출력결과=Aksie-100;Terminaal_inskrywing=&Windows_Lys[출력결과];return 0;}
    if(Aksie>=200&&Aksie<204){앞으로올리기(Aksie-200);return 0;}
    if(Aksie==3){다시그리기();return 0;}Terminaal_inskrywing=&Windows_Lys[출력결과];if(!Terminaal_inskrywing->살아있음)return 0;
    if(Aksie==4)vee_uit_inhoud();if(Aksie==5||Aksie==6){unsigned 이전=단추들;Terminaal_wyser(Aksie==5?8:16,0,0);단추들=이전;}return 1;
}
