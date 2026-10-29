// 동일 日本語 헤더를 사용하는 별도 EL0 ライブラリ. 中核値 직접 호출판과 혼합 禁止対象値.
#include "ファイルABI.h"
#include "呼出.h"
#include "通信網ABI.h"
static int エラーコード;
int *pk_errno_location(void) { return &エラーコード; }
static intptr_t 検査済み(intptr_t 結果) { if (結果 < 0) { エラーコード = -結果; return -1; } return 結果; }
int pk_open(const char *path, int flags, ...) { return 検査済み(利用者呼出(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
入出力結果型 pk_read(int fd, void *p, size_t n) { return 検査済み(利用者呼出(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
入出力結果型 pk_write(int fd, const void *p, size_t n) { return 検査済み(利用者呼出(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 検査済み(利用者呼出(4, fd, 0, 0, 0, 0, 0)); }
ファイル変位量型 pk_lseek(int fd, ファイル変位量型 offset, int origin) { return 検査済み(利用者呼出(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 検査済み(利用者呼出(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, ファイル変位量型 size) { return 検査済み(利用者呼出(10, fd, size, 0, 0, 0, 0)); }
int pk_fsync(int fd) { return 検査済み(利用者呼出(12, fd, 0, 0, 0, 0, 0)); }
int pk_size(int fd) { return 検査済み(利用者呼出(9, fd, 0, 0, 0, 0, 0)); }
int pk_socket(int domain, int type, int protocol) { return 検査済み(利用者呼出(32, domain, type, protocol, 0, 0, 0)); }
int pk_bind(int fd, const struct pk_sockaddr *address, pk_socklen_t length) {
    return 検査済み(利用者呼出(33, fd, (uintptr_t)address, length, 0, 0, 0));
}
intptr_t pk_sendto(int fd, const void *buffer, size_t count, int flags, const struct pk_sockaddr *address, pk_socklen_t length) {
    return 検査済み(利用者呼出(34, fd, (uintptr_t)buffer, count, flags, (uintptr_t)address, length));
}
intptr_t pk_recvfrom(int fd, void *buffer, size_t count, int flags, struct pk_sockaddr *address, pk_socklen_t *length) {
    return 検査済み(利用者呼出(35, fd, (uintptr_t)buffer, count, flags, (uintptr_t)address, (uintptr_t)length));
}
int pk_getsockname(int fd, struct pk_sockaddr *address, pk_socklen_t *length) {
    return 検査済み(利用者呼出(36, fd, (uintptr_t)address, (uintptr_t)length, 0, 0, 0));
}
int pk_connect(int fd,const struct pk_sockaddr *address,pk_socklen_t length){return 検査済み(利用者呼出(37,fd,(uintptr_t)address,length,0,0,0));}
int pk_listen(int fd,int backlog){return 検査済み(利用者呼出(38,fd,backlog,0,0,0,0));}
int pk_accept(int fd,struct pk_sockaddr *address,pk_socklen_t *length){return 検査済み(利用者呼出(39,fd,(uintptr_t)address,(uintptr_t)length,0,0,0));}

/* 日本語 공개 함수의 実際データ EL0 実装. 구조체는 SVC에서 値複写·검증한다. */
int 通信端点作成(int 番地体系,int 通信方式,int 転送通信規約) {
    return 検査済み(利用者呼出(32,番地体系,通信方式,転送通信規約,0,0,0));
}
int 番地結合(int 通信端点,const struct ソケット番地 *番地,ソケット番地長さ型 長さ) {
    return 検査済み(利用者呼出(33,通信端点,(uintptr_t)番地,長さ,0,0,0));
}
intptr_t データグラムデータ送信(int 通信端点,const void *データ,size_t 項目個数,int 選択状態値,const struct ソケット番地 *番地,ソケット番地長さ型 長さ) {
    return 検査済み(利用者呼出(34,通信端点,(uintptr_t)データ,項目個数,選択状態値,(uintptr_t)番地,長さ));
}
intptr_t データグラムデータ受取(int 通信端点,void *データ,size_t 項目個数,int 選択状態値,struct ソケット番地 *番地,ソケット番地長さ型 *長さ) {
    return 検査済み(利用者呼出(35,通信端点,(uintptr_t)データ,項目個数,選択状態値,(uintptr_t)番地,(uintptr_t)長さ));
}
int ソケット番地読取(int 通信端点,struct ソケット番地 *番地,ソケット番地長さ型 *長さ) {
    return 検査済み(利用者呼出(36,通信端点,(uintptr_t)番地,(uintptr_t)長さ,0,0,0));
}
int 通信網接続(int 通信端点,const struct ソケット番地 *番地,ソケット番地長さ型 長さ) {
    return 検査済み(利用者呼出(37,通信端点,(uintptr_t)番地,長さ,0,0,0));
}
int 対象通信網接続状態待合(int 通信端点,int 待機中個数) {
    return 検査済み(利用者呼出(38,通信端点,待機中個数,0,0,0,0));
}
int 通信網接続状態受理(int 通信端点,struct ソケット番地 *番地,ソケット番地長さ型 *長さ) {
    return 検査済み(利用者呼出(39,通信端点,(uintptr_t)番地,(uintptr_t)長さ,0,0,0));
}

/* ファイル 함수도 독립된 日本語 関数 심볼로 제공한다. */
int ファイル開放(const char *経路,int メソッド方式,...) { return 検査済み(利用者呼出(3,(uintptr_t)経路,メソッド方式,0,0,0,0)); }
入出力結果型 ファイルデータ読取(int ファイル,void *データ,size_t 項目個数) { return 検査済み(利用者呼出(2,ファイル,(uintptr_t)データ,項目個数,0,0,0)); }
入出力結果型 ファイルデータ書込(int ファイル,const void *データ,size_t 項目個数) { return 検査済み(利用者呼出(1,ファイル,(uintptr_t)データ,項目個数,0,0,0)); }
int ファイル閉鎖(int ファイル) { return 検査済み(利用者呼出(4,ファイル,0,0,0,0,0)); }
ファイル変位量型 ファイル位置移動(int ファイル,ファイル変位量型 距離値,int 計画根) { return 検査済み(利用者呼出(5,ファイル,距離値,計画根,0,0,0)); }
int ファイル入口名前除去(const char *経路) { return 検査済み(利用者呼出(11,(uintptr_t)経路,0,0,0,0,0)); }
int ファイル長さ設定(int ファイル,ファイル変位量型 容量) { return 検査済み(利用者呼出(10,ファイル,容量,0,0,0,0)); }
int 確定ファイル記憶装置(int ファイル) { return 検査済み(利用者呼出(12,ファイル,0,0,0,0,0)); }
int ファイル容量(int ファイル) { return 検査済み(利用者呼出(9,ファイル,0,0,0,0,0)); }
