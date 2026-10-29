#include "../명명/기계연결이름.h"
#include "../maskin/skjermbilde_info.h"
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>
void 커널중단(const char *설명){fputs(설명,stderr);abort();}
extern uintptr_t Tavle_Terminal(uintptr_t),Tavle_piksel(uintptr_t,uintptr_t,uintptr_t);
extern void Terminal_peker(unsigned,int,int),Terminal_byte(unsigned);
extern int 화면호출(int,unsigned,int,int,int,int,int);
static uint32_t skjermbilde[1080][1936],Sammenligning_BILDE[1080][1936];
uintptr_t 보드화면기억공간(void){return 1;}
static void 전체와비교(void){
    Tavle_peker(0,0,0);memcpy(Sammenligning_BILDE,skjermbilde,sizeof(skjermbilde));
    uint64_t Forrige_vare=Tavle_tegning_ANTALL();Tavle_Terminal(3);
    assert(memcmp(Sammenligning_BILDE,skjermbilde,sizeof(skjermbilde))==0);
    assert(Tavle_tegning_ANTALL()==Forrige_vare); /* 같은 화면을 prøve_på_nytt_VERDI 그려도 vise_VERDI_487749b8 메모리에 쓰지 않는다. */
}
static void skrive_SMS(const char *Tekst){while(*Tekst)Terminal_byte((unsigned char)*Tekst++);}
int main(void){
    Tavle_Forbered_tegning(&skjermbilde[0][0],1920,1080,sizeof(skjermbilde[0]));
    Tavle_Terminal(300);skrive_SMS("첫 창의 한글 data\n");
    for(int INDEKS=1;INDEKS<4;INDEKS++){Tavle_Terminal(1);Tavle_Terminal(100+INDEKS);skrive_SMS("겹친 창의 한글 data\n\033[41m색칠한 빈칸     \033[0m\n");}
    전체와비교();
    int 가로=60,vertikal_plassere=102,폭=568,높이=360;
    uint64_t flytte_LOG=0;double 이동시간=0;
    for(int SEKVENS_VERDI=0;SEKVENS_VERDI<80;SEKVENS_VERDI++){
        Terminal_peker(1,가로+100,vertikal_plassere+15);
        int 새가로=80+(SEKVENS_VERDI*37)%850,새세로=50+(SEKVENS_VERDI*13)%450;
        Tavle_piksel(1900,1050,0x123456); /* oppdatere område_VERDI_0e9a97ab 밖의 bruker tegning_VERDI */
        uint64_t Forrige_vare=Tavle_tegning_ANTALL();clock_t Kjør_2=clock();
        Terminal_peker(1,새가로+100,새세로+15);
        이동시간+=(double)(clock()-Kjør_2)/CLOCKS_PER_SEC;
        flytte_LOG+=Tavle_tegning_ANTALL()-Forrige_vare;
        assert(Tavle_tegning_ANTALL()-Forrige_vare<=2u*폭*높이);
        assert(skjermbilde[1050][1900]==0x123456);
        Tavle_piksel(1900,1050,0x302018);
        Terminal_peker(0,새가로+100,새세로+15);가로=새가로;vertikal_plassere=새세로;
        전체와비교();
    }
    for(int SEKVENS_VERDI=0;SEKVENS_VERDI<40;SEKVENS_VERDI++){
        int 새폭=360+(SEKVENS_VERDI*29)%700,새높이=216+(SEKVENS_VERDI*17)%350;
        if(새폭>1920-가로)새폭=1920-가로;if(새높이>1080-vertikal_plassere)새높이=1080-vertikal_plassere;
        Terminal_peker(1,가로+폭-4,vertikal_plassere+높이-4);
        Terminal_peker(1,가로+새폭-4,vertikal_plassere+새높이-4);
        uint64_t Forrige_vare=Tavle_tegning_ANTALL();
        Terminal_peker(1,가로+새폭-4,vertikal_plassere+새높이-4);
        assert(Tavle_tegning_ANTALL()==Forrige_vare); /* 같은 좌표의 중복 Hendelse */
        Terminal_peker(0,가로+새폭-4,vertikal_plassere+새높이-4);폭=새폭;높이=새높이;
        전체와비교();
    }
    /* 잘린 범위와 faktisk_data Linje 간격을 지킨다. */
    for(int Linje=0;Linje<1080;Linje++)for(int åpning_oppføring=1920;åpning_oppføring<1936;åpning_oppføring++)assert(skjermbilde[Linje][åpning_oppføring]==0);
    assert(!Tavle_START_tegning(0,0,1920,33));
    printf("PASS: 80 moves, 40 resizes, 4 overlapping windows; %.3f ms/move; %llu framebuffer writes/move\n",이동시간*1000/80,(unsigned long long)(flytte_LOG/80));
    return 0;
}
