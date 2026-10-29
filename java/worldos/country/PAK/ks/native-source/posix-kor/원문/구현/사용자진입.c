#include "호출경계.h"
extern int main(int 인수개수, char **인수목록);
static char 인수기억[2048];
static char *인수목록[18];
int jkoros_main(void) {
    int 개수 = jkoros_syscall(2, 0, 0, 0, 0, 0);
    if (개수 < 0 || 개수 > 16) return 126;
    /* 현재 커널의 argv는 실행 이름을 제외한다. C argv[0]은 고정 식별 이름이다. */
    인수목록[0] = "jkoros-app";
    int जाय_प्य्यटठ = 0;
    for (int 번호 = 0; 번호 < 개수; 번호++) {
        const int *원본 = (const int *)jkoros_syscall(3, 번호, 0, 0, 0, 0);
        if (!원본 || 원본[0] < 0 || 원본[0] > 127) return 126;
        인수목록[번호 + 1] = 인수기억 + जाय_प्य्यटठ;
        for (int 칸 = 0; 칸 < 원본[0]; 칸++) {
            if (जाय_प्य्यटठ >= 2047) return 126;
            인수기억[जाय_प्य्यटठ++] = 원본[칸 + 1];
        }
        인수기억[जाय_प्य्यटठ++] = 0;
    }
    인수목록[개수 + 1] = 0;
    return main(개수 + 1, 인수목록);
}
