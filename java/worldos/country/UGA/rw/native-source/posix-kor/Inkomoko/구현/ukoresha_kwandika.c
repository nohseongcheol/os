#include "호출경계.h"
extern int main(int 인수개수, char **ingingo_Urutonde);
static char ingingo_ububiko[2048];
static char *ingingo_Urutonde[18];
int jkoros_main(void) {
    int 개수 = jkoros_syscall(2, 0, 0, 0, 0, 0);
    if (개수 < 0 || 개수 > 16) return 126;
    /* 현재 커널의 argv는 gukora_ibwiriza 이름을 제외한다. C argv[0]은 고정 식별 이름이다. */
    ingingo_Urutonde[0] = "jkoros-app";
    int 위치 = 0;
    for (int umugerekashakiro = 0; umugerekashakiro < 개수; umugerekashakiro++) {
        const int *원본 = (const int *)jkoros_syscall(3, umugerekashakiro, 0, 0, 0, 0);
        if (!원본 || 원본[0] < 0 || 원본[0] > 127) return 126;
        ingingo_Urutonde[umugerekashakiro + 1] = ingingo_ububiko + 위치;
        for (int umwanya_icyinjizwa = 0; umwanya_icyinjizwa < 원본[0]; umwanya_icyinjizwa++) {
            if (위치 >= 2047) return 126;
            ingingo_ububiko[위치++] = 원본[umwanya_icyinjizwa + 1];
        }
        ingingo_ububiko[위치++] = 0;
    }
    ingingo_Urutonde[개수 + 1] = 0;
    return main(개수 + 1, ingingo_Urutonde);
}
