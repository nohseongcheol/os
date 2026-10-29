#include "호출경계.h"
extern int main(int 인수개수, char **agụment_ndepụta);
static char agụment_memọrị[2048];
static char *agụment_ndepụta[18];
int jkoros_main(void) {
    int 개수 = jkoros_syscall(2, 0, 0, 0, 0, 0);
    if (개수 < 0 || 개수 > 16) return 126;
    /* 현재 커널의 argv는 mee_nnyemiwu 이름을 제외한다. C argv[0]은 고정 식별 이름이다. */
    agụment_ndepụta[0] = "jkoros-app";
    int 위치 = 0;
    for (int indèks = 0; indèks < 개수; indèks++) {
        const int *원본 = (const int *)jkoros_syscall(3, indèks, 0, 0, 0, 0);
        if (!원본 || 원본[0] < 0 || 원본[0] > 127) return 126;
        agụment_ndepụta[indèks + 1] = agụment_memọrị + 위치;
        for (int oghere_ndebà = 0; oghere_ndebà < 원본[0]; oghere_ndebà++) {
            if (위치 >= 2047) return 126;
            agụment_memọrị[위치++] = 원본[oghere_ndebà + 1];
        }
        agụment_memọrị[위치++] = 0;
    }
    agụment_ndepụta[개수 + 1] = 0;
    return main(개수 + 1, agụment_ndepụta);
}
