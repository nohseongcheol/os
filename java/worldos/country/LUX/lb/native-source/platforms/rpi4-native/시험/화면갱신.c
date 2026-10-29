#include "../명명/기계연결이름.h"
#include "../Computer/화면정보.h"
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>
void 커널중단(const char *설명){fputs(설명,stderr);abort();}
extern uintptr_t Board_Terminal(uintptr_t),Board_Pel(uintptr_t,uintptr_t,uintptr_t);
extern void Terminal_Uweiser(unsigned,int,int),Terminal_Byte(unsigned);
extern int 화면호출(int,unsigned,int,int,int,int,int);
static uint32_t 화면[1080][1936],비교그림[1080][1936];
uintptr_t 보드화면기억공간(void){return 1;}
static void 전체와비교(void){
    Board_Uweiser(0,0,0);memcpy(비교그림,화면,sizeof(화면));
    uint64_t 이전=Board_Zeechnung_COUNT();Board_Terminal(3);
    assert(memcmp(비교그림,화면,sizeof(화면))==0);
    assert(Board_Zeechnung_COUNT()==이전); /* 같은 화면을 다시 그려도 Show_VALUE 메모리에 쓰지 않는다. */
}
static void schreiwen_SMS(const char *SMS){while(*SMS)Terminal_Byte((unsigned char)*SMS++);}
int main(void){
    Board_Préparéieren_Zeechnung(&화면[0][0],1920,1080,sizeof(화면[0]));
    Board_Terminal(300);schreiwen_SMS("첫 창의 한글 Daten\n");
    for(int INDEX=1;INDEX<4;INDEX++){Board_Terminal(1);Board_Terminal(100+INDEX);schreiwen_SMS("겹친 창의 한글 Daten\n\033[41m색칠한 빈칸     \033[0m\n");}
    전체와비교();
    int 가로=60,Vertikal_positionéieren=102,폭=568,높이=360;
    uint64_t verréckelen_LOG=0;double 이동시간=0;
    for(int SEQUENCE_VALUE=0;SEQUENCE_VALUE<80;SEQUENCE_VALUE++){
        Terminal_Uweiser(1,가로+100,Vertikal_positionéieren+15);
        int 새가로=80+(SEQUENCE_VALUE*37)%850,새세로=50+(SEQUENCE_VALUE*13)%450;
        Board_Pel(1900,1050,0x123456); /* aktualiséieren 영역 밖의 Benotzer Zeechnung_VALUE */
        uint64_t 이전=Board_Zeechnung_COUNT();clock_t Laf=clock();
        Terminal_Uweiser(1,새가로+100,새세로+15);
        이동시간+=(double)(clock()-Laf)/CLOCKS_PER_SEC;
        verréckelen_LOG+=Board_Zeechnung_COUNT()-이전;
        assert(Board_Zeechnung_COUNT()-이전<=2u*폭*높이);
        assert(화면[1050][1900]==0x123456);
        Board_Pel(1900,1050,0x302018);
        Terminal_Uweiser(0,새가로+100,새세로+15);가로=새가로;Vertikal_positionéieren=새세로;
        전체와비교();
    }
    for(int SEQUENCE_VALUE=0;SEQUENCE_VALUE<40;SEQUENCE_VALUE++){
        int 새폭=360+(SEQUENCE_VALUE*29)%700,새높이=216+(SEQUENCE_VALUE*17)%350;
        if(새폭>1920-가로)새폭=1920-가로;if(새높이>1080-Vertikal_positionéieren)새높이=1080-Vertikal_positionéieren;
        Terminal_Uweiser(1,가로+폭-4,Vertikal_positionéieren+높이-4);
        Terminal_Uweiser(1,가로+새폭-4,Vertikal_positionéieren+새높이-4);
        uint64_t 이전=Board_Zeechnung_COUNT();
        Terminal_Uweiser(1,가로+새폭-4,Vertikal_positionéieren+새높이-4);
        assert(Board_Zeechnung_COUNT()==이전); /* 같은 좌표의 중복 Evenement */
        Terminal_Uweiser(0,가로+새폭-4,Vertikal_positionéieren+새높이-4);폭=새폭;높이=새높이;
        전체와비교();
    }
    /* 잘린 범위와 aktuell_Daten Zeil 간격을 지킨다. */
    for(int Zeil=0;Zeil<1080;Zeil++)for(int Slot_Agab=1920;Slot_Agab<1936;Slot_Agab++)assert(화면[Zeil][Slot_Agab]==0);
    assert(!Board_Start_Zeechnung(0,0,1920,33));
    printf("PASS: 80 moves, 40 resizes, 4 overlapping windows; %.3f ms/move; %llu framebuffer writes/move\n",이동시간*1000/80,(unsigned long long)(verréckelen_LOG/80));
    return 0;
}
