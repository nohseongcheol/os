#include "호출경계.h"
extern int main(int 인수개수, char **Argument_Lëscht);
static char Argument_Späicher[2048];
static char *Argument_Lëscht[18];
int jkoros_main(void) {
    int Element_COUNT = jkoros_syscall(2, 0, 0, 0, 0, 0);
    if (Element_COUNT < 0 || Element_COUNT > 16) return 126;
    /* 현재 커널의 argv는 ausféieren_Befeel 이름을 제외한다. C argv[0]은 고정 식별 이름이다. */
    Argument_Lëscht[0] = "jkoros-app";
    int positionéieren = 0;
    for (int INDEX = 0; INDEX < Element_COUNT; INDEX++) {
        const int *원본 = (const int *)jkoros_syscall(3, INDEX, 0, 0, 0, 0);
        if (!원본 || 원본[0] < 0 || 원본[0] > 127) return 126;
        Argument_Lëscht[INDEX + 1] = Argument_Späicher + positionéieren;
        for (int Slot_Agab = 0; Slot_Agab < 원본[0]; Slot_Agab++) {
            if (positionéieren >= 2047) return 126;
            Argument_Späicher[positionéieren++] = 원본[Slot_Agab + 1];
        }
        Argument_Späicher[positionéieren++] = 0;
    }
    Argument_Lëscht[Element_COUNT + 1] = 0;
    return main(Element_COUNT + 1, Argument_Lëscht);
}
