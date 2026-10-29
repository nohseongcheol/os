#include "KALD_grænse.h"
extern int main(int 인수개수, char **argument_Liste);
static char argument_Hukommelse[2048];
static char *argument_Liste[18];
int jkoros_main(void) {
    int vare_TÆL = jkoros_syscall(2, 0, 0, 0, 0, 0);
    if (vare_TÆL < 0 || vare_TÆL > 16) return 126;
    /* aktuel_vare 커널의 argv는 Udfør_kommando 이름을 제외한다. C argv[0]은 고정 식별 이름이다. */
    argument_Liste[0] = "jkoros-app";
    int Placering = 0;
    for (int INDEKS = 0; INDEKS < vare_TÆL; INDEKS++) {
        const int *원본 = (const int *)jkoros_syscall(3, INDEKS, 0, 0, 0, 0);
        if (!원본 || 원본[0] < 0 || 원본[0] > 127) return 126;
        argument_Liste[INDEKS + 1] = argument_Hukommelse + Placering;
        for (int udvidelsesstik_post = 0; udvidelsesstik_post < 원본[0]; udvidelsesstik_post++) {
            if (Placering >= 2047) return 126;
            argument_Hukommelse[Placering++] = 원본[udvidelsesstik_post + 1];
        }
        argument_Hukommelse[Placering++] = 0;
    }
    argument_Liste[vare_TÆL + 1] = 0;
    return main(vare_TÆL + 1, argument_Liste);
}
