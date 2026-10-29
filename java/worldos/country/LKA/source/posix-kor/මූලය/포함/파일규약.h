#ifndef JKOROS_KOREAN_FILE_H
#define JKOROS_KOREAN_FILE_H
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#define සාදන්න_ගොනුව open
#define සාදන්න_ගොනුව_e47823fb creat
#define 파일자료읽기 read
#define ලියන්න_ගොනුව_දත්ත write
#define වසන්න_ගොනුව close
#define සොයන්න_ගොනුව lseek
#define 파일서술자복제 dup
#define 파일서술자지정복제 dup2
#define ඉවත්_කරන්න_ගොනුව_පිවිසුම_නම unlink
#define කට්ටලය_ගොනුව_දිග ftruncate
#define 파일저장확정 fsync
#define 파일상태읽기 fstat
#define 파일서술자제어 fcntl
#define කියවීම්_පමණි_අගය O_RDONLY
#define 쓰기전용 O_WRONLY
#define කියවීම්_ලිවීම් O_RDWR
#define 없으면만들기 O_CREAT
#define 새파일만들기 (O_CREAT | O_EXCL)
#define 내용비우기 O_TRUNC
#define 끝에이어쓰기 O_APPEND
#define 기다리지않기 O_NONBLOCK
#define 처음기준 SEEK_SET
#define 현재기준 SEEK_CUR
#define 끝기준 SEEK_END
#define ගොනුව_තත්වය stat
typedef size_t 바이트수형;
typedef ssize_t 입출력결과형;
typedef off_t ගොනුව_ඕෆ්සෙට්_ටයිප්_කරන්න;
#endif
