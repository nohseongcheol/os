#include "파일규약.h"
// 이 기호는 ARM64 AOT 변환기가 Java 메서드의 AAPCS64 래퍼로 만든다.
extern int32_t jfs_path_start(int32_t);
extern int32_t jfs_path_byte(int32_t, int32_t);
extern int32_t jfs_open(int32_t);
extern int32_t jfs_read(int32_t);
extern int32_t jfs_write(int32_t, int32_t);
extern int32_t jfs_close(int32_t);
extern int32_t jfs_seek(int32_t, int32_t, int32_t);
extern int32_t jfs_unlink(void);
extern int32_t jfs_truncate(int32_t, int32_t);
extern int32_t jfs_size(int32_t);

static int result(int value) {
    if (value < 0) { အမှားကိန်း = -value; return -1; }
    return value;
}
static int path_set(const char *path) {
    if (!path) return result(-14);
    size_t length = 0;
    while (length < 64 && path[length]) length++;
    if (result(jfs_path_start((int32_t)length)) < 0) return -1;
    for (size_t i = 0; i < length; i++)
        if (result(jfs_path_byte(i, (unsigned char)path[i])) < 0) return -1;
    return 0;
}
int pk_open(const char *path, int flags, ...) {
    // လက်ရှိအချက်အလက်တစ်ခု 파일에는 접근권한 메타데이터가 없다. 가변 mode 인수는 저장하지 않는다.
    if (path_set(path) < 0) return -1;
    return result(jfs_open(flags));
}
အဝင်အထွက်ရလဒ်အမျိုးပုံစံ pk_read(int fd, void *buffer, size_t count) {
    if (count > INTPTR_MAX) return result(-22);
    if (!buffer && count) return result(-14);
    if (!count) return result(jfs_seek(fd, 0, 1)) < 0 ? -1 : 0;
    unsigned char *p = buffer;
    size_t done = 0;
    while (done < count) {
        int value = jfs_read(fd);
        if (value < 0) return done ? (အဝင်အထွက်ရလဒ်အမျိုးပုံစံ)done : result(value);
        if (value == 256) break;
        p[done++] = value;
    }
    return done;
}
အဝင်အထွက်ရလဒ်အမျိုးပုံစံ pk_write(int fd, const void *buffer, size_t count) {
    if (count > INTPTR_MAX) return result(-22);
    if (!buffer && count) return result(-14);
    if (!count) return result(jfs_seek(fd, 0, 1)) < 0 ? -1 : 0;
    const unsigned char *p = buffer;
    size_t done = 0;
    while (done < count) {
        int value = jfs_write(fd, p[done]);
        if (value < 0) return done ? (အဝင်အထွက်ရလဒ်အမျိုးပုံစံ)done : result(value);
        done++;
    }
    return done;
}
int pk_close(int fd) { return result(jfs_close(fd)); }
ဖိုင်အရွေ့အမျိုးပုံစံ pk_lseek(int fd, ဖိုင်အရွေ့အမျိုးပုံစံ offset, int origin) {
    if (offset < -16384 || offset > 16384) return result(-22);
    return result(jfs_seek(fd, (int32_t)offset, origin));
}
int pk_unlink(const char *path) { return path_set(path) < 0 ? -1 : result(jfs_unlink()); }
int pk_ftruncate(int fd, ဖိုင်အရွေ့အမျိုးပုံစံ size) {
    if (size < 0 || size > 16384) return result(-22);
    return result(jfs_truncate(fd, (int32_t)size));
}
int pk_fsync(int fd) {
    if (result(jfs_size(fd)) < 0) return -1;
    return result(-38); // ENOSYS: RAM 내용이 디스크에 저장되었다고 မှားတန်ဖိုး 응답하지 않는다.
}
int pk_size(int fd) { return result(jfs_size(fd)); }

/* ဖိုင် 함수도 독립된 မြန်မာ လုပ်ဆောင်ချက် 심볼로 제공한다. */
int ဖိုင်ဖွင့်(const char *လမ်း,int နည်းလမ်းနည်းစနစ်,...) { return pk_open(လမ်း,နည်းလမ်းနည်းစနစ်); }
အဝင်အထွက်ရလဒ်အမျိုးပုံစံ ဖိုင်ဒေတာဖတ်(int ဖိုင်,void *ဒေတာ,size_t အရေအတွက်) { return pk_read(ဖိုင်,ဒေတာ,အရေအတွက်); }
အဝင်အထွက်ရလဒ်အမျိုးပုံစံ ဖိုင်ဒေတာရေး(int ဖိုင်,const void *ဒေတာ,size_t အရေအတွက်) { return pk_write(ဖိုင်,ဒေတာ,အရေအတွက်); }
int ဖိုင်ပိတ်(int ဖိုင်) { return pk_close(ဖိုင်); }
ဖိုင်အရွေ့အမျိုးပုံစံ ဖိုင်နေရာရွှေ့(int ဖိုင်,ဖိုင်အရွေ့အမျိုးပုံစံ အကွာအဝေး,int စီမံကိန်းအမြစ်) { return pk_lseek(ဖိုင်,အကွာအဝေး,စီမံကိန်းအမြစ်); }
int ဖိုင်အချက်အမည်ဖယ်ရှား(const char *လမ်း) { return pk_unlink(လမ်း); }
int ဖိုင်အလျားသတ်မှတ်(int ဖိုင်,ဖိုင်အရွေ့အမျိုးပုံစံ အရွယ်) { return pk_ftruncate(ဖိုင်,အရွယ်); }
int ဖိုင်သိုလှောင်အတည်ပြု(int ဖိုင်) { return pk_fsync(ဖိုင်); }
int ဖိုင်အရွယ်(int ဖိုင်) { return pk_size(ဖိုင်); }
