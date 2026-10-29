#ifndef JKOROS_UNISTD_H
#define JKOROS_UNISTD_H
#include <sys/types.h>
#define STDIN_FILENO 0
#define STDOUT_FILENO 1
#define STDERR_FILENO 2
#define SEEK_SET 0
#define SEEK_CUR 1
#define SEEK_END 2
ssize_t read(int ဖိုင်အညွှန်း, void *ဒေတာ, size_t ဘိုက်အရေအတွက်);
ssize_t write(int ဖိုင်အညွှန်း, const void *ဒေတာ, size_t ဘိုက်အရေအတွက်);
int close(int ဖိုင်အညွှန်း);
off_t lseek(int ဖိုင်အညွှန်း, off_t အရွေ့တန်ဖိုး, int စီမံကိန်းအမြစ်);
int dup(int ဖိုင်အညွှန်း);
int dup2(int ဖိုင်အညွှန်း, int အသစ်အညွှန်း);
int unlink(const char *ဖိုင်အချက်အမည်);
int ftruncate(int ဖိုင်အညွှန်း, off_t ဘိုက်အရေအတွက်);
int fsync(int ဖိုင်အညွှန်း);
void _exit(int ထွက်ကုဒ်) __attribute__((noreturn));
#endif
