#include "afstands_VALUE.h"
#include <string.h>
#include "두벌식표.h"
static unsigned kontrole_VALUE,SHIFT_sleutel,한글;
typedef struct {unsigned 첫,가운데,끝;} 조합상태;
static 조합상태 조합,LOG_ry[16];
static unsigned LOG_COUNT;
void 원격글쇠확정(void){memset(&조합,0,sizeof(조합));LOG_COUNT=0;}
void 원격글쇠초기화(void){kontrole_VALUE=SHIFT_sleutel=한글=0;원격글쇠확정();}
static void 글넣기(unsigned VALUE){
    unsigned char Teks[4];unsigned 수;
    if(VALUE<128){Teks[0]=VALUE;수=1;}else if(VALUE<2048){Teks[0]=0xc0|(VALUE>>6);Teks[1]=0x80|(VALUE&63);수=2;}
    else if(VALUE<65536){Teks[0]=0xe0|(VALUE>>12);Teks[1]=0x80|((VALUE>>6)&63);Teks[2]=0x80|(VALUE&63);수=3;}
    else{Teks[0]=0xf0|(VALUE>>18);Teks[1]=0x80|((VALUE>>12)&63);Teks[2]=0x80|((VALUE>>6)&63);Teks[3]=0x80|(VALUE&63);수=4;}
    원격입력넣기(Teks,수);
}
static int FIND_inskrywing(const unsigned *inskrywing_Lys,unsigned 수,unsigned VALUE){for(unsigned 순번=0;순번<수;순번++)if(inskrywing_Lys[순번]==VALUE)return 순번;return -1;}
static unsigned 겹찾기(const unsigned LOOKUP_tabel[][3],unsigned 수,unsigned 가,unsigned 나){for(unsigned 순번=0;순번<수;순번++)if(LOOKUP_tabel[순번][0]==가&&LOOKUP_tabel[순번][1]==나)return LOOKUP_tabel[순번][2];return 0;}
static unsigned 조합글(void){
    if(조합.첫&&조합.가운데)return 0xac00+(FIND_inskrywing(첫소리목록,19,조합.첫)*21+FIND_inskrywing(가운뎃소리목록,21,조합.가운데))*28+(조합.끝?FIND_inskrywing(끝소리목록,28,조합.끝):0);
    return 조합.첫?조합.첫:조합.가운데;
}
static int 한글넣기(unsigned 글쇠){
    unsigned 자모=0;for(unsigned 순번=0;순번<sizeof(Sleutel_Uitleg)/sizeof(Sleutel_Uitleg[0]);순번++)if(Sleutel_Uitleg[순번][0]==글쇠)자모=Sleutel_Uitleg[순번][1];
    if(!자모&&글쇠>='A'&&글쇠<='Z')return 한글넣기(글쇠+32);if(!자모)return 0;
    unsigned 이전=조합글(),확정=0;조합상태 전=조합;
    if(LOG_COUNT<16)LOG_ry[LOG_COUNT++]=전;
    if(FIND_inskrywing(첫소리목록,19,자모)>=0){
        if(조합.첫&&조합.가운데&&!조합.끝&&FIND_inskrywing(끝소리목록,28,자모)>=0)조합.끝=자모;
        else{unsigned oorlegging_VALUE=겹찾기(겹끝소리,11,조합.끝,자모);if(조합.끝&&oorlegging_VALUE)조합.끝=oorlegging_VALUE;
            else{확정=이전;원격글쇠확정();조합.첫=자모;LOG_COUNT=1;memset(LOG_ry,0,sizeof(조합상태));}}
    }else if(조합.끝){
        unsigned 왼쪽=0,RIGHT=조합.끝;for(unsigned 순번=0;순번<11;순번++)if(겹끝소리[순번][2]==조합.끝){왼쪽=겹끝소리[순번][0];RIGHT=겹끝소리[순번][1];break;}
        조합.끝=왼쪽;확정=조합글();원격글쇠확정();조합.첫=RIGHT;조합.가운데=자모;LOG_COUNT=2;
        memset(LOG_ry,0,2*sizeof(조합상태));LOG_ry[1].첫=RIGHT;
    }else if(조합.가운데){unsigned oorlegging_VALUE=겹찾기(겹가운뎃소리,7,조합.가운데,자모);
        if(oorlegging_VALUE)조합.가운데=oorlegging_VALUE;else{확정=이전;원격글쇠확정();조합.가운데=자모;LOG_COUNT=1;memset(LOG_ry,0,sizeof(조합상태));}
    }else 조합.가운데=자모;
    if(이전)글넣기(127);if(확정)글넣기(확정);unsigned NOU_VALUE=조합글();if(NOU_VALUE)글넣기(NOU_VALUE);return 1;
}
void 원격글쇠(unsigned simbool,int druk_VALUE){
    if(simbool==0xffe3||simbool==0xffe4){kontrole_VALUE=druk_VALUE;return;}
    if(simbool==0xffe1||simbool==0xffe2){SHIFT_sleutel=druk_VALUE;return;}
    if(!druk_VALUE)return;
    if(simbool==0xffc6||simbool==0xff31||(simbool==32&&SHIFT_sleutel&&!kontrole_VALUE)){
        원격글쇠확정();한글=!한글;unsigned char gebeurtenis[]={30,3,한글,0,0,0,0};원격입력넣기(gebeurtenis,7);return;
    }
    if(simbool==0xff08&&한글&&!kontrole_VALUE&&LOG_COUNT){조합=LOG_ry[--LOG_COUNT];글넣기(127);unsigned Teks=조합글();if(Teks)글넣기(Teks);return;}
    if(한글&&!kontrole_VALUE&&simbool<128&&한글넣기(simbool))return;
    원격글쇠확정();
    if((kontrole_VALUE&&SHIFT_sleutel&&(simbool=='t'||simbool=='T'))||simbool==0xffc3||simbool==0xffc9){unsigned char gebeurtenis[]={30,2,simbool==0xffc3?2:simbool==0xffc9?3:1,0,0,0,0};원격입력넣기(gebeurtenis,7);return;}
    const char *특수=simbool==0xff08?"\177":simbool==0xff09?"\t":simbool==0xff0d?"\r":simbool==0xff1b?"\033":
        simbool==0xffff?"\033[3~":simbool==0xff50?"\033[H":simbool==0xff57?"\033[F":simbool==0xff51?"\033[D":
        simbool==0xff52?"\033[A":simbool==0xff53?"\033[C":simbool==0xff54?"\033[B":simbool==0xff55?"\033[5~":simbool==0xff56?"\033[6~":0;
    if(특수){원격입력넣기((const unsigned char*)특수,strlen(특수));return;}
    unsigned VALUE=(simbool&0xff000000)==0x01000000?simbool&0xffffff:simbool;
    if(VALUE>0x10ffff||(VALUE>=0xd800&&VALUE<=0xdfff)||(simbool>=0xff00&&simbool<0x1000000))return;
    if(kontrole_VALUE){if(VALUE>='a'&&VALUE<='z')VALUE-=96;else if(VALUE>='A'&&VALUE<='Z')VALUE-=64;}
    글넣기(VALUE);
}
