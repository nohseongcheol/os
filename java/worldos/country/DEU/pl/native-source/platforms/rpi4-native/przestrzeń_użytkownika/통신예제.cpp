#include "sieć_ABI.h"
static chmura_gniazdo_ADRES Adres(unsigned port_WARTOŚĆ) {
    chmura_gniazdo_ADRES WARTOŚĆ = {}; WARTOŚĆ.ADRES_Rodzina = chmura_Rodzina;
    WARTOŚĆ.numer_portu = 망차례짧은수(port_WARTOŚĆ); WARTOŚĆ.adres_internetowy.ADRES_WARTOŚĆ = sieć_liczba_całkowita(adres_sprzężenia_zwrotnego); return WARTOŚĆ;
}
extern "C" int START_użytkownik_program(int) {
    int 보내는곳 = Twórca_uczestnik(chmura_Rodzina, gniazdo_do_przesyłania_datagramów, 0);
    int 받는곳 = Twórca_uczestnik(chmura_Rodzina, gniazdo_do_przesyłania_datagramów, datagram_protokół);
    if (보내는곳 < 0 || 받는곳 < 0) return 1;
    chmura_gniazdo_ADRES 도착 = Adres(7777), 출발 = Adres(7778), 보낸주소 = {};
    gniazdo_ADRES_długość_TYP ADRES_długość = sizeof(보낸주소);
    if (BIND_ADRES(받는곳, (gniazdo_ADRES *)&도착, sizeof(도착))) return 2;
    if (BIND_ADRES(보내는곳, (gniazdo_ADRES *)&도착, sizeof(도착)) != -1 || numer_błędu != 98) return 3;
    if (BIND_ADRES(보내는곳, (gniazdo_ADRES *)&출발, sizeof(출발))) return 4;
    static const char treść_WARTOŚĆ_cb0f2404[] = "한글 UDP loopback 😀";
    char KWOTA_WYKUP_WARTOŚĆ[64] = {};
    if (wysłać_datagram_dane(보내는곳, treść_WARTOŚĆ_cb0f2404, sizeof(treść_WARTOŚĆ_cb0f2404), 0, (gniazdo_ADRES *)&도착, sizeof(도착)) != sizeof(treść_WARTOŚĆ_cb0f2404)) return 5;
    if (odbierać_datagram_dane(받는곳, (void *)treść_WARTOŚĆ_cb0f2404, sizeof(treść_WARTOŚĆ_cb0f2404), 0, 0, 0) != -1 || numer_błędu != 14) return 6;
    if (odbierać_datagram_dane(받는곳, KWOTA_WYKUP_WARTOŚĆ, sizeof(KWOTA_WYKUP_WARTOŚĆ), 0, (gniazdo_ADRES *)&보낸주소, &ADRES_długość) != sizeof(treść_WARTOŚĆ_cb0f2404)) return 7;
    if (ADRES_długość != sizeof(보낸주소) || 장치차례짧은수(보낸주소.numer_portu) != 7778 || urządzenie_zamówić_liczba_całkowita(보낸주소.adres_internetowy.ADRES_WARTOŚĆ) != adres_sprzężenia_zwrotnego) return 8;
    for (unsigned 순번 = 0; 순번 < sizeof(treść_WARTOŚĆ_cb0f2404); 순번++) if (KWOTA_WYKUP_WARTOŚĆ[순번] != treść_WARTOŚĆ_cb0f2404[순번]) return 9;
    if (odbierać_datagram_dane(받는곳, KWOTA_WYKUP_WARTOŚĆ, sizeof(KWOTA_WYKUP_WARTOŚĆ), 0, 0, 0) != -1 || numer_błędu != 11) return 10;
    if (wysłać_datagram_dane(받는곳, KWOTA_WYKUP_WARTOŚĆ, sizeof(treść_WARTOŚĆ_cb0f2404), 0, (gniazdo_ADRES *)&보낸주소, sizeof(보낸주소)) != sizeof(treść_WARTOŚĆ_cb0f2404)) return 11;
    if (odbierać_datagram_dane(보내는곳, KWOTA_WYKUP_WARTOŚĆ, 4, 0, 0, 0) != 4) return 12;
    if (odbierać_datagram_dane(보내는곳, KWOTA_WYKUP_WARTOŚĆ, 4, 0, 0, 0) != -1 || numer_błędu != 11) return 13;
    for (int 순번 = 0; 순번 < 4; 순번++) if (wysłać_datagram_dane(보내는곳, treść_WARTOŚĆ_cb0f2404, sizeof(treść_WARTOŚĆ_cb0f2404), 0, (gniazdo_ADRES *)&도착, sizeof(도착)) != sizeof(treść_WARTOŚĆ_cb0f2404)) return 14;
    if (wysłać_datagram_dane(보내는곳, treść_WARTOŚĆ_cb0f2404, sizeof(treść_WARTOŚĆ_cb0f2404), 0, (gniazdo_ADRES *)&도착, sizeof(도착)) != -1 || numer_błędu != 11) return 15;
    for (int 순번 = 0; 순번 < 4; 순번++) if (odbierać_datagram_dane(받는곳, KWOTA_WYKUP_WARTOŚĆ, sizeof(KWOTA_WYKUP_WARTOŚĆ), 0, 0, 0) != sizeof(treść_WARTOŚĆ_cb0f2404)) return 16;
    if (wysłać_datagram_dane(보내는곳, 0, 0, 0, (gniazdo_ADRES *)&도착, sizeof(도착)) != 0 ||
        odbierać_datagram_dane(받는곳, 0, 0, 0, 0, 0) != 0) return 21;
    도착.adres_internetowy.ADRES_WARTOŚĆ = sieć_liczba_całkowita(0x08080808);
    if (wysłać_datagram_dane(보내는곳, treść_WARTOŚĆ_cb0f2404, sizeof(treść_WARTOŚĆ_cb0f2404), 0, (gniazdo_ADRES *)&도착, sizeof(도착)) != -1 || numer_błędu != 101) return 17;
    if (Twórca_uczestnik(chmura_Rodzina, Stream_sieć, datagram_protokół) != -1 || numer_błędu != 93) return 18;
    ADRES_długość = sizeof(보낸주소);
    if (통신주소읽기(받는곳, (gniazdo_ADRES *)&보낸주소, &ADRES_długość) || 장치차례짧은수(보낸주소.numer_portu) != 7777) return 19;
    if (Zamknij_Plik(받는곳) || Zamknij_Plik(받는곳) != -1 || numer_błędu != 9) return 20;
    // 보내는곳은 열어 둔다: wyjść_program 시 프로세스별 socket 정리를 검사한다.
    static const char 완료[] = "EL0 UDP LOOPBACK PASS (external network unavailable)\n";
    zapis_Plik_dane(1, 완료, sizeof(완료) - 1);
    return 0;
}
