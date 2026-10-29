#include "통신규약.h"

int START_korisnik_program(int Argumenti) {
    (void)Argumenti;
    struct 인터넷통신주소 adresa = {0};
    adresa.adresa_linija = oblak_linija;
    adresa.broj_priključka = 망차례짧은수(9260);
    adresa.internetska_adresa.adresa_VALUE = mreža_cijeli_broj(povratna_adresa);
    int server_VALUE = Create_sudionik(oblak_linija, tok_mreža, tok_protokol_za_prijenos);
    if (server_VALUE < 0 || BIND_adresa(server_VALUE, (struct 통신주소 *)&adresa, sizeof(adresa)) < 0 ||
        통신연결기다리기(server_VALUE, 4) < 0) return 1;
    if (prihvatiti_mrežna_veza(server_VALUE, 0, 0) != -1 || broj_pogreške != 11) return 2;
    int gost_VALUE = Create_sudionik(oblak_linija, tok_mreža, tok_protokol_za_prijenos);
    if (gost_VALUE < 0 || CONNECT_mreža(gost_VALUE, (struct 통신주소 *)&adresa, sizeof(adresa)) < 0) return 3;
    int Spoji_se = prihvatiti_mrežna_veza(server_VALUE, 0, 0);
    if (Spoji_se < 0) return 4;
    unsigned char 보낼것[1500], RECEIVED_artikl[1500];
    for (int 수 = 0; 수 < 1500; 수++) 보낼것[수] = (unsigned char)수;
    int 보낸수 = 0;
    while (보낸수 < 1024) {
        int 길이 = zapisivanje_Datoteka_podaci(gost_VALUE, 보낼것 + 보낸수, sizeof(보낼것) - 보낸수);
        if (길이 <= 0) return 5;
        보낸수 += 길이;
    }
    if (zapisivanje_Datoteka_podaci(gost_VALUE, 보낼것, 1) != -1 || broj_pogreške != 11) return 6;
    /* 상대가 닫아도 이미 도착한 자료를 모두 읽은 TRAG_VALUE EOF가 된다. */
    Zatvori_Datoteka(gost_VALUE);
    int RECEIVED_COUNT = 0;
    while (RECEIVED_COUNT < 보낸수) {
        int 길이 = 파일자료읽기(Spoji_se, RECEIVED_artikl + RECEIVED_COUNT, sizeof(RECEIVED_artikl) - RECEIVED_COUNT);
        if (길이 <= 0) return 7;
        RECEIVED_COUNT += 길이;
    }
    for (int 수 = 0; 수 < RECEIVED_COUNT; 수++) if (RECEIVED_artikl[수] != 보낼것[수]) return 8;
    if (파일자료읽기(Spoji_se, RECEIVED_artikl, 1) != 0) return 9;
    if (zapisivanje_Datoteka_podaci(Spoji_se, 보낼것, 1) != -1 || broj_pogreške != 32) return 10;
    Zatvori_Datoteka(Spoji_se); Zatvori_Datoteka(server_VALUE);
    const char REZULTAT[] = "C posix-kor 연결형 통신 PASS\n";
    zapisivanje_Datoteka_podaci(1, REZULTAT, sizeof(REZULTAT) - 1);
    return 0;
}
