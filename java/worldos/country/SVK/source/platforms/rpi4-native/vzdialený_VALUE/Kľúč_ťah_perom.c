#include "vzdialený_VALUE.h"
#include <string.h>
#include "두벌식표.h"
static unsigned riadenie_VALUE,kláves_Shift,한글;
typedef struct {unsigned 첫,가운데,끝;} 조합상태;
static 조합상태 조합,LOG_RECORD[16];
static unsigned LOG_COUNT;
void potvrdenie_vzdialený_Kľúč(void){memset(&조합,0,sizeof(조합));LOG_COUNT=0;}
void incializovať_vzdialený_Kľúč_ťah_perom(void){riadenie_VALUE=kláves_Shift=한글=0;potvrdenie_vzdialený_Kľúč();}
static void 글넣기(unsigned VALUE){
    unsigned char Spracovanie_textu[4];unsigned 수;
    if(VALUE<128){Spracovanie_textu[0]=VALUE;수=1;}else if(VALUE<2048){Spracovanie_textu[0]=0xc0|(VALUE>>6);Spracovanie_textu[1]=0x80|(VALUE&63);수=2;}
    else if(VALUE<65536){Spracovanie_textu[0]=0xe0|(VALUE>>12);Spracovanie_textu[1]=0x80|((VALUE>>6)&63);Spracovanie_textu[2]=0x80|(VALUE&63);수=3;}
    else{Spracovanie_textu[0]=0xf0|(VALUE>>18);Spracovanie_textu[1]=0x80|((VALUE>>12)&63);Spracovanie_textu[2]=0x80|((VALUE>>6)&63);Spracovanie_textu[3]=0x80|(VALUE&63);수=4;}
    súhrnný_obsah_vzdialený_vstup(Spracovanie_textu,수);
}
static int FIND_položka(const unsigned *položka_Zoznam,unsigned 수,unsigned VALUE){for(unsigned 순번=0;순번<수;순번++)if(položka_Zoznam[순번]==VALUE)return 순번;return -1;}
static unsigned FIND_duplikát(const unsigned vyhľadávacia_tabuľka[][3],unsigned 수,unsigned 가,unsigned SECOND_operand){for(unsigned 순번=0;순번<수;순번++)if(vyhľadávacia_tabuľka[순번][0]==가&&vyhľadávacia_tabuľka[순번][1]==SECOND_operand)return vyhľadávacia_tabuľka[순번][2];return 0;}
static unsigned 조합글(void){
    if(조합.첫&&조합.가운데)return 0xac00+(FIND_položka(첫소리목록,19,조합.첫)*21+FIND_položka(가운뎃소리목록,21,조합.가운데))*28+(조합.끝?FIND_položka(끝소리목록,28,조합.끝):0);
    return 조합.첫?조합.첫:조합.가운데;
}
static int 한글넣기(unsigned Kľúč_ťah_perom){
    unsigned 자모=0;for(unsigned 순번=0;순번<sizeof(Kľúč_Navigácia)/sizeof(Kľúč_Navigácia[0]);순번++)if(Kľúč_Navigácia[순번][0]==Kľúč_ťah_perom)자모=Kľúč_Navigácia[순번][1];
    if(!자모&&Kľúč_ťah_perom>='A'&&Kľúč_ťah_perom<='Z')return 한글넣기(Kľúč_ťah_perom+32);if(!자모)return 0;
    unsigned 이전=조합글(),potvrdenie_VALUE=0;조합상태 전=조합;
    if(LOG_COUNT<16)LOG_RECORD[LOG_COUNT++]=전;
    if(FIND_položka(첫소리목록,19,자모)>=0){
        if(조합.첫&&조합.가운데&&!조합.끝&&FIND_položka(끝소리목록,28,자모)>=0)조합.끝=자모;
        else{unsigned prekrývajúci_prvok_VALUE=FIND_duplikát(겹끝소리,11,조합.끝,자모);if(조합.끝&&prekrývajúci_prvok_VALUE)조합.끝=prekrývajúci_prvok_VALUE;
            else{potvrdenie_VALUE=이전;potvrdenie_vzdialený_Kľúč();조합.첫=자모;LOG_COUNT=1;memset(LOG_RECORD,0,sizeof(조합상태));}}
    }else if(조합.끝){
        unsigned 왼쪽=0,RIGHT=조합.끝;for(unsigned 순번=0;순번<11;순번++)if(겹끝소리[순번][2]==조합.끝){왼쪽=겹끝소리[순번][0];RIGHT=겹끝소리[순번][1];break;}
        조합.끝=왼쪽;potvrdenie_VALUE=조합글();potvrdenie_vzdialený_Kľúč();조합.첫=RIGHT;조합.가운데=자모;LOG_COUNT=2;
        memset(LOG_RECORD,0,2*sizeof(조합상태));LOG_RECORD[1].첫=RIGHT;
    }else if(조합.가운데){unsigned prekrývajúci_prvok_VALUE=FIND_duplikát(겹가운뎃소리,7,조합.가운데,자모);
        if(prekrývajúci_prvok_VALUE)조합.가운데=prekrývajúci_prvok_VALUE;else{potvrdenie_VALUE=이전;potvrdenie_vzdialený_Kľúč();조합.가운데=자모;LOG_COUNT=1;memset(LOG_RECORD,0,sizeof(조합상태));}
    }else 조합.가운데=자모;
    if(이전)글넣기(127);if(potvrdenie_VALUE)글넣기(potvrdenie_VALUE);unsigned NOW_VALUE=조합글();if(NOW_VALUE)글넣기(NOW_VALUE);return 1;
}
void vzdialený_Kľúč_ťah_perom(unsigned symbol,int 누름){
    if(symbol==0xffe3||symbol==0xffe4){riadenie_VALUE=누름;return;}
    if(symbol==0xffe1||symbol==0xffe2){kláves_Shift=누름;return;}
    if(!누름)return;
    if(symbol==0xffc6||symbol==0xff31||(symbol==32&&kláves_Shift&&!riadenie_VALUE)){
        potvrdenie_vzdialený_Kľúč();한글=!한글;unsigned char Udalosť[]={30,3,한글,0,0,0,0};súhrnný_obsah_vzdialený_vstup(Udalosť,7);return;
    }
    if(symbol==0xff08&&한글&&!riadenie_VALUE&&LOG_COUNT){조합=LOG_RECORD[--LOG_COUNT];글넣기(127);unsigned Spracovanie_textu=조합글();if(Spracovanie_textu)글넣기(Spracovanie_textu);return;}
    if(한글&&!riadenie_VALUE&&symbol<128&&한글넣기(symbol))return;
    potvrdenie_vzdialený_Kľúč();
    if((riadenie_VALUE&&kláves_Shift&&(symbol=='t'||symbol=='T'))||symbol==0xffc3||symbol==0xffc9){unsigned char Udalosť[]={30,2,symbol==0xffc3?2:symbol==0xffc9?3:1,0,0,0,0};súhrnný_obsah_vzdialený_vstup(Udalosť,7);return;}
    const char *특수=symbol==0xff08?"\177":symbol==0xff09?"\t":symbol==0xff0d?"\r":symbol==0xff1b?"\033":
        symbol==0xffff?"\033[3~":symbol==0xff50?"\033[H":symbol==0xff57?"\033[F":symbol==0xff51?"\033[D":
        symbol==0xff52?"\033[A":symbol==0xff53?"\033[C":symbol==0xff54?"\033[B":symbol==0xff55?"\033[5~":symbol==0xff56?"\033[6~":0;
    if(특수){súhrnný_obsah_vzdialený_vstup((const unsigned char*)특수,strlen(특수));return;}
    unsigned VALUE=(symbol&0xff000000)==0x01000000?symbol&0xffffff:symbol;
    if(VALUE>0x10ffff||(VALUE>=0xd800&&VALUE<=0xdfff)||(symbol>=0xff00&&symbol<0x1000000))return;
    if(riadenie_VALUE){if(VALUE>='a'&&VALUE<='z')VALUE-=96;else if(VALUE>='A'&&VALUE<='Z')VALUE-=64;}
    글넣기(VALUE);
}
