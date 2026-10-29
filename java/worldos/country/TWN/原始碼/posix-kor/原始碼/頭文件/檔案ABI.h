#ifndef JKOROS_KOREAN_FILE_H
#define JKOROS_KOREAN_FILE_H
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#define 打開檔案 open
#define 創建檔案 creat
#define 讀取檔案資料 read
#define 寫入檔案資料 write
#define 關閉檔案 close
#define 尋道檔案 lseek
#define 複製副本檔案描述符 dup
#define 複製副本檔案描述符位置 dup2
#define 移除檔案條目名稱 unlink
#define 設定檔案長度 ftruncate
#define 提交檔案存儲裝置 fsync
#define 讀取檔案運行狀態 fstat
#define 控制檔案描述符 fcntl
#define 讀取僅用值 O_RDONLY
#define 寫入僅用值 O_WRONLY
#define 讀取寫入 O_RDWR
#define 創建條件缺失 O_CREAT
#define 創建新建檔案 (O_CREAT | O_EXCL)
#define 截斷內容 O_TRUNC
#define 追加位置結束 O_APPEND
#define 執行行爲非判斷等待狀態 O_NONBLOCK
#define 起點開頭 SEEK_SET
#define 當前根 SEEK_CUR
#define 結束原點 SEEK_END
#define 檔案運行狀態 stat
typedef size_t 位元組個數類型;
typedef ssize_t 輸入輸出結果類型;
typedef off_t 檔案偏移類型;
#endif
