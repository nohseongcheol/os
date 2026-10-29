#include "../명명/기계연결이름.h"
#include "../mašina/화면정보.h"
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>
void 커널중단(const char *설명){fputs(설명,stderr);abort();}
extern uintptr_t ploča_Terminal(uintptr_t),ploča_pel(uintptr_t,uintptr_t,uintptr_t);
extern void Terminal_pokazivač(unsigned,int,int),Terminal_bajt(unsigned);
extern int 화면호출(int,unsigned,int,int,int,int,int);
static uint32_t 화면[1080][1936],Poređenje_IMAGE[1080][1936];
uintptr_t 보드화면기억공간(void){return 1;}
static void 전체와비교(void){
    ploča_pokazivač(0,0,0);memcpy(Poređenje_IMAGE,화면,sizeof(화면));
    uint64_t 이전=ploča_ucrtavanje_COUNT();ploča_Terminal(3);
    assert(memcmp(Poređenje_IMAGE,화면,sizeof(화면))==0);
    assert(ploča_ucrtavanje_COUNT()==이전); /* 같은 화면을 다시 그려도 program_VALUE 메모리에 쓰지 않는다. */
}
static void pisati_SMS(const char *Tekst){while(*Tekst)Terminal_bajt((unsigned char)*Tekst++);}
int main(void){
    ploča_Pripremiti_ucrtavanje(&화면[0][0],1920,1080,sizeof(화면[0]));
    ploča_Terminal(300);pisati_SMS("첫 창의 한글 podaci\n");
    for(int INDEX=1;INDEX<4;INDEX++){ploča_Terminal(1);ploča_Terminal(100+INDEX);pisati_SMS("겹친 창의 한글 podaci\n\033[41m색칠한 빈칸     \033[0m\n");}
    전체와비교();
    int 가로=60,Vertikalno_položaj=102,폭=568,높이=360;
    uint64_t pomaći_LOG=0;double 이동시간=0;
    for(int SEQUENCE_VALUE=0;SEQUENCE_VALUE<80;SEQUENCE_VALUE++){
        Terminal_pokazivač(1,가로+100,Vertikalno_položaj+15);
        int 새가로=80+(SEQUENCE_VALUE*37)%850,새세로=50+(SEQUENCE_VALUE*13)%450;
        ploča_pel(1900,1050,0x123456); /* osvježiti 영역 밖의 korisnik ucrtavanje_VALUE */
        uint64_t 이전=ploča_ucrtavanje_COUNT();clock_t Pokreni=clock();
        Terminal_pokazivač(1,새가로+100,새세로+15);
        이동시간+=(double)(clock()-Pokreni)/CLOCKS_PER_SEC;
        pomaći_LOG+=ploča_ucrtavanje_COUNT()-이전;
        assert(ploča_ucrtavanje_COUNT()-이전<=2u*폭*높이);
        assert(화면[1050][1900]==0x123456);
        ploča_pel(1900,1050,0x302018);
        Terminal_pokazivač(0,새가로+100,새세로+15);가로=새가로;Vertikalno_položaj=새세로;
        전체와비교();
    }
    for(int SEQUENCE_VALUE=0;SEQUENCE_VALUE<40;SEQUENCE_VALUE++){
        int 새폭=360+(SEQUENCE_VALUE*29)%700,새높이=216+(SEQUENCE_VALUE*17)%350;
        if(새폭>1920-가로)새폭=1920-가로;if(새높이>1080-Vertikalno_položaj)새높이=1080-Vertikalno_položaj;
        Terminal_pokazivač(1,가로+폭-4,Vertikalno_položaj+높이-4);
        Terminal_pokazivač(1,가로+새폭-4,Vertikalno_položaj+새높이-4);
        uint64_t 이전=ploča_ucrtavanje_COUNT();
        Terminal_pokazivač(1,가로+새폭-4,Vertikalno_položaj+새높이-4);
        assert(ploča_ucrtavanje_COUNT()==이전); /* 같은 좌표의 중복 događaj */
        Terminal_pokazivač(0,가로+새폭-4,Vertikalno_položaj+새높이-4);폭=새폭;높이=새높이;
        전체와비교();
    }
    /* 잘린 범위와 stvaran_podaci Linija 간격을 지킨다. */
    for(int Linija=0;Linija<1080;Linija++)for(int prostor_za_unos_unos=1920;prostor_za_unos_unos<1936;prostor_za_unos_unos++)assert(화면[Linija][prostor_za_unos_unos]==0);
    assert(!ploča_START_ucrtavanje(0,0,1920,33));
    printf("PASS: 80 moves, 40 resizes, 4 overlapping windows; %.3f ms/move; %llu framebuffer writes/move\n",이동시간*1000/80,(unsigned long long)(pomaći_LOG/80));
    return 0;
}
