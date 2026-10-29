#ifndef JKOROS_ARM64_NATIVE_FILE_H
#define JKOROS_ARM64_NATIVE_FILE_H
#include <stddef.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
// 독립된 bare-metal ABI. Linux/i386의 헤더나 libc와 혼합하지 않는다.
typedef intptr_t 入出力結果型;
typedef size_t バイト個数型;
typedef int64_t ファイル変位量型;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
入出力結果型 pk_read(int fd, void *buffer, size_t count);
入出力結果型 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
ファイル変位量型 pk_lseek(int fd, ファイル変位量型 offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, ファイル変位量型 size);
int pk_fsync(int fd);
int pk_size(int fd);
int ファイル開放(const char *経路, int メソッド方式, ...);
入出力結果型 ファイルデータ読取(int ファイル, void *データ, size_t 項目個数);
入出力結果型 ファイルデータ書込(int ファイル, const void *データ, size_t 項目個数);
int ファイル閉鎖(int ファイル);
ファイル変位量型 ファイル位置移動(int ファイル, ファイル変位量型 距離値, int 計画根);
int ファイル入口名前除去(const char *経路);
int ファイル長さ設定(int ファイル, ファイル変位量型 容量);
int 確定ファイル記憶装置(int ファイル);
int ファイル容量(int ファイル);
#ifdef __cplusplus
}
#endif
#define エラー番号 (*pk_errno_location())
#define 専用値読取 0
#define 専用値書込 1
#define 読取書込 2
#define 作成条件未存在 0x40
#define 新規ファイル作成 0xc0
#define 切詰め内容 0x200
#define 位置終端位置追記 0x400
#define 起点先頭 0
#define 現在根 1
#define 終端位置原点 2
#endif
