#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *ສະຕຣິງ_ຄ່າ) { size_t ຄວາມຍາວ_ຄ່າ = 0; while (ສະຕຣິງ_ຄ່າ[ຄວາມຍາວ_ຄ່າ]) ຄວາມຍາວ_ຄ່າ++; return ຄວາມຍາວ_ຄ່າ; }
int strcmp(const char *ດ້ານຫນ້າ_ຄ່າ, const char *ກັບ_ຄືນ_ຄ່າ) {
    while (*ດ້ານຫນ້າ_ຄ່າ && *ດ້ານຫນ້າ_ຄ່າ == *ກັບ_ຄືນ_ຄ່າ) { ດ້ານຫນ້າ_ຄ່າ++; ກັບ_ຄືນ_ຄ່າ++; }
    return (unsigned char)*ດ້ານຫນ້າ_ຄ່າ - (unsigned char)*ກັບ_ຄືນ_ຄ່າ;
}
int memcmp(const void *ດ້ານຫນ້າ_ຄ່າ, const void *ກັບ_ຄືນ_ຄ່າ, size_t 바이트수) {
    const unsigned char *가 = ດ້ານຫນ້າ_ຄ່າ, *나 = ກັບ_ຄືນ_ຄ່າ;
    for (size_t ຊ່ອງ_ເຂົ້າໃນ = 0; ຊ່ອງ_ເຂົ້າໃນ < 바이트수; ຊ່ອງ_ເຂົ້າໃນ++) if (가[ຊ່ອງ_ເຂົ້າໃນ] != 나[ຊ່ອງ_ເຂົ້າໃນ]) return 가[ຊ່ອງ_ເຂົ້າໃນ] - 나[ຊ່ອງ_ເຂົ້າໃນ];
    return 0;
}
void *memcpy(void *ປາຍທາງ_ຄ່າ, const void *원본, size_t 바이트수) {
    unsigned char *가 = ປາຍທາງ_ຄ່າ; const unsigned char *나 = 원본;
    for (size_t ຊ່ອງ_ເຂົ້າໃນ = 0; ຊ່ອງ_ເຂົ້າໃນ < 바이트수; ຊ່ອງ_ເຂົ້າໃນ++) 가[ຊ່ອງ_ເຂົ້າໃນ] = 나[ຊ່ອງ_ເຂົ້າໃນ];
    return ປາຍທາງ_ຄ່າ;
}
void *memset(void *ປາຍທາງ_ຄ່າ, int ຄ່າ, size_t 바이트수) {
    unsigned char *ຂໍ້ມູນ = ປາຍທາງ_ຄ່າ;
    for (size_t ຊ່ອງ_ເຂົ້າໃນ = 0; ຊ່ອງ_ເຂົ້າໃນ < 바이트수; ຊ່ອງ_ເຂົ້າໃນ++) ຂໍ້ມູນ[ຊ່ອງ_ເຂົ້າໃນ] = ຄ່າ;
    return ປາຍທາງ_ຄ່າ;
}
int putchar(int 문자) { unsigned char ຄ່າ = 문자; return write(1, &ຄ່າ, 1) == 1 ? ຄ່າ : EOF; }
int puts(const char *ສະຕຣິງ_ຄ່າ) {
    size_t ຄວາມຍາວ_ຄ່າ = strlen(ສະຕຣິງ_ຄ່າ), ຈັດຕໍາແຫນ່ງ = 0;
    while (ຈັດຕໍາແຫນ່ງ < ຄວາມຍາວ_ຄ່າ) { ssize_t ມາດຕະການ = write(1, ສະຕຣິງ_ຄ່າ + ຈັດຕໍາແຫນ່ງ, ຄວາມຍາວ_ຄ່າ - ຈັດຕໍາແຫນ່ງ); if (ມາດຕະການ <= 0) return EOF; ຈັດຕໍາແຫນ່ງ += ມາດຕະການ; }
    return putchar('\n') == EOF ? EOF : 0;
}
