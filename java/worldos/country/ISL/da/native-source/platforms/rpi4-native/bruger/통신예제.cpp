#include "통신규약.h"
static net_socket_mail mail(unsigned port_VÆRDI) {
    net_socket_mail VÆRDI = {}; VÆRDI.mail_serie = net_serie;
    VÆRDI.portnummer = 망차례짧은수(port_VÆRDI); VÆRDI.internetadresse.mail_VÆRDI = netværk_heltal(tilbagekoblingsadresse); return VÆRDI;
}
extern "C" int START_bruger_app(int) {
    int 보내는곳 = åbne_slutpunkt(net_serie, datagram_socket, 0);
    int 받는곳 = åbne_slutpunkt(net_serie, datagram_socket, datagram_protokol);
    if (보내는곳 < 0 || 받는곳 < 0) return 1;
    net_socket_mail 도착 = mail(7777), 출발 = mail(7778), 보낸주소 = {};
    socket_mail_varighed_Type mail_varighed = sizeof(보낸주소);
    if (BIND_mail(받는곳, (socket_mail *)&도착, sizeof(도착))) return 2;
    if (BIND_mail(보내는곳, (socket_mail *)&도착, sizeof(도착)) != -1 || fejlnummer != 98) return 3;
    if (BIND_mail(보내는곳, (socket_mail *)&출발, sizeof(출발))) return 4;
    static const char Indhold_VÆRDI[] = "한글 UDP loopback 😀";
    char MODTAGET_VED_UDLØB_VÆRDI[64] = {};
    if (maile_datagram_data(보내는곳, Indhold_VÆRDI, sizeof(Indhold_VÆRDI), 0, (socket_mail *)&도착, sizeof(도착)) != sizeof(Indhold_VÆRDI)) return 5;
    if (modtage_datagram_data(받는곳, (void *)Indhold_VÆRDI, sizeof(Indhold_VÆRDI), 0, 0, 0) != -1 || fejlnummer != 14) return 6;
    if (modtage_datagram_data(받는곳, MODTAGET_VED_UDLØB_VÆRDI, sizeof(MODTAGET_VED_UDLØB_VÆRDI), 0, (socket_mail *)&보낸주소, &mail_varighed) != sizeof(Indhold_VÆRDI)) return 7;
    if (mail_varighed != sizeof(보낸주소) || 장치차례짧은수(보낸주소.portnummer) != 7778 || enhed_ordre_heltal(보낸주소.internetadresse.mail_VÆRDI) != tilbagekoblingsadresse) return 8;
    for (unsigned 순번 = 0; 순번 < sizeof(Indhold_VÆRDI); 순번++) if (MODTAGET_VED_UDLØB_VÆRDI[순번] != Indhold_VÆRDI[순번]) return 9;
    if (modtage_datagram_data(받는곳, MODTAGET_VED_UDLØB_VÆRDI, sizeof(MODTAGET_VED_UDLØB_VÆRDI), 0, 0, 0) != -1 || fejlnummer != 11) return 10;
    if (maile_datagram_data(받는곳, MODTAGET_VED_UDLØB_VÆRDI, sizeof(Indhold_VÆRDI), 0, (socket_mail *)&보낸주소, sizeof(보낸주소)) != sizeof(Indhold_VÆRDI)) return 11;
    if (modtage_datagram_data(보내는곳, MODTAGET_VED_UDLØB_VÆRDI, 4, 0, 0, 0) != 4) return 12;
    if (modtage_datagram_data(보내는곳, MODTAGET_VED_UDLØB_VÆRDI, 4, 0, 0, 0) != -1 || fejlnummer != 11) return 13;
    for (int 순번 = 0; 순번 < 4; 순번++) if (maile_datagram_data(보내는곳, Indhold_VÆRDI, sizeof(Indhold_VÆRDI), 0, (socket_mail *)&도착, sizeof(도착)) != sizeof(Indhold_VÆRDI)) return 14;
    if (maile_datagram_data(보내는곳, Indhold_VÆRDI, sizeof(Indhold_VÆRDI), 0, (socket_mail *)&도착, sizeof(도착)) != -1 || fejlnummer != 11) return 15;
    for (int 순번 = 0; 순번 < 4; 순번++) if (modtage_datagram_data(받는곳, MODTAGET_VED_UDLØB_VÆRDI, sizeof(MODTAGET_VED_UDLØB_VÆRDI), 0, 0, 0) != sizeof(Indhold_VÆRDI)) return 16;
    if (maile_datagram_data(보내는곳, 0, 0, 0, (socket_mail *)&도착, sizeof(도착)) != 0 ||
        modtage_datagram_data(받는곳, 0, 0, 0, 0, 0) != 0) return 21;
    도착.internetadresse.mail_VÆRDI = netværk_heltal(0x08080808);
    if (maile_datagram_data(보내는곳, Indhold_VÆRDI, sizeof(Indhold_VÆRDI), 0, (socket_mail *)&도착, sizeof(도착)) != -1 || fejlnummer != 101) return 17;
    if (åbne_slutpunkt(net_serie, strøm_netværk, datagram_protokol) != -1 || fejlnummer != 93) return 18;
    mail_varighed = sizeof(보낸주소);
    if (통신주소읽기(받는곳, (socket_mail *)&보낸주소, &mail_varighed) || 장치차례짧은수(보낸주소.portnummer) != 7777) return 19;
    if (Luk_fil(받는곳) || Luk_fil(받는곳) != -1 || fejlnummer != 9) return 20;
    // 보내는곳은 열어 둔다: Afslut_app 시 프로세스별 socket 정리를 검사한다.
    static const char 완료[] = "EL0 UDP LOOPBACK PASS (external network unavailable)\n";
    skrive_fil_data(1, 완료, sizeof(완료) - 1);
    return 0;
}
