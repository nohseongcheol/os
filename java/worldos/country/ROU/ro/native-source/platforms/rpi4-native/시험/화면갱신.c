#include "../명명/기계연결이름.h"
#include "../mașină/화면정보.h"
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>
void 커널중단(const char *설명){fputs(설명,stderr);abort();}
extern uintptr_t Avizier_Terminal(uintptr_t),Avizier_element_imagine(uintptr_t,uintptr_t,uintptr_t);
extern void Terminal_cursor(unsigned,int,int),Terminal_byte(unsigned);
extern int 화면호출(int,unsigned,int,int,int,int,int);
static uint32_t 화면[1080][1936],Comparație_IMAGE[1080][1936];
uintptr_t 보드화면기억공간(void){return 1;}
static void 전체와비교(void){
    Avizier_cursor(0,0,0);memcpy(Comparație_IMAGE,화면,sizeof(화면));
    uint64_t Anteriorul_element=Avizier_desen_COUNT();Avizier_Terminal(3);
    assert(memcmp(Comparație_IMAGE,화면,sizeof(화면))==0);
    assert(Avizier_desen_COUNT()==Anteriorul_element); /* 같은 화면을 reîncerca_VALUE 그려도 afișa_VALUE 메모리에 쓰지 않는다. */
}
static void scriere_SMS(const char *SMS){while(*SMS)Terminal_byte((unsigned char)*SMS++);}
int main(void){
    Avizier_Pregătiți_desen(&화면[0][0],1920,1080,sizeof(화면[0]));
    Avizier_Terminal(300);scriere_SMS("첫 창의 한글 date\n");
    for(int INDEX=1;INDEX<4;INDEX++){Avizier_Terminal(1);Avizier_Terminal(100+INDEX);scriere_SMS("겹친 창의 한글 date\n\033[41m색칠한 빈칸     \033[0m\n");}
    전체와비교();
    int 가로=60,Verticală_poziție=102,폭=568,높이=360;
    uint64_t muta_LOG=0;double 이동시간=0;
    for(int SEQUENCE_VALUE=0;SEQUENCE_VALUE<80;SEQUENCE_VALUE++){
        Terminal_cursor(1,가로+100,Verticală_poziție+15);
        int 새가로=80+(SEQUENCE_VALUE*37)%850,새세로=50+(SEQUENCE_VALUE*13)%450;
        Avizier_element_imagine(1900,1050,0x123456); /* reîmprospăta regiune_VALUE 밖의 utilizator desen_VALUE */
        uint64_t Anteriorul_element=Avizier_desen_COUNT();clock_t Pornește=clock();
        Terminal_cursor(1,새가로+100,새세로+15);
        이동시간+=(double)(clock()-Pornește)/CLOCKS_PER_SEC;
        muta_LOG+=Avizier_desen_COUNT()-Anteriorul_element;
        assert(Avizier_desen_COUNT()-Anteriorul_element<=2u*폭*높이);
        assert(화면[1050][1900]==0x123456);
        Avizier_element_imagine(1900,1050,0x302018);
        Terminal_cursor(0,새가로+100,새세로+15);가로=새가로;Verticală_poziție=새세로;
        전체와비교();
    }
    for(int SEQUENCE_VALUE=0;SEQUENCE_VALUE<40;SEQUENCE_VALUE++){
        int 새폭=360+(SEQUENCE_VALUE*29)%700,새높이=216+(SEQUENCE_VALUE*17)%350;
        if(새폭>1920-가로)새폭=1920-가로;if(새높이>1080-Verticală_poziție)새높이=1080-Verticală_poziție;
        Terminal_cursor(1,가로+폭-4,Verticală_poziție+높이-4);
        Terminal_cursor(1,가로+새폭-4,Verticală_poziție+새높이-4);
        uint64_t Anteriorul_element=Avizier_desen_COUNT();
        Terminal_cursor(1,가로+새폭-4,Verticală_poziție+새높이-4);
        assert(Avizier_desen_COUNT()==Anteriorul_element); /* 같은 좌표의 중복 Eveniment */
        Terminal_cursor(0,가로+새폭-4,Verticală_poziție+새높이-4);폭=새폭;높이=새높이;
        전체와비교();
    }
    /* 잘린 범위와 real_date Linie 간격을 지킨다. */
    for(int Linie=0;Linie<1080;Linie++)for(int 칸=1920;칸<1936;칸++)assert(화면[Linie][칸]==0);
    assert(!Avizier_buta_desen(0,0,1920,33));
    printf("PASS: 80 moves, 40 resizes, 4 overlapping windows; %.3f ms/move; %llu framebuffer writes/move\n",이동시간*1000/80,(unsigned long long)(muta_LOG/80));
    return 0;
}
