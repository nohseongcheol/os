#include "Plik_ABI.h"
#include "호출.h"
static int inicjator_WARTOŚĆ;
static volatile int inicjator_umieścić = 72;
static volatile double liczba_zmiennoprzecinkowa_umieścić = 1.25;
static int 소멸횟수;
struct test_inicjowanie { test_inicjowanie() { inicjator_WARTOŚĆ = inicjator_umieścić + 1; } } 정적초기화;
class Automatyczna_Plik {
    int INDEKS;
public:
    explicit Automatyczna_Plik(const char *Nazwa) : INDEKS(otwarty_Plik(Nazwa, R_W | 없으면만들기 | obcinać_Spis_treści, 0600)) {}
    ~Automatyczna_Plik() { if (INDEKS >= 0) Zamknij_Plik(INDEKS); 소멸횟수++; }
    int deskryptor_wpis() const { return INDEKS; }
};
extern "C" int START_użytkownik_program(int) {
    if (inicjator_WARTOŚĆ != 73 || 사용자호출(0, 0, 0, 0, 0, 0, 0) != 1) return 1;
    double liczba_zmiennoprzecinkowa_WARTOŚĆ = liczba_zmiennoprzecinkowa_umieścić * 2.0 + 0.5;
    if (사용자호출(0, 0, 0, 0, 0, 0, 0) != 1 || liczba_zmiennoprzecinkowa_WARTOŚĆ != 3.0) return 16;
    static const char treść_WARTOŚĆ_cb0f2404[] = "EL0 C++ → posix-kor → Java nazwa_pliku · 안녕하세요 😀\n";
    char 읽은값[sizeof(treść_WARTOŚĆ_cb0f2404)] = {};
    {
        Automatyczna_Plik nazwa_pliku("przestrzeń_użytkownika.txt");
        int INDEKS = nazwa_pliku.deskryptor_wpis();
        if (INDEKS < 0 || zapis_Plik_dane(INDEKS, treść_WARTOŚĆ_cb0f2404, sizeof(treść_WARTOŚĆ_cb0f2404)) != sizeof(treść_WARTOŚĆ_cb0f2404)) return 2;
        if (szukać_Plik(INDEKS, 0, 처음기준) || 파일자료읽기(INDEKS, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 3;
        for (unsigned 순번 = 0; 순번 < sizeof(treść_WARTOŚĆ_cb0f2404); 순번++) if (읽은값[순번] != treść_WARTOŚĆ_cb0f2404[순번]) return 4;
    }
    if (소멸횟수 != 1) return 5;
    if (zapis_Plik_dane(1, treść_WARTOŚĆ_cb0f2404, sizeof(treść_WARTOŚĆ_cb0f2404) - 1) != sizeof(treść_WARTOŚĆ_cb0f2404) - 1) return 6;
    uintptr_t 바닥 = użytkownik_Pamięć_Koniec(0);
    if (바닥 != 0x02c00000 || użytkownik_Pamięć_Koniec(바닥 + 8192) != (intptr_t)(바닥 + 8192)) return 7;
    volatile unsigned char *Pamięć_WARTOŚĆ = (volatile unsigned char *)바닥;
    if (Pamięć_WARTOŚĆ[0] || Pamięć_WARTOŚĆ[8191]) return 8;
    Pamięć_WARTOŚĆ[8191] = 137;
    if (użytkownik_Pamięć_Koniec(바닥) != (intptr_t)바닥 || użytkownik_Pamięć_Koniec(바닥 + 8192) != (intptr_t)(바닥 + 8192) || Pamięć_WARTOŚĆ[8191]) return 9;
    // 잘못된 przestrzeń_użytkownika wskaźnik/번호는 오류이며 커널을 중단하지 않는다.
    if (zapis_Plik_dane(1, (const void *)0x80000, 8) != -1 || numer_błędu != 14) return 10;
    if (파일자료읽기(0, (void *)treść_WARTOŚĆ_cb0f2404, 1) != -1 || numer_błędu != 14) return 11;
    if (사용자호출(999, 0, 0, 0, 0, 0, 0) != -38) return 12;
    intptr_t 화면폭 = 화면너비읽기(), 화면길이 = 화면높이읽기();
    if (화면폭 <= 0 || 화면길이 <= 0 || 사용자호출(13, 화면폭-1, 화면길이-1, 0, 2, 2, 0) != -22) return 13;
    if (화면사각형(470, 310, 80, 60, 0x40c050)) return 14;
    // 프로세스 wyjść_program 시 열린 서술자가 자동 정리되어야 한다.
    if (otwarty_Plik("przestrzeń_użytkownika.txt", tylko_do_odczytu_WARTOŚĆ) < 0) return 15;
    return 0;
}
