#ifndef JKOROS_ARM64_NATIVE_FILE_H
#define JKOROS_ARM64_NATIVE_FILE_H
#include <stddef.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
// 독립된 bare-metal ABI. Linux/i386의 헤더나 libc와 혼합하지 않는다.
typedef intptr_t 입출력결과형;
typedef size_t byte_ANTAL_Typ;
typedef int64_t fil_FÖRSKJUTNING_Typ;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
fil_FÖRSKJUTNING_Typ pk_lseek(int fd, fil_FÖRSKJUTNING_Typ offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, fil_FÖRSKJUTNING_Typ size);
int pk_fsync(int fd);
int pk_size(int fd);
int skapa_fil(const char *sökväg_2, int metod_läge, ...);
입출력결과형 läsa_fil_data(int filnamn, void *data, size_t objekt_ANTAL);
입출력결과형 skriva_fil_data(int filnamn, const void *data, size_t objekt_ANTAL);
int Stäng_fil(int filnamn);
fil_FÖRSKJUTNING_Typ söka_fil(int filnamn, fil_FÖRSKJUTNING_Typ 거리, int åtgärd_rot);
int ta_bort_fil_post_namn(const char *sökväg_2);
int uppsättning_fil_längd(int filnamn, fil_FÖRSKJUTNING_Typ Storlek);
int incheckning_Files(int filnamn);
int filstorlek(int filnamn);
#ifdef __cplusplus
}
#endif
#define felnummer (*pk_errno_location())
#define skrivskyddad_värde 0
#define 쓰기전용 1
#define läsa_skriva 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define trimma_Innehåll 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define aktuellt_rot 1
#define avsluta_origo 2
#endif
