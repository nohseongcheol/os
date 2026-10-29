#ifndef JKOROS_KOREAN_FILE_H
#define JKOROS_KOREAN_FILE_H
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#define otwarty_Plik open
#define Twórca_Plik creat
#define 파일자료읽기 read
#define zapis_Plik_dane write
#define Zamknij_Plik close
#define szukać_Plik lseek
#define Duplikuj_Plik_deskryptor dup
#define 파일서술자지정복제 dup2
#define usuń_Plik_wpis_nazwa unlink
#define set_Plik_długość ftruncate
#define przekazywać_Files fsync
#define 파일상태읽기 fstat
#define kontrola_Plik_deskryptor fcntl
#define tylko_do_odczytu_WARTOŚĆ O_RDONLY
#define tylko_do_zapisu_WARTOŚĆ O_WRONLY
#define R_W O_RDWR
#define 없으면만들기 O_CREAT
#define 새파일만들기 (O_CREAT | O_EXCL)
#define obcinać_Spis_treści O_TRUNC
#define 끝에이어쓰기 O_APPEND
#define 기다리지않기 O_NONBLOCK
#define 처음기준 SEEK_SET
#define bieżący_korzeń SEEK_CUR
#define Koniec_źródło SEEK_END
#define stan_pliku stat
typedef size_t bajt_ILE_LICZB_TYP;
typedef ssize_t 입출력결과형;
typedef off_t Plik_przesunąć_TYP;
#endif
