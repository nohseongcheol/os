#ifndef JKOROS_KOREAN_FILE_H
#define JKOROS_KOREAN_FILE_H
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#define avata_Tiedosto open
#define Luo_Tiedosto creat
#define lukea_Tiedosto_data read
#define kirjoitus_Tiedosto_data write
#define Sulje_Tiedosto close
#define hae_Tiedosto lseek
#define 파일서술자복제 dup
#define 파일서술자지정복제 dup2
#define poistaa_Tiedosto_merkintä_nimi unlink
#define ryhmä_Tiedosto_kesto ftruncate
#define vahvistaa_muutokset_Files fsync
#define lukea_Tiedosto_tila fstat
#define 파일서술자제어 fcntl
#define vain_luku_ARVO O_RDONLY
#define 쓰기전용 O_WRONLY
#define luku_ja_kirjoitus O_RDWR
#define 없으면만들기 O_CREAT
#define 새파일만들기 (O_CREAT | O_EXCL)
#define 내용비우기 O_TRUNC
#define 끝에이어쓰기 O_APPEND
#define 기다리지않기 O_NONBLOCK
#define 처음기준 SEEK_SET
#define nykyinen_juuri SEEK_CUR
#define lopettaa_puhelu_origo SEEK_END
#define tiedoston_tila stat
typedef size_t tavu_LASKE_TYYPPI;
typedef ssize_t 입출력결과형;
typedef off_t Tiedosto_SIIRTYMÄ_TYYPPI;
#endif
