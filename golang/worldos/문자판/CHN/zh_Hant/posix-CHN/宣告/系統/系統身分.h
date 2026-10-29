#ifndef _宣告_系統_系統身分
#define _宣告_系統_系統身分

struct 系統身分資訊 {
    char 系統名稱[65];
    char 節點名稱[65];
    char 系統發行版[65];
    char 系統修訂版[65];
    char 機器類型[65];
};

#ifdef __cplusplus
extern "C" {
#endif
int 取得系統資訊(struct 系統身分資訊 *系統資料);
#ifdef __cplusplus
}
#endif

#endif
