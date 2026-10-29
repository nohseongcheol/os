#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* Small native peer layer for the explicitly supported Swing subset. */
#include <stdint.h>
#include <stddef.h>
extern uintptr_t 보드화소(uintptr_t,uintptr_t,uintptr_t),보드터미널(uintptr_t);
extern void 터미널글자그림(unsigned,unsigned,unsigned,unsigned,unsigned);
extern void *memset(void *,int,size_t);
typedef struct { int ngiir_xëyma,부모항목,rëddu_iks_yi,세로좌표,너비값,높이값,보이는지,téere_leeral_Tëralin,Tëralin_sàrt;unsigned Tekst[128],diir_xëyma; } kifin_nekkin;
static kifin_nekkin 요소들[4][32];
static int Yiñ_fësal[4],xewxew_lim[4][16];static unsigned 첫항목[4],항목수[4],부호없는결과[4],긴부호없는값[4];
static void xewxew(int boroom_yëf,int xëyma){if(항목수[boroom_yëf]<16){xewxew_lim[boroom_yëf][(첫항목[boroom_yëf]+항목수[boroom_yëf])%16]=xëyma;항목수[boroom_yëf]++;}}
static kifin_nekkin *cër_xëyma(int boroom_yëf,int raññeekaay_xëyma){return boroom_yëf>=0&&boroom_yëf<4&&raññeekaay_xëyma>0&&raññeekaay_xëyma<=32&&요소들[boroom_yëf][raññeekaay_xëyma-1].ngiir_xëyma?&요소들[boroom_yëf][raññeekaay_xëyma-1]:0;}
static void 사각영역(int rëddu_iks_yi,int 세로좌표,int 너비값,int 높이값,unsigned 색상){보드사각그림(rëddu_iks_yi,세로좌표,너비값,높이값,색상);}
int 화면보임(int boroom_yëf){if(boroom_yëf<0||boroom_yëf>=4)return 0;for(int 순번=0;순번<32;순번++)if(요소들[boroom_yëf][순번].ngiir_xëyma==1&&요소들[boroom_yëf][순번].보이는지)return 1;return 0;}
void 화면초기화(int boroom_yëf){memset(요소들[boroom_yëf],0,sizeof(요소들[boroom_yëf]));항목수[boroom_yëf]=첫항목[boroom_yëf]=Yiñ_fësal[boroom_yëf]=긴부호없는값[boroom_yëf]=0;}
static void 위치(int boroom_yëf,kifin_nekkin *너비값,int *rëddu_iks_yi,int *세로좌표){*rëddu_iks_yi=너비값->rëddu_iks_yi;*세로좌표=너비값->세로좌표;int 자료위치=너비값->부모항목;for(int 개수=0;자료위치&&개수<32;개수++){kifin_nekkin *위쪽=cër_xëyma(boroom_yëf,자료위치);if(!위쪽)break;*rëddu_iks_yi+=위쪽->rëddu_iks_yi;*세로좌표+=위쪽->세로좌표+(위쪽->ngiir_xëyma==1?30:0);자료위치=위쪽->부모항목;}}
static int 표시됨(int boroom_yëf,kifin_nekkin *너비값){for(int 개수=0;개수<32;개수++){if(!너비값->보이는지)return 0;if(너비값->ngiir_xëyma==1)return 1;너비값=cër_xëyma(boroom_yëf,너비값->부모항목);if(!너비값)return 0;}return 0;}
static void Tekst(int rëddu_iks_yi,int 세로좌표,kifin_nekkin *너비값,int 최대값,unsigned 색상,unsigned 배경색){int 현재위치=0;for(unsigned 순번=0;순번<너비값->diir_xëyma;순번++){unsigned Araf_nëbbin_ci_lim=너비값->Tekst[순번],너비=Araf_nëbbin_ci_lim>=256?16:8;if(현재위치+(int)너비>최대값)break;터미널글자그림(rëddu_iks_yi+현재위치,세로좌표,Araf_nëbbin_ci_lim,색상,배경색);현재위치+=너비;}}
void 화면다시그림(int boroom_yëf){
    if(!화면보임(boroom_yëf))return;
    for(int 처리차례=1;처리차례<=5;처리차례++)for(int 순번=0;순번<32;순번++){
        kifin_nekkin *너비값=&요소들[boroom_yëf][순번];if(너비값->ngiir_xëyma!=처리차례||!표시됨(boroom_yëf,너비값))continue;int rëddu_iks_yi,세로좌표;위치(boroom_yëf,너비값,&rëddu_iks_yi,&세로좌표);
        if(처리차례==1){사각영역(rëddu_iks_yi,세로좌표,너비값->너비값,너비값->높이값,0xeee9e0);사각영역(rëddu_iks_yi,세로좌표,너비값->너비값,30,0x905020);Tekst(rëddu_iks_yi+10,세로좌표+7,너비값,너비값->너비값-50,0xffffff,0x905020);사각영역(rëddu_iks_yi+너비값->너비값-28,세로좌표+4,24,22,0x5555b8);터미널글자그림(rëddu_iks_yi+너비값->너비값-20,세로좌표+7,'X',0xffffff,0x5555b8);}
        if(처리차례==2)사각영역(rëddu_iks_yi,세로좌표,너비값->너비값,너비값->높이값,0xeee9e0);
        if(처리차례>=3){unsigned 배경색=처리차례==4?0xc0ab86:처리차례==5?0xffffff:0xeee9e0;if(처리차례!=3)사각영역(rëddu_iks_yi,세로좌표,너비값->너비값,너비값->높이값,배경색);Tekst(rëddu_iks_yi+4,세로좌표+4,너비값,너비값->너비값-8,0x201a15,배경색);if(처리차례==5&&Yiñ_fësal[boroom_yëf]==순번+1)사각영역(rëddu_iks_yi,세로좌표+너비값->높이값-2,너비값->너비값,2,0x905020);}
    }
}
int 화면덮음(int boroom_yëf,int rëddu_iks_yi,int 세로좌표){
    if(!화면보임(boroom_yëf))return 0;
    for(int 순번=0;순번<32;순번++){
        kifin_nekkin *palanteer=&요소들[boroom_yëf][순번];
        if(palanteer->ngiir_xëyma==1&&palanteer->보이는지&&rëddu_iks_yi>=palanteer->rëddu_iks_yi&&세로좌표>=palanteer->세로좌표&&
           rëddu_iks_yi<palanteer->rëddu_iks_yi+palanteer->너비값&&세로좌표<palanteer->세로좌표+palanteer->높이값)return 1;
    }return 0;
}
int 화면가리킴(int boroom_yëf,unsigned 눌림,int rëddu_iks_yi,int 세로좌표){
    if(!화면보임(boroom_yëf))return 0;
    if(눌림&1)for(int 순번=31;순번>=0;순번--){kifin_nekkin *너비값=&요소들[boroom_yëf][순번];if(!너비값->ngiir_xëyma||!표시됨(boroom_yëf,너비값))continue;int 창가로,창세로;위치(boroom_yëf,너비값,&창가로,&창세로);
        if(rëddu_iks_yi<창가로||세로좌표<창세로||rëddu_iks_yi>=창가로+너비값->너비값||세로좌표>=창세로+너비값->높이값)continue;
        if(너비값->ngiir_xëyma==1&&세로좌표<창세로+30&&rëddu_iks_yi>=창가로+너비값->너비값-28){if(너비값->Tëralin_sàrt!=0)너비값->보이는지=0;xewxew(boroom_yëf,0x10000+순번+1);보드터미널(3);return 1;}
        if(너비값->ngiir_xëyma==4){xewxew(boroom_yëf,순번+1);return 1;}if(너비값->ngiir_xëyma==5){Yiñ_fësal[boroom_yëf]=순번+1;보드터미널(3);return 1;}
        if(너비값->ngiir_xëyma==1)return 1;
    }return 0;
}
void 화면누름(int boroom_yëf,unsigned 둘째값){
    kifin_nekkin *너비값=cër_xëyma(boroom_yëf,Yiñ_fësal[boroom_yëf]);if(!너비값||너비값->ngiir_xëyma!=5)return;
    if(둘째값==13||둘째값==10){xewxew(boroom_yëf,Yiñ_fësal[boroom_yëf]);return;}
    if(둘째값==8||둘째값==127){if(너비값->diir_xëyma)너비값->diir_xëyma--;긴부호없는값[boroom_yëf]=0;}
    else{
        unsigned Araf_nëbbin_ci_lim=둘째값;
        if(긴부호없는값[boroom_yëf]){if((둘째값&192)!=128){긴부호없는값[boroom_yëf]=0;return;}부호없는결과[boroom_yëf]=(부호없는결과[boroom_yëf]<<6)|(둘째값&63);if(--긴부호없는값[boroom_yëf])return;Araf_nëbbin_ci_lim=부호없는결과[boroom_yëf];}
        else if(둘째값>=0xc2&&둘째값<=0xf4){긴부호없는값[boroom_yëf]=둘째값<0xe0?1:둘째값<0xf0?2:3;부호없는결과[boroom_yëf]=둘째값&((1u<<(6-긴부호없는값[boroom_yëf]))-1);return;}
        else if(둘째값<32||둘째값>=128)return;
        if(Araf_nëbbin_ci_lim>0x10ffff||(Araf_nëbbin_ci_lim>=0xd800&&Araf_nëbbin_ci_lim<=0xdfff))return;if(너비값->diir_xëyma<127)너비값->Tekst[너비값->diir_xëyma++]=Araf_nëbbin_ci_lim;
    }
    보드터미널(3);
}
int 화면호출(int boroom_yëf,unsigned jëf,int raññeekaay_xëyma,int 첫째값,int 둘째값,int kotu_araf,int jëmmukaay_mbir){
    if(boroom_yëf<0||boroom_yëf>=4)return -22;kifin_nekkin *너비값=cër_xëyma(boroom_yëf,raññeekaay_xëyma);
    if(jëf==0){if(raññeekaay_xëyma<1||raññeekaay_xëyma>5)return -22;for(int 순번=0;순번<32;순번++)if(요소들[boroom_yëf][순번].ngiir_xëyma==0){너비값=&요소들[boroom_yëf][순번];memset(너비값,0,sizeof(*너비값));너비값->ngiir_xëyma=raññeekaay_xëyma;너비값->보이는지=raññeekaay_xëyma!=1;너비값->너비값=raññeekaay_xëyma==1?380:220;너비값->높이값=raññeekaay_xëyma==1?240:28;너비값->Tëralin_sàrt=1;너비값->rëddu_iks_yi=raññeekaay_xëyma==1?130:16;너비값->세로좌표=raññeekaay_xëyma==1?110:16;return 순번+1;}return -28;}
    if(jëf==5){if(!항목수[boroom_yëf])return 0;int 반환값=xewxew_lim[boroom_yëf][첫항목[boroom_yëf]];첫항목[boroom_yëf]=(첫항목[boroom_yëf]+1)%16;항목수[boroom_yëf]--;return 반환값;}
    if(jëf==6)return 화면보임(boroom_yëf);
    if(!너비값)return -9;
    int 이전표시=표시됨(boroom_yëf,너비값);
    if(jëf==1){int 바탕너비=보드화면너비(),바탕높이=보드화면높이();if(첫째값<0||둘째값<0||kotu_araf<1||jëmmukaay_mbir<1||첫째값>바탕너비||둘째값>바탕높이||kotu_araf>바탕너비-첫째값||jëmmukaay_mbir>바탕높이-둘째값)return -22;너비값->rëddu_iks_yi=첫째값;너비값->세로좌표=둘째값;너비값->너비값=kotu_araf;너비값->높이값=jëmmukaay_mbir;너비값->téere_leeral_Tëralin=1;}
    else if(jëf==2){kifin_nekkin *mujjantalu_toftalin=cër_xëyma(boroom_yëf,첫째값);if(!mujjantalu_toftalin||mujjantalu_toftalin==너비값||mujjantalu_toftalin->ngiir_xëyma==1)return -22;int 자료위치=raññeekaay_xëyma;for(int 깊이=0;자료위치&&깊이<32;깊이++){if(자료위치==첫째값)return -22;kifin_nekkin *위쪽=cër_xëyma(boroom_yëf,자료위치);자료위치=위쪽?위쪽->부모항목:0;}mujjantalu_toftalin->부모항목=raññeekaay_xëyma;if(!mujjantalu_toftalin->téere_leeral_Tëralin){int 형제요소=0;for(int 순번=0;순번<32;순번++)if(&요소들[boroom_yëf][순번]!=mujjantalu_toftalin&&요소들[boroom_yëf][순번].부모항목==raññeekaay_xëyma)형제요소++;mujjantalu_toftalin->세로좌표=16+형제요소*36;}}
    else if(jëf==3)너비값->보이는지=첫째값!=0;
    else if(jëf==4)너비값->보이는지=0;
    else if(jëf==7)너비값->Tëralin_sàrt=첫째값;
    else if(jëf==8)return 너비값->diir_xëyma;
    else if(jëf==9)return 첫째값>=0&&(unsigned)첫째값<너비값->diir_xëyma?너비값->Tekst[첫째값]:-22;
    else return -22;
    if(이전표시||표시됨(boroom_yëf,너비값))보드터미널(3);return 0;
}
int 화면글(int boroom_yëf,int raññeekaay_xëyma,const uint32_t *mbir,unsigned 개수){kifin_nekkin *너비값=cër_xëyma(boroom_yëf,raññeekaay_xëyma);if(!너비값)return -9;if(개수>127)return -22;for(unsigned 순번=0;순번<개수;순번++){unsigned Araf_nëbbin_ci_lim=mbir[순번];if(Araf_nëbbin_ci_lim>0x10ffff||(Araf_nëbbin_ci_lim>=0xd800&&Araf_nëbbin_ci_lim<=0xdfff))return -22;}for(unsigned 순번=0;순번<개수;순번++)너비값->Tekst[순번]=mbir[순번];너비값->diir_xëyma=개수;if(표시됨(boroom_yëf,너비값))보드터미널(3);return 0;}
