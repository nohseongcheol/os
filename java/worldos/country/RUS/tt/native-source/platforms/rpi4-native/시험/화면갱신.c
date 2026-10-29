#include "../명명/기계연결이름.h"
#include "../машина/화면정보.h"
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>
void 커널중단(const char *설명){fputs(설명,stderr);abort();}
extern uintptr_t такта_Терминал(uintptr_t),такта_нокта(uintptr_t,uintptr_t,uintptr_t);
extern void Терминал_күрсәткеч(unsigned,int,int),Терминал_байт(unsigned);
extern int 화면호출(int,unsigned,int,int,int,int,int);
static uint32_t 화면[1080][1936],비교그림[1080][1936];
uintptr_t 보드화면기억공간(void){return 1;}
static void 전체와비교(void){
    такта_күрсәткеч(0,0,0);memcpy(비교그림,화면,sizeof(화면));
    uint64_t 이전=такта_сызым_COUNT();такта_Терминал(3);
    assert(memcmp(비교그림,화면,sizeof(화면))==0);
    assert(такта_сызым_COUNT()==이전); /* 같은 화면을 다시 그려도 күрсәтү_VALUE 메모리에 쓰지 않는다. */
}
static void язу_СМС(const char *Mäten){while(*Mäten)Терминал_байт((unsigned char)*Mäten++);}
int main(void){
    такта_Әзерләү_сызым(&화면[0][0],1920,1080,sizeof(화면[0]));
    такта_Терминал(300);язу_СМС("첫 창의 한글 мәгълүмат\n");
    for(int INDEX=1;INDEX<4;INDEX++){такта_Терминал(1);такта_Терминал(100+INDEX);язу_СМС("겹친 창의 한글 мәгълүмат\n\033[41m색칠한 빈칸     \033[0m\n");}
    전체와비교();
    int 가로=60,Вертикаль_урнаштыру=102,폭=568,높이=360;
    uint64_t күчерү_LOG=0;double 이동시간=0;
    for(int SEQUENCE_VALUE=0;SEQUENCE_VALUE<80;SEQUENCE_VALUE++){
        Терминал_күрсәткеч(1,가로+100,Вертикаль_урнаштыру+15);
        int 새가로=80+(SEQUENCE_VALUE*37)%850,새세로=50+(SEQUENCE_VALUE*13)%450;
        такта_нокта(1900,1050,0x123456); /* яңарту 영역 밖의 кулланучы сызым_VALUE */
        uint64_t 이전=такта_сызым_COUNT();clock_t эшләтү=clock();
        Терминал_күрсәткеч(1,새가로+100,새세로+15);
        이동시간+=(double)(clock()-эшләтү)/CLOCKS_PER_SEC;
        күчерү_LOG+=такта_сызым_COUNT()-이전;
        assert(такта_сызым_COUNT()-이전<=2u*폭*높이);
        assert(화면[1050][1900]==0x123456);
        такта_нокта(1900,1050,0x302018);
        Терминал_күрсәткеч(0,새가로+100,새세로+15);가로=새가로;Вертикаль_урнаштыру=새세로;
        전체와비교();
    }
    for(int SEQUENCE_VALUE=0;SEQUENCE_VALUE<40;SEQUENCE_VALUE++){
        int 새폭=360+(SEQUENCE_VALUE*29)%700,새높이=216+(SEQUENCE_VALUE*17)%350;
        if(새폭>1920-가로)새폭=1920-가로;if(새높이>1080-Вертикаль_урнаштыру)새높이=1080-Вертикаль_урнаштыру;
        Терминал_күрсәткеч(1,가로+폭-4,Вертикаль_урнаштыру+높이-4);
        Терминал_күрсәткеч(1,가로+새폭-4,Вертикаль_урнаштыру+새높이-4);
        uint64_t 이전=такта_сызым_COUNT();
        Терминал_күрсәткеч(1,가로+새폭-4,Вертикаль_урнаштыру+새높이-4);
        assert(такта_сызым_COUNT()==이전); /* 같은 좌표의 중복 вакыйга */
        Терминал_күрсәткеч(0,가로+새폭-4,Вертикаль_урнаштыру+새높이-4);폭=새폭;높이=새높이;
        전체와비교();
    }
    /* 잘린 범위와 фактик_мәгълүмат юл 간격을 지킨다. */
    for(int юл=0;юл<1080;юл++)for(int оя_кертү=1920;оя_кертү<1936;оя_кертү++)assert(화면[юл][оя_кертү]==0);
    assert(!такта_Start_сызым(0,0,1920,33));
    printf("PASS: 80 moves, 40 resizes, 4 overlapping windows; %.3f ms/move; %llu framebuffer writes/move\n",이동시간*1000/80,(unsigned long long)(күчерү_LOG/80));
    return 0;
}
