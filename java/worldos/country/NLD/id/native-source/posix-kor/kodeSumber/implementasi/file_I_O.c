#include <파일규약.h>
#include "호출경계.h"

int nomor_kesalahan;
int 호출결과(int hasil) {
    if (hasil < 0) { nomor_kesalahan = -hasil; return -1; }
    return hasil;
}
int open(const char *file_entri_nama, int buat_Pengaturan, ...) {
    mode_t 허가 = 0;
    if (buat_Pengaturan & O_CREAT) {
        __builtin_va_list argumen;
        __builtin_va_start(argumen, buat_Pengaturan);
        허가 = __builtin_va_arg(argumen, mode_t);
        __builtin_va_end(argumen);
    }
    return 호출결과(jkoros_syscall(30, (int)file_entri_nama, buat_Pengaturan, 허가, 0, 0));
}
int creat(const char *file_entri_nama, mode_t 허가) { return open(file_entri_nama, O_WRONLY | O_CREAT | O_TRUNC, 허가); }
ssize_t read(int 파일서술자, void *data, size_t byte_COUNT) {
    return 호출결과(jkoros_syscall(31, 파일서술자, (int)data, byte_COUNT, 0, 0));
}
ssize_t write(int 파일서술자, const void *data, size_t byte_COUNT) {
    return 호출결과(jkoros_syscall(32, 파일서술자, (int)data, byte_COUNT, 0, 0));
}
int close(int 파일서술자) { return 호출결과(jkoros_syscall(33, 파일서술자, 0, 0, 0, 0)); }
off_t lseek(int 파일서술자, off_t OFFSET_VALUE, int Tugas_akar) {
    return 호출결과(jkoros_syscall(34, 파일서술자, OFFSET_VALUE, Tugas_akar, 0, 0));
}
int dup(int 파일서술자) { return 호출결과(jkoros_syscall(35, 파일서술자, 0, 0, 0, 0)); }
int dup2(int 파일서술자, int 새서술자) { return 호출결과(jkoros_syscall(36, 파일서술자, 새서술자, 0, 0, 0)); }
int fstat(int 파일서술자, struct stat *Status_VALUE) { return 호출결과(jkoros_syscall(37, 파일서술자, (int)Status_VALUE, 0, 0, 0)); }
int unlink(const char *file_entri_nama) { return 호출결과(jkoros_syscall(38, (int)file_entri_nama, 0, 0, 0, 0)); }
int ftruncate(int 파일서술자, off_t byte_COUNT) { return 호출결과(jkoros_syscall(39, 파일서술자, byte_COUNT, 0, 0, 0)); }
int fsync(int 파일서술자) { return 호출결과(jkoros_syscall(47, 파일서술자, 0, 0, 0, 0)); }
int fcntl(int 파일서술자, int perintah, ...) {
    int VALUE = 0;
    if (perintah == F_DUPFD || perintah == F_DUPFD_CLOEXEC || perintah == F_SETFD || perintah == F_SETFL) {
        __builtin_va_list argumen;
        __builtin_va_start(argumen, perintah); VALUE = __builtin_va_arg(argumen, int); __builtin_va_end(argumen);
    }
    return 호출결과(jkoros_syscall(40, 파일서술자, perintah, VALUE, 0, 0));
}
