#include "../명명/기계연결이름.h"
#include "../gép/화면정보.h"
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>
void 커널중단(const char *설명){fputs(설명,stderr);abort();}
extern uintptr_t fal_Terminál(uintptr_t),fal_képpont(uintptr_t,uintptr_t,uintptr_t);
extern void Terminál_mutató(unsigned,int,int),Terminál_bájt(unsigned);
extern int 화면호출(int,unsigned,int,int,int,int,int);
static uint32_t 화면[1080][1936],Összehasonlítás_KÉP[1080][1936];
uintptr_t 보드화면기억공간(void){return 1;}
static void 전체와비교(void){
    fal_mutató(0,0,0);memcpy(Összehasonlítás_KÉP,화면,sizeof(화면));
    uint64_t Előző_cikk=fal_rajz_DARAB();fal_Terminál(3);
    assert(memcmp(Összehasonlítás_KÉP,화면,sizeof(화면))==0);
    assert(fal_rajz_DARAB()==Előző_cikk); /* 같은 화면을 újrapróbál_ÉRTÉK 그려도 bemutató_ÉRTÉK 메모리에 쓰지 않는다. */
}
static void ír_SMS(const char *Szöveg){while(*Szöveg)Terminál_bájt((unsigned char)*Szöveg++);}
int main(void){
    fal_Előkészítés_rajz(&화면[0][0],1920,1080,sizeof(화면[0]));
    fal_Terminál(300);ír_SMS("첫 창의 한글 adat\n");
    for(int INDEX=1;INDEX<4;INDEX++){fal_Terminál(1);fal_Terminál(100+INDEX);ír_SMS("겹친 창의 한글 adat\n\033[41m색칠한 빈칸     \033[0m\n");}
    전체와비교();
    int 가로=60,szektor_pozíció=102,폭=568,높이=360;
    uint64_t áthelyez_LOG=0;double 이동시간=0;
    for(int szekvencia_ÉRTÉK=0;szekvencia_ÉRTÉK<80;szekvencia_ÉRTÉK++){
        Terminál_mutató(1,가로+100,szektor_pozíció+15);
        int 새가로=80+(szekvencia_ÉRTÉK*37)%850,새세로=50+(szekvencia_ÉRTÉK*13)%450;
        fal_képpont(1900,1050,0x123456); /* frissít régió_ÉRTÉK 밖의 felhasználó rajz_ÉRTÉK */
        uint64_t Előző_cikk=fal_rajz_DARAB();clock_t Futtatás=clock();
        Terminál_mutató(1,새가로+100,새세로+15);
        이동시간+=(double)(clock()-Futtatás)/CLOCKS_PER_SEC;
        áthelyez_LOG+=fal_rajz_DARAB()-Előző_cikk;
        assert(fal_rajz_DARAB()-Előző_cikk<=2u*폭*높이);
        assert(화면[1050][1900]==0x123456);
        fal_képpont(1900,1050,0x302018);
        Terminál_mutató(0,새가로+100,새세로+15);가로=새가로;szektor_pozíció=새세로;
        전체와비교();
    }
    for(int szekvencia_ÉRTÉK=0;szekvencia_ÉRTÉK<40;szekvencia_ÉRTÉK++){
        int 새폭=360+(szekvencia_ÉRTÉK*29)%700,새높이=216+(szekvencia_ÉRTÉK*17)%350;
        if(새폭>1920-가로)새폭=1920-가로;if(새높이>1080-szektor_pozíció)새높이=1080-szektor_pozíció;
        Terminál_mutató(1,가로+폭-4,szektor_pozíció+높이-4);
        Terminál_mutató(1,가로+새폭-4,szektor_pozíció+새높이-4);
        uint64_t Előző_cikk=fal_rajz_DARAB();
        Terminál_mutató(1,가로+새폭-4,szektor_pozíció+새높이-4);
        assert(fal_rajz_DARAB()==Előző_cikk); /* 같은 좌표의 중복 Esemény */
        Terminál_mutató(0,가로+새폭-4,szektor_pozíció+새높이-4);폭=새폭;높이=새높이;
        전체와비교();
    }
    /* 잘린 범위와 tényleges_adat Vonal 간격을 지킨다. */
    for(int Vonal=0;Vonal<1080;Vonal++)for(int tárolóhely_bejegyzés=1920;tárolóhely_bejegyzés<1936;tárolóhely_bejegyzés++)assert(화면[Vonal][tárolóhely_bejegyzés]==0);
    assert(!fal_START_rajz(0,0,1920,33));
    printf("PASS: 80 moves, 40 resizes, 4 overlapping windows; %.3f ms/move; %llu framebuffer writes/move\n",이동시간*1000/80,(unsigned long long)(áthelyez_LOG/80));
    return 0;
}
