#include <파일규약.h>
#include <stdio.h>
int main(int element_COUNT, char **kiritish_Ro_yxat) {
    (void)element_COUNT; (void)kiritish_Ro_yxat;
    int Fayl = ochmoq_fayl("stored.txt", o_qish_yozish_mumkin | 없으면만들기 | 내용비우기, 0600);
    if (Fayl < 0 || yozmoq_fayl_ma_lumotlar(Fayl, "saved-from-C", 12) != 12) return 1;
    if (파일저장확정(Fayl) < 0) return 2;
    if (yopmoq_fayl(Fayl) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}
