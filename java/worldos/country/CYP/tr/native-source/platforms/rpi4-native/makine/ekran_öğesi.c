#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* Small native peer layer for the explicitly supported Swing subset. */
#include <stdint.h>
#include <stddef.h>
extern uintptr_t Pano_piksel(uintptr_t,uintptr_t,uintptr_t),Pano_Terminal(uintptr_t);
extern void Terminal_karakter(unsigned,unsigned,unsigned,unsigned,unsigned);
extern void *memset(void *,int,size_t);
typedef struct { int alan_değer,ana,x_koordinatı,Y_koordinat,너비값,높이값,보이는지,el_ile_Düzen,Düzen_ilke;unsigned metin[128],süre_değer; } widget_Durum;
static widget_Durum 요소들[4][32];
static int Odaklanmış[4],olay_Liste[4][16];static unsigned 첫항목[4],girdi_BAĞ_DEĞ_SAY[4],부호없는결과[4],긴부호없는값[4];
static void Olay(int sahip_nesne,int değer){if(girdi_BAĞ_DEĞ_SAY[sahip_nesne]<16){olay_Liste[sahip_nesne][(첫항목[sahip_nesne]+girdi_BAĞ_DEĞ_SAY[sahip_nesne])%16]=değer;girdi_BAĞ_DEĞ_SAY[sahip_nesne]++;}}
static widget_Durum *öğe_değer(int sahip_nesne,int tanımlayıcı_değer){return sahip_nesne>=0&&sahip_nesne<4&&tanımlayıcı_değer>0&&tanımlayıcı_değer<=32&&요소들[sahip_nesne][tanımlayıcı_değer-1].alan_değer?&요소들[sahip_nesne][tanımlayıcı_değer-1]:0;}
static void 사각영역(int x_koordinatı,int Y_koordinat,int 너비값,int 높이값,unsigned 색상){Pano_dikdörtgen_dolgu(x_koordinatı,Y_koordinat,너비값,높이값,색상);}
int 화면보임(int sahip_nesne){if(sahip_nesne<0||sahip_nesne>=4)return 0;for(int 순번=0;순번<32;순번++)if(요소들[sahip_nesne][순번].alan_değer==1&&요소들[sahip_nesne][순번].보이는지)return 1;return 0;}
void 화면초기화(int sahip_nesne){memset(요소들[sahip_nesne],0,sizeof(요소들[sahip_nesne]));girdi_BAĞ_DEĞ_SAY[sahip_nesne]=첫항목[sahip_nesne]=Odaklanmış[sahip_nesne]=긴부호없는값[sahip_nesne]=0;}
static void konum(int sahip_nesne,widget_Durum *너비값,int *x_koordinatı,int *Y_koordinat){*x_koordinatı=너비값->x_koordinatı;*Y_koordinat=너비값->Y_koordinat;int veri_konum=너비값->ana;for(int öğe_BAĞ_DEĞ_SAY=0;veri_konum&&öğe_BAĞ_DEĞ_SAY<32;öğe_BAĞ_DEĞ_SAY++){widget_Durum *위쪽=öğe_değer(sahip_nesne,veri_konum);if(!위쪽)break;*x_koordinatı+=위쪽->x_koordinatı;*Y_koordinat+=위쪽->Y_koordinat+(위쪽->alan_değer==1?30:0);veri_konum=위쪽->ana;}}
static int 표시됨(int sahip_nesne,widget_Durum *너비값){for(int öğe_BAĞ_DEĞ_SAY=0;öğe_BAĞ_DEĞ_SAY<32;öğe_BAĞ_DEĞ_SAY++){if(!너비값->보이는지)return 0;if(너비값->alan_değer==1)return 1;너비값=öğe_değer(sahip_nesne,너비값->ana);if(!너비값)return 0;}return 0;}
static void metin(int x_koordinatı,int Y_koordinat,widget_Durum *너비값,int 최대값,unsigned 색상,unsigned 배경색){int geçerli_konum=0;for(unsigned 순번=0;순번<너비값->süre_değer;순번++){unsigned karakter_kodlaması=너비값->metin[순번],너비=karakter_kodlaması>=256?16:8;if(geçerli_konum+(int)너비>최대값)break;Terminal_karakter(x_koordinatı+geçerli_konum,Y_koordinat,karakter_kodlaması,색상,배경색);geçerli_konum+=너비;}}
void 화면다시그림(int sahip_nesne){
    if(!화면보임(sahip_nesne))return;
    for(int işleniyor_düzen=1;işleniyor_düzen<=5;işleniyor_düzen++)for(int 순번=0;순번<32;순번++){
        widget_Durum *너비값=&요소들[sahip_nesne][순번];if(너비값->alan_değer!=işleniyor_düzen||!표시됨(sahip_nesne,너비값))continue;int x_koordinatı,Y_koordinat;konum(sahip_nesne,너비값,&x_koordinatı,&Y_koordinat);
        if(işleniyor_düzen==1){사각영역(x_koordinatı,Y_koordinat,너비값->너비값,너비값->높이값,0xeee9e0);사각영역(x_koordinatı,Y_koordinat,너비값->너비값,30,0x905020);metin(x_koordinatı+10,Y_koordinat+7,너비값,너비값->너비값-50,0xffffff,0x905020);사각영역(x_koordinatı+너비값->너비값-28,Y_koordinat+4,24,22,0x5555b8);Terminal_karakter(x_koordinatı+너비값->너비값-20,Y_koordinat+7,'X',0xffffff,0x5555b8);}
        if(işleniyor_düzen==2)사각영역(x_koordinatı,Y_koordinat,너비값->너비값,너비값->높이값,0xeee9e0);
        if(işleniyor_düzen>=3){unsigned 배경색=işleniyor_düzen==4?0xc0ab86:işleniyor_düzen==5?0xffffff:0xeee9e0;if(işleniyor_düzen!=3)사각영역(x_koordinatı,Y_koordinat,너비값->너비값,너비값->높이값,배경색);metin(x_koordinatı+4,Y_koordinat+4,너비값,너비값->너비값-8,0x201a15,배경색);if(işleniyor_düzen==5&&Odaklanmış[sahip_nesne]==순번+1)사각영역(x_koordinatı,Y_koordinat+너비값->높이값-2,너비값->너비값,2,0x905020);}
    }
}
int 화면덮음(int sahip_nesne,int x_koordinatı,int Y_koordinat){
    if(!화면보임(sahip_nesne))return 0;
    for(int 순번=0;순번<32;순번++){
        widget_Durum *Pencere=&요소들[sahip_nesne][순번];
        if(Pencere->alan_değer==1&&Pencere->보이는지&&x_koordinatı>=Pencere->x_koordinatı&&Y_koordinat>=Pencere->Y_koordinat&&
           x_koordinatı<Pencere->x_koordinatı+Pencere->너비값&&Y_koordinat<Pencere->Y_koordinat+Pencere->높이값)return 1;
    }return 0;
}
int 화면가리킴(int sahip_nesne,unsigned 눌림,int x_koordinatı,int Y_koordinat){
    if(!화면보임(sahip_nesne))return 0;
    if(눌림&1)for(int 순번=31;순번>=0;순번--){widget_Durum *너비값=&요소들[sahip_nesne][순번];if(!너비값->alan_değer||!표시됨(sahip_nesne,너비값))continue;int pencere_X,pencere_Y;konum(sahip_nesne,너비값,&pencere_X,&pencere_Y);
        if(x_koordinatı<pencere_X||Y_koordinat<pencere_Y||x_koordinatı>=pencere_X+너비값->너비값||Y_koordinat>=pencere_Y+너비값->높이값)continue;
        if(너비값->alan_değer==1&&Y_koordinat<pencere_Y+30&&x_koordinatı>=pencere_X+너비값->너비값-28){if(너비값->Düzen_ilke!=0)너비값->보이는지=0;Olay(sahip_nesne,0x10000+순번+1);Pano_Terminal(3);return 1;}
        if(너비값->alan_değer==4){Olay(sahip_nesne,순번+1);return 1;}if(너비값->alan_değer==5){Odaklanmış[sahip_nesne]=순번+1;Pano_Terminal(3);return 1;}
        if(너비값->alan_değer==1)return 1;
    }return 0;
}
void 화면누름(int sahip_nesne,unsigned SANİYE_değer){
    widget_Durum *너비값=öğe_değer(sahip_nesne,Odaklanmış[sahip_nesne]);if(!너비값||너비값->alan_değer!=5)return;
    if(SANİYE_değer==13||SANİYE_değer==10){Olay(sahip_nesne,Odaklanmış[sahip_nesne]);return;}
    if(SANİYE_değer==8||SANİYE_değer==127){if(너비값->süre_değer)너비값->süre_değer--;긴부호없는값[sahip_nesne]=0;}
    else{
        unsigned karakter_kodlaması=SANİYE_değer;
        if(긴부호없는값[sahip_nesne]){if((SANİYE_değer&192)!=128){긴부호없는값[sahip_nesne]=0;return;}부호없는결과[sahip_nesne]=(부호없는결과[sahip_nesne]<<6)|(SANİYE_değer&63);if(--긴부호없는값[sahip_nesne])return;karakter_kodlaması=부호없는결과[sahip_nesne];}
        else if(SANİYE_değer>=0xc2&&SANİYE_değer<=0xf4){긴부호없는값[sahip_nesne]=SANİYE_değer<0xe0?1:SANİYE_değer<0xf0?2:3;부호없는결과[sahip_nesne]=SANİYE_değer&((1u<<(6-긴부호없는값[sahip_nesne]))-1);return;}
        else if(SANİYE_değer<32||SANİYE_değer>=128)return;
        if(karakter_kodlaması>0x10ffff||(karakter_kodlaması>=0xd800&&karakter_kodlaması<=0xdfff))return;if(너비값->süre_değer<127)너비값->metin[너비값->süre_değer++]=karakter_kodlaması;
    }
    Pano_Terminal(3);
}
int 화면호출(int sahip_nesne,unsigned Eylem,int tanımlayıcı_değer,int 첫째값,int SANİYE_değer,int kod_noktası,int hedef_veri){
    if(sahip_nesne<0||sahip_nesne>=4)return -22;widget_Durum *너비값=öğe_değer(sahip_nesne,tanımlayıcı_değer);
    if(Eylem==0){if(tanımlayıcı_değer<1||tanımlayıcı_değer>5)return -22;for(int 순번=0;순번<32;순번++)if(요소들[sahip_nesne][순번].alan_değer==0){너비값=&요소들[sahip_nesne][순번];memset(너비값,0,sizeof(*너비값));너비값->alan_değer=tanımlayıcı_değer;너비값->보이는지=tanımlayıcı_değer!=1;너비값->너비값=tanımlayıcı_değer==1?380:220;너비값->높이값=tanımlayıcı_değer==1?240:28;너비값->Düzen_ilke=1;너비값->x_koordinatı=tanımlayıcı_değer==1?130:16;너비값->Y_koordinat=tanımlayıcı_değer==1?110:16;return 순번+1;}return -28;}
    if(Eylem==5){if(!girdi_BAĞ_DEĞ_SAY[sahip_nesne])return 0;int 반환값=olay_Liste[sahip_nesne][첫항목[sahip_nesne]];첫항목[sahip_nesne]=(첫항목[sahip_nesne]+1)%16;girdi_BAĞ_DEĞ_SAY[sahip_nesne]--;return 반환값;}
    if(Eylem==6)return 화면보임(sahip_nesne);
    if(!너비값)return -9;
    int 이전표시=표시됨(sahip_nesne,너비값);
    if(Eylem==1){int 바탕너비=보드화면너비(),바탕높이=보드화면높이();if(첫째값<0||SANİYE_değer<0||kod_noktası<1||hedef_veri<1||첫째값>바탕너비||SANİYE_değer>바탕높이||kod_noktası>바탕너비-첫째값||hedef_veri>바탕높이-SANİYE_değer)return -22;너비값->x_koordinatı=첫째값;너비값->Y_koordinat=SANİYE_değer;너비값->너비값=kod_noktası;너비값->높이값=hedef_veri;너비값->el_ile_Düzen=1;}
    else if(Eylem==2){widget_Durum *alt_öğe=öğe_değer(sahip_nesne,첫째값);if(!alt_öğe||alt_öğe==너비값||alt_öğe->alan_değer==1)return -22;int veri_konum=tanımlayıcı_değer;for(int 깊이=0;veri_konum&&깊이<32;깊이++){if(veri_konum==첫째값)return -22;widget_Durum *위쪽=öğe_değer(sahip_nesne,veri_konum);veri_konum=위쪽?위쪽->ana:0;}alt_öğe->ana=tanımlayıcı_değer;if(!alt_öğe->el_ile_Düzen){int 형제요소=0;for(int 순번=0;순번<32;순번++)if(&요소들[sahip_nesne][순번]!=alt_öğe&&요소들[sahip_nesne][순번].ana==tanımlayıcı_değer)형제요소++;alt_öğe->Y_koordinat=16+형제요소*36;}}
    else if(Eylem==3)너비값->보이는지=첫째값!=0;
    else if(Eylem==4)너비값->보이는지=0;
    else if(Eylem==7)너비값->Düzen_ilke=첫째값;
    else if(Eylem==8)return 너비값->süre_değer;
    else if(Eylem==9)return 첫째값>=0&&(unsigned)첫째값<너비값->süre_değer?너비값->metin[첫째값]:-22;
    else return -22;
    if(이전표시||표시됨(sahip_nesne,너비값))Pano_Terminal(3);return 0;
}
int 화면글(int sahip_nesne,int tanımlayıcı_değer,const uint32_t *veri,unsigned öğe_BAĞ_DEĞ_SAY){widget_Durum *너비값=öğe_değer(sahip_nesne,tanımlayıcı_değer);if(!너비값)return -9;if(öğe_BAĞ_DEĞ_SAY>127)return -22;for(unsigned 순번=0;순번<öğe_BAĞ_DEĞ_SAY;순번++){unsigned karakter_kodlaması=veri[순번];if(karakter_kodlaması>0x10ffff||(karakter_kodlaması>=0xd800&&karakter_kodlaması<=0xdfff))return -22;}for(unsigned 순번=0;순번<öğe_BAĞ_DEĞ_SAY;순번++)너비값->metin[순번]=veri[순번];너비값->süre_değer=öğe_BAĞ_DEĞ_SAY;if(표시됨(sahip_nesne,너비값))Pano_Terminal(3);return 0;}
