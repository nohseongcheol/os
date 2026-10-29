#include "../명명/기계연결이름.h"
#include "화면정보.h"
/* Small native peer layer for the explicitly supported Swing subset. */
#include <stdint.h>
#include <stddef.h>
extern uintptr_t 보드화소(uintptr_t,uintptr_t,uintptr_t),보드터미널(uintptr_t);
extern void 터미널글자그림(unsigned,unsigned,unsigned,unsigned,unsigned);
extern void *memset(void *,int,size_t);
typedef struct { int ìsọ̀rí_iye,부모항목,ibi_ìtọ́kasí_x,세로좌표,너비값,높이값,보이는지,aláfọwọ́ṣe_ètò_ìrísí,ètò_ìrísí_ìlànà;unsigned SMS[128],gígùn_iye; } wíjẹ́ẹ̀tì_ipò;
static wíjẹ́ẹ̀tì_ipò 요소들[4][32];
static int Fojúsùn[4],ìgbéṣẹ̀_Àtòkọ[4][16];static unsigned 첫항목[4],항목수[4],부호없는결과[4],긴부호없는값[4];
static void ìgbéṣẹ̀(int Oníǹkan_nǹkan,int iye){if(항목수[Oníǹkan_nǹkan]<16){ìgbéṣẹ̀_Àtòkọ[Oníǹkan_nǹkan][(첫항목[Oníǹkan_nǹkan]+항목수[Oníǹkan_nǹkan])%16]=iye;항목수[Oníǹkan_nǹkan]++;}}
static wíjẹ́ẹ̀tì_ipò *ìdá_ìpìlẹ̀_iye(int Oníǹkan_nǹkan,int Àfidámọ̀_iye){return Oníǹkan_nǹkan>=0&&Oníǹkan_nǹkan<4&&Àfidámọ̀_iye>0&&Àfidámọ̀_iye<=32&&요소들[Oníǹkan_nǹkan][Àfidámọ̀_iye-1].ìsọ̀rí_iye?&요소들[Oníǹkan_nǹkan][Àfidámọ̀_iye-1]:0;}
static void 사각영역(int ibi_ìtọ́kasí_x,int 세로좌표,int 너비값,int 높이값,unsigned 색상){보드사각그림(ibi_ìtọ́kasí_x,세로좌표,너비값,높이값,색상);}
int 화면보임(int Oníǹkan_nǹkan){if(Oníǹkan_nǹkan<0||Oníǹkan_nǹkan>=4)return 0;for(int 순번=0;순번<32;순번++)if(요소들[Oníǹkan_nǹkan][순번].ìsọ̀rí_iye==1&&요소들[Oníǹkan_nǹkan][순번].보이는지)return 1;return 0;}
void 화면초기화(int Oníǹkan_nǹkan){memset(요소들[Oníǹkan_nǹkan],0,sizeof(요소들[Oníǹkan_nǹkan]));항목수[Oníǹkan_nǹkan]=첫항목[Oníǹkan_nǹkan]=Fojúsùn[Oníǹkan_nǹkan]=긴부호없는값[Oníǹkan_nǹkan]=0;}
static void 위치(int Oníǹkan_nǹkan,wíjẹ́ẹ̀tì_ipò *너비값,int *ibi_ìtọ́kasí_x,int *세로좌표){*ibi_ìtọ́kasí_x=너비값->ibi_ìtọ́kasí_x;*세로좌표=너비값->세로좌표;int 자료위치=너비값->부모항목;for(int 개수=0;자료위치&&개수<32;개수++){wíjẹ́ẹ̀tì_ipò *위쪽=ìdá_ìpìlẹ̀_iye(Oníǹkan_nǹkan,자료위치);if(!위쪽)break;*ibi_ìtọ́kasí_x+=위쪽->ibi_ìtọ́kasí_x;*세로좌표+=위쪽->세로좌표+(위쪽->ìsọ̀rí_iye==1?30:0);자료위치=위쪽->부모항목;}}
static int 표시됨(int Oníǹkan_nǹkan,wíjẹ́ẹ̀tì_ipò *너비값){for(int 개수=0;개수<32;개수++){if(!너비값->보이는지)return 0;if(너비값->ìsọ̀rí_iye==1)return 1;너비값=ìdá_ìpìlẹ̀_iye(Oníǹkan_nǹkan,너비값->부모항목);if(!너비값)return 0;}return 0;}
static void SMS(int ibi_ìtọ́kasí_x,int 세로좌표,wíjẹ́ẹ̀tì_ipò *너비값,int 최대값,unsigned 색상,unsigned 배경색){int 현재위치=0;for(unsigned 순번=0;순번<너비값->gígùn_iye;순번++){unsigned ẹyọ_ọ̀rọ̀_pípàrokò=너비값->SMS[순번],너비=ẹyọ_ọ̀rọ̀_pípàrokò>=256?16:8;if(현재위치+(int)너비>최대값)break;터미널글자그림(ibi_ìtọ́kasí_x+현재위치,세로좌표,ẹyọ_ọ̀rọ̀_pípàrokò,색상,배경색);현재위치+=너비;}}
void 화면다시그림(int Oníǹkan_nǹkan){
    if(!화면보임(Oníǹkan_nǹkan))return;
    for(int 처리차례=1;처리차례<=5;처리차례++)for(int 순번=0;순번<32;순번++){
        wíjẹ́ẹ̀tì_ipò *너비값=&요소들[Oníǹkan_nǹkan][순번];if(너비값->ìsọ̀rí_iye!=처리차례||!표시됨(Oníǹkan_nǹkan,너비값))continue;int ibi_ìtọ́kasí_x,세로좌표;위치(Oníǹkan_nǹkan,너비값,&ibi_ìtọ́kasí_x,&세로좌표);
        if(처리차례==1){사각영역(ibi_ìtọ́kasí_x,세로좌표,너비값->너비값,너비값->높이값,0xeee9e0);사각영역(ibi_ìtọ́kasí_x,세로좌표,너비값->너비값,30,0x905020);SMS(ibi_ìtọ́kasí_x+10,세로좌표+7,너비값,너비값->너비값-50,0xffffff,0x905020);사각영역(ibi_ìtọ́kasí_x+너비값->너비값-28,세로좌표+4,24,22,0x5555b8);터미널글자그림(ibi_ìtọ́kasí_x+너비값->너비값-20,세로좌표+7,'X',0xffffff,0x5555b8);}
        if(처리차례==2)사각영역(ibi_ìtọ́kasí_x,세로좌표,너비값->너비값,너비값->높이값,0xeee9e0);
        if(처리차례>=3){unsigned 배경색=처리차례==4?0xc0ab86:처리차례==5?0xffffff:0xeee9e0;if(처리차례!=3)사각영역(ibi_ìtọ́kasí_x,세로좌표,너비값->너비값,너비값->높이값,배경색);SMS(ibi_ìtọ́kasí_x+4,세로좌표+4,너비값,너비값->너비값-8,0x201a15,배경색);if(처리차례==5&&Fojúsùn[Oníǹkan_nǹkan]==순번+1)사각영역(ibi_ìtọ́kasí_x,세로좌표+너비값->높이값-2,너비값->너비값,2,0x905020);}
    }
}
int 화면덮음(int Oníǹkan_nǹkan,int ibi_ìtọ́kasí_x,int 세로좌표){
    if(!화면보임(Oníǹkan_nǹkan))return 0;
    for(int 순번=0;순번<32;순번++){
        wíjẹ́ẹ̀tì_ipò *wínńdò=&요소들[Oníǹkan_nǹkan][순번];
        if(wínńdò->ìsọ̀rí_iye==1&&wínńdò->보이는지&&ibi_ìtọ́kasí_x>=wínńdò->ibi_ìtọ́kasí_x&&세로좌표>=wínńdò->세로좌표&&
           ibi_ìtọ́kasí_x<wínńdò->ibi_ìtọ́kasí_x+wínńdò->너비값&&세로좌표<wínńdò->세로좌표+wínńdò->높이값)return 1;
    }return 0;
}
int 화면가리킴(int Oníǹkan_nǹkan,unsigned 눌림,int ibi_ìtọ́kasí_x,int 세로좌표){
    if(!화면보임(Oníǹkan_nǹkan))return 0;
    if(눌림&1)for(int 순번=31;순번>=0;순번--){wíjẹ́ẹ̀tì_ipò *너비값=&요소들[Oníǹkan_nǹkan][순번];if(!너비값->ìsọ̀rí_iye||!표시됨(Oníǹkan_nǹkan,너비값))continue;int 창가로,창세로;위치(Oníǹkan_nǹkan,너비값,&창가로,&창세로);
        if(ibi_ìtọ́kasí_x<창가로||세로좌표<창세로||ibi_ìtọ́kasí_x>=창가로+너비값->너비값||세로좌표>=창세로+너비값->높이값)continue;
        if(너비값->ìsọ̀rí_iye==1&&세로좌표<창세로+30&&ibi_ìtọ́kasí_x>=창가로+너비값->너비값-28){if(너비값->ètò_ìrísí_ìlànà!=0)너비값->보이는지=0;ìgbéṣẹ̀(Oníǹkan_nǹkan,0x10000+순번+1);보드터미널(3);return 1;}
        if(너비값->ìsọ̀rí_iye==4){ìgbéṣẹ̀(Oníǹkan_nǹkan,순번+1);return 1;}if(너비값->ìsọ̀rí_iye==5){Fojúsùn[Oníǹkan_nǹkan]=순번+1;보드터미널(3);return 1;}
        if(너비값->ìsọ̀rí_iye==1)return 1;
    }return 0;
}
void 화면누름(int Oníǹkan_nǹkan,unsigned 둘째값){
    wíjẹ́ẹ̀tì_ipò *너비값=ìdá_ìpìlẹ̀_iye(Oníǹkan_nǹkan,Fojúsùn[Oníǹkan_nǹkan]);if(!너비값||너비값->ìsọ̀rí_iye!=5)return;
    if(둘째값==13||둘째값==10){ìgbéṣẹ̀(Oníǹkan_nǹkan,Fojúsùn[Oníǹkan_nǹkan]);return;}
    if(둘째값==8||둘째값==127){if(너비값->gígùn_iye)너비값->gígùn_iye--;긴부호없는값[Oníǹkan_nǹkan]=0;}
    else{
        unsigned ẹyọ_ọ̀rọ̀_pípàrokò=둘째값;
        if(긴부호없는값[Oníǹkan_nǹkan]){if((둘째값&192)!=128){긴부호없는값[Oníǹkan_nǹkan]=0;return;}부호없는결과[Oníǹkan_nǹkan]=(부호없는결과[Oníǹkan_nǹkan]<<6)|(둘째값&63);if(--긴부호없는값[Oníǹkan_nǹkan])return;ẹyọ_ọ̀rọ̀_pípàrokò=부호없는결과[Oníǹkan_nǹkan];}
        else if(둘째값>=0xc2&&둘째값<=0xf4){긴부호없는값[Oníǹkan_nǹkan]=둘째값<0xe0?1:둘째값<0xf0?2:3;부호없는결과[Oníǹkan_nǹkan]=둘째값&((1u<<(6-긴부호없는값[Oníǹkan_nǹkan]))-1);return;}
        else if(둘째값<32||둘째값>=128)return;
        if(ẹyọ_ọ̀rọ̀_pípàrokò>0x10ffff||(ẹyọ_ọ̀rọ̀_pípàrokò>=0xd800&&ẹyọ_ọ̀rọ̀_pípàrokò<=0xdfff))return;if(너비값->gígùn_iye<127)너비값->SMS[너비값->gígùn_iye++]=ẹyọ_ọ̀rọ̀_pípàrokò;
    }
    보드터미널(3);
}
int 화면호출(int Oníǹkan_nǹkan,unsigned ìṣe,int Àfidámọ̀_iye,int 첫째값,int 둘째값,int kóòdù_ẹyọ_ọ̀rọ̀,int èbúté_détà){
    if(Oníǹkan_nǹkan<0||Oníǹkan_nǹkan>=4)return -22;wíjẹ́ẹ̀tì_ipò *너비값=ìdá_ìpìlẹ̀_iye(Oníǹkan_nǹkan,Àfidámọ̀_iye);
    if(ìṣe==0){if(Àfidámọ̀_iye<1||Àfidámọ̀_iye>5)return -22;for(int 순번=0;순번<32;순번++)if(요소들[Oníǹkan_nǹkan][순번].ìsọ̀rí_iye==0){너비값=&요소들[Oníǹkan_nǹkan][순번];memset(너비값,0,sizeof(*너비값));너비값->ìsọ̀rí_iye=Àfidámọ̀_iye;너비값->보이는지=Àfidámọ̀_iye!=1;너비값->너비값=Àfidámọ̀_iye==1?380:220;너비값->높이값=Àfidámọ̀_iye==1?240:28;너비값->ètò_ìrísí_ìlànà=1;너비값->ibi_ìtọ́kasí_x=Àfidámọ̀_iye==1?130:16;너비값->세로좌표=Àfidámọ̀_iye==1?110:16;return 순번+1;}return -28;}
    if(ìṣe==5){if(!항목수[Oníǹkan_nǹkan])return 0;int 반환값=ìgbéṣẹ̀_Àtòkọ[Oníǹkan_nǹkan][첫항목[Oníǹkan_nǹkan]];첫항목[Oníǹkan_nǹkan]=(첫항목[Oníǹkan_nǹkan]+1)%16;항목수[Oníǹkan_nǹkan]--;return 반환값;}
    if(ìṣe==6)return 화면보임(Oníǹkan_nǹkan);
    if(!너비값)return -9;
    int 이전표시=표시됨(Oníǹkan_nǹkan,너비값);
    if(ìṣe==1){int 바탕너비=보드화면너비(),바탕높이=보드화면높이();if(첫째값<0||둘째값<0||kóòdù_ẹyọ_ọ̀rọ̀<1||èbúté_détà<1||첫째값>바탕너비||둘째값>바탕높이||kóòdù_ẹyọ_ọ̀rọ̀>바탕너비-첫째값||èbúté_détà>바탕높이-둘째값)return -22;너비값->ibi_ìtọ́kasí_x=첫째값;너비값->세로좌표=둘째값;너비값->너비값=kóòdù_ẹyọ_ọ̀rọ̀;너비값->높이값=èbúté_détà;너비값->aláfọwọ́ṣe_ètò_ìrísí=1;}
    else if(ìṣe==2){wíjẹ́ẹ̀tì_ipò *ọmọ=ìdá_ìpìlẹ̀_iye(Oníǹkan_nǹkan,첫째값);if(!ọmọ||ọmọ==너비값||ọmọ->ìsọ̀rí_iye==1)return -22;int 자료위치=Àfidámọ̀_iye;for(int 깊이=0;자료위치&&깊이<32;깊이++){if(자료위치==첫째값)return -22;wíjẹ́ẹ̀tì_ipò *위쪽=ìdá_ìpìlẹ̀_iye(Oníǹkan_nǹkan,자료위치);자료위치=위쪽?위쪽->부모항목:0;}ọmọ->부모항목=Àfidámọ̀_iye;if(!ọmọ->aláfọwọ́ṣe_ètò_ìrísí){int 형제요소=0;for(int 순번=0;순번<32;순번++)if(&요소들[Oníǹkan_nǹkan][순번]!=ọmọ&&요소들[Oníǹkan_nǹkan][순번].부모항목==Àfidámọ̀_iye)형제요소++;ọmọ->세로좌표=16+형제요소*36;}}
    else if(ìṣe==3)너비값->보이는지=첫째값!=0;
    else if(ìṣe==4)너비값->보이는지=0;
    else if(ìṣe==7)너비값->ètò_ìrísí_ìlànà=첫째값;
    else if(ìṣe==8)return 너비값->gígùn_iye;
    else if(ìṣe==9)return 첫째값>=0&&(unsigned)첫째값<너비값->gígùn_iye?너비값->SMS[첫째값]:-22;
    else return -22;
    if(이전표시||표시됨(Oníǹkan_nǹkan,너비값))보드터미널(3);return 0;
}
int 화면글(int Oníǹkan_nǹkan,int Àfidámọ̀_iye,const uint32_t *détà,unsigned 개수){wíjẹ́ẹ̀tì_ipò *너비값=ìdá_ìpìlẹ̀_iye(Oníǹkan_nǹkan,Àfidámọ̀_iye);if(!너비값)return -9;if(개수>127)return -22;for(unsigned 순번=0;순번<개수;순번++){unsigned ẹyọ_ọ̀rọ̀_pípàrokò=détà[순번];if(ẹyọ_ọ̀rọ̀_pípàrokò>0x10ffff||(ẹyọ_ọ̀rọ̀_pípàrokò>=0xd800&&ẹyọ_ọ̀rọ̀_pípàrokò<=0xdfff))return -22;}for(unsigned 순번=0;순번<개수;순번++)너비값->SMS[순번]=détà[순번];너비값->gígùn_iye=개수;if(표시됨(Oníǹkan_nǹkan,너비값))보드터미널(3);return 0;}
