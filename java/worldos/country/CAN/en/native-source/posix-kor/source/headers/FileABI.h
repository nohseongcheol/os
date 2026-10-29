#ifndef JKOROS_KOREAN_FILE_H
#define JKOROS_KOREAN_FILE_H
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#define openFile open
#define createFile creat
#define readFileData read
#define writeFileData write
#define closeFile close
#define seekFile lseek
#define duplicateFileDescriptor dup
#define duplicateFileDescriptorAt dup2
#define removeFileEntryName unlink
#define setFileLength ftruncate
#define commitFileStorage fsync
#define readFileStatus fstat
#define controlFileDescriptor fcntl
#define readOnlyValue O_RDONLY
#define writeOnlyValue O_WRONLY
#define ReadWrite O_RDWR
#define CreateIfMissing O_CREAT
#define createNewFile (O_CREAT | O_EXCL)
#define TruncateContents O_TRUNC
#define appendAtEnd O_APPEND
#define doNotWait O_NONBLOCK
#define FromBeginning SEEK_SET
#define currentRoot SEEK_CUR
#define endOrigin SEEK_END
#define fileStatus stat
typedef size_t byteCountType;
typedef ssize_t ioResultType;
typedef off_t fileOffsetType;
#endif
