#include "../명명/기계연결이름.h"
#include "../gailu/화면정보.h"
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>
void 커널중단(const char *설명){fputs(설명,stderr);abort();}
extern uintptr_t arbel_Terminal(uintptr_t),arbel_pixel(uintptr_t,uintptr_t,uintptr_t);
extern void Terminal_erakusle(unsigned,int,int),Terminal_byte(unsigned);
extern int 화면호출(int,unsigned,int,int,int,int,int);
static uint32_t 화면[1080][1936],Konparazioa_irudi[1080][1936];
uintptr_t 보드화면기억공간(void){return 1;}
static void 전체와비교(void){
    arbel_erakusle(0,0,0);memcpy(Konparazioa_irudi,화면,sizeof(화면));
    uint64_t 이전=보드그림기록수();arbel_Terminal(3);
    assert(memcmp(Konparazioa_irudi,화면,sizeof(화면))==0);
    assert(보드그림기록수()==이전); /* 같은 화면을 다시 그려도 erakutsi_balio 메모리에 쓰지 않는다. */
}
static void idatzi_SMS(const char *Testua){while(*Testua)Terminal_byte((unsigned char)*Testua++);}
int main(void){
    보드그림준비(&화면[0][0],1920,1080,sizeof(화면[0]));
    arbel_Terminal(300);idatzi_SMS("첫 창의 한글 datuak\n");
    for(int INDIZE=1;INDIZE<4;INDIZE++){arbel_Terminal(1);arbel_Terminal(100+INDIZE);idatzi_SMS("겹친 창의 한글 datuak\n\033[41m색칠한 빈칸     \033[0m\n");}
    전체와비교();
    int 가로=60,Bertikala_kargu=102,폭=568,높이=360;
    uint64_t eraman_LOG=0;double 이동시간=0;
    for(int SEKUENTZIA_balio=0;SEKUENTZIA_balio<80;SEKUENTZIA_balio++){
        Terminal_erakusle(1,가로+100,Bertikala_kargu+15);
        int 새가로=80+(SEKUENTZIA_balio*37)%850,새세로=50+(SEKUENTZIA_balio*13)%450;
        arbel_pixel(1900,1050,0x123456); /* freskatu 영역 밖의 erabiltzaile 그림 */
        uint64_t 이전=보드그림기록수();clock_t Exekutatu_2=clock();
        Terminal_erakusle(1,새가로+100,새세로+15);
        이동시간+=(double)(clock()-Exekutatu_2)/CLOCKS_PER_SEC;
        eraman_LOG+=보드그림기록수()-이전;
        assert(보드그림기록수()-이전<=2u*폭*높이);
        assert(화면[1050][1900]==0x123456);
        arbel_pixel(1900,1050,0x302018);
        Terminal_erakusle(0,새가로+100,새세로+15);가로=새가로;Bertikala_kargu=새세로;
        전체와비교();
    }
    for(int SEKUENTZIA_balio=0;SEKUENTZIA_balio<40;SEKUENTZIA_balio++){
        int 새폭=360+(SEKUENTZIA_balio*29)%700,새높이=216+(SEKUENTZIA_balio*17)%350;
        if(새폭>1920-가로)새폭=1920-가로;if(새높이>1080-Bertikala_kargu)새높이=1080-Bertikala_kargu;
        Terminal_erakusle(1,가로+폭-4,Bertikala_kargu+높이-4);
        Terminal_erakusle(1,가로+새폭-4,Bertikala_kargu+새높이-4);
        uint64_t 이전=보드그림기록수();
        Terminal_erakusle(1,가로+새폭-4,Bertikala_kargu+새높이-4);
        assert(보드그림기록수()==이전); /* 같은 좌표의 중복 Gertaera */
        Terminal_erakusle(0,가로+새폭-4,Bertikala_kargu+새높이-4);폭=새폭;높이=새높이;
        전체와비교();
    }
    /* 잘린 범위와 benetako_datuak Marra 간격을 지킨다. */
    for(int Marra=0;Marra<1080;Marra++)for(int 칸=1920;칸<1936;칸++)assert(화면[Marra][칸]==0);
    assert(!보드그림시작(0,0,1920,33));
    printf("PASS: 80 moves, 40 resizes, 4 overlapping windows; %.3f ms/move; %llu framebuffer writes/move\n",이동시간*1000/80,(unsigned long long)(eraman_LOG/80));
    return 0;
}
