#include "호출경계.h"
extern int main(int 인수개수, char **dalil_Ro_yxat);
static char dalil_Xotira[2048];
static char *dalil_Ro_yxat[18];
int jkoros_main(void) {
    int element_COUNT = jkoros_syscall(2, 0, 0, 0, 0, 0);
    if (element_COUNT < 0 || element_COUNT > 16) return 126;
    /* 현재 커널의 argv는 bajarmoq_buyruq 이름을 제외한다. C argv[0]은 고정 식별 이름이다. */
    dalil_Ro_yxat[0] = "jkoros-app";
    int Holati = 0;
    for (int INDEX = 0; INDEX < element_COUNT; INDEX++) {
        const int *원본 = (const int *)jkoros_syscall(3, INDEX, 0, 0, 0, 0);
        if (!원본 || 원본[0] < 0 || 원본[0] > 127) return 126;
        dalil_Ro_yxat[INDEX + 1] = dalil_Xotira + Holati;
        for (int in_kiritish = 0; in_kiritish < 원본[0]; in_kiritish++) {
            if (Holati >= 2047) return 126;
            dalil_Xotira[Holati++] = 원본[in_kiritish + 1];
        }
        dalil_Xotira[Holati++] = 0;
    }
    dalil_Ro_yxat[element_COUNT + 1] = 0;
    return main(element_COUNT + 1, dalil_Ro_yxat);
}
