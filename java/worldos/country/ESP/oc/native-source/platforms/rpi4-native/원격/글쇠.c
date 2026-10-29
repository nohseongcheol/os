#include "원격.h"
#include <string.h>
#include "두벌식표.h"
static unsigned 제어,윗글쇠,한글;
typedef struct {unsigned 첫,가운데,끝;} 조합상태;
static 조합상태 조합,기록[16];
static unsigned 기록수;
void 원격글쇠확정(void){memset(&조합,0,sizeof(조합));기록수=0;}
void 원격글쇠초기화(void){제어=윗글쇠=한글=0;원격글쇠확정();}
static void 글넣기(unsigned 값){
    unsigned char Tèxte[4];unsigned 수;
    if(값<128){Tèxte[0]=값;수=1;}else if(값<2048){Tèxte[0]=0xc0|(값>>6);Tèxte[1]=0x80|(값&63);수=2;}
    else if(값<65536){Tèxte[0]=0xe0|(값>>12);Tèxte[1]=0x80|((값>>6)&63);Tèxte[2]=0x80|(값&63);수=3;}
    else{Tèxte[0]=0xf0|(값>>18);Tèxte[1]=0x80|((값>>12)&63);Tèxte[2]=0x80|((값>>6)&63);Tèxte[3]=0x80|(값&63);수=4;}
    원격입력넣기(Tèxte,수);
}
static int 찾기(const unsigned *목록,unsigned 수,unsigned 값){for(unsigned 순번=0;순번<수;순번++)if(목록[순번]==값)return 순번;return -1;}
static unsigned 겹찾기(const unsigned 표[][3],unsigned 수,unsigned 가,unsigned 나){for(unsigned 순번=0;순번<수;순번++)if(표[순번][0]==가&&표[순번][1]==나)return 표[순번][2];return 0;}
static unsigned 조합글(void){
    if(조합.첫&&조합.가운데)return 0xac00+(찾기(첫소리목록,19,조합.첫)*21+찾기(가운뎃소리목록,21,조합.가운데))*28+(조합.끝?찾기(끝소리목록,28,조합.끝):0);
    return 조합.첫?조합.첫:조합.가운데;
}
static int 한글넣기(unsigned 글쇠){
    unsigned 자모=0;for(unsigned 순번=0;순번<sizeof(글쇠배열)/sizeof(글쇠배열[0]);순번++)if(글쇠배열[순번][0]==글쇠)자모=글쇠배열[순번][1];
    if(!자모&&글쇠>='A'&&글쇠<='Z')return 한글넣기(글쇠+32);if(!자모)return 0;
    unsigned 이전=조합글(),확정=0;조합상태 전=조합;
    if(기록수<16)기록[기록수++]=전;
    if(찾기(첫소리목록,19,자모)>=0){
        if(조합.첫&&조합.가운데&&!조합.끝&&찾기(끝소리목록,28,자모)>=0)조합.끝=자모;
        else{unsigned 겹=겹찾기(겹끝소리,11,조합.끝,자모);if(조합.끝&&겹)조합.끝=겹;
            else{확정=이전;원격글쇠확정();조합.첫=자모;기록수=1;memset(기록,0,sizeof(조합상태));}}
    }else if(조합.끝){
        unsigned 왼쪽=0,오른쪽=조합.끝;for(unsigned 순번=0;순번<11;순번++)if(겹끝소리[순번][2]==조합.끝){왼쪽=겹끝소리[순번][0];오른쪽=겹끝소리[순번][1];break;}
        조합.끝=왼쪽;확정=조합글();원격글쇠확정();조합.첫=오른쪽;조합.가운데=자모;기록수=2;
        memset(기록,0,2*sizeof(조합상태));기록[1].첫=오른쪽;
    }else if(조합.가운데){unsigned 겹=겹찾기(겹가운뎃소리,7,조합.가운데,자모);
        if(겹)조합.가운데=겹;else{확정=이전;원격글쇠확정();조합.가운데=자모;기록수=1;memset(기록,0,sizeof(조합상태));}
    }else 조합.가운데=자모;
    if(이전)글넣기(127);if(확정)글넣기(확정);unsigned 지금=조합글();if(지금)글넣기(지금);return 1;
}
void 원격글쇠(unsigned 기호,int 누름){
    if(기호==0xffe3||기호==0xffe4){제어=누름;return;}
    if(기호==0xffe1||기호==0xffe2){윗글쇠=누름;return;}
    if(!누름)return;
    if(기호==0xffc6||기호==0xff31||(기호==32&&윗글쇠&&!제어)){
        원격글쇠확정();한글=!한글;unsigned char Eveniment[]={30,3,한글,0,0,0,0};원격입력넣기(Eveniment,7);return;
    }
    if(기호==0xff08&&한글&&!제어&&기록수){조합=기록[--기록수];글넣기(127);unsigned Tèxte=조합글();if(Tèxte)글넣기(Tèxte);return;}
    if(한글&&!제어&&기호<128&&한글넣기(기호))return;
    원격글쇠확정();
    if((제어&&윗글쇠&&(기호=='t'||기호=='T'))||기호==0xffc3||기호==0xffc9){unsigned char Eveniment[]={30,2,기호==0xffc3?2:기호==0xffc9?3:1,0,0,0,0};원격입력넣기(Eveniment,7);return;}
    const char *특수=기호==0xff08?"\177":기호==0xff09?"\t":기호==0xff0d?"\r":기호==0xff1b?"\033":
        기호==0xffff?"\033[3~":기호==0xff50?"\033[H":기호==0xff57?"\033[F":기호==0xff51?"\033[D":
        기호==0xff52?"\033[A":기호==0xff53?"\033[C":기호==0xff54?"\033[B":기호==0xff55?"\033[5~":기호==0xff56?"\033[6~":0;
    if(특수){원격입력넣기((const unsigned char*)특수,strlen(특수));return;}
    unsigned 값=(기호&0xff000000)==0x01000000?기호&0xffffff:기호;
    if(값>0x10ffff||(값>=0xd800&&값<=0xdfff)||(기호>=0xff00&&기호<0x1000000))return;
    if(제어){if(값>='a'&&값<='z')값-=96;else if(값>='A'&&값<='Z')값-=64;}
    글넣기(값);
}
