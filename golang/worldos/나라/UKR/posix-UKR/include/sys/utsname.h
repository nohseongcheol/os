#ifndef _LIBC_SYS_UTSNAME_H
#define _LIBC_SYS_UTSNAME_H

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
int uname(struct utsname *відомості_про_систему);
#ifdef __cplusplus
}
#endif

#endif
