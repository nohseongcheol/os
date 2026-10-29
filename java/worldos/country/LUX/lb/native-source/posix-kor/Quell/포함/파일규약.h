#ifndef JKOROS_KOREAN_FILE_H
#define JKOROS_KOREAN_FILE_H
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#define ariichten_Fichier open
#define Create_Fichier creat
#define 파일자료읽기 read
#define schreiwen_Fichier_Daten write
#define Clôture_Fichier close
#define sichen_Fichier lseek
#define 파일서술자복제 dup
#define 파일서술자지정복제 dup2
#define ewechhuelen_Fichier_Agab_Numm unlink
#define Saz_Fichier_Längt ftruncate
#define 파일저장확정 fsync
#define 파일상태읽기 fstat
#define 파일서술자제어 fcntl
#define schreifgeschützt_VALUE O_RDONLY
#define 쓰기전용 O_WRONLY
#define lies_schreiffäeg O_RDWR
#define 없으면만들기 O_CREAT
#define 새파일만들기 (O_CREAT | O_EXCL)
#define 내용비우기 O_TRUNC
#define 끝에이어쓰기 O_APPEND
#define 기다리지않기 O_NONBLOCK
#define 처음기준 SEEK_SET
#define 현재기준 SEEK_CUR
#define 끝기준 SEEK_END
#define Fichier_Status stat
typedef size_t Byte_COUNT_TYPE;
typedef ssize_t 입출력결과형;
typedef off_t Fichier_OFFSET_TYPE;
#endif
