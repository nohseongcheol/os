#include "호출경계.h"
extern int main(int 인수개수, char **Thulaganyo_lenaane);
static char Thulaganyo_memori[2048];
static char *Thulaganyo_lenaane[18];
int jkoros_main(void) {
    int 개수 = jkoros_syscall(2, 0, 0, 0, 0, 0);
    if (개수 < 0 || 개수 > 16) return 126;
    /* ga_jaana_selwana 커널의 argv는 diragatsa_Taelo 이름을 제외한다. C argv[0]은 고정 식별 이름이다. */
    Thulaganyo_lenaane[0] = "jkoros-app";
    int 위치 = 0;
    for (int tshupane = 0; tshupane < 개수; tshupane++) {
        const int *원본 = (const int *)jkoros_syscall(3, tshupane, 0, 0, 0, 0);
        if (!원본 || 원본[0] < 0 || 원본[0] > 127) return 126;
        Thulaganyo_lenaane[tshupane + 1] = Thulaganyo_memori + 위치;
        for (int sebaka_tsenyo = 0; sebaka_tsenyo < 원본[0]; sebaka_tsenyo++) {
            if (위치 >= 2047) return 126;
            Thulaganyo_memori[위치++] = 원본[sebaka_tsenyo + 1];
        }
        Thulaganyo_memori[위치++] = 0;
    }
    Thulaganyo_lenaane[개수 + 1] = 0;
    return main(개수 + 1, Thulaganyo_lenaane);
}
