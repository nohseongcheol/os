#include "uzaq_VALUE.h"
#include <string.h>
#include "두벌식표.h"
static unsigned nəzarət_VALUE,SHIFT_düyməsi,한글;
typedef struct {unsigned 첫,가운데,끝;} 조합상태;
static 조합상태 조합,LOG_yaz[16];
static unsigned LOG_COUNT;
void 원격글쇠확정(void){memset(&조합,0,sizeof(조합));LOG_COUNT=0;}
void 원격글쇠초기화(void){nəzarət_VALUE=SHIFT_düyməsi=한글=0;원격글쇠확정();}
static void 글넣기(unsigned VALUE){
    unsigned char Mətn[4];unsigned 수;
    if(VALUE<128){Mətn[0]=VALUE;수=1;}else if(VALUE<2048){Mətn[0]=0xc0|(VALUE>>6);Mətn[1]=0x80|(VALUE&63);수=2;}
    else if(VALUE<65536){Mətn[0]=0xe0|(VALUE>>12);Mətn[1]=0x80|((VALUE>>6)&63);Mətn[2]=0x80|(VALUE&63);수=3;}
    else{Mətn[0]=0xf0|(VALUE>>18);Mətn[1]=0x80|((VALUE>>12)&63);Mətn[2]=0x80|((VALUE>>6)&63);Mətn[3]=0x80|(VALUE&63);수=4;}
    원격입력넣기(Mətn,수);
}
static int FIND_daxiletmə(const unsigned *daxiletmə_Siyahı,unsigned 수,unsigned VALUE){for(unsigned 순번=0;순번<수;순번++)if(daxiletmə_Siyahı[순번]==VALUE)return 순번;return -1;}
static unsigned 겹찾기(const unsigned LOOKUP_cədvəl[][3],unsigned 수,unsigned 가,unsigned 나){for(unsigned 순번=0;순번<수;순번++)if(LOOKUP_cədvəl[순번][0]==가&&LOOKUP_cədvəl[순번][1]==나)return LOOKUP_cədvəl[순번][2];return 0;}
static unsigned 조합글(void){
    if(조합.첫&&조합.가운데)return 0xac00+(FIND_daxiletmə(첫소리목록,19,조합.첫)*21+FIND_daxiletmə(가운뎃소리목록,21,조합.가운데))*28+(조합.끝?FIND_daxiletmə(끝소리목록,28,조합.끝):0);
    return 조합.첫?조합.첫:조합.가운데;
}
static int 한글넣기(unsigned 글쇠){
    unsigned 자모=0;for(unsigned 순번=0;순번<sizeof(Açar_Düzüm)/sizeof(Açar_Düzüm[0]);순번++)if(Açar_Düzüm[순번][0]==글쇠)자모=Açar_Düzüm[순번][1];
    if(!자모&&글쇠>='A'&&글쇠<='Z')return 한글넣기(글쇠+32);if(!자모)return 0;
    unsigned 이전=조합글(),확정=0;조합상태 전=조합;
    if(LOG_COUNT<16)LOG_yaz[LOG_COUNT++]=전;
    if(FIND_daxiletmə(첫소리목록,19,자모)>=0){
        if(조합.첫&&조합.가운데&&!조합.끝&&FIND_daxiletmə(끝소리목록,28,자모)>=0)조합.끝=자모;
        else{unsigned yardımçı_qrafik_VALUE=겹찾기(겹끝소리,11,조합.끝,자모);if(조합.끝&&yardımçı_qrafik_VALUE)조합.끝=yardımçı_qrafik_VALUE;
            else{확정=이전;원격글쇠확정();조합.첫=자모;LOG_COUNT=1;memset(LOG_yaz,0,sizeof(조합상태));}}
    }else if(조합.끝){
        unsigned 왼쪽=0,RIGHT=조합.끝;for(unsigned 순번=0;순번<11;순번++)if(겹끝소리[순번][2]==조합.끝){왼쪽=겹끝소리[순번][0];RIGHT=겹끝소리[순번][1];break;}
        조합.끝=왼쪽;확정=조합글();원격글쇠확정();조합.첫=RIGHT;조합.가운데=자모;LOG_COUNT=2;
        memset(LOG_yaz,0,2*sizeof(조합상태));LOG_yaz[1].첫=RIGHT;
    }else if(조합.가운데){unsigned yardımçı_qrafik_VALUE=겹찾기(겹가운뎃소리,7,조합.가운데,자모);
        if(yardımçı_qrafik_VALUE)조합.가운데=yardımçı_qrafik_VALUE;else{확정=이전;원격글쇠확정();조합.가운데=자모;LOG_COUNT=1;memset(LOG_yaz,0,sizeof(조합상태));}
    }else 조합.가운데=자모;
    if(이전)글넣기(127);if(확정)글넣기(확정);unsigned NOW_VALUE=조합글();if(NOW_VALUE)글넣기(NOW_VALUE);return 1;
}
void 원격글쇠(unsigned simvol,int bas_VALUE){
    if(simvol==0xffe3||simvol==0xffe4){nəzarət_VALUE=bas_VALUE;return;}
    if(simvol==0xffe1||simvol==0xffe2){SHIFT_düyməsi=bas_VALUE;return;}
    if(!bas_VALUE)return;
    if(simvol==0xffc6||simvol==0xff31||(simvol==32&&SHIFT_düyməsi&&!nəzarət_VALUE)){
        원격글쇠확정();한글=!한글;unsigned char hadisə[]={30,3,한글,0,0,0,0};원격입력넣기(hadisə,7);return;
    }
    if(simvol==0xff08&&한글&&!nəzarət_VALUE&&LOG_COUNT){조합=LOG_yaz[--LOG_COUNT];글넣기(127);unsigned Mətn=조합글();if(Mətn)글넣기(Mətn);return;}
    if(한글&&!nəzarət_VALUE&&simvol<128&&한글넣기(simvol))return;
    원격글쇠확정();
    if((nəzarət_VALUE&&SHIFT_düyməsi&&(simvol=='t'||simvol=='T'))||simvol==0xffc3||simvol==0xffc9){unsigned char hadisə[]={30,2,simvol==0xffc3?2:simvol==0xffc9?3:1,0,0,0,0};원격입력넣기(hadisə,7);return;}
    const char *특수=simvol==0xff08?"\177":simvol==0xff09?"\t":simvol==0xff0d?"\r":simvol==0xff1b?"\033":
        simvol==0xffff?"\033[3~":simvol==0xff50?"\033[H":simvol==0xff57?"\033[F":simvol==0xff51?"\033[D":
        simvol==0xff52?"\033[A":simvol==0xff53?"\033[C":simvol==0xff54?"\033[B":simvol==0xff55?"\033[5~":simvol==0xff56?"\033[6~":0;
    if(특수){원격입력넣기((const unsigned char*)특수,strlen(특수));return;}
    unsigned VALUE=(simvol&0xff000000)==0x01000000?simvol&0xffffff:simvol;
    if(VALUE>0x10ffff||(VALUE>=0xd800&&VALUE<=0xdfff)||(simvol>=0xff00&&simvol<0x1000000))return;
    if(nəzarət_VALUE){if(VALUE>='a'&&VALUE<='z')VALUE-=96;else if(VALUE>='A'&&VALUE<='Z')VALUE-=64;}
    글넣기(VALUE);
}
