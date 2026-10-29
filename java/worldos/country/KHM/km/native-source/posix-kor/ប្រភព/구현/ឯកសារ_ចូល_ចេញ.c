#include <파일규약.h>
#include "호출경계.h"

int 오류번호;
int 호출결과(int ការវាស់វែង) {
    if (ការវាស់វែង < 0) { 오류번호 = -ការវាស់វែង; return -1; }
    return ការវាស់វែង;
}
int open(const char *ឯកសារ_ការបញ្ចូល_ឈ្មោះ, int បើក_ការកំណត់, ...) {
    mode_t 허가 = 0;
    if (បើក_ការកំណត់ & O_CREAT) {
        __builtin_va_list អាគុយម៉ង់;
        __builtin_va_start(អាគុយម៉ង់, បើក_ការកំណត់);
        허가 = __builtin_va_arg(អាគុយម៉ង់, mode_t);
        __builtin_va_end(អាគុយម៉ង់);
    }
    return 호출결과(jkoros_syscall(30, (int)ឯកសារ_ការបញ្ចូល_ឈ្មោះ, បើក_ការកំណត់, 허가, 0, 0));
}
int creat(const char *ឯកសារ_ការបញ្ចូល_ឈ្មោះ, mode_t 허가) { return open(ឯកសារ_ការបញ្ចូល_ឈ្មោះ, O_WRONLY | O_CREAT | O_TRUNC, 허가); }
ssize_t read(int 파일서술자, void *ទិន្នន័យ, size_t 바이트수) {
    return 호출결과(jkoros_syscall(31, 파일서술자, (int)ទិន្នន័យ, 바이트수, 0, 0));
}
ssize_t write(int 파일서술자, const void *ទិន្នន័យ, size_t 바이트수) {
    return 호출결과(jkoros_syscall(32, 파일서술자, (int)ទិន្នន័យ, 바이트수, 0, 0));
}
int close(int 파일서술자) { return 호출결과(jkoros_syscall(33, 파일서술자, 0, 0, 0, 0)); }
off_t lseek(int 파일서술자, off_t ការបែង_ភាគ_តំលៃ, int បញ្ចាំង_ឬស) {
    return 호출결과(jkoros_syscall(34, 파일서술자, ការបែង_ភាគ_តំលៃ, បញ្ចាំង_ឬស, 0, 0));
}
int dup(int 파일서술자) { return 호출결과(jkoros_syscall(35, 파일서술자, 0, 0, 0, 0)); }
int dup2(int 파일서술자, int 새서술자) { return 호출결과(jkoros_syscall(36, 파일서술자, 새서술자, 0, 0, 0)); }
int fstat(int 파일서술자, struct stat *ភាព_តំលៃ) { return 호출결과(jkoros_syscall(37, 파일서술자, (int)ភាព_តំលៃ, 0, 0, 0)); }
int unlink(const char *ឯកសារ_ការបញ្ចូល_ឈ្មោះ) { return 호출결과(jkoros_syscall(38, (int)ឯកសារ_ការបញ្ចូល_ឈ្មោះ, 0, 0, 0, 0)); }
int ftruncate(int 파일서술자, off_t 바이트수) { return 호출결과(jkoros_syscall(39, 파일서술자, 바이트수, 0, 0, 0)); }
int fsync(int 파일서술자) { return 호출결과(jkoros_syscall(47, 파일서술자, 0, 0, 0, 0)); }
int fcntl(int 파일서술자, int ពាក្យ_បញ្ជា, ...) {
    int តំលៃ = 0;
    if (ពាក្យ_បញ្ជា == F_DUPFD || ពាក្យ_បញ្ជា == F_DUPFD_CLOEXEC || ពាក្យ_បញ្ជា == F_SETFD || ពាក្យ_បញ្ជា == F_SETFL) {
        __builtin_va_list អាគុយម៉ង់;
        __builtin_va_start(អាគុយម៉ង់, ពាក្យ_បញ្ជា); តំលៃ = __builtin_va_arg(អាគុយម៉ង់, int); __builtin_va_end(អាគុយម៉ង់);
    }
    return 호출결과(jkoros_syscall(40, 파일서술자, ពាក្យ_បញ្ជា, តំលៃ, 0, 0));
}
