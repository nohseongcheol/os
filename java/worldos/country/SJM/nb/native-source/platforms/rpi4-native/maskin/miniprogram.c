#include "../명명/기계연결이름.h"
#include "skjermbilde_info.h"
/* Small native peer layer for the explicitly supported Swing subset. */
#include <stdint.h>
#include <stddef.h>
extern uintptr_t Tavle_piksel(uintptr_t,uintptr_t,uintptr_t),Tavle_Terminal(uintptr_t);
extern void Terminal_figur(unsigned,unsigned,unsigned,unsigned,unsigned);
extern void *memset(void *,int,size_t);
typedef struct { int område_VERDI,overordnet,x_koordinat,Y_koordinat,너비값,높이값,보이는지,manuell_Oppsett,Oppsett_Policy;unsigned Tekst[128],lengde_VERDI; } miniprogram_status;
static miniprogram_status 요소들[4][32];
static int Fokus_f7e69dab[4],hendelse_Liste[4][16];static unsigned 첫항목[4],oppføring_ANTALL[4],부호없는결과[4],긴부호없는값[4];
static void Hendelse(int eier_objekt,int VERDI){if(oppføring_ANTALL[eier_objekt]<16){hendelse_Liste[eier_objekt][(첫항목[eier_objekt]+oppføring_ANTALL[eier_objekt])%16]=VERDI;oppføring_ANTALL[eier_objekt]++;}}
static miniprogram_status *element_VERDI(int eier_objekt,int identifikator_VERDI){return eier_objekt>=0&&eier_objekt<4&&identifikator_VERDI>0&&identifikator_VERDI<=32&&요소들[eier_objekt][identifikator_VERDI-1].område_VERDI?&요소들[eier_objekt][identifikator_VERDI-1]:0;}
static void 사각영역(int x_koordinat,int Y_koordinat,int 너비값,int 높이값,unsigned 색상){Tavle_rektangel_fyll(x_koordinat,Y_koordinat,너비값,높이값,색상);}
int 화면보임(int eier_objekt){if(eier_objekt<0||eier_objekt>=4)return 0;for(int 순번=0;순번<32;순번++)if(요소들[eier_objekt][순번].område_VERDI==1&&요소들[eier_objekt][순번].보이는지)return 1;return 0;}
void starte_skjermbilde(int eier_objekt){memset(요소들[eier_objekt],0,sizeof(요소들[eier_objekt]));oppføring_ANTALL[eier_objekt]=첫항목[eier_objekt]=Fokus_f7e69dab[eier_objekt]=긴부호없는값[eier_objekt]=0;}
static void Posisjon(int eier_objekt,miniprogram_status *너비값,int *x_koordinat,int *Y_koordinat){*x_koordinat=너비값->x_koordinat;*Y_koordinat=너비값->Y_koordinat;int data_plassere=너비값->overordnet;for(int vare_ANTALL=0;data_plassere&&vare_ANTALL<32;vare_ANTALL++){miniprogram_status *위쪽=element_VERDI(eier_objekt,data_plassere);if(!위쪽)break;*x_koordinat+=위쪽->x_koordinat;*Y_koordinat+=위쪽->Y_koordinat+(위쪽->område_VERDI==1?30:0);data_plassere=위쪽->overordnet;}}
static int 표시됨(int eier_objekt,miniprogram_status *너비값){for(int vare_ANTALL=0;vare_ANTALL<32;vare_ANTALL++){if(!너비값->보이는지)return 0;if(너비값->område_VERDI==1)return 1;너비값=element_VERDI(eier_objekt,너비값->overordnet);if(!너비값)return 0;}return 0;}
static void Tekst(int x_koordinat,int Y_koordinat,miniprogram_status *너비값,int 최대값,unsigned 색상,unsigned 배경색){int betalt_plassere=0;for(unsigned 순번=0;순번<너비값->lengde_VERDI;순번++){unsigned tegn_koding=너비값->Tekst[순번],너비=tegn_koding>=256?16:8;if(betalt_plassere+(int)너비>최대값)break;Terminal_figur(x_koordinat+betalt_plassere,Y_koordinat,tegn_koding,색상,배경색);betalt_plassere+=너비;}}
void 화면다시그림(int eier_objekt){
    if(!화면보임(eier_objekt))return;
    for(int behandling_ordre=1;behandling_ordre<=5;behandling_ordre++)for(int 순번=0;순번<32;순번++){
        miniprogram_status *너비값=&요소들[eier_objekt][순번];if(너비값->område_VERDI!=behandling_ordre||!표시됨(eier_objekt,너비값))continue;int x_koordinat,Y_koordinat;Posisjon(eier_objekt,너비값,&x_koordinat,&Y_koordinat);
        if(behandling_ordre==1){사각영역(x_koordinat,Y_koordinat,너비값->너비값,너비값->높이값,0xeee9e0);사각영역(x_koordinat,Y_koordinat,너비값->너비값,30,0x905020);Tekst(x_koordinat+10,Y_koordinat+7,너비값,너비값->너비값-50,0xffffff,0x905020);사각영역(x_koordinat+너비값->너비값-28,Y_koordinat+4,24,22,0x5555b8);Terminal_figur(x_koordinat+너비값->너비값-20,Y_koordinat+7,'X',0xffffff,0x5555b8);}
        if(behandling_ordre==2)사각영역(x_koordinat,Y_koordinat,너비값->너비값,너비값->높이값,0xeee9e0);
        if(behandling_ordre>=3){unsigned 배경색=behandling_ordre==4?0xc0ab86:behandling_ordre==5?0xffffff:0xeee9e0;if(behandling_ordre!=3)사각영역(x_koordinat,Y_koordinat,너비값->너비값,너비값->높이값,배경색);Tekst(x_koordinat+4,Y_koordinat+4,너비값,너비값->너비값-8,0x201a15,배경색);if(behandling_ordre==5&&Fokus_f7e69dab[eier_objekt]==순번+1)사각영역(x_koordinat,Y_koordinat+너비값->높이값-2,너비값->너비값,2,0x905020);}
    }
}
int skjermbilde_overlegg(int eier_objekt,int x_koordinat,int Y_koordinat){
    if(!화면보임(eier_objekt))return 0;
    for(int 순번=0;순번<32;순번++){
        miniprogram_status *Vindu=&요소들[eier_objekt][순번];
        if(Vindu->område_VERDI==1&&Vindu->보이는지&&x_koordinat>=Vindu->x_koordinat&&Y_koordinat>=Vindu->Y_koordinat&&
           x_koordinat<Vindu->x_koordinat+Vindu->너비값&&Y_koordinat<Vindu->Y_koordinat+Vindu->높이값)return 1;
    }return 0;
}
int skjermbilde_peker(int eier_objekt,unsigned 눌림,int x_koordinat,int Y_koordinat){
    if(!화면보임(eier_objekt))return 0;
    if(눌림&1)for(int 순번=31;순번>=0;순번--){miniprogram_status *너비값=&요소들[eier_objekt][순번];if(!너비값->område_VERDI||!표시됨(eier_objekt,너비값))continue;int vindu_X,vindu_Y;Posisjon(eier_objekt,너비값,&vindu_X,&vindu_Y);
        if(x_koordinat<vindu_X||Y_koordinat<vindu_Y||x_koordinat>=vindu_X+너비값->너비값||Y_koordinat>=vindu_Y+너비값->높이값)continue;
        if(너비값->område_VERDI==1&&Y_koordinat<vindu_Y+30&&x_koordinat>=vindu_X+너비값->너비값-28){if(너비값->Oppsett_Policy!=0)너비값->보이는지=0;Hendelse(eier_objekt,0x10000+순번+1);Tavle_Terminal(3);return 1;}
        if(너비값->område_VERDI==4){Hendelse(eier_objekt,순번+1);return 1;}if(너비값->område_VERDI==5){Fokus_f7e69dab[eier_objekt]=순번+1;Tavle_Terminal(3);return 1;}
        if(너비값->område_VERDI==1)return 1;
    }return 0;
}
void 화면누름(int eier_objekt,unsigned SEKUND_VERDI){
    miniprogram_status *너비값=element_VERDI(eier_objekt,Fokus_f7e69dab[eier_objekt]);if(!너비값||너비값->område_VERDI!=5)return;
    if(SEKUND_VERDI==13||SEKUND_VERDI==10){Hendelse(eier_objekt,Fokus_f7e69dab[eier_objekt]);return;}
    if(SEKUND_VERDI==8||SEKUND_VERDI==127){if(너비값->lengde_VERDI)너비값->lengde_VERDI--;긴부호없는값[eier_objekt]=0;}
    else{
        unsigned tegn_koding=SEKUND_VERDI;
        if(긴부호없는값[eier_objekt]){if((SEKUND_VERDI&192)!=128){긴부호없는값[eier_objekt]=0;return;}부호없는결과[eier_objekt]=(부호없는결과[eier_objekt]<<6)|(SEKUND_VERDI&63);if(--긴부호없는값[eier_objekt])return;tegn_koding=부호없는결과[eier_objekt];}
        else if(SEKUND_VERDI>=0xc2&&SEKUND_VERDI<=0xf4){긴부호없는값[eier_objekt]=SEKUND_VERDI<0xe0?1:SEKUND_VERDI<0xf0?2:3;부호없는결과[eier_objekt]=SEKUND_VERDI&((1u<<(6-긴부호없는값[eier_objekt]))-1);return;}
        else if(SEKUND_VERDI<32||SEKUND_VERDI>=128)return;
        if(tegn_koding>0x10ffff||(tegn_koding>=0xd800&&tegn_koding<=0xdfff))return;if(너비값->lengde_VERDI<127)너비값->Tekst[너비값->lengde_VERDI++]=tegn_koding;
    }
    Tavle_Terminal(3);
}
int 화면호출(int eier_objekt,unsigned Handling,int identifikator_VERDI,int 첫째값,int SEKUND_VERDI,int tegnkode,int mål_data){
    if(eier_objekt<0||eier_objekt>=4)return -22;miniprogram_status *너비값=element_VERDI(eier_objekt,identifikator_VERDI);
    if(Handling==0){if(identifikator_VERDI<1||identifikator_VERDI>5)return -22;for(int 순번=0;순번<32;순번++)if(요소들[eier_objekt][순번].område_VERDI==0){너비값=&요소들[eier_objekt][순번];memset(너비값,0,sizeof(*너비값));너비값->område_VERDI=identifikator_VERDI;너비값->보이는지=identifikator_VERDI!=1;너비값->너비값=identifikator_VERDI==1?380:220;너비값->높이값=identifikator_VERDI==1?240:28;너비값->Oppsett_Policy=1;너비값->x_koordinat=identifikator_VERDI==1?130:16;너비값->Y_koordinat=identifikator_VERDI==1?110:16;return 순번+1;}return -28;}
    if(Handling==5){if(!oppføring_ANTALL[eier_objekt])return 0;int 반환값=hendelse_Liste[eier_objekt][첫항목[eier_objekt]];첫항목[eier_objekt]=(첫항목[eier_objekt]+1)%16;oppføring_ANTALL[eier_objekt]--;return 반환값;}
    if(Handling==6)return 화면보임(eier_objekt);
    if(!너비값)return -9;
    int 이전표시=표시됨(eier_objekt,너비값);
    if(Handling==1){int 바탕너비=보드화면너비(),바탕높이=보드화면높이();if(첫째값<0||SEKUND_VERDI<0||tegnkode<1||mål_data<1||첫째값>바탕너비||SEKUND_VERDI>바탕높이||tegnkode>바탕너비-첫째값||mål_data>바탕높이-SEKUND_VERDI)return -22;너비값->x_koordinat=첫째값;너비값->Y_koordinat=SEKUND_VERDI;너비값->너비값=tegnkode;너비값->높이값=mål_data;너비값->manuell_Oppsett=1;}
    else if(Handling==2){miniprogram_status *underordnet=element_VERDI(eier_objekt,첫째값);if(!underordnet||underordnet==너비값||underordnet->område_VERDI==1)return -22;int data_plassere=identifikator_VERDI;for(int 깊이=0;data_plassere&&깊이<32;깊이++){if(data_plassere==첫째값)return -22;miniprogram_status *위쪽=element_VERDI(eier_objekt,data_plassere);data_plassere=위쪽?위쪽->overordnet:0;}underordnet->overordnet=identifikator_VERDI;if(!underordnet->manuell_Oppsett){int 형제요소=0;for(int 순번=0;순번<32;순번++)if(&요소들[eier_objekt][순번]!=underordnet&&요소들[eier_objekt][순번].overordnet==identifikator_VERDI)형제요소++;underordnet->Y_koordinat=16+형제요소*36;}}
    else if(Handling==3)너비값->보이는지=첫째값!=0;
    else if(Handling==4)너비값->보이는지=0;
    else if(Handling==7)너비값->Oppsett_Policy=첫째값;
    else if(Handling==8)return 너비값->lengde_VERDI;
    else if(Handling==9)return 첫째값>=0&&(unsigned)첫째값<너비값->lengde_VERDI?너비값->Tekst[첫째값]:-22;
    else return -22;
    if(이전표시||표시됨(eier_objekt,너비값))Tavle_Terminal(3);return 0;
}
int skjermbilde_SMS(int eier_objekt,int identifikator_VERDI,const uint32_t *data,unsigned vare_ANTALL){miniprogram_status *너비값=element_VERDI(eier_objekt,identifikator_VERDI);if(!너비값)return -9;if(vare_ANTALL>127)return -22;for(unsigned 순번=0;순번<vare_ANTALL;순번++){unsigned tegn_koding=data[순번];if(tegn_koding>0x10ffff||(tegn_koding>=0xd800&&tegn_koding<=0xdfff))return -22;}for(unsigned 순번=0;순번<vare_ANTALL;순번++)너비값->Tekst[순번]=data[순번];너비값->lengde_VERDI=vare_ANTALL;if(표시됨(eier_objekt,너비값))Tavle_Terminal(3);return 0;}
