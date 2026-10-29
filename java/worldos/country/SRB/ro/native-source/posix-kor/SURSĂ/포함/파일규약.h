#ifndef JKOROS_KOREAN_FILE_H
#define JKOROS_KOREAN_FILE_H
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#define crea_Fișier open
#define crea_Fișier_e47823fb creat
#define 파일자료읽기 read
#define scriere_Fișier_date write
#define închide_Fișier close
#define căuta_Fișier lseek
#define 파일서술자복제 dup
#define 파일서술자지정복제 dup2
#define elimina_Fișier_intrare_nume unlink
#define set_Fișier_lungime ftruncate
#define comitere_Fișiere fsync
#define 파일상태읽기 fstat
#define 파일서술자제어 fcntl
#define doar_în_citire_VALUE O_RDONLY
#define 쓰기전용 O_WRONLY
#define citire_scriere O_RDWR
#define 없으면만들기 O_CREAT
#define 새파일만들기 (O_CREAT | O_EXCL)
#define trunchia_TOC O_TRUNC
#define 끝에이어쓰기 O_APPEND
#define 기다리지않기 O_NONBLOCK
#define 처음기준 SEEK_SET
#define curent_rădăcină SEEK_CUR
#define 끝기준 SEEK_END
#define Fișier_stare stat
typedef size_t byte_COUNT_Tip;
typedef ssize_t 입출력결과형;
typedef off_t Fișier_OFFSET_Tip;
#endif
