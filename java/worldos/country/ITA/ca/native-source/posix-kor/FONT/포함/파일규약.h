#ifndef JKOROS_KOREAN_FILE_H
#define JKOROS_KOREAN_FILE_H
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#define crear_arxiu open
#define Crear_arxiu creat
#define tancar_arxiu_dades read
#define escriure_arxiu_dades write
#define Tanca_arxiu close
#define cercar_arxiu lseek
#define 파일서술자복제 dup
#define 파일서술자지정복제 dup2
#define suprimir_arxiu_introducció_nom unlink
#define conjunt_arxiu_durada ftruncate
#define 파일저장확정 fsync
#define tancar_arxiu_estat fstat
#define 파일서술자제어 fcntl
#define només_de_lectura_VALOR O_RDONLY
#define 쓰기전용 O_WRONLY
#define lectura_escriptura O_RDWR
#define 없으면만들기 O_CREAT
#define 새파일만들기 (O_CREAT | O_EXCL)
#define 내용비우기 O_TRUNC
#define 끝에이어쓰기 O_APPEND
#define 기다리지않기 O_NONBLOCK
#define 처음기준 SEEK_SET
#define 현재기준 SEEK_CUR
#define 끝기준 SEEK_END
#define arxiu_estat stat
typedef size_t byte_COMPT_TIPUS;
typedef ssize_t 입출력결과형;
typedef off_t arxiu_DESPLAÇAMENT_TIPUS;
#endif
