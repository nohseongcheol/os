/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#ifndef _LIBC_UNISTD_H
#define _LIBC_UNISTD_H

#include <அடிப்படை_வரையறைகள்.h>
#include <அமைப்பு/தரவு_வகைகள்.h>

#define STDIN_FILENO 0
#define STDOUT_FILENO 1
#define STDERR_FILENO 2
#define F_OK 0
#define X_OK 1
#define W_OK 2
#define R_OK 4
#define SEEK_SET 0
#define SEEK_CUR 1
#define SEEK_END 2

#ifdef __cplusplus
extern "C" {
#endif
extern char **environ;
void உடனே_முடி(int நிலை) __attribute__((noreturn));
ssize_t படி(int கோப்பு_விவரிப்பி, void *பரிமாற்ற_இடையகம், size_t count);
ssize_t எழுது(int கோப்பு_விவரிப்பி, const void *பரிமாற்ற_இடையகம், size_t count);
int மூடு(int கோப்பு_விவரிப்பி);
off_t கோப்பின்_படிப்பிடத்தை_நகர்த்து(int கோப்பு_விவரிப்பி, off_t offset, int whence);
pid_t சேய்_செயல்முறையை_உருவாக்கு(void);
int இயங்கும்_நிரலை_மாற்று(const char *பாதை, char *const செயலுருபுகள்_2[], char *const envp[]);
pid_t செயல்முறை_அடையாளத்தைப்_பெறு(void);
pid_t தாய்_செயல்முறை_அடையாளத்தைப்_பெறு(void);
uid_t பயனர்_அடையாளத்தைப்_பெறு(void);
uid_t நடப்பு_உரிமைப்_பயனர்_அடையாளத்தைப்_பெறு(void);
gid_t குழு_அடையாளத்தைப்_பெறு(void);
gid_t நடப்பு_உரிமைக்_குழு_அடையாளத்தைப்_பெறு(void);
int அணுகல்_உரிமையைச்_சோதி(const char *பாதை, int mode);
int பணி_அடைவை_மாற்று(const char *பாதை);
char *பணி_அடைவின்_பாதையைப்_பெறு(char *பரிமாற்ற_இடையகம், size_t இலக்கங்களின்_எண்ணிக்கை);
int திறந்த_கோப்பின்_குறிப்பை_நகலெடு(int கோப்பு_விவரிப்பி);
int குறித்த_எண்ணுக்கு_கோப்புக்_குறிப்பை_நகலெடு(int oldfd, int newfd);
int கோப்பின்_பதிவை_ஒத்திசை(int கோப்பு_விவரிப்பி);
void அனைத்துப்_பதிவுகளையும்_ஒத்திசை(void);
int முனையமா_எனச்_சோதி(int கோப்பு_விவரிப்பி);
int மாறும்_நினைவக_முடிவை_அமை(void *address);
void *மாறும்_நினைவக_முடிவை_நகர்த்து(int increment);
#ifdef __cplusplus
}
#endif

#endif
