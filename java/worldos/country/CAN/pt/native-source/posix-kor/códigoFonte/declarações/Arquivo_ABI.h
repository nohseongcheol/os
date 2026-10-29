#ifndef JKOROS_KOREAN_FILE_H
#define JKOROS_KOREAN_FILE_H
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#define abrir_Arquivo open
#define Criar_Arquivo creat
#define leitura_Arquivo_dados read
#define gravar_Arquivo_dados write
#define Close_Arquivo close
#define busca_Arquivo lseek
#define Duplicar_Arquivo_descritor dup
#define 파일서술자지정복제 dup2
#define remover_Arquivo_entrada_nome unlink
#define set_Arquivo_duração ftruncate
#define commit_Arquivos fsync
#define leitura_Arquivo_Status fstat
#define visual_Arquivo_descritor fcntl
#define somente_leitura_VALOR O_RDONLY
#define somente_gravação_VALOR O_WRONLY
#define de_leitura_gravação O_RDWR
#define 없으면만들기 O_CREAT
#define 새파일만들기 (O_CREAT | O_EXCL)
#define cortar_Sumário O_TRUNC
#define 끝에이어쓰기 O_APPEND
#define 기다리지않기 O_NONBLOCK
#define 처음기준 SEEK_SET
#define em_dia_raiz SEEK_CUR
#define encerrar_origem SEEK_END
#define estado_de_ficheiro stat
typedef size_t byte_CONT_NÚM_TIPO;
typedef ssize_t 입출력결과형;
typedef off_t Arquivo_DESLOC_TIPO;
#endif
