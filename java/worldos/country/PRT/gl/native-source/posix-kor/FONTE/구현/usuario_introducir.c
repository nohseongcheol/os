#include "호출경계.h"
extern int main(int 인수개수, char **argumento_Lista);
static char argumento_Memoria[2048];
static char *argumento_Lista[18];
int jkoros_main(void) {
    int elemento_CONTAR = jkoros_syscall(2, 0, 0, 0, 0, 0);
    if (elemento_CONTAR < 0 || elemento_CONTAR > 16) return 126;
    /* ao_corrente_elemento 커널의 argv는 executar_comando 이름을 제외한다. C argv[0]은 고정 식별 이름이다. */
    argumento_Lista[0] = "jkoros-app";
    int Posición = 0;
    for (int ÍNDICE = 0; ÍNDICE < elemento_CONTAR; ÍNDICE++) {
        const int *원본 = (const int *)jkoros_syscall(3, ÍNDICE, 0, 0, 0, 0);
        if (!원본 || 원본[0] < 0 || 원본[0] > 127) return 126;
        argumento_Lista[ÍNDICE + 1] = argumento_Memoria + Posición;
        for (int 칸 = 0; 칸 < 원본[0]; 칸++) {
            if (Posición >= 2047) return 126;
            argumento_Memoria[Posición++] = 원본[칸 + 1];
        }
        argumento_Memoria[Posición++] = 0;
    }
    argumento_Lista[elemento_CONTAR + 1] = 0;
    return main(elemento_CONTAR + 1, argumento_Lista);
}
