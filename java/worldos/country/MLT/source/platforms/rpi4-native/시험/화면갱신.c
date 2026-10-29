#include "../명명/기계연결이름.h"
#include "../kompjuter/화면정보.h"
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>
void 커널중단(const char *설명){fputs(설명,stderr);abort();}
extern uintptr_t bord_Terminal(uintptr_t),bord_pel(uintptr_t,uintptr_t,uintptr_t);
extern void Terminal_pointer(unsigned,int,int),Terminal_byte(unsigned);
extern int 화면호출(int,unsigned,int,int,int,int,int);
static uint32_t 화면[1080][1936],비교그림[1080][1936];
uintptr_t 보드화면기억공간(void){return 1;}
static void 전체와비교(void){
    bord_pointer(0,0,0);memcpy(비교그림,화면,sizeof(화면));
    uint64_t 이전=bord_tpinġija_COUNT();bord_Terminal(3);
    assert(memcmp(비교그림,화면,sizeof(화면))==0);
    assert(bord_tpinġija_COUNT()==이전); /* 같은 화면을 다시 그려도 wera_VALUE_487749b8 메모리에 쓰지 않는다. */
}
static void kiteb_SMS(const char *SMS){while(*SMS)Terminal_byte((unsigned char)*SMS++);}
int main(void){
    bord_Ħejji_tpinġija(&화면[0][0],1920,1080,sizeof(화면[0]));
    bord_Terminal(300);kiteb_SMS("첫 창의 한글 data\n");
    for(int INDEX=1;INDEX<4;INDEX++){bord_Terminal(1);bord_Terminal(100+INDEX);kiteb_SMS("겹친 창의 한글 data\n\033[41m색칠한 빈칸     \033[0m\n");}
    전체와비교();
    int 가로=60,Vertikali_pożizzjoni=102,폭=568,높이=360;
    uint64_t mexxi_LOG=0;double 이동시간=0;
    for(int SEQUENCE_VALUE=0;SEQUENCE_VALUE<80;SEQUENCE_VALUE++){
        Terminal_pointer(1,가로+100,Vertikali_pożizzjoni+15);
        int 새가로=80+(SEQUENCE_VALUE*37)%850,새세로=50+(SEQUENCE_VALUE*13)%450;
        bord_pel(1900,1050,0x123456); /* aġġorna 영역 밖의 utent tpinġija_VALUE */
        uint64_t 이전=bord_tpinġija_COUNT();clock_t serje=clock();
        Terminal_pointer(1,새가로+100,새세로+15);
        이동시간+=(double)(clock()-serje)/CLOCKS_PER_SEC;
        mexxi_LOG+=bord_tpinġija_COUNT()-이전;
        assert(bord_tpinġija_COUNT()-이전<=2u*폭*높이);
        assert(화면[1050][1900]==0x123456);
        bord_pel(1900,1050,0x302018);
        Terminal_pointer(0,새가로+100,새세로+15);가로=새가로;Vertikali_pożizzjoni=새세로;
        전체와비교();
    }
    for(int SEQUENCE_VALUE=0;SEQUENCE_VALUE<40;SEQUENCE_VALUE++){
        int 새폭=360+(SEQUENCE_VALUE*29)%700,새높이=216+(SEQUENCE_VALUE*17)%350;
        if(새폭>1920-가로)새폭=1920-가로;if(새높이>1080-Vertikali_pożizzjoni)새높이=1080-Vertikali_pożizzjoni;
        Terminal_pointer(1,가로+폭-4,Vertikali_pożizzjoni+높이-4);
        Terminal_pointer(1,가로+새폭-4,Vertikali_pożizzjoni+새높이-4);
        uint64_t 이전=bord_tpinġija_COUNT();
        Terminal_pointer(1,가로+새폭-4,Vertikali_pożizzjoni+새높이-4);
        assert(bord_tpinġija_COUNT()==이전); /* 같은 좌표의 중복 avveniment */
        Terminal_pointer(0,가로+새폭-4,Vertikali_pożizzjoni+새높이-4);폭=새폭;높이=새높이;
        전체와비교();
    }
    /* 잘린 범위와 attwali_data linja 간격을 지킨다. */
    for(int linja=0;linja<1080;linja++)for(int slott_entrata=1920;slott_entrata<1936;slott_entrata++)assert(화면[linja][slott_entrata]==0);
    assert(!bord_Bidu_tpinġija(0,0,1920,33));
    printf("PASS: 80 moves, 40 resizes, 4 overlapping windows; %.3f ms/move; %llu framebuffer writes/move\n",이동시간*1000/80,(unsigned long long)(mexxi_LOG/80));
    return 0;
}
