#include "../명명/기계연결이름.h"
#include "../maskine/skærmbillede_info.h"
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>
void 커널중단(const char *설명){fputs(설명,stderr);abort();}
extern uintptr_t Tavle_Terminal(uintptr_t),Tavle_pixel(uintptr_t,uintptr_t,uintptr_t);
extern void Terminal_markør(unsigned,int,int),Terminal_byte(unsigned);
extern int 화면호출(int,unsigned,int,int,int,int,int);
static uint32_t skærmbillede[1080][1936],Sammenligning_Image[1080][1936];
uintptr_t 보드화면기억공간(void){return 1;}
static void 전체와비교(void){
    Tavle_markør(0,0,0);memcpy(Sammenligning_Image,skærmbillede,sizeof(skærmbillede));
    uint64_t Forrige_vare=Tavle_tegning_TÆL();Tavle_Terminal(3);
    assert(memcmp(Sammenligning_Image,skærmbillede,sizeof(skærmbillede))==0);
    assert(Tavle_tegning_TÆL()==Forrige_vare); /* 같은 화면을 prøve_igen_VÆRDI 그려도 vise_VÆRDI 메모리에 쓰지 않는다. */
}
static void skrive_sms(const char *Tekst){while(*Tekst)Terminal_byte((unsigned char)*Tekst++);}
int main(void){
    Tavle_Tilrettelæg_tegning(&skærmbillede[0][0],1920,1080,sizeof(skærmbillede[0]));
    Tavle_Terminal(300);skrive_sms("첫 창의 한글 data\n");
    for(int INDEKS=1;INDEKS<4;INDEKS++){Tavle_Terminal(1);Tavle_Terminal(100+INDEKS);skrive_sms("겹친 창의 한글 data\n\033[41m색칠한 빈칸     \033[0m\n");}
    전체와비교();
    int 가로=60,Lodret_placere=102,폭=568,높이=360;
    uint64_t flytte_LOG=0;double 이동시간=0;
    for(int SEKVENS_VÆRDI=0;SEKVENS_VÆRDI<80;SEKVENS_VÆRDI++){
        Terminal_markør(1,가로+100,Lodret_placere+15);
        int 새가로=80+(SEKVENS_VÆRDI*37)%850,새세로=50+(SEKVENS_VÆRDI*13)%450;
        Tavle_pixel(1900,1050,0x123456); /* opdatere område_VÆRDI_0e9a97ab 밖의 bruger tegning_VÆRDI */
        uint64_t Forrige_vare=Tavle_tegning_TÆL();clock_t Kør_2=clock();
        Terminal_markør(1,새가로+100,새세로+15);
        이동시간+=(double)(clock()-Kør_2)/CLOCKS_PER_SEC;
        flytte_LOG+=Tavle_tegning_TÆL()-Forrige_vare;
        assert(Tavle_tegning_TÆL()-Forrige_vare<=2u*폭*높이);
        assert(skærmbillede[1050][1900]==0x123456);
        Tavle_pixel(1900,1050,0x302018);
        Terminal_markør(0,새가로+100,새세로+15);가로=새가로;Lodret_placere=새세로;
        전체와비교();
    }
    for(int SEKVENS_VÆRDI=0;SEKVENS_VÆRDI<40;SEKVENS_VÆRDI++){
        int 새폭=360+(SEKVENS_VÆRDI*29)%700,새높이=216+(SEKVENS_VÆRDI*17)%350;
        if(새폭>1920-가로)새폭=1920-가로;if(새높이>1080-Lodret_placere)새높이=1080-Lodret_placere;
        Terminal_markør(1,가로+폭-4,Lodret_placere+높이-4);
        Terminal_markør(1,가로+새폭-4,Lodret_placere+새높이-4);
        uint64_t Forrige_vare=Tavle_tegning_TÆL();
        Terminal_markør(1,가로+새폭-4,Lodret_placere+새높이-4);
        assert(Tavle_tegning_TÆL()==Forrige_vare); /* 같은 좌표의 중복 hændelse */
        Terminal_markør(0,가로+새폭-4,Lodret_placere+새높이-4);폭=새폭;높이=새높이;
        전체와비교();
    }
    /* 잘린 범위와 faktisk_data Linje 간격을 지킨다. */
    for(int Linje=0;Linje<1080;Linje++)for(int udvidelsesstik_post=1920;udvidelsesstik_post<1936;udvidelsesstik_post++)assert(skærmbillede[Linje][udvidelsesstik_post]==0);
    assert(!Tavle_START_tegning(0,0,1920,33));
    printf("PASS: 80 moves, 40 resizes, 4 overlapping windows; %.3f ms/move; %llu framebuffer writes/move\n",이동시간*1000/80,(unsigned long long)(flytte_LOG/80));
    return 0;
}
