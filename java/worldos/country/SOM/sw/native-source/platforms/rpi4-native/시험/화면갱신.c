#include "../명명/기계연결이름.h"
#include "../mashine/화면정보.h"
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
static uint32_t 화면[1080][1936],Kulinganisha_picha[1080][1936];
uintptr_t 보드화면기억공간(void){return 1;}
static void 전체와비교(void){
    보드포인터(0,0,0);memcpy(Kulinganisha_picha,화면,sizeof(화면));
    uint64_t 이전=보드그림기록수();보드터미널(3);
    assert(memcmp(Kulinganisha_picha,화면,sizeof(화면))==0);
    assert(보드그림기록수()==이전); /* 같은 화면을 다시 그려도 onyesha_thamani 메모리에 쓰지 않는다. */
}
static void andika_SMS(const char *SMS){while(*SMS)터미널바이트((unsigned char)*SMS++);}
int main(void){
    보드그림준비(&화면[0][0],1920,1080,sizeof(화면[0]));
    보드터미널(300);andika_SMS("첫 창의 한글 data\n");
    for(int kielezo=1;kielezo<4;kielezo++){보드터미널(1);보드터미널(100+kielezo);andika_SMS("겹친 창의 한글 data\n\033[41m색칠한 빈칸     \033[0m\n");}
    전체와비교();
    int 가로=60,세로=102,폭=568,높이=360;
    uint64_t hamisha_batli=0;double 이동시간=0;
    for(int MFUATANO_thamani=0;MFUATANO_thamani<80;MFUATANO_thamani++){
        터미널가리킴(1,가로+100,세로+15);
        int 새가로=80+(MFUATANO_thamani*37)%850,새세로=50+(MFUATANO_thamani*13)%450;
        보드화소(1900,1050,0x123456); /* onyesha_upya 영역 밖의 mtumiaji mchoro_thamani */
        uint64_t 이전=보드그림기록수();clock_t endesha=clock();
        터미널가리킴(1,새가로+100,새세로+15);
        이동시간+=(double)(clock()-endesha)/CLOCKS_PER_SEC;
        hamisha_batli+=보드그림기록수()-이전;
        assert(보드그림기록수()-이전<=2u*폭*높이);
        assert(화면[1050][1900]==0x123456);
        보드화소(1900,1050,0x302018);
        터미널가리킴(0,새가로+100,새세로+15);가로=새가로;세로=새세로;
        전체와비교();
    }
    for(int MFUATANO_thamani=0;MFUATANO_thamani<40;MFUATANO_thamani++){
        int 새폭=360+(MFUATANO_thamani*29)%700,새높이=216+(MFUATANO_thamani*17)%350;
        if(새폭>1920-가로)새폭=1920-가로;if(새높이>1080-세로)새높이=1080-세로;
        터미널가리킴(1,가로+폭-4,세로+높이-4);
        터미널가리킴(1,가로+새폭-4,세로+새높이-4);
        uint64_t 이전=보드그림기록수();
        터미널가리킴(1,가로+새폭-4,세로+새높이-4);
        assert(보드그림기록수()==이전); /* 같은 좌표의 중복 tukio */
        터미널가리킴(0,가로+새폭-4,세로+새높이-4);폭=새폭;높이=새높이;
        전체와비교();
    }
    /* 잘린 범위와 halisi_data laini 간격을 지킨다. */
    for(int laini=0;laini<1080;laini++)for(int Sloti_ingizo=1920;Sloti_ingizo<1936;Sloti_ingizo++)assert(화면[laini][Sloti_ingizo]==0);
    assert(!보드그림시작(0,0,1920,33));
    printf("PASS: 80 moves, 40 resizes, 4 overlapping windows; %.3f ms/move; %llu framebuffer writes/move\n",이동시간*1000/80,(unsigned long long)(hamisha_batli/80));
    return 0;
}
