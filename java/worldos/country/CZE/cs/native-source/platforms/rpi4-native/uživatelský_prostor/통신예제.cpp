#include "síť_ABI.h"
static cloud_soket_ODKAZ Adresa(unsigned port_HODNOTA) {
    cloud_soket_ODKAZ HODNOTA = {}; HODNOTA.ODKAZ_řada = cloud_řada;
    HODNOTA.číslo_portu = 망차례짧은수(port_HODNOTA); HODNOTA.internetová_adresa.ODKAZ_HODNOTA = síť_integer(adresa_zpětné_smyčky); return HODNOTA;
}
extern "C" int START_uživatel_program(int) {
    int 보내는곳 = Create_účastník(cloud_řada, datagramový_soket, 0);
    int 받는곳 = Create_účastník(cloud_řada, datagramový_soket, datagram_protokol);
    if (보내는곳 < 0 || 받는곳 < 0) return 1;
    cloud_soket_ODKAZ 도착 = Adresa(7777), 출발 = Adresa(7778), 보낸주소 = {};
    soket_ODKAZ_délka_TYP ODKAZ_délka = sizeof(보낸주소);
    if (vázat_ODKAZ(받는곳, (soket_ODKAZ *)&도착, sizeof(도착))) return 2;
    if (vázat_ODKAZ(보내는곳, (soket_ODKAZ *)&도착, sizeof(도착)) != -1 || číslo_chyby != 98) return 3;
    if (vázat_ODKAZ(보내는곳, (soket_ODKAZ *)&출발, sizeof(출발))) return 4;
    static const char Obsah_HODNOTA[] = "한글 UDP loopback 😀";
    char RECEIVED_HODNOTA[64] = {};
    if (poslat_datagram_data(보내는곳, Obsah_HODNOTA, sizeof(Obsah_HODNOTA), 0, (soket_ODKAZ *)&도착, sizeof(도착)) != sizeof(Obsah_HODNOTA)) return 5;
    if (dostat_datagram_data(받는곳, (void *)Obsah_HODNOTA, sizeof(Obsah_HODNOTA), 0, 0, 0) != -1 || číslo_chyby != 14) return 6;
    if (dostat_datagram_data(받는곳, RECEIVED_HODNOTA, sizeof(RECEIVED_HODNOTA), 0, (soket_ODKAZ *)&보낸주소, &ODKAZ_délka) != sizeof(Obsah_HODNOTA)) return 7;
    if (ODKAZ_délka != sizeof(보낸주소) || 장치차례짧은수(보낸주소.číslo_portu) != 7778 || mobilní_pořadí_integer(보낸주소.internetová_adresa.ODKAZ_HODNOTA) != adresa_zpětné_smyčky) return 8;
    for (unsigned 순번 = 0; 순번 < sizeof(Obsah_HODNOTA); 순번++) if (RECEIVED_HODNOTA[순번] != Obsah_HODNOTA[순번]) return 9;
    if (dostat_datagram_data(받는곳, RECEIVED_HODNOTA, sizeof(RECEIVED_HODNOTA), 0, 0, 0) != -1 || číslo_chyby != 11) return 10;
    if (poslat_datagram_data(받는곳, RECEIVED_HODNOTA, sizeof(Obsah_HODNOTA), 0, (soket_ODKAZ *)&보낸주소, sizeof(보낸주소)) != sizeof(Obsah_HODNOTA)) return 11;
    if (dostat_datagram_data(보내는곳, RECEIVED_HODNOTA, 4, 0, 0, 0) != 4) return 12;
    if (dostat_datagram_data(보내는곳, RECEIVED_HODNOTA, 4, 0, 0, 0) != -1 || číslo_chyby != 11) return 13;
    for (int 순번 = 0; 순번 < 4; 순번++) if (poslat_datagram_data(보내는곳, Obsah_HODNOTA, sizeof(Obsah_HODNOTA), 0, (soket_ODKAZ *)&도착, sizeof(도착)) != sizeof(Obsah_HODNOTA)) return 14;
    if (poslat_datagram_data(보내는곳, Obsah_HODNOTA, sizeof(Obsah_HODNOTA), 0, (soket_ODKAZ *)&도착, sizeof(도착)) != -1 || číslo_chyby != 11) return 15;
    for (int 순번 = 0; 순번 < 4; 순번++) if (dostat_datagram_data(받는곳, RECEIVED_HODNOTA, sizeof(RECEIVED_HODNOTA), 0, 0, 0) != sizeof(Obsah_HODNOTA)) return 16;
    if (poslat_datagram_data(보내는곳, 0, 0, 0, (soket_ODKAZ *)&도착, sizeof(도착)) != 0 ||
        dostat_datagram_data(받는곳, 0, 0, 0, 0, 0) != 0) return 21;
    도착.internetová_adresa.ODKAZ_HODNOTA = síť_integer(0x08080808);
    if (poslat_datagram_data(보내는곳, Obsah_HODNOTA, sizeof(Obsah_HODNOTA), 0, (soket_ODKAZ *)&도착, sizeof(도착)) != -1 || číslo_chyby != 101) return 17;
    if (Create_účastník(cloud_řada, tok_síť, datagram_protokol) != -1 || číslo_chyby != 93) return 18;
    ODKAZ_délka = sizeof(보낸주소);
    if (통신주소읽기(받는곳, (soket_ODKAZ *)&보낸주소, &ODKAZ_délka) || 장치차례짧은수(보낸주소.číslo_portu) != 7777) return 19;
    if (Zavřít_Soubor(받는곳) || Zavřít_Soubor(받는곳) != -1 || číslo_chyby != 9) return 20;
    // 보내는곳은 열어 둔다: Konec_program 시 프로세스별 socket 정리를 검사한다.
    static const char 완료[] = "EL0 UDP LOOPBACK PASS (external network unavailable)\n";
    zápis_Soubor_data(1, 완료, sizeof(완료) - 1);
    return 0;
}
