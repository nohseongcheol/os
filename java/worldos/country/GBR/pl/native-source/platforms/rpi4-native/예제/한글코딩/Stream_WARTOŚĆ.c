#include "sieć_ABI.h"

int START_użytkownik_program(int argumenty) {
    (void)argumenty;
    struct chmura_gniazdo_ADRES Adres = {0};
    Adres.ADRES_Rodzina = chmura_Rodzina;
    Adres.numer_portu = 망차례짧은수(9260);
    Adres.adres_internetowy.ADRES_WARTOŚĆ = sieć_liczba_całkowita(adres_sprzężenia_zwrotnego);
    int serwer_WARTOŚĆ = Twórca_uczestnik(chmura_Rodzina, Stream_sieć, Stream_protokół_transportu);
    if (serwer_WARTOŚĆ < 0 || BIND_ADRES(serwer_WARTOŚĆ, (struct gniazdo_ADRES *)&Adres, sizeof(Adres)) < 0 ||
        통신연결기다리기(serwer_WARTOŚĆ, 4) < 0) return 1;
    if (akceptować_połączenie_sieciowe(serwer_WARTOŚĆ, 0, 0) != -1 || numer_błędu != 11) return 2;
    int gość_WARTOŚĆ = Twórca_uczestnik(chmura_Rodzina, Stream_sieć, Stream_protokół_transportu);
    if (gość_WARTOŚĆ < 0 || POŁĄCZ_sieć(gość_WARTOŚĆ, (struct gniazdo_ADRES *)&Adres, sizeof(Adres)) < 0) return 3;
    int Połącz = akceptować_połączenie_sieciowe(serwer_WARTOŚĆ, 0, 0);
    if (Połącz < 0) return 4;
    unsigned char 보낼것[1500], KWOTA_WYKUP_towar[1500];
    for (int identyfikator = 0; identyfikator < 1500; identyfikator++) 보낼것[identyfikator] = (unsigned char)identyfikator;
    int 보낸수 = 0;
    while (보낸수 < 1024) {
        int długość_WARTOŚĆ = zapis_Plik_dane(gość_WARTOŚĆ, 보낼것 + 보낸수, sizeof(보낼것) - 보낸수);
        if (długość_WARTOŚĆ <= 0) return 5;
        보낸수 += długość_WARTOŚĆ;
    }
    if (zapis_Plik_dane(gość_WARTOŚĆ, 보낼것, 1) != -1 || numer_błędu != 11) return 6;
    /* 상대가 닫아도 이미 도착한 자료를 모두 읽은 BACK_WARTOŚĆ EOF가 된다. */
    Zamknij_Plik(gość_WARTOŚĆ);
    int KWOTA_WYKUP_ILE_LICZB = 0;
    while (KWOTA_WYKUP_ILE_LICZB < 보낸수) {
        int długość_WARTOŚĆ = 파일자료읽기(Połącz, KWOTA_WYKUP_towar + KWOTA_WYKUP_ILE_LICZB, sizeof(KWOTA_WYKUP_towar) - KWOTA_WYKUP_ILE_LICZB);
        if (długość_WARTOŚĆ <= 0) return 7;
        KWOTA_WYKUP_ILE_LICZB += długość_WARTOŚĆ;
    }
    for (int identyfikator = 0; identyfikator < KWOTA_WYKUP_ILE_LICZB; identyfikator++) if (KWOTA_WYKUP_towar[identyfikator] != 보낼것[identyfikator]) return 8;
    if (파일자료읽기(Połącz, KWOTA_WYKUP_towar, 1) != 0) return 9;
    if (zapis_Plik_dane(Połącz, 보낼것, 1) != -1 || numer_błędu != 32) return 10;
    Zamknij_Plik(Połącz); Zamknij_Plik(serwer_WARTOŚĆ);
    const char WYNIK[] = "C posix-kor 연결형 komunikacja PASS\n";
    zapis_Plik_dane(1, WYNIK, sizeof(WYNIK) - 1);
    return 0;
}
