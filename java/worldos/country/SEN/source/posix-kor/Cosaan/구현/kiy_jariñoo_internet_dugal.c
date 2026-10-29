#include "호출경계.h"
extern int main(int 인수개수, char **Tegtal_lim);
static char Tegtal_fatlekookaay[2048];
static char *Tegtal_lim[18];
int jkoros_main(void) {
    int 개수 = jkoros_syscall(2, 0, 0, 0, 0, 0);
    if (개수 < 0 || 개수 > 16) return 126;
    /* 현재 커널의 argv는 def_ndigel 이름을 제외한다. C argv[0]은 고정 식별 이름이다. */
    Tegtal_lim[0] = "jkoros-app";
    int 위치 = 0;
    for (int àlluwa_tur = 0; àlluwa_tur < 개수; àlluwa_tur++) {
        const int *원본 = (const int *)jkoros_syscall(3, àlluwa_tur, 0, 0, 0, 0);
        if (!원본 || 원본[0] < 0 || 원본[0] > 127) return 126;
        Tegtal_lim[àlluwa_tur + 1] = Tegtal_fatlekookaay + 위치;
        for (int xar_xar_dugal_xabaar = 0; xar_xar_dugal_xabaar < 원본[0]; xar_xar_dugal_xabaar++) {
            if (위치 >= 2047) return 126;
            Tegtal_fatlekookaay[위치++] = 원본[xar_xar_dugal_xabaar + 1];
        }
        Tegtal_fatlekookaay[위치++] = 0;
    }
    Tegtal_lim[개수 + 1] = 0;
    return main(개수 + 1, Tegtal_lim);
}
