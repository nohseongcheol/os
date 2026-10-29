#include "kauge_VALUE.h"
#include <string.h>
#include "두벌식표.h"
static unsigned meede_VALUE,윗글쇠,한글;
typedef struct {unsigned 첫,가운데,끝;} koosseis_Olek;
static koosseis_Olek koosseis_VALUE,LOG_kirje[16];
static unsigned LOG_COUNT;
void kinnitamine_kauge_Võti(void){memset(&koosseis_VALUE,0,sizeof(koosseis_VALUE));LOG_COUNT=0;}
void 원격글쇠초기화(void){meede_VALUE=윗글쇠=한글=0;kinnitamine_kauge_Võti();}
static void 글넣기(unsigned VALUE){
    unsigned char Tekst[4];unsigned number;
    if(VALUE<128){Tekst[0]=VALUE;number=1;}else if(VALUE<2048){Tekst[0]=0xc0|(VALUE>>6);Tekst[1]=0x80|(VALUE&63);number=2;}
    else if(VALUE<65536){Tekst[0]=0xe0|(VALUE>>12);Tekst[1]=0x80|((VALUE>>6)&63);Tekst[2]=0x80|(VALUE&63);number=3;}
    else{Tekst[0]=0xf0|(VALUE>>18);Tekst[1]=0x80|((VALUE>>12)&63);Tekst[2]=0x80|((VALUE>>6)&63);Tekst[3]=0x80|(VALUE&63);number=4;}
    원격입력넣기(Tekst,number);
}
static int FIND_kirje(const unsigned *kirje_Loend,unsigned number,unsigned VALUE){for(unsigned 순번=0;순번<number;순번++)if(kirje_Loend[순번]==VALUE)return 순번;return -1;}
static unsigned FIND_Dubleeri(const unsigned LOOKUP_tabel[][3],unsigned number,unsigned 가,unsigned SECOND_operand){for(unsigned 순번=0;순번<number;순번++)if(LOOKUP_tabel[순번][0]==가&&LOOKUP_tabel[순번][1]==SECOND_operand)return LOOKUP_tabel[순번][2];return 0;}
static unsigned 조합글(void){
    if(koosseis_VALUE.첫&&koosseis_VALUE.가운데)return 0xac00+(FIND_kirje(첫소리목록,19,koosseis_VALUE.첫)*21+FIND_kirje(가운뎃소리목록,21,koosseis_VALUE.가운데))*28+(koosseis_VALUE.끝?FIND_kirje(끝소리목록,28,koosseis_VALUE.끝):0);
    return koosseis_VALUE.첫?koosseis_VALUE.첫:koosseis_VALUE.가운데;
}
static int 한글넣기(unsigned Võti_tinditõmme){
    unsigned 자모=0;for(unsigned 순번=0;순번<sizeof(Võti_küljend)/sizeof(Võti_küljend[0]);순번++)if(Võti_küljend[순번][0]==Võti_tinditõmme)자모=Võti_küljend[순번][1];
    if(!자모&&Võti_tinditõmme>='A'&&Võti_tinditõmme<='Z')return 한글넣기(Võti_tinditõmme+32);if(!자모)return 0;
    unsigned 이전=조합글(),kinnitamine_VALUE=0;koosseis_Olek 전=koosseis_VALUE;
    if(LOG_COUNT<16)LOG_kirje[LOG_COUNT++]=전;
    if(FIND_kirje(첫소리목록,19,자모)>=0){
        if(koosseis_VALUE.첫&&koosseis_VALUE.가운데&&!koosseis_VALUE.끝&&FIND_kirje(끝소리목록,28,자모)>=0)koosseis_VALUE.끝=자모;
        else{unsigned ülekate_VALUE=FIND_Dubleeri(겹끝소리,11,koosseis_VALUE.끝,자모);if(koosseis_VALUE.끝&&ülekate_VALUE)koosseis_VALUE.끝=ülekate_VALUE;
            else{kinnitamine_VALUE=이전;kinnitamine_kauge_Võti();koosseis_VALUE.첫=자모;LOG_COUNT=1;memset(LOG_kirje,0,sizeof(koosseis_Olek));}}
    }else if(koosseis_VALUE.끝){
        unsigned 왼쪽=0,RIGHT=koosseis_VALUE.끝;for(unsigned 순번=0;순번<11;순번++)if(겹끝소리[순번][2]==koosseis_VALUE.끝){왼쪽=겹끝소리[순번][0];RIGHT=겹끝소리[순번][1];break;}
        koosseis_VALUE.끝=왼쪽;kinnitamine_VALUE=조합글();kinnitamine_kauge_Võti();koosseis_VALUE.첫=RIGHT;koosseis_VALUE.가운데=자모;LOG_COUNT=2;
        memset(LOG_kirje,0,2*sizeof(koosseis_Olek));LOG_kirje[1].첫=RIGHT;
    }else if(koosseis_VALUE.가운데){unsigned ülekate_VALUE=FIND_Dubleeri(겹가운뎃소리,7,koosseis_VALUE.가운데,자모);
        if(ülekate_VALUE)koosseis_VALUE.가운데=ülekate_VALUE;else{kinnitamine_VALUE=이전;kinnitamine_kauge_Võti();koosseis_VALUE.가운데=자모;LOG_COUNT=1;memset(LOG_kirje,0,sizeof(koosseis_Olek));}
    }else koosseis_VALUE.가운데=자모;
    if(이전)글넣기(127);if(kinnitamine_VALUE)글넣기(kinnitamine_VALUE);unsigned NOW_VALUE=조합글();if(NOW_VALUE)글넣기(NOW_VALUE);return 1;
}
void kauge_Võti_tinditõmme(unsigned sümbol,int vajutama_VALUE){
    if(sümbol==0xffe3||sümbol==0xffe4){meede_VALUE=vajutama_VALUE;return;}
    if(sümbol==0xffe1||sümbol==0xffe2){윗글쇠=vajutama_VALUE;return;}
    if(!vajutama_VALUE)return;
    if(sümbol==0xffc6||sümbol==0xff31||(sümbol==32&&윗글쇠&&!meede_VALUE)){
        kinnitamine_kauge_Võti();한글=!한글;unsigned char Sündmus[]={30,3,한글,0,0,0,0};원격입력넣기(Sündmus,7);return;
    }
    if(sümbol==0xff08&&한글&&!meede_VALUE&&LOG_COUNT){koosseis_VALUE=LOG_kirje[--LOG_COUNT];글넣기(127);unsigned Tekst=조합글();if(Tekst)글넣기(Tekst);return;}
    if(한글&&!meede_VALUE&&sümbol<128&&한글넣기(sümbol))return;
    kinnitamine_kauge_Võti();
    if((meede_VALUE&&윗글쇠&&(sümbol=='t'||sümbol=='T'))||sümbol==0xffc3||sümbol==0xffc9){unsigned char Sündmus[]={30,2,sümbol==0xffc3?2:sümbol==0xffc9?3:1,0,0,0,0};원격입력넣기(Sündmus,7);return;}
    const char *특수=sümbol==0xff08?"\177":sümbol==0xff09?"\t":sümbol==0xff0d?"\r":sümbol==0xff1b?"\033":
        sümbol==0xffff?"\033[3~":sümbol==0xff50?"\033[H":sümbol==0xff57?"\033[F":sümbol==0xff51?"\033[D":
        sümbol==0xff52?"\033[A":sümbol==0xff53?"\033[C":sümbol==0xff54?"\033[B":sümbol==0xff55?"\033[5~":sümbol==0xff56?"\033[6~":0;
    if(특수){원격입력넣기((const unsigned char*)특수,strlen(특수));return;}
    unsigned VALUE=(sümbol&0xff000000)==0x01000000?sümbol&0xffffff:sümbol;
    if(VALUE>0x10ffff||(VALUE>=0xd800&&VALUE<=0xdfff)||(sümbol>=0xff00&&sümbol<0x1000000))return;
    if(meede_VALUE){if(VALUE>='a'&&VALUE<='z')VALUE-=96;else if(VALUE>='A'&&VALUE<='Z')VALUE-=64;}
    글넣기(VALUE);
}
