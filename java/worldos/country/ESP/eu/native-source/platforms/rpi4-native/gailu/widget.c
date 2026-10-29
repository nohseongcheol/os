#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* Small native peer layer for the explicitly supported Swing subset. */
#include <stdint.h>
#include <stddef.h>
extern uintptr_t arbel_pixel(uintptr_t,uintptr_t,uintptr_t),arbel_Terminal(uintptr_t);
extern void Terminal_glifo(unsigned,unsigned,unsigned,unsigned,unsigned);
extern void *memset(void *,int,size_t);
typedef struct { int Kategoria_balio,부모항목,X_koordenatu,Y_koordenatu,너비값,높이값,보이는지,eskuzko_diseinu,diseinu_gidalerro;unsigned Testua[128],luzera_balio; } widget_Egoera;
static widget_Egoera 요소들[4][32];
static int Lehentasunezkoak[4],gertaera_Zerrenda[4][16];static unsigned 첫항목[4],sarrera_ZENBATU[4],부호없는결과[4],긴부호없는값[4];
static void Gertaera(int jabe_objektu,int balio){if(sarrera_ZENBATU[jabe_objektu]<16){gertaera_Zerrenda[jabe_objektu][(첫항목[jabe_objektu]+sarrera_ZENBATU[jabe_objektu])%16]=balio;sarrera_ZENBATU[jabe_objektu]++;}}
static widget_Egoera *elementu_balio(int jabe_objektu,int identifikatzaile_balio){return jabe_objektu>=0&&jabe_objektu<4&&identifikatzaile_balio>0&&identifikatzaile_balio<=32&&요소들[jabe_objektu][identifikatzaile_balio-1].Kategoria_balio?&요소들[jabe_objektu][identifikatzaile_balio-1]:0;}
static void 사각영역(int X_koordenatu,int Y_koordenatu,int 너비값,int 높이값,unsigned 색상){보드사각그림(X_koordenatu,Y_koordenatu,너비값,높이값,색상);}
int 화면보임(int jabe_objektu){if(jabe_objektu<0||jabe_objektu>=4)return 0;for(int 순번=0;순번<32;순번++)if(요소들[jabe_objektu][순번].Kategoria_balio==1&&요소들[jabe_objektu][순번].보이는지)return 1;return 0;}
void 화면초기화(int jabe_objektu){memset(요소들[jabe_objektu],0,sizeof(요소들[jabe_objektu]));sarrera_ZENBATU[jabe_objektu]=첫항목[jabe_objektu]=Lehentasunezkoak[jabe_objektu]=긴부호없는값[jabe_objektu]=0;}
static void Posizioa(int jabe_objektu,widget_Egoera *너비값,int *X_koordenatu,int *Y_koordenatu){*X_koordenatu=너비값->X_koordenatu;*Y_koordenatu=너비값->Y_koordenatu;int datuak_kargu=너비값->부모항목;for(int elementu_ZENBATU=0;datuak_kargu&&elementu_ZENBATU<32;elementu_ZENBATU++){widget_Egoera *위쪽=elementu_balio(jabe_objektu,datuak_kargu);if(!위쪽)break;*X_koordenatu+=위쪽->X_koordenatu;*Y_koordenatu+=위쪽->Y_koordenatu+(위쪽->Kategoria_balio==1?30:0);datuak_kargu=위쪽->부모항목;}}
static int 표시됨(int jabe_objektu,widget_Egoera *너비값){for(int elementu_ZENBATU=0;elementu_ZENBATU<32;elementu_ZENBATU++){if(!너비값->보이는지)return 0;if(너비값->Kategoria_balio==1)return 1;너비값=elementu_balio(jabe_objektu,너비값->부모항목);if(!너비값)return 0;}return 0;}
static void Testua(int X_koordenatu,int Y_koordenatu,widget_Egoera *너비값,int 최대값,unsigned 색상,unsigned 배경색){int 현재위치=0;for(unsigned 순번=0;순번<너비값->luzera_balio;순번++){unsigned karaktere_kodeketa=너비값->Testua[순번],너비=karaktere_kodeketa>=256?16:8;if(현재위치+(int)너비>최대값)break;Terminal_glifo(X_koordenatu+현재위치,Y_koordenatu,karaktere_kodeketa,색상,배경색);현재위치+=너비;}}
void 화면다시그림(int jabe_objektu){
    if(!화면보임(jabe_objektu))return;
    for(int prozesatze_ordena=1;prozesatze_ordena<=5;prozesatze_ordena++)for(int 순번=0;순번<32;순번++){
        widget_Egoera *너비값=&요소들[jabe_objektu][순번];if(너비값->Kategoria_balio!=prozesatze_ordena||!표시됨(jabe_objektu,너비값))continue;int X_koordenatu,Y_koordenatu;Posizioa(jabe_objektu,너비값,&X_koordenatu,&Y_koordenatu);
        if(prozesatze_ordena==1){사각영역(X_koordenatu,Y_koordenatu,너비값->너비값,너비값->높이값,0xeee9e0);사각영역(X_koordenatu,Y_koordenatu,너비값->너비값,30,0x905020);Testua(X_koordenatu+10,Y_koordenatu+7,너비값,너비값->너비값-50,0xffffff,0x905020);사각영역(X_koordenatu+너비값->너비값-28,Y_koordenatu+4,24,22,0x5555b8);Terminal_glifo(X_koordenatu+너비값->너비값-20,Y_koordenatu+7,'X',0xffffff,0x5555b8);}
        if(prozesatze_ordena==2)사각영역(X_koordenatu,Y_koordenatu,너비값->너비값,너비값->높이값,0xeee9e0);
        if(prozesatze_ordena>=3){unsigned 배경색=prozesatze_ordena==4?0xc0ab86:prozesatze_ordena==5?0xffffff:0xeee9e0;if(prozesatze_ordena!=3)사각영역(X_koordenatu,Y_koordenatu,너비값->너비값,너비값->높이값,배경색);Testua(X_koordenatu+4,Y_koordenatu+4,너비값,너비값->너비값-8,0x201a15,배경색);if(prozesatze_ordena==5&&Lehentasunezkoak[jabe_objektu]==순번+1)사각영역(X_koordenatu,Y_koordenatu+너비값->높이값-2,너비값->너비값,2,0x905020);}
    }
}
int 화면덮음(int jabe_objektu,int X_koordenatu,int Y_koordenatu){
    if(!화면보임(jabe_objektu))return 0;
    for(int 순번=0;순번<32;순번++){
        widget_Egoera *Leihoa=&요소들[jabe_objektu][순번];
        if(Leihoa->Kategoria_balio==1&&Leihoa->보이는지&&X_koordenatu>=Leihoa->X_koordenatu&&Y_koordenatu>=Leihoa->Y_koordenatu&&
           X_koordenatu<Leihoa->X_koordenatu+Leihoa->너비값&&Y_koordenatu<Leihoa->Y_koordenatu+Leihoa->높이값)return 1;
    }return 0;
}
int 화면가리킴(int jabe_objektu,unsigned 눌림,int X_koordenatu,int Y_koordenatu){
    if(!화면보임(jabe_objektu))return 0;
    if(눌림&1)for(int 순번=31;순번>=0;순번--){widget_Egoera *너비값=&요소들[jabe_objektu][순번];if(!너비값->Kategoria_balio||!표시됨(jabe_objektu,너비값))continue;int leiho_X,leiho_Y;Posizioa(jabe_objektu,너비값,&leiho_X,&leiho_Y);
        if(X_koordenatu<leiho_X||Y_koordenatu<leiho_Y||X_koordenatu>=leiho_X+너비값->너비값||Y_koordenatu>=leiho_Y+너비값->높이값)continue;
        if(너비값->Kategoria_balio==1&&Y_koordenatu<leiho_Y+30&&X_koordenatu>=leiho_X+너비값->너비값-28){if(너비값->diseinu_gidalerro!=0)너비값->보이는지=0;Gertaera(jabe_objektu,0x10000+순번+1);arbel_Terminal(3);return 1;}
        if(너비값->Kategoria_balio==4){Gertaera(jabe_objektu,순번+1);return 1;}if(너비값->Kategoria_balio==5){Lehentasunezkoak[jabe_objektu]=순번+1;arbel_Terminal(3);return 1;}
        if(너비값->Kategoria_balio==1)return 1;
    }return 0;
}
void 화면누름(int jabe_objektu,unsigned SEGUNDOA_balio){
    widget_Egoera *너비값=elementu_balio(jabe_objektu,Lehentasunezkoak[jabe_objektu]);if(!너비값||너비값->Kategoria_balio!=5)return;
    if(SEGUNDOA_balio==13||SEGUNDOA_balio==10){Gertaera(jabe_objektu,Lehentasunezkoak[jabe_objektu]);return;}
    if(SEGUNDOA_balio==8||SEGUNDOA_balio==127){if(너비값->luzera_balio)너비값->luzera_balio--;긴부호없는값[jabe_objektu]=0;}
    else{
        unsigned karaktere_kodeketa=SEGUNDOA_balio;
        if(긴부호없는값[jabe_objektu]){if((SEGUNDOA_balio&192)!=128){긴부호없는값[jabe_objektu]=0;return;}부호없는결과[jabe_objektu]=(부호없는결과[jabe_objektu]<<6)|(SEGUNDOA_balio&63);if(--긴부호없는값[jabe_objektu])return;karaktere_kodeketa=부호없는결과[jabe_objektu];}
        else if(SEGUNDOA_balio>=0xc2&&SEGUNDOA_balio<=0xf4){긴부호없는값[jabe_objektu]=SEGUNDOA_balio<0xe0?1:SEGUNDOA_balio<0xf0?2:3;부호없는결과[jabe_objektu]=SEGUNDOA_balio&((1u<<(6-긴부호없는값[jabe_objektu]))-1);return;}
        else if(SEGUNDOA_balio<32||SEGUNDOA_balio>=128)return;
        if(karaktere_kodeketa>0x10ffff||(karaktere_kodeketa>=0xd800&&karaktere_kodeketa<=0xdfff))return;if(너비값->luzera_balio<127)너비값->Testua[너비값->luzera_balio++]=karaktere_kodeketa;
    }
    arbel_Terminal(3);
}
int 화면호출(int jabe_objektu,unsigned Ekintza,int identifikatzaile_balio,int 첫째값,int SEGUNDOA_balio,int karaktere_kode,int helburu_datuak){
    if(jabe_objektu<0||jabe_objektu>=4)return -22;widget_Egoera *너비값=elementu_balio(jabe_objektu,identifikatzaile_balio);
    if(Ekintza==0){if(identifikatzaile_balio<1||identifikatzaile_balio>5)return -22;for(int 순번=0;순번<32;순번++)if(요소들[jabe_objektu][순번].Kategoria_balio==0){너비값=&요소들[jabe_objektu][순번];memset(너비값,0,sizeof(*너비값));너비값->Kategoria_balio=identifikatzaile_balio;너비값->보이는지=identifikatzaile_balio!=1;너비값->너비값=identifikatzaile_balio==1?380:220;너비값->높이값=identifikatzaile_balio==1?240:28;너비값->diseinu_gidalerro=1;너비값->X_koordenatu=identifikatzaile_balio==1?130:16;너비값->Y_koordenatu=identifikatzaile_balio==1?110:16;return 순번+1;}return -28;}
    if(Ekintza==5){if(!sarrera_ZENBATU[jabe_objektu])return 0;int 반환값=gertaera_Zerrenda[jabe_objektu][첫항목[jabe_objektu]];첫항목[jabe_objektu]=(첫항목[jabe_objektu]+1)%16;sarrera_ZENBATU[jabe_objektu]--;return 반환값;}
    if(Ekintza==6)return 화면보임(jabe_objektu);
    if(!너비값)return -9;
    int 이전표시=표시됨(jabe_objektu,너비값);
    if(Ekintza==1){int 바탕너비=보드화면너비(),바탕높이=보드화면높이();if(첫째값<0||SEGUNDOA_balio<0||karaktere_kode<1||helburu_datuak<1||첫째값>바탕너비||SEGUNDOA_balio>바탕높이||karaktere_kode>바탕너비-첫째값||helburu_datuak>바탕높이-SEGUNDOA_balio)return -22;너비값->X_koordenatu=첫째값;너비값->Y_koordenatu=SEGUNDOA_balio;너비값->너비값=karaktere_kode;너비값->높이값=helburu_datuak;너비값->eskuzko_diseinu=1;}
    else if(Ekintza==2){widget_Egoera *elementu_ume=elementu_balio(jabe_objektu,첫째값);if(!elementu_ume||elementu_ume==너비값||elementu_ume->Kategoria_balio==1)return -22;int datuak_kargu=identifikatzaile_balio;for(int 깊이=0;datuak_kargu&&깊이<32;깊이++){if(datuak_kargu==첫째값)return -22;widget_Egoera *위쪽=elementu_balio(jabe_objektu,datuak_kargu);datuak_kargu=위쪽?위쪽->부모항목:0;}elementu_ume->부모항목=identifikatzaile_balio;if(!elementu_ume->eskuzko_diseinu){int 형제요소=0;for(int 순번=0;순번<32;순번++)if(&요소들[jabe_objektu][순번]!=elementu_ume&&요소들[jabe_objektu][순번].부모항목==identifikatzaile_balio)형제요소++;elementu_ume->Y_koordenatu=16+형제요소*36;}}
    else if(Ekintza==3)너비값->보이는지=첫째값!=0;
    else if(Ekintza==4)너비값->보이는지=0;
    else if(Ekintza==7)너비값->diseinu_gidalerro=첫째값;
    else if(Ekintza==8)return 너비값->luzera_balio;
    else if(Ekintza==9)return 첫째값>=0&&(unsigned)첫째값<너비값->luzera_balio?너비값->Testua[첫째값]:-22;
    else return -22;
    if(이전표시||표시됨(jabe_objektu,너비값))arbel_Terminal(3);return 0;
}
int 화면글(int jabe_objektu,int identifikatzaile_balio,const uint32_t *datuak,unsigned elementu_ZENBATU){widget_Egoera *너비값=elementu_balio(jabe_objektu,identifikatzaile_balio);if(!너비값)return -9;if(elementu_ZENBATU>127)return -22;for(unsigned 순번=0;순번<elementu_ZENBATU;순번++){unsigned karaktere_kodeketa=datuak[순번];if(karaktere_kodeketa>0x10ffff||(karaktere_kodeketa>=0xd800&&karaktere_kodeketa<=0xdfff))return -22;}for(unsigned 순번=0;순번<elementu_ZENBATU;순번++)너비값->Testua[순번]=datuak[순번];너비값->luzera_balio=elementu_ZENBATU;if(표시됨(jabe_objektu,너비값))arbel_Terminal(3);return 0;}
