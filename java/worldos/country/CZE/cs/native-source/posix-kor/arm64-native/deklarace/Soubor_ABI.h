#ifndef JKOROS_ARM64_NATIVE_FILE_H
#define JKOROS_ARM64_NATIVE_FILE_H
#include <stddef.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
// 독립된 bare-metal ABI. Linux/i386의 헤더나 libc와 혼합하지 않는다.
typedef intptr_t 입출력결과형;
typedef size_t bajt_POČET_TYP;
typedef int64_t Soubor_POSUN_TYP;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
Soubor_POSUN_TYP pk_lseek(int fd, Soubor_POSUN_TYP offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, Soubor_POSUN_TYP size);
int pk_fsync(int fd);
int pk_size(int fd);
int otevřít_Soubor(const char *cesta_2, int metoda_MODE, ...);
입출력결과형 파일자료읽기(int název_souboru, void *data, size_t zboží_POČET);
입출력결과형 zápis_Soubor_data(int název_souboru, const void *data, size_t zboží_POČET);
int Zavřít_Soubor(int název_souboru);
Soubor_POSUN_TYP hledat_Soubor(int název_souboru, Soubor_POSUN_TYP 거리, int akce_kořen);
int odebrat_Soubor_položka_název(const char *cesta_2);
int sada_Soubor_délka(int název_souboru, Soubor_POSUN_TYP Velikost);
int zápis_Files(int název_souboru);
int velikost_souboru(int název_souboru);
#ifdef __cplusplus
}
#endif
#define číslo_chyby (*pk_errno_location())
#define jen_pro_čtení_HODNOTA 0
#define 쓰기전용 1
#define pro_čtení_i_zápis 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define stříhat_Obsah 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define dobrá_kořen 1
#define konec_origin 2
#endif
