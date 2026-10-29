#include "통신규약.h"

int Start_uporabnik_aplikacija(int Argumenti) {
    (void)Argumenti;
    struct oblak_vtičnica_naslov naslov = {0};
    naslov.naslov_Družina = oblak_Družina;
    naslov.številka_vrat = 망차례짧은수(9260);
    naslov.internetni_račun.naslov_VALUE = mreža_celo_število(naslov_povratne_zanke);
    int strežnik_VALUE = Ustvari_končna_točka(oblak_Družina, tok_mreža, tok_protokol_prenosa);
    if (strežnik_VALUE < 0 || BIND_naslov(strežnik_VALUE, (struct vtičnica_naslov *)&naslov, sizeof(naslov)) < 0 ||
        통신연결기다리기(strežnik_VALUE, 4) < 0) return 1;
    if (sprejeti_omrežna_povezava(strežnik_VALUE, 0, 0) != -1 || številka_napake != 11) return 2;
    int gost_VALUE = Ustvari_končna_točka(oblak_Družina, tok_mreža, tok_protokol_prenosa);
    if (gost_VALUE < 0 || POVEŽI_mreža(gost_VALUE, (struct vtičnica_naslov *)&naslov, sizeof(naslov)) < 0) return 3;
    int Poveži = sprejeti_omrežna_povezava(strežnik_VALUE, 0, 0);
    if (Poveži < 0) return 4;
    unsigned char 보낼것[1500], RECEIVED_element[1500];
    for (int 수 = 0; 수 < 1500; 수++) 보낼것[수] = (unsigned char)수;
    int 보낸수 = 0;
    while (보낸수 < 1024) {
        int 길이 = pisati_Datoteka_podatki(gost_VALUE, 보낼것 + 보낸수, sizeof(보낼것) - 보낸수);
        if (길이 <= 0) return 5;
        보낸수 += 길이;
    }
    if (pisati_Datoteka_podatki(gost_VALUE, 보낼것, 1) != -1 || številka_napake != 11) return 6;
    /* 상대가 닫아도 이미 도착한 자료를 모두 읽은 ZAJ_VALUE EOF가 된다. */
    Zapri_Datoteka(gost_VALUE);
    int RECEIVED_COUNT = 0;
    while (RECEIVED_COUNT < 보낸수) {
        int 길이 = 파일자료읽기(Poveži, RECEIVED_element + RECEIVED_COUNT, sizeof(RECEIVED_element) - RECEIVED_COUNT);
        if (길이 <= 0) return 7;
        RECEIVED_COUNT += 길이;
    }
    for (int 수 = 0; 수 < RECEIVED_COUNT; 수++) if (RECEIVED_element[수] != 보낼것[수]) return 8;
    if (파일자료읽기(Poveži, RECEIVED_element, 1) != 0) return 9;
    if (pisati_Datoteka_podatki(Poveži, 보낼것, 1) != -1 || številka_napake != 32) return 10;
    Zapri_Datoteka(Poveži); Zapri_Datoteka(strežnik_VALUE);
    const char REZULTAT[] = "C posix-kor 연결형 통신 PASS\n";
    pisati_Datoteka_podatki(1, REZULTAT, sizeof(REZULTAT) - 1);
    return 0;
}
