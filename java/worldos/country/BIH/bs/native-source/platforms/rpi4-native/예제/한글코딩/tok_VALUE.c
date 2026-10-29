#include "통신규약.h"

int START_korisnik_program(int Argumenti) {
    (void)Argumenti;
    struct 인터넷통신주소 adresa = {0};
    adresa.adresa_Porodica = oblak_Porodica;
    adresa.broj_priključka = 망차례짧은수(9260);
    adresa.internetska_adresa.adresa_VALUE = Mreža_cijeli_broj(povratna_adresa);
    int server_VALUE = Create_završna_tačka(oblak_Porodica, tok_Mreža, 흐름전송규약);
    if (server_VALUE < 0 || BIND_adresa(server_VALUE, (struct 통신주소 *)&adresa, sizeof(adresa)) < 0 ||
        통신연결기다리기(server_VALUE, 4) < 0) return 1;
    if (prihvatiti_mrežna_veza(server_VALUE, 0, 0) != -1 || broj_greške != 11) return 2;
    int gost_VALUE = Create_završna_tačka(oblak_Porodica, tok_Mreža, 흐름전송규약);
    if (gost_VALUE < 0 || povezati_Mreža(gost_VALUE, (struct 통신주소 *)&adresa, sizeof(adresa)) < 0) return 3;
    int Spoji_se = prihvatiti_mrežna_veza(server_VALUE, 0, 0);
    if (Spoji_se < 0) return 4;
    unsigned char 보낼것[1500], RECEIVED_stavka[1500];
    for (int 수 = 0; 수 < 1500; 수++) 보낼것[수] = (unsigned char)수;
    int 보낸수 = 0;
    while (보낸수 < 1024) {
        int dužina_VALUE = pisati_fajl_podaci(gost_VALUE, 보낼것 + 보낸수, sizeof(보낼것) - 보낸수);
        if (dužina_VALUE <= 0) return 5;
        보낸수 += dužina_VALUE;
    }
    if (pisati_fajl_podaci(gost_VALUE, 보낼것, 1) != -1 || broj_greške != 11) return 6;
    /* 상대가 닫아도 이미 도착한 자료를 모두 읽은 ZAD_VALUE EOF가 된다. */
    zatvoriti_fajl(gost_VALUE);
    int RECEIVED_COUNT = 0;
    while (RECEIVED_COUNT < 보낸수) {
        int dužina_VALUE = 파일자료읽기(Spoji_se, RECEIVED_stavka + RECEIVED_COUNT, sizeof(RECEIVED_stavka) - RECEIVED_COUNT);
        if (dužina_VALUE <= 0) return 7;
        RECEIVED_COUNT += dužina_VALUE;
    }
    for (int 수 = 0; 수 < RECEIVED_COUNT; 수++) if (RECEIVED_stavka[수] != 보낼것[수]) return 8;
    if (파일자료읽기(Spoji_se, RECEIVED_stavka, 1) != 0) return 9;
    if (pisati_fajl_podaci(Spoji_se, 보낼것, 1) != -1 || broj_greške != 32) return 10;
    zatvoriti_fajl(Spoji_se); zatvoriti_fajl(server_VALUE);
    const char mjera[] = "C posix-kor 연결형 통신 PASS\n";
    pisati_fajl_podaci(1, mjera, sizeof(mjera) - 1);
    return 0;
}
