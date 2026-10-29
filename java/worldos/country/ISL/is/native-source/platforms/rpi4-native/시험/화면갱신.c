#include "../명명/기계연결이름.h"
#include "../vél/화면정보.h"
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>
void 커널중단(const char *설명){fputs(설명,stderr);abort();}
extern uintptr_t bretti_Endastöð(uintptr_t),bretti_díll(uintptr_t,uintptr_t,uintptr_t);
extern void Endastöð_bendill(unsigned,int,int),Endastöð_bæti(unsigned);
extern int 화면호출(int,unsigned,int,int,int,int,int);
static uint32_t 화면[1080][1936],Samanburður_mynd[1080][1936];
uintptr_t 보드화면기억공간(void){return 1;}
static void 전체와비교(void){
    bretti_bendill(0,0,0);memcpy(Samanburður_mynd,화면,sizeof(화면));
    uint64_t 이전=bretti_teikning_COUNT();bretti_Endastöð(3);
    assert(memcmp(Samanburður_mynd,화면,sizeof(화면))==0);
    assert(bretti_teikning_COUNT()==이전); /* 같은 화면을 다시 그려도 sýna_VALUE 메모리에 쓰지 않는다. */
}
static void skrifa_SMS(const char *Texti){while(*Texti)Endastöð_bæti((unsigned char)*Texti++);}
int main(void){
    bretti_Undirbúa_teikning(&화면[0][0],1920,1080,sizeof(화면[0]));
    bretti_Endastöð(300);skrifa_SMS("첫 창의 한글 gögn\n");
    for(int INDEX=1;INDEX<4;INDEX++){bretti_Endastöð(1);bretti_Endastöð(100+INDEX);skrifa_SMS("겹친 창의 한글 gögn\n\033[41m색칠한 빈칸     \033[0m\n");}
    전체와비교();
    int 가로=60,Lóðrétt_staða=102,폭=568,높이=360;
    uint64_t færa_LOG=0;double 이동시간=0;
    for(int SEQUENCE_VALUE=0;SEQUENCE_VALUE<80;SEQUENCE_VALUE++){
        Endastöð_bendill(1,가로+100,Lóðrétt_staða+15);
        int 새가로=80+(SEQUENCE_VALUE*37)%850,새세로=50+(SEQUENCE_VALUE*13)%450;
        bretti_díll(1900,1050,0x123456); /* uppfæra 영역 밖의 notandi teikning_VALUE */
        uint64_t 이전=bretti_teikning_COUNT();clock_t Keyra_2=clock();
        Endastöð_bendill(1,새가로+100,새세로+15);
        이동시간+=(double)(clock()-Keyra_2)/CLOCKS_PER_SEC;
        færa_LOG+=bretti_teikning_COUNT()-이전;
        assert(bretti_teikning_COUNT()-이전<=2u*폭*높이);
        assert(화면[1050][1900]==0x123456);
        bretti_díll(1900,1050,0x302018);
        Endastöð_bendill(0,새가로+100,새세로+15);가로=새가로;Lóðrétt_staða=새세로;
        전체와비교();
    }
    for(int SEQUENCE_VALUE=0;SEQUENCE_VALUE<40;SEQUENCE_VALUE++){
        int 새폭=360+(SEQUENCE_VALUE*29)%700,새높이=216+(SEQUENCE_VALUE*17)%350;
        if(새폭>1920-가로)새폭=1920-가로;if(새높이>1080-Lóðrétt_staða)새높이=1080-Lóðrétt_staða;
        Endastöð_bendill(1,가로+폭-4,Lóðrétt_staða+높이-4);
        Endastöð_bendill(1,가로+새폭-4,Lóðrétt_staða+새높이-4);
        uint64_t 이전=bretti_teikning_COUNT();
        Endastöð_bendill(1,가로+새폭-4,Lóðrétt_staða+새높이-4);
        assert(bretti_teikning_COUNT()==이전); /* 같은 좌표의 중복 atvik */
        Endastöð_bendill(0,가로+새폭-4,Lóðrétt_staða+새높이-4);폭=새폭;높이=새높이;
        전체와비교();
    }
    /* 잘린 범위와 raun_gögn Lína 간격을 지킨다. */
    for(int Lína=0;Lína<1080;Lína++)for(int rauf_færsla=1920;rauf_færsla<1936;rauf_færsla++)assert(화면[Lína][rauf_færsla]==0);
    assert(!bretti_Opna_teikning(0,0,1920,33));
    printf("PASS: 80 moves, 40 resizes, 4 overlapping windows; %.3f ms/move; %llu framebuffer writes/move\n",이동시간*1000/80,(unsigned long long)(færa_LOG/80));
    return 0;
}
