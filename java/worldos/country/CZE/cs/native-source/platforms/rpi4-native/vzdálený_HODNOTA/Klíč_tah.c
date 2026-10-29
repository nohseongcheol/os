#include "vzdálený_HODNOTA.h"
#include <string.h>
#include "두벌식표.h"
static unsigned řízení_HODNOTA,klávesa_Shift,한글;
typedef struct {unsigned 첫,가운데,끝;} složení_Stav;
static složení_Stav složení_HODNOTA,LOGZ_ZÁZNAM[16];
static unsigned LOGZ_POČET;
void zápis_vzdálený_Klíč(void){memset(&složení_HODNOTA,0,sizeof(složení_HODNOTA));LOGZ_POČET=0;}
void inicializovat_vzdálený_Klíč_tah(void){řízení_HODNOTA=klávesa_Shift=한글=0;zápis_vzdálený_Klíč();}
static void 글넣기(unsigned HODNOTA){
    unsigned char text[4];unsigned číslo;
    if(HODNOTA<128){text[0]=HODNOTA;číslo=1;}else if(HODNOTA<2048){text[0]=0xc0|(HODNOTA>>6);text[1]=0x80|(HODNOTA&63);číslo=2;}
    else if(HODNOTA<65536){text[0]=0xe0|(HODNOTA>>12);text[1]=0x80|((HODNOTA>>6)&63);text[2]=0x80|(HODNOTA&63);číslo=3;}
    else{text[0]=0xf0|(HODNOTA>>18);text[1]=0x80|((HODNOTA>>12)&63);text[2]=0x80|((HODNOTA>>6)&63);text[3]=0x80|(HODNOTA&63);číslo=4;}
    novinky_vzdálený_vstup(text,číslo);
}
static int NAJÍT_položka(const unsigned *položka_Seznam,unsigned číslo,unsigned HODNOTA){for(unsigned 순번=0;순번<číslo;순번++)if(položka_Seznam[순번]==HODNOTA)return 순번;return -1;}
static unsigned NAJÍT_duplikát(const unsigned VYHLEDAT_tabulka[][3],unsigned číslo,unsigned 가,unsigned SEKUNDA_operand){for(unsigned 순번=0;순번<číslo;순번++)if(VYHLEDAT_tabulka[순번][0]==가&&VYHLEDAT_tabulka[순번][1]==SEKUNDA_operand)return VYHLEDAT_tabulka[순번][2];return 0;}
static unsigned 조합글(void){
    if(složení_HODNOTA.첫&&složení_HODNOTA.가운데)return 0xac00+(NAJÍT_položka(첫소리목록,19,složení_HODNOTA.첫)*21+NAJÍT_položka(가운뎃소리목록,21,složení_HODNOTA.가운데))*28+(složení_HODNOTA.끝?NAJÍT_položka(끝소리목록,28,složení_HODNOTA.끝):0);
    return složení_HODNOTA.첫?složení_HODNOTA.첫:složení_HODNOTA.가운데;
}
static int 한글넣기(unsigned Klíč_tah){
    unsigned 자모=0;for(unsigned 순번=0;순번<sizeof(Klíč_Navigace)/sizeof(Klíč_Navigace[0]);순번++)if(Klíč_Navigace[순번][0]==Klíč_tah)자모=Klíč_Navigace[순번][1];
    if(!자모&&Klíč_tah>='A'&&Klíč_tah<='Z')return 한글넣기(Klíč_tah+32);if(!자모)return 0;
    unsigned Předchozí_zboží=조합글(),zápis_HODNOTA=0;složení_Stav 전=složení_HODNOTA;
    if(LOGZ_POČET<16)LOGZ_ZÁZNAM[LOGZ_POČET++]=전;
    if(NAJÍT_položka(첫소리목록,19,자모)>=0){
        if(složení_HODNOTA.첫&&složení_HODNOTA.가운데&&!složení_HODNOTA.끝&&NAJÍT_položka(끝소리목록,28,자모)>=0)složení_HODNOTA.끝=자모;
        else{unsigned překryvný_prvek_HODNOTA=NAJÍT_duplikát(겹끝소리,11,složení_HODNOTA.끝,자모);if(složení_HODNOTA.끝&&překryvný_prvek_HODNOTA)složení_HODNOTA.끝=překryvný_prvek_HODNOTA;
            else{zápis_HODNOTA=Předchozí_zboží;zápis_vzdálený_Klíč();složení_HODNOTA.첫=자모;LOGZ_POČET=1;memset(LOGZ_ZÁZNAM,0,sizeof(složení_Stav));}}
    }else if(složení_HODNOTA.끝){
        unsigned 왼쪽=0,právo=složení_HODNOTA.끝;for(unsigned 순번=0;순번<11;순번++)if(겹끝소리[순번][2]==složení_HODNOTA.끝){왼쪽=겹끝소리[순번][0];právo=겹끝소리[순번][1];break;}
        složení_HODNOTA.끝=왼쪽;zápis_HODNOTA=조합글();zápis_vzdálený_Klíč();složení_HODNOTA.첫=právo;složení_HODNOTA.가운데=자모;LOGZ_POČET=2;
        memset(LOGZ_ZÁZNAM,0,2*sizeof(složení_Stav));LOGZ_ZÁZNAM[1].첫=právo;
    }else if(složení_HODNOTA.가운데){unsigned překryvný_prvek_HODNOTA=NAJÍT_duplikát(겹가운뎃소리,7,složení_HODNOTA.가운데,자모);
        if(překryvný_prvek_HODNOTA)složení_HODNOTA.가운데=překryvný_prvek_HODNOTA;else{zápis_HODNOTA=Předchozí_zboží;zápis_vzdálený_Klíč();složení_HODNOTA.가운데=자모;LOGZ_POČET=1;memset(LOGZ_ZÁZNAM,0,sizeof(složení_Stav));}
    }else složení_HODNOTA.가운데=자모;
    if(Předchozí_zboží)글넣기(127);if(zápis_HODNOTA)글넣기(zápis_HODNOTA);unsigned NOW_HODNOTA=조합글();if(NOW_HODNOTA)글넣기(NOW_HODNOTA);return 1;
}
void vzdálený_Klíč_tah(unsigned symbol,int 누름){
    if(symbol==0xffe3||symbol==0xffe4){řízení_HODNOTA=누름;return;}
    if(symbol==0xffe1||symbol==0xffe2){klávesa_Shift=누름;return;}
    if(!누름)return;
    if(symbol==0xffc6||symbol==0xff31||(symbol==32&&klávesa_Shift&&!řízení_HODNOTA)){
        zápis_vzdálený_Klíč();한글=!한글;unsigned char Události[]={30,3,한글,0,0,0,0};novinky_vzdálený_vstup(Události,7);return;
    }
    if(symbol==0xff08&&한글&&!řízení_HODNOTA&&LOGZ_POČET){složení_HODNOTA=LOGZ_ZÁZNAM[--LOGZ_POČET];글넣기(127);unsigned text=조합글();if(text)글넣기(text);return;}
    if(한글&&!řízení_HODNOTA&&symbol<128&&한글넣기(symbol))return;
    zápis_vzdálený_Klíč();
    if((řízení_HODNOTA&&klávesa_Shift&&(symbol=='t'||symbol=='T'))||symbol==0xffc3||symbol==0xffc9){unsigned char Události[]={30,2,symbol==0xffc3?2:symbol==0xffc9?3:1,0,0,0,0};novinky_vzdálený_vstup(Události,7);return;}
    const char *특수=symbol==0xff08?"\177":symbol==0xff09?"\t":symbol==0xff0d?"\r":symbol==0xff1b?"\033":
        symbol==0xffff?"\033[3~":symbol==0xff50?"\033[H":symbol==0xff57?"\033[F":symbol==0xff51?"\033[D":
        symbol==0xff52?"\033[A":symbol==0xff53?"\033[C":symbol==0xff54?"\033[B":symbol==0xff55?"\033[5~":symbol==0xff56?"\033[6~":0;
    if(특수){novinky_vzdálený_vstup((const unsigned char*)특수,strlen(특수));return;}
    unsigned HODNOTA=(symbol&0xff000000)==0x01000000?symbol&0xffffff:symbol;
    if(HODNOTA>0x10ffff||(HODNOTA>=0xd800&&HODNOTA<=0xdfff)||(symbol>=0xff00&&symbol<0x1000000))return;
    if(řízení_HODNOTA){if(HODNOTA>='a'&&HODNOTA<='z')HODNOTA-=96;else if(HODNOTA>='A'&&HODNOTA<='Z')HODNOTA-=64;}
    글넣기(HODNOTA);
}
