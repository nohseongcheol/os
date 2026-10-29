#include "통신규약.h"
static sky_socket_e_post e_post(unsigned port_VERDI) {
    sky_socket_e_post VERDI = {}; VERDI.e_post_serie = sky_serie;
    VERDI.portnummer = 망차례짧은수(port_VERDI); VERDI.Internett_adresse.e_post_VERDI = nettverk_heltall(tilbakekoblingsadresse); return VERDI;
}
extern "C" int START_bruker_app(int) {
    int 보내는곳 = åpne_deltaker(sky_serie, datagramsocket, 0);
    int 받는곳 = åpne_deltaker(sky_serie, datagramsocket, datagram_protokoll);
    if (보내는곳 < 0 || 받는곳 < 0) return 1;
    sky_socket_e_post 도착 = e_post(7777), 출발 = e_post(7778), 보낸주소 = {};
    socket_e_post_lengde_Type e_post_lengde = sizeof(보낸주소);
    if (BIND_e_post(받는곳, (socket_e_post *)&도착, sizeof(도착))) return 2;
    if (BIND_e_post(보내는곳, (socket_e_post *)&도착, sizeof(도착)) != -1 || feilnummer != 98) return 3;
    if (BIND_e_post(보내는곳, (socket_e_post *)&출발, sizeof(출발))) return 4;
    static const char Innhold_VERDI[] = "한글 UDP loopback 😀";
    char MOTTATT_AVKAST_VERDI[64] = {};
    if (sende_datagram_data(보내는곳, Innhold_VERDI, sizeof(Innhold_VERDI), 0, (socket_e_post *)&도착, sizeof(도착)) != sizeof(Innhold_VERDI)) return 5;
    if (motta_datagram_data(받는곳, (void *)Innhold_VERDI, sizeof(Innhold_VERDI), 0, 0, 0) != -1 || feilnummer != 14) return 6;
    if (motta_datagram_data(받는곳, MOTTATT_AVKAST_VERDI, sizeof(MOTTATT_AVKAST_VERDI), 0, (socket_e_post *)&보낸주소, &e_post_lengde) != sizeof(Innhold_VERDI)) return 7;
    if (e_post_lengde != sizeof(보낸주소) || 장치차례짧은수(보낸주소.portnummer) != 7778 || enhet_ordre_heltall(보낸주소.Internett_adresse.e_post_VERDI) != tilbakekoblingsadresse) return 8;
    for (unsigned 순번 = 0; 순번 < sizeof(Innhold_VERDI); 순번++) if (MOTTATT_AVKAST_VERDI[순번] != Innhold_VERDI[순번]) return 9;
    if (motta_datagram_data(받는곳, MOTTATT_AVKAST_VERDI, sizeof(MOTTATT_AVKAST_VERDI), 0, 0, 0) != -1 || feilnummer != 11) return 10;
    if (sende_datagram_data(받는곳, MOTTATT_AVKAST_VERDI, sizeof(Innhold_VERDI), 0, (socket_e_post *)&보낸주소, sizeof(보낸주소)) != sizeof(Innhold_VERDI)) return 11;
    if (motta_datagram_data(보내는곳, MOTTATT_AVKAST_VERDI, 4, 0, 0, 0) != 4) return 12;
    if (motta_datagram_data(보내는곳, MOTTATT_AVKAST_VERDI, 4, 0, 0, 0) != -1 || feilnummer != 11) return 13;
    for (int 순번 = 0; 순번 < 4; 순번++) if (sende_datagram_data(보내는곳, Innhold_VERDI, sizeof(Innhold_VERDI), 0, (socket_e_post *)&도착, sizeof(도착)) != sizeof(Innhold_VERDI)) return 14;
    if (sende_datagram_data(보내는곳, Innhold_VERDI, sizeof(Innhold_VERDI), 0, (socket_e_post *)&도착, sizeof(도착)) != -1 || feilnummer != 11) return 15;
    for (int 순번 = 0; 순번 < 4; 순번++) if (motta_datagram_data(받는곳, MOTTATT_AVKAST_VERDI, sizeof(MOTTATT_AVKAST_VERDI), 0, 0, 0) != sizeof(Innhold_VERDI)) return 16;
    if (sende_datagram_data(보내는곳, 0, 0, 0, (socket_e_post *)&도착, sizeof(도착)) != 0 ||
        motta_datagram_data(받는곳, 0, 0, 0, 0, 0) != 0) return 21;
    도착.Internett_adresse.e_post_VERDI = nettverk_heltall(0x08080808);
    if (sende_datagram_data(보내는곳, Innhold_VERDI, sizeof(Innhold_VERDI), 0, (socket_e_post *)&도착, sizeof(도착)) != -1 || feilnummer != 101) return 17;
    if (åpne_deltaker(sky_serie, strøm_nettverk, datagram_protokoll) != -1 || feilnummer != 93) return 18;
    e_post_lengde = sizeof(보낸주소);
    if (통신주소읽기(받는곳, (socket_e_post *)&보낸주소, &e_post_lengde) || 장치차례짧은수(보낸주소.portnummer) != 7777) return 19;
    if (Lukk_Fil(받는곳) || Lukk_Fil(받는곳) != -1 || feilnummer != 9) return 20;
    // 보내는곳은 열어 둔다: Utgang_app 시 프로세스별 socket 정리를 검사한다.
    static const char 완료[] = "EL0 UDP LOOPBACK PASS (external network unavailable)\n";
    skrive_Fil_data(1, 완료, sizeof(완료) - 1);
    return 0;
}
