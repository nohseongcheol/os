#include <errno.h>
#include <fcntl.h>
#include <அமைப்பு/stat.h>
#include <அமைப்பு/சேய்_காத்திருப்பு.h>
#include <unistd.h>
#include <அமைப்பு/syscall.h>

enum {
    SYS_உடனே_முடி = 1,
    SYS_சேய்_செயல்முறையை_உருவாக்கு = 2,
    SYS_படி = 3,
    SYS_எழுது = 4,
    SYS_மூடு = 6,
    SYS_இயங்கும்_நிரலை_மாற்று = 11,
    SYS_பணி_அடைவை_மாற்று = 12,
    SYS_கோப்பின்_படிப்பிடத்தை_நகர்த்து = 19,
    SYS_செயல்முறை_அடையாளத்தைப்_பெறு = 20,
    SYS_பயனர்_அடையாளத்தைப்_பெறு = 24,
    SYS_அணுகல்_உரிமையைச்_சோதி = 33,
    SYS_அனைத்துப்_பதிவுகளையும்_ஒத்திசை = 36,
    SYS_திறந்த_கோப்பின்_குறிப்பை_நகலெடு = 41,
    SYS_மாறும்_நினைவக_முடிவை_அமை = 45,
    SYS_குழு_அடையாளத்தைப்_பெறு = 47,
    SYS_நடப்பு_உரிமைப்_பயனர்_அடையாளத்தைப்_பெறு = 49,
    SYS_நடப்பு_உரிமைக்_குழு_அடையாளத்தைப்_பெறு = 50,
    SYS_குறித்த_எண்ணுக்கு_கோப்புக்_குறிப்பை_நகலெடு = 63,
    SYS_தாய்_செயல்முறை_அடையாளத்தைப்_பெறு = 64,
    SYS_கோப்பின்_பதிவை_ஒத்திசை = 118,
    SYS_பணி_அடைவின்_பாதையைப்_பெறு = 183
};

#define SC0(n) __syscall6((n), 0, 0, 0, 0, 0, 0)
#define SC1(n,a) __syscall6((n), (long)(a), 0, 0, 0, 0, 0)
#define SC2(n,a,b) __syscall6((n), (long)(a), (long)(b), 0, 0, 0, 0)
#define SC3(n,a,b,c) __syscall6((n), (long)(a), (long)(b), (long)(c), 0, 0, 0)

void உடனே_முடி(int நிலை)
{
    SC1(SYS_உடனே_முடி, நிலை);
    for (;;) {
        __asm__ __volatile__("hlt");
    }
}

ssize_t படி(int கோப்பு_விவரிப்பி, void *பரிமாற்ற_இடையகம், size_t count)
{
    return (ssize_t)__syscall_result(SC3(SYS_படி, கோப்பு_விவரிப்பி, பரிமாற்ற_இடையகம், count));
}

ssize_t எழுது(int கோப்பு_விவரிப்பி, const void *பரிமாற்ற_இடையகம், size_t count)
{
    return (ssize_t)__syscall_result(SC3(SYS_எழுது, கோப்பு_விவரிப்பி, பரிமாற்ற_இடையகம், count));
}

int மூடு(int கோப்பு_விவரிப்பி)
{
    return (int)__syscall_result(SC1(SYS_மூடு, கோப்பு_விவரிப்பி));
}

off_t கோப்பின்_படிப்பிடத்தை_நகர்த்து(int கோப்பு_விவரிப்பி, off_t offset, int whence)
{
    return (off_t)__syscall_result(SC3(SYS_கோப்பின்_படிப்பிடத்தை_நகர்த்து, கோப்பு_விவரிப்பி, offset, whence));
}

pid_t சேய்_செயல்முறையை_உருவாக்கு(void)
{
    return (pid_t)__syscall_result(SC0(SYS_சேய்_செயல்முறையை_உருவாக்கு));
}

int இயங்கும்_நிரலை_மாற்று(const char *பாதை, char *const செயலுருபுகள்_2[], char *const envp[])
{
    return (int)__syscall_result(SC3(SYS_இயங்கும்_நிரலை_மாற்று, பாதை, செயலுருபுகள்_2, envp));
}

pid_t செயல்முறை_அடையாளத்தைப்_பெறு(void) { return (pid_t)SC0(SYS_செயல்முறை_அடையாளத்தைப்_பெறு); }
pid_t தாய்_செயல்முறை_அடையாளத்தைப்_பெறு(void) { return (pid_t)SC0(SYS_தாய்_செயல்முறை_அடையாளத்தைப்_பெறு); }
uid_t பயனர்_அடையாளத்தைப்_பெறு(void) { return (uid_t)SC0(SYS_பயனர்_அடையாளத்தைப்_பெறு); }
uid_t நடப்பு_உரிமைப்_பயனர்_அடையாளத்தைப்_பெறு(void) { return (uid_t)SC0(SYS_நடப்பு_உரிமைப்_பயனர்_அடையாளத்தைப்_பெறு); }
gid_t குழு_அடையாளத்தைப்_பெறு(void) { return (gid_t)SC0(SYS_குழு_அடையாளத்தைப்_பெறு); }
gid_t நடப்பு_உரிமைக்_குழு_அடையாளத்தைப்_பெறு(void) { return (gid_t)SC0(SYS_நடப்பு_உரிமைக்_குழு_அடையாளத்தைப்_பெறு); }

int அணுகல்_உரிமையைச்_சோதி(const char *பாதை, int mode)
{
    return (int)__syscall_result(SC2(SYS_அணுகல்_உரிமையைச்_சோதி, பாதை, mode));
}

int பணி_அடைவை_மாற்று(const char *பாதை)
{
    return (int)__syscall_result(SC1(SYS_பணி_அடைவை_மாற்று, பாதை));
}

char *பணி_அடைவின்_பாதையைப்_பெறு(char *பரிமாற்ற_இடையகம், size_t இலக்கங்களின்_எண்ணிக்கை)
{
    long result = __syscall_result(SC2(SYS_பணி_அடைவின்_பாதையைப்_பெறு, பரிமாற்ற_இடையகம், இலக்கங்களின்_எண்ணிக்கை));
    return result < 0 ? (char *)0 : பரிமாற்ற_இடையகம்;
}

int திறந்த_கோப்பின்_குறிப்பை_நகலெடு(int கோப்பு_விவரிப்பி)
{
    return (int)__syscall_result(SC1(SYS_திறந்த_கோப்பின்_குறிப்பை_நகலெடு, கோப்பு_விவரிப்பி));
}

int குறித்த_எண்ணுக்கு_கோப்புக்_குறிப்பை_நகலெடு(int oldfd, int newfd)
{
    return (int)__syscall_result(SC2(SYS_குறித்த_எண்ணுக்கு_கோப்புக்_குறிப்பை_நகலெடு, oldfd, newfd));
}

int கோப்பின்_பதிவை_ஒத்திசை(int கோப்பு_விவரிப்பி)
{
    return (int)__syscall_result(SC1(SYS_கோப்பின்_பதிவை_ஒத்திசை, கோப்பு_விவரிப்பி));
}

void அனைத்துப்_பதிவுகளையும்_ஒத்திசை(void)
{
    SC0(SYS_அனைத்துப்_பதிவுகளையும்_ஒத்திசை);
}

int முனையமா_எனச்_சோதி(int கோப்பு_விவரிப்பி)
{
    struct கோப்பு_நிலை st;
    if (திறந்த_கோப்பின்_நிலையைப்_பெறு(கோப்பு_விவரிப்பி, &st) < 0)
        return 0;
    if (!S_ISCHR(st.st_mode)) {
        errno = ENOTTY;
        return 0;
    }
    return 1;
}

int மாறும்_நினைவக_முடிவை_அமை(void *address)
{
    long result = SC1(SYS_மாறும்_நினைவக_முடிவை_அமை, address);
    if (result != (long)address) {
        errno = ENOMEM;
        return -1;
    }
    return 0;
}

void *மாறும்_நினைவக_முடிவை_நகர்த்து(int increment)
{
    long current = SC1(SYS_மாறும்_நினைவக_முடிவை_அமை, 0);
    long requested = current + increment;
    if (increment != 0 && மாறும்_நினைவக_முடிவை_அமை((void *)requested) < 0)
        return (void *)-1;
    return (void *)current;
}

pid_t குறித்த_சேய்க்குக்_காத்திரு(pid_t pid, int *நிலை, int options)
{
    long result;
    do {
        result = SC3(7, pid, நிலை, options);
    } while (result == -EAGAIN && (options & WNOHANG) == 0);
    return (pid_t)__syscall_result(result);
}

pid_t சேய்க்குக்_காத்திரு(int *நிலை)
{
    return குறித்த_சேய்க்குக்_காத்திரு(-1, நிலை, 0);
}
