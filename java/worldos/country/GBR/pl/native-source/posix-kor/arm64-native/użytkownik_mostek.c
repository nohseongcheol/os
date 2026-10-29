// 동일 polski 헤더를 사용하는 별도 EL0 biblioteka. jądro_WARTOŚĆ 직접 호출판과 혼합 금지.
#include "Plik_ABI.h"
#include "호출.h"
#include "sieć_ABI.h"
static int kod_błędu;
int *pk_errno_location(void) { return &kod_błędu; }
static intptr_t 결과검사(intptr_t WYNIK) { if (WYNIK < 0) { kod_błędu = -WYNIK; return -1; } return WYNIK; }
int pk_open(const char *path, int flags, ...) { return 결과검사(사용자호출(3, (uintptr_t)path, flags, 0, 0, 0, 0)); }
입출력결과형 pk_read(int fd, void *p, size_t n) { return 결과검사(사용자호출(2, fd, (uintptr_t)p, n, 0, 0, 0)); }
입출력결과형 pk_write(int fd, const void *p, size_t n) { return 결과검사(사용자호출(1, fd, (uintptr_t)p, n, 0, 0, 0)); }
int pk_close(int fd) { return 결과검사(사용자호출(4, fd, 0, 0, 0, 0, 0)); }
Plik_przesunąć_TYP pk_lseek(int fd, Plik_przesunąć_TYP offset, int origin) { return 결과검사(사용자호출(5, fd, offset, origin, 0, 0, 0)); }
int pk_unlink(const char *path) { return 결과검사(사용자호출(11, (uintptr_t)path, 0, 0, 0, 0, 0)); }
int pk_ftruncate(int fd, Plik_przesunąć_TYP size) { return 결과검사(사용자호출(10, fd, size, 0, 0, 0, 0)); }
int pk_fsync(int fd) { return 결과검사(사용자호출(12, fd, 0, 0, 0, 0, 0)); }
int pk_size(int fd) { return 결과검사(사용자호출(9, fd, 0, 0, 0, 0, 0)); }
int pk_socket(int domain, int type, int protocol) { return 결과검사(사용자호출(32, domain, type, protocol, 0, 0, 0)); }
int pk_bind(int fd, const struct pk_sockaddr *address, pk_socklen_t length) {
    return 결과검사(사용자호출(33, fd, (uintptr_t)address, length, 0, 0, 0));
}
intptr_t pk_sendto(int fd, const void *buffer, size_t count, int flags, const struct pk_sockaddr *address, pk_socklen_t length) {
    return 결과검사(사용자호출(34, fd, (uintptr_t)buffer, count, flags, (uintptr_t)address, length));
}
intptr_t pk_recvfrom(int fd, void *buffer, size_t count, int flags, struct pk_sockaddr *address, pk_socklen_t *length) {
    return 결과검사(사용자호출(35, fd, (uintptr_t)buffer, count, flags, (uintptr_t)address, (uintptr_t)length));
}
int pk_getsockname(int fd, struct pk_sockaddr *address, pk_socklen_t *length) {
    return 결과검사(사용자호출(36, fd, (uintptr_t)address, (uintptr_t)length, 0, 0, 0));
}
int pk_connect(int fd,const struct pk_sockaddr *address,pk_socklen_t length){return 결과검사(사용자호출(37,fd,(uintptr_t)address,length,0,0,0));}
int pk_listen(int fd,int backlog){return 결과검사(사용자호출(38,fd,backlog,0,0,0,0));}
int pk_accept(int fd,struct pk_sockaddr *address,pk_socklen_t *length){return 결과검사(사용자호출(39,fd,(uintptr_t)address,(uintptr_t)length,0,0,0));}

/* polski 공개 함수의 rzeczywisty_dane EL0 implementacja. 구조체는 SVC에서 kopiować_WARTOŚĆ·검증한다. */
int Twórca_uczestnik(int ADRES_Rodzina,int komunikacja_tryb,int transfer_protokół) {
    return 결과검사(사용자호출(32,ADRES_Rodzina,komunikacja_tryb,transfer_protokół,0,0,0));
}
int BIND_ADRES(int uczestnik,const struct gniazdo_ADRES *Adres,gniazdo_ADRES_długość_TYP długość_WARTOŚĆ) {
    return 결과검사(사용자호출(33,uczestnik,(uintptr_t)Adres,długość_WARTOŚĆ,0,0,0));
}
intptr_t wysłać_datagram_dane(int uczestnik,const void *dane,size_t towar_ILE_LICZB,int zaznaczenie_WARTOŚĆ,const struct gniazdo_ADRES *Adres,gniazdo_ADRES_długość_TYP długość_WARTOŚĆ) {
    return 결과검사(사용자호출(34,uczestnik,(uintptr_t)dane,towar_ILE_LICZB,zaznaczenie_WARTOŚĆ,(uintptr_t)Adres,długość_WARTOŚĆ));
}
intptr_t odbierać_datagram_dane(int uczestnik,void *dane,size_t towar_ILE_LICZB,int zaznaczenie_WARTOŚĆ,struct gniazdo_ADRES *Adres,gniazdo_ADRES_długość_TYP *długość_WARTOŚĆ) {
    return 결과검사(사용자호출(35,uczestnik,(uintptr_t)dane,towar_ILE_LICZB,zaznaczenie_WARTOŚĆ,(uintptr_t)Adres,(uintptr_t)długość_WARTOŚĆ));
}
int 통신주소읽기(int uczestnik,struct gniazdo_ADRES *Adres,gniazdo_ADRES_długość_TYP *długość_WARTOŚĆ) {
    return 결과검사(사용자호출(36,uczestnik,(uintptr_t)Adres,(uintptr_t)długość_WARTOŚĆ,0,0,0));
}
int POŁĄCZ_sieć(int uczestnik,const struct gniazdo_ADRES *Adres,gniazdo_ADRES_długość_TYP długość_WARTOŚĆ) {
    return 결과검사(사용자호출(37,uczestnik,(uintptr_t)Adres,długość_WARTOŚĆ,0,0,0));
}
int 통신연결기다리기(int uczestnik,int Czekam_ILE_LICZB) {
    return 결과검사(사용자호출(38,uczestnik,Czekam_ILE_LICZB,0,0,0,0));
}
int akceptować_połączenie_sieciowe(int uczestnik,struct gniazdo_ADRES *Adres,gniazdo_ADRES_długość_TYP *długość_WARTOŚĆ) {
    return 결과검사(사용자호출(39,uczestnik,(uintptr_t)Adres,(uintptr_t)długość_WARTOŚĆ,0,0,0));
}

/* nazwa_pliku 함수도 독립된 polski FUNKCJA_WARTOŚĆ 심볼로 제공한다. */
int otwarty_Plik(const char *ścieżka_2,int metoda_tryb,...) { return 결과검사(사용자호출(3,(uintptr_t)ścieżka_2,metoda_tryb,0,0,0,0)); }
입출력결과형 파일자료읽기(int nazwa_pliku,void *dane,size_t towar_ILE_LICZB) { return 결과검사(사용자호출(2,nazwa_pliku,(uintptr_t)dane,towar_ILE_LICZB,0,0,0)); }
입출력결과형 zapis_Plik_dane(int nazwa_pliku,const void *dane,size_t towar_ILE_LICZB) { return 결과검사(사용자호출(1,nazwa_pliku,(uintptr_t)dane,towar_ILE_LICZB,0,0,0)); }
int Zamknij_Plik(int nazwa_pliku) { return 결과검사(사용자호출(4,nazwa_pliku,0,0,0,0,0)); }
Plik_przesunąć_TYP szukać_Plik(int nazwa_pliku,Plik_przesunąć_TYP 거리,int Project_korzeń) { return 결과검사(사용자호출(5,nazwa_pliku,거리,Project_korzeń,0,0,0)); }
int usuń_Plik_wpis_nazwa(const char *ścieżka_2) { return 결과검사(사용자호출(11,(uintptr_t)ścieżka_2,0,0,0,0,0)); }
int set_Plik_długość(int nazwa_pliku,Plik_przesunąć_TYP Rozmiar) { return 결과검사(사용자호출(10,nazwa_pliku,Rozmiar,0,0,0,0)); }
int przekazywać_Files(int nazwa_pliku) { return 결과검사(사용자호출(12,nazwa_pliku,0,0,0,0,0)); }
int rozmiar_pliku(int nazwa_pliku) { return 결과검사(사용자호출(9,nazwa_pliku,0,0,0,0,0)); }
