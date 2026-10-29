#ifndef JKOROS_KOREAN_FILE_H
#define JKOROS_KOREAN_FILE_H
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#define जारी_फ़ाइल open
#define बनाएँ_फ़ाइल creat
#define पढें_फ़ाइल_डेटा read
#define लिखना_फ़ाइल_डेटा write
#define बंद_फ़ाइल close
#define खोजें_फ़ाइल lseek
#define 파일서술자복제 dup
#define 파일서술자지정복제 dup2
#define निकालें_फ़ाइल_एन्ट्री_नाम unlink
#define 파일길이정하기 ftruncate
#define कमिट_फ़ाइल_संग्रहण fsync
#define पढें_फ़ाइल_स्थिति fstat
#define 파일서술자제어 fcntl
#define केवल_पढ़ने_के_लिए_मान O_RDONLY
#define सिर्फ_लिखे_मान O_WRONLY
#define पठन_लेखन O_RDWR
#define 없으면만들기 O_CREAT
#define 새파일만들기 (O_CREAT | O_EXCL)
#define कम_करें_सामग्री O_TRUNC
#define 끝에이어쓰기 O_APPEND
#define 기다리지않기 O_NONBLOCK
#define 처음기준 SEEK_SET
#define अद्यतित_मूल SEEK_CUR
#define 끝기준 SEEK_END
#define फ़ाइल_स्थिति stat
typedef size_t 바이트수형;
typedef ssize_t 입출력결과형;
typedef off_t फ़ाइल_ऑफ़सेट_लिखें;
#endif
