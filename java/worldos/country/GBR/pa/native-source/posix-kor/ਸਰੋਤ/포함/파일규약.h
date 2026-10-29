#ifndef JKOROS_KOREAN_FILE_H
#define JKOROS_KOREAN_FILE_H
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#define ਖੋਲੋ_ਲਿਖਤ_ਪੱਤਰ open
#define ਬਣਾਓ_ਲਿਖਤ_ਪੱਤਰ creat
#define 파일자료읽기 read
#define ਲਿੱਖੋ_ਲਿਖਤ_ਪੱਤਰ_ਸਮੱਗਰੀ write
#define ਬੰਦ_ਕਰੋ_ਲਿਖਤ_ਪੱਤਰ close
#define ਸੀਕ_ਲਿਖਤ_ਪੱਤਰ lseek
#define 파일서술자복제 dup
#define 파일서술자지정복제 dup2
#define ਹਟਾਉਣਾ_ਲਿਖਤ_ਪੱਤਰ_ਦਾਖਲਾ_ਨਾਮ unlink
#define ਸੈਟ_ਲਿਖਤ_ਪੱਤਰ_ਲੰਬਾਈ ftruncate
#define 파일저장확정 fsync
#define 파일상태읽기 fstat
#define 파일서술자제어 fcntl
#define ਸਿਰਫ਼_ਪੜ੍ਹੋ_ਕੀਮਤ O_RDONLY
#define 쓰기전용 O_WRONLY
#define ਪੜ੍ਹਨ_ਲਿਖਣ O_RDWR
#define 없으면만들기 O_CREAT
#define 새파일만들기 (O_CREAT | O_EXCL)
#define 내용비우기 O_TRUNC
#define 끝에이어쓰기 O_APPEND
#define 기다리지않기 O_NONBLOCK
#define 처음기준 SEEK_SET
#define 현재기준 SEEK_CUR
#define 끝기준 SEEK_END
#define ਲਿਖਤ_ਪੱਤਰ_ਸਥਿਤੀ stat
typedef size_t 바이트수형;
typedef ssize_t 입출력결과형;
typedef off_t ਲਿਖਤ_ਪੱਤਰ_ਔਫਸੈਟ_ਟਾਈਪ_ਕਰੋ;
#endif
