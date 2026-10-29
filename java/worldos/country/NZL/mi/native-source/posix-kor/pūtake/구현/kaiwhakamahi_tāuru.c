#include "호출경계.h"
extern int main(int 인수개수, char **tohenga_Rārangi);
static char tohenga_Pūmahara[2048];
static char *tohenga_Rārangi[18];
int jkoros_main(void) {
    int tuemi_COUNT = jkoros_syscall(2, 0, 0, 0, 0, 0);
    if (tuemi_COUNT < 0 || tuemi_COUNT > 16) return 126;
    /* 현재 커널의 argv는 kawe_tono 이름을 제외한다. C argv[0]은 고정 식별 이름이다. */
    tohenga_Rārangi[0] = "jkoros-app";
    int tūranga = 0;
    for (int INDEX = 0; INDEX < tuemi_COUNT; INDEX++) {
        const int *원본 = (const int *)jkoros_syscall(3, INDEX, 0, 0, 0, 0);
        if (!원본 || 원본[0] < 0 || 원본[0] > 127) return 126;
        tohenga_Rārangi[INDEX + 1] = tohenga_Pūmahara + tūranga;
        for (int kāniwha_tāurunga = 0; kāniwha_tāurunga < 원본[0]; kāniwha_tāurunga++) {
            if (tūranga >= 2047) return 126;
            tohenga_Pūmahara[tūranga++] = 원본[kāniwha_tāurunga + 1];
        }
        tohenga_Pūmahara[tūranga++] = 0;
    }
    tohenga_Rārangi[tuemi_COUNT + 1] = 0;
    return main(tuemi_COUNT + 1, tohenga_Rārangi);
}
