#ifndef _include_النظام_stat
#define _include_النظام_stat

#include <النظام/أنواع_البيانات.h>

#define S_IFMT 0170000
#define S_IFDIR 0040000
#define S_IFCHR 0020000
#define S_IFREG 0100000
#define S_IRUSR 0400
#define S_IWUSR 0200
#define S_IXUSR 0100
#define S_IRGRP 0040
#define S_IWGRP 0020
#define S_IXGRP 0010
#define S_IROTH 0004
#define S_IWOTH 0002
#define S_IXOTH 0001
#define S_ISDIR(m) (((m) & S_IFMT) == S_IFDIR)
#define S_ISCHR(m) (((m) & S_IFMT) == S_IFCHR)
#define S_ISREG(m) (((m) & S_IFMT) == S_IFREG)

struct حالة_الملف {
    dev_t st_dev;
    ino_t st_ino;
    mode_t st_mode;
    nlink_t st_nlink;
    uid_t st_uid;
    gid_t st_gid;
    dev_t st_rdev;
    off_t st_size;
    blksize_t st_blksize;
    blkcnt_t st_blocks;
    time_t st_atime;
    int st_atimensec;
    time_t st_mtime;
    int st_mtimensec;
    time_t st_ctime;
    int st_ctimensec;
};

#ifdef __cplusplus
extern "C" {
#endif
int حالة_الملف(const char *المسار, struct حالة_الملف *مخزن_النقل_المؤقت);
int جلب_حالة_الرابط_نفسه(const char *المسار, struct حالة_الملف *مخزن_النقل_المؤقت);
int جلب_حالة_الملف_المفتوح(int واصف_الملف, struct حالة_الملف *مخزن_النقل_المؤقت);
#ifdef __cplusplus
}
#endif

#endif
