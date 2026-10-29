#ifndef _include_प्रणाली_प्रणाली_पहचान
#define _include_प्रणाली_प्रणाली_पहचान

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
int प्रणाली_जानकारी_पाना(struct utsname *प्रणाली_की_पहचान);
#ifdef __cplusplus
}
#endif

#endif
