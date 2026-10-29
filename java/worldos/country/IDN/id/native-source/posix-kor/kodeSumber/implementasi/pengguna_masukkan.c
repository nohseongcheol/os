#include "호출경계.h"
extern int main(int 인수개수, char **argumen_Daftar);
static char argumen_Memori[2048];
static char *argumen_Daftar[18];
int jkoros_main(void) {
    int item_COUNT = jkoros_syscall(2, 0, 0, 0, 0, 0);
    if (item_COUNT < 0 || item_COUNT > 16) return 126;
    /* saat_ini_item 커널의 argv는 Jalankan_perintah 이름을 제외한다. C argv[0]은 고정 식별 이름이다. */
    argumen_Daftar[0] = "jkoros-app";
    int posisi = 0;
    for (int INDEX = 0; INDEX < item_COUNT; INDEX++) {
        const int *원본 = (const int *)jkoros_syscall(3, INDEX, 0, 0, 0, 0);
        if (!원본 || 원본[0] < 0 || 원본[0] > 127) return 126;
        argumen_Daftar[INDEX + 1] = argumen_Memori + posisi;
        for (int slot_entri = 0; slot_entri < 원본[0]; slot_entri++) {
            if (posisi >= 2047) return 126;
            argumen_Memori[posisi++] = 원본[slot_entri + 1];
        }
        argumen_Memori[posisi++] = 0;
    }
    argumen_Daftar[item_COUNT + 1] = 0;
    return main(item_COUNT + 1, argumen_Daftar);
}
