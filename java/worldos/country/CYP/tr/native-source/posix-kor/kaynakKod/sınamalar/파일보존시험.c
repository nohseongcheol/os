#include <Dosya_ABI.h>
#include <stdio.h>
int main(int öğe_BAĞ_DEĞ_SAY, char **girdi_Liste) {
    (void)öğe_BAĞ_DEĞ_SAY; (void)girdi_Liste;
    int dosya = açık_Dosya("stored.txt", R_W | 없으면만들기 | kesmek_içindekiler, 0600);
    if (dosya < 0 || yazma_Dosya_veri(dosya, "saved-from-C", 12) != 12) return 1;
    if (commit_Dosyalar(dosya) < 0) return 2;
    if (Kapat_Dosya(dosya) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}
