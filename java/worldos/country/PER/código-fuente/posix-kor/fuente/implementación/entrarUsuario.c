#include "FronteraLlamada.h"
extern int main(int númeroElementosArgumentos, char **listaArgumento);
static char memoriaArgumento[2048];
static char *listaArgumento[18];
int jkoros_main(void) {
    int númeroElementosElementoLista = jkoros_syscall(2, 0, 0, 0, 0, 0);
    if (númeroElementosElementoLista < 0 || númeroElementosElementoLista > 16) return 126;
    /* elementoListaActual 커널의 argv는 ejecutarComando 이름을 제외한다. C argv[0]은 고정 identificarValor 이름이다. */
    listaArgumento[0] = "jkoros-app";
    int posición = 0;
    for (int número = 0; número < númeroElementosElementoLista; número++) {
        const int *original = (const int *)jkoros_syscall(3, número, 0, 0, 0, 0);
        if (!original || original[0] < 0 || original[0] > 127) return 126;
        listaArgumento[número + 1] = memoriaArgumento + posición;
        for (int entradaElementoRanura = 0; entradaElementoRanura < original[0]; entradaElementoRanura++) {
            if (posición >= 2047) return 126;
            memoriaArgumento[posición++] = original[entradaElementoRanura + 1];
        }
        memoriaArgumento[posición++] = 0;
    }
    listaArgumento[númeroElementosElementoLista + 1] = 0;
    return main(númeroElementosElementoLista + 1, listaArgumento);
}
