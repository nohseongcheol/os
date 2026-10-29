#ifndef JKOROS_KOREAN_FILE_H
#define JKOROS_KOREAN_FILE_H
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#define otvoriť_Súbor open
#define Create_Súbor creat
#define 파일자료읽기 read
#define zapísať_Súbor_údaje write
#define Zavrieť_Súbor close
#define hľadať_Súbor lseek
#define 파일서술자복제 dup
#define 파일서술자지정복제 dup2
#define odobrať_Súbor_položka_názov unlink
#define množina_Súbor_dĺžka ftruncate
#define potvrdenie_ukladací_priestor_súborov fsync
#define 파일상태읽기 fstat
#define 파일서술자제어 fcntl
#define iba_na_čítanie_VALUE O_RDONLY
#define 쓰기전용 O_WRONLY
#define na_čítanie_a_zapisovanie O_RDWR
#define 없으면만들기 O_CREAT
#define 새파일만들기 (O_CREAT | O_EXCL)
#define skrátiť_Obsah O_TRUNC
#define 끝에이어쓰기 O_APPEND
#define 기다리지않기 O_NONBLOCK
#define 처음기준 SEEK_SET
#define v_termíne_splatnosti_koreň SEEK_CUR
#define 끝기준 SEEK_END
#define Súbor_stav stat
typedef size_t Byte_COUNT_Typ;
typedef ssize_t 입출력결과형;
typedef off_t Súbor_Posun_Typ;
#endif
