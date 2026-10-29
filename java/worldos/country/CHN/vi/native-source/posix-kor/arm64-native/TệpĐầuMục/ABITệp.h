#ifndef JKOROS_ARM64_NATIVE_FILE_H
#define JKOROS_ARM64_NATIVE_FILE_H
#include <stddef.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
// 독립된 bare-metal ABI. Linux/i386의 헤더나 libc와 혼합하지 않는다.
typedef intptr_t kiểuKếtQuảVàoRa;
typedef size_t kiểuSốLượngByte;
typedef int64_t kiểuĐộLệchTệp;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
kiểuKếtQuảVàoRa pk_read(int fd, void *buffer, size_t count);
kiểuKếtQuảVàoRa pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
kiểuĐộLệchTệp pk_lseek(int fd, kiểuĐộLệchTệp offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, kiểuĐộLệchTệp size);
int pk_fsync(int fd);
int pk_size(int fd);
int mởTệp(const char *đườngDẫn, int chếĐộPhươngThức, ...);
kiểuKếtQuảVàoRa đọcDữLiệuTệp(int Tệp, void *DữLiệu, size_t sốLượngPhầnMục);
kiểuKếtQuảVàoRa ghiDữLiệuTệp(int Tệp, const void *DữLiệu, size_t sốLượngPhầnMục);
int đóngTệp(int Tệp);
kiểuĐộLệchTệp dịchVịTệp(int Tệp, kiểuĐộLệchTệp giáTrịKhoảngCách, int gốcCâyDựÁn);
int gỡTênMụcTệp(const char *đườngDẫn);
int đặtGiáTrịĐộDàiTệp(int Tệp, kiểuĐộLệchTệp cỡ);
int lưuTrữTệpChốt(int Tệp);
int cỡTệp(int Tệp);
#ifdef __cplusplus
}
#endif
#define sốLỗi (*pk_errno_location())
#define đọcGiáTrịChỉ 0
#define ghiGiáTrịChỉ 1
#define GhiĐọc 2
#define ThiếuNếuTạo 0x40
#define tạoTệpMới 0xc0
#define CácNộiDungCắtNgắn 0x200
#define thêmCuốiKếtThúcTại 0x400
#define PhầnĐầuTừ 0
#define gốcCâyHiệnTại 1
#define gốcKếtThúc 2
#endif
