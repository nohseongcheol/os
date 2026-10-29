#ifndef JKOROS_KOREAN_FILE_H
#define JKOROS_KOREAN_FILE_H
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#define készít_Fájl open
#define készít_Fájl_e47823fb creat
#define 파일자료읽기 read
#define ír_Fájl_adat write
#define bezár_Fájl close
#define keres_Fájl lseek
#define 파일서술자복제 dup
#define 파일서술자지정복제 dup2
#define eltávolít_Fájl_bejegyzés_név unlink
#define halmaz_Fájl_hossz ftruncate
#define véglegesít_Files fsync
#define 파일상태읽기 fstat
#define 파일서술자제어 fcntl
#define írásvédett_ÉRTÉK O_RDONLY
#define 쓰기전용 O_WRONLY
#define 읽고쓰기 O_RDWR
#define 없으면만들기 O_CREAT
#define 새파일만들기 (O_CREAT | O_EXCL)
#define vág_Tartalom O_TRUNC
#define 끝에이어쓰기 O_APPEND
#define 기다리지않기 O_NONBLOCK
#define 처음기준 SEEK_SET
#define aktuális_gyök SEEK_CUR
#define megszüntet_eredet SEEK_END
#define Fájl_állapot stat
typedef size_t bájt_DARAB_beír;
typedef ssize_t 입출력결과형;
typedef off_t Fájl_Ofszet_beír;
#endif
