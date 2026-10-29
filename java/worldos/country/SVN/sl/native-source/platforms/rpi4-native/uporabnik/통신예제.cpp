#include "통신규약.h"
static oblak_vtičnica_naslov naslov(unsigned vrata_VALUE) {
    oblak_vtičnica_naslov VALUE = {}; VALUE.naslov_Družina = oblak_Družina;
    VALUE.številka_vrat = 망차례짧은수(vrata_VALUE); VALUE.internetni_račun.naslov_VALUE = mreža_celo_število(naslov_povratne_zanke); return VALUE;
}
extern "C" int Start_uporabnik_aplikacija(int) {
    int 보내는곳 = Ustvari_končna_točka(oblak_Družina, vtičnica_za_prenos_datagramov, 0);
    int 받는곳 = Ustvari_končna_točka(oblak_Družina, vtičnica_za_prenos_datagramov, datagram_protokol);
    if (보내는곳 < 0 || 받는곳 < 0) return 1;
    oblak_vtičnica_naslov 도착 = naslov(7777), 출발 = naslov(7778), 보낸주소 = {};
    통신주소길이형 주소길이 = sizeof(보낸주소);
    if (BIND_naslov(받는곳, (vtičnica_naslov *)&도착, sizeof(도착))) return 2;
    if (BIND_naslov(보내는곳, (vtičnica_naslov *)&도착, sizeof(도착)) != -1 || številka_napake != 98) return 3;
    if (BIND_naslov(보내는곳, (vtičnica_naslov *)&출발, sizeof(출발))) return 4;
    static const char vsebina_VALUE[] = "한글 UDP loopback 😀";
    char RECEIVED_VALUE[64] = {};
    if (poslati_datagram_podatki(보내는곳, vsebina_VALUE, sizeof(vsebina_VALUE), 0, (vtičnica_naslov *)&도착, sizeof(도착)) != sizeof(vsebina_VALUE)) return 5;
    if (sprejeti_sprejemati_prejeti_prejemati_datagram_podatki(받는곳, (void *)vsebina_VALUE, sizeof(vsebina_VALUE), 0, 0, 0) != -1 || številka_napake != 14) return 6;
    if (sprejeti_sprejemati_prejeti_prejemati_datagram_podatki(받는곳, RECEIVED_VALUE, sizeof(RECEIVED_VALUE), 0, (vtičnica_naslov *)&보낸주소, &주소길이) != sizeof(vsebina_VALUE)) return 7;
    if (주소길이 != sizeof(보낸주소) || 장치차례짧은수(보낸주소.številka_vrat) != 7778 || naprava_naročilo_celo_število(보낸주소.internetni_račun.naslov_VALUE) != naslov_povratne_zanke) return 8;
    for (unsigned 순번 = 0; 순번 < sizeof(vsebina_VALUE); 순번++) if (RECEIVED_VALUE[순번] != vsebina_VALUE[순번]) return 9;
    if (sprejeti_sprejemati_prejeti_prejemati_datagram_podatki(받는곳, RECEIVED_VALUE, sizeof(RECEIVED_VALUE), 0, 0, 0) != -1 || številka_napake != 11) return 10;
    if (poslati_datagram_podatki(받는곳, RECEIVED_VALUE, sizeof(vsebina_VALUE), 0, (vtičnica_naslov *)&보낸주소, sizeof(보낸주소)) != sizeof(vsebina_VALUE)) return 11;
    if (sprejeti_sprejemati_prejeti_prejemati_datagram_podatki(보내는곳, RECEIVED_VALUE, 4, 0, 0, 0) != 4) return 12;
    if (sprejeti_sprejemati_prejeti_prejemati_datagram_podatki(보내는곳, RECEIVED_VALUE, 4, 0, 0, 0) != -1 || številka_napake != 11) return 13;
    for (int 순번 = 0; 순번 < 4; 순번++) if (poslati_datagram_podatki(보내는곳, vsebina_VALUE, sizeof(vsebina_VALUE), 0, (vtičnica_naslov *)&도착, sizeof(도착)) != sizeof(vsebina_VALUE)) return 14;
    if (poslati_datagram_podatki(보내는곳, vsebina_VALUE, sizeof(vsebina_VALUE), 0, (vtičnica_naslov *)&도착, sizeof(도착)) != -1 || številka_napake != 11) return 15;
    for (int 순번 = 0; 순번 < 4; 순번++) if (sprejeti_sprejemati_prejeti_prejemati_datagram_podatki(받는곳, RECEIVED_VALUE, sizeof(RECEIVED_VALUE), 0, 0, 0) != sizeof(vsebina_VALUE)) return 16;
    if (poslati_datagram_podatki(보내는곳, 0, 0, 0, (vtičnica_naslov *)&도착, sizeof(도착)) != 0 ||
        sprejeti_sprejemati_prejeti_prejemati_datagram_podatki(받는곳, 0, 0, 0, 0, 0) != 0) return 21;
    도착.internetni_račun.naslov_VALUE = mreža_celo_število(0x08080808);
    if (poslati_datagram_podatki(보내는곳, vsebina_VALUE, sizeof(vsebina_VALUE), 0, (vtičnica_naslov *)&도착, sizeof(도착)) != -1 || številka_napake != 101) return 17;
    if (Ustvari_končna_točka(oblak_Družina, tok_mreža, datagram_protokol) != -1 || številka_napake != 93) return 18;
    주소길이 = sizeof(보낸주소);
    if (통신주소읽기(받는곳, (vtičnica_naslov *)&보낸주소, &주소길이) || 장치차례짧은수(보낸주소.številka_vrat) != 7777) return 19;
    if (Zapri_Datoteka(받는곳) || Zapri_Datoteka(받는곳) != -1 || številka_napake != 9) return 20;
    // 보내는곳은 열어 둔다: Izhod_aplikacija 시 프로세스별 socket 정리를 검사한다.
    static const char 완료[] = "EL0 UDP LOOPBACK PASS (external network unavailable)\n";
    pisati_Datoteka_podatki(1, 완료, sizeof(완료) - 1);
    return 0;
}
