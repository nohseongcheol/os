#include "호출경계.h"
extern int main(int 인수개수, char **argument_spisak);
static char argument_Memorija[2048];
static char *argument_spisak[18];
int jkoros_main(void) {
    int stavka_COUNT = jkoros_syscall(2, 0, 0, 0, 0, 0);
    if (stavka_COUNT < 0 || stavka_COUNT > 16) return 126;
    /* trenutno_stavka 커널의 argv는 Izvrši_komanda 이름을 제외한다. C argv[0]은 고정 식별 이름이다. */
    argument_spisak[0] = "jkoros-app";
    int Pozicija = 0;
    for (int INDEX = 0; INDEX < stavka_COUNT; INDEX++) {
        const int *원본 = (const int *)jkoros_syscall(3, INDEX, 0, 0, 0, 0);
        if (!원본 || 원본[0] < 0 || 원본[0] > 127) return 126;
        argument_spisak[INDEX + 1] = argument_Memorija + Pozicija;
        for (int prostor_za_unos_unos = 0; prostor_za_unos_unos < 원본[0]; prostor_za_unos_unos++) {
            if (Pozicija >= 2047) return 126;
            argument_Memorija[Pozicija++] = 원본[prostor_za_unos_unos + 1];
        }
        argument_Memorija[Pozicija++] = 0;
    }
    argument_spisak[stavka_COUNT + 1] = 0;
    return main(stavka_COUNT + 1, argument_spisak);
}
