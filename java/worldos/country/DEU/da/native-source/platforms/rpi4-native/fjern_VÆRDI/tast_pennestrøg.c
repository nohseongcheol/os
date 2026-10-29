#include "fjern_VÆRDI.h"
#include <string.h>
#include "두벌식표.h"
static unsigned kontrol_VÆRDI,Skift_tast,한글;
typedef struct {unsigned 첫,가운데,끝;} komposition_status;
static komposition_status komposition_VÆRDI,LOG_post[16];
static unsigned LOG_TÆL;
void udføre_fjern_tast(void){memset(&komposition_VÆRDI,0,sizeof(komposition_VÆRDI));LOG_TÆL=0;}
void starte_fjern_tast_pennestrøg(void){kontrol_VÆRDI=Skift_tast=한글=0;udføre_fjern_tast();}
static void 글넣기(unsigned VÆRDI){
    unsigned char Tekst[4];unsigned tal;
    if(VÆRDI<128){Tekst[0]=VÆRDI;tal=1;}else if(VÆRDI<2048){Tekst[0]=0xc0|(VÆRDI>>6);Tekst[1]=0x80|(VÆRDI&63);tal=2;}
    else if(VÆRDI<65536){Tekst[0]=0xe0|(VÆRDI>>12);Tekst[1]=0x80|((VÆRDI>>6)&63);Tekst[2]=0x80|(VÆRDI&63);tal=3;}
    else{Tekst[0]=0xf0|(VÆRDI>>18);Tekst[1]=0x80|((VÆRDI>>12)&63);Tekst[2]=0x80|((VÆRDI>>6)&63);Tekst[3]=0x80|(VÆRDI&63);tal=4;}
    feed_fjern_input(Tekst,tal);
}
static int Søg_post(const unsigned *post_Liste,unsigned tal,unsigned VÆRDI){for(unsigned 순번=0;순번<tal;순번++)if(post_Liste[순번]==VÆRDI)return 순번;return -1;}
static unsigned Søg_dublet(const unsigned Opslag_tabel[][3],unsigned tal,unsigned 가,unsigned SEKUND_operand){for(unsigned 순번=0;순번<tal;순번++)if(Opslag_tabel[순번][0]==가&&Opslag_tabel[순번][1]==SEKUND_operand)return Opslag_tabel[순번][2];return 0;}
static unsigned 조합글(void){
    if(komposition_VÆRDI.첫&&komposition_VÆRDI.가운데)return 0xac00+(Søg_post(첫소리목록,19,komposition_VÆRDI.첫)*21+Søg_post(가운뎃소리목록,21,komposition_VÆRDI.가운데))*28+(komposition_VÆRDI.끝?Søg_post(끝소리목록,28,komposition_VÆRDI.끝):0);
    return komposition_VÆRDI.첫?komposition_VÆRDI.첫:komposition_VÆRDI.가운데;
}
static int 한글넣기(unsigned tast_pennestrøg){
    unsigned 자모=0;for(unsigned 순번=0;순번<sizeof(tast_Layout)/sizeof(tast_Layout[0]);순번++)if(tast_Layout[순번][0]==tast_pennestrøg)자모=tast_Layout[순번][1];
    if(!자모&&tast_pennestrøg>='A'&&tast_pennestrøg<='Z')return 한글넣기(tast_pennestrøg+32);if(!자모)return 0;
    unsigned Forrige_vare=조합글(),udføre_VÆRDI=0;komposition_status 전=komposition_VÆRDI;
    if(LOG_TÆL<16)LOG_post[LOG_TÆL++]=전;
    if(Søg_post(첫소리목록,19,자모)>=0){
        if(komposition_VÆRDI.첫&&komposition_VÆRDI.가운데&&!komposition_VÆRDI.끝&&Søg_post(끝소리목록,28,자모)>=0)komposition_VÆRDI.끝=자모;
        else{unsigned overlejring_VÆRDI=Søg_dublet(겹끝소리,11,komposition_VÆRDI.끝,자모);if(komposition_VÆRDI.끝&&overlejring_VÆRDI)komposition_VÆRDI.끝=overlejring_VÆRDI;
            else{udføre_VÆRDI=Forrige_vare;udføre_fjern_tast();komposition_VÆRDI.첫=자모;LOG_TÆL=1;memset(LOG_post,0,sizeof(komposition_status));}}
    }else if(komposition_VÆRDI.끝){
        unsigned 왼쪽=0,HØJRE=komposition_VÆRDI.끝;for(unsigned 순번=0;순번<11;순번++)if(겹끝소리[순번][2]==komposition_VÆRDI.끝){왼쪽=겹끝소리[순번][0];HØJRE=겹끝소리[순번][1];break;}
        komposition_VÆRDI.끝=왼쪽;udføre_VÆRDI=조합글();udføre_fjern_tast();komposition_VÆRDI.첫=HØJRE;komposition_VÆRDI.가운데=자모;LOG_TÆL=2;
        memset(LOG_post,0,2*sizeof(komposition_status));LOG_post[1].첫=HØJRE;
    }else if(komposition_VÆRDI.가운데){unsigned overlejring_VÆRDI=Søg_dublet(겹가운뎃소리,7,komposition_VÆRDI.가운데,자모);
        if(overlejring_VÆRDI)komposition_VÆRDI.가운데=overlejring_VÆRDI;else{udføre_VÆRDI=Forrige_vare;udføre_fjern_tast();komposition_VÆRDI.가운데=자모;LOG_TÆL=1;memset(LOG_post,0,sizeof(komposition_status));}
    }else komposition_VÆRDI.가운데=자모;
    if(Forrige_vare)글넣기(127);if(udføre_VÆRDI)글넣기(udføre_VÆRDI);unsigned NU_VÆRDI=조합글();if(NU_VÆRDI)글넣기(NU_VÆRDI);return 1;
}
void fjern_tast_pennestrøg(unsigned symbol,int 누름){
    if(symbol==0xffe3||symbol==0xffe4){kontrol_VÆRDI=누름;return;}
    if(symbol==0xffe1||symbol==0xffe2){Skift_tast=누름;return;}
    if(!누름)return;
    if(symbol==0xffc6||symbol==0xff31||(symbol==32&&Skift_tast&&!kontrol_VÆRDI)){
        udføre_fjern_tast();한글=!한글;unsigned char hændelse[]={30,3,한글,0,0,0,0};feed_fjern_input(hændelse,7);return;
    }
    if(symbol==0xff08&&한글&&!kontrol_VÆRDI&&LOG_TÆL){komposition_VÆRDI=LOG_post[--LOG_TÆL];글넣기(127);unsigned Tekst=조합글();if(Tekst)글넣기(Tekst);return;}
    if(한글&&!kontrol_VÆRDI&&symbol<128&&한글넣기(symbol))return;
    udføre_fjern_tast();
    if((kontrol_VÆRDI&&Skift_tast&&(symbol=='t'||symbol=='T'))||symbol==0xffc3||symbol==0xffc9){unsigned char hændelse[]={30,2,symbol==0xffc3?2:symbol==0xffc9?3:1,0,0,0,0};feed_fjern_input(hændelse,7);return;}
    const char *특수=symbol==0xff08?"\177":symbol==0xff09?"\t":symbol==0xff0d?"\r":symbol==0xff1b?"\033":
        symbol==0xffff?"\033[3~":symbol==0xff50?"\033[H":symbol==0xff57?"\033[F":symbol==0xff51?"\033[D":
        symbol==0xff52?"\033[A":symbol==0xff53?"\033[C":symbol==0xff54?"\033[B":symbol==0xff55?"\033[5~":symbol==0xff56?"\033[6~":0;
    if(특수){feed_fjern_input((const unsigned char*)특수,strlen(특수));return;}
    unsigned VÆRDI=(symbol&0xff000000)==0x01000000?symbol&0xffffff:symbol;
    if(VÆRDI>0x10ffff||(VÆRDI>=0xd800&&VÆRDI<=0xdfff)||(symbol>=0xff00&&symbol<0x1000000))return;
    if(kontrol_VÆRDI){if(VÆRDI>='a'&&VÆRDI<='z')VÆRDI-=96;else if(VÆRDI>='A'&&VÆRDI<='Z')VÆRDI-=64;}
    글넣기(VÆRDI);
}
