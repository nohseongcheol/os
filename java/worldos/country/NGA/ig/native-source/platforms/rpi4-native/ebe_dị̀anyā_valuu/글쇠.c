#include "ebe_dị̀anyā_valuu.h"
#include <string.h>
#include "두벌식표.h"
static unsigned njizi_valuu,ọtụgwo_SHIFT,한글;
typedef struct {unsigned 첫,가운데,끝;} 조합상태;
static 조합상태 조합,ndekọ_NDEKỌ[16];
static unsigned 기록수;
void 원격글쇠확정(void){memset(&조합,0,sizeof(조합));기록수=0;}
void 원격글쇠초기화(void){njizi_valuu=ọtụgwo_SHIFT=한글=0;원격글쇠확정();}
static void 글넣기(unsigned valuu){
    unsigned char SMS[4];unsigned 수;
    if(valuu<128){SMS[0]=valuu;수=1;}else if(valuu<2048){SMS[0]=0xc0|(valuu>>6);SMS[1]=0x80|(valuu&63);수=2;}
    else if(valuu<65536){SMS[0]=0xe0|(valuu>>12);SMS[1]=0x80|((valuu>>6)&63);SMS[2]=0x80|(valuu&63);수=3;}
    else{SMS[0]=0xf0|(valuu>>18);SMS[1]=0x80|((valuu>>12)&63);SMS[2]=0x80|((valuu>>6)&63);SMS[3]=0x80|(valuu&63);수=4;}
    원격입력넣기(SMS,수);
}
static int chọta_ndebà(const unsigned *ndebà_ndepụta,unsigned 수,unsigned valuu){for(unsigned 순번=0;순번<수;순번++)if(ndebà_ndepụta[순번]==valuu)return 순번;return -1;}
static unsigned 겹찾기(const unsigned 표[][3],unsigned 수,unsigned 가,unsigned 나){for(unsigned 순번=0;순번<수;순번++)if(표[순번][0]==가&&표[순번][1]==나)return 표[순번][2];return 0;}
static unsigned 조합글(void){
    if(조합.첫&&조합.가운데)return 0xac00+(chọta_ndebà(첫소리목록,19,조합.첫)*21+chọta_ndebà(가운뎃소리목록,21,조합.가운데))*28+(조합.끝?chọta_ndebà(끝소리목록,28,조합.끝):0);
    return 조합.첫?조합.첫:조합.가운데;
}
static int 한글넣기(unsigned 글쇠){
    unsigned 자모=0;for(unsigned 순번=0;순번<sizeof(ọtụgwo_Nhàzi)/sizeof(ọtụgwo_Nhàzi[0]);순번++)if(ọtụgwo_Nhàzi[순번][0]==글쇠)자모=ọtụgwo_Nhàzi[순번][1];
    if(!자모&&글쇠>='A'&&글쇠<='Z')return 한글넣기(글쇠+32);if(!자모)return 0;
    unsigned 이전=조합글(),확정=0;조합상태 전=조합;
    if(기록수<16)ndekọ_NDEKỌ[기록수++]=전;
    if(chọta_ndebà(첫소리목록,19,자모)>=0){
        if(조합.첫&&조합.가운데&&!조합.끝&&chọta_ndebà(끝소리목록,28,자모)>=0)조합.끝=자모;
        else{unsigned mkpọngosi_valuu=겹찾기(겹끝소리,11,조합.끝,자모);if(조합.끝&&mkpọngosi_valuu)조합.끝=mkpọngosi_valuu;
            else{확정=이전;원격글쇠확정();조합.첫=자모;기록수=1;memset(ndekọ_NDEKỌ,0,sizeof(조합상태));}}
    }else if(조합.끝){
        unsigned 왼쪽=0,오른쪽=조합.끝;for(unsigned 순번=0;순번<11;순번++)if(겹끝소리[순번][2]==조합.끝){왼쪽=겹끝소리[순번][0];오른쪽=겹끝소리[순번][1];break;}
        조합.끝=왼쪽;확정=조합글();원격글쇠확정();조합.첫=오른쪽;조합.가운데=자모;기록수=2;
        memset(ndekọ_NDEKỌ,0,2*sizeof(조합상태));ndekọ_NDEKỌ[1].첫=오른쪽;
    }else if(조합.가운데){unsigned mkpọngosi_valuu=겹찾기(겹가운뎃소리,7,조합.가운데,자모);
        if(mkpọngosi_valuu)조합.가운데=mkpọngosi_valuu;else{확정=이전;원격글쇠확정();조합.가운데=자모;기록수=1;memset(ndekọ_NDEKỌ,0,sizeof(조합상태));}
    }else 조합.가운데=자모;
    if(이전)글넣기(127);if(확정)글넣기(확정);unsigned 지금=조합글();if(지금)글넣기(지금);return 1;
}
void 원격글쇠(unsigned adimara,int 누름){
    if(adimara==0xffe3||adimara==0xffe4){njizi_valuu=누름;return;}
    if(adimara==0xffe1||adimara==0xffe2){ọtụgwo_SHIFT=누름;return;}
    if(!누름)return;
    if(adimara==0xffc6||adimara==0xff31||(adimara==32&&ọtụgwo_SHIFT&&!njizi_valuu)){
        원격글쇠확정();한글=!한글;unsigned char mmèrème[]={30,3,한글,0,0,0,0};원격입력넣기(mmèrème,7);return;
    }
    if(adimara==0xff08&&한글&&!njizi_valuu&&기록수){조합=ndekọ_NDEKỌ[--기록수];글넣기(127);unsigned SMS=조합글();if(SMS)글넣기(SMS);return;}
    if(한글&&!njizi_valuu&&adimara<128&&한글넣기(adimara))return;
    원격글쇠확정();
    if((njizi_valuu&&ọtụgwo_SHIFT&&(adimara=='t'||adimara=='T'))||adimara==0xffc3||adimara==0xffc9){unsigned char mmèrème[]={30,2,adimara==0xffc3?2:adimara==0xffc9?3:1,0,0,0,0};원격입력넣기(mmèrème,7);return;}
    const char *특수=adimara==0xff08?"\177":adimara==0xff09?"\t":adimara==0xff0d?"\r":adimara==0xff1b?"\033":
        adimara==0xffff?"\033[3~":adimara==0xff50?"\033[H":adimara==0xff57?"\033[F":adimara==0xff51?"\033[D":
        adimara==0xff52?"\033[A":adimara==0xff53?"\033[C":adimara==0xff54?"\033[B":adimara==0xff55?"\033[5~":adimara==0xff56?"\033[6~":0;
    if(특수){원격입력넣기((const unsigned char*)특수,strlen(특수));return;}
    unsigned valuu=(adimara&0xff000000)==0x01000000?adimara&0xffffff:adimara;
    if(valuu>0x10ffff||(valuu>=0xd800&&valuu<=0xdfff)||(adimara>=0xff00&&adimara<0x1000000))return;
    if(njizi_valuu){if(valuu>='a'&&valuu<='z')valuu-=96;else if(valuu>='A'&&valuu<='Z')valuu-=64;}
    글넣기(valuu);
}
