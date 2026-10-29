#ifndef JKOROS_ARM64_NATIVE_FILE_H
#define JKOROS_ARM64_NATIVE_FILE_H
#include <stddef.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
// 독립된 bare-metal ABI. Linux/i386의 헤더나 libc와 혼합하지 않는다.
typedef intptr_t ioResultType;
typedef size_t byteCountType;
typedef int64_t fileOffsetType;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
ioResultType pk_read(int fd, void *buffer, size_t count);
ioResultType pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
fileOffsetType pk_lseek(int fd, fileOffsetType offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, fileOffsetType size);
int pk_fsync(int fd);
int pk_size(int fd);
int openFile(const char *path, int methodMode, ...);
ioResultType readFileData(int file, void *data, size_t itemCount);
ioResultType writeFileData(int file, const void *data, size_t itemCount);
int closeFile(int file);
fileOffsetType seekFile(int file, fileOffsetType distanceValue, int projectRoot);
int removeFileEntryName(const char *path);
int setFileLength(int file, fileOffsetType size);
int commitFileStorage(int file);
int fileSize(int file);
#ifdef __cplusplus
}
#endif
#define errorNumber (*pk_errno_location())
#define readOnlyValue 0
#define writeOnlyValue 1
#define ReadWrite 2
#define CreateIfMissing 0x40
#define createNewFile 0xc0
#define TruncateContents 0x200
#define appendAtEnd 0x400
#define FromBeginning 0
#define currentRoot 1
#define endOrigin 2
#endif
