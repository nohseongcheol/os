#include "../명명/기계연결이름.h"
#include "../기계/화면정보.h"
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>
void 커널중단(const char *설명){fputs(설명,stderr);abort();}
extern uintptr_t yozuv_taxtasi_Terminal(uintptr_t),yozuv_taxtasi_piksel(uintptr_t,uintptr_t,uintptr_t);
extern void Terminal_kursor(unsigned,int,int),Terminal_bayt(unsigned);
extern int 화면호출(int,unsigned,int,int,int,int,int);
static uint32_t 화면[1080][1936],Taqqoslama_rasm[1080][1936];
uintptr_t 보드화면기억공간(void){return 1;}
static void 전체와비교(void){
    yozuv_taxtasi_kursor(0,0,0);memcpy(Taqqoslama_rasm,화면,sizeof(화면));
    uint64_t 이전=yozuv_taxtasi_chizish_COUNT();yozuv_taxtasi_Terminal(3);
    assert(memcmp(Taqqoslama_rasm,화면,sizeof(화면))==0);
    assert(yozuv_taxtasi_chizish_COUNT()==이전); /* 같은 화면을 다시 그려도 ko_rsatmoq_VALUE 메모리에 쓰지 않는다. */
}
static void yozmoq_SMS(const char *Matn){while(*Matn)Terminal_bayt((unsigned char)*Matn++);}
int main(void){
    yozuv_taxtasi_Tayyorlamoq_chizish(&화면[0][0],1920,1080,sizeof(화면[0]));
    yozuv_taxtasi_Terminal(300);yozmoq_SMS("첫 창의 한글 ma_lumotlar\n");
    for(int INDEX=1;INDEX<4;INDEX++){yozuv_taxtasi_Terminal(1);yozuv_taxtasi_Terminal(100+INDEX);yozmoq_SMS("겹친 창의 한글 ma_lumotlar\n\033[41m색칠한 빈칸     \033[0m\n");}
    전체와비교();
    int 가로=60,Vertikal_holat=102,폭=568,높이=360;
    uint64_t ko_chirmoq_LOG=0;double 이동시간=0;
    for(int SEQUENCE_VALUE=0;SEQUENCE_VALUE<80;SEQUENCE_VALUE++){
        Terminal_kursor(1,가로+100,Vertikal_holat+15);
        int 새가로=80+(SEQUENCE_VALUE*37)%850,새세로=50+(SEQUENCE_VALUE*13)%450;
        yozuv_taxtasi_piksel(1900,1050,0x123456); /* yangilamoq 영역 밖의 foydalanuvchi chizish_VALUE */
        uint64_t 이전=yozuv_taxtasi_chizish_COUNT();clock_t Bajarish=clock();
        Terminal_kursor(1,새가로+100,새세로+15);
        이동시간+=(double)(clock()-Bajarish)/CLOCKS_PER_SEC;
        ko_chirmoq_LOG+=yozuv_taxtasi_chizish_COUNT()-이전;
        assert(yozuv_taxtasi_chizish_COUNT()-이전<=2u*폭*높이);
        assert(화면[1050][1900]==0x123456);
        yozuv_taxtasi_piksel(1900,1050,0x302018);
        Terminal_kursor(0,새가로+100,새세로+15);가로=새가로;Vertikal_holat=새세로;
        전체와비교();
    }
    for(int SEQUENCE_VALUE=0;SEQUENCE_VALUE<40;SEQUENCE_VALUE++){
        int 새폭=360+(SEQUENCE_VALUE*29)%700,새높이=216+(SEQUENCE_VALUE*17)%350;
        if(새폭>1920-가로)새폭=1920-가로;if(새높이>1080-Vertikal_holat)새높이=1080-Vertikal_holat;
        Terminal_kursor(1,가로+폭-4,Vertikal_holat+높이-4);
        Terminal_kursor(1,가로+새폭-4,Vertikal_holat+새높이-4);
        uint64_t 이전=yozuv_taxtasi_chizish_COUNT();
        Terminal_kursor(1,가로+새폭-4,Vertikal_holat+새높이-4);
        assert(yozuv_taxtasi_chizish_COUNT()==이전); /* 같은 좌표의 중복 hodisa */
        Terminal_kursor(0,가로+새폭-4,Vertikal_holat+새높이-4);폭=새폭;높이=새높이;
        전체와비교();
    }
    /* 잘린 범위와 real_ma_lumotlar satr 간격을 지킨다. */
    for(int satr=0;satr<1080;satr++)for(int in_kiritish=1920;in_kiritish<1936;in_kiritish++)assert(화면[satr][in_kiritish]==0);
    assert(!yozuv_taxtasi_Start_chizish(0,0,1920,33));
    printf("PASS: 80 moves, 40 resizes, 4 overlapping windows; %.3f ms/move; %llu framebuffer writes/move\n",이동시간*1000/80,(unsigned long long)(ko_chirmoq_LOG/80));
    return 0;
}
