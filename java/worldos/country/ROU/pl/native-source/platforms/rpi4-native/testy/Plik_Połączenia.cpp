#include "../명명/기계연결이름.h"
#include "Plik_ABI.h"
// 표준 C++ biblioteka 없는 freestanding C++11 program_f5044b9b. 커널에 statyczny_WARTOŚĆ 링크한다.
extern "C" uintptr_t 시플플시험(void) {
    const char treść_WARTOŚĆ_cb0f2404[] = "C++ → Java jądro_WARTOŚĆ · 한글 😀";
    unsigned char 읽은값[sizeof(treść_WARTOŚĆ_cb0f2404)] = {};
    int nazwa_pliku = otwarty_Plik("testy.txt", R_W | 없으면만들기 | obcinać_Spis_treści, 0600);
    if (nazwa_pliku < 0) return 1;
    if (zapis_Plik_dane(nazwa_pliku, treść_WARTOŚĆ_cb0f2404, sizeof(treść_WARTOŚĆ_cb0f2404)) != sizeof(treść_WARTOŚĆ_cb0f2404)) return 2;
    if (szukać_Plik(nazwa_pliku, 0, 처음기준) != 0) return 3;
    if (파일자료읽기(nazwa_pliku, 읽은값, sizeof(읽은값)) != sizeof(읽은값)) return 4;
    for (size_t 순번 = 0; 순번 < sizeof(treść_WARTOŚĆ_cb0f2404); 순번++) if (읽은값[순번] != (unsigned char)treść_WARTOŚĆ_cb0f2404[순번]) return 5;
    if (파일자료읽기(nazwa_pliku, 읽은값, 1) != 0) return 6;
    if (przekazywać_Files(nazwa_pliku) != -1 || numer_błędu != 38) return 7;
    if (Zamknij_Plik(nazwa_pliku) || Zamknij_Plik(nazwa_pliku) != -1 || numer_błędu != 9) return 8;
    nazwa_pliku = otwarty_Plik("testy.txt", tylko_do_odczytu_WARTOŚĆ);
    if (nazwa_pliku < 0 || zapis_Plik_dane(nazwa_pliku, treść_WARTOŚĆ_cb0f2404, 1) != -1 || numer_błędu != 9) return 9;
    if (Zamknij_Plik(nazwa_pliku)) return 10;
    nazwa_pliku = otwarty_Plik("testy.txt", R_W | 끝에이어쓰기);
    if (nazwa_pliku < 0 || szukać_Plik(nazwa_pliku, 0, 처음기준) != 0 || zapis_Plik_dane(nazwa_pliku, "!", 1) != 1 || rozmiar_pliku(nazwa_pliku) != sizeof(treść_WARTOŚĆ_cb0f2404) + 1) return 11;
    if (set_Plik_długość(nazwa_pliku, 2) || szukać_Plik(nazwa_pliku, 4, 처음기준) != 4) return 12;
    // append는 매 write 때 EOF를 사용한다.
    if (zapis_Plik_dane(nazwa_pliku, "x", 1) != 1 || rozmiar_pliku(nazwa_pliku) != 3 || Zamknij_Plik(nazwa_pliku)) return 13;
    nazwa_pliku = otwarty_Plik("구멍.bin", R_W | 없으면만들기 | obcinać_Spis_treści, 0600);
    if (nazwa_pliku < 0 || szukać_Plik(nazwa_pliku, 3, 처음기준) != 3 || zapis_Plik_dane(nazwa_pliku, "z", 1) != 1) return 14;
    if (szukać_Plik(nazwa_pliku, 0, 처음기준) != 0 || 파일자료읽기(nazwa_pliku, 읽은값, 4) != 4 || 읽은값[0] || 읽은값[1] || 읽은값[2] || 읽은값[3] != 'z') return 15;
    if (usuń_Plik_wpis_nazwa("구멍.bin") || rozmiar_pliku(nazwa_pliku) != 4 || Zamknij_Plik(nazwa_pliku)) return 16;
    if (otwarty_Plik("구멍.bin", tylko_do_odczytu_WARTOŚĆ) != -1 || numer_błędu != 2) return 17;
    if (otwarty_Plik("testy.txt", R_W | 새파일만들기, 0600) != -1 || numer_błędu != 17) return 18;
    if (otwarty_Plik("../금지", tylko_do_odczytu_WARTOŚĆ) != -1) return 19;
    return 0;
}
