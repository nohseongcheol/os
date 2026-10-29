#include "호출경계.h"
extern int main(int 인수개수, char **frumbreyta_Listi);
static char frumbreyta_Minni[2048];
static char *frumbreyta_Listi[18];
int jkoros_main(void) {
    int vara_COUNT = jkoros_syscall(2, 0, 0, 0, 0, 0);
    if (vara_COUNT < 0 || vara_COUNT > 16) return 126;
    /* 현재 커널의 argv는 keyra_skipun 이름을 제외한다. C argv[0]은 고정 식별 이름이다. */
    frumbreyta_Listi[0] = "jkoros-app";
    int Staðsetning = 0;
    for (int INDEX = 0; INDEX < vara_COUNT; INDEX++) {
        const int *원본 = (const int *)jkoros_syscall(3, INDEX, 0, 0, 0, 0);
        if (!원본 || 원본[0] < 0 || 원본[0] > 127) return 126;
        frumbreyta_Listi[INDEX + 1] = frumbreyta_Minni + Staðsetning;
        for (int rauf_færsla = 0; rauf_færsla < 원본[0]; rauf_færsla++) {
            if (Staðsetning >= 2047) return 126;
            frumbreyta_Minni[Staðsetning++] = 원본[rauf_færsla + 1];
        }
        frumbreyta_Minni[Staðsetning++] = 0;
    }
    frumbreyta_Listi[vara_COUNT + 1] = 0;
    return main(vara_COUNT + 1, frumbreyta_Listi);
}
