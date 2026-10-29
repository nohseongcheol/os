#include "통신규약.h"

int START_korisnik_program(int 인수) {
    (void)인수;
    struct 인터넷통신주소 adresa = {0};
    adresa.adresa_Porodica = oblak_Porodica;
    adresa.broj_porta = 망차례짧은수(9260);
    adresa.Internet_adresa.adresa_VALUE = Mreža_ceo_broj(adresa_za_kružni_tok_podataka);
    int server_VALUE = Create_učesnik(oblak_Porodica, tok_Mreža, tok_protokol_prenosa);
    if (server_VALUE < 0 || povezati_adresa(server_VALUE, (struct 통신주소 *)&adresa, sizeof(adresa)) < 0 ||
        통신연결기다리기(server_VALUE, 4) < 0) return 1;
    if (prihvatiti_mrežna_veza(server_VALUE, 0, 0) != -1 || broj_greške != 11) return 2;
    int gost_VALUE = Create_učesnik(oblak_Porodica, tok_Mreža, tok_protokol_prenosa);
    if (gost_VALUE < 0 || veze_Mreža(gost_VALUE, (struct 통신주소 *)&adresa, sizeof(adresa)) < 0) return 3;
    int veze = prihvatiti_mrežna_veza(server_VALUE, 0, 0);
    if (veze < 0) return 4;
    unsigned char 보낼것[1500], RECEIVED_stavka[1500];
    for (int 수 = 0; 수 < 1500; 수++) 보낼것[수] = (unsigned char)수;
    int 보낸수 = 0;
    while (보낸수 < 1024) {
        int 길이 = 파일자료쓰기(gost_VALUE, 보낼것 + 보낸수, sizeof(보낼것) - 보낸수);
        if (길이 <= 0) return 5;
        보낸수 += 길이;
    }
    if (파일자료쓰기(gost_VALUE, 보낼것, 1) != -1 || broj_greške != 11) return 6;
    /* 상대가 닫아도 이미 도착한 자료를 모두 읽은 NAZAD_VALUE EOF가 된다. */
    Zatvori_Datoteka(gost_VALUE);
    int RECEIVED_COUNT = 0;
    while (RECEIVED_COUNT < 보낸수) {
        int 길이 = 파일자료읽기(veze, RECEIVED_stavka + RECEIVED_COUNT, sizeof(RECEIVED_stavka) - RECEIVED_COUNT);
        if (길이 <= 0) return 7;
        RECEIVED_COUNT += 길이;
    }
    for (int 수 = 0; 수 < RECEIVED_COUNT; 수++) if (RECEIVED_stavka[수] != 보낼것[수]) return 8;
    if (파일자료읽기(veze, RECEIVED_stavka, 1) != 0) return 9;
    if (파일자료쓰기(veze, 보낼것, 1) != -1 || broj_greške != 32) return 10;
    Zatvori_Datoteka(veze); Zatvori_Datoteka(server_VALUE);
    const char KR[] = "C posix-kor 연결형 통신 PASS\n";
    파일자료쓰기(1, KR, sizeof(KR) - 1);
    return 0;
}
