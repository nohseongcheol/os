#include "../명명/기계연결이름.h"
#include "../mesin/화면정보.h"
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>
void 커널중단(const char *설명){fputs(설명,stderr);abort();}
extern uintptr_t Papan_Terminal(uintptr_t),Papan_elgam(uintptr_t,uintptr_t,uintptr_t);
extern void Terminal_pointer(unsigned,int,int),Terminal_byte(unsigned);
extern int 화면호출(int,unsigned,int,int,int,int,int);
static uint32_t 화면[1080][1936],Perbandingan_foto[1080][1936];
uintptr_t 보드화면기억공간(void){return 1;}
static void 전체와비교(void){
    Papan_pointer(0,0,0);memcpy(Perbandingan_foto,화면,sizeof(화면));
    uint64_t 이전=Papan_gambar_COUNT();Papan_Terminal(3);
    assert(memcmp(Perbandingan_foto,화면,sizeof(화면))==0);
    assert(Papan_gambar_COUNT()==이전); /* 같은 화면을 coba_lagi_VALUE 그려도 show_VALUE 메모리에 쓰지 않는다. */
}
static void tulis_SMS(const char *teks){while(*teks)Terminal_byte((unsigned char)*teks++);}
int main(void){
    Papan_Siapkan_gambar(&화면[0][0],1920,1080,sizeof(화면[0]));
    Papan_Terminal(300);tulis_SMS("첫 창의 한글 data\n");
    for(int INDEX=1;INDEX<4;INDEX++){Papan_Terminal(1);Papan_Terminal(100+INDEX);tulis_SMS("겹친 창의 한글 data\n\033[41m색칠한 빈칸     \033[0m\n");}
    전체와비교();
    int 가로=60,Vertikal_posisi=102,폭=568,높이=360;
    uint64_t gerak_LOG=0;double 이동시간=0;
    for(int urutan_VALUE_e9fa7815=0;urutan_VALUE_e9fa7815<80;urutan_VALUE_e9fa7815++){
        Terminal_pointer(1,가로+100,Vertikal_posisi+15);
        int 새가로=80+(urutan_VALUE_e9fa7815*37)%850,새세로=50+(urutan_VALUE_e9fa7815*13)%450;
        Papan_elgam(1900,1050,0x123456); /* refresh wilayah_VALUE 밖의 ruang_pengguna gambar_VALUE */
        uint64_t 이전=Papan_gambar_COUNT();clock_t jalankan=clock();
        Terminal_pointer(1,새가로+100,새세로+15);
        이동시간+=(double)(clock()-jalankan)/CLOCKS_PER_SEC;
        gerak_LOG+=Papan_gambar_COUNT()-이전;
        assert(Papan_gambar_COUNT()-이전<=2u*폭*높이);
        assert(화면[1050][1900]==0x123456);
        Papan_elgam(1900,1050,0x302018);
        Terminal_pointer(0,새가로+100,새세로+15);가로=새가로;Vertikal_posisi=새세로;
        전체와비교();
    }
    for(int urutan_VALUE_e9fa7815=0;urutan_VALUE_e9fa7815<40;urutan_VALUE_e9fa7815++){
        int 새폭=360+(urutan_VALUE_e9fa7815*29)%700,새높이=216+(urutan_VALUE_e9fa7815*17)%350;
        if(새폭>1920-가로)새폭=1920-가로;if(새높이>1080-Vertikal_posisi)새높이=1080-Vertikal_posisi;
        Terminal_pointer(1,가로+폭-4,Vertikal_posisi+높이-4);
        Terminal_pointer(1,가로+새폭-4,Vertikal_posisi+새높이-4);
        uint64_t 이전=Papan_gambar_COUNT();
        Terminal_pointer(1,가로+새폭-4,Vertikal_posisi+새높이-4);
        assert(Papan_gambar_COUNT()==이전); /* 같은 좌표의 중복 Even */
        Terminal_pointer(0,가로+새폭-4,Vertikal_posisi+새높이-4);폭=새폭;높이=새높이;
        전체와비교();
    }
    /* 잘린 범위와 aktual_data baris_masukan 간격을 지킨다. */
    for(int baris_masukan=0;baris_masukan<1080;baris_masukan++)for(int slot_entri=1920;slot_entri<1936;slot_entri++)assert(화면[baris_masukan][slot_entri]==0);
    assert(!Papan_Mulai_gambar(0,0,1920,33));
    printf("PASS: 80 moves, 40 resizes, 4 overlapping windows; %.3f ms/move; %llu framebuffer writes/move\n",이동시간*1000/80,(unsigned long long)(gerak_LOG/80));
    return 0;
}
