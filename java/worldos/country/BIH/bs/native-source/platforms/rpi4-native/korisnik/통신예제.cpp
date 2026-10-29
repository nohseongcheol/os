#include "통신규약.h"
static 인터넷통신주소 adresa(unsigned port_VALUE) {
    인터넷통신주소 VALUE = {}; VALUE.adresa_Porodica = oblak_Porodica;
    VALUE.broj_priključka = 망차례짧은수(port_VALUE); VALUE.internetska_adresa.adresa_VALUE = Mreža_cijeli_broj(povratna_adresa); return VALUE;
}
extern "C" int START_korisnik_program(int) {
    int 보내는곳 = Create_završna_tačka(oblak_Porodica, 전문통신, 0);
    int 받는곳 = Create_završna_tačka(oblak_Porodica, 전문통신, 전문전송규약);
    if (보내는곳 < 0 || 받는곳 < 0) return 1;
    인터넷통신주소 도착 = adresa(7777), 출발 = adresa(7778), 보낸주소 = {};
    통신주소길이형 adresa_dužina = sizeof(보낸주소);
    if (BIND_adresa(받는곳, (통신주소 *)&도착, sizeof(도착))) return 2;
    if (BIND_adresa(보내는곳, (통신주소 *)&도착, sizeof(도착)) != -1 || broj_greške != 98) return 3;
    if (BIND_adresa(보내는곳, (통신주소 *)&출발, sizeof(출발))) return 4;
    static const char Sadržaj_VALUE[] = "한글 UDP loopback 😀";
    char RECEIVED_VALUE[64] = {};
    if (자료전문보내기(보내는곳, Sadržaj_VALUE, sizeof(Sadržaj_VALUE), 0, (통신주소 *)&도착, sizeof(도착)) != sizeof(Sadržaj_VALUE)) return 5;
    if (자료전문받기(받는곳, (void *)Sadržaj_VALUE, sizeof(Sadržaj_VALUE), 0, 0, 0) != -1 || broj_greške != 14) return 6;
    if (자료전문받기(받는곳, RECEIVED_VALUE, sizeof(RECEIVED_VALUE), 0, (통신주소 *)&보낸주소, &adresa_dužina) != sizeof(Sadržaj_VALUE)) return 7;
    if (adresa_dužina != sizeof(보낸주소) || 장치차례짧은수(보낸주소.broj_priključka) != 7778 || uređaj_redoslijed_cijeli_broj(보낸주소.internetska_adresa.adresa_VALUE) != povratna_adresa) return 8;
    for (unsigned 순번 = 0; 순번 < sizeof(Sadržaj_VALUE); 순번++) if (RECEIVED_VALUE[순번] != Sadržaj_VALUE[순번]) return 9;
    if (자료전문받기(받는곳, RECEIVED_VALUE, sizeof(RECEIVED_VALUE), 0, 0, 0) != -1 || broj_greške != 11) return 10;
    if (자료전문보내기(받는곳, RECEIVED_VALUE, sizeof(Sadržaj_VALUE), 0, (통신주소 *)&보낸주소, sizeof(보낸주소)) != sizeof(Sadržaj_VALUE)) return 11;
    if (자료전문받기(보내는곳, RECEIVED_VALUE, 4, 0, 0, 0) != 4) return 12;
    if (자료전문받기(보내는곳, RECEIVED_VALUE, 4, 0, 0, 0) != -1 || broj_greške != 11) return 13;
    for (int 순번 = 0; 순번 < 4; 순번++) if (자료전문보내기(보내는곳, Sadržaj_VALUE, sizeof(Sadržaj_VALUE), 0, (통신주소 *)&도착, sizeof(도착)) != sizeof(Sadržaj_VALUE)) return 14;
    if (자료전문보내기(보내는곳, Sadržaj_VALUE, sizeof(Sadržaj_VALUE), 0, (통신주소 *)&도착, sizeof(도착)) != -1 || broj_greške != 11) return 15;
    for (int 순번 = 0; 순번 < 4; 순번++) if (자료전문받기(받는곳, RECEIVED_VALUE, sizeof(RECEIVED_VALUE), 0, 0, 0) != sizeof(Sadržaj_VALUE)) return 16;
    if (자료전문보내기(보내는곳, 0, 0, 0, (통신주소 *)&도착, sizeof(도착)) != 0 ||
        자료전문받기(받는곳, 0, 0, 0, 0, 0) != 0) return 21;
    도착.internetska_adresa.adresa_VALUE = Mreža_cijeli_broj(0x08080808);
    if (자료전문보내기(보내는곳, Sadržaj_VALUE, sizeof(Sadržaj_VALUE), 0, (통신주소 *)&도착, sizeof(도착)) != -1 || broj_greške != 101) return 17;
    if (Create_završna_tačka(oblak_Porodica, tok_Mreža, 전문전송규약) != -1 || broj_greške != 93) return 18;
    adresa_dužina = sizeof(보낸주소);
    if (통신주소읽기(받는곳, (통신주소 *)&보낸주소, &adresa_dužina) || 장치차례짧은수(보낸주소.broj_priključka) != 7777) return 19;
    if (zatvoriti_fajl(받는곳) || zatvoriti_fajl(받는곳) != -1 || broj_greške != 9) return 20;
    // 보내는곳은 열어 둔다: izaći_program 시 프로세스별 socket 정리를 검사한다.
    static const char 완료[] = "EL0 UDP LOOPBACK PASS (external network unavailable)\n";
    pisati_fajl_podaci(1, 완료, sizeof(완료) - 1);
    return 0;
}
