#ifndef _include_sistema_identidad_del_sistema
#define _include_sistema_identidad_del_sistema

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
int obtener_información_del_sistema(struct utsname *identidad_del_sistema);
#ifdef __cplusplus
}
#endif

#endif
