#include "../명명/기계연결이름.h"
#include "../maşın/화면정보.h"
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>
void 커널중단(const char *설명){fputs(설명,stderr);abort();}
extern uintptr_t lövhə_Terminal(uintptr_t),lövhə_piksel(uintptr_t,uintptr_t,uintptr_t);
extern void Terminal_göstərici(unsigned,int,int),Terminal_bayt(unsigned);
extern int 화면호출(int,unsigned,int,int,int,int,int);
static uint32_t 화면[1080][1936],Müqayisə_IMAGE[1080][1936];
uintptr_t 보드화면기억공간(void){return 1;}
static void 전체와비교(void){
    lövhə_göstərici(0,0,0);memcpy(Müqayisə_IMAGE,화면,sizeof(화면));
    uint64_t 이전=lövhə_rəsm_COUNT();lövhə_Terminal(3);
    assert(memcmp(Müqayisə_IMAGE,화면,sizeof(화면))==0);
    assert(lövhə_rəsm_COUNT()==이전); /* 같은 화면을 다시 그려도 göstərmək_VALUE 메모리에 쓰지 않는다. */
}
static void yazmaq_SMS(const char *Mətn){while(*Mətn)Terminal_bayt((unsigned char)*Mətn++);}
int main(void){
    lövhə_Hazırla_rəsm(&화면[0][0],1920,1080,sizeof(화면[0]));
    lövhə_Terminal(300);yazmaq_SMS("첫 창의 한글 verilənlər\n");
    for(int INDEX=1;INDEX<4;INDEX++){lövhə_Terminal(1);lövhə_Terminal(100+INDEX);yazmaq_SMS("겹친 창의 한글 verilənlər\n\033[41m색칠한 빈칸     \033[0m\n");}
    전체와비교();
    int 가로=60,Şaquli_yerinə_qoymaq=102,폭=568,높이=360;
    uint64_t hərəkət_etdir_LOG=0;double 이동시간=0;
    for(int SEQUENCE_VALUE=0;SEQUENCE_VALUE<80;SEQUENCE_VALUE++){
        Terminal_göstərici(1,가로+100,Şaquli_yerinə_qoymaq+15);
        int 새가로=80+(SEQUENCE_VALUE*37)%850,새세로=50+(SEQUENCE_VALUE*13)%450;
        lövhə_piksel(1900,1050,0x123456); /* təzələmək 영역 밖의 istifadəçi rəsm_VALUE */
        uint64_t 이전=lövhə_rəsm_COUNT();clock_t İcra_Et=clock();
        Terminal_göstərici(1,새가로+100,새세로+15);
        이동시간+=(double)(clock()-İcra_Et)/CLOCKS_PER_SEC;
        hərəkət_etdir_LOG+=lövhə_rəsm_COUNT()-이전;
        assert(lövhə_rəsm_COUNT()-이전<=2u*폭*높이);
        assert(화면[1050][1900]==0x123456);
        lövhə_piksel(1900,1050,0x302018);
        Terminal_göstərici(0,새가로+100,새세로+15);가로=새가로;Şaquli_yerinə_qoymaq=새세로;
        전체와비교();
    }
    for(int SEQUENCE_VALUE=0;SEQUENCE_VALUE<40;SEQUENCE_VALUE++){
        int 새폭=360+(SEQUENCE_VALUE*29)%700,새높이=216+(SEQUENCE_VALUE*17)%350;
        if(새폭>1920-가로)새폭=1920-가로;if(새높이>1080-Şaquli_yerinə_qoymaq)새높이=1080-Şaquli_yerinə_qoymaq;
        Terminal_göstərici(1,가로+폭-4,Şaquli_yerinə_qoymaq+높이-4);
        Terminal_göstərici(1,가로+새폭-4,Şaquli_yerinə_qoymaq+새높이-4);
        uint64_t 이전=lövhə_rəsm_COUNT();
        Terminal_göstərici(1,가로+새폭-4,Şaquli_yerinə_qoymaq+새높이-4);
        assert(lövhə_rəsm_COUNT()==이전); /* 같은 좌표의 중복 hadisə */
        Terminal_göstərici(0,가로+새폭-4,Şaquli_yerinə_qoymaq+새높이-4);폭=새폭;높이=새높이;
        전체와비교();
    }
    /* 잘린 범위와 faktiki_verilənlər Giriş 간격을 지킨다. */
    for(int Giriş=0;Giriş<1080;Giriş++)for(int slot_daxiletmə=1920;slot_daxiletmə<1936;slot_daxiletmə++)assert(화면[Giriş][slot_daxiletmə]==0);
    assert(!lövhə_Başla_rəsm(0,0,1920,33));
    printf("PASS: 80 moves, 40 resizes, 4 overlapping windows; %.3f ms/move; %llu framebuffer writes/move\n",이동시간*1000/80,(unsigned long long)(hərəkət_etdir_LOG/80));
    return 0;
}
