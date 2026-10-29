#include "ファイルABI.h"
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
    if (value < 0) { エラー番号 = -value; return -1; }
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
    // 現在項目 파일에는 アクセス許可一覧表 메타데이터가 없다. 가변 mode 인수는 저장하지 않는다.
    if (path_set(path) < 0) return -1;
    return result(jfs_open(flags));
}
入出力結果型 pk_read(int fd, void *buffer, size_t count) {
    if (count > INTPTR_MAX) return result(-22);
    if (!buffer && count) return result(-14);
    if (!count) return result(jfs_seek(fd, 0, 1)) < 0 ? -1 : 0;
    unsigned char *p = buffer;
    size_t done = 0;
    while (done < count) {
        int value = jfs_read(fd);
        if (value < 0) return done ? (入出力結果型)done : result(value);
        if (value == 256) break;
        p[done++] = value;
    }
    return done;
}
入出力結果型 pk_write(int fd, const void *buffer, size_t count) {
    if (count > INTPTR_MAX) return result(-22);
    if (!buffer && count) return result(-14);
    if (!count) return result(jfs_seek(fd, 0, 1)) < 0 ? -1 : 0;
    const unsigned char *p = buffer;
    size_t done = 0;
    while (done < count) {
        int value = jfs_write(fd, p[done]);
        if (value < 0) return done ? (入出力結果型)done : result(value);
        done++;
    }
    return done;
}
int pk_close(int fd) { return result(jfs_close(fd)); }
ファイル変位量型 pk_lseek(int fd, ファイル変位量型 offset, int origin) {
    if (offset < -16384 || offset > 16384) return result(-22);
    return result(jfs_seek(fd, (int32_t)offset, origin));
}
int pk_unlink(const char *path) { return path_set(path) < 0 ? -1 : result(jfs_unlink()); }
int pk_ftruncate(int fd, ファイル変位量型 size) {
    if (size < 0 || size > 16384) return result(-22);
    return result(jfs_truncate(fd, (int32_t)size));
}
int pk_fsync(int fd) {
    if (result(jfs_size(fd)) < 0) return -1;
    return result(-38); // ENOSYS: RAM 내용이 디스크에 저장되었다고 偽値 응답하지 않는다.
}
int pk_size(int fd) { return result(jfs_size(fd)); }

/* ファイル 함수도 독립된 日本語 関数 심볼로 제공한다. */
int ファイル開放(const char *経路,int メソッド方式,...) { return pk_open(経路,メソッド方式); }
入出力結果型 ファイルデータ読取(int ファイル,void *データ,size_t 項目個数) { return pk_read(ファイル,データ,項目個数); }
入出力結果型 ファイルデータ書込(int ファイル,const void *データ,size_t 項目個数) { return pk_write(ファイル,データ,項目個数); }
int ファイル閉鎖(int ファイル) { return pk_close(ファイル); }
ファイル変位量型 ファイル位置移動(int ファイル,ファイル変位量型 距離値,int 計画根) { return pk_lseek(ファイル,距離値,計画根); }
int ファイル入口名前除去(const char *経路) { return pk_unlink(経路); }
int ファイル長さ設定(int ファイル,ファイル変位量型 容量) { return pk_ftruncate(ファイル,容量); }
int 確定ファイル記憶装置(int ファイル) { return pk_fsync(ファイル); }
int ファイル容量(int ファイル) { return pk_size(ファイル); }
