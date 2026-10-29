#include <파일규약.h>
#include <stdio.h>
int main(int 개수, char **ເຂົ້າໃນ_ລາຍຊື່) {
    (void)개수; (void)ເຂົ້າໃນ_ລາຍຊື່;
    int ຟາຍ = ສ້າງ_ຟາຍ("stored.txt", ອ່ານ_ຂຽນ | 없으면만들기 | 내용비우기, 0600);
    if (ຟາຍ < 0 || ຂຽນ_ຟາຍ_ຂໍ້ມູນ(ຟາຍ, "saved-from-C", 12) != 12) return 1;
    if (파일저장확정(ຟາຍ) < 0) return 2;
    if (ປິດ_ຟາຍ(ຟາຍ) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}
