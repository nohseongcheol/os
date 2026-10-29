#include "호출경계.h"
extern int main(int 인수개수, char **аргумент_Список);
static char аргумент_Меморија[2048];
static char *аргумент_Список[18];
int jkoros_main(void) {
    int ставка_COUNT = jkoros_syscall(2, 0, 0, 0, 0, 0);
    if (ставка_COUNT < 0 || ставка_COUNT > 16) return 126;
    /* 현재 커널의 argv는 Изврши_наредба 이름을 제외한다. C argv[0]은 고정 식별 이름이다. */
    аргумент_Список[0] = "jkoros-app";
    int Позиција = 0;
    for (int INDEX = 0; INDEX < ставка_COUNT; INDEX++) {
        const int *원본 = (const int *)jkoros_syscall(3, INDEX, 0, 0, 0, 0);
        if (!원본 || 원본[0] < 0 || 원본[0] > 127) return 126;
        аргумент_Список[INDEX + 1] = аргумент_Меморија + Позиција;
        for (int отвор_внес = 0; отвор_внес < 원본[0]; отвор_внес++) {
            if (Позиција >= 2047) return 126;
            аргумент_Меморија[Позиција++] = 원본[отвор_внес + 1];
        }
        аргумент_Меморија[Позиција++] = 0;
    }
    аргумент_Список[ставка_COUNT + 1] = 0;
    return main(ставка_COUNT + 1, аргумент_Список);
}
