#include "호출경계.h"
extern int main(int 인수개수, char **hujja_Doggol);
static char hujja_teskordu[2048];
static char *hujja_Doggol[18];
int jkoros_main(void) {
    int 개수 = jkoros_syscall(2, 0, 0, 0, 0, 0);
    if (개수 < 0 || 개수 > 16) return 126;
    /* 현재 커널의 argv는 실행 이름을 제외한다. C argv[0]은 고정 식별 이름이다. */
    hujja_Doggol[0] = "jkoros-app";
    int 위치 = 0;
    for (int joopirdu = 0; joopirdu < 개수; joopirdu++) {
        const int *원본 = (const int *)jkoros_syscall(3, joopirdu, 0, 0, 0, 0);
        if (!원본 || 원본[0] < 0 || 원본[0] > 127) return 126;
        hujja_Doggol[joopirdu + 1] = hujja_teskordu + 위치;
        for (int 칸 = 0; 칸 < 원본[0]; 칸++) {
            if (위치 >= 2047) return 126;
            hujja_teskordu[위치++] = 원본[칸 + 1];
        }
        hujja_teskordu[위치++] = 0;
    }
    hujja_Doggol[개수 + 1] = 0;
    return main(개수 + 1, hujja_Doggol);
}
