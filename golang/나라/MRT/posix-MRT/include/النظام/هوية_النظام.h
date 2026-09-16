/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#ifndef _include_النظام_هوية_النظام
#define _include_النظام_هوية_النظام

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
int جلب_معلومات_النظام(struct utsname *هوية_النظام);
#ifdef __cplusplus
}
#endif

#endif
