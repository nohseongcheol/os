#ifndef JKOROS_KOREAN_FILE_H
#define JKOROS_KOREAN_FILE_H
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#define ファイル開放 open
#define ファイル作成 creat
#define ファイルデータ読取 read
#define ファイルデータ書込 write
#define ファイル閉鎖 close
#define ファイル位置移動 lseek
#define 複製ファイル記述子 dup
#define 複製ファイル記述子位置 dup2
#define ファイル入口名前除去 unlink
#define ファイル長さ設定 ftruncate
#define 確定ファイル記憶装置 fsync
#define ファイル状態読取 fstat
#define 制御ファイル記述子 fcntl
#define 専用値読取 O_RDONLY
#define 専用値書込 O_WRONLY
#define 読取書込 O_RDWR
#define 作成条件未存在 O_CREAT
#define 新規ファイル作成 (O_CREAT | O_EXCL)
#define 切詰め内容 O_TRUNC
#define 位置終端位置追記 O_APPEND
#define 実施否定待合 O_NONBLOCK
#define 起点先頭 SEEK_SET
#define 現在根 SEEK_CUR
#define 終端位置原点 SEEK_END
#define ファイル状態 stat
typedef size_t バイト個数型;
typedef ssize_t 入出力結果型;
typedef off_t ファイル変位量型;
#endif
