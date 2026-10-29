#ifndef JKOROS_KOREAN_FILE_H
#define JKOROS_KOREAN_FILE_H
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#define skapa_fil open
#define Skapa_fil creat
#define läsa_fil_data read
#define skriva_fil_data write
#define Stäng_fil close
#define söka_fil lseek
#define 파일서술자복제 dup
#define 파일서술자지정복제 dup2
#define ta_bort_fil_post_namn unlink
#define uppsättning_fil_längd ftruncate
#define incheckning_Files fsync
#define läsa_fil_status fstat
#define 파일서술자제어 fcntl
#define skrivskyddad_värde O_RDONLY
#define 쓰기전용 O_WRONLY
#define läsa_skriva O_RDWR
#define 없으면만들기 O_CREAT
#define 새파일만들기 (O_CREAT | O_EXCL)
#define trimma_Innehåll O_TRUNC
#define 끝에이어쓰기 O_APPEND
#define 기다리지않기 O_NONBLOCK
#define 처음기준 SEEK_SET
#define aktuellt_rot SEEK_CUR
#define avsluta_origo SEEK_END
#define filstatus stat
typedef size_t byte_ANTAL_Typ;
typedef ssize_t 입출력결과형;
typedef off_t fil_FÖRSKJUTNING_Typ;
#endif
