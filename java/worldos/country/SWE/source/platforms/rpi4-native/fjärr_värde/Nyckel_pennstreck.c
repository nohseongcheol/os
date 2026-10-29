#include "fjärr_värde.h"
#include <string.h>
#include "두벌식표.h"
static unsigned kontroll_värde,SKIFT_tangenten,한글;
typedef struct {unsigned 첫,가운데,끝;} komposition_status;
static komposition_status komposition_värde,LOG_POST[16];
static unsigned LOG_ANTAL;
void incheckning_fjärr_Nyckel(void){memset(&komposition_värde,0,sizeof(komposition_värde));LOG_ANTAL=0;}
void starta_fjärr_Nyckel_pennstreck(void){kontroll_värde=SKIFT_tangenten=한글=0;incheckning_fjärr_Nyckel();}
static void 글넣기(unsigned värde){
    unsigned char text[4];unsigned nummer;
    if(värde<128){text[0]=värde;nummer=1;}else if(värde<2048){text[0]=0xc0|(värde>>6);text[1]=0x80|(värde&63);nummer=2;}
    else if(värde<65536){text[0]=0xe0|(värde>>12);text[1]=0x80|((värde>>6)&63);text[2]=0x80|(värde&63);nummer=3;}
    else{text[0]=0xf0|(värde>>18);text[1]=0x80|((värde>>12)&63);text[2]=0x80|((värde>>6)&63);text[3]=0x80|(värde&63);nummer=4;}
    feed_fjärr_indata(text,nummer);
}
static int Sök_post(const unsigned *post_ange,unsigned nummer,unsigned värde){for(unsigned 순번=0;순번<nummer;순번++)if(post_ange[순번]==värde)return 순번;return -1;}
static unsigned Sök_dubblett(const unsigned LETAUPP_tabell[][3],unsigned nummer,unsigned 가,unsigned SEKUND_operand){for(unsigned 순번=0;순번<nummer;순번++)if(LETAUPP_tabell[순번][0]==가&&LETAUPP_tabell[순번][1]==SEKUND_operand)return LETAUPP_tabell[순번][2];return 0;}
static unsigned 조합글(void){
    if(komposition_värde.첫&&komposition_värde.가운데)return 0xac00+(Sök_post(첫소리목록,19,komposition_värde.첫)*21+Sök_post(가운뎃소리목록,21,komposition_värde.가운데))*28+(komposition_värde.끝?Sök_post(끝소리목록,28,komposition_värde.끝):0);
    return komposition_värde.첫?komposition_värde.첫:komposition_värde.가운데;
}
static int 한글넣기(unsigned Nyckel_pennstreck){
    unsigned 자모=0;for(unsigned 순번=0;순번<sizeof(Nyckel_Layout)/sizeof(Nyckel_Layout[0]);순번++)if(Nyckel_Layout[순번][0]==Nyckel_pennstreck)자모=Nyckel_Layout[순번][1];
    if(!자모&&Nyckel_pennstreck>='A'&&Nyckel_pennstreck<='Z')return 한글넣기(Nyckel_pennstreck+32);if(!자모)return 0;
    unsigned Föregående_objekt=조합글(),incheckning_värde=0;komposition_status 전=komposition_värde;
    if(LOG_ANTAL<16)LOG_POST[LOG_ANTAL++]=전;
    if(Sök_post(첫소리목록,19,자모)>=0){
        if(komposition_värde.첫&&komposition_värde.가운데&&!komposition_värde.끝&&Sök_post(끝소리목록,28,자모)>=0)komposition_värde.끝=자모;
        else{unsigned överlägg_värde=Sök_dubblett(겹끝소리,11,komposition_värde.끝,자모);if(komposition_värde.끝&&överlägg_värde)komposition_värde.끝=överlägg_värde;
            else{incheckning_värde=Föregående_objekt;incheckning_fjärr_Nyckel();komposition_värde.첫=자모;LOG_ANTAL=1;memset(LOG_POST,0,sizeof(komposition_status));}}
    }else if(komposition_värde.끝){
        unsigned 왼쪽=0,HÖGER=komposition_värde.끝;for(unsigned 순번=0;순번<11;순번++)if(겹끝소리[순번][2]==komposition_värde.끝){왼쪽=겹끝소리[순번][0];HÖGER=겹끝소리[순번][1];break;}
        komposition_värde.끝=왼쪽;incheckning_värde=조합글();incheckning_fjärr_Nyckel();komposition_värde.첫=HÖGER;komposition_värde.가운데=자모;LOG_ANTAL=2;
        memset(LOG_POST,0,2*sizeof(komposition_status));LOG_POST[1].첫=HÖGER;
    }else if(komposition_värde.가운데){unsigned överlägg_värde=Sök_dubblett(겹가운뎃소리,7,komposition_värde.가운데,자모);
        if(överlägg_värde)komposition_värde.가운데=överlägg_värde;else{incheckning_värde=Föregående_objekt;incheckning_fjärr_Nyckel();komposition_värde.가운데=자모;LOG_ANTAL=1;memset(LOG_POST,0,sizeof(komposition_status));}
    }else komposition_värde.가운데=자모;
    if(Föregående_objekt)글넣기(127);if(incheckning_värde)글넣기(incheckning_värde);unsigned NU_värde=조합글();if(NU_värde)글넣기(NU_värde);return 1;
}
void fjärr_Nyckel_pennstreck(unsigned symbol,int tryck_värde){
    if(symbol==0xffe3||symbol==0xffe4){kontroll_värde=tryck_värde;return;}
    if(symbol==0xffe1||symbol==0xffe2){SKIFT_tangenten=tryck_värde;return;}
    if(!tryck_värde)return;
    if(symbol==0xffc6||symbol==0xff31||(symbol==32&&SKIFT_tangenten&&!kontroll_värde)){
        incheckning_fjärr_Nyckel();한글=!한글;unsigned char Händelse[]={30,3,한글,0,0,0,0};feed_fjärr_indata(Händelse,7);return;
    }
    if(symbol==0xff08&&한글&&!kontroll_värde&&LOG_ANTAL){komposition_värde=LOG_POST[--LOG_ANTAL];글넣기(127);unsigned text=조합글();if(text)글넣기(text);return;}
    if(한글&&!kontroll_värde&&symbol<128&&한글넣기(symbol))return;
    incheckning_fjärr_Nyckel();
    if((kontroll_värde&&SKIFT_tangenten&&(symbol=='t'||symbol=='T'))||symbol==0xffc3||symbol==0xffc9){unsigned char Händelse[]={30,2,symbol==0xffc3?2:symbol==0xffc9?3:1,0,0,0,0};feed_fjärr_indata(Händelse,7);return;}
    const char *특수=symbol==0xff08?"\177":symbol==0xff09?"\t":symbol==0xff0d?"\r":symbol==0xff1b?"\033":
        symbol==0xffff?"\033[3~":symbol==0xff50?"\033[H":symbol==0xff57?"\033[F":symbol==0xff51?"\033[D":
        symbol==0xff52?"\033[A":symbol==0xff53?"\033[C":symbol==0xff54?"\033[B":symbol==0xff55?"\033[5~":symbol==0xff56?"\033[6~":0;
    if(특수){feed_fjärr_indata((const unsigned char*)특수,strlen(특수));return;}
    unsigned värde=(symbol&0xff000000)==0x01000000?symbol&0xffffff:symbol;
    if(värde>0x10ffff||(värde>=0xd800&&värde<=0xdfff)||(symbol>=0xff00&&symbol<0x1000000))return;
    if(kontroll_värde){if(värde>='a'&&värde<='z')värde-=96;else if(värde>='A'&&värde<='Z')värde-=64;}
    글넣기(värde);
}
