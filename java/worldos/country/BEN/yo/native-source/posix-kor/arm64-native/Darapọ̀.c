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
    // 현재 파일에는 ìyànda 메타데이터가 없다. 가변 mode 인수는 저장하지 않는다.
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
fáìlì_Ìtayọ_irú pk_lseek(int fd, fáìlì_Ìtayọ_irú offset, int origin) {
    if (offset < -16384 || offset > 16384) return result(-22);
    return result(jfs_seek(fd, (int32_t)offset, origin));
}
int pk_unlink(const char *path) { return path_set(path) < 0 ? -1 : result(jfs_unlink()); }
int pk_ftruncate(int fd, fáìlì_Ìtayọ_irú size) {
    if (size < 0 || size > 16384) return result(-22);
    return result(jfs_truncate(fd, (int32_t)size));
}
int pk_fsync(int fd) {
    if (result(jfs_size(fd)) < 0) return -1;
    return result(-38); // ENOSYS: RAM 내용이 디스크에 저장되었다고 거짓 응답하지 않는다.
}
int pk_size(int fd) { return result(jfs_size(fd)); }

/* Fáìlì 함수도 독립된 한국어 ÀKÀNṢEFỌMÚLÀ_iye 심볼로 제공한다. */
int ṣí_fáìlì(const char *ọ̀nà,int ìlànà_móòdù,...) { return pk_open(ọ̀nà,ìlànà_móòdù); }
입출력결과형 파일자료읽기(int Fáìlì,void *détà,size_t 개수) { return pk_read(Fáìlì,détà,개수); }
입출력결과형 kọ_fáìlì_détà(int Fáìlì,const void *détà,size_t 개수) { return pk_write(Fáìlì,détà,개수); }
int pa_dé_fáìlì(int Fáìlì) { return pk_close(Fáìlì); }
fáìlì_Ìtayọ_irú ṣàwárí_fáìlì(int Fáìlì,fáìlì_Ìtayọ_irú 거리,int 기준) { return pk_lseek(Fáìlì,거리,기준); }
int ṣèmúkúro_fáìlì_ìgbéwọlé_orúkọ(const char *ọ̀nà) { return pk_unlink(ọ̀nà); }
int ọ̀wọ̀_fáìlì_gígùn(int Fáìlì,fáìlì_Ìtayọ_irú Ìwọ̀n) { return pk_ftruncate(Fáìlì,Ìwọ̀n); }
int 파일저장확정(int Fáìlì) { return pk_fsync(Fáìlì); }
int fáìlì_ìwọn(int Fáìlì) { return pk_size(Fáìlì); }
