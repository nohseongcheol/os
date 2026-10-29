#include "kude_ixabiso.h"
#include <string.h>
#include "두벌식표.h"
static unsigned isilawuli_ixabiso,iqhosha_le_SHIFT,한글;
typedef struct {unsigned 첫,가운데,끝;} 조합상태;
static 조합상태 조합,ilog_umqolo[16];
static unsigned 기록수;
void 원격글쇠확정(void){memset(&조합,0,sizeof(조합));기록수=0;}
void 원격글쇠초기화(void){isilawuli_ixabiso=iqhosha_le_SHIFT=한글=0;원격글쇠확정();}
static void 글넣기(unsigned ixabiso){
    unsigned char Umbhalo[4];unsigned 수;
    if(ixabiso<128){Umbhalo[0]=ixabiso;수=1;}else if(ixabiso<2048){Umbhalo[0]=0xc0|(ixabiso>>6);Umbhalo[1]=0x80|(ixabiso&63);수=2;}
    else if(ixabiso<65536){Umbhalo[0]=0xe0|(ixabiso>>12);Umbhalo[1]=0x80|((ixabiso>>6)&63);Umbhalo[2]=0x80|(ixabiso&63);수=3;}
    else{Umbhalo[0]=0xf0|(ixabiso>>18);Umbhalo[1]=0x80|((ixabiso>>12)&63);Umbhalo[2]=0x80|((ixabiso>>6)&63);Umbhalo[3]=0x80|(ixabiso&63);수=4;}
    원격입력넣기(Umbhalo,수);
}
static int fumana_ufako_nkcukacha(const unsigned *ufako_nkcukacha_uludwe,unsigned 수,unsigned ixabiso){for(unsigned 순번=0;순번<수;순번++)if(ufako_nkcukacha_uludwe[순번]==ixabiso)return 순번;return -1;}
static unsigned 겹찾기(const unsigned 표[][3],unsigned 수,unsigned 가,unsigned 나){for(unsigned 순번=0;순번<수;순번++)if(표[순번][0]==가&&표[순번][1]==나)return 표[순번][2];return 0;}
static unsigned 조합글(void){
    if(조합.첫&&조합.가운데)return 0xac00+(fumana_ufako_nkcukacha(첫소리목록,19,조합.첫)*21+fumana_ufako_nkcukacha(가운뎃소리목록,21,조합.가운데))*28+(조합.끝?fumana_ufako_nkcukacha(끝소리목록,28,조합.끝):0);
    return 조합.첫?조합.첫:조합.가운데;
}
static int 한글넣기(unsigned 글쇠){
    unsigned 자모=0;for(unsigned 순번=0;순번<sizeof(iqhosha_ubume)/sizeof(iqhosha_ubume[0]);순번++)if(iqhosha_ubume[순번][0]==글쇠)자모=iqhosha_ubume[순번][1];
    if(!자모&&글쇠>='A'&&글쇠<='Z')return 한글넣기(글쇠+32);if(!자모)return 0;
    unsigned 이전=조합글(),확정=0;조합상태 전=조합;
    if(기록수<16)ilog_umqolo[기록수++]=전;
    if(fumana_ufako_nkcukacha(첫소리목록,19,자모)>=0){
        if(조합.첫&&조합.가운데&&!조합.끝&&fumana_ufako_nkcukacha(끝소리목록,28,자모)>=0)조합.끝=자모;
        else{unsigned ubume_obungaphaya_ixabiso=겹찾기(겹끝소리,11,조합.끝,자모);if(조합.끝&&ubume_obungaphaya_ixabiso)조합.끝=ubume_obungaphaya_ixabiso;
            else{확정=이전;원격글쇠확정();조합.첫=자모;기록수=1;memset(ilog_umqolo,0,sizeof(조합상태));}}
    }else if(조합.끝){
        unsigned 왼쪽=0,오른쪽=조합.끝;for(unsigned 순번=0;순번<11;순번++)if(겹끝소리[순번][2]==조합.끝){왼쪽=겹끝소리[순번][0];오른쪽=겹끝소리[순번][1];break;}
        조합.끝=왼쪽;확정=조합글();원격글쇠확정();조합.첫=오른쪽;조합.가운데=자모;기록수=2;
        memset(ilog_umqolo,0,2*sizeof(조합상태));ilog_umqolo[1].첫=오른쪽;
    }else if(조합.가운데){unsigned ubume_obungaphaya_ixabiso=겹찾기(겹가운뎃소리,7,조합.가운데,자모);
        if(ubume_obungaphaya_ixabiso)조합.가운데=ubume_obungaphaya_ixabiso;else{확정=이전;원격글쇠확정();조합.가운데=자모;기록수=1;memset(ilog_umqolo,0,sizeof(조합상태));}
    }else 조합.가운데=자모;
    if(이전)글넣기(127);if(확정)글넣기(확정);unsigned 지금=조합글();if(지금)글넣기(지금);return 1;
}
void 원격글쇠(unsigned isimboli,int 누름){
    if(isimboli==0xffe3||isimboli==0xffe4){isilawuli_ixabiso=누름;return;}
    if(isimboli==0xffe1||isimboli==0xffe2){iqhosha_le_SHIFT=누름;return;}
    if(!누름)return;
    if(isimboli==0xffc6||isimboli==0xff31||(isimboli==32&&iqhosha_le_SHIFT&&!isilawuli_ixabiso)){
        원격글쇠확정();한글=!한글;unsigned char umcimbi[]={30,3,한글,0,0,0,0};원격입력넣기(umcimbi,7);return;
    }
    if(isimboli==0xff08&&한글&&!isilawuli_ixabiso&&기록수){조합=ilog_umqolo[--기록수];글넣기(127);unsigned Umbhalo=조합글();if(Umbhalo)글넣기(Umbhalo);return;}
    if(한글&&!isilawuli_ixabiso&&isimboli<128&&한글넣기(isimboli))return;
    원격글쇠확정();
    if((isilawuli_ixabiso&&iqhosha_le_SHIFT&&(isimboli=='t'||isimboli=='T'))||isimboli==0xffc3||isimboli==0xffc9){unsigned char umcimbi[]={30,2,isimboli==0xffc3?2:isimboli==0xffc9?3:1,0,0,0,0};원격입력넣기(umcimbi,7);return;}
    const char *특수=isimboli==0xff08?"\177":isimboli==0xff09?"\t":isimboli==0xff0d?"\r":isimboli==0xff1b?"\033":
        isimboli==0xffff?"\033[3~":isimboli==0xff50?"\033[H":isimboli==0xff57?"\033[F":isimboli==0xff51?"\033[D":
        isimboli==0xff52?"\033[A":isimboli==0xff53?"\033[C":isimboli==0xff54?"\033[B":isimboli==0xff55?"\033[5~":isimboli==0xff56?"\033[6~":0;
    if(특수){원격입력넣기((const unsigned char*)특수,strlen(특수));return;}
    unsigned ixabiso=(isimboli&0xff000000)==0x01000000?isimboli&0xffffff:isimboli;
    if(ixabiso>0x10ffff||(ixabiso>=0xd800&&ixabiso<=0xdfff)||(isimboli>=0xff00&&isimboli<0x1000000))return;
    if(isilawuli_ixabiso){if(ixabiso>='a'&&ixabiso<='z')ixabiso-=96;else if(ixabiso>='A'&&ixabiso<='Z')ixabiso-=64;}
    글넣기(ixabiso);
}
