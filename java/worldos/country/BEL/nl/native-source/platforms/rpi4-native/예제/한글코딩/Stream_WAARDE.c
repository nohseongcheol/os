#include "통신규약.h"

int START_gebruiker_app(int argumenten) {
    (void)argumenten;
    struct mesh_socket_ADRES ADRES = {0};
    ADRES.ADRES_Gezin = mesh_Gezin;
    ADRES.poortnummer = 망차례짧은수(9260);
    ADRES.internetadres.ADRES_WAARDE = net_geheel_getal(loopback_adres);
    int server_WAARDE = maken_eindpunt(mesh_Gezin, Stream_net, Stream_transportprotocol);
    if (server_WAARDE < 0 || BIND_ADRES(server_WAARDE, (struct socket_ADRES *)&ADRES, sizeof(ADRES)) < 0 ||
        통신연결기다리기(server_WAARDE, 4) < 0) return 1;
    if (accepteren_netwerkverbinding(server_WAARDE, 0, 0) != -1 || foutnummer != 11) return 2;
    int gast_WAARDE = maken_eindpunt(mesh_Gezin, Stream_net, Stream_transportprotocol);
    if (gast_WAARDE < 0 || VERBINDEN_net(gast_WAARDE, (struct socket_ADRES *)&ADRES, sizeof(ADRES)) < 0) return 3;
    int Verbinden = accepteren_netwerkverbinding(server_WAARDE, 0, 0);
    if (Verbinden < 0) return 4;
    unsigned char 보낼것[1500], OPBRENGST_item[1500];
    for (int nummer = 0; nummer < 1500; nummer++) 보낼것[nummer] = (unsigned char)nummer;
    int 보낸수 = 0;
    while (보낸수 < 1024) {
        int tijdsduur_WAARDE = schrijven_Bestand_gegevens(gast_WAARDE, 보낼것 + 보낸수, sizeof(보낼것) - 보낸수);
        if (tijdsduur_WAARDE <= 0) return 5;
        보낸수 += tijdsduur_WAARDE;
    }
    if (schrijven_Bestand_gegevens(gast_WAARDE, 보낼것, 1) != -1 || foutnummer != 11) return 6;
    /* 상대가 닫아도 이미 도착한 자료를 모두 읽은 BACK_WAARDE EOF가 된다. */
    Sluiten_Bestand(gast_WAARDE);
    int OPBRENGST_AANTAL = 0;
    while (OPBRENGST_AANTAL < 보낸수) {
        int tijdsduur_WAARDE = 파일자료읽기(Verbinden, OPBRENGST_item + OPBRENGST_AANTAL, sizeof(OPBRENGST_item) - OPBRENGST_AANTAL);
        if (tijdsduur_WAARDE <= 0) return 7;
        OPBRENGST_AANTAL += tijdsduur_WAARDE;
    }
    for (int nummer = 0; nummer < OPBRENGST_AANTAL; nummer++) if (OPBRENGST_item[nummer] != 보낼것[nummer]) return 8;
    if (파일자료읽기(Verbinden, OPBRENGST_item, 1) != 0) return 9;
    if (schrijven_Bestand_gegevens(Verbinden, 보낼것, 1) != -1 || foutnummer != 32) return 10;
    Sluiten_Bestand(Verbinden); Sluiten_Bestand(server_WAARDE);
    const char resultaat[] = "C posix-kor 연결형 communicatie PASS\n";
    schrijven_Bestand_gegevens(1, resultaat, sizeof(resultaat) - 1);
    return 0;
}
