#include "호출경계.h"
extern int main(int 인수개수, char **arg_Llista);
static char arg_Memòria[2048];
static char *arg_Llista[18];
int jkoros_main(void) {
    int element_COMPT = jkoros_syscall(2, 0, 0, 0, 0, 0);
    if (element_COMPT < 0 || element_COMPT > 16) return 126;
    /* 현재 커널의 argv는 Executa_ordre 이름을 제외한다. C argv[0]은 고정 식별 이름이다. */
    arg_Llista[0] = "jkoros-app";
    int Posició = 0;
    for (int INDEX = 0; INDEX < element_COMPT; INDEX++) {
        const int *원본 = (const int *)jkoros_syscall(3, INDEX, 0, 0, 0, 0);
        if (!원본 || 원본[0] < 0 || 원본[0] > 127) return 126;
        arg_Llista[INDEX + 1] = arg_Memòria + Posició;
        for (int 칸 = 0; 칸 < 원본[0]; 칸++) {
            if (Posició >= 2047) return 126;
            arg_Memòria[Posició++] = 원본[칸 + 1];
        }
        arg_Memòria[Posició++] = 0;
    }
    arg_Llista[element_COMPT + 1] = 0;
    return main(element_COMPT + 1, arg_Llista);
}
