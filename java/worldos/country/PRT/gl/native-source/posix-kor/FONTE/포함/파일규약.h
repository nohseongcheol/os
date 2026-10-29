#ifndef JKOROS_KOREAN_FILE_H
#define JKOROS_KOREAN_FILE_H
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#define abrir_Ficheiro open
#define crear_Ficheiro creat
#define 파일자료읽기 read
#define escribir_Ficheiro_datos write
#define peche_Ficheiro close
#define buscar_Ficheiro lseek
#define 파일서술자복제 dup
#define 파일서술자지정복제 dup2
#define eliminar_Ficheiro_introdución_nome unlink
#define conxunto_Ficheiro_duración ftruncate
#define 파일저장확정 fsync
#define 파일상태읽기 fstat
#define 파일서술자제어 fcntl
#define só_de_lectura_VALOR O_RDONLY
#define 쓰기전용 O_WRONLY
#define de_lectura_e_escrita O_RDWR
#define 없으면만들기 O_CREAT
#define 새파일만들기 (O_CREAT | O_EXCL)
#define 내용비우기 O_TRUNC
#define 끝에이어쓰기 O_APPEND
#define 기다리지않기 O_NONBLOCK
#define 처음기준 SEEK_SET
#define ao_corrente_raíz SEEK_CUR
#define 끝기준 SEEK_END
#define Ficheiro_estado stat
typedef size_t byte_CONTAR_TIPO;
typedef ssize_t 입출력결과형;
typedef off_t Ficheiro_DESPRAZAMENTO_TIPO;
#endif
