#include <파일규약.h>
#include "ခေါ်နယ်နိမိတ်.h"

int အမှားကိန်း;
int 호출결과(int ရလဒ်) {
    if (ရလဒ် < 0) { အမှားကိန်း = -ရလဒ်; return -1; }
    return ရလဒ်;
}
int open(const char *ဖိုင်အချက်အမည်, int ဖွင့်ရန်သတ်မှတ်ချက်, ...) {
    mode_t ခွင့်ပြုပေး = 0;
    if (ဖွင့်ရန်သတ်မှတ်ချက် & O_CREAT) {
        __builtin_va_list အချက်များ;
        __builtin_va_start(အချက်များ, ဖွင့်ရန်သတ်မှတ်ချက်);
        ခွင့်ပြုပေး = __builtin_va_arg(အချက်များ, mode_t);
        __builtin_va_end(အချက်များ);
    }
    return 호출결과(jkoros_syscall(30, (int)ဖိုင်အချက်အမည်, ဖွင့်ရန်သတ်မှတ်ချက်, ခွင့်ပြုပေး, 0, 0));
}
int creat(const char *ဖိုင်အချက်အမည်, mode_t ခွင့်ပြုပေး) { return open(ဖိုင်အချက်အမည်, O_WRONLY | O_CREAT | O_TRUNC, ခွင့်ပြုပေး); }
ssize_t read(int ဖိုင်အညွှန်း, void *ဒေတာ, size_t ဘိုက်အရေအတွက်) {
    return 호출결과(jkoros_syscall(31, ဖိုင်အညွှန်း, (int)ဒေတာ, ဘိုက်အရေအတွက်, 0, 0));
}
ssize_t write(int ဖိုင်အညွှန်း, const void *ဒေတာ, size_t ဘိုက်အရေအတွက်) {
    return 호출결과(jkoros_syscall(32, ဖိုင်အညွှန်း, (int)ဒေတာ, ဘိုက်အရေအတွက်, 0, 0));
}
int close(int ဖိုင်အညွှန်း) { return 호출결과(jkoros_syscall(33, ဖိုင်အညွှန်း, 0, 0, 0, 0)); }
off_t lseek(int ဖိုင်အညွှန်း, off_t အရွေ့တန်ဖိုး, int စီမံကိန်းအမြစ်) {
    return 호출결과(jkoros_syscall(34, ဖိုင်အညွှန်း, အရွေ့တန်ဖိုး, စီမံကိန်းအမြစ်, 0, 0));
}
int dup(int ဖိုင်အညွှန်း) { return 호출결과(jkoros_syscall(35, ဖိုင်အညွှန်း, 0, 0, 0, 0)); }
int dup2(int ဖိုင်အညွှန်း, int အသစ်အညွှန်း) { return 호출결과(jkoros_syscall(36, ဖိုင်အညွှန်း, အသစ်အညွှန်း, 0, 0, 0)); }
int fstat(int ဖိုင်အညွှန်း, struct stat *အခြေအနေတန်ဖိုး) { return 호출결과(jkoros_syscall(37, ဖိုင်အညွှန်း, (int)အခြေအနေတန်ဖိုး, 0, 0, 0)); }
int unlink(const char *ဖိုင်အချက်အမည်) { return 호출결과(jkoros_syscall(38, (int)ဖိုင်အချက်အမည်, 0, 0, 0, 0)); }
int ftruncate(int ဖိုင်အညွှန်း, off_t ဘိုက်အရေအတွက်) { return 호출결과(jkoros_syscall(39, ဖိုင်အညွှန်း, ဘိုက်အရေအတွက်, 0, 0, 0)); }
int fsync(int ဖိုင်အညွှန်း) { return 호출결과(jkoros_syscall(47, ဖိုင်အညွှန်း, 0, 0, 0, 0)); }
int fcntl(int ဖိုင်အညွှန်း, int အမိန့်, ...) {
    int တန်ဖိုး = 0;
    if (အမိန့် == F_DUPFD || အမိန့် == F_DUPFD_CLOEXEC || အမိန့် == F_SETFD || အမိန့် == F_SETFL) {
        __builtin_va_list အချက်များ;
        __builtin_va_start(အချက်များ, အမိန့်); တန်ဖိုး = __builtin_va_arg(အချက်များ, int); __builtin_va_end(အချက်များ);
    }
    return 호출결과(jkoros_syscall(40, ဖိုင်အညွှန်း, အမိန့်, တန်ဖိုး, 0, 0));
}
