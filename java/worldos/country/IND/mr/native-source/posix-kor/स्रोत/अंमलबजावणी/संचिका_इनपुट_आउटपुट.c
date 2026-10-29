#include <संचिका_द्विमानजोडणी.h>
#include "कॉल_सीमा.h"

int त्रुटी_संख्या;
int आवाहन_मोजमाप(int मोजमाप) {
    if (मोजमाप < 0) { त्रुटी_संख्या = -मोजमाप; return -1; }
    return मोजमाप;
}
int open(const char *संचिका_प्रविष्टी_नाव, int सेटिंग्ज_उघडा, ...) {
    mode_t अनुमती_परवानगी = 0;
    if (सेटिंग्ज_उघडा & O_CREAT) {
        __builtin_va_list बाबी;
        __builtin_va_start(बाबी, सेटिंग्ज_उघडा);
        अनुमती_परवानगी = __builtin_va_arg(बाबी, mode_t);
        __builtin_va_end(बाबी);
    }
    return आवाहन_मोजमाप(jkoros_syscall(30, (int)संचिका_प्रविष्टी_नाव, सेटिंग्ज_उघडा, अनुमती_परवानगी, 0, 0));
}
int creat(const char *संचिका_प्रविष्टी_नाव, mode_t अनुमती_परवानगी) { return open(संचिका_प्रविष्टी_नाव, O_WRONLY | O_CREAT | O_TRUNC, अनुमती_परवानगी); }
ssize_t read(int संचिका_विवरणक, void *डेटा, size_t बाइट_संख्या) {
    return आवाहन_मोजमाप(jkoros_syscall(31, संचिका_विवरणक, (int)डेटा, बाइट_संख्या, 0, 0));
}
ssize_t write(int संचिका_विवरणक, const void *डेटा, size_t बाइट_संख्या) {
    return आवाहन_मोजमाप(jkoros_syscall(32, संचिका_विवरणक, (int)डेटा, बाइट_संख्या, 0, 0));
}
int close(int संचिका_विवरणक) { return आवाहन_मोजमाप(jkoros_syscall(33, संचिका_विवरणक, 0, 0, 0, 0)); }
off_t lseek(int संचिका_विवरणक, off_t ऑफसेट_मूल्य, int प्रोजेक्ट_मूळ) {
    return आवाहन_मोजमाप(jkoros_syscall(34, संचिका_विवरणक, ऑफसेट_मूल्य, प्रोजेक्ट_मूळ, 0, 0));
}
int dup(int संचिका_विवरणक) { return आवाहन_मोजमाप(jkoros_syscall(35, संचिका_विवरणक, 0, 0, 0, 0)); }
int dup2(int संचिका_विवरणक, int नवे_विवरणक) { return आवाहन_मोजमाप(jkoros_syscall(36, संचिका_विवरणक, नवे_विवरणक, 0, 0, 0)); }
int fstat(int संचिका_विवरणक, struct stat *राज्य_मूल्य) { return आवाहन_मोजमाप(jkoros_syscall(37, संचिका_विवरणक, (int)राज्य_मूल्य, 0, 0, 0)); }
int unlink(const char *संचिका_प्रविष्टी_नाव) { return आवाहन_मोजमाप(jkoros_syscall(38, (int)संचिका_प्रविष्टी_नाव, 0, 0, 0, 0)); }
int ftruncate(int संचिका_विवरणक, off_t बाइट_संख्या) { return आवाहन_मोजमाप(jkoros_syscall(39, संचिका_विवरणक, बाइट_संख्या, 0, 0, 0)); }
int fsync(int संचिका_विवरणक) { return आवाहन_मोजमाप(jkoros_syscall(47, संचिका_विवरणक, 0, 0, 0, 0)); }
int fcntl(int संचिका_विवरणक, int आदेश, ...) {
    int मूल्य = 0;
    if (आदेश == F_DUPFD || आदेश == F_DUPFD_CLOEXEC || आदेश == F_SETFD || आदेश == F_SETFL) {
        __builtin_va_list बाबी;
        __builtin_va_start(बाबी, आदेश); मूल्य = __builtin_va_arg(बाबी, int); __builtin_va_end(बाबी);
    }
    return आवाहन_मोजमाप(jkoros_syscall(40, संचिका_विवरणक, आदेश, मूल्य, 0, 0));
}
