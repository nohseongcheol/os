#include "kwa_mbali_thamani.h"
#include <string.h>
#include "두벌식표.h"
static unsigned udhibiti_thamani,kibonye_SHIFT,한글;
typedef struct {unsigned 첫,가운데,끝;} 조합상태;
static 조합상태 조합,batli_REKODI[16];
static unsigned 기록수;
void 원격글쇠확정(void){memset(&조합,0,sizeof(조합));기록수=0;}
void 원격글쇠초기화(void){udhibiti_thamani=kibonye_SHIFT=한글=0;원격글쇠확정();}
static void 글넣기(unsigned thamani){
    unsigned char SMS[4];unsigned 수;
    if(thamani<128){SMS[0]=thamani;수=1;}else if(thamani<2048){SMS[0]=0xc0|(thamani>>6);SMS[1]=0x80|(thamani&63);수=2;}
    else if(thamani<65536){SMS[0]=0xe0|(thamani>>12);SMS[1]=0x80|((thamani>>6)&63);SMS[2]=0x80|(thamani&63);수=3;}
    else{SMS[0]=0xf0|(thamani>>18);SMS[1]=0x80|((thamani>>12)&63);SMS[2]=0x80|((thamani>>6)&63);SMS[3]=0x80|(thamani&63);수=4;}
    원격입력넣기(SMS,수);
}
static int gundua_ingizo(const unsigned *ingizo_Orodha,unsigned 수,unsigned thamani){for(unsigned 순번=0;순번<수;순번++)if(ingizo_Orodha[순번]==thamani)return 순번;return -1;}
static unsigned 겹찾기(const unsigned 표[][3],unsigned 수,unsigned 가,unsigned 나){for(unsigned 순번=0;순번<수;순번++)if(표[순번][0]==가&&표[순번][1]==나)return 표[순번][2];return 0;}
static unsigned 조합글(void){
    if(조합.첫&&조합.가운데)return 0xac00+(gundua_ingizo(첫소리목록,19,조합.첫)*21+gundua_ingizo(가운뎃소리목록,21,조합.가운데))*28+(조합.끝?gundua_ingizo(끝소리목록,28,조합.끝):0);
    return 조합.첫?조합.첫:조합.가운데;
}
static int 한글넣기(unsigned 글쇠){
    unsigned 자모=0;for(unsigned 순번=0;순번<sizeof(Kitufe_Muundo)/sizeof(Kitufe_Muundo[0]);순번++)if(Kitufe_Muundo[순번][0]==글쇠)자모=Kitufe_Muundo[순번][1];
    if(!자모&&글쇠>='A'&&글쇠<='Z')return 한글넣기(글쇠+32);if(!자모)return 0;
    unsigned 이전=조합글(),확정=0;조합상태 전=조합;
    if(기록수<16)batli_REKODI[기록수++]=전;
    if(gundua_ingizo(첫소리목록,19,자모)>=0){
        if(조합.첫&&조합.가운데&&!조합.끝&&gundua_ingizo(끝소리목록,28,자모)>=0)조합.끝=자모;
        else{unsigned tandazo_thamani=겹찾기(겹끝소리,11,조합.끝,자모);if(조합.끝&&tandazo_thamani)조합.끝=tandazo_thamani;
            else{확정=이전;원격글쇠확정();조합.첫=자모;기록수=1;memset(batli_REKODI,0,sizeof(조합상태));}}
    }else if(조합.끝){
        unsigned 왼쪽=0,오른쪽=조합.끝;for(unsigned 순번=0;순번<11;순번++)if(겹끝소리[순번][2]==조합.끝){왼쪽=겹끝소리[순번][0];오른쪽=겹끝소리[순번][1];break;}
        조합.끝=왼쪽;확정=조합글();원격글쇠확정();조합.첫=오른쪽;조합.가운데=자모;기록수=2;
        memset(batli_REKODI,0,2*sizeof(조합상태));batli_REKODI[1].첫=오른쪽;
    }else if(조합.가운데){unsigned tandazo_thamani=겹찾기(겹가운뎃소리,7,조합.가운데,자모);
        if(tandazo_thamani)조합.가운데=tandazo_thamani;else{확정=이전;원격글쇠확정();조합.가운데=자모;기록수=1;memset(batli_REKODI,0,sizeof(조합상태));}
    }else 조합.가운데=자모;
    if(이전)글넣기(127);if(확정)글넣기(확정);unsigned SASA_thamani=조합글();if(SASA_thamani)글넣기(SASA_thamani);return 1;
}
void 원격글쇠(unsigned ishara,int 누름){
    if(ishara==0xffe3||ishara==0xffe4){udhibiti_thamani=누름;return;}
    if(ishara==0xffe1||ishara==0xffe2){kibonye_SHIFT=누름;return;}
    if(!누름)return;
    if(ishara==0xffc6||ishara==0xff31||(ishara==32&&kibonye_SHIFT&&!udhibiti_thamani)){
        원격글쇠확정();한글=!한글;unsigned char tukio[]={30,3,한글,0,0,0,0};원격입력넣기(tukio,7);return;
    }
    if(ishara==0xff08&&한글&&!udhibiti_thamani&&기록수){조합=batli_REKODI[--기록수];글넣기(127);unsigned SMS=조합글();if(SMS)글넣기(SMS);return;}
    if(한글&&!udhibiti_thamani&&ishara<128&&한글넣기(ishara))return;
    원격글쇠확정();
    if((udhibiti_thamani&&kibonye_SHIFT&&(ishara=='t'||ishara=='T'))||ishara==0xffc3||ishara==0xffc9){unsigned char tukio[]={30,2,ishara==0xffc3?2:ishara==0xffc9?3:1,0,0,0,0};원격입력넣기(tukio,7);return;}
    const char *특수=ishara==0xff08?"\177":ishara==0xff09?"\t":ishara==0xff0d?"\r":ishara==0xff1b?"\033":
        ishara==0xffff?"\033[3~":ishara==0xff50?"\033[H":ishara==0xff57?"\033[F":ishara==0xff51?"\033[D":
        ishara==0xff52?"\033[A":ishara==0xff53?"\033[C":ishara==0xff54?"\033[B":ishara==0xff55?"\033[5~":ishara==0xff56?"\033[6~":0;
    if(특수){원격입력넣기((const unsigned char*)특수,strlen(특수));return;}
    unsigned thamani=(ishara&0xff000000)==0x01000000?ishara&0xffffff:ishara;
    if(thamani>0x10ffff||(thamani>=0xd800&&thamani<=0xdfff)||(ishara>=0xff00&&ishara<0x1000000))return;
    if(udhibiti_thamani){if(thamani>='a'&&thamani<='z')thamani-=96;else if(thamani>='A'&&thamani<='Z')thamani-=64;}
    글넣기(thamani);
}
