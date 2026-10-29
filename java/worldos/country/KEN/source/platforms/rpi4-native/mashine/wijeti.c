#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* Small native peer layer for the explicitly supported Swing subset. */
#include <stdint.h>
#include <stddef.h>
extern uintptr_t 보드화소(uintptr_t,uintptr_t,uintptr_t),보드터미널(uintptr_t);
extern void 터미널글자그림(unsigned,unsigned,unsigned,unsigned,unsigned);
extern void *memset(void *,int,size_t);
typedef struct { int kategoria_thamani,부모항목,jira_x,Kitufe_cha_Y_kiratibu,너비값,높이값,보이는지,a_mikono_Muundo,Muundo_sera;unsigned SMS[128],urefu_thamani; } wijeti_hali;
static wijeti_hali 요소들[4][32];
static int Lengwa[4],tukio_Orodha[4][16];static unsigned 첫항목[4],항목수[4],부호없는결과[4],긴부호없는값[4];
static void tukio(int mmiliki_kipengee,int thamani){if(항목수[mmiliki_kipengee]<16){tukio_Orodha[mmiliki_kipengee][(첫항목[mmiliki_kipengee]+항목수[mmiliki_kipengee])%16]=thamani;항목수[mmiliki_kipengee]++;}}
static wijeti_hali *elementi_thamani(int mmiliki_kipengee,int kitambulishi_thamani){return mmiliki_kipengee>=0&&mmiliki_kipengee<4&&kitambulishi_thamani>0&&kitambulishi_thamani<=32&&요소들[mmiliki_kipengee][kitambulishi_thamani-1].kategoria_thamani?&요소들[mmiliki_kipengee][kitambulishi_thamani-1]:0;}
static void 사각영역(int jira_x,int Kitufe_cha_Y_kiratibu,int 너비값,int 높이값,unsigned 색상){보드사각그림(jira_x,Kitufe_cha_Y_kiratibu,너비값,높이값,색상);}
int 화면보임(int mmiliki_kipengee){if(mmiliki_kipengee<0||mmiliki_kipengee>=4)return 0;for(int 순번=0;순번<32;순번++)if(요소들[mmiliki_kipengee][순번].kategoria_thamani==1&&요소들[mmiliki_kipengee][순번].보이는지)return 1;return 0;}
void 화면초기화(int mmiliki_kipengee){memset(요소들[mmiliki_kipengee],0,sizeof(요소들[mmiliki_kipengee]));항목수[mmiliki_kipengee]=첫항목[mmiliki_kipengee]=Lengwa[mmiliki_kipengee]=긴부호없는값[mmiliki_kipengee]=0;}
static void 위치(int mmiliki_kipengee,wijeti_hali *너비값,int *jira_x,int *Kitufe_cha_Y_kiratibu){*jira_x=너비값->jira_x;*Kitufe_cha_Y_kiratibu=너비값->Kitufe_cha_Y_kiratibu;int 자료위치=너비값->부모항목;for(int 개수=0;자료위치&&개수<32;개수++){wijeti_hali *위쪽=elementi_thamani(mmiliki_kipengee,자료위치);if(!위쪽)break;*jira_x+=위쪽->jira_x;*Kitufe_cha_Y_kiratibu+=위쪽->Kitufe_cha_Y_kiratibu+(위쪽->kategoria_thamani==1?30:0);자료위치=위쪽->부모항목;}}
static int 표시됨(int mmiliki_kipengee,wijeti_hali *너비값){for(int 개수=0;개수<32;개수++){if(!너비값->보이는지)return 0;if(너비값->kategoria_thamani==1)return 1;너비값=elementi_thamani(mmiliki_kipengee,너비값->부모항목);if(!너비값)return 0;}return 0;}
static void SMS(int jira_x,int Kitufe_cha_Y_kiratibu,wijeti_hali *너비값,int 최대값,unsigned 색상,unsigned 배경색){int 현재위치=0;for(unsigned 순번=0;순번<너비값->urefu_thamani;순번++){unsigned kibambo_usimbaji=너비값->SMS[순번],너비=kibambo_usimbaji>=256?16:8;if(현재위치+(int)너비>최대값)break;터미널글자그림(jira_x+현재위치,Kitufe_cha_Y_kiratibu,kibambo_usimbaji,색상,배경색);현재위치+=너비;}}
void 화면다시그림(int mmiliki_kipengee){
    if(!화면보임(mmiliki_kipengee))return;
    for(int 처리차례=1;처리차례<=5;처리차례++)for(int 순번=0;순번<32;순번++){
        wijeti_hali *너비값=&요소들[mmiliki_kipengee][순번];if(너비값->kategoria_thamani!=처리차례||!표시됨(mmiliki_kipengee,너비값))continue;int jira_x,Kitufe_cha_Y_kiratibu;위치(mmiliki_kipengee,너비값,&jira_x,&Kitufe_cha_Y_kiratibu);
        if(처리차례==1){사각영역(jira_x,Kitufe_cha_Y_kiratibu,너비값->너비값,너비값->높이값,0xeee9e0);사각영역(jira_x,Kitufe_cha_Y_kiratibu,너비값->너비값,30,0x905020);SMS(jira_x+10,Kitufe_cha_Y_kiratibu+7,너비값,너비값->너비값-50,0xffffff,0x905020);사각영역(jira_x+너비값->너비값-28,Kitufe_cha_Y_kiratibu+4,24,22,0x5555b8);터미널글자그림(jira_x+너비값->너비값-20,Kitufe_cha_Y_kiratibu+7,'X',0xffffff,0x5555b8);}
        if(처리차례==2)사각영역(jira_x,Kitufe_cha_Y_kiratibu,너비값->너비값,너비값->높이값,0xeee9e0);
        if(처리차례>=3){unsigned 배경색=처리차례==4?0xc0ab86:처리차례==5?0xffffff:0xeee9e0;if(처리차례!=3)사각영역(jira_x,Kitufe_cha_Y_kiratibu,너비값->너비값,너비값->높이값,배경색);SMS(jira_x+4,Kitufe_cha_Y_kiratibu+4,너비값,너비값->너비값-8,0x201a15,배경색);if(처리차례==5&&Lengwa[mmiliki_kipengee]==순번+1)사각영역(jira_x,Kitufe_cha_Y_kiratibu+너비값->높이값-2,너비값->너비값,2,0x905020);}
    }
}
int 화면덮음(int mmiliki_kipengee,int jira_x,int Kitufe_cha_Y_kiratibu){
    if(!화면보임(mmiliki_kipengee))return 0;
    for(int 순번=0;순번<32;순번++){
        wijeti_hali *dirisha=&요소들[mmiliki_kipengee][순번];
        if(dirisha->kategoria_thamani==1&&dirisha->보이는지&&jira_x>=dirisha->jira_x&&Kitufe_cha_Y_kiratibu>=dirisha->Kitufe_cha_Y_kiratibu&&
           jira_x<dirisha->jira_x+dirisha->너비값&&Kitufe_cha_Y_kiratibu<dirisha->Kitufe_cha_Y_kiratibu+dirisha->높이값)return 1;
    }return 0;
}
int 화면가리킴(int mmiliki_kipengee,unsigned 눌림,int jira_x,int Kitufe_cha_Y_kiratibu){
    if(!화면보임(mmiliki_kipengee))return 0;
    if(눌림&1)for(int 순번=31;순번>=0;순번--){wijeti_hali *너비값=&요소들[mmiliki_kipengee][순번];if(!너비값->kategoria_thamani||!표시됨(mmiliki_kipengee,너비값))continue;int dirisha_Kitufe_cha_X,dirisha_Kitufe_cha_Y;위치(mmiliki_kipengee,너비값,&dirisha_Kitufe_cha_X,&dirisha_Kitufe_cha_Y);
        if(jira_x<dirisha_Kitufe_cha_X||Kitufe_cha_Y_kiratibu<dirisha_Kitufe_cha_Y||jira_x>=dirisha_Kitufe_cha_X+너비값->너비값||Kitufe_cha_Y_kiratibu>=dirisha_Kitufe_cha_Y+너비값->높이값)continue;
        if(너비값->kategoria_thamani==1&&Kitufe_cha_Y_kiratibu<dirisha_Kitufe_cha_Y+30&&jira_x>=dirisha_Kitufe_cha_X+너비값->너비값-28){if(너비값->Muundo_sera!=0)너비값->보이는지=0;tukio(mmiliki_kipengee,0x10000+순번+1);보드터미널(3);return 1;}
        if(너비값->kategoria_thamani==4){tukio(mmiliki_kipengee,순번+1);return 1;}if(너비값->kategoria_thamani==5){Lengwa[mmiliki_kipengee]=순번+1;보드터미널(3);return 1;}
        if(너비값->kategoria_thamani==1)return 1;
    }return 0;
}
void 화면누름(int mmiliki_kipengee,unsigned 둘째값){
    wijeti_hali *너비값=elementi_thamani(mmiliki_kipengee,Lengwa[mmiliki_kipengee]);if(!너비값||너비값->kategoria_thamani!=5)return;
    if(둘째값==13||둘째값==10){tukio(mmiliki_kipengee,Lengwa[mmiliki_kipengee]);return;}
    if(둘째값==8||둘째값==127){if(너비값->urefu_thamani)너비값->urefu_thamani--;긴부호없는값[mmiliki_kipengee]=0;}
    else{
        unsigned kibambo_usimbaji=둘째값;
        if(긴부호없는값[mmiliki_kipengee]){if((둘째값&192)!=128){긴부호없는값[mmiliki_kipengee]=0;return;}부호없는결과[mmiliki_kipengee]=(부호없는결과[mmiliki_kipengee]<<6)|(둘째값&63);if(--긴부호없는값[mmiliki_kipengee])return;kibambo_usimbaji=부호없는결과[mmiliki_kipengee];}
        else if(둘째값>=0xc2&&둘째값<=0xf4){긴부호없는값[mmiliki_kipengee]=둘째값<0xe0?1:둘째값<0xf0?2:3;부호없는결과[mmiliki_kipengee]=둘째값&((1u<<(6-긴부호없는값[mmiliki_kipengee]))-1);return;}
        else if(둘째값<32||둘째값>=128)return;
        if(kibambo_usimbaji>0x10ffff||(kibambo_usimbaji>=0xd800&&kibambo_usimbaji<=0xdfff))return;if(너비값->urefu_thamani<127)너비값->SMS[너비값->urefu_thamani++]=kibambo_usimbaji;
    }
    보드터미널(3);
}
int 화면호출(int mmiliki_kipengee,unsigned Kitendo,int kitambulishi_thamani,int 첫째값,int 둘째값,int msimbo_wa_kibambo,int fikio_data){
    if(mmiliki_kipengee<0||mmiliki_kipengee>=4)return -22;wijeti_hali *너비값=elementi_thamani(mmiliki_kipengee,kitambulishi_thamani);
    if(Kitendo==0){if(kitambulishi_thamani<1||kitambulishi_thamani>5)return -22;for(int 순번=0;순번<32;순번++)if(요소들[mmiliki_kipengee][순번].kategoria_thamani==0){너비값=&요소들[mmiliki_kipengee][순번];memset(너비값,0,sizeof(*너비값));너비값->kategoria_thamani=kitambulishi_thamani;너비값->보이는지=kitambulishi_thamani!=1;너비값->너비값=kitambulishi_thamani==1?380:220;너비값->높이값=kitambulishi_thamani==1?240:28;너비값->Muundo_sera=1;너비값->jira_x=kitambulishi_thamani==1?130:16;너비값->Kitufe_cha_Y_kiratibu=kitambulishi_thamani==1?110:16;return 순번+1;}return -28;}
    if(Kitendo==5){if(!항목수[mmiliki_kipengee])return 0;int 반환값=tukio_Orodha[mmiliki_kipengee][첫항목[mmiliki_kipengee]];첫항목[mmiliki_kipengee]=(첫항목[mmiliki_kipengee]+1)%16;항목수[mmiliki_kipengee]--;return 반환값;}
    if(Kitendo==6)return 화면보임(mmiliki_kipengee);
    if(!너비값)return -9;
    int 이전표시=표시됨(mmiliki_kipengee,너비값);
    if(Kitendo==1){int 바탕너비=보드화면너비(),바탕높이=보드화면높이();if(첫째값<0||둘째값<0||msimbo_wa_kibambo<1||fikio_data<1||첫째값>바탕너비||둘째값>바탕높이||msimbo_wa_kibambo>바탕너비-첫째값||fikio_data>바탕높이-둘째값)return -22;너비값->jira_x=첫째값;너비값->Kitufe_cha_Y_kiratibu=둘째값;너비값->너비값=msimbo_wa_kibambo;너비값->높이값=fikio_data;너비값->a_mikono_Muundo=1;}
    else if(Kitendo==2){wijeti_hali *Elementi_zaliwa=elementi_thamani(mmiliki_kipengee,첫째값);if(!Elementi_zaliwa||Elementi_zaliwa==너비값||Elementi_zaliwa->kategoria_thamani==1)return -22;int 자료위치=kitambulishi_thamani;for(int 깊이=0;자료위치&&깊이<32;깊이++){if(자료위치==첫째값)return -22;wijeti_hali *위쪽=elementi_thamani(mmiliki_kipengee,자료위치);자료위치=위쪽?위쪽->부모항목:0;}Elementi_zaliwa->부모항목=kitambulishi_thamani;if(!Elementi_zaliwa->a_mikono_Muundo){int 형제요소=0;for(int 순번=0;순번<32;순번++)if(&요소들[mmiliki_kipengee][순번]!=Elementi_zaliwa&&요소들[mmiliki_kipengee][순번].부모항목==kitambulishi_thamani)형제요소++;Elementi_zaliwa->Kitufe_cha_Y_kiratibu=16+형제요소*36;}}
    else if(Kitendo==3)너비값->보이는지=첫째값!=0;
    else if(Kitendo==4)너비값->보이는지=0;
    else if(Kitendo==7)너비값->Muundo_sera=첫째값;
    else if(Kitendo==8)return 너비값->urefu_thamani;
    else if(Kitendo==9)return 첫째값>=0&&(unsigned)첫째값<너비값->urefu_thamani?너비값->SMS[첫째값]:-22;
    else return -22;
    if(이전표시||표시됨(mmiliki_kipengee,너비값))보드터미널(3);return 0;
}
int 화면글(int mmiliki_kipengee,int kitambulishi_thamani,const uint32_t *data,unsigned 개수){wijeti_hali *너비값=elementi_thamani(mmiliki_kipengee,kitambulishi_thamani);if(!너비값)return -9;if(개수>127)return -22;for(unsigned 순번=0;순번<개수;순번++){unsigned kibambo_usimbaji=data[순번];if(kibambo_usimbaji>0x10ffff||(kibambo_usimbaji>=0xd800&&kibambo_usimbaji<=0xdfff))return -22;}for(unsigned 순번=0;순번<개수;순번++)너비값->SMS[순번]=data[순번];너비값->urefu_thamani=개수;if(표시됨(mmiliki_kipengee,너비값))보드터미널(3);return 0;}
