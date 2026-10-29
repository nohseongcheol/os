#include "síť_ABI.h"

int START_uživatel_program(int argumenty) {
    (void)argumenty;
    struct cloud_soket_ODKAZ Adresa = {0};
    Adresa.ODKAZ_řada = cloud_řada;
    Adresa.číslo_portu = 망차례짧은수(9260);
    Adresa.internetová_adresa.ODKAZ_HODNOTA = síť_integer(adresa_zpětné_smyčky);
    int server_HODNOTA = Create_účastník(cloud_řada, tok_síť, tok_transportní_protokol);
    if (server_HODNOTA < 0 || vázat_ODKAZ(server_HODNOTA, (struct soket_ODKAZ *)&Adresa, sizeof(Adresa)) < 0 ||
        통신연결기다리기(server_HODNOTA, 4) < 0) return 1;
    if (přijmout_síťové_připojení(server_HODNOTA, 0, 0) != -1 || číslo_chyby != 11) return 2;
    int host_HODNOTA = Create_účastník(cloud_řada, tok_síť, tok_transportní_protokol);
    if (host_HODNOTA < 0 || spojit_síť(host_HODNOTA, (struct soket_ODKAZ *)&Adresa, sizeof(Adresa)) < 0) return 3;
    int Připojit = přijmout_síťové_připojení(server_HODNOTA, 0, 0);
    if (Připojit < 0) return 4;
    unsigned char 보낼것[1500], RECEIVED_zboží[1500];
    for (int číslo = 0; číslo < 1500; číslo++) 보낼것[číslo] = (unsigned char)číslo;
    int 보낸수 = 0;
    while (보낸수 < 1024) {
        int délka_HODNOTA = zápis_Soubor_data(host_HODNOTA, 보낼것 + 보낸수, sizeof(보낼것) - 보낸수);
        if (délka_HODNOTA <= 0) return 5;
        보낸수 += délka_HODNOTA;
    }
    if (zápis_Soubor_data(host_HODNOTA, 보낼것, 1) != -1 || číslo_chyby != 11) return 6;
    /* 상대가 닫아도 이미 도착한 자료를 모두 읽은 BACK_HODNOTA EOF가 된다. */
    Zavřít_Soubor(host_HODNOTA);
    int RECEIVED_POČET = 0;
    while (RECEIVED_POČET < 보낸수) {
        int délka_HODNOTA = 파일자료읽기(Připojit, RECEIVED_zboží + RECEIVED_POČET, sizeof(RECEIVED_zboží) - RECEIVED_POČET);
        if (délka_HODNOTA <= 0) return 7;
        RECEIVED_POČET += délka_HODNOTA;
    }
    for (int číslo = 0; číslo < RECEIVED_POČET; číslo++) if (RECEIVED_zboží[číslo] != 보낼것[číslo]) return 8;
    if (파일자료읽기(Připojit, RECEIVED_zboží, 1) != 0) return 9;
    if (zápis_Soubor_data(Připojit, 보낼것, 1) != -1 || číslo_chyby != 32) return 10;
    Zavřít_Soubor(Připojit); Zavřít_Soubor(server_HODNOTA);
    const char VÝSLEDEK[] = "C posix-kor 연결형 komunikace PASS\n";
    zápis_Soubor_data(1, VÝSLEDEK, sizeof(VÝSLEDEK) - 1);
    return 0;
}
