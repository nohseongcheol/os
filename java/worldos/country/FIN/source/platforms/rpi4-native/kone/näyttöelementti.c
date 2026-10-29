#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* Small native peer layer for the explicitly supported Swing subset. */
#include <stdint.h>
#include <stddef.h>
extern uintptr_t Taulu_kuvapiste(uintptr_t,uintptr_t,uintptr_t),Taulu_Pääte(uintptr_t);
extern void Pääte_merkki(unsigned,unsigned,unsigned,unsigned,unsigned);
extern void *memset(void *,int,size_t);
typedef struct { int alue_ARVO,pää,x_koordinaatti,Y_koordinaatti,너비값,높이값,보이는지,manuaalinen_Asettelu,Asettelu_Käytäntö;unsigned teksti[128],kesto_ARVO; } pienoissovellus_Tila;
static pienoissovellus_Tila 요소들[4][32];
static int Tärkeät[4],tapahtuma_luettelo[4][16];static unsigned 첫항목[4],merkintä_LASKE[4],부호없는결과[4],긴부호없는값[4];
static void Tapahtuma(int omistaja_objekti,int ARVO){if(merkintä_LASKE[omistaja_objekti]<16){tapahtuma_luettelo[omistaja_objekti][(첫항목[omistaja_objekti]+merkintä_LASKE[omistaja_objekti])%16]=ARVO;merkintä_LASKE[omistaja_objekti]++;}}
static pienoissovellus_Tila *elementti_ARVO(int omistaja_objekti,int tunniste_ARVO){return omistaja_objekti>=0&&omistaja_objekti<4&&tunniste_ARVO>0&&tunniste_ARVO<=32&&요소들[omistaja_objekti][tunniste_ARVO-1].alue_ARVO?&요소들[omistaja_objekti][tunniste_ARVO-1]:0;}
static void 사각영역(int x_koordinaatti,int Y_koordinaatti,int 너비값,int 높이값,unsigned 색상){Taulu_suorakulmio_täyttö(x_koordinaatti,Y_koordinaatti,너비값,높이값,색상);}
int 화면보임(int omistaja_objekti){if(omistaja_objekti<0||omistaja_objekti>=4)return 0;for(int 순번=0;순번<32;순번++)if(요소들[omistaja_objekti][순번].alue_ARVO==1&&요소들[omistaja_objekti][순번].보이는지)return 1;return 0;}
void 화면초기화(int omistaja_objekti){memset(요소들[omistaja_objekti],0,sizeof(요소들[omistaja_objekti]));merkintä_LASKE[omistaja_objekti]=첫항목[omistaja_objekti]=Tärkeät[omistaja_objekti]=긴부호없는값[omistaja_objekti]=0;}
static void paikka(int omistaja_objekti,pienoissovellus_Tila *너비값,int *x_koordinaatti,int *Y_koordinaatti){*x_koordinaatti=너비값->x_koordinaatti;*Y_koordinaatti=너비값->Y_koordinaatti;int data_toimi=너비값->pää;for(int kohde_LASKE=0;data_toimi&&kohde_LASKE<32;kohde_LASKE++){pienoissovellus_Tila *위쪽=elementti_ARVO(omistaja_objekti,data_toimi);if(!위쪽)break;*x_koordinaatti+=위쪽->x_koordinaatti;*Y_koordinaatti+=위쪽->Y_koordinaatti+(위쪽->alue_ARVO==1?30:0);data_toimi=위쪽->pää;}}
static int 표시됨(int omistaja_objekti,pienoissovellus_Tila *너비값){for(int kohde_LASKE=0;kohde_LASKE<32;kohde_LASKE++){if(!너비값->보이는지)return 0;if(너비값->alue_ARVO==1)return 1;너비값=elementti_ARVO(omistaja_objekti,너비값->pää);if(!너비값)return 0;}return 0;}
static void teksti(int x_koordinaatti,int Y_koordinaatti,pienoissovellus_Tila *너비값,int 최대값,unsigned 색상,unsigned 배경색){int nykyinen_toimi=0;for(unsigned 순번=0;순번<너비값->kesto_ARVO;순번++){unsigned merkkikoodaus=너비값->teksti[순번],너비=merkkikoodaus>=256?16:8;if(nykyinen_toimi+(int)너비>최대값)break;Pääte_merkki(x_koordinaatti+nykyinen_toimi,Y_koordinaatti,merkkikoodaus,색상,배경색);nykyinen_toimi+=너비;}}
void 화면다시그림(int omistaja_objekti){
    if(!화면보임(omistaja_objekti))return;
    for(int käsittely_tilata=1;käsittely_tilata<=5;käsittely_tilata++)for(int 순번=0;순번<32;순번++){
        pienoissovellus_Tila *너비값=&요소들[omistaja_objekti][순번];if(너비값->alue_ARVO!=käsittely_tilata||!표시됨(omistaja_objekti,너비값))continue;int x_koordinaatti,Y_koordinaatti;paikka(omistaja_objekti,너비값,&x_koordinaatti,&Y_koordinaatti);
        if(käsittely_tilata==1){사각영역(x_koordinaatti,Y_koordinaatti,너비값->너비값,너비값->높이값,0xeee9e0);사각영역(x_koordinaatti,Y_koordinaatti,너비값->너비값,30,0x905020);teksti(x_koordinaatti+10,Y_koordinaatti+7,너비값,너비값->너비값-50,0xffffff,0x905020);사각영역(x_koordinaatti+너비값->너비값-28,Y_koordinaatti+4,24,22,0x5555b8);Pääte_merkki(x_koordinaatti+너비값->너비값-20,Y_koordinaatti+7,'X',0xffffff,0x5555b8);}
        if(käsittely_tilata==2)사각영역(x_koordinaatti,Y_koordinaatti,너비값->너비값,너비값->높이값,0xeee9e0);
        if(käsittely_tilata>=3){unsigned 배경색=käsittely_tilata==4?0xc0ab86:käsittely_tilata==5?0xffffff:0xeee9e0;if(käsittely_tilata!=3)사각영역(x_koordinaatti,Y_koordinaatti,너비값->너비값,너비값->높이값,배경색);teksti(x_koordinaatti+4,Y_koordinaatti+4,너비값,너비값->너비값-8,0x201a15,배경색);if(käsittely_tilata==5&&Tärkeät[omistaja_objekti]==순번+1)사각영역(x_koordinaatti,Y_koordinaatti+너비값->높이값-2,너비값->너비값,2,0x905020);}
    }
}
int 화면덮음(int omistaja_objekti,int x_koordinaatti,int Y_koordinaatti){
    if(!화면보임(omistaja_objekti))return 0;
    for(int 순번=0;순번<32;순번++){
        pienoissovellus_Tila *Ikkuna=&요소들[omistaja_objekti][순번];
        if(Ikkuna->alue_ARVO==1&&Ikkuna->보이는지&&x_koordinaatti>=Ikkuna->x_koordinaatti&&Y_koordinaatti>=Ikkuna->Y_koordinaatti&&
           x_koordinaatti<Ikkuna->x_koordinaatti+Ikkuna->너비값&&Y_koordinaatti<Ikkuna->Y_koordinaatti+Ikkuna->높이값)return 1;
    }return 0;
}
int 화면가리킴(int omistaja_objekti,unsigned 눌림,int x_koordinaatti,int Y_koordinaatti){
    if(!화면보임(omistaja_objekti))return 0;
    if(눌림&1)for(int 순번=31;순번>=0;순번--){pienoissovellus_Tila *너비값=&요소들[omistaja_objekti][순번];if(!너비값->alue_ARVO||!표시됨(omistaja_objekti,너비값))continue;int ikkuna_X,ikkuna_Y;paikka(omistaja_objekti,너비값,&ikkuna_X,&ikkuna_Y);
        if(x_koordinaatti<ikkuna_X||Y_koordinaatti<ikkuna_Y||x_koordinaatti>=ikkuna_X+너비값->너비값||Y_koordinaatti>=ikkuna_Y+너비값->높이값)continue;
        if(너비값->alue_ARVO==1&&Y_koordinaatti<ikkuna_Y+30&&x_koordinaatti>=ikkuna_X+너비값->너비값-28){if(너비값->Asettelu_Käytäntö!=0)너비값->보이는지=0;Tapahtuma(omistaja_objekti,0x10000+순번+1);Taulu_Pääte(3);return 1;}
        if(너비값->alue_ARVO==4){Tapahtuma(omistaja_objekti,순번+1);return 1;}if(너비값->alue_ARVO==5){Tärkeät[omistaja_objekti]=순번+1;Taulu_Pääte(3);return 1;}
        if(너비값->alue_ARVO==1)return 1;
    }return 0;
}
void 화면누름(int omistaja_objekti,unsigned SEKUNNIT_ARVO){
    pienoissovellus_Tila *너비값=elementti_ARVO(omistaja_objekti,Tärkeät[omistaja_objekti]);if(!너비값||너비값->alue_ARVO!=5)return;
    if(SEKUNNIT_ARVO==13||SEKUNNIT_ARVO==10){Tapahtuma(omistaja_objekti,Tärkeät[omistaja_objekti]);return;}
    if(SEKUNNIT_ARVO==8||SEKUNNIT_ARVO==127){if(너비값->kesto_ARVO)너비값->kesto_ARVO--;긴부호없는값[omistaja_objekti]=0;}
    else{
        unsigned merkkikoodaus=SEKUNNIT_ARVO;
        if(긴부호없는값[omistaja_objekti]){if((SEKUNNIT_ARVO&192)!=128){긴부호없는값[omistaja_objekti]=0;return;}부호없는결과[omistaja_objekti]=(부호없는결과[omistaja_objekti]<<6)|(SEKUNNIT_ARVO&63);if(--긴부호없는값[omistaja_objekti])return;merkkikoodaus=부호없는결과[omistaja_objekti];}
        else if(SEKUNNIT_ARVO>=0xc2&&SEKUNNIT_ARVO<=0xf4){긴부호없는값[omistaja_objekti]=SEKUNNIT_ARVO<0xe0?1:SEKUNNIT_ARVO<0xf0?2:3;부호없는결과[omistaja_objekti]=SEKUNNIT_ARVO&((1u<<(6-긴부호없는값[omistaja_objekti]))-1);return;}
        else if(SEKUNNIT_ARVO<32||SEKUNNIT_ARVO>=128)return;
        if(merkkikoodaus>0x10ffff||(merkkikoodaus>=0xd800&&merkkikoodaus<=0xdfff))return;if(너비값->kesto_ARVO<127)너비값->teksti[너비값->kesto_ARVO++]=merkkikoodaus;
    }
    Taulu_Pääte(3);
}
int 화면호출(int omistaja_objekti,unsigned Toiminto,int tunniste_ARVO,int 첫째값,int SEKUNNIT_ARVO,int merkkikoodi,int kohde_data){
    if(omistaja_objekti<0||omistaja_objekti>=4)return -22;pienoissovellus_Tila *너비값=elementti_ARVO(omistaja_objekti,tunniste_ARVO);
    if(Toiminto==0){if(tunniste_ARVO<1||tunniste_ARVO>5)return -22;for(int 순번=0;순번<32;순번++)if(요소들[omistaja_objekti][순번].alue_ARVO==0){너비값=&요소들[omistaja_objekti][순번];memset(너비값,0,sizeof(*너비값));너비값->alue_ARVO=tunniste_ARVO;너비값->보이는지=tunniste_ARVO!=1;너비값->너비값=tunniste_ARVO==1?380:220;너비값->높이값=tunniste_ARVO==1?240:28;너비값->Asettelu_Käytäntö=1;너비값->x_koordinaatti=tunniste_ARVO==1?130:16;너비값->Y_koordinaatti=tunniste_ARVO==1?110:16;return 순번+1;}return -28;}
    if(Toiminto==5){if(!merkintä_LASKE[omistaja_objekti])return 0;int 반환값=tapahtuma_luettelo[omistaja_objekti][첫항목[omistaja_objekti]];첫항목[omistaja_objekti]=(첫항목[omistaja_objekti]+1)%16;merkintä_LASKE[omistaja_objekti]--;return 반환값;}
    if(Toiminto==6)return 화면보임(omistaja_objekti);
    if(!너비값)return -9;
    int 이전표시=표시됨(omistaja_objekti,너비값);
    if(Toiminto==1){int 바탕너비=보드화면너비(),바탕높이=보드화면높이();if(첫째값<0||SEKUNNIT_ARVO<0||merkkikoodi<1||kohde_data<1||첫째값>바탕너비||SEKUNNIT_ARVO>바탕높이||merkkikoodi>바탕너비-첫째값||kohde_data>바탕높이-SEKUNNIT_ARVO)return -22;너비값->x_koordinaatti=첫째값;너비값->Y_koordinaatti=SEKUNNIT_ARVO;너비값->너비값=merkkikoodi;너비값->높이값=kohde_data;너비값->manuaalinen_Asettelu=1;}
    else if(Toiminto==2){pienoissovellus_Tila *alielementti=elementti_ARVO(omistaja_objekti,첫째값);if(!alielementti||alielementti==너비값||alielementti->alue_ARVO==1)return -22;int data_toimi=tunniste_ARVO;for(int 깊이=0;data_toimi&&깊이<32;깊이++){if(data_toimi==첫째값)return -22;pienoissovellus_Tila *위쪽=elementti_ARVO(omistaja_objekti,data_toimi);data_toimi=위쪽?위쪽->pää:0;}alielementti->pää=tunniste_ARVO;if(!alielementti->manuaalinen_Asettelu){int 형제요소=0;for(int 순번=0;순번<32;순번++)if(&요소들[omistaja_objekti][순번]!=alielementti&&요소들[omistaja_objekti][순번].pää==tunniste_ARVO)형제요소++;alielementti->Y_koordinaatti=16+형제요소*36;}}
    else if(Toiminto==3)너비값->보이는지=첫째값!=0;
    else if(Toiminto==4)너비값->보이는지=0;
    else if(Toiminto==7)너비값->Asettelu_Käytäntö=첫째값;
    else if(Toiminto==8)return 너비값->kesto_ARVO;
    else if(Toiminto==9)return 첫째값>=0&&(unsigned)첫째값<너비값->kesto_ARVO?너비값->teksti[첫째값]:-22;
    else return -22;
    if(이전표시||표시됨(omistaja_objekti,너비값))Taulu_Pääte(3);return 0;
}
int 화면글(int omistaja_objekti,int tunniste_ARVO,const uint32_t *data,unsigned kohde_LASKE){pienoissovellus_Tila *너비값=elementti_ARVO(omistaja_objekti,tunniste_ARVO);if(!너비값)return -9;if(kohde_LASKE>127)return -22;for(unsigned 순번=0;순번<kohde_LASKE;순번++){unsigned merkkikoodaus=data[순번];if(merkkikoodaus>0x10ffff||(merkkikoodaus>=0xd800&&merkkikoodaus<=0xdfff))return -22;}for(unsigned 순번=0;순번<kohde_LASKE;순번++)너비값->teksti[순번]=data[순번];너비값->kesto_ARVO=kohde_LASKE;if(표시됨(omistaja_objekti,너비값))Taulu_Pääte(3);return 0;}
