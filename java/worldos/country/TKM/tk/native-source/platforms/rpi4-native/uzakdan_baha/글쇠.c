#include "uzakdan_baha.h"
#include <string.h>
#include "두벌식표.h"
static unsigned dolandyryş_baha,SHIFT_klawişasy,한글;
typedef struct {unsigned 첫,가운데,끝;} 조합상태;
static 조합상태 조합,hasaba_alyş_setir[16];
static unsigned 기록수;
void 원격글쇠확정(void){memset(&조합,0,sizeof(조합));기록수=0;}
void 원격글쇠초기화(void){dolandyryş_baha=SHIFT_klawişasy=한글=0;원격글쇠확정();}
static void 글넣기(unsigned baha){
    unsigned char Metin[4];unsigned 수;
    if(baha<128){Metin[0]=baha;수=1;}else if(baha<2048){Metin[0]=0xc0|(baha>>6);Metin[1]=0x80|(baha&63);수=2;}
    else if(baha<65536){Metin[0]=0xe0|(baha>>12);Metin[1]=0x80|((baha>>6)&63);Metin[2]=0x80|(baha&63);수=3;}
    else{Metin[0]=0xf0|(baha>>18);Metin[1]=0x80|((baha>>12)&63);Metin[2]=0x80|((baha>>6)&63);Metin[3]=0x80|(baha&63);수=4;}
    원격입력넣기(Metin,수);
}
static int tap_girizmeklik(const unsigned *girizmeklik_Sanaw,unsigned 수,unsigned baha){for(unsigned 순번=0;순번<수;순번++)if(girizmeklik_Sanaw[순번]==baha)return 순번;return -1;}
static unsigned 겹찾기(const unsigned 표[][3],unsigned 수,unsigned 가,unsigned 나){for(unsigned 순번=0;순번<수;순번++)if(표[순번][0]==가&&표[순번][1]==나)return 표[순번][2];return 0;}
static unsigned 조합글(void){
    if(조합.첫&&조합.가운데)return 0xac00+(tap_girizmeklik(첫소리목록,19,조합.첫)*21+tap_girizmeklik(가운뎃소리목록,21,조합.가운데))*28+(조합.끝?tap_girizmeklik(끝소리목록,28,조합.끝):0);
    return 조합.첫?조합.첫:조합.가운데;
}
static int 한글넣기(unsigned 글쇠){
    unsigned 자모=0;for(unsigned 순번=0;순번<sizeof(açar_Ýerleşiş)/sizeof(açar_Ýerleşiş[0]);순번++)if(açar_Ýerleşiş[순번][0]==글쇠)자모=açar_Ýerleşiş[순번][1];
    if(!자모&&글쇠>='A'&&글쇠<='Z')return 한글넣기(글쇠+32);if(!자모)return 0;
    unsigned 이전=조합글(),확정=0;조합상태 전=조합;
    if(기록수<16)hasaba_alyş_setir[기록수++]=전;
    if(tap_girizmeklik(첫소리목록,19,자모)>=0){
        if(조합.첫&&조합.가운데&&!조합.끝&&tap_girizmeklik(끝소리목록,28,자모)>=0)조합.끝=자모;
        else{unsigned ýokarky_gatlak_baha=겹찾기(겹끝소리,11,조합.끝,자모);if(조합.끝&&ýokarky_gatlak_baha)조합.끝=ýokarky_gatlak_baha;
            else{확정=이전;원격글쇠확정();조합.첫=자모;기록수=1;memset(hasaba_alyş_setir,0,sizeof(조합상태));}}
    }else if(조합.끝){
        unsigned 왼쪽=0,오른쪽=조합.끝;for(unsigned 순번=0;순번<11;순번++)if(겹끝소리[순번][2]==조합.끝){왼쪽=겹끝소리[순번][0];오른쪽=겹끝소리[순번][1];break;}
        조합.끝=왼쪽;확정=조합글();원격글쇠확정();조합.첫=오른쪽;조합.가운데=자모;기록수=2;
        memset(hasaba_alyş_setir,0,2*sizeof(조합상태));hasaba_alyş_setir[1].첫=오른쪽;
    }else if(조합.가운데){unsigned ýokarky_gatlak_baha=겹찾기(겹가운뎃소리,7,조합.가운데,자모);
        if(ýokarky_gatlak_baha)조합.가운데=ýokarky_gatlak_baha;else{확정=이전;원격글쇠확정();조합.가운데=자모;기록수=1;memset(hasaba_alyş_setir,0,sizeof(조합상태));}
    }else 조합.가운데=자모;
    if(이전)글넣기(127);if(확정)글넣기(확정);unsigned 지금=조합글();if(지금)글넣기(지금);return 1;
}
void 원격글쇠(unsigned nyşan,int 누름){
    if(nyşan==0xffe3||nyşan==0xffe4){dolandyryş_baha=누름;return;}
    if(nyşan==0xffe1||nyşan==0xffe2){SHIFT_klawişasy=누름;return;}
    if(!누름)return;
    if(nyşan==0xffc6||nyşan==0xff31||(nyşan==32&&SHIFT_klawişasy&&!dolandyryş_baha)){
        원격글쇠확정();한글=!한글;unsigned char waka[]={30,3,한글,0,0,0,0};원격입력넣기(waka,7);return;
    }
    if(nyşan==0xff08&&한글&&!dolandyryş_baha&&기록수){조합=hasaba_alyş_setir[--기록수];글넣기(127);unsigned Metin=조합글();if(Metin)글넣기(Metin);return;}
    if(한글&&!dolandyryş_baha&&nyşan<128&&한글넣기(nyşan))return;
    원격글쇠확정();
    if((dolandyryş_baha&&SHIFT_klawişasy&&(nyşan=='t'||nyşan=='T'))||nyşan==0xffc3||nyşan==0xffc9){unsigned char waka[]={30,2,nyşan==0xffc3?2:nyşan==0xffc9?3:1,0,0,0,0};원격입력넣기(waka,7);return;}
    const char *특수=nyşan==0xff08?"\177":nyşan==0xff09?"\t":nyşan==0xff0d?"\r":nyşan==0xff1b?"\033":
        nyşan==0xffff?"\033[3~":nyşan==0xff50?"\033[H":nyşan==0xff57?"\033[F":nyşan==0xff51?"\033[D":
        nyşan==0xff52?"\033[A":nyşan==0xff53?"\033[C":nyşan==0xff54?"\033[B":nyşan==0xff55?"\033[5~":nyşan==0xff56?"\033[6~":0;
    if(특수){원격입력넣기((const unsigned char*)특수,strlen(특수));return;}
    unsigned baha=(nyşan&0xff000000)==0x01000000?nyşan&0xffffff:nyşan;
    if(baha>0x10ffff||(baha>=0xd800&&baha<=0xdfff)||(nyşan>=0xff00&&nyşan<0x1000000))return;
    if(dolandyryş_baha){if(baha>='a'&&baha<='z')baha-=96;else if(baha>='A'&&baha<='Z')baha-=64;}
    글넣기(baha);
}
