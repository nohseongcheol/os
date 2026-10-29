#include "호출경계.h"
extern int main(int 인수개수, char **argument_Lista);
static char argument_Memorija[2048];
static char *argument_Lista[18];
int jkoros_main(void) {
    int stavka_COUNT = jkoros_syscall(2, 0, 0, 0, 0, 0);
    if (stavka_COUNT < 0 || stavka_COUNT > 16) return 126;
    /* aktuelno_stavka 커널의 argv는 Izvrši_komanda 이름을 제외한다. C argv[0]은 고정 식별 이름이다. */
    argument_Lista[0] = "jkoros-app";
    int pozicija = 0;
    for (int INDEX = 0; INDEX < stavka_COUNT; INDEX++) {
        const int *원본 = (const int *)jkoros_syscall(3, INDEX, 0, 0, 0, 0);
        if (!원본 || 원본[0] < 0 || 원본[0] > 127) return 126;
        argument_Lista[INDEX + 1] = argument_Memorija + pozicija;
        for (int 칸 = 0; 칸 < 원본[0]; 칸++) {
            if (pozicija >= 2047) return 126;
            argument_Memorija[pozicija++] = 원본[칸 + 1];
        }
        argument_Memorija[pozicija++] = 0;
    }
    argument_Lista[stavka_COUNT + 1] = 0;
    return main(stavka_COUNT + 1, argument_Lista);
}
