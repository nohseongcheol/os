#ifndef JKOROS_KOREAN_FILE_H
#define JKOROS_KOREAN_FILE_H
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#define aperto_File open
#define Crea_File creat
#define 파일자료읽기 read
#define scrivere_File_dati write
#define Chiudi_File close
#define cercare_File lseek
#define Duplica_File_descrittore dup
#define 파일서술자지정복제 dup2
#define rimuovere_File_voce_nome unlink
#define set_File_durata ftruncate
#define commit_File fsync
#define 파일상태읽기 fstat
#define controllo_File_descrittore fcntl
#define di_sola_lettura_VALORE O_RDONLY
#define sola_scrittura_VALORE O_WRONLY
#define in_lettura_scrittura O_RDWR
#define 없으면만들기 O_CREAT
#define 새파일만들기 (O_CREAT | O_EXCL)
#define tagliare_Sommario O_TRUNC
#define 끝에이어쓰기 O_APPEND
#define 기다리지않기 O_NONBLOCK
#define 처음기준 SEEK_SET
#define Regolari_radice SEEK_CUR
#define chiudere_origine SEEK_END
#define stato_file stat
typedef size_t byte_CONTA_NUMERI_TIPO;
typedef ssize_t 입출력결과형;
typedef off_t File_SCARTO_TIPO;
#endif
