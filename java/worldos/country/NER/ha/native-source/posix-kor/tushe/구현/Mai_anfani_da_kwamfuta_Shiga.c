#include "호출경계.h"
extern int main(int 인수개수, char **Tubalin_aiki_Jeri);
static char Tubalin_aiki_Mahardatar_kwamfuta[2048];
static char *Tubalin_aiki_Jeri[18];
int jkoros_main(void) {
    int 개수 = jkoros_syscall(2, 0, 0, 0, 0, 0);
    if (개수 < 0 || 개수 > 16) return 126;
    /* 현재 커널의 argv는 gudanar_Umarni 이름을 제외한다. C argv[0]은 고정 식별 이름이다. */
    Tubalin_aiki_Jeri[0] = "jkoros-app";
    int 위치 = 0;
    for (int Indes = 0; Indes < 개수; Indes++) {
        const int *원본 = (const int *)jkoros_syscall(3, Indes, 0, 0, 0, 0);
        if (!원본 || 원본[0] < 0 || 원본[0] > 127) return 126;
        Tubalin_aiki_Jeri[Indes + 1] = Tubalin_aiki_Mahardatar_kwamfuta + 위치;
        for (int rami_Mashigar_bayanai = 0; rami_Mashigar_bayanai < 원본[0]; rami_Mashigar_bayanai++) {
            if (위치 >= 2047) return 126;
            Tubalin_aiki_Mahardatar_kwamfuta[위치++] = 원본[rami_Mashigar_bayanai + 1];
        }
        Tubalin_aiki_Mahardatar_kwamfuta[위치++] = 0;
    }
    Tubalin_aiki_Jeri[개수 + 1] = 0;
    return main(개수 + 1, Tubalin_aiki_Jeri);
}
