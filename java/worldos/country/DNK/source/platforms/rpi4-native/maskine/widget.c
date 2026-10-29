#include "../명명/기계연결이름.h"
#include "skærmbillede_info.h"
/* Small native peer layer for the explicitly supported Swing subset. */
#include <stdint.h>
#include <stddef.h>
extern uintptr_t Tavle_pixel(uintptr_t,uintptr_t,uintptr_t),Tavle_Terminal(uintptr_t);
extern void Terminal_specialtegn(unsigned,unsigned,unsigned,unsigned,unsigned);
extern void *memset(void *,int,size_t);
typedef struct { int område_VÆRDI,overordnet,X_koordinat,Y_koordinat,너비값,높이값,보이는지,manuel_Layout,Layout_Policy;unsigned Tekst[128],varighed_VÆRDI; } widget_status;
static widget_status 요소들[4][32];
static int Fokuseret[4],hændelse_Liste[4][16];static unsigned 첫항목[4],post_TÆL_8f7753a1[4],부호없는결과[4],긴부호없는값[4];
static void hændelse(int ejer_objekt,int VÆRDI){if(post_TÆL_8f7753a1[ejer_objekt]<16){hændelse_Liste[ejer_objekt][(첫항목[ejer_objekt]+post_TÆL_8f7753a1[ejer_objekt])%16]=VÆRDI;post_TÆL_8f7753a1[ejer_objekt]++;}}
static widget_status *element_VÆRDI(int ejer_objekt,int identifikator_VÆRDI){return ejer_objekt>=0&&ejer_objekt<4&&identifikator_VÆRDI>0&&identifikator_VÆRDI<=32&&요소들[ejer_objekt][identifikator_VÆRDI-1].område_VÆRDI?&요소들[ejer_objekt][identifikator_VÆRDI-1]:0;}
static void 사각영역(int X_koordinat,int Y_koordinat,int 너비값,int 높이값,unsigned 색상){Tavle_rektangel_udfyld(X_koordinat,Y_koordinat,너비값,높이값,색상);}
int 화면보임(int ejer_objekt){if(ejer_objekt<0||ejer_objekt>=4)return 0;for(int 순번=0;순번<32;순번++)if(요소들[ejer_objekt][순번].område_VÆRDI==1&&요소들[ejer_objekt][순번].보이는지)return 1;return 0;}
void starte_skærmbillede(int ejer_objekt){memset(요소들[ejer_objekt],0,sizeof(요소들[ejer_objekt]));post_TÆL_8f7753a1[ejer_objekt]=첫항목[ejer_objekt]=Fokuseret[ejer_objekt]=긴부호없는값[ejer_objekt]=0;}
static void Placering(int ejer_objekt,widget_status *너비값,int *X_koordinat,int *Y_koordinat){*X_koordinat=너비값->X_koordinat;*Y_koordinat=너비값->Y_koordinat;int data_placere=너비값->overordnet;for(int vare_TÆL=0;data_placere&&vare_TÆL<32;vare_TÆL++){widget_status *위쪽=element_VÆRDI(ejer_objekt,data_placere);if(!위쪽)break;*X_koordinat+=위쪽->X_koordinat;*Y_koordinat+=위쪽->Y_koordinat+(위쪽->område_VÆRDI==1?30:0);data_placere=위쪽->overordnet;}}
static int 표시됨(int ejer_objekt,widget_status *너비값){for(int vare_TÆL=0;vare_TÆL<32;vare_TÆL++){if(!너비값->보이는지)return 0;if(너비값->område_VÆRDI==1)return 1;너비값=element_VÆRDI(ejer_objekt,너비값->overordnet);if(!너비값)return 0;}return 0;}
static void Tekst(int X_koordinat,int Y_koordinat,widget_status *너비값,int 최대값,unsigned 색상,unsigned 배경색){int aktuel_placere=0;for(unsigned 순번=0;순번<너비값->varighed_VÆRDI;순번++){unsigned tegnkodning=너비값->Tekst[순번],너비=tegnkodning>=256?16:8;if(aktuel_placere+(int)너비>최대값)break;Terminal_specialtegn(X_koordinat+aktuel_placere,Y_koordinat,tegnkodning,색상,배경색);aktuel_placere+=너비;}}
void 화면다시그림(int ejer_objekt){
    if(!화면보임(ejer_objekt))return;
    for(int behandling_ordre=1;behandling_ordre<=5;behandling_ordre++)for(int 순번=0;순번<32;순번++){
        widget_status *너비값=&요소들[ejer_objekt][순번];if(너비값->område_VÆRDI!=behandling_ordre||!표시됨(ejer_objekt,너비값))continue;int X_koordinat,Y_koordinat;Placering(ejer_objekt,너비값,&X_koordinat,&Y_koordinat);
        if(behandling_ordre==1){사각영역(X_koordinat,Y_koordinat,너비값->너비값,너비값->높이값,0xeee9e0);사각영역(X_koordinat,Y_koordinat,너비값->너비값,30,0x905020);Tekst(X_koordinat+10,Y_koordinat+7,너비값,너비값->너비값-50,0xffffff,0x905020);사각영역(X_koordinat+너비값->너비값-28,Y_koordinat+4,24,22,0x5555b8);Terminal_specialtegn(X_koordinat+너비값->너비값-20,Y_koordinat+7,'X',0xffffff,0x5555b8);}
        if(behandling_ordre==2)사각영역(X_koordinat,Y_koordinat,너비값->너비값,너비값->높이값,0xeee9e0);
        if(behandling_ordre>=3){unsigned 배경색=behandling_ordre==4?0xc0ab86:behandling_ordre==5?0xffffff:0xeee9e0;if(behandling_ordre!=3)사각영역(X_koordinat,Y_koordinat,너비값->너비값,너비값->높이값,배경색);Tekst(X_koordinat+4,Y_koordinat+4,너비값,너비값->너비값-8,0x201a15,배경색);if(behandling_ordre==5&&Fokuseret[ejer_objekt]==순번+1)사각영역(X_koordinat,Y_koordinat+너비값->높이값-2,너비값->너비값,2,0x905020);}
    }
}
int skærmbillede_overlejring(int ejer_objekt,int X_koordinat,int Y_koordinat){
    if(!화면보임(ejer_objekt))return 0;
    for(int 순번=0;순번<32;순번++){
        widget_status *Vindue=&요소들[ejer_objekt][순번];
        if(Vindue->område_VÆRDI==1&&Vindue->보이는지&&X_koordinat>=Vindue->X_koordinat&&Y_koordinat>=Vindue->Y_koordinat&&
           X_koordinat<Vindue->X_koordinat+Vindue->너비값&&Y_koordinat<Vindue->Y_koordinat+Vindue->높이값)return 1;
    }return 0;
}
int skærmbillede_markør(int ejer_objekt,unsigned 눌림,int X_koordinat,int Y_koordinat){
    if(!화면보임(ejer_objekt))return 0;
    if(눌림&1)for(int 순번=31;순번>=0;순번--){widget_status *너비값=&요소들[ejer_objekt][순번];if(!너비값->område_VÆRDI||!표시됨(ejer_objekt,너비값))continue;int vindue_X,vindue_Y;Placering(ejer_objekt,너비값,&vindue_X,&vindue_Y);
        if(X_koordinat<vindue_X||Y_koordinat<vindue_Y||X_koordinat>=vindue_X+너비값->너비값||Y_koordinat>=vindue_Y+너비값->높이값)continue;
        if(너비값->område_VÆRDI==1&&Y_koordinat<vindue_Y+30&&X_koordinat>=vindue_X+너비값->너비값-28){if(너비값->Layout_Policy!=0)너비값->보이는지=0;hændelse(ejer_objekt,0x10000+순번+1);Tavle_Terminal(3);return 1;}
        if(너비값->område_VÆRDI==4){hændelse(ejer_objekt,순번+1);return 1;}if(너비값->område_VÆRDI==5){Fokuseret[ejer_objekt]=순번+1;Tavle_Terminal(3);return 1;}
        if(너비값->område_VÆRDI==1)return 1;
    }return 0;
}
void 화면누름(int ejer_objekt,unsigned SEKUND_VÆRDI){
    widget_status *너비값=element_VÆRDI(ejer_objekt,Fokuseret[ejer_objekt]);if(!너비값||너비값->område_VÆRDI!=5)return;
    if(SEKUND_VÆRDI==13||SEKUND_VÆRDI==10){hændelse(ejer_objekt,Fokuseret[ejer_objekt]);return;}
    if(SEKUND_VÆRDI==8||SEKUND_VÆRDI==127){if(너비값->varighed_VÆRDI)너비값->varighed_VÆRDI--;긴부호없는값[ejer_objekt]=0;}
    else{
        unsigned tegnkodning=SEKUND_VÆRDI;
        if(긴부호없는값[ejer_objekt]){if((SEKUND_VÆRDI&192)!=128){긴부호없는값[ejer_objekt]=0;return;}부호없는결과[ejer_objekt]=(부호없는결과[ejer_objekt]<<6)|(SEKUND_VÆRDI&63);if(--긴부호없는값[ejer_objekt])return;tegnkodning=부호없는결과[ejer_objekt];}
        else if(SEKUND_VÆRDI>=0xc2&&SEKUND_VÆRDI<=0xf4){긴부호없는값[ejer_objekt]=SEKUND_VÆRDI<0xe0?1:SEKUND_VÆRDI<0xf0?2:3;부호없는결과[ejer_objekt]=SEKUND_VÆRDI&((1u<<(6-긴부호없는값[ejer_objekt]))-1);return;}
        else if(SEKUND_VÆRDI<32||SEKUND_VÆRDI>=128)return;
        if(tegnkodning>0x10ffff||(tegnkodning>=0xd800&&tegnkodning<=0xdfff))return;if(너비값->varighed_VÆRDI<127)너비값->Tekst[너비값->varighed_VÆRDI++]=tegnkodning;
    }
    Tavle_Terminal(3);
}
int 화면호출(int ejer_objekt,unsigned Handling,int identifikator_VÆRDI,int 첫째값,int SEKUND_VÆRDI,int tegnkode,int destination_data){
    if(ejer_objekt<0||ejer_objekt>=4)return -22;widget_status *너비값=element_VÆRDI(ejer_objekt,identifikator_VÆRDI);
    if(Handling==0){if(identifikator_VÆRDI<1||identifikator_VÆRDI>5)return -22;for(int 순번=0;순번<32;순번++)if(요소들[ejer_objekt][순번].område_VÆRDI==0){너비값=&요소들[ejer_objekt][순번];memset(너비값,0,sizeof(*너비값));너비값->område_VÆRDI=identifikator_VÆRDI;너비값->보이는지=identifikator_VÆRDI!=1;너비값->너비값=identifikator_VÆRDI==1?380:220;너비값->높이값=identifikator_VÆRDI==1?240:28;너비값->Layout_Policy=1;너비값->X_koordinat=identifikator_VÆRDI==1?130:16;너비값->Y_koordinat=identifikator_VÆRDI==1?110:16;return 순번+1;}return -28;}
    if(Handling==5){if(!post_TÆL_8f7753a1[ejer_objekt])return 0;int 반환값=hændelse_Liste[ejer_objekt][첫항목[ejer_objekt]];첫항목[ejer_objekt]=(첫항목[ejer_objekt]+1)%16;post_TÆL_8f7753a1[ejer_objekt]--;return 반환값;}
    if(Handling==6)return 화면보임(ejer_objekt);
    if(!너비값)return -9;
    int 이전표시=표시됨(ejer_objekt,너비값);
    if(Handling==1){int 바탕너비=보드화면너비(),바탕높이=보드화면높이();if(첫째값<0||SEKUND_VÆRDI<0||tegnkode<1||destination_data<1||첫째값>바탕너비||SEKUND_VÆRDI>바탕높이||tegnkode>바탕너비-첫째값||destination_data>바탕높이-SEKUND_VÆRDI)return -22;너비값->X_koordinat=첫째값;너비값->Y_koordinat=SEKUND_VÆRDI;너비값->너비값=tegnkode;너비값->높이값=destination_data;너비값->manuel_Layout=1;}
    else if(Handling==2){widget_status *underordnet=element_VÆRDI(ejer_objekt,첫째값);if(!underordnet||underordnet==너비값||underordnet->område_VÆRDI==1)return -22;int data_placere=identifikator_VÆRDI;for(int 깊이=0;data_placere&&깊이<32;깊이++){if(data_placere==첫째값)return -22;widget_status *위쪽=element_VÆRDI(ejer_objekt,data_placere);data_placere=위쪽?위쪽->overordnet:0;}underordnet->overordnet=identifikator_VÆRDI;if(!underordnet->manuel_Layout){int 형제요소=0;for(int 순번=0;순번<32;순번++)if(&요소들[ejer_objekt][순번]!=underordnet&&요소들[ejer_objekt][순번].overordnet==identifikator_VÆRDI)형제요소++;underordnet->Y_koordinat=16+형제요소*36;}}
    else if(Handling==3)너비값->보이는지=첫째값!=0;
    else if(Handling==4)너비값->보이는지=0;
    else if(Handling==7)너비값->Layout_Policy=첫째값;
    else if(Handling==8)return 너비값->varighed_VÆRDI;
    else if(Handling==9)return 첫째값>=0&&(unsigned)첫째값<너비값->varighed_VÆRDI?너비값->Tekst[첫째값]:-22;
    else return -22;
    if(이전표시||표시됨(ejer_objekt,너비값))Tavle_Terminal(3);return 0;
}
int skærmbillede_sms(int ejer_objekt,int identifikator_VÆRDI,const uint32_t *data,unsigned vare_TÆL){widget_status *너비값=element_VÆRDI(ejer_objekt,identifikator_VÆRDI);if(!너비값)return -9;if(vare_TÆL>127)return -22;for(unsigned 순번=0;순번<vare_TÆL;순번++){unsigned tegnkodning=data[순번];if(tegnkodning>0x10ffff||(tegnkodning>=0xd800&&tegnkodning<=0xdfff))return -22;}for(unsigned 순번=0;순번<vare_TÆL;순번++)너비값->Tekst[순번]=data[순번];너비값->varighed_VÆRDI=vare_TÆL;if(표시됨(ejer_objekt,너비값))Tavle_Terminal(3);return 0;}
