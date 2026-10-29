#include "../명명/기계연결이름.h"
#include "../машина/화면정보.h"
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>
void 커널중단(const char *설명){fputs(설명,stderr);abort();}
extern uintptr_t табла_Терминал(uintptr_t),табла_пиксел(uintptr_t,uintptr_t,uintptr_t);
extern void Терминал_покажувач(unsigned,int,int),Терминал_бајт(unsigned);
extern int 화면호출(int,unsigned,int,int,int,int,int);
static uint32_t 화면[1080][1936],Споредба_IMAGE[1080][1936];
uintptr_t 보드화면기억공간(void){return 1;}
static void 전체와비교(void){
    табла_покажувач(0,0,0);memcpy(Споредба_IMAGE,화면,sizeof(화면));
    uint64_t 이전=табла_цртеж_COUNT();табла_Терминал(3);
    assert(memcmp(Споредба_IMAGE,화면,sizeof(화면))==0);
    assert(табла_цртеж_COUNT()==이전); /* 같은 화면을 다시 그려도 прикажи_VALUE 메모리에 쓰지 않는다. */
}
static void запиши_СМС(const char *Текст){while(*Текст)Терминал_бајт((unsigned char)*Текст++);}
int main(void){
    табла_Подготви_цртеж(&화면[0][0],1920,1080,sizeof(화면[0]));
    табла_Терминал(300);запиши_СМС("첫 창의 한글 податоци\n");
    for(int INDEX=1;INDEX<4;INDEX++){табла_Терминал(1);табла_Терминал(100+INDEX);запиши_СМС("겹친 창의 한글 податоци\n\033[41m색칠한 빈칸     \033[0m\n");}
    전체와비교();
    int 가로=60,вертикала_позиционирање=102,폭=568,높이=360;
    uint64_t премести_LOG=0;double 이동시간=0;
    for(int SEQUENCE_VALUE=0;SEQUENCE_VALUE<80;SEQUENCE_VALUE++){
        Терминал_покажувач(1,가로+100,вертикала_позиционирање+15);
        int 새가로=80+(SEQUENCE_VALUE*37)%850,새세로=50+(SEQUENCE_VALUE*13)%450;
        табла_пиксел(1900,1050,0x123456); /* освежи 영역 밖의 корисник цртеж_VALUE */
        uint64_t 이전=табла_цртеж_COUNT();clock_t Изврши_2=clock();
        Терминал_покажувач(1,새가로+100,새세로+15);
        이동시간+=(double)(clock()-Изврши_2)/CLOCKS_PER_SEC;
        премести_LOG+=табла_цртеж_COUNT()-이전;
        assert(табла_цртеж_COUNT()-이전<=2u*폭*높이);
        assert(화면[1050][1900]==0x123456);
        табла_пиксел(1900,1050,0x302018);
        Терминал_покажувач(0,새가로+100,새세로+15);가로=새가로;вертикала_позиционирање=새세로;
        전체와비교();
    }
    for(int SEQUENCE_VALUE=0;SEQUENCE_VALUE<40;SEQUENCE_VALUE++){
        int 새폭=360+(SEQUENCE_VALUE*29)%700,새높이=216+(SEQUENCE_VALUE*17)%350;
        if(새폭>1920-가로)새폭=1920-가로;if(새높이>1080-вертикала_позиционирање)새높이=1080-вертикала_позиционирање;
        Терминал_покажувач(1,가로+폭-4,вертикала_позиционирање+높이-4);
        Терминал_покажувач(1,가로+새폭-4,вертикала_позиционирање+새높이-4);
        uint64_t 이전=табла_цртеж_COUNT();
        Терминал_покажувач(1,가로+새폭-4,вертикала_позиционирање+새높이-4);
        assert(табла_цртеж_COUNT()==이전); /* 같은 좌표의 중복 настан */
        Терминал_покажувач(0,가로+새폭-4,вертикала_позиционирање+새높이-4);폭=새폭;높이=새높이;
        전체와비교();
    }
    /* 잘린 범위와 реален_податоци ред 간격을 지킨다. */
    for(int ред=0;ред<1080;ред++)for(int отвор_внес=1920;отвор_внес<1936;отвор_внес++)assert(화면[ред][отвор_внес]==0);
    assert(!табла_Start_цртеж(0,0,1920,33));
    printf("PASS: 80 moves, 40 resizes, 4 overlapping windows; %.3f ms/move; %llu framebuffer writes/move\n",이동시간*1000/80,(unsigned long long)(премести_LOG/80));
    return 0;
}
