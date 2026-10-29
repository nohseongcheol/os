#ifndef JKOROS_KOREAN_FILE_H
#define JKOROS_KOREAN_FILE_H
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#define открыть_файл open
#define Create_файл creat
#define чтение_файл_данные read
#define запись_файл_данные write
#define Close_файл close
#define поиск_файл lseek
#define дубликат_файл_дескриптор dup
#define 파일서술자지정복제 dup2
#define удалить_файл_ввод_имя unlink
#define сет_файл_длина ftruncate
#define фиксация_Файлы fsync
#define чтение_файл_статус fstat
#define управление_файл_дескриптор fcntl
#define нередактируемый_ЗНАЧЕН O_RDONLY
#define доступный_только_на_запись_ЗНАЧЕН O_WRONLY
#define для_чтения_и_записи O_RDWR
#define 없으면만들기 O_CREAT
#define 새파일만들기 (O_CREAT | O_EXCL)
#define усечь_Оглавление O_TRUNC
#define 끝에이어쓰기 O_APPEND
#define 기다리지않기 O_NONBLOCK
#define 처음기준 SEEK_SET
#define текущий_корень SEEK_CUR
#define элемент_origin SEEK_END
#define состояние_файла stat
typedef size_t байт_СЧЁТ_ТИП;
typedef ssize_t 입출력결과형;
typedef off_t файл_СМЕЩ_ТИП;
#endif
