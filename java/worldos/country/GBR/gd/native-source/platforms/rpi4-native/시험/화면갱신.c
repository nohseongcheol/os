#include "../명명/기계연결이름.h"
#include "../inneal/화면정보.h"
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>
void 커널중단(const char *설명){fputs(설명,stderr);abort();}
extern uintptr_t bòrd_tèirmineal(uintptr_t),bòrd_pel(uintptr_t,uintptr_t,uintptr_t);
extern void tèirmineal_tomhaire(unsigned,int,int),tèirmineal_baidht(unsigned);
extern int 화면호출(int,unsigned,int,int,int,int,int);
static uint32_t 화면[1080][1936],비교그림[1080][1936];
uintptr_t 보드화면기억공간(void){return 1;}
static void 전체와비교(void){
    bòrd_tomhaire(0,0,0);memcpy(비교그림,화면,sizeof(화면));
    uint64_t 이전=bòrd_tarraing_COUNT();bòrd_tèirmineal(3);
    assert(memcmp(비교그림,화면,sizeof(화면))==0);
    assert(bòrd_tarraing_COUNT()==이전); /* 같은 화면을 다시 그려도 show_VALUE 메모리에 쓰지 않는다. */
}
static void sgrìobh_SMS(const char *SMS){while(*SMS)tèirmineal_baidht((unsigned char)*SMS++);}
int main(void){
    bòrd_Ullaich_tarraing(&화면[0][0],1920,1080,sizeof(화면[0]));
    bòrd_tèirmineal(300);sgrìobh_SMS("첫 창의 한글 dàta\n");
    for(int INDEX=1;INDEX<4;INDEX++){bòrd_tèirmineal(1);bòrd_tèirmineal(100+INDEX);sgrìobh_SMS("겹친 창의 한글 dàta\n\033[41m색칠한 빈칸     \033[0m\n");}
    전체와비교();
    int 가로=60,inghearach_suidhich=102,폭=568,높이=360;
    uint64_t gluais_LOG=0;double 이동시간=0;
    for(int SEQUENCE_VALUE=0;SEQUENCE_VALUE<80;SEQUENCE_VALUE++){
        tèirmineal_tomhaire(1,가로+100,inghearach_suidhich+15);
        int 새가로=80+(SEQUENCE_VALUE*37)%850,새세로=50+(SEQUENCE_VALUE*13)%450;
        bòrd_pel(1900,1050,0x123456); /* ath_nuadhaich 영역 밖의 cleachdaiche tarraing_VALUE */
        uint64_t 이전=bòrd_tarraing_COUNT();clock_t ruith=clock();
        tèirmineal_tomhaire(1,새가로+100,새세로+15);
        이동시간+=(double)(clock()-ruith)/CLOCKS_PER_SEC;
        gluais_LOG+=bòrd_tarraing_COUNT()-이전;
        assert(bòrd_tarraing_COUNT()-이전<=2u*폭*높이);
        assert(화면[1050][1900]==0x123456);
        bòrd_pel(1900,1050,0x302018);
        tèirmineal_tomhaire(0,새가로+100,새세로+15);가로=새가로;inghearach_suidhich=새세로;
        전체와비교();
    }
    for(int SEQUENCE_VALUE=0;SEQUENCE_VALUE<40;SEQUENCE_VALUE++){
        int 새폭=360+(SEQUENCE_VALUE*29)%700,새높이=216+(SEQUENCE_VALUE*17)%350;
        if(새폭>1920-가로)새폭=1920-가로;if(새높이>1080-inghearach_suidhich)새높이=1080-inghearach_suidhich;
        tèirmineal_tomhaire(1,가로+폭-4,inghearach_suidhich+높이-4);
        tèirmineal_tomhaire(1,가로+새폭-4,inghearach_suidhich+새높이-4);
        uint64_t 이전=bòrd_tarraing_COUNT();
        tèirmineal_tomhaire(1,가로+새폭-4,inghearach_suidhich+새높이-4);
        assert(bòrd_tarraing_COUNT()==이전); /* 같은 좌표의 중복 tachartas */
        tèirmineal_tomhaire(0,가로+새폭-4,inghearach_suidhich+새높이-4);폭=새폭;높이=새높이;
        전체와비교();
    }
    /* 잘린 범위와 dearbh_dàta loidhne 간격을 지킨다. */
    for(int loidhne=0;loidhne<1080;loidhne++)for(int slot_cur_a_steach=1920;slot_cur_a_steach<1936;slot_cur_a_steach++)assert(화면[loidhne][slot_cur_a_steach]==0);
    assert(!bòrd_Start_tarraing(0,0,1920,33));
    printf("PASS: 80 moves, 40 resizes, 4 overlapping windows; %.3f ms/move; %llu framebuffer writes/move\n",이동시간*1000/80,(unsigned long long)(gluais_LOG/80));
    return 0;
}
