#include "호출경계.h"
extern int main(int 인수개수, char **arg_Zerrenda);
static char arg_Memoria[2048];
static char *arg_Zerrenda[18];
int jkoros_main(void) {
    int elementu_ZENBATU = jkoros_syscall(2, 0, 0, 0, 0, 0);
    if (elementu_ZENBATU < 0 || elementu_ZENBATU > 16) return 126;
    /* 현재 커널의 argv는 exekutatu_komando 이름을 제외한다. C argv[0]은 고정 식별 이름이다. */
    arg_Zerrenda[0] = "jkoros-app";
    int Posizioa = 0;
    for (int INDIZE = 0; INDIZE < elementu_ZENBATU; INDIZE++) {
        const int *원본 = (const int *)jkoros_syscall(3, INDIZE, 0, 0, 0, 0);
        if (!원본 || 원본[0] < 0 || 원본[0] > 127) return 126;
        arg_Zerrenda[INDIZE + 1] = arg_Memoria + Posizioa;
        for (int 칸 = 0; 칸 < 원본[0]; 칸++) {
            if (Posizioa >= 2047) return 126;
            arg_Memoria[Posizioa++] = 원본[칸 + 1];
        }
        arg_Memoria[Posizioa++] = 0;
    }
    arg_Zerrenda[elementu_ZENBATU + 1] = 0;
    return main(elementu_ZENBATU + 1, arg_Zerrenda);
}
