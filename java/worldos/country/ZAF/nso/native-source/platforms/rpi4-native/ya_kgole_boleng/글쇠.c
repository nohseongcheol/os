#include "ya_kgole_boleng.h"
#include <string.h>
#include "두벌식표.h"
static unsigned taolo_boleng,khii_ya_SHIFT,한글;
typedef struct {unsigned 첫,가운데,끝;} 조합상태;
static 조합상태 조합,pego_rei[16];
static unsigned 기록수;
void 원격글쇠확정(void){memset(&조합,0,sizeof(조합));기록수=0;}
void 원격글쇠초기화(void){taolo_boleng=khii_ya_SHIFT=한글=0;원격글쇠확정();}
static void 글넣기(unsigned boleng){
    unsigned char Sengwalwa[4];unsigned 수;
    if(boleng<128){Sengwalwa[0]=boleng;수=1;}else if(boleng<2048){Sengwalwa[0]=0xc0|(boleng>>6);Sengwalwa[1]=0x80|(boleng&63);수=2;}
    else if(boleng<65536){Sengwalwa[0]=0xe0|(boleng>>12);Sengwalwa[1]=0x80|((boleng>>6)&63);Sengwalwa[2]=0x80|(boleng&63);수=3;}
    else{Sengwalwa[0]=0xf0|(boleng>>18);Sengwalwa[1]=0x80|((boleng>>12)&63);Sengwalwa[2]=0x80|((boleng>>6)&63);Sengwalwa[3]=0x80|(boleng&63);수=4;}
    원격입력넣기(Sengwalwa,수);
}
static int hwetša_go_tsenya_tshedimošo(const unsigned *go_tsenya_tshedimošo_Lenaneo,unsigned 수,unsigned boleng){for(unsigned 순번=0;순번<수;순번++)if(go_tsenya_tshedimošo_Lenaneo[순번]==boleng)return 순번;return -1;}
static unsigned 겹찾기(const unsigned 표[][3],unsigned 수,unsigned 가,unsigned 나){for(unsigned 순번=0;순번<수;순번++)if(표[순번][0]==가&&표[순번][1]==나)return 표[순번][2];return 0;}
static unsigned 조합글(void){
    if(조합.첫&&조합.가운데)return 0xac00+(hwetša_go_tsenya_tshedimošo(첫소리목록,19,조합.첫)*21+hwetša_go_tsenya_tshedimošo(가운뎃소리목록,21,조합.가운데))*28+(조합.끝?hwetša_go_tsenya_tshedimošo(끝소리목록,28,조합.끝):0);
    return 조합.첫?조합.첫:조합.가운데;
}
static int 한글넣기(unsigned 글쇠){
    unsigned 자모=0;for(unsigned 순번=0;순번<sizeof(khii_Sebopego)/sizeof(khii_Sebopego[0]);순번++)if(khii_Sebopego[순번][0]==글쇠)자모=khii_Sebopego[순번][1];
    if(!자모&&글쇠>='A'&&글쇠<='Z')return 한글넣기(글쇠+32);if(!자모)return 0;
    unsigned 이전=조합글(),확정=0;조합상태 전=조합;
    if(기록수<16)pego_rei[기록수++]=전;
    if(hwetša_go_tsenya_tshedimošo(첫소리목록,19,자모)>=0){
        if(조합.첫&&조합.가운데&&!조합.끝&&hwetša_go_tsenya_tshedimošo(끝소리목록,28,자모)>=0)조합.끝=자모;
        else{unsigned go_tlaleletša_boleng=겹찾기(겹끝소리,11,조합.끝,자모);if(조합.끝&&go_tlaleletša_boleng)조합.끝=go_tlaleletša_boleng;
            else{확정=이전;원격글쇠확정();조합.첫=자모;기록수=1;memset(pego_rei,0,sizeof(조합상태));}}
    }else if(조합.끝){
        unsigned 왼쪽=0,오른쪽=조합.끝;for(unsigned 순번=0;순번<11;순번++)if(겹끝소리[순번][2]==조합.끝){왼쪽=겹끝소리[순번][0];오른쪽=겹끝소리[순번][1];break;}
        조합.끝=왼쪽;확정=조합글();원격글쇠확정();조합.첫=오른쪽;조합.가운데=자모;기록수=2;
        memset(pego_rei,0,2*sizeof(조합상태));pego_rei[1].첫=오른쪽;
    }else if(조합.가운데){unsigned go_tlaleletša_boleng=겹찾기(겹가운뎃소리,7,조합.가운데,자모);
        if(go_tlaleletša_boleng)조합.가운데=go_tlaleletša_boleng;else{확정=이전;원격글쇠확정();조합.가운데=자모;기록수=1;memset(pego_rei,0,sizeof(조합상태));}
    }else 조합.가운데=자모;
    if(이전)글넣기(127);if(확정)글넣기(확정);unsigned 지금=조합글();if(지금)글넣기(지금);return 1;
}
void 원격글쇠(unsigned leswao,int 누름){
    if(leswao==0xffe3||leswao==0xffe4){taolo_boleng=누름;return;}
    if(leswao==0xffe1||leswao==0xffe2){khii_ya_SHIFT=누름;return;}
    if(!누름)return;
    if(leswao==0xffc6||leswao==0xff31||(leswao==32&&khii_ya_SHIFT&&!taolo_boleng)){
        원격글쇠확정();한글=!한글;unsigned char tiragalo[]={30,3,한글,0,0,0,0};원격입력넣기(tiragalo,7);return;
    }
    if(leswao==0xff08&&한글&&!taolo_boleng&&기록수){조합=pego_rei[--기록수];글넣기(127);unsigned Sengwalwa=조합글();if(Sengwalwa)글넣기(Sengwalwa);return;}
    if(한글&&!taolo_boleng&&leswao<128&&한글넣기(leswao))return;
    원격글쇠확정();
    if((taolo_boleng&&khii_ya_SHIFT&&(leswao=='t'||leswao=='T'))||leswao==0xffc3||leswao==0xffc9){unsigned char tiragalo[]={30,2,leswao==0xffc3?2:leswao==0xffc9?3:1,0,0,0,0};원격입력넣기(tiragalo,7);return;}
    const char *특수=leswao==0xff08?"\177":leswao==0xff09?"\t":leswao==0xff0d?"\r":leswao==0xff1b?"\033":
        leswao==0xffff?"\033[3~":leswao==0xff50?"\033[H":leswao==0xff57?"\033[F":leswao==0xff51?"\033[D":
        leswao==0xff52?"\033[A":leswao==0xff53?"\033[C":leswao==0xff54?"\033[B":leswao==0xff55?"\033[5~":leswao==0xff56?"\033[6~":0;
    if(특수){원격입력넣기((const unsigned char*)특수,strlen(특수));return;}
    unsigned boleng=(leswao&0xff000000)==0x01000000?leswao&0xffffff:leswao;
    if(boleng>0x10ffff||(boleng>=0xd800&&boleng<=0xdfff)||(leswao>=0xff00&&leswao<0x1000000))return;
    if(taolo_boleng){if(boleng>='a'&&boleng<='z')boleng-=96;else if(boleng>='A'&&boleng<='Z')boleng-=64;}
    글넣기(boleng);
}
