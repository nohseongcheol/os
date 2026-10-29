#ifndef JKOROS_ARM64_NATIVE_FILE_H
#define JKOROS_ARM64_NATIVE_FILE_H
#include <stddef.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
// 독립된 bare-metal ABI. Linux/i386의 헤더나 libc와 혼합하지 않는다.
typedef intptr_t 입출력결과형;
typedef size_t 바이트수형;
typedef int64_t ಫೈಲ್_ಆಫ್_ಸೆಟ್_ಪ್ರಕಾರ;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
ಫೈಲ್_ಆಫ್_ಸೆಟ್_ಪ್ರಕಾರ pk_lseek(int fd, ಫೈಲ್_ಆಫ್_ಸೆಟ್_ಪ್ರಕಾರ offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, ಫೈಲ್_ಆಫ್_ಸೆಟ್_ಪ್ರಕಾರ size);
int pk_fsync(int fd);
int pk_size(int fd);
int ರಚಿಸು_ಫೈಲ್(const char *ಮಾರ್ಗ, int ವಿಧಾನ_ಮೋಡ್, ...);
입출력결과형 파일자료읽기(int ಕಡತ, void *ಡೇಟಾ, size_t 개수);
입출력결과형 ಬರೆ_ಫೈಲ್_ಡೇಟಾ(int ಕಡತ, const void *ಡೇಟಾ, size_t 개수);
int ಮುಚ್ಚು_ಫೈಲ್(int ಕಡತ);
ಫೈಲ್_ಆಫ್_ಸೆಟ್_ಪ್ರಕಾರ ಸೀಕ್_ಫೈಲ್(int ಕಡತ, ಫೈಲ್_ಆಫ್_ಸೆಟ್_ಪ್ರಕಾರ 거리, int ಬಿಂಬಿಸು_ಮೂಲ);
int ತೆಗೆ_ಫೈಲ್_ನಮೂದು_ಹೆಸರು(const char *ಮಾರ್ಗ);
int ಸೆಟ್_ಫೈಲ್_ಉದ್ದ(int ಕಡತ, ಫೈಲ್_ಆಫ್_ಸೆಟ್_ಪ್ರಕಾರ ಗಾತ್ರ);
int 파일저장확정(int ಕಡತ);
int ಫೈಲ್_ಗಾತ್ರಿಸು(int ಕಡತ);
#ifdef __cplusplus
}
#endif
#define 오류번호 (*pk_errno_location())
#define ಓದಲು_ಮಾತ್ರ_ಮೌಲ್ಯ 0
#define 쓰기전용 1
#define ಓದು_ಬರೆ 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define 내용비우기 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define 현재기준 1
#define 끝기준 2
#endif
