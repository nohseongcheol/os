#include "attāls_VALUE.h"
#include <string.h>
#include "두벌식표.h"
static unsigned vadība_VALUE,윗글쇠,한글;
typedef struct {unsigned 첫,가운데,끝;} salikums_Statuss;
static salikums_Statuss salikums_VALUE,LOG_RECORD[16];
static unsigned LOG_COUNT;
void izpilde_attāls_Atslēga(void){memset(&salikums_VALUE,0,sizeof(salikums_VALUE));LOG_COUNT=0;}
void 원격글쇠초기화(void){vadība_VALUE=윗글쇠=한글=0;izpilde_attāls_Atslēga();}
static void 글넣기(unsigned VALUE){
    unsigned char Teksts[4];unsigned numurs;
    if(VALUE<128){Teksts[0]=VALUE;numurs=1;}else if(VALUE<2048){Teksts[0]=0xc0|(VALUE>>6);Teksts[1]=0x80|(VALUE&63);numurs=2;}
    else if(VALUE<65536){Teksts[0]=0xe0|(VALUE>>12);Teksts[1]=0x80|((VALUE>>6)&63);Teksts[2]=0x80|(VALUE&63);numurs=3;}
    else{Teksts[0]=0xf0|(VALUE>>18);Teksts[1]=0x80|((VALUE>>12)&63);Teksts[2]=0x80|((VALUE>>6)&63);Teksts[3]=0x80|(VALUE&63);numurs=4;}
    원격입력넣기(Teksts,numurs);
}
static int FIND_ievade(const unsigned *ievade_Saraksts,unsigned numurs,unsigned VALUE){for(unsigned 순번=0;순번<numurs;순번++)if(ievade_Saraksts[순번]==VALUE)return 순번;return -1;}
static unsigned FIND_dublikāts(const unsigned LOOKUP_tabula[][3],unsigned numurs,unsigned 가,unsigned SECOND_operands){for(unsigned 순번=0;순번<numurs;순번++)if(LOOKUP_tabula[순번][0]==가&&LOOKUP_tabula[순번][1]==SECOND_operands)return LOOKUP_tabula[순번][2];return 0;}
static unsigned 조합글(void){
    if(salikums_VALUE.첫&&salikums_VALUE.가운데)return 0xac00+(FIND_ievade(첫소리목록,19,salikums_VALUE.첫)*21+FIND_ievade(가운뎃소리목록,21,salikums_VALUE.가운데))*28+(salikums_VALUE.끝?FIND_ievade(끝소리목록,28,salikums_VALUE.끝):0);
    return salikums_VALUE.첫?salikums_VALUE.첫:salikums_VALUE.가운데;
}
static int 한글넣기(unsigned Atslēga_ciparrokraksta_vilkums){
    unsigned 자모=0;for(unsigned 순번=0;순번<sizeof(Atslēga_shēma)/sizeof(Atslēga_shēma[0]);순번++)if(Atslēga_shēma[순번][0]==Atslēga_ciparrokraksta_vilkums)자모=Atslēga_shēma[순번][1];
    if(!자모&&Atslēga_ciparrokraksta_vilkums>='A'&&Atslēga_ciparrokraksta_vilkums<='Z')return 한글넣기(Atslēga_ciparrokraksta_vilkums+32);if(!자모)return 0;
    unsigned 이전=조합글(),izpilde_VALUE=0;salikums_Statuss 전=salikums_VALUE;
    if(LOG_COUNT<16)LOG_RECORD[LOG_COUNT++]=전;
    if(FIND_ievade(첫소리목록,19,자모)>=0){
        if(salikums_VALUE.첫&&salikums_VALUE.가운데&&!salikums_VALUE.끝&&FIND_ievade(끝소리목록,28,자모)>=0)salikums_VALUE.끝=자모;
        else{unsigned pārklājums_VALUE=FIND_dublikāts(겹끝소리,11,salikums_VALUE.끝,자모);if(salikums_VALUE.끝&&pārklājums_VALUE)salikums_VALUE.끝=pārklājums_VALUE;
            else{izpilde_VALUE=이전;izpilde_attāls_Atslēga();salikums_VALUE.첫=자모;LOG_COUNT=1;memset(LOG_RECORD,0,sizeof(salikums_Statuss));}}
    }else if(salikums_VALUE.끝){
        unsigned 왼쪽=0,RIGHT=salikums_VALUE.끝;for(unsigned 순번=0;순번<11;순번++)if(겹끝소리[순번][2]==salikums_VALUE.끝){왼쪽=겹끝소리[순번][0];RIGHT=겹끝소리[순번][1];break;}
        salikums_VALUE.끝=왼쪽;izpilde_VALUE=조합글();izpilde_attāls_Atslēga();salikums_VALUE.첫=RIGHT;salikums_VALUE.가운데=자모;LOG_COUNT=2;
        memset(LOG_RECORD,0,2*sizeof(salikums_Statuss));LOG_RECORD[1].첫=RIGHT;
    }else if(salikums_VALUE.가운데){unsigned pārklājums_VALUE=FIND_dublikāts(겹가운뎃소리,7,salikums_VALUE.가운데,자모);
        if(pārklājums_VALUE)salikums_VALUE.가운데=pārklājums_VALUE;else{izpilde_VALUE=이전;izpilde_attāls_Atslēga();salikums_VALUE.가운데=자모;LOG_COUNT=1;memset(LOG_RECORD,0,sizeof(salikums_Statuss));}
    }else salikums_VALUE.가운데=자모;
    if(이전)글넣기(127);if(izpilde_VALUE)글넣기(izpilde_VALUE);unsigned NOW_VALUE=조합글();if(NOW_VALUE)글넣기(NOW_VALUE);return 1;
}
void attāls_Atslēga_ciparrokraksta_vilkums(unsigned simbols,int nospiest_VALUE){
    if(simbols==0xffe3||simbols==0xffe4){vadība_VALUE=nospiest_VALUE;return;}
    if(simbols==0xffe1||simbols==0xffe2){윗글쇠=nospiest_VALUE;return;}
    if(!nospiest_VALUE)return;
    if(simbols==0xffc6||simbols==0xff31||(simbols==32&&윗글쇠&&!vadība_VALUE)){
        izpilde_attāls_Atslēga();한글=!한글;unsigned char Notikums[]={30,3,한글,0,0,0,0};원격입력넣기(Notikums,7);return;
    }
    if(simbols==0xff08&&한글&&!vadība_VALUE&&LOG_COUNT){salikums_VALUE=LOG_RECORD[--LOG_COUNT];글넣기(127);unsigned Teksts=조합글();if(Teksts)글넣기(Teksts);return;}
    if(한글&&!vadība_VALUE&&simbols<128&&한글넣기(simbols))return;
    izpilde_attāls_Atslēga();
    if((vadība_VALUE&&윗글쇠&&(simbols=='t'||simbols=='T'))||simbols==0xffc3||simbols==0xffc9){unsigned char Notikums[]={30,2,simbols==0xffc3?2:simbols==0xffc9?3:1,0,0,0,0};원격입력넣기(Notikums,7);return;}
    const char *특수=simbols==0xff08?"\177":simbols==0xff09?"\t":simbols==0xff0d?"\r":simbols==0xff1b?"\033":
        simbols==0xffff?"\033[3~":simbols==0xff50?"\033[H":simbols==0xff57?"\033[F":simbols==0xff51?"\033[D":
        simbols==0xff52?"\033[A":simbols==0xff53?"\033[C":simbols==0xff54?"\033[B":simbols==0xff55?"\033[5~":simbols==0xff56?"\033[6~":0;
    if(특수){원격입력넣기((const unsigned char*)특수,strlen(특수));return;}
    unsigned VALUE=(simbols&0xff000000)==0x01000000?simbols&0xffffff:simbols;
    if(VALUE>0x10ffff||(VALUE>=0xd800&&VALUE<=0xdfff)||(simbols>=0xff00&&simbols<0x1000000))return;
    if(vadība_VALUE){if(VALUE>='a'&&VALUE<='z')VALUE-=96;else if(VALUE>='A'&&VALUE<='Z')VALUE-=64;}
    글넣기(VALUE);
}
