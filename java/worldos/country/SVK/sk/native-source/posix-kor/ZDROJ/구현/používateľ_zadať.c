#include "호출경계.h"
extern int main(int 인수개수, char **argument_Zoznam);
static char argument_Pamäť[2048];
static char *argument_Zoznam[18];
int jkoros_main(void) {
    int položka_COUNT = jkoros_syscall(2, 0, 0, 0, 0, 0);
    if (položka_COUNT < 0 || položka_COUNT > 16) return 126;
    /* v_termíne_splatnosti_položka 커널의 argv는 Vykonať_príkaz 이름을 제외한다. C argv[0]은 고정 식별 이름이다. */
    argument_Zoznam[0] = "jkoros-app";
    int Pozícia = 0;
    for (int INDEX = 0; INDEX < položka_COUNT; INDEX++) {
        const int *원본 = (const int *)jkoros_syscall(3, INDEX, 0, 0, 0, 0);
        if (!원본 || 원본[0] < 0 || 원본[0] > 127) return 126;
        argument_Zoznam[INDEX + 1] = argument_Pamäť + Pozícia;
        for (int 칸 = 0; 칸 < 원본[0]; 칸++) {
            if (Pozícia >= 2047) return 126;
            argument_Pamäť[Pozícia++] = 원본[칸 + 1];
        }
        argument_Pamäť[Pozícia++] = 0;
    }
    argument_Zoznam[položka_COUNT + 1] = 0;
    return main(položka_COUNT + 1, argument_Zoznam);
}
