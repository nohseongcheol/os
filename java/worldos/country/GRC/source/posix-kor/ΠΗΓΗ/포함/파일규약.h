#ifndef JKOROS_KOREAN_FILE_H
#define JKOROS_KOREAN_FILE_H
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#define ανοίγω_Αρχείο open
#define ανοίγω_Αρχείο_e47823fb creat
#define 파일자료읽기 read
#define εγγράφω_Αρχείο_δεδομένα write
#define κλείνω_Αρχείο close
#define αναζητώ_Αρχείο lseek
#define 파일서술자복제 dup
#define 파일서술자지정복제 dup2
#define καταργώ_Αρχείο_καταχώρηση_όνομα unlink
#define σύνολο_Αρχείο_διάρκεια ftruncate
#define δέσμευση_Αρχεία fsync
#define 파일상태읽기 fstat
#define 파일서술자제어 fcntl
#define μόνο_για_ανάγνωση_τιμή O_RDONLY
#define μόνο_για_εγγραφή_τιμή O_WRONLY
#define 읽고쓰기 O_RDWR
#define 없으면만들기 O_CREAT
#define 새파일만들기 (O_CREAT | O_EXCL)
#define περικοπή_Περιεχόμενα O_TRUNC
#define 끝에이어쓰기 O_APPEND
#define 기다리지않기 O_NONBLOCK
#define 처음기준 SEEK_SET
#define τρέχων_ρίζα SEEK_CUR
#define Τελική_οντότητα_προέλευση SEEK_END
#define Αρχείο_κατάσταση stat
typedef size_t 바이트수형;
typedef ssize_t 입출력결과형;
typedef off_t Αρχείο_Υπέρθεση_Τύπος;
#endif
