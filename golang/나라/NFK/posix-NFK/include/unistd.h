/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#ifndef _LIBC_UNISTD_H
#define _LIBC_UNISTD_H

#include <basic_definitions.h>
#include <system/data_types.h>

#define standard_input_descriptor 0
#define standard_output_descriptor 1
#define standard_error_descriptor 2
#define test_existence 0
#define test_execute_permission 1
#define test_write_permission 2
#define test_read_permission 4
#define offset_from_start 0
#define offset_from_current 1
#define offset_from_end 2

#ifdef __cplusplus
extern "C" {
#endif
extern char **environ;
void _exit(int status) __attribute__((noreturn));
signed_size_type read(int file_descriptor, void *transfer_buffer, object_size_type count);
signed_size_type write(int file_descriptor, const void *transfer_buffer, object_size_type count);
int close(int file_descriptor);
file_offset_type lseek(int file_descriptor, file_offset_type offset, int whence);
process_identifier_type fork(void);
int execve(const char *path, char *const arguments_2[], char *const envp[]);
process_identifier_type getpid(void);
process_identifier_type getppid(void);
user_identifier_type getuid(void);
user_identifier_type geteuid(void);
group_identifier_type getgid(void);
group_identifier_type getegid(void);
int access(const char *path, int mode);
int chdir(const char *path);
char *getcwd(char *transfer_buffer, object_size_type digit_count);
int dup(int file_descriptor);
int dup2(int oldfd, int newfd);
int fsync(int file_descriptor);
void sync(void);
int isatty(int file_descriptor);
int brk(void *address);
void *sbrk(int increment);
#ifdef __cplusplus
}
#endif

#endif
