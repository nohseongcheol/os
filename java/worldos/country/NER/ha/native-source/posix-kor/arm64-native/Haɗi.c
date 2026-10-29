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
    // 현재 파일에는 umurni 메타데이터가 없다. 가변 mode 인수는 저장하지 않는다.
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
Fayil_Sassautawa_rubuta pk_lseek(int fd, Fayil_Sassautawa_rubuta offset, int origin) {
    if (offset < -16384 || offset > 16384) return result(-22);
    return result(jfs_seek(fd, (int32_t)offset, origin));
}
int pk_unlink(const char *path) { return path_set(path) < 0 ? -1 : result(jfs_unlink()); }
int pk_ftruncate(int fd, Fayil_Sassautawa_rubuta size) {
    if (size < 0 || size > 16384) return result(-22);
    return result(jfs_truncate(fd, (int32_t)size));
}
int pk_fsync(int fd) {
    if (result(jfs_size(fd)) < 0) return -1;
    return result(-38); // ENOSYS: RAM 내용이 디스크에 저장되었다고 거짓 응답하지 않는다.
}
int pk_size(int fd) { return result(jfs_size(fd)); }

/* Fayil 함수도 독립된 한국어 AIKI_Daraja 심볼로 제공한다. */
int buɗe_Fayil(const char *Hanyar_shiga,int tsari_yanayin_aiki,...) { return pk_open(Hanyar_shiga,tsari_yanayin_aiki); }
입출력결과형 파일자료읽기(int Fayil,void *Tarin_bayani,size_t 개수) { return pk_read(Fayil,Tarin_bayani,개수); }
입출력결과형 Rubuta_Fayil_Tarin_bayani(int Fayil,const void *Tarin_bayani,size_t 개수) { return pk_write(Fayil,Tarin_bayani,개수); }
int Rufe_Fayil(int Fayil) { return pk_close(Fayil); }
Fayil_Sassautawa_rubuta binciko_Fayil(int Fayil,Fayil_Sassautawa_rubuta 거리,int 기준) { return pk_lseek(Fayil,거리,기준); }
int Cire_Fayil_Mashigar_bayanai_Suna(const char *Hanyar_shiga) { return pk_unlink(Hanyar_shiga); }
int zubi_Fayil_Tsawo(int Fayil,Fayil_Sassautawa_rubuta Girma) { return pk_ftruncate(Fayil,Girma); }
int 파일저장확정(int Fayil) { return pk_fsync(Fayil); }
int Fayil_girma(int Fayil) { return pk_size(Fayil); }
