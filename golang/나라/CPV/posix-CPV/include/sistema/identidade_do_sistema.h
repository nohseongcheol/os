#ifndef _include_sistema_identidade_do_sistema
#define _include_sistema_identidade_do_sistema

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
int obter_informações_do_sistema(struct utsname *identidade_do_sistema);
#ifdef __cplusplus
}
#endif

#endif
