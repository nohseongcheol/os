#include "../명명/기계연결이름.h"
#include "../mīhini/화면정보.h"
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>
void 커널중단(const char *설명){fputs(설명,stderr);abort();}
extern uintptr_t papa_Tauranga(uintptr_t),papa_pika(uintptr_t,uintptr_t,uintptr_t);
extern void Tauranga_atatohu(unsigned,int,int),Tauranga_paita(unsigned);
extern int 화면호출(int,unsigned,int,int,int,int,int);
static uint32_t 화면[1080][1936],비교그림[1080][1936];
uintptr_t 보드화면기억공간(void){return 1;}
static void 전체와비교(void){
    papa_atatohu(0,0,0);memcpy(비교그림,화면,sizeof(화면));
    uint64_t 이전=papa_tātuhi_COUNT();papa_Tauranga(3);
    assert(memcmp(비교그림,화면,sizeof(화면))==0);
    assert(papa_tātuhi_COUNT()==이전); /* 같은 화면을 다시 그려도 whakaatu_uara 메모리에 쓰지 않는다. */
}
static void tuhi_TEXT(const char *Ngā_kupu){while(*Ngā_kupu)Tauranga_paita((unsigned char)*Ngā_kupu++);}
int main(void){
    papa_Whakarite_tātuhi(&화면[0][0],1920,1080,sizeof(화면[0]));
    papa_Tauranga(300);tuhi_TEXT("첫 창의 한글 raraunga\n");
    for(int INDEX=1;INDEX<4;INDEX++){papa_Tauranga(1);papa_Tauranga(100+INDEX);tuhi_TEXT("겹친 창의 한글 raraunga\n\033[41m색칠한 빈칸     \033[0m\n");}
    전체와비교();
    int 가로=60,Poutū_tūranga=102,폭=568,높이=360;
    uint64_t nuku_LOG=0;double 이동시간=0;
    for(int SEQUENCE_uara=0;SEQUENCE_uara<80;SEQUENCE_uara++){
        Tauranga_atatohu(1,가로+100,Poutū_tūranga+15);
        int 새가로=80+(SEQUENCE_uara*37)%850,새세로=50+(SEQUENCE_uara*13)%450;
        papa_pika(1900,1050,0x123456); /* tāmata 영역 밖의 kaiwhakamahi tātuhi_uara */
        uint64_t 이전=papa_tātuhi_COUNT();clock_t whakahaere=clock();
        Tauranga_atatohu(1,새가로+100,새세로+15);
        이동시간+=(double)(clock()-whakahaere)/CLOCKS_PER_SEC;
        nuku_LOG+=papa_tātuhi_COUNT()-이전;
        assert(papa_tātuhi_COUNT()-이전<=2u*폭*높이);
        assert(화면[1050][1900]==0x123456);
        papa_pika(1900,1050,0x302018);
        Tauranga_atatohu(0,새가로+100,새세로+15);가로=새가로;Poutū_tūranga=새세로;
        전체와비교();
    }
    for(int SEQUENCE_uara=0;SEQUENCE_uara<40;SEQUENCE_uara++){
        int 새폭=360+(SEQUENCE_uara*29)%700,새높이=216+(SEQUENCE_uara*17)%350;
        if(새폭>1920-가로)새폭=1920-가로;if(새높이>1080-Poutū_tūranga)새높이=1080-Poutū_tūranga;
        Tauranga_atatohu(1,가로+폭-4,Poutū_tūranga+높이-4);
        Tauranga_atatohu(1,가로+새폭-4,Poutū_tūranga+새높이-4);
        uint64_t 이전=papa_tātuhi_COUNT();
        Tauranga_atatohu(1,가로+새폭-4,Poutū_tūranga+새높이-4);
        assert(papa_tātuhi_COUNT()==이전); /* 같은 좌표의 중복 hui */
        Tauranga_atatohu(0,가로+새폭-4,Poutū_tūranga+새높이-4);폭=새폭;높이=새높이;
        전체와비교();
    }
    /* 잘린 범위와 tūturu_raraunga hononga 간격을 지킨다. */
    for(int hononga=0;hononga<1080;hononga++)for(int kāniwha_tāurunga=1920;kāniwha_tāurunga<1936;kāniwha_tāurunga++)assert(화면[hononga][kāniwha_tāurunga]==0);
    assert(!papa_Start_tātuhi(0,0,1920,33));
    printf("PASS: 80 moves, 40 resizes, 4 overlapping windows; %.3f ms/move; %llu framebuffer writes/move\n",이동시간*1000/80,(unsigned long long)(nuku_LOG/80));
    return 0;
}
