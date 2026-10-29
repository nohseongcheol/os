#include "lu_soree_xëyma.h"
#include <string.h>
#include "두벌식표.h"
static unsigned Saytu_doxinu_ordinateur_xëyma,caabi_Maj,한글;
typedef struct {unsigned 첫,가운데,끝;} 조합상태;
static 조합상태 조합,làq_Dënk[16];
static unsigned 기록수;
void 원격글쇠확정(void){memset(&조합,0,sizeof(조합));기록수=0;}
void 원격글쇠초기화(void){Saytu_doxinu_ordinateur_xëyma=caabi_Maj=한글=0;원격글쇠확정();}
static void 글넣기(unsigned xëyma){
    unsigned char Tekst[4];unsigned 수;
    if(xëyma<128){Tekst[0]=xëyma;수=1;}else if(xëyma<2048){Tekst[0]=0xc0|(xëyma>>6);Tekst[1]=0x80|(xëyma&63);수=2;}
    else if(xëyma<65536){Tekst[0]=0xe0|(xëyma>>12);Tekst[1]=0x80|((xëyma>>6)&63);Tekst[2]=0x80|(xëyma&63);수=3;}
    else{Tekst[0]=0xf0|(xëyma>>18);Tekst[1]=0x80|((xëyma>>12)&63);Tekst[2]=0x80|((xëyma>>6)&63);Tekst[3]=0x80|(xëyma&63);수=4;}
    원격입력넣기(Tekst,수);
}
static int seet_dugal_xabaar(const unsigned *dugal_xabaar_lim,unsigned 수,unsigned xëyma){for(unsigned 순번=0;순번<수;순번++)if(dugal_xabaar_lim[순번]==xëyma)return 순번;return -1;}
static unsigned 겹찾기(const unsigned 표[][3],unsigned 수,unsigned 가,unsigned 나){for(unsigned 순번=0;순번<수;순번++)if(표[순번][0]==가&&표[순번][1]==나)return 표[순번][2];return 0;}
static unsigned 조합글(void){
    if(조합.첫&&조합.가운데)return 0xac00+(seet_dugal_xabaar(첫소리목록,19,조합.첫)*21+seet_dugal_xabaar(가운뎃소리목록,21,조합.가운데))*28+(조합.끝?seet_dugal_xabaar(끝소리목록,28,조합.끝):0);
    return 조합.첫?조합.첫:조합.가운데;
}
static int 한글넣기(unsigned 글쇠){
    unsigned 자모=0;for(unsigned 순번=0;순번<sizeof(kër_Tëralin)/sizeof(kër_Tëralin[0]);순번++)if(kër_Tëralin[순번][0]==글쇠)자모=kër_Tëralin[순번][1];
    if(!자모&&글쇠>='A'&&글쇠<='Z')return 한글넣기(글쇠+32);if(!자모)return 0;
    unsigned 이전=조합글(),확정=0;조합상태 전=조합;
    if(기록수<16)làq_Dënk[기록수++]=전;
    if(seet_dugal_xabaar(첫소리목록,19,자모)>=0){
        if(조합.첫&&조합.가운데&&!조합.끝&&seet_dugal_xabaar(끝소리목록,28,자모)>=0)조합.끝=자모;
        else{unsigned gëna_fës_xëyma=겹찾기(겹끝소리,11,조합.끝,자모);if(조합.끝&&gëna_fës_xëyma)조합.끝=gëna_fës_xëyma;
            else{확정=이전;원격글쇠확정();조합.첫=자모;기록수=1;memset(làq_Dënk,0,sizeof(조합상태));}}
    }else if(조합.끝){
        unsigned 왼쪽=0,오른쪽=조합.끝;for(unsigned 순번=0;순번<11;순번++)if(겹끝소리[순번][2]==조합.끝){왼쪽=겹끝소리[순번][0];오른쪽=겹끝소리[순번][1];break;}
        조합.끝=왼쪽;확정=조합글();원격글쇠확정();조합.첫=오른쪽;조합.가운데=자모;기록수=2;
        memset(làq_Dënk,0,2*sizeof(조합상태));làq_Dënk[1].첫=오른쪽;
    }else if(조합.가운데){unsigned gëna_fës_xëyma=겹찾기(겹가운뎃소리,7,조합.가운데,자모);
        if(gëna_fës_xëyma)조합.가운데=gëna_fës_xëyma;else{확정=이전;원격글쇠확정();조합.가운데=자모;기록수=1;memset(làq_Dënk,0,sizeof(조합상태));}
    }else 조합.가운데=자모;
    if(이전)글넣기(127);if(확정)글넣기(확정);unsigned 지금=조합글();if(지금)글넣기(지금);return 1;
}
void 원격글쇠(unsigned sembóol,int 누름){
    if(sembóol==0xffe3||sembóol==0xffe4){Saytu_doxinu_ordinateur_xëyma=누름;return;}
    if(sembóol==0xffe1||sembóol==0xffe2){caabi_Maj=누름;return;}
    if(!누름)return;
    if(sembóol==0xffc6||sembóol==0xff31||(sembóol==32&&caabi_Maj&&!Saytu_doxinu_ordinateur_xëyma)){
        원격글쇠확정();한글=!한글;unsigned char xewxew[]={30,3,한글,0,0,0,0};원격입력넣기(xewxew,7);return;
    }
    if(sembóol==0xff08&&한글&&!Saytu_doxinu_ordinateur_xëyma&&기록수){조합=làq_Dënk[--기록수];글넣기(127);unsigned Tekst=조합글();if(Tekst)글넣기(Tekst);return;}
    if(한글&&!Saytu_doxinu_ordinateur_xëyma&&sembóol<128&&한글넣기(sembóol))return;
    원격글쇠확정();
    if((Saytu_doxinu_ordinateur_xëyma&&caabi_Maj&&(sembóol=='t'||sembóol=='T'))||sembóol==0xffc3||sembóol==0xffc9){unsigned char xewxew[]={30,2,sembóol==0xffc3?2:sembóol==0xffc9?3:1,0,0,0,0};원격입력넣기(xewxew,7);return;}
    const char *특수=sembóol==0xff08?"\177":sembóol==0xff09?"\t":sembóol==0xff0d?"\r":sembóol==0xff1b?"\033":
        sembóol==0xffff?"\033[3~":sembóol==0xff50?"\033[H":sembóol==0xff57?"\033[F":sembóol==0xff51?"\033[D":
        sembóol==0xff52?"\033[A":sembóol==0xff53?"\033[C":sembóol==0xff54?"\033[B":sembóol==0xff55?"\033[5~":sembóol==0xff56?"\033[6~":0;
    if(특수){원격입력넣기((const unsigned char*)특수,strlen(특수));return;}
    unsigned xëyma=(sembóol&0xff000000)==0x01000000?sembóol&0xffffff:sembóol;
    if(xëyma>0x10ffff||(xëyma>=0xd800&&xëyma<=0xdfff)||(sembóol>=0xff00&&sembóol<0x1000000))return;
    if(Saytu_doxinu_ordinateur_xëyma){if(xëyma>='a'&&xëyma<='z')xëyma-=96;else if(xëyma>='A'&&xëyma<='Z')xëyma-=64;}
    글넣기(xëyma);
}
