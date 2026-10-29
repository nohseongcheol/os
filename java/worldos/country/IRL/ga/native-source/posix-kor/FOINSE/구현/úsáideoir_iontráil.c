#include "호출경계.h"
extern int main(int 인수개수, char **argóint_Liosta);
static char argóint_Cuimhne[2048];
static char *argóint_Liosta[18];
int jkoros_main(void) {
    int mír_COUNT = jkoros_syscall(2, 0, 0, 0, 0, 0);
    if (mír_COUNT < 0 || mír_COUNT > 16) return 126;
    /* 현재 커널의 argv는 Rith_ordú 이름을 제외한다. C argv[0]은 고정 식별 이름이다. */
    argóint_Liosta[0] = "jkoros-app";
    int suíomh = 0;
    for (int INDEX = 0; INDEX < mír_COUNT; INDEX++) {
        const int *원본 = (const int *)jkoros_syscall(3, INDEX, 0, 0, 0, 0);
        if (!원본 || 원본[0] < 0 || 원본[0] > 127) return 126;
        argóint_Liosta[INDEX + 1] = argóint_Cuimhne + suíomh;
        for (int spás_iontráil = 0; spás_iontráil < 원본[0]; spás_iontráil++) {
            if (suíomh >= 2047) return 126;
            argóint_Cuimhne[suíomh++] = 원본[spás_iontráil + 1];
        }
        argóint_Cuimhne[suíomh++] = 0;
    }
    argóint_Liosta[mír_COUNT + 1] = 0;
    return main(mír_COUNT + 1, argóint_Liosta);
}
