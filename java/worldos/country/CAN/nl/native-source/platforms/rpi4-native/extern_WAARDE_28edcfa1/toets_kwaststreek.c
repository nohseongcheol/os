#include "extern_WAARDE_28edcfa1.h"
#include <string.h>
#include "두벌식표.h"
static unsigned controle_WAARDE,SHIFT_toets,한글;
typedef struct {unsigned 첫,가운데,끝;} samenstelling_Status;
static samenstelling_Status samenstelling_WAARDE,LOG_RECORD[16];
static unsigned LOG_AANTAL;
void doorvoeren_extern_toets(void){memset(&samenstelling_WAARDE,0,sizeof(samenstelling_WAARDE));LOG_AANTAL=0;}
void initialiseren_extern_toets_kwaststreek(void){controle_WAARDE=SHIFT_toets=한글=0;doorvoeren_extern_toets();}
static void 글넣기(unsigned WAARDE){
    unsigned char tekst[4];unsigned nummer;
    if(WAARDE<128){tekst[0]=WAARDE;nummer=1;}else if(WAARDE<2048){tekst[0]=0xc0|(WAARDE>>6);tekst[1]=0x80|(WAARDE&63);nummer=2;}
    else if(WAARDE<65536){tekst[0]=0xe0|(WAARDE>>12);tekst[1]=0x80|((WAARDE>>6)&63);tekst[2]=0x80|(WAARDE&63);nummer=3;}
    else{tekst[0]=0xf0|(WAARDE>>18);tekst[1]=0x80|((WAARDE>>12)&63);tekst[2]=0x80|((WAARDE>>6)&63);tekst[3]=0x80|(WAARDE&63);nummer=4;}
    feed_extern_invoer(tekst,nummer);
}
static int Zoeken_invoer(const unsigned *invoer_Lijst_f07b3200,unsigned nummer,unsigned WAARDE){for(unsigned 순번=0;순번<nummer;순번++)if(invoer_Lijst_f07b3200[순번]==WAARDE)return 순번;return -1;}
static unsigned Zoeken_duplicaat(const unsigned opzoektabel[][3],unsigned nummer,unsigned 가,unsigned SECONDE_operand){for(unsigned 순번=0;순번<nummer;순번++)if(opzoektabel[순번][0]==가&&opzoektabel[순번][1]==SECONDE_operand)return opzoektabel[순번][2];return 0;}
static unsigned 조합글(void){
    if(samenstelling_WAARDE.첫&&samenstelling_WAARDE.가운데)return 0xac00+(Zoeken_invoer(첫소리목록,19,samenstelling_WAARDE.첫)*21+Zoeken_invoer(가운뎃소리목록,21,samenstelling_WAARDE.가운데))*28+(samenstelling_WAARDE.끝?Zoeken_invoer(끝소리목록,28,samenstelling_WAARDE.끝):0);
    return samenstelling_WAARDE.첫?samenstelling_WAARDE.첫:samenstelling_WAARDE.가운데;
}
static int 한글넣기(unsigned toets_kwaststreek){
    unsigned 자모=0;for(unsigned 순번=0;순번<sizeof(toets_Indeling)/sizeof(toets_Indeling[0]);순번++)if(toets_Indeling[순번][0]==toets_kwaststreek)자모=toets_Indeling[순번][1];
    if(!자모&&toets_kwaststreek>='A'&&toets_kwaststreek<='Z')return 한글넣기(toets_kwaststreek+32);if(!자모)return 0;
    unsigned Vorige_item=조합글(),doorvoeren_WAARDE=0;samenstelling_Status 전=samenstelling_WAARDE;
    if(LOG_AANTAL<16)LOG_RECORD[LOG_AANTAL++]=전;
    if(Zoeken_invoer(첫소리목록,19,자모)>=0){
        if(samenstelling_WAARDE.첫&&samenstelling_WAARDE.가운데&&!samenstelling_WAARDE.끝&&Zoeken_invoer(끝소리목록,28,자모)>=0)samenstelling_WAARDE.끝=자모;
        else{unsigned overlay_WAARDE=Zoeken_duplicaat(겹끝소리,11,samenstelling_WAARDE.끝,자모);if(samenstelling_WAARDE.끝&&overlay_WAARDE)samenstelling_WAARDE.끝=overlay_WAARDE;
            else{doorvoeren_WAARDE=Vorige_item;doorvoeren_extern_toets();samenstelling_WAARDE.첫=자모;LOG_AANTAL=1;memset(LOG_RECORD,0,sizeof(samenstelling_Status));}}
    }else if(samenstelling_WAARDE.끝){
        unsigned 왼쪽=0,recht=samenstelling_WAARDE.끝;for(unsigned 순번=0;순번<11;순번++)if(겹끝소리[순번][2]==samenstelling_WAARDE.끝){왼쪽=겹끝소리[순번][0];recht=겹끝소리[순번][1];break;}
        samenstelling_WAARDE.끝=왼쪽;doorvoeren_WAARDE=조합글();doorvoeren_extern_toets();samenstelling_WAARDE.첫=recht;samenstelling_WAARDE.가운데=자모;LOG_AANTAL=2;
        memset(LOG_RECORD,0,2*sizeof(samenstelling_Status));LOG_RECORD[1].첫=recht;
    }else if(samenstelling_WAARDE.가운데){unsigned overlay_WAARDE=Zoeken_duplicaat(겹가운뎃소리,7,samenstelling_WAARDE.가운데,자모);
        if(overlay_WAARDE)samenstelling_WAARDE.가운데=overlay_WAARDE;else{doorvoeren_WAARDE=Vorige_item;doorvoeren_extern_toets();samenstelling_WAARDE.가운데=자모;LOG_AANTAL=1;memset(LOG_RECORD,0,sizeof(samenstelling_Status));}
    }else samenstelling_WAARDE.가운데=자모;
    if(Vorige_item)글넣기(127);if(doorvoeren_WAARDE)글넣기(doorvoeren_WAARDE);unsigned NU_WAARDE=조합글();if(NU_WAARDE)글넣기(NU_WAARDE);return 1;
}
void extern_toets_kwaststreek(unsigned symbool,int 누름){
    if(symbool==0xffe3||symbool==0xffe4){controle_WAARDE=누름;return;}
    if(symbool==0xffe1||symbool==0xffe2){SHIFT_toets=누름;return;}
    if(!누름)return;
    if(symbool==0xffc6||symbool==0xff31||(symbool==32&&SHIFT_toets&&!controle_WAARDE)){
        doorvoeren_extern_toets();한글=!한글;unsigned char Gebeurtenis[]={30,3,한글,0,0,0,0};feed_extern_invoer(Gebeurtenis,7);return;
    }
    if(symbool==0xff08&&한글&&!controle_WAARDE&&LOG_AANTAL){samenstelling_WAARDE=LOG_RECORD[--LOG_AANTAL];글넣기(127);unsigned tekst=조합글();if(tekst)글넣기(tekst);return;}
    if(한글&&!controle_WAARDE&&symbool<128&&한글넣기(symbool))return;
    doorvoeren_extern_toets();
    if((controle_WAARDE&&SHIFT_toets&&(symbool=='t'||symbool=='T'))||symbool==0xffc3||symbool==0xffc9){unsigned char Gebeurtenis[]={30,2,symbool==0xffc3?2:symbool==0xffc9?3:1,0,0,0,0};feed_extern_invoer(Gebeurtenis,7);return;}
    const char *특수=symbool==0xff08?"\177":symbool==0xff09?"\t":symbool==0xff0d?"\r":symbool==0xff1b?"\033":
        symbool==0xffff?"\033[3~":symbool==0xff50?"\033[H":symbool==0xff57?"\033[F":symbool==0xff51?"\033[D":
        symbool==0xff52?"\033[A":symbool==0xff53?"\033[C":symbool==0xff54?"\033[B":symbool==0xff55?"\033[5~":symbool==0xff56?"\033[6~":0;
    if(특수){feed_extern_invoer((const unsigned char*)특수,strlen(특수));return;}
    unsigned WAARDE=(symbool&0xff000000)==0x01000000?symbool&0xffffff:symbool;
    if(WAARDE>0x10ffff||(WAARDE>=0xd800&&WAARDE<=0xdfff)||(symbool>=0xff00&&symbool<0x1000000))return;
    if(controle_WAARDE){if(WAARDE>='a'&&WAARDE<='z')WAARDE-=96;else if(WAARDE>='A'&&WAARDE<='Z')WAARDE-=64;}
    글넣기(WAARDE);
}
