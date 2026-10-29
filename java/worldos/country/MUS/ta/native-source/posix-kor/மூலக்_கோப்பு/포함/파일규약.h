#ifndef JKOROS_KOREAN_FILE_H
#define JKOROS_KOREAN_FILE_H
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#define திற_கோப்பு open
#define உருவாக்கு_கோப்பு creat
#define 파일자료읽기 read
#define எழுது_கோப்பு_தரவு write
#define மூடு_கோப்பு close
#define தேடு_கோப்பு lseek
#define 파일서술자복제 dup
#define 파일서술자지정복제 dup2
#define அகற்று_கோப்பு_உள்ளீடு_பெயர் unlink
#define அமை_கோப்பு_நீளம் ftruncate
#define 파일저장확정 fsync
#define 파일상태읽기 fstat
#define 파일서술자제어 fcntl
#define படிக்க_மட்டும்_மதிப்பு O_RDONLY
#define எழுதுதல்_மட்டும்_மதிப்பு O_WRONLY
#define படிக்க_எழுத O_RDWR
#define 없으면만들기 O_CREAT
#define 새파일만들기 (O_CREAT | O_EXCL)
#define 내용비우기 O_TRUNC
#define 끝에이어쓰기 O_APPEND
#define 기다리지않기 O_NONBLOCK
#define 처음기준 SEEK_SET
#define 현재기준 SEEK_CUR
#define 끝기준 SEEK_END
#define கோப்பு_நிலை stat
typedef size_t 바이트수형;
typedef ssize_t 입출력결과형;
typedef off_t கோப்பு_ஆஃப்செட்_வகை;
#endif
