#ifndef JKOROS_ARM64_NATIVE_FILE_H
#define JKOROS_ARM64_NATIVE_FILE_H
#include <stddef.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
// 독립된 bare-metal ABI. Linux/i386의 헤더나 libc와 혼합하지 않는다.
typedef intptr_t 輸入輸出結果類型;
typedef size_t 位元組個數類型;
typedef int64_t 檔案偏移類型;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
輸入輸出結果類型 pk_read(int fd, void *buffer, size_t count);
輸入輸出結果類型 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
檔案偏移類型 pk_lseek(int fd, 檔案偏移類型 offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, 檔案偏移類型 size);
int pk_fsync(int fd);
int pk_size(int fd);
int 打開檔案(const char *路徑, int 方法模式, ...);
輸入輸出結果類型 讀取檔案資料(int 檔案, void *資料, size_t 項目個數);
輸入輸出結果類型 寫入檔案資料(int 檔案, const void *資料, size_t 項目個數);
int 關閉檔案(int 檔案);
檔案偏移類型 尋道檔案(int 檔案, 檔案偏移類型 距離值, int 項目根);
int 移除檔案條目名稱(const char *路徑);
int 設定檔案長度(int 檔案, 檔案偏移類型 大小);
int 提交檔案存儲裝置(int 檔案);
int 檔案大小(int 檔案);
#ifdef __cplusplus
}
#endif
#define 錯誤編號 (*pk_errno_location())
#define 讀取僅用值 0
#define 寫入僅用值 1
#define 讀取寫入 2
#define 創建條件缺失 0x40
#define 創建新建檔案 0xc0
#define 截斷內容 0x200
#define 追加位置結束 0x400
#define 起點開頭 0
#define 當前根 1
#define 結束原點 2
#endif
