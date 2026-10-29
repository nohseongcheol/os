#include "ekstern_VERDI_28edcfa1.h"
#include <string.h>
#include "두벌식표.h"
static unsigned kontroll_VERDI,Skift,한글;
typedef struct {unsigned 첫,가운데,끝;} sammensetning_status;
static sammensetning_status sammensetning_VERDI,LOG_POST[16];
static unsigned LOG_ANTALL;
void 원격글쇠확정(void){memset(&sammensetning_VERDI,0,sizeof(sammensetning_VERDI));LOG_ANTALL=0;}
void starte_ekstern_tast_pennestrøk(void){kontroll_VERDI=Skift=한글=0;원격글쇠확정();}
static void 글넣기(unsigned VERDI){
    unsigned char Tekst[4];unsigned nummer;
    if(VERDI<128){Tekst[0]=VERDI;nummer=1;}else if(VERDI<2048){Tekst[0]=0xc0|(VERDI>>6);Tekst[1]=0x80|(VERDI&63);nummer=2;}
    else if(VERDI<65536){Tekst[0]=0xe0|(VERDI>>12);Tekst[1]=0x80|((VERDI>>6)&63);Tekst[2]=0x80|(VERDI&63);nummer=3;}
    else{Tekst[0]=0xf0|(VERDI>>18);Tekst[1]=0x80|((VERDI>>12)&63);Tekst[2]=0x80|((VERDI>>6)&63);Tekst[3]=0x80|(VERDI&63);nummer=4;}
    feed_ekstern_inndata(Tekst,nummer);
}
static int Søk_oppføring(const unsigned *oppføring_Liste,unsigned nummer,unsigned VERDI){for(unsigned 순번=0;순번<nummer;순번++)if(oppføring_Liste[순번]==VERDI)return 순번;return -1;}
static unsigned Søk_Lag_kopi(const unsigned oppslagstabell[][3],unsigned nummer,unsigned 가,unsigned SEKUND_operand){for(unsigned 순번=0;순번<nummer;순번++)if(oppslagstabell[순번][0]==가&&oppslagstabell[순번][1]==SEKUND_operand)return oppslagstabell[순번][2];return 0;}
static unsigned 조합글(void){
    if(sammensetning_VERDI.첫&&sammensetning_VERDI.가운데)return 0xac00+(Søk_oppføring(첫소리목록,19,sammensetning_VERDI.첫)*21+Søk_oppføring(가운뎃소리목록,21,sammensetning_VERDI.가운데))*28+(sammensetning_VERDI.끝?Søk_oppføring(끝소리목록,28,sammensetning_VERDI.끝):0);
    return sammensetning_VERDI.첫?sammensetning_VERDI.첫:sammensetning_VERDI.가운데;
}
static int 한글넣기(unsigned tast_pennestrøk){
    unsigned 자모=0;for(unsigned 순번=0;순번<sizeof(tast_Oppsett)/sizeof(tast_Oppsett[0]);순번++)if(tast_Oppsett[순번][0]==tast_pennestrøk)자모=tast_Oppsett[순번][1];
    if(!자모&&tast_pennestrøk>='A'&&tast_pennestrøk<='Z')return 한글넣기(tast_pennestrøk+32);if(!자모)return 0;
    unsigned Forrige_vare=조합글(),확정=0;sammensetning_status 전=sammensetning_VERDI;
    if(LOG_ANTALL<16)LOG_POST[LOG_ANTALL++]=전;
    if(Søk_oppføring(첫소리목록,19,자모)>=0){
        if(sammensetning_VERDI.첫&&sammensetning_VERDI.가운데&&!sammensetning_VERDI.끝&&Søk_oppføring(끝소리목록,28,자모)>=0)sammensetning_VERDI.끝=자모;
        else{unsigned overlegg_VERDI=Søk_Lag_kopi(겹끝소리,11,sammensetning_VERDI.끝,자모);if(sammensetning_VERDI.끝&&overlegg_VERDI)sammensetning_VERDI.끝=overlegg_VERDI;
            else{확정=Forrige_vare;원격글쇠확정();sammensetning_VERDI.첫=자모;LOG_ANTALL=1;memset(LOG_POST,0,sizeof(sammensetning_status));}}
    }else if(sammensetning_VERDI.끝){
        unsigned 왼쪽=0,HØYRE=sammensetning_VERDI.끝;for(unsigned 순번=0;순번<11;순번++)if(겹끝소리[순번][2]==sammensetning_VERDI.끝){왼쪽=겹끝소리[순번][0];HØYRE=겹끝소리[순번][1];break;}
        sammensetning_VERDI.끝=왼쪽;확정=조합글();원격글쇠확정();sammensetning_VERDI.첫=HØYRE;sammensetning_VERDI.가운데=자모;LOG_ANTALL=2;
        memset(LOG_POST,0,2*sizeof(sammensetning_status));LOG_POST[1].첫=HØYRE;
    }else if(sammensetning_VERDI.가운데){unsigned overlegg_VERDI=Søk_Lag_kopi(겹가운뎃소리,7,sammensetning_VERDI.가운데,자모);
        if(overlegg_VERDI)sammensetning_VERDI.가운데=overlegg_VERDI;else{확정=Forrige_vare;원격글쇠확정();sammensetning_VERDI.가운데=자모;LOG_ANTALL=1;memset(LOG_POST,0,sizeof(sammensetning_status));}
    }else sammensetning_VERDI.가운데=자모;
    if(Forrige_vare)글넣기(127);if(확정)글넣기(확정);unsigned NÅ_VERDI=조합글();if(NÅ_VERDI)글넣기(NÅ_VERDI);return 1;
}
void ekstern_tast_pennestrøk(unsigned symbol,int 누름){
    if(symbol==0xffe3||symbol==0xffe4){kontroll_VERDI=누름;return;}
    if(symbol==0xffe1||symbol==0xffe2){Skift=누름;return;}
    if(!누름)return;
    if(symbol==0xffc6||symbol==0xff31||(symbol==32&&Skift&&!kontroll_VERDI)){
        원격글쇠확정();한글=!한글;unsigned char Hendelse[]={30,3,한글,0,0,0,0};feed_ekstern_inndata(Hendelse,7);return;
    }
    if(symbol==0xff08&&한글&&!kontroll_VERDI&&LOG_ANTALL){sammensetning_VERDI=LOG_POST[--LOG_ANTALL];글넣기(127);unsigned Tekst=조합글();if(Tekst)글넣기(Tekst);return;}
    if(한글&&!kontroll_VERDI&&symbol<128&&한글넣기(symbol))return;
    원격글쇠확정();
    if((kontroll_VERDI&&Skift&&(symbol=='t'||symbol=='T'))||symbol==0xffc3||symbol==0xffc9){unsigned char Hendelse[]={30,2,symbol==0xffc3?2:symbol==0xffc9?3:1,0,0,0,0};feed_ekstern_inndata(Hendelse,7);return;}
    const char *특수=symbol==0xff08?"\177":symbol==0xff09?"\t":symbol==0xff0d?"\r":symbol==0xff1b?"\033":
        symbol==0xffff?"\033[3~":symbol==0xff50?"\033[H":symbol==0xff57?"\033[F":symbol==0xff51?"\033[D":
        symbol==0xff52?"\033[A":symbol==0xff53?"\033[C":symbol==0xff54?"\033[B":symbol==0xff55?"\033[5~":symbol==0xff56?"\033[6~":0;
    if(특수){feed_ekstern_inndata((const unsigned char*)특수,strlen(특수));return;}
    unsigned VERDI=(symbol&0xff000000)==0x01000000?symbol&0xffffff:symbol;
    if(VERDI>0x10ffff||(VERDI>=0xd800&&VERDI<=0xdfff)||(symbol>=0xff00&&symbol<0x1000000))return;
    if(kontroll_VERDI){if(VERDI>='a'&&VERDI<='z')VERDI-=96;else if(VERDI>='A'&&VERDI<='Z')VERDI-=64;}
    글넣기(VERDI);
}
