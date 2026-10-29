#include "호출경계.h"
extern int main(int 인수개수, char **akumente_Lenaneo);
static char akumente_memori[2048];
static char *akumente_Lenaneo[18];
int jkoros_main(void) {
    int 개수 = jkoros_syscall(2, 0, 0, 0, 0, 0);
    if (개수 < 0 || 개수 > 16) return 126;
    /* 현재 커널의 argv는 phethagatša_taelo 이름을 제외한다. C argv[0]은 고정 식별 이름이다. */
    akumente_Lenaneo[0] = "jkoros-app";
    int 위치 = 0;
    for (int lokela = 0; lokela < 개수; lokela++) {
        const int *원본 = (const int *)jkoros_syscall(3, lokela, 0, 0, 0, 0);
        if (!원본 || 원본[0] < 0 || 원본[0] > 127) return 126;
        akumente_Lenaneo[lokela + 1] = akumente_memori + 위치;
        for (int sekgobana_go_tsenya_tshedimošo = 0; sekgobana_go_tsenya_tshedimošo < 원본[0]; sekgobana_go_tsenya_tshedimošo++) {
            if (위치 >= 2047) return 126;
            akumente_memori[위치++] = 원본[sekgobana_go_tsenya_tshedimošo + 1];
        }
        akumente_memori[위치++] = 0;
    }
    akumente_Lenaneo[개수 + 1] = 0;
    return main(개수 + 1, akumente_Lenaneo);
}
