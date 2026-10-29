#include "távoli_ÉRTÉK.h"
#include <string.h>
#include "두벌식표.h"
static unsigned vezérlő_ÉRTÉK,SHIFT_billentyű,한글;
typedef struct {unsigned 첫,가운데,끝;} rész_egész_Állapot;
static rész_egész_Állapot rész_egész_ÉRTÉK,LOG_REKORD[16];
static unsigned LOG_DARAB;
void véglegesít_távoli_Kulcs(void){memset(&rész_egész_ÉRTÉK,0,sizeof(rész_egész_ÉRTÉK));LOG_DARAB=0;}
void inicializál_távoli_Kulcs_tollvonás(void){vezérlő_ÉRTÉK=SHIFT_billentyű=한글=0;véglegesít_távoli_Kulcs();}
static void 글넣기(unsigned ÉRTÉK){
    unsigned char Szöveg[4];unsigned szám;
    if(ÉRTÉK<128){Szöveg[0]=ÉRTÉK;szám=1;}else if(ÉRTÉK<2048){Szöveg[0]=0xc0|(ÉRTÉK>>6);Szöveg[1]=0x80|(ÉRTÉK&63);szám=2;}
    else if(ÉRTÉK<65536){Szöveg[0]=0xe0|(ÉRTÉK>>12);Szöveg[1]=0x80|((ÉRTÉK>>6)&63);Szöveg[2]=0x80|(ÉRTÉK&63);szám=3;}
    else{Szöveg[0]=0xf0|(ÉRTÉK>>18);Szöveg[1]=0x80|((ÉRTÉK>>12)&63);Szöveg[2]=0x80|((ÉRTÉK>>6)&63);Szöveg[3]=0x80|(ÉRTÉK&63);szám=4;}
    csatorna_távoli_bevitel(Szöveg,szám);
}
static int keres_bejegyzés(const unsigned *bejegyzés_Lista,unsigned szám,unsigned ÉRTÉK){for(unsigned 순번=0;순번<szám;순번++)if(bejegyzés_Lista[순번]==ÉRTÉK)return 순번;return -1;}
static unsigned keres_másol(const unsigned keresőtáblázat[][3],unsigned szám,unsigned 가,unsigned MPERC_operandus){for(unsigned 순번=0;순번<szám;순번++)if(keresőtáblázat[순번][0]==가&&keresőtáblázat[순번][1]==MPERC_operandus)return keresőtáblázat[순번][2];return 0;}
static unsigned 조합글(void){
    if(rész_egész_ÉRTÉK.첫&&rész_egész_ÉRTÉK.가운데)return 0xac00+(keres_bejegyzés(첫소리목록,19,rész_egész_ÉRTÉK.첫)*21+keres_bejegyzés(가운뎃소리목록,21,rész_egész_ÉRTÉK.가운데))*28+(rész_egész_ÉRTÉK.끝?keres_bejegyzés(끝소리목록,28,rész_egész_ÉRTÉK.끝):0);
    return rész_egész_ÉRTÉK.첫?rész_egész_ÉRTÉK.첫:rész_egész_ÉRTÉK.가운데;
}
static int 한글넣기(unsigned Kulcs_tollvonás){
    unsigned 자모=0;for(unsigned 순번=0;순번<sizeof(Kulcs_Navigáció)/sizeof(Kulcs_Navigáció[0]);순번++)if(Kulcs_Navigáció[순번][0]==Kulcs_tollvonás)자모=Kulcs_Navigáció[순번][1];
    if(!자모&&Kulcs_tollvonás>='A'&&Kulcs_tollvonás<='Z')return 한글넣기(Kulcs_tollvonás+32);if(!자모)return 0;
    unsigned Előző_cikk=조합글(),véglegesít_ÉRTÉK=0;rész_egész_Állapot 전=rész_egész_ÉRTÉK;
    if(LOG_DARAB<16)LOG_REKORD[LOG_DARAB++]=전;
    if(keres_bejegyzés(첫소리목록,19,자모)>=0){
        if(rész_egész_ÉRTÉK.첫&&rész_egész_ÉRTÉK.가운데&&!rész_egész_ÉRTÉK.끝&&keres_bejegyzés(끝소리목록,28,자모)>=0)rész_egész_ÉRTÉK.끝=자모;
        else{unsigned átfedés_ÉRTÉK=keres_másol(겹끝소리,11,rész_egész_ÉRTÉK.끝,자모);if(rész_egész_ÉRTÉK.끝&&átfedés_ÉRTÉK)rész_egész_ÉRTÉK.끝=átfedés_ÉRTÉK;
            else{véglegesít_ÉRTÉK=Előző_cikk;véglegesít_távoli_Kulcs();rész_egész_ÉRTÉK.첫=자모;LOG_DARAB=1;memset(LOG_REKORD,0,sizeof(rész_egész_Állapot));}}
    }else if(rész_egész_ÉRTÉK.끝){
        unsigned 왼쪽=0,jog=rész_egész_ÉRTÉK.끝;for(unsigned 순번=0;순번<11;순번++)if(겹끝소리[순번][2]==rész_egész_ÉRTÉK.끝){왼쪽=겹끝소리[순번][0];jog=겹끝소리[순번][1];break;}
        rész_egész_ÉRTÉK.끝=왼쪽;véglegesít_ÉRTÉK=조합글();véglegesít_távoli_Kulcs();rész_egész_ÉRTÉK.첫=jog;rész_egész_ÉRTÉK.가운데=자모;LOG_DARAB=2;
        memset(LOG_REKORD,0,2*sizeof(rész_egész_Állapot));LOG_REKORD[1].첫=jog;
    }else if(rész_egész_ÉRTÉK.가운데){unsigned átfedés_ÉRTÉK=keres_másol(겹가운뎃소리,7,rész_egész_ÉRTÉK.가운데,자모);
        if(átfedés_ÉRTÉK)rész_egész_ÉRTÉK.가운데=átfedés_ÉRTÉK;else{véglegesít_ÉRTÉK=Előző_cikk;véglegesít_távoli_Kulcs();rész_egész_ÉRTÉK.가운데=자모;LOG_DARAB=1;memset(LOG_REKORD,0,sizeof(rész_egész_Állapot));}
    }else rész_egész_ÉRTÉK.가운데=자모;
    if(Előző_cikk)글넣기(127);if(véglegesít_ÉRTÉK)글넣기(véglegesít_ÉRTÉK);unsigned MOST_ÉRTÉK=조합글();if(MOST_ÉRTÉK)글넣기(MOST_ÉRTÉK);return 1;
}
void távoli_Kulcs_tollvonás(unsigned szimbólum,int 누름){
    if(szimbólum==0xffe3||szimbólum==0xffe4){vezérlő_ÉRTÉK=누름;return;}
    if(szimbólum==0xffe1||szimbólum==0xffe2){SHIFT_billentyű=누름;return;}
    if(!누름)return;
    if(szimbólum==0xffc6||szimbólum==0xff31||(szimbólum==32&&SHIFT_billentyű&&!vezérlő_ÉRTÉK)){
        véglegesít_távoli_Kulcs();한글=!한글;unsigned char Esemény[]={30,3,한글,0,0,0,0};csatorna_távoli_bevitel(Esemény,7);return;
    }
    if(szimbólum==0xff08&&한글&&!vezérlő_ÉRTÉK&&LOG_DARAB){rész_egész_ÉRTÉK=LOG_REKORD[--LOG_DARAB];글넣기(127);unsigned Szöveg=조합글();if(Szöveg)글넣기(Szöveg);return;}
    if(한글&&!vezérlő_ÉRTÉK&&szimbólum<128&&한글넣기(szimbólum))return;
    véglegesít_távoli_Kulcs();
    if((vezérlő_ÉRTÉK&&SHIFT_billentyű&&(szimbólum=='t'||szimbólum=='T'))||szimbólum==0xffc3||szimbólum==0xffc9){unsigned char Esemény[]={30,2,szimbólum==0xffc3?2:szimbólum==0xffc9?3:1,0,0,0,0};csatorna_távoli_bevitel(Esemény,7);return;}
    const char *특수=szimbólum==0xff08?"\177":szimbólum==0xff09?"\t":szimbólum==0xff0d?"\r":szimbólum==0xff1b?"\033":
        szimbólum==0xffff?"\033[3~":szimbólum==0xff50?"\033[H":szimbólum==0xff57?"\033[F":szimbólum==0xff51?"\033[D":
        szimbólum==0xff52?"\033[A":szimbólum==0xff53?"\033[C":szimbólum==0xff54?"\033[B":szimbólum==0xff55?"\033[5~":szimbólum==0xff56?"\033[6~":0;
    if(특수){csatorna_távoli_bevitel((const unsigned char*)특수,strlen(특수));return;}
    unsigned ÉRTÉK=(szimbólum&0xff000000)==0x01000000?szimbólum&0xffffff:szimbólum;
    if(ÉRTÉK>0x10ffff||(ÉRTÉK>=0xd800&&ÉRTÉK<=0xdfff)||(szimbólum>=0xff00&&szimbólum<0x1000000))return;
    if(vezérlő_ÉRTÉK){if(ÉRTÉK>='a'&&ÉRTÉK<='z')ÉRTÉK-=96;else if(ÉRTÉK>='A'&&ÉRTÉK<='Z')ÉRTÉK-=64;}
    글넣기(ÉRTÉK);
}
