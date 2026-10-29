#include "pell_VALUE.h"
#include <string.h>
#include "두벌식표.h"
static unsigned rheoli_VALUE,bysell_SHIFT,한글;
typedef struct {unsigned 첫,가운데,끝;} 조합상태;
static 조합상태 조합,LOG_rhes[16];
static unsigned LOG_COUNT;
void 원격글쇠확정(void){memset(&조합,0,sizeof(조합));LOG_COUNT=0;}
void 원격글쇠초기화(void){rheoli_VALUE=bysell_SHIFT=한글=0;원격글쇠확정();}
static void 글넣기(unsigned VALUE){
    unsigned char Testun[4];unsigned 수;
    if(VALUE<128){Testun[0]=VALUE;수=1;}else if(VALUE<2048){Testun[0]=0xc0|(VALUE>>6);Testun[1]=0x80|(VALUE&63);수=2;}
    else if(VALUE<65536){Testun[0]=0xe0|(VALUE>>12);Testun[1]=0x80|((VALUE>>6)&63);Testun[2]=0x80|(VALUE&63);수=3;}
    else{Testun[0]=0xf0|(VALUE>>18);Testun[1]=0x80|((VALUE>>12)&63);Testun[2]=0x80|((VALUE>>6)&63);Testun[3]=0x80|(VALUE&63);수=4;}
    원격입력넣기(Testun,수);
}
static int FIND_cofnod(const unsigned *cofnod_Rhestr,unsigned 수,unsigned VALUE){for(unsigned 순번=0;순번<수;순번++)if(cofnod_Rhestr[순번]==VALUE)return 순번;return -1;}
static unsigned 겹찾기(const unsigned LOOKUP_tabl[][3],unsigned 수,unsigned 가,unsigned 나){for(unsigned 순번=0;순번<수;순번++)if(LOOKUP_tabl[순번][0]==가&&LOOKUP_tabl[순번][1]==나)return LOOKUP_tabl[순번][2];return 0;}
static unsigned 조합글(void){
    if(조합.첫&&조합.가운데)return 0xac00+(FIND_cofnod(첫소리목록,19,조합.첫)*21+FIND_cofnod(가운뎃소리목록,21,조합.가운데))*28+(조합.끝?FIND_cofnod(끝소리목록,28,조합.끝):0);
    return 조합.첫?조합.첫:조합.가운데;
}
static int 한글넣기(unsigned 글쇠){
    unsigned 자모=0;for(unsigned 순번=0;순번<sizeof(bysell_Llywio)/sizeof(bysell_Llywio[0]);순번++)if(bysell_Llywio[순번][0]==글쇠)자모=bysell_Llywio[순번][1];
    if(!자모&&글쇠>='A'&&글쇠<='Z')return 한글넣기(글쇠+32);if(!자모)return 0;
    unsigned 이전=조합글(),확정=0;조합상태 전=조합;
    if(LOG_COUNT<16)LOG_rhes[LOG_COUNT++]=전;
    if(FIND_cofnod(첫소리목록,19,자모)>=0){
        if(조합.첫&&조합.가운데&&!조합.끝&&FIND_cofnod(끝소리목록,28,자모)>=0)조합.끝=자모;
        else{unsigned troshaen_VALUE=겹찾기(겹끝소리,11,조합.끝,자모);if(조합.끝&&troshaen_VALUE)조합.끝=troshaen_VALUE;
            else{확정=이전;원격글쇠확정();조합.첫=자모;LOG_COUNT=1;memset(LOG_rhes,0,sizeof(조합상태));}}
    }else if(조합.끝){
        unsigned 왼쪽=0,RIGHT=조합.끝;for(unsigned 순번=0;순번<11;순번++)if(겹끝소리[순번][2]==조합.끝){왼쪽=겹끝소리[순번][0];RIGHT=겹끝소리[순번][1];break;}
        조합.끝=왼쪽;확정=조합글();원격글쇠확정();조합.첫=RIGHT;조합.가운데=자모;LOG_COUNT=2;
        memset(LOG_rhes,0,2*sizeof(조합상태));LOG_rhes[1].첫=RIGHT;
    }else if(조합.가운데){unsigned troshaen_VALUE=겹찾기(겹가운뎃소리,7,조합.가운데,자모);
        if(troshaen_VALUE)조합.가운데=troshaen_VALUE;else{확정=이전;원격글쇠확정();조합.가운데=자모;LOG_COUNT=1;memset(LOG_rhes,0,sizeof(조합상태));}
    }else 조합.가운데=자모;
    if(이전)글넣기(127);if(확정)글넣기(확정);unsigned NOW_VALUE=조합글();if(NOW_VALUE)글넣기(NOW_VALUE);return 1;
}
void 원격글쇠(unsigned symbol,int pwyso_VALUE){
    if(symbol==0xffe3||symbol==0xffe4){rheoli_VALUE=pwyso_VALUE;return;}
    if(symbol==0xffe1||symbol==0xffe2){bysell_SHIFT=pwyso_VALUE;return;}
    if(!pwyso_VALUE)return;
    if(symbol==0xffc6||symbol==0xff31||(symbol==32&&bysell_SHIFT&&!rheoli_VALUE)){
        원격글쇠확정();한글=!한글;unsigned char digwyddiad[]={30,3,한글,0,0,0,0};원격입력넣기(digwyddiad,7);return;
    }
    if(symbol==0xff08&&한글&&!rheoli_VALUE&&LOG_COUNT){조합=LOG_rhes[--LOG_COUNT];글넣기(127);unsigned Testun=조합글();if(Testun)글넣기(Testun);return;}
    if(한글&&!rheoli_VALUE&&symbol<128&&한글넣기(symbol))return;
    원격글쇠확정();
    if((rheoli_VALUE&&bysell_SHIFT&&(symbol=='t'||symbol=='T'))||symbol==0xffc3||symbol==0xffc9){unsigned char digwyddiad[]={30,2,symbol==0xffc3?2:symbol==0xffc9?3:1,0,0,0,0};원격입력넣기(digwyddiad,7);return;}
    const char *특수=symbol==0xff08?"\177":symbol==0xff09?"\t":symbol==0xff0d?"\r":symbol==0xff1b?"\033":
        symbol==0xffff?"\033[3~":symbol==0xff50?"\033[H":symbol==0xff57?"\033[F":symbol==0xff51?"\033[D":
        symbol==0xff52?"\033[A":symbol==0xff53?"\033[C":symbol==0xff54?"\033[B":symbol==0xff55?"\033[5~":symbol==0xff56?"\033[6~":0;
    if(특수){원격입력넣기((const unsigned char*)특수,strlen(특수));return;}
    unsigned VALUE=(symbol&0xff000000)==0x01000000?symbol&0xffffff:symbol;
    if(VALUE>0x10ffff||(VALUE>=0xd800&&VALUE<=0xdfff)||(symbol>=0xff00&&symbol<0x1000000))return;
    if(rheoli_VALUE){if(VALUE>='a'&&VALUE<='z')VALUE-=96;else if(VALUE>='A'&&VALUE<='Z')VALUE-=64;}
    글넣기(VALUE);
}
