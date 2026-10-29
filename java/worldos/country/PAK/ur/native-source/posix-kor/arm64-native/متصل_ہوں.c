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
    // 현재 파일에는 اجازتیں 메타데이터가 없다. 가변 mode 인수는 저장하지 않는다.
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
فائل_آفسٹ_ٹائپ_کریں pk_lseek(int fd, فائل_آفسٹ_ٹائپ_کریں offset, int origin) {
    if (offset < -16384 || offset > 16384) return result(-22);
    return result(jfs_seek(fd, (int32_t)offset, origin));
}
int pk_unlink(const char *path) { return path_set(path) < 0 ? -1 : result(jfs_unlink()); }
int pk_ftruncate(int fd, فائل_آفسٹ_ٹائپ_کریں size) {
    if (size < 0 || size > 16384) return result(-22);
    return result(jfs_truncate(fd, (int32_t)size));
}
int pk_fsync(int fd) {
    if (result(jfs_size(fd)) < 0) return -1;
    return result(-38); // ENOSYS: RAM 내용이 디스크에 저장되었다고 거짓 응답하지 않는다.
}
int pk_size(int fd) { return result(jfs_size(fd)); }

/* فائل_کا_نام 함수도 독립된 اردو فعل_قدر 심볼로 제공한다. */
int بنائیں_فائل(const char *راستہ_2,int طریقہ_موڈ,...) { return pk_open(راستہ_2,طریقہ_موڈ); }
입출력결과형 파일자료읽기(int فائل_کا_نام,void *کوائف,size_t 개수) { return pk_read(فائل_کا_نام,کوائف,개수); }
입출력결과형 لکھیں_فائل_کوائف(int فائل_کا_نام,const void *کوائف,size_t 개수) { return pk_write(فائل_کا_نام,کوائف,개수); }
int بند_فائل(int فائل_کا_نام) { return pk_close(فائل_کا_نام); }
فائل_آفسٹ_ٹائپ_کریں تلاش_کرنا_فائل(int فائل_کا_نام,فائل_آفسٹ_ٹائپ_کریں 거리,int عکس_ڈالنا_روٹ) { return pk_lseek(فائل_کا_نام,거리,عکس_ڈالنا_روٹ); }
int ہٹائیں_فائل_اندراج_نام(const char *راستہ_2) { return pk_unlink(راستہ_2); }
int سیٹ_فائل_لمبا_ئی(int فائل_کا_نام,فائل_آفسٹ_ٹائپ_کریں حجم) { return pk_ftruncate(فائل_کا_نام,حجم); }
int 파일저장확정(int فائل_کا_نام) { return pk_fsync(فائل_کا_نام); }
int فائل_سائز_دیں(int فائل_کا_نام) { return pk_size(فائل_کا_نام); }
