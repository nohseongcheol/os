#include "통신규약.h"

int START_používateľ_program(int Argumenty) {
    (void)Argumenty;
    struct cloud_soket_adresa adresa = {0};
    adresa.adresa_séria = cloud_séria;
    adresa.číslo_portu = 망차례짧은수(9260);
    adresa.internetová_adresa.adresa_VALUE = sieť_celé_číslo(adresa_systémovej_slučky);
    int server_VALUE = Create_účastník(cloud_séria, Stream_sieť, Stream_prenosový_protokol);
    if (server_VALUE < 0 || BIND_adresa(server_VALUE, (struct soket_adresa *)&adresa, sizeof(adresa)) < 0 ||
        통신연결기다리기(server_VALUE, 4) < 0) return 1;
    if (prijať_sieťové_pripojenie(server_VALUE, 0, 0) != -1 || chybové_číslo != 11) return 2;
    int hosť_VALUE = Create_účastník(cloud_séria, Stream_sieť, Stream_prenosový_protokol);
    if (hosť_VALUE < 0 || spojiť_sieť(hosť_VALUE, (struct soket_adresa *)&adresa, sizeof(adresa)) < 0) return 3;
    int Pripojiť = prijať_sieťové_pripojenie(server_VALUE, 0, 0);
    if (Pripojiť < 0) return 4;
    unsigned char 보낼것[1500], RECEIVED_položka[1500];
    for (int 수 = 0; 수 < 1500; 수++) 보낼것[수] = (unsigned char)수;
    int 보낸수 = 0;
    while (보낸수 < 1024) {
        int dĺžka_VALUE = zapísať_Súbor_údaje(hosť_VALUE, 보낼것 + 보낸수, sizeof(보낼것) - 보낸수);
        if (dĺžka_VALUE <= 0) return 5;
        보낸수 += dĺžka_VALUE;
    }
    if (zapísať_Súbor_údaje(hosť_VALUE, 보낼것, 1) != -1 || chybové_číslo != 11) return 6;
    /* 상대가 닫아도 이미 도착한 자료를 모두 읽은 BACK_VALUE EOF가 된다. */
    Zavrieť_Súbor(hosť_VALUE);
    int RECEIVED_COUNT = 0;
    while (RECEIVED_COUNT < 보낸수) {
        int dĺžka_VALUE = 파일자료읽기(Pripojiť, RECEIVED_položka + RECEIVED_COUNT, sizeof(RECEIVED_položka) - RECEIVED_COUNT);
        if (dĺžka_VALUE <= 0) return 7;
        RECEIVED_COUNT += dĺžka_VALUE;
    }
    for (int 수 = 0; 수 < RECEIVED_COUNT; 수++) if (RECEIVED_položka[수] != 보낼것[수]) return 8;
    if (파일자료읽기(Pripojiť, RECEIVED_položka, 1) != 0) return 9;
    if (zapísať_Súbor_údaje(Pripojiť, 보낼것, 1) != -1 || chybové_číslo != 32) return 10;
    Zavrieť_Súbor(Pripojiť); Zavrieť_Súbor(server_VALUE);
    const char KR[] = "C posix-kor 연결형 통신 PASS\n";
    zapísať_Súbor_údaje(1, KR, sizeof(KR) - 1);
    return 0;
}
