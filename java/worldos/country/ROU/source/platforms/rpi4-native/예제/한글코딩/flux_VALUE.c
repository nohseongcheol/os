#include "통신규약.h"

int buta_utilizator_program(int Argumente) {
    (void)Argumente;
    struct 인터넷통신주소 adresa = {0};
    adresa.adresa_Familie = cloud_Familie;
    adresa.număr_port = 망차례짧은수(9260);
    adresa.adresă_internet.adresa_VALUE = rețea_întreg(adresă_de_întoarcere_în_buclă);
    int server_VALUE = crea_participant(cloud_Familie, flux_rețea, flux_protocol_de_transport);
    if (server_VALUE < 0 || BIND_adresa(server_VALUE, (struct 통신주소 *)&adresa, sizeof(adresa)) < 0 ||
        통신연결기다리기(server_VALUE, 4) < 0) return 1;
    if (accepta_conexiune_rețea(server_VALUE, 0, 0) != -1 || număr_de_eroare != 11) return 2;
    int invitat_VALUE = crea_participant(cloud_Familie, flux_rețea, flux_protocol_de_transport);
    if (invitat_VALUE < 0 || conecta_rețea(invitat_VALUE, (struct 통신주소 *)&adresa, sizeof(adresa)) < 0) return 3;
    int Conectează = accepta_conexiune_rețea(server_VALUE, 0, 0);
    if (Conectează < 0) return 4;
    unsigned char 보낼것[1500], RECEIVED_element[1500];
    for (int 수 = 0; 수 < 1500; 수++) 보낼것[수] = (unsigned char)수;
    int 보낸수 = 0;
    while (보낸수 < 1024) {
        int lungime_VALUE = scriere_Fișier_date(invitat_VALUE, 보낼것 + 보낸수, sizeof(보낼것) - 보낸수);
        if (lungime_VALUE <= 0) return 5;
        보낸수 += lungime_VALUE;
    }
    if (scriere_Fișier_date(invitat_VALUE, 보낼것, 1) != -1 || număr_de_eroare != 11) return 6;
    /* 상대가 닫아도 이미 도착한 자료를 모두 읽은 ÎNAPOI_VALUE EOF가 된다. */
    închide_Fișier(invitat_VALUE);
    int RECEIVED_COUNT = 0;
    while (RECEIVED_COUNT < 보낸수) {
        int lungime_VALUE = 파일자료읽기(Conectează, RECEIVED_element + RECEIVED_COUNT, sizeof(RECEIVED_element) - RECEIVED_COUNT);
        if (lungime_VALUE <= 0) return 7;
        RECEIVED_COUNT += lungime_VALUE;
    }
    for (int 수 = 0; 수 < RECEIVED_COUNT; 수++) if (RECEIVED_element[수] != 보낼것[수]) return 8;
    if (파일자료읽기(Conectează, RECEIVED_element, 1) != 0) return 9;
    if (scriere_Fișier_date(Conectează, 보낼것, 1) != -1 || număr_de_eroare != 32) return 10;
    închide_Fișier(Conectează); închide_Fișier(server_VALUE);
    const char KR[] = "C posix-kor 연결형 통신 PASS\n";
    scriere_Fișier_date(1, KR, sizeof(KR) - 1);
    return 0;
}
