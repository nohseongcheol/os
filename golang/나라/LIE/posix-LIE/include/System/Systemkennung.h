#ifndef _include_System_Systemkennung
#define _include_System_Systemkennung

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
int Systeminformationen_ermitteln(struct utsname *Systemidentität);
#ifdef __cplusplus
}
#endif

#endif
