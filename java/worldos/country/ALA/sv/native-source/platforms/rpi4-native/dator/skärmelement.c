#include "../명명/기계연결이름.h"
#include "skärmbild_info.h"
/* Small native peer layer for the explicitly supported Swing subset. */
#include <stdint.h>
#include <stddef.h>
extern uintptr_t Tavla_bildpunkt(uintptr_t,uintptr_t,uintptr_t),Tavla_Terminal(uintptr_t);
extern void Terminal_glyf(unsigned,unsigned,unsigned,unsigned,unsigned);
extern void *memset(void *,int,size_t);
typedef struct { int område_värde,överordnad,x_koordinat,Y_koordinat,너비값,높이값,보이는지,manuell_Layout,Layout_Policy;unsigned text[128],längd_värde; } widget_status;
static widget_status 요소들[4][32];
static int Prioriterad[4],händelse_ange[4][16];static unsigned 첫항목[4],post_ANTAL[4],부호없는결과[4],긴부호없는값[4];
static void Händelse(int ägare_objekt,int värde){if(post_ANTAL[ägare_objekt]<16){händelse_ange[ägare_objekt][(첫항목[ägare_objekt]+post_ANTAL[ägare_objekt])%16]=värde;post_ANTAL[ägare_objekt]++;}}
static widget_status *element_värde(int ägare_objekt,int identifierare_värde){return ägare_objekt>=0&&ägare_objekt<4&&identifierare_värde>0&&identifierare_värde<=32&&요소들[ägare_objekt][identifierare_värde-1].område_värde?&요소들[ägare_objekt][identifierare_värde-1]:0;}
static void 사각영역(int x_koordinat,int Y_koordinat,int 너비값,int 높이값,unsigned 색상){Tavla_rektangel_Fyll(x_koordinat,Y_koordinat,너비값,높이값,색상);}
int 화면보임(int ägare_objekt){if(ägare_objekt<0||ägare_objekt>=4)return 0;for(int 순번=0;순번<32;순번++)if(요소들[ägare_objekt][순번].område_värde==1&&요소들[ägare_objekt][순번].보이는지)return 1;return 0;}
void starta_skärmbild(int ägare_objekt){memset(요소들[ägare_objekt],0,sizeof(요소들[ägare_objekt]));post_ANTAL[ägare_objekt]=첫항목[ägare_objekt]=Prioriterad[ägare_objekt]=긴부호없는값[ägare_objekt]=0;}
static void position(int ägare_objekt,widget_status *너비값,int *x_koordinat,int *Y_koordinat){*x_koordinat=너비값->x_koordinat;*Y_koordinat=너비값->Y_koordinat;int data_placera=너비값->överordnad;for(int objekt_ANTAL=0;data_placera&&objekt_ANTAL<32;objekt_ANTAL++){widget_status *위쪽=element_värde(ägare_objekt,data_placera);if(!위쪽)break;*x_koordinat+=위쪽->x_koordinat;*Y_koordinat+=위쪽->Y_koordinat+(위쪽->område_värde==1?30:0);data_placera=위쪽->överordnad;}}
static int 표시됨(int ägare_objekt,widget_status *너비값){for(int objekt_ANTAL=0;objekt_ANTAL<32;objekt_ANTAL++){if(!너비값->보이는지)return 0;if(너비값->område_värde==1)return 1;너비값=element_värde(ägare_objekt,너비값->överordnad);if(!너비값)return 0;}return 0;}
static void text(int x_koordinat,int Y_koordinat,widget_status *너비값,int 최대값,unsigned 색상,unsigned 배경색){int aktuellt_placera=0;for(unsigned 순번=0;순번<너비값->längd_värde;순번++){unsigned teckenkodning=너비값->text[순번],너비=teckenkodning>=256?16:8;if(aktuellt_placera+(int)너비>최대값)break;Terminal_glyf(x_koordinat+aktuellt_placera,Y_koordinat,teckenkodning,색상,배경색);aktuellt_placera+=너비;}}
void 화면다시그림(int ägare_objekt){
    if(!화면보임(ägare_objekt))return;
    for(int bearbetning_order=1;bearbetning_order<=5;bearbetning_order++)for(int 순번=0;순번<32;순번++){
        widget_status *너비값=&요소들[ägare_objekt][순번];if(너비값->område_värde!=bearbetning_order||!표시됨(ägare_objekt,너비값))continue;int x_koordinat,Y_koordinat;position(ägare_objekt,너비값,&x_koordinat,&Y_koordinat);
        if(bearbetning_order==1){사각영역(x_koordinat,Y_koordinat,너비값->너비값,너비값->높이값,0xeee9e0);사각영역(x_koordinat,Y_koordinat,너비값->너비값,30,0x905020);text(x_koordinat+10,Y_koordinat+7,너비값,너비값->너비값-50,0xffffff,0x905020);사각영역(x_koordinat+너비값->너비값-28,Y_koordinat+4,24,22,0x5555b8);Terminal_glyf(x_koordinat+너비값->너비값-20,Y_koordinat+7,'X',0xffffff,0x5555b8);}
        if(bearbetning_order==2)사각영역(x_koordinat,Y_koordinat,너비값->너비값,너비값->높이값,0xeee9e0);
        if(bearbetning_order>=3){unsigned 배경색=bearbetning_order==4?0xc0ab86:bearbetning_order==5?0xffffff:0xeee9e0;if(bearbetning_order!=3)사각영역(x_koordinat,Y_koordinat,너비값->너비값,너비값->높이값,배경색);text(x_koordinat+4,Y_koordinat+4,너비값,너비값->너비값-8,0x201a15,배경색);if(bearbetning_order==5&&Prioriterad[ägare_objekt]==순번+1)사각영역(x_koordinat,Y_koordinat+너비값->높이값-2,너비값->너비값,2,0x905020);}
    }
}
int skärmbild_överlägg(int ägare_objekt,int x_koordinat,int Y_koordinat){
    if(!화면보임(ägare_objekt))return 0;
    for(int 순번=0;순번<32;순번++){
        widget_status *Fönster=&요소들[ägare_objekt][순번];
        if(Fönster->område_värde==1&&Fönster->보이는지&&x_koordinat>=Fönster->x_koordinat&&Y_koordinat>=Fönster->Y_koordinat&&
           x_koordinat<Fönster->x_koordinat+Fönster->너비값&&Y_koordinat<Fönster->Y_koordinat+Fönster->높이값)return 1;
    }return 0;
}
int skärmbild_markör(int ägare_objekt,unsigned 눌림,int x_koordinat,int Y_koordinat){
    if(!화면보임(ägare_objekt))return 0;
    if(눌림&1)for(int 순번=31;순번>=0;순번--){widget_status *너비값=&요소들[ägare_objekt][순번];if(!너비값->område_värde||!표시됨(ägare_objekt,너비값))continue;int fönster_X,fönster_Y;position(ägare_objekt,너비값,&fönster_X,&fönster_Y);
        if(x_koordinat<fönster_X||Y_koordinat<fönster_Y||x_koordinat>=fönster_X+너비값->너비값||Y_koordinat>=fönster_Y+너비값->높이값)continue;
        if(너비값->område_värde==1&&Y_koordinat<fönster_Y+30&&x_koordinat>=fönster_X+너비값->너비값-28){if(너비값->Layout_Policy!=0)너비값->보이는지=0;Händelse(ägare_objekt,0x10000+순번+1);Tavla_Terminal(3);return 1;}
        if(너비값->område_värde==4){Händelse(ägare_objekt,순번+1);return 1;}if(너비값->område_värde==5){Prioriterad[ägare_objekt]=순번+1;Tavla_Terminal(3);return 1;}
        if(너비값->område_värde==1)return 1;
    }return 0;
}
void skärmbild_tryck(int ägare_objekt,unsigned SEKUND_värde){
    widget_status *너비값=element_värde(ägare_objekt,Prioriterad[ägare_objekt]);if(!너비값||너비값->område_värde!=5)return;
    if(SEKUND_värde==13||SEKUND_värde==10){Händelse(ägare_objekt,Prioriterad[ägare_objekt]);return;}
    if(SEKUND_värde==8||SEKUND_värde==127){if(너비값->längd_värde)너비값->längd_värde--;긴부호없는값[ägare_objekt]=0;}
    else{
        unsigned teckenkodning=SEKUND_värde;
        if(긴부호없는값[ägare_objekt]){if((SEKUND_värde&192)!=128){긴부호없는값[ägare_objekt]=0;return;}부호없는결과[ägare_objekt]=(부호없는결과[ägare_objekt]<<6)|(SEKUND_värde&63);if(--긴부호없는값[ägare_objekt])return;teckenkodning=부호없는결과[ägare_objekt];}
        else if(SEKUND_värde>=0xc2&&SEKUND_värde<=0xf4){긴부호없는값[ägare_objekt]=SEKUND_värde<0xe0?1:SEKUND_värde<0xf0?2:3;부호없는결과[ägare_objekt]=SEKUND_värde&((1u<<(6-긴부호없는값[ägare_objekt]))-1);return;}
        else if(SEKUND_värde<32||SEKUND_värde>=128)return;
        if(teckenkodning>0x10ffff||(teckenkodning>=0xd800&&teckenkodning<=0xdfff))return;if(너비값->längd_värde<127)너비값->text[너비값->längd_värde++]=teckenkodning;
    }
    Tavla_Terminal(3);
}
int 화면호출(int ägare_objekt,unsigned Åtgärd,int identifierare_värde,int 첫째값,int SEKUND_värde,int kodpunkt,int mål_data){
    if(ägare_objekt<0||ägare_objekt>=4)return -22;widget_status *너비값=element_värde(ägare_objekt,identifierare_värde);
    if(Åtgärd==0){if(identifierare_värde<1||identifierare_värde>5)return -22;for(int 순번=0;순번<32;순번++)if(요소들[ägare_objekt][순번].område_värde==0){너비값=&요소들[ägare_objekt][순번];memset(너비값,0,sizeof(*너비값));너비값->område_värde=identifierare_värde;너비값->보이는지=identifierare_värde!=1;너비값->너비값=identifierare_värde==1?380:220;너비값->높이값=identifierare_värde==1?240:28;너비값->Layout_Policy=1;너비값->x_koordinat=identifierare_värde==1?130:16;너비값->Y_koordinat=identifierare_värde==1?110:16;return 순번+1;}return -28;}
    if(Åtgärd==5){if(!post_ANTAL[ägare_objekt])return 0;int 반환값=händelse_ange[ägare_objekt][첫항목[ägare_objekt]];첫항목[ägare_objekt]=(첫항목[ägare_objekt]+1)%16;post_ANTAL[ägare_objekt]--;return 반환값;}
    if(Åtgärd==6)return 화면보임(ägare_objekt);
    if(!너비값)return -9;
    int 이전표시=표시됨(ägare_objekt,너비값);
    if(Åtgärd==1){int 바탕너비=보드화면너비(),바탕높이=보드화면높이();if(첫째값<0||SEKUND_värde<0||kodpunkt<1||mål_data<1||첫째값>바탕너비||SEKUND_värde>바탕높이||kodpunkt>바탕너비-첫째값||mål_data>바탕높이-SEKUND_värde)return -22;너비값->x_koordinat=첫째값;너비값->Y_koordinat=SEKUND_värde;너비값->너비값=kodpunkt;너비값->높이값=mål_data;너비값->manuell_Layout=1;}
    else if(Åtgärd==2){widget_status *underordnat_objekt=element_värde(ägare_objekt,첫째값);if(!underordnat_objekt||underordnat_objekt==너비값||underordnat_objekt->område_värde==1)return -22;int data_placera=identifierare_värde;for(int 깊이=0;data_placera&&깊이<32;깊이++){if(data_placera==첫째값)return -22;widget_status *위쪽=element_värde(ägare_objekt,data_placera);data_placera=위쪽?위쪽->överordnad:0;}underordnat_objekt->överordnad=identifierare_värde;if(!underordnat_objekt->manuell_Layout){int 형제요소=0;for(int 순번=0;순번<32;순번++)if(&요소들[ägare_objekt][순번]!=underordnat_objekt&&요소들[ägare_objekt][순번].överordnad==identifierare_värde)형제요소++;underordnat_objekt->Y_koordinat=16+형제요소*36;}}
    else if(Åtgärd==3)너비값->보이는지=첫째값!=0;
    else if(Åtgärd==4)너비값->보이는지=0;
    else if(Åtgärd==7)너비값->Layout_Policy=첫째값;
    else if(Åtgärd==8)return 너비값->längd_värde;
    else if(Åtgärd==9)return 첫째값>=0&&(unsigned)첫째값<너비값->längd_värde?너비값->text[첫째값]:-22;
    else return -22;
    if(이전표시||표시됨(ägare_objekt,너비값))Tavla_Terminal(3);return 0;
}
int skärmbild_SMS(int ägare_objekt,int identifierare_värde,const uint32_t *data,unsigned objekt_ANTAL){widget_status *너비값=element_värde(ägare_objekt,identifierare_värde);if(!너비값)return -9;if(objekt_ANTAL>127)return -22;for(unsigned 순번=0;순번<objekt_ANTAL;순번++){unsigned teckenkodning=data[순번];if(teckenkodning>0x10ffff||(teckenkodning>=0xd800&&teckenkodning<=0xdfff))return -22;}for(unsigned 순번=0;순번<objekt_ANTAL;순번++)너비값->text[순번]=data[순번];너비값->längd_värde=objekt_ANTAL;if(표시됨(ägare_objekt,너비값))Tavla_Terminal(3);return 0;}
