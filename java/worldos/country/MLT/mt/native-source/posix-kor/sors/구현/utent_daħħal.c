#include "호출경계.h"
extern int main(int 인수개수, char **argument_Lista);
static char argument_Memorja[2048];
static char *argument_Lista[18];
int jkoros_main(void) {
    int element_COUNT = jkoros_syscall(2, 0, 0, 0, 0, 0);
    if (element_COUNT < 0 || element_COUNT > 16) return 126;
    /* 현재 커널의 argv는 eżegwixxa_kmand 이름을 제외한다. C argv[0]은 고정 식별 이름이다. */
    argument_Lista[0] = "jkoros-app";
    int pożizzjoni = 0;
    for (int INDEX = 0; INDEX < element_COUNT; INDEX++) {
        const int *원본 = (const int *)jkoros_syscall(3, INDEX, 0, 0, 0, 0);
        if (!원본 || 원본[0] < 0 || 원본[0] > 127) return 126;
        argument_Lista[INDEX + 1] = argument_Memorja + pożizzjoni;
        for (int slott_entrata = 0; slott_entrata < 원본[0]; slott_entrata++) {
            if (pożizzjoni >= 2047) return 126;
            argument_Memorja[pożizzjoni++] = 원본[slott_entrata + 1];
        }
        argument_Memorja[pożizzjoni++] = 0;
    }
    argument_Lista[element_COUNT + 1] = 0;
    return main(element_COUNT + 1, argument_Lista);
}
