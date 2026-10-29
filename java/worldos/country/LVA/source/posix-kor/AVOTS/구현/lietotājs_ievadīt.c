#include "호출경계.h"
extern int main(int 인수개수, char **arg_Saraksts);
static char arg_atmiņa[2048];
static char *arg_Saraksts[18];
int jkoros_main(void) {
    int krājums_COUNT = jkoros_syscall(2, 0, 0, 0, 0, 0);
    if (krājums_COUNT < 0 || krājums_COUNT > 16) return 126;
    /* pašreizējais_krājums 커널의 argv는 Izpildīt_komanda 이름을 제외한다. C argv[0]은 고정 식별 이름이다. */
    arg_Saraksts[0] = "jkoros-app";
    int Novietojums = 0;
    for (int INDEX = 0; INDEX < krājums_COUNT; INDEX++) {
        const int *원본 = (const int *)jkoros_syscall(3, INDEX, 0, 0, 0, 0);
        if (!원본 || 원본[0] < 0 || 원본[0] > 127) return 126;
        arg_Saraksts[INDEX + 1] = arg_atmiņa + Novietojums;
        for (int 칸 = 0; 칸 < 원본[0]; 칸++) {
            if (Novietojums >= 2047) return 126;
            arg_atmiņa[Novietojums++] = 원본[칸 + 1];
        }
        arg_atmiņa[Novietojums++] = 0;
    }
    arg_Saraksts[krājums_COUNT + 1] = 0;
    return main(krājums_COUNT + 1, arg_Saraksts);
}
