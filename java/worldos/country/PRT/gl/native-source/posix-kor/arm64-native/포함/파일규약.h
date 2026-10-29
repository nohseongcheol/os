#ifndef JKOROS_ARM64_NATIVE_FILE_H
#define JKOROS_ARM64_NATIVE_FILE_H
#include <stddef.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
// 독립된 bare-metal ABI. Linux/i386의 헤더나 libc와 혼합하지 않는다.
typedef intptr_t 입출력결과형;
typedef size_t byte_CONTAR_TIPO;
typedef int64_t Ficheiro_DESPRAZAMENTO_TIPO;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
Ficheiro_DESPRAZAMENTO_TIPO pk_lseek(int fd, Ficheiro_DESPRAZAMENTO_TIPO offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, Ficheiro_DESPRAZAMENTO_TIPO size);
int pk_fsync(int fd);
int pk_size(int fd);
int abrir_Ficheiro(const char *CAMIÑO, int 방식, ...);
입출력결과형 파일자료읽기(int Ficheiro, void *datos, size_t elemento_CONTAR);
입출력결과형 escribir_Ficheiro_datos(int Ficheiro, const void *datos, size_t elemento_CONTAR);
int peche_Ficheiro(int Ficheiro);
Ficheiro_DESPRAZAMENTO_TIPO buscar_Ficheiro(int Ficheiro, Ficheiro_DESPRAZAMENTO_TIPO 거리, int Project_raíz);
int eliminar_Ficheiro_introdución_nome(const char *CAMIÑO);
int conxunto_Ficheiro_duración(int Ficheiro, Ficheiro_DESPRAZAMENTO_TIPO Tamaño);
int 파일저장확정(int Ficheiro);
int 파일크기(int Ficheiro);
#ifdef __cplusplus
}
#endif
#define número_de_erro (*pk_errno_location())
#define só_de_lectura_VALOR 0
#define 쓰기전용 1
#define de_lectura_e_escrita 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define 내용비우기 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define ao_corrente_raíz 1
#define 끝기준 2
#endif
