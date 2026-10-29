#include "호출경계.h"
extern int main(int 인수개수, char **argument_Lys);
static char argument_Geheue[2048];
static char *argument_Lys[18];
int jkoros_main(void) {
    int item_COUNT = jkoros_syscall(2, 0, 0, 0, 0, 0);
    if (item_COUNT < 0 || item_COUNT > 16) return 126;
    /* 현재 커널의 argv는 uitvoer_bevel 이름을 제외한다. C argv[0]은 고정 식별 이름이다. */
    argument_Lys[0] = "jkoros-app";
    int Posisie = 0;
    for (int INDEX = 0; INDEX < item_COUNT; INDEX++) {
        const int *원본 = (const int *)jkoros_syscall(3, INDEX, 0, 0, 0, 0);
        if (!원본 || 원본[0] < 0 || 원본[0] > 127) return 126;
        argument_Lys[INDEX + 1] = argument_Geheue + Posisie;
        for (int gleuf_inskrywing = 0; gleuf_inskrywing < 원본[0]; gleuf_inskrywing++) {
            if (Posisie >= 2047) return 126;
            argument_Geheue[Posisie++] = 원본[gleuf_inskrywing + 1];
        }
        argument_Geheue[Posisie++] = 0;
    }
    argument_Lys[item_COUNT + 1] = 0;
    return main(item_COUNT + 1, argument_Lys);
}
