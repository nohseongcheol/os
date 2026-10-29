#ifndef JKOROS_ARM64_NATIVE_FILE_H
#define JKOROS_ARM64_NATIVE_FILE_H
#include <stddef.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
// 독립된 bare-metal ABI. Linux/i386의 헤더나 libc와 혼합하지 않는다.
typedef intptr_t အဝင်အထွက်ရလဒ်အမျိုးပုံစံ;
typedef size_t ဘိုက်အရေအတွက်အမျိုးပုံစံ;
typedef int64_t ဖိုင်အရွေ့အမျိုးပုံစံ;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
အဝင်အထွက်ရလဒ်အမျိုးပုံစံ pk_read(int fd, void *buffer, size_t count);
အဝင်အထွက်ရလဒ်အမျိုးပုံစံ pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
ဖိုင်အရွေ့အမျိုးပုံစံ pk_lseek(int fd, ဖိုင်အရွေ့အမျိုးပုံစံ offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, ဖိုင်အရွေ့အမျိုးပုံစံ size);
int pk_fsync(int fd);
int pk_size(int fd);
int ဖိုင်ဖွင့်(const char *လမ်း, int နည်းလမ်းနည်းစနစ်, ...);
အဝင်အထွက်ရလဒ်အမျိုးပုံစံ ဖိုင်ဒေတာဖတ်(int ဖိုင်, void *ဒေတာ, size_t အရေအတွက်);
အဝင်အထွက်ရလဒ်အမျိုးပုံစံ ဖိုင်ဒေတာရေး(int ဖိုင်, const void *ဒေတာ, size_t အရေအတွက်);
int ဖိုင်ပိတ်(int ဖိုင်);
ဖိုင်အရွေ့အမျိုးပုံစံ ဖိုင်နေရာရွှေ့(int ဖိုင်, ဖိုင်အရွေ့အမျိုးပုံစံ အကွာအဝေး, int စီမံကိန်းအမြစ်);
int ဖိုင်အချက်အမည်ဖယ်ရှား(const char *လမ်း);
int ဖိုင်အလျားသတ်မှတ်(int ဖိုင်, ဖိုင်အရွေ့အမျိုးပုံစံ အရွယ်);
int ဖိုင်သိုလှောင်အတည်ပြု(int ဖိုင်);
int ဖိုင်အရွယ်(int ဖိုင်);
#ifdef __cplusplus
}
#endif
#define အမှားကိန်း (*pk_errno_location())
#define သာတန်ဖိုးဖတ် 0
#define သာတန်ဖိုးရေး 1
#define ဖတ်ရေး 2
#define 없으면만들기 0x40
#define အသစ်ဖိုင်ဖန်တီး 0xc0
#define 내용비우기 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define လက်ရှိအမြစ် 1
#define 끝기준 2
#endif
