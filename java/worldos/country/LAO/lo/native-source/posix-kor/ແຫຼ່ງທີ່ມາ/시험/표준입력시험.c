#include <파일규약.h>
#include <stdio.h>
#include <string.h>
int main(int 개수, char **ເຂົ້າໃນ_ລາຍຊື່) {
    (void)개수; (void)ເຂົ້າໃນ_ລາຍຊື່;
    char ຂໍ້ມູນ[6]; int ຄວາມຍາວ_ຄ່າ = 0;
    puts("POSIX INPUT READY");
    while (ຄວາມຍາວ_ຄ່າ < 6) {
        int ມາດຕະການ = 파일자료읽기(0, ຂໍ້ມູນ + ຄວາມຍາວ_ຄ່າ, 6 - ຄວາມຍາວ_ຄ່າ);
        if (ມາດຕະການ <= 0) return 1;
        ຄວາມຍາວ_ຄ່າ += ມາດຕະການ;
    }
    if (memcmp(ຂໍ້ມູນ, "abcdef", 6)) return 2;
    puts("POSIX INPUT PASS");
    return 0;
}
