#include "Ìjìnnà_iye.h"
#include <string.h>
#include "두벌식표.h"
static unsigned ìdarí_iye,bọ́tìnnì_SHIFT,한글;
typedef struct {unsigned 첫,가운데,끝;} 조합상태;
static 조합상태 조합,àkọsílẹ̀_ìṣe_ìlà_ìbú[16];
static unsigned 기록수;
void 원격글쇠확정(void){memset(&조합,0,sizeof(조합));기록수=0;}
void 원격글쇠초기화(void){ìdarí_iye=bọ́tìnnì_SHIFT=한글=0;원격글쇠확정();}
static void 글넣기(unsigned iye){
    unsigned char SMS[4];unsigned 수;
    if(iye<128){SMS[0]=iye;수=1;}else if(iye<2048){SMS[0]=0xc0|(iye>>6);SMS[1]=0x80|(iye&63);수=2;}
    else if(iye<65536){SMS[0]=0xe0|(iye>>12);SMS[1]=0x80|((iye>>6)&63);SMS[2]=0x80|(iye&63);수=3;}
    else{SMS[0]=0xf0|(iye>>18);SMS[1]=0x80|((iye>>12)&63);SMS[2]=0x80|((iye>>6)&63);SMS[3]=0x80|(iye&63);수=4;}
    원격입력넣기(SMS,수);
}
static int wá_ìgbéwọlé(const unsigned *ìgbéwọlé_Àtòkọ,unsigned 수,unsigned iye){for(unsigned 순번=0;순번<수;순번++)if(ìgbéwọlé_Àtòkọ[순번]==iye)return 순번;return -1;}
static unsigned 겹찾기(const unsigned 표[][3],unsigned 수,unsigned 가,unsigned 나){for(unsigned 순번=0;순번<수;순번++)if(표[순번][0]==가&&표[순번][1]==나)return 표[순번][2];return 0;}
static unsigned 조합글(void){
    if(조합.첫&&조합.가운데)return 0xac00+(wá_ìgbéwọlé(첫소리목록,19,조합.첫)*21+wá_ìgbéwọlé(가운뎃소리목록,21,조합.가운데))*28+(조합.끝?wá_ìgbéwọlé(끝소리목록,28,조합.끝):0);
    return 조합.첫?조합.첫:조합.가운데;
}
static int 한글넣기(unsigned 글쇠){
    unsigned 자모=0;for(unsigned 순번=0;순번<sizeof(bọ́tìnnì_ètò_ìrísí)/sizeof(bọ́tìnnì_ètò_ìrísí[0]);순번++)if(bọ́tìnnì_ètò_ìrísí[순번][0]==글쇠)자모=bọ́tìnnì_ètò_ìrísí[순번][1];
    if(!자모&&글쇠>='A'&&글쇠<='Z')return 한글넣기(글쇠+32);if(!자모)return 0;
    unsigned 이전=조합글(),확정=0;조합상태 전=조합;
    if(기록수<16)àkọsílẹ̀_ìṣe_ìlà_ìbú[기록수++]=전;
    if(wá_ìgbéwọlé(첫소리목록,19,자모)>=0){
        if(조합.첫&&조합.가운데&&!조합.끝&&wá_ìgbéwọlé(끝소리목록,28,자모)>=0)조합.끝=자모;
        else{unsigned àgbélé_iye=겹찾기(겹끝소리,11,조합.끝,자모);if(조합.끝&&àgbélé_iye)조합.끝=àgbélé_iye;
            else{확정=이전;원격글쇠확정();조합.첫=자모;기록수=1;memset(àkọsílẹ̀_ìṣe_ìlà_ìbú,0,sizeof(조합상태));}}
    }else if(조합.끝){
        unsigned 왼쪽=0,오른쪽=조합.끝;for(unsigned 순번=0;순번<11;순번++)if(겹끝소리[순번][2]==조합.끝){왼쪽=겹끝소리[순번][0];오른쪽=겹끝소리[순번][1];break;}
        조합.끝=왼쪽;확정=조합글();원격글쇠확정();조합.첫=오른쪽;조합.가운데=자모;기록수=2;
        memset(àkọsílẹ̀_ìṣe_ìlà_ìbú,0,2*sizeof(조합상태));àkọsílẹ̀_ìṣe_ìlà_ìbú[1].첫=오른쪽;
    }else if(조합.가운데){unsigned àgbélé_iye=겹찾기(겹가운뎃소리,7,조합.가운데,자모);
        if(àgbélé_iye)조합.가운데=àgbélé_iye;else{확정=이전;원격글쇠확정();조합.가운데=자모;기록수=1;memset(àkọsílẹ̀_ìṣe_ìlà_ìbú,0,sizeof(조합상태));}
    }else 조합.가운데=자모;
    if(이전)글넣기(127);if(확정)글넣기(확정);unsigned 지금=조합글();if(지금)글넣기(지금);return 1;
}
void 원격글쇠(unsigned àmì,int 누름){
    if(àmì==0xffe3||àmì==0xffe4){ìdarí_iye=누름;return;}
    if(àmì==0xffe1||àmì==0xffe2){bọ́tìnnì_SHIFT=누름;return;}
    if(!누름)return;
    if(àmì==0xffc6||àmì==0xff31||(àmì==32&&bọ́tìnnì_SHIFT&&!ìdarí_iye)){
        원격글쇠확정();한글=!한글;unsigned char ìgbéṣẹ̀[]={30,3,한글,0,0,0,0};원격입력넣기(ìgbéṣẹ̀,7);return;
    }
    if(àmì==0xff08&&한글&&!ìdarí_iye&&기록수){조합=àkọsílẹ̀_ìṣe_ìlà_ìbú[--기록수];글넣기(127);unsigned SMS=조합글();if(SMS)글넣기(SMS);return;}
    if(한글&&!ìdarí_iye&&àmì<128&&한글넣기(àmì))return;
    원격글쇠확정();
    if((ìdarí_iye&&bọ́tìnnì_SHIFT&&(àmì=='t'||àmì=='T'))||àmì==0xffc3||àmì==0xffc9){unsigned char ìgbéṣẹ̀[]={30,2,àmì==0xffc3?2:àmì==0xffc9?3:1,0,0,0,0};원격입력넣기(ìgbéṣẹ̀,7);return;}
    const char *특수=àmì==0xff08?"\177":àmì==0xff09?"\t":àmì==0xff0d?"\r":àmì==0xff1b?"\033":
        àmì==0xffff?"\033[3~":àmì==0xff50?"\033[H":àmì==0xff57?"\033[F":àmì==0xff51?"\033[D":
        àmì==0xff52?"\033[A":àmì==0xff53?"\033[C":àmì==0xff54?"\033[B":àmì==0xff55?"\033[5~":àmì==0xff56?"\033[6~":0;
    if(특수){원격입력넣기((const unsigned char*)특수,strlen(특수));return;}
    unsigned iye=(àmì&0xff000000)==0x01000000?àmì&0xffffff:àmì;
    if(iye>0x10ffff||(iye>=0xd800&&iye<=0xdfff)||(àmì>=0xff00&&àmì<0x1000000))return;
    if(ìdarí_iye){if(iye>='a'&&iye<='z')iye-=96;else if(iye>='A'&&iye<='Z')iye-=64;}
    글넣기(iye);
}
