#include "통신규약.h"
static mesh_socket_ADRES ADRES(unsigned poort_WAARDE) {
    mesh_socket_ADRES WAARDE = {}; WAARDE.ADRES_Gezin = mesh_Gezin;
    WAARDE.poortnummer = 망차례짧은수(poort_WAARDE); WAARDE.internetadres.ADRES_WAARDE = net_geheel_getal(loopback_adres); return WAARDE;
}
extern "C" int START_gebruiker_app(int) {
    int 보내는곳 = maken_eindpunt(mesh_Gezin, datagramsocket, 0);
    int 받는곳 = maken_eindpunt(mesh_Gezin, datagramsocket, datagram_protocol);
    if (보내는곳 < 0 || 받는곳 < 0) return 1;
    mesh_socket_ADRES 도착 = ADRES(7777), 출발 = ADRES(7778), 보낸주소 = {};
    socket_ADRES_tijdsduur_TYPE ADRES_tijdsduur = sizeof(보낸주소);
    if (BIND_ADRES(받는곳, (socket_ADRES *)&도착, sizeof(도착))) return 2;
    if (BIND_ADRES(보내는곳, (socket_ADRES *)&도착, sizeof(도착)) != -1 || foutnummer != 98) return 3;
    if (BIND_ADRES(보내는곳, (socket_ADRES *)&출발, sizeof(출발))) return 4;
    static const char Inhoud_WAARDE[] = "한글 UDP loopback 😀";
    char OPBRENGST_WAARDE[64] = {};
    if (e_mailen_datagram_gegevens(보내는곳, Inhoud_WAARDE, sizeof(Inhoud_WAARDE), 0, (socket_ADRES *)&도착, sizeof(도착)) != sizeof(Inhoud_WAARDE)) return 5;
    if (ontvangen_datagram_gegevens(받는곳, (void *)Inhoud_WAARDE, sizeof(Inhoud_WAARDE), 0, 0, 0) != -1 || foutnummer != 14) return 6;
    if (ontvangen_datagram_gegevens(받는곳, OPBRENGST_WAARDE, sizeof(OPBRENGST_WAARDE), 0, (socket_ADRES *)&보낸주소, &ADRES_tijdsduur) != sizeof(Inhoud_WAARDE)) return 7;
    if (ADRES_tijdsduur != sizeof(보낸주소) || 장치차례짧은수(보낸주소.poortnummer) != 7778 || mobiel_order_geheel_getal(보낸주소.internetadres.ADRES_WAARDE) != loopback_adres) return 8;
    for (unsigned 순번 = 0; 순번 < sizeof(Inhoud_WAARDE); 순번++) if (OPBRENGST_WAARDE[순번] != Inhoud_WAARDE[순번]) return 9;
    if (ontvangen_datagram_gegevens(받는곳, OPBRENGST_WAARDE, sizeof(OPBRENGST_WAARDE), 0, 0, 0) != -1 || foutnummer != 11) return 10;
    if (e_mailen_datagram_gegevens(받는곳, OPBRENGST_WAARDE, sizeof(Inhoud_WAARDE), 0, (socket_ADRES *)&보낸주소, sizeof(보낸주소)) != sizeof(Inhoud_WAARDE)) return 11;
    if (ontvangen_datagram_gegevens(보내는곳, OPBRENGST_WAARDE, 4, 0, 0, 0) != 4) return 12;
    if (ontvangen_datagram_gegevens(보내는곳, OPBRENGST_WAARDE, 4, 0, 0, 0) != -1 || foutnummer != 11) return 13;
    for (int 순번 = 0; 순번 < 4; 순번++) if (e_mailen_datagram_gegevens(보내는곳, Inhoud_WAARDE, sizeof(Inhoud_WAARDE), 0, (socket_ADRES *)&도착, sizeof(도착)) != sizeof(Inhoud_WAARDE)) return 14;
    if (e_mailen_datagram_gegevens(보내는곳, Inhoud_WAARDE, sizeof(Inhoud_WAARDE), 0, (socket_ADRES *)&도착, sizeof(도착)) != -1 || foutnummer != 11) return 15;
    for (int 순번 = 0; 순번 < 4; 순번++) if (ontvangen_datagram_gegevens(받는곳, OPBRENGST_WAARDE, sizeof(OPBRENGST_WAARDE), 0, 0, 0) != sizeof(Inhoud_WAARDE)) return 16;
    if (e_mailen_datagram_gegevens(보내는곳, 0, 0, 0, (socket_ADRES *)&도착, sizeof(도착)) != 0 ||
        ontvangen_datagram_gegevens(받는곳, 0, 0, 0, 0, 0) != 0) return 21;
    도착.internetadres.ADRES_WAARDE = net_geheel_getal(0x08080808);
    if (e_mailen_datagram_gegevens(보내는곳, Inhoud_WAARDE, sizeof(Inhoud_WAARDE), 0, (socket_ADRES *)&도착, sizeof(도착)) != -1 || foutnummer != 101) return 17;
    if (maken_eindpunt(mesh_Gezin, Stream_net, datagram_protocol) != -1 || foutnummer != 93) return 18;
    ADRES_tijdsduur = sizeof(보낸주소);
    if (통신주소읽기(받는곳, (socket_ADRES *)&보낸주소, &ADRES_tijdsduur) || 장치차례짧은수(보낸주소.poortnummer) != 7777) return 19;
    if (Sluiten_Bestand(받는곳) || Sluiten_Bestand(받는곳) != -1 || foutnummer != 9) return 20;
    // 보내는곳은 열어 둔다: Einde_app 시 프로세스별 socket 정리를 검사한다.
    static const char 완료[] = "EL0 UDP LOOPBACK PASS (external network unavailable)\n";
    schrijven_Bestand_gegevens(1, 완료, sizeof(완료) - 1);
    return 0;
}
