#ifndef _LIBC_FCNTL_H
#define _LIBC_FCNTL_H

#include <प्रणाली/आँकड़ा_प्रकार.h>

#define O_RDONLY 0x0000
#define O_WRONLY 0x0001
#define O_RDWR 0x0002
#define O_ACCMODE 0x0003
#define O_CREAT 0x0040
#define O_EXCL 0x0080
#define O_TRUNC 0x0200
#define O_APPEND 0x0400
#define O_DIRECTORY 0x10000

#define F_DUPFD 0
#define F_GETFD 1
#define F_SETFD 2
#define F_GETFL 3
#define F_SETFL 4
#define FD_CLOEXEC 1

#ifdef __cplusplus
extern "C" {
#endif
int खोलना(const char *पथ, int oflag, ...);
int संचिका_बनाना(const char *पथ, mode_t mode);
int संचिका_नियंत्रित_करना(int संचिका_विवरणक, int cmd, ...);
#ifdef __cplusplus
}
#endif

#endif
