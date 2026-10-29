#include "../명명/기계연결이름.h"
#include "scherm_info.h"
/* Small native peer layer for the explicitly supported Swing subset. */
#include <stdint.h>
#include <stddef.h>
extern uintptr_t Bord_pixel(uintptr_t,uintptr_t,uintptr_t),Bord_Terminal(uintptr_t);
extern void Terminal_symbool(unsigned,unsigned,unsigned,unsigned,unsigned);
extern void *memset(void *,int,size_t);
typedef struct { int gebied_WAARDE,bovenliggend,x_coördinaat,Y_coördinaat,너비값,aangevraagd_hoogte_WAARDE,보이는지,handmatig_Indeling,Indeling_Policy;unsigned tekst[128],tijdsduur_WAARDE; } widget_Status;
static widget_Status 요소들[4][32];
static int Prioriteit[4],gebeurtenis_Lijst[4][16];static unsigned 첫항목[4],invoer_AANTAL_8f7753a1[4],부호없는결과[4],긴부호없는값[4];
static void Gebeurtenis(int eigenaar_object,int WAARDE){if(invoer_AANTAL_8f7753a1[eigenaar_object]<16){gebeurtenis_Lijst[eigenaar_object][(첫항목[eigenaar_object]+invoer_AANTAL_8f7753a1[eigenaar_object])%16]=WAARDE;invoer_AANTAL_8f7753a1[eigenaar_object]++;}}
static widget_Status *element_WAARDE(int eigenaar_object,int id_WAARDE){return eigenaar_object>=0&&eigenaar_object<4&&id_WAARDE>0&&id_WAARDE<=32&&요소들[eigenaar_object][id_WAARDE-1].gebied_WAARDE?&요소들[eigenaar_object][id_WAARDE-1]:0;}
static void 사각영역(int x_coördinaat,int Y_coördinaat,int 너비값,int aangevraagd_hoogte_WAARDE,unsigned 색상){Bord_rechthoek_vullen(x_coördinaat,Y_coördinaat,너비값,aangevraagd_hoogte_WAARDE,색상);}
int 화면보임(int eigenaar_object){if(eigenaar_object<0||eigenaar_object>=4)return 0;for(int 순번=0;순번<32;순번++)if(요소들[eigenaar_object][순번].gebied_WAARDE==1&&요소들[eigenaar_object][순번].보이는지)return 1;return 0;}
void initialiseren_scherm(int eigenaar_object){memset(요소들[eigenaar_object],0,sizeof(요소들[eigenaar_object]));invoer_AANTAL_8f7753a1[eigenaar_object]=첫항목[eigenaar_object]=Prioriteit[eigenaar_object]=긴부호없는값[eigenaar_object]=0;}
static void positie(int eigenaar_object,widget_Status *너비값,int *x_coördinaat,int *Y_coördinaat){*x_coördinaat=너비값->x_coördinaat;*Y_coördinaat=너비값->Y_coördinaat;int gegevens_functie=너비값->bovenliggend;for(int item_AANTAL=0;gegevens_functie&&item_AANTAL<32;item_AANTAL++){widget_Status *위쪽=element_WAARDE(eigenaar_object,gegevens_functie);if(!위쪽)break;*x_coördinaat+=위쪽->x_coördinaat;*Y_coördinaat+=위쪽->Y_coördinaat+(위쪽->gebied_WAARDE==1?30:0);gegevens_functie=위쪽->bovenliggend;}}
static int 표시됨(int eigenaar_object,widget_Status *너비값){for(int item_AANTAL=0;item_AANTAL<32;item_AANTAL++){if(!너비값->보이는지)return 0;if(너비값->gebied_WAARDE==1)return 1;너비값=element_WAARDE(eigenaar_object,너비값->bovenliggend);if(!너비값)return 0;}return 0;}
static void tekst(int x_coördinaat,int Y_coördinaat,widget_Status *너비값,int 최대값,unsigned 색상,unsigned 배경색){int actueel_functie=0;for(unsigned 순번=0;순번<너비값->tijdsduur_WAARDE;순번++){unsigned tekencodering=너비값->tekst[순번],너비=tekencodering>=256?16:8;if(actueel_functie+(int)너비>최대값)break;Terminal_symbool(x_coördinaat+actueel_functie,Y_coördinaat,tekencodering,색상,배경색);actueel_functie+=너비;}}
void 화면다시그림(int eigenaar_object){
    if(!화면보임(eigenaar_object))return;
    for(int verwerking_order=1;verwerking_order<=5;verwerking_order++)for(int 순번=0;순번<32;순번++){
        widget_Status *너비값=&요소들[eigenaar_object][순번];if(너비값->gebied_WAARDE!=verwerking_order||!표시됨(eigenaar_object,너비값))continue;int x_coördinaat,Y_coördinaat;positie(eigenaar_object,너비값,&x_coördinaat,&Y_coördinaat);
        if(verwerking_order==1){사각영역(x_coördinaat,Y_coördinaat,너비값->너비값,너비값->aangevraagd_hoogte_WAARDE,0xeee9e0);사각영역(x_coördinaat,Y_coördinaat,너비값->너비값,30,0x905020);tekst(x_coördinaat+10,Y_coördinaat+7,너비값,너비값->너비값-50,0xffffff,0x905020);사각영역(x_coördinaat+너비값->너비값-28,Y_coördinaat+4,24,22,0x5555b8);Terminal_symbool(x_coördinaat+너비값->너비값-20,Y_coördinaat+7,'X',0xffffff,0x5555b8);}
        if(verwerking_order==2)사각영역(x_coördinaat,Y_coördinaat,너비값->너비값,너비값->aangevraagd_hoogte_WAARDE,0xeee9e0);
        if(verwerking_order>=3){unsigned 배경색=verwerking_order==4?0xc0ab86:verwerking_order==5?0xffffff:0xeee9e0;if(verwerking_order!=3)사각영역(x_coördinaat,Y_coördinaat,너비값->너비값,너비값->aangevraagd_hoogte_WAARDE,배경색);tekst(x_coördinaat+4,Y_coördinaat+4,너비값,너비값->너비값-8,0x201a15,배경색);if(verwerking_order==5&&Prioriteit[eigenaar_object]==순번+1)사각영역(x_coördinaat,Y_coördinaat+너비값->aangevraagd_hoogte_WAARDE-2,너비값->너비값,2,0x905020);}
    }
}
int scherm_overlay(int eigenaar_object,int x_coördinaat,int Y_coördinaat){
    if(!화면보임(eigenaar_object))return 0;
    for(int 순번=0;순번<32;순번++){
        widget_Status *Venster=&요소들[eigenaar_object][순번];
        if(Venster->gebied_WAARDE==1&&Venster->보이는지&&x_coördinaat>=Venster->x_coördinaat&&Y_coördinaat>=Venster->Y_coördinaat&&
           x_coördinaat<Venster->x_coördinaat+Venster->너비값&&Y_coördinaat<Venster->Y_coördinaat+Venster->aangevraagd_hoogte_WAARDE)return 1;
    }return 0;
}
int scherm_wijzer(int eigenaar_object,unsigned 눌림,int x_coördinaat,int Y_coördinaat){
    if(!화면보임(eigenaar_object))return 0;
    if(눌림&1)for(int 순번=31;순번>=0;순번--){widget_Status *너비값=&요소들[eigenaar_object][순번];if(!너비값->gebied_WAARDE||!표시됨(eigenaar_object,너비값))continue;int venster_X,venster_Y;positie(eigenaar_object,너비값,&venster_X,&venster_Y);
        if(x_coördinaat<venster_X||Y_coördinaat<venster_Y||x_coördinaat>=venster_X+너비값->너비값||Y_coördinaat>=venster_Y+너비값->aangevraagd_hoogte_WAARDE)continue;
        if(너비값->gebied_WAARDE==1&&Y_coördinaat<venster_Y+30&&x_coördinaat>=venster_X+너비값->너비값-28){if(너비값->Indeling_Policy!=0)너비값->보이는지=0;Gebeurtenis(eigenaar_object,0x10000+순번+1);Bord_Terminal(3);return 1;}
        if(너비값->gebied_WAARDE==4){Gebeurtenis(eigenaar_object,순번+1);return 1;}if(너비값->gebied_WAARDE==5){Prioriteit[eigenaar_object]=순번+1;Bord_Terminal(3);return 1;}
        if(너비값->gebied_WAARDE==1)return 1;
    }return 0;
}
void 화면누름(int eigenaar_object,unsigned SECONDE_WAARDE){
    widget_Status *너비값=element_WAARDE(eigenaar_object,Prioriteit[eigenaar_object]);if(!너비값||너비값->gebied_WAARDE!=5)return;
    if(SECONDE_WAARDE==13||SECONDE_WAARDE==10){Gebeurtenis(eigenaar_object,Prioriteit[eigenaar_object]);return;}
    if(SECONDE_WAARDE==8||SECONDE_WAARDE==127){if(너비값->tijdsduur_WAARDE)너비값->tijdsduur_WAARDE--;긴부호없는값[eigenaar_object]=0;}
    else{
        unsigned tekencodering=SECONDE_WAARDE;
        if(긴부호없는값[eigenaar_object]){if((SECONDE_WAARDE&192)!=128){긴부호없는값[eigenaar_object]=0;return;}부호없는결과[eigenaar_object]=(부호없는결과[eigenaar_object]<<6)|(SECONDE_WAARDE&63);if(--긴부호없는값[eigenaar_object])return;tekencodering=부호없는결과[eigenaar_object];}
        else if(SECONDE_WAARDE>=0xc2&&SECONDE_WAARDE<=0xf4){긴부호없는값[eigenaar_object]=SECONDE_WAARDE<0xe0?1:SECONDE_WAARDE<0xf0?2:3;부호없는결과[eigenaar_object]=SECONDE_WAARDE&((1u<<(6-긴부호없는값[eigenaar_object]))-1);return;}
        else if(SECONDE_WAARDE<32||SECONDE_WAARDE>=128)return;
        if(tekencodering>0x10ffff||(tekencodering>=0xd800&&tekencodering<=0xdfff))return;if(너비값->tijdsduur_WAARDE<127)너비값->tekst[너비값->tijdsduur_WAARDE++]=tekencodering;
    }
    Bord_Terminal(3);
}
int 화면호출(int eigenaar_object,unsigned Actie,int id_WAARDE,int 첫째값,int SECONDE_WAARDE,int codepoint,int doel_gegevens){
    if(eigenaar_object<0||eigenaar_object>=4)return -22;widget_Status *너비값=element_WAARDE(eigenaar_object,id_WAARDE);
    if(Actie==0){if(id_WAARDE<1||id_WAARDE>5)return -22;for(int 순번=0;순번<32;순번++)if(요소들[eigenaar_object][순번].gebied_WAARDE==0){너비값=&요소들[eigenaar_object][순번];memset(너비값,0,sizeof(*너비값));너비값->gebied_WAARDE=id_WAARDE;너비값->보이는지=id_WAARDE!=1;너비값->너비값=id_WAARDE==1?380:220;너비값->aangevraagd_hoogte_WAARDE=id_WAARDE==1?240:28;너비값->Indeling_Policy=1;너비값->x_coördinaat=id_WAARDE==1?130:16;너비값->Y_coördinaat=id_WAARDE==1?110:16;return 순번+1;}return -28;}
    if(Actie==5){if(!invoer_AANTAL_8f7753a1[eigenaar_object])return 0;int 반환값=gebeurtenis_Lijst[eigenaar_object][첫항목[eigenaar_object]];첫항목[eigenaar_object]=(첫항목[eigenaar_object]+1)%16;invoer_AANTAL_8f7753a1[eigenaar_object]--;return 반환값;}
    if(Actie==6)return 화면보임(eigenaar_object);
    if(!너비값)return -9;
    int 이전표시=표시됨(eigenaar_object,너비값);
    if(Actie==1){int 바탕너비=보드화면너비(),Achtergrond_hoogte=Bord_scherm_hoogte();if(첫째값<0||SECONDE_WAARDE<0||codepoint<1||doel_gegevens<1||첫째값>바탕너비||SECONDE_WAARDE>Achtergrond_hoogte||codepoint>바탕너비-첫째값||doel_gegevens>Achtergrond_hoogte-SECONDE_WAARDE)return -22;너비값->x_coördinaat=첫째값;너비값->Y_coördinaat=SECONDE_WAARDE;너비값->너비값=codepoint;너비값->aangevraagd_hoogte_WAARDE=doel_gegevens;너비값->handmatig_Indeling=1;}
    else if(Actie==2){widget_Status *onderliggend=element_WAARDE(eigenaar_object,첫째값);if(!onderliggend||onderliggend==너비값||onderliggend->gebied_WAARDE==1)return -22;int gegevens_functie=id_WAARDE;for(int 깊이=0;gegevens_functie&&깊이<32;깊이++){if(gegevens_functie==첫째값)return -22;widget_Status *위쪽=element_WAARDE(eigenaar_object,gegevens_functie);gegevens_functie=위쪽?위쪽->bovenliggend:0;}onderliggend->bovenliggend=id_WAARDE;if(!onderliggend->handmatig_Indeling){int 형제요소=0;for(int 순번=0;순번<32;순번++)if(&요소들[eigenaar_object][순번]!=onderliggend&&요소들[eigenaar_object][순번].bovenliggend==id_WAARDE)형제요소++;onderliggend->Y_coördinaat=16+형제요소*36;}}
    else if(Actie==3)너비값->보이는지=첫째값!=0;
    else if(Actie==4)너비값->보이는지=0;
    else if(Actie==7)너비값->Indeling_Policy=첫째값;
    else if(Actie==8)return 너비값->tijdsduur_WAARDE;
    else if(Actie==9)return 첫째값>=0&&(unsigned)첫째값<너비값->tijdsduur_WAARDE?너비값->tekst[첫째값]:-22;
    else return -22;
    if(이전표시||표시됨(eigenaar_object,너비값))Bord_Terminal(3);return 0;
}
int scherm_sms(int eigenaar_object,int id_WAARDE,const uint32_t *gegevens,unsigned item_AANTAL){widget_Status *너비값=element_WAARDE(eigenaar_object,id_WAARDE);if(!너비값)return -9;if(item_AANTAL>127)return -22;for(unsigned 순번=0;순번<item_AANTAL;순번++){unsigned tekencodering=gegevens[순번];if(tekencodering>0x10ffff||(tekencodering>=0xd800&&tekencodering<=0xdfff))return -22;}for(unsigned 순번=0;순번<item_AANTAL;순번++)너비값->tekst[순번]=gegevens[순번];너비값->tijdsduur_WAARDE=item_AANTAL;if(표시됨(eigenaar_object,너비값))Bord_Terminal(3);return 0;}
