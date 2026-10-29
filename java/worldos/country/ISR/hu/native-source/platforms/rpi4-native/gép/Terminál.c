#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* saját 네 Ablak 합성과 UTF-8 Terminál. 바뀐 영역의 Kész_ÉRTÉK 그림만 표시한다. */
#include <stdint.h>
#include <stddef.h>
typedef uintptr_t gép_szó;
extern gép_szó fal_képpont(gép_szó,gép_szó,gép_szó),보드화면기억공간(void);
extern void *memset(void *,int,size_t);
extern const unsigned char Terminál_betűkészlet[];
#define 최대열수 237
#define Előzmények_sor_DARAB 160
typedef struct {
    uint32_t 글자칸들[Előzmények_sor_DARAB][최대열수]; uint8_t 모양들[Előzmények_sor_DARAB][최대열수];
    unsigned 너비,높이,OSZLOPOK,SOR_DARAB,크기바뀜;
    unsigned 살아있음,x_koordináta,Y_koordináta,SOR_pozíció,OSZLOP_pozíció,맨위,görget,전경색,배경색,탈출상태,paraméter_ÉRTÉK[4],paraméter_INDEX,저장행,저장열;
    unsigned 부호없는결과,긴부호없는값,KICSI_ÉRTÉK,대체화면,가리개보임;
} Terminál_d413d4bc;
static Terminál_d413d4bc Windows_Lista[4];
static int Fókusz=-1,kimenet,rendel_ÉRTÉK[4],bejegyzés_DARAB,húz_ÉRTÉK=-1,húz_X,húz_Y;
static unsigned informatikai_részleg_Függő,단추들,Asztal_Nézet,한글입력;
static const uint32_t 색상들[16]={0x201a15,0x6060df,0x9dcc86,0x80cfea,0xefaf72,0xca96c9,0xceda76,0xede9df,0x858078,0x8888ff,0xb9eba7,0xa5eaff,0xffcc99,0xf0bef1,0xf0f0a0,0xffffff};
extern int 화면보임(int),화면가리킴(int,unsigned,int,int);
extern void 화면다시그림(int);
static Terminál_d413d4bc *Terminál_bejegyzés;
static unsigned kétbájtos_karakter(unsigned kódpont){return kódpont>=256?2:1;}
static void 사각영역(unsigned x_koordináta,unsigned Y_koordináta,unsigned 너비값,unsigned 높이값,unsigned 색상){
    fal_téglalap_kitöltés(x_koordináta,Y_koordináta,너비값,높이값,색상);
}
void Terminál_betűkép(unsigned x_koordináta,unsigned Y_koordináta,unsigned kódpont,unsigned 전경색,unsigned 배경색){
    unsigned 너비=kétbájtos_karakter(kódpont)*8;if(kódpont==0xffffffffu)return;
    int 왼쪽=x_koordináta,위쪽=Y_koordináta,폭=너비,hossz_ÉRTÉK=16;
    if(!보드그림범위(&왼쪽,&위쪽,&폭,&hossz_ÉRTÉK))return;
    if(kódpont==' '){fal_téglalap_kitöltés(왼쪽,위쪽,폭,hossz_ÉRTÉK,배경색);return;}
    unsigned KERES_INDEX=kódpont<65536?kódpont:kódpont>=0x1f600&&kódpont<0x1f650?65536+kódpont-0x1f600:0xfffd;
    const unsigned char *betűkészlet_ÉRTÉK=Terminál_betűkészlet+KERES_INDEX*32;
    for(int Vonal=위쪽;Vonal<위쪽+hossz_ÉRTÉK;Vonal++){unsigned BITS_Lista=betűkészlet_ÉRTÉK[(Vonal-Y_koordináta)*2]*256+betűkészlet_ÉRTÉK[(Vonal-Y_koordináta)*2+1];for(int tárolóhely_bejegyzés=왼쪽;tárolóhely_bejegyzés<왼쪽+폭;tárolóhely_bejegyzés++)fal_képpont(tárolóhely_bejegyzés,Vonal,(BITS_Lista&(0x8000>>(tárolóhely_bejegyzés-x_koordináta)))?전경색:배경색);}
}
static void név_tábla(unsigned x_koordináta,unsigned Y_koordináta,const char *sztring_adat,unsigned 전경색,unsigned 배경색){while(*sztring_adat){unsigned kódpont=(unsigned char)*sztring_adat++, 남은수=0;if(kódpont>=0xc0){남은수=kódpont<0xe0?1:kódpont<0xf0?2:3;kódpont&=(1u<<(6-남은수))-1;while(남은수--&&*sztring_adat)kódpont=(kódpont<<6)|((unsigned char)*sztring_adat++&63);}Terminál_betűkép(x_koordináta,Y_koordináta,kódpont,전경색,배경색);x_koordináta+=kétbájtos_karakter(kódpont)*8;}}
static unsigned 첫항목(void){return Terminál_bejegyzés->맨위;}
static int 보이는지(void){return Terminál_bejegyzés->살아있음&&Fókusz>=0&&Terminál_bejegyzés==&Windows_Lista[Fókusz]&&!화면보임(Fókusz);}
static void 그리기(unsigned SOR_pozíció,unsigned OSZLOP_pozíció){
    if(!보이는지()||SOR_pozíció<첫항목()-Terminál_bejegyzés->görget||SOR_pozíció>=첫항목()-Terminál_bejegyzés->görget+Terminál_bejegyzés->SOR_DARAB||OSZLOP_pozíció>=Terminál_bejegyzés->OSZLOPOK)return;
    unsigned kódpont=Terminál_bejegyzés->글자칸들[SOR_pozíció%Előzmények_sor_DARAB][OSZLOP_pozíció],sztring_adat=Terminál_bejegyzés->모양들[SOR_pozíció%Előzmények_sor_DARAB][OSZLOP_pozíció];
    if(kétbájtos_karakter(kódpont)==2&&OSZLOP_pozíció+1>=Terminál_bejegyzés->OSZLOPOK)kódpont=' ';
    Terminál_betűkép(Terminál_bejegyzés->x_koordináta+12+OSZLOP_pozíció*8,Terminál_bejegyzés->Y_koordináta+36+(SOR_pozíció-첫항목()+Terminál_bejegyzés->görget)*16,kódpont?kódpont:' ',색상들[sztring_adat&15],색상들[sztring_adat>>4]);
}
static void kalap_jel_ÉRTÉK(int bemutató_ablak){if(!보이는지()||Terminál_bejegyzés->görget||Terminál_bejegyzés->OSZLOP_pozíció>=Terminál_bejegyzés->OSZLOPOK||Terminál_bejegyzés->SOR_pozíció<Terminál_bejegyzés->맨위||Terminál_bejegyzés->SOR_pozíció>=Terminál_bejegyzés->맨위+Terminál_bejegyzés->SOR_DARAB)return;
    if(!bemutató_ablak||!Terminál_bejegyzés->가리개보임)그리기(Terminál_bejegyzés->SOR_pozíció,Terminál_bejegyzés->OSZLOP_pozíció);else 사각영역(Terminál_bejegyzés->x_koordináta+12+Terminál_bejegyzés->OSZLOP_pozíció*8,Terminál_bejegyzés->Y_koordináta+36+(Terminál_bejegyzés->SOR_pozíció-Terminál_bejegyzés->맨위)*16+14,8,2,색상들[Terminál_bejegyzés->전경색]);}
static void Tartalom_ÉRTÉK(void){
    사각영역(Terminál_bejegyzés->x_koordináta+12,Terminál_bejegyzés->Y_koordináta+36,Terminál_bejegyzés->OSZLOPOK*8,Terminál_bejegyzés->SOR_DARAB*16,색상들[0]);
    int 가로=Terminál_bejegyzés->x_koordináta+12,szektor_pozíció=Terminál_bejegyzés->Y_koordináta+36,폭=Terminál_bejegyzés->OSZLOPOK*8,hossz_ÉRTÉK=Terminál_bejegyzés->SOR_DARAB*16;
    if(보드그림범위(&가로,&szektor_pozíció,&폭,&hossz_ÉRTÉK)){
    unsigned 첫줄=(szektor_pozíció-Terminál_bejegyzés->Y_koordináta-36)/16,끝줄=(szektor_pozíció+hossz_ÉRTÉK-Terminál_bejegyzés->Y_koordináta-36+15)/16;
    unsigned 첫칸=(가로-Terminál_bejegyzés->x_koordináta-12)/8,끝칸=(가로+폭-Terminál_bejegyzés->x_koordináta-12+7)/8;
    if(첫칸)첫칸--; /* 잘림 határ_ÉRTÉK 왼쪽에서 시작한 두 tárolóhely_bejegyzés 글자도 그린다. */
    for(unsigned 반환값=첫줄;반환값<끝줄;반환값++)for(unsigned kódpont=첫칸;kódpont<끝칸;kódpont++){
        unsigned SOR_pozíció=첫항목()-Terminál_bejegyzés->görget+반환값,karakter_ÉRTÉK=Terminál_bejegyzés->글자칸들[SOR_pozíció%Előzmények_sor_DARAB][kódpont],sztring_adat=Terminál_bejegyzés->모양들[SOR_pozíció%Előzmények_sor_DARAB][kódpont];
        if(kétbájtos_karakter(karakter_ÉRTÉK)==2&&kódpont+1>=Terminál_bejegyzés->OSZLOPOK)karakter_ÉRTÉK=' ';
        if((karakter_ÉRTÉK==0||karakter_ÉRTÉK==' ')&&(sztring_adat>>4)==0)continue;
        Terminál_betűkép(Terminál_bejegyzés->x_koordináta+12+kódpont*8,Terminál_bejegyzés->Y_koordináta+36+반환값*16,karakter_ÉRTÉK?karakter_ÉRTÉK:' ',색상들[sztring_adat&15],색상들[sztring_adat>>4]);
    }}
    név_tábla(Terminál_bejegyzés->x_koordináta+12,Terminál_bejegyzés->Y_koordináta+Terminál_bejegyzés->높이-18,Terminál_bejegyzés->görget?"PgDn: recent output":Terminál_bejegyzés->너비>=500?"F6: next | Corner + left drag: resize":"Corner + left drag: resize",0xece8e2,0x403127);kalap_jel_ÉRTÉK(1);
}
static void végrehajtás_doboz(int azonosító_ÉRTÉK){
    Terminál_bejegyzés=&Windows_Lista[azonosító_ÉRTÉK];
    int 가로=Terminál_bejegyzés->x_koordináta,szektor_pozíció=Terminál_bejegyzés->Y_koordináta,폭=Terminál_bejegyzés->너비,hossz_ÉRTÉK=Terminál_bejegyzés->높이;
    if(!보드그림범위(&가로,&szektor_pozíció,&폭,&hossz_ÉRTÉK))return;
    사각영역(Terminál_bejegyzés->x_koordináta,Terminál_bejegyzés->Y_koordináta,Terminál_bejegyzés->너비,Terminál_bejegyzés->높이,0x403127);
    unsigned 색상=azonosító_ÉRTÉK==Fókusz?0x905020:0x604438;사각영역(Terminál_bejegyzés->x_koordináta,Terminál_bejegyzés->Y_koordináta,Terminál_bejegyzés->너비,30,색상);
    név_tábla(Terminál_bejegyzés->x_koordináta+12,Terminál_bejegyzés->Y_koordináta+7,"JKOROS Terminal",0xffffff,색상);
    char 수치[2]={(char)('1'+azonosító_ÉRTÉK),0};név_tábla(Terminál_bejegyzés->x_koordináta+148,Terminál_bejegyzés->Y_koordináta+7,수치,0xffffff,색상);
    név_tábla(Terminál_bejegyzés->x_koordináta+240,Terminál_bejegyzés->Y_koordináta+7,Terminál_bejegyzés->너비>=500?(한글입력?"[HU] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[HU]":"[EN]"),0xffffff,색상);
    사각영역(Terminál_bejegyzés->x_koordináta+Terminál_bejegyzés->너비-32,Terminál_bejegyzés->Y_koordináta+4,26,22,0x5555b8);név_tábla(Terminál_bejegyzés->x_koordináta+Terminál_bejegyzés->너비-24,Terminál_bejegyzés->Y_koordináta+7,"X",0xffffff,0x5555b8);
    Tartalom_ÉRTÉK();
}
static void Rajz_jelenet(void){
    if(!Asztal_Nézet)return;사각영역(0,0,보드화면너비(),보드화면높이(),0x302018);사각영역(0,0,보드화면너비(),32,0x403127);
    사각영역(6,4,136,24,0x905020);név_tábla(14,8,"+ New terminal",0xffffff,0x905020);
    for(int 순번=0;순번<4;순번++)if(Windows_Lista[순번].살아있음){unsigned kódpont=Fókusz==순번?0x905020:0x604438;사각영역(154+순번*112,4,106,24,kódpont);név_tábla(160+순번*112,8,"Terminal",0xffffff,kódpont);char sztring_adat[2]={(char)('1'+순번),0};név_tábla(232+순번*112,8,sztring_adat,0xffffff,kódpont);}
    if(!bejegyzés_DARAB)név_tábla(140,210,"Click + New terminal to start",0xede9df,0x302018);
    for(int 순번=0;순번<bejegyzés_DARAB;순번++)végrehajtás_doboz(rendel_ÉRTÉK[순번]);화면다시그림(Fókusz);Terminál_bejegyzés=&Windows_Lista[kimenet];
}
static void Paint_régió(int 가로,int szektor_pozíció,int 폭,int hossz_ÉRTÉK){
    if(!Asztal_Nézet||!보드그림범위(&가로,&szektor_pozíció,&폭,&hossz_ÉRTÉK))return;
    for(int Vonal=szektor_pozíció;Vonal<szektor_pozíció+hossz_ÉRTÉK;Vonal+=32){
        int 띠높이=szektor_pozíció+hossz_ÉRTÉK-Vonal;if(띠높이>32)띠높이=32;
        if(fal_START_rajz(가로,Vonal,폭,띠높이)){Rajz_jelenet();fal_Befejezés_rajz();}
    }
}
static void 다시그리기(void){Paint_régió(0,0,보드화면너비(),보드화면높이());}
/* 서로 겹치지 않는 새 Ablak 영역과 Előző_cikk 자리의 네 띠를 복구한다. */
static void 창자리그리기(int 가로,int szektor_pozíció,int 폭,int hossz_ÉRTÉK,Terminál_d413d4bc *Ablak){
    int 왼쪽=가로>(int)Ablak->x_koordináta?가로:(int)Ablak->x_koordináta;
    int 위쪽=szektor_pozíció>(int)Ablak->Y_koordináta?szektor_pozíció:(int)Ablak->Y_koordináta;
    int jog=가로+폭<(int)(Ablak->x_koordináta+Ablak->너비)?가로+폭:(int)(Ablak->x_koordináta+Ablak->너비);
    int 아래쪽=szektor_pozíció+hossz_ÉRTÉK<(int)(Ablak->Y_koordináta+Ablak->높이)?szektor_pozíció+hossz_ÉRTÉK:(int)(Ablak->Y_koordináta+Ablak->높이);
    Paint_régió(Ablak->x_koordináta,Ablak->Y_koordináta,Ablak->너비,Ablak->높이);
    if(왼쪽>=jog||위쪽>=아래쪽){Paint_régió(가로,szektor_pozíció,폭,hossz_ÉRTÉK);return;}
    Paint_régió(가로,szektor_pozíció,폭,위쪽-szektor_pozíció);
    Paint_régió(가로,아래쪽,폭,szektor_pozíció+hossz_ÉRTÉK-아래쪽);
    Paint_régió(가로,위쪽,왼쪽-가로,아래쪽-위쪽);
    Paint_régió(jog,위쪽,가로+폭-jog,아래쪽-위쪽);
}
static void jelzés_Fókusz(void){informatikai_részleg_Függő=(informatikai_részleg_Függő&~15u)|(unsigned)(Fókusz+1)|0x10000;}
void Terminál_bevitel_mód(unsigned 한글여부){
    한글입력=한글여부!=0;
    /* Update title bars only: a mode switch must not erase an EL0 drawing. */
    if(Fókusz>=0){
        Terminál_d413d4bc *ablak_bejegyzés=&Windows_Lista[Fókusz];
        név_tábla(ablak_bejegyzés->x_koordináta+240,ablak_bejegyzés->Y_koordináta+7,ablak_bejegyzés->너비>=500?(한글입력?"[HU] F9 / Shift+Space":"[EN] F9 / Shift+Space"):(한글입력?"[HU]":"[EN]"),0xffffff,0x905020);
    }
}
static void 앞으로올리기(int azonosító_ÉRTÉK){if(azonosító_ÉRTÉK<0||azonosító_ÉRTÉK>=4||!Windows_Lista[azonosító_ÉRTÉK].살아있음)return;int aktuális_pozíció=0;while(aktuális_pozíció<bejegyzés_DARAB&&rendel_ÉRTÉK[aktuális_pozíció]!=azonosító_ÉRTÉK)aktuális_pozíció++;for(;aktuális_pozíció+1<bejegyzés_DARAB;aktuális_pozíció++)rendel_ÉRTÉK[aktuális_pozíció]=rendel_ÉRTÉK[aktuális_pozíció+1];rendel_ÉRTÉK[bejegyzés_DARAB-1]=azonosító_ÉRTÉK;Fókusz=azonosító_ÉRTÉK;jelzés_Fókusz();다시그리기();}
static void 빈칸채우기(unsigned SOR_pozíció){for(unsigned kódpont=0;kódpont<최대열수;kódpont++){Terminál_bejegyzés->글자칸들[SOR_pozíció%Előzmények_sor_DARAB][kódpont]=0;Terminál_bejegyzés->모양들[SOR_pozíció%Előzmények_sor_DARAB][kódpont]=Terminál_bejegyzés->전경색|(Terminál_bejegyzés->배경색<<4);}}
static void töröl_Tartalom(void){Terminál_bejegyzés->SOR_pozíció=Terminál_bejegyzés->OSZLOP_pozíció=Terminál_bejegyzés->맨위=Terminál_bejegyzés->görget=0;for(unsigned 반환값=0;반환값<Előzmények_sor_DARAB;반환값++)빈칸채우기(반환값);if(보이는지())Tartalom_ÉRTÉK();}
static int készít_bejegyzés(void){
    if(!보드화면기억공간())return -19;int azonosító_ÉRTÉK=0;while(azonosító_ÉRTÉK<4&&Windows_Lista[azonosító_ÉRTÉK].살아있음)azonosító_ÉRTÉK++;if(azonosító_ÉRTÉK==4)return -28;
    Asztal_Nézet=1;Terminál_bejegyzés=&Windows_Lista[azonosító_ÉRTÉK];memset(Terminál_bejegyzés,0,sizeof(*Terminál_bejegyzés));Terminál_bejegyzés->살아있음=1;Terminál_bejegyzés->너비=568;Terminál_bejegyzés->높이=360;Terminál_bejegyzés->OSZLOPOK=68;Terminál_bejegyzés->SOR_DARAB=19;Terminál_bejegyzés->x_koordináta=12+azonosító_ÉRTÉK*16;Terminál_bejegyzés->Y_koordináta=48+azonosító_ÉRTÉK*18;Terminál_bejegyzés->전경색=7;Terminál_bejegyzés->가리개보임=1;
    for(unsigned 반환값=0;반환값<Előzmények_sor_DARAB;반환값++)빈칸채우기(반환값);rendel_ÉRTÉK[bejegyzés_DARAB++]=azonosító_ÉRTÉK;Fókusz=azonosító_ÉRTÉK;informatikai_részleg_Függő|=1u<<(4+azonosító_ÉRTÉK);jelzés_Fókusz();다시그리기();return azonosító_ÉRTÉK+1;
}
static void bezár_ablak(int azonosító_ÉRTÉK){
    if(azonosító_ÉRTÉK<0||azonosító_ÉRTÉK>=4||!Windows_Lista[azonosító_ÉRTÉK].살아있음)return;Windows_Lista[azonosító_ÉRTÉK].살아있음=0;informatikai_részleg_Függő|=1u<<(8+azonosító_ÉRTÉK);
    int aktuális_pozíció=0;while(aktuális_pozíció<bejegyzés_DARAB&&rendel_ÉRTÉK[aktuális_pozíció]!=azonosító_ÉRTÉK)aktuális_pozíció++;for(;aktuális_pozíció+1<bejegyzés_DARAB;aktuális_pozíció++)rendel_ÉRTÉK[aktuális_pozíció]=rendel_ÉRTÉK[aktuális_pozíció+1];bejegyzés_DARAB--;
    if(Fókusz==azonosító_ÉRTÉK)Fókusz=bejegyzés_DARAB?rendel_ÉRTÉK[bejegyzés_DARAB-1]:-1;jelzés_Fókusz();다시그리기();
}
static void 줄바꿈(void){Terminál_bejegyzés->OSZLOP_pozíció=0;Terminál_bejegyzés->SOR_pozíció++;if(Terminál_bejegyzés->SOR_pozíció>=Terminál_bejegyzés->맨위+Terminál_bejegyzés->SOR_DARAB){Terminál_bejegyzés->맨위++;빈칸채우기(Terminál_bejegyzés->SOR_pozíció);if(보이는지())Tartalom_ÉRTÉK();}}
static void kódpont_451f2815(unsigned kódpont){
    if(kódpont==13){Terminál_bejegyzés->OSZLOP_pozíció=0;return;}if(kódpont==10){줄바꿈();return;}if(kódpont==8){if(Terminál_bejegyzés->OSZLOP_pozíció)Terminál_bejegyzés->OSZLOP_pozíció--;return;}
    if(kódpont==9){unsigned cikk_DARAB=8-Terminál_bejegyzés->OSZLOP_pozíció%8;while(cikk_DARAB--)kódpont_451f2815(' ');return;}if(kódpont<32||kódpont==127)return;
    unsigned 너비값=kétbájtos_karakter(kódpont);if(Terminál_bejegyzés->OSZLOP_pozíció+너비값>Terminál_bejegyzés->OSZLOPOK)줄바꿈();
    if(Terminál_bejegyzés->글자칸들[Terminál_bejegyzés->SOR_pozíció%Előzmények_sor_DARAB][Terminál_bejegyzés->OSZLOP_pozíció]==0xffffffffu&&Terminál_bejegyzés->OSZLOP_pozíció){Terminál_bejegyzés->글자칸들[Terminál_bejegyzés->SOR_pozíció%Előzmények_sor_DARAB][Terminál_bejegyzés->OSZLOP_pozíció-1]=' ';그리기(Terminál_bejegyzés->SOR_pozíció,Terminál_bejegyzés->OSZLOP_pozíció-1);}
    if(kétbájtos_karakter(Terminál_bejegyzés->글자칸들[Terminál_bejegyzés->SOR_pozíció%Előzmények_sor_DARAB][Terminál_bejegyzés->OSZLOP_pozíció])==2&&Terminál_bejegyzés->OSZLOP_pozíció+1<Terminál_bejegyzés->OSZLOPOK){Terminál_bejegyzés->글자칸들[Terminál_bejegyzés->SOR_pozíció%Előzmények_sor_DARAB][Terminál_bejegyzés->OSZLOP_pozíció+1]=' ';그리기(Terminál_bejegyzés->SOR_pozíció,Terminál_bejegyzés->OSZLOP_pozíció+1);}
    Terminál_bejegyzés->글자칸들[Terminál_bejegyzés->SOR_pozíció%Előzmények_sor_DARAB][Terminál_bejegyzés->OSZLOP_pozíció]=kódpont;Terminál_bejegyzés->모양들[Terminál_bejegyzés->SOR_pozíció%Előzmények_sor_DARAB][Terminál_bejegyzés->OSZLOP_pozíció]=Terminál_bejegyzés->전경색|(Terminál_bejegyzés->배경색<<4);
    if(너비값==2)Terminál_bejegyzés->글자칸들[Terminál_bejegyzés->SOR_pozíció%Előzmények_sor_DARAB][Terminál_bejegyzés->OSZLOP_pozíció+1]=0xffffffffu;
    그리기(Terminál_bejegyzés->SOR_pozíció,Terminál_bejegyzés->OSZLOP_pozíció);Terminál_bejegyzés->OSZLOP_pozíció+=너비값;
}
static void leíró_vezérlő_szekvencia(unsigned kódpont){
    unsigned cikk_DARAB=Terminál_bejegyzés->paraméter_ÉRTÉK[0]?Terminál_bejegyzés->paraméter_ÉRTÉK[0]:1;
    if(kódpont=='m')for(unsigned 순번=0;순번<=Terminál_bejegyzés->paraméter_INDEX;순번++){unsigned adat_pozíció=Terminál_bejegyzés->paraméter_ÉRTÉK[순번];if(!adat_pozíció){Terminál_bejegyzés->전경색=7;Terminál_bejegyzés->배경색=0;}if(adat_pozíció==1&&Terminál_bejegyzés->전경색<8)Terminál_bejegyzés->전경색+=8;if(adat_pozíció==7){unsigned 유지=Terminál_bejegyzés->전경색;Terminál_bejegyzés->전경색=Terminál_bejegyzés->배경색;Terminál_bejegyzés->배경색=유지;}if(adat_pozíció>=30&&adat_pozíció<=37)Terminál_bejegyzés->전경색=adat_pozíció-30;if(adat_pozíció>=90&&adat_pozíció<=97)Terminál_bejegyzés->전경색=adat_pozíció-90+8;if(adat_pozíció>=40&&adat_pozíció<=47)Terminál_bejegyzés->배경색=adat_pozíció-40;if(adat_pozíció>=100&&adat_pozíció<=107)Terminál_bejegyzés->배경색=adat_pozíció-100+8;if(adat_pozíció==39)Terminál_bejegyzés->전경색=7;if(adat_pozíció==49)Terminál_bejegyzés->배경색=0;}
    if(kódpont=='J'&&(Terminál_bejegyzés->paraméter_ÉRTÉK[0]==2||Terminál_bejegyzés->paraméter_ÉRTÉK[0]==3))töröl_Tartalom();
    if(kódpont=='K'){unsigned 출발위치=Terminál_bejegyzés->paraméter_ÉRTÉK[0]==2?0:Terminál_bejegyzés->OSZLOP_pozíció,도착위치=Terminál_bejegyzés->paraméter_ÉRTÉK[0]==1?Terminál_bejegyzés->OSZLOP_pozíció+1:Terminál_bejegyzés->OSZLOPOK;if(Terminál_bejegyzés->paraméter_ÉRTÉK[0]==1)출발위치=0;for(unsigned 순번=출발위치;순번<도착위치&&순번<Terminál_bejegyzés->OSZLOPOK;순번++){
        unsigned SOR_ÉRTÉK=Terminál_bejegyzés->SOR_pozíció%Előzmények_sor_DARAB,karakter_ÉRTÉK=Terminál_bejegyzés->글자칸들[SOR_ÉRTÉK][순번],alakzat_ÉRTÉK=Terminál_bejegyzés->전경색|(Terminál_bejegyzés->배경색<<4);
        /* 넓은 vi 화면에서도 이미 빈 칸의 betűkészlet_ÉRTÉK 화소를 되풀이해 칠하지 않는다. */
        int 바뀜=(karakter_ÉRTÉK!=0&&karakter_ÉRTÉK!=' ')||Terminál_bejegyzés->모양들[SOR_ÉRTÉK][순번]!=alakzat_ÉRTÉK;
        Terminál_bejegyzés->글자칸들[SOR_ÉRTÉK][순번]=' ';Terminál_bejegyzés->모양들[SOR_ÉRTÉK][순번]=alakzat_ÉRTÉK;
        if(바뀜)그리기(Terminál_bejegyzés->SOR_pozíció,순번);
    }}
    if(kódpont=='D')Terminál_bejegyzés->OSZLOP_pozíció=cikk_DARAB>Terminál_bejegyzés->OSZLOP_pozíció?0:Terminál_bejegyzés->OSZLOP_pozíció-cikk_DARAB;if(kódpont=='C')Terminál_bejegyzés->OSZLOP_pozíció=Terminál_bejegyzés->OSZLOP_pozíció+cikk_DARAB>=Terminál_bejegyzés->OSZLOPOK?Terminál_bejegyzés->OSZLOPOK-1:Terminál_bejegyzés->OSZLOP_pozíció+cikk_DARAB;
    if(kódpont=='G')Terminál_bejegyzés->OSZLOP_pozíció=cikk_DARAB>Terminál_bejegyzés->OSZLOPOK?Terminál_bejegyzés->OSZLOPOK-1:cikk_DARAB-1;if(kódpont=='A')Terminál_bejegyzés->SOR_pozíció=cikk_DARAB>Terminál_bejegyzés->SOR_pozíció-Terminál_bejegyzés->맨위?Terminál_bejegyzés->맨위:Terminál_bejegyzés->SOR_pozíció-cikk_DARAB;
    if(kódpont=='B')Terminál_bejegyzés->SOR_pozíció=Terminál_bejegyzés->SOR_pozíció+cikk_DARAB>=Terminál_bejegyzés->맨위+Terminál_bejegyzés->SOR_DARAB?Terminál_bejegyzés->맨위+Terminál_bejegyzés->SOR_DARAB-1:Terminál_bejegyzés->SOR_pozíció+cikk_DARAB;
    if(kódpont=='H'||kódpont=='f'){Terminál_bejegyzés->SOR_pozíció=Terminál_bejegyzés->맨위+(cikk_DARAB>Terminál_bejegyzés->SOR_DARAB?Terminál_bejegyzés->SOR_DARAB:cikk_DARAB)-1;unsigned x_koordináta=Terminál_bejegyzés->paraméter_ÉRTÉK[1]?Terminál_bejegyzés->paraméter_ÉRTÉK[1]:1;Terminál_bejegyzés->OSZLOP_pozíció=(x_koordináta>Terminál_bejegyzés->OSZLOPOK?Terminál_bejegyzés->OSZLOPOK:x_koordináta)-1;}
    if(kódpont=='s'){Terminál_bejegyzés->저장행=Terminál_bejegyzés->SOR_pozíció;Terminál_bejegyzés->저장열=Terminál_bejegyzés->OSZLOP_pozíció;}if(kódpont=='u'){Terminál_bejegyzés->SOR_pozíció=Terminál_bejegyzés->저장행;Terminál_bejegyzés->OSZLOP_pozíció=Terminál_bejegyzés->저장열<Terminál_bejegyzés->OSZLOPOK?Terminál_bejegyzés->저장열:Terminál_bejegyzés->OSZLOPOK-1;}
    if((kódpont=='h'||kódpont=='l')&&Terminál_bejegyzés->paraméter_ÉRTÉK[0]==25)Terminál_bejegyzés->가리개보임=kódpont=='h';
}
void Terminál_bájt(unsigned MPERC_ÉRTÉK){
    Terminál_bejegyzés=&Windows_Lista[kimenet];if(!Terminál_bejegyzés->살아있음)return;kalap_jel_ÉRTÉK(0);if(Terminál_bejegyzés->görget){Terminál_bejegyzés->görget=0;if(보이는지())Tartalom_ÉRTÉK();}
    if(Terminál_bejegyzés->탈출상태==1){Terminál_bejegyzés->탈출상태=MPERC_ÉRTÉK=='['?2:0;Terminál_bejegyzés->paraméter_INDEX=0;for(unsigned 순번=0;순번<4;순번++)Terminál_bejegyzés->paraméter_ÉRTÉK[순번]=0;}
    else if(Terminál_bejegyzés->탈출상태==2){if(MPERC_ÉRTÉK=='?'){}else if(MPERC_ÉRTÉK>='0'&&MPERC_ÉRTÉK<='9'){if(Terminál_bejegyzés->paraméter_ÉRTÉK[Terminál_bejegyzés->paraméter_INDEX]<10000)Terminál_bejegyzés->paraméter_ÉRTÉK[Terminál_bejegyzés->paraméter_INDEX]=Terminál_bejegyzés->paraméter_ÉRTÉK[Terminál_bejegyzés->paraméter_INDEX]*10+MPERC_ÉRTÉK-'0';}else if(MPERC_ÉRTÉK==';'&&Terminál_bejegyzés->paraméter_INDEX<3)Terminál_bejegyzés->paraméter_INDEX++;else{leíró_vezérlő_szekvencia(MPERC_ÉRTÉK);Terminál_bejegyzés->탈출상태=0;}}
    else if(MPERC_ÉRTÉK==27){Terminál_bejegyzés->긴부호없는값=0;Terminál_bejegyzés->탈출상태=1;}else{
        if(Terminál_bejegyzés->긴부호없는값&&(MPERC_ÉRTÉK&0xc0)!=0x80){Terminál_bejegyzés->긴부호없는값=0;kódpont_451f2815(0xfffd);}
        if(Terminál_bejegyzés->긴부호없는값){Terminál_bejegyzés->부호없는결과=Terminál_bejegyzés->부호없는결과*64+(MPERC_ÉRTÉK&63);if(--Terminál_bejegyzés->긴부호없는값==0)kódpont_451f2815(Terminál_bejegyzés->부호없는결과<Terminál_bejegyzés->KICSI_ÉRTÉK||Terminál_bejegyzés->부호없는결과>0x10ffff||(Terminál_bejegyzés->부호없는결과>=0xd800&&Terminál_bejegyzés->부호없는결과<=0xdfff)?0xfffd:Terminál_bejegyzés->부호없는결과);}
        else if(MPERC_ÉRTÉK<128)kódpont_451f2815(MPERC_ÉRTÉK);else if(MPERC_ÉRTÉK>=0xc2&&MPERC_ÉRTÉK<=0xf4){Terminál_bejegyzés->긴부호없는값=MPERC_ÉRTÉK<0xe0?1:MPERC_ÉRTÉK<0xf0?2:3;Terminál_bejegyzés->부호없는결과=MPERC_ÉRTÉK&((1u<<(6-Terminál_bejegyzés->긴부호없는값))-1);Terminál_bejegyzés->KICSI_ÉRTÉK=Terminál_bejegyzés->긴부호없는값==1?128:Terminál_bejegyzés->긴부호없는값==2?2048:65536;}else kódpont_451f2815(0xfffd);
    }kalap_jel_ÉRTÉK(1);
}
int Terminál_Függő(void){return informatikai_részleg_Függő!=0;}
/* 모서리 INDEX: 1 좌상, 2 우상, 3 좌하, 4 우하. */
static int méretez_húz=-1,잡은모서리,잡은가로,잡은세로,처음가로,처음세로,처음너비,처음높이;
static int 가리킨창(int 가로,int szektor_pozíció) {
    for(int szekvencia_ÉRTÉK=bejegyzés_DARAB-1;szekvencia_ÉRTÉK>=0;szekvencia_ÉRTÉK--){
        int azonosító_ÉRTÉK=rendel_ÉRTÉK[szekvencia_ÉRTÉK];Terminál_d413d4bc *Ablak=&Windows_Lista[azonosító_ÉRTÉK];
        if(가로>=(int)Ablak->x_koordináta&&szektor_pozíció>=(int)Ablak->Y_koordináta&&
           가로<(int)(Ablak->x_koordináta+Ablak->너비)&&szektor_pozíció<(int)(Ablak->Y_koordináta+Ablak->높이))return azonosító_ÉRTÉK;
    }return -1;
}
static int 모서리찾기(int azonosító_ÉRTÉK,int 가로,int szektor_pozíció) {
    if(azonosító_ÉRTÉK<0)return 0;Terminál_d413d4bc *Ablak=&Windows_Lista[azonosító_ÉRTÉK];
    int 왼쪽=가로<(int)Ablak->x_koordináta+8,jog=가로>=(int)(Ablak->x_koordináta+Ablak->너비)-8;
    int 위쪽=szektor_pozíció<(int)Ablak->Y_koordináta+8,아래쪽=szektor_pozíció>=(int)(Ablak->Y_koordináta+Ablak->높이)-8;
    return (왼쪽||jog)&&(위쪽||아래쪽)?1+jog+아래쪽*2:0;
}
static int elválasztó_ÉRTÉK(int ÉRTÉK,int 최소,int 최대){return ÉRTÉK<최소?최소:ÉRTÉK>최대?최대:ÉRTÉK;}
static void áthelyez_méretez(int 가로,int szektor_pozíció) {
    Terminál_d413d4bc *Ablak=&Windows_Lista[méretez_húz];int 왼쪽=처음가로,위쪽=처음세로,jog=처음가로+처음너비,아래쪽=처음세로+처음높이;
    if(잡은모서리==1||잡은모서리==3)왼쪽=elválasztó_ÉRTÉK(처음가로+가로-잡은가로,0,jog-360);
    else jog=elválasztó_ÉRTÉK(처음가로+처음너비+가로-잡은가로,왼쪽+360,보드화면너비());
    if(잡은모서리<=2)위쪽=elválasztó_ÉRTÉK(처음세로+szektor_pozíció-잡은세로,34,아래쪽-216);
    else 아래쪽=elválasztó_ÉRTÉK(처음세로+처음높이+szektor_pozíció-잡은세로,위쪽+216,보드화면높이());
    unsigned OSZLOPOK=(jog-왼쪽-24)/8,SOR_DARAB=(아래쪽-위쪽-56)/16;
    if(Ablak->OSZLOPOK!=OSZLOPOK||Ablak->SOR_DARAB!=SOR_DARAB){
        Ablak->크기바뀜=1;Ablak->OSZLOPOK=OSZLOPOK;Ablak->SOR_DARAB=SOR_DARAB;
        if(Ablak->OSZLOP_pozíció>=OSZLOPOK)Ablak->OSZLOP_pozíció=OSZLOPOK-1;
        if(Ablak->SOR_pozíció>=Ablak->맨위+SOR_DARAB)Ablak->맨위=Ablak->SOR_pozíció-SOR_DARAB+1;
        unsigned 한도=Ablak->맨위;if(한도>Előzmények_sor_DARAB-SOR_DARAB)한도=Előzmények_sor_DARAB-SOR_DARAB;
        if(Ablak->görget>한도)Ablak->görget=한도;
    }
    int 옛가로=Ablak->x_koordináta,옛세로=Ablak->Y_koordináta,옛폭=Ablak->너비,옛길이=Ablak->높이;
    if(옛가로==왼쪽&&옛세로==위쪽&&옛폭==jog-왼쪽&&옛길이==아래쪽-위쪽)return;
    Ablak->x_koordináta=왼쪽;Ablak->Y_koordináta=위쪽;Ablak->너비=jog-왼쪽;Ablak->높이=아래쪽-위쪽;
    창자리그리기(옛가로,옛세로,옛폭,옛길이,Ablak);
}
void Terminál_mutató(unsigned Tovább_cikk,int x_koordináta,int Y_koordináta){
    unsigned 눌림=Tovább_cikk&~단추들;단추들=Tovább_cikk;
    if(!Asztal_Nézet){húz_ÉRTÉK=-1;méretez_húz=-1;fal_mutató(x_koordináta,Y_koordináta,1);return;}
    if(!(Tovább_cikk&1)){húz_ÉRTÉK=-1;méretez_húz=-1;}
    if(méretez_húz>=0&&!Windows_Lista[méretez_húz].살아있음)méretez_húz=-1;
    if(húz_ÉRTÉK>=0&&!Windows_Lista[húz_ÉRTÉK].살아있음)húz_ÉRTÉK=-1;
    if(méretez_húz>=0){
        áthelyez_méretez(x_koordináta,Y_koordináta);fal_mutató(x_koordináta,Y_koordináta,잡은모서리==1||잡은모서리==4?2:3);return;
    }
    fal_mutató(x_koordináta,Y_koordináta,1);
    if(húz_ÉRTÉK>=0){
        Terminál_d413d4bc *Ablak=&Windows_Lista[húz_ÉRTÉK];
        int 옛가로=Ablak->x_koordináta,옛세로=Ablak->Y_koordináta;
        Ablak->x_koordináta=elválasztó_ÉRTÉK(x_koordináta-húz_X,0,보드화면너비()-Ablak->너비);
        Ablak->Y_koordináta=elválasztó_ÉRTÉK(Y_koordináta-húz_Y,34,보드화면높이()-Ablak->높이);
        if(옛가로!=(int)Ablak->x_koordináta||옛세로!=(int)Ablak->Y_koordináta)창자리그리기(옛가로,옛세로,Ablak->너비,Ablak->높이,Ablak);
        return;
    }
    extern int 화면덮음(int,int,int);
    if(화면덮음(Fókusz,x_koordináta,Y_koordináta)){화면가리킴(Fókusz,눌림,x_koordináta,Y_koordináta);return;}
    int azonosító_ÉRTÉK=가리킨창(x_koordináta,Y_koordináta),모서리=모서리찾기(azonosító_ÉRTÉK,x_koordináta,Y_koordináta);
    if(모서리)fal_mutató(x_koordináta,Y_koordináta,모서리==1||모서리==4?2:3);
    if(눌림&1){
        if(모서리){
            Terminál_d413d4bc *Ablak=&Windows_Lista[azonosító_ÉRTÉK];méretez_húz=azonosító_ÉRTÉK;잡은모서리=모서리;잡은가로=x_koordináta;잡은세로=Y_koordináta;
            처음가로=Ablak->x_koordináta;처음세로=Ablak->Y_koordináta;처음너비=Ablak->너비;처음높이=Ablak->높이;
            if(azonosító_ÉRTÉK!=Fókusz)앞으로올리기(azonosító_ÉRTÉK);return;
        }
        if(Y_koordináta<32&&x_koordináta>=6&&x_koordináta<142){készít_bejegyzés();return;}
        if(Y_koordináta<32&&x_koordináta>=154&&x_koordináta<602){앞으로올리기((x_koordináta-154)/112);return;}
        if(azonosító_ÉRTÉK>=0){
            Terminál_d413d4bc *Ablak=&Windows_Lista[azonosító_ÉRTÉK];
            if(Y_koordináta<(int)Ablak->Y_koordináta+30&&x_koordináta>=(int)(Ablak->x_koordináta+Ablak->너비)-32){bezár_ablak(azonosító_ÉRTÉK);return;}
            if(azonosító_ÉRTÉK!=Fókusz)앞으로올리기(azonosító_ÉRTÉK);
            if(Y_koordináta<(int)Ablak->Y_koordináta+30){húz_ÉRTÉK=azonosító_ÉRTÉK;húz_X=x_koordináta-Ablak->x_koordináta;húz_Y=Y_koordináta-Ablak->Y_koordináta;}return;
        }
    }
    if(Fókusz>=0&&(눌림&(8|16))){Terminál_bejegyzés=&Windows_Lista[Fókusz];if(눌림&8){unsigned 한도=Terminál_bejegyzés->맨위;if(한도>Előzmények_sor_DARAB-Terminál_bejegyzés->SOR_DARAB)한도=Előzmények_sor_DARAB-Terminál_bejegyzés->SOR_DARAB;Terminál_bejegyzés->görget=Terminál_bejegyzés->görget+9>한도?한도:Terminál_bejegyzés->görget+9;}else Terminál_bejegyzés->görget=Terminál_bejegyzés->görget<9?0:Terminál_bejegyzés->görget-9;다시그리기();}
}
void 터미널바로가기키(unsigned 누름값){if(누름값==1)készít_bejegyzés();if(누름값==2&&bejegyzés_DARAB)앞으로올리기(rendel_ÉRTÉK[0]);if(누름값==3)bezár_ablak(Fókusz);}
gép_szó fal_Terminál(gép_szó Művelet){
    if(Művelet==300){if(!Windows_Lista[kimenet].살아있음)return készít_bejegyzés();Asztal_Nézet=1;다시그리기();return 0;}
    if(Művelet==0){bezár_ablak(Fókusz);return 0;}if(Művelet==1)return (uint32_t)készít_bejegyzés();if(Művelet==2)return Fókusz>=0;
    if(Művelet==9){Asztal_Nézet=0;return 0;}if(Művelet==7)return bejegyzés_DARAB;if(Művelet==10)return Fókusz+1;if(Művelet==11)return kimenet;
    if(Művelet==13){Terminál_d413d4bc *Ablak=&Windows_Lista[kimenet];return Ablak->살아있음?(Ablak->SOR_DARAB<<16)|Ablak->OSZLOPOK:(19<<16)|68;}
    if(Művelet==14){unsigned ÉRTÉK=Windows_Lista[kimenet].크기바뀜;Windows_Lista[kimenet].크기바뀜=0;return ÉRTÉK;}
    if(Művelet==12){unsigned ÉRTÉK=informatikai_részleg_Függő;informatikai_részleg_Függő=0;return ÉRTÉK;}
    if(Művelet>=20&&Művelet<24)return Windows_Lista[Művelet-20].살아있음;
    if(Művelet>=100&&Művelet<104){kimenet=Művelet-100;Terminál_bejegyzés=&Windows_Lista[kimenet];return 0;}
    if(Művelet>=200&&Művelet<204){앞으로올리기(Művelet-200);return 0;}
    if(Művelet==3){다시그리기();return 0;}Terminál_bejegyzés=&Windows_Lista[kimenet];if(!Terminál_bejegyzés->살아있음)return 0;
    if(Művelet==4)töröl_Tartalom();if(Művelet==5||Művelet==6){unsigned Előző_cikk=단추들;Terminál_mutató(Művelet==5?8:16,0,0);단추들=Előző_cikk;}return 1;
}
