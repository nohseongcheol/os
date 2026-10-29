#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* Small native peer layer for the explicitly supported Swing subset. */
#include <stdint.h>
#include <stddef.h>
extern uintptr_t bretti_díll(uintptr_t,uintptr_t,uintptr_t),bretti_Endastöð(uintptr_t);
extern void Endastöð_stafbrigði(unsigned,unsigned,unsigned,unsigned,unsigned);
extern void *memset(void *,int,size_t);
typedef struct { int tegund_VALUE,yfireining,x_hnit,Y_hnit,너비값,높이값,보이는지,handvirkt_útlit,útlit_regla;unsigned Texti[128],lengd_VALUE; } græja_staða;
static græja_staða 요소들[4][32];
static int Forgangur[4],atvik_Listi[4][16];static unsigned 첫항목[4],færsla_COUNT[4],부호없는결과[4],긴부호없는값[4];
static void atvik(int eigandi_hlutur,int VALUE){if(færsla_COUNT[eigandi_hlutur]<16){atvik_Listi[eigandi_hlutur][(첫항목[eigandi_hlutur]+færsla_COUNT[eigandi_hlutur])%16]=VALUE;færsla_COUNT[eigandi_hlutur]++;}}
static græja_staða *eining_VALUE(int eigandi_hlutur,int auðkenni_VALUE){return eigandi_hlutur>=0&&eigandi_hlutur<4&&auðkenni_VALUE>0&&auðkenni_VALUE<=32&&요소들[eigandi_hlutur][auðkenni_VALUE-1].tegund_VALUE?&요소들[eigandi_hlutur][auðkenni_VALUE-1]:0;}
static void 사각영역(int x_hnit,int Y_hnit,int 너비값,int 높이값,unsigned 색상){보드사각그림(x_hnit,Y_hnit,너비값,높이값,색상);}
int 화면보임(int eigandi_hlutur){if(eigandi_hlutur<0||eigandi_hlutur>=4)return 0;for(int 순번=0;순번<32;순번++)if(요소들[eigandi_hlutur][순번].tegund_VALUE==1&&요소들[eigandi_hlutur][순번].보이는지)return 1;return 0;}
void 화면초기화(int eigandi_hlutur){memset(요소들[eigandi_hlutur],0,sizeof(요소들[eigandi_hlutur]));færsla_COUNT[eigandi_hlutur]=첫항목[eigandi_hlutur]=Forgangur[eigandi_hlutur]=긴부호없는값[eigandi_hlutur]=0;}
static void Staðsetning(int eigandi_hlutur,græja_staða *너비값,int *x_hnit,int *Y_hnit){*x_hnit=너비값->x_hnit;*Y_hnit=너비값->Y_hnit;int gögn_staða=너비값->yfireining;for(int vara_COUNT=0;gögn_staða&&vara_COUNT<32;vara_COUNT++){græja_staða *위쪽=eining_VALUE(eigandi_hlutur,gögn_staða);if(!위쪽)break;*x_hnit+=위쪽->x_hnit;*Y_hnit+=위쪽->Y_hnit+(위쪽->tegund_VALUE==1?30:0);gögn_staða=위쪽->yfireining;}}
static int 표시됨(int eigandi_hlutur,græja_staða *너비값){for(int vara_COUNT=0;vara_COUNT<32;vara_COUNT++){if(!너비값->보이는지)return 0;if(너비값->tegund_VALUE==1)return 1;너비값=eining_VALUE(eigandi_hlutur,너비값->yfireining);if(!너비값)return 0;}return 0;}
static void Texti(int x_hnit,int Y_hnit,græja_staða *너비값,int 최대값,unsigned 색상,unsigned 배경색){int 현재위치=0;for(unsigned 순번=0;순번<너비값->lengd_VALUE;순번++){unsigned stafur_kóðun=너비값->Texti[순번],너비=stafur_kóðun>=256?16:8;if(현재위치+(int)너비>최대값)break;Endastöð_stafbrigði(x_hnit+현재위치,Y_hnit,stafur_kóðun,색상,배경색);현재위치+=너비;}}
void 화면다시그림(int eigandi_hlutur){
    if(!화면보임(eigandi_hlutur))return;
    for(int 처리차례=1;처리차례<=5;처리차례++)for(int 순번=0;순번<32;순번++){
        græja_staða *너비값=&요소들[eigandi_hlutur][순번];if(너비값->tegund_VALUE!=처리차례||!표시됨(eigandi_hlutur,너비값))continue;int x_hnit,Y_hnit;Staðsetning(eigandi_hlutur,너비값,&x_hnit,&Y_hnit);
        if(처리차례==1){사각영역(x_hnit,Y_hnit,너비값->너비값,너비값->높이값,0xeee9e0);사각영역(x_hnit,Y_hnit,너비값->너비값,30,0x905020);Texti(x_hnit+10,Y_hnit+7,너비값,너비값->너비값-50,0xffffff,0x905020);사각영역(x_hnit+너비값->너비값-28,Y_hnit+4,24,22,0x5555b8);Endastöð_stafbrigði(x_hnit+너비값->너비값-20,Y_hnit+7,'X',0xffffff,0x5555b8);}
        if(처리차례==2)사각영역(x_hnit,Y_hnit,너비값->너비값,너비값->높이값,0xeee9e0);
        if(처리차례>=3){unsigned 배경색=처리차례==4?0xc0ab86:처리차례==5?0xffffff:0xeee9e0;if(처리차례!=3)사각영역(x_hnit,Y_hnit,너비값->너비값,너비값->높이값,배경색);Texti(x_hnit+4,Y_hnit+4,너비값,너비값->너비값-8,0x201a15,배경색);if(처리차례==5&&Forgangur[eigandi_hlutur]==순번+1)사각영역(x_hnit,Y_hnit+너비값->높이값-2,너비값->너비값,2,0x905020);}
    }
}
int 화면덮음(int eigandi_hlutur,int x_hnit,int Y_hnit){
    if(!화면보임(eigandi_hlutur))return 0;
    for(int 순번=0;순번<32;순번++){
        græja_staða *Gluggi=&요소들[eigandi_hlutur][순번];
        if(Gluggi->tegund_VALUE==1&&Gluggi->보이는지&&x_hnit>=Gluggi->x_hnit&&Y_hnit>=Gluggi->Y_hnit&&
           x_hnit<Gluggi->x_hnit+Gluggi->너비값&&Y_hnit<Gluggi->Y_hnit+Gluggi->높이값)return 1;
    }return 0;
}
int 화면가리킴(int eigandi_hlutur,unsigned 눌림,int x_hnit,int Y_hnit){
    if(!화면보임(eigandi_hlutur))return 0;
    if(눌림&1)for(int 순번=31;순번>=0;순번--){græja_staða *너비값=&요소들[eigandi_hlutur][순번];if(!너비값->tegund_VALUE||!표시됨(eigandi_hlutur,너비값))continue;int gluggi_X,gluggi_Y;Staðsetning(eigandi_hlutur,너비값,&gluggi_X,&gluggi_Y);
        if(x_hnit<gluggi_X||Y_hnit<gluggi_Y||x_hnit>=gluggi_X+너비값->너비값||Y_hnit>=gluggi_Y+너비값->높이값)continue;
        if(너비값->tegund_VALUE==1&&Y_hnit<gluggi_Y+30&&x_hnit>=gluggi_X+너비값->너비값-28){if(너비값->útlit_regla!=0)너비값->보이는지=0;atvik(eigandi_hlutur,0x10000+순번+1);bretti_Endastöð(3);return 1;}
        if(너비값->tegund_VALUE==4){atvik(eigandi_hlutur,순번+1);return 1;}if(너비값->tegund_VALUE==5){Forgangur[eigandi_hlutur]=순번+1;bretti_Endastöð(3);return 1;}
        if(너비값->tegund_VALUE==1)return 1;
    }return 0;
}
void 화면누름(int eigandi_hlutur,unsigned SECOND_VALUE){
    græja_staða *너비값=eining_VALUE(eigandi_hlutur,Forgangur[eigandi_hlutur]);if(!너비값||너비값->tegund_VALUE!=5)return;
    if(SECOND_VALUE==13||SECOND_VALUE==10){atvik(eigandi_hlutur,Forgangur[eigandi_hlutur]);return;}
    if(SECOND_VALUE==8||SECOND_VALUE==127){if(너비값->lengd_VALUE)너비값->lengd_VALUE--;긴부호없는값[eigandi_hlutur]=0;}
    else{
        unsigned stafur_kóðun=SECOND_VALUE;
        if(긴부호없는값[eigandi_hlutur]){if((SECOND_VALUE&192)!=128){긴부호없는값[eigandi_hlutur]=0;return;}부호없는결과[eigandi_hlutur]=(부호없는결과[eigandi_hlutur]<<6)|(SECOND_VALUE&63);if(--긴부호없는값[eigandi_hlutur])return;stafur_kóðun=부호없는결과[eigandi_hlutur];}
        else if(SECOND_VALUE>=0xc2&&SECOND_VALUE<=0xf4){긴부호없는값[eigandi_hlutur]=SECOND_VALUE<0xe0?1:SECOND_VALUE<0xf0?2:3;부호없는결과[eigandi_hlutur]=SECOND_VALUE&((1u<<(6-긴부호없는값[eigandi_hlutur]))-1);return;}
        else if(SECOND_VALUE<32||SECOND_VALUE>=128)return;
        if(stafur_kóðun>0x10ffff||(stafur_kóðun>=0xd800&&stafur_kóðun<=0xdfff))return;if(너비값->lengd_VALUE<127)너비값->Texti[너비값->lengd_VALUE++]=stafur_kóðun;
    }
    bretti_Endastöð(3);
}
int 화면호출(int eigandi_hlutur,unsigned Aðgerð,int auðkenni_VALUE,int 첫째값,int SECOND_VALUE,int stafkóði,int endastaður_gögn){
    if(eigandi_hlutur<0||eigandi_hlutur>=4)return -22;græja_staða *너비값=eining_VALUE(eigandi_hlutur,auðkenni_VALUE);
    if(Aðgerð==0){if(auðkenni_VALUE<1||auðkenni_VALUE>5)return -22;for(int 순번=0;순번<32;순번++)if(요소들[eigandi_hlutur][순번].tegund_VALUE==0){너비값=&요소들[eigandi_hlutur][순번];memset(너비값,0,sizeof(*너비값));너비값->tegund_VALUE=auðkenni_VALUE;너비값->보이는지=auðkenni_VALUE!=1;너비값->너비값=auðkenni_VALUE==1?380:220;너비값->높이값=auðkenni_VALUE==1?240:28;너비값->útlit_regla=1;너비값->x_hnit=auðkenni_VALUE==1?130:16;너비값->Y_hnit=auðkenni_VALUE==1?110:16;return 순번+1;}return -28;}
    if(Aðgerð==5){if(!færsla_COUNT[eigandi_hlutur])return 0;int 반환값=atvik_Listi[eigandi_hlutur][첫항목[eigandi_hlutur]];첫항목[eigandi_hlutur]=(첫항목[eigandi_hlutur]+1)%16;færsla_COUNT[eigandi_hlutur]--;return 반환값;}
    if(Aðgerð==6)return 화면보임(eigandi_hlutur);
    if(!너비값)return -9;
    int 이전표시=표시됨(eigandi_hlutur,너비값);
    if(Aðgerð==1){int 바탕너비=보드화면너비(),바탕높이=보드화면높이();if(첫째값<0||SECOND_VALUE<0||stafkóði<1||endastaður_gögn<1||첫째값>바탕너비||SECOND_VALUE>바탕높이||stafkóði>바탕너비-첫째값||endastaður_gögn>바탕높이-SECOND_VALUE)return -22;너비값->x_hnit=첫째값;너비값->Y_hnit=SECOND_VALUE;너비값->너비값=stafkóði;너비값->높이값=endastaður_gögn;너비값->handvirkt_útlit=1;}
    else if(Aðgerð==2){græja_staða *undireining=eining_VALUE(eigandi_hlutur,첫째값);if(!undireining||undireining==너비값||undireining->tegund_VALUE==1)return -22;int gögn_staða=auðkenni_VALUE;for(int 깊이=0;gögn_staða&&깊이<32;깊이++){if(gögn_staða==첫째값)return -22;græja_staða *위쪽=eining_VALUE(eigandi_hlutur,gögn_staða);gögn_staða=위쪽?위쪽->yfireining:0;}undireining->yfireining=auðkenni_VALUE;if(!undireining->handvirkt_útlit){int 형제요소=0;for(int 순번=0;순번<32;순번++)if(&요소들[eigandi_hlutur][순번]!=undireining&&요소들[eigandi_hlutur][순번].yfireining==auðkenni_VALUE)형제요소++;undireining->Y_hnit=16+형제요소*36;}}
    else if(Aðgerð==3)너비값->보이는지=첫째값!=0;
    else if(Aðgerð==4)너비값->보이는지=0;
    else if(Aðgerð==7)너비값->útlit_regla=첫째값;
    else if(Aðgerð==8)return 너비값->lengd_VALUE;
    else if(Aðgerð==9)return 첫째값>=0&&(unsigned)첫째값<너비값->lengd_VALUE?너비값->Texti[첫째값]:-22;
    else return -22;
    if(이전표시||표시됨(eigandi_hlutur,너비값))bretti_Endastöð(3);return 0;
}
int 화면글(int eigandi_hlutur,int auðkenni_VALUE,const uint32_t *gögn,unsigned vara_COUNT){græja_staða *너비값=eining_VALUE(eigandi_hlutur,auðkenni_VALUE);if(!너비값)return -9;if(vara_COUNT>127)return -22;for(unsigned 순번=0;순번<vara_COUNT;순번++){unsigned stafur_kóðun=gögn[순번];if(stafur_kóðun>0x10ffff||(stafur_kóðun>=0xd800&&stafur_kóðun<=0xdfff))return -22;}for(unsigned 순번=0;순번<vara_COUNT;순번++)너비값->Texti[순번]=gögn[순번];너비값->lengd_VALUE=vara_COUNT;if(표시됨(eigandi_hlutur,너비값))bretti_Endastöð(3);return 0;}
