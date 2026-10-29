#include "jauh_VALUE.h"
#include <string.h>
#include "두벌식표.h"
static unsigned kawalan_VALUE,kekunci_SHIFT,한글;
typedef struct {unsigned 첫,가운데,끝;} 조합상태;
static 조합상태 조합,LOG_baris[16];
static unsigned LOG_COUNT;
void lakukan_jauh_Kunci(void){memset(&조합,0,sizeof(조합));LOG_COUNT=0;}
void 원격글쇠초기화(void){kawalan_VALUE=kekunci_SHIFT=한글=0;lakukan_jauh_Kunci();}
static void 글넣기(unsigned VALUE){
    unsigned char Teks[4];unsigned 수;
    if(VALUE<128){Teks[0]=VALUE;수=1;}else if(VALUE<2048){Teks[0]=0xc0|(VALUE>>6);Teks[1]=0x80|(VALUE&63);수=2;}
    else if(VALUE<65536){Teks[0]=0xe0|(VALUE>>12);Teks[1]=0x80|((VALUE>>6)&63);Teks[2]=0x80|(VALUE&63);수=3;}
    else{Teks[0]=0xf0|(VALUE>>18);Teks[1]=0x80|((VALUE>>12)&63);Teks[2]=0x80|((VALUE>>6)&63);Teks[3]=0x80|(VALUE&63);수=4;}
    원격입력넣기(Teks,수);
}
static int Cari_pemasukan(const unsigned *pemasukan_Senarai,unsigned 수,unsigned VALUE){for(unsigned 순번=0;순번<수;순번++)if(pemasukan_Senarai[순번]==VALUE)return 순번;return -1;}
static unsigned Cari_Pendua(const unsigned Carian_jadual[][3],unsigned 수,unsigned 가,unsigned 나){for(unsigned 순번=0;순번<수;순번++)if(Carian_jadual[순번][0]==가&&Carian_jadual[순번][1]==나)return Carian_jadual[순번][2];return 0;}
static unsigned 조합글(void){
    if(조합.첫&&조합.가운데)return 0xac00+(Cari_pemasukan(첫소리목록,19,조합.첫)*21+Cari_pemasukan(가운뎃소리목록,21,조합.가운데))*28+(조합.끝?Cari_pemasukan(끝소리목록,28,조합.끝):0);
    return 조합.첫?조합.첫:조합.가운데;
}
static int 한글넣기(unsigned 글쇠){
    unsigned 자모=0;for(unsigned 순번=0;순번<sizeof(Kunci_Navigasi)/sizeof(Kunci_Navigasi[0]);순번++)if(Kunci_Navigasi[순번][0]==글쇠)자모=Kunci_Navigasi[순번][1];
    if(!자모&&글쇠>='A'&&글쇠<='Z')return 한글넣기(글쇠+32);if(!자모)return 0;
    unsigned 이전=조합글(),lakukan_VALUE=0;조합상태 전=조합;
    if(LOG_COUNT<16)LOG_baris[LOG_COUNT++]=전;
    if(Cari_pemasukan(첫소리목록,19,자모)>=0){
        if(조합.첫&&조합.가운데&&!조합.끝&&Cari_pemasukan(끝소리목록,28,자모)>=0)조합.끝=자모;
        else{unsigned tindihan_VALUE=Cari_Pendua(겹끝소리,11,조합.끝,자모);if(조합.끝&&tindihan_VALUE)조합.끝=tindihan_VALUE;
            else{lakukan_VALUE=이전;lakukan_jauh_Kunci();조합.첫=자모;LOG_COUNT=1;memset(LOG_baris,0,sizeof(조합상태));}}
    }else if(조합.끝){
        unsigned 왼쪽=0,RIGHT=조합.끝;for(unsigned 순번=0;순번<11;순번++)if(겹끝소리[순번][2]==조합.끝){왼쪽=겹끝소리[순번][0];RIGHT=겹끝소리[순번][1];break;}
        조합.끝=왼쪽;lakukan_VALUE=조합글();lakukan_jauh_Kunci();조합.첫=RIGHT;조합.가운데=자모;LOG_COUNT=2;
        memset(LOG_baris,0,2*sizeof(조합상태));LOG_baris[1].첫=RIGHT;
    }else if(조합.가운데){unsigned tindihan_VALUE=Cari_Pendua(겹가운뎃소리,7,조합.가운데,자모);
        if(tindihan_VALUE)조합.가운데=tindihan_VALUE;else{lakukan_VALUE=이전;lakukan_jauh_Kunci();조합.가운데=자모;LOG_COUNT=1;memset(LOG_baris,0,sizeof(조합상태));}
    }else 조합.가운데=자모;
    if(이전)글넣기(127);if(lakukan_VALUE)글넣기(lakukan_VALUE);unsigned NOW_VALUE=조합글();if(NOW_VALUE)글넣기(NOW_VALUE);return 1;
}
void 원격글쇠(unsigned simbol,int tekan_VALUE){
    if(simbol==0xffe3||simbol==0xffe4){kawalan_VALUE=tekan_VALUE;return;}
    if(simbol==0xffe1||simbol==0xffe2){kekunci_SHIFT=tekan_VALUE;return;}
    if(!tekan_VALUE)return;
    if(simbol==0xffc6||simbol==0xff31||(simbol==32&&kekunci_SHIFT&&!kawalan_VALUE)){
        lakukan_jauh_Kunci();한글=!한글;unsigned char Peristiwa[]={30,3,한글,0,0,0,0};원격입력넣기(Peristiwa,7);return;
    }
    if(simbol==0xff08&&한글&&!kawalan_VALUE&&LOG_COUNT){조합=LOG_baris[--LOG_COUNT];글넣기(127);unsigned Teks=조합글();if(Teks)글넣기(Teks);return;}
    if(한글&&!kawalan_VALUE&&simbol<128&&한글넣기(simbol))return;
    lakukan_jauh_Kunci();
    if((kawalan_VALUE&&kekunci_SHIFT&&(simbol=='t'||simbol=='T'))||simbol==0xffc3||simbol==0xffc9){unsigned char Peristiwa[]={30,2,simbol==0xffc3?2:simbol==0xffc9?3:1,0,0,0,0};원격입력넣기(Peristiwa,7);return;}
    const char *특수=simbol==0xff08?"\177":simbol==0xff09?"\t":simbol==0xff0d?"\r":simbol==0xff1b?"\033":
        simbol==0xffff?"\033[3~":simbol==0xff50?"\033[H":simbol==0xff57?"\033[F":simbol==0xff51?"\033[D":
        simbol==0xff52?"\033[A":simbol==0xff53?"\033[C":simbol==0xff54?"\033[B":simbol==0xff55?"\033[5~":simbol==0xff56?"\033[6~":0;
    if(특수){원격입력넣기((const unsigned char*)특수,strlen(특수));return;}
    unsigned VALUE=(simbol&0xff000000)==0x01000000?simbol&0xffffff:simbol;
    if(VALUE>0x10ffff||(VALUE>=0xd800&&VALUE<=0xdfff)||(simbol>=0xff00&&simbol<0x1000000))return;
    if(kawalan_VALUE){if(VALUE>='a'&&VALUE<='z')VALUE-=96;else if(VALUE>='A'&&VALUE<='Z')VALUE-=64;}
    글넣기(VALUE);
}
