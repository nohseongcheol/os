#ifndef _include_system_system_identity
#define _include_system_system_identity

struct system_identity_2 {
    char system_name[65];
    char node_name[65];
    char system_release[65];
    char system_version[65];
    char machine_kind[65];
};

#ifdef __cplusplus
extern "C" {
#endif
int uname(struct system_identity_2 *system_identity);
#ifdef __cplusplus
}
#endif

#endif
