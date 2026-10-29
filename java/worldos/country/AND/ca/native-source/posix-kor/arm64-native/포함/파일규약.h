#ifndef JKOROS_ARM64_NATIVE_FILE_H
#define JKOROS_ARM64_NATIVE_FILE_H
#include <stddef.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
// 독립된 bare-metal ABI. Linux/i386의 헤더나 libc와 혼합하지 않는다.
typedef intptr_t 입출력결과형;
typedef size_t byte_COMPT_TIPUS;
typedef int64_t arxiu_DESPLAÇAMENT_TIPUS;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
arxiu_DESPLAÇAMENT_TIPUS pk_lseek(int fd, arxiu_DESPLAÇAMENT_TIPUS offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, arxiu_DESPLAÇAMENT_TIPUS size);
int pk_fsync(int fd);
int pk_size(int fd);
int crear_arxiu(const char *Camí, int 방식, ...);
입출력결과형 tancar_arxiu_dades(int Fitxer, void *dades, size_t element_COMPT);
입출력결과형 escriure_arxiu_dades(int Fitxer, const void *dades, size_t element_COMPT);
int Tanca_arxiu(int Fitxer);
arxiu_DESPLAÇAMENT_TIPUS cercar_arxiu(int Fitxer, arxiu_DESPLAÇAMENT_TIPUS 거리, int Project_rel);
int suprimir_arxiu_introducció_nom(const char *Camí);
int conjunt_arxiu_durada(int Fitxer, arxiu_DESPLAÇAMENT_TIPUS Mida);
int 파일저장확정(int Fitxer);
int arxiu_canviar_la_mida(int Fitxer);
#ifdef __cplusplus
}
#endif
#define número_d_error (*pk_errno_location())
#define només_de_lectura_VALOR 0
#define 쓰기전용 1
#define lectura_escriptura 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define 내용비우기 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define 현재기준 1
#define 끝기준 2
#endif
