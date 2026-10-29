#include "통신규약.h"
static cloud_soket_adresa adresa(unsigned port_VALUE) {
    cloud_soket_adresa VALUE = {}; VALUE.adresa_séria = cloud_séria;
    VALUE.číslo_portu = 망차례짧은수(port_VALUE); VALUE.internetová_adresa.adresa_VALUE = sieť_celé_číslo(adresa_systémovej_slučky); return VALUE;
}
extern "C" int START_používateľ_program(int) {
    int 보내는곳 = Create_účastník(cloud_séria, datagramový_soket, 0);
    int 받는곳 = Create_účastník(cloud_séria, datagramový_soket, datagram_protokol);
    if (보내는곳 < 0 || 받는곳 < 0) return 1;
    cloud_soket_adresa 도착 = adresa(7777), 출발 = adresa(7778), 보낸주소 = {};
    soket_adresa_dĺžka_Typ adresa_dĺžka = sizeof(보낸주소);
    if (BIND_adresa(받는곳, (soket_adresa *)&도착, sizeof(도착))) return 2;
    if (BIND_adresa(보내는곳, (soket_adresa *)&도착, sizeof(도착)) != -1 || chybové_číslo != 98) return 3;
    if (BIND_adresa(보내는곳, (soket_adresa *)&출발, sizeof(출발))) return 4;
    static const char obsah_VALUE[] = "한글 UDP loopback 😀";
    char RECEIVED_VALUE[64] = {};
    if (odoslať_datagram_údaje(보내는곳, obsah_VALUE, sizeof(obsah_VALUE), 0, (soket_adresa *)&도착, sizeof(도착)) != sizeof(obsah_VALUE)) return 5;
    if (dostať_datagram_údaje(받는곳, (void *)obsah_VALUE, sizeof(obsah_VALUE), 0, 0, 0) != -1 || chybové_číslo != 14) return 6;
    if (dostať_datagram_údaje(받는곳, RECEIVED_VALUE, sizeof(RECEIVED_VALUE), 0, (soket_adresa *)&보낸주소, &adresa_dĺžka) != sizeof(obsah_VALUE)) return 7;
    if (adresa_dĺžka != sizeof(보낸주소) || 장치차례짧은수(보낸주소.číslo_portu) != 7778 || telefón_poradie_celé_číslo(보낸주소.internetová_adresa.adresa_VALUE) != adresa_systémovej_slučky) return 8;
    for (unsigned 순번 = 0; 순번 < sizeof(obsah_VALUE); 순번++) if (RECEIVED_VALUE[순번] != obsah_VALUE[순번]) return 9;
    if (dostať_datagram_údaje(받는곳, RECEIVED_VALUE, sizeof(RECEIVED_VALUE), 0, 0, 0) != -1 || chybové_číslo != 11) return 10;
    if (odoslať_datagram_údaje(받는곳, RECEIVED_VALUE, sizeof(obsah_VALUE), 0, (soket_adresa *)&보낸주소, sizeof(보낸주소)) != sizeof(obsah_VALUE)) return 11;
    if (dostať_datagram_údaje(보내는곳, RECEIVED_VALUE, 4, 0, 0, 0) != 4) return 12;
    if (dostať_datagram_údaje(보내는곳, RECEIVED_VALUE, 4, 0, 0, 0) != -1 || chybové_číslo != 11) return 13;
    for (int 순번 = 0; 순번 < 4; 순번++) if (odoslať_datagram_údaje(보내는곳, obsah_VALUE, sizeof(obsah_VALUE), 0, (soket_adresa *)&도착, sizeof(도착)) != sizeof(obsah_VALUE)) return 14;
    if (odoslať_datagram_údaje(보내는곳, obsah_VALUE, sizeof(obsah_VALUE), 0, (soket_adresa *)&도착, sizeof(도착)) != -1 || chybové_číslo != 11) return 15;
    for (int 순번 = 0; 순번 < 4; 순번++) if (dostať_datagram_údaje(받는곳, RECEIVED_VALUE, sizeof(RECEIVED_VALUE), 0, 0, 0) != sizeof(obsah_VALUE)) return 16;
    if (odoslať_datagram_údaje(보내는곳, 0, 0, 0, (soket_adresa *)&도착, sizeof(도착)) != 0 ||
        dostať_datagram_údaje(받는곳, 0, 0, 0, 0, 0) != 0) return 21;
    도착.internetová_adresa.adresa_VALUE = sieť_celé_číslo(0x08080808);
    if (odoslať_datagram_údaje(보내는곳, obsah_VALUE, sizeof(obsah_VALUE), 0, (soket_adresa *)&도착, sizeof(도착)) != -1 || chybové_číslo != 101) return 17;
    if (Create_účastník(cloud_séria, Stream_sieť, datagram_protokol) != -1 || chybové_číslo != 93) return 18;
    adresa_dĺžka = sizeof(보낸주소);
    if (통신주소읽기(받는곳, (soket_adresa *)&보낸주소, &adresa_dĺžka) || 장치차례짧은수(보낸주소.číslo_portu) != 7777) return 19;
    if (Zavrieť_Súbor(받는곳) || Zavrieť_Súbor(받는곳) != -1 || chybové_číslo != 9) return 20;
    // 보내는곳은 열어 둔다: Skončiť_program 시 프로세스별 socket 정리를 검사한다.
    static const char 완료[] = "EL0 UDP LOOPBACK PASS (external network unavailable)\n";
    zapísať_Súbor_údaje(1, 완료, sizeof(완료) - 1);
    return 0;
}
