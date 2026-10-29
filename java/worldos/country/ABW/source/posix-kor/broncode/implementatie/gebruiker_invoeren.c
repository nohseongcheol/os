#include "Bellen_grens.h"
extern int main(int 인수개수, char **argument_Lijst);
static char argument_Geheugen[2048];
static char *argument_Lijst[18];
int jkoros_main(void) {
    int item_AANTAL = jkoros_syscall(2, 0, 0, 0, 0, 0);
    if (item_AANTAL < 0 || item_AANTAL > 16) return 126;
    /* actueel_item 커널의 argv는 Uitvoeren_opdracht 이름을 제외한다. C argv[0]은 고정 식별 이름이다. */
    argument_Lijst[0] = "jkoros-app";
    int positie = 0;
    for (int INDEX = 0; INDEX < item_AANTAL; INDEX++) {
        const int *원본 = (const int *)jkoros_syscall(3, INDEX, 0, 0, 0, 0);
        if (!원본 || 원본[0] < 0 || 원본[0] > 127) return 126;
        argument_Lijst[INDEX + 1] = argument_Geheugen + positie;
        for (int sleuf_invoer = 0; sleuf_invoer < 원본[0]; sleuf_invoer++) {
            if (positie >= 2047) return 126;
            argument_Geheugen[positie++] = 원본[sleuf_invoer + 1];
        }
        argument_Geheugen[positie++] = 0;
    }
    argument_Lijst[item_AANTAL + 1] = 0;
    return main(item_AANTAL + 1, argument_Lijst);
}
