#include "Chiama_limite.h"
extern int main(int 인수개수, char **argomento_elenco);
static char argomento_Memoria[2048];
static char *argomento_elenco[18];
int jkoros_main(void) {
    int articolo_CONTA_NUMERI = jkoros_syscall(2, 0, 0, 0, 0, 0);
    if (articolo_CONTA_NUMERI < 0 || articolo_CONTA_NUMERI > 16) return 126;
    /* Regolari_articolo 커널의 argv는 Esegui_comando 이름을 제외한다. C argv[0]은 고정 식별 이름이다. */
    argomento_elenco[0] = "jkoros-app";
    int posizione = 0;
    for (int INDICE = 0; INDICE < articolo_CONTA_NUMERI; INDICE++) {
        const int *원본 = (const int *)jkoros_syscall(3, INDICE, 0, 0, 0, 0);
        if (!원본 || 원본[0] < 0 || 원본[0] > 127) return 126;
        argomento_elenco[INDICE + 1] = argomento_Memoria + posizione;
        for (int slot_voce = 0; slot_voce < 원본[0]; slot_voce++) {
            if (posizione >= 2047) return 126;
            argomento_Memoria[posizione++] = 원본[slot_voce + 1];
        }
        argomento_Memoria[posizione++] = 0;
    }
    argomento_elenco[articolo_CONTA_NUMERI + 1] = 0;
    return main(articolo_CONTA_NUMERI + 1, argomento_elenco);
}
