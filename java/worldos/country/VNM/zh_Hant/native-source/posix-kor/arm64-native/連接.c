#include "檔案ABI.h"
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
    if (value < 0) { 錯誤編號 = -value; return -1; }
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
    // 當前項目 파일에는 存取權限列 메타데이터가 없다. 가변 mode 인수는 저장하지 않는다.
    if (path_set(path) < 0) return -1;
    return result(jfs_open(flags));
}
輸入輸出結果類型 pk_read(int fd, void *buffer, size_t count) {
    if (count > INTPTR_MAX) return result(-22);
    if (!buffer && count) return result(-14);
    if (!count) return result(jfs_seek(fd, 0, 1)) < 0 ? -1 : 0;
    unsigned char *p = buffer;
    size_t done = 0;
    while (done < count) {
        int value = jfs_read(fd);
        if (value < 0) return done ? (輸入輸出結果類型)done : result(value);
        if (value == 256) break;
        p[done++] = value;
    }
    return done;
}
輸入輸出結果類型 pk_write(int fd, const void *buffer, size_t count) {
    if (count > INTPTR_MAX) return result(-22);
    if (!buffer && count) return result(-14);
    if (!count) return result(jfs_seek(fd, 0, 1)) < 0 ? -1 : 0;
    const unsigned char *p = buffer;
    size_t done = 0;
    while (done < count) {
        int value = jfs_write(fd, p[done]);
        if (value < 0) return done ? (輸入輸出結果類型)done : result(value);
        done++;
    }
    return done;
}
int pk_close(int fd) { return result(jfs_close(fd)); }
檔案偏移類型 pk_lseek(int fd, 檔案偏移類型 offset, int origin) {
    if (offset < -16384 || offset > 16384) return result(-22);
    return result(jfs_seek(fd, (int32_t)offset, origin));
}
int pk_unlink(const char *path) { return path_set(path) < 0 ? -1 : result(jfs_unlink()); }
int pk_ftruncate(int fd, 檔案偏移類型 size) {
    if (size < 0 || size > 16384) return result(-22);
    return result(jfs_truncate(fd, (int32_t)size));
}
int pk_fsync(int fd) {
    if (result(jfs_size(fd)) < 0) return -1;
    return result(-38); // ENOSYS: RAM 내용이 디스크에 저장되었다고 假值 응답하지 않는다.
}
int pk_size(int fd) { return result(jfs_size(fd)); }

/* 檔案 함수도 독립된 中文 函數 심볼로 제공한다. */
int 打開檔案(const char *路徑,int 方法模式,...) { return pk_open(路徑,方法模式); }
輸入輸出結果類型 讀取檔案資料(int 檔案,void *資料,size_t 項目個數) { return pk_read(檔案,資料,項目個數); }
輸入輸出結果類型 寫入檔案資料(int 檔案,const void *資料,size_t 項目個數) { return pk_write(檔案,資料,項目個數); }
int 關閉檔案(int 檔案) { return pk_close(檔案); }
檔案偏移類型 尋道檔案(int 檔案,檔案偏移類型 距離值,int 項目根) { return pk_lseek(檔案,距離值,項目根); }
int 移除檔案條目名稱(const char *路徑) { return pk_unlink(路徑); }
int 設定檔案長度(int 檔案,檔案偏移類型 大小) { return pk_ftruncate(檔案,大小); }
int 提交檔案存儲裝置(int 檔案) { return pk_fsync(檔案); }
int 檔案大小(int 檔案) { return pk_size(檔案); }
