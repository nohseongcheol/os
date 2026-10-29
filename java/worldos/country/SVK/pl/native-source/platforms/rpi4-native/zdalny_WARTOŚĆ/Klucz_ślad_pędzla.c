#include "zdalny_WARTOŚĆ.h"
#include <string.h>
#include "두벌식표.h"
static unsigned kontrola_WARTOŚĆ,klawisz_SHIFT,한글;
typedef struct {unsigned 첫,가운데,끝;} kompozycja_Stan;
static kompozycja_Stan kompozycja_WARTOŚĆ,LOG_zapis[16];
static unsigned LOG_ILE_LICZB;
void przekazywać_zdalny_Klucz(void){memset(&kompozycja_WARTOŚĆ,0,sizeof(kompozycja_WARTOŚĆ));LOG_ILE_LICZB=0;}
void inicjuj_zdalny_Klucz_ślad_pędzla(void){kontrola_WARTOŚĆ=klawisz_SHIFT=한글=0;przekazywać_zdalny_Klucz();}
static void 글넣기(unsigned WARTOŚĆ){
    unsigned char tekst[4];unsigned identyfikator;
    if(WARTOŚĆ<128){tekst[0]=WARTOŚĆ;identyfikator=1;}else if(WARTOŚĆ<2048){tekst[0]=0xc0|(WARTOŚĆ>>6);tekst[1]=0x80|(WARTOŚĆ&63);identyfikator=2;}
    else if(WARTOŚĆ<65536){tekst[0]=0xe0|(WARTOŚĆ>>12);tekst[1]=0x80|((WARTOŚĆ>>6)&63);tekst[2]=0x80|(WARTOŚĆ&63);identyfikator=3;}
    else{tekst[0]=0xf0|(WARTOŚĆ>>18);tekst[1]=0x80|((WARTOŚĆ>>12)&63);tekst[2]=0x80|((WARTOŚĆ>>6)&63);tekst[3]=0x80|(WARTOŚĆ&63);identyfikator=4;}
    kanał_zdalny_wejście(tekst,identyfikator);
}
static int ZNAJDŹ_wpis(const unsigned *wpis_Lista,unsigned identyfikator,unsigned WARTOŚĆ){for(unsigned 순번=0;순번<identyfikator;순번++)if(wpis_Lista[순번]==WARTOŚĆ)return 순번;return -1;}
static unsigned ZNAJDŹ_Duplikuj(const unsigned WYSZUKAJ_tabela[][3],unsigned identyfikator,unsigned 가,unsigned SEKUNDA_operand){for(unsigned 순번=0;순번<identyfikator;순번++)if(WYSZUKAJ_tabela[순번][0]==가&&WYSZUKAJ_tabela[순번][1]==SEKUNDA_operand)return WYSZUKAJ_tabela[순번][2];return 0;}
static unsigned 조합글(void){
    if(kompozycja_WARTOŚĆ.첫&&kompozycja_WARTOŚĆ.가운데)return 0xac00+(ZNAJDŹ_wpis(첫소리목록,19,kompozycja_WARTOŚĆ.첫)*21+ZNAJDŹ_wpis(가운뎃소리목록,21,kompozycja_WARTOŚĆ.가운데))*28+(kompozycja_WARTOŚĆ.끝?ZNAJDŹ_wpis(끝소리목록,28,kompozycja_WARTOŚĆ.끝):0);
    return kompozycja_WARTOŚĆ.첫?kompozycja_WARTOŚĆ.첫:kompozycja_WARTOŚĆ.가운데;
}
static int 한글넣기(unsigned Klucz_ślad_pędzla){
    unsigned 자모=0;for(unsigned 순번=0;순번<sizeof(Klucz_Układ)/sizeof(Klucz_Układ[0]);순번++)if(Klucz_Układ[순번][0]==Klucz_ślad_pędzla)자모=Klucz_Układ[순번][1];
    if(!자모&&Klucz_ślad_pędzla>='A'&&Klucz_ślad_pędzla<='Z')return 한글넣기(Klucz_ślad_pędzla+32);if(!자모)return 0;
    unsigned Wstecz_towar=조합글(),przekazywać_WARTOŚĆ=0;kompozycja_Stan 전=kompozycja_WARTOŚĆ;
    if(LOG_ILE_LICZB<16)LOG_zapis[LOG_ILE_LICZB++]=전;
    if(ZNAJDŹ_wpis(첫소리목록,19,자모)>=0){
        if(kompozycja_WARTOŚĆ.첫&&kompozycja_WARTOŚĆ.가운데&&!kompozycja_WARTOŚĆ.끝&&ZNAJDŹ_wpis(끝소리목록,28,자모)>=0)kompozycja_WARTOŚĆ.끝=자모;
        else{unsigned nakładka_WARTOŚĆ=ZNAJDŹ_Duplikuj(겹끝소리,11,kompozycja_WARTOŚĆ.끝,자모);if(kompozycja_WARTOŚĆ.끝&&nakładka_WARTOŚĆ)kompozycja_WARTOŚĆ.끝=nakładka_WARTOŚĆ;
            else{przekazywać_WARTOŚĆ=Wstecz_towar;przekazywać_zdalny_Klucz();kompozycja_WARTOŚĆ.첫=자모;LOG_ILE_LICZB=1;memset(LOG_zapis,0,sizeof(kompozycja_Stan));}}
    }else if(kompozycja_WARTOŚĆ.끝){
        unsigned 왼쪽=0,PRAWY=kompozycja_WARTOŚĆ.끝;for(unsigned 순번=0;순번<11;순번++)if(겹끝소리[순번][2]==kompozycja_WARTOŚĆ.끝){왼쪽=겹끝소리[순번][0];PRAWY=겹끝소리[순번][1];break;}
        kompozycja_WARTOŚĆ.끝=왼쪽;przekazywać_WARTOŚĆ=조합글();przekazywać_zdalny_Klucz();kompozycja_WARTOŚĆ.첫=PRAWY;kompozycja_WARTOŚĆ.가운데=자모;LOG_ILE_LICZB=2;
        memset(LOG_zapis,0,2*sizeof(kompozycja_Stan));LOG_zapis[1].첫=PRAWY;
    }else if(kompozycja_WARTOŚĆ.가운데){unsigned nakładka_WARTOŚĆ=ZNAJDŹ_Duplikuj(겹가운뎃소리,7,kompozycja_WARTOŚĆ.가운데,자모);
        if(nakładka_WARTOŚĆ)kompozycja_WARTOŚĆ.가운데=nakładka_WARTOŚĆ;else{przekazywać_WARTOŚĆ=Wstecz_towar;przekazywać_zdalny_Klucz();kompozycja_WARTOŚĆ.가운데=자모;LOG_ILE_LICZB=1;memset(LOG_zapis,0,sizeof(kompozycja_Stan));}
    }else kompozycja_WARTOŚĆ.가운데=자모;
    if(Wstecz_towar)글넣기(127);if(przekazywać_WARTOŚĆ)글넣기(przekazywać_WARTOŚĆ);unsigned TERAZ_WARTOŚĆ=조합글();if(TERAZ_WARTOŚĆ)글넣기(TERAZ_WARTOŚĆ);return 1;
}
void zdalny_Klucz_ślad_pędzla(unsigned symbol,int 누름){
    if(symbol==0xffe3||symbol==0xffe4){kontrola_WARTOŚĆ=누름;return;}
    if(symbol==0xffe1||symbol==0xffe2){klawisz_SHIFT=누름;return;}
    if(!누름)return;
    if(symbol==0xffc6||symbol==0xff31||(symbol==32&&klawisz_SHIFT&&!kontrola_WARTOŚĆ)){
        przekazywać_zdalny_Klucz();한글=!한글;unsigned char Wydarzenie[]={30,3,한글,0,0,0,0};kanał_zdalny_wejście(Wydarzenie,7);return;
    }
    if(symbol==0xff08&&한글&&!kontrola_WARTOŚĆ&&LOG_ILE_LICZB){kompozycja_WARTOŚĆ=LOG_zapis[--LOG_ILE_LICZB];글넣기(127);unsigned tekst=조합글();if(tekst)글넣기(tekst);return;}
    if(한글&&!kontrola_WARTOŚĆ&&symbol<128&&한글넣기(symbol))return;
    przekazywać_zdalny_Klucz();
    if((kontrola_WARTOŚĆ&&klawisz_SHIFT&&(symbol=='t'||symbol=='T'))||symbol==0xffc3||symbol==0xffc9){unsigned char Wydarzenie[]={30,2,symbol==0xffc3?2:symbol==0xffc9?3:1,0,0,0,0};kanał_zdalny_wejście(Wydarzenie,7);return;}
    const char *특수=symbol==0xff08?"\177":symbol==0xff09?"\t":symbol==0xff0d?"\r":symbol==0xff1b?"\033":
        symbol==0xffff?"\033[3~":symbol==0xff50?"\033[H":symbol==0xff57?"\033[F":symbol==0xff51?"\033[D":
        symbol==0xff52?"\033[A":symbol==0xff53?"\033[C":symbol==0xff54?"\033[B":symbol==0xff55?"\033[5~":symbol==0xff56?"\033[6~":0;
    if(특수){kanał_zdalny_wejście((const unsigned char*)특수,strlen(특수));return;}
    unsigned WARTOŚĆ=(symbol&0xff000000)==0x01000000?symbol&0xffffff:symbol;
    if(WARTOŚĆ>0x10ffff||(WARTOŚĆ>=0xd800&&WARTOŚĆ<=0xdfff)||(symbol>=0xff00&&symbol<0x1000000))return;
    if(kontrola_WARTOŚĆ){if(WARTOŚĆ>='a'&&WARTOŚĆ<='z')WARTOŚĆ-=96;else if(WARTOŚĆ>='A'&&WARTOŚĆ<='Z')WARTOŚĆ-=64;}
    글넣기(WARTOŚĆ);
}
