#include "../명명/기계연결이름.h"
#include "../peiriant/화면정보.h"
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>
void 커널중단(const char *설명){fputs(설명,stderr);abort();}
extern uintptr_t bwrdd_Terfynell(uintptr_t),bwrdd_pel(uintptr_t,uintptr_t,uintptr_t);
extern void Terfynell_pwyntydd(unsigned,int,int),Terfynell_beit(unsigned);
extern int 화면호출(int,unsigned,int,int,int,int,int);
static uint32_t 화면[1080][1936],비교그림[1080][1936];
uintptr_t 보드화면기억공간(void){return 1;}
static void 전체와비교(void){
    bwrdd_pwyntydd(0,0,0);memcpy(비교그림,화면,sizeof(화면));
    uint64_t 이전=bwrdd_lluniad_COUNT();bwrdd_Terfynell(3);
    assert(memcmp(비교그림,화면,sizeof(화면))==0);
    assert(bwrdd_lluniad_COUNT()==이전); /* 같은 화면을 다시 그려도 sioe_VALUE 메모리에 쓰지 않는다. */
}
static void ysgrifennu_SMS(const char *Testun){while(*Testun)Terfynell_beit((unsigned char)*Testun++);}
int main(void){
    bwrdd_Paratoi_lluniad(&화면[0][0],1920,1080,sizeof(화면[0]));
    bwrdd_Terfynell(300);ysgrifennu_SMS("첫 창의 한글 data\n");
    for(int INDEX=1;INDEX<4;INDEX++){bwrdd_Terfynell(1);bwrdd_Terfynell(100+INDEX);ysgrifennu_SMS("겹친 창의 한글 data\n\033[41m색칠한 빈칸     \033[0m\n");}
    전체와비교();
    int 가로=60,Ar_i_fyny_safle=102,폭=568,높이=360;
    uint64_t symud_LOG=0;double 이동시간=0;
    for(int SEQUENCE_VALUE=0;SEQUENCE_VALUE<80;SEQUENCE_VALUE++){
        Terfynell_pwyntydd(1,가로+100,Ar_i_fyny_safle+15);
        int 새가로=80+(SEQUENCE_VALUE*37)%850,새세로=50+(SEQUENCE_VALUE*13)%450;
        bwrdd_pel(1900,1050,0x123456); /* adnewyddu 영역 밖의 defnyddiwr lluniad_VALUE */
        uint64_t 이전=bwrdd_lluniad_COUNT();clock_t Gweithredu_2=clock();
        Terfynell_pwyntydd(1,새가로+100,새세로+15);
        이동시간+=(double)(clock()-Gweithredu_2)/CLOCKS_PER_SEC;
        symud_LOG+=bwrdd_lluniad_COUNT()-이전;
        assert(bwrdd_lluniad_COUNT()-이전<=2u*폭*높이);
        assert(화면[1050][1900]==0x123456);
        bwrdd_pel(1900,1050,0x302018);
        Terfynell_pwyntydd(0,새가로+100,새세로+15);가로=새가로;Ar_i_fyny_safle=새세로;
        전체와비교();
    }
    for(int SEQUENCE_VALUE=0;SEQUENCE_VALUE<40;SEQUENCE_VALUE++){
        int 새폭=360+(SEQUENCE_VALUE*29)%700,새높이=216+(SEQUENCE_VALUE*17)%350;
        if(새폭>1920-가로)새폭=1920-가로;if(새높이>1080-Ar_i_fyny_safle)새높이=1080-Ar_i_fyny_safle;
        Terfynell_pwyntydd(1,가로+폭-4,Ar_i_fyny_safle+높이-4);
        Terfynell_pwyntydd(1,가로+새폭-4,Ar_i_fyny_safle+새높이-4);
        uint64_t 이전=bwrdd_lluniad_COUNT();
        Terfynell_pwyntydd(1,가로+새폭-4,Ar_i_fyny_safle+새높이-4);
        assert(bwrdd_lluniad_COUNT()==이전); /* 같은 좌표의 중복 digwyddiad */
        Terfynell_pwyntydd(0,가로+새폭-4,Ar_i_fyny_safle+새높이-4);폭=새폭;높이=새높이;
        전체와비교();
    }
    /* 잘린 범위와 go_iawn_data llinell 간격을 지킨다. */
    for(int llinell=0;llinell<1080;llinell++)for(int slot_cofnod=1920;slot_cofnod<1936;slot_cofnod++)assert(화면[llinell][slot_cofnod]==0);
    assert(!bwrdd_START_lluniad(0,0,1920,33));
    printf("PASS: 80 moves, 40 resizes, 4 overlapping windows; %.3f ms/move; %llu framebuffer writes/move\n",이동시간*1000/80,(unsigned long long)(symud_LOG/80));
    return 0;
}
