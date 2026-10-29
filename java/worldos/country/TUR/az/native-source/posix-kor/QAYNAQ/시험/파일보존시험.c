#include <파일규약.h>
#include <stdio.h>
int main(int element_COUNT, char **daxiletmə_Siyahı) {
    (void)element_COUNT; (void)daxiletmə_Siyahı;
    int FAYL = açmaq_fayl("stored.txt", oxunan_yazılan | 없으면만들기 | 내용비우기, 0600);
    if (FAYL < 0 || yazmaq_fayl_verilənlər(FAYL, "saved-from-C", 12) != 12) return 1;
    if (파일저장확정(FAYL) < 0) return 2;
    if (bağlamaq_fayl(FAYL) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}
