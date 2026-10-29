#ifndef JKOROS_KOREAN_FILE_H
#define JKOROS_KOREAN_FILE_H
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#define odprto_Datoteka open
#define Ustvari_Datoteka creat
#define 파일자료읽기 read
#define pisati_Datoteka_podatki write
#define Zapri_Datoteka close
#define iskati_Datoteka lseek
#define 파일서술자복제 dup
#define 파일서술자지정복제 dup2
#define odstraniti_Datoteka_vnos_ime unlink
#define 파일길이정하기 ftruncate
#define potrjevanje_datotečna_shramba fsync
#define 파일상태읽기 fstat
#define 파일서술자제어 fcntl
#define samo_za_branje_VALUE O_RDONLY
#define 쓰기전용 O_WRONLY
#define branje_pisanje O_RDWR
#define 없으면만들기 O_CREAT
#define 새파일만들기 (O_CREAT | O_EXCL)
#define 내용비우기 O_TRUNC
#define 끝에이어쓰기 O_APPEND
#define 기다리지않기 O_NONBLOCK
#define 처음기준 SEEK_SET
#define sprotno_koren SEEK_CUR
#define 끝기준 SEEK_END
#define Datoteka_stanje stat
typedef size_t bajt_COUNT_Tip;
typedef ssize_t 입출력결과형;
typedef off_t Datoteka_odmik_Tip;
#endif
