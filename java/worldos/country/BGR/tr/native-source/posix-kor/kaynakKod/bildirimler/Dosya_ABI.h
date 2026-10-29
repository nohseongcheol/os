#ifndef JKOROS_KOREAN_FILE_H
#define JKOROS_KOREAN_FILE_H
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#define açık_Dosya open
#define açmak_Dosya creat
#define 파일자료읽기 read
#define yazma_Dosya_veri write
#define Kapat_Dosya close
#define arama_Dosya lseek
#define kopya_Dosya_tanımlayıcı dup
#define 파일서술자지정복제 dup2
#define kaldırmak_Dosya_girdi_ad unlink
#define küme_Dosya_süre ftruncate
#define commit_Dosyalar fsync
#define 파일상태읽기 fstat
#define denetim_Dosya_tanımlayıcı fcntl
#define salt_okunur_değer O_RDONLY
#define sadece_yazılabilir_değer O_WRONLY
#define R_W O_RDWR
#define 없으면만들기 O_CREAT
#define 새파일만들기 (O_CREAT | O_EXCL)
#define kesmek_içindekiler O_TRUNC
#define 끝에이어쓰기 O_APPEND
#define 기다리지않기 O_NONBLOCK
#define 처음기준 SEEK_SET
#define geçerli_kök SEEK_CUR
#define Bitiş_origin SEEK_END
#define dosya_durumu stat
typedef size_t bayt_BAĞ_DEĞ_SAY_TÜR;
typedef ssize_t 입출력결과형;
typedef off_t Dosya_Ofset_TÜR;
#endif
