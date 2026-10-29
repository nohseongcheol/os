#include "호출경계.h"
extern int main(int 인수개수, char **argument_Popis);
static char argument_Memorija[2048];
static char *argument_Popis[18];
int jkoros_main(void) {
    int artikl_COUNT = jkoros_syscall(2, 0, 0, 0, 0, 0);
    if (artikl_COUNT < 0 || artikl_COUNT > 16) return 126;
    /* redovno_artikl 커널의 argv는 Izvrši_naredba 이름을 제외한다. C argv[0]은 고정 식별 이름이다. */
    argument_Popis[0] = "jkoros-app";
    int Položaj = 0;
    for (int INDEX = 0; INDEX < artikl_COUNT; INDEX++) {
        const int *원본 = (const int *)jkoros_syscall(3, INDEX, 0, 0, 0, 0);
        if (!원본 || 원본[0] < 0 || 원본[0] > 127) return 126;
        argument_Popis[INDEX + 1] = argument_Memorija + Položaj;
        for (int 칸 = 0; 칸 < 원본[0]; 칸++) {
            if (Položaj >= 2047) return 126;
            argument_Memorija[Položaj++] = 원본[칸 + 1];
        }
        argument_Memorija[Položaj++] = 0;
    }
    argument_Popis[artikl_COUNT + 1] = 0;
    return main(artikl_COUNT + 1, argument_Popis);
}
