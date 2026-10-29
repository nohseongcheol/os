#include "../명명/기계연결이름.h"
#include "../računar/화면정보.h"
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>
void 커널중단(const char *설명){fputs(설명,stderr);abort();}
extern uintptr_t Tabla_Terminal(uintptr_t),Tabla_piksel(uintptr_t,uintptr_t,uintptr_t);
extern void Terminal_pokazivač(unsigned,int,int),Terminal_bajt(unsigned);
extern int 화면호출(int,unsigned,int,int,int,int,int);
static uint32_t 화면[1080][1936],Poređenje_IMAGE[1080][1936];
uintptr_t 보드화면기억공간(void){return 1;}
static void 전체와비교(void){
    Tabla_pokazivač(0,0,0);memcpy(Poređenje_IMAGE,화면,sizeof(화면));
    uint64_t 이전=Tabla_crtež_COUNT();Tabla_Terminal(3);
    assert(memcmp(Poređenje_IMAGE,화면,sizeof(화면))==0);
    assert(Tabla_crtež_COUNT()==이전); /* 같은 화면을 pokušati_ponovo_VALUE 그려도 emisija_VALUE 메모리에 쓰지 않는다. */
}
static void 글쓰기(const char *SMS){while(*SMS)Terminal_bajt((unsigned char)*SMS++);}
int main(void){
    Tabla_Pripremi_crtež(&화면[0][0],1920,1080,sizeof(화면[0]));
    Tabla_Terminal(300);글쓰기("첫 창의 한글 podaci\n");
    for(int INDEX=1;INDEX<4;INDEX++){Tabla_Terminal(1);Tabla_Terminal(100+INDEX);글쓰기("겹친 창의 한글 podaci\n\033[41m색칠한 빈칸     \033[0m\n");}
    전체와비교();
    int 가로=60,vertikala_pozicija=102,폭=568,높이=360;
    uint64_t premestiti_LOG=0;double 이동시간=0;
    for(int SEQUENCE_VALUE=0;SEQUENCE_VALUE<80;SEQUENCE_VALUE++){
        Terminal_pokazivač(1,가로+100,vertikala_pozicija+15);
        int 새가로=80+(SEQUENCE_VALUE*37)%850,새세로=50+(SEQUENCE_VALUE*13)%450;
        Tabla_piksel(1900,1050,0x123456); /* osvežiti oblast_VALUE_0e9a97ab 밖의 korisnik crtež_VALUE */
        uint64_t 이전=Tabla_crtež_COUNT();clock_t koristiti=clock();
        Terminal_pokazivač(1,새가로+100,새세로+15);
        이동시간+=(double)(clock()-koristiti)/CLOCKS_PER_SEC;
        premestiti_LOG+=Tabla_crtež_COUNT()-이전;
        assert(Tabla_crtež_COUNT()-이전<=2u*폭*높이);
        assert(화면[1050][1900]==0x123456);
        Tabla_piksel(1900,1050,0x302018);
        Terminal_pokazivač(0,새가로+100,새세로+15);가로=새가로;vertikala_pozicija=새세로;
        전체와비교();
    }
    for(int SEQUENCE_VALUE=0;SEQUENCE_VALUE<40;SEQUENCE_VALUE++){
        int 새폭=360+(SEQUENCE_VALUE*29)%700,새높이=216+(SEQUENCE_VALUE*17)%350;
        if(새폭>1920-가로)새폭=1920-가로;if(새높이>1080-vertikala_pozicija)새높이=1080-vertikala_pozicija;
        Terminal_pokazivač(1,가로+폭-4,vertikala_pozicija+높이-4);
        Terminal_pokazivač(1,가로+새폭-4,vertikala_pozicija+새높이-4);
        uint64_t 이전=Tabla_crtež_COUNT();
        Terminal_pokazivač(1,가로+새폭-4,vertikala_pozicija+새높이-4);
        assert(Tabla_crtež_COUNT()==이전); /* 같은 좌표의 중복 događaj */
        Terminal_pokazivač(0,가로+새폭-4,vertikala_pozicija+새높이-4);폭=새폭;높이=새높이;
        전체와비교();
    }
    /* 잘린 범위와 stvarni_podaci red 간격을 지킨다. */
    for(int red=0;red<1080;red++)for(int 칸=1920;칸<1936;칸++)assert(화면[red][칸]==0);
    assert(!Tabla_START_crtež(0,0,1920,33));
    printf("PASS: 80 moves, 40 resizes, 4 overlapping windows; %.3f ms/move; %llu framebuffer writes/move\n",이동시간*1000/80,(unsigned long long)(premestiti_LOG/80));
    return 0;
}
