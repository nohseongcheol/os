/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#ifndef _LIBC_FCNTL_H
#define _LIBC_FCNTL_H

#include <système/types_de_données.h>

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
int ouvrir(const char *chemin, int oflag, ...);
int créer_un_fichier(const char *chemin, mode_t mode);
int contrôler_le_fichier(int descripteur_de_fichier, int cmd, ...);
#ifdef __cplusplus
}
#endif

#endif
