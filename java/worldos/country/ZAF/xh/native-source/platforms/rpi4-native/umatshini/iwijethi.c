#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* Small native peer layer for the explicitly supported Swing subset. */
#include <stdint.h>
#include <stddef.h>
extern uintptr_t 보드화소(uintptr_t,uintptr_t,uintptr_t),보드터미널(uintptr_t);
extern void 터미널글자그림(unsigned,unsigned,unsigned,unsigned,unsigned);
extern void *memset(void *,int,size_t);
typedef struct { int udidi_ixabiso,부모항목,isilungelelanisi_x,세로좌표,너비값,높이값,보이는지,ozenzela_ngokwakho_ubume,ubume_umgaqo_nkqubo;unsigned Umbhalo[128],ubude_ixabiso; } iwijethi_imo;
static iwijethi_imo 요소들[4][32];
static int Igqalisele[4],umcimbi_uludwe[4][16];static unsigned 첫항목[4],항목수[4],부호없는결과[4],긴부호없는값[4];
static void umcimbi(int umnini_into,int ixabiso){if(항목수[umnini_into]<16){umcimbi_uludwe[umnini_into][(첫항목[umnini_into]+항목수[umnini_into])%16]=ixabiso;항목수[umnini_into]++;}}
static iwijethi_imo *ielement_ixabiso(int umnini_into,int isalathisi_ixabiso){return umnini_into>=0&&umnini_into<4&&isalathisi_ixabiso>0&&isalathisi_ixabiso<=32&&요소들[umnini_into][isalathisi_ixabiso-1].udidi_ixabiso?&요소들[umnini_into][isalathisi_ixabiso-1]:0;}
static void 사각영역(int isilungelelanisi_x,int 세로좌표,int 너비값,int 높이값,unsigned 색상){보드사각그림(isilungelelanisi_x,세로좌표,너비값,높이값,색상);}
int 화면보임(int umnini_into){if(umnini_into<0||umnini_into>=4)return 0;for(int 순번=0;순번<32;순번++)if(요소들[umnini_into][순번].udidi_ixabiso==1&&요소들[umnini_into][순번].보이는지)return 1;return 0;}
void 화면초기화(int umnini_into){memset(요소들[umnini_into],0,sizeof(요소들[umnini_into]));항목수[umnini_into]=첫항목[umnini_into]=Igqalisele[umnini_into]=긴부호없는값[umnini_into]=0;}
static void 위치(int umnini_into,iwijethi_imo *너비값,int *isilungelelanisi_x,int *세로좌표){*isilungelelanisi_x=너비값->isilungelelanisi_x;*세로좌표=너비값->세로좌표;int 자료위치=너비값->부모항목;for(int 개수=0;자료위치&&개수<32;개수++){iwijethi_imo *위쪽=ielement_ixabiso(umnini_into,자료위치);if(!위쪽)break;*isilungelelanisi_x+=위쪽->isilungelelanisi_x;*세로좌표+=위쪽->세로좌표+(위쪽->udidi_ixabiso==1?30:0);자료위치=위쪽->부모항목;}}
static int 표시됨(int umnini_into,iwijethi_imo *너비값){for(int 개수=0;개수<32;개수++){if(!너비값->보이는지)return 0;if(너비값->udidi_ixabiso==1)return 1;너비값=ielement_ixabiso(umnini_into,너비값->부모항목);if(!너비값)return 0;}return 0;}
static void Umbhalo(int isilungelelanisi_x,int 세로좌표,iwijethi_imo *너비값,int 최대값,unsigned 색상,unsigned 배경색){int 현재위치=0;for(unsigned 순번=0;순번<너비값->ubude_ixabiso;순번++){unsigned ikharakhtha_ujiko_nkcukacha_zibe_ziikhowudi=너비값->Umbhalo[순번],너비=ikharakhtha_ujiko_nkcukacha_zibe_ziikhowudi>=256?16:8;if(현재위치+(int)너비>최대값)break;터미널글자그림(isilungelelanisi_x+현재위치,세로좌표,ikharakhtha_ujiko_nkcukacha_zibe_ziikhowudi,색상,배경색);현재위치+=너비;}}
void 화면다시그림(int umnini_into){
    if(!화면보임(umnini_into))return;
    for(int 처리차례=1;처리차례<=5;처리차례++)for(int 순번=0;순번<32;순번++){
        iwijethi_imo *너비값=&요소들[umnini_into][순번];if(너비값->udidi_ixabiso!=처리차례||!표시됨(umnini_into,너비값))continue;int isilungelelanisi_x,세로좌표;위치(umnini_into,너비값,&isilungelelanisi_x,&세로좌표);
        if(처리차례==1){사각영역(isilungelelanisi_x,세로좌표,너비값->너비값,너비값->높이값,0xeee9e0);사각영역(isilungelelanisi_x,세로좌표,너비값->너비값,30,0x905020);Umbhalo(isilungelelanisi_x+10,세로좌표+7,너비값,너비값->너비값-50,0xffffff,0x905020);사각영역(isilungelelanisi_x+너비값->너비값-28,세로좌표+4,24,22,0x5555b8);터미널글자그림(isilungelelanisi_x+너비값->너비값-20,세로좌표+7,'X',0xffffff,0x5555b8);}
        if(처리차례==2)사각영역(isilungelelanisi_x,세로좌표,너비값->너비값,너비값->높이값,0xeee9e0);
        if(처리차례>=3){unsigned 배경색=처리차례==4?0xc0ab86:처리차례==5?0xffffff:0xeee9e0;if(처리차례!=3)사각영역(isilungelelanisi_x,세로좌표,너비값->너비값,너비값->높이값,배경색);Umbhalo(isilungelelanisi_x+4,세로좌표+4,너비값,너비값->너비값-8,0x201a15,배경색);if(처리차례==5&&Igqalisele[umnini_into]==순번+1)사각영역(isilungelelanisi_x,세로좌표+너비값->높이값-2,너비값->너비값,2,0x905020);}
    }
}
int 화면덮음(int umnini_into,int isilungelelanisi_x,int 세로좌표){
    if(!화면보임(umnini_into))return 0;
    for(int 순번=0;순번<32;순번++){
        iwijethi_imo *i_window=&요소들[umnini_into][순번];
        if(i_window->udidi_ixabiso==1&&i_window->보이는지&&isilungelelanisi_x>=i_window->isilungelelanisi_x&&세로좌표>=i_window->세로좌표&&
           isilungelelanisi_x<i_window->isilungelelanisi_x+i_window->너비값&&세로좌표<i_window->세로좌표+i_window->높이값)return 1;
    }return 0;
}
int 화면가리킴(int umnini_into,unsigned 눌림,int isilungelelanisi_x,int 세로좌표){
    if(!화면보임(umnini_into))return 0;
    if(눌림&1)for(int 순번=31;순번>=0;순번--){iwijethi_imo *너비값=&요소들[umnini_into][순번];if(!너비값->udidi_ixabiso||!표시됨(umnini_into,너비값))continue;int 창가로,창세로;위치(umnini_into,너비값,&창가로,&창세로);
        if(isilungelelanisi_x<창가로||세로좌표<창세로||isilungelelanisi_x>=창가로+너비값->너비값||세로좌표>=창세로+너비값->높이값)continue;
        if(너비값->udidi_ixabiso==1&&세로좌표<창세로+30&&isilungelelanisi_x>=창가로+너비값->너비값-28){if(너비값->ubume_umgaqo_nkqubo!=0)너비값->보이는지=0;umcimbi(umnini_into,0x10000+순번+1);보드터미널(3);return 1;}
        if(너비값->udidi_ixabiso==4){umcimbi(umnini_into,순번+1);return 1;}if(너비값->udidi_ixabiso==5){Igqalisele[umnini_into]=순번+1;보드터미널(3);return 1;}
        if(너비값->udidi_ixabiso==1)return 1;
    }return 0;
}
void 화면누름(int umnini_into,unsigned 둘째값){
    iwijethi_imo *너비값=ielement_ixabiso(umnini_into,Igqalisele[umnini_into]);if(!너비값||너비값->udidi_ixabiso!=5)return;
    if(둘째값==13||둘째값==10){umcimbi(umnini_into,Igqalisele[umnini_into]);return;}
    if(둘째값==8||둘째값==127){if(너비값->ubude_ixabiso)너비값->ubude_ixabiso--;긴부호없는값[umnini_into]=0;}
    else{
        unsigned ikharakhtha_ujiko_nkcukacha_zibe_ziikhowudi=둘째값;
        if(긴부호없는값[umnini_into]){if((둘째값&192)!=128){긴부호없는값[umnini_into]=0;return;}부호없는결과[umnini_into]=(부호없는결과[umnini_into]<<6)|(둘째값&63);if(--긴부호없는값[umnini_into])return;ikharakhtha_ujiko_nkcukacha_zibe_ziikhowudi=부호없는결과[umnini_into];}
        else if(둘째값>=0xc2&&둘째값<=0xf4){긴부호없는값[umnini_into]=둘째값<0xe0?1:둘째값<0xf0?2:3;부호없는결과[umnini_into]=둘째값&((1u<<(6-긴부호없는값[umnini_into]))-1);return;}
        else if(둘째값<32||둘째값>=128)return;
        if(ikharakhtha_ujiko_nkcukacha_zibe_ziikhowudi>0x10ffff||(ikharakhtha_ujiko_nkcukacha_zibe_ziikhowudi>=0xd800&&ikharakhtha_ujiko_nkcukacha_zibe_ziikhowudi<=0xdfff))return;if(너비값->ubude_ixabiso<127)너비값->Umbhalo[너비값->ubude_ixabiso++]=ikharakhtha_ujiko_nkcukacha_zibe_ziikhowudi;
    }
    보드터미널(3);
}
int 화면호출(int umnini_into,unsigned Intshukumo,int isalathisi_ixabiso,int 첫째값,int 둘째값,int ikhowudi_yekharakhtha,int indawo_ekuyiwa_kuyo_iingcombolo){
    if(umnini_into<0||umnini_into>=4)return -22;iwijethi_imo *너비값=ielement_ixabiso(umnini_into,isalathisi_ixabiso);
    if(Intshukumo==0){if(isalathisi_ixabiso<1||isalathisi_ixabiso>5)return -22;for(int 순번=0;순번<32;순번++)if(요소들[umnini_into][순번].udidi_ixabiso==0){너비값=&요소들[umnini_into][순번];memset(너비값,0,sizeof(*너비값));너비값->udidi_ixabiso=isalathisi_ixabiso;너비값->보이는지=isalathisi_ixabiso!=1;너비값->너비값=isalathisi_ixabiso==1?380:220;너비값->높이값=isalathisi_ixabiso==1?240:28;너비값->ubume_umgaqo_nkqubo=1;너비값->isilungelelanisi_x=isalathisi_ixabiso==1?130:16;너비값->세로좌표=isalathisi_ixabiso==1?110:16;return 순번+1;}return -28;}
    if(Intshukumo==5){if(!항목수[umnini_into])return 0;int 반환값=umcimbi_uludwe[umnini_into][첫항목[umnini_into]];첫항목[umnini_into]=(첫항목[umnini_into]+1)%16;항목수[umnini_into]--;return 반환값;}
    if(Intshukumo==6)return 화면보임(umnini_into);
    if(!너비값)return -9;
    int 이전표시=표시됨(umnini_into,너비값);
    if(Intshukumo==1){int 바탕너비=보드화면너비(),바탕높이=보드화면높이();if(첫째값<0||둘째값<0||ikhowudi_yekharakhtha<1||indawo_ekuyiwa_kuyo_iingcombolo<1||첫째값>바탕너비||둘째값>바탕높이||ikhowudi_yekharakhtha>바탕너비-첫째값||indawo_ekuyiwa_kuyo_iingcombolo>바탕높이-둘째값)return -22;너비값->isilungelelanisi_x=첫째값;너비값->세로좌표=둘째값;너비값->너비값=ikhowudi_yekharakhtha;너비값->높이값=indawo_ekuyiwa_kuyo_iingcombolo;너비값->ozenzela_ngokwakho_ubume=1;}
    else if(Intshukumo==2){iwijethi_imo *ielementi_encinci=ielement_ixabiso(umnini_into,첫째값);if(!ielementi_encinci||ielementi_encinci==너비값||ielementi_encinci->udidi_ixabiso==1)return -22;int 자료위치=isalathisi_ixabiso;for(int 깊이=0;자료위치&&깊이<32;깊이++){if(자료위치==첫째값)return -22;iwijethi_imo *위쪽=ielement_ixabiso(umnini_into,자료위치);자료위치=위쪽?위쪽->부모항목:0;}ielementi_encinci->부모항목=isalathisi_ixabiso;if(!ielementi_encinci->ozenzela_ngokwakho_ubume){int 형제요소=0;for(int 순번=0;순번<32;순번++)if(&요소들[umnini_into][순번]!=ielementi_encinci&&요소들[umnini_into][순번].부모항목==isalathisi_ixabiso)형제요소++;ielementi_encinci->세로좌표=16+형제요소*36;}}
    else if(Intshukumo==3)너비값->보이는지=첫째값!=0;
    else if(Intshukumo==4)너비값->보이는지=0;
    else if(Intshukumo==7)너비값->ubume_umgaqo_nkqubo=첫째값;
    else if(Intshukumo==8)return 너비값->ubude_ixabiso;
    else if(Intshukumo==9)return 첫째값>=0&&(unsigned)첫째값<너비값->ubude_ixabiso?너비값->Umbhalo[첫째값]:-22;
    else return -22;
    if(이전표시||표시됨(umnini_into,너비값))보드터미널(3);return 0;
}
int 화면글(int umnini_into,int isalathisi_ixabiso,const uint32_t *iingcombolo,unsigned 개수){iwijethi_imo *너비값=ielement_ixabiso(umnini_into,isalathisi_ixabiso);if(!너비값)return -9;if(개수>127)return -22;for(unsigned 순번=0;순번<개수;순번++){unsigned ikharakhtha_ujiko_nkcukacha_zibe_ziikhowudi=iingcombolo[순번];if(ikharakhtha_ujiko_nkcukacha_zibe_ziikhowudi>0x10ffff||(ikharakhtha_ujiko_nkcukacha_zibe_ziikhowudi>=0xd800&&ikharakhtha_ujiko_nkcukacha_zibe_ziikhowudi<=0xdfff))return -22;}for(unsigned 순번=0;순번<개수;순번++)너비값->Umbhalo[순번]=iingcombolo[순번];너비값->ubude_ixabiso=개수;if(표시됨(umnini_into,너비값))보드터미널(3);return 0;}
