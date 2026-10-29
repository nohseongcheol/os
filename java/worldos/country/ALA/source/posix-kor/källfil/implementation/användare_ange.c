#include "ring_gräns.h"
extern int main(int 인수개수, char **argument_ange);
static char argument_Minne[2048];
static char *argument_ange[18];
int jkoros_main(void) {
    int objekt_ANTAL = jkoros_syscall(2, 0, 0, 0, 0, 0);
    if (objekt_ANTAL < 0 || objekt_ANTAL > 16) return 126;
    /* aktuellt_objekt 커널의 argv는 köra_kommando 이름을 제외한다. C argv[0]은 고정 식별 이름이다. */
    argument_ange[0] = "jkoros-app";
    int position = 0;
    for (int INDEX = 0; INDEX < objekt_ANTAL; INDEX++) {
        const int *원본 = (const int *)jkoros_syscall(3, INDEX, 0, 0, 0, 0);
        if (!원본 || 원본[0] < 0 || 원본[0] > 127) return 126;
        argument_ange[INDEX + 1] = argument_Minne + position;
        for (int fack_post = 0; fack_post < 원본[0]; fack_post++) {
            if (position >= 2047) return 126;
            argument_Minne[position++] = 원본[fack_post + 1];
        }
        argument_Minne[position++] = 0;
    }
    argument_ange[objekt_ANTAL + 1] = 0;
    return main(objekt_ANTAL + 1, argument_ange);
}
