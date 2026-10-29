#include "uzak_değer.h"
#include <string.h>
#include "두벌식표.h"
static unsigned denetim_değer,SHIFT_tuşu,한글;
typedef struct {unsigned 첫,가운데,끝;} 조합상태;
static 조합상태 조합,LOG_KAYIT[16];
static unsigned LOG_BAĞ_DEĞ_SAY;
void commit_uzak_tuş(void){memset(&조합,0,sizeof(조합));LOG_BAĞ_DEĞ_SAY=0;}
void 원격글쇠초기화(void){denetim_değer=SHIFT_tuşu=한글=0;commit_uzak_tuş();}
static void 글넣기(unsigned değer){
    unsigned char metin[4];unsigned 수;
    if(değer<128){metin[0]=değer;수=1;}else if(değer<2048){metin[0]=0xc0|(değer>>6);metin[1]=0x80|(değer&63);수=2;}
    else if(değer<65536){metin[0]=0xe0|(değer>>12);metin[1]=0x80|((değer>>6)&63);metin[2]=0x80|(değer&63);수=3;}
    else{metin[0]=0xf0|(değer>>18);metin[1]=0x80|((değer>>12)&63);metin[2]=0x80|((değer>>6)&63);metin[3]=0x80|(değer&63);수=4;}
    akış_uzak_artış(metin,수);
}
static int BUL_girdi(const unsigned *girdi_Liste,unsigned 수,unsigned değer){for(unsigned 순번=0;순번<수;순번++)if(girdi_Liste[순번]==değer)return 순번;return -1;}
static unsigned BUL_kopya(const unsigned arama_tablosu[][3],unsigned 수,unsigned 가,unsigned SANİYE_işlenen){for(unsigned 순번=0;순번<수;순번++)if(arama_tablosu[순번][0]==가&&arama_tablosu[순번][1]==SANİYE_işlenen)return arama_tablosu[순번][2];return 0;}
static unsigned 조합글(void){
    if(조합.첫&&조합.가운데)return 0xac00+(BUL_girdi(첫소리목록,19,조합.첫)*21+BUL_girdi(가운뎃소리목록,21,조합.가운데))*28+(조합.끝?BUL_girdi(끝소리목록,28,조합.끝):0);
    return 조합.첫?조합.첫:조합.가운데;
}
static int 한글넣기(unsigned tuş_vuruş){
    unsigned 자모=0;for(unsigned 순번=0;순번<sizeof(tuş_Düzen)/sizeof(tuş_Düzen[0]);순번++)if(tuş_Düzen[순번][0]==tuş_vuruş)자모=tuş_Düzen[순번][1];
    if(!자모&&tuş_vuruş>='A'&&tuş_vuruş<='Z')return 한글넣기(tuş_vuruş+32);if(!자모)return 0;
    unsigned Önceki_öğe=조합글(),commit_değer=0;조합상태 전=조합;
    if(LOG_BAĞ_DEĞ_SAY<16)LOG_KAYIT[LOG_BAĞ_DEĞ_SAY++]=전;
    if(BUL_girdi(첫소리목록,19,자모)>=0){
        if(조합.첫&&조합.가운데&&!조합.끝&&BUL_girdi(끝소리목록,28,자모)>=0)조합.끝=자모;
        else{unsigned katman_değer=BUL_kopya(겹끝소리,11,조합.끝,자모);if(조합.끝&&katman_değer)조합.끝=katman_değer;
            else{commit_değer=Önceki_öğe;commit_uzak_tuş();조합.첫=자모;LOG_BAĞ_DEĞ_SAY=1;memset(LOG_KAYIT,0,sizeof(조합상태));}}
    }else if(조합.끝){
        unsigned 왼쪽=0,hak=조합.끝;for(unsigned 순번=0;순번<11;순번++)if(겹끝소리[순번][2]==조합.끝){왼쪽=겹끝소리[순번][0];hak=겹끝소리[순번][1];break;}
        조합.끝=왼쪽;commit_değer=조합글();commit_uzak_tuş();조합.첫=hak;조합.가운데=자모;LOG_BAĞ_DEĞ_SAY=2;
        memset(LOG_KAYIT,0,2*sizeof(조합상태));LOG_KAYIT[1].첫=hak;
    }else if(조합.가운데){unsigned katman_değer=BUL_kopya(겹가운뎃소리,7,조합.가운데,자모);
        if(katman_değer)조합.가운데=katman_değer;else{commit_değer=Önceki_öğe;commit_uzak_tuş();조합.가운데=자모;LOG_BAĞ_DEĞ_SAY=1;memset(LOG_KAYIT,0,sizeof(조합상태));}
    }else 조합.가운데=자모;
    if(Önceki_öğe)글넣기(127);if(commit_değer)글넣기(commit_değer);unsigned ŞİMDİ_değer=조합글();if(ŞİMDİ_değer)글넣기(ŞİMDİ_değer);return 1;
}
void uzak_tuş_vuruş(unsigned simge,int bas_değer){
    if(simge==0xffe3||simge==0xffe4){denetim_değer=bas_değer;return;}
    if(simge==0xffe1||simge==0xffe2){SHIFT_tuşu=bas_değer;return;}
    if(!bas_değer)return;
    if(simge==0xffc6||simge==0xff31||(simge==32&&SHIFT_tuşu&&!denetim_değer)){
        commit_uzak_tuş();한글=!한글;unsigned char Olay[]={30,3,한글,0,0,0,0};akış_uzak_artış(Olay,7);return;
    }
    if(simge==0xff08&&한글&&!denetim_değer&&LOG_BAĞ_DEĞ_SAY){조합=LOG_KAYIT[--LOG_BAĞ_DEĞ_SAY];글넣기(127);unsigned metin=조합글();if(metin)글넣기(metin);return;}
    if(한글&&!denetim_değer&&simge<128&&한글넣기(simge))return;
    commit_uzak_tuş();
    if((denetim_değer&&SHIFT_tuşu&&(simge=='t'||simge=='T'))||simge==0xffc3||simge==0xffc9){unsigned char Olay[]={30,2,simge==0xffc3?2:simge==0xffc9?3:1,0,0,0,0};akış_uzak_artış(Olay,7);return;}
    const char *특수=simge==0xff08?"\177":simge==0xff09?"\t":simge==0xff0d?"\r":simge==0xff1b?"\033":
        simge==0xffff?"\033[3~":simge==0xff50?"\033[H":simge==0xff57?"\033[F":simge==0xff51?"\033[D":
        simge==0xff52?"\033[A":simge==0xff53?"\033[C":simge==0xff54?"\033[B":simge==0xff55?"\033[5~":simge==0xff56?"\033[6~":0;
    if(특수){akış_uzak_artış((const unsigned char*)특수,strlen(특수));return;}
    unsigned değer=(simge&0xff000000)==0x01000000?simge&0xffffff:simge;
    if(değer>0x10ffff||(değer>=0xd800&&değer<=0xdfff)||(simge>=0xff00&&simge<0x1000000))return;
    if(denetim_değer){if(değer>='a'&&değer<='z')değer-=96;else if(değer>='A'&&değer<='Z')değer-=64;}
    글넣기(değer);
}
