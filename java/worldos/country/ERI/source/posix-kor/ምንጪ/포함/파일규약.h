#ifndef JKOROS_KOREAN_FILE_H
#define JKOROS_KOREAN_FILE_H
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#define ክፈት_ፋይል open
#define ፍጠር_ፋይል creat
#define 파일자료읽기 read
#define ጸሓፍ_ፋይል_ሓበሬታ write
#define ዕጸው_ፋይል close
#define መድለዪ_ፋይል lseek
#define 파일서술자복제 dup
#define 파일서술자지정복제 dup2
#define ኣልግስ_ፋይል_ምእታው_ሽም unlink
#define እኩብ_ፋይል_ንውሓት ftruncate
#define 파일저장확정 fsync
#define 파일상태읽기 fstat
#define 파일서술자제어 fcntl
#define ንምንባብ_ጥራይ_ዋጋ O_RDONLY
#define 쓰기전용 O_WRONLY
#define ኣንብብ_ጽሓፍ O_RDWR
#define 없으면만들기 O_CREAT
#define 새파일만들기 (O_CREAT | O_EXCL)
#define 내용비우기 O_TRUNC
#define 끝에이어쓰기 O_APPEND
#define 기다리지않기 O_NONBLOCK
#define 처음기준 SEEK_SET
#define 현재기준 SEEK_CUR
#define 끝기준 SEEK_END
#define ፋይል_ደረጃ stat
typedef size_t 바이트수형;
typedef ssize_t 입출력결과형;
typedef off_t ፋይል_ሽፋን_ዓይነት;
#endif
