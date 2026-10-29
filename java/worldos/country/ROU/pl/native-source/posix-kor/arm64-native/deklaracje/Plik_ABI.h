#ifndef JKOROS_ARM64_NATIVE_FILE_H
#define JKOROS_ARM64_NATIVE_FILE_H
#include <stddef.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
// 독립된 bare-metal ABI. Linux/i386의 헤더나 libc와 혼합하지 않는다.
typedef intptr_t 입출력결과형;
typedef size_t bajt_ILE_LICZB_TYP;
typedef int64_t Plik_przesunąć_TYP;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
입출력결과형 pk_read(int fd, void *buffer, size_t count);
입출력결과형 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
Plik_przesunąć_TYP pk_lseek(int fd, Plik_przesunąć_TYP offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, Plik_przesunąć_TYP size);
int pk_fsync(int fd);
int pk_size(int fd);
int otwarty_Plik(const char *ścieżka_2, int metoda_tryb, ...);
입출력결과형 파일자료읽기(int nazwa_pliku, void *dane, size_t towar_ILE_LICZB);
입출력결과형 zapis_Plik_dane(int nazwa_pliku, const void *dane, size_t towar_ILE_LICZB);
int Zamknij_Plik(int nazwa_pliku);
Plik_przesunąć_TYP szukać_Plik(int nazwa_pliku, Plik_przesunąć_TYP 거리, int Project_korzeń);
int usuń_Plik_wpis_nazwa(const char *ścieżka_2);
int set_Plik_długość(int nazwa_pliku, Plik_przesunąć_TYP Rozmiar);
int przekazywać_Files(int nazwa_pliku);
int rozmiar_pliku(int nazwa_pliku);
#ifdef __cplusplus
}
#endif
#define numer_błędu (*pk_errno_location())
#define tylko_do_odczytu_WARTOŚĆ 0
#define tylko_do_zapisu_WARTOŚĆ 1
#define R_W 2
#define 없으면만들기 0x40
#define 새파일만들기 0xc0
#define obcinać_Spis_treści 0x200
#define 끝에이어쓰기 0x400
#define 처음기준 0
#define bieżący_korzeń 1
#define Koniec_źródło 2
#endif
