#include "../명명/기계연결이름.h"
#include "../arvuti/화면정보.h"
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>
void 커널중단(const char *설명){fputs(설명,stderr);abort();}
extern uintptr_t Tahvel_terminal(uintptr_t),Tahvel_piksel(uintptr_t,uintptr_t,uintptr_t);
extern void terminal_kursor(unsigned,int,int),terminal_bait(unsigned);
extern int 화면호출(int,unsigned,int,int,int,int,int);
static uint32_t 화면[1080][1936],Võrdlus_pilt[1080][1936];
uintptr_t 보드화면기억공간(void){return 1;}
static void 전체와비교(void){
    Tahvel_kursor(0,0,0);memcpy(Võrdlus_pilt,화면,sizeof(화면));
    uint64_t 이전=Tahvel_joonis_COUNT();Tahvel_terminal(3);
    assert(memcmp(Võrdlus_pilt,화면,sizeof(화면))==0);
    assert(Tahvel_joonis_COUNT()==이전); /* 같은 화면을 uuesti_proovima_VALUE 그려도 saade_VALUE 메모리에 쓰지 않는다. */
}
static void kirjutamine_SMS(const char *Tekst){while(*Tekst)terminal_bait((unsigned char)*Tekst++);}
int main(void){
    Tahvel_Ettevalmistamine_joonis(&화면[0][0],1920,1080,sizeof(화면[0]));
    Tahvel_terminal(300);kirjutamine_SMS("첫 창의 한글 andmed\n");
    for(int INDEX=1;INDEX<4;INDEX++){Tahvel_terminal(1);Tahvel_terminal(100+INDEX);kirjutamine_SMS("겹친 창의 한글 andmed\n\033[41m색칠한 빈칸     \033[0m\n");}
    전체와비교();
    int 가로=60,vertikaal_ametikoht=102,폭=568,높이=360;
    uint64_t liigutama_LOG=0;double 이동시간=0;
    for(int SEQUENCE_VALUE=0;SEQUENCE_VALUE<80;SEQUENCE_VALUE++){
        terminal_kursor(1,가로+100,vertikaal_ametikoht+15);
        int 새가로=80+(SEQUENCE_VALUE*37)%850,새세로=50+(SEQUENCE_VALUE*13)%450;
        Tahvel_piksel(1900,1050,0x123456); /* värskendama regioon_VALUE 밖의 kasutaja joonis_VALUE */
        uint64_t 이전=Tahvel_joonis_COUNT();clock_t Käivita_2=clock();
        terminal_kursor(1,새가로+100,새세로+15);
        이동시간+=(double)(clock()-Käivita_2)/CLOCKS_PER_SEC;
        liigutama_LOG+=Tahvel_joonis_COUNT()-이전;
        assert(Tahvel_joonis_COUNT()-이전<=2u*폭*높이);
        assert(화면[1050][1900]==0x123456);
        Tahvel_piksel(1900,1050,0x302018);
        terminal_kursor(0,새가로+100,새세로+15);가로=새가로;vertikaal_ametikoht=새세로;
        전체와비교();
    }
    for(int SEQUENCE_VALUE=0;SEQUENCE_VALUE<40;SEQUENCE_VALUE++){
        int 새폭=360+(SEQUENCE_VALUE*29)%700,새높이=216+(SEQUENCE_VALUE*17)%350;
        if(새폭>1920-가로)새폭=1920-가로;if(새높이>1080-vertikaal_ametikoht)새높이=1080-vertikaal_ametikoht;
        terminal_kursor(1,가로+폭-4,vertikaal_ametikoht+높이-4);
        terminal_kursor(1,가로+새폭-4,vertikaal_ametikoht+새높이-4);
        uint64_t 이전=Tahvel_joonis_COUNT();
        terminal_kursor(1,가로+새폭-4,vertikaal_ametikoht+새높이-4);
        assert(Tahvel_joonis_COUNT()==이전); /* 같은 좌표의 중복 Sündmus */
        terminal_kursor(0,가로+새폭-4,vertikaal_ametikoht+새높이-4);폭=새폭;높이=새높이;
        전체와비교();
    }
    /* 잘린 범위와 tegelik_andmed Joon 간격을 지킨다. */
    for(int Joon=0;Joon<1080;Joon++)for(int 칸=1920;칸<1936;칸++)assert(화면[Joon][칸]==0);
    assert(!Tahvel_START_joonis(0,0,1920,33));
    printf("PASS: 80 moves, 40 resizes, 4 overlapping windows; %.3f ms/move; %llu framebuffer writes/move\n",이동시간*1000/80,(unsigned long long)(liigutama_LOG/80));
    return 0;
}
