#ifndef JKOROS_KOREAN_FILE_H
#define JKOROS_KOREAN_FILE_H
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#define відкрито_Файл open
#define Створення_Файл creat
#define 파일자료읽기 read
#define записування_Файл_дані write
#define Закрити_Файл close
#define шукати_Файл lseek
#define 파일서술자복제 dup
#define 파일서술자지정복제 dup2
#define вилучати_Файл_запис_ім_я unlink
#define 파일길이정하기 ftruncate
#define затвердження_файлове_сховище fsync
#define 파일상태읽기 fstat
#define 파일서술자제어 fcntl
#define лише_для_читання_значення O_RDONLY
#define 쓰기전용 O_WRONLY
#define 읽고쓰기 O_RDWR
#define 없으면만들기 O_CREAT
#define 새파일만들기 (O_CREAT | O_EXCL)
#define скорочувати_Зміст O_TRUNC
#define 끝에이어쓰기 O_APPEND
#define 기다리지않기 O_NONBLOCK
#define 처음기준 SEEK_SET
#define чинний_корінь SEEK_CUR
#define 끝기준 SEEK_END
#define стан_файла stat
typedef size_t 바이트수형;
typedef ssize_t 입출력결과형;
typedef off_t Файл_Зміщена_копія_Тип;
#endif
