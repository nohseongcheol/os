#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* Small native peer layer for the explicitly supported Swing subset. */
#include <stdint.h>
#include <stddef.h>
extern uintptr_t 보드화소(uintptr_t,uintptr_t,uintptr_t),보드터미널(uintptr_t);
extern void 터미널글자그림(unsigned,unsigned,unsigned,unsigned,unsigned);
extern void *memset(void *,int,size_t);
typedef struct { int ɓangare_Daraja,부모항목,gamayyar_x,Maɓallin_Y_Mai_tsarawa,너비값,높이값,보이는지,Aikin_hannu_Zagaye,Zagaye_doka;unsigned SMS[128],Tsawo_Daraja; } wijet_Matsayi;
static wijet_Matsayi 요소들[4][32];
static int Muhimmi[4],Faruwa_Jeri[4][16];static unsigned 첫항목[4],항목수[4],부호없는결과[4],긴부호없는값[4];
static void Faruwa(int mamallaki_abu,int Daraja){if(항목수[mamallaki_abu]<16){Faruwa_Jeri[mamallaki_abu][(첫항목[mamallaki_abu]+항목수[mamallaki_abu])%16]=Daraja;항목수[mamallaki_abu]++;}}
static wijet_Matsayi *Dan_gutsuren_bayani_Daraja(int mamallaki_abu,int mai_ganewa_Daraja){return mamallaki_abu>=0&&mamallaki_abu<4&&mai_ganewa_Daraja>0&&mai_ganewa_Daraja<=32&&요소들[mamallaki_abu][mai_ganewa_Daraja-1].ɓangare_Daraja?&요소들[mamallaki_abu][mai_ganewa_Daraja-1]:0;}
static void 사각영역(int gamayyar_x,int Maɓallin_Y_Mai_tsarawa,int 너비값,int 높이값,unsigned 색상){보드사각그림(gamayyar_x,Maɓallin_Y_Mai_tsarawa,너비값,높이값,색상);}
int 화면보임(int mamallaki_abu){if(mamallaki_abu<0||mamallaki_abu>=4)return 0;for(int 순번=0;순번<32;순번++)if(요소들[mamallaki_abu][순번].ɓangare_Daraja==1&&요소들[mamallaki_abu][순번].보이는지)return 1;return 0;}
void 화면초기화(int mamallaki_abu){memset(요소들[mamallaki_abu],0,sizeof(요소들[mamallaki_abu]));항목수[mamallaki_abu]=첫항목[mamallaki_abu]=Muhimmi[mamallaki_abu]=긴부호없는값[mamallaki_abu]=0;}
static void 위치(int mamallaki_abu,wijet_Matsayi *너비값,int *gamayyar_x,int *Maɓallin_Y_Mai_tsarawa){*gamayyar_x=너비값->gamayyar_x;*Maɓallin_Y_Mai_tsarawa=너비값->Maɓallin_Y_Mai_tsarawa;int 자료위치=너비값->부모항목;for(int 개수=0;자료위치&&개수<32;개수++){wijet_Matsayi *위쪽=Dan_gutsuren_bayani_Daraja(mamallaki_abu,자료위치);if(!위쪽)break;*gamayyar_x+=위쪽->gamayyar_x;*Maɓallin_Y_Mai_tsarawa+=위쪽->Maɓallin_Y_Mai_tsarawa+(위쪽->ɓangare_Daraja==1?30:0);자료위치=위쪽->부모항목;}}
static int 표시됨(int mamallaki_abu,wijet_Matsayi *너비값){for(int 개수=0;개수<32;개수++){if(!너비값->보이는지)return 0;if(너비값->ɓangare_Daraja==1)return 1;너비값=Dan_gutsuren_bayani_Daraja(mamallaki_abu,너비값->부모항목);if(!너비값)return 0;}return 0;}
static void SMS(int gamayyar_x,int Maɓallin_Y_Mai_tsarawa,wijet_Matsayi *너비값,int 최대값,unsigned 색상,unsigned 배경색){int 현재위치=0;for(unsigned 순번=0;순번<너비값->Tsawo_Daraja;순번++){unsigned Harafi_Juyar_da_bayanai_zuwa_lamba=너비값->SMS[순번],너비=Harafi_Juyar_da_bayanai_zuwa_lamba>=256?16:8;if(현재위치+(int)너비>최대값)break;터미널글자그림(gamayyar_x+현재위치,Maɓallin_Y_Mai_tsarawa,Harafi_Juyar_da_bayanai_zuwa_lamba,색상,배경색);현재위치+=너비;}}
void 화면다시그림(int mamallaki_abu){
    if(!화면보임(mamallaki_abu))return;
    for(int 처리차례=1;처리차례<=5;처리차례++)for(int 순번=0;순번<32;순번++){
        wijet_Matsayi *너비값=&요소들[mamallaki_abu][순번];if(너비값->ɓangare_Daraja!=처리차례||!표시됨(mamallaki_abu,너비값))continue;int gamayyar_x,Maɓallin_Y_Mai_tsarawa;위치(mamallaki_abu,너비값,&gamayyar_x,&Maɓallin_Y_Mai_tsarawa);
        if(처리차례==1){사각영역(gamayyar_x,Maɓallin_Y_Mai_tsarawa,너비값->너비값,너비값->높이값,0xeee9e0);사각영역(gamayyar_x,Maɓallin_Y_Mai_tsarawa,너비값->너비값,30,0x905020);SMS(gamayyar_x+10,Maɓallin_Y_Mai_tsarawa+7,너비값,너비값->너비값-50,0xffffff,0x905020);사각영역(gamayyar_x+너비값->너비값-28,Maɓallin_Y_Mai_tsarawa+4,24,22,0x5555b8);터미널글자그림(gamayyar_x+너비값->너비값-20,Maɓallin_Y_Mai_tsarawa+7,'X',0xffffff,0x5555b8);}
        if(처리차례==2)사각영역(gamayyar_x,Maɓallin_Y_Mai_tsarawa,너비값->너비값,너비값->높이값,0xeee9e0);
        if(처리차례>=3){unsigned 배경색=처리차례==4?0xc0ab86:처리차례==5?0xffffff:0xeee9e0;if(처리차례!=3)사각영역(gamayyar_x,Maɓallin_Y_Mai_tsarawa,너비값->너비값,너비값->높이값,배경색);SMS(gamayyar_x+4,Maɓallin_Y_Mai_tsarawa+4,너비값,너비값->너비값-8,0x201a15,배경색);if(처리차례==5&&Muhimmi[mamallaki_abu]==순번+1)사각영역(gamayyar_x,Maɓallin_Y_Mai_tsarawa+너비값->높이값-2,너비값->너비값,2,0x905020);}
    }
}
int 화면덮음(int mamallaki_abu,int gamayyar_x,int Maɓallin_Y_Mai_tsarawa){
    if(!화면보임(mamallaki_abu))return 0;
    for(int 순번=0;순번<32;순번++){
        wijet_Matsayi *taga=&요소들[mamallaki_abu][순번];
        if(taga->ɓangare_Daraja==1&&taga->보이는지&&gamayyar_x>=taga->gamayyar_x&&Maɓallin_Y_Mai_tsarawa>=taga->Maɓallin_Y_Mai_tsarawa&&
           gamayyar_x<taga->gamayyar_x+taga->너비값&&Maɓallin_Y_Mai_tsarawa<taga->Maɓallin_Y_Mai_tsarawa+taga->높이값)return 1;
    }return 0;
}
int 화면가리킴(int mamallaki_abu,unsigned 눌림,int gamayyar_x,int Maɓallin_Y_Mai_tsarawa){
    if(!화면보임(mamallaki_abu))return 0;
    if(눌림&1)for(int 순번=31;순번>=0;순번--){wijet_Matsayi *너비값=&요소들[mamallaki_abu][순번];if(!너비값->ɓangare_Daraja||!표시됨(mamallaki_abu,너비값))continue;int taga_Maɓallin_X,taga_Maɓallin_Y;위치(mamallaki_abu,너비값,&taga_Maɓallin_X,&taga_Maɓallin_Y);
        if(gamayyar_x<taga_Maɓallin_X||Maɓallin_Y_Mai_tsarawa<taga_Maɓallin_Y||gamayyar_x>=taga_Maɓallin_X+너비값->너비값||Maɓallin_Y_Mai_tsarawa>=taga_Maɓallin_Y+너비값->높이값)continue;
        if(너비값->ɓangare_Daraja==1&&Maɓallin_Y_Mai_tsarawa<taga_Maɓallin_Y+30&&gamayyar_x>=taga_Maɓallin_X+너비값->너비값-28){if(너비값->Zagaye_doka!=0)너비값->보이는지=0;Faruwa(mamallaki_abu,0x10000+순번+1);보드터미널(3);return 1;}
        if(너비값->ɓangare_Daraja==4){Faruwa(mamallaki_abu,순번+1);return 1;}if(너비값->ɓangare_Daraja==5){Muhimmi[mamallaki_abu]=순번+1;보드터미널(3);return 1;}
        if(너비값->ɓangare_Daraja==1)return 1;
    }return 0;
}
void 화면누름(int mamallaki_abu,unsigned 둘째값){
    wijet_Matsayi *너비값=Dan_gutsuren_bayani_Daraja(mamallaki_abu,Muhimmi[mamallaki_abu]);if(!너비값||너비값->ɓangare_Daraja!=5)return;
    if(둘째값==13||둘째값==10){Faruwa(mamallaki_abu,Muhimmi[mamallaki_abu]);return;}
    if(둘째값==8||둘째값==127){if(너비값->Tsawo_Daraja)너비값->Tsawo_Daraja--;긴부호없는값[mamallaki_abu]=0;}
    else{
        unsigned Harafi_Juyar_da_bayanai_zuwa_lamba=둘째값;
        if(긴부호없는값[mamallaki_abu]){if((둘째값&192)!=128){긴부호없는값[mamallaki_abu]=0;return;}부호없는결과[mamallaki_abu]=(부호없는결과[mamallaki_abu]<<6)|(둘째값&63);if(--긴부호없는값[mamallaki_abu])return;Harafi_Juyar_da_bayanai_zuwa_lamba=부호없는결과[mamallaki_abu];}
        else if(둘째값>=0xc2&&둘째값<=0xf4){긴부호없는값[mamallaki_abu]=둘째값<0xe0?1:둘째값<0xf0?2:3;부호없는결과[mamallaki_abu]=둘째값&((1u<<(6-긴부호없는값[mamallaki_abu]))-1);return;}
        else if(둘째값<32||둘째값>=128)return;
        if(Harafi_Juyar_da_bayanai_zuwa_lamba>0x10ffff||(Harafi_Juyar_da_bayanai_zuwa_lamba>=0xd800&&Harafi_Juyar_da_bayanai_zuwa_lamba<=0xdfff))return;if(너비값->Tsawo_Daraja<127)너비값->SMS[너비값->Tsawo_Daraja++]=Harafi_Juyar_da_bayanai_zuwa_lamba;
    }
    보드터미널(3);
}
int 화면호출(int mamallaki_abu,unsigned Aiki,int mai_ganewa_Daraja,int 첫째값,int 둘째값,int Lambar_sirrin_harafi,int Zangon_ƙarshe_Tarin_bayani){
    if(mamallaki_abu<0||mamallaki_abu>=4)return -22;wijet_Matsayi *너비값=Dan_gutsuren_bayani_Daraja(mamallaki_abu,mai_ganewa_Daraja);
    if(Aiki==0){if(mai_ganewa_Daraja<1||mai_ganewa_Daraja>5)return -22;for(int 순번=0;순번<32;순번++)if(요소들[mamallaki_abu][순번].ɓangare_Daraja==0){너비값=&요소들[mamallaki_abu][순번];memset(너비값,0,sizeof(*너비값));너비값->ɓangare_Daraja=mai_ganewa_Daraja;너비값->보이는지=mai_ganewa_Daraja!=1;너비값->너비값=mai_ganewa_Daraja==1?380:220;너비값->높이값=mai_ganewa_Daraja==1?240:28;너비값->Zagaye_doka=1;너비값->gamayyar_x=mai_ganewa_Daraja==1?130:16;너비값->Maɓallin_Y_Mai_tsarawa=mai_ganewa_Daraja==1?110:16;return 순번+1;}return -28;}
    if(Aiki==5){if(!항목수[mamallaki_abu])return 0;int 반환값=Faruwa_Jeri[mamallaki_abu][첫항목[mamallaki_abu]];첫항목[mamallaki_abu]=(첫항목[mamallaki_abu]+1)%16;항목수[mamallaki_abu]--;return 반환값;}
    if(Aiki==6)return 화면보임(mamallaki_abu);
    if(!너비값)return -9;
    int 이전표시=표시됨(mamallaki_abu,너비값);
    if(Aiki==1){int 바탕너비=보드화면너비(),바탕높이=보드화면높이();if(첫째값<0||둘째값<0||Lambar_sirrin_harafi<1||Zangon_ƙarshe_Tarin_bayani<1||첫째값>바탕너비||둘째값>바탕높이||Lambar_sirrin_harafi>바탕너비-첫째값||Zangon_ƙarshe_Tarin_bayani>바탕높이-둘째값)return -22;너비값->gamayyar_x=첫째값;너비값->Maɓallin_Y_Mai_tsarawa=둘째값;너비값->너비값=Lambar_sirrin_harafi;너비값->높이값=Zangon_ƙarshe_Tarin_bayani;너비값->Aikin_hannu_Zagaye=1;}
    else if(Aiki==2){wijet_Matsayi *Ƙaramin_shafi=Dan_gutsuren_bayani_Daraja(mamallaki_abu,첫째값);if(!Ƙaramin_shafi||Ƙaramin_shafi==너비값||Ƙaramin_shafi->ɓangare_Daraja==1)return -22;int 자료위치=mai_ganewa_Daraja;for(int 깊이=0;자료위치&&깊이<32;깊이++){if(자료위치==첫째값)return -22;wijet_Matsayi *위쪽=Dan_gutsuren_bayani_Daraja(mamallaki_abu,자료위치);자료위치=위쪽?위쪽->부모항목:0;}Ƙaramin_shafi->부모항목=mai_ganewa_Daraja;if(!Ƙaramin_shafi->Aikin_hannu_Zagaye){int 형제요소=0;for(int 순번=0;순번<32;순번++)if(&요소들[mamallaki_abu][순번]!=Ƙaramin_shafi&&요소들[mamallaki_abu][순번].부모항목==mai_ganewa_Daraja)형제요소++;Ƙaramin_shafi->Maɓallin_Y_Mai_tsarawa=16+형제요소*36;}}
    else if(Aiki==3)너비값->보이는지=첫째값!=0;
    else if(Aiki==4)너비값->보이는지=0;
    else if(Aiki==7)너비값->Zagaye_doka=첫째값;
    else if(Aiki==8)return 너비값->Tsawo_Daraja;
    else if(Aiki==9)return 첫째값>=0&&(unsigned)첫째값<너비값->Tsawo_Daraja?너비값->SMS[첫째값]:-22;
    else return -22;
    if(이전표시||표시됨(mamallaki_abu,너비값))보드터미널(3);return 0;
}
int 화면글(int mamallaki_abu,int mai_ganewa_Daraja,const uint32_t *Tarin_bayani,unsigned 개수){wijet_Matsayi *너비값=Dan_gutsuren_bayani_Daraja(mamallaki_abu,mai_ganewa_Daraja);if(!너비값)return -9;if(개수>127)return -22;for(unsigned 순번=0;순번<개수;순번++){unsigned Harafi_Juyar_da_bayanai_zuwa_lamba=Tarin_bayani[순번];if(Harafi_Juyar_da_bayanai_zuwa_lamba>0x10ffff||(Harafi_Juyar_da_bayanai_zuwa_lamba>=0xd800&&Harafi_Juyar_da_bayanai_zuwa_lamba<=0xdfff))return -22;}for(unsigned 순번=0;순번<개수;순번++)너비값->SMS[순번]=Tarin_bayani[순번];너비값->Tsawo_Daraja=개수;if(표시됨(mamallaki_abu,너비값))보드터미널(3);return 0;}
