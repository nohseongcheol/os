#include "читтәге_VALUE.h"
#include <string.h>
#include "두벌식표.h"
static unsigned идарә_VALUE,SHIFT_төймәсе,한글;
typedef struct {unsigned 첫,가운데,끝;} 조합상태;
static 조합상태 조합,LOG_юл[16];
static unsigned LOG_COUNT;
void 원격글쇠확정(void){memset(&조합,0,sizeof(조합));LOG_COUNT=0;}
void 원격글쇠초기화(void){идарә_VALUE=SHIFT_төймәсе=한글=0;원격글쇠확정();}
static void 글넣기(unsigned VALUE){
    unsigned char Mäten[4];unsigned 수;
    if(VALUE<128){Mäten[0]=VALUE;수=1;}else if(VALUE<2048){Mäten[0]=0xc0|(VALUE>>6);Mäten[1]=0x80|(VALUE&63);수=2;}
    else if(VALUE<65536){Mäten[0]=0xe0|(VALUE>>12);Mäten[1]=0x80|((VALUE>>6)&63);Mäten[2]=0x80|(VALUE&63);수=3;}
    else{Mäten[0]=0xf0|(VALUE>>18);Mäten[1]=0x80|((VALUE>>12)&63);Mäten[2]=0x80|((VALUE>>6)&63);Mäten[3]=0x80|(VALUE&63);수=4;}
    원격입력넣기(Mäten,수);
}
static int FIND_кертү(const unsigned *кертү_Исемлек,unsigned 수,unsigned VALUE){for(unsigned 순번=0;순번<수;순번++)if(кертү_Исемлек[순번]==VALUE)return 순번;return -1;}
static unsigned 겹찾기(const unsigned Эзләү_таблица[][3],unsigned 수,unsigned 가,unsigned 나){for(unsigned 순번=0;순번<수;순번++)if(Эзләү_таблица[순번][0]==가&&Эзләү_таблица[순번][1]==나)return Эзләү_таблица[순번][2];return 0;}
static unsigned 조합글(void){
    if(조합.첫&&조합.가운데)return 0xac00+(FIND_кертү(첫소리목록,19,조합.첫)*21+FIND_кертү(가운뎃소리목록,21,조합.가운데))*28+(조합.끝?FIND_кертү(끝소리목록,28,조합.끝):0);
    return 조합.첫?조합.첫:조합.가운데;
}
static int 한글넣기(unsigned 글쇠){
    unsigned 자모=0;for(unsigned 순번=0;순번<sizeof(ачкыч_план)/sizeof(ачкыч_план[0]);순번++)if(ачкыч_план[순번][0]==글쇠)자모=ачкыч_план[순번][1];
    if(!자모&&글쇠>='A'&&글쇠<='Z')return 한글넣기(글쇠+32);if(!자모)return 0;
    unsigned 이전=조합글(),확정=0;조합상태 전=조합;
    if(LOG_COUNT<16)LOG_юл[LOG_COUNT++]=전;
    if(FIND_кертү(첫소리목록,19,자모)>=0){
        if(조합.첫&&조합.가운데&&!조합.끝&&FIND_кертү(끝소리목록,28,자모)>=0)조합.끝=자모;
        else{unsigned каплаучы_элемент_VALUE=겹찾기(겹끝소리,11,조합.끝,자모);if(조합.끝&&каплаучы_элемент_VALUE)조합.끝=каплаучы_элемент_VALUE;
            else{확정=이전;원격글쇠확정();조합.첫=자모;LOG_COUNT=1;memset(LOG_юл,0,sizeof(조합상태));}}
    }else if(조합.끝){
        unsigned 왼쪽=0,RIGHT=조합.끝;for(unsigned 순번=0;순번<11;순번++)if(겹끝소리[순번][2]==조합.끝){왼쪽=겹끝소리[순번][0];RIGHT=겹끝소리[순번][1];break;}
        조합.끝=왼쪽;확정=조합글();원격글쇠확정();조합.첫=RIGHT;조합.가운데=자모;LOG_COUNT=2;
        memset(LOG_юл,0,2*sizeof(조합상태));LOG_юл[1].첫=RIGHT;
    }else if(조합.가운데){unsigned каплаучы_элемент_VALUE=겹찾기(겹가운뎃소리,7,조합.가운데,자모);
        if(каплаучы_элемент_VALUE)조합.가운데=каплаучы_элемент_VALUE;else{확정=이전;원격글쇠확정();조합.가운데=자모;LOG_COUNT=1;memset(LOG_юл,0,sizeof(조합상태));}
    }else 조합.가운데=자모;
    if(이전)글넣기(127);if(확정)글넣기(확정);unsigned NOW_VALUE=조합글();if(NOW_VALUE)글넣기(NOW_VALUE);return 1;
}
void 원격글쇠(unsigned символ,int 누름){
    if(символ==0xffe3||символ==0xffe4){идарә_VALUE=누름;return;}
    if(символ==0xffe1||символ==0xffe2){SHIFT_төймәсе=누름;return;}
    if(!누름)return;
    if(символ==0xffc6||символ==0xff31||(символ==32&&SHIFT_төймәсе&&!идарә_VALUE)){
        원격글쇠확정();한글=!한글;unsigned char вакыйга[]={30,3,한글,0,0,0,0};원격입력넣기(вакыйга,7);return;
    }
    if(символ==0xff08&&한글&&!идарә_VALUE&&LOG_COUNT){조합=LOG_юл[--LOG_COUNT];글넣기(127);unsigned Mäten=조합글();if(Mäten)글넣기(Mäten);return;}
    if(한글&&!идарә_VALUE&&символ<128&&한글넣기(символ))return;
    원격글쇠확정();
    if((идарә_VALUE&&SHIFT_төймәсе&&(символ=='t'||символ=='T'))||символ==0xffc3||символ==0xffc9){unsigned char вакыйга[]={30,2,символ==0xffc3?2:символ==0xffc9?3:1,0,0,0,0};원격입력넣기(вакыйга,7);return;}
    const char *특수=символ==0xff08?"\177":символ==0xff09?"\t":символ==0xff0d?"\r":символ==0xff1b?"\033":
        символ==0xffff?"\033[3~":символ==0xff50?"\033[H":символ==0xff57?"\033[F":символ==0xff51?"\033[D":
        символ==0xff52?"\033[A":символ==0xff53?"\033[C":символ==0xff54?"\033[B":символ==0xff55?"\033[5~":символ==0xff56?"\033[6~":0;
    if(특수){원격입력넣기((const unsigned char*)특수,strlen(특수));return;}
    unsigned VALUE=(символ&0xff000000)==0x01000000?символ&0xffffff:символ;
    if(VALUE>0x10ffff||(VALUE>=0xd800&&VALUE<=0xdfff)||(символ>=0xff00&&символ<0x1000000))return;
    if(идарә_VALUE){if(VALUE>='a'&&VALUE<='z')VALUE-=96;else if(VALUE>='A'&&VALUE<='Z')VALUE-=64;}
    글넣기(VALUE);
}
