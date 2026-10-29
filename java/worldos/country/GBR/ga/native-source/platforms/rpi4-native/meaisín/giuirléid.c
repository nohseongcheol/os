#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* Small native peer layer for the explicitly supported Swing subset. */
#include <stdint.h>
#include <stddef.h>
extern uintptr_t clár_picteilín(uintptr_t,uintptr_t,uintptr_t),clár_Teirminéal(uintptr_t);
extern void Teirminéal_glif(unsigned,unsigned,unsigned,unsigned,unsigned);
extern void *memset(void *,int,size_t);
typedef struct { int catagóir_VALUE,부모항목,x_chomhordanáid,세로좌표,너비값,높이값,보이는지,láimhe_dáileadh,dáileadh_polasaí;unsigned Téacs[128],fad_VALUE; } giuirléid_staid;
static giuirléid_staid 요소들[4][32];
static int Fócasaithe[4],ócáid_Liosta[4][16];static unsigned 첫항목[4],iontráil_COUNT[4],부호없는결과[4],긴부호없는값[4];
static void ócáid(int úinéir_oibiacht,int VALUE){if(iontráil_COUNT[úinéir_oibiacht]<16){ócáid_Liosta[úinéir_oibiacht][(첫항목[úinéir_oibiacht]+iontráil_COUNT[úinéir_oibiacht])%16]=VALUE;iontráil_COUNT[úinéir_oibiacht]++;}}
static giuirléid_staid *eilimint_VALUE(int úinéir_oibiacht,int aitheantóir_VALUE){return úinéir_oibiacht>=0&&úinéir_oibiacht<4&&aitheantóir_VALUE>0&&aitheantóir_VALUE<=32&&요소들[úinéir_oibiacht][aitheantóir_VALUE-1].catagóir_VALUE?&요소들[úinéir_oibiacht][aitheantóir_VALUE-1]:0;}
static void 사각영역(int x_chomhordanáid,int 세로좌표,int 너비값,int 높이값,unsigned 색상){보드사각그림(x_chomhordanáid,세로좌표,너비값,높이값,색상);}
int 화면보임(int úinéir_oibiacht){if(úinéir_oibiacht<0||úinéir_oibiacht>=4)return 0;for(int 순번=0;순번<32;순번++)if(요소들[úinéir_oibiacht][순번].catagóir_VALUE==1&&요소들[úinéir_oibiacht][순번].보이는지)return 1;return 0;}
void 화면초기화(int úinéir_oibiacht){memset(요소들[úinéir_oibiacht],0,sizeof(요소들[úinéir_oibiacht]));iontráil_COUNT[úinéir_oibiacht]=첫항목[úinéir_oibiacht]=Fócasaithe[úinéir_oibiacht]=긴부호없는값[úinéir_oibiacht]=0;}
static void suíomh(int úinéir_oibiacht,giuirléid_staid *너비값,int *x_chomhordanáid,int *세로좌표){*x_chomhordanáid=너비값->x_chomhordanáid;*세로좌표=너비값->세로좌표;int sonraí_suíomh=너비값->부모항목;for(int mír_COUNT=0;sonraí_suíomh&&mír_COUNT<32;mír_COUNT++){giuirléid_staid *위쪽=eilimint_VALUE(úinéir_oibiacht,sonraí_suíomh);if(!위쪽)break;*x_chomhordanáid+=위쪽->x_chomhordanáid;*세로좌표+=위쪽->세로좌표+(위쪽->catagóir_VALUE==1?30:0);sonraí_suíomh=위쪽->부모항목;}}
static int 표시됨(int úinéir_oibiacht,giuirléid_staid *너비값){for(int mír_COUNT=0;mír_COUNT<32;mír_COUNT++){if(!너비값->보이는지)return 0;if(너비값->catagóir_VALUE==1)return 1;너비값=eilimint_VALUE(úinéir_oibiacht,너비값->부모항목);if(!너비값)return 0;}return 0;}
static void Téacs(int x_chomhordanáid,int 세로좌표,giuirléid_staid *너비값,int 최대값,unsigned 색상,unsigned 배경색){int 현재위치=0;for(unsigned 순번=0;순번<너비값->fad_VALUE;순번++){unsigned carachtar_ionchódú=너비값->Téacs[순번],너비=carachtar_ionchódú>=256?16:8;if(현재위치+(int)너비>최대값)break;Teirminéal_glif(x_chomhordanáid+현재위치,세로좌표,carachtar_ionchódú,색상,배경색);현재위치+=너비;}}
void 화면다시그림(int úinéir_oibiacht){
    if(!화면보임(úinéir_oibiacht))return;
    for(int 처리차례=1;처리차례<=5;처리차례++)for(int 순번=0;순번<32;순번++){
        giuirléid_staid *너비값=&요소들[úinéir_oibiacht][순번];if(너비값->catagóir_VALUE!=처리차례||!표시됨(úinéir_oibiacht,너비값))continue;int x_chomhordanáid,세로좌표;suíomh(úinéir_oibiacht,너비값,&x_chomhordanáid,&세로좌표);
        if(처리차례==1){사각영역(x_chomhordanáid,세로좌표,너비값->너비값,너비값->높이값,0xeee9e0);사각영역(x_chomhordanáid,세로좌표,너비값->너비값,30,0x905020);Téacs(x_chomhordanáid+10,세로좌표+7,너비값,너비값->너비값-50,0xffffff,0x905020);사각영역(x_chomhordanáid+너비값->너비값-28,세로좌표+4,24,22,0x5555b8);Teirminéal_glif(x_chomhordanáid+너비값->너비값-20,세로좌표+7,'X',0xffffff,0x5555b8);}
        if(처리차례==2)사각영역(x_chomhordanáid,세로좌표,너비값->너비값,너비값->높이값,0xeee9e0);
        if(처리차례>=3){unsigned 배경색=처리차례==4?0xc0ab86:처리차례==5?0xffffff:0xeee9e0;if(처리차례!=3)사각영역(x_chomhordanáid,세로좌표,너비값->너비값,너비값->높이값,배경색);Téacs(x_chomhordanáid+4,세로좌표+4,너비값,너비값->너비값-8,0x201a15,배경색);if(처리차례==5&&Fócasaithe[úinéir_oibiacht]==순번+1)사각영역(x_chomhordanáid,세로좌표+너비값->높이값-2,너비값->너비값,2,0x905020);}
    }
}
int 화면덮음(int úinéir_oibiacht,int x_chomhordanáid,int 세로좌표){
    if(!화면보임(úinéir_oibiacht))return 0;
    for(int 순번=0;순번<32;순번++){
        giuirléid_staid *fuinneog=&요소들[úinéir_oibiacht][순번];
        if(fuinneog->catagóir_VALUE==1&&fuinneog->보이는지&&x_chomhordanáid>=fuinneog->x_chomhordanáid&&세로좌표>=fuinneog->세로좌표&&
           x_chomhordanáid<fuinneog->x_chomhordanáid+fuinneog->너비값&&세로좌표<fuinneog->세로좌표+fuinneog->높이값)return 1;
    }return 0;
}
int 화면가리킴(int úinéir_oibiacht,unsigned 눌림,int x_chomhordanáid,int 세로좌표){
    if(!화면보임(úinéir_oibiacht))return 0;
    if(눌림&1)for(int 순번=31;순번>=0;순번--){giuirléid_staid *너비값=&요소들[úinéir_oibiacht][순번];if(!너비값->catagóir_VALUE||!표시됨(úinéir_oibiacht,너비값))continue;int 창가로,창세로;suíomh(úinéir_oibiacht,너비값,&창가로,&창세로);
        if(x_chomhordanáid<창가로||세로좌표<창세로||x_chomhordanáid>=창가로+너비값->너비값||세로좌표>=창세로+너비값->높이값)continue;
        if(너비값->catagóir_VALUE==1&&세로좌표<창세로+30&&x_chomhordanáid>=창가로+너비값->너비값-28){if(너비값->dáileadh_polasaí!=0)너비값->보이는지=0;ócáid(úinéir_oibiacht,0x10000+순번+1);clár_Teirminéal(3);return 1;}
        if(너비값->catagóir_VALUE==4){ócáid(úinéir_oibiacht,순번+1);return 1;}if(너비값->catagóir_VALUE==5){Fócasaithe[úinéir_oibiacht]=순번+1;clár_Teirminéal(3);return 1;}
        if(너비값->catagóir_VALUE==1)return 1;
    }return 0;
}
void 화면누름(int úinéir_oibiacht,unsigned SECOND_VALUE){
    giuirléid_staid *너비값=eilimint_VALUE(úinéir_oibiacht,Fócasaithe[úinéir_oibiacht]);if(!너비값||너비값->catagóir_VALUE!=5)return;
    if(SECOND_VALUE==13||SECOND_VALUE==10){ócáid(úinéir_oibiacht,Fócasaithe[úinéir_oibiacht]);return;}
    if(SECOND_VALUE==8||SECOND_VALUE==127){if(너비값->fad_VALUE)너비값->fad_VALUE--;긴부호없는값[úinéir_oibiacht]=0;}
    else{
        unsigned carachtar_ionchódú=SECOND_VALUE;
        if(긴부호없는값[úinéir_oibiacht]){if((SECOND_VALUE&192)!=128){긴부호없는값[úinéir_oibiacht]=0;return;}부호없는결과[úinéir_oibiacht]=(부호없는결과[úinéir_oibiacht]<<6)|(SECOND_VALUE&63);if(--긴부호없는값[úinéir_oibiacht])return;carachtar_ionchódú=부호없는결과[úinéir_oibiacht];}
        else if(SECOND_VALUE>=0xc2&&SECOND_VALUE<=0xf4){긴부호없는값[úinéir_oibiacht]=SECOND_VALUE<0xe0?1:SECOND_VALUE<0xf0?2:3;부호없는결과[úinéir_oibiacht]=SECOND_VALUE&((1u<<(6-긴부호없는값[úinéir_oibiacht]))-1);return;}
        else if(SECOND_VALUE<32||SECOND_VALUE>=128)return;
        if(carachtar_ionchódú>0x10ffff||(carachtar_ionchódú>=0xd800&&carachtar_ionchódú<=0xdfff))return;if(너비값->fad_VALUE<127)너비값->Téacs[너비값->fad_VALUE++]=carachtar_ionchódú;
    }
    clár_Teirminéal(3);
}
int 화면호출(int úinéir_oibiacht,unsigned Gníomh,int aitheantóir_VALUE,int 첫째값,int SECOND_VALUE,int pointe_cóid,int sprioc_sonraí){
    if(úinéir_oibiacht<0||úinéir_oibiacht>=4)return -22;giuirléid_staid *너비값=eilimint_VALUE(úinéir_oibiacht,aitheantóir_VALUE);
    if(Gníomh==0){if(aitheantóir_VALUE<1||aitheantóir_VALUE>5)return -22;for(int 순번=0;순번<32;순번++)if(요소들[úinéir_oibiacht][순번].catagóir_VALUE==0){너비값=&요소들[úinéir_oibiacht][순번];memset(너비값,0,sizeof(*너비값));너비값->catagóir_VALUE=aitheantóir_VALUE;너비값->보이는지=aitheantóir_VALUE!=1;너비값->너비값=aitheantóir_VALUE==1?380:220;너비값->높이값=aitheantóir_VALUE==1?240:28;너비값->dáileadh_polasaí=1;너비값->x_chomhordanáid=aitheantóir_VALUE==1?130:16;너비값->세로좌표=aitheantóir_VALUE==1?110:16;return 순번+1;}return -28;}
    if(Gníomh==5){if(!iontráil_COUNT[úinéir_oibiacht])return 0;int 반환값=ócáid_Liosta[úinéir_oibiacht][첫항목[úinéir_oibiacht]];첫항목[úinéir_oibiacht]=(첫항목[úinéir_oibiacht]+1)%16;iontráil_COUNT[úinéir_oibiacht]--;return 반환값;}
    if(Gníomh==6)return 화면보임(úinéir_oibiacht);
    if(!너비값)return -9;
    int 이전표시=표시됨(úinéir_oibiacht,너비값);
    if(Gníomh==1){int 바탕너비=보드화면너비(),바탕높이=보드화면높이();if(첫째값<0||SECOND_VALUE<0||pointe_cóid<1||sprioc_sonraí<1||첫째값>바탕너비||SECOND_VALUE>바탕높이||pointe_cóid>바탕너비-첫째값||sprioc_sonraí>바탕높이-SECOND_VALUE)return -22;너비값->x_chomhordanáid=첫째값;너비값->세로좌표=SECOND_VALUE;너비값->너비값=pointe_cóid;너비값->높이값=sprioc_sonraí;너비값->láimhe_dáileadh=1;}
    else if(Gníomh==2){giuirléid_staid *maceilimint=eilimint_VALUE(úinéir_oibiacht,첫째값);if(!maceilimint||maceilimint==너비값||maceilimint->catagóir_VALUE==1)return -22;int sonraí_suíomh=aitheantóir_VALUE;for(int 깊이=0;sonraí_suíomh&&깊이<32;깊이++){if(sonraí_suíomh==첫째값)return -22;giuirléid_staid *위쪽=eilimint_VALUE(úinéir_oibiacht,sonraí_suíomh);sonraí_suíomh=위쪽?위쪽->부모항목:0;}maceilimint->부모항목=aitheantóir_VALUE;if(!maceilimint->láimhe_dáileadh){int 형제요소=0;for(int 순번=0;순번<32;순번++)if(&요소들[úinéir_oibiacht][순번]!=maceilimint&&요소들[úinéir_oibiacht][순번].부모항목==aitheantóir_VALUE)형제요소++;maceilimint->세로좌표=16+형제요소*36;}}
    else if(Gníomh==3)너비값->보이는지=첫째값!=0;
    else if(Gníomh==4)너비값->보이는지=0;
    else if(Gníomh==7)너비값->dáileadh_polasaí=첫째값;
    else if(Gníomh==8)return 너비값->fad_VALUE;
    else if(Gníomh==9)return 첫째값>=0&&(unsigned)첫째값<너비값->fad_VALUE?너비값->Téacs[첫째값]:-22;
    else return -22;
    if(이전표시||표시됨(úinéir_oibiacht,너비값))clár_Teirminéal(3);return 0;
}
int 화면글(int úinéir_oibiacht,int aitheantóir_VALUE,const uint32_t *sonraí,unsigned mír_COUNT){giuirléid_staid *너비값=eilimint_VALUE(úinéir_oibiacht,aitheantóir_VALUE);if(!너비값)return -9;if(mír_COUNT>127)return -22;for(unsigned 순번=0;순번<mír_COUNT;순번++){unsigned carachtar_ionchódú=sonraí[순번];if(carachtar_ionchódú>0x10ffff||(carachtar_ionchódú>=0xd800&&carachtar_ionchódú<=0xdfff))return -22;}for(unsigned 순번=0;순번<mír_COUNT;순번++)너비값->Téacs[순번]=sonraí[순번];너비값->fad_VALUE=mír_COUNT;if(표시됨(úinéir_oibiacht,너비값))clár_Teirminéal(3);return 0;}
