#ifndef JKOROS_ARM64_NATIVE_FILE_H
#define JKOROS_ARM64_NATIVE_FILE_H
#include <stddef.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
// 독립된 bare-metal ABI. Linux/i386의 헤더나 libc와 혼합하지 않는다.
typedef intptr_t 입출력결과형;
typedef size_t byte_AANTAL_TYPE;
typedef int64_t Bestand_VERSCHUIVING_TYPE;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
Bestand_VERSCHUIVING_TYPE pk_lseek(int fd, Bestand_VERSCHUIVING_TYPE offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, Bestand_VERSCHUIVING_TYPE size);
int pk_fsync(int fd);
int pk_size(int fd);
int open_Bestand(const char *pad, int methode_MODUS, ...);
입출력결과형 파일자료읽기(int bestand, void *gegevens, size_t item_AANTAL);
입출력결과형 schrijven_Bestand_gegevens(int bestand, const void *gegevens, size_t item_AANTAL);
int Sluiten_Bestand(int bestand);
Bestand_VERSCHUIVING_TYPE zoeken_Bestand(int bestand, Bestand_VERSCHUIVING_TYPE 거리, int Taken_wortel);
int verwijderen_Bestand_invoer_naam(const char *pad);
int set_Bestand_tijdsduur(int bestand, Bestand_VERSCHUIVING_TYPE Grootte);
int doorvoeren_Files(int bestand);
int bestandsgrootte(int bestand);
#ifdef __cplusplus
}
#endif
#define foutnummer (*pk_errno_location())
#define alleen_lezen_WAARDE 0
#define 쓰기전용 1
#define lezen_schrijven 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define afkappen_Inhoud 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define actueel_wortel 1
#define beëindigen_oorsprong 2
#endif
