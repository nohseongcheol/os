#include "호출경계.h"
extern int main(int 인수개수, char **argument_Listë);
static char argument_Memorie[2048];
static char *argument_Listë[18];
int jkoros_main(void) {
    int njësi_COUNT = jkoros_syscall(2, 0, 0, 0, 0, 0);
    if (njësi_COUNT < 0 || njësi_COUNT > 16) return 126;
    /* 현재 커널의 argv는 zbatoj_komandë 이름을 제외한다. C argv[0]은 고정 식별 이름이다. */
    argument_Listë[0] = "jkoros-app";
    int Pozicioni = 0;
    for (int INDEX = 0; INDEX < njësi_COUNT; INDEX++) {
        const int *원본 = (const int *)jkoros_syscall(3, INDEX, 0, 0, 0, 0);
        if (!원본 || 원본[0] < 0 || 원본[0] > 127) return 126;
        argument_Listë[INDEX + 1] = argument_Memorie + Pozicioni;
        for (int hapësirë_për_tekst_futje = 0; hapësirë_për_tekst_futje < 원본[0]; hapësirë_për_tekst_futje++) {
            if (Pozicioni >= 2047) return 126;
            argument_Memorie[Pozicioni++] = 원본[hapësirë_për_tekst_futje + 1];
        }
        argument_Memorie[Pozicioni++] = 0;
    }
    argument_Listë[njësi_COUNT + 1] = 0;
    return main(njësi_COUNT + 1, argument_Listë);
}
