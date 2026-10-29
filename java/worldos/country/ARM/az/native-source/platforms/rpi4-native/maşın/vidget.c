#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* Small native peer layer for the explicitly supported Swing subset. */
#include <stdint.h>
#include <stddef.h>
extern uintptr_t lövhə_piksel(uintptr_t,uintptr_t,uintptr_t),lövhə_Terminal(uintptr_t);
extern void Terminal_qlif(unsigned,unsigned,unsigned,unsigned,unsigned);
extern void *memset(void *,int,size_t);
typedef struct { int sahə_VALUE,부모항목,x_koordinatı,Y_koordinat,너비값,높이값,보이는지,əl_ilə_Düzüm,Düzüm_siyasət;unsigned Mətn[128],uzunluq_VALUE; } vidget_vəziyyət;
static vidget_vəziyyət 요소들[4][32];
static int Fokuslanmış[4],hadisə_Siyahı[4][16];static unsigned 첫항목[4],daxiletmə_COUNT[4],부호없는결과[4],긴부호없는값[4];
static void hadisə(int sahib_obyekt,int VALUE){if(daxiletmə_COUNT[sahib_obyekt]<16){hadisə_Siyahı[sahib_obyekt][(첫항목[sahib_obyekt]+daxiletmə_COUNT[sahib_obyekt])%16]=VALUE;daxiletmə_COUNT[sahib_obyekt]++;}}
static vidget_vəziyyət *element_VALUE(int sahib_obyekt,int identifikator_VALUE){return sahib_obyekt>=0&&sahib_obyekt<4&&identifikator_VALUE>0&&identifikator_VALUE<=32&&요소들[sahib_obyekt][identifikator_VALUE-1].sahə_VALUE?&요소들[sahib_obyekt][identifikator_VALUE-1]:0;}
static void 사각영역(int x_koordinatı,int Y_koordinat,int 너비값,int 높이값,unsigned 색상){보드사각그림(x_koordinatı,Y_koordinat,너비값,높이값,색상);}
int 화면보임(int sahib_obyekt){if(sahib_obyekt<0||sahib_obyekt>=4)return 0;for(int 순번=0;순번<32;순번++)if(요소들[sahib_obyekt][순번].sahə_VALUE==1&&요소들[sahib_obyekt][순번].보이는지)return 1;return 0;}
void 화면초기화(int sahib_obyekt){memset(요소들[sahib_obyekt],0,sizeof(요소들[sahib_obyekt]));daxiletmə_COUNT[sahib_obyekt]=첫항목[sahib_obyekt]=Fokuslanmış[sahib_obyekt]=긴부호없는값[sahib_obyekt]=0;}
static void yerinə_qoymaq(int sahib_obyekt,vidget_vəziyyət *너비값,int *x_koordinatı,int *Y_koordinat){*x_koordinatı=너비값->x_koordinatı;*Y_koordinat=너비값->Y_koordinat;int verilənlər_yerinə_qoymaq=너비값->부모항목;for(int element_COUNT=0;verilənlər_yerinə_qoymaq&&element_COUNT<32;element_COUNT++){vidget_vəziyyət *위쪽=element_VALUE(sahib_obyekt,verilənlər_yerinə_qoymaq);if(!위쪽)break;*x_koordinatı+=위쪽->x_koordinatı;*Y_koordinat+=위쪽->Y_koordinat+(위쪽->sahə_VALUE==1?30:0);verilənlər_yerinə_qoymaq=위쪽->부모항목;}}
static int 표시됨(int sahib_obyekt,vidget_vəziyyət *너비값){for(int element_COUNT=0;element_COUNT<32;element_COUNT++){if(!너비값->보이는지)return 0;if(너비값->sahə_VALUE==1)return 1;너비값=element_VALUE(sahib_obyekt,너비값->부모항목);if(!너비값)return 0;}return 0;}
static void Mətn(int x_koordinatı,int Y_koordinat,vidget_vəziyyət *너비값,int 최대값,unsigned 색상,unsigned 배경색){int 현재위치=0;for(unsigned 순번=0;순번<너비값->uzunluq_VALUE;순번++){unsigned simvol_kodlaşdırma=너비값->Mətn[순번],너비=simvol_kodlaşdırma>=256?16:8;if(현재위치+(int)너비>최대값)break;Terminal_qlif(x_koordinatı+현재위치,Y_koordinat,simvol_kodlaşdırma,색상,배경색);현재위치+=너비;}}
void 화면다시그림(int sahib_obyekt){
    if(!화면보임(sahib_obyekt))return;
    for(int 처리차례=1;처리차례<=5;처리차례++)for(int 순번=0;순번<32;순번++){
        vidget_vəziyyət *너비값=&요소들[sahib_obyekt][순번];if(너비값->sahə_VALUE!=처리차례||!표시됨(sahib_obyekt,너비값))continue;int x_koordinatı,Y_koordinat;yerinə_qoymaq(sahib_obyekt,너비값,&x_koordinatı,&Y_koordinat);
        if(처리차례==1){사각영역(x_koordinatı,Y_koordinat,너비값->너비값,너비값->높이값,0xeee9e0);사각영역(x_koordinatı,Y_koordinat,너비값->너비값,30,0x905020);Mətn(x_koordinatı+10,Y_koordinat+7,너비값,너비값->너비값-50,0xffffff,0x905020);사각영역(x_koordinatı+너비값->너비값-28,Y_koordinat+4,24,22,0x5555b8);Terminal_qlif(x_koordinatı+너비값->너비값-20,Y_koordinat+7,'X',0xffffff,0x5555b8);}
        if(처리차례==2)사각영역(x_koordinatı,Y_koordinat,너비값->너비값,너비값->높이값,0xeee9e0);
        if(처리차례>=3){unsigned 배경색=처리차례==4?0xc0ab86:처리차례==5?0xffffff:0xeee9e0;if(처리차례!=3)사각영역(x_koordinatı,Y_koordinat,너비값->너비값,너비값->높이값,배경색);Mətn(x_koordinatı+4,Y_koordinat+4,너비값,너비값->너비값-8,0x201a15,배경색);if(처리차례==5&&Fokuslanmış[sahib_obyekt]==순번+1)사각영역(x_koordinatı,Y_koordinat+너비값->높이값-2,너비값->너비값,2,0x905020);}
    }
}
int 화면덮음(int sahib_obyekt,int x_koordinatı,int Y_koordinat){
    if(!화면보임(sahib_obyekt))return 0;
    for(int 순번=0;순번<32;순번++){
        vidget_vəziyyət *pəncərə=&요소들[sahib_obyekt][순번];
        if(pəncərə->sahə_VALUE==1&&pəncərə->보이는지&&x_koordinatı>=pəncərə->x_koordinatı&&Y_koordinat>=pəncərə->Y_koordinat&&
           x_koordinatı<pəncərə->x_koordinatı+pəncərə->너비값&&Y_koordinat<pəncərə->Y_koordinat+pəncərə->높이값)return 1;
    }return 0;
}
int 화면가리킴(int sahib_obyekt,unsigned 눌림,int x_koordinatı,int Y_koordinat){
    if(!화면보임(sahib_obyekt))return 0;
    if(눌림&1)for(int 순번=31;순번>=0;순번--){vidget_vəziyyət *너비값=&요소들[sahib_obyekt][순번];if(!너비값->sahə_VALUE||!표시됨(sahib_obyekt,너비값))continue;int pəncərə_X,pəncərə_Y;yerinə_qoymaq(sahib_obyekt,너비값,&pəncərə_X,&pəncərə_Y);
        if(x_koordinatı<pəncərə_X||Y_koordinat<pəncərə_Y||x_koordinatı>=pəncərə_X+너비값->너비값||Y_koordinat>=pəncərə_Y+너비값->높이값)continue;
        if(너비값->sahə_VALUE==1&&Y_koordinat<pəncərə_Y+30&&x_koordinatı>=pəncərə_X+너비값->너비값-28){if(너비값->Düzüm_siyasət!=0)너비값->보이는지=0;hadisə(sahib_obyekt,0x10000+순번+1);lövhə_Terminal(3);return 1;}
        if(너비값->sahə_VALUE==4){hadisə(sahib_obyekt,순번+1);return 1;}if(너비값->sahə_VALUE==5){Fokuslanmış[sahib_obyekt]=순번+1;lövhə_Terminal(3);return 1;}
        if(너비값->sahə_VALUE==1)return 1;
    }return 0;
}
void 화면누름(int sahib_obyekt,unsigned SECOND_VALUE){
    vidget_vəziyyət *너비값=element_VALUE(sahib_obyekt,Fokuslanmış[sahib_obyekt]);if(!너비값||너비값->sahə_VALUE!=5)return;
    if(SECOND_VALUE==13||SECOND_VALUE==10){hadisə(sahib_obyekt,Fokuslanmış[sahib_obyekt]);return;}
    if(SECOND_VALUE==8||SECOND_VALUE==127){if(너비값->uzunluq_VALUE)너비값->uzunluq_VALUE--;긴부호없는값[sahib_obyekt]=0;}
    else{
        unsigned simvol_kodlaşdırma=SECOND_VALUE;
        if(긴부호없는값[sahib_obyekt]){if((SECOND_VALUE&192)!=128){긴부호없는값[sahib_obyekt]=0;return;}부호없는결과[sahib_obyekt]=(부호없는결과[sahib_obyekt]<<6)|(SECOND_VALUE&63);if(--긴부호없는값[sahib_obyekt])return;simvol_kodlaşdırma=부호없는결과[sahib_obyekt];}
        else if(SECOND_VALUE>=0xc2&&SECOND_VALUE<=0xf4){긴부호없는값[sahib_obyekt]=SECOND_VALUE<0xe0?1:SECOND_VALUE<0xf0?2:3;부호없는결과[sahib_obyekt]=SECOND_VALUE&((1u<<(6-긴부호없는값[sahib_obyekt]))-1);return;}
        else if(SECOND_VALUE<32||SECOND_VALUE>=128)return;
        if(simvol_kodlaşdırma>0x10ffff||(simvol_kodlaşdırma>=0xd800&&simvol_kodlaşdırma<=0xdfff))return;if(너비값->uzunluq_VALUE<127)너비값->Mətn[너비값->uzunluq_VALUE++]=simvol_kodlaşdırma;
    }
    lövhə_Terminal(3);
}
int 화면호출(int sahib_obyekt,unsigned Gedişat,int identifikator_VALUE,int 첫째값,int SECOND_VALUE,int simvol_kodu,int təyinat_verilənlər){
    if(sahib_obyekt<0||sahib_obyekt>=4)return -22;vidget_vəziyyət *너비값=element_VALUE(sahib_obyekt,identifikator_VALUE);
    if(Gedişat==0){if(identifikator_VALUE<1||identifikator_VALUE>5)return -22;for(int 순번=0;순번<32;순번++)if(요소들[sahib_obyekt][순번].sahə_VALUE==0){너비값=&요소들[sahib_obyekt][순번];memset(너비값,0,sizeof(*너비값));너비값->sahə_VALUE=identifikator_VALUE;너비값->보이는지=identifikator_VALUE!=1;너비값->너비값=identifikator_VALUE==1?380:220;너비값->높이값=identifikator_VALUE==1?240:28;너비값->Düzüm_siyasət=1;너비값->x_koordinatı=identifikator_VALUE==1?130:16;너비값->Y_koordinat=identifikator_VALUE==1?110:16;return 순번+1;}return -28;}
    if(Gedişat==5){if(!daxiletmə_COUNT[sahib_obyekt])return 0;int 반환값=hadisə_Siyahı[sahib_obyekt][첫항목[sahib_obyekt]];첫항목[sahib_obyekt]=(첫항목[sahib_obyekt]+1)%16;daxiletmə_COUNT[sahib_obyekt]--;return 반환값;}
    if(Gedişat==6)return 화면보임(sahib_obyekt);
    if(!너비값)return -9;
    int 이전표시=표시됨(sahib_obyekt,너비값);
    if(Gedişat==1){int 바탕너비=보드화면너비(),바탕높이=보드화면높이();if(첫째값<0||SECOND_VALUE<0||simvol_kodu<1||təyinat_verilənlər<1||첫째값>바탕너비||SECOND_VALUE>바탕높이||simvol_kodu>바탕너비-첫째값||təyinat_verilənlər>바탕높이-SECOND_VALUE)return -22;너비값->x_koordinatı=첫째값;너비값->Y_koordinat=SECOND_VALUE;너비값->너비값=simvol_kodu;너비값->높이값=təyinat_verilənlər;너비값->əl_ilə_Düzüm=1;}
    else if(Gedişat==2){vidget_vəziyyət *törəmə_element=element_VALUE(sahib_obyekt,첫째값);if(!törəmə_element||törəmə_element==너비값||törəmə_element->sahə_VALUE==1)return -22;int verilənlər_yerinə_qoymaq=identifikator_VALUE;for(int 깊이=0;verilənlər_yerinə_qoymaq&&깊이<32;깊이++){if(verilənlər_yerinə_qoymaq==첫째값)return -22;vidget_vəziyyət *위쪽=element_VALUE(sahib_obyekt,verilənlər_yerinə_qoymaq);verilənlər_yerinə_qoymaq=위쪽?위쪽->부모항목:0;}törəmə_element->부모항목=identifikator_VALUE;if(!törəmə_element->əl_ilə_Düzüm){int 형제요소=0;for(int 순번=0;순번<32;순번++)if(&요소들[sahib_obyekt][순번]!=törəmə_element&&요소들[sahib_obyekt][순번].부모항목==identifikator_VALUE)형제요소++;törəmə_element->Y_koordinat=16+형제요소*36;}}
    else if(Gedişat==3)너비값->보이는지=첫째값!=0;
    else if(Gedişat==4)너비값->보이는지=0;
    else if(Gedişat==7)너비값->Düzüm_siyasət=첫째값;
    else if(Gedişat==8)return 너비값->uzunluq_VALUE;
    else if(Gedişat==9)return 첫째값>=0&&(unsigned)첫째값<너비값->uzunluq_VALUE?너비값->Mətn[첫째값]:-22;
    else return -22;
    if(이전표시||표시됨(sahib_obyekt,너비값))lövhə_Terminal(3);return 0;
}
int 화면글(int sahib_obyekt,int identifikator_VALUE,const uint32_t *verilənlər,unsigned element_COUNT){vidget_vəziyyət *너비값=element_VALUE(sahib_obyekt,identifikator_VALUE);if(!너비값)return -9;if(element_COUNT>127)return -22;for(unsigned 순번=0;순번<element_COUNT;순번++){unsigned simvol_kodlaşdırma=verilənlər[순번];if(simvol_kodlaşdırma>0x10ffff||(simvol_kodlaşdırma>=0xd800&&simvol_kodlaşdırma<=0xdfff))return -22;}for(unsigned 순번=0;순번<element_COUNT;순번++)너비값->Mətn[순번]=verilənlər[순번];너비값->uzunluq_VALUE=element_COUNT;if(표시됨(sahib_obyekt,너비값))lövhə_Terminal(3);return 0;}
