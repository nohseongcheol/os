#ifndef JKOROS_ARM64_NATIVE_FILE_H
#define JKOROS_ARM64_NATIVE_FILE_H
#include <stddef.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
// 독립된 bare-metal ABI. Linux/i386의 헤더나 libc와 혼합하지 않는다.
typedef intptr_t 입출력결과형;
typedef size_t tavu_LASKE_TYYPPI;
typedef int64_t Tiedosto_SIIRTYMÄ_TYYPPI;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
Tiedosto_SIIRTYMÄ_TYYPPI pk_lseek(int fd, Tiedosto_SIIRTYMÄ_TYYPPI offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, Tiedosto_SIIRTYMÄ_TYYPPI size);
int pk_fsync(int fd);
int pk_size(int fd);
int avata_Tiedosto(const char *polku_2, int menetelmä_tila, ...);
입출력결과형 lukea_Tiedosto_data(int tiedoston_nimi, void *data, size_t kohde_LASKE);
입출력결과형 kirjoitus_Tiedosto_data(int tiedoston_nimi, const void *data, size_t kohde_LASKE);
int Sulje_Tiedosto(int tiedoston_nimi);
Tiedosto_SIIRTYMÄ_TYYPPI hae_Tiedosto(int tiedoston_nimi, Tiedosto_SIIRTYMÄ_TYYPPI 거리, int aloite_juuri);
int poistaa_Tiedosto_merkintä_nimi(const char *polku_2);
int ryhmä_Tiedosto_kesto(int tiedoston_nimi, Tiedosto_SIIRTYMÄ_TYYPPI Koko);
int vahvistaa_muutokset_Files(int tiedoston_nimi);
int tiedostokoko(int tiedoston_nimi);
#ifdef __cplusplus
}
#endif
#define virhenumero (*pk_errno_location())
#define vain_luku_ARVO 0
#define 쓰기전용 1
#define luku_ja_kirjoitus 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define 내용비우기 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define nykyinen_juuri 1
#define lopettaa_puhelu_origo 2
#endif
