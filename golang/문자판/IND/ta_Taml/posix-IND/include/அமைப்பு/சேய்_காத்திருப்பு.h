/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#ifndef _include_அமைப்பு_சேய்_காத்திருப்பு
#define _include_அமைப்பு_சேய்_காத்திருப்பு

#include <அமைப்பு/தரவு_வகைகள்.h>

#define WNOHANG 1
#define WEXITSTATUS(நிலை) (((நிலை) >> 8) & 0xff)
#define WIFEXITED(நிலை) (((நிலை) & 0x7f) == 0)

#ifdef __cplusplus
extern "C" {
#endif
pid_t சேய்க்குக்_காத்திரு(int *நிலை);
pid_t குறித்த_சேய்க்குக்_காத்திரு(pid_t pid, int *நிலை, int options);
#ifdef __cplusplus
}
#endif

#endif
