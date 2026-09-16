#ifndef _include_система_сведения_о_системе
#define _include_система_сведения_о_системе

struct utsname {
    char sysname[65];
    char nodename[65];
    char release[65];
    char version[65];
    char machine[65];
};

#ifdef __cplusplus
extern "C" {
#endif
int получить_сведения_о_системе(struct utsname *сведения_о_системе);
#ifdef __cplusplus
}
#endif

#endif
