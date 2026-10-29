#include "kude_inani.h"
#include <string.h>
#include "두벌식표.h"
static unsigned isilawuli_inani,inkinobho_ye_SHIFT,한글;
typedef struct {unsigned 첫,가운데,끝;} 조합상태;
static 조합상태 조합,loga_umugqa[16];
static unsigned 기록수;
void 원격글쇠확정(void){memset(&조합,0,sizeof(조합));기록수=0;}
void 원격글쇠초기화(void){isilawuli_inani=inkinobho_ye_SHIFT=한글=0;원격글쇠확정();}
static void 글넣기(unsigned inani){
    unsigned char Itekisi[4];unsigned 수;
    if(inani<128){Itekisi[0]=inani;수=1;}else if(inani<2048){Itekisi[0]=0xc0|(inani>>6);Itekisi[1]=0x80|(inani&63);수=2;}
    else if(inani<65536){Itekisi[0]=0xe0|(inani>>12);Itekisi[1]=0x80|((inani>>6)&63);Itekisi[2]=0x80|(inani&63);수=3;}
    else{Itekisi[0]=0xf0|(inani>>18);Itekisi[1]=0x80|((inani>>12)&63);Itekisi[2]=0x80|((inani>>6)&63);Itekisi[3]=0x80|(inani&63);수=4;}
    원격입력넣기(Itekisi,수);
}
static int thola_okufakwayo(const unsigned *okufakwayo_Uhlu,unsigned 수,unsigned inani){for(unsigned 순번=0;순번<수;순번++)if(okufakwayo_Uhlu[순번]==inani)return 순번;return -1;}
static unsigned 겹찾기(const unsigned 표[][3],unsigned 수,unsigned 가,unsigned 나){for(unsigned 순번=0;순번<수;순번++)if(표[순번][0]==가&&표[순번][1]==나)return 표[순번][2];return 0;}
static unsigned 조합글(void){
    if(조합.첫&&조합.가운데)return 0xac00+(thola_okufakwayo(첫소리목록,19,조합.첫)*21+thola_okufakwayo(가운뎃소리목록,21,조합.가운데))*28+(조합.끝?thola_okufakwayo(끝소리목록,28,조합.끝):0);
    return 조합.첫?조합.첫:조합.가운데;
}
static int 한글넣기(unsigned 글쇠){
    unsigned 자모=0;for(unsigned 순번=0;순번<sizeof(inkomba_I_layout)/sizeof(inkomba_I_layout[0]);순번++)if(inkomba_I_layout[순번][0]==글쇠)자모=inkomba_I_layout[순번][1];
    if(!자모&&글쇠>='A'&&글쇠<='Z')return 한글넣기(글쇠+32);if(!자모)return 0;
    unsigned 이전=조합글(),확정=0;조합상태 전=조합;
    if(기록수<16)loga_umugqa[기록수++]=전;
    if(thola_okufakwayo(첫소리목록,19,자모)>=0){
        if(조합.첫&&조합.가운데&&!조합.끝&&thola_okufakwayo(끝소리목록,28,자모)>=0)조합.끝=자모;
        else{unsigned isembozo_inani=겹찾기(겹끝소리,11,조합.끝,자모);if(조합.끝&&isembozo_inani)조합.끝=isembozo_inani;
            else{확정=이전;원격글쇠확정();조합.첫=자모;기록수=1;memset(loga_umugqa,0,sizeof(조합상태));}}
    }else if(조합.끝){
        unsigned 왼쪽=0,오른쪽=조합.끝;for(unsigned 순번=0;순번<11;순번++)if(겹끝소리[순번][2]==조합.끝){왼쪽=겹끝소리[순번][0];오른쪽=겹끝소리[순번][1];break;}
        조합.끝=왼쪽;확정=조합글();원격글쇠확정();조합.첫=오른쪽;조합.가운데=자모;기록수=2;
        memset(loga_umugqa,0,2*sizeof(조합상태));loga_umugqa[1].첫=오른쪽;
    }else if(조합.가운데){unsigned isembozo_inani=겹찾기(겹가운뎃소리,7,조합.가운데,자모);
        if(isembozo_inani)조합.가운데=isembozo_inani;else{확정=이전;원격글쇠확정();조합.가운데=자모;기록수=1;memset(loga_umugqa,0,sizeof(조합상태));}
    }else 조합.가운데=자모;
    if(이전)글넣기(127);if(확정)글넣기(확정);unsigned 지금=조합글();if(지금)글넣기(지금);return 1;
}
void 원격글쇠(unsigned uphawu_ad6f1a96,int 누름){
    if(uphawu_ad6f1a96==0xffe3||uphawu_ad6f1a96==0xffe4){isilawuli_inani=누름;return;}
    if(uphawu_ad6f1a96==0xffe1||uphawu_ad6f1a96==0xffe2){inkinobho_ye_SHIFT=누름;return;}
    if(!누름)return;
    if(uphawu_ad6f1a96==0xffc6||uphawu_ad6f1a96==0xff31||(uphawu_ad6f1a96==32&&inkinobho_ye_SHIFT&&!isilawuli_inani)){
        원격글쇠확정();한글=!한글;unsigned char isigameko[]={30,3,한글,0,0,0,0};원격입력넣기(isigameko,7);return;
    }
    if(uphawu_ad6f1a96==0xff08&&한글&&!isilawuli_inani&&기록수){조합=loga_umugqa[--기록수];글넣기(127);unsigned Itekisi=조합글();if(Itekisi)글넣기(Itekisi);return;}
    if(한글&&!isilawuli_inani&&uphawu_ad6f1a96<128&&한글넣기(uphawu_ad6f1a96))return;
    원격글쇠확정();
    if((isilawuli_inani&&inkinobho_ye_SHIFT&&(uphawu_ad6f1a96=='t'||uphawu_ad6f1a96=='T'))||uphawu_ad6f1a96==0xffc3||uphawu_ad6f1a96==0xffc9){unsigned char isigameko[]={30,2,uphawu_ad6f1a96==0xffc3?2:uphawu_ad6f1a96==0xffc9?3:1,0,0,0,0};원격입력넣기(isigameko,7);return;}
    const char *특수=uphawu_ad6f1a96==0xff08?"\177":uphawu_ad6f1a96==0xff09?"\t":uphawu_ad6f1a96==0xff0d?"\r":uphawu_ad6f1a96==0xff1b?"\033":
        uphawu_ad6f1a96==0xffff?"\033[3~":uphawu_ad6f1a96==0xff50?"\033[H":uphawu_ad6f1a96==0xff57?"\033[F":uphawu_ad6f1a96==0xff51?"\033[D":
        uphawu_ad6f1a96==0xff52?"\033[A":uphawu_ad6f1a96==0xff53?"\033[C":uphawu_ad6f1a96==0xff54?"\033[B":uphawu_ad6f1a96==0xff55?"\033[5~":uphawu_ad6f1a96==0xff56?"\033[6~":0;
    if(특수){원격입력넣기((const unsigned char*)특수,strlen(특수));return;}
    unsigned inani=(uphawu_ad6f1a96&0xff000000)==0x01000000?uphawu_ad6f1a96&0xffffff:uphawu_ad6f1a96;
    if(inani>0x10ffff||(inani>=0xd800&&inani<=0xdfff)||(uphawu_ad6f1a96>=0xff00&&uphawu_ad6f1a96<0x1000000))return;
    if(isilawuli_inani){if(inani>='a'&&inani<='z')inani-=96;else if(inani>='A'&&inani<='Z')inani-=64;}
    글넣기(inani);
}
