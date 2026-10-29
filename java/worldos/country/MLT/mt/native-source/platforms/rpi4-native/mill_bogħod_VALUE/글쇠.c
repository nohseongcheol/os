#include "mill_bogħod_VALUE.h"
#include <string.h>
#include "두벌식표.h"
static unsigned kontroll_VALUE,tast_SHIFT,한글;
typedef struct {unsigned 첫,가운데,끝;} 조합상태;
static 조합상태 조합,LOG_RECORD[16];
static unsigned LOG_COUNT;
void 원격글쇠확정(void){memset(&조합,0,sizeof(조합));LOG_COUNT=0;}
void 원격글쇠초기화(void){kontroll_VALUE=tast_SHIFT=한글=0;원격글쇠확정();}
static void 글넣기(unsigned VALUE){
    unsigned char SMS[4];unsigned 수;
    if(VALUE<128){SMS[0]=VALUE;수=1;}else if(VALUE<2048){SMS[0]=0xc0|(VALUE>>6);SMS[1]=0x80|(VALUE&63);수=2;}
    else if(VALUE<65536){SMS[0]=0xe0|(VALUE>>12);SMS[1]=0x80|((VALUE>>6)&63);SMS[2]=0x80|(VALUE&63);수=3;}
    else{SMS[0]=0xf0|(VALUE>>18);SMS[1]=0x80|((VALUE>>12)&63);SMS[2]=0x80|((VALUE>>6)&63);SMS[3]=0x80|(VALUE&63);수=4;}
    원격입력넣기(SMS,수);
}
static int sab_entrata(const unsigned *entrata_Lista,unsigned 수,unsigned VALUE){for(unsigned 순번=0;순번<수;순번++)if(entrata_Lista[순번]==VALUE)return 순번;return -1;}
static unsigned 겹찾기(const unsigned LOOKUP_tabella[][3],unsigned 수,unsigned 가,unsigned 나){for(unsigned 순번=0;순번<수;순번++)if(LOOKUP_tabella[순번][0]==가&&LOOKUP_tabella[순번][1]==나)return LOOKUP_tabella[순번][2];return 0;}
static unsigned 조합글(void){
    if(조합.첫&&조합.가운데)return 0xac00+(sab_entrata(첫소리목록,19,조합.첫)*21+sab_entrata(가운뎃소리목록,21,조합.가운데))*28+(조합.끝?sab_entrata(끝소리목록,28,조합.끝):0);
    return 조합.첫?조합.첫:조합.가운데;
}
static int 한글넣기(unsigned 글쇠){
    unsigned 자모=0;for(unsigned 순번=0;순번<sizeof(tast_Tqassim)/sizeof(tast_Tqassim[0]);순번++)if(tast_Tqassim[순번][0]==글쇠)자모=tast_Tqassim[순번][1];
    if(!자모&&글쇠>='A'&&글쇠<='Z')return 한글넣기(글쇠+32);if(!자모)return 0;
    unsigned 이전=조합글(),확정=0;조합상태 전=조합;
    if(LOG_COUNT<16)LOG_RECORD[LOG_COUNT++]=전;
    if(sab_entrata(첫소리목록,19,자모)>=0){
        if(조합.첫&&조합.가운데&&!조합.끝&&sab_entrata(끝소리목록,28,자모)>=0)조합.끝=자모;
        else{unsigned sovrapożizzjoni_VALUE=겹찾기(겹끝소리,11,조합.끝,자모);if(조합.끝&&sovrapożizzjoni_VALUE)조합.끝=sovrapożizzjoni_VALUE;
            else{확정=이전;원격글쇠확정();조합.첫=자모;LOG_COUNT=1;memset(LOG_RECORD,0,sizeof(조합상태));}}
    }else if(조합.끝){
        unsigned 왼쪽=0,RIGHT=조합.끝;for(unsigned 순번=0;순번<11;순번++)if(겹끝소리[순번][2]==조합.끝){왼쪽=겹끝소리[순번][0];RIGHT=겹끝소리[순번][1];break;}
        조합.끝=왼쪽;확정=조합글();원격글쇠확정();조합.첫=RIGHT;조합.가운데=자모;LOG_COUNT=2;
        memset(LOG_RECORD,0,2*sizeof(조합상태));LOG_RECORD[1].첫=RIGHT;
    }else if(조합.가운데){unsigned sovrapożizzjoni_VALUE=겹찾기(겹가운뎃소리,7,조합.가운데,자모);
        if(sovrapożizzjoni_VALUE)조합.가운데=sovrapożizzjoni_VALUE;else{확정=이전;원격글쇠확정();조합.가운데=자모;LOG_COUNT=1;memset(LOG_RECORD,0,sizeof(조합상태));}
    }else 조합.가운데=자모;
    if(이전)글넣기(127);if(확정)글넣기(확정);unsigned NOW_VALUE=조합글();if(NOW_VALUE)글넣기(NOW_VALUE);return 1;
}
void 원격글쇠(unsigned simbolu,int 누름){
    if(simbolu==0xffe3||simbolu==0xffe4){kontroll_VALUE=누름;return;}
    if(simbolu==0xffe1||simbolu==0xffe2){tast_SHIFT=누름;return;}
    if(!누름)return;
    if(simbolu==0xffc6||simbolu==0xff31||(simbolu==32&&tast_SHIFT&&!kontroll_VALUE)){
        원격글쇠확정();한글=!한글;unsigned char avveniment[]={30,3,한글,0,0,0,0};원격입력넣기(avveniment,7);return;
    }
    if(simbolu==0xff08&&한글&&!kontroll_VALUE&&LOG_COUNT){조합=LOG_RECORD[--LOG_COUNT];글넣기(127);unsigned SMS=조합글();if(SMS)글넣기(SMS);return;}
    if(한글&&!kontroll_VALUE&&simbolu<128&&한글넣기(simbolu))return;
    원격글쇠확정();
    if((kontroll_VALUE&&tast_SHIFT&&(simbolu=='t'||simbolu=='T'))||simbolu==0xffc3||simbolu==0xffc9){unsigned char avveniment[]={30,2,simbolu==0xffc3?2:simbolu==0xffc9?3:1,0,0,0,0};원격입력넣기(avveniment,7);return;}
    const char *특수=simbolu==0xff08?"\177":simbolu==0xff09?"\t":simbolu==0xff0d?"\r":simbolu==0xff1b?"\033":
        simbolu==0xffff?"\033[3~":simbolu==0xff50?"\033[H":simbolu==0xff57?"\033[F":simbolu==0xff51?"\033[D":
        simbolu==0xff52?"\033[A":simbolu==0xff53?"\033[C":simbolu==0xff54?"\033[B":simbolu==0xff55?"\033[5~":simbolu==0xff56?"\033[6~":0;
    if(특수){원격입력넣기((const unsigned char*)특수,strlen(특수));return;}
    unsigned VALUE=(simbolu&0xff000000)==0x01000000?simbolu&0xffffff:simbolu;
    if(VALUE>0x10ffff||(VALUE>=0xd800&&VALUE<=0xdfff)||(simbolu>=0xff00&&simbolu<0x1000000))return;
    if(kontroll_VALUE){if(VALUE>='a'&&VALUE<='z')VALUE-=96;else if(VALUE>='A'&&VALUE<='Z')VALUE-=64;}
    글넣기(VALUE);
}
