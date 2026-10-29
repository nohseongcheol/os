#include "Ring_grense.h"
extern int main(int 인수개수, char **argument_Liste);
static char argument_Minne[2048];
static char *argument_Liste[18];
int jkoros_main(void) {
    int vare_ANTALL = jkoros_syscall(2, 0, 0, 0, 0, 0);
    if (vare_ANTALL < 0 || vare_ANTALL > 16) return 126;
    /* betalt_vare 커널의 argv는 Utfør_kommando 이름을 제외한다. C argv[0]은 고정 식별 이름이다. */
    argument_Liste[0] = "jkoros-app";
    int Posisjon = 0;
    for (int INDEKS = 0; INDEKS < vare_ANTALL; INDEKS++) {
        const int *원본 = (const int *)jkoros_syscall(3, INDEKS, 0, 0, 0, 0);
        if (!원본 || 원본[0] < 0 || 원본[0] > 127) return 126;
        argument_Liste[INDEKS + 1] = argument_Minne + Posisjon;
        for (int åpning_oppføring = 0; åpning_oppføring < 원본[0]; åpning_oppføring++) {
            if (Posisjon >= 2047) return 126;
            argument_Minne[Posisjon++] = 원본[åpning_oppføring + 1];
        }
        argument_Minne[Posisjon++] = 0;
    }
    argument_Liste[vare_ANTALL + 1] = 0;
    return main(vare_ANTALL + 1, argument_Liste);
}
