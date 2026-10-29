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
typedef int64_t Αρχείο_Υπέρθεση_Τύπος;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
Αρχείο_Υπέρθεση_Τύπος pk_lseek(int fd, Αρχείο_Υπέρθεση_Τύπος offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, Αρχείο_Υπέρθεση_Τύπος size);
int pk_fsync(int fd);
int pk_size(int fd);
int ανοίγω_Αρχείο(const char *ΔΙΑΔΡΟΜΗ, int μέθοδος_λειτουργία, ...);
입출력결과형 파일자료읽기(int Αρχείο, void *δεδομένα, size_t 개수);
입출력결과형 εγγράφω_Αρχείο_δεδομένα(int Αρχείο, const void *δεδομένα, size_t 개수);
int κλείνω_Αρχείο(int Αρχείο);
Αρχείο_Υπέρθεση_Τύπος αναζητώ_Αρχείο(int Αρχείο, Αρχείο_Υπέρθεση_Τύπος 거리, int έργο_ρίζα);
int καταργώ_Αρχείο_καταχώρηση_όνομα(const char *ΔΙΑΔΡΟΜΗ);
int σύνολο_Αρχείο_διάρκεια(int Αρχείο, Αρχείο_Υπέρθεση_Τύπος Μέγεθος);
int δέσμευση_Αρχεία(int Αρχείο);
int μέγεθος_αρχείου(int Αρχείο);
#ifdef __cplusplus
}
#endif
#define αριθμός_σφάλματος (*pk_errno_location())
#define μόνο_για_ανάγνωση_τιμή 0
#define μόνο_για_εγγραφή_τιμή 1
#define 읽고쓰기 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define περικοπή_Περιεχόμενα 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define τρέχων_ρίζα 1
#define Τελική_οντότητα_προέλευση 2
#endif
