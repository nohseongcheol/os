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
    if (value < 0) { 오류번호 = -value; return -1; }
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
    // 현재 파일에는 অনুমতি 메타데이터가 없다. 가변 mode 인수는 저장하지 않는다.
    if (path_set(path) < 0) return -1;
    return result(jfs_open(flags));
}
입출력결과형 pk_read(int fd, void *buffer, size_t count) {
    if (count > INTPTR_MAX) return result(-22);
    if (!buffer && count) return result(-14);
    if (!count) return result(jfs_seek(fd, 0, 1)) < 0 ? -1 : 0;
    unsigned char *p = buffer;
    size_t done = 0;
    while (done < count) {
        int value = jfs_read(fd);
        if (value < 0) return done ? (입출력결과형)done : result(value);
        if (value == 256) break;
        p[done++] = value;
    }
    return done;
}
입출력결과형 pk_write(int fd, const void *buffer, size_t count) {
    if (count > INTPTR_MAX) return result(-22);
    if (!buffer && count) return result(-14);
    if (!count) return result(jfs_seek(fd, 0, 1)) < 0 ? -1 : 0;
    const unsigned char *p = buffer;
    size_t done = 0;
    while (done < count) {
        int value = jfs_write(fd, p[done]);
        if (value < 0) return done ? (입출력결과형)done : result(value);
        done++;
    }
    return done;
}
int pk_close(int fd) { return result(jfs_close(fd)); }
ফাইল_অফসেট_টাইপ_করুন pk_lseek(int fd, ফাইল_অফসেট_টাইপ_করুন offset, int origin) {
    if (offset < -16384 || offset > 16384) return result(-22);
    return result(jfs_seek(fd, (int32_t)offset, origin));
}
int pk_unlink(const char *path) { return path_set(path) < 0 ? -1 : result(jfs_unlink()); }
int pk_ftruncate(int fd, ফাইল_অফসেট_টাইপ_করুন size) {
    if (size < 0 || size > 16384) return result(-22);
    return result(jfs_truncate(fd, (int32_t)size));
}
int pk_fsync(int fd) {
    if (result(jfs_size(fd)) < 0) return -1;
    return result(-38); // ENOSYS: RAM 내용이 디스크에 저장되었다고 거짓 응답하지 않는다.
}
int pk_size(int fd) { return result(jfs_size(fd)); }

/* নথির_নাম 함수도 독립된 বাংলা ফাংশন_মান 심볼로 제공한다. */
int খোলা_ফাইল(const char *পথ_2,int পদ্ধতি_মোড,...) { return pk_open(পথ_2,পদ্ধতি_মোড); }
입출력결과형 파일자료읽기(int নথির_নাম,void *ডাটা,size_t 개수) { return pk_read(নথির_নাম,ডাটা,개수); }
입출력결과형 লেখা_ফাইল_ডাটা(int নথির_নাম,const void *ডাটা,size_t 개수) { return pk_write(নথির_নাম,ডাটা,개수); }
int বন্ধ_ফাইল(int নথির_নাম) { return pk_close(নথির_নাম); }
ফাইল_অফসেট_টাইপ_করুন সিক_ফাইল(int নথির_নাম,ফাইল_অফসেট_টাইপ_করুন 거리,int প্রকল্প_মূল) { return pk_lseek(নথির_নাম,거리,প্রকল্প_মূল); }
int সরানো_ফাইল_ভুক্তি_নাম(const char *পথ_2) { return pk_unlink(পথ_2); }
int সেট_ফাইল_দৈর্ঘ্য(int নথির_নাম,ফাইল_অফসেট_টাইপ_করুন আকার) { return pk_ftruncate(নথির_নাম,আকার); }
int 파일저장확정(int নথির_নাম) { return pk_fsync(নথির_নাম); }
int ফাইল_আয়তন(int নথির_নাম) { return pk_size(নথির_নাম); }
