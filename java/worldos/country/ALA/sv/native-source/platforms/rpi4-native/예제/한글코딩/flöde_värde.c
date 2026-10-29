#include "통신규약.h"

int START_användare_app(int argument) {
    (void)argument;
    struct nät_socket_ADRESS Adress = {0};
    Adress.ADRESS_serie = nät_serie;
    Adress.portnummer = 망차례짧은수(9260);
    Adress.Internetadress.ADRESS_värde = nätverk_heltal(loopback_adress);
    int server_värde = Skapa_deltagare(nät_serie, flöde_nätverk, flöde_transportprotokoll);
    if (server_värde < 0 || BIND_ADRESS(server_värde, (struct socket_ADRESS *)&Adress, sizeof(Adress)) < 0 ||
        통신연결기다리기(server_värde, 4) < 0) return 1;
    if (acceptera_nätverksanslutning(server_värde, 0, 0) != -1 || felnummer != 11) return 2;
    int gäst_värde = Skapa_deltagare(nät_serie, flöde_nätverk, flöde_transportprotokoll);
    if (gäst_värde < 0 || ANSLUT_nätverk(gäst_värde, (struct socket_ADRESS *)&Adress, sizeof(Adress)) < 0) return 3;
    int Anslut = acceptera_nätverksanslutning(server_värde, 0, 0);
    if (Anslut < 0) return 4;
    unsigned char 보낼것[1500], BELOPP_objekt[1500];
    for (int nummer = 0; nummer < 1500; nummer++) 보낼것[nummer] = (unsigned char)nummer;
    int 보낸수 = 0;
    while (보낸수 < 1024) {
        int längd_värde = skriva_fil_data(gäst_värde, 보낼것 + 보낸수, sizeof(보낼것) - 보낸수);
        if (längd_värde <= 0) return 5;
        보낸수 += längd_värde;
    }
    if (skriva_fil_data(gäst_värde, 보낼것, 1) != -1 || felnummer != 11) return 6;
    /* 상대가 닫아도 이미 도착한 자료를 모두 읽은 BACK_värde EOF가 된다. */
    Stäng_fil(gäst_värde);
    int BELOPP_ANTAL = 0;
    while (BELOPP_ANTAL < 보낸수) {
        int längd_värde = läsa_fil_data(Anslut, BELOPP_objekt + BELOPP_ANTAL, sizeof(BELOPP_objekt) - BELOPP_ANTAL);
        if (längd_värde <= 0) return 7;
        BELOPP_ANTAL += längd_värde;
    }
    for (int nummer = 0; nummer < BELOPP_ANTAL; nummer++) if (BELOPP_objekt[nummer] != 보낼것[nummer]) return 8;
    if (läsa_fil_data(Anslut, BELOPP_objekt, 1) != 0) return 9;
    if (skriva_fil_data(Anslut, 보낼것, 1) != -1 || felnummer != 32) return 10;
    Stäng_fil(Anslut); Stäng_fil(server_värde);
    const char RESULTAT[] = "C posix-kor 연결형 kommunikation PASS\n";
    skriva_fil_data(1, RESULTAT, sizeof(RESULTAT) - 1);
    return 0;
}
