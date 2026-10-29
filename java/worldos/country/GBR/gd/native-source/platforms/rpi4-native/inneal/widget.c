#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* Small native peer layer for the explicitly supported Swing subset. */
#include <stdint.h>
#include <stddef.h>
extern uintptr_t bòrd_pel(uintptr_t,uintptr_t,uintptr_t),bòrd_tèirmineal(uintptr_t);
extern void 터미널글자그림(unsigned,unsigned,unsigned,unsigned,unsigned);
extern void *memset(void *,int,size_t);
typedef struct { int roinn_seòrsa_VALUE,부모항목,co_chomharra_x,세로좌표,너비값,높이값,보이는지,de_làimh_co_dhealbhachd,co_dhealbhachd_poileasaidh;unsigned SMS[128],faid_VALUE; } widget_cor;
static widget_cor 요소들[4][32];
static int fòcasaichte[4],tachartas_Liosta[4][16];static unsigned 첫항목[4],cur_a_steach_COUNT[4],부호없는결과[4],긴부호없는값[4];
static void tachartas(int sealbhadair_nì,int VALUE){if(cur_a_steach_COUNT[sealbhadair_nì]<16){tachartas_Liosta[sealbhadair_nì][(첫항목[sealbhadair_nì]+cur_a_steach_COUNT[sealbhadair_nì])%16]=VALUE;cur_a_steach_COUNT[sealbhadair_nì]++;}}
static widget_cor *eileamaid_VALUE(int sealbhadair_nì,int aithnichear_VALUE){return sealbhadair_nì>=0&&sealbhadair_nì<4&&aithnichear_VALUE>0&&aithnichear_VALUE<=32&&요소들[sealbhadair_nì][aithnichear_VALUE-1].roinn_seòrsa_VALUE?&요소들[sealbhadair_nì][aithnichear_VALUE-1]:0;}
static void 사각영역(int co_chomharra_x,int 세로좌표,int 너비값,int 높이값,unsigned 색상){보드사각그림(co_chomharra_x,세로좌표,너비값,높이값,색상);}
int 화면보임(int sealbhadair_nì){if(sealbhadair_nì<0||sealbhadair_nì>=4)return 0;for(int 순번=0;순번<32;순번++)if(요소들[sealbhadair_nì][순번].roinn_seòrsa_VALUE==1&&요소들[sealbhadair_nì][순번].보이는지)return 1;return 0;}
void 화면초기화(int sealbhadair_nì){memset(요소들[sealbhadair_nì],0,sizeof(요소들[sealbhadair_nì]));cur_a_steach_COUNT[sealbhadair_nì]=첫항목[sealbhadair_nì]=fòcasaichte[sealbhadair_nì]=긴부호없는값[sealbhadair_nì]=0;}
static void suidhich(int sealbhadair_nì,widget_cor *너비값,int *co_chomharra_x,int *세로좌표){*co_chomharra_x=너비값->co_chomharra_x;*세로좌표=너비값->세로좌표;int dàta_suidhich=너비값->부모항목;for(int nì_COUNT=0;dàta_suidhich&&nì_COUNT<32;nì_COUNT++){widget_cor *위쪽=eileamaid_VALUE(sealbhadair_nì,dàta_suidhich);if(!위쪽)break;*co_chomharra_x+=위쪽->co_chomharra_x;*세로좌표+=위쪽->세로좌표+(위쪽->roinn_seòrsa_VALUE==1?30:0);dàta_suidhich=위쪽->부모항목;}}
static int 표시됨(int sealbhadair_nì,widget_cor *너비값){for(int nì_COUNT=0;nì_COUNT<32;nì_COUNT++){if(!너비값->보이는지)return 0;if(너비값->roinn_seòrsa_VALUE==1)return 1;너비값=eileamaid_VALUE(sealbhadair_nì,너비값->부모항목);if(!너비값)return 0;}return 0;}
static void SMS(int co_chomharra_x,int 세로좌표,widget_cor *너비값,int 최대값,unsigned 색상,unsigned 배경색){int 현재위치=0;for(unsigned 순번=0;순번<너비값->faid_VALUE;순번++){unsigned caractar_còdachadh=너비값->SMS[순번],너비=caractar_còdachadh>=256?16:8;if(현재위치+(int)너비>최대값)break;터미널글자그림(co_chomharra_x+현재위치,세로좌표,caractar_còdachadh,색상,배경색);현재위치+=너비;}}
void 화면다시그림(int sealbhadair_nì){
    if(!화면보임(sealbhadair_nì))return;
    for(int 처리차례=1;처리차례<=5;처리차례++)for(int 순번=0;순번<32;순번++){
        widget_cor *너비값=&요소들[sealbhadair_nì][순번];if(너비값->roinn_seòrsa_VALUE!=처리차례||!표시됨(sealbhadair_nì,너비값))continue;int co_chomharra_x,세로좌표;suidhich(sealbhadair_nì,너비값,&co_chomharra_x,&세로좌표);
        if(처리차례==1){사각영역(co_chomharra_x,세로좌표,너비값->너비값,너비값->높이값,0xeee9e0);사각영역(co_chomharra_x,세로좌표,너비값->너비값,30,0x905020);SMS(co_chomharra_x+10,세로좌표+7,너비값,너비값->너비값-50,0xffffff,0x905020);사각영역(co_chomharra_x+너비값->너비값-28,세로좌표+4,24,22,0x5555b8);터미널글자그림(co_chomharra_x+너비값->너비값-20,세로좌표+7,'X',0xffffff,0x5555b8);}
        if(처리차례==2)사각영역(co_chomharra_x,세로좌표,너비값->너비값,너비값->높이값,0xeee9e0);
        if(처리차례>=3){unsigned 배경색=처리차례==4?0xc0ab86:처리차례==5?0xffffff:0xeee9e0;if(처리차례!=3)사각영역(co_chomharra_x,세로좌표,너비값->너비값,너비값->높이값,배경색);SMS(co_chomharra_x+4,세로좌표+4,너비값,너비값->너비값-8,0x201a15,배경색);if(처리차례==5&&fòcasaichte[sealbhadair_nì]==순번+1)사각영역(co_chomharra_x,세로좌표+너비값->높이값-2,너비값->너비값,2,0x905020);}
    }
}
int 화면덮음(int sealbhadair_nì,int co_chomharra_x,int 세로좌표){
    if(!화면보임(sealbhadair_nì))return 0;
    for(int 순번=0;순번<32;순번++){
        widget_cor *uinneag=&요소들[sealbhadair_nì][순번];
        if(uinneag->roinn_seòrsa_VALUE==1&&uinneag->보이는지&&co_chomharra_x>=uinneag->co_chomharra_x&&세로좌표>=uinneag->세로좌표&&
           co_chomharra_x<uinneag->co_chomharra_x+uinneag->너비값&&세로좌표<uinneag->세로좌표+uinneag->높이값)return 1;
    }return 0;
}
int 화면가리킴(int sealbhadair_nì,unsigned 눌림,int co_chomharra_x,int 세로좌표){
    if(!화면보임(sealbhadair_nì))return 0;
    if(눌림&1)for(int 순번=31;순번>=0;순번--){widget_cor *너비값=&요소들[sealbhadair_nì][순번];if(!너비값->roinn_seòrsa_VALUE||!표시됨(sealbhadair_nì,너비값))continue;int 창가로,창세로;suidhich(sealbhadair_nì,너비값,&창가로,&창세로);
        if(co_chomharra_x<창가로||세로좌표<창세로||co_chomharra_x>=창가로+너비값->너비값||세로좌표>=창세로+너비값->높이값)continue;
        if(너비값->roinn_seòrsa_VALUE==1&&세로좌표<창세로+30&&co_chomharra_x>=창가로+너비값->너비값-28){if(너비값->co_dhealbhachd_poileasaidh!=0)너비값->보이는지=0;tachartas(sealbhadair_nì,0x10000+순번+1);bòrd_tèirmineal(3);return 1;}
        if(너비값->roinn_seòrsa_VALUE==4){tachartas(sealbhadair_nì,순번+1);return 1;}if(너비값->roinn_seòrsa_VALUE==5){fòcasaichte[sealbhadair_nì]=순번+1;bòrd_tèirmineal(3);return 1;}
        if(너비값->roinn_seòrsa_VALUE==1)return 1;
    }return 0;
}
void 화면누름(int sealbhadair_nì,unsigned SECOND_VALUE){
    widget_cor *너비값=eileamaid_VALUE(sealbhadair_nì,fòcasaichte[sealbhadair_nì]);if(!너비값||너비값->roinn_seòrsa_VALUE!=5)return;
    if(SECOND_VALUE==13||SECOND_VALUE==10){tachartas(sealbhadair_nì,fòcasaichte[sealbhadair_nì]);return;}
    if(SECOND_VALUE==8||SECOND_VALUE==127){if(너비값->faid_VALUE)너비값->faid_VALUE--;긴부호없는값[sealbhadair_nì]=0;}
    else{
        unsigned caractar_còdachadh=SECOND_VALUE;
        if(긴부호없는값[sealbhadair_nì]){if((SECOND_VALUE&192)!=128){긴부호없는값[sealbhadair_nì]=0;return;}부호없는결과[sealbhadair_nì]=(부호없는결과[sealbhadair_nì]<<6)|(SECOND_VALUE&63);if(--긴부호없는값[sealbhadair_nì])return;caractar_còdachadh=부호없는결과[sealbhadair_nì];}
        else if(SECOND_VALUE>=0xc2&&SECOND_VALUE<=0xf4){긴부호없는값[sealbhadair_nì]=SECOND_VALUE<0xe0?1:SECOND_VALUE<0xf0?2:3;부호없는결과[sealbhadair_nì]=SECOND_VALUE&((1u<<(6-긴부호없는값[sealbhadair_nì]))-1);return;}
        else if(SECOND_VALUE<32||SECOND_VALUE>=128)return;
        if(caractar_còdachadh>0x10ffff||(caractar_còdachadh>=0xd800&&caractar_còdachadh<=0xdfff))return;if(너비값->faid_VALUE<127)너비값->SMS[너비값->faid_VALUE++]=caractar_còdachadh;
    }
    bòrd_tèirmineal(3);
}
int 화면호출(int sealbhadair_nì,unsigned Gnìomh,int aithnichear_VALUE,int 첫째값,int SECOND_VALUE,int còd_a_charactair,int ceann_uidhe_dàta){
    if(sealbhadair_nì<0||sealbhadair_nì>=4)return -22;widget_cor *너비값=eileamaid_VALUE(sealbhadair_nì,aithnichear_VALUE);
    if(Gnìomh==0){if(aithnichear_VALUE<1||aithnichear_VALUE>5)return -22;for(int 순번=0;순번<32;순번++)if(요소들[sealbhadair_nì][순번].roinn_seòrsa_VALUE==0){너비값=&요소들[sealbhadair_nì][순번];memset(너비값,0,sizeof(*너비값));너비값->roinn_seòrsa_VALUE=aithnichear_VALUE;너비값->보이는지=aithnichear_VALUE!=1;너비값->너비값=aithnichear_VALUE==1?380:220;너비값->높이값=aithnichear_VALUE==1?240:28;너비값->co_dhealbhachd_poileasaidh=1;너비값->co_chomharra_x=aithnichear_VALUE==1?130:16;너비값->세로좌표=aithnichear_VALUE==1?110:16;return 순번+1;}return -28;}
    if(Gnìomh==5){if(!cur_a_steach_COUNT[sealbhadair_nì])return 0;int 반환값=tachartas_Liosta[sealbhadair_nì][첫항목[sealbhadair_nì]];첫항목[sealbhadair_nì]=(첫항목[sealbhadair_nì]+1)%16;cur_a_steach_COUNT[sealbhadair_nì]--;return 반환값;}
    if(Gnìomh==6)return 화면보임(sealbhadair_nì);
    if(!너비값)return -9;
    int 이전표시=표시됨(sealbhadair_nì,너비값);
    if(Gnìomh==1){int 바탕너비=보드화면너비(),바탕높이=보드화면높이();if(첫째값<0||SECOND_VALUE<0||còd_a_charactair<1||ceann_uidhe_dàta<1||첫째값>바탕너비||SECOND_VALUE>바탕높이||còd_a_charactair>바탕너비-첫째값||ceann_uidhe_dàta>바탕높이-SECOND_VALUE)return -22;너비값->co_chomharra_x=첫째값;너비값->세로좌표=SECOND_VALUE;너비값->너비값=còd_a_charactair;너비값->높이값=ceann_uidhe_dàta;너비값->de_làimh_co_dhealbhachd=1;}
    else if(Gnìomh==2){widget_cor *eileamaid_cloinne=eileamaid_VALUE(sealbhadair_nì,첫째값);if(!eileamaid_cloinne||eileamaid_cloinne==너비값||eileamaid_cloinne->roinn_seòrsa_VALUE==1)return -22;int dàta_suidhich=aithnichear_VALUE;for(int 깊이=0;dàta_suidhich&&깊이<32;깊이++){if(dàta_suidhich==첫째값)return -22;widget_cor *위쪽=eileamaid_VALUE(sealbhadair_nì,dàta_suidhich);dàta_suidhich=위쪽?위쪽->부모항목:0;}eileamaid_cloinne->부모항목=aithnichear_VALUE;if(!eileamaid_cloinne->de_làimh_co_dhealbhachd){int 형제요소=0;for(int 순번=0;순번<32;순번++)if(&요소들[sealbhadair_nì][순번]!=eileamaid_cloinne&&요소들[sealbhadair_nì][순번].부모항목==aithnichear_VALUE)형제요소++;eileamaid_cloinne->세로좌표=16+형제요소*36;}}
    else if(Gnìomh==3)너비값->보이는지=첫째값!=0;
    else if(Gnìomh==4)너비값->보이는지=0;
    else if(Gnìomh==7)너비값->co_dhealbhachd_poileasaidh=첫째값;
    else if(Gnìomh==8)return 너비값->faid_VALUE;
    else if(Gnìomh==9)return 첫째값>=0&&(unsigned)첫째값<너비값->faid_VALUE?너비값->SMS[첫째값]:-22;
    else return -22;
    if(이전표시||표시됨(sealbhadair_nì,너비값))bòrd_tèirmineal(3);return 0;
}
int 화면글(int sealbhadair_nì,int aithnichear_VALUE,const uint32_t *dàta,unsigned nì_COUNT){widget_cor *너비값=eileamaid_VALUE(sealbhadair_nì,aithnichear_VALUE);if(!너비값)return -9;if(nì_COUNT>127)return -22;for(unsigned 순번=0;순번<nì_COUNT;순번++){unsigned caractar_còdachadh=dàta[순번];if(caractar_còdachadh>0x10ffff||(caractar_còdachadh>=0xd800&&caractar_còdachadh<=0xdfff))return -22;}for(unsigned 순번=0;순번<nì_COUNT;순번++)너비값->SMS[순번]=dàta[순번];너비값->faid_VALUE=nì_COUNT;if(표시됨(sealbhadair_nì,너비값))bòrd_tèirmineal(3);return 0;}
