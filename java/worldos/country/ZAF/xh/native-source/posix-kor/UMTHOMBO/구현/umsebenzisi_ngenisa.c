#include "호출경계.h"
extern int main(int 인수개수, char **isiniki_myalelo_uludwe);
static char isiniki_myalelo_imemori[2048];
static char *isiniki_myalelo_uludwe[18];
int jkoros_main(void) {
    int 개수 = jkoros_syscall(2, 0, 0, 0, 0, 0);
    if (개수 < 0 || 개수 > 16) return 126;
    /* 현재 커널의 argv는 ukwenza_umyalelo 이름을 제외한다. C argv[0]은 고정 식별 이름이다. */
    isiniki_myalelo_uludwe[0] = "jkoros-app";
    int 위치 = 0;
    for (int indeksa = 0; indeksa < 개수; indeksa++) {
        const int *원본 = (const int *)jkoros_syscall(3, indeksa, 0, 0, 0, 0);
        if (!원본 || 원본[0] < 0 || 원본[0] > 127) return 126;
        isiniki_myalelo_uludwe[indeksa + 1] = isiniki_myalelo_imemori + 위치;
        for (int isithuba_ufako_nkcukacha = 0; isithuba_ufako_nkcukacha < 원본[0]; isithuba_ufako_nkcukacha++) {
            if (위치 >= 2047) return 126;
            isiniki_myalelo_imemori[위치++] = 원본[isithuba_ufako_nkcukacha + 1];
        }
        isiniki_myalelo_imemori[위치++] = 0;
    }
    isiniki_myalelo_uludwe[개수 + 1] = 0;
    return main(개수 + 1, isiniki_myalelo_uludwe);
}
