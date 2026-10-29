#include <파일규약.h>
#include <stdio.h>
int main(int vare_TÆL, char **post_Liste) {
    (void)vare_TÆL; (void)post_Liste;
    int Fil = åben_fil("stored.txt", læse_skrive | 없으면만들기 | afkorte_Indhold, 0600);
    if (Fil < 0 || skrive_fil_data(Fil, "saved-from-C", 12) != 12) return 1;
    if (udføre_Files(Fil) < 0) return 2;
    if (Luk_fil(Fil) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}
