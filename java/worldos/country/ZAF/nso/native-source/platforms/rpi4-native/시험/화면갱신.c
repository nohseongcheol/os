#include "../명명/기계연결이름.h"
#include "../motšhene/화면정보.h"
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>
void 커널중단(const char *설명){fputs(설명,stderr);abort();}
extern uintptr_t 보드터미널(uintptr_t),보드화소(uintptr_t,uintptr_t,uintptr_t);
extern void 터미널가리킴(unsigned,int,int),터미널바이트(unsigned);
extern int 화면호출(int,unsigned,int,int,int,int,int);
static uint32_t 화면[1080][1936],비교그림[1080][1936];
uintptr_t 보드화면기억공간(void){return 1;}
static void 전체와비교(void){
    보드포인터(0,0,0);memcpy(비교그림,화면,sizeof(화면));
    uint64_t 이전=보드그림기록수();보드터미널(3);
    assert(memcmp(비교그림,화면,sizeof(화면))==0);
    assert(보드그림기록수()==이전); /* 같은 화면을 다시 그려도 bontšha_boleng 메모리에 쓰지 않는다. */
}
static void ngwala_SMS(const char *Sengwalwa){while(*Sengwalwa)터미널바이트((unsigned char)*Sengwalwa++);}
int main(void){
    보드그림준비(&화면[0][0],1920,1080,sizeof(화면[0]));
    보드터미널(300);ngwala_SMS("첫 창의 한글 data\n");
    for(int lokela=1;lokela<4;lokela++){보드터미널(1);보드터미널(100+lokela);ngwala_SMS("겹친 창의 한글 data\n\033[41m색칠한 빈칸     \033[0m\n");}
    전체와비교();
    int 가로=60,세로=102,폭=568,높이=360;
    uint64_t šuthiša_pego=0;double 이동시간=0;
    for(int TATELANO_boleng=0;TATELANO_boleng<80;TATELANO_boleng++){
        터미널가리킴(1,가로+100,세로+15);
        int 새가로=80+(TATELANO_boleng*37)%850,새세로=50+(TATELANO_boleng*13)%450;
        보드화소(1900,1050,0x123456); /* mpshafatša 영역 밖의 mošomiši sethalwa_boleng */
        uint64_t 이전=보드그림기록수();clock_t Diriša=clock();
        터미널가리킴(1,새가로+100,새세로+15);
        이동시간+=(double)(clock()-Diriša)/CLOCKS_PER_SEC;
        šuthiša_pego+=보드그림기록수()-이전;
        assert(보드그림기록수()-이전<=2u*폭*높이);
        assert(화면[1050][1900]==0x123456);
        보드화소(1900,1050,0x302018);
        터미널가리킴(0,새가로+100,새세로+15);가로=새가로;세로=새세로;
        전체와비교();
    }
    for(int TATELANO_boleng=0;TATELANO_boleng<40;TATELANO_boleng++){
        int 새폭=360+(TATELANO_boleng*29)%700,새높이=216+(TATELANO_boleng*17)%350;
        if(새폭>1920-가로)새폭=1920-가로;if(새높이>1080-세로)새높이=1080-세로;
        터미널가리킴(1,가로+폭-4,세로+높이-4);
        터미널가리킴(1,가로+새폭-4,세로+새높이-4);
        uint64_t 이전=보드그림기록수();
        터미널가리킴(1,가로+새폭-4,세로+새높이-4);
        assert(보드그림기록수()==이전); /* 같은 좌표의 중복 tiragalo */
        터미널가리킴(0,가로+새폭-4,세로+새높이-4);폭=새폭;높이=새높이;
        전체와비교();
    }
    /* 잘린 범위와 kgonthe_data mothaladi 간격을 지킨다. */
    for(int mothaladi=0;mothaladi<1080;mothaladi++)for(int sekgobana_go_tsenya_tshedimošo=1920;sekgobana_go_tsenya_tshedimošo<1936;sekgobana_go_tsenya_tshedimošo++)assert(화면[mothaladi][sekgobana_go_tsenya_tshedimošo]==0);
    assert(!보드그림시작(0,0,1920,33));
    printf("PASS: 80 moves, 40 resizes, 4 overlapping windows; %.3f ms/move; %llu framebuffer writes/move\n",이동시간*1000/80,(unsigned long long)(šuthiša_pego/80));
    return 0;
}
