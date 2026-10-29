#include "통신규약.h"

int START_bruker_app(int Argumenter) {
    (void)Argumenter;
    struct sky_socket_e_post e_post = {0};
    e_post.e_post_serie = sky_serie;
    e_post.portnummer = 망차례짧은수(9260);
    e_post.Internett_adresse.e_post_VERDI = nettverk_heltall(tilbakekoblingsadresse);
    int server_VERDI = åpne_deltaker(sky_serie, strøm_nettverk, strøm_transportprotokoll);
    if (server_VERDI < 0 || BIND_e_post(server_VERDI, (struct socket_e_post *)&e_post, sizeof(e_post)) < 0 ||
        통신연결기다리기(server_VERDI, 4) < 0) return 1;
    if (godta_nettverkstilkobling(server_VERDI, 0, 0) != -1 || feilnummer != 11) return 2;
    int gjest_VERDI = åpne_deltaker(sky_serie, strøm_nettverk, strøm_transportprotokoll);
    if (gjest_VERDI < 0 || KOBLE_TIL_nettverk(gjest_VERDI, (struct socket_e_post *)&e_post, sizeof(e_post)) < 0) return 3;
    int Koble_til = godta_nettverkstilkobling(server_VERDI, 0, 0);
    if (Koble_til < 0) return 4;
    unsigned char 보낼것[1500], MOTTATT_AVKAST_vare[1500];
    for (int nummer = 0; nummer < 1500; nummer++) 보낼것[nummer] = (unsigned char)nummer;
    int 보낸수 = 0;
    while (보낸수 < 1024) {
        int lengde_VERDI = skrive_Fil_data(gjest_VERDI, 보낼것 + 보낸수, sizeof(보낼것) - 보낸수);
        if (lengde_VERDI <= 0) return 5;
        보낸수 += lengde_VERDI;
    }
    if (skrive_Fil_data(gjest_VERDI, 보낼것, 1) != -1 || feilnummer != 11) return 6;
    /* 상대가 닫아도 이미 도착한 자료를 모두 읽은 TILBAKE_VERDI EOF가 된다. */
    Lukk_Fil(gjest_VERDI);
    int MOTTATT_AVKAST_ANTALL = 0;
    while (MOTTATT_AVKAST_ANTALL < 보낸수) {
        int lengde_VERDI = 파일자료읽기(Koble_til, MOTTATT_AVKAST_vare + MOTTATT_AVKAST_ANTALL, sizeof(MOTTATT_AVKAST_vare) - MOTTATT_AVKAST_ANTALL);
        if (lengde_VERDI <= 0) return 7;
        MOTTATT_AVKAST_ANTALL += lengde_VERDI;
    }
    for (int nummer = 0; nummer < MOTTATT_AVKAST_ANTALL; nummer++) if (MOTTATT_AVKAST_vare[nummer] != 보낼것[nummer]) return 8;
    if (파일자료읽기(Koble_til, MOTTATT_AVKAST_vare, 1) != 0) return 9;
    if (skrive_Fil_data(Koble_til, 보낼것, 1) != -1 || feilnummer != 32) return 10;
    Lukk_Fil(Koble_til); Lukk_Fil(server_VERDI);
    const char KR[] = "C posix-kor 연결형 통신 PASS\n";
    skrive_Fil_data(1, KR, sizeof(KR) - 1);
    return 0;
}
