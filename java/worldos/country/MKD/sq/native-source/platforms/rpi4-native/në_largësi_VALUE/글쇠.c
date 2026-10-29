#include "në_largësi_VALUE.h"
#include <string.h>
#include "두벌식표.h"
static unsigned kontroll_VALUE,tasti_SHIFT,한글;
typedef struct {unsigned 첫,가운데,끝;} 조합상태;
static 조합상태 조합,LOG_RECORD[16];
static unsigned LOG_COUNT;
void 원격글쇠확정(void){memset(&조합,0,sizeof(조합));LOG_COUNT=0;}
void 원격글쇠초기화(void){kontroll_VALUE=tasti_SHIFT=한글=0;원격글쇠확정();}
static void 글넣기(unsigned VALUE){
    unsigned char Teksti[4];unsigned 수;
    if(VALUE<128){Teksti[0]=VALUE;수=1;}else if(VALUE<2048){Teksti[0]=0xc0|(VALUE>>6);Teksti[1]=0x80|(VALUE&63);수=2;}
    else if(VALUE<65536){Teksti[0]=0xe0|(VALUE>>12);Teksti[1]=0x80|((VALUE>>6)&63);Teksti[2]=0x80|(VALUE&63);수=3;}
    else{Teksti[0]=0xf0|(VALUE>>18);Teksti[1]=0x80|((VALUE>>12)&63);Teksti[2]=0x80|((VALUE>>6)&63);Teksti[3]=0x80|(VALUE&63);수=4;}
    원격입력넣기(Teksti,수);
}
static int FIND_futje(const unsigned *futje_Listë,unsigned 수,unsigned VALUE){for(unsigned 순번=0;순번<수;순번++)if(futje_Listë[순번]==VALUE)return 순번;return -1;}
static unsigned 겹찾기(const unsigned LOOKUP_tabelë[][3],unsigned 수,unsigned 가,unsigned 나){for(unsigned 순번=0;순번<수;순번++)if(LOOKUP_tabelë[순번][0]==가&&LOOKUP_tabelë[순번][1]==나)return LOOKUP_tabelë[순번][2];return 0;}
static unsigned 조합글(void){
    if(조합.첫&&조합.가운데)return 0xac00+(FIND_futje(첫소리목록,19,조합.첫)*21+FIND_futje(가운뎃소리목록,21,조합.가운데))*28+(조합.끝?FIND_futje(끝소리목록,28,조합.끝):0);
    return 조합.첫?조합.첫:조합.가운데;
}
static int 한글넣기(unsigned 글쇠){
    unsigned 자모=0;for(unsigned 순번=0;순번<sizeof(tast_Navigimi)/sizeof(tast_Navigimi[0]);순번++)if(tast_Navigimi[순번][0]==글쇠)자모=tast_Navigimi[순번][1];
    if(!자모&&글쇠>='A'&&글쇠<='Z')return 한글넣기(글쇠+32);if(!자모)return 0;
    unsigned 이전=조합글(),확정=0;조합상태 전=조합;
    if(LOG_COUNT<16)LOG_RECORD[LOG_COUNT++]=전;
    if(FIND_futje(첫소리목록,19,자모)>=0){
        if(조합.첫&&조합.가운데&&!조합.끝&&FIND_futje(끝소리목록,28,자모)>=0)조합.끝=자모;
        else{unsigned mbivendosje_VALUE=겹찾기(겹끝소리,11,조합.끝,자모);if(조합.끝&&mbivendosje_VALUE)조합.끝=mbivendosje_VALUE;
            else{확정=이전;원격글쇠확정();조합.첫=자모;LOG_COUNT=1;memset(LOG_RECORD,0,sizeof(조합상태));}}
    }else if(조합.끝){
        unsigned 왼쪽=0,RIGHT=조합.끝;for(unsigned 순번=0;순번<11;순번++)if(겹끝소리[순번][2]==조합.끝){왼쪽=겹끝소리[순번][0];RIGHT=겹끝소리[순번][1];break;}
        조합.끝=왼쪽;확정=조합글();원격글쇠확정();조합.첫=RIGHT;조합.가운데=자모;LOG_COUNT=2;
        memset(LOG_RECORD,0,2*sizeof(조합상태));LOG_RECORD[1].첫=RIGHT;
    }else if(조합.가운데){unsigned mbivendosje_VALUE=겹찾기(겹가운뎃소리,7,조합.가운데,자모);
        if(mbivendosje_VALUE)조합.가운데=mbivendosje_VALUE;else{확정=이전;원격글쇠확정();조합.가운데=자모;LOG_COUNT=1;memset(LOG_RECORD,0,sizeof(조합상태));}
    }else 조합.가운데=자모;
    if(이전)글넣기(127);if(확정)글넣기(확정);unsigned NOW_VALUE=조합글();if(NOW_VALUE)글넣기(NOW_VALUE);return 1;
}
void 원격글쇠(unsigned simbol,int shtyp_VALUE){
    if(simbol==0xffe3||simbol==0xffe4){kontroll_VALUE=shtyp_VALUE;return;}
    if(simbol==0xffe1||simbol==0xffe2){tasti_SHIFT=shtyp_VALUE;return;}
    if(!shtyp_VALUE)return;
    if(simbol==0xffc6||simbol==0xff31||(simbol==32&&tasti_SHIFT&&!kontroll_VALUE)){
        원격글쇠확정();한글=!한글;unsigned char Ngjarje[]={30,3,한글,0,0,0,0};원격입력넣기(Ngjarje,7);return;
    }
    if(simbol==0xff08&&한글&&!kontroll_VALUE&&LOG_COUNT){조합=LOG_RECORD[--LOG_COUNT];글넣기(127);unsigned Teksti=조합글();if(Teksti)글넣기(Teksti);return;}
    if(한글&&!kontroll_VALUE&&simbol<128&&한글넣기(simbol))return;
    원격글쇠확정();
    if((kontroll_VALUE&&tasti_SHIFT&&(simbol=='t'||simbol=='T'))||simbol==0xffc3||simbol==0xffc9){unsigned char Ngjarje[]={30,2,simbol==0xffc3?2:simbol==0xffc9?3:1,0,0,0,0};원격입력넣기(Ngjarje,7);return;}
    const char *특수=simbol==0xff08?"\177":simbol==0xff09?"\t":simbol==0xff0d?"\r":simbol==0xff1b?"\033":
        simbol==0xffff?"\033[3~":simbol==0xff50?"\033[H":simbol==0xff57?"\033[F":simbol==0xff51?"\033[D":
        simbol==0xff52?"\033[A":simbol==0xff53?"\033[C":simbol==0xff54?"\033[B":simbol==0xff55?"\033[5~":simbol==0xff56?"\033[6~":0;
    if(특수){원격입력넣기((const unsigned char*)특수,strlen(특수));return;}
    unsigned VALUE=(simbol&0xff000000)==0x01000000?simbol&0xffffff:simbol;
    if(VALUE>0x10ffff||(VALUE>=0xd800&&VALUE<=0xdfff)||(simbol>=0xff00&&simbol<0x1000000))return;
    if(kontroll_VALUE){if(VALUE>='a'&&VALUE<='z')VALUE-=96;else if(VALUE>='A'&&VALUE<='Z')VALUE-=64;}
    글넣기(VALUE);
}
