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
    if (value < 0) { त्रुटि_संख्या = -value; return -1; }
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
    // अद्यतित_आइटम 파일에는 अनुमतियाँ 메타데이터가 없다. 가변 mode 인수는 저장하지 않는다.
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
फ़ाइल_ऑफ़सेट_लिखें pk_lseek(int fd, फ़ाइल_ऑफ़सेट_लिखें offset, int origin) {
    if (offset < -16384 || offset > 16384) return result(-22);
    return result(jfs_seek(fd, (int32_t)offset, origin));
}
int pk_unlink(const char *path) { return path_set(path) < 0 ? -1 : result(jfs_unlink()); }
int pk_ftruncate(int fd, फ़ाइल_ऑफ़सेट_लिखें size) {
    if (size < 0 || size > 16384) return result(-22);
    return result(jfs_truncate(fd, (int32_t)size));
}
int pk_fsync(int fd) {
    if (result(jfs_size(fd)) < 0) return -1;
    return result(-38); // ENOSYS: RAM 내용이 디스크에 저장되었다고 거짓 응답하지 않는다.
}
int pk_size(int fd) { return result(jfs_size(fd)); }

/* संचिका 함수도 독립된 हिंदी फ़ंक्_शन_मान 심볼로 제공한다. */
int जारी_फ़ाइल(const char *पथ,int विधि_मोड,...) { return pk_open(पथ,विधि_मोड); }
입출력결과형 पढें_फ़ाइल_डेटा(int संचिका,void *आँकड़े,size_t 개수) { return pk_read(संचिका,आँकड़े,개수); }
입출력결과형 लिखना_फ़ाइल_डेटा(int संचिका,const void *आँकड़े,size_t 개수) { return pk_write(संचिका,आँकड़े,개수); }
int बंद_फ़ाइल(int संचिका) { return pk_close(संचिका); }
फ़ाइल_ऑफ़सेट_लिखें खोजें_फ़ाइल(int संचिका,फ़ाइल_ऑफ़सेट_लिखें 거리,int प्रोजेक्ट_करें_मूल) { return pk_lseek(संचिका,거리,प्रोजेक्ट_करें_मूल); }
int निकालें_फ़ाइल_एन्ट्री_नाम(const char *पथ) { return pk_unlink(पथ); }
int 파일길이정하기(int संचिका,फ़ाइल_ऑफ़सेट_लिखें आकार) { return pk_ftruncate(संचिका,आकार); }
int कमिट_फ़ाइल_संग्रहण(int संचिका) { return pk_fsync(संचिका); }
int फ़ाइल_आकार(int संचिका) { return pk_size(संचिका); }
