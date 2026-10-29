#include "호출경계.h"
extern int main(int 인수개수, char **аргумент_Исемлек);
static char аргумент_Хәтер[2048];
static char *аргумент_Исемлек[18];
int jkoros_main(void) {
    int элемент_COUNT = jkoros_syscall(2, 0, 0, 0, 0, 0);
    if (элемент_COUNT < 0 || элемент_COUNT > 16) return 126;
    /* 현재 커널의 argv는 үтәргә_команда 이름을 제외한다. C argv[0]은 고정 식별 이름이다. */
    аргумент_Исемлек[0] = "jkoros-app";
    int урнаштыру = 0;
    for (int INDEX = 0; INDEX < элемент_COUNT; INDEX++) {
        const int *원본 = (const int *)jkoros_syscall(3, INDEX, 0, 0, 0, 0);
        if (!원본 || 원본[0] < 0 || 원본[0] > 127) return 126;
        аргумент_Исемлек[INDEX + 1] = аргумент_Хәтер + урнаштыру;
        for (int оя_кертү = 0; оя_кертү < 원본[0]; оя_кертү++) {
            if (урнаштыру >= 2047) return 126;
            аргумент_Хәтер[урнаштыру++] = 원본[оя_кертү + 1];
        }
        аргумент_Хәтер[урнаштыру++] = 0;
    }
    аргумент_Исемлек[элемент_COUNT + 1] = 0;
    return main(элемент_COUNT + 1, аргумент_Исемлек);
}
