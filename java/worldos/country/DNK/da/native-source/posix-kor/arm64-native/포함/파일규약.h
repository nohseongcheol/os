#ifndef JKOROS_ARM64_NATIVE_FILE_H
#define JKOROS_ARM64_NATIVE_FILE_H
#include <stddef.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
// 독립된 bare-metal ABI. Linux/i386의 헤더나 libc와 혼합하지 않는다.
typedef intptr_t 입출력결과형;
typedef size_t byte_TÆL_Type;
typedef int64_t fil_FORSKYDNING_Type;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
fil_FORSKYDNING_Type pk_lseek(int fd, fil_FORSKYDNING_Type offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, fil_FORSKYDNING_Type size);
int pk_fsync(int fd);
int pk_size(int fd);
int åben_fil(const char *Sti, int metode_HYPPIGST, ...);
입출력결과형 파일자료읽기(int Fil, void *data, size_t vare_TÆL);
입출력결과형 skrive_fil_data(int Fil, const void *data, size_t vare_TÆL);
int Luk_fil(int Fil);
fil_FORSKYDNING_Type søge_fil(int Fil, fil_FORSKYDNING_Type 거리, int To_do_rod);
int fjerne_fil_post_navn(const char *Sti);
int sæt_fil_varighed(int Fil, fil_FORSKYDNING_Type Størrelse);
int udføre_Files(int Fil);
int filstørrelse(int Fil);
#ifdef __cplusplus
}
#endif
#define fejlnummer (*pk_errno_location())
#define skrivebeskyttet_VÆRDI 0
#define 쓰기전용 1
#define læse_skrive 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define afkorte_Indhold 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define aktuel_rod 1
#define afslutte_et_opkald_begyndelsespunkt 2
#endif
