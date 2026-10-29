#include "../명명/기계연결이름.h"
#include "../mašina/화면정보.h"
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>
void 커널중단(const char *aprašas){fputs(aprašas,stderr);abort();}
extern uintptr_t Lenta_Terminalas(uintptr_t),Lenta_pikselis(uintptr_t,uintptr_t,uintptr_t);
extern void Terminalas_rodyklė(unsigned,int,int),Terminalas_baitas(unsigned);
extern int 화면호출(int,unsigned,int,int,int,int,int);
static uint32_t 화면[1080][1936],Palyginimas_IMAGE[1080][1936];
uintptr_t 보드화면기억공간(void){return 1;}
static void 전체와비교(void){
    Lenta_rodyklė(0,0,0);memcpy(Palyginimas_IMAGE,화면,sizeof(화면));
    uint64_t 이전=Lenta_piešinys_COUNT();Lenta_Terminalas(3);
    assert(memcmp(Palyginimas_IMAGE,화면,sizeof(화면))==0);
    assert(Lenta_piešinys_COUNT()==이전); /* 같은 화면을 kartoti_VALUE 그려도 laida_VALUE 메모리에 쓰지 않는다. */
}
static void rašymas_SMS(const char *Tekstas){while(*Tekstas)Terminalas_baitas((unsigned char)*Tekstas++);}
int main(void){
    Lenta_Parengti_piešinys(&화면[0][0],1920,1080,sizeof(화면[0]));
    Lenta_Terminalas(300);rašymas_SMS("첫 창의 한글 duomenys\n");
    for(int INDEX=1;INDEX<4;INDEX++){Lenta_Terminalas(1);Lenta_Terminalas(100+INDEX);rašymas_SMS("겹친 창의 한글 duomenys\n\033[41m색칠한 빈칸     \033[0m\n");}
    전체와비교();
    int 가로=60,segmentas_padėtis=102,폭=568,높이=360;
    uint64_t judėti_LOG=0;double 이동시간=0;
    for(int SEQUENCE_VALUE=0;SEQUENCE_VALUE<80;SEQUENCE_VALUE++){
        Terminalas_rodyklė(1,가로+100,segmentas_padėtis+15);
        int 새가로=80+(SEQUENCE_VALUE*37)%850,새세로=50+(SEQUENCE_VALUE*13)%450;
        Lenta_pikselis(1900,1050,0x123456); /* atnaujinti sritis_VALUE_0e9a97ab 밖의 naudotojas piešinys_VALUE */
        uint64_t 이전=Lenta_piešinys_COUNT();clock_t Paleisti=clock();
        Terminalas_rodyklė(1,새가로+100,새세로+15);
        이동시간+=(double)(clock()-Paleisti)/CLOCKS_PER_SEC;
        judėti_LOG+=Lenta_piešinys_COUNT()-이전;
        assert(Lenta_piešinys_COUNT()-이전<=2u*폭*높이);
        assert(화면[1050][1900]==0x123456);
        Lenta_pikselis(1900,1050,0x302018);
        Terminalas_rodyklė(0,새가로+100,새세로+15);가로=새가로;segmentas_padėtis=새세로;
        전체와비교();
    }
    for(int SEQUENCE_VALUE=0;SEQUENCE_VALUE<40;SEQUENCE_VALUE++){
        int 새폭=360+(SEQUENCE_VALUE*29)%700,새높이=216+(SEQUENCE_VALUE*17)%350;
        if(새폭>1920-가로)새폭=1920-가로;if(새높이>1080-segmentas_padėtis)새높이=1080-segmentas_padėtis;
        Terminalas_rodyklė(1,가로+폭-4,segmentas_padėtis+높이-4);
        Terminalas_rodyklė(1,가로+새폭-4,segmentas_padėtis+새높이-4);
        uint64_t 이전=Lenta_piešinys_COUNT();
        Terminalas_rodyklė(1,가로+새폭-4,segmentas_padėtis+새높이-4);
        assert(Lenta_piešinys_COUNT()==이전); /* 같은 좌표의 중복 Įvykis */
        Terminalas_rodyklė(0,가로+새폭-4,segmentas_padėtis+새높이-4);폭=새폭;높이=새높이;
        전체와비교();
    }
    /* 잘린 범위와 faktinis_duomenys Eilutė 간격을 지킨다. */
    for(int Eilutė=0;Eilutė<1080;Eilutė++)for(int 칸=1920;칸<1936;칸++)assert(화면[Eilutė][칸]==0);
    assert(!Lenta_Start_piešinys(0,0,1920,33));
    printf("PASS: 80 moves, 40 resizes, 4 overlapping windows; %.3f ms/move; %llu framebuffer writes/move\n",이동시간*1000/80,(unsigned long long)(judėti_LOG/80));
    return 0;
}
