#ifndef JKOROS_ARM64_NATIVE_FILE_H
#define JKOROS_ARM64_NATIVE_FILE_H
#include <stddef.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
// 독립된 bare-metal ABI. Linux/i386의 헤더나 libc와 혼합하지 않는다.
typedef intptr_t 입출력결과형;
typedef size_t bayt_BAĞ_DEĞ_SAY_TÜR;
typedef int64_t Dosya_Ofset_TÜR;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
Dosya_Ofset_TÜR pk_lseek(int fd, Dosya_Ofset_TÜR offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, Dosya_Ofset_TÜR size);
int pk_fsync(int fd);
int pk_size(int fd);
int açık_Dosya(const char *yol, int metot_mod, ...);
입출력결과형 파일자료읽기(int dosya, void *veri, size_t öğe_BAĞ_DEĞ_SAY);
입출력결과형 yazma_Dosya_veri(int dosya, const void *veri, size_t öğe_BAĞ_DEĞ_SAY);
int Kapat_Dosya(int dosya);
Dosya_Ofset_TÜR arama_Dosya(int dosya, Dosya_Ofset_TÜR 거리, int işlem_kök);
int kaldırmak_Dosya_girdi_ad(const char *yol);
int küme_Dosya_süre(int dosya, Dosya_Ofset_TÜR Boyut);
int commit_Dosyalar(int dosya);
int dosya_boyutu(int dosya);
#ifdef __cplusplus
}
#endif
#define hata_numarası (*pk_errno_location())
#define salt_okunur_değer 0
#define sadece_yazılabilir_değer 1
#define R_W 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define kesmek_içindekiler 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define geçerli_kök 1
#define Bitiş_origin 2
#endif
