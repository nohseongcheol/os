#include "दुर्मीळ_मोल.h"
#include <string.h>
#include "두벌식표.h"
static unsigned नियंत्रण_मोल,SHIFT_की,한글;
typedef struct {unsigned 첫,가운데,끝;} 조합상태;
static 조합상태 조합,LOG_नोंद[16];
static unsigned LOG_COUNT;
void 원격글쇠확정(void){memset(&조합,0,sizeof(조합));LOG_COUNT=0;}
void 원격글쇠초기화(void){नियंत्रण_मोल=SHIFT_की=한글=0;원격글쇠확정();}
static void 글넣기(unsigned मोल){
    unsigned char SMS[4];unsigned 수;
    if(मोल<128){SMS[0]=मोल;수=1;}else if(मोल<2048){SMS[0]=0xc0|(मोल>>6);SMS[1]=0x80|(मोल&63);수=2;}
    else if(मोल<65536){SMS[0]=0xe0|(मोल>>12);SMS[1]=0x80|((मोल>>6)&63);SMS[2]=0x80|(मोल&63);수=3;}
    else{SMS[0]=0xf0|(मोल>>18);SMS[1]=0x80|((मोल>>12)&63);SMS[2]=0x80|((मोल>>6)&63);SMS[3]=0x80|(मोल&63);수=4;}
    원격입력넣기(SMS,수);
}
static int FIND_प्रवेश(const unsigned *प्रवेश_सुची,unsigned 수,unsigned मोल){for(unsigned 순번=0;순번<수;순번++)if(प्रवेश_सुची[순번]==मोल)return 순번;return -1;}
static unsigned 겹찾기(const unsigned लूकअप_तकटो[][3],unsigned 수,unsigned 가,unsigned 나){for(unsigned 순번=0;순번<수;순번++)if(लूकअप_तकटो[순번][0]==가&&लूकअप_तकटो[순번][1]==나)return लूकअप_तकटो[순번][2];return 0;}
static unsigned 조합글(void){
    if(조합.첫&&조합.가운데)return 0xac00+(FIND_प्रवेश(첫소리목록,19,조합.첫)*21+FIND_प्रवेश(가운뎃소리목록,21,조합.가운데))*28+(조합.끝?FIND_प्रवेश(끝소리목록,28,조합.끝):0);
    return 조합.첫?조합.첫:조합.가운데;
}
static int 한글넣기(unsigned 글쇠){
    unsigned 자모=0;for(unsigned 순번=0;순번<sizeof(की_रचणाय)/sizeof(की_रचणाय[0]);순번++)if(की_रचणाय[순번][0]==글쇠)자모=की_रचणाय[순번][1];
    if(!자모&&글쇠>='A'&&글쇠<='Z')return 한글넣기(글쇠+32);if(!자모)return 0;
    unsigned 이전=조합글(),확정=0;조합상태 전=조합;
    if(LOG_COUNT<16)LOG_नोंद[LOG_COUNT++]=전;
    if(FIND_प्रवेश(첫소리목록,19,자모)>=0){
        if(조합.첫&&조합.가운데&&!조합.끝&&FIND_प्रवेश(끝소리목록,28,자모)>=0)조합.끝=자모;
        else{unsigned ओवरले_मोल=겹찾기(겹끝소리,11,조합.끝,자모);if(조합.끝&&ओवरले_मोल)조합.끝=ओवरले_मोल;
            else{확정=이전;원격글쇠확정();조합.첫=자모;LOG_COUNT=1;memset(LOG_नोंद,0,sizeof(조합상태));}}
    }else if(조합.끝){
        unsigned 왼쪽=0,RIGHT=조합.끝;for(unsigned 순번=0;순번<11;순번++)if(겹끝소리[순번][2]==조합.끝){왼쪽=겹끝소리[순번][0];RIGHT=겹끝소리[순번][1];break;}
        조합.끝=왼쪽;확정=조합글();원격글쇠확정();조합.첫=RIGHT;조합.가운데=자모;LOG_COUNT=2;
        memset(LOG_नोंद,0,2*sizeof(조합상태));LOG_नोंद[1].첫=RIGHT;
    }else if(조합.가운데){unsigned ओवरले_मोल=겹찾기(겹가운뎃소리,7,조합.가운데,자모);
        if(ओवरले_मोल)조합.가운데=ओवरले_मोल;else{확정=이전;원격글쇠확정();조합.가운데=자모;LOG_COUNT=1;memset(LOG_नोंद,0,sizeof(조합상태));}
    }else 조합.가운데=자모;
    if(이전)글넣기(127);if(확정)글넣기(확정);unsigned NOW_मोल=조합글();if(NOW_मोल)글넣기(NOW_मोल);return 1;
}
void 원격글쇠(unsigned चिन्न,int 누름){
    if(चिन्न==0xffe3||चिन्न==0xffe4){नियंत्रण_मोल=누름;return;}
    if(चिन्न==0xffe1||चिन्न==0xffe2){SHIFT_की=누름;return;}
    if(!누름)return;
    if(चिन्न==0xffc6||चिन्न==0xff31||(चिन्न==32&&SHIFT_की&&!नियंत्रण_मोल)){
        원격글쇠확정();한글=!한글;unsigned char प्रसंग[]={30,3,한글,0,0,0,0};원격입력넣기(प्रसंग,7);return;
    }
    if(चिन्न==0xff08&&한글&&!नियंत्रण_मोल&&LOG_COUNT){조합=LOG_नोंद[--LOG_COUNT];글넣기(127);unsigned SMS=조합글();if(SMS)글넣기(SMS);return;}
    if(한글&&!नियंत्रण_मोल&&चिन्न<128&&한글넣기(चिन्न))return;
    원격글쇠확정();
    if((नियंत्रण_मोल&&SHIFT_की&&(चिन्न=='t'||चिन्न=='T'))||चिन्न==0xffc3||चिन्न==0xffc9){unsigned char प्रसंग[]={30,2,चिन्न==0xffc3?2:चिन्न==0xffc9?3:1,0,0,0,0};원격입력넣기(प्रसंग,7);return;}
    const char *특수=चिन्न==0xff08?"\177":चिन्न==0xff09?"\t":चिन्न==0xff0d?"\r":चिन्न==0xff1b?"\033":
        चिन्न==0xffff?"\033[3~":चिन्न==0xff50?"\033[H":चिन्न==0xff57?"\033[F":चिन्न==0xff51?"\033[D":
        चिन्न==0xff52?"\033[A":चिन्न==0xff53?"\033[C":चिन्न==0xff54?"\033[B":चिन्न==0xff55?"\033[5~":चिन्न==0xff56?"\033[6~":0;
    if(특수){원격입력넣기((const unsigned char*)특수,strlen(특수));return;}
    unsigned मोल=(चिन्न&0xff000000)==0x01000000?चिन्न&0xffffff:चिन्न;
    if(मोल>0x10ffff||(मोल>=0xd800&&मोल<=0xdfff)||(चिन्न>=0xff00&&चिन्न<0x1000000))return;
    if(नियंत्रण_मोल){if(मोल>='a'&&मोल<='z')मोल-=96;else if(मोल>='A'&&मोल<='Z')मोल-=64;}
    글넣기(मोल);
}
