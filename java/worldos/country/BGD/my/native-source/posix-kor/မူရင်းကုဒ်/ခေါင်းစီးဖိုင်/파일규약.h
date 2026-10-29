#ifndef JKOROS_KOREAN_FILE_H
#define JKOROS_KOREAN_FILE_H
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#define ဖိုင်ဖွင့် open
#define ဖိုင်ဖန်တီး creat
#define ဖိုင်ဒေတာဖတ် read
#define ဖိုင်ဒေတာရေး write
#define ဖိုင်ပိတ် close
#define ဖိုင်နေရာရွှေ့ lseek
#define မိတ္တူဖိုင်အညွှန်း dup
#define 파일서술자지정복제 dup2
#define ဖိုင်အချက်အမည်ဖယ်ရှား unlink
#define ဖိုင်အလျားသတ်မှတ် ftruncate
#define ဖိုင်သိုလှောင်အတည်ပြု fsync
#define ဖိုင်လက်ရှိအခြေအနေဖတ် fstat
#define ထိန်းချုပ်ဖိုင်အညွှန်း fcntl
#define သာတန်ဖိုးဖတ် O_RDONLY
#define သာတန်ဖိုးရေး O_WRONLY
#define ဖတ်ရေး O_RDWR
#define 없으면만들기 O_CREAT
#define အသစ်ဖိုင်ဖန်တီး (O_CREAT | O_EXCL)
#define 내용비우기 O_TRUNC
#define 끝에이어쓰기 O_APPEND
#define မစောင့်ဘဲလုပ် O_NONBLOCK
#define 처음기준 SEEK_SET
#define လက်ရှိအမြစ် SEEK_CUR
#define 끝기준 SEEK_END
#define ဖိုင်အခြေအနေ stat
typedef size_t ဘိုက်အရေအတွက်အမျိုးပုံစံ;
typedef ssize_t အဝင်အထွက်ရလဒ်အမျိုးပုံစံ;
typedef off_t ဖိုင်အရွေ့အမျိုးပုံစံ;
#endif
