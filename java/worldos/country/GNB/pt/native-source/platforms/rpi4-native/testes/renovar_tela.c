#include "../명명/기계연결이름.h"
#include "../computador/tela_informações.h"
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdlib.h>
void 커널중단(const char *설명){fputs(설명,stderr);abort();}
extern uintptr_t Quadro_Terminal(uintptr_t),Quadro_pixel(uintptr_t,uintptr_t,uintptr_t);
extern void Terminal_ponteiro(unsigned,int,int),Terminal_byte(unsigned);
extern int 화면호출(int,unsigned,int,int,int,int,int);
static uint32_t tela[1080][1936],Comparação_foto[1080][1936];
uintptr_t 보드화면기억공간(void){return 1;}
static void 전체와비교(void){
    Quadro_ponteiro(0,0,0);memcpy(Comparação_foto,tela,sizeof(tela));
    uint64_t Anterior_item=Quadro_desenho_CONT_NÚM();Quadro_Terminal(3);
    assert(memcmp(Comparação_foto,tela,sizeof(tela))==0);
    assert(Quadro_desenho_CONT_NÚM()==Anterior_item); /* 같은 화면을 repetir_VALOR 그려도 mostrar_VALOR 메모리에 쓰지 않는다. */
}
static void gravar_SMS(const char *texto){while(*texto)Terminal_byte((unsigned char)*texto++);}
int main(void){
    Quadro_Preparar_desenho(&tela[0][0],1920,1080,sizeof(tela[0]));
    Quadro_Terminal(300);gravar_SMS("첫 창의 한글 dados\n");
    for(int ÍNDICE=1;ÍNDICE<4;ÍNDICE++){Quadro_Terminal(1);Quadro_Terminal(100+ÍNDICE);gravar_SMS("겹친 창의 한글 dados\n\033[41m색칠한 빈칸     \033[0m\n");}
    전체와비교();
    int 가로=60,Vertical_cargo=102,폭=568,altura_VALOR=360;
    uint64_t mover_LOG=0;double 이동시간=0;
    for(int SEQUÊNCIA_VALOR=0;SEQUÊNCIA_VALOR<80;SEQUÊNCIA_VALOR++){
        Terminal_ponteiro(1,가로+100,Vertical_cargo+15);
        int 새가로=80+(SEQUÊNCIA_VALOR*37)%850,새세로=50+(SEQUÊNCIA_VALOR*13)%450;
        Quadro_pixel(1900,1050,0x123456); /* renovar região_VALOR 밖의 espaço_do_utilizador desenho_VALOR */
        uint64_t Anterior_item=Quadro_desenho_CONT_NÚM();clock_t iniciar=clock();
        Terminal_ponteiro(1,새가로+100,새세로+15);
        이동시간+=(double)(clock()-iniciar)/CLOCKS_PER_SEC;
        mover_LOG+=Quadro_desenho_CONT_NÚM()-Anterior_item;
        assert(Quadro_desenho_CONT_NÚM()-Anterior_item<=2u*폭*altura_VALOR);
        assert(tela[1050][1900]==0x123456);
        Quadro_pixel(1900,1050,0x302018);
        Terminal_ponteiro(0,새가로+100,새세로+15);가로=새가로;Vertical_cargo=새세로;
        전체와비교();
    }
    for(int SEQUÊNCIA_VALOR=0;SEQUÊNCIA_VALOR<40;SEQUÊNCIA_VALOR++){
        int 새폭=360+(SEQUÊNCIA_VALOR*29)%700,새높이=216+(SEQUÊNCIA_VALOR*17)%350;
        if(새폭>1920-가로)새폭=1920-가로;if(새높이>1080-Vertical_cargo)새높이=1080-Vertical_cargo;
        Terminal_ponteiro(1,가로+폭-4,Vertical_cargo+altura_VALOR-4);
        Terminal_ponteiro(1,가로+새폭-4,Vertical_cargo+새높이-4);
        uint64_t Anterior_item=Quadro_desenho_CONT_NÚM();
        Terminal_ponteiro(1,가로+새폭-4,Vertical_cargo+새높이-4);
        assert(Quadro_desenho_CONT_NÚM()==Anterior_item); /* 같은 좌표의 중복 Evento */
        Terminal_ponteiro(0,가로+새폭-4,Vertical_cargo+새높이-4);폭=새폭;altura_VALOR=새높이;
        전체와비교();
    }
    /* 잘린 범위와 real_dados linha_de_entrada 간격을 지킨다. */
    for(int linha_de_entrada=0;linha_de_entrada<1080;linha_de_entrada++)for(int slot_entrada=1920;slot_entrada<1936;slot_entrada++)assert(tela[linha_de_entrada][slot_entrada]==0);
    assert(!Quadro_START_desenho(0,0,1920,33));
    printf("PASS: 80 moves, 40 resizes, 4 overlapping windows; %.3f ms/move; %llu framebuffer writes/move\n",이동시간*1000/80,(unsigned long long)(mover_LOG/80));
    return 0;
}
