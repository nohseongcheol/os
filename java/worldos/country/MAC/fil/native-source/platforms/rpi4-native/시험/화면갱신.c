#include "../명명/기계연결이름.h"
#include "../machine/화면정보.h"
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>
void 커널중단(const char *설명){fputs(설명,stderr);abort();}
extern uintptr_t board_Terminal(uintptr_t),board_pel(uintptr_t,uintptr_t,uintptr_t);
extern void Terminal_pointer(unsigned,int,int),Terminal_byte(unsigned);
extern int 화면호출(int,unsigned,int,int,int,int,int);
static uint32_t 화면[1080][1936],Paghahambing_IMAGE[1080][1936];
uintptr_t 보드화면기억공간(void){return 1;}
static void 전체와비교(void){
    board_pointer(0,0,0);memcpy(Paghahambing_IMAGE,화면,sizeof(화면));
    uint64_t 이전=board_iginuhit_COUNT();board_Terminal(3);
    assert(memcmp(Paghahambing_IMAGE,화면,sizeof(화면))==0);
    assert(board_iginuhit_COUNT()==이전); /* 같은 화면을 다시 그려도 ipakita_VALUE 메모리에 쓰지 않는다. */
}
static void sumulat_SMS(const char *SMS){while(*SMS)Terminal_byte((unsigned char)*SMS++);}
int main(void){
    board_Ihanda_iginuhit(&화면[0][0],1920,1080,sizeof(화면[0]));
    board_Terminal(300);sumulat_SMS("첫 창의 한글 data\n");
    for(int INDEX=1;INDEX<4;INDEX++){board_Terminal(1);board_Terminal(100+INDEX);sumulat_SMS("겹친 창의 한글 data\n\033[41m색칠한 빈칸     \033[0m\n");}
    전체와비교();
    int 가로=60,archive_posisyon=102,폭=568,높이=360;
    uint64_t ilipat_LOG=0;double 이동시간=0;
    for(int SEQUENCE_VALUE=0;SEQUENCE_VALUE<80;SEQUENCE_VALUE++){
        Terminal_pointer(1,가로+100,archive_posisyon+15);
        int 새가로=80+(SEQUENCE_VALUE*37)%850,새세로=50+(SEQUENCE_VALUE*13)%450;
        board_pel(1900,1050,0x123456); /* i_refresh 영역 밖의 gumagamit iginuhit_VALUE */
        uint64_t 이전=board_iginuhit_COUNT();clock_t run=clock();
        Terminal_pointer(1,새가로+100,새세로+15);
        이동시간+=(double)(clock()-run)/CLOCKS_PER_SEC;
        ilipat_LOG+=board_iginuhit_COUNT()-이전;
        assert(board_iginuhit_COUNT()-이전<=2u*폭*높이);
        assert(화면[1050][1900]==0x123456);
        board_pel(1900,1050,0x302018);
        Terminal_pointer(0,새가로+100,새세로+15);가로=새가로;archive_posisyon=새세로;
        전체와비교();
    }
    for(int SEQUENCE_VALUE=0;SEQUENCE_VALUE<40;SEQUENCE_VALUE++){
        int 새폭=360+(SEQUENCE_VALUE*29)%700,새높이=216+(SEQUENCE_VALUE*17)%350;
        if(새폭>1920-가로)새폭=1920-가로;if(새높이>1080-archive_posisyon)새높이=1080-archive_posisyon;
        Terminal_pointer(1,가로+폭-4,archive_posisyon+높이-4);
        Terminal_pointer(1,가로+새폭-4,archive_posisyon+새높이-4);
        uint64_t 이전=board_iginuhit_COUNT();
        Terminal_pointer(1,가로+새폭-4,archive_posisyon+새높이-4);
        assert(board_iginuhit_COUNT()==이전); /* 같은 좌표의 중복 kaganapan */
        Terminal_pointer(0,가로+새폭-4,archive_posisyon+새높이-4);폭=새폭;높이=새높이;
        전체와비교();
    }
    /* 잘린 범위와 totoo_data linya 간격을 지킨다. */
    for(int linya=0;linya<1080;linya++)for(int espasyo_pagpasok=1920;espasyo_pagpasok<1936;espasyo_pagpasok++)assert(화면[linya][espasyo_pagpasok]==0);
    assert(!board_Start_iginuhit(0,0,1920,33));
    printf("PASS: 80 moves, 40 resizes, 4 overlapping windows; %.3f ms/move; %llu framebuffer writes/move\n",이동시간*1000/80,(unsigned long long)(ilipat_LOG/80));
    return 0;
}
