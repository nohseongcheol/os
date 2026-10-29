#ifndef _include_அமைப்பு_stat
#define _include_அமைப்பு_stat

#include <அமைப்பு/தரவு_வகைகள்.h>

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

struct கோப்பு_நிலை {
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
int கோப்பு_நிலை(const char *பாதை, struct கோப்பு_நிலை *பரிமாற்ற_இடையகம்);
int இணைப்பின்_சொந்த_நிலையைப்_பெறு(const char *பாதை, struct கோப்பு_நிலை *பரிமாற்ற_இடையகம்);
int திறந்த_கோப்பின்_நிலையைப்_பெறு(int கோப்பு_விவரிப்பி, struct கோப்பு_நிலை *பரிமாற்ற_இடையகம்);
#ifdef __cplusplus
}
#endif

#endif
