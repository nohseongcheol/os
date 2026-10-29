#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* Small native peer layer for the explicitly supported Swing subset. */
#include <stdint.h>
#include <stddef.h>
extern uintptr_t 보드화소(uintptr_t,uintptr_t,uintptr_t),보드터미널(uintptr_t);
extern void 터미널글자그림(unsigned,unsigned,unsigned,unsigned,unsigned);
extern void *memset(void *,int,size_t);
typedef struct { int kategoriýa_baha,부모항목,x_koordinatasy,세로좌표,너비값,높이값,보이는지,el_bilen_edilýän_Ýerleşiş,Ýerleşiş_syýasat;unsigned Metin[128],dowamlylyk_baha; } wijet_ýagdaý;
static wijet_ýagdaý 요소들[4][32];
static int Fokusly[4],waka_Sanaw[4][16];static unsigned 첫항목[4],항목수[4],부호없는결과[4],긴부호없는값[4];
static void waka(int eýe_obýekt,int baha){if(항목수[eýe_obýekt]<16){waka_Sanaw[eýe_obýekt][(첫항목[eýe_obýekt]+항목수[eýe_obýekt])%16]=baha;항목수[eýe_obýekt]++;}}
static wijet_ýagdaý *element_baha(int eýe_obýekt,int tanaýjy_baha){return eýe_obýekt>=0&&eýe_obýekt<4&&tanaýjy_baha>0&&tanaýjy_baha<=32&&요소들[eýe_obýekt][tanaýjy_baha-1].kategoriýa_baha?&요소들[eýe_obýekt][tanaýjy_baha-1]:0;}
static void 사각영역(int x_koordinatasy,int 세로좌표,int 너비값,int 높이값,unsigned 색상){보드사각그림(x_koordinatasy,세로좌표,너비값,높이값,색상);}
int 화면보임(int eýe_obýekt){if(eýe_obýekt<0||eýe_obýekt>=4)return 0;for(int 순번=0;순번<32;순번++)if(요소들[eýe_obýekt][순번].kategoriýa_baha==1&&요소들[eýe_obýekt][순번].보이는지)return 1;return 0;}
void 화면초기화(int eýe_obýekt){memset(요소들[eýe_obýekt],0,sizeof(요소들[eýe_obýekt]));항목수[eýe_obýekt]=첫항목[eýe_obýekt]=Fokusly[eýe_obýekt]=긴부호없는값[eýe_obýekt]=0;}
static void 위치(int eýe_obýekt,wijet_ýagdaý *너비값,int *x_koordinatasy,int *세로좌표){*x_koordinatasy=너비값->x_koordinatasy;*세로좌표=너비값->세로좌표;int 자료위치=너비값->부모항목;for(int 개수=0;자료위치&&개수<32;개수++){wijet_ýagdaý *위쪽=element_baha(eýe_obýekt,자료위치);if(!위쪽)break;*x_koordinatasy+=위쪽->x_koordinatasy;*세로좌표+=위쪽->세로좌표+(위쪽->kategoriýa_baha==1?30:0);자료위치=위쪽->부모항목;}}
static int 표시됨(int eýe_obýekt,wijet_ýagdaý *너비값){for(int 개수=0;개수<32;개수++){if(!너비값->보이는지)return 0;if(너비값->kategoriýa_baha==1)return 1;너비값=element_baha(eýe_obýekt,너비값->부모항목);if(!너비값)return 0;}return 0;}
static void Metin(int x_koordinatasy,int 세로좌표,wijet_ýagdaý *너비값,int 최대값,unsigned 색상,unsigned 배경색){int 현재위치=0;for(unsigned 순번=0;순번<너비값->dowamlylyk_baha;순번++){unsigned nyşan_kodlaşdyrma=너비값->Metin[순번],너비=nyşan_kodlaşdyrma>=256?16:8;if(현재위치+(int)너비>최대값)break;터미널글자그림(x_koordinatasy+현재위치,세로좌표,nyşan_kodlaşdyrma,색상,배경색);현재위치+=너비;}}
void 화면다시그림(int eýe_obýekt){
    if(!화면보임(eýe_obýekt))return;
    for(int 처리차례=1;처리차례<=5;처리차례++)for(int 순번=0;순번<32;순번++){
        wijet_ýagdaý *너비값=&요소들[eýe_obýekt][순번];if(너비값->kategoriýa_baha!=처리차례||!표시됨(eýe_obýekt,너비값))continue;int x_koordinatasy,세로좌표;위치(eýe_obýekt,너비값,&x_koordinatasy,&세로좌표);
        if(처리차례==1){사각영역(x_koordinatasy,세로좌표,너비값->너비값,너비값->높이값,0xeee9e0);사각영역(x_koordinatasy,세로좌표,너비값->너비값,30,0x905020);Metin(x_koordinatasy+10,세로좌표+7,너비값,너비값->너비값-50,0xffffff,0x905020);사각영역(x_koordinatasy+너비값->너비값-28,세로좌표+4,24,22,0x5555b8);터미널글자그림(x_koordinatasy+너비값->너비값-20,세로좌표+7,'X',0xffffff,0x5555b8);}
        if(처리차례==2)사각영역(x_koordinatasy,세로좌표,너비값->너비값,너비값->높이값,0xeee9e0);
        if(처리차례>=3){unsigned 배경색=처리차례==4?0xc0ab86:처리차례==5?0xffffff:0xeee9e0;if(처리차례!=3)사각영역(x_koordinatasy,세로좌표,너비값->너비값,너비값->높이값,배경색);Metin(x_koordinatasy+4,세로좌표+4,너비값,너비값->너비값-8,0x201a15,배경색);if(처리차례==5&&Fokusly[eýe_obýekt]==순번+1)사각영역(x_koordinatasy,세로좌표+너비값->높이값-2,너비값->너비값,2,0x905020);}
    }
}
int 화면덮음(int eýe_obýekt,int x_koordinatasy,int 세로좌표){
    if(!화면보임(eýe_obýekt))return 0;
    for(int 순번=0;순번<32;순번++){
        wijet_ýagdaý *penjire=&요소들[eýe_obýekt][순번];
        if(penjire->kategoriýa_baha==1&&penjire->보이는지&&x_koordinatasy>=penjire->x_koordinatasy&&세로좌표>=penjire->세로좌표&&
           x_koordinatasy<penjire->x_koordinatasy+penjire->너비값&&세로좌표<penjire->세로좌표+penjire->높이값)return 1;
    }return 0;
}
int 화면가리킴(int eýe_obýekt,unsigned 눌림,int x_koordinatasy,int 세로좌표){
    if(!화면보임(eýe_obýekt))return 0;
    if(눌림&1)for(int 순번=31;순번>=0;순번--){wijet_ýagdaý *너비값=&요소들[eýe_obýekt][순번];if(!너비값->kategoriýa_baha||!표시됨(eýe_obýekt,너비값))continue;int 창가로,창세로;위치(eýe_obýekt,너비값,&창가로,&창세로);
        if(x_koordinatasy<창가로||세로좌표<창세로||x_koordinatasy>=창가로+너비값->너비값||세로좌표>=창세로+너비값->높이값)continue;
        if(너비값->kategoriýa_baha==1&&세로좌표<창세로+30&&x_koordinatasy>=창가로+너비값->너비값-28){if(너비값->Ýerleşiş_syýasat!=0)너비값->보이는지=0;waka(eýe_obýekt,0x10000+순번+1);보드터미널(3);return 1;}
        if(너비값->kategoriýa_baha==4){waka(eýe_obýekt,순번+1);return 1;}if(너비값->kategoriýa_baha==5){Fokusly[eýe_obýekt]=순번+1;보드터미널(3);return 1;}
        if(너비값->kategoriýa_baha==1)return 1;
    }return 0;
}
void 화면누름(int eýe_obýekt,unsigned 둘째값){
    wijet_ýagdaý *너비값=element_baha(eýe_obýekt,Fokusly[eýe_obýekt]);if(!너비값||너비값->kategoriýa_baha!=5)return;
    if(둘째값==13||둘째값==10){waka(eýe_obýekt,Fokusly[eýe_obýekt]);return;}
    if(둘째값==8||둘째값==127){if(너비값->dowamlylyk_baha)너비값->dowamlylyk_baha--;긴부호없는값[eýe_obýekt]=0;}
    else{
        unsigned nyşan_kodlaşdyrma=둘째값;
        if(긴부호없는값[eýe_obýekt]){if((둘째값&192)!=128){긴부호없는값[eýe_obýekt]=0;return;}부호없는결과[eýe_obýekt]=(부호없는결과[eýe_obýekt]<<6)|(둘째값&63);if(--긴부호없는값[eýe_obýekt])return;nyşan_kodlaşdyrma=부호없는결과[eýe_obýekt];}
        else if(둘째값>=0xc2&&둘째값<=0xf4){긴부호없는값[eýe_obýekt]=둘째값<0xe0?1:둘째값<0xf0?2:3;부호없는결과[eýe_obýekt]=둘째값&((1u<<(6-긴부호없는값[eýe_obýekt]))-1);return;}
        else if(둘째값<32||둘째값>=128)return;
        if(nyşan_kodlaşdyrma>0x10ffff||(nyşan_kodlaşdyrma>=0xd800&&nyşan_kodlaşdyrma<=0xdfff))return;if(너비값->dowamlylyk_baha<127)너비값->Metin[너비값->dowamlylyk_baha++]=nyşan_kodlaşdyrma;
    }
    보드터미널(3);
}
int 화면호출(int eýe_obýekt,unsigned iş,int tanaýjy_baha,int 첫째값,int 둘째값,int nyşanyň_kody,int barylmaly_ýer_maglumat){
    if(eýe_obýekt<0||eýe_obýekt>=4)return -22;wijet_ýagdaý *너비값=element_baha(eýe_obýekt,tanaýjy_baha);
    if(iş==0){if(tanaýjy_baha<1||tanaýjy_baha>5)return -22;for(int 순번=0;순번<32;순번++)if(요소들[eýe_obýekt][순번].kategoriýa_baha==0){너비값=&요소들[eýe_obýekt][순번];memset(너비값,0,sizeof(*너비값));너비값->kategoriýa_baha=tanaýjy_baha;너비값->보이는지=tanaýjy_baha!=1;너비값->너비값=tanaýjy_baha==1?380:220;너비값->높이값=tanaýjy_baha==1?240:28;너비값->Ýerleşiş_syýasat=1;너비값->x_koordinatasy=tanaýjy_baha==1?130:16;너비값->세로좌표=tanaýjy_baha==1?110:16;return 순번+1;}return -28;}
    if(iş==5){if(!항목수[eýe_obýekt])return 0;int 반환값=waka_Sanaw[eýe_obýekt][첫항목[eýe_obýekt]];첫항목[eýe_obýekt]=(첫항목[eýe_obýekt]+1)%16;항목수[eýe_obýekt]--;return 반환값;}
    if(iş==6)return 화면보임(eýe_obýekt);
    if(!너비값)return -9;
    int 이전표시=표시됨(eýe_obýekt,너비값);
    if(iş==1){int 바탕너비=보드화면너비(),바탕높이=보드화면높이();if(첫째값<0||둘째값<0||nyşanyň_kody<1||barylmaly_ýer_maglumat<1||첫째값>바탕너비||둘째값>바탕높이||nyşanyň_kody>바탕너비-첫째값||barylmaly_ýer_maglumat>바탕높이-둘째값)return -22;너비값->x_koordinatasy=첫째값;너비값->세로좌표=둘째값;너비값->너비값=nyşanyň_kody;너비값->높이값=barylmaly_ýer_maglumat;너비값->el_bilen_edilýän_Ýerleşiş=1;}
    else if(iş==2){wijet_ýagdaý *tabyn_element=element_baha(eýe_obýekt,첫째값);if(!tabyn_element||tabyn_element==너비값||tabyn_element->kategoriýa_baha==1)return -22;int 자료위치=tanaýjy_baha;for(int 깊이=0;자료위치&&깊이<32;깊이++){if(자료위치==첫째값)return -22;wijet_ýagdaý *위쪽=element_baha(eýe_obýekt,자료위치);자료위치=위쪽?위쪽->부모항목:0;}tabyn_element->부모항목=tanaýjy_baha;if(!tabyn_element->el_bilen_edilýän_Ýerleşiş){int 형제요소=0;for(int 순번=0;순번<32;순번++)if(&요소들[eýe_obýekt][순번]!=tabyn_element&&요소들[eýe_obýekt][순번].부모항목==tanaýjy_baha)형제요소++;tabyn_element->세로좌표=16+형제요소*36;}}
    else if(iş==3)너비값->보이는지=첫째값!=0;
    else if(iş==4)너비값->보이는지=0;
    else if(iş==7)너비값->Ýerleşiş_syýasat=첫째값;
    else if(iş==8)return 너비값->dowamlylyk_baha;
    else if(iş==9)return 첫째값>=0&&(unsigned)첫째값<너비값->dowamlylyk_baha?너비값->Metin[첫째값]:-22;
    else return -22;
    if(이전표시||표시됨(eýe_obýekt,너비값))보드터미널(3);return 0;
}
int 화면글(int eýe_obýekt,int tanaýjy_baha,const uint32_t *maglumat,unsigned 개수){wijet_ýagdaý *너비값=element_baha(eýe_obýekt,tanaýjy_baha);if(!너비값)return -9;if(개수>127)return -22;for(unsigned 순번=0;순번<개수;순번++){unsigned nyşan_kodlaşdyrma=maglumat[순번];if(nyşan_kodlaşdyrma>0x10ffff||(nyşan_kodlaşdyrma>=0xd800&&nyşan_kodlaşdyrma<=0xdfff))return -22;}for(unsigned 순번=0;순번<개수;순번++)너비값->Metin[순번]=maglumat[순번];너비값->dowamlylyk_baha=개수;if(표시됨(eýe_obýekt,너비값))보드터미널(3);return 0;}
