#include <파일규약.h>
#include "호출경계.h"

int villa_númer;
int 호출결과(int NIÐURSTAÐA) {
    if (NIÐURSTAÐA < 0) { villa_númer = -NIÐURSTAÐA; return -1; }
    return NIÐURSTAÐA;
}
int open(const char *skrá_færsla_heiti, int opið_Stillingar, ...) {
    mode_t 허가 = 0;
    if (opið_Stillingar & O_CREAT) {
        __builtin_va_list Viðföng;
        __builtin_va_start(Viðföng, opið_Stillingar);
        허가 = __builtin_va_arg(Viðföng, mode_t);
        __builtin_va_end(Viðföng);
    }
    return 호출결과(jkoros_syscall(30, (int)skrá_færsla_heiti, opið_Stillingar, 허가, 0, 0));
}
int creat(const char *skrá_færsla_heiti, mode_t 허가) { return open(skrá_færsla_heiti, O_WRONLY | O_CREAT | O_TRUNC, 허가); }
ssize_t read(int 파일서술자, void *gögn, size_t bæti_COUNT) {
    return 호출결과(jkoros_syscall(31, 파일서술자, (int)gögn, bæti_COUNT, 0, 0));
}
ssize_t write(int 파일서술자, const void *gögn, size_t bæti_COUNT) {
    return 호출결과(jkoros_syscall(32, 파일서술자, (int)gögn, bæti_COUNT, 0, 0));
}
int close(int 파일서술자) { return 호출결과(jkoros_syscall(33, 파일서술자, 0, 0, 0, 0)); }
off_t lseek(int 파일서술자, off_t OFFSET_VALUE, int verk_rót) {
    return 호출결과(jkoros_syscall(34, 파일서술자, OFFSET_VALUE, verk_rót, 0, 0));
}
int dup(int 파일서술자) { return 호출결과(jkoros_syscall(35, 파일서술자, 0, 0, 0, 0)); }
int dup2(int 파일서술자, int 새서술자) { return 호출결과(jkoros_syscall(36, 파일서술자, 새서술자, 0, 0, 0)); }
int fstat(int 파일서술자, struct stat *staða_VALUE_e10195a1) { return 호출결과(jkoros_syscall(37, 파일서술자, (int)staða_VALUE_e10195a1, 0, 0, 0)); }
int unlink(const char *skrá_færsla_heiti) { return 호출결과(jkoros_syscall(38, (int)skrá_færsla_heiti, 0, 0, 0, 0)); }
int ftruncate(int 파일서술자, off_t bæti_COUNT) { return 호출결과(jkoros_syscall(39, 파일서술자, bæti_COUNT, 0, 0, 0)); }
int fsync(int 파일서술자) { return 호출결과(jkoros_syscall(47, 파일서술자, 0, 0, 0, 0)); }
int fcntl(int 파일서술자, int Skipun, ...) {
    int VALUE = 0;
    if (Skipun == F_DUPFD || Skipun == F_DUPFD_CLOEXEC || Skipun == F_SETFD || Skipun == F_SETFL) {
        __builtin_va_list Viðföng;
        __builtin_va_start(Viðföng, Skipun); VALUE = __builtin_va_arg(Viðföng, int); __builtin_va_end(Viðföng);
    }
    return 호출결과(jkoros_syscall(40, 파일서술자, Skipun, VALUE, 0, 0));
}
