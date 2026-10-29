#include "호출경계.h"
extern int main(int 인수개수, char **arqument_Siyahı);
static char arqument_Yaddaş[2048];
static char *arqument_Siyahı[18];
int jkoros_main(void) {
    int element_COUNT = jkoros_syscall(2, 0, 0, 0, 0, 0);
    if (element_COUNT < 0 || element_COUNT > 16) return 126;
    /* 현재 커널의 argv는 icra_etmək_əmr 이름을 제외한다. C argv[0]은 고정 식별 이름이다. */
    arqument_Siyahı[0] = "jkoros-app";
    int yerinə_qoymaq = 0;
    for (int INDEX = 0; INDEX < element_COUNT; INDEX++) {
        const int *원본 = (const int *)jkoros_syscall(3, INDEX, 0, 0, 0, 0);
        if (!원본 || 원본[0] < 0 || 원본[0] > 127) return 126;
        arqument_Siyahı[INDEX + 1] = arqument_Yaddaş + yerinə_qoymaq;
        for (int slot_daxiletmə = 0; slot_daxiletmə < 원본[0]; slot_daxiletmə++) {
            if (yerinə_qoymaq >= 2047) return 126;
            arqument_Yaddaş[yerinə_qoymaq++] = 원본[slot_daxiletmə + 1];
        }
        arqument_Yaddaş[yerinə_qoymaq++] = 0;
    }
    arqument_Siyahı[element_COUNT + 1] = 0;
    return main(element_COUNT + 1, arqument_Siyahı);
}
