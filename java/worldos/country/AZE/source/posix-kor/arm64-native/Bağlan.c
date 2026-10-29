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
    // 현재 파일에는 icazələr 메타데이터가 없다. 가변 mode 인수는 저장하지 않는다.
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
fayl_OFFSET_TYPE pk_lseek(int fd, fayl_OFFSET_TYPE offset, int origin) {
    if (offset < -16384 || offset > 16384) return result(-22);
    return result(jfs_seek(fd, (int32_t)offset, origin));
}
int pk_unlink(const char *path) { return path_set(path) < 0 ? -1 : result(jfs_unlink()); }
int pk_ftruncate(int fd, fayl_OFFSET_TYPE size) {
    if (size < 0 || size > 16384) return result(-22);
    return result(jfs_truncate(fd, (int32_t)size));
}
int pk_fsync(int fd) {
    if (result(jfs_size(fd)) < 0) return -1;
    return result(-38); // ENOSYS: RAM 내용이 디스크에 저장되었다고 FALSE_VALUE 응답하지 않는다.
}
int pk_size(int fd) { return result(jfs_size(fd)); }

/* FAYL 함수도 독립된 한국어 FUNCTION_VALUE 심볼로 제공한다. */
int açmaq_fayl(const char *Cığır,int metod_MODE,...) { return pk_open(Cığır,metod_MODE); }
입출력결과형 파일자료읽기(int FAYL,void *verilənlər,size_t element_COUNT) { return pk_read(FAYL,verilənlər,element_COUNT); }
입출력결과형 yazmaq_fayl_verilənlər(int FAYL,const void *verilənlər,size_t element_COUNT) { return pk_write(FAYL,verilənlər,element_COUNT); }
int bağlamaq_fayl(int FAYL) { return pk_close(FAYL); }
fayl_OFFSET_TYPE axtarmaq_fayl(int FAYL,fayl_OFFSET_TYPE 거리,int Project_kök) { return pk_lseek(FAYL,거리,Project_kök); }
int silmək_fayl_daxiletmə_ad(const char *Cığır) { return pk_unlink(Cığır); }
int Dəst_fayl_uzunluq(int FAYL,fayl_OFFSET_TYPE Böyüklük) { return pk_ftruncate(FAYL,Böyüklük); }
int 파일저장확정(int FAYL) { return pk_fsync(FAYL); }
int fayl_ölçünü_dəyişmək(int FAYL) { return pk_size(FAYL); }
