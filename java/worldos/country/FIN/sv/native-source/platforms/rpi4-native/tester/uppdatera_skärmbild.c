#include "../명명/기계연결이름.h"
#include "../dator/skärmbild_info.h"
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>
void 커널중단(const char *설명){fputs(설명,stderr);abort();}
extern uintptr_t Tavla_Terminal(uintptr_t),Tavla_bildpunkt(uintptr_t,uintptr_t,uintptr_t);
extern void Terminal_markör(unsigned,int,int),Terminal_byte(unsigned);
extern int 화면호출(int,unsigned,int,int,int,int,int);
static uint32_t skärmbild[1080][1936],Jämförelse_BILD[1080][1936];
uintptr_t 보드화면기억공간(void){return 1;}
static void 전체와비교(void){
    Tavla_markör(0,0,0);memcpy(Jämförelse_BILD,skärmbild,sizeof(skärmbild));
    uint64_t Föregående_objekt=Tavla_ritning_ANTAL();Tavla_Terminal(3);
    assert(memcmp(Jämförelse_BILD,skärmbild,sizeof(skärmbild))==0);
    assert(Tavla_ritning_ANTAL()==Föregående_objekt); /* 같은 화면을 försöka_igen_värde 그려도 visa_värde 메모리에 쓰지 않는다. */
}
static void skriva_SMS(const char *text){while(*text)Terminal_byte((unsigned char)*text++);}
int main(void){
    Tavla_Förbereda_ritning(&skärmbild[0][0],1920,1080,sizeof(skärmbild[0]));
    Tavla_Terminal(300);skriva_SMS("첫 창의 한글 data\n");
    for(int INDEX=1;INDEX<4;INDEX++){Tavla_Terminal(1);Tavla_Terminal(100+INDEX);skriva_SMS("겹친 창의 한글 data\n\033[41m색칠한 빈칸     \033[0m\n");}
    전체와비교();
    int 가로=60,bransch_placera=102,폭=568,높이=360;
    uint64_t flytta_LOG=0;double 이동시간=0;
    for(int SEKVENS_värde=0;SEKVENS_värde<80;SEKVENS_värde++){
        Terminal_markör(1,가로+100,bransch_placera+15);
        int 새가로=80+(SEKVENS_värde*37)%850,새세로=50+(SEKVENS_värde*13)%450;
        Tavla_bildpunkt(1900,1050,0x123456); /* uppdatera område_värde_0e9a97ab 밖의 användarutrymme ritning_värde */
        uint64_t Föregående_objekt=Tavla_ritning_ANTAL();clock_t Kör=clock();
        Terminal_markör(1,새가로+100,새세로+15);
        이동시간+=(double)(clock()-Kör)/CLOCKS_PER_SEC;
        flytta_LOG+=Tavla_ritning_ANTAL()-Föregående_objekt;
        assert(Tavla_ritning_ANTAL()-Föregående_objekt<=2u*폭*높이);
        assert(skärmbild[1050][1900]==0x123456);
        Tavla_bildpunkt(1900,1050,0x302018);
        Terminal_markör(0,새가로+100,새세로+15);가로=새가로;bransch_placera=새세로;
        전체와비교();
    }
    for(int SEKVENS_värde=0;SEKVENS_värde<40;SEKVENS_värde++){
        int 새폭=360+(SEKVENS_värde*29)%700,새높이=216+(SEKVENS_värde*17)%350;
        if(새폭>1920-가로)새폭=1920-가로;if(새높이>1080-bransch_placera)새높이=1080-bransch_placera;
        Terminal_markör(1,가로+폭-4,bransch_placera+높이-4);
        Terminal_markör(1,가로+새폭-4,bransch_placera+새높이-4);
        uint64_t Föregående_objekt=Tavla_ritning_ANTAL();
        Terminal_markör(1,가로+새폭-4,bransch_placera+새높이-4);
        assert(Tavla_ritning_ANTAL()==Föregående_objekt); /* 같은 좌표의 중복 Händelse */
        Terminal_markör(0,가로+새폭-4,bransch_placera+새높이-4);폭=새폭;높이=새높이;
        전체와비교();
    }
    /* 잘린 범위와 verklig_data inmatningsrad 간격을 지킨다. */
    for(int inmatningsrad=0;inmatningsrad<1080;inmatningsrad++)for(int fack_post=1920;fack_post<1936;fack_post++)assert(skärmbild[inmatningsrad][fack_post]==0);
    assert(!Tavla_START_ritning(0,0,1920,33));
    printf("PASS: 80 moves, 40 resizes, 4 overlapping windows; %.3f ms/move; %llu framebuffer writes/move\n",이동시간*1000/80,(unsigned long long)(flytta_LOG/80));
    return 0;
}
