/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#ifndef _LIBC_UNISTD_H
#define _LIBC_UNISTD_H

#include <मूल_परिभाषाएँ.h>
#include <प्रणाली/आँकड़ा_प्रकार.h>

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
void तुरंत_समाप्त_करना(int स्थिति) __attribute__((noreturn));
ssize_t पढ़ना(int संचिका_विवरणक, void *स्थानांतरण_का_अस्थायी_भंडार, size_t count);
ssize_t लिखना(int संचिका_विवरणक, const void *स्थानांतरण_का_अस्थायी_भंडार, size_t count);
int बंद_करना(int संचिका_विवरणक);
off_t पठन_लेखन_स्थिति_बदलना(int संचिका_विवरणक, off_t offset, int whence);
pid_t संतान_प्रक्रिया_बनाना(void);
int निष्पादन_सामग्री_बदलना(const char *पथ, char *const तर्क_सूची_2[], char *const envp[]);
pid_t प्रक्रिया_पहचान_पाना(void);
pid_t जनक_प्रक्रिया_पहचान_पाना(void);
uid_t उपयोगकर्ता_पहचान_पाना(void);
uid_t प्रभावी_उपयोगकर्ता_पहचान_पाना(void);
gid_t समूह_पहचान_पाना(void);
gid_t प्रभावी_समूह_पहचान_पाना(void);
int पहुँच_अनुमति_जाँचना(const char *पथ, int mode);
int कार्य_निर्देशिका_बदलना(const char *पथ);
char *कार्य_निर्देशिका_पथ_पाना(char *स्थानांतरण_का_अस्थायी_भंडार, size_t अंकों_की_संख्या);
int खुली_संचिका_संदर्भ_की_प्रतिलिपि_बनाना(int संचिका_विवरणक);
int नियत_क्रमांक_पर_संचिका_संदर्भ_प्रतिलिपि_बनाना(int oldfd, int newfd);
int संचिका_अभिलेख_समकालित_करना(int संचिका_विवरणक);
void सभी_अभिलेख_समकालित_करना(void);
int अंतक_है_या_नहीं_जाँचना(int संचिका_विवरणक);
int गतिशील_स्मृति_अंत_निर्धारित_करना(void *address);
void *गतिशील_स्मृति_अंत_बदलना(int increment);
#ifdef __cplusplus
}
#endif

#endif
