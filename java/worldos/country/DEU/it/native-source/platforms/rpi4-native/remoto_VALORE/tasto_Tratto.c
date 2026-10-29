#include "remoto_VALORE.h"
#include <string.h>
#include "두벌식표.h"
static unsigned controllo_VALORE,tasto_MAIUSC,한글;
typedef struct {unsigned 첫,가운데,끝;} composizione_Stato;
static composizione_Stato composizione_VALORE,LOG_riga[16];
static unsigned LOG_CONTA_NUMERI;
void commit_remoto_tasto(void){memset(&composizione_VALORE,0,sizeof(composizione_VALORE));LOG_CONTA_NUMERI=0;}
void inizializzare_remoto_tasto_Tratto(void){controllo_VALORE=tasto_MAIUSC=한글=0;commit_remoto_tasto();}
static void 글넣기(unsigned VALORE){
    unsigned char testo[4];unsigned numero;
    if(VALORE<128){testo[0]=VALORE;numero=1;}else if(VALORE<2048){testo[0]=0xc0|(VALORE>>6);testo[1]=0x80|(VALORE&63);numero=2;}
    else if(VALORE<65536){testo[0]=0xe0|(VALORE>>12);testo[1]=0x80|((VALORE>>6)&63);testo[2]=0x80|(VALORE&63);numero=3;}
    else{testo[0]=0xf0|(VALORE>>18);testo[1]=0x80|((VALORE>>12)&63);testo[2]=0x80|((VALORE>>6)&63);testo[3]=0x80|(VALORE&63);numero=4;}
    feed_remoto_input(testo,numero);
}
static int TROVA_voce(const unsigned *voce_elenco,unsigned numero,unsigned VALORE){for(unsigned 순번=0;순번<numero;순번++)if(voce_elenco[순번]==VALORE)return 순번;return -1;}
static unsigned TROVA_Duplica(const unsigned tabella_di_ricerca[][3],unsigned numero,unsigned 가,unsigned SECONDO_operando){for(unsigned 순번=0;순번<numero;순번++)if(tabella_di_ricerca[순번][0]==가&&tabella_di_ricerca[순번][1]==SECONDO_operando)return tabella_di_ricerca[순번][2];return 0;}
static unsigned 조합글(void){
    if(composizione_VALORE.첫&&composizione_VALORE.가운데)return 0xac00+(TROVA_voce(첫소리목록,19,composizione_VALORE.첫)*21+TROVA_voce(가운뎃소리목록,21,composizione_VALORE.가운데))*28+(composizione_VALORE.끝?TROVA_voce(끝소리목록,28,composizione_VALORE.끝):0);
    return composizione_VALORE.첫?composizione_VALORE.첫:composizione_VALORE.가운데;
}
static int 한글넣기(unsigned tasto_Tratto){
    unsigned 자모=0;for(unsigned 순번=0;순번<sizeof(tasto_Layout)/sizeof(tasto_Layout[0]);순번++)if(tasto_Layout[순번][0]==tasto_Tratto)자모=tasto_Layout[순번][1];
    if(!자모&&tasto_Tratto>='A'&&tasto_Tratto<='Z')return 한글넣기(tasto_Tratto+32);if(!자모)return 0;
    unsigned Indietro_articolo=조합글(),commit_VALORE=0;composizione_Stato 전=composizione_VALORE;
    if(LOG_CONTA_NUMERI<16)LOG_riga[LOG_CONTA_NUMERI++]=전;
    if(TROVA_voce(첫소리목록,19,자모)>=0){
        if(composizione_VALORE.첫&&composizione_VALORE.가운데&&!composizione_VALORE.끝&&TROVA_voce(끝소리목록,28,자모)>=0)composizione_VALORE.끝=자모;
        else{unsigned sovrimpressione_VALORE=TROVA_Duplica(겹끝소리,11,composizione_VALORE.끝,자모);if(composizione_VALORE.끝&&sovrimpressione_VALORE)composizione_VALORE.끝=sovrimpressione_VALORE;
            else{commit_VALORE=Indietro_articolo;commit_remoto_tasto();composizione_VALORE.첫=자모;LOG_CONTA_NUMERI=1;memset(LOG_riga,0,sizeof(composizione_Stato));}}
    }else if(composizione_VALORE.끝){
        unsigned 왼쪽=0,DESTRA=composizione_VALORE.끝;for(unsigned 순번=0;순번<11;순번++)if(겹끝소리[순번][2]==composizione_VALORE.끝){왼쪽=겹끝소리[순번][0];DESTRA=겹끝소리[순번][1];break;}
        composizione_VALORE.끝=왼쪽;commit_VALORE=조합글();commit_remoto_tasto();composizione_VALORE.첫=DESTRA;composizione_VALORE.가운데=자모;LOG_CONTA_NUMERI=2;
        memset(LOG_riga,0,2*sizeof(composizione_Stato));LOG_riga[1].첫=DESTRA;
    }else if(composizione_VALORE.가운데){unsigned sovrimpressione_VALORE=TROVA_Duplica(겹가운뎃소리,7,composizione_VALORE.가운데,자모);
        if(sovrimpressione_VALORE)composizione_VALORE.가운데=sovrimpressione_VALORE;else{commit_VALORE=Indietro_articolo;commit_remoto_tasto();composizione_VALORE.가운데=자모;LOG_CONTA_NUMERI=1;memset(LOG_riga,0,sizeof(composizione_Stato));}
    }else composizione_VALORE.가운데=자모;
    if(Indietro_articolo)글넣기(127);if(commit_VALORE)글넣기(commit_VALORE);unsigned ADESSO_VALORE=조합글();if(ADESSO_VALORE)글넣기(ADESSO_VALORE);return 1;
}
void remoto_tasto_Tratto(unsigned simbolo,int 누름){
    if(simbolo==0xffe3||simbolo==0xffe4){controllo_VALORE=누름;return;}
    if(simbolo==0xffe1||simbolo==0xffe2){tasto_MAIUSC=누름;return;}
    if(!누름)return;
    if(simbolo==0xffc6||simbolo==0xff31||(simbolo==32&&tasto_MAIUSC&&!controllo_VALORE)){
        commit_remoto_tasto();한글=!한글;unsigned char Evento[]={30,3,한글,0,0,0,0};feed_remoto_input(Evento,7);return;
    }
    if(simbolo==0xff08&&한글&&!controllo_VALORE&&LOG_CONTA_NUMERI){composizione_VALORE=LOG_riga[--LOG_CONTA_NUMERI];글넣기(127);unsigned testo=조합글();if(testo)글넣기(testo);return;}
    if(한글&&!controllo_VALORE&&simbolo<128&&한글넣기(simbolo))return;
    commit_remoto_tasto();
    if((controllo_VALORE&&tasto_MAIUSC&&(simbolo=='t'||simbolo=='T'))||simbolo==0xffc3||simbolo==0xffc9){unsigned char Evento[]={30,2,simbolo==0xffc3?2:simbolo==0xffc9?3:1,0,0,0,0};feed_remoto_input(Evento,7);return;}
    const char *특수=simbolo==0xff08?"\177":simbolo==0xff09?"\t":simbolo==0xff0d?"\r":simbolo==0xff1b?"\033":
        simbolo==0xffff?"\033[3~":simbolo==0xff50?"\033[H":simbolo==0xff57?"\033[F":simbolo==0xff51?"\033[D":
        simbolo==0xff52?"\033[A":simbolo==0xff53?"\033[C":simbolo==0xff54?"\033[B":simbolo==0xff55?"\033[5~":simbolo==0xff56?"\033[6~":0;
    if(특수){feed_remoto_input((const unsigned char*)특수,strlen(특수));return;}
    unsigned VALORE=(simbolo&0xff000000)==0x01000000?simbolo&0xffffff:simbolo;
    if(VALORE>0x10ffff||(VALORE>=0xd800&&VALORE<=0xdfff)||(simbolo>=0xff00&&simbolo<0x1000000))return;
    if(controllo_VALORE){if(VALORE>='a'&&VALORE<='z')VALORE-=96;else if(VALORE>='A'&&VALORE<='Z')VALORE-=64;}
    글넣기(VALORE);
}
