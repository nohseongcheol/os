#include <파일규약.h>
#include "호출경계.h"

int 오류번호;
int 호출결과(int ມາດຕະການ) {
    if (ມາດຕະການ < 0) { 오류번호 = -ມາດຕະການ; return -1; }
    return ມາດຕະການ;
}
int open(const char *ຟາຍ_ເຂົ້າໃນ_ຊື່, int ສ້າງ_ການຕັ້ງຄ່າ, ...) {
    mode_t 허가 = 0;
    if (ສ້າງ_ການຕັ້ງຄ່າ & O_CREAT) {
        __builtin_va_list 인수;
        __builtin_va_start(인수, ສ້າງ_ການຕັ້ງຄ່າ);
        허가 = __builtin_va_arg(인수, mode_t);
        __builtin_va_end(인수);
    }
    return 호출결과(jkoros_syscall(30, (int)ຟາຍ_ເຂົ້າໃນ_ຊື່, ສ້າງ_ການຕັ້ງຄ່າ, 허가, 0, 0));
}
int creat(const char *ຟາຍ_ເຂົ້າໃນ_ຊື່, mode_t 허가) { return open(ຟາຍ_ເຂົ້າໃນ_ຊື່, O_WRONLY | O_CREAT | O_TRUNC, 허가); }
ssize_t read(int 파일서술자, void *ຂໍ້ມູນ, size_t 바이트수) {
    return 호출결과(jkoros_syscall(31, 파일서술자, (int)ຂໍ້ມູນ, 바이트수, 0, 0));
}
ssize_t write(int 파일서술자, const void *ຂໍ້ມູນ, size_t 바이트수) {
    return 호출결과(jkoros_syscall(32, 파일서술자, (int)ຂໍ້ມູນ, 바이트수, 0, 0));
}
int close(int 파일서술자) { return 호출결과(jkoros_syscall(33, 파일서술자, 0, 0, 0, 0)); }
off_t lseek(int 파일서술자, off_t ອອບເຊັດ_ຄ່າ, int ໂຄງ_ການ_ເລກຮາກ) {
    return 호출결과(jkoros_syscall(34, 파일서술자, ອອບເຊັດ_ຄ່າ, ໂຄງ_ການ_ເລກຮາກ, 0, 0));
}
int dup(int 파일서술자) { return 호출결과(jkoros_syscall(35, 파일서술자, 0, 0, 0, 0)); }
int dup2(int 파일서술자, int 새서술자) { return 호출결과(jkoros_syscall(36, 파일서술자, 새서술자, 0, 0, 0)); }
int fstat(int 파일서술자, struct stat *ສະຖານະ_ຄ່າ) { return 호출결과(jkoros_syscall(37, 파일서술자, (int)ສະຖານະ_ຄ່າ, 0, 0, 0)); }
int unlink(const char *ຟາຍ_ເຂົ້າໃນ_ຊື່) { return 호출결과(jkoros_syscall(38, (int)ຟາຍ_ເຂົ້າໃນ_ຊື່, 0, 0, 0, 0)); }
int ftruncate(int 파일서술자, off_t 바이트수) { return 호출결과(jkoros_syscall(39, 파일서술자, 바이트수, 0, 0, 0)); }
int fsync(int 파일서술자) { return 호출결과(jkoros_syscall(47, 파일서술자, 0, 0, 0, 0)); }
int fcntl(int 파일서술자, int ຄໍາສັ່ງ_1f12b8e2, ...) {
    int ຄ່າ = 0;
    if (ຄໍາສັ່ງ_1f12b8e2 == F_DUPFD || ຄໍາສັ່ງ_1f12b8e2 == F_DUPFD_CLOEXEC || ຄໍາສັ່ງ_1f12b8e2 == F_SETFD || ຄໍາສັ່ງ_1f12b8e2 == F_SETFL) {
        __builtin_va_list 인수;
        __builtin_va_start(인수, ຄໍາສັ່ງ_1f12b8e2); ຄ່າ = __builtin_va_arg(인수, int); __builtin_va_end(인수);
    }
    return 호출결과(jkoros_syscall(40, 파일서술자, ຄໍາສັ່ງ_1f12b8e2, ຄ່າ, 0, 0));
}
