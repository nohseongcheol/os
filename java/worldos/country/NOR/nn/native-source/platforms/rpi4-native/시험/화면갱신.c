#include "../명명/기계연결이름.h"
#include "../maskin/화면정보.h"
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>
void 커널중단(const char *설명){fputs(설명,stderr);abort();}
extern uintptr_t Tavle_Terminal(uintptr_t),Tavle_piksel(uintptr_t,uintptr_t,uintptr_t);
extern void Terminal_peikar(unsigned,int,int),Terminal_byte(unsigned);
extern int 화면호출(int,unsigned,int,int,int,int,int);
static uint32_t 화면[1080][1936],Samanlikning_IMAGE[1080][1936];
uintptr_t 보드화면기억공간(void){return 1;}
static void 전체와비교(void){
    Tavle_peikar(0,0,0);memcpy(Samanlikning_IMAGE,화면,sizeof(화면));
    uint64_t 이전=Tavle_teikning_COUNT();Tavle_Terminal(3);
    assert(memcmp(Samanlikning_IMAGE,화면,sizeof(화면))==0);
    assert(Tavle_teikning_COUNT()==이전); /* 같은 화면을 다시 그려도 vise_VALUE_487749b8 메모리에 쓰지 않는다. */
}
static void skrive_SMS(const char *Tekst){while(*Tekst)Terminal_byte((unsigned char)*Tekst++);}
int main(void){
    Tavle_Klargjer_teikning(&화면[0][0],1920,1080,sizeof(화면[0]));
    Tavle_Terminal(300);skrive_SMS("첫 창의 한글 data\n");
    for(int INDEX=1;INDEX<4;INDEX++){Tavle_Terminal(1);Tavle_Terminal(100+INDEX);skrive_SMS("겹친 창의 한글 data\n\033[41m색칠한 빈칸     \033[0m\n");}
    전체와비교();
    int 가로=60,vertikalvising_plassere=102,폭=568,높이=360;
    uint64_t flytte_LOG=0;double 이동시간=0;
    for(int SEQUENCE_VALUE=0;SEQUENCE_VALUE<80;SEQUENCE_VALUE++){
        Terminal_peikar(1,가로+100,vertikalvising_plassere+15);
        int 새가로=80+(SEQUENCE_VALUE*37)%850,새세로=50+(SEQUENCE_VALUE*13)%450;
        Tavle_piksel(1900,1050,0x123456); /* oppdatere 영역 밖의 brukar teikning_VALUE */
        uint64_t 이전=Tavle_teikning_COUNT();clock_t Køyr_2=clock();
        Terminal_peikar(1,새가로+100,새세로+15);
        이동시간+=(double)(clock()-Køyr_2)/CLOCKS_PER_SEC;
        flytte_LOG+=Tavle_teikning_COUNT()-이전;
        assert(Tavle_teikning_COUNT()-이전<=2u*폭*높이);
        assert(화면[1050][1900]==0x123456);
        Tavle_piksel(1900,1050,0x302018);
        Terminal_peikar(0,새가로+100,새세로+15);가로=새가로;vertikalvising_plassere=새세로;
        전체와비교();
    }
    for(int SEQUENCE_VALUE=0;SEQUENCE_VALUE<40;SEQUENCE_VALUE++){
        int 새폭=360+(SEQUENCE_VALUE*29)%700,새높이=216+(SEQUENCE_VALUE*17)%350;
        if(새폭>1920-가로)새폭=1920-가로;if(새높이>1080-vertikalvising_plassere)새높이=1080-vertikalvising_plassere;
        Terminal_peikar(1,가로+폭-4,vertikalvising_plassere+높이-4);
        Terminal_peikar(1,가로+새폭-4,vertikalvising_plassere+새높이-4);
        uint64_t 이전=Tavle_teikning_COUNT();
        Terminal_peikar(1,가로+새폭-4,vertikalvising_plassere+새높이-4);
        assert(Tavle_teikning_COUNT()==이전); /* 같은 좌표의 중복 Hending */
        Terminal_peikar(0,가로+새폭-4,vertikalvising_plassere+새높이-4);폭=새폭;높이=새높이;
        전체와비교();
    }
    /* 잘린 범위와 faktisk_data linje 간격을 지킨다. */
    for(int linje=0;linje<1080;linje++)for(int felt_oppføring=1920;felt_oppføring<1936;felt_oppføring++)assert(화면[linje][felt_oppføring]==0);
    assert(!Tavle_START_teikning(0,0,1920,33));
    printf("PASS: 80 moves, 40 resizes, 4 overlapping windows; %.3f ms/move; %llu framebuffer writes/move\n",이동시간*1000/80,(unsigned long long)(flytte_LOG/80));
    return 0;
}
