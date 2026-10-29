#ifndef JKOROS_FCNTL_H
#define JKOROS_FCNTL_H
#include <sys/types.h>
#define O_RDONLY 0
#define O_WRONLY 1
#define O_RDWR 2
#define O_ACCMODE 3
#define O_CREAT 64
#define O_EXCL 128
#define O_TRUNC 512
#define O_APPEND 1024
#define O_NONBLOCK 2048
#define O_CLOEXEC 524288
#define F_DUPFD 0
#define F_GETFD 1
#define F_SETFD 2
#define F_GETFL 3
#define F_SETFL 4
#define F_DUPFD_CLOEXEC 1030
#define FD_CLOEXEC 1
int open(const char *ຟາຍ_ເຂົ້າໃນ_ຊື່, int ສ້າງ_ການຕັ້ງຄ່າ, ...);
int creat(const char *ຟາຍ_ເຂົ້າໃນ_ຊື່, mode_t 허가);
int fcntl(int 파일서술자, int ຄໍາສັ່ງ_1f12b8e2, ...);
#endif
