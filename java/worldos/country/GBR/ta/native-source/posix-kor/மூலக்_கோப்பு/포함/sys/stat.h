#ifndef JKOROS_STAT_H
#define JKOROS_STAT_H
#include <sys/types.h>
/* jkoros i386 전용 48바이트 ABI. 다른 운영체제의 struct stat과 섞지 않는다. */
struct stat {
    dev_t st_dev;
    ino_t st_ino;
    mode_t st_mode;
    nlink_t st_nlink;
    uid_t st_uid;
    gid_t st_gid;
    dev_t st_rdev;
    off_t st_size;
    int st_blksize, st_blocks;
    int jkoros_reserved[2];
};
#define S_IFMT 0170000
#define S_IFREG 0100000
#define S_IFCHR 0020000
#define S_IFSOCK 0140000
#define S_ISREG(மதிப்பு) (((மதிப்பு) & S_IFMT) == S_IFREG)
#define S_ISCHR(மதிப்பு) (((மதிப்பு) & S_IFMT) == S_IFCHR)
#define S_ISSOCK(மதிப்பு) (((மதிப்பு) & S_IFMT) == S_IFSOCK)
int fstat(int 파일서술자, struct stat *நிலை_மதிப்பு_e10195a1);
#endif
