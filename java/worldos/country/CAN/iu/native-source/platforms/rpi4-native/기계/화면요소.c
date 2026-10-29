#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* Small native peer layer for the explicitly supported Swing subset. */
#include <stdint.h>
#include <stddef.h>
extern uintptr_t 보드화소(uintptr_t,uintptr_t,uintptr_t),보드터미널(uintptr_t);
extern void 터미널글자그림(unsigned,unsigned,unsigned,unsigned,unsigned);
extern void *memset(void *,int,size_t);
typedef struct { int Ataqatigiivvik_atuutilik,부모항목,가로좌표,세로좌표,너비값,높이값,보이는지,namminiq_kamagilugu_ilinganinga,배치정책;unsigned titiqqaq[128],takininga_atuutilik; } 화면요소상태;
static 화면요소상태 요소들[4][32];
static int 초점요소[4],piniku_Titiqpalliagaq[4][16];static unsigned 첫항목[4],항목수[4],부호없는결과[4],긴부호없는값[4];
static void piniku(int 소유자,int atuutilik){if(항목수[소유자]<16){piniku_Titiqpalliagaq[소유자][(첫항목[소유자]+항목수[소유자])%16]=atuutilik;항목수[소유자]++;}}
static 화면요소상태 *ilanga_atuutilik(int 소유자,int 식별자){return 소유자>=0&&소유자<4&&식별자>0&&식별자<=32&&요소들[소유자][식별자-1].Ataqatigiivvik_atuutilik?&요소들[소유자][식별자-1]:0;}
static void 사각영역(int 가로좌표,int 세로좌표,int 너비값,int 높이값,unsigned 색상){보드사각그림(가로좌표,세로좌표,너비값,높이값,색상);}
int 화면보임(int 소유자){if(소유자<0||소유자>=4)return 0;for(int 순번=0;순번<32;순번++)if(요소들[소유자][순번].Ataqatigiivvik_atuutilik==1&&요소들[소유자][순번].보이는지)return 1;return 0;}
void 화면초기화(int 소유자){memset(요소들[소유자],0,sizeof(요소들[소유자]));항목수[소유자]=첫항목[소유자]=초점요소[소유자]=긴부호없는값[소유자]=0;}
static void 위치(int 소유자,화면요소상태 *너비값,int *가로좌표,int *세로좌표){*가로좌표=너비값->가로좌표;*세로좌표=너비값->세로좌표;int 자료위치=너비값->부모항목;for(int 개수=0;자료위치&&개수<32;개수++){화면요소상태 *위쪽=ilanga_atuutilik(소유자,자료위치);if(!위쪽)break;*가로좌표+=위쪽->가로좌표;*세로좌표+=위쪽->세로좌표+(위쪽->Ataqatigiivvik_atuutilik==1?30:0);자료위치=위쪽->부모항목;}}
static int 표시됨(int 소유자,화면요소상태 *너비값){for(int 개수=0;개수<32;개수++){if(!너비값->보이는지)return 0;if(너비값->Ataqatigiivvik_atuutilik==1)return 1;너비값=ilanga_atuutilik(소유자,너비값->부모항목);if(!너비값)return 0;}return 0;}
static void titiqqaq(int 가로좌표,int 세로좌표,화면요소상태 *너비값,int 최대값,unsigned 색상,unsigned 배경색){int 현재위치=0;for(unsigned 순번=0;순번<너비값->takininga_atuutilik;순번++){unsigned immikkuuqtuq_tukiniktiri=너비값->titiqqaq[순번],너비=immikkuuqtuq_tukiniktiri>=256?16:8;if(현재위치+(int)너비>최대값)break;터미널글자그림(가로좌표+현재위치,세로좌표,immikkuuqtuq_tukiniktiri,색상,배경색);현재위치+=너비;}}
void 화면다시그림(int 소유자){
    if(!화면보임(소유자))return;
    for(int 처리차례=1;처리차례<=5;처리차례++)for(int 순번=0;순번<32;순번++){
        화면요소상태 *너비값=&요소들[소유자][순번];if(너비값->Ataqatigiivvik_atuutilik!=처리차례||!표시됨(소유자,너비값))continue;int 가로좌표,세로좌표;위치(소유자,너비값,&가로좌표,&세로좌표);
        if(처리차례==1){사각영역(가로좌표,세로좌표,너비값->너비값,너비값->높이값,0xeee9e0);사각영역(가로좌표,세로좌표,너비값->너비값,30,0x905020);titiqqaq(가로좌표+10,세로좌표+7,너비값,너비값->너비값-50,0xffffff,0x905020);사각영역(가로좌표+너비값->너비값-28,세로좌표+4,24,22,0x5555b8);터미널글자그림(가로좌표+너비값->너비값-20,세로좌표+7,'X',0xffffff,0x5555b8);}
        if(처리차례==2)사각영역(가로좌표,세로좌표,너비값->너비값,너비값->높이값,0xeee9e0);
        if(처리차례>=3){unsigned 배경색=처리차례==4?0xc0ab86:처리차례==5?0xffffff:0xeee9e0;if(처리차례!=3)사각영역(가로좌표,세로좌표,너비값->너비값,너비값->높이값,배경색);titiqqaq(가로좌표+4,세로좌표+4,너비값,너비값->너비값-8,0x201a15,배경색);if(처리차례==5&&초점요소[소유자]==순번+1)사각영역(가로좌표,세로좌표+너비값->높이값-2,너비값->너비값,2,0x905020);}
    }
}
int 화면덮음(int 소유자,int 가로좌표,int 세로좌표){
    if(!화면보임(소유자))return 0;
    for(int 순번=0;순번<32;순번++){
        화면요소상태 *igalaangujaq=&요소들[소유자][순번];
        if(igalaangujaq->Ataqatigiivvik_atuutilik==1&&igalaangujaq->보이는지&&가로좌표>=igalaangujaq->가로좌표&&세로좌표>=igalaangujaq->세로좌표&&
           가로좌표<igalaangujaq->가로좌표+igalaangujaq->너비값&&세로좌표<igalaangujaq->세로좌표+igalaangujaq->높이값)return 1;
    }return 0;
}
int 화면가리킴(int 소유자,unsigned 눌림,int 가로좌표,int 세로좌표){
    if(!화면보임(소유자))return 0;
    if(눌림&1)for(int 순번=31;순번>=0;순번--){화면요소상태 *너비값=&요소들[소유자][순번];if(!너비값->Ataqatigiivvik_atuutilik||!표시됨(소유자,너비값))continue;int 창가로,창세로;위치(소유자,너비값,&창가로,&창세로);
        if(가로좌표<창가로||세로좌표<창세로||가로좌표>=창가로+너비값->너비값||세로좌표>=창세로+너비값->높이값)continue;
        if(너비값->Ataqatigiivvik_atuutilik==1&&세로좌표<창세로+30&&가로좌표>=창가로+너비값->너비값-28){if(너비값->배치정책!=0)너비값->보이는지=0;piniku(소유자,0x10000+순번+1);보드터미널(3);return 1;}
        if(너비값->Ataqatigiivvik_atuutilik==4){piniku(소유자,순번+1);return 1;}if(너비값->Ataqatigiivvik_atuutilik==5){초점요소[소유자]=순번+1;보드터미널(3);return 1;}
        if(너비값->Ataqatigiivvik_atuutilik==1)return 1;
    }return 0;
}
void 화면누름(int 소유자,unsigned 둘째값){
    화면요소상태 *너비값=ilanga_atuutilik(소유자,초점요소[소유자]);if(!너비값||너비값->Ataqatigiivvik_atuutilik!=5)return;
    if(둘째값==13||둘째값==10){piniku(소유자,초점요소[소유자]);return;}
    if(둘째값==8||둘째값==127){if(너비값->takininga_atuutilik)너비값->takininga_atuutilik--;긴부호없는값[소유자]=0;}
    else{
        unsigned immikkuuqtuq_tukiniktiri=둘째값;
        if(긴부호없는값[소유자]){if((둘째값&192)!=128){긴부호없는값[소유자]=0;return;}부호없는결과[소유자]=(부호없는결과[소유자]<<6)|(둘째값&63);if(--긴부호없는값[소유자])return;immikkuuqtuq_tukiniktiri=부호없는결과[소유자];}
        else if(둘째값>=0xc2&&둘째값<=0xf4){긴부호없는값[소유자]=둘째값<0xe0?1:둘째값<0xf0?2:3;부호없는결과[소유자]=둘째값&((1u<<(6-긴부호없는값[소유자]))-1);return;}
        else if(둘째값<32||둘째값>=128)return;
        if(immikkuuqtuq_tukiniktiri>0x10ffff||(immikkuuqtuq_tukiniktiri>=0xd800&&immikkuuqtuq_tukiniktiri<=0xdfff))return;if(너비값->takininga_atuutilik<127)너비값->titiqqaq[너비값->takininga_atuutilik++]=immikkuuqtuq_tukiniktiri;
    }
    보드터미널(3);
}
int 화면호출(int 소유자,unsigned sugiarut,int 식별자,int 첫째값,int 둘째값,int immikkuuqtumut_nalunaikkut,int namunngarvik_titiqqat){
    if(소유자<0||소유자>=4)return -22;화면요소상태 *너비값=ilanga_atuutilik(소유자,식별자);
    if(sugiarut==0){if(식별자<1||식별자>5)return -22;for(int 순번=0;순번<32;순번++)if(요소들[소유자][순번].Ataqatigiivvik_atuutilik==0){너비값=&요소들[소유자][순번];memset(너비값,0,sizeof(*너비값));너비값->Ataqatigiivvik_atuutilik=식별자;너비값->보이는지=식별자!=1;너비값->너비값=식별자==1?380:220;너비값->높이값=식별자==1?240:28;너비값->배치정책=1;너비값->가로좌표=식별자==1?130:16;너비값->세로좌표=식별자==1?110:16;return 순번+1;}return -28;}
    if(sugiarut==5){if(!항목수[소유자])return 0;int 반환값=piniku_Titiqpalliagaq[소유자][첫항목[소유자]];첫항목[소유자]=(첫항목[소유자]+1)%16;항목수[소유자]--;return 반환값;}
    if(sugiarut==6)return 화면보임(소유자);
    if(!너비값)return -9;
    int 이전표시=표시됨(소유자,너비값);
    if(sugiarut==1){int 바탕너비=보드화면너비(),바탕높이=보드화면높이();if(첫째값<0||둘째값<0||immikkuuqtumut_nalunaikkut<1||namunngarvik_titiqqat<1||첫째값>바탕너비||둘째값>바탕높이||immikkuuqtumut_nalunaikkut>바탕너비-첫째값||namunngarvik_titiqqat>바탕높이-둘째값)return -22;너비값->가로좌표=첫째값;너비값->세로좌표=둘째값;너비값->너비값=immikkuuqtumut_nalunaikkut;너비값->높이값=namunngarvik_titiqqat;너비값->namminiq_kamagilugu_ilinganinga=1;}
    else if(sugiarut==2){화면요소상태 *atavilik=ilanga_atuutilik(소유자,첫째값);if(!atavilik||atavilik==너비값||atavilik->Ataqatigiivvik_atuutilik==1)return -22;int 자료위치=식별자;for(int 깊이=0;자료위치&&깊이<32;깊이++){if(자료위치==첫째값)return -22;화면요소상태 *위쪽=ilanga_atuutilik(소유자,자료위치);자료위치=위쪽?위쪽->부모항목:0;}atavilik->부모항목=식별자;if(!atavilik->namminiq_kamagilugu_ilinganinga){int 형제요소=0;for(int 순번=0;순번<32;순번++)if(&요소들[소유자][순번]!=atavilik&&요소들[소유자][순번].부모항목==식별자)형제요소++;atavilik->세로좌표=16+형제요소*36;}}
    else if(sugiarut==3)너비값->보이는지=첫째값!=0;
    else if(sugiarut==4)너비값->보이는지=0;
    else if(sugiarut==7)너비값->배치정책=첫째값;
    else if(sugiarut==8)return 너비값->takininga_atuutilik;
    else if(sugiarut==9)return 첫째값>=0&&(unsigned)첫째값<너비값->takininga_atuutilik?너비값->titiqqaq[첫째값]:-22;
    else return -22;
    if(이전표시||표시됨(소유자,너비값))보드터미널(3);return 0;
}
int 화면글(int 소유자,int 식별자,const uint32_t *titiqqat,unsigned 개수){화면요소상태 *너비값=ilanga_atuutilik(소유자,식별자);if(!너비값)return -9;if(개수>127)return -22;for(unsigned 순번=0;순번<개수;순번++){unsigned immikkuuqtuq_tukiniktiri=titiqqat[순번];if(immikkuuqtuq_tukiniktiri>0x10ffff||(immikkuuqtuq_tukiniktiri>=0xd800&&immikkuuqtuq_tukiniktiri<=0xdfff))return -22;}for(unsigned 순번=0;순번<개수;순번++)너비값->titiqqaq[순번]=titiqqat[순번];너비값->takininga_atuutilik=개수;if(표시됨(소유자,너비값))보드터미널(3);return 0;}
