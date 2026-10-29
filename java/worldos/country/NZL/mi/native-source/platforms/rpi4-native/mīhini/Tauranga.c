#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* 자체 네 matapihi 합성과 UTF-8 Tauranga. 바뀐 영역의 완성 그림만 표시한다. */
#include <stdint.h>
#include <stddef.h>
typedef uintptr_t mīhini_Word;
extern mīhini_Word papa_pika(mīhini_Word,mīhini_Word,mīhini_Word),보드화면기억공간(void);
extern void *memset(void *,int,size_t);
extern const unsigned char Tauranga_momotuhi[];
#define 최대열수 237
#define Hītori_hononga_COUNT 160
typedef struct {
    uint32_t 글자칸들[Hītori_hononga_COUNT][최대열수]; uint8_t 모양들[Hītori_hononga_COUNT][최대열수];
    unsigned 너비,높이,COLUMNS,ROW_COUNT,크기바뀜;
    unsigned 살아있음,taunga_x,세로좌표,ROW_tūranga,tīwae_tūranga,맨위,panuku,전경색,배경색,탈출상태,매개값[4],매개색인,저장행,저장열;
    unsigned 부호없는결과,긴부호없는값,SMALL_uara,대체화면,가리개보임;
} Tauranga_d413d4bc;
static Tauranga_d413d4bc Windows_Rārangi[4];
static int Arotahi=-1,출력결과,whakaraupapa_uara[4],tāurunga_COUNT,tō_uara=-1,끌기가로,끌기세로;
static unsigned 대기중,단추들,papamahi_tiro,한글입력;
static const uint32_t 색상들[16]={0x201a15,0x6060df,0x9dcc86,0x80cfea,0xefaf72,0xca96c9,0xceda76,0xede9df,0x858078,0x8888ff,0xb9eba7,0xa5eaff,0xffcc99,0xf0bef1,0xf0f0a0,0xffffff};
extern int 화면보임(int),화면가리킴(int,unsigned,int,int);
extern void 화면다시그림(int);
static Tauranga_d413d4bc *Tauranga_tāurunga;
static unsigned 넓은글자(unsigned waehere_pūāhua){return waehere_pūāhua>=256?2:1;}
static void 사각영역(unsigned taunga_x,unsigned 세로좌표,unsigned 너비값,unsigned 높이값,unsigned 색상){
    보드사각그림(taunga_x,세로좌표,너비값,높이값,색상);
}
void Tauranga_kiriwhi(unsigned taunga_x,unsigned 세로좌표,unsigned waehere_pūāhua,unsigned 전경색,unsigned 배경색){
    unsigned 너비=넓은글자(waehere_pūāhua)*8;if(waehere_pūāhua==0xffffffffu)return;
    int 왼쪽=taunga_x,위쪽=세로좌표,폭=너비,roa_uara=16;
    if(!보드그림범위(&왼쪽,&위쪽,&폭,&roa_uara))return;
    if(waehere_pūāhua==' '){보드사각그림(왼쪽,위쪽,폭,roa_uara,배경색);return;}
    unsigned Rapu_INDEX=waehere_pūāhua<65536?waehere_pūāhua:waehere_pūāhua>=0x1f600&&waehere_pūāhua<0x1f650?65536+waehere_pūāhua-0x1f600:0xfffd;
    const unsigned char *momotuhi_uara=Tauranga_momotuhi+Rapu_INDEX*32;
    for(int hononga=위쪽;hononga<위쪽+roa_uara;hononga++){unsigned 비트들=momotuhi_uara[(hononga-세로좌표)*2]*256+momotuhi_uara[(hononga-세로좌표)*2+1];for(int kāniwha_tāurunga=왼쪽;kāniwha_tāurunga<왼쪽+폭;kāniwha_tāurunga++)papa_pika(kāniwha_tāurunga,hononga,(비트들&(0x8000>>(kāniwha_tāurunga-taunga_x)))?전경색:배경색);}
}
static void ingoa_ripanga(unsigned taunga_x,unsigned 세로좌표,const char *aho_raraunga,unsigned 전경색,unsigned 배경색){while(*aho_raraunga){unsigned waehere_pūāhua=(unsigned char)*aho_raraunga++, 남은수=0;if(waehere_pūāhua>=0xc0){남은수=waehere_pūāhua<0xe0?1:waehere_pūāhua<0xf0?2:3;waehere_pūāhua&=(1u<<(6-남은수))-1;while(남은수--&&*aho_raraunga)waehere_pūāhua=(waehere_pūāhua<<6)|((unsigned char)*aho_raraunga++&63);}Tauranga_kiriwhi(taunga_x,세로좌표,waehere_pūāhua,전경색,배경색);taunga_x+=넓은글자(waehere_pūāhua)*8;}}
static unsigned 첫항목(void){return Tauranga_tāurunga->맨위;}
static int 보이는지(void){return Tauranga_tāurunga->살아있음&&Arotahi>=0&&Tauranga_tāurunga==&Windows_Rārangi[Arotahi]&&!화면보임(Arotahi);}
static void 그리기(unsigned ROW_tūranga,unsigned tīwae_tūranga){
    if(!보이는지()||ROW_tūranga<첫항목()-Tauranga_tāurunga->panuku||ROW_tūranga>=첫항목()-Tauranga_tāurunga->panuku+Tauranga_tāurunga->ROW_COUNT||tīwae_tūranga>=Tauranga_tāurunga->COLUMNS)return;
    unsigned waehere_pūāhua=Tauranga_tāurunga->글자칸들[ROW_tūranga%Hītori_hononga_COUNT][tīwae_tūranga],aho_raraunga=Tauranga_tāurunga->모양들[ROW_tūranga%Hītori_hononga_COUNT][tīwae_tūranga];
    if(넓은글자(waehere_pūāhua)==2&&tīwae_tūranga+1>=Tauranga_tāurunga->COLUMNS)waehere_pūāhua=' ';
    Tauranga_kiriwhi(Tauranga_tāurunga->taunga_x+12+tīwae_tūranga*8,Tauranga_tāurunga->세로좌표+36+(ROW_tūranga-첫항목()+Tauranga_tāurunga->panuku)*16,waehere_pūāhua?waehere_pūāhua:' ',색상들[aho_raraunga&15],색상들[aho_raraunga>>4]);
}
static void hiwi_uara(int whakaatu_matapihi){if(!보이는지()||Tauranga_tāurunga->panuku||Tauranga_tāurunga->tīwae_tūranga>=Tauranga_tāurunga->COLUMNS||Tauranga_tāurunga->ROW_tūranga<Tauranga_tāurunga->맨위||Tauranga_tāurunga->ROW_tūranga>=Tauranga_tāurunga->맨위+Tauranga_tāurunga->ROW_COUNT)return;
    if(!whakaatu_matapihi||!Tauranga_tāurunga->가리개보임)그리기(Tauranga_tāurunga->ROW_tūranga,Tauranga_tāurunga->tīwae_tūranga);else 사각영역(Tauranga_tāurunga->taunga_x+12+Tauranga_tāurunga->tīwae_tūranga*8,Tauranga_tāurunga->세로좌표+36+(Tauranga_tāurunga->ROW_tūranga-Tauranga_tāurunga->맨위)*16+14,8,2,색상들[Tauranga_tāurunga->전경색]);}
static void Ihirangi_uara(void){
    사각영역(Tauranga_tāurunga->taunga_x+12,Tauranga_tāurunga->세로좌표+36,Tauranga_tāurunga->COLUMNS*8,Tauranga_tāurunga->ROW_COUNT*16,색상들[0]);
    int 가로=Tauranga_tāurunga->taunga_x+12,Poutū_tūranga=Tauranga_tāurunga->세로좌표+36,폭=Tauranga_tāurunga->COLUMNS*8,roa_uara=Tauranga_tāurunga->ROW_COUNT*16;
    if(보드그림범위(&가로,&Poutū_tūranga,&폭,&roa_uara)){
    unsigned 첫줄=(Poutū_tūranga-Tauranga_tāurunga->세로좌표-36)/16,끝줄=(Poutū_tūranga+roa_uara-Tauranga_tāurunga->세로좌표-36+15)/16;
    unsigned 첫칸=(가로-Tauranga_tāurunga->taunga_x-12)/8,끝칸=(가로+폭-Tauranga_tāurunga->taunga_x-12+7)/8;
    if(첫칸)첫칸--; /* 잘림 경계 왼쪽에서 시작한 두 kāniwha_tāurunga 글자도 그린다. */
    for(unsigned 반환값=첫줄;반환값<끝줄;반환값++)for(unsigned waehere_pūāhua=첫칸;waehere_pūāhua<끝칸;waehere_pūāhua++){
        unsigned ROW_tūranga=첫항목()-Tauranga_tāurunga->panuku+반환값,pūāhua_uara=Tauranga_tāurunga->글자칸들[ROW_tūranga%Hītori_hononga_COUNT][waehere_pūāhua],aho_raraunga=Tauranga_tāurunga->모양들[ROW_tūranga%Hītori_hononga_COUNT][waehere_pūāhua];
        if(넓은글자(pūāhua_uara)==2&&waehere_pūāhua+1>=Tauranga_tāurunga->COLUMNS)pūāhua_uara=' ';
        if((pūāhua_uara==0||pūāhua_uara==' ')&&(aho_raraunga>>4)==0)continue;
        Tauranga_kiriwhi(Tauranga_tāurunga->taunga_x+12+waehere_pūāhua*8,Tauranga_tāurunga->세로좌표+36+반환값*16,pūāhua_uara?pūāhua_uara:' ',색상들[aho_raraunga&15],색상들[aho_raraunga>>4]);
    }}
    ingoa_ripanga(Tauranga_tāurunga->taunga_x+12,Tauranga_tāurunga->세로좌표+Tauranga_tāurunga->높이-18,Tauranga_tāurunga->panuku?"PgDn: recent output":Tauranga_tāurunga->너비>=500?"F6: next | Corner + left drag: resize":"Corner + left drag: resize",0xece8e2,0x403127);hiwi_uara(1);
}
static void 실행틀(int pūtāutu_uara){
    Tauranga_tāurunga=&Windows_Rārangi[pūtāutu_uara];
    int 가로=Tauranga_tāurunga->taunga_x,Poutū_tūranga=Tauranga_tāurunga->세로좌표,폭=Tauranga_tāurunga->너비,roa_uara=Tauranga_tāurunga->높이;
    if(!보드그림범위(&가로,&Poutū_tūranga,&폭,&roa_uara))return;
    사각영역(Tauranga_tāurunga->taunga_x,Tauranga_tāurunga->세로좌표,Tauranga_tāurunga->너비,Tauranga_tāurunga->높이,0x403127);
    unsigned 색상=pūtāutu_uara==Arotahi?0x905020:0x604438;사각영역(Tauranga_tāurunga->taunga_x,Tauranga_tāurunga->세로좌표,Tauranga_tāurunga->너비,30,색상);
    ingoa_ripanga(Tauranga_tāurunga->taunga_x+12,Tauranga_tāurunga->세로좌표+7,"JKOROS Terminal",0xffffff,색상);
    char 수치[2]={(char)('1'+pūtāutu_uara),0};ingoa_ripanga(Tauranga_tāurunga->taunga_x+148,Tauranga_tāurunga->세로좌표+7,수치,0xffffff,색상);
    ingoa_ripanga(Tauranga_tāurunga->taunga_x+240,Tauranga_tāurunga->세로좌표+7,Tauranga_tāurunga->너비>=500?(한글입력?"[MI] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[MI]":"[EN]"),0xffffff,색상);
    사각영역(Tauranga_tāurunga->taunga_x+Tauranga_tāurunga->너비-32,Tauranga_tāurunga->세로좌표+4,26,22,0x5555b8);ingoa_ripanga(Tauranga_tāurunga->taunga_x+Tauranga_tāurunga->너비-24,Tauranga_tāurunga->세로좌표+7,"X",0xffffff,0x5555b8);
    Ihirangi_uara();
}
static void 장면그리기(void){
    if(!papamahi_tiro)return;사각영역(0,0,보드화면너비(),보드화면높이(),0x302018);사각영역(0,0,보드화면너비(),32,0x403127);
    사각영역(6,4,136,24,0x905020);ingoa_ripanga(14,8,"+ New terminal",0xffffff,0x905020);
    for(int 순번=0;순번<4;순번++)if(Windows_Rārangi[순번].살아있음){unsigned waehere_pūāhua=Arotahi==순번?0x905020:0x604438;사각영역(154+순번*112,4,106,24,waehere_pūāhua);ingoa_ripanga(160+순번*112,8,"Terminal",0xffffff,waehere_pūāhua);char aho_raraunga[2]={(char)('1'+순번),0};ingoa_ripanga(232+순번*112,8,aho_raraunga,0xffffff,waehere_pūāhua);}
    if(!tāurunga_COUNT)ingoa_ripanga(140,210,"Click + New terminal to start",0xede9df,0x302018);
    for(int 순번=0;순번<tāurunga_COUNT;순번++)실행틀(whakaraupapa_uara[순번]);화면다시그림(Arotahi);Tauranga_tāurunga=&Windows_Rārangi[출력결과];
}
static void 영역그리기(int 가로,int Poutū_tūranga,int 폭,int roa_uara){
    if(!papamahi_tiro||!보드그림범위(&가로,&Poutū_tūranga,&폭,&roa_uara))return;
    for(int hononga=Poutū_tūranga;hononga<Poutū_tūranga+roa_uara;hononga+=32){
        int 띠높이=Poutū_tūranga+roa_uara-hononga;if(띠높이>32)띠높이=32;
        if(papa_Start_tātuhi(가로,hononga,폭,띠높이)){장면그리기();papa_Mutu_tātuhi();}
    }
}
static void 다시그리기(void){영역그리기(0,0,보드화면너비(),보드화면높이());}
/* 서로 겹치지 않는 새 matapihi 영역과 이전 자리의 네 띠를 복구한다. */
static void 창자리그리기(int 가로,int Poutū_tūranga,int 폭,int roa_uara,Tauranga_d413d4bc *matapihi){
    int 왼쪽=가로>(int)matapihi->taunga_x?가로:(int)matapihi->taunga_x;
    int 위쪽=Poutū_tūranga>(int)matapihi->세로좌표?Poutū_tūranga:(int)matapihi->세로좌표;
    int RIGHT=가로+폭<(int)(matapihi->taunga_x+matapihi->너비)?가로+폭:(int)(matapihi->taunga_x+matapihi->너비);
    int 아래쪽=Poutū_tūranga+roa_uara<(int)(matapihi->세로좌표+matapihi->높이)?Poutū_tūranga+roa_uara:(int)(matapihi->세로좌표+matapihi->높이);
    영역그리기(matapihi->taunga_x,matapihi->세로좌표,matapihi->너비,matapihi->높이);
    if(왼쪽>=RIGHT||위쪽>=아래쪽){영역그리기(가로,Poutū_tūranga,폭,roa_uara);return;}
    영역그리기(가로,Poutū_tūranga,폭,위쪽-Poutū_tūranga);
    영역그리기(가로,아래쪽,폭,Poutū_tūranga+roa_uara-아래쪽);
    영역그리기(가로,위쪽,왼쪽-가로,아래쪽-위쪽);
    영역그리기(RIGHT,위쪽,가로+폭-RIGHT,아래쪽-위쪽);
}
static void 초점알리기(void){대기중=(대기중&~15u)|(unsigned)(Arotahi+1)|0x10000;}
void 터미널입력방식(unsigned 한글여부){
    한글입력=한글여부!=0;
    /* Update title bars only: a mode switch must not erase an EL0 drawing. */
    if(Arotahi>=0){
        Tauranga_d413d4bc *matapihi_tāurunga=&Windows_Rārangi[Arotahi];
        ingoa_ripanga(matapihi_tāurunga->taunga_x+240,matapihi_tāurunga->세로좌표+7,matapihi_tāurunga->너비>=500?(한글입력?"[MI] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[MI]":"[EN]"),0xffffff,0x905020);
    }
}
static void 앞으로올리기(int pūtāutu_uara){if(pūtāutu_uara<0||pūtāutu_uara>=4||!Windows_Rārangi[pūtāutu_uara].살아있음)return;int 현재위치=0;while(현재위치<tāurunga_COUNT&&whakaraupapa_uara[현재위치]!=pūtāutu_uara)현재위치++;for(;현재위치+1<tāurunga_COUNT;현재위치++)whakaraupapa_uara[현재위치]=whakaraupapa_uara[현재위치+1];whakaraupapa_uara[tāurunga_COUNT-1]=pūtāutu_uara;Arotahi=pūtāutu_uara;초점알리기();다시그리기();}
static void 빈칸채우기(unsigned ROW_tūranga){for(unsigned waehere_pūāhua=0;waehere_pūāhua<최대열수;waehere_pūāhua++){Tauranga_tāurunga->글자칸들[ROW_tūranga%Hītori_hononga_COUNT][waehere_pūāhua]=0;Tauranga_tāurunga->모양들[ROW_tūranga%Hītori_hononga_COUNT][waehere_pūāhua]=Tauranga_tāurunga->전경색|(Tauranga_tāurunga->배경색<<4);}}
static void ūkui_IRI(void){Tauranga_tāurunga->ROW_tūranga=Tauranga_tāurunga->tīwae_tūranga=Tauranga_tāurunga->맨위=Tauranga_tāurunga->panuku=0;for(unsigned 반환값=0;반환값<Hītori_hononga_COUNT;반환값++)빈칸채우기(반환값);if(보이는지())Ihirangi_uara();}
static int Waihanga_tāurunga(void){
    if(!보드화면기억공간())return -19;int pūtāutu_uara=0;while(pūtāutu_uara<4&&Windows_Rārangi[pūtāutu_uara].살아있음)pūtāutu_uara++;if(pūtāutu_uara==4)return -28;
    papamahi_tiro=1;Tauranga_tāurunga=&Windows_Rārangi[pūtāutu_uara];memset(Tauranga_tāurunga,0,sizeof(*Tauranga_tāurunga));Tauranga_tāurunga->살아있음=1;Tauranga_tāurunga->너비=568;Tauranga_tāurunga->높이=360;Tauranga_tāurunga->COLUMNS=68;Tauranga_tāurunga->ROW_COUNT=19;Tauranga_tāurunga->taunga_x=12+pūtāutu_uara*16;Tauranga_tāurunga->세로좌표=48+pūtāutu_uara*18;Tauranga_tāurunga->전경색=7;Tauranga_tāurunga->가리개보임=1;
    for(unsigned 반환값=0;반환값<Hītori_hononga_COUNT;반환값++)빈칸채우기(반환값);whakaraupapa_uara[tāurunga_COUNT++]=pūtāutu_uara;Arotahi=pūtāutu_uara;대기중|=1u<<(4+pūtāutu_uara);초점알리기();다시그리기();return pūtāutu_uara+1;
}
static void kati_matapihi(int pūtāutu_uara){
    if(pūtāutu_uara<0||pūtāutu_uara>=4||!Windows_Rārangi[pūtāutu_uara].살아있음)return;Windows_Rārangi[pūtāutu_uara].살아있음=0;대기중|=1u<<(8+pūtāutu_uara);
    int 현재위치=0;while(현재위치<tāurunga_COUNT&&whakaraupapa_uara[현재위치]!=pūtāutu_uara)현재위치++;for(;현재위치+1<tāurunga_COUNT;현재위치++)whakaraupapa_uara[현재위치]=whakaraupapa_uara[현재위치+1];tāurunga_COUNT--;
    if(Arotahi==pūtāutu_uara)Arotahi=tāurunga_COUNT?whakaraupapa_uara[tāurunga_COUNT-1]:-1;초점알리기();다시그리기();
}
static void 줄바꿈(void){Tauranga_tāurunga->tīwae_tūranga=0;Tauranga_tāurunga->ROW_tūranga++;if(Tauranga_tāurunga->ROW_tūranga>=Tauranga_tāurunga->맨위+Tauranga_tāurunga->ROW_COUNT){Tauranga_tāurunga->맨위++;빈칸채우기(Tauranga_tāurunga->ROW_tūranga);if(보이는지())Ihirangi_uara();}}
static void waehere_pūāhua_451f2815(unsigned waehere_pūāhua){
    if(waehere_pūāhua==13){Tauranga_tāurunga->tīwae_tūranga=0;return;}if(waehere_pūāhua==10){줄바꿈();return;}if(waehere_pūāhua==8){if(Tauranga_tāurunga->tīwae_tūranga)Tauranga_tāurunga->tīwae_tūranga--;return;}
    if(waehere_pūāhua==9){unsigned tuemi_COUNT=8-Tauranga_tāurunga->tīwae_tūranga%8;while(tuemi_COUNT--)waehere_pūāhua_451f2815(' ');return;}if(waehere_pūāhua<32||waehere_pūāhua==127)return;
    unsigned 너비값=넓은글자(waehere_pūāhua);if(Tauranga_tāurunga->tīwae_tūranga+너비값>Tauranga_tāurunga->COLUMNS)줄바꿈();
    if(Tauranga_tāurunga->글자칸들[Tauranga_tāurunga->ROW_tūranga%Hītori_hononga_COUNT][Tauranga_tāurunga->tīwae_tūranga]==0xffffffffu&&Tauranga_tāurunga->tīwae_tūranga){Tauranga_tāurunga->글자칸들[Tauranga_tāurunga->ROW_tūranga%Hītori_hononga_COUNT][Tauranga_tāurunga->tīwae_tūranga-1]=' ';그리기(Tauranga_tāurunga->ROW_tūranga,Tauranga_tāurunga->tīwae_tūranga-1);}
    if(넓은글자(Tauranga_tāurunga->글자칸들[Tauranga_tāurunga->ROW_tūranga%Hītori_hononga_COUNT][Tauranga_tāurunga->tīwae_tūranga])==2&&Tauranga_tāurunga->tīwae_tūranga+1<Tauranga_tāurunga->COLUMNS){Tauranga_tāurunga->글자칸들[Tauranga_tāurunga->ROW_tūranga%Hītori_hononga_COUNT][Tauranga_tāurunga->tīwae_tūranga+1]=' ';그리기(Tauranga_tāurunga->ROW_tūranga,Tauranga_tāurunga->tīwae_tūranga+1);}
    Tauranga_tāurunga->글자칸들[Tauranga_tāurunga->ROW_tūranga%Hītori_hononga_COUNT][Tauranga_tāurunga->tīwae_tūranga]=waehere_pūāhua;Tauranga_tāurunga->모양들[Tauranga_tāurunga->ROW_tūranga%Hītori_hononga_COUNT][Tauranga_tāurunga->tīwae_tūranga]=Tauranga_tāurunga->전경색|(Tauranga_tāurunga->배경색<<4);
    if(너비값==2)Tauranga_tāurunga->글자칸들[Tauranga_tāurunga->ROW_tūranga%Hītori_hononga_COUNT][Tauranga_tāurunga->tīwae_tūranga+1]=0xffffffffu;
    그리기(Tauranga_tāurunga->ROW_tūranga,Tauranga_tāurunga->tīwae_tūranga);Tauranga_tāurunga->tīwae_tūranga+=너비값;
}
static void raweke_mana_SEQUENCE(unsigned waehere_pūāhua){
    unsigned tuemi_COUNT=Tauranga_tāurunga->매개값[0]?Tauranga_tāurunga->매개값[0]:1;
    if(waehere_pūāhua=='m')for(unsigned 순번=0;순번<=Tauranga_tāurunga->매개색인;순번++){unsigned raraunga_tūranga=Tauranga_tāurunga->매개값[순번];if(!raraunga_tūranga){Tauranga_tāurunga->전경색=7;Tauranga_tāurunga->배경색=0;}if(raraunga_tūranga==1&&Tauranga_tāurunga->전경색<8)Tauranga_tāurunga->전경색+=8;if(raraunga_tūranga==7){unsigned 유지=Tauranga_tāurunga->전경색;Tauranga_tāurunga->전경색=Tauranga_tāurunga->배경색;Tauranga_tāurunga->배경색=유지;}if(raraunga_tūranga>=30&&raraunga_tūranga<=37)Tauranga_tāurunga->전경색=raraunga_tūranga-30;if(raraunga_tūranga>=90&&raraunga_tūranga<=97)Tauranga_tāurunga->전경색=raraunga_tūranga-90+8;if(raraunga_tūranga>=40&&raraunga_tūranga<=47)Tauranga_tāurunga->배경색=raraunga_tūranga-40;if(raraunga_tūranga>=100&&raraunga_tūranga<=107)Tauranga_tāurunga->배경색=raraunga_tūranga-100+8;if(raraunga_tūranga==39)Tauranga_tāurunga->전경색=7;if(raraunga_tūranga==49)Tauranga_tāurunga->배경색=0;}
    if(waehere_pūāhua=='J'&&(Tauranga_tāurunga->매개값[0]==2||Tauranga_tāurunga->매개값[0]==3))ūkui_IRI();
    if(waehere_pūāhua=='K'){unsigned 출발위치=Tauranga_tāurunga->매개값[0]==2?0:Tauranga_tāurunga->tīwae_tūranga,도착위치=Tauranga_tāurunga->매개값[0]==1?Tauranga_tāurunga->tīwae_tūranga+1:Tauranga_tāurunga->COLUMNS;if(Tauranga_tāurunga->매개값[0]==1)출발위치=0;for(unsigned 순번=출발위치;순번<도착위치&&순번<Tauranga_tāurunga->COLUMNS;순번++){
        unsigned ROW_uara=Tauranga_tāurunga->ROW_tūranga%Hītori_hononga_COUNT,pūāhua_uara=Tauranga_tāurunga->글자칸들[ROW_uara][순번],hanga_uara=Tauranga_tāurunga->전경색|(Tauranga_tāurunga->배경색<<4);
        /* 넓은 vi 화면에서도 이미 빈 칸의 momotuhi_uara 화소를 되풀이해 칠하지 않는다. */
        int 바뀜=(pūāhua_uara!=0&&pūāhua_uara!=' ')||Tauranga_tāurunga->모양들[ROW_uara][순번]!=hanga_uara;
        Tauranga_tāurunga->글자칸들[ROW_uara][순번]=' ';Tauranga_tāurunga->모양들[ROW_uara][순번]=hanga_uara;
        if(바뀜)그리기(Tauranga_tāurunga->ROW_tūranga,순번);
    }}
    if(waehere_pūāhua=='D')Tauranga_tāurunga->tīwae_tūranga=tuemi_COUNT>Tauranga_tāurunga->tīwae_tūranga?0:Tauranga_tāurunga->tīwae_tūranga-tuemi_COUNT;if(waehere_pūāhua=='C')Tauranga_tāurunga->tīwae_tūranga=Tauranga_tāurunga->tīwae_tūranga+tuemi_COUNT>=Tauranga_tāurunga->COLUMNS?Tauranga_tāurunga->COLUMNS-1:Tauranga_tāurunga->tīwae_tūranga+tuemi_COUNT;
    if(waehere_pūāhua=='G')Tauranga_tāurunga->tīwae_tūranga=tuemi_COUNT>Tauranga_tāurunga->COLUMNS?Tauranga_tāurunga->COLUMNS-1:tuemi_COUNT-1;if(waehere_pūāhua=='A')Tauranga_tāurunga->ROW_tūranga=tuemi_COUNT>Tauranga_tāurunga->ROW_tūranga-Tauranga_tāurunga->맨위?Tauranga_tāurunga->맨위:Tauranga_tāurunga->ROW_tūranga-tuemi_COUNT;
    if(waehere_pūāhua=='B')Tauranga_tāurunga->ROW_tūranga=Tauranga_tāurunga->ROW_tūranga+tuemi_COUNT>=Tauranga_tāurunga->맨위+Tauranga_tāurunga->ROW_COUNT?Tauranga_tāurunga->맨위+Tauranga_tāurunga->ROW_COUNT-1:Tauranga_tāurunga->ROW_tūranga+tuemi_COUNT;
    if(waehere_pūāhua=='H'||waehere_pūāhua=='f'){Tauranga_tāurunga->ROW_tūranga=Tauranga_tāurunga->맨위+(tuemi_COUNT>Tauranga_tāurunga->ROW_COUNT?Tauranga_tāurunga->ROW_COUNT:tuemi_COUNT)-1;unsigned taunga_x=Tauranga_tāurunga->매개값[1]?Tauranga_tāurunga->매개값[1]:1;Tauranga_tāurunga->tīwae_tūranga=(taunga_x>Tauranga_tāurunga->COLUMNS?Tauranga_tāurunga->COLUMNS:taunga_x)-1;}
    if(waehere_pūāhua=='s'){Tauranga_tāurunga->저장행=Tauranga_tāurunga->ROW_tūranga;Tauranga_tāurunga->저장열=Tauranga_tāurunga->tīwae_tūranga;}if(waehere_pūāhua=='u'){Tauranga_tāurunga->ROW_tūranga=Tauranga_tāurunga->저장행;Tauranga_tāurunga->tīwae_tūranga=Tauranga_tāurunga->저장열<Tauranga_tāurunga->COLUMNS?Tauranga_tāurunga->저장열:Tauranga_tāurunga->COLUMNS-1;}
    if((waehere_pūāhua=='h'||waehere_pūāhua=='l')&&Tauranga_tāurunga->매개값[0]==25)Tauranga_tāurunga->가리개보임=waehere_pūāhua=='h';
}
void Tauranga_paita(unsigned SECOND_uara){
    Tauranga_tāurunga=&Windows_Rārangi[출력결과];if(!Tauranga_tāurunga->살아있음)return;hiwi_uara(0);if(Tauranga_tāurunga->panuku){Tauranga_tāurunga->panuku=0;if(보이는지())Ihirangi_uara();}
    if(Tauranga_tāurunga->탈출상태==1){Tauranga_tāurunga->탈출상태=SECOND_uara=='['?2:0;Tauranga_tāurunga->매개색인=0;for(unsigned 순번=0;순번<4;순번++)Tauranga_tāurunga->매개값[순번]=0;}
    else if(Tauranga_tāurunga->탈출상태==2){if(SECOND_uara=='?'){}else if(SECOND_uara>='0'&&SECOND_uara<='9'){if(Tauranga_tāurunga->매개값[Tauranga_tāurunga->매개색인]<10000)Tauranga_tāurunga->매개값[Tauranga_tāurunga->매개색인]=Tauranga_tāurunga->매개값[Tauranga_tāurunga->매개색인]*10+SECOND_uara-'0';}else if(SECOND_uara==';'&&Tauranga_tāurunga->매개색인<3)Tauranga_tāurunga->매개색인++;else{raweke_mana_SEQUENCE(SECOND_uara);Tauranga_tāurunga->탈출상태=0;}}
    else if(SECOND_uara==27){Tauranga_tāurunga->긴부호없는값=0;Tauranga_tāurunga->탈출상태=1;}else{
        if(Tauranga_tāurunga->긴부호없는값&&(SECOND_uara&0xc0)!=0x80){Tauranga_tāurunga->긴부호없는값=0;waehere_pūāhua_451f2815(0xfffd);}
        if(Tauranga_tāurunga->긴부호없는값){Tauranga_tāurunga->부호없는결과=Tauranga_tāurunga->부호없는결과*64+(SECOND_uara&63);if(--Tauranga_tāurunga->긴부호없는값==0)waehere_pūāhua_451f2815(Tauranga_tāurunga->부호없는결과<Tauranga_tāurunga->SMALL_uara||Tauranga_tāurunga->부호없는결과>0x10ffff||(Tauranga_tāurunga->부호없는결과>=0xd800&&Tauranga_tāurunga->부호없는결과<=0xdfff)?0xfffd:Tauranga_tāurunga->부호없는결과);}
        else if(SECOND_uara<128)waehere_pūāhua_451f2815(SECOND_uara);else if(SECOND_uara>=0xc2&&SECOND_uara<=0xf4){Tauranga_tāurunga->긴부호없는값=SECOND_uara<0xe0?1:SECOND_uara<0xf0?2:3;Tauranga_tāurunga->부호없는결과=SECOND_uara&((1u<<(6-Tauranga_tāurunga->긴부호없는값))-1);Tauranga_tāurunga->SMALL_uara=Tauranga_tāurunga->긴부호없는값==1?128:Tauranga_tāurunga->긴부호없는값==2?2048:65536;}else waehere_pūāhua_451f2815(0xfffd);
    }hiwi_uara(1);
}
int Tauranga_tārewa(void){return 대기중!=0;}
/* 모서리 INDEX: 1 좌상, 2 우상, 3 좌하, 4 우하. */
static int whakarahi_anō_tō=-1,잡은모서리,잡은가로,잡은세로,처음가로,처음세로,처음너비,처음높이;
static int 가리킨창(int 가로,int Poutū_tūranga) {
    for(int SEQUENCE_uara=tāurunga_COUNT-1;SEQUENCE_uara>=0;SEQUENCE_uara--){
        int pūtāutu_uara=whakaraupapa_uara[SEQUENCE_uara];Tauranga_d413d4bc *matapihi=&Windows_Rārangi[pūtāutu_uara];
        if(가로>=(int)matapihi->taunga_x&&Poutū_tūranga>=(int)matapihi->세로좌표&&
           가로<(int)(matapihi->taunga_x+matapihi->너비)&&Poutū_tūranga<(int)(matapihi->세로좌표+matapihi->높이))return pūtāutu_uara;
    }return -1;
}
static int 모서리찾기(int pūtāutu_uara,int 가로,int Poutū_tūranga) {
    if(pūtāutu_uara<0)return 0;Tauranga_d413d4bc *matapihi=&Windows_Rārangi[pūtāutu_uara];
    int 왼쪽=가로<(int)matapihi->taunga_x+8,RIGHT=가로>=(int)(matapihi->taunga_x+matapihi->너비)-8;
    int 위쪽=Poutū_tūranga<(int)matapihi->세로좌표+8,아래쪽=Poutū_tūranga>=(int)(matapihi->세로좌표+matapihi->높이)-8;
    return (왼쪽||RIGHT)&&(위쪽||아래쪽)?1+RIGHT+아래쪽*2:0;
}
static int whakawehe_uara(int uara,int 최소,int 최대){return uara<최소?최소:uara>최대?최대:uara;}
static void nuku_whakarahi_anō(int 가로,int Poutū_tūranga) {
    Tauranga_d413d4bc *matapihi=&Windows_Rārangi[whakarahi_anō_tō];int 왼쪽=처음가로,위쪽=처음세로,RIGHT=처음가로+처음너비,아래쪽=처음세로+처음높이;
    if(잡은모서리==1||잡은모서리==3)왼쪽=whakawehe_uara(처음가로+가로-잡은가로,0,RIGHT-360);
    else RIGHT=whakawehe_uara(처음가로+처음너비+가로-잡은가로,왼쪽+360,보드화면너비());
    if(잡은모서리<=2)위쪽=whakawehe_uara(처음세로+Poutū_tūranga-잡은세로,34,아래쪽-216);
    else 아래쪽=whakawehe_uara(처음세로+처음높이+Poutū_tūranga-잡은세로,위쪽+216,보드화면높이());
    unsigned COLUMNS=(RIGHT-왼쪽-24)/8,ROW_COUNT=(아래쪽-위쪽-56)/16;
    if(matapihi->COLUMNS!=COLUMNS||matapihi->ROW_COUNT!=ROW_COUNT){
        matapihi->크기바뀜=1;matapihi->COLUMNS=COLUMNS;matapihi->ROW_COUNT=ROW_COUNT;
        if(matapihi->tīwae_tūranga>=COLUMNS)matapihi->tīwae_tūranga=COLUMNS-1;
        if(matapihi->ROW_tūranga>=matapihi->맨위+ROW_COUNT)matapihi->맨위=matapihi->ROW_tūranga-ROW_COUNT+1;
        unsigned 한도=matapihi->맨위;if(한도>Hītori_hononga_COUNT-ROW_COUNT)한도=Hītori_hononga_COUNT-ROW_COUNT;
        if(matapihi->panuku>한도)matapihi->panuku=한도;
    }
    int 옛가로=matapihi->taunga_x,옛세로=matapihi->세로좌표,옛폭=matapihi->너비,옛길이=matapihi->높이;
    if(옛가로==왼쪽&&옛세로==위쪽&&옛폭==RIGHT-왼쪽&&옛길이==아래쪽-위쪽)return;
    matapihi->taunga_x=왼쪽;matapihi->세로좌표=위쪽;matapihi->너비=RIGHT-왼쪽;matapihi->높이=아래쪽-위쪽;
    창자리그리기(옛가로,옛세로,옛폭,옛길이,matapihi);
}
void Tauranga_atatohu(unsigned Panuku_tuemi,int taunga_x,int 세로좌표){
    unsigned 눌림=Panuku_tuemi&~단추들;단추들=Panuku_tuemi;
    if(!papamahi_tiro){tō_uara=-1;whakarahi_anō_tō=-1;papa_atatohu(taunga_x,세로좌표,1);return;}
    if(!(Panuku_tuemi&1)){tō_uara=-1;whakarahi_anō_tō=-1;}
    if(whakarahi_anō_tō>=0&&!Windows_Rārangi[whakarahi_anō_tō].살아있음)whakarahi_anō_tō=-1;
    if(tō_uara>=0&&!Windows_Rārangi[tō_uara].살아있음)tō_uara=-1;
    if(whakarahi_anō_tō>=0){
        nuku_whakarahi_anō(taunga_x,세로좌표);papa_atatohu(taunga_x,세로좌표,잡은모서리==1||잡은모서리==4?2:3);return;
    }
    papa_atatohu(taunga_x,세로좌표,1);
    if(tō_uara>=0){
        Tauranga_d413d4bc *matapihi=&Windows_Rārangi[tō_uara];
        int 옛가로=matapihi->taunga_x,옛세로=matapihi->세로좌표;
        matapihi->taunga_x=whakawehe_uara(taunga_x-끌기가로,0,보드화면너비()-matapihi->너비);
        matapihi->세로좌표=whakawehe_uara(세로좌표-끌기세로,34,보드화면높이()-matapihi->높이);
        if(옛가로!=(int)matapihi->taunga_x||옛세로!=(int)matapihi->세로좌표)창자리그리기(옛가로,옛세로,matapihi->너비,matapihi->높이,matapihi);
        return;
    }
    extern int 화면덮음(int,int,int);
    if(화면덮음(Arotahi,taunga_x,세로좌표)){화면가리킴(Arotahi,눌림,taunga_x,세로좌표);return;}
    int pūtāutu_uara=가리킨창(taunga_x,세로좌표),모서리=모서리찾기(pūtāutu_uara,taunga_x,세로좌표);
    if(모서리)papa_atatohu(taunga_x,세로좌표,모서리==1||모서리==4?2:3);
    if(눌림&1){
        if(모서리){
            Tauranga_d413d4bc *matapihi=&Windows_Rārangi[pūtāutu_uara];whakarahi_anō_tō=pūtāutu_uara;잡은모서리=모서리;잡은가로=taunga_x;잡은세로=세로좌표;
            처음가로=matapihi->taunga_x;처음세로=matapihi->세로좌표;처음너비=matapihi->너비;처음높이=matapihi->높이;
            if(pūtāutu_uara!=Arotahi)앞으로올리기(pūtāutu_uara);return;
        }
        if(세로좌표<32&&taunga_x>=6&&taunga_x<142){Waihanga_tāurunga();return;}
        if(세로좌표<32&&taunga_x>=154&&taunga_x<602){앞으로올리기((taunga_x-154)/112);return;}
        if(pūtāutu_uara>=0){
            Tauranga_d413d4bc *matapihi=&Windows_Rārangi[pūtāutu_uara];
            if(세로좌표<(int)matapihi->세로좌표+30&&taunga_x>=(int)(matapihi->taunga_x+matapihi->너비)-32){kati_matapihi(pūtāutu_uara);return;}
            if(pūtāutu_uara!=Arotahi)앞으로올리기(pūtāutu_uara);
            if(세로좌표<(int)matapihi->세로좌표+30){tō_uara=pūtāutu_uara;끌기가로=taunga_x-matapihi->taunga_x;끌기세로=세로좌표-matapihi->세로좌표;}return;
        }
    }
    if(Arotahi>=0&&(눌림&(8|16))){Tauranga_tāurunga=&Windows_Rārangi[Arotahi];if(눌림&8){unsigned 한도=Tauranga_tāurunga->맨위;if(한도>Hītori_hononga_COUNT-Tauranga_tāurunga->ROW_COUNT)한도=Hītori_hononga_COUNT-Tauranga_tāurunga->ROW_COUNT;Tauranga_tāurunga->panuku=Tauranga_tāurunga->panuku+9>한도?한도:Tauranga_tāurunga->panuku+9;}else Tauranga_tāurunga->panuku=Tauranga_tāurunga->panuku<9?0:Tauranga_tāurunga->panuku-9;다시그리기();}
}
void 터미널바로가기키(unsigned 누름값){if(누름값==1)Waihanga_tāurunga();if(누름값==2&&tāurunga_COUNT)앞으로올리기(whakaraupapa_uara[0]);if(누름값==3)kati_matapihi(Arotahi);}
mīhini_Word papa_Tauranga(mīhini_Word hohenga){
    if(hohenga==300){if(!Windows_Rārangi[출력결과].살아있음)return Waihanga_tāurunga();papamahi_tiro=1;다시그리기();return 0;}
    if(hohenga==0){kati_matapihi(Arotahi);return 0;}if(hohenga==1)return (uint32_t)Waihanga_tāurunga();if(hohenga==2)return Arotahi>=0;
    if(hohenga==9){papamahi_tiro=0;return 0;}if(hohenga==7)return tāurunga_COUNT;if(hohenga==10)return Arotahi+1;if(hohenga==11)return 출력결과;
    if(hohenga==13){Tauranga_d413d4bc *matapihi=&Windows_Rārangi[출력결과];return matapihi->살아있음?(matapihi->ROW_COUNT<<16)|matapihi->COLUMNS:(19<<16)|68;}
    if(hohenga==14){unsigned uara=Windows_Rārangi[출력결과].크기바뀜;Windows_Rārangi[출력결과].크기바뀜=0;return uara;}
    if(hohenga==12){unsigned uara=대기중;대기중=0;return uara;}
    if(hohenga>=20&&hohenga<24)return Windows_Rārangi[hohenga-20].살아있음;
    if(hohenga>=100&&hohenga<104){출력결과=hohenga-100;Tauranga_tāurunga=&Windows_Rārangi[출력결과];return 0;}
    if(hohenga>=200&&hohenga<204){앞으로올리기(hohenga-200);return 0;}
    if(hohenga==3){다시그리기();return 0;}Tauranga_tāurunga=&Windows_Rārangi[출력결과];if(!Tauranga_tāurunga->살아있음)return 0;
    if(hohenga==4)ūkui_IRI();if(hohenga==5||hohenga==6){unsigned 이전=단추들;Tauranga_atatohu(hohenga==5?8:16,0,0);단추들=이전;}return 1;
}
