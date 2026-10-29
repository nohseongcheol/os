#include "kure_agaciro.h"
#include <string.h>
#include "두벌식표.h"
static unsigned icunga_agaciro,buto_SHIFT,한글;
typedef struct {unsigned 첫,가운데,끝;} 조합상태;
static 조합상태 조합,kubika_umurongo[16];
static unsigned 기록수;
void 원격글쇠확정(void){memset(&조합,0,sizeof(조합));기록수=0;}
void 원격글쇠초기화(void){icunga_agaciro=buto_SHIFT=한글=0;원격글쇠확정();}
static void 글넣기(unsigned agaciro){
    unsigned char Umwandiko[4];unsigned 수;
    if(agaciro<128){Umwandiko[0]=agaciro;수=1;}else if(agaciro<2048){Umwandiko[0]=0xc0|(agaciro>>6);Umwandiko[1]=0x80|(agaciro&63);수=2;}
    else if(agaciro<65536){Umwandiko[0]=0xe0|(agaciro>>12);Umwandiko[1]=0x80|((agaciro>>6)&63);Umwandiko[2]=0x80|(agaciro&63);수=3;}
    else{Umwandiko[0]=0xf0|(agaciro>>18);Umwandiko[1]=0x80|((agaciro>>12)&63);Umwandiko[2]=0x80|((agaciro>>6)&63);Umwandiko[3]=0x80|(agaciro&63);수=4;}
    원격입력넣기(Umwandiko,수);
}
static int gushaka_icyinjizwa(const unsigned *icyinjizwa_Urutonde,unsigned 수,unsigned agaciro){for(unsigned 순번=0;순번<수;순번++)if(icyinjizwa_Urutonde[순번]==agaciro)return 순번;return -1;}
static unsigned 겹찾기(const unsigned 표[][3],unsigned 수,unsigned 가,unsigned 나){for(unsigned 순번=0;순번<수;순번++)if(표[순번][0]==가&&표[순번][1]==나)return 표[순번][2];return 0;}
static unsigned 조합글(void){
    if(조합.첫&&조합.가운데)return 0xac00+(gushaka_icyinjizwa(첫소리목록,19,조합.첫)*21+gushaka_icyinjizwa(가운뎃소리목록,21,조합.가운데))*28+(조합.끝?gushaka_icyinjizwa(끝소리목록,28,조합.끝):0);
    return 조합.첫?조합.첫:조합.가운데;
}
static int 한글넣기(unsigned 글쇠){
    unsigned 자모=0;for(unsigned 순번=0;순번<sizeof(buto_Imimerere)/sizeof(buto_Imimerere[0]);순번++)if(buto_Imimerere[순번][0]==글쇠)자모=buto_Imimerere[순번][1];
    if(!자모&&글쇠>='A'&&글쇠<='Z')return 한글넣기(글쇠+32);if(!자모)return 0;
    unsigned 이전=조합글(),확정=0;조합상태 전=조합;
    if(기록수<16)kubika_umurongo[기록수++]=전;
    if(gushaka_icyinjizwa(첫소리목록,19,자모)>=0){
        if(조합.첫&&조합.가운데&&!조합.끝&&gushaka_icyinjizwa(끝소리목록,28,자모)>=0)조합.끝=자모;
        else{unsigned ingaragira_agaciro=겹찾기(겹끝소리,11,조합.끝,자모);if(조합.끝&&ingaragira_agaciro)조합.끝=ingaragira_agaciro;
            else{확정=이전;원격글쇠확정();조합.첫=자모;기록수=1;memset(kubika_umurongo,0,sizeof(조합상태));}}
    }else if(조합.끝){
        unsigned 왼쪽=0,오른쪽=조합.끝;for(unsigned 순번=0;순번<11;순번++)if(겹끝소리[순번][2]==조합.끝){왼쪽=겹끝소리[순번][0];오른쪽=겹끝소리[순번][1];break;}
        조합.끝=왼쪽;확정=조합글();원격글쇠확정();조합.첫=오른쪽;조합.가운데=자모;기록수=2;
        memset(kubika_umurongo,0,2*sizeof(조합상태));kubika_umurongo[1].첫=오른쪽;
    }else if(조합.가운데){unsigned ingaragira_agaciro=겹찾기(겹가운뎃소리,7,조합.가운데,자모);
        if(ingaragira_agaciro)조합.가운데=ingaragira_agaciro;else{확정=이전;원격글쇠확정();조합.가운데=자모;기록수=1;memset(kubika_umurongo,0,sizeof(조합상태));}
    }else 조합.가운데=자모;
    if(이전)글넣기(127);if(확정)글넣기(확정);unsigned 지금=조합글();if(지금)글넣기(지금);return 1;
}
void 원격글쇠(unsigned ikimenyetso,int 누름){
    if(ikimenyetso==0xffe3||ikimenyetso==0xffe4){icunga_agaciro=누름;return;}
    if(ikimenyetso==0xffe1||ikimenyetso==0xffe2){buto_SHIFT=누름;return;}
    if(!누름)return;
    if(ikimenyetso==0xffc6||ikimenyetso==0xff31||(ikimenyetso==32&&buto_SHIFT&&!icunga_agaciro)){
        원격글쇠확정();한글=!한글;unsigned char icyabaye[]={30,3,한글,0,0,0,0};원격입력넣기(icyabaye,7);return;
    }
    if(ikimenyetso==0xff08&&한글&&!icunga_agaciro&&기록수){조합=kubika_umurongo[--기록수];글넣기(127);unsigned Umwandiko=조합글();if(Umwandiko)글넣기(Umwandiko);return;}
    if(한글&&!icunga_agaciro&&ikimenyetso<128&&한글넣기(ikimenyetso))return;
    원격글쇠확정();
    if((icunga_agaciro&&buto_SHIFT&&(ikimenyetso=='t'||ikimenyetso=='T'))||ikimenyetso==0xffc3||ikimenyetso==0xffc9){unsigned char icyabaye[]={30,2,ikimenyetso==0xffc3?2:ikimenyetso==0xffc9?3:1,0,0,0,0};원격입력넣기(icyabaye,7);return;}
    const char *특수=ikimenyetso==0xff08?"\177":ikimenyetso==0xff09?"\t":ikimenyetso==0xff0d?"\r":ikimenyetso==0xff1b?"\033":
        ikimenyetso==0xffff?"\033[3~":ikimenyetso==0xff50?"\033[H":ikimenyetso==0xff57?"\033[F":ikimenyetso==0xff51?"\033[D":
        ikimenyetso==0xff52?"\033[A":ikimenyetso==0xff53?"\033[C":ikimenyetso==0xff54?"\033[B":ikimenyetso==0xff55?"\033[5~":ikimenyetso==0xff56?"\033[6~":0;
    if(특수){원격입력넣기((const unsigned char*)특수,strlen(특수));return;}
    unsigned agaciro=(ikimenyetso&0xff000000)==0x01000000?ikimenyetso&0xffffff:ikimenyetso;
    if(agaciro>0x10ffff||(agaciro>=0xd800&&agaciro<=0xdfff)||(ikimenyetso>=0xff00&&ikimenyetso<0x1000000))return;
    if(icunga_agaciro){if(agaciro>='a'&&agaciro<='z')agaciro-=96;else if(agaciro>='A'&&agaciro<='Z')agaciro-=64;}
    글넣기(agaciro);
}
