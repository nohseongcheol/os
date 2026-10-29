#include "호출경계.h"
extern int main(int 인수개수, char **argamaid_Liosta);
static char argamaid_cuimhne[2048];
static char *argamaid_Liosta[18];
int jkoros_main(void) {
    int nì_COUNT = jkoros_syscall(2, 0, 0, 0, 0, 0);
    if (nì_COUNT < 0 || nì_COUNT > 16) return 126;
    /* 현재 커널의 argv는 gnìomhaich_àithne 이름을 제외한다. C argv[0]은 고정 식별 이름이다. */
    argamaid_Liosta[0] = "jkoros-app";
    int suidhich = 0;
    for (int INDEX = 0; INDEX < nì_COUNT; INDEX++) {
        const int *원본 = (const int *)jkoros_syscall(3, INDEX, 0, 0, 0, 0);
        if (!원본 || 원본[0] < 0 || 원본[0] > 127) return 126;
        argamaid_Liosta[INDEX + 1] = argamaid_cuimhne + suidhich;
        for (int slot_cur_a_steach = 0; slot_cur_a_steach < 원본[0]; slot_cur_a_steach++) {
            if (suidhich >= 2047) return 126;
            argamaid_cuimhne[suidhich++] = 원본[slot_cur_a_steach + 1];
        }
        argamaid_cuimhne[suidhich++] = 0;
    }
    argamaid_Liosta[nì_COUNT + 1] = 0;
    return main(nì_COUNT + 1, argamaid_Liosta);
}
