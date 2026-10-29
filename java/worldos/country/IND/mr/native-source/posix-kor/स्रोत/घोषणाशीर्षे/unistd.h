#ifndef JKOROS_UNISTD_H
#define JKOROS_UNISTD_H
#include <sys/types.h>
#define STDIN_FILENO 0
#define STDOUT_FILENO 1
#define STDERR_FILENO 2
#define SEEK_SET 0
#define SEEK_CUR 1
#define SEEK_END 2
ssize_t read(int संचिका_विवरणक, void *डेटा, size_t बाइट_संख्या);
ssize_t write(int संचिका_विवरणक, const void *डेटा, size_t बाइट_संख्या);
int close(int संचिका_विवरणक);
off_t lseek(int संचिका_विवरणक, off_t ऑफसेट_मूल्य, int प्रोजेक्ट_मूळ);
int dup(int संचिका_विवरणक);
int dup2(int संचिका_विवरणक, int नवे_विवरणक);
int unlink(const char *संचिका_प्रविष्टी_नाव);
int ftruncate(int संचिका_विवरणक, off_t बाइट_संख्या);
int fsync(int संचिका_विवरणक);
void _exit(int निर्गमन_करा_संहिता) __attribute__((noreturn));
#endif
