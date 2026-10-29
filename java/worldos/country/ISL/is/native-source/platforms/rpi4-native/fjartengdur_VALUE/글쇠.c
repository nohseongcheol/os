#include "fjartengdur_VALUE.h"
#include <string.h>
#include "두벌식표.h"
static unsigned stýring_VALUE,SHIFT_lykill,한글;
typedef struct {unsigned 첫,가운데,끝;} samsetning_staða;
static samsetning_staða samsetning_VALUE,LOG_lína[16];
static unsigned LOG_COUNT;
void 원격글쇠확정(void){memset(&samsetning_VALUE,0,sizeof(samsetning_VALUE));LOG_COUNT=0;}
void 원격글쇠초기화(void){stýring_VALUE=SHIFT_lykill=한글=0;원격글쇠확정();}
static void 글넣기(unsigned VALUE){
    unsigned char Texti[4];unsigned númer;
    if(VALUE<128){Texti[0]=VALUE;númer=1;}else if(VALUE<2048){Texti[0]=0xc0|(VALUE>>6);Texti[1]=0x80|(VALUE&63);númer=2;}
    else if(VALUE<65536){Texti[0]=0xe0|(VALUE>>12);Texti[1]=0x80|((VALUE>>6)&63);Texti[2]=0x80|(VALUE&63);númer=3;}
    else{Texti[0]=0xf0|(VALUE>>18);Texti[1]=0x80|((VALUE>>12)&63);Texti[2]=0x80|((VALUE>>6)&63);Texti[3]=0x80|(VALUE&63);númer=4;}
    원격입력넣기(Texti,númer);
}
static int FIND_færsla(const unsigned *færsla_Listi,unsigned númer,unsigned VALUE){for(unsigned 순번=0;순번<númer;순번++)if(færsla_Listi[순번]==VALUE)return 순번;return -1;}
static unsigned 겹찾기(const unsigned LOOKUP_tafla[][3],unsigned númer,unsigned 가,unsigned 나){for(unsigned 순번=0;순번<númer;순번++)if(LOOKUP_tafla[순번][0]==가&&LOOKUP_tafla[순번][1]==나)return LOOKUP_tafla[순번][2];return 0;}
static unsigned 조합글(void){
    if(samsetning_VALUE.첫&&samsetning_VALUE.가운데)return 0xac00+(FIND_færsla(첫소리목록,19,samsetning_VALUE.첫)*21+FIND_færsla(가운뎃소리목록,21,samsetning_VALUE.가운데))*28+(samsetning_VALUE.끝?FIND_færsla(끝소리목록,28,samsetning_VALUE.끝):0);
    return samsetning_VALUE.첫?samsetning_VALUE.첫:samsetning_VALUE.가운데;
}
static int 한글넣기(unsigned 글쇠){
    unsigned 자모=0;for(unsigned 순번=0;순번<sizeof(Lykill_útlit)/sizeof(Lykill_útlit[0]);순번++)if(Lykill_útlit[순번][0]==글쇠)자모=Lykill_útlit[순번][1];
    if(!자모&&글쇠>='A'&&글쇠<='Z')return 한글넣기(글쇠+32);if(!자모)return 0;
    unsigned 이전=조합글(),확정=0;samsetning_staða 전=samsetning_VALUE;
    if(LOG_COUNT<16)LOG_lína[LOG_COUNT++]=전;
    if(FIND_færsla(첫소리목록,19,자모)>=0){
        if(samsetning_VALUE.첫&&samsetning_VALUE.가운데&&!samsetning_VALUE.끝&&FIND_færsla(끝소리목록,28,자모)>=0)samsetning_VALUE.끝=자모;
        else{unsigned yfirlögn_VALUE=겹찾기(겹끝소리,11,samsetning_VALUE.끝,자모);if(samsetning_VALUE.끝&&yfirlögn_VALUE)samsetning_VALUE.끝=yfirlögn_VALUE;
            else{확정=이전;원격글쇠확정();samsetning_VALUE.첫=자모;LOG_COUNT=1;memset(LOG_lína,0,sizeof(samsetning_staða));}}
    }else if(samsetning_VALUE.끝){
        unsigned 왼쪽=0,RIGHT=samsetning_VALUE.끝;for(unsigned 순번=0;순번<11;순번++)if(겹끝소리[순번][2]==samsetning_VALUE.끝){왼쪽=겹끝소리[순번][0];RIGHT=겹끝소리[순번][1];break;}
        samsetning_VALUE.끝=왼쪽;확정=조합글();원격글쇠확정();samsetning_VALUE.첫=RIGHT;samsetning_VALUE.가운데=자모;LOG_COUNT=2;
        memset(LOG_lína,0,2*sizeof(samsetning_staða));LOG_lína[1].첫=RIGHT;
    }else if(samsetning_VALUE.가운데){unsigned yfirlögn_VALUE=겹찾기(겹가운뎃소리,7,samsetning_VALUE.가운데,자모);
        if(yfirlögn_VALUE)samsetning_VALUE.가운데=yfirlögn_VALUE;else{확정=이전;원격글쇠확정();samsetning_VALUE.가운데=자모;LOG_COUNT=1;memset(LOG_lína,0,sizeof(samsetning_staða));}
    }else samsetning_VALUE.가운데=자모;
    if(이전)글넣기(127);if(확정)글넣기(확정);unsigned NOW_VALUE=조합글();if(NOW_VALUE)글넣기(NOW_VALUE);return 1;
}
void 원격글쇠(unsigned tákn,int ýta_VALUE){
    if(tákn==0xffe3||tákn==0xffe4){stýring_VALUE=ýta_VALUE;return;}
    if(tákn==0xffe1||tákn==0xffe2){SHIFT_lykill=ýta_VALUE;return;}
    if(!ýta_VALUE)return;
    if(tákn==0xffc6||tákn==0xff31||(tákn==32&&SHIFT_lykill&&!stýring_VALUE)){
        원격글쇠확정();한글=!한글;unsigned char atvik[]={30,3,한글,0,0,0,0};원격입력넣기(atvik,7);return;
    }
    if(tákn==0xff08&&한글&&!stýring_VALUE&&LOG_COUNT){samsetning_VALUE=LOG_lína[--LOG_COUNT];글넣기(127);unsigned Texti=조합글();if(Texti)글넣기(Texti);return;}
    if(한글&&!stýring_VALUE&&tákn<128&&한글넣기(tákn))return;
    원격글쇠확정();
    if((stýring_VALUE&&SHIFT_lykill&&(tákn=='t'||tákn=='T'))||tákn==0xffc3||tákn==0xffc9){unsigned char atvik[]={30,2,tákn==0xffc3?2:tákn==0xffc9?3:1,0,0,0,0};원격입력넣기(atvik,7);return;}
    const char *특수=tákn==0xff08?"\177":tákn==0xff09?"\t":tákn==0xff0d?"\r":tákn==0xff1b?"\033":
        tákn==0xffff?"\033[3~":tákn==0xff50?"\033[H":tákn==0xff57?"\033[F":tákn==0xff51?"\033[D":
        tákn==0xff52?"\033[A":tákn==0xff53?"\033[C":tákn==0xff54?"\033[B":tákn==0xff55?"\033[5~":tákn==0xff56?"\033[6~":0;
    if(특수){원격입력넣기((const unsigned char*)특수,strlen(특수));return;}
    unsigned VALUE=(tákn&0xff000000)==0x01000000?tákn&0xffffff:tákn;
    if(VALUE>0x10ffff||(VALUE>=0xd800&&VALUE<=0xdfff)||(tákn>=0xff00&&tákn<0x1000000))return;
    if(stýring_VALUE){if(VALUE>='a'&&VALUE<='z')VALUE-=96;else if(VALUE>='A'&&VALUE<='Z')VALUE-=64;}
    글넣기(VALUE);
}
