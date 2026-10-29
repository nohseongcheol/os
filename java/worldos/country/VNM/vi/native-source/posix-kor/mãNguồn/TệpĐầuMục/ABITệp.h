#ifndef JKOROS_KOREAN_FILE_H
#define JKOROS_KOREAN_FILE_H
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#define mởTệp open
#define tạoTệp creat
#define đọcDữLiệuTệp read
#define ghiDữLiệuTệp write
#define đóngTệp close
#define dịchVịTệp lseek
#define bộMôTảTệpBảnSao dup
#define tạiBộMôTảTệpBảnSao dup2
#define gỡTênMụcTệp unlink
#define đặtGiáTrịĐộDàiTệp ftruncate
#define lưuTrữTệpChốt fsync
#define đọcTìnhTrạngTệp fstat
#define bộMôTảTệpĐiềuKhiển fcntl
#define đọcGiáTrịChỉ O_RDONLY
#define ghiGiáTrịChỉ O_WRONLY
#define GhiĐọc O_RDWR
#define ThiếuNếuTạo O_CREAT
#define tạoTệpMới (O_CREAT | O_EXCL)
#define CácNộiDungCắtNgắn O_TRUNC
#define thêmCuốiKếtThúcTại O_APPEND
#define chờKhôngThựcHiện O_NONBLOCK
#define PhầnĐầuTừ SEEK_SET
#define gốcCâyHiệnTại SEEK_CUR
#define gốcKếtThúc SEEK_END
#define tìnhTrạngTệp stat
typedef size_t kiểuSốLượngByte;
typedef ssize_t kiểuKếtQuảVàoRa;
typedef off_t kiểuĐộLệchTệp;
#endif
