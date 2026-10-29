#include "../명명/기계연결이름.h"
#include "../máquina/화면정보.h"
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>
void 커널중단(const char *설명){fputs(설명,stderr);abort();}
extern uintptr_t Panel_Terminal(uintptr_t),Panel_píxel(uintptr_t,uintptr_t,uintptr_t);
extern void Terminal_punteiro(unsigned,int,int),Terminal_byte(unsigned);
extern int 화면호출(int,unsigned,int,int,int,int,int);
static uint32_t 화면[1080][1936],Comparación_IMAXE[1080][1936];
uintptr_t 보드화면기억공간(void){return 1;}
static void 전체와비교(void){
    Panel_punteiro(0,0,0);memcpy(Comparación_IMAXE,화면,sizeof(화면));
    uint64_t 이전=보드그림기록수();Panel_Terminal(3);
    assert(memcmp(Comparación_IMAXE,화면,sizeof(화면))==0);
    assert(보드그림기록수()==이전); /* 같은 화면을 다시 그려도 mostrar_VALOR 메모리에 쓰지 않는다. */
}
static void escribir_SMS(const char *Texto){while(*Texto)Terminal_byte((unsigned char)*Texto++);}
int main(void){
    보드그림준비(&화면[0][0],1920,1080,sizeof(화면[0]));
    Panel_Terminal(300);escribir_SMS("첫 창의 한글 datos\n");
    for(int ÍNDICE=1;ÍNDICE<4;ÍNDICE++){Panel_Terminal(1);Panel_Terminal(100+ÍNDICE);escribir_SMS("겹친 창의 한글 datos\n\033[41m색칠한 빈칸     \033[0m\n");}
    전체와비교();
    int 가로=60,Vertical_cargo=102,폭=568,높이=360;
    uint64_t mover_LOG=0;double 이동시간=0;
    for(int SECUENCIA_VALOR=0;SECUENCIA_VALOR<80;SECUENCIA_VALOR++){
        Terminal_punteiro(1,가로+100,Vertical_cargo+15);
        int 새가로=80+(SECUENCIA_VALOR*37)%850,새세로=50+(SECUENCIA_VALOR*13)%450;
        Panel_píxel(1900,1050,0x123456); /* actualizar 영역 밖의 usuario 그림 */
        uint64_t 이전=보드그림기록수();clock_t Executar_2=clock();
        Terminal_punteiro(1,새가로+100,새세로+15);
        이동시간+=(double)(clock()-Executar_2)/CLOCKS_PER_SEC;
        mover_LOG+=보드그림기록수()-이전;
        assert(보드그림기록수()-이전<=2u*폭*높이);
        assert(화면[1050][1900]==0x123456);
        Panel_píxel(1900,1050,0x302018);
        Terminal_punteiro(0,새가로+100,새세로+15);가로=새가로;Vertical_cargo=새세로;
        전체와비교();
    }
    for(int SECUENCIA_VALOR=0;SECUENCIA_VALOR<40;SECUENCIA_VALOR++){
        int 새폭=360+(SECUENCIA_VALOR*29)%700,새높이=216+(SECUENCIA_VALOR*17)%350;
        if(새폭>1920-가로)새폭=1920-가로;if(새높이>1080-Vertical_cargo)새높이=1080-Vertical_cargo;
        Terminal_punteiro(1,가로+폭-4,Vertical_cargo+높이-4);
        Terminal_punteiro(1,가로+새폭-4,Vertical_cargo+새높이-4);
        uint64_t 이전=보드그림기록수();
        Terminal_punteiro(1,가로+새폭-4,Vertical_cargo+새높이-4);
        assert(보드그림기록수()==이전); /* 같은 좌표의 중복 Evento */
        Terminal_punteiro(0,가로+새폭-4,Vertical_cargo+새높이-4);폭=새폭;높이=새높이;
        전체와비교();
    }
    /* 잘린 범위와 real_datos Liña 간격을 지킨다. */
    for(int Liña=0;Liña<1080;Liña++)for(int 칸=1920;칸<1936;칸++)assert(화면[Liña][칸]==0);
    assert(!보드그림시작(0,0,1920,33));
    printf("PASS: 80 moves, 40 resizes, 4 overlapping windows; %.3f ms/move; %llu framebuffer writes/move\n",이동시간*1000/80,(unsigned long long)(mover_LOG/80));
    return 0;
}
