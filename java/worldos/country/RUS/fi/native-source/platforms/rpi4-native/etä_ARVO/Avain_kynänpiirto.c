#include "etä_ARVO.h"
#include <string.h>
#include "두벌식표.h"
static unsigned ohjain_ARVO,VAIHTONÄPPÄIN,한글;
typedef struct {unsigned 첫,가운데,끝;} kokoonpano_Tila;
static kokoonpano_Tila kokoonpano_ARVO,LOG_TIETUE[16];
static unsigned LOG_LASKE;
void vahvistaa_muutokset_etä_Avain(void){memset(&kokoonpano_ARVO,0,sizeof(kokoonpano_ARVO));LOG_LASKE=0;}
void alustaa_etä_Avain_kynänpiirto(void){ohjain_ARVO=VAIHTONÄPPÄIN=한글=0;vahvistaa_muutokset_etä_Avain();}
static void 글넣기(unsigned ARVO){
    unsigned char teksti[4];unsigned numero;
    if(ARVO<128){teksti[0]=ARVO;numero=1;}else if(ARVO<2048){teksti[0]=0xc0|(ARVO>>6);teksti[1]=0x80|(ARVO&63);numero=2;}
    else if(ARVO<65536){teksti[0]=0xe0|(ARVO>>12);teksti[1]=0x80|((ARVO>>6)&63);teksti[2]=0x80|(ARVO&63);numero=3;}
    else{teksti[0]=0xf0|(ARVO>>18);teksti[1]=0x80|((ARVO>>12)&63);teksti[2]=0x80|((ARVO>>6)&63);teksti[3]=0x80|(ARVO&63);numero=4;}
    syöte_etä_syöte(teksti,numero);
}
static int ETSI_merkintä(const unsigned *merkintä_luettelo,unsigned numero,unsigned ARVO){for(unsigned 순번=0;순번<numero;순번++)if(merkintä_luettelo[순번]==ARVO)return 순번;return -1;}
static unsigned ETSI_Monista(const unsigned HAKU_taulukko[][3],unsigned numero,unsigned 가,unsigned SEKUNNIT_operandi){for(unsigned 순번=0;순번<numero;순번++)if(HAKU_taulukko[순번][0]==가&&HAKU_taulukko[순번][1]==SEKUNNIT_operandi)return HAKU_taulukko[순번][2];return 0;}
static unsigned 조합글(void){
    if(kokoonpano_ARVO.첫&&kokoonpano_ARVO.가운데)return 0xac00+(ETSI_merkintä(첫소리목록,19,kokoonpano_ARVO.첫)*21+ETSI_merkintä(가운뎃소리목록,21,kokoonpano_ARVO.가운데))*28+(kokoonpano_ARVO.끝?ETSI_merkintä(끝소리목록,28,kokoonpano_ARVO.끝):0);
    return kokoonpano_ARVO.첫?kokoonpano_ARVO.첫:kokoonpano_ARVO.가운데;
}
static int 한글넣기(unsigned Avain_kynänpiirto){
    unsigned 자모=0;for(unsigned 순번=0;순번<sizeof(Avain_Asettelu)/sizeof(Avain_Asettelu[0]);순번++)if(Avain_Asettelu[순번][0]==Avain_kynänpiirto)자모=Avain_Asettelu[순번][1];
    if(!자모&&Avain_kynänpiirto>='A'&&Avain_kynänpiirto<='Z')return 한글넣기(Avain_kynänpiirto+32);if(!자모)return 0;
    unsigned Edellinen_kohde=조합글(),vahvistaa_muutokset_ARVO=0;kokoonpano_Tila 전=kokoonpano_ARVO;
    if(LOG_LASKE<16)LOG_TIETUE[LOG_LASKE++]=전;
    if(ETSI_merkintä(첫소리목록,19,자모)>=0){
        if(kokoonpano_ARVO.첫&&kokoonpano_ARVO.가운데&&!kokoonpano_ARVO.끝&&ETSI_merkintä(끝소리목록,28,자모)>=0)kokoonpano_ARVO.끝=자모;
        else{unsigned kerros_ARVO=ETSI_Monista(겹끝소리,11,kokoonpano_ARVO.끝,자모);if(kokoonpano_ARVO.끝&&kerros_ARVO)kokoonpano_ARVO.끝=kerros_ARVO;
            else{vahvistaa_muutokset_ARVO=Edellinen_kohde;vahvistaa_muutokset_etä_Avain();kokoonpano_ARVO.첫=자모;LOG_LASKE=1;memset(LOG_TIETUE,0,sizeof(kokoonpano_Tila));}}
    }else if(kokoonpano_ARVO.끝){
        unsigned 왼쪽=0,OIKEA=kokoonpano_ARVO.끝;for(unsigned 순번=0;순번<11;순번++)if(겹끝소리[순번][2]==kokoonpano_ARVO.끝){왼쪽=겹끝소리[순번][0];OIKEA=겹끝소리[순번][1];break;}
        kokoonpano_ARVO.끝=왼쪽;vahvistaa_muutokset_ARVO=조합글();vahvistaa_muutokset_etä_Avain();kokoonpano_ARVO.첫=OIKEA;kokoonpano_ARVO.가운데=자모;LOG_LASKE=2;
        memset(LOG_TIETUE,0,2*sizeof(kokoonpano_Tila));LOG_TIETUE[1].첫=OIKEA;
    }else if(kokoonpano_ARVO.가운데){unsigned kerros_ARVO=ETSI_Monista(겹가운뎃소리,7,kokoonpano_ARVO.가운데,자모);
        if(kerros_ARVO)kokoonpano_ARVO.가운데=kerros_ARVO;else{vahvistaa_muutokset_ARVO=Edellinen_kohde;vahvistaa_muutokset_etä_Avain();kokoonpano_ARVO.가운데=자모;LOG_LASKE=1;memset(LOG_TIETUE,0,sizeof(kokoonpano_Tila));}
    }else kokoonpano_ARVO.가운데=자모;
    if(Edellinen_kohde)글넣기(127);if(vahvistaa_muutokset_ARVO)글넣기(vahvistaa_muutokset_ARVO);unsigned NYT_ARVO=조합글();if(NYT_ARVO)글넣기(NYT_ARVO);return 1;
}
void etä_Avain_kynänpiirto(unsigned symboli,int paina_ARVO){
    if(symboli==0xffe3||symboli==0xffe4){ohjain_ARVO=paina_ARVO;return;}
    if(symboli==0xffe1||symboli==0xffe2){VAIHTONÄPPÄIN=paina_ARVO;return;}
    if(!paina_ARVO)return;
    if(symboli==0xffc6||symboli==0xff31||(symboli==32&&VAIHTONÄPPÄIN&&!ohjain_ARVO)){
        vahvistaa_muutokset_etä_Avain();한글=!한글;unsigned char Tapahtuma[]={30,3,한글,0,0,0,0};syöte_etä_syöte(Tapahtuma,7);return;
    }
    if(symboli==0xff08&&한글&&!ohjain_ARVO&&LOG_LASKE){kokoonpano_ARVO=LOG_TIETUE[--LOG_LASKE];글넣기(127);unsigned teksti=조합글();if(teksti)글넣기(teksti);return;}
    if(한글&&!ohjain_ARVO&&symboli<128&&한글넣기(symboli))return;
    vahvistaa_muutokset_etä_Avain();
    if((ohjain_ARVO&&VAIHTONÄPPÄIN&&(symboli=='t'||symboli=='T'))||symboli==0xffc3||symboli==0xffc9){unsigned char Tapahtuma[]={30,2,symboli==0xffc3?2:symboli==0xffc9?3:1,0,0,0,0};syöte_etä_syöte(Tapahtuma,7);return;}
    const char *특수=symboli==0xff08?"\177":symboli==0xff09?"\t":symboli==0xff0d?"\r":symboli==0xff1b?"\033":
        symboli==0xffff?"\033[3~":symboli==0xff50?"\033[H":symboli==0xff57?"\033[F":symboli==0xff51?"\033[D":
        symboli==0xff52?"\033[A":symboli==0xff53?"\033[C":symboli==0xff54?"\033[B":symboli==0xff55?"\033[5~":symboli==0xff56?"\033[6~":0;
    if(특수){syöte_etä_syöte((const unsigned char*)특수,strlen(특수));return;}
    unsigned ARVO=(symboli&0xff000000)==0x01000000?symboli&0xffffff:symboli;
    if(ARVO>0x10ffff||(ARVO>=0xd800&&ARVO<=0xdfff)||(symboli>=0xff00&&symboli<0x1000000))return;
    if(ohjain_ARVO){if(ARVO>='a'&&ARVO<='z')ARVO-=96;else if(ARVO>='A'&&ARVO<='Z')ARVO-=64;}
    글넣기(ARVO);
}
