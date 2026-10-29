#ifndef JKOROS_ARM64_NATIVE_FILE_H
#define JKOROS_ARM64_NATIVE_FILE_H
#include <stddef.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
// 독립된 bare-metal ABI. Linux/i386의 헤더나 libc와 혼합하지 않는다.
typedef intptr_t 입출력결과형;
typedef size_t byte_ANTALL_Type;
typedef int64_t Fil_FORSKYVNING_Type;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
Fil_FORSKYVNING_Type pk_lseek(int fd, Fil_FORSKYVNING_Type offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, Fil_FORSKYVNING_Type size);
int pk_fsync(int fd);
int pk_size(int fd);
int åpen_Fil(const char *Sti, int metode_MODUS, ...);
입출력결과형 파일자료읽기(int Fil, void *data, size_t vare_ANTALL);
입출력결과형 skrive_Fil_data(int Fil, const void *data, size_t vare_ANTALL);
int Lukk_Fil(int Fil);
Fil_FORSKYVNING_Type søk_Fil(int Fil, Fil_FORSKYVNING_Type 거리, int speile_rot);
int fjerne_Fil_oppføring_navn(const char *Sti);
int sett_Fil_lengde(int Fil, Fil_FORSKYVNING_Type Størrelse);
int 파일저장확정(int Fil);
int filstørrelse(int Fil);
#ifdef __cplusplus
}
#endif
#define feilnummer (*pk_errno_location())
#define skrivebeskyttet_VERDI 0
#define 쓰기전용 1
#define lese_og_skrive 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define avkorte_Innhold 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define betalt_rot 1
#define avslutte_en_samtale_origo 2
#endif
