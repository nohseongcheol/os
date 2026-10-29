#include "../명명/기계연결이름.h"
#include "../mesin/화면정보.h"
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>
void 커널중단(const char *설명){fputs(설명,stderr);abort();}
extern uintptr_t Papan_Terminal(uintptr_t),Papan_pel(uintptr_t,uintptr_t,uintptr_t);
extern void Terminal_penuding(unsigned,int,int),Terminal_bait(unsigned);
extern int 화면호출(int,unsigned,int,int,int,int,int);
static uint32_t 화면[1080][1936],Perbandingan_imej[1080][1936];
uintptr_t 보드화면기억공간(void){return 1;}
static void 전체와비교(void){
    Papan_penuding(0,0,0);memcpy(Perbandingan_imej,화면,sizeof(화면));
    uint64_t 이전=Papan_lukisan_COUNT();Papan_Terminal(3);
    assert(memcmp(Perbandingan_imej,화면,sizeof(화면))==0);
    assert(Papan_lukisan_COUNT()==이전); /* 같은 화면을 다시 그려도 tayang_VALUE 메모리에 쓰지 않는다. */
}
static void tulis_SMS(const char *Teks){while(*Teks)Terminal_bait((unsigned char)*Teks++);}
int main(void){
    Papan_Sediakan_lukisan(&화면[0][0],1920,1080,sizeof(화면[0]));
    Papan_Terminal(300);tulis_SMS("첫 창의 한글 data\n");
    for(int INDEX=1;INDEX<4;INDEX++){Papan_Terminal(1);Papan_Terminal(100+INDEX);tulis_SMS("겹친 창의 한글 data\n\033[41m색칠한 빈칸     \033[0m\n");}
    전체와비교();
    int 가로=60,Menegak_jawatan=102,폭=568,높이=360;
    uint64_t alih_LOG=0;double 이동시간=0;
    for(int jujukan_VALUE=0;jujukan_VALUE<80;jujukan_VALUE++){
        Terminal_penuding(1,가로+100,Menegak_jawatan+15);
        int 새가로=80+(jujukan_VALUE*37)%850,새세로=50+(jujukan_VALUE*13)%450;
        Papan_pel(1900,1050,0x123456); /* segar_semula rantau_VALUE 밖의 ruang_pengguna lukisan_VALUE */
        uint64_t 이전=Papan_lukisan_COUNT();clock_t Jalan=clock();
        Terminal_penuding(1,새가로+100,새세로+15);
        이동시간+=(double)(clock()-Jalan)/CLOCKS_PER_SEC;
        alih_LOG+=Papan_lukisan_COUNT()-이전;
        assert(Papan_lukisan_COUNT()-이전<=2u*폭*높이);
        assert(화면[1050][1900]==0x123456);
        Papan_pel(1900,1050,0x302018);
        Terminal_penuding(0,새가로+100,새세로+15);가로=새가로;Menegak_jawatan=새세로;
        전체와비교();
    }
    for(int jujukan_VALUE=0;jujukan_VALUE<40;jujukan_VALUE++){
        int 새폭=360+(jujukan_VALUE*29)%700,새높이=216+(jujukan_VALUE*17)%350;
        if(새폭>1920-가로)새폭=1920-가로;if(새높이>1080-Menegak_jawatan)새높이=1080-Menegak_jawatan;
        Terminal_penuding(1,가로+폭-4,Menegak_jawatan+높이-4);
        Terminal_penuding(1,가로+새폭-4,Menegak_jawatan+새높이-4);
        uint64_t 이전=Papan_lukisan_COUNT();
        Terminal_penuding(1,가로+새폭-4,Menegak_jawatan+새높이-4);
        assert(Papan_lukisan_COUNT()==이전); /* 같은 좌표의 중복 Peristiwa */
        Terminal_penuding(0,가로+새폭-4,Menegak_jawatan+새높이-4);폭=새폭;높이=새높이;
        전체와비교();
    }
    /* 잘린 범위와 sebenar_data baris 간격을 지킨다. */
    for(int baris=0;baris<1080;baris++)for(int 칸=1920;칸<1936;칸++)assert(화면[baris][칸]==0);
    assert(!Papan_Mula_lukisan(0,0,1920,33));
    printf("PASS: 80 moves, 40 resizes, 4 overlapping windows; %.3f ms/move; %llu framebuffer writes/move\n",이동시간*1000/80,(unsigned long long)(alih_LOG/80));
    return 0;
}
