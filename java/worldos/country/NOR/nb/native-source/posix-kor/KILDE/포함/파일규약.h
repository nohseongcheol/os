#ifndef JKOROS_KOREAN_FILE_H
#define JKOROS_KOREAN_FILE_H
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#define åpen_Fil open
#define åpne_Fil creat
#define 파일자료읽기 read
#define skrive_Fil_data write
#define Lukk_Fil close
#define søk_Fil lseek
#define 파일서술자복제 dup
#define 파일서술자지정복제 dup2
#define fjerne_Fil_oppføring_navn unlink
#define sett_Fil_lengde ftruncate
#define 파일저장확정 fsync
#define 파일상태읽기 fstat
#define 파일서술자제어 fcntl
#define skrivebeskyttet_VERDI O_RDONLY
#define 쓰기전용 O_WRONLY
#define lese_og_skrive O_RDWR
#define 없으면만들기 O_CREAT
#define 새파일만들기 (O_CREAT | O_EXCL)
#define avkorte_Innhold O_TRUNC
#define 끝에이어쓰기 O_APPEND
#define 기다리지않기 O_NONBLOCK
#define 처음기준 SEEK_SET
#define betalt_rot SEEK_CUR
#define avslutte_en_samtale_origo SEEK_END
#define Fil_status stat
typedef size_t byte_ANTALL_Type;
typedef ssize_t 입출력결과형;
typedef off_t Fil_FORSKYVNING_Type;
#endif
