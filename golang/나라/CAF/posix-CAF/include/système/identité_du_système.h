/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#ifndef _include_système_identité_du_système
#define _include_système_identité_du_système

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
int obtenir_informations_du_système(struct utsname *identité_du_système);
#ifdef __cplusplus
}
#endif

#endif
