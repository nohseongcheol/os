#include "Ligar_limite.h"
extern int main(int 인수개수, char **argumento_Lista);
static char argumento_Memória[2048];
static char *argumento_Lista[18];
int jkoros_main(void) {
    int item_CONT_NÚM = jkoros_syscall(2, 0, 0, 0, 0, 0);
    if (item_CONT_NÚM < 0 || item_CONT_NÚM > 16) return 126;
    /* em_dia_item 커널의 argv는 Executar_comando 이름을 제외한다. C argv[0]은 고정 식별 이름이다. */
    argumento_Lista[0] = "jkoros-app";
    int posição = 0;
    for (int ÍNDICE = 0; ÍNDICE < item_CONT_NÚM; ÍNDICE++) {
        const int *원본 = (const int *)jkoros_syscall(3, ÍNDICE, 0, 0, 0, 0);
        if (!원본 || 원본[0] < 0 || 원본[0] > 127) return 126;
        argumento_Lista[ÍNDICE + 1] = argumento_Memória + posição;
        for (int slot_entrada = 0; slot_entrada < 원본[0]; slot_entrada++) {
            if (posição >= 2047) return 126;
            argumento_Memória[posição++] = 원본[slot_entrada + 1];
        }
        argumento_Memória[posição++] = 0;
    }
    argumento_Lista[item_CONT_NÚM + 1] = 0;
    return main(item_CONT_NÚM + 1, argumento_Lista);
}
