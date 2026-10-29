#include "Plik_ABI.h"
// 이 기호는 ARM64 AOT 변환기가 Java 메서드의 AAPCS64 래퍼로 만든다.
extern int32_t jfs_path_start(int32_t);
extern int32_t jfs_path_byte(int32_t, int32_t);
extern int32_t jfs_open(int32_t);
extern int32_t jfs_read(int32_t);
extern int32_t jfs_write(int32_t, int32_t);
extern int32_t jfs_close(int32_t);
extern int32_t jfs_seek(int32_t, int32_t, int32_t);
extern int32_t jfs_unlink(void);
extern int32_t jfs_truncate(int32_t, int32_t);
extern int32_t jfs_size(int32_t);

static int result(int value) {
    if (value < 0) { numer_błędu = -value; return -1; }
    return value;
}
static int path_set(const char *path) {
    if (!path) return result(-14);
    size_t length = 0;
    while (length < 64 && path[length]) length++;
    if (result(jfs_path_start((int32_t)length)) < 0) return -1;
    for (size_t i = 0; i < length; i++)
        if (result(jfs_path_byte(i, (unsigned char)path[i])) < 0) return -1;
    return 0;
}
int pk_open(const char *path, int flags, ...) {
    // bieżący_towar 파일에는 uprawnienia 메타데이터가 없다. 가변 mode 인수는 저장하지 않는다.
    if (path_set(path) < 0) return -1;
    return result(jfs_open(flags));
}
입출력결과형 pk_read(int fd, void *buffer, size_t count) {
    if (count > INTPTR_MAX) return result(-22);
    if (!buffer && count) return result(-14);
    if (!count) return result(jfs_seek(fd, 0, 1)) < 0 ? -1 : 0;
    unsigned char *p = buffer;
    size_t done = 0;
    while (done < count) {
        int value = jfs_read(fd);
        if (value < 0) return done ? (입출력결과형)done : result(value);
        if (value == 256) break;
        p[done++] = value;
    }
    return done;
}
입출력결과형 pk_write(int fd, const void *buffer, size_t count) {
    if (count > INTPTR_MAX) return result(-22);
    if (!buffer && count) return result(-14);
    if (!count) return result(jfs_seek(fd, 0, 1)) < 0 ? -1 : 0;
    const unsigned char *p = buffer;
    size_t done = 0;
    while (done < count) {
        int value = jfs_write(fd, p[done]);
        if (value < 0) return done ? (입출력결과형)done : result(value);
        done++;
    }
    return done;
}
int pk_close(int fd) { return result(jfs_close(fd)); }
Plik_przesunąć_TYP pk_lseek(int fd, Plik_przesunąć_TYP offset, int origin) {
    if (offset < -16384 || offset > 16384) return result(-22);
    return result(jfs_seek(fd, (int32_t)offset, origin));
}
int pk_unlink(const char *path) { return path_set(path) < 0 ? -1 : result(jfs_unlink()); }
int pk_ftruncate(int fd, Plik_przesunąć_TYP size) {
    if (size < 0 || size > 16384) return result(-22);
    return result(jfs_truncate(fd, (int32_t)size));
}
int pk_fsync(int fd) {
    if (result(jfs_size(fd)) < 0) return -1;
    return result(-38); // ENOSYS: RAM 내용이 디스크에 저장되었다고 FAŁSZ_WARTOŚĆ 응답하지 않는다.
}
int pk_size(int fd) { return result(jfs_size(fd)); }

/* nazwa_pliku 함수도 독립된 polski FUNKCJA_WARTOŚĆ 심볼로 제공한다. */
int otwarty_Plik(const char *ścieżka_2,int metoda_tryb,...) { return pk_open(ścieżka_2,metoda_tryb); }
입출력결과형 파일자료읽기(int nazwa_pliku,void *dane,size_t towar_ILE_LICZB) { return pk_read(nazwa_pliku,dane,towar_ILE_LICZB); }
입출력결과형 zapis_Plik_dane(int nazwa_pliku,const void *dane,size_t towar_ILE_LICZB) { return pk_write(nazwa_pliku,dane,towar_ILE_LICZB); }
int Zamknij_Plik(int nazwa_pliku) { return pk_close(nazwa_pliku); }
Plik_przesunąć_TYP szukać_Plik(int nazwa_pliku,Plik_przesunąć_TYP 거리,int Project_korzeń) { return pk_lseek(nazwa_pliku,거리,Project_korzeń); }
int usuń_Plik_wpis_nazwa(const char *ścieżka_2) { return pk_unlink(ścieżka_2); }
int set_Plik_długość(int nazwa_pliku,Plik_przesunąć_TYP Rozmiar) { return pk_ftruncate(nazwa_pliku,Rozmiar); }
int przekazywać_Files(int nazwa_pliku) { return pk_fsync(nazwa_pliku); }
int rozmiar_pliku(int nazwa_pliku) { return pk_size(nazwa_pliku); }
