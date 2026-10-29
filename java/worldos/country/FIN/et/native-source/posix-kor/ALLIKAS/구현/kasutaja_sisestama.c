#include "호출경계.h"
extern int main(int 인수개수, char **argument_Loend);
static char argument_Mälu[2048];
static char *argument_Loend[18];
int jkoros_main(void) {
    int kaup_COUNT = jkoros_syscall(2, 0, 0, 0, 0, 0);
    if (kaup_COUNT < 0 || kaup_COUNT > 16) return 126;
    /* tähtaja_piires_kaup 커널의 argv는 Täida_käsk 이름을 제외한다. C argv[0]은 고정 식별 이름이다. */
    argument_Loend[0] = "jkoros-app";
    int Asukoht = 0;
    for (int INDEX = 0; INDEX < kaup_COUNT; INDEX++) {
        const int *원본 = (const int *)jkoros_syscall(3, INDEX, 0, 0, 0, 0);
        if (!원본 || 원본[0] < 0 || 원본[0] > 127) return 126;
        argument_Loend[INDEX + 1] = argument_Mälu + Asukoht;
        for (int 칸 = 0; 칸 < 원본[0]; 칸++) {
            if (Asukoht >= 2047) return 126;
            argument_Mälu[Asukoht++] = 원본[칸 + 1];
        }
        argument_Mälu[Asukoht++] = 0;
    }
    argument_Loend[kaup_COUNT + 1] = 0;
    return main(kaup_COUNT + 1, argument_Loend);
}
