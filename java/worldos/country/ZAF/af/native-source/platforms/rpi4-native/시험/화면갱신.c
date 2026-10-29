#include "../명명/기계연결이름.h"
#include "../masjien/화면정보.h"
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>
void 커널중단(const char *설명){fputs(설명,stderr);abort();}
extern uintptr_t bord_Terminaal(uintptr_t),bord_pieksel(uintptr_t,uintptr_t,uintptr_t);
extern void Terminaal_wyser(unsigned,int,int),Terminaal_greep(unsigned);
extern int 화면호출(int,unsigned,int,int,int,int,int);
static uint32_t 화면[1080][1936],Vergelyking_foto[1080][1936];
uintptr_t 보드화면기억공간(void){return 1;}
static void 전체와비교(void){
    bord_wyser(0,0,0);memcpy(Vergelyking_foto,화면,sizeof(화면));
    uint64_t 이전=bord_tekening_COUNT();bord_Terminaal(3);
    assert(memcmp(Vergelyking_foto,화면,sizeof(화면))==0);
    assert(bord_tekening_COUNT()==이전); /* 같은 화면을 다시 그려도 wys_VALUE 메모리에 쓰지 않는다. */
}
static void skryf_SMS(const char *Teks){while(*Teks)Terminaal_greep((unsigned char)*Teks++);}
int main(void){
    bord_Maak_gereed_tekening(&화면[0][0],1920,1080,sizeof(화면[0]));
    bord_Terminaal(300);skryf_SMS("첫 창의 한글 data\n");
    for(int INDEX=1;INDEX<4;INDEX++){bord_Terminaal(1);bord_Terminaal(100+INDEX);skryf_SMS("겹친 창의 한글 data\n\033[41m색칠한 빈칸     \033[0m\n");}
    전체와비교();
    int 가로=60,Vertikaal_plaas=102,폭=568,높이=360;
    uint64_t skuif_LOG=0;double 이동시간=0;
    for(int SEQUENCE_VALUE=0;SEQUENCE_VALUE<80;SEQUENCE_VALUE++){
        Terminaal_wyser(1,가로+100,Vertikaal_plaas+15);
        int 새가로=80+(SEQUENCE_VALUE*37)%850,새세로=50+(SEQUENCE_VALUE*13)%450;
        bord_pieksel(1900,1050,0x123456); /* verfris 영역 밖의 gebruiker tekening_VALUE */
        uint64_t 이전=bord_tekening_COUNT();clock_t Loop=clock();
        Terminaal_wyser(1,새가로+100,새세로+15);
        이동시간+=(double)(clock()-Loop)/CLOCKS_PER_SEC;
        skuif_LOG+=bord_tekening_COUNT()-이전;
        assert(bord_tekening_COUNT()-이전<=2u*폭*높이);
        assert(화면[1050][1900]==0x123456);
        bord_pieksel(1900,1050,0x302018);
        Terminaal_wyser(0,새가로+100,새세로+15);가로=새가로;Vertikaal_plaas=새세로;
        전체와비교();
    }
    for(int SEQUENCE_VALUE=0;SEQUENCE_VALUE<40;SEQUENCE_VALUE++){
        int 새폭=360+(SEQUENCE_VALUE*29)%700,새높이=216+(SEQUENCE_VALUE*17)%350;
        if(새폭>1920-가로)새폭=1920-가로;if(새높이>1080-Vertikaal_plaas)새높이=1080-Vertikaal_plaas;
        Terminaal_wyser(1,가로+폭-4,Vertikaal_plaas+높이-4);
        Terminaal_wyser(1,가로+새폭-4,Vertikaal_plaas+새높이-4);
        uint64_t 이전=bord_tekening_COUNT();
        Terminaal_wyser(1,가로+새폭-4,Vertikaal_plaas+새높이-4);
        assert(bord_tekening_COUNT()==이전); /* 같은 좌표의 중복 gebeurtenis */
        Terminaal_wyser(0,가로+새폭-4,Vertikaal_plaas+새높이-4);폭=새폭;높이=새높이;
        전체와비교();
    }
    /* 잘린 범위와 werklik_data lyn 간격을 지킨다. */
    for(int lyn=0;lyn<1080;lyn++)for(int gleuf_inskrywing=1920;gleuf_inskrywing<1936;gleuf_inskrywing++)assert(화면[lyn][gleuf_inskrywing]==0);
    assert(!bord_BEGIN_tekening(0,0,1920,33));
    printf("PASS: 80 moves, 40 resizes, 4 overlapping windows; %.3f ms/move; %llu framebuffer writes/move\n",이동시간*1000/80,(unsigned long long)(skuif_LOG/80));
    return 0;
}
