#ifndef JKOROS_KOREAN_FILE_H
#define JKOROS_KOREAN_FILE_H
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#define åben_fil open
#define åbne_fil creat
#define 파일자료읽기 read
#define skrive_fil_data write
#define Luk_fil close
#define søge_fil lseek
#define 파일서술자복제 dup
#define 파일서술자지정복제 dup2
#define fjerne_fil_post_navn unlink
#define sæt_fil_varighed ftruncate
#define udføre_Files fsync
#define 파일상태읽기 fstat
#define 파일서술자제어 fcntl
#define skrivebeskyttet_VÆRDI O_RDONLY
#define 쓰기전용 O_WRONLY
#define læse_skrive O_RDWR
#define 없으면만들기 O_CREAT
#define 새파일만들기 (O_CREAT | O_EXCL)
#define afkorte_Indhold O_TRUNC
#define 끝에이어쓰기 O_APPEND
#define 기다리지않기 O_NONBLOCK
#define 처음기준 SEEK_SET
#define aktuel_rod SEEK_CUR
#define afslutte_et_opkald_begyndelsespunkt SEEK_END
#define fil_status stat
typedef size_t byte_TÆL_Type;
typedef ssize_t 입출력결과형;
typedef off_t fil_FORSKYDNING_Type;
#endif
