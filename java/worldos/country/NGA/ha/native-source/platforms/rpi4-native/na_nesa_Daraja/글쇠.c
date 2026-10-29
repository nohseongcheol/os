#include "na_nesa_Daraja.h"
#include <string.h>
#include "두벌식표.h"
static unsigned masarrafa_Daraja,Makullin_matsawas,한글;
typedef struct {unsigned 첫,가운데,끝;} 조합상태;
static 조합상태 조합,logu_naɗa[16];
static unsigned 기록수;
void 원격글쇠확정(void){memset(&조합,0,sizeof(조합));기록수=0;}
void 원격글쇠초기화(void){masarrafa_Daraja=Makullin_matsawas=한글=0;원격글쇠확정();}
static void 글넣기(unsigned Daraja){
    unsigned char SMS[4];unsigned 수;
    if(Daraja<128){SMS[0]=Daraja;수=1;}else if(Daraja<2048){SMS[0]=0xc0|(Daraja>>6);SMS[1]=0x80|(Daraja&63);수=2;}
    else if(Daraja<65536){SMS[0]=0xe0|(Daraja>>12);SMS[1]=0x80|((Daraja>>6)&63);SMS[2]=0x80|(Daraja&63);수=3;}
    else{SMS[0]=0xf0|(Daraja>>18);SMS[1]=0x80|((Daraja>>12)&63);SMS[2]=0x80|((Daraja>>6)&63);SMS[3]=0x80|(Daraja&63);수=4;}
    원격입력넣기(SMS,수);
}
static int nema_Mashigar_bayanai(const unsigned *Mashigar_bayanai_Jeri,unsigned 수,unsigned Daraja){for(unsigned 순번=0;순번<수;순번++)if(Mashigar_bayanai_Jeri[순번]==Daraja)return 순번;return -1;}
static unsigned 겹찾기(const unsigned 표[][3],unsigned 수,unsigned 가,unsigned 나){for(unsigned 순번=0;순번<수;순번++)if(표[순번][0]==가&&표[순번][1]==나)return 표[순번][2];return 0;}
static unsigned 조합글(void){
    if(조합.첫&&조합.가운데)return 0xac00+(nema_Mashigar_bayanai(첫소리목록,19,조합.첫)*21+nema_Mashigar_bayanai(가운뎃소리목록,21,조합.가운데))*28+(조합.끝?nema_Mashigar_bayanai(끝소리목록,28,조합.끝):0);
    return 조합.첫?조합.첫:조합.가운데;
}
static int 한글넣기(unsigned 글쇠){
    unsigned 자모=0;for(unsigned 순번=0;순번<sizeof(Makulli_Zagaye)/sizeof(Makulli_Zagaye[0]);순번++)if(Makulli_Zagaye[순번][0]==글쇠)자모=Makulli_Zagaye[순번][1];
    if(!자모&&글쇠>='A'&&글쇠<='Z')return 한글넣기(글쇠+32);if(!자모)return 0;
    unsigned 이전=조합글(),확정=0;조합상태 전=조합;
    if(기록수<16)logu_naɗa[기록수++]=전;
    if(nema_Mashigar_bayanai(첫소리목록,19,자모)>=0){
        if(조합.첫&&조합.가운데&&!조합.끝&&nema_Mashigar_bayanai(끝소리목록,28,자모)>=0)조합.끝=자모;
        else{unsigned obalay_Daraja=겹찾기(겹끝소리,11,조합.끝,자모);if(조합.끝&&obalay_Daraja)조합.끝=obalay_Daraja;
            else{확정=이전;원격글쇠확정();조합.첫=자모;기록수=1;memset(logu_naɗa,0,sizeof(조합상태));}}
    }else if(조합.끝){
        unsigned 왼쪽=0,오른쪽=조합.끝;for(unsigned 순번=0;순번<11;순번++)if(겹끝소리[순번][2]==조합.끝){왼쪽=겹끝소리[순번][0];오른쪽=겹끝소리[순번][1];break;}
        조합.끝=왼쪽;확정=조합글();원격글쇠확정();조합.첫=오른쪽;조합.가운데=자모;기록수=2;
        memset(logu_naɗa,0,2*sizeof(조합상태));logu_naɗa[1].첫=오른쪽;
    }else if(조합.가운데){unsigned obalay_Daraja=겹찾기(겹가운뎃소리,7,조합.가운데,자모);
        if(obalay_Daraja)조합.가운데=obalay_Daraja;else{확정=이전;원격글쇠확정();조합.가운데=자모;기록수=1;memset(logu_naɗa,0,sizeof(조합상태));}
    }else 조합.가운데=자모;
    if(이전)글넣기(127);if(확정)글넣기(확정);unsigned Yanzu_Daraja=조합글();if(Yanzu_Daraja)글넣기(Yanzu_Daraja);return 1;
}
void 원격글쇠(unsigned alama_ad6f1a96,int 누름){
    if(alama_ad6f1a96==0xffe3||alama_ad6f1a96==0xffe4){masarrafa_Daraja=누름;return;}
    if(alama_ad6f1a96==0xffe1||alama_ad6f1a96==0xffe2){Makullin_matsawas=누름;return;}
    if(!누름)return;
    if(alama_ad6f1a96==0xffc6||alama_ad6f1a96==0xff31||(alama_ad6f1a96==32&&Makullin_matsawas&&!masarrafa_Daraja)){
        원격글쇠확정();한글=!한글;unsigned char Faruwa[]={30,3,한글,0,0,0,0};원격입력넣기(Faruwa,7);return;
    }
    if(alama_ad6f1a96==0xff08&&한글&&!masarrafa_Daraja&&기록수){조합=logu_naɗa[--기록수];글넣기(127);unsigned SMS=조합글();if(SMS)글넣기(SMS);return;}
    if(한글&&!masarrafa_Daraja&&alama_ad6f1a96<128&&한글넣기(alama_ad6f1a96))return;
    원격글쇠확정();
    if((masarrafa_Daraja&&Makullin_matsawas&&(alama_ad6f1a96=='t'||alama_ad6f1a96=='T'))||alama_ad6f1a96==0xffc3||alama_ad6f1a96==0xffc9){unsigned char Faruwa[]={30,2,alama_ad6f1a96==0xffc3?2:alama_ad6f1a96==0xffc9?3:1,0,0,0,0};원격입력넣기(Faruwa,7);return;}
    const char *특수=alama_ad6f1a96==0xff08?"\177":alama_ad6f1a96==0xff09?"\t":alama_ad6f1a96==0xff0d?"\r":alama_ad6f1a96==0xff1b?"\033":
        alama_ad6f1a96==0xffff?"\033[3~":alama_ad6f1a96==0xff50?"\033[H":alama_ad6f1a96==0xff57?"\033[F":alama_ad6f1a96==0xff51?"\033[D":
        alama_ad6f1a96==0xff52?"\033[A":alama_ad6f1a96==0xff53?"\033[C":alama_ad6f1a96==0xff54?"\033[B":alama_ad6f1a96==0xff55?"\033[5~":alama_ad6f1a96==0xff56?"\033[6~":0;
    if(특수){원격입력넣기((const unsigned char*)특수,strlen(특수));return;}
    unsigned Daraja=(alama_ad6f1a96&0xff000000)==0x01000000?alama_ad6f1a96&0xffffff:alama_ad6f1a96;
    if(Daraja>0x10ffff||(Daraja>=0xd800&&Daraja<=0xdfff)||(alama_ad6f1a96>=0xff00&&alama_ad6f1a96<0x1000000))return;
    if(masarrafa_Daraja){if(Daraja>='a'&&Daraja<='z')Daraja-=96;else if(Daraja>='A'&&Daraja<='Z')Daraja-=64;}
    글넣기(Daraja);
}
