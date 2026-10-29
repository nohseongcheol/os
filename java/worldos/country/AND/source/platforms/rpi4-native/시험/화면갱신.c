#include "../명명/기계연결이름.h"
#include "../màquina/화면정보.h"
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>
void 커널중단(const char *설명){fputs(설명,stderr);abort();}
extern uintptr_t Tauler_Terminal(uintptr_t),Tauler_píxel(uintptr_t,uintptr_t,uintptr_t);
extern void Terminal_punter(unsigned,int,int),Terminal_byte(unsigned);
extern int 화면호출(int,unsigned,int,int,int,int,int);
static uint32_t 화면[1080][1936],Comparació_IMATGE[1080][1936];
uintptr_t 보드화면기억공간(void){return 1;}
static void 전체와비교(void){
    Tauler_punter(0,0,0);memcpy(Comparació_IMATGE,화면,sizeof(화면));
    uint64_t 이전=Tauler_dibuix_COMPT();Tauler_Terminal(3);
    assert(memcmp(Comparació_IMATGE,화면,sizeof(화면))==0);
    assert(Tauler_dibuix_COMPT()==이전); /* 같은 화면을 tornar_ho_a_provar_VALOR 그려도 mostrar_VALOR 메모리에 쓰지 않는다. */
}
static void escriure_SMS(const char *SMS){while(*SMS)Terminal_byte((unsigned char)*SMS++);}
int main(void){
    Tauler_Prepara_dibuix(&화면[0][0],1920,1080,sizeof(화면[0]));
    Tauler_Terminal(300);escriure_SMS("첫 창의 한글 dades\n");
    for(int INDEX=1;INDEX<4;INDEX++){Tauler_Terminal(1);Tauler_Terminal(100+INDEX);escriure_SMS("겹친 창의 한글 dades\n\033[41m색칠한 빈칸     \033[0m\n");}
    전체와비교();
    int 가로=60,Vertical_càrrec=102,폭=568,높이=360;
    uint64_t moure_LOG=0;double 이동시간=0;
    for(int SEQÜÈNCIA_VALOR=0;SEQÜÈNCIA_VALOR<80;SEQÜÈNCIA_VALOR++){
        Terminal_punter(1,가로+100,Vertical_càrrec+15);
        int 새가로=80+(SEQÜÈNCIA_VALOR*37)%850,새세로=50+(SEQÜÈNCIA_VALOR*13)%450;
        Tauler_píxel(1900,1050,0x123456); /* actualitzar 영역 밖의 usuari dibuix_VALOR */
        uint64_t 이전=Tauler_dibuix_COMPT();clock_t Executa_2=clock();
        Terminal_punter(1,새가로+100,새세로+15);
        이동시간+=(double)(clock()-Executa_2)/CLOCKS_PER_SEC;
        moure_LOG+=Tauler_dibuix_COMPT()-이전;
        assert(Tauler_dibuix_COMPT()-이전<=2u*폭*높이);
        assert(화면[1050][1900]==0x123456);
        Tauler_píxel(1900,1050,0x302018);
        Terminal_punter(0,새가로+100,새세로+15);가로=새가로;Vertical_càrrec=새세로;
        전체와비교();
    }
    for(int SEQÜÈNCIA_VALOR=0;SEQÜÈNCIA_VALOR<40;SEQÜÈNCIA_VALOR++){
        int 새폭=360+(SEQÜÈNCIA_VALOR*29)%700,새높이=216+(SEQÜÈNCIA_VALOR*17)%350;
        if(새폭>1920-가로)새폭=1920-가로;if(새높이>1080-Vertical_càrrec)새높이=1080-Vertical_càrrec;
        Terminal_punter(1,가로+폭-4,Vertical_càrrec+높이-4);
        Terminal_punter(1,가로+새폭-4,Vertical_càrrec+새높이-4);
        uint64_t 이전=Tauler_dibuix_COMPT();
        Terminal_punter(1,가로+새폭-4,Vertical_càrrec+새높이-4);
        assert(Tauler_dibuix_COMPT()==이전); /* 같은 좌표의 중복 Esdeveniment */
        Terminal_punter(0,가로+새폭-4,Vertical_càrrec+새높이-4);폭=새폭;높이=새높이;
        전체와비교();
    }
    /* 잘린 범위와 real_dades línia 간격을 지킨다. */
    for(int línia=0;línia<1080;línia++)for(int 칸=1920;칸<1936;칸++)assert(화면[línia][칸]==0);
    assert(!Tauler_Inici_dibuix(0,0,1920,33));
    printf("PASS: 80 moves, 40 resizes, 4 overlapping windows; %.3f ms/move; %llu framebuffer writes/move\n",이동시간*1000/80,(unsigned long long)(moure_LOG/80));
    return 0;
}
