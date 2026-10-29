#ifndef JKOROS_ERRNO_H
#define JKOROS_ERRNO_H
extern int broj_pogreške;
#define errno broj_pogreške
#define EPERM 1
#define ENOENT 2
#define EIO 5
#define EBADF 9
#define EAGAIN 11
#define EWOULDBLOCK EAGAIN
#define ENOMEM 12
#define EACCES 13
#define EFAULT 14
#define EEXIST 17
#define ENODEV 19
#define ENOTDIR 20
#define EISDIR 21
#define EINVAL 22
#define EMFILE 24
#define EFBIG 27
#define ENOSPC 28
#define ESPIPE 29
#define ENAMETOOLONG 36
#define ENOSYS 38
#define EOVERFLOW 75
#define ENOTSOCK 88
#define EDESTADDRREQ 89
#define EMSGSIZE 90
#define ENOPROTOOPT 92
#define EPROTONOSUPPORT 93
#define EOPNOTSUPP 95
#define ENOTSUP EOPNOTSUPP
#define EAFNOSUPPORT 97
#define EADDRINUSE 98
#define EADDRNOTAVAIL 99
#define ENETUNREACH 101
#define ETIMEDOUT 110
#endif
