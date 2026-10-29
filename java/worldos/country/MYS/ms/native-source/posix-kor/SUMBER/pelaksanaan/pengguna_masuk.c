#include "호출경계.h"
extern int main(int 인수개수, char **argumen_Senarai);
static char argumen_Memori[2048];
static char *argumen_Senarai[18];
int jkoros_main(void) {
    int item_COUNT = jkoros_syscall(2, 0, 0, 0, 0, 0);
    if (item_COUNT < 0 || item_COUNT > 16) return 126;
    /* 현재 커널의 argv는 laksanakan_perintah 이름을 제외한다. C argv[0]은 고정 식별 이름이다. */
    argumen_Senarai[0] = "jkoros-app";
    int Kedudukan = 0;
    for (int INDEX = 0; INDEX < item_COUNT; INDEX++) {
        const int *원본 = (const int *)jkoros_syscall(3, INDEX, 0, 0, 0, 0);
        if (!원본 || 원본[0] < 0 || 원본[0] > 127) return 126;
        argumen_Senarai[INDEX + 1] = argumen_Memori + Kedudukan;
        for (int 칸 = 0; 칸 < 원본[0]; 칸++) {
            if (Kedudukan >= 2047) return 126;
            argumen_Memori[Kedudukan++] = 원본[칸 + 1];
        }
        argumen_Memori[Kedudukan++] = 0;
    }
    argumen_Senarai[item_COUNT + 1] = 0;
    return main(item_COUNT + 1, argumen_Senarai);
}
