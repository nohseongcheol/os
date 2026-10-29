#ifndef JKOROS_KOREAN_FILE_H
#define JKOROS_KOREAN_FILE_H
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#define उगडचें_फायल open
#define निर्माण_करचें_फायल creat
#define 파일자료읽기 read
#define बरोवचें_फायल_डेटा write
#define शेवट_फायल close
#define सोद_फायल lseek
#define 파일서술자복제 dup
#define 파일서술자지정복제 dup2
#define काडचें_फायल_प्रवेश_नांव unlink
#define संच_फायल_लांबाय ftruncate
#define 파일저장확정 fsync
#define 파일상태읽기 fstat
#define 파일서술자제어 fcntl
#define फकत_वाचचें_मोल O_RDONLY
#define 쓰기전용 O_WRONLY
#define वाचन_बरप O_RDWR
#define 없으면만들기 O_CREAT
#define 새파일만들기 (O_CREAT | O_EXCL)
#define 내용비우기 O_TRUNC
#define 끝에이어쓰기 O_APPEND
#define 기다리지않기 O_NONBLOCK
#define 처음기준 SEEK_SET
#define 현재기준 SEEK_CUR
#define 끝기준 SEEK_END
#define फायल_स्थिती stat
typedef size_t बायट_COUNT_TYPE;
typedef ssize_t 입출력결과형;
typedef off_t फायल_ऑफसॅट_TYPE;
#endif
