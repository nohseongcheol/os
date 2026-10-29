#ifndef JKOROS_KOREAN_FILE_H
#define JKOROS_KOREAN_FILE_H
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#define otevřít_Soubor open
#define Create_Soubor creat
#define 파일자료읽기 read
#define zápis_Soubor_data write
#define Zavřít_Soubor close
#define hledat_Soubor lseek
#define duplikát_Soubor_popisovač dup
#define 파일서술자지정복제 dup2
#define odebrat_Soubor_položka_název unlink
#define sada_Soubor_délka ftruncate
#define zápis_Files fsync
#define 파일상태읽기 fstat
#define řízení_Soubor_popisovač fcntl
#define jen_pro_čtení_HODNOTA O_RDONLY
#define 쓰기전용 O_WRONLY
#define pro_čtení_i_zápis O_RDWR
#define 없으면만들기 O_CREAT
#define 새파일만들기 (O_CREAT | O_EXCL)
#define stříhat_Obsah O_TRUNC
#define 끝에이어쓰기 O_APPEND
#define 기다리지않기 O_NONBLOCK
#define 처음기준 SEEK_SET
#define dobrá_kořen SEEK_CUR
#define konec_origin SEEK_END
#define stav_souboru stat
typedef size_t bajt_POČET_TYP;
typedef ssize_t 입출력결과형;
typedef off_t Soubor_POSUN_TYP;
#endif
