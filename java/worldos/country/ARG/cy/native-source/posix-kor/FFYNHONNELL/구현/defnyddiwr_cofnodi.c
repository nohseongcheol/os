#include "호출경계.h"
extern int main(int 인수개수, char **arg_Rhestr);
static char arg_Cof[2048];
static char *arg_Rhestr[18];
int jkoros_main(void) {
    int eitem_COUNT = jkoros_syscall(2, 0, 0, 0, 0, 0);
    if (eitem_COUNT < 0 || eitem_COUNT > 16) return 126;
    /* 현재 커널의 argv는 Gweithredu_gorchymyn 이름을 제외한다. C argv[0]은 고정 식별 이름이다. */
    arg_Rhestr[0] = "jkoros-app";
    int safle = 0;
    for (int INDEX = 0; INDEX < eitem_COUNT; INDEX++) {
        const int *원본 = (const int *)jkoros_syscall(3, INDEX, 0, 0, 0, 0);
        if (!원본 || 원본[0] < 0 || 원본[0] > 127) return 126;
        arg_Rhestr[INDEX + 1] = arg_Cof + safle;
        for (int slot_cofnod = 0; slot_cofnod < 원본[0]; slot_cofnod++) {
            if (safle >= 2047) return 126;
            arg_Cof[safle++] = 원본[slot_cofnod + 1];
        }
        arg_Cof[safle++] = 0;
    }
    arg_Rhestr[eitem_COUNT + 1] = 0;
    return main(eitem_COUNT + 1, arg_Rhestr);
}
