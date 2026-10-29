#include "../명명/기계연결이름.h"
#include "../računalnik/화면정보.h"
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>
void 커널중단(const char *설명){fputs(설명,stderr);abort();}
extern uintptr_t Tabla_Terminal(uintptr_t),Tabla_slikovna_pika(uintptr_t,uintptr_t,uintptr_t);
extern void Terminal_kazalec(unsigned,int,int),Terminal_bajt(unsigned);
extern int 화면호출(int,unsigned,int,int,int,int,int);
static uint32_t 화면[1080][1936],Primerjava_IMAGE[1080][1936];
uintptr_t 보드화면기억공간(void){return 1;}
static void 전체와비교(void){
    Tabla_kazalec(0,0,0);memcpy(Primerjava_IMAGE,화면,sizeof(화면));
    uint64_t 이전=Tabla_risba_COUNT();Tabla_Terminal(3);
    assert(memcmp(Primerjava_IMAGE,화면,sizeof(화면))==0);
    assert(Tabla_risba_COUNT()==이전); /* 같은 화면을 znova_poskusiti_VALUE 그려도 oddaja_VALUE_487749b8 메모리에 쓰지 않는다. */
}
static void pisati_SMS(const char *Besedilo){while(*Besedilo)Terminal_bajt((unsigned char)*Besedilo++);}
int main(void){
    Tabla_Pripravi_risba(&화면[0][0],1920,1080,sizeof(화면[0]));
    Tabla_Terminal(300);pisati_SMS("첫 창의 한글 podatki\n");
    for(int INDEX=1;INDEX<4;INDEX++){Tabla_Terminal(1);Tabla_Terminal(100+INDEX);pisati_SMS("겹친 창의 한글 podatki\n\033[41m색칠한 빈칸     \033[0m\n");}
    전체와비교();
    int 가로=60,Navpično_položaj=102,폭=568,višina_VALUE=360;
    uint64_t premikati_LOG=0;double 이동시간=0;
    for(int SEQUENCE_VALUE=0;SEQUENCE_VALUE<80;SEQUENCE_VALUE++){
        Terminal_kazalec(1,가로+100,Navpično_položaj+15);
        int 새가로=80+(SEQUENCE_VALUE*37)%850,새세로=50+(SEQUENCE_VALUE*13)%450;
        Tabla_slikovna_pika(1900,1050,0x123456); /* osvežiti območje_VALUE_0e9a97ab 밖의 uporabnik risba_VALUE */
        uint64_t 이전=Tabla_risba_COUNT();clock_t Zaženi=clock();
        Terminal_kazalec(1,새가로+100,새세로+15);
        이동시간+=(double)(clock()-Zaženi)/CLOCKS_PER_SEC;
        premikati_LOG+=Tabla_risba_COUNT()-이전;
        assert(Tabla_risba_COUNT()-이전<=2u*폭*višina_VALUE);
        assert(화면[1050][1900]==0x123456);
        Tabla_slikovna_pika(1900,1050,0x302018);
        Terminal_kazalec(0,새가로+100,새세로+15);가로=새가로;Navpično_položaj=새세로;
        전체와비교();
    }
    for(int SEQUENCE_VALUE=0;SEQUENCE_VALUE<40;SEQUENCE_VALUE++){
        int 새폭=360+(SEQUENCE_VALUE*29)%700,새높이=216+(SEQUENCE_VALUE*17)%350;
        if(새폭>1920-가로)새폭=1920-가로;if(새높이>1080-Navpično_položaj)새높이=1080-Navpično_položaj;
        Terminal_kazalec(1,가로+폭-4,Navpično_položaj+višina_VALUE-4);
        Terminal_kazalec(1,가로+새폭-4,Navpično_položaj+새높이-4);
        uint64_t 이전=Tabla_risba_COUNT();
        Terminal_kazalec(1,가로+새폭-4,Navpično_položaj+새높이-4);
        assert(Tabla_risba_COUNT()==이전); /* 같은 좌표의 중복 dogodek */
        Terminal_kazalec(0,가로+새폭-4,Navpično_položaj+새높이-4);폭=새폭;višina_VALUE=새높이;
        전체와비교();
    }
    /* 잘린 범위와 dejanski_podatki Črtni 간격을 지킨다. */
    for(int Črtni=0;Črtni<1080;Črtni++)for(int 칸=1920;칸<1936;칸++)assert(화면[Črtni][칸]==0);
    assert(!Tabla_Start_risba(0,0,1920,33));
    printf("PASS: 80 moves, 40 resizes, 4 overlapping windows; %.3f ms/move; %llu framebuffer writes/move\n",이동시간*1000/80,(unsigned long long)(premikati_LOG/80));
    return 0;
}
