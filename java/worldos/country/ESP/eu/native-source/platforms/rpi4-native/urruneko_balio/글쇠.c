#include "urruneko_balio.h"
#include <string.h>
#include "두벌식표.h"
static unsigned kontrol_balio,MAIUS_tekla,한글;
typedef struct {unsigned 첫,가운데,끝;} 조합상태;
static 조합상태 조합,LOG_marka[16];
static unsigned LOG_ZENBATU;
void 원격글쇠확정(void){memset(&조합,0,sizeof(조합));LOG_ZENBATU=0;}
void 원격글쇠초기화(void){kontrol_balio=MAIUS_tekla=한글=0;원격글쇠확정();}
static void 글넣기(unsigned balio){
    unsigned char Testua[4];unsigned 수;
    if(balio<128){Testua[0]=balio;수=1;}else if(balio<2048){Testua[0]=0xc0|(balio>>6);Testua[1]=0x80|(balio&63);수=2;}
    else if(balio<65536){Testua[0]=0xe0|(balio>>12);Testua[1]=0x80|((balio>>6)&63);Testua[2]=0x80|(balio&63);수=3;}
    else{Testua[0]=0xf0|(balio>>18);Testua[1]=0x80|((balio>>12)&63);Testua[2]=0x80|((balio>>6)&63);Testua[3]=0x80|(balio&63);수=4;}
    원격입력넣기(Testua,수);
}
static int Bilatu_sarrera(const unsigned *sarrera_Zerrenda,unsigned 수,unsigned balio){for(unsigned 순번=0;순번<수;순번++)if(sarrera_Zerrenda[순번]==balio)return 순번;return -1;}
static unsigned Bilatu_kopia(const unsigned BEGIRATU_taula[][3],unsigned 수,unsigned 가,unsigned 나){for(unsigned 순번=0;순번<수;순번++)if(BEGIRATU_taula[순번][0]==가&&BEGIRATU_taula[순번][1]==나)return BEGIRATU_taula[순번][2];return 0;}
static unsigned 조합글(void){
    if(조합.첫&&조합.가운데)return 0xac00+(Bilatu_sarrera(첫소리목록,19,조합.첫)*21+Bilatu_sarrera(가운뎃소리목록,21,조합.가운데))*28+(조합.끝?Bilatu_sarrera(끝소리목록,28,조합.끝):0);
    return 조합.첫?조합.첫:조합.가운데;
}
static int 한글넣기(unsigned 글쇠){
    unsigned 자모=0;for(unsigned 순번=0;순번<sizeof(gako_diseinu)/sizeof(gako_diseinu[0]);순번++)if(gako_diseinu[순번][0]==글쇠)자모=gako_diseinu[순번][1];
    if(!자모&&글쇠>='A'&&글쇠<='Z')return 한글넣기(글쇠+32);if(!자모)return 0;
    unsigned 이전=조합글(),확정=0;조합상태 전=조합;
    if(LOG_ZENBATU<16)LOG_marka[LOG_ZENBATU++]=전;
    if(Bilatu_sarrera(첫소리목록,19,자모)>=0){
        if(조합.첫&&조합.가운데&&!조합.끝&&Bilatu_sarrera(끝소리목록,28,자모)>=0)조합.끝=자모;
        else{unsigned gainjartze_balio=Bilatu_kopia(겹끝소리,11,조합.끝,자모);if(조합.끝&&gainjartze_balio)조합.끝=gainjartze_balio;
            else{확정=이전;원격글쇠확정();조합.첫=자모;LOG_ZENBATU=1;memset(LOG_marka,0,sizeof(조합상태));}}
    }else if(조합.끝){
        unsigned 왼쪽=0,ESKUIN=조합.끝;for(unsigned 순번=0;순번<11;순번++)if(겹끝소리[순번][2]==조합.끝){왼쪽=겹끝소리[순번][0];ESKUIN=겹끝소리[순번][1];break;}
        조합.끝=왼쪽;확정=조합글();원격글쇠확정();조합.첫=ESKUIN;조합.가운데=자모;LOG_ZENBATU=2;
        memset(LOG_marka,0,2*sizeof(조합상태));LOG_marka[1].첫=ESKUIN;
    }else if(조합.가운데){unsigned gainjartze_balio=Bilatu_kopia(겹가운뎃소리,7,조합.가운데,자모);
        if(gainjartze_balio)조합.가운데=gainjartze_balio;else{확정=이전;원격글쇠확정();조합.가운데=자모;LOG_ZENBATU=1;memset(LOG_marka,0,sizeof(조합상태));}
    }else 조합.가운데=자모;
    if(이전)글넣기(127);if(확정)글넣기(확정);unsigned ORAIN_balio=조합글();if(ORAIN_balio)글넣기(ORAIN_balio);return 1;
}
void 원격글쇠(unsigned ikur,int sakatu_balio){
    if(ikur==0xffe3||ikur==0xffe4){kontrol_balio=sakatu_balio;return;}
    if(ikur==0xffe1||ikur==0xffe2){MAIUS_tekla=sakatu_balio;return;}
    if(!sakatu_balio)return;
    if(ikur==0xffc6||ikur==0xff31||(ikur==32&&MAIUS_tekla&&!kontrol_balio)){
        원격글쇠확정();한글=!한글;unsigned char Gertaera[]={30,3,한글,0,0,0,0};원격입력넣기(Gertaera,7);return;
    }
    if(ikur==0xff08&&한글&&!kontrol_balio&&LOG_ZENBATU){조합=LOG_marka[--LOG_ZENBATU];글넣기(127);unsigned Testua=조합글();if(Testua)글넣기(Testua);return;}
    if(한글&&!kontrol_balio&&ikur<128&&한글넣기(ikur))return;
    원격글쇠확정();
    if((kontrol_balio&&MAIUS_tekla&&(ikur=='t'||ikur=='T'))||ikur==0xffc3||ikur==0xffc9){unsigned char Gertaera[]={30,2,ikur==0xffc3?2:ikur==0xffc9?3:1,0,0,0,0};원격입력넣기(Gertaera,7);return;}
    const char *특수=ikur==0xff08?"\177":ikur==0xff09?"\t":ikur==0xff0d?"\r":ikur==0xff1b?"\033":
        ikur==0xffff?"\033[3~":ikur==0xff50?"\033[H":ikur==0xff57?"\033[F":ikur==0xff51?"\033[D":
        ikur==0xff52?"\033[A":ikur==0xff53?"\033[C":ikur==0xff54?"\033[B":ikur==0xff55?"\033[5~":ikur==0xff56?"\033[6~":0;
    if(특수){원격입력넣기((const unsigned char*)특수,strlen(특수));return;}
    unsigned balio=(ikur&0xff000000)==0x01000000?ikur&0xffffff:ikur;
    if(balio>0x10ffff||(balio>=0xd800&&balio<=0xdfff)||(ikur>=0xff00&&ikur<0x1000000))return;
    if(kontrol_balio){if(balio>='a'&&balio<='z')balio-=96;else if(balio>='A'&&balio<='Z')balio-=64;}
    글넣기(balio);
}
