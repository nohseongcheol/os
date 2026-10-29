#include "통신규약.h"
static nät_socket_ADRESS Adress(unsigned port_värde) {
    nät_socket_ADRESS värde = {}; värde.ADRESS_serie = nät_serie;
    värde.portnummer = 망차례짧은수(port_värde); värde.Internetadress.ADRESS_värde = nätverk_heltal(loopback_adress); return värde;
}
extern "C" int START_användare_app(int) {
    int 보내는곳 = Skapa_deltagare(nät_serie, datagramsocket, 0);
    int 받는곳 = Skapa_deltagare(nät_serie, datagramsocket, datagram_protokoll);
    if (보내는곳 < 0 || 받는곳 < 0) return 1;
    nät_socket_ADRESS 도착 = Adress(7777), 출발 = Adress(7778), 보낸주소 = {};
    socket_ADRESS_längd_Typ ADRESS_längd = sizeof(보낸주소);
    if (BIND_ADRESS(받는곳, (socket_ADRESS *)&도착, sizeof(도착))) return 2;
    if (BIND_ADRESS(보내는곳, (socket_ADRESS *)&도착, sizeof(도착)) != -1 || felnummer != 98) return 3;
    if (BIND_ADRESS(보내는곳, (socket_ADRESS *)&출발, sizeof(출발))) return 4;
    static const char Innehåll_värde[] = "한글 UDP loopback 😀";
    char BELOPP_värde[64] = {};
    if (skicka_datagram_data(보내는곳, Innehåll_värde, sizeof(Innehåll_värde), 0, (socket_ADRESS *)&도착, sizeof(도착)) != sizeof(Innehåll_värde)) return 5;
    if (få_datagram_data(받는곳, (void *)Innehåll_värde, sizeof(Innehåll_värde), 0, 0, 0) != -1 || felnummer != 14) return 6;
    if (få_datagram_data(받는곳, BELOPP_värde, sizeof(BELOPP_värde), 0, (socket_ADRESS *)&보낸주소, &ADRESS_längd) != sizeof(Innehåll_värde)) return 7;
    if (ADRESS_längd != sizeof(보낸주소) || 장치차례짧은수(보낸주소.portnummer) != 7778 || enhet_order_heltal(보낸주소.Internetadress.ADRESS_värde) != loopback_adress) return 8;
    for (unsigned 순번 = 0; 순번 < sizeof(Innehåll_värde); 순번++) if (BELOPP_värde[순번] != Innehåll_värde[순번]) return 9;
    if (få_datagram_data(받는곳, BELOPP_värde, sizeof(BELOPP_värde), 0, 0, 0) != -1 || felnummer != 11) return 10;
    if (skicka_datagram_data(받는곳, BELOPP_värde, sizeof(Innehåll_värde), 0, (socket_ADRESS *)&보낸주소, sizeof(보낸주소)) != sizeof(Innehåll_värde)) return 11;
    if (få_datagram_data(보내는곳, BELOPP_värde, 4, 0, 0, 0) != 4) return 12;
    if (få_datagram_data(보내는곳, BELOPP_värde, 4, 0, 0, 0) != -1 || felnummer != 11) return 13;
    for (int 순번 = 0; 순번 < 4; 순번++) if (skicka_datagram_data(보내는곳, Innehåll_värde, sizeof(Innehåll_värde), 0, (socket_ADRESS *)&도착, sizeof(도착)) != sizeof(Innehåll_värde)) return 14;
    if (skicka_datagram_data(보내는곳, Innehåll_värde, sizeof(Innehåll_värde), 0, (socket_ADRESS *)&도착, sizeof(도착)) != -1 || felnummer != 11) return 15;
    for (int 순번 = 0; 순번 < 4; 순번++) if (få_datagram_data(받는곳, BELOPP_värde, sizeof(BELOPP_värde), 0, 0, 0) != sizeof(Innehåll_värde)) return 16;
    if (skicka_datagram_data(보내는곳, 0, 0, 0, (socket_ADRESS *)&도착, sizeof(도착)) != 0 ||
        få_datagram_data(받는곳, 0, 0, 0, 0, 0) != 0) return 21;
    도착.Internetadress.ADRESS_värde = nätverk_heltal(0x08080808);
    if (skicka_datagram_data(보내는곳, Innehåll_värde, sizeof(Innehåll_värde), 0, (socket_ADRESS *)&도착, sizeof(도착)) != -1 || felnummer != 101) return 17;
    if (Skapa_deltagare(nät_serie, flöde_nätverk, datagram_protokoll) != -1 || felnummer != 93) return 18;
    ADRESS_längd = sizeof(보낸주소);
    if (läsa_socket_ADRESS(받는곳, (socket_ADRESS *)&보낸주소, &ADRESS_längd) || 장치차례짧은수(보낸주소.portnummer) != 7777) return 19;
    if (Stäng_fil(받는곳) || Stäng_fil(받는곳) != -1 || felnummer != 9) return 20;
    // 보내는곳은 열어 둔다: Utgång_app 시 프로세스별 socket 정리를 검사한다.
    static const char 완료[] = "EL0 UDP LOOPBACK PASS (external network unavailable)\n";
    skriva_fil_data(1, 완료, sizeof(완료) - 1);
    return 0;
}
