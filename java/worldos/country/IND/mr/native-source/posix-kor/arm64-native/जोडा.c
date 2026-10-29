#include "संचिका_द्विमानजोडणी.h"
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
    if (value < 0) { त्रुटी_संख्या = -value; return -1; }
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
    // सध्याचे_आयटम 파일에는 परवानगी 메타데이터가 없다. 가변 mode 인수는 저장하지 않는다.
    if (path_set(path) < 0) return -1;
    return result(jfs_open(flags));
}
आदानप्रदान_मोजमाप_टाइप_करा pk_read(int fd, void *buffer, size_t count) {
    if (count > INTPTR_MAX) return result(-22);
    if (!buffer && count) return result(-14);
    if (!count) return result(jfs_seek(fd, 0, 1)) < 0 ? -1 : 0;
    unsigned char *p = buffer;
    size_t done = 0;
    while (done < count) {
        int value = jfs_read(fd);
        if (value < 0) return done ? (आदानप्रदान_मोजमाप_टाइप_करा)done : result(value);
        if (value == 256) break;
        p[done++] = value;
    }
    return done;
}
आदानप्रदान_मोजमाप_टाइप_करा pk_write(int fd, const void *buffer, size_t count) {
    if (count > INTPTR_MAX) return result(-22);
    if (!buffer && count) return result(-14);
    if (!count) return result(jfs_seek(fd, 0, 1)) < 0 ? -1 : 0;
    const unsigned char *p = buffer;
    size_t done = 0;
    while (done < count) {
        int value = jfs_write(fd, p[done]);
        if (value < 0) return done ? (आदानप्रदान_मोजमाप_टाइप_करा)done : result(value);
        done++;
    }
    return done;
}
int pk_close(int fd) { return result(jfs_close(fd)); }
संचिका_ऑफसेट_टाइप_करा pk_lseek(int fd, संचिका_ऑफसेट_टाइप_करा offset, int origin) {
    if (offset < -16384 || offset > 16384) return result(-22);
    return result(jfs_seek(fd, (int32_t)offset, origin));
}
int pk_unlink(const char *path) { return path_set(path) < 0 ? -1 : result(jfs_unlink()); }
int pk_ftruncate(int fd, संचिका_ऑफसेट_टाइप_करा size) {
    if (size < 0 || size > 16384) return result(-22);
    return result(jfs_truncate(fd, (int32_t)size));
}
int pk_fsync(int fd) {
    if (result(jfs_size(fd)) < 0) return -1;
    return result(-38); // ENOSYS: RAM 내용이 디스크에 저장되었다고 असत्य_मूल्य 응답하지 않는다.
}
int pk_size(int fd) { return result(jfs_size(fd)); }

/* फाइल 함수도 독립된 मराठी फलन_मूल्य 심볼로 제공한다. */
int संचिका_उघडा(const char *मार्ग,int पद्धत_मोड,...) { return pk_open(मार्ग,पद्धत_मोड); }
आदानप्रदान_मोजमाप_टाइप_करा संचिका_डेटा_वाचा(int फाइल,void *डेटा,size_t आयटम_संख्या) { return pk_read(फाइल,डेटा,आयटम_संख्या); }
आदानप्रदान_मोजमाप_टाइप_करा संचिका_डेटा_लिहा(int फाइल,const void *डेटा,size_t आयटम_संख्या) { return pk_write(फाइल,डेटा,आयटम_संख्या); }
int संचिका_मिटवा(int फाइल) { return pk_close(फाइल); }
संचिका_ऑफसेट_टाइप_करा शोधा_संचिका(int फाइल,संचिका_ऑफसेट_टाइप_करा अंतर_मूल्य,int प्रोजेक्ट_मूळ) { return pk_lseek(फाइल,अंतर_मूल्य,प्रोजेक्ट_मूळ); }
int संचिका_प्रविष्टी_नाव_काढणे(const char *मार्ग) { return pk_unlink(मार्ग); }
int संचिका_लांबी_संच(int फाइल,संचिका_ऑफसेट_टाइप_करा आकार) { return pk_ftruncate(फाइल,आकार); }
int स्थिरकरा_फाईल_संग्रहण(int फाइल) { return pk_fsync(फाइल); }
int संचिका_आकारा(int फाइल) { return pk_size(फाइल); }
