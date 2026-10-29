#ifndef JKOROS_KOREAN_FILE_H
#define JKOROS_KOREAN_FILE_H
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#define open_Bestand open
#define maken_Bestand creat
#define 파일자료읽기 read
#define schrijven_Bestand_gegevens write
#define Sluiten_Bestand close
#define zoeken_Bestand lseek
#define 파일서술자복제 dup
#define 파일서술자지정복제 dup2
#define verwijderen_Bestand_invoer_naam unlink
#define set_Bestand_tijdsduur ftruncate
#define doorvoeren_Files fsync
#define 파일상태읽기 fstat
#define 파일서술자제어 fcntl
#define alleen_lezen_WAARDE O_RDONLY
#define 쓰기전용 O_WRONLY
#define lezen_schrijven O_RDWR
#define 없으면만들기 O_CREAT
#define 새파일만들기 (O_CREAT | O_EXCL)
#define afkappen_Inhoud O_TRUNC
#define 끝에이어쓰기 O_APPEND
#define 기다리지않기 O_NONBLOCK
#define 처음기준 SEEK_SET
#define actueel_wortel SEEK_CUR
#define beëindigen_oorsprong SEEK_END
#define bestandsstatus stat
typedef size_t byte_AANTAL_TYPE;
typedef ssize_t 입출력결과형;
typedef off_t Bestand_VERSCHUIVING_TYPE;
#endif
