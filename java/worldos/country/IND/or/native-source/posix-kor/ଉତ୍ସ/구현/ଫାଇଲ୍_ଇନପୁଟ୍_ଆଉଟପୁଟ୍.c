#include <파일규약.h>
#include "호출경계.h"

int 오류번호;
int 호출결과(int ମାପ) {
    if (ମାପ < 0) { 오류번호 = -ମାପ; return -1; }
    return ମାପ;
}
int open(const char *ଫାଇଲ୍_ଏଣ୍ଟ୍ରି_ନାମ, int ଖୋଲିବା_ସେଟିଂସ୍, ...) {
    mode_t 허가 = 0;
    if (ଖୋଲିବା_ସେଟିଂସ୍ & O_CREAT) {
        __builtin_va_list 인수;
        __builtin_va_start(인수, ଖୋଲିବା_ସେଟିଂସ୍);
        허가 = __builtin_va_arg(인수, mode_t);
        __builtin_va_end(인수);
    }
    return 호출결과(jkoros_syscall(30, (int)ଫାଇଲ୍_ଏଣ୍ଟ୍ରି_ନାମ, ଖୋଲିବା_ସେଟିଂସ୍, 허가, 0, 0));
}
int creat(const char *ଫାଇଲ୍_ଏଣ୍ଟ୍ରି_ନାମ, mode_t 허가) { return open(ଫାଇଲ୍_ଏଣ୍ଟ୍ରି_ନାମ, O_WRONLY | O_CREAT | O_TRUNC, 허가); }
ssize_t read(int 파일서술자, void *ଡାଟା, size_t 바이트수) {
    return 호출결과(jkoros_syscall(31, 파일서술자, (int)ଡାଟା, 바이트수, 0, 0));
}
ssize_t write(int 파일서술자, const void *ଡାଟା, size_t 바이트수) {
    return 호출결과(jkoros_syscall(32, 파일서술자, (int)ଡାଟା, 바이트수, 0, 0));
}
int close(int 파일서술자) { return 호출결과(jkoros_syscall(33, 파일서술자, 0, 0, 0, 0)); }
off_t lseek(int 파일서술자, off_t ଅଫ୍_ସେଟ୍_ମୂଲ୍ୟ, int ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍) {
    return 호출결과(jkoros_syscall(34, 파일서술자, ଅଫ୍_ସେଟ୍_ମୂଲ୍ୟ, ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍, 0, 0));
}
int dup(int 파일서술자) { return 호출결과(jkoros_syscall(35, 파일서술자, 0, 0, 0, 0)); }
int dup2(int 파일서술자, int 새서술자) { return 호출결과(jkoros_syscall(36, 파일서술자, 새서술자, 0, 0, 0)); }
int fstat(int 파일서술자, struct stat *ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1) { return 호출결과(jkoros_syscall(37, 파일서술자, (int)ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1, 0, 0, 0)); }
int unlink(const char *ଫାଇଲ୍_ଏଣ୍ଟ୍ରି_ନାମ) { return 호출결과(jkoros_syscall(38, (int)ଫାଇଲ୍_ଏଣ୍ଟ୍ରି_ନାମ, 0, 0, 0, 0)); }
int ftruncate(int 파일서술자, off_t 바이트수) { return 호출결과(jkoros_syscall(39, 파일서술자, 바이트수, 0, 0, 0)); }
int fsync(int 파일서술자) { return 호출결과(jkoros_syscall(47, 파일서술자, 0, 0, 0, 0)); }
int fcntl(int 파일서술자, int ନିର୍ଦ୍ଦେଶ, ...) {
    int ମୂଲ୍ୟ = 0;
    if (ନିର୍ଦ୍ଦେଶ == F_DUPFD || ନିର୍ଦ୍ଦେଶ == F_DUPFD_CLOEXEC || ନିର୍ଦ୍ଦେଶ == F_SETFD || ନିର୍ଦ୍ଦେଶ == F_SETFL) {
        __builtin_va_list 인수;
        __builtin_va_start(인수, ନିର୍ଦ୍ଦେଶ); ମୂଲ୍ୟ = __builtin_va_arg(인수, int); __builtin_va_end(인수);
    }
    return 호출결과(jkoros_syscall(40, 파일서술자, ନିର୍ଦ୍ଦେଶ, ମୂଲ୍ୟ, 0, 0));
}
