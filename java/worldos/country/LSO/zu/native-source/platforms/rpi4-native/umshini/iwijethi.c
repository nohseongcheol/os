#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* Small native peer layer for the explicitly supported Swing subset. */
#include <stdint.h>
#include <stddef.h>
extern uintptr_t 보드화소(uintptr_t,uintptr_t,uintptr_t),보드터미널(uintptr_t);
extern void 터미널글자그림(unsigned,unsigned,unsigned,unsigned,unsigned);
extern void *memset(void *,int,size_t);
typedef struct { int umunxa_inani,부모항목,okuxhumanisa_u_x,세로좌표,너비값,높이값,보이는지,isilandelwa_I_layout,I_layout_inqubomgomo;unsigned Itekisi[128],ubude_inani; } iwijethi_isimo;
static iwijethi_isimo 요소들[4][32];
static int Okugxilile[4],isigameko_Uhlu[4][16];static unsigned 첫항목[4],항목수[4],부호없는결과[4],긴부호없는값[4];
static void isigameko(int umnikazi_into,int inani){if(항목수[umnikazi_into]<16){isigameko_Uhlu[umnikazi_into][(첫항목[umnikazi_into]+항목수[umnikazi_into])%16]=inani;항목수[umnikazi_into]++;}}
static iwijethi_isimo *ilungu_inani(int umnikazi_into,int isivezi_inani){return umnikazi_into>=0&&umnikazi_into<4&&isivezi_inani>0&&isivezi_inani<=32&&요소들[umnikazi_into][isivezi_inani-1].umunxa_inani?&요소들[umnikazi_into][isivezi_inani-1]:0;}
static void 사각영역(int okuxhumanisa_u_x,int 세로좌표,int 너비값,int 높이값,unsigned 색상){보드사각그림(okuxhumanisa_u_x,세로좌표,너비값,높이값,색상);}
int 화면보임(int umnikazi_into){if(umnikazi_into<0||umnikazi_into>=4)return 0;for(int 순번=0;순번<32;순번++)if(요소들[umnikazi_into][순번].umunxa_inani==1&&요소들[umnikazi_into][순번].보이는지)return 1;return 0;}
void 화면초기화(int umnikazi_into){memset(요소들[umnikazi_into],0,sizeof(요소들[umnikazi_into]));항목수[umnikazi_into]=첫항목[umnikazi_into]=Okugxilile[umnikazi_into]=긴부호없는값[umnikazi_into]=0;}
static void 위치(int umnikazi_into,iwijethi_isimo *너비값,int *okuxhumanisa_u_x,int *세로좌표){*okuxhumanisa_u_x=너비값->okuxhumanisa_u_x;*세로좌표=너비값->세로좌표;int 자료위치=너비값->부모항목;for(int 개수=0;자료위치&&개수<32;개수++){iwijethi_isimo *위쪽=ilungu_inani(umnikazi_into,자료위치);if(!위쪽)break;*okuxhumanisa_u_x+=위쪽->okuxhumanisa_u_x;*세로좌표+=위쪽->세로좌표+(위쪽->umunxa_inani==1?30:0);자료위치=위쪽->부모항목;}}
static int 표시됨(int umnikazi_into,iwijethi_isimo *너비값){for(int 개수=0;개수<32;개수++){if(!너비값->보이는지)return 0;if(너비값->umunxa_inani==1)return 1;너비값=ilungu_inani(umnikazi_into,너비값->부모항목);if(!너비값)return 0;}return 0;}
static void Itekisi(int okuxhumanisa_u_x,int 세로좌표,iwijethi_isimo *너비값,int 최대값,unsigned 색상,unsigned 배경색){int 현재위치=0;for(unsigned 순번=0;순번<너비값->ubude_inani;순번++){unsigned uhlamvusimo_ukubhala_ngokufihla=너비값->Itekisi[순번],너비=uhlamvusimo_ukubhala_ngokufihla>=256?16:8;if(현재위치+(int)너비>최대값)break;터미널글자그림(okuxhumanisa_u_x+현재위치,세로좌표,uhlamvusimo_ukubhala_ngokufihla,색상,배경색);현재위치+=너비;}}
void 화면다시그림(int umnikazi_into){
    if(!화면보임(umnikazi_into))return;
    for(int 처리차례=1;처리차례<=5;처리차례++)for(int 순번=0;순번<32;순번++){
        iwijethi_isimo *너비값=&요소들[umnikazi_into][순번];if(너비값->umunxa_inani!=처리차례||!표시됨(umnikazi_into,너비값))continue;int okuxhumanisa_u_x,세로좌표;위치(umnikazi_into,너비값,&okuxhumanisa_u_x,&세로좌표);
        if(처리차례==1){사각영역(okuxhumanisa_u_x,세로좌표,너비값->너비값,너비값->높이값,0xeee9e0);사각영역(okuxhumanisa_u_x,세로좌표,너비값->너비값,30,0x905020);Itekisi(okuxhumanisa_u_x+10,세로좌표+7,너비값,너비값->너비값-50,0xffffff,0x905020);사각영역(okuxhumanisa_u_x+너비값->너비값-28,세로좌표+4,24,22,0x5555b8);터미널글자그림(okuxhumanisa_u_x+너비값->너비값-20,세로좌표+7,'X',0xffffff,0x5555b8);}
        if(처리차례==2)사각영역(okuxhumanisa_u_x,세로좌표,너비값->너비값,너비값->높이값,0xeee9e0);
        if(처리차례>=3){unsigned 배경색=처리차례==4?0xc0ab86:처리차례==5?0xffffff:0xeee9e0;if(처리차례!=3)사각영역(okuxhumanisa_u_x,세로좌표,너비값->너비값,너비값->높이값,배경색);Itekisi(okuxhumanisa_u_x+4,세로좌표+4,너비값,너비값->너비값-8,0x201a15,배경색);if(처리차례==5&&Okugxilile[umnikazi_into]==순번+1)사각영역(okuxhumanisa_u_x,세로좌표+너비값->높이값-2,너비값->너비값,2,0x905020);}
    }
}
int 화면덮음(int umnikazi_into,int okuxhumanisa_u_x,int 세로좌표){
    if(!화면보임(umnikazi_into))return 0;
    for(int 순번=0;순번<32;순번++){
        iwijethi_isimo *ifasitela=&요소들[umnikazi_into][순번];
        if(ifasitela->umunxa_inani==1&&ifasitela->보이는지&&okuxhumanisa_u_x>=ifasitela->okuxhumanisa_u_x&&세로좌표>=ifasitela->세로좌표&&
           okuxhumanisa_u_x<ifasitela->okuxhumanisa_u_x+ifasitela->너비값&&세로좌표<ifasitela->세로좌표+ifasitela->높이값)return 1;
    }return 0;
}
int 화면가리킴(int umnikazi_into,unsigned 눌림,int okuxhumanisa_u_x,int 세로좌표){
    if(!화면보임(umnikazi_into))return 0;
    if(눌림&1)for(int 순번=31;순번>=0;순번--){iwijethi_isimo *너비값=&요소들[umnikazi_into][순번];if(!너비값->umunxa_inani||!표시됨(umnikazi_into,너비값))continue;int 창가로,창세로;위치(umnikazi_into,너비값,&창가로,&창세로);
        if(okuxhumanisa_u_x<창가로||세로좌표<창세로||okuxhumanisa_u_x>=창가로+너비값->너비값||세로좌표>=창세로+너비값->높이값)continue;
        if(너비값->umunxa_inani==1&&세로좌표<창세로+30&&okuxhumanisa_u_x>=창가로+너비값->너비값-28){if(너비값->I_layout_inqubomgomo!=0)너비값->보이는지=0;isigameko(umnikazi_into,0x10000+순번+1);보드터미널(3);return 1;}
        if(너비값->umunxa_inani==4){isigameko(umnikazi_into,순번+1);return 1;}if(너비값->umunxa_inani==5){Okugxilile[umnikazi_into]=순번+1;보드터미널(3);return 1;}
        if(너비값->umunxa_inani==1)return 1;
    }return 0;
}
void 화면누름(int umnikazi_into,unsigned 둘째값){
    iwijethi_isimo *너비값=ilungu_inani(umnikazi_into,Okugxilile[umnikazi_into]);if(!너비값||너비값->umunxa_inani!=5)return;
    if(둘째값==13||둘째값==10){isigameko(umnikazi_into,Okugxilile[umnikazi_into]);return;}
    if(둘째값==8||둘째값==127){if(너비값->ubude_inani)너비값->ubude_inani--;긴부호없는값[umnikazi_into]=0;}
    else{
        unsigned uhlamvusimo_ukubhala_ngokufihla=둘째값;
        if(긴부호없는값[umnikazi_into]){if((둘째값&192)!=128){긴부호없는값[umnikazi_into]=0;return;}부호없는결과[umnikazi_into]=(부호없는결과[umnikazi_into]<<6)|(둘째값&63);if(--긴부호없는값[umnikazi_into])return;uhlamvusimo_ukubhala_ngokufihla=부호없는결과[umnikazi_into];}
        else if(둘째값>=0xc2&&둘째값<=0xf4){긴부호없는값[umnikazi_into]=둘째값<0xe0?1:둘째값<0xf0?2:3;부호없는결과[umnikazi_into]=둘째값&((1u<<(6-긴부호없는값[umnikazi_into]))-1);return;}
        else if(둘째값<32||둘째값>=128)return;
        if(uhlamvusimo_ukubhala_ngokufihla>0x10ffff||(uhlamvusimo_ukubhala_ngokufihla>=0xd800&&uhlamvusimo_ukubhala_ngokufihla<=0xdfff))return;if(너비값->ubude_inani<127)너비값->Itekisi[너비값->ubude_inani++]=uhlamvusimo_ukubhala_ngokufihla;
    }
    보드터미널(3);
}
int 화면호출(int umnikazi_into,unsigned Isenzo,int isivezi_inani,int 첫째값,int 둘째값,int ikhodi_yohlamvu,int isikhumulo_imininingwane){
    if(umnikazi_into<0||umnikazi_into>=4)return -22;iwijethi_isimo *너비값=ilungu_inani(umnikazi_into,isivezi_inani);
    if(Isenzo==0){if(isivezi_inani<1||isivezi_inani>5)return -22;for(int 순번=0;순번<32;순번++)if(요소들[umnikazi_into][순번].umunxa_inani==0){너비값=&요소들[umnikazi_into][순번];memset(너비값,0,sizeof(*너비값));너비값->umunxa_inani=isivezi_inani;너비값->보이는지=isivezi_inani!=1;너비값->너비값=isivezi_inani==1?380:220;너비값->높이값=isivezi_inani==1?240:28;너비값->I_layout_inqubomgomo=1;너비값->okuxhumanisa_u_x=isivezi_inani==1?130:16;너비값->세로좌표=isivezi_inani==1?110:16;return 순번+1;}return -28;}
    if(Isenzo==5){if(!항목수[umnikazi_into])return 0;int 반환값=isigameko_Uhlu[umnikazi_into][첫항목[umnikazi_into]];첫항목[umnikazi_into]=(첫항목[umnikazi_into]+1)%16;항목수[umnikazi_into]--;return 반환값;}
    if(Isenzo==6)return 화면보임(umnikazi_into);
    if(!너비값)return -9;
    int 이전표시=표시됨(umnikazi_into,너비값);
    if(Isenzo==1){int 바탕너비=보드화면너비(),바탕높이=보드화면높이();if(첫째값<0||둘째값<0||ikhodi_yohlamvu<1||isikhumulo_imininingwane<1||첫째값>바탕너비||둘째값>바탕높이||ikhodi_yohlamvu>바탕너비-첫째값||isikhumulo_imininingwane>바탕높이-둘째값)return -22;너비값->okuxhumanisa_u_x=첫째값;너비값->세로좌표=둘째값;너비값->너비값=ikhodi_yohlamvu;너비값->높이값=isikhumulo_imininingwane;너비값->isilandelwa_I_layout=1;}
    else if(Isenzo==2){iwijethi_isimo *ichwane=ilungu_inani(umnikazi_into,첫째값);if(!ichwane||ichwane==너비값||ichwane->umunxa_inani==1)return -22;int 자료위치=isivezi_inani;for(int 깊이=0;자료위치&&깊이<32;깊이++){if(자료위치==첫째값)return -22;iwijethi_isimo *위쪽=ilungu_inani(umnikazi_into,자료위치);자료위치=위쪽?위쪽->부모항목:0;}ichwane->부모항목=isivezi_inani;if(!ichwane->isilandelwa_I_layout){int 형제요소=0;for(int 순번=0;순번<32;순번++)if(&요소들[umnikazi_into][순번]!=ichwane&&요소들[umnikazi_into][순번].부모항목==isivezi_inani)형제요소++;ichwane->세로좌표=16+형제요소*36;}}
    else if(Isenzo==3)너비값->보이는지=첫째값!=0;
    else if(Isenzo==4)너비값->보이는지=0;
    else if(Isenzo==7)너비값->I_layout_inqubomgomo=첫째값;
    else if(Isenzo==8)return 너비값->ubude_inani;
    else if(Isenzo==9)return 첫째값>=0&&(unsigned)첫째값<너비값->ubude_inani?너비값->Itekisi[첫째값]:-22;
    else return -22;
    if(이전표시||표시됨(umnikazi_into,너비값))보드터미널(3);return 0;
}
int 화면글(int umnikazi_into,int isivezi_inani,const uint32_t *imininingwane,unsigned 개수){iwijethi_isimo *너비값=ilungu_inani(umnikazi_into,isivezi_inani);if(!너비값)return -9;if(개수>127)return -22;for(unsigned 순번=0;순번<개수;순번++){unsigned uhlamvusimo_ukubhala_ngokufihla=imininingwane[순번];if(uhlamvusimo_ukubhala_ngokufihla>0x10ffff||(uhlamvusimo_ukubhala_ngokufihla>=0xd800&&uhlamvusimo_ukubhala_ngokufihla<=0xdfff))return -22;}for(unsigned 순번=0;순번<개수;순번++)너비값->Itekisi[순번]=imininingwane[순번];너비값->ubude_inani=개수;if(표시됨(umnikazi_into,너비값))보드터미널(3);return 0;}
