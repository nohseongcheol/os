#include "../명명/기계연결이름.h"
#include "../machine/scherm_info.h"
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>
void 커널중단(const char *설명){fputs(설명,stderr);abort();}
extern uintptr_t Bord_Terminal(uintptr_t),Bord_pixel(uintptr_t,uintptr_t,uintptr_t);
extern void Terminal_wijzer(unsigned,int,int),Terminal_byte(unsigned);
extern int 화면호출(int,unsigned,int,int,int,int,int);
static uint32_t scherm[1080][1936],Vergelijking_kopie[1080][1936];
uintptr_t 보드화면기억공간(void){return 1;}
static void 전체와비교(void){
    Bord_wijzer(0,0,0);memcpy(Vergelijking_kopie,scherm,sizeof(scherm));
    uint64_t Vorige_item=Bord_tekening_AANTAL();Bord_Terminal(3);
    assert(memcmp(Vergelijking_kopie,scherm,sizeof(scherm))==0);
    assert(Bord_tekening_AANTAL()==Vorige_item); /* 같은 화면을 opnieuw_proberen_WAARDE 그려도 weergeven_WAARDE 메모리에 쓰지 않는다. */
}
static void schrijven_sms(const char *tekst){while(*tekst)Terminal_byte((unsigned char)*tekst++);}
int main(void){
    Bord_Bereid_voor_tekening(&scherm[0][0],1920,1080,sizeof(scherm[0]));
    Bord_Terminal(300);schrijven_sms("첫 창의 한글 gegevens\n");
    for(int INDEX=1;INDEX<4;INDEX++){Bord_Terminal(1);Bord_Terminal(100+INDEX);schrijven_sms("겹친 창의 한글 gegevens\n\033[41m색칠한 빈칸     \033[0m\n");}
    전체와비교();
    int 가로=60,Verticaal_functie=102,폭=568,hoogte_WAARDE=360;
    uint64_t verplaatsen_LOG=0;double 이동시간=0;
    for(int REEKS_WAARDE=0;REEKS_WAARDE<80;REEKS_WAARDE++){
        Terminal_wijzer(1,가로+100,Verticaal_functie+15);
        int 새가로=80+(REEKS_WAARDE*37)%850,새세로=50+(REEKS_WAARDE*13)%450;
        Bord_pixel(1900,1050,0x123456); /* vernieuwen regio_WAARDE 밖의 gebruikersruimte tekening_WAARDE */
        uint64_t Vorige_item=Bord_tekening_AANTAL();clock_t starten=clock();
        Terminal_wijzer(1,새가로+100,새세로+15);
        이동시간+=(double)(clock()-starten)/CLOCKS_PER_SEC;
        verplaatsen_LOG+=Bord_tekening_AANTAL()-Vorige_item;
        assert(Bord_tekening_AANTAL()-Vorige_item<=2u*폭*hoogte_WAARDE);
        assert(scherm[1050][1900]==0x123456);
        Bord_pixel(1900,1050,0x302018);
        Terminal_wijzer(0,새가로+100,새세로+15);가로=새가로;Verticaal_functie=새세로;
        전체와비교();
    }
    for(int REEKS_WAARDE=0;REEKS_WAARDE<40;REEKS_WAARDE++){
        int 새폭=360+(REEKS_WAARDE*29)%700,새높이=216+(REEKS_WAARDE*17)%350;
        if(새폭>1920-가로)새폭=1920-가로;if(새높이>1080-Verticaal_functie)새높이=1080-Verticaal_functie;
        Terminal_wijzer(1,가로+폭-4,Verticaal_functie+hoogte_WAARDE-4);
        Terminal_wijzer(1,가로+새폭-4,Verticaal_functie+새높이-4);
        uint64_t Vorige_item=Bord_tekening_AANTAL();
        Terminal_wijzer(1,가로+새폭-4,Verticaal_functie+새높이-4);
        assert(Bord_tekening_AANTAL()==Vorige_item); /* 같은 좌표의 중복 Gebeurtenis */
        Terminal_wijzer(0,가로+새폭-4,Verticaal_functie+새높이-4);폭=새폭;hoogte_WAARDE=새높이;
        전체와비교();
    }
    /* 잘린 범위와 werkelijk_gegevens invoerregel 간격을 지킨다. */
    for(int invoerregel=0;invoerregel<1080;invoerregel++)for(int sleuf_invoer=1920;sleuf_invoer<1936;sleuf_invoer++)assert(scherm[invoerregel][sleuf_invoer]==0);
    assert(!Bord_START_tekening(0,0,1920,33));
    printf("PASS: 80 moves, 40 resizes, 4 overlapping windows; %.3f ms/move; %llu framebuffer writes/move\n",이동시간*1000/80,(unsigned long long)(verplaatsen_LOG/80));
    return 0;
}
