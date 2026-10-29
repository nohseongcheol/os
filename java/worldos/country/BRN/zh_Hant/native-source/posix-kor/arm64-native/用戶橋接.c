// 동일 中文 헤더를 사용하는 별도 EL0 庫. 內核值 직접 호출판과 혼합 禁用值.
#include "檔案ABI.h"
#include "調用.h"
#include "網路ABI.h"
static int 錯誤程式碼;
int *pk_errno_location(void) { return &錯誤程式碼; }
static intptr_t 已檢查(intptr_t 結果) { if (結果 < 0) { 錯誤程式碼 = -結果; return -1; } return 結果; }
int pk_open(const char *path, int flags, ...) { return 已檢查(用戶調用(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
輸入輸出結果類型 pk_read(int fd, void *p, size_t n) { return 已檢查(用戶調用(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
輸入輸出結果類型 pk_write(int fd, const void *p, size_t n) { return 已檢查(用戶調用(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 已檢查(用戶調用(4, fd, 0, 0, 0, 0, 0)); }
檔案偏移類型 pk_lseek(int fd, 檔案偏移類型 offset, int origin) { return 已檢查(用戶調用(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 已檢查(用戶調用(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, 檔案偏移類型 size) { return 已檢查(用戶調用(10, fd, size, 0, 0, 0, 0)); }
int pk_fsync(int fd) { return 已檢查(用戶調用(12, fd, 0, 0, 0, 0, 0)); }
int pk_size(int fd) { return 已檢查(用戶調用(9, fd, 0, 0, 0, 0, 0)); }
int pk_socket(int domain, int type, int protocol) { return 已檢查(用戶調用(32, domain, type, protocol, 0, 0, 0)); }
int pk_bind(int fd, const struct pk_sockaddr *address, pk_socklen_t length) {
    return 已檢查(用戶調用(33, fd, (uintptr_t)address, length, 0, 0, 0));
}
intptr_t pk_sendto(int fd, const void *buffer, size_t count, int flags, const struct pk_sockaddr *address, pk_socklen_t length) {
    return 已檢查(用戶調用(34, fd, (uintptr_t)buffer, count, flags, (uintptr_t)address, length));
}
intptr_t pk_recvfrom(int fd, void *buffer, size_t count, int flags, struct pk_sockaddr *address, pk_socklen_t *length) {
    return 已檢查(用戶調用(35, fd, (uintptr_t)buffer, count, flags, (uintptr_t)address, (uintptr_t)length));
}
int pk_getsockname(int fd, struct pk_sockaddr *address, pk_socklen_t *length) {
    return 已檢查(用戶調用(36, fd, (uintptr_t)address, (uintptr_t)length, 0, 0, 0));
}
int pk_connect(int fd,const struct pk_sockaddr *address,pk_socklen_t length){return 已檢查(用戶調用(37,fd,(uintptr_t)address,length,0,0,0));}
int pk_listen(int fd,int backlog){return 已檢查(用戶調用(38,fd,backlog,0,0,0,0));}
int pk_accept(int fd,struct pk_sockaddr *address,pk_socklen_t *length){return 已檢查(用戶調用(39,fd,(uintptr_t)address,(uintptr_t)length,0,0,0));}

/* 中文 공개 함수의 實際資料 EL0 實現. 구조체는 SVC에서 複製值·검증한다. */
int 創建端點(int 地址族,int 通信模式,int 傳送通訊協定) {
    return 已檢查(用戶調用(32,地址族,通信模式,傳送通訊協定,0,0,0));
}
int 綁定地址(int 端點,const struct 通訊端地址 *地址,通訊端地址長度類型 長度) {
    return 已檢查(用戶調用(33,端點,(uintptr_t)地址,長度,0,0,0));
}
intptr_t 發送數據報資料(int 端點,const void *資料,size_t 項目個數,int 選中狀態值,const struct 通訊端地址 *地址,通訊端地址長度類型 長度) {
    return 已檢查(用戶調用(34,端點,(uintptr_t)資料,項目個數,選中狀態值,(uintptr_t)地址,長度));
}
intptr_t 接收數據報資料(int 端點,void *資料,size_t 項目個數,int 選中狀態值,struct 通訊端地址 *地址,通訊端地址長度類型 *長度) {
    return 已檢查(用戶調用(35,端點,(uintptr_t)資料,項目個數,選中狀態值,(uintptr_t)地址,(uintptr_t)長度));
}
int 讀取通訊端地址(int 端點,struct 通訊端地址 *地址,通訊端地址長度類型 *長度) {
    return 已檢查(用戶調用(36,端點,(uintptr_t)地址,(uintptr_t)長度,0,0,0));
}
int 連接網路(int 端點,const struct 通訊端地址 *地址,通訊端地址長度類型 長度) {
    return 已檢查(用戶調用(37,端點,(uintptr_t)地址,長度,0,0,0));
}
int 等待狀態用於網路連接狀態(int 端點,int 等待中個數) {
    return 已檢查(用戶調用(38,端點,等待中個數,0,0,0,0));
}
int 接受網路連接狀態(int 端點,struct 通訊端地址 *地址,通訊端地址長度類型 *長度) {
    return 已檢查(用戶調用(39,端點,(uintptr_t)地址,(uintptr_t)長度,0,0,0));
}

/* 檔案 함수도 독립된 中文 函數 심볼로 제공한다. */
int 打開檔案(const char *路徑,int 方法模式,...) { return 已檢查(用戶調用(3,(uintptr_t)路徑,方法模式,0,0,0,0)); }
輸入輸出結果類型 讀取檔案資料(int 檔案,void *資料,size_t 項目個數) { return 已檢查(用戶調用(2,檔案,(uintptr_t)資料,項目個數,0,0,0)); }
輸入輸出結果類型 寫入檔案資料(int 檔案,const void *資料,size_t 項目個數) { return 已檢查(用戶調用(1,檔案,(uintptr_t)資料,項目個數,0,0,0)); }
int 關閉檔案(int 檔案) { return 已檢查(用戶調用(4,檔案,0,0,0,0,0)); }
檔案偏移類型 尋道檔案(int 檔案,檔案偏移類型 距離值,int 項目根) { return 已檢查(用戶調用(5,檔案,距離值,項目根,0,0,0)); }
int 移除檔案條目名稱(const char *路徑) { return 已檢查(用戶調用(11,(uintptr_t)路徑,0,0,0,0,0)); }
int 設定檔案長度(int 檔案,檔案偏移類型 大小) { return 已檢查(用戶調用(10,檔案,大小,0,0,0,0)); }
int 提交檔案存儲裝置(int 檔案) { return 已檢查(用戶調用(12,檔案,0,0,0,0,0)); }
int 檔案大小(int 檔案) { return 已檢查(用戶調用(9,檔案,0,0,0,0,0)); }
