#include "호출경계.h"
extern int main(int 인수개수, char **argumento_list);
static char argumento_Memory[2048];
static char *argumento_list[18];
int jkoros_main(void) {
    int item_COUNT = jkoros_syscall(2, 0, 0, 0, 0, 0);
    if (item_COUNT < 0 || item_COUNT > 16) return 126;
    /* 현재 커널의 argv는 Mag_execute_utos 이름을 제외한다. C argv[0]은 고정 식별 이름이다. */
    argumento_list[0] = "jkoros-app";
    int posisyon = 0;
    for (int INDEX = 0; INDEX < item_COUNT; INDEX++) {
        const int *원본 = (const int *)jkoros_syscall(3, INDEX, 0, 0, 0, 0);
        if (!원본 || 원본[0] < 0 || 원본[0] > 127) return 126;
        argumento_list[INDEX + 1] = argumento_Memory + posisyon;
        for (int espasyo_pagpasok = 0; espasyo_pagpasok < 원본[0]; espasyo_pagpasok++) {
            if (posisyon >= 2047) return 126;
            argumento_Memory[posisyon++] = 원본[espasyo_pagpasok + 1];
        }
        argumento_Memory[posisyon++] = 0;
    }
    argumento_list[item_COUNT + 1] = 0;
    return main(item_COUNT + 1, argumento_list);
}
