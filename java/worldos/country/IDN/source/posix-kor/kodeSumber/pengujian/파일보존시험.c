#include <파일규약.h>
#include <stdio.h>
int main(int item_COUNT, char **entri_Daftar) {
    (void)item_COUNT; (void)entri_Daftar;
    int berkas = buat_file("stored.txt", baca_tulis | 없으면만들기 | 내용비우기, 0600);
    if (berkas < 0 || tulis_file_data(berkas, "saved-from-C", 12) != 12) return 1;
    if (penerapan_Files(berkas) < 0) return 2;
    if (Tutup_file(berkas) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}
