#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* 자체 네 taga 합성과 UTF-8 터미널. 바뀐 영역의 완성 그림만 표시한다. */
#include <stdint.h>
#include <stddef.h>
typedef uintptr_t na_ura_mai_kwakwalwa_Microsoft_Word;
extern na_ura_mai_kwakwalwa_Microsoft_Word 보드화소(na_ura_mai_kwakwalwa_Microsoft_Word,na_ura_mai_kwakwalwa_Microsoft_Word,na_ura_mai_kwakwalwa_Microsoft_Word),보드화면기억공간(void);
extern void *memset(void *,int,size_t);
extern const unsigned char 터미널글꼴자료[];
#define 최대열수 237
#define 기록줄수 160
typedef struct {
    uint32_t 글자칸들[기록줄수][최대열수]; uint8_t 모양들[기록줄수][최대열수];
    unsigned 너비,높이,열수,행수,크기바뀜;
    unsigned 살아있음,gamayyar_x,Maɓallin_Y_Mai_tsarawa,행위치,열위치,맨위,Jirgawa,전경색,배경색,탈출상태,maaunin_Daraja[4],maaunin_Indes,저장행,저장열;
    unsigned 부호없는결과,긴부호없는값,작은값,대체화면,가리개보임;
} 터미널상태;
static 터미널상태 창들[4];
static int Himma=-1,출력결과,Hanyar_jejjerawa_Daraja[4],항목수,Jawo_abu_Daraja=-1,Jawo_abu_Maɓallin_X,Jawo_abu_Maɓallin_Y;
static unsigned kimiyar_bayanai_mai_jira,단추들,destof_s,한글입력;
static const uint32_t 색상들[16]={0x201a15,0x6060df,0x9dcc86,0x80cfea,0xefaf72,0xca96c9,0xceda76,0xede9df,0x858078,0x8888ff,0xb9eba7,0xa5eaff,0xffcc99,0xf0bef1,0xf0f0a0,0xffffff};
extern int 화면보임(int),화면가리킴(int,unsigned,int,int);
extern void 화면다시그림(int);
static 터미널상태 *터미널항목;
static unsigned 넓은글자(unsigned Lambar_sirrin_harafi){return Lambar_sirrin_harafi>=256?2:1;}
static void 사각영역(unsigned gamayyar_x,unsigned Maɓallin_Y_Mai_tsarawa,unsigned 너비값,unsigned 높이값,unsigned 색상){
    보드사각그림(gamayyar_x,Maɓallin_Y_Mai_tsarawa,너비값,높이값,색상);
}
void 터미널글자그림(unsigned gamayyar_x,unsigned Maɓallin_Y_Mai_tsarawa,unsigned Lambar_sirrin_harafi,unsigned 전경색,unsigned 배경색){
    unsigned 너비=넓은글자(Lambar_sirrin_harafi)*8;if(Lambar_sirrin_harafi==0xffffffffu)return;
    int 왼쪽=gamayyar_x,위쪽=Maɓallin_Y_Mai_tsarawa,폭=너비,Tsawo_Daraja=16;
    if(!보드그림범위(&왼쪽,&위쪽,&폭,&Tsawo_Daraja))return;
    if(Lambar_sirrin_harafi==' '){보드사각그림(왼쪽,위쪽,폭,Tsawo_Daraja,배경색);return;}
    unsigned 색인=Lambar_sirrin_harafi<65536?Lambar_sirrin_harafi:Lambar_sirrin_harafi>=0x1f600&&Lambar_sirrin_harafi<0x1f650?65536+Lambar_sirrin_harafi-0x1f600:0xfffd;
    const unsigned char *salon_rubutu_Daraja=터미널글꼴자료+색인*32;
    for(int Layi=위쪽;Layi<위쪽+Tsawo_Daraja;Layi++){unsigned Sabis_ɗin_Gusar_da_Tarin_Bayanan_Bayan_Bango_Jeri=salon_rubutu_Daraja[(Layi-Maɓallin_Y_Mai_tsarawa)*2]*256+salon_rubutu_Daraja[(Layi-Maɓallin_Y_Mai_tsarawa)*2+1];for(int rami_Mashigar_bayanai=왼쪽;rami_Mashigar_bayanai<왼쪽+폭;rami_Mashigar_bayanai++)보드화소(rami_Mashigar_bayanai,Layi,(Sabis_ɗin_Gusar_da_Tarin_Bayanan_Bayan_Bango_Jeri&(0x8000>>(rami_Mashigar_bayanai-gamayyar_x)))?전경색:배경색);}
}
static void Suna_tebur(unsigned gamayyar_x,unsigned Maɓallin_Y_Mai_tsarawa,const char *Zare_Tarin_bayani,unsigned 전경색,unsigned 배경색){while(*Zare_Tarin_bayani){unsigned Lambar_sirrin_harafi=(unsigned char)*Zare_Tarin_bayani++, 남은수=0;if(Lambar_sirrin_harafi>=0xc0){남은수=Lambar_sirrin_harafi<0xe0?1:Lambar_sirrin_harafi<0xf0?2:3;Lambar_sirrin_harafi&=(1u<<(6-남은수))-1;while(남은수--&&*Zare_Tarin_bayani)Lambar_sirrin_harafi=(Lambar_sirrin_harafi<<6)|((unsigned char)*Zare_Tarin_bayani++&63);}터미널글자그림(gamayyar_x,Maɓallin_Y_Mai_tsarawa,Lambar_sirrin_harafi,전경색,배경색);gamayyar_x+=넓은글자(Lambar_sirrin_harafi)*8;}}
static unsigned 첫항목(void){return 터미널항목->맨위;}
static int 보이는지(void){return 터미널항목->살아있음&&Himma>=0&&터미널항목==&창들[Himma]&&!화면보임(Himma);}
static void 그리기(unsigned 행위치,unsigned 열위치){
    if(!보이는지()||행위치<첫항목()-터미널항목->Jirgawa||행위치>=첫항목()-터미널항목->Jirgawa+터미널항목->행수||열위치>=터미널항목->열수)return;
    unsigned Lambar_sirrin_harafi=터미널항목->글자칸들[행위치%기록줄수][열위치],Zare_Tarin_bayani=터미널항목->모양들[행위치%기록줄수][열위치];
    if(넓은글자(Lambar_sirrin_harafi)==2&&열위치+1>=터미널항목->열수)Lambar_sirrin_harafi=' ';
    터미널글자그림(터미널항목->gamayyar_x+12+열위치*8,터미널항목->Maɓallin_Y_Mai_tsarawa+36+(행위치-첫항목()+터미널항목->Jirgawa)*16,Lambar_sirrin_harafi?Lambar_sirrin_harafi:' ',색상들[Zare_Tarin_bayani&15],색상들[Zare_Tarin_bayani>>4]);
}
static void Alamar_karet_Daraja(int Nuna_taga){if(!보이는지()||터미널항목->Jirgawa||터미널항목->열위치>=터미널항목->열수||터미널항목->행위치<터미널항목->맨위||터미널항목->행위치>=터미널항목->맨위+터미널항목->행수)return;
    if(!Nuna_taga||!터미널항목->가리개보임)그리기(터미널항목->행위치,터미널항목->열위치);else 사각영역(터미널항목->gamayyar_x+12+터미널항목->열위치*8,터미널항목->Maɓallin_Y_Mai_tsarawa+36+(터미널항목->행위치-터미널항목->맨위)*16+14,8,2,색상들[터미널항목->전경색]);}
static void kunshiya_Daraja(void){
    사각영역(터미널항목->gamayyar_x+12,터미널항목->Maɓallin_Y_Mai_tsarawa+36,터미널항목->열수*8,터미널항목->행수*16,색상들[0]);
    int 가로=터미널항목->gamayyar_x+12,세로=터미널항목->Maɓallin_Y_Mai_tsarawa+36,폭=터미널항목->열수*8,Tsawo_Daraja=터미널항목->행수*16;
    if(보드그림범위(&가로,&세로,&폭,&Tsawo_Daraja)){
    unsigned 첫줄=(세로-터미널항목->Maɓallin_Y_Mai_tsarawa-36)/16,끝줄=(세로+Tsawo_Daraja-터미널항목->Maɓallin_Y_Mai_tsarawa-36+15)/16;
    unsigned 첫칸=(가로-터미널항목->gamayyar_x-12)/8,끝칸=(가로+폭-터미널항목->gamayyar_x-12+7)/8;
    if(첫칸)첫칸--; /* 잘림 경계 왼쪽에서 시작한 두 rami_Mashigar_bayanai 글자도 그린다. */
    for(unsigned 반환값=첫줄;반환값<끝줄;반환값++)for(unsigned Lambar_sirrin_harafi=첫칸;Lambar_sirrin_harafi<끝칸;Lambar_sirrin_harafi++){
        unsigned 행위치=첫항목()-터미널항목->Jirgawa+반환값,Harafi_Daraja=터미널항목->글자칸들[행위치%기록줄수][Lambar_sirrin_harafi],Zare_Tarin_bayani=터미널항목->모양들[행위치%기록줄수][Lambar_sirrin_harafi];
        if(넓은글자(Harafi_Daraja)==2&&Lambar_sirrin_harafi+1>=터미널항목->열수)Harafi_Daraja=' ';
        if((Harafi_Daraja==0||Harafi_Daraja==' ')&&(Zare_Tarin_bayani>>4)==0)continue;
        터미널글자그림(터미널항목->gamayyar_x+12+Lambar_sirrin_harafi*8,터미널항목->Maɓallin_Y_Mai_tsarawa+36+반환값*16,Harafi_Daraja?Harafi_Daraja:' ',색상들[Zare_Tarin_bayani&15],색상들[Zare_Tarin_bayani>>4]);
    }}
    Suna_tebur(터미널항목->gamayyar_x+12,터미널항목->Maɓallin_Y_Mai_tsarawa+터미널항목->높이-18,터미널항목->Jirgawa?"PgDn: recent output":터미널항목->너비>=500?"F6: next | Corner + left drag: resize":"Corner + left drag: resize",0xece8e2,0x403127);Alamar_karet_Daraja(1);
}
static void 실행틀(int mai_ganewa_Daraja){
    터미널항목=&창들[mai_ganewa_Daraja];
    int 가로=터미널항목->gamayyar_x,세로=터미널항목->Maɓallin_Y_Mai_tsarawa,폭=터미널항목->너비,Tsawo_Daraja=터미널항목->높이;
    if(!보드그림범위(&가로,&세로,&폭,&Tsawo_Daraja))return;
    사각영역(터미널항목->gamayyar_x,터미널항목->Maɓallin_Y_Mai_tsarawa,터미널항목->너비,터미널항목->높이,0x403127);
    unsigned 색상=mai_ganewa_Daraja==Himma?0x905020:0x604438;사각영역(터미널항목->gamayyar_x,터미널항목->Maɓallin_Y_Mai_tsarawa,터미널항목->너비,30,색상);
    Suna_tebur(터미널항목->gamayyar_x+12,터미널항목->Maɓallin_Y_Mai_tsarawa+7,"JKOROS Terminal",0xffffff,색상);
    char 수치[2]={(char)('1'+mai_ganewa_Daraja),0};Suna_tebur(터미널항목->gamayyar_x+148,터미널항목->Maɓallin_Y_Mai_tsarawa+7,수치,0xffffff,색상);
    Suna_tebur(터미널항목->gamayyar_x+240,터미널항목->Maɓallin_Y_Mai_tsarawa+7,터미널항목->너비>=500?(한글입력?"[HA] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[HA]":"[EN]"),0xffffff,색상);
    사각영역(터미널항목->gamayyar_x+터미널항목->너비-32,터미널항목->Maɓallin_Y_Mai_tsarawa+4,26,22,0x5555b8);Suna_tebur(터미널항목->gamayyar_x+터미널항목->너비-24,터미널항목->Maɓallin_Y_Mai_tsarawa+7,"X",0xffffff,0x5555b8);
    kunshiya_Daraja();
}
static void 장면그리기(void){
    if(!destof_s)return;사각영역(0,0,보드화면너비(),보드화면높이(),0x302018);사각영역(0,0,보드화면너비(),32,0x403127);
    사각영역(6,4,136,24,0x905020);Suna_tebur(14,8,"+ New terminal",0xffffff,0x905020);
    for(int 순번=0;순번<4;순번++)if(창들[순번].살아있음){unsigned Lambar_sirrin_harafi=Himma==순번?0x905020:0x604438;사각영역(154+순번*112,4,106,24,Lambar_sirrin_harafi);Suna_tebur(160+순번*112,8,"Terminal",0xffffff,Lambar_sirrin_harafi);char Zare_Tarin_bayani[2]={(char)('1'+순번),0};Suna_tebur(232+순번*112,8,Zare_Tarin_bayani,0xffffff,Lambar_sirrin_harafi);}
    if(!항목수)Suna_tebur(140,210,"Click + New terminal to start",0xede9df,0x302018);
    for(int 순번=0;순번<항목수;순번++)실행틀(Hanyar_jejjerawa_Daraja[순번]);화면다시그림(Himma);터미널항목=&창들[출력결과];
}
static void 영역그리기(int 가로,int 세로,int 폭,int Tsawo_Daraja){
    if(!destof_s||!보드그림범위(&가로,&세로,&폭,&Tsawo_Daraja))return;
    for(int Layi=세로;Layi<세로+Tsawo_Daraja;Layi+=32){
        int 띠높이=세로+Tsawo_Daraja-Layi;if(띠높이>32)띠높이=32;
        if(보드그림시작(가로,Layi,폭,띠높이)){장면그리기();보드그림마침();}
    }
}
static void 다시그리기(void){영역그리기(0,0,보드화면너비(),보드화면높이());}
/* 서로 겹치지 않는 새 taga 영역과 이전 자리의 네 띠를 복구한다. */
static void 창자리그리기(int 가로,int 세로,int 폭,int Tsawo_Daraja,터미널상태 *taga){
    int 왼쪽=가로>(int)taga->gamayyar_x?가로:(int)taga->gamayyar_x;
    int 위쪽=세로>(int)taga->Maɓallin_Y_Mai_tsarawa?세로:(int)taga->Maɓallin_Y_Mai_tsarawa;
    int 오른쪽=가로+폭<(int)(taga->gamayyar_x+taga->너비)?가로+폭:(int)(taga->gamayyar_x+taga->너비);
    int 아래쪽=세로+Tsawo_Daraja<(int)(taga->Maɓallin_Y_Mai_tsarawa+taga->높이)?세로+Tsawo_Daraja:(int)(taga->Maɓallin_Y_Mai_tsarawa+taga->높이);
    영역그리기(taga->gamayyar_x,taga->Maɓallin_Y_Mai_tsarawa,taga->너비,taga->높이);
    if(왼쪽>=오른쪽||위쪽>=아래쪽){영역그리기(가로,세로,폭,Tsawo_Daraja);return;}
    영역그리기(가로,세로,폭,위쪽-세로);
    영역그리기(가로,아래쪽,폭,세로+Tsawo_Daraja-아래쪽);
    영역그리기(가로,위쪽,왼쪽-가로,아래쪽-위쪽);
    영역그리기(오른쪽,위쪽,가로+폭-오른쪽,아래쪽-위쪽);
}
static void 초점알리기(void){kimiyar_bayanai_mai_jira=(kimiyar_bayanai_mai_jira&~15u)|(unsigned)(Himma+1)|0x10000;}
void 터미널입력방식(unsigned 한글여부){
    한글입력=한글여부!=0;
    /* Update title bars only: a mode switch must not erase an EL0 drawing. */
    if(Himma>=0){
        터미널상태 *taga_Mashigar_bayanai=&창들[Himma];
        Suna_tebur(taga_Mashigar_bayanai->gamayyar_x+240,taga_Mashigar_bayanai->Maɓallin_Y_Mai_tsarawa+7,taga_Mashigar_bayanai->너비>=500?(한글입력?"[HA] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[HA]":"[EN]"),0xffffff,0x905020);
    }
}
static void 앞으로올리기(int mai_ganewa_Daraja){if(mai_ganewa_Daraja<0||mai_ganewa_Daraja>=4||!창들[mai_ganewa_Daraja].살아있음)return;int 현재위치=0;while(현재위치<항목수&&Hanyar_jejjerawa_Daraja[현재위치]!=mai_ganewa_Daraja)현재위치++;for(;현재위치+1<항목수;현재위치++)Hanyar_jejjerawa_Daraja[현재위치]=Hanyar_jejjerawa_Daraja[현재위치+1];Hanyar_jejjerawa_Daraja[항목수-1]=mai_ganewa_Daraja;Himma=mai_ganewa_Daraja;초점알리기();다시그리기();}
static void 빈칸채우기(unsigned 행위치){for(unsigned Lambar_sirrin_harafi=0;Lambar_sirrin_harafi<최대열수;Lambar_sirrin_harafi++){터미널항목->글자칸들[행위치%기록줄수][Lambar_sirrin_harafi]=0;터미널항목->모양들[행위치%기록줄수][Lambar_sirrin_harafi]=터미널항목->전경색|(터미널항목->배경색<<4);}}
static void Share_TOC(void){터미널항목->행위치=터미널항목->열위치=터미널항목->맨위=터미널항목->Jirgawa=0;for(unsigned 반환값=0;반환값<기록줄수;반환값++)빈칸채우기(반환값);if(보이는지())kunshiya_Daraja();}
static int ƙirƙíra_Mashigar_bayanai(void){
    if(!보드화면기억공간())return -19;int mai_ganewa_Daraja=0;while(mai_ganewa_Daraja<4&&창들[mai_ganewa_Daraja].살아있음)mai_ganewa_Daraja++;if(mai_ganewa_Daraja==4)return -28;
    destof_s=1;터미널항목=&창들[mai_ganewa_Daraja];memset(터미널항목,0,sizeof(*터미널항목));터미널항목->살아있음=1;터미널항목->너비=568;터미널항목->높이=360;터미널항목->열수=68;터미널항목->행수=19;터미널항목->gamayyar_x=12+mai_ganewa_Daraja*16;터미널항목->Maɓallin_Y_Mai_tsarawa=48+mai_ganewa_Daraja*18;터미널항목->전경색=7;터미널항목->가리개보임=1;
    for(unsigned 반환값=0;반환값<기록줄수;반환값++)빈칸채우기(반환값);Hanyar_jejjerawa_Daraja[항목수++]=mai_ganewa_Daraja;Himma=mai_ganewa_Daraja;kimiyar_bayanai_mai_jira|=1u<<(4+mai_ganewa_Daraja);초점알리기();다시그리기();return mai_ganewa_Daraja+1;
}
static void Rufe_taga(int mai_ganewa_Daraja){
    if(mai_ganewa_Daraja<0||mai_ganewa_Daraja>=4||!창들[mai_ganewa_Daraja].살아있음)return;창들[mai_ganewa_Daraja].살아있음=0;kimiyar_bayanai_mai_jira|=1u<<(8+mai_ganewa_Daraja);
    int 현재위치=0;while(현재위치<항목수&&Hanyar_jejjerawa_Daraja[현재위치]!=mai_ganewa_Daraja)현재위치++;for(;현재위치+1<항목수;현재위치++)Hanyar_jejjerawa_Daraja[현재위치]=Hanyar_jejjerawa_Daraja[현재위치+1];항목수--;
    if(Himma==mai_ganewa_Daraja)Himma=항목수?Hanyar_jejjerawa_Daraja[항목수-1]:-1;초점알리기();다시그리기();
}
static void 줄바꿈(void){터미널항목->열위치=0;터미널항목->행위치++;if(터미널항목->행위치>=터미널항목->맨위+터미널항목->행수){터미널항목->맨위++;빈칸채우기(터미널항목->행위치);if(보이는지())kunshiya_Daraja();}}
static void Lambar_sirrin_harafi_451f2815(unsigned Lambar_sirrin_harafi){
    if(Lambar_sirrin_harafi==13){터미널항목->열위치=0;return;}if(Lambar_sirrin_harafi==10){줄바꿈();return;}if(Lambar_sirrin_harafi==8){if(터미널항목->열위치)터미널항목->열위치--;return;}
    if(Lambar_sirrin_harafi==9){unsigned 개수=8-터미널항목->열위치%8;while(개수--)Lambar_sirrin_harafi_451f2815(' ');return;}if(Lambar_sirrin_harafi<32||Lambar_sirrin_harafi==127)return;
    unsigned 너비값=넓은글자(Lambar_sirrin_harafi);if(터미널항목->열위치+너비값>터미널항목->열수)줄바꿈();
    if(터미널항목->글자칸들[터미널항목->행위치%기록줄수][터미널항목->열위치]==0xffffffffu&&터미널항목->열위치){터미널항목->글자칸들[터미널항목->행위치%기록줄수][터미널항목->열위치-1]=' ';그리기(터미널항목->행위치,터미널항목->열위치-1);}
    if(넓은글자(터미널항목->글자칸들[터미널항목->행위치%기록줄수][터미널항목->열위치])==2&&터미널항목->열위치+1<터미널항목->열수){터미널항목->글자칸들[터미널항목->행위치%기록줄수][터미널항목->열위치+1]=' ';그리기(터미널항목->행위치,터미널항목->열위치+1);}
    터미널항목->글자칸들[터미널항목->행위치%기록줄수][터미널항목->열위치]=Lambar_sirrin_harafi;터미널항목->모양들[터미널항목->행위치%기록줄수][터미널항목->열위치]=터미널항목->전경색|(터미널항목->배경색<<4);
    if(너비값==2)터미널항목->글자칸들[터미널항목->행위치%기록줄수][터미널항목->열위치+1]=0xffffffffu;
    그리기(터미널항목->행위치,터미널항목->열위치);터미널항목->열위치+=너비값;
}
static void Mariki_masarrafa_JERI(unsigned Lambar_sirrin_harafi){
    unsigned 개수=터미널항목->maaunin_Daraja[0]?터미널항목->maaunin_Daraja[0]:1;
    if(Lambar_sirrin_harafi=='m')for(unsigned 순번=0;순번<=터미널항목->maaunin_Indes;순번++){unsigned 자료위치=터미널항목->maaunin_Daraja[순번];if(!자료위치){터미널항목->전경색=7;터미널항목->배경색=0;}if(자료위치==1&&터미널항목->전경색<8)터미널항목->전경색+=8;if(자료위치==7){unsigned 유지=터미널항목->전경색;터미널항목->전경색=터미널항목->배경색;터미널항목->배경색=유지;}if(자료위치>=30&&자료위치<=37)터미널항목->전경색=자료위치-30;if(자료위치>=90&&자료위치<=97)터미널항목->전경색=자료위치-90+8;if(자료위치>=40&&자료위치<=47)터미널항목->배경색=자료위치-40;if(자료위치>=100&&자료위치<=107)터미널항목->배경색=자료위치-100+8;if(자료위치==39)터미널항목->전경색=7;if(자료위치==49)터미널항목->배경색=0;}
    if(Lambar_sirrin_harafi=='J'&&(터미널항목->maaunin_Daraja[0]==2||터미널항목->maaunin_Daraja[0]==3))Share_TOC();
    if(Lambar_sirrin_harafi=='K'){unsigned 출발위치=터미널항목->maaunin_Daraja[0]==2?0:터미널항목->열위치,도착위치=터미널항목->maaunin_Daraja[0]==1?터미널항목->열위치+1:터미널항목->열수;if(터미널항목->maaunin_Daraja[0]==1)출발위치=0;for(unsigned 순번=출발위치;순번<도착위치&&순번<터미널항목->열수;순번++){
        unsigned layin_kwance_Daraja=터미널항목->행위치%기록줄수,Harafi_Daraja=터미널항목->글자칸들[layin_kwance_Daraja][순번],siffa_Daraja=터미널항목->전경색|(터미널항목->배경색<<4);
        /* 넓은 vi 화면에서도 이미 빈 칸의 salon_rubutu_Daraja 화소를 되풀이해 칠하지 않는다. */
        int 바뀜=(Harafi_Daraja!=0&&Harafi_Daraja!=' ')||터미널항목->모양들[layin_kwance_Daraja][순번]!=siffa_Daraja;
        터미널항목->글자칸들[layin_kwance_Daraja][순번]=' ';터미널항목->모양들[layin_kwance_Daraja][순번]=siffa_Daraja;
        if(바뀜)그리기(터미널항목->행위치,순번);
    }}
    if(Lambar_sirrin_harafi=='D')터미널항목->열위치=개수>터미널항목->열위치?0:터미널항목->열위치-개수;if(Lambar_sirrin_harafi=='C')터미널항목->열위치=터미널항목->열위치+개수>=터미널항목->열수?터미널항목->열수-1:터미널항목->열위치+개수;
    if(Lambar_sirrin_harafi=='G')터미널항목->열위치=개수>터미널항목->열수?터미널항목->열수-1:개수-1;if(Lambar_sirrin_harafi=='A')터미널항목->행위치=개수>터미널항목->행위치-터미널항목->맨위?터미널항목->맨위:터미널항목->행위치-개수;
    if(Lambar_sirrin_harafi=='B')터미널항목->행위치=터미널항목->행위치+개수>=터미널항목->맨위+터미널항목->행수?터미널항목->맨위+터미널항목->행수-1:터미널항목->행위치+개수;
    if(Lambar_sirrin_harafi=='H'||Lambar_sirrin_harafi=='f'){터미널항목->행위치=터미널항목->맨위+(개수>터미널항목->행수?터미널항목->행수:개수)-1;unsigned gamayyar_x=터미널항목->maaunin_Daraja[1]?터미널항목->maaunin_Daraja[1]:1;터미널항목->열위치=(gamayyar_x>터미널항목->열수?터미널항목->열수:gamayyar_x)-1;}
    if(Lambar_sirrin_harafi=='s'){터미널항목->저장행=터미널항목->행위치;터미널항목->저장열=터미널항목->열위치;}if(Lambar_sirrin_harafi=='u'){터미널항목->행위치=터미널항목->저장행;터미널항목->열위치=터미널항목->저장열<터미널항목->열수?터미널항목->저장열:터미널항목->열수-1;}
    if((Lambar_sirrin_harafi=='h'||Lambar_sirrin_harafi=='l')&&터미널항목->maaunin_Daraja[0]==25)터미널항목->가리개보임=Lambar_sirrin_harafi=='h';
}
void 터미널바이트(unsigned 둘째값){
    터미널항목=&창들[출력결과];if(!터미널항목->살아있음)return;Alamar_karet_Daraja(0);if(터미널항목->Jirgawa){터미널항목->Jirgawa=0;if(보이는지())kunshiya_Daraja();}
    if(터미널항목->탈출상태==1){터미널항목->탈출상태=둘째값=='['?2:0;터미널항목->maaunin_Indes=0;for(unsigned 순번=0;순번<4;순번++)터미널항목->maaunin_Daraja[순번]=0;}
    else if(터미널항목->탈출상태==2){if(둘째값=='?'){}else if(둘째값>='0'&&둘째값<='9'){if(터미널항목->maaunin_Daraja[터미널항목->maaunin_Indes]<10000)터미널항목->maaunin_Daraja[터미널항목->maaunin_Indes]=터미널항목->maaunin_Daraja[터미널항목->maaunin_Indes]*10+둘째값-'0';}else if(둘째값==';'&&터미널항목->maaunin_Indes<3)터미널항목->maaunin_Indes++;else{Mariki_masarrafa_JERI(둘째값);터미널항목->탈출상태=0;}}
    else if(둘째값==27){터미널항목->긴부호없는값=0;터미널항목->탈출상태=1;}else{
        if(터미널항목->긴부호없는값&&(둘째값&0xc0)!=0x80){터미널항목->긴부호없는값=0;Lambar_sirrin_harafi_451f2815(0xfffd);}
        if(터미널항목->긴부호없는값){터미널항목->부호없는결과=터미널항목->부호없는결과*64+(둘째값&63);if(--터미널항목->긴부호없는값==0)Lambar_sirrin_harafi_451f2815(터미널항목->부호없는결과<터미널항목->작은값||터미널항목->부호없는결과>0x10ffff||(터미널항목->부호없는결과>=0xd800&&터미널항목->부호없는결과<=0xdfff)?0xfffd:터미널항목->부호없는결과);}
        else if(둘째값<128)Lambar_sirrin_harafi_451f2815(둘째값);else if(둘째값>=0xc2&&둘째값<=0xf4){터미널항목->긴부호없는값=둘째값<0xe0?1:둘째값<0xf0?2:3;터미널항목->부호없는결과=둘째값&((1u<<(6-터미널항목->긴부호없는값))-1);터미널항목->작은값=터미널항목->긴부호없는값==1?128:터미널항목->긴부호없는값==2?2048:65536;}else Lambar_sirrin_harafi_451f2815(0xfffd);
    }Alamar_karet_Daraja(1);
}
int 터미널대기(void){return kimiyar_bayanai_mai_jira!=0;}
/* 모서리 Indes: 1 좌상, 2 우상, 3 좌하, 4 우하. */
static int sakegirma_Jawo_abu=-1,잡은모서리,잡은가로,잡은세로,처음가로,처음세로,처음너비,처음높이;
static int 가리킨창(int 가로,int 세로) {
    for(int JERI_Daraja=항목수-1;JERI_Daraja>=0;JERI_Daraja--){
        int mai_ganewa_Daraja=Hanyar_jejjerawa_Daraja[JERI_Daraja];터미널상태 *taga=&창들[mai_ganewa_Daraja];
        if(가로>=(int)taga->gamayyar_x&&세로>=(int)taga->Maɓallin_Y_Mai_tsarawa&&
           가로<(int)(taga->gamayyar_x+taga->너비)&&세로<(int)(taga->Maɓallin_Y_Mai_tsarawa+taga->높이))return mai_ganewa_Daraja;
    }return -1;
}
static int 모서리찾기(int mai_ganewa_Daraja,int 가로,int 세로) {
    if(mai_ganewa_Daraja<0)return 0;터미널상태 *taga=&창들[mai_ganewa_Daraja];
    int 왼쪽=가로<(int)taga->gamayyar_x+8,오른쪽=가로>=(int)(taga->gamayyar_x+taga->너비)-8;
    int 위쪽=세로<(int)taga->Maɓallin_Y_Mai_tsarawa+8,아래쪽=세로>=(int)(taga->Maɓallin_Y_Mai_tsarawa+taga->높이)-8;
    return (왼쪽||오른쪽)&&(위쪽||아래쪽)?1+오른쪽+아래쪽*2:0;
}
static int mai_rabawa_Daraja(int Daraja,int 최소,int 최대){return Daraja<최소?최소:Daraja>최대?최대:Daraja;}
static void Matsar_da_sakegirma(int 가로,int 세로) {
    터미널상태 *taga=&창들[sakegirma_Jawo_abu];int 왼쪽=처음가로,위쪽=처음세로,오른쪽=처음가로+처음너비,아래쪽=처음세로+처음높이;
    if(잡은모서리==1||잡은모서리==3)왼쪽=mai_rabawa_Daraja(처음가로+가로-잡은가로,0,오른쪽-360);
    else 오른쪽=mai_rabawa_Daraja(처음가로+처음너비+가로-잡은가로,왼쪽+360,보드화면너비());
    if(잡은모서리<=2)위쪽=mai_rabawa_Daraja(처음세로+세로-잡은세로,34,아래쪽-216);
    else 아래쪽=mai_rabawa_Daraja(처음세로+처음높이+세로-잡은세로,위쪽+216,보드화면높이());
    unsigned 열수=(오른쪽-왼쪽-24)/8,행수=(아래쪽-위쪽-56)/16;
    if(taga->열수!=열수||taga->행수!=행수){
        taga->크기바뀜=1;taga->열수=열수;taga->행수=행수;
        if(taga->열위치>=열수)taga->열위치=열수-1;
        if(taga->행위치>=taga->맨위+행수)taga->맨위=taga->행위치-행수+1;
        unsigned 한도=taga->맨위;if(한도>기록줄수-행수)한도=기록줄수-행수;
        if(taga->Jirgawa>한도)taga->Jirgawa=한도;
    }
    int 옛가로=taga->gamayyar_x,옛세로=taga->Maɓallin_Y_Mai_tsarawa,옛폭=taga->너비,옛길이=taga->높이;
    if(옛가로==왼쪽&&옛세로==위쪽&&옛폭==오른쪽-왼쪽&&옛길이==아래쪽-위쪽)return;
    taga->gamayyar_x=왼쪽;taga->Maɓallin_Y_Mai_tsarawa=위쪽;taga->너비=오른쪽-왼쪽;taga->높이=아래쪽-위쪽;
    창자리그리기(옛가로,옛세로,옛폭,옛길이,taga);
}
void 터미널가리킴(unsigned 다음,int gamayyar_x,int Maɓallin_Y_Mai_tsarawa){
    unsigned 눌림=다음&~단추들;단추들=다음;
    if(!destof_s){Jawo_abu_Daraja=-1;sakegirma_Jawo_abu=-1;보드포인터(gamayyar_x,Maɓallin_Y_Mai_tsarawa,1);return;}
    if(!(다음&1)){Jawo_abu_Daraja=-1;sakegirma_Jawo_abu=-1;}
    if(sakegirma_Jawo_abu>=0&&!창들[sakegirma_Jawo_abu].살아있음)sakegirma_Jawo_abu=-1;
    if(Jawo_abu_Daraja>=0&&!창들[Jawo_abu_Daraja].살아있음)Jawo_abu_Daraja=-1;
    if(sakegirma_Jawo_abu>=0){
        Matsar_da_sakegirma(gamayyar_x,Maɓallin_Y_Mai_tsarawa);보드포인터(gamayyar_x,Maɓallin_Y_Mai_tsarawa,잡은모서리==1||잡은모서리==4?2:3);return;
    }
    보드포인터(gamayyar_x,Maɓallin_Y_Mai_tsarawa,1);
    if(Jawo_abu_Daraja>=0){
        터미널상태 *taga=&창들[Jawo_abu_Daraja];
        int 옛가로=taga->gamayyar_x,옛세로=taga->Maɓallin_Y_Mai_tsarawa;
        taga->gamayyar_x=mai_rabawa_Daraja(gamayyar_x-Jawo_abu_Maɓallin_X,0,보드화면너비()-taga->너비);
        taga->Maɓallin_Y_Mai_tsarawa=mai_rabawa_Daraja(Maɓallin_Y_Mai_tsarawa-Jawo_abu_Maɓallin_Y,34,보드화면높이()-taga->높이);
        if(옛가로!=(int)taga->gamayyar_x||옛세로!=(int)taga->Maɓallin_Y_Mai_tsarawa)창자리그리기(옛가로,옛세로,taga->너비,taga->높이,taga);
        return;
    }
    extern int 화면덮음(int,int,int);
    if(화면덮음(Himma,gamayyar_x,Maɓallin_Y_Mai_tsarawa)){화면가리킴(Himma,눌림,gamayyar_x,Maɓallin_Y_Mai_tsarawa);return;}
    int mai_ganewa_Daraja=가리킨창(gamayyar_x,Maɓallin_Y_Mai_tsarawa),모서리=모서리찾기(mai_ganewa_Daraja,gamayyar_x,Maɓallin_Y_Mai_tsarawa);
    if(모서리)보드포인터(gamayyar_x,Maɓallin_Y_Mai_tsarawa,모서리==1||모서리==4?2:3);
    if(눌림&1){
        if(모서리){
            터미널상태 *taga=&창들[mai_ganewa_Daraja];sakegirma_Jawo_abu=mai_ganewa_Daraja;잡은모서리=모서리;잡은가로=gamayyar_x;잡은세로=Maɓallin_Y_Mai_tsarawa;
            처음가로=taga->gamayyar_x;처음세로=taga->Maɓallin_Y_Mai_tsarawa;처음너비=taga->너비;처음높이=taga->높이;
            if(mai_ganewa_Daraja!=Himma)앞으로올리기(mai_ganewa_Daraja);return;
        }
        if(Maɓallin_Y_Mai_tsarawa<32&&gamayyar_x>=6&&gamayyar_x<142){ƙirƙíra_Mashigar_bayanai();return;}
        if(Maɓallin_Y_Mai_tsarawa<32&&gamayyar_x>=154&&gamayyar_x<602){앞으로올리기((gamayyar_x-154)/112);return;}
        if(mai_ganewa_Daraja>=0){
            터미널상태 *taga=&창들[mai_ganewa_Daraja];
            if(Maɓallin_Y_Mai_tsarawa<(int)taga->Maɓallin_Y_Mai_tsarawa+30&&gamayyar_x>=(int)(taga->gamayyar_x+taga->너비)-32){Rufe_taga(mai_ganewa_Daraja);return;}
            if(mai_ganewa_Daraja!=Himma)앞으로올리기(mai_ganewa_Daraja);
            if(Maɓallin_Y_Mai_tsarawa<(int)taga->Maɓallin_Y_Mai_tsarawa+30){Jawo_abu_Daraja=mai_ganewa_Daraja;Jawo_abu_Maɓallin_X=gamayyar_x-taga->gamayyar_x;Jawo_abu_Maɓallin_Y=Maɓallin_Y_Mai_tsarawa-taga->Maɓallin_Y_Mai_tsarawa;}return;
        }
    }
    if(Himma>=0&&(눌림&(8|16))){터미널항목=&창들[Himma];if(눌림&8){unsigned 한도=터미널항목->맨위;if(한도>기록줄수-터미널항목->행수)한도=기록줄수-터미널항목->행수;터미널항목->Jirgawa=터미널항목->Jirgawa+9>한도?한도:터미널항목->Jirgawa+9;}else 터미널항목->Jirgawa=터미널항목->Jirgawa<9?0:터미널항목->Jirgawa-9;다시그리기();}
}
void 터미널바로가기키(unsigned 누름값){if(누름값==1)ƙirƙíra_Mashigar_bayanai();if(누름값==2&&항목수)앞으로올리기(Hanyar_jejjerawa_Daraja[0]);if(누름값==3)Rufe_taga(Himma);}
na_ura_mai_kwakwalwa_Microsoft_Word 보드터미널(na_ura_mai_kwakwalwa_Microsoft_Word Aiki){
    if(Aiki==300){if(!창들[출력결과].살아있음)return ƙirƙíra_Mashigar_bayanai();destof_s=1;다시그리기();return 0;}
    if(Aiki==0){Rufe_taga(Himma);return 0;}if(Aiki==1)return (uint32_t)ƙirƙíra_Mashigar_bayanai();if(Aiki==2)return Himma>=0;
    if(Aiki==9){destof_s=0;return 0;}if(Aiki==7)return 항목수;if(Aiki==10)return Himma+1;if(Aiki==11)return 출력결과;
    if(Aiki==13){터미널상태 *taga=&창들[출력결과];return taga->살아있음?(taga->행수<<16)|taga->열수:(19<<16)|68;}
    if(Aiki==14){unsigned Daraja=창들[출력결과].크기바뀜;창들[출력결과].크기바뀜=0;return Daraja;}
    if(Aiki==12){unsigned Daraja=kimiyar_bayanai_mai_jira;kimiyar_bayanai_mai_jira=0;return Daraja;}
    if(Aiki>=20&&Aiki<24)return 창들[Aiki-20].살아있음;
    if(Aiki>=100&&Aiki<104){출력결과=Aiki-100;터미널항목=&창들[출력결과];return 0;}
    if(Aiki>=200&&Aiki<204){앞으로올리기(Aiki-200);return 0;}
    if(Aiki==3){다시그리기();return 0;}터미널항목=&창들[출력결과];if(!터미널항목->살아있음)return 0;
    if(Aiki==4)Share_TOC();if(Aiki==5||Aiki==6){unsigned 이전=단추들;터미널가리킴(Aiki==5?8:16,0,0);단추들=이전;}return 1;
}
